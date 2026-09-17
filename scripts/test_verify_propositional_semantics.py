#!/usr/bin/env python3
"""Unit tests for the propositional semantic verifier."""

import unittest

from verify_propositional_semantics import (
    BOUND_VARIABLES,
    constraint_holds,
    evaluate,
    instantiate,
    instantiate_binders,
    verify_rule,
    wildcard_candidates,
)


class EvaluateTests(unittest.TestCase):
    def test_core_connectives(self) -> None:
        self.assertTrue(evaluate(["And", True, ["Not", False]], {}))
        self.assertFalse(evaluate(["Or", False, False], {}))
        self.assertTrue(evaluate(["Implies", False, False], {}))
        self.assertFalse(evaluate(["Equivalent", True, False], {}))

    def test_quantifier_scope(self) -> None:
        expression = ["Forall", ["x"], ["Or", "x", ["Not", "x"]]]
        self.assertTrue(evaluate(expression, {"x": False}))

    def test_quantifier_shadowing(self) -> None:
        expression = ["Exists", ["x"], ["And", "x", ["Not", "x"]]]
        self.assertFalse(evaluate(expression, {"x": True}))


class InstantiationTests(unittest.TestCase):
    def test_binder_sequence_becomes_a_concrete_list(self) -> None:
        pattern = ["Forall", ["xs__"], "p_"]
        self.assertEqual(instantiate_binders(pattern), ["Forall", BOUND_VARIABLES, "p_"])

    def test_a_wildcard_may_stand_for_a_bound_variable(self) -> None:
        # A wildcard instantiated only with constants can never depend on the
        # bound variable, which would verify every quantifier rule vacuously.
        candidates = wildcard_candidates("p_", BOUND_VARIABLES)
        for variable in BOUND_VARIABLES:
            self.assertIn(variable, candidates)
            self.assertIn(["Not", variable], candidates)
        # A fresh atom stands for a body independent of the binder.
        self.assertTrue(any(isinstance(c, str) and c not in BOUND_VARIABLES for c in candidates))


class ConstraintTests(unittest.TestCase):
    def test_free_q_over_a_variable_list(self) -> None:
        self.assertTrue(constraint_holds(["FreeQ", "atom0", ["x", "y"]], {}))
        self.assertFalse(constraint_holds(["FreeQ", "x", ["x", "y"]], {}))
        self.assertFalse(constraint_holds(["FreeQ", ["Not", "y"], ["x", "y"]], {}))

    def test_free_q_ignores_bound_occurrences(self) -> None:
        expression = ["Forall", ["x"], "x"]
        self.assertTrue(constraint_holds(["FreeQ", expression, ["x"]], {}))

    def test_free_q_reads_its_arguments_from_the_environment(self) -> None:
        self.assertTrue(constraint_holds(["FreeQ", "p_", "xs_"], {"p_": "atom0", "xs_": ["x"]}))
        self.assertFalse(constraint_holds(["FreeQ", "p_", "xs_"], {"p_": "x", "xs_": ["x"]}))

    def test_an_unmodelled_constraint_is_refused(self) -> None:
        # Silently ignoring a side condition would let the verifier claim a rule
        # sound that it never checked.
        with self.assertRaises(ValueError):
            constraint_holds(["PositiveQ", "p_"], {"p_": "atom0"})


class RuleVerificationTests(unittest.TestCase):
    def test_a_guarded_rule_verifies(self) -> None:
        rule = {
            "id": 1,
            "pattern": ["Forall", ["xs__"], "p_"],
            "constraints": [["FreeQ", "p_", "xs_"]],
            "result": "p_",
        }
        self.assertGreater(verify_rule(rule, "test"), 0)

    def test_the_same_rule_without_its_guard_is_unsound(self) -> None:
        rule = {
            "id": 1,
            "pattern": ["Forall", ["xs__"], "p_"],
            "constraints": [],
            "result": "p_",
        }
        with self.assertRaises(AssertionError):
            verify_rule(rule, "test")

    def test_quantifier_negation_is_checked_against_dependent_bodies(self) -> None:
        rule = {
            "id": 1,
            "pattern": ["Not", ["Forall", ["xs__"], "p_"]],
            "constraints": [],
            "result": ["Exists", ["xs__"], ["Not", "p_"]],
        }
        self.assertGreater(verify_rule(rule, "test"), 1)


if __name__ == "__main__":
    unittest.main()
