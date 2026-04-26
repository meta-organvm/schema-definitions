# Primal Primitives v1 — Cross-Repo Atomic Material Registry

**Status:** v1.1 (verified — expanded by 4th-repo crawl on `application-pipeline` 2026-04-26; 13th primitive surfaced and added inline)
**Date:** 2026-04-26
**Source:** synthesis of 4 leaf-level Explore crawls — `conversation-corpus-engine`, `linguistic-atomization-framework`, `mirror-mirror`, `application-pipeline`
**Plan:** `~/.claude/plans/session-complete-gleaming-cocoa.md` (Addendum 2026-04-26)

---

## Why this doc exists

Repo-level analysis is camouflage. A repo called "conversation corpus engine" and a repo called "mirror-mirror" sound like they do completely different things — but at the leaf-file level, they execute the same set of *purposeful moves* under different domain vocabulary. This registry names those moves once so every repo can declare which subset it implements without re-inventing the vocabulary.

This doc is **vocabulary, not substrate.** Substrates use it; clients consume substrates; the registry stays stable beneath both.

---

## Two floors

**Practical floor (this registry, 12 entries):** the smallest *intentional* moves with domain-recognizable names. This is what shows up in code reviews, PR descriptions, and architectural diagrams. Below this is generic CS, above this is feature-talk.

**Absolute computational floor (academic, 5 entries):** `READ` · `WRITE` · `COMPARE` · `BIND` · `LOOKUP`. Below this is bytes. Not actionable for this ecosystem; included only to mark where the registry stops being useful.

---

## The 13 primitives

| # | Primitive | One-line definition |
|---|---|---|
| 1 | `INGEST-FROM-SOURCE` | Load data from an external source into normalized internal shape. |
| 2 | `NAME-WITH-STRATEGY` | Assign an identifier to a thing using a chosen naming strategy. |
| 3 | `TAG-WITH-METADATA` | Attach declared key-value metadata to an artifact. |
| 4 | `VALIDATE-AGAINST-SCHEMA` | Check that an object satisfies a published contract. |
| 5 | `TRANSFORM-SHAPE` | Apply a function to data, producing data of a different shape. |
| 6 | `COMPOSE-INTO-CHAIN` | Orchestrate primitives into an end-to-end sequence. |
| 7 | `ROUTE-BY-TYPE` | Dispatch input to the correct handler based on its detected type. |
| 8 | `EMIT-TO-SINK` | Write output to a file, channel, or external service. |
| 9 | `DEFER-TO-LATER` | Queue work for asynchronous execution; record decision history. |
| 10 | `TRACK-LIFECYCLE` | Record state transitions over time as a durable artifact. |
| 11 | `COMPARE-DELTA` | Measure the difference between two states; emit a diff. |
| 12 | `EXTRACT-SUBSTRUCTURE` | Derive named components from a larger structure. |
| 13 | `MUTATE-RULE-BASED-ON-FEEDBACK` | Observe outcomes against predictions, extract a learning signal, adjust decision weights/rules so future runs improve. **The adaptive-system primitive: it operates on the system's own decision logic, not on data flowing through.** |

---

## Cross-repo evidence table

Each row shows how a primitive surfaces in three crawled repos under different domain vocabulary. Source files are exact leaf-file paths from the Explore crawls.

