import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_release_docs.py"
REPOSITORY = "example/project"


class ReleaseDocumentationGateTests(unittest.TestCase):
    def run_gate(self, *, tag="v1.2.3", version="1.2.3", repository=REPOSITORY, readmes=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = []
            for index, source in enumerate(readmes or [self.valid_readme("English"), self.valid_readme("中文")]):
                path = root / f"README-{index}.md"
                path.write_text(source, encoding="utf-8")
                paths.extend(["--readme", str(path)])
            return subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--tag",
                    tag,
                    "--version",
                    version,
                    "--repository",
                    repository,
                    *paths,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

    @staticmethod
    def valid_readme(title):
        return f"""# {title}

<!-- icarus-release-fact: dynamic -->
Public releases: [latest](https://github.com/{REPOSITORY}/releases/latest) ·
[all](https://github.com/{REPOSITORY}/releases).
"""

    def test_accepts_matching_semver_and_dynamic_release_links(self):
        result = self.run_gate()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: release documentation matches v1.2.3", result.stdout)

    def test_repository_readmes_satisfy_the_current_source_version_contract(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        result = self.run_gate(
            tag=f"v{version}",
            version=version,
            repository="boomkalakasha/icarus-open-source-governance-skill",
            readmes=[
                (ROOT / "README.md").read_text(encoding="utf-8"),
                (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
            ],
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertLess(english.index("## What you get"), english.index("## What it covers"))
        self.assertIn("Illustrative evidence summary", english)
        self.assertIn("privacy, provenance, documentation, licensing, and release evidence", english)
        self.assertLess(chinese.index("## 你会得到什么"), chinese.index("## 覆盖范围"))
        self.assertIn("示意证据摘要", chinese)
        self.assertIn("隐私、来源、文档、许可证和发布证据", chinese)

    def test_rejects_tag_and_source_version_mismatch(self):
        result = self.run_gate(version="1.2.4")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("does not match source version", result.stderr)

    def test_rejects_missing_dynamic_marker_or_latest_link(self):
        missing_marker = self.valid_readme("English").replace(
            "<!-- icarus-release-fact: dynamic -->", ""
        )
        missing_latest = self.valid_readme("中文").replace("/releases/latest", "/releases/tag/v1.2.3")
        result = self.run_gate(readmes=[missing_marker, missing_latest])
        self.assertNotEqual(0, result.returncode)
        self.assertIn("dynamic release fact marker", result.stderr)
        self.assertIn("releases/latest", result.stderr)

    def test_rejects_a_missing_complete_release_history_link(self):
        missing_history = self.valid_readme("English").replace(
            f"[all](https://github.com/{REPOSITORY}/releases).", ""
        )
        result = self.run_gate(readmes=[missing_history, self.valid_readme("中文")])
        self.assertNotEqual(0, result.returncode)
        self.assertIn("complete release history link", result.stderr)

    def test_rejects_hard_coded_latest_stable_release_claims(self):
        claims = (
            "The latest public stable release is v1.2.3.",
            "Latest release is v1.2.3.",
            "Current version: v1.2.3.",
            "最新公开稳定版是 v1.2.3。",
            "最新版本是 v1.2.3。",
            "最新发布：v1.2.3。",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                result = self.run_gate(
                    readmes=[self.valid_readme("English") + f"\n{claim}\n"]
                )
                self.assertNotEqual(0, result.returncode)
                self.assertIn("hard-coded latest stable release claim", result.stderr)

    def test_rejects_prerelease_and_loose_semver_tags(self):
        for tag in ("1.2.3", "v1.2", "v1.2.3-rc.1", "v01.2.3"):
            with self.subTest(tag=tag):
                result = self.run_gate(tag=tag)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("stable SemVer", result.stderr)


if __name__ == "__main__":
    unittest.main()
