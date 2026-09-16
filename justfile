set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

validate:
    ./scripts/validate.sh
