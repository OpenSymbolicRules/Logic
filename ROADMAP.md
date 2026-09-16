# Logic rule-set roadmap

## Completed

- [x] Boolean simplification: identity, annihilation, idempotence, complement,
  and absorption.
- [x] Negation normal form for binary conjunction and disjunction.
- [x] Expansion of implication and equivalence to core Boolean connectives.

## Next

- [ ] Define explicit `to_cnf` and `to_dnf` normalization profiles. These will
  use distributivity and must remain separate from size-reducing simplification.
- [ ] Add propositional resolution as an inference profile.
- [ ] Specify safe bound-variable representation before adding quantifier rules
  from the OpenMath `quant1` content dictionary.
