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

They retain the original bound-variable list exactly. Instantiation,
quantifier elimination, and domain-specific quantifier rules are intentionally
out of scope until their side conditions and capture-avoiding substitution are
specified.
