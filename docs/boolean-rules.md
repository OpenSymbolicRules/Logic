# Boolean rules

The initial Boolean rule set covers the simplifications that are both common
and safe to apply repeatedly:

- identity: `p ∨ false` and `p ∧ true` become `p`;
- annihilation: `p ∨ true` becomes `true` and `p ∧ false` becomes `false`;
- idempotence: `p ∨ p` and `p ∧ p` become `p`;
- complements: `p ∨ ¬p` becomes `true` and `p ∧ ¬p` becomes `false`;
- double negation: `¬¬p` becomes `p`.
- absorption: `p ∨ (p ∧ q)` and `p ∧ (p ∨ q)` become `p`.

For binary `And` and `Or` trees, rules whose result depends on an operand
position are included in both operand orders. A consumer therefore does not
need to canonicalize commutative expressions before applying this rule set.

Rules are deliberately directed from a larger expression to a smaller one.
For example, the inverse of double negation is not included: adding it would
allow an engine to rewrite `p` to `¬¬p` indefinitely.

All Boolean operators are defined by the OpenMath `logic1` content dictionary.
Consumers should use the `semantics` object in each rule file to associate an
OSR expression head with that content-dictionary symbol.
