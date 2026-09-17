# Capture-avoiding substitution

This document specifies what a consumer of the quantifier rules must implement
before instantiation or quantifier elimination can be added. It defines scope,
alpha-equivalence, and capture-avoiding substitution for OSR expressions, and
states which quantifier rules those definitions make expressible.

## Binding forms

`Forall` and `Exists` are the binding forms of this rule set:

```json
["Forall", ["x", "y"], body]
```

The second element is the binder: a non-empty list of plain identifiers. It is a
declaration, not a use — the identifiers in it are not occurrences of anything.
The third element is the body, and the binder scopes over it.

Other OSR domains bind through `openmath:fns1#lambda`, and a derivative, an
integral, a sum, and a product all carry their bound variable inside such a
lambda. A consumer that implements the definitions below for one binding form
therefore implements them for all of them.

## Free and bound occurrences

An occurrence of an identifier `x` in an expression `e` is **bound** when some
enclosing binder of `e` declares `x`, and **free** otherwise. Only the innermost
enclosing binder of a name captures it, so a nested binder shadows an outer one.

The free identifiers of an expression are written `FV(e)`:

- `FV(x)` is `{x}` for an identifier;
- `FV(f(e₁, …, eₙ))` is the union of `FV(eᵢ)`, and a collection argument such as
  a branch list contributes the union of its elements;
- `FV(Forall(xs, b))` and `FV(Exists(xs, b))` are `FV(b)` minus `xs`.

So `x` is free in `And(Forall(["x"], x), x)` — the second occurrence is free
even though the first is bound — and `Forall(["x"], x)` has no free identifier
at all.

A side condition written `FreeQ(e, x)` in a rule file holds exactly when `x` is
not free in `e`. A bound occurrence is not an occurrence of the free identifier,
so `FreeQ(Forall(["x"], x), x)` holds.

## Alpha-equivalence

Two expressions are **alpha-equivalent** when they are equal up to a consistent
renaming of their bound identifiers. Free identifiers are compared by name and
are never renamed.

```text
Forall(["x"], x)  ≡α  Forall(["y"], y)
Forall(["x"], x)  ≢α  Forall(["y"], x)
```

A consumer must treat alpha-equivalent formulas as the same formula. In
particular, a rule that matches `Forall(["x"], p_)` must equally match
`Forall(["y"], p_)`, and a proof of equivalence must accept two results that
differ only in the names of their bound identifiers.

## Substitution

Writing `e[x := t]` for the replacement of every free occurrence of `x` in `e`
by `t`:

- an identifier equal to `x` becomes `t`, and any other identifier is unchanged;
- a function application substitutes into each of its arguments;
- a binder that declares `x` is left unchanged, because it has no free
  occurrence of `x`;
- any other binder substitutes into its body — **after** the renaming below.

The substitution is **capture-avoiding**: before descending into a binder, every
declared identifier that is free in `t` is renamed to an identifier fresh for
`t`, for the binder's body, and for `x`. Without that renaming the replacement
would stop referring to the identifier it referred to outside the binder:

```text
Forall(["y"], And(x, y))[x := y]
  = Forall(["y1"], And(y, y1))          correct
  ≠ Forall(["y"],  And(y, y))           y captured
```

The choice of fresh identifier is not observable, because two correct results
differ only in bound names and are therefore alpha-equivalent.

## Why instantiation is an inference, not a rewrite

An OSR rewrite result is built only from the expression fragments its pattern
bound. The expression grammar has no operator that denotes substitution, so the
conclusion of universal instantiation,

```text
from Forall(["x"], p)   derive   p[x := t]
```

cannot be written as a rewrite result: `p[x := t]` is not a fragment of the
premise, it is computed from it.

This is the same shape as propositional resolution, whose resolvent is likewise
computed from its premises, and which this rule set already publishes as an
inference profile rather than as a rewrite. Universal instantiation, existential
generalisation, and quantifier elimination therefore belong in an inference
profile, where the consumer performs the substitution defined above. Adding a
substitution operator to the expression grammar is the alternative, and it would
oblige every consumer to evaluate it; that is a specification decision and is
deliberately left open here.

## Quantifier rules these definitions make expressible

Rules whose only side condition is `FreeQ` need nothing beyond the definitions
above, because the side condition is a question about the premise rather than a
computation on it:

- `∀x.(P ∧ Q) ≡ (∀x.P) ∧ Q` and `∃x.(P ∨ Q) ≡ (∃x.P) ∨ Q`, when `x` is not free
  in `Q`;
- `∀x.P ≡ P` and `∃x.P ≡ P`, when `x` is not free in `P`.

Rules that distribute a quantifier over a matching connective need no side
condition at all, and section 6.2 of the rule set publishes both in their
contracting direction:

- `∀x.(P ∧ Q) ≡ (∀x.P) ∧ (∀x.Q)`;
- `∃x.(P ∨ Q) ≡ (∃x.P) ∨ (∃x.Q)`.

All of these assume a non-empty domain of quantification, as classical
first-order logic does. A rule set for a logic that admits the empty domain must
state that assumption explicitly and drop the vacuous-quantification rules.

The dual distributions — `∀` over `∨` and `∃` over `∧` — hold in one direction
only and are not equivalences, so they belong in an inference profile rather
than among the rewrites.
