"""Validate release tag/version alignment and dynamic README release facts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


STABLE_TAG = re.compile(r"^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
STABLE_VERSION = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
MARKER = "<!-- icarus-release-fact: dynamic -->"
STALE_CLAIMS = (
    re.compile(
        r"(?:latest|current)(?:\s+public)?(?:\s+stable)?\s+(?:release|version)"
        r"(?:\s+(?:is|equals)|\s*:)?.{0,160}\bv\d+\.\d+\.\d+\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"最新(?:公开)?(?:稳定)?(?:版|版本|发布)(?:是|为|：|:)?[^\n]{0,160}"
        r"v\d+\.\d+\.\d+"
    ),
)


def validate(tag: str, version: str, repository: str, readmes: list[Path]) -> list[str]:
    errors: list[str] = []
    if STABLE_TAG.fullmatch(tag) is None:
        errors.append(f"release tag must use stable SemVer vMAJOR.MINOR.PATCH: {tag}")
    if STABLE_VERSION.fullmatch(version) is None:
        errors.append(f"source version must use stable SemVer MAJOR.MINOR.PATCH: {version}")
    elif tag != f"v{version}":
        errors.append(f"release tag {tag} does not match source version {version}")
    if REPOSITORY.fullmatch(repository) is None:
        errors.append("repository must use the owner/name GitHub slug")
        return errors
    latest_url = f"https://github.com/{repository}/releases/latest"
    releases_url = f"https://github.com/{repository}/releases"
    if not readmes:
        errors.append("at least one README path is required")
    for path in readmes:
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path}: could not read README: {exc}")
            continue
        if MARKER not in source:
            errors.append(f"{path}: missing dynamic release fact marker")
        if f"]({latest_url})" not in source:
            errors.append(f"{path}: missing {latest_url}")
        if f"]({releases_url})" not in source:
            errors.append(f"{path}: missing complete release history link: {releases_url}")
        if any(pattern.search(source) for pattern in STALE_CLAIMS):
            errors.append(f"{path}: hard-coded latest stable release claim is forbidden")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--readme", action="append", type=Path, default=[])
    args = parser.parse_args()
    errors = validate(args.tag, args.version, args.repository, args.readme)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: release documentation matches {args.tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
