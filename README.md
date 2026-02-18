# schema-definitions

Canonical JSON Schema definitions for the organvm eight-organ system's data contracts.

## Schemas

| Schema | Validates | Source of Truth |
|--------|-----------|-----------------|
| `registry-v2.schema.json` | `registry-v2.json` | Repository state across all 8 organs |
| `seed-v1.schema.json` | `seed.yaml` | Per-repo automation contracts |
| `governance-rules.schema.json` | `governance-rules.json` | Dependency rules, promotion state machine |
| `dispatch-payload.schema.json` | Cross-org dispatch events | ORGAN-IV routing payloads |
| `soak-test.schema.json` | `daily-*.json` | VIGILIA soak test snapshots |
| `system-metrics.schema.json` | `system-metrics.json` | Computed + manual system metrics |

## Usage

```bash
# Validate a file (auto-detects schema from filename)
python scripts/validate.py path/to/registry-v2.json

# Validate all examples
python scripts/validate.py --all-examples

# Run tests
pytest
```

## Install

```bash
pip install -e ".[dev]"
```

Requires: Python 3.11+, `jsonschema`, `pyyaml`.

## Part of the Eight-Organ System

This repo belongs to **meta-organvm** (ORGAN VIII) and provides the data contracts that `organvm-engine` validates against.
