import hashlib
import json
import subprocess
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


class PackageContractTests(unittest.TestCase):
    def run_package(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["pwsh", "-NoProfile", "-File", str(ROOT / "scripts" / "package.ps1"), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_dot_prefixed_package_entries_are_read_with_force_on_unix(self):
        source = (ROOT / "scripts" / "package.ps1").read_text(encoding="utf-8")
        self.assertIn("Get-Item -LiteralPath $source -Force", source)

    def test_release_workflow_uploads_only_the_tagged_archive(self):
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertNotIn("dist/*.zip", workflow)
        self.assertIn('"dist/icarus-open-source-governance-${version}.zip"', workflow)

    def test_one_staged_tree_produces_matching_skill_and_zip_manifests(self):
        result = self.run_package()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        manifest = json.loads((DIST / "manifest.json").read_text(encoding="utf-8"))
        self.assertIn(manifest["sourceTree"], {"clean", "dirty"})
        archives = [DIST / artifact["name"] for artifact in manifest["artifacts"]]
        self.assertEqual(2, len(archives))
        self.assertTrue(all(path.is_file() for path in archives))
        archive_names = []
        for path in archives:
            with zipfile.ZipFile(path) as archive:
                archive_names.append(sorted(archive.namelist()))
        self.assertEqual(archive_names[0], archive_names[1])
        self.assertTrue(
            {
                ".icarus-open-source.example.yml",
                "assets/brand/boomkalakasha/avatar.png",
                "assets/brand/boomkalakasha/watermark-dark.svg",
                "docs/brand/preview.html",
            }.issubset(set(archive_names[0]))
        )
        for artifact, path in zip(manifest["artifacts"], archives):
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), artifact["sha256"])
        sums = (DIST / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(
            {f"{artifact['sha256']}  {artifact['name']}" for artifact in manifest["artifacts"]},
            set(sums),
        )

    def test_explicit_semver_version_controls_the_archive_name_and_manifest(self):
        first = self.run_package("-Version", "1.0.0")
        self.assertEqual(0, first.returncode, first.stdout + first.stderr)
        result = self.run_package("-Version", "1.0.1")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        manifest = json.loads((DIST / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("1.0.1", manifest["version"])
        self.assertIn("icarus-open-source-governance-1.0.1.zip", [artifact["name"] for artifact in manifest["artifacts"]])
        self.assertEqual(
            ["icarus-open-source-governance-1.0.1.zip"],
            sorted(path.name for path in DIST.glob("icarus-open-source-governance-*.zip")),
        )


if __name__ == "__main__":
    unittest.main()
