# OpenSymbolicRules Logic

This repository provides an OpenSymbolicRules (OSR) rule set for Boolean
simplification and propositional logic.  It is language-neutral: each rule
uses OSR expression syntax and declares its operator meaning with OpenMath.

## Contents

- Boolean identity and idempotence rules.
- Negation normal form and complement rules.
- Implication and equivalence expansion to core connectives.
- NAND, NOR, XOR, and XNOR expansion to core connectives.
- Explicit `to_cnf` and `to_dnf` profiles for distributive normalisation.
- An explicit `resolution` inference profile for sound clause derivation.
- Lexically scoped universal and existential quantifier negation rules.
- Executable fixtures for every rule.

The current rules are intentionally oriented towards smaller expressions. This
keeps simplification terminating and avoids rewrite loops such as expanding an
expression and immediately applying its inverse identity.

## OpenMath semantics

The rule files map their operators to the `logic1` OpenMath content dictionary:

| OSR operator | OpenMath symbol |
| --- | --- |
| `And` | `openmath:logic1#and` |
| `Or` | `openmath:logic1#or` |
| `Not` | `openmath:logic1#not` |
| `True` | `openmath:logic1#true` |
| `False` | `openmath:logic1#false` |

This semantic mapping is part of the rule data, rather than an implementation
detail of a particular computer algebra system.

## Repository layout

```text
rules/       Rule files, ordered by rules/meta.json
tests/       Test fixtures corresponding to the rules
docs/        Explanatory documentation
Specification/  Pinned OSR specification and JSON schemas
```

## Validation

Initialize submodules and validate all JSON files:

```bash
git submodule update --init --recursive
just validate
just test
just verify
```

The validation command checks the OSR JSON Schemas and validates the rule and
test data against them. The semantic verifier exhaustively checks the supported
propositional rules and resolution inferences over Boolean valuations.
