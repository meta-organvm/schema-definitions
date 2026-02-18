# CLAUDE.md — schema-definitions

**ORGAN Meta** (Meta) · `meta-organvm/schema-definitions`
**Status:** ACTIVE · **Branch:** `main`

## What This Repo Is

Canonical JSON Schema definitions for all eight-organ system data contracts — registry, seed.yaml, governance rules, dispatch payloads, soak tests, and system metrics.

## Stack

**Languages:** Python
**Build:** Python (pip/setuptools)
**Testing:** pytest (likely)

## Directory Structure

```
📁 .github/
📁 examples/
📁 schemas/
📁 scripts/
    validate.py
📁 tests/
    test_schemas.py
  CHANGELOG.md
  README.md
  pyproject.toml
  seed.yaml
```

## Key Files

- `README.md` — Project documentation
- `pyproject.toml` — Python project config
- `seed.yaml` — ORGANVM orchestration metadata
- `tests/` — Test suite

## Development

```bash
pip install -e .    # Install in development mode
pytest              # Run tests
```

## ORGANVM Context

This repository is part of the **ORGANVM** eight-organ creative-institutional system.
It belongs to **ORGAN Meta (Meta)** under the `meta-organvm` GitHub organization.

**Registry:** [`registry-v2.json`](https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/registry-v2.json)
**Corpus:** [`organvm-corpvs-testamentvm`](https://github.com/meta-organvm/organvm-corpvs-testamentvm)
