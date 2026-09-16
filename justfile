set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

validate:
    ./scripts/validate.sh

test:
    python3 scripts/test_verify_propositional_semantics.py

verify:
    python3 scripts/verify_propositional_semantics.py
