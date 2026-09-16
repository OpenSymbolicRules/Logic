# Propositional resolution

The `resolution` inference profile derives consequences from pairs of clauses.
It does not rewrite or discard its premises.

For example, from `p ∨ q` and `¬p ∨ r`, binary resolution derives `q ∨ r`.
The pivot proposition and its negation are complementary; the remaining
literals form the resolvent.

Unit resolution is also available. From `p` and `¬p ∨ q`, it derives `q`.
The rule file includes both literal positions in binary clauses and both premise
orders so consumers do not need to reorder a clause before unit propagation.

Complementary unit clauses derive `False`. This is the base contradiction used
by a resolution refutation and provides a compact inconsistency certificate.

Use the `to_cnf` profile before resolution so that a formula is represented as
a conjunction of disjunctive clauses. The current profile covers binary
clauses represented by OSR's binary `Or` trees. Clause-set canonicalisation,
factoring, subsumption, and saturation strategy remain responsibilities of the
consumer and are intentionally outside this first sound inference set.
