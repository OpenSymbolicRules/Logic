# Quantifiers

Quantified OSR expressions use an explicit lexical binding form:

```json
["Forall", ["x"], body]
```

`Forall` and `Exists` map to `openmath:quant1#forall` and
`openmath:quant1#exists`. Their variable list is non-empty, contains plain
identifiers only, and scopes over the body. A nested binder may shadow an outer
variable; consumers must preserve this scope and alpha-rename bound variables
when a host representation requires it.

The initial rules push negation through a quantifier:

- `¬∀x.P` becomes `∃x.¬P`;
- `¬∃x.P` becomes `∀x.¬P`.

They retain the original bound-variable list exactly.

Two further rules merge quantifiers of the same kind over the same variables:

- `(∀x.P) ∧ (∀x.Q)` becomes `∀x.(P ∧ Q)`;
- `(∃x.P) ∨ (∃x.Q)` becomes `∃x.(P ∨ Q)`.

Both are equivalences and need no side condition. They are oriented towards
fewer binders, which is the contracting direction the default profile keeps
throughout, and they require the two variable lists to be written identically;
a consumer that compares binders up to alpha-equivalence may merge more.

A quantifier whose body does not mention its variables is dropped:

- `∀x.P` and `∃x.P` become `P` when `x` is not free in `P`.

Both assume a non-empty domain of quantification, as classical first-order logic
does. A rule set for a logic that admits the empty domain must drop them.

[Capture-avoiding substitution](substitution.md) specifies scope,
alpha-equivalence, and substitution for these binders, and states which further
quantifier rules those definitions make expressible. Instantiation and
quantifier elimination compute their conclusion from the premise rather than
selecting a fragment of it, so they belong in an inference profile alongside
resolution rather than among the rewrites.
