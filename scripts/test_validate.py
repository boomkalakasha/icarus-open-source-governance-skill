import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate  # noqa: E402


class ValidateContractTests(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate.py"), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_schema_requires_the_public_governance_sections(self):
        schema = json.loads((ROOT / "schemas" / "icarus-open-source.schema.json").read_text(encoding="utf-8"))
        self.assertTrue(
            {"schemaVersion", "project", "license", "privacy", "brand", "git", "release", "evidence"}.issubset(
                set(schema["required"])
            )
        )
        self.assertEqual(["none", "subtle", "full"], schema["properties"]["brand"]["properties"]["mode"]["enum"])

    def test_example_config_is_generic_and_brand_disabled(self):
        result = self.run_validator("--config", ".icarus-open-source.example.yml")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: configuration contract", result.stdout)
        source = (ROOT / ".icarus-open-source.example.yml").read_text(encoding="utf-8")
        self.assertIn("mode: none", source)
        self.assertIn("profile: null", source)
        self.assertNotIn("BOOMKALAKASHA", source)

    def test_repository_validator_checks_bilingual_navigation_and_optional_branding(self):
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: bilingual navigation", result.stdout)
        self.assertIn("PASS: optional brand configuration", result.stdout)

    def test_templates_never_force_the_example_personal_brand(self):
        for path in (ROOT / "templates").glob("*.md"):
            self.assertNotIn("BOOMKALAKASHA", path.read_text(encoding="utf-8"), path.name)

    def test_validator_requires_community_files_and_pinned_workflows(self):
        required = set(validate.REQUIRED_FILES)
        self.assertTrue(
            {
                "templates/README.md",
                "templates/README.zh-CN.md",
                ".github/CODEOWNERS",
                ".github/dependabot.yml",
                ".github/PULL_REQUEST_TEMPLATE.md",
                ".github/workflows/ci.yml",
                ".github/workflows/codeql.yml",
                ".github/workflows/release.yml",
            }.issubset(required)
        )

    def test_validator_rejects_an_unpinned_action_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate"
            shutil.copytree(ROOT, candidate, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", "*.pyc"))
            workflow = candidate / ".github" / "workflows" / "ci.yml"
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace(
                    "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1", "actions/checkout@v7"
                ),
                encoding="utf-8",
            )
            result = self.run_validator("--root", str(candidate), "--config", ".icarus-open-source.example.yml")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("action reference must be pinned", result.stdout)

    def test_ci_fetches_reachable_history_before_claiming_a_history_scan(self):
        source = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("fetch-depth: 0", source)
        self.assertIn("scan_public_risks.py --history", source)

    def test_release_workflow_requires_a_tag_commit_reachable_from_main(self):
        source = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn("merge-base --is-ancestor", source)

    def test_validator_requires_a_semver_version_source_and_release_checks_it(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate"
            shutil.copytree(ROOT, candidate, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", "*.pyc"))
            (candidate / "VERSION").write_text("not-a-semver\n", encoding="utf-8")
            result = self.run_validator("--root", str(candidate), "--config", ".icarus-open-source.example.yml")

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("VERSION must be stable SemVer", result.stdout)
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn('version_file="$(tr -d', workflow)

    def test_release_changelog_records_the_current_version_source(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertEqual("1.0.2", (ROOT / "VERSION").read_text(encoding="utf-8").strip())
        self.assertIn("## [1.0.2] - 2026-08-26", changelog)
        self.assertNotIn("## [Unreleased]", changelog)


if __name__ == "__main__":
    unittest.main()
