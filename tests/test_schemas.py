"""Test JSON Schema definitions against example files."""

import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest
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
