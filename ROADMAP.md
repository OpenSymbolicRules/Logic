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
- [ ] Specify safe bound-variable representation before adding quantifier rules
  from the OpenMath `quant1` content dictionary.
