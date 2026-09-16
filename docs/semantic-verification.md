# Propositional semantic verification

The semantic verifier evaluates every propositional rewrite rule over all
Boolean valuations of its wildcards. It rejects a rule when its pattern and
result differ for any valuation.

It also verifies that each test expression is logically equivalent to its
expected result, and that every resolution inference conclusion is entailed by
its premises. Quantifier expressions are evaluated over the Boolean domain
with lexical scope and shadowing.

Run the checks locally:

```bash
just test
just verify
```

This is an exhaustive model check for the supported propositional operators;
it is not a general proof procedure for arbitrary predicates, domains, or
quantifier elimination.
