#!/usr/bin/env bash
set -euo pipefail

schema_dir="Specification/schemas"

check-jsonschema --check-metaschema "$schema_dir"/*.schema.json
check-jsonschema --schemafile "$schema_dir/meta.schema.json" rules/meta.json
find rules -type f -name '*.json' ! -path 'rules/meta.json' -print0 | \
  xargs -0 -r check-jsonschema --schemafile "$schema_dir/rule-file.schema.json" --base-uri "file://${PWD}/$schema_dir/"
find tests -type f -name '*.json' -print0 | \
  xargs -0 -r check-jsonschema --schemafile "$schema_dir/test-file.schema.json" --base-uri "file://${PWD}/$schema_dir/"
find inferences -type f -name '*.json' -print0 | \
  xargs -0 -r check-jsonschema --schemafile "$schema_dir/inference-file.schema.json" --base-uri "file://${PWD}/$schema_dir/"
find inference-tests -type f -name '*.json' -print0 | \
  xargs -0 -r check-jsonschema --schemafile "$schema_dir/inference-test-file.schema.json" --base-uri "file://${PWD}/$schema_dir/"

duplicate_ids="$(find rules -type f -name '*.json' ! -path 'rules/meta.json' -print0 | \
  xargs -0 -r jq -r '.rules[].id' | sort -n | uniq -d)"
if [[ -n "$duplicate_ids" ]]; then
  echo "Duplicate rule identifiers: $duplicate_ids" >&2
  exit 1
fi
