# Propositional semantic verification

The semantic verifier evaluates every propositional rewrite rule over all
Boolean valuations of its wildcards. It rejects a rule when its pattern and
result differ for any valuation.

It also verifies that each test expression is logically equivalent to its
expected result, and that every resolution inference conclusion is entailed by
its premises. Quantifier expressions are evaluated over the Boolean domain
with lexical scope and shadowing.

## What a wildcard stands for

A wildcard is instantiated with a fresh atom, with each variable the rule's
binder declares, and with the negation of each. The fresh atom stands for a body
independent of the binder, and it subsumes the two Boolean constants because the
equivalence is then checked under every valuation of that atom.

Including the bound variables matters: a wildcard instantiated only with
constants can never depend on the binder, which would verify every quantifier
rule vacuously.

## Side conditions

A rule's `constraints` are decided for each instantiation, and an instantiation
the side conditions reject is not checked — the rule claims nothing there.
`FreeQ` is decided syntactically on the instantiated expressions, respecting
binders, and accepts a list of variables.

A constraint the verifier cannot model is an error rather than a skip. Skipping
it silently would let the verifier report a rule sound that it never checked.

The summary line reports how many rule instantiations were checked, so a rule
set whose side conditions admit fewer cases is visible rather than silent; a
rule that admits none at all is rejected.

Run the checks locally:

```bash
just test
just verify
```

This is an exhaustive model check for the supported propositional operators;
it is not a general proof procedure for arbitrary predicates, domains, or
quantifier elimination.
