import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicRiskScannerTests(unittest.TestCase):
    def run_scanner(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "scan_public_risks.py"), "--root", str(root), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def git(self, root: Path, *args: str) -> None:
        result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_current_tree_reports_a_credential_like_assignment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config.txt").write_text("api_" + "key = 'abcdefghijklmnop'\n", encoding="utf-8")
            result = self.run_scanner(root)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("generic-secret-assignment", result.stdout)
        self.assertIn("config.txt", result.stdout)

    def test_negative_security_assertion_is_not_reported_as_a_leak(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "test_scan.py").write_text('assert "BEGIN PRIVATE KEY" not in output\n', encoding="utf-8")
            result = self.run_scanner(root)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: current tree", result.stdout)

    def test_config_supplies_project_specific_patterns(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".icarus-open-source.yml").write_text(
                "privacy:\n  scanReachableHistory: false\n  forbiddenPatterns: [PROJECT_ONLY_MARKER]\n",
                encoding="utf-8",
            )
            (root / "notes.txt").write_text("PROJECT_ONLY_MARKER\n", encoding="utf-8")
            result = self.run_scanner(root, "--config", ".icarus-open-source.yml")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("custom-1", result.stdout)

    def test_current_tree_reports_private_network_markers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "deploy.txt").write_text("endpoint=https://10." + "42.0.5\n", encoding="utf-8")
            result = self.run_scanner(root)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("private-ipv4", result.stdout)

    def test_reachable_history_detects_a_deleted_secret(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.git(root, "init")
            self.git(root, "config", "user.email", "tests@example.invalid")
            self.git(root, "config", "user.name", "Scanner Test")
            target = root / "settings.txt"
            target.write_text("to" + "ken: abcdefghijklmnop\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "add temporary setting")
            target.write_text("safe: true\n", encoding="utf-8")
            self.git(root, "add", ".")
            self.git(root, "commit", "-m", "remove secret")
            result = self.run_scanner(root, "--history")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("history", result.stdout)
        self.assertIn("generic-secret-assignment", result.stdout)


if __name__ == "__main__":
    unittest.main()
