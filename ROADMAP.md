# Logic rule-set roadmap

## Completed

- [x] Boolean simplification: identity, annihilation, idempotence, complement,
  and absorption.
- [x] Negation normal form for binary conjunction and disjunction.
- [x] Expansion of implication and equivalence to core Boolean connectives.
- [x] Expansion of NAND, NOR, XOR, and XNOR to core Boolean connectives.

## Next

- [x] Define explicit `to_cnf` and `to_dnf` normalization profiles. These use
  distributivity and remain separate from size-reducing simplification.
- [x] Add binary propositional resolution as an inference profile.
- [x] Add unit resolution for binary clauses.
- [x] Add unit-conflict derivation for propositional refutation.
- [x] Specify safe bound-variable representation and add quantifier-negation
  rules from the OpenMath `quant1` content dictionary.

## Later

- [x] Specify capture-avoiding substitution and domain-aware quantifier rules
  before adding instantiation or quantifier elimination. See
  [docs/substitution.md](docs/substitution.md).
- [x] Add the distribution of `Forall` over `And` and of `Exists` over `Or`,
  in their contracting direction.
- [x] Add the `FreeQ`-guarded vacuous-quantification rules.
- [ ] Add the `FreeQ`-guarded extraction rules, `∀x.(P ∧ Q) ≡ (∀x.P) ∧ Q` and
  `∃x.(P ∨ Q) ≡ (∃x.P) ∨ Q`. Check first that they do not cycle against the
  merging rules of section 6.2.
- [ ] Add universal instantiation and existential generalisation as an inference
  profile, where the consumer performs the substitution.
