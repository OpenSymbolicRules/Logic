#!/usr/bin/env python3
"""Verify the propositional soundness of Logic rules, tests, and inferences."""

from __future__ import annotations

import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


Expression = Any
WILDCARD = re.compile(r"^[A-Za-z][A-Za-z0-9]*_(?:integer|rational|positive|negative|complex)?$")
SEQUENCE_WILDCARD = re.compile(r"^[A-Za-z][A-Za-z0-9]*_{2,3}$")
CONSTANTS = {"True": True, "False": False}
OPERATORS = {
    "And",
    "Or",
    "Not",
    "Implies",
    "Equivalent",
    "Nand",
    "Nor",
    "Xor",
    "Xnor",
    "Forall",
    "Exists",
}


def evaluate(expression: Expression, environment: dict[str, bool]) -> bool:
    """Evaluate a supported propositional OSR expression over Boolean values."""
    if isinstance(expression, bool):
        return expression
    if isinstance(expression, str):
        if expression in CONSTANTS:
            return CONSTANTS[expression]
        try:
            return environment[expression]
        except KeyError as error:
            raise ValueError(f"Unbound proposition: {expression}") from error
    if not isinstance(expression, list) or not expression:
        raise ValueError(f"Unsupported expression: {expression!r}")

    head, *arguments = expression
    if head in {"Forall", "Exists"}:
        if len(arguments) != 2 or not isinstance(arguments[0], list):
            raise ValueError(f"Malformed quantifier: {expression!r}")
        variables, body = arguments
        outcomes = []
        for values in itertools.product((False, True), repeat=len(variables)):
            scoped_environment = environment | dict(zip(variables, values, strict=True))
            outcomes.append(evaluate(body, scoped_environment))
        return all(outcomes) if head == "Forall" else any(outcomes)

    values = [evaluate(argument, environment) for argument in arguments]
    if head == "And":
        return all(values)
    if head == "Or":
        return any(values)
    if head == "Not" and len(values) == 1:
        return not values[0]
    if head == "Implies" and len(values) == 2:
        return not values[0] or values[1]
    if head == "Equivalent" and len(values) == 2:
        return values[0] == values[1]
    if head == "Nand" and len(values) == 2:
        return not all(values)
    if head == "Nor" and len(values) == 2:
        return not any(values)
    if head == "Xor" and len(values) == 2:
        return values[0] != values[1]
    if head == "Xnor" and len(values) == 2:
        return values[0] == values[1]
    raise ValueError(f"Unsupported connective or arity: {expression!r}")


def instantiate(expression: Expression, environment: dict[str, bool]) -> Expression:
    """Replace scalar and binder-list wildcards with concrete Boolean data."""
    if isinstance(expression, str):
        if WILDCARD.fullmatch(expression):
            return environment[expression]
        return expression
    if not isinstance(expression, list):
        return expression
    if len(expression) == 1 and isinstance(expression[0], str) and SEQUENCE_WILDCARD.fullmatch(expression[0]):
        return ["x", "y"]
    return [instantiate(part, environment) for part in expression]


def bound_variables(expression: Expression) -> set[str]:
    """Return lexical variables occurring in quantifier binders."""
    if not isinstance(expression, list) or not expression:
        return set()
    if expression[0] in {"Forall", "Exists"} and len(expression) == 3:
        variables = expression[1]
        body = expression[2]
        return set(variables) | bound_variables(body)
    return set().union(*(bound_variables(part) for part in expression[1:]))


def propositions(expression: Expression) -> set[str]:
    """Collect free atomic propositions or wildcards in an expression."""
    if isinstance(expression, str):
        return set() if expression in CONSTANTS else {expression}
    if not isinstance(expression, list) or not expression:
        return set()
    if expression[0] in {"Forall", "Exists"} and len(expression) == 3:
        return propositions(expression[2]) - set(expression[1])
    return set().union(*(propositions(part) for part in expression[1:]))


def valuations(names: Iterable[str]) -> Iterable[dict[str, bool]]:
    names = sorted(set(names))
    for values in itertools.product((False, True), repeat=len(names)):
        yield dict(zip(names, values, strict=True))


def require_equivalent(left: Expression, right: Expression, context: str) -> None:
    """Raise when two expressions differ under any Boolean valuation."""
    for environment in valuations(propositions(left) | propositions(right)):
        if evaluate(left, environment) != evaluate(right, environment):
            raise AssertionError(f"{context} is not equivalent for {environment}")


def verify_rule_file(path: Path) -> int:
    document = json.loads(path.read_text())
    checked = 0
    for rule in document["rules"]:
        wildcard_names = {
            name
            for name in propositions(rule["pattern"]) | propositions(rule["result"])
            if WILDCARD.fullmatch(name)
        }
        for environment in valuations(wildcard_names):
            pattern = instantiate(rule["pattern"], environment)
            result = instantiate(rule["result"], environment)
            require_equivalent(pattern, result, f"{path}:{rule['id']}")
        checked += 1
    return checked


def verify_test_file(path: Path) -> int:
    document = json.loads(path.read_text())
    for test in document["tests"]:
        require_equivalent(test["expression"], test["expected_result"], f"{path}:{test['id']}")
    return len(document["tests"])


def verify_inference_file(path: Path) -> int:
    document = json.loads(path.read_text())
    for inference in document["inferences"]:
        wildcard_names = set().union(*(propositions(premise) for premise in inference["premises"]))
        wildcard_names |= propositions(inference["conclusion"])
        wildcard_names = {name for name in wildcard_names if WILDCARD.fullmatch(name)}
        for environment in valuations(wildcard_names):
            premises = [instantiate(premise, environment) for premise in inference["premises"]]
            conclusion = instantiate(inference["conclusion"], environment)
            names = set().union(*(propositions(premise) for premise in premises)) | propositions(conclusion)
            for valuation in valuations(names):
                if all(evaluate(premise, valuation) for premise in premises) and not evaluate(conclusion, valuation):
                    raise AssertionError(f"{path}:{inference['id']} is unsound for {valuation}")
    return len(document["inferences"])


def verify_inference_test_file(path: Path) -> int:
    document = json.loads(path.read_text())
    for test in document["tests"]:
        premises = test["premises"]
        conclusion = test["expected_conclusion"]
        names = set().union(*(propositions(premise) for premise in premises)) | propositions(conclusion)
        for valuation in valuations(names):
            if all(evaluate(premise, valuation) for premise in premises) and not evaluate(conclusion, valuation):
                raise AssertionError(f"{path}:{test['id']} is not entailed for {valuation}")
    return len(document["tests"])


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    counts = {
        "rules": sum(verify_rule_file(path) for path in sorted((root / "rules").rglob("*.json")) if path.name != "meta.json"),
        "tests": sum(verify_test_file(path) for path in sorted((root / "tests").rglob("*.json"))),
        "inferences": sum(verify_inference_file(path) for path in sorted((root / "inferences").rglob("*.json"))),
        "inference tests": sum(verify_inference_test_file(path) for path in sorted((root / "inference-tests").rglob("*.json"))),
    }
    print(", ".join(f"{count} {name}" for name, count in counts.items()) + " verified semantically")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error
