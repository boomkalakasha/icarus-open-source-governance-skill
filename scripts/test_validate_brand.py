import re
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_brand  # noqa: E402

BRAND = ROOT / "assets" / "brand" / "boomkalakasha"
DOC = ROOT / "docs" / "brand" / "preview.html"
WORDMARK = "BOOMKALAKASHA"
PALETTE = {"#10162F", "#35D6FF", "#FFB65A", "#FF6B6B", "#F7F4EC"}
REQUIRED = (
    "brand-mark.svg",
    "avatar.svg",
    "avatar.png",
    "watermark-dark.svg",
    "watermark-light.svg",
    "brand-preview.png",
    "brand-guidelines.md",
)


class BrandContractTests(unittest.TestCase):
    def test_required_assets_exist(self):
        missing = [name for name in REQUIRED if not (BRAND / name).is_file()]
        self.assertEqual([], missing, f"missing brand assets: {missing}")
        self.assertTrue(DOC.is_file(), "missing docs/brand/preview.html")

    def test_svg_contract_and_wordmark(self):
        for name in ("brand-mark.svg", "avatar.svg", "watermark-dark.svg", "watermark-light.svg"):
            path = BRAND / name
            self.assertTrue(path.is_file(), name)
            text = path.read_text(encoding="utf-8")
            root = ET.fromstring(text)
            self.assertIn("viewBox", root.attrib, name)
            self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}title"), name)
            self.assertIsNotNone(root.find("{http://www.w3.org/2000/svg}desc"), name)
            self.assertNotRegex(text, re.compile(r"<script|data:|file:|[A-Za-z]:\\|metadata|inkscape|sodipodi", re.I), name)
            self.assertNotRegex(text, re.compile(r"https?://(?!www\.w3\.org/2000/svg)", re.I), name)
            for color in PALETTE:
                self.assertIn(color, text, f"{name} missing palette color {color}")
        for name in ("watermark-dark.svg", "watermark-light.svg"):
            self.assertIn(WORDMARK, (BRAND / name).read_text(encoding="utf-8"), name)

    def test_png_dimensions_alpha_and_preview_size(self):
        avatar = validate_brand.read_png_contract(BRAND / "avatar.png")
        preview = validate_brand.read_png_contract(BRAND / "brand-preview.png")
        self.assertEqual((1024, 1024), avatar["size"])
        self.assertTrue(avatar["has_alpha"], "avatar.png must preserve alpha")
        self.assertEqual((1600, 900), preview["size"])
        self.assertEqual([], avatar["metadata"])
        self.assertEqual([], preview["metadata"])

    def test_wordmark_and_no_remote_content_in_specimen(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertIn(WORDMARK, text)
        self.assertIn("Warm systems. Bold momentum.", text)
        self.assertNotRegex(text, re.compile(r"<script|https?://|//[^/]|[A-Za-z]:\\|file:", re.I))

    def test_mobile_overflow_and_intentional_hero_wordmark_contract(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertRegex(text, re.compile(r'<h1[^>]*class="wordmark"[^>]*>\s*BOOMKALAKASHA\s*</h1>', re.I))
        self.assertIn(".wordmark {", text)
        self.assertIn("white-space: nowrap", text)
        self.assertIn("max-width: 100%", text)
        self.assertIn("min-width: 0", text)
        self.assertNotIn("min-width: 650px", text)
        self.assertNotIn("min-width: 560px", text)

    def test_hero_decorative_pseudo_is_contained(self):
        text = DOC.read_text(encoding="utf-8")
        hero = re.search(r"\.hero\s*\{(?P<body>.*?)\n\s*\}", text, re.S)
        self.assertIsNotNone(hero, "hero rule missing")
        self.assertRegex(hero.group("body"), r"overflow:\s*(?:clip|hidden)\s*;", "hero must clip its decorative overflow")

    def test_canonical_watermark_references_and_terminal_dot(self):
        text = DOC.read_text(encoding="utf-8")
        for name in ("watermark-dark.svg", "watermark-light.svg"):
            self.assertIn(f"../../assets/brand/boomkalakasha/{name}", text, name)
            source = (BRAND / name).read_text(encoding="utf-8")
            self.assertIn('circle cx="211" cy="126" r="4" fill="#35D6FF"', source, name)
        watermark_section = text.split('<section aria-labelledby="watermark-heading">', 1)[1].split("</section>", 1)[0]
        self.assertNotIn("<text", watermark_section, "watermark markup must come from canonical SVG assets")

    def test_validator_passes(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_brand.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
