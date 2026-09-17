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
# The concrete binder a sequence wildcard stands for while checking a rule.
BOUND_VARIABLES = ["x", "y"]
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


def instantiate_binders(expression: Expression) -> Expression:
    """Replace a sequence wildcard standing for a binder with a concrete list."""
    if not isinstance(expression, list):
        return expression
    if len(expression) == 1 and isinstance(expression[0], str) and SEQUENCE_WILDCARD.fullmatch(expression[0]):
        return list(BOUND_VARIABLES)
    return [instantiate_binders(part) for part in expression]


def instantiate(expression: Expression, environment: dict[str, Expression]) -> Expression:
    """Replace each wildcard with the expression the environment assigns it."""
    if isinstance(expression, str):
        if WILDCARD.fullmatch(expression):
            return environment[expression]
        return expression
    if not isinstance(expression, list):
        return expression
    return [instantiate(part, environment) for part in expression]


def wildcard_candidates(name: str, bound: Iterable[str]) -> list[Expression]:
    """Return the expressions a scalar wildcard is checked against.

    A wildcard instantiated only with constants can never depend on a bound
    variable, which would verify every quantifier rule vacuously. The candidates
    therefore include each bound variable and its negation, alongside a fresh
    atom standing for a body independent of the binder. The fresh atom also
    subsumes the two Boolean constants, because an equivalence is then checked
    under every valuation of that atom.
    """
    candidates: list[Expression] = [f"atom{abs(hash(name)) % 997}"]
    for variable in bound:
        candidates.append(variable)
        candidates.append(["Not", variable])
    return candidates


def constraint_holds(constraint: Expression, environment: dict[str, Expression]) -> bool:
    """Decide a rule's side condition for one instantiation.

    A constraint this verifier cannot model raises, because skipping it silently
    would let the verifier report a rule sound that it never checked.
    """
    if not isinstance(constraint, list) or not constraint or not isinstance(constraint[0], str):
        raise ValueError(f"Malformed constraint: {constraint!r}")
    head, *arguments = constraint

    if head == "FreeQ":
        if len(arguments) != 2:
            raise ValueError(f"FreeQ takes an expression and a variable: {constraint!r}")
        expression, variables = (instantiate(argument, environment) for argument in arguments)
        if not isinstance(variables, list):
            variables = [variables]
        free = propositions(expression)
        return all(variable not in free for variable in variables)

    raise ValueError(f"Unsupported constraint: {constraint!r}")


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


def binder_references(expression: Expression) -> dict[str, list[str]]:
    """Map the reference spelling of each binder sequence to the list it names.

    A binder declared `xs__` is referred to as `xs_` in a side condition: the
    reference names the one value the binder captured, which is the whole
    variable list.
    """
    references: dict[str, list[str]] = {}
    if not isinstance(expression, list) or not expression:
        return references
    if expression[0] in {"Forall", "Exists"} and len(expression) == 3:
        variables = expression[1]
        if (
            isinstance(variables, list)
            and len(variables) == 1
            and isinstance(variables[0], str)
            and SEQUENCE_WILDCARD.fullmatch(variables[0])
        ):
            references[variables[0].rstrip("_") + "_"] = list(BOUND_VARIABLES)
        references |= binder_references(expression[2])
        return references
    for part in expression[1:]:
        references |= binder_references(part)
    return references


def scalar_wildcards(expression: Expression) -> set[str]:
    """Collect the scalar wildcards of an expression, including in constraints."""
    if isinstance(expression, str):
        return {expression} if WILDCARD.fullmatch(expression) else set()
    if not isinstance(expression, list):
        return set()
    return set().union(*(scalar_wildcards(part) for part in expression), set())


def verify_rule(rule: dict[str, Any], context: str) -> int:
    """Check one rule over every instantiation its side conditions admit.

    Returns the number of instantiations checked, which is zero when the side
    conditions admit none.
    """
    references = binder_references(rule["pattern"])
    pattern = instantiate_binders(rule["pattern"])
    result = instantiate_binders(rule["result"])
    constraints = [instantiate_binders(constraint) for constraint in rule.get("constraints", [])]

    bound = sorted(bound_variables(pattern))
    names = sorted(
        (scalar_wildcards(pattern) | scalar_wildcards(result) | scalar_wildcards(constraints))
        - references.keys()
    )
    candidates = [wildcard_candidates(name, bound) for name in names]

    checked = 0
    for choice in itertools.product(*candidates):
        environment: dict[str, Expression] = dict(references)
        environment |= dict(zip(names, choice, strict=True))
        if not all(constraint_holds(constraint, environment) for constraint in constraints):
            continue
        require_equivalent(
            instantiate(pattern, environment),
            instantiate(result, environment),
            f"{context}:{rule['id']}",
        )
        checked += 1
    return checked


INSTANTIATIONS = 0


def verify_rule_file(path: Path) -> int:
    global INSTANTIATIONS
    document = json.loads(path.read_text())
    checked = 0
    for rule in document["rules"]:
        instantiations = verify_rule(rule, str(path))
        if instantiations == 0:
            raise AssertionError(f"{path}:{rule['id']} has no instantiation to check")
        INSTANTIATIONS += instantiations
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
    print(
        ", ".join(f"{count} {name}" for name, count in counts.items())
        + f" verified semantically over {INSTANTIATIONS} rule instantiations"
    )


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error
