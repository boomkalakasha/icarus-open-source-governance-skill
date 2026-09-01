import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TargetAuditTests(unittest.TestCase):
    def make_target(self, base: Path) -> Path:
        target = base / "target"
        target.mkdir()
        (target / "README.md").write_text(
            "# Example\n\n[简体中文](README.zh-CN.md)\n", encoding="utf-8"
        )
        (target / "README.zh-CN.md").write_text(
            "# 示例\n\n[English](README.md)\n", encoding="utf-8"
        )
        (target / "LICENSE").write_text("Example license decision\n", encoding="utf-8")
        (target / "SECURITY.md").write_text("Report privately.\n", encoding="utf-8")
        (target / ".icarus-open-source.yml").write_text(
            "schemaVersion: 1\n"
            "project:\n"
            "  name: example\n"
            "  languages: [en, zh-CN]\n"
            "target:\n"
            "  requiredFiles: [README.md, README.zh-CN.md, LICENSE, SECURITY.md]\n"
            "  readme: README.md\n"
            "  readmeZh: README.zh-CN.md\n"
            "license:\n"
            "  decision: not-applicable\n"
            "privacy:\n"
            "  scanReachableHistory: false\n"
            "  forbiddenPatterns: []\n"
            "brand:\n"
            "  mode: none\n"
            "  profile: null\n"
            "git:\n"
            "  flow: github-flow\n"
            "  commits: conventional-commits\n"
            "release:\n"
            "  versioning: semver\n"
            "  immutable: true\n"
            "evidence:\n"
            "  requireLocal: true\n"
            "  requirePublicHost: true\n",
            encoding="utf-8",
        )
        return target

    def run_audit(
        self, target: Path, *args: str, environment: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "audit_target.py"),
                "--root",
                str(target),
                "--policy",
                ".icarus-open-source.yml",
                *args,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            env=environment,
        )

    def git(self, root: Path, *args: str) -> None:
        result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_minimal_target_passes_without_requiring_governance_package_files(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            result = self.run_audit(target)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: target audit", result.stdout)
        self.assertNotIn("SKILL.md", result.stdout)

    def test_missing_required_file_holds_the_target(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            (target / "SECURITY.md").unlink()
            result = self.run_audit(target)
        self.assertEqual(1, result.returncode)
        self.assertIn("missing-required-file:SECURITY.md", result.stdout)

    def test_bilingual_navigation_must_be_reciprocal(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            (target / "README.zh-CN.md").write_text("# 示例\n", encoding="utf-8")
            result = self.run_audit(target)
        self.assertEqual(1, result.returncode)
        self.assertIn("bilingual-navigation", result.stdout)

    def test_current_tree_secret_is_reported_without_echoing_value_in_json(self):
        secret_value = "abc" + "defghijklmnop"
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            (target / "config.txt").write_text(f"to{'ken'}: {secret_value}\n", encoding="utf-8")
            result = self.run_audit(target, "--format", "json")
        self.assertEqual(1, result.returncode)
        payload = json.loads(result.stdout)
        self.assertEqual("HOLD", payload["status"])
        self.assertTrue(any(item["rule"] == "generic-secret-assignment" for item in payload["findings"]))
        self.assertNotIn(secret_value, result.stdout)

    def test_history_secret_is_detected_when_requested(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            self.git(target, "init")
            self.git(target, "config", "user.email", "audit@example.invalid")
            self.git(target, "config", "user.name", "Audit Test")
            hidden = target / "temporary.txt"
            hidden.write_text("api_" + "key = 'abcdefghijklmnop'\n", encoding="utf-8")
            self.git(target, "add", ".")
            self.git(target, "commit", "-m", "add temporary value")
            hidden.unlink()
            self.git(target, "add", "-u")
            self.git(target, "commit", "-m", "remove temporary value")
            result = self.run_audit(target, "--history")
        self.assertEqual(1, result.returncode)
        self.assertIn("history:", result.stdout)

    def test_policy_must_be_inside_the_target(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            target = self.make_target(base)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "audit_target.py"),
                    "--root",
                    str(target),
                    "--policy",
                    str(base / "outside.yml"),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(2, result.returncode)
        self.assertIn("policy must be inside target", result.stderr)

    def test_v10_policy_without_target_uses_documented_defaults(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            policy = target / ".icarus-open-source.yml"
            source = policy.read_text(encoding="utf-8")
            source = source.replace(
                "target:\n"
                "  requiredFiles: [README.md, README.zh-CN.md, LICENSE, SECURITY.md]\n"
                "  readme: README.md\n"
                "  readmeZh: README.zh-CN.md\n",
                "",
            )
            policy.write_text(source, encoding="utf-8")
            result = self.run_audit(target)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: target audit", result.stdout)

    def test_review_required_license_is_explicit_human_review_not_a_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            policy = target / ".icarus-open-source.yml"
            policy.write_text(
                policy.read_text(encoding="utf-8").replace(
                    "decision: not-applicable", "decision: review-required"
                ),
                encoding="utf-8",
            )
            result = self.run_audit(target, "--format", "json")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("HUMAN_REVIEW", payload["status"])
        self.assertTrue(
            any(item["name"] == "license-decision" and item["status"] == "HUMAN_REVIEW" for item in payload["checks"])
        )

    def test_required_missing_mature_tool_holds_instead_of_becoming_a_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            policy = target / ".icarus-open-source.yml"
            policy.write_text(
                policy.read_text(encoding="utf-8")
                + "integrations:\n"
                + "  gitleaks: required\n"
                + "  reuse: disabled\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment["PATH"] = str(target / "empty-tool-path")
            result = self.run_audit(target, "--format", "json", environment=environment)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("HOLD", payload["status"])
        self.assertTrue(
            any(item["name"] == "gitleaks" and item["status"] == "HOLD" for item in payload["checks"])
        )

    def test_optional_missing_mature_tool_requires_human_review(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            policy = target / ".icarus-open-source.yml"
            policy.write_text(
                policy.read_text(encoding="utf-8")
                + "integrations:\n"
                + "  gitleaks: optional\n"
                + "  reuse: disabled\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment["PATH"] = str(target / "empty-tool-path")
            result = self.run_audit(target, "--format", "json", environment=environment)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("HUMAN_REVIEW", payload["status"])
        self.assertTrue(
            any(item["name"] == "gitleaks" and item["status"] == "HUMAN_REVIEW" for item in payload["checks"])
        )

    def test_policy_cannot_supply_an_arbitrary_tool_command(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            policy = target / ".icarus-open-source.yml"
            policy.write_text(
                policy.read_text(encoding="utf-8")
                + "integrations:\n"
                + "  gitleaks: required\n"
                + "  reuse: disabled\n"
                + "  gitleaksCommand: powershell -Command Invoke-Expression\n",
                encoding="utf-8",
            )
            result = self.run_audit(target)
        self.assertEqual(2, result.returncode)
        self.assertIn("unknown integrations keys: gitleaksCommand", result.stderr)

    def test_drive_unc_traversal_and_ads_target_paths_are_rejected(self):
        unsafe_paths = (
            "C:/outside.txt",
            "D:outside.txt",
            "//server/share.txt",
            "/absolute.txt",
            "../outside.txt",
            "nested\\outside.txt",
            "file:outside.txt",
            "inside.txt:stream",
        )
        for unsafe in unsafe_paths:
            with self.subTest(path=unsafe), tempfile.TemporaryDirectory() as directory:
                target = self.make_target(Path(directory))
                policy = target / ".icarus-open-source.yml"
                source = policy.read_text(encoding="utf-8").replace(
                    "requiredFiles: [README.md, README.zh-CN.md, LICENSE, SECURITY.md]",
                    f"requiredFiles: [{unsafe}]",
                )
                policy.write_text(source, encoding="utf-8")
                result = self.run_audit(target)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("unsafe-required-path", result.stdout)

    def test_existing_markdown_link_outside_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            target = self.make_target(base)
            (base / "outside.md").write_text("outside\n", encoding="utf-8")
            readme = target / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8") + "\n[outside](../outside.md)\n",
                encoding="utf-8",
            )
            result = self.run_audit(target)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("unsafe relative link", result.stdout)

    def test_json_target_identity_does_not_echo_absolute_machine_path(self):
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_target(Path(directory))
            result = self.run_audit(target, "--format", "json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("target", payload["target"])
        self.assertNotIn(str(target.resolve()), result.stdout)


if __name__ == "__main__":
    unittest.main()
