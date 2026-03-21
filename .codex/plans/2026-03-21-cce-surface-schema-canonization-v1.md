# CCE Surface Schema Canonization V1

Date: 2026-03-21
Project: meta-organvm/schema-definitions

## Goal

Promote the Conversation Corpus Engine outward surface contracts into Meta's canonical schema repository so downstream consumers validate against one shared source of truth.

## Scope

1. Add canonical JSON Schemas for:
   - surface manifest
   - MCP context payload
   - surface bundle
2. Add example payloads that validate against those schemas.
3. Extend the repo validator to auto-detect the new examples.
4. Add regression tests covering example validation and basic required-field failures.
5. Update repo docs so the new contracts are discoverable.

## Constraints

- Preserve existing schema naming patterns and validator behavior.
- Keep the contracts compatible with the already-working CCE export implementation.
- Do not introduce a second divergent schema vocabulary.

## Verification

- Run targeted schema tests.
- Run the example validator across the new examples.
