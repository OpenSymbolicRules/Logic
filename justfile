set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

# Everything CI runs, except the comparison with a Verification report.
check: validate test verify v1

validate:
    ./scripts/validate.sh

test:
    python3 scripts/test_verify_propositional_semantics.py

verify:
    python3 scripts/verify_propositional_semantics.py

# Check the generated OSR v1 files; pass a Verification report directory to
# also compare them byte for byte.
v1 report="":
    ./scripts/check-v1.sh {{report}}

# Copy the v1 files from a Verification report directory, then check them.
update-v1 report:
    cp {{report}}/logic.osr.json {{report}}/logic.report.json {{report}}/logic.report.md v1/
    ./scripts/check-v1.sh {{report}}
