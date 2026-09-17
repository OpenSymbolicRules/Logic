# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Boolean identity, idempotence, double-negation, and complement rules with
  OpenMath `logic1` semantics.
- Symmetric identity and annihilation rules, plus Boolean absorption rules.
- De Morgan, Boolean constant-negation, implication, and equivalence rules.
- Explicit `to_cnf` and `to_dnf` profiles with distributivity rules.
- Expansion rules for NAND, NOR, XOR, and XNOR.
- Binary propositional resolution inference profile and inference fixtures.
- Unit-resolution inference rules for binary clauses and both clause orders.
- Unit-conflict inference rules deriving `False` as a resolution certificate.
- MIT licensing, an OpenMath attribution notice, and SPDX metadata in the rule manifest.
- OpenMath `quant1` universal and existential quantifier-negation rules.
- Exhaustive propositional semantic verification of rules, fixtures, and
  resolution inferences in CI.
- JSON Schema validation, executable fixtures, and Boolean-rule documentation.
- Quantifier scope rules merging two universals over a conjunction and two
  existentials over a disjunction when their variable lists agree.
- A specification of scope, alpha-equivalence, and capture-avoiding substitution
  for the quantifier binders, including which further quantifier rules it makes
  expressible as rewrites and why instantiation belongs in an inference profile.
