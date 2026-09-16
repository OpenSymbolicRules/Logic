#!/usr/bin/env python3
"""Unit tests for the propositional semantic verifier."""

import unittest

from verify_propositional_semantics import evaluate


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


if __name__ == "__main__":
    unittest.main()
