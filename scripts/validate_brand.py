"""Validate the deterministic BOOMKALAKASHA brand kit."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets" / "brand" / "boomkalakasha"
SPECIMEN = ROOT / "docs" / "brand" / "preview.html"
WORDMARK = "BOOMKALAKASHA"
PALETTE = ("#10162F", "#35D6FF", "#FFB65A", "#FF6B6B", "#F7F4EC")
SVG_NAMES = ("brand-mark.svg", "avatar.svg", "watermark-dark.svg", "watermark-light.svg")
REQUIRED_NAMES = SVG_NAMES + (
    "avatar.png",
    "brand-preview.png",
    "brand-guidelines.md",
)
FORBIDDEN_SVG = (
    re.compile(r"<script\b", re.I),
    re.compile(r"(?:data:|file:)", re.I),
    re.compile(r"https?://(?!www\.w3\.org/2000/svg)", re.I),
    re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]"),
    re.compile(r"/(?:Users|home|tmp|var)/", re.I),
    re.compile(r"<(?:metadata|image)\b", re.I),
    re.compile(r"(?:inkscape|sodipodi)", re.I),
)
FORBIDDEN_HTML = (
    re.compile(r"<script\b", re.I),
    re.compile(r"https?://", re.I),
    re.compile(r"(?:data:|file:)", re.I),
    re.compile(r"[A-Za-z]:[\\/]"),
    re.compile(r"/(?:Users|home|tmp|var)/", re.I),
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate() -> list[str]:
    errors: list[str] = []

    for name in REQUIRED_NAMES:
        if not (BRAND / name).is_file():
            errors.append(f"missing asset: {name}")
    if not SPECIMEN.is_file():
        errors.append("missing specimen: docs/brand/preview.html")
    if errors:
        return errors

    svg_sources: dict[str, str] = {}
    for name in SVG_NAMES:
        path = BRAND / name
        source = _read(path)
        svg_sources[name] = source
        try:
            root = ET.fromstring(source)
        except ET.ParseError as exc:
            errors.append(f"{name}: invalid XML ({exc})")
            continue
        if not root.tag.endswith("svg"):
            errors.append(f"{name}: root element is not svg")
        view_box = root.get("viewBox", "").split()
        if len(view_box) != 4:
            errors.append(f"{name}: viewBox must have four values")
        else:
            try:
                width, height = float(view_box[2]), float(view_box[3])
            except ValueError:
                errors.append(f"{name}: viewBox dimensions must be numeric")
            else:
                if name in ("brand-mark.svg", "avatar.svg") and width != height:
                    errors.append(f"{name}: square viewBox required")
                if name.startswith("watermark-") and width <= height:
                    errors.append(f"{name}: horizontal viewBox required")
        namespace = "{http://www.w3.org/2000/svg}"
        if root.find(f"{namespace}title") is None:
            errors.append(f"{name}: accessible title missing")
        if root.find(f"{namespace}desc") is None:
            errors.append(f"{name}: accessible description missing")
        for pattern in FORBIDDEN_SVG:
            if pattern.search(source):
                errors.append(f"{name}: forbidden content matches {pattern.pattern}")
        for color in PALETTE:
            if color not in source:
                errors.append(f"{name}: palette color missing: {color}")

    for name in ("watermark-dark.svg", "watermark-light.svg"):
        if not re.search(rf">{WORDMARK}<", svg_sources.get(name, "")):
            errors.append(f"{name}: exact live wordmark missing")
    if "<rect width=\"256\" height=\"256\" fill=\"#10162F\"" not in svg_sources.get("avatar.svg", ""):
        errors.append("avatar.svg: Midnight square background missing")

    html = _read(SPECIMEN)
    for pattern in FORBIDDEN_HTML:
        if pattern.search(html):
            errors.append(f"preview.html: forbidden content matches {pattern.pattern}")
    if WORDMARK not in html:
        errors.append("preview.html: exact wordmark missing")
    if "Warm systems. Bold momentum." not in html:
        errors.append("preview.html: tagline missing")
    for heading in ("Construction", "Avatar", "Watermarks", "README", "Usage", "Accessibility"):
        if heading.lower() not in html.lower():
            errors.append(f"preview.html: section missing: {heading}")

    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - environment diagnostic
        errors.append(f"Pillow is required for raster validation: {exc}")
    else:
        for name, expected_size in (("avatar.png", (1024, 1024)), ("brand-preview.png", (1600, 900))):
            path = BRAND / name
            try:
                with Image.open(path) as image:
                    if image.size != expected_size:
                        errors.append(f"{name}: expected {expected_size}, got {image.size}")
                    if name == "avatar.png" and "A" not in image.getbands():
                        errors.append("avatar.png: alpha channel missing")
                    if image.info:
                        errors.append(f"{name}: unexpected metadata keys: {sorted(image.info)}")
            except (OSError, ValueError) as exc:
                errors.append(f"{name}: unreadable raster ({exc})")

    guidelines = _read(BRAND / "brand-guidelines.md").lower()
    for keyword in ("palette", "clear space", "minimum", "accessibility", "misuse"):
        if keyword not in guidelines:
            errors.append(f"brand-guidelines.md: section missing: {keyword}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"FAIL: {len(errors)} brand contract issue(s)")
        return 1
    print("PASS: BOOMKALAKASHA brand contract")
    print("PASS: SVG accessibility, palette, and forbidden-content checks")
    print("PASS: PNG dimensions, alpha, and metadata checks")
    print("PASS: self-contained HTML specimen checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
