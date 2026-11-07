# OSR v1 files

`v1/` holds the propositional rules of this repository in the OSR v1
interchange format (Specification, `docs/osr-v1.md`).  These files are
generated, never edited by hand:

| File | Content |
|---|---|
| `v1/logic.osr.json` | All 39 rules: OpenMath patterns over `logic1` and `quant1` (as `OMBIND`), profiles, and verification records in the `boolean` domain. |
| `v1/logic.report.json` | Machine-readable audit: metrics, the rules not migrated, and the termination proof of every profile. |
| `v1/logic.report.md` | The same audit for humans. |

## Where they come from

1. `OpenSymbolicRules/Lean` states each rule and proves it (`OSR/Logic.lean`):
   both sides have the same truth value for every assignment of the variables,
   with the `logic1` connectives interpreted on Lean's `Bool`.
2. `OpenSymbolicRules/Verification` publishes the export under
   `reports/<source digest>/` and can rebuild it independently.
3. This repository copies the published files.  The CI checks that they
   validate against the v1 schema, share one source digest, and are
   byte-identical to the published report.

## Differences from v0.1

The v0.1 files in `rules/` and `inferences/` remain for the v0.1 loader of
OpenSymbolicRules.jl.  In v1:

- all 39 rules are proved and certified in the `boolean` domain (carrier
  `setname2#Boolean`).  Quantifiers range over the truth values, as in the
  v0.1 tests, and bind one variable (v0.1 binds a sequence; a sequence is a
  chain of binders);
- `FreeQ` side conditions become `independent` matching constraints: the
  subterm matched by the metavariable must not mention the bound variable,
  which an engine checks syntactically;
- the profiles `default`, `to_cnf` and `to_dnf` are proved to terminate under
  the reference strategy (Lean `OSR.Logic.default_terminates`,
  `cnf_terminates`, `dnf_terminates`);
- the profiles are sound and terminating, not complete: v0.1 has
  `p ∧ ¬p ⟶ false` but not `¬p ∧ p ⟶ false`, so `p xor p` normalizes to
  `¬p ∧ p`;
- the inference rules (resolution) are not part of v1.

## Updating

```bash
just update-v1 <Verification>/reports/<digest>
```

Then update the Verification commit pinned in the CI workflow.
