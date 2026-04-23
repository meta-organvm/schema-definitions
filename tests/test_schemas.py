"""Test JSON Schema definitions against example files."""

import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import yaml

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "schemas"
EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


def load_schema(name: str) -> dict:
    with open(SCHEMAS_DIR / name) as f:
        return json.load(f)


def validate(data: dict, schema: dict) -> list[str]:
    validator = jsonschema.Draft202012Validator(schema)
    return [e.message for e in validator.iter_errors(data)]


class TestRegistrySchema:
    def test_example_validates(self):
        schema = load_schema("registry-v2.schema.json")
        with open(EXAMPLES_DIR / "registry-minimal.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_version_fails(self):
        schema = load_schema("registry-v2.schema.json")
        data = {"organs": {}}
        errors = validate(data, schema)
        assert any("version" in e for e in errors)

    def test_invalid_organ_key_fails(self):
        schema = load_schema("registry-v2.schema.json")
        data = {
            "version": "2.0",
            "schema_version": "0.5",
            "organs": {
                "BAD-KEY": {"name": "Bad", "repositories": []}
            },
        }
        errors = validate(data, schema)
        assert len(errors) > 0

    def test_repo_missing_required_fails(self):
        schema = load_schema("registry-v2.schema.json")
        data = {
            "version": "2.0",
            "schema_version": "0.5",
            "organs": {
                "ORGAN-I": {
                    "name": "Theory",
                    "repositories": [{"name": "test"}],
                }
            },
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestSeedSchema:
    def test_example_validates(self):
        schema = load_schema("seed-v1.schema.json")
        with open(EXAMPLES_DIR / "seed-minimal.yaml") as f:
            data = yaml.safe_load(f)
        assert validate(data, schema) == []

    def test_missing_organ_fails(self):
        schema = load_schema("seed-v1.schema.json")
        data = {"schema_version": "1.0", "repo": "x", "org": "y"}
        errors = validate(data, schema)
        assert any("organ" in e for e in errors)


class TestDispatchSchema:
    def test_example_validates(self):
        schema = load_schema("dispatch-payload.schema.json")
        with open(EXAMPLES_DIR / "dispatch-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_event_fails(self):
        schema = load_schema("dispatch-payload.schema.json")
        data = {
            "source": {"organ": "ORGAN-I"},
            "target": {"organ": "ORGAN-II"},
            "payload": {},
        }
        errors = validate(data, schema)
        assert any("event" in e for e in errors)


class TestSoakTestSchema:
    def test_minimal_validates(self):
        schema = load_schema("soak-test.schema.json")
        data = {
            "date": "2026-02-17",
            "collected_at": "2026-02-17T12:00:00Z",
            "validation": {
                "registry_pass": True,
                "dependency_pass": True,
            },
            "ci": {
                "total_checked": 71,
                "passing": 53,
                "failing": 18,
            },
        }
        assert validate(data, schema) == []


class TestSystemMetricsSchema:
    def test_minimal_validates(self):
        schema = load_schema("system-metrics.schema.json")
        data = {
            "schema_version": "1.0",
            "generated": "2026-02-17T12:00:00Z",
            "computed": {
                "total_repos": 97,
                "active_repos": 87,
                "archived_repos": 10,
                "total_organs": 8,
                "operational_organs": 8,
            },
            "manual": {},
        }
        assert validate(data, schema) == []


class TestGovernanceRulesSchema:
    def test_minimal_validates(self):
        schema = load_schema("governance-rules.schema.json")
        data = {
            "version": "1.0",
            "dependency_rules": {
                "max_transitive_depth": 4,
                "no_circular_dependencies": True,
                "no_back_edges": True,
            },
            "promotion_rules": {},
            "state_machine": {
                "states": ["LOCAL", "CANDIDATE"],
                "transitions": {"LOCAL": ["CANDIDATE"]},
            },
            "audit_thresholds": {},
        }
        assert validate(data, schema) == []


class TestEcosystemSchema:
    def test_example_validates(self):
        schema = load_schema("ecosystem-v1.schema.json")
        with open(EXAMPLES_DIR / "ecosystem-example.yaml") as f:
            data = yaml.safe_load(f)
        assert validate(data, schema) == []

    def test_missing_repo_fails(self):
        schema = load_schema("ecosystem-v1.schema.json")
        data = {"schema_version": "1.0", "organ": "III"}
        errors = validate(data, schema)
        assert any("repo" in e for e in errors)

    def test_missing_status_in_arm_fails(self):
        schema = load_schema("ecosystem-v1.schema.json")
        data = {
            "schema_version": "1.0",
            "repo": "x",
            "organ": "III",
            "delivery": [{"platform": "web_app"}],
        }
        errors = validate(data, schema)
        assert any("status" in e for e in errors)

    def test_invalid_status_fails(self):
        schema = load_schema("ecosystem-v1.schema.json")
        data = {
            "schema_version": "1.0",
            "repo": "x",
            "organ": "III",
            "delivery": [{"platform": "web_app", "status": "INVALID"}],
        }
        errors = validate(data, schema)
        assert len(errors) > 0

    def test_custom_pillar_accepted(self):
        schema = load_schema("ecosystem-v1.schema.json")
        data = {
            "schema_version": "1.0",
            "repo": "x",
            "organ": "III",
            "partnerships": [{"platform": "aws", "status": "planned"}],
        }
        assert validate(data, schema) == []

    def test_additional_arm_properties_accepted(self):
        schema = load_schema("ecosystem-v1.schema.json")
        data = {
            "schema_version": "1.0",
            "repo": "x",
            "organ": "III",
            "revenue": [
                {"platform": "subscription", "status": "live", "stripe_id": "prod_123"},
            ],
        }
        assert validate(data, schema) == []


class TestSystemOrganismSchema:
    def test_example_validates(self):
        schema = load_schema("system-organism.schema.json")
        with open(EXAMPLES_DIR / "system-organism-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_organs_fails(self):
        schema = load_schema("system-organism.schema.json")
        data = {"total_repos": 1, "sys_pct": 50, "generated": "2026-03-06T12:00:00+00:00"}
        errors = validate(data, schema)
        assert any("organs" in e for e in errors)

    def test_missing_generated_fails(self):
        schema = load_schema("system-organism.schema.json")
        data = {"total_repos": 1, "sys_pct": 50, "organs": []}
        errors = validate(data, schema)
        assert any("generated" in e for e in errors)

    def test_invalid_sys_pct_fails(self):
        schema = load_schema("system-organism.schema.json")
        data = {
            "total_repos": 1,
            "sys_pct": 200,
            "organs": [],
            "generated": "2026-03-06T12:00:00+00:00",
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestPulseEventSchema:
    def test_example_validates(self):
        schema = load_schema("pulse-event.schema.json")
        with open(EXAMPLES_DIR / "pulse-event-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_ontologia_event_validates(self):
        """Pulse event schema is a superset of ontologia events."""
        schema = load_schema("pulse-event.schema.json")
        with open(EXAMPLES_DIR / "ontologia-event-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_invalid_event_type_fails(self):
        schema = load_schema("pulse-event.schema.json")
        data = {
            "event_type": "not.a.real.event",
            "source": "test",
            "timestamp": "2026-03-13T10:00:00Z",
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestConversationCorpusSurfaceManifestSchema:
    def test_example_validates(self):
        schema = load_schema("conversation-corpus-surface-manifest.schema.json")
        with open(EXAMPLES_DIR / "conversation-corpus-surface-manifest-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_registry_fails(self):
        schema = load_schema("conversation-corpus-surface-manifest.schema.json")
        data = {
            "contract_name": "conversation-corpus-engine-surface-manifest-v1",
            "contract_version": 1,
            "generated_at": "2026-03-21T12:00:00Z",
            "engine": {
                "package": "conversation-corpus-engine",
                "version": "0.1.0",
                "repo_root": "/tmp/cce",
            },
            "project": {
                "project_root": "/tmp/cce",
                "source_drop_root": "/tmp/source-drop",
                "organ": "ORGAN-I",
                "system_role": "conversation-corpus-engine",
            },
            "schemas": [],
            "cli_surfaces": [],
            "providers": [],
            "artifacts": {
                "registry_path": "/tmp/cce/state/corpus-registry.json",
                "promotion_policy_path": "/tmp/cce/state/promotion-policy.json",
                "federation_summary_path": "/tmp/cce/federation/federation-summary.md",
                "policy_replay_latest_json_path": "/tmp/cce/state/policy-replay-latest.json",
                "policy_candidate_latest_json_path": "/tmp/cce/state/policy-candidate-latest.json",
                "policy_application_latest_json_path": "/tmp/cce/state/policy-application-latest.json",
                "corpus_candidate_latest_json_path": "/tmp/cce/state/corpus-candidate-latest.json",
                "corpus_promotion_latest_json_path": "/tmp/cce/state/corpus-promotion-latest.json",
                "corpus_live_pointer_path": "/tmp/cce/state/corpus-live-pointer.json",
                "source_policy_paths": {},
                "provider_refresh_latest_json_paths": {},
            },
        }
        errors = validate(data, schema)
        assert any("registry" in e for e in errors)


class TestConversationCorpusMcpContextSchema:
    def test_example_validates(self):
        schema = load_schema("conversation-corpus-mcp-context.schema.json")
        with open(EXAMPLES_DIR / "conversation-corpus-mcp-context-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_summary_field_fails(self):
        schema = load_schema("conversation-corpus-mcp-context.schema.json")
        data = {
            "contract_name": "conversation-corpus-engine-mcp-context-v1",
            "contract_version": 1,
            "generated_at": "2026-03-21T12:00:00Z",
            "project_root": "/tmp/cce",
            "source_drop_root": "/tmp/source-drop",
            "summary": {
                "registered_corpus_count": 1,
                "active_corpus_count": 1,
                "provider_count": 1,
                "healthy_provider_count": 1,
                "refresh_recommended_count": 0,
            },
            "registry": {"default_corpus_id": None, "corpora": []},
            "providers": [],
            "governance": {
                "promotion_policy": {},
                "latest_policy_replay": None,
                "latest_policy_candidate": None,
                "latest_policy_application": None,
                "latest_corpus_candidate": None,
                "latest_corpus_promotion": None,
            },
            "latest_events": {
                "latest_corpus_live_pointer": None,
                "latest_policy_live_pointer": None,
                "latest_provider_refreshes": {},
            },
            "review_queue": {"open_count": 0, "items": []},
            "schema_catalog": [],
        }
        errors = validate(data, schema)
        assert any("open_review_count" in e for e in errors)


class TestConversationCorpusSurfaceBundleSchema:
    def test_example_validates(self):
        schema = load_schema("conversation-corpus-surface-bundle.schema.json")
        with open(EXAMPLES_DIR / "conversation-corpus-surface-bundle-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_context_fails(self):
        schema = load_schema("conversation-corpus-surface-bundle.schema.json")
        data = {
            "contract_name": "conversation-corpus-engine-surface-bundle-v1",
            "contract_version": 1,
            "generated_at": "2026-03-21T12:00:00Z",
            "project_root": "/tmp/cce",
            "source_drop_root": "/tmp/source-drop",
            "summary": {"valid": True, "error_count": 0},
            "manifest": {
                "schema_name": "surface-manifest",
                "path": "/tmp/cce/reports/surfaces/surface-manifest.json",
                "markdown_path": "/tmp/cce/reports/surfaces/surface-manifest.md",
                "valid": True,
                "error_count": 0,
                "errors": [],
            },
        }
        errors = validate(data, schema)
        assert any("context" in e for e in errors)

    def test_missing_source_fails(self):
        schema = load_schema("pulse-event.schema.json")
        data = {
            "event_type": "pulse.heartbeat",
            "timestamp": "2026-03-13T10:00:00Z",
        }
        errors = validate(data, schema)
        assert any("source" in e for e in errors)


class TestAmmoiSchema:
    def test_example_validates(self):
        schema = load_schema("ammoi-v1.schema.json")
        with open(EXAMPLES_DIR / "ammoi-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_organs_fails(self):
        schema = load_schema("ammoi-v1.schema.json")
        data = {
            "timestamp": "2026-03-13T15:00:00Z",
            "system_density": 0.5,
            "total_entities": 10,
        }
        errors = validate(data, schema)
        assert any("organs" in e for e in errors)

    def test_density_out_of_range_fails(self):
        schema = load_schema("ammoi-v1.schema.json")
        data = {
            "timestamp": "2026-03-13T15:00:00Z",
            "system_density": 1.5,
            "total_entities": 10,
            "organs": {},
        }
        errors = validate(data, schema)
        assert len(errors) > 0

    def test_minimal_organ_validates(self):
        schema = load_schema("ammoi-v1.schema.json")
        data = {
            "timestamp": "2026-03-13T15:00:00Z",
            "system_density": 0.5,
            "total_entities": 10,
            "organs": {
                "ORGAN-I": {
                    "organ_id": "ORGAN-I",
                    "organ_name": "Theory",
                }
            },
        }
        assert validate(data, schema) == []

    def test_organ_extra_fields_rejected(self):
        schema = load_schema("ammoi-v1.schema.json")
        data = {
            "timestamp": "2026-03-13T15:00:00Z",
            "system_density": 0.5,
            "total_entities": 10,
            "organs": {
                "ORGAN-I": {
                    "organ_id": "ORGAN-I",
                    "organ_name": "Theory",
                    "bogus_field": 99,
                }
            },
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestOrganDefinitionsSchema:
    def test_example_validates(self):
        schema = load_schema("organ-definitions.schema.json")
        with open(EXAMPLES_DIR / "organ-definitions-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_organs_fails(self):
        schema = load_schema("organ-definitions.schema.json")
        data = {"schema_version": "1.0"}
        errors = validate(data, schema)
        assert any("organs" in e for e in errors)

    def test_invalid_organ_key_fails(self):
        schema = load_schema("organ-definitions.schema.json")
        data = {
            "schema_version": "1.0",
            "organs": {
                "BAD-KEY": {
                    "name": "Bad",
                    "domain_boundary": "x" * 25,
                    "inclusion_criteria": ["a", "b", "c"],
                    "exclusion_criteria": [
                        {"condition": "x", "redirect": "y"},
                        {"condition": "z", "redirect": "w"},
                    ],
                    "canonical_repo_types": ["a", "b"],
                    "boundary_tests": [
                        {"question": "q?", "expected": True},
                        {"question": "r?", "expected": False},
                    ],
                }
            },
        }
        errors = validate(data, schema)
        assert len(errors) > 0

    def test_missing_required_organ_fields_fails(self):
        schema = load_schema("organ-definitions.schema.json")
        data = {
            "schema_version": "1.0",
            "organs": {
                "ORGAN-I": {"name": "Theory"},
            },
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestExcavationReportSchema:
    def test_example_validates(self):
        schema = load_schema("excavation-report.schema.json")
        with open(EXAMPLES_DIR / "excavation-report-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_findings_fails(self):
        schema = load_schema("excavation-report.schema.json")
        data = {"scanned_repos": 10, "total_findings": 0}
        errors = validate(data, schema)
        assert any("findings" in e for e in errors)

    def test_invalid_entity_type_fails(self):
        schema = load_schema("excavation-report.schema.json")
        data = {
            "scanned_repos": 1,
            "total_findings": 1,
            "findings": [
                {
                    "repo": "test",
                    "organ": "ORGAN-I",
                    "entity_path": "x",
                    "entity_type": "invalid_type",
                    "severity": "warning",
                },
            ],
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestUaksSourceObjectSchema:
    def test_example_validates(self):
        schema = load_schema("uaks-source-object.schema.json")
        with open(EXAMPLES_DIR / "uaks-source-object-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_checksum_fails(self):
        schema = load_schema("uaks-source-object.schema.json")
        data = {
            "sourceId": "src_test",
            "sourceType": "raw_text",
            "origin": "/tmp/test.md",
            "ingestedAt": "2026-04-23T00:00:00Z",
            "mimeType": "text/markdown",
            "rawArchiveRef": "cas_abc123",
        }
        errors = validate(data, schema)
        assert any("checksum" in e for e in errors)

    def test_invalid_source_type_fails(self):
        schema = load_schema("uaks-source-object.schema.json")
        data = {
            "sourceId": "src_test",
            "sourceType": "invalid_type",
            "origin": "/tmp/test.md",
            "ingestedAt": "2026-04-23T00:00:00Z",
            "checksum": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "mimeType": "text/markdown",
            "rawArchiveRef": "cas_abc123",
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestUaksTextAtomSchema:
    def test_example_validates(self):
        schema = load_schema("uaks-text-atom.schema.json")
        with open(EXAMPLES_DIR / "uaks-text-atom-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_content_fails(self):
        schema = load_schema("uaks-text-atom.schema.json")
        data = {
            "atomId": "ta_test",
            "atomFamily": "text",
            "atomClass": "claim",
            "contentHash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "sourceRef": "src_test",
            "validationState": "DRAFT",
            "createdAt": "2026-04-23T00:00:00Z",
        }
        errors = validate(data, schema)
        assert any("content" in e for e in errors)

    def test_invalid_validation_state_fails(self):
        schema = load_schema("uaks-text-atom.schema.json")
        data = {
            "atomId": "ta_test",
            "atomFamily": "text",
            "atomClass": "claim",
            "content": "Test content",
            "contentHash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "sourceRef": "src_test",
            "validationState": "INVALID_STATE",
            "createdAt": "2026-04-23T00:00:00Z",
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestUaksCodeAtomSchema:
    def test_example_validates(self):
        schema = load_schema("uaks-code-atom.schema.json")
        with open(EXAMPLES_DIR / "uaks-code-atom-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_wrong_atom_family_fails(self):
        schema = load_schema("uaks-code-atom.schema.json")
        data = {
            "atomId": "ca_test",
            "atomFamily": "text",
            "codeKind": "function",
            "content": "def foo(): pass",
            "contentHash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "sourceRef": "src_test",
            "validationState": "DRAFT",
            "createdAt": "2026-04-23T00:00:00Z",
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestUaksAssemblyRecipeSchema:
    def test_example_validates(self):
        schema = load_schema("uaks-assembly-recipe.schema.json")
        with open(EXAMPLES_DIR / "uaks-assembly-recipe-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_empty_atom_sequence_fails(self):
        schema = load_schema("uaks-assembly-recipe.schema.json")
        data = {
            "recipeId": "rcp_test",
            "recipeType": "summary",
            "atomSequence": [],
            "resolutionLevel": "standard",
            "createdAt": "2026-04-23T00:00:00Z",
        }
        errors = validate(data, schema)
        assert len(errors) > 0


class TestUaksValidationEventSchema:
    def test_example_validates(self):
        schema = load_schema("uaks-validation-event.schema.json")
        with open(EXAMPLES_DIR / "uaks-validation-event-example.json") as f:
            data = json.load(f)
        assert validate(data, schema) == []

    def test_missing_reviewer_fails(self):
        schema = load_schema("uaks-validation-event.schema.json")
        data = {
            "eventId": "vev_test",
            "atomId": "ta_test",
            "fromState": "DRAFT",
            "toState": "DISTILLED",
            "timestamp": "2026-04-23T00:00:00Z",
        }
        errors = validate(data, schema)
        assert any("reviewer" in e for e in errors)


class TestValidateScriptAutoDetect:
    def test_detects_system_organism_and_pillar_dna_examples(self):
        script = Path(__file__).resolve().parent.parent / "scripts" / "validate.py"
        organism = EXAMPLES_DIR / "system-organism-example.json"
        pillar = EXAMPLES_DIR / "pillar-dna-example.yaml"
        result = subprocess.run(
            [sys.executable, str(script), str(organism), str(pillar)],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stdout + result.stderr
        assert "PASS system-organism-example.json" in result.stdout
        assert "PASS pillar-dna-example.yaml" in result.stdout