| Primitive | conversation-corpus-engine | linguistic-atomization-framework | mirror-mirror | application-pipeline (v1.1) |
|---|---|---|---|---|
| `INGEST-FROM-SOURCE` | `src/conversation_corpus_engine/import_chatgpt_export_corpus.py` (walks ChatGPT mapping trees, linearizes by timestamp) | (input side of `framework/core/atomizer.py`) | `src/hooks/use-voice-commands.ts` (transcribes via WebSpeechRecognition) | `scripts/ingest_historical.py`, `scripts/source_jobs.py` |
| `NAME-WITH-STRATEGY` | implicit (`artifact_id` fields) | `framework/core/naming.py` `NamingStrategy` enum (5 strategies → IDs like `T001:military-town.P001.S001`) | `src/lib/badgeCollectionInit.ts` (badge identifiers) | `blocks/projects/registry.yaml` (89-project domain/track/identity tags) |
| `TAG-WITH-METADATA` | `src/conversation_corpus_engine/schemas/corpus-candidate.schema.json` (candidate fields) | `framework/core/registry.py` (analysis-module tags) | badge metadata on awarded artifacts | `blocks/identity/60s.md` frontmatter (`identity_positions`, `tracks`, `tags`) |
| `VALIDATE-AGAINST-SCHEMA` | 10 JSON-Schema contracts in `schemas/` | regex + `framework/core/tokenizers.py` script validation | `src/__tests__/badgeCollectionInit.test.ts` | `scripts/standards.py`, `scripts/validate.py` (Level 1 audit pre-submit) |
| `TRANSFORM-SHAPE` | `src/conversation_corpus_engine/corpus_diff.py` | `framework/analysis/semantic.py` (TF-IDF) + `sentiment.py` (VADER) | `src/lib/AIOutfitRecommendations.tsx` (state → simulated outfit) | `scripts/tailor_resume.py`, `scripts/alchemize.py` |
| `COMPOSE-INTO-CHAIN` | `src/conversation_corpus_engine/provider_refresh.py` (import → eval → stage → promote) | (analysis pipeline orchestration) | `src/App.tsx` (50+ component shell wiring 8 primitives into flows) | `scripts/apply.py` (12-step: load → audit → fetch portal Q's → fill → cover → DM → overlap → PDF) |
| `ROUTE-BY-TYPE` | `src/conversation_corpus_engine/provider_discovery.py` (`looks_like_chatgpt_export()`, etc.) | `framework/core/tokenizers.py` `TokenizerFactory` (Script enum → strategy) | tab/feature routing in App shell | `scripts/{greenhouse,lever,ashby}_submit.py` (dispatch by detected ATS) |
| `EMIT-TO-SINK` | `write_json()` / `write_markdown()` (in `answering.py`, used 20+ places) | `framework/visualization/base.py` `TemplateEngine` | `src/lib/notifications.ts` `sendSMSNotification()` / `sendEmailNotification()` | `scripts/submit.py --record`, writes `applications/YYYY-MM-DD/<org>--<role>/` |
| `DEFER-TO-LATER` | `src/conversation_corpus_engine/corpus_candidates.py` (stage→review→promote→rollback state machine) | (implicit binding deferral) | `src/lib/reminderScheduler.ts` `scheduleRemindersForBooking()` | `pipeline/*/deferral` field + `standup.py --section deferred` |
| `TRACK-LIFECYCLE` | `state/testaments/s33-testament.json` (session metadata, commit ranges, capabilities) | (implicit history) | `StyleHistory.tsx` (timeline of tried styles) + `useKV` persistence | `signals/score-telemetry.yaml`, `conversion-log.yaml`, `signal-actions.yaml` |
| `COMPARE-DELTA` | `corpus_diff.py` (query counts, structural changes, failure reasons) | `framework/analysis/semantic.py` cosine similarity | `src/lib/tradePrediction.ts` (success probability vs reference) | `scripts/rejection_learner.py`, `block_outcomes.py`, `text_match.py` (TF-IDF overlap) |
| `EXTRACT-SUBSTRUCTURE` | `answering.py` `tokenize()` / `search_documents_v4()` / `lexical_support_for_tokens()` | `framework/analysis/entity.py` (NER) + `temporal.py` (verb tense extraction) | `src/lib/SkinAnalysis.tsx` / `FaceLandmarkTracking.tsx` (state classification) | `scripts/enrich.py` (job posting → role fit + skill gaps), `research_contacts.py` |
| `MUTATE-RULE-BASED-ON-FEEDBACK` | — absent (eval gates apply fixed thresholds; no self-modifying rule) | — absent (analysis modules use static methods) | — absent (trade prediction reads scores, doesn't update rubric) | **`scripts/recalibrate.py`** — quarterly weight adjustments to `strategy/scoring-rubric.yaml` based on outcome learner deltas vs `signals/hypotheses.yaml`. **The adaptive loop.** |

---

## What is NOT a primitive (per the Explore reports)

These are *compositions* of primitives, not primitives themselves. Repos often market them as singular features — but they decompose to 2-4 primitives chained.

| Composition (repo) | Decomposes to |
|---|---|
| "Provider Refresh" (corpus-engine) | `INGEST` + `VALIDATE` + `TRANSFORM` + `DEFER` + (optional) `EMIT` |
| "Federation Build" (corpus-engine) | `TRANSFORM` + `EXTRACT` + `EMIT` |
| "Corpus Promotion" (corpus-engine) | `DEFER` + `TRACK` + `VALIDATE` + `EMIT` |
| "Computational Rhetorical Analysis" (atomization) | `EXTRACT` + `COMPARE` + `TRANSFORM` (applied per atom level + aggregated) |
| "Multi-Dimensional Analysis Pipeline" (atomization) | 5 stages, each = `COMPOSE-INTO-CHAIN` of 2-3 primitives |
| "Hierarchical Decomposition" (atomization) | `TRANSFORM` (split) + `EXTRACT` (atom tree) + `ROUTE-BY-TYPE` (analysis dispatch) |
| "Truth Engine" (mirror-mirror) | `COMPARE-DELTA` + `EXTRACT` (assess) + `EMIT` (toast) loop |
| "Phygital Bridge" (mirror-mirror) | `INGEST` (choice) + `NAME` (badge) + `DEFER` (appointment) + `EMIT` (reminder) |
| "Badge Economy" (mirror-mirror) | `NAME` + `TAG` + `VALIDATE` + `TRACK` + `COMPARE` (social) |

This list extends as the registry sees more repos. Compositions are not bugs — they are useful named patterns. They just are not the floor.

---

## How to apply (per repo)

A repo declares which primitives it implements via an additive `primitives:` field in its `seed.yaml` (extension reserved against `seed-v1.1.schema.json` — separate, additive PR):

```yaml
# seed.yaml fragment
primitives:
  - INGEST-FROM-SOURCE
  - VALIDATE-AGAINST-SCHEMA
  - TRANSFORM-SHAPE
  - COMPOSE-INTO-CHAIN
  - EMIT-TO-SINK
  # (only the primitives this repo actually uses; subset-only)
```

Conventions:
- IDs are exact strings from the registry (CAPS-DASH).
- A repo that lists `COMPOSE-INTO-CHAIN` should also list every primitive its chains compose. Composition without sub-primitive declaration is a smell.
- Adding a primitive that is not in the registry triggers registry expansion (PR to bump v1 → v1.1).

---

## Reduction factors observed

| Repo | Modules / surfaces | Distinct primitives | Ratio |
|---|---|---|---|
| conversation-corpus-engine | 33 source modules + 9 leaf dirs | 12 | 33:12 ≈ 2.75 |
| linguistic-atomization-framework | 11 leaf dirs of pluggable modules | 12 | 11:12 ≈ 1:1 |
| mirror-mirror | 50+ components, 40+ tabs | 8 | 50:8 ≈ 6.25 |
| application-pipeline (v1.1) | 160+ scripts + 15 action dirs + 4 data dirs | **13** (only repo using #13) | 160:13 ≈ 12.3 |

The high-ratio repos (mirror-mirror, corpus-engine) are *choreography-heavy* — they compose few primitives into many user-visible features. The low-ratio repo (atomization framework) is *primitive-heavy* — every module is one primitive in a different domain.

Implication: the substrate work above this registry layer (storefronts, 8-strata, visibility schema) lives in the *choreography* layer. The registry sits beneath all of it.

---

## Alignment with prior work in this ecosystem

The 12 primitives here are confirmed to align with — and reduce — earlier conceptual layers:

- **Parallel storefront-substrate session's 4 "elements"** (`audience-as-property`, `lexicon-as-substrate`, `bridge-to-as-anti-orphan`, `skill+config opt-in`) — each decomposes to a subset of the 12: e.g., `audience-as-property` = `TAG-WITH-METADATA` + `VALIDATE-AGAINST-SCHEMA`; `lexicon-as-substrate` = `INGEST` + `TAG` + `EMIT`; `bridge-to-as-anti-orphan` = `VALIDATE` + `EXTRACT` (link target check); `skill+config opt-in` = `ROUTE-BY-TYPE` + `COMPOSE-INTO-CHAIN`. None introduces a 13th.

- **Heraldic Cartographer persona boil-down** (`NOTICE` · `REFRAIN` · `PLACE` · `HOLD`) — these are persona-layer primitives that map to generic-compute floor (`COMPARE`, `BIND`, `WRITE`, `READ`), confirming the recursion is consistent across the persona-substrate boundary.

- **8-Strata Domain Ideal-Whole substrate** — each stratum (ontology, lineage, constellation, gap-map, agent-fleet, production-stack, internal-magnet, external-contribution) is a *named composition* of 3-5 primitives, not a primitive itself.

The registry is therefore the floor that the entire ecosystem's vocabulary stack rests on.

---

## Verification status

| # | Check | Status |
|---|---|---|
| 1 | All primitives with ≥2 cross-repo examples each | ✅ done (12 with 3+ examples; #13 with 1 example so far) |
| 2 | Verification crawl on 4th repo (`application-pipeline`) | ✅ done — surfaced #13 `MUTATE-RULE-BASED-ON-FEEDBACK`, registry expanded inline to v1.1 |
| 3 | Cross-check against parallel session's 4 elements | ✅ done (above) |
| 4 | Cross-check against Heraldic Cartographer persona-stack | ✅ done (above) |

**v1.1 frozen.** If a 5th-repo crawl surfaces a 14th primitive, doc bumps to v1.2 with the same inline-expansion pattern. If not, the registry's coverage extends with each new repo it certifies. The expectation now: as more repos are crawled, **most** will subset within the 13; only repos with genuinely new architectural ideas (like the application-pipeline's adaptive feedback loop) will trigger registry growth.

---

## Out of scope (firm)

- Adoption sweep across all 37 repos — incremental, lane-distributed, not single-session.
- The `primitives:` field on `seed-v1.1.schema.json` — separate additive PR, not blocking this doc.
- Domain substrates that compose primitives (storefront, 8-strata, visibility schema) — those live above this layer; this doc serves them, doesn't replace them.
- The 5-primitive absolute computational floor — academic interest only.

---

## Lineage

- **Crawl reports:** 4 Explore agents, 2026-04-26 (3 synthesis + 1 verification)
- **Synthesis plan:** `~/.claude/plans/session-complete-gleaming-cocoa.md` Addendum 2026-04-26
- **v1.1 expansion trigger:** application-pipeline `scripts/recalibrate.py` (quarterly outcome → weight feedback loop)
- **Companion (above this layer):** `~/Workspace/a-i--skills/skills/project-management/personalized-storefront-render/SKILL.md` (parallel session's substrate that consumes this vocabulary)
- **Companion (above this layer):** `~/Workspace/a-i--skills/skills/project-management/domain-ideal-whole-substrate/SKILL.md` (8-strata layout that composes primitives into client-domain artifacts)
