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

<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** META-ORGANVM (Meta) | **Tier:** standard | **Status:** CANDIDATE
**Org:** `unknown` | **Repo:** `schema-definitions`

### Edges
- **Produces** → `unknown`: unknown

### Siblings in Meta
`.github`, `organvm-corpvs-testamentvm`, `alchemia-ingestvm`, `organvm-engine`, `system-dashboard`, `organvm-mcp-server`

### Governance
- *Standard ORGANVM governance applies*

*Last synced: 2026-02-24T12:41:28Z*
<!-- ORGANVM:AUTO:END -->


## ⚡ Conductor OS Integration
This repository is a managed component of the ORGANVM meta-workspace.
- **Orchestration:** Use `conductor patch` for system status and work queue.
- **Lifecycle:** Follow the `FRAME -> SHAPE -> BUILD -> PROVE` workflow.
- **Governance:** Promotions are managed via `conductor wip promote`.
- **Intelligence:** Conductor MCP tools are available for routing and mission synthesis.
