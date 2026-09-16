#!/usr/bin/env bash
set -euo pipefail

schema_dir="Specification/schemas"

check-jsonschema --check-metaschema "$schema_dir"/*.schema.json
check-jsonschema --schemafile "$schema_dir/meta.schema.json" rules/meta.json
find rules -type f -name '*.json' ! -path 'rules/meta.json' -print0 | \
  xargs -0 -r check-jsonschema --schemafile "$schema_dir/rule-file.schema.json"
find tests -type f -name '*.json' -print0 | \
  xargs -0 -r check-jsonschema --schemafile "$schema_dir/test-file.schema.json"
