# Boolean rules

The initial Boolean rule set covers the simplifications that are both common
and safe to apply repeatedly:

- identity: `p ∨ false` and `p ∧ true` become `p`;
- annihilation: `p ∨ true` becomes `true` and `p ∧ false` becomes `false`;
- idempotence: `p ∨ p` and `p ∧ p` become `p`;
- complements: `p ∨ ¬p` becomes `true` and `p ∧ ¬p` becomes `false`;
- double negation: `¬¬p` becomes `p`.
- absorption: `p ∨ (p ∧ q)` and `p ∧ (p ∨ q)` become `p`.
- negation normal form: De Morgan's laws push `Not` through `And` and `Or`.
- derived connectives: implication and equivalence reduce to `And`, `Or`, and
  `Not`.

For binary `And` and `Or` trees, rules whose result depends on an operand
position are included in both operand orders. A consumer therefore does not
need to canonicalize commutative expressions before applying this rule set.

The negation-normal-form rules may increase expression size, but strictly move
negation toward atomic propositions. They are therefore a normalizing pass,
not a general-purpose size-reducing simplification.

## CNF and DNF profiles

The default manifest does not include distributivity. Select the `to_cnf`
profile to distribute `Or` over `And`, or `to_dnf` to distribute `And` over
`Or`. Both profiles are complete manifests declared in `rules/meta.json` and
include the prerequisite simplification, connective-expansion, and
negation-normal-form rules.

The profiles operate on binary expression trees and include both operand orders
for distributivity. Consumers that want a canonical representation should also
canonicalize associative and commutative `And` and `Or` nodes.

Rules are deliberately directed from a larger expression to a smaller one.
For example, the inverse of double negation is not included: adding it would
allow an engine to rewrite `p` to `¬¬p` indefinitely.

All Boolean operators are defined by the OpenMath `logic1` content dictionary.
Consumers should use the `semantics` object in each rule file to associate an
OSR expression head with that content-dictionary symbol.
