"""Scan a candidate current tree and optional reachable Git history for public-risk markers."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from validate import parse_minimal_yaml


DEFAULT_RULES = {
    "private-key": r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
    "aws-access-key": r"\bAKIA[0-9A-Z]{16}\b",
    "github-token": r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b",
    "bearer-token": r"\bBearer\s+[A-Za-z0-9._~+/=-]{24,}\b",
    "generic-secret-assignment": r"\b(?:api[_-]?key|secret|token|password)\b\s*[:=]\s*['\"]?[A-Za-z0-9_~+/=-]{12,}",
    "private-ipv4": (
        r"\b(?:10\.(?:25[0-5]|2[0-4]\d|1?\d?\d)\.(?:25[0-5]|2[0-4]\d|1?\d?\d)\.(?:25[0-5]|2[0-4]\d|1?\d?\d)"
        r"|192\.168\.(?:25[0-5]|2[0-4]\d|1?\d?\d)\.(?:25[0-5]|2[0-4]\d|1?\d?\d)"
        r"|172\.(?:1[6-9]|2\d|3[0-1])\.(?:25[0-5]|2[0-4]\d|1?\d?\d)\.(?:25[0-5]|2[0-4]\d|1?\d?\d))\b"
    ),
    "private-domain": r"\b[a-z0-9.-]+\.(?:internal|corp|lan)\b",
}
SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache"}
MAX_TEXT_BYTES = 2_000_000


@dataclass(frozen=True)
class Finding:
    scope: str
    location: str
    line: int
    rule: str


def compile_rules(extra_patterns: list[str]) -> list[tuple[str, re.Pattern[str]]]:
    rules = list(DEFAULT_RULES.items()) + [(f"custom-{index}", item) for index, item in enumerate(extra_patterns, start=1)]
    compiled = []
    for name, source in rules:
        try:
            compiled.append((name, re.compile(source, re.IGNORECASE)))
        except re.error as exc:
            raise ValueError(f"invalid {name} regular expression: {exc}") from exc
    return compiled


def findings_for_text(scope: str, location: str, source: str, rules: list[tuple[str, re.Pattern[str]]]) -> list[Finding]:
    findings: list[Finding] = []
    for number, line in enumerate(source.splitlines(), start=1):
        for name, pattern in rules:
            if pattern.search(line):
                findings.append(Finding(scope, location, number, name))
    return findings


def read_text(path: Path) -> str | None:
    if path.stat().st_size > MAX_TEXT_BYTES:
        return None
    raw = path.read_bytes()
    if b"\x00" in raw:
        return None
    return raw.decode("utf-8", errors="replace")


def scan_current_tree(root: Path, rules: list[tuple[str, re.Pattern[str]]], include_generated: bool) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    files = 0
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if not path.is_file() or any(part in SKIP_PARTS for part in relative.parts):
            continue
        if not include_generated and "dist" in relative.parts:
            continue
        source = read_text(path)
        if source is None:
            continue
        files += 1
        findings.extend(findings_for_text("current-tree", relative.as_posix(), source, rules))
    return findings, files


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "git command failed")
    return result.stdout


def scan_history(root: Path, rules: list[tuple[str, re.Pattern[str]]]) -> tuple[list[Finding], int, int]:
    git(root, "rev-parse", "--is-inside-work-tree")
    commits = [line for line in git(root, "rev-list", "--all").splitlines() if line]
    findings: list[Finding] = []
    blobs = 0
    for commit in commits:
        metadata = git(root, "show", "-s", "--format=%H%n%an%n%ae%n%cn%n%ce%n%B", commit)
        findings.extend(findings_for_text("history-metadata", commit, metadata, rules))
        for relative in git(root, "ls-tree", "-r", "--name-only", commit).splitlines():
            if not relative or any(part in SKIP_PARTS for part in Path(relative).parts):
                continue
            result = subprocess.run(
                ["git", "show", f"{commit}:{relative}"],
                cwd=root,
                capture_output=True,
                check=False,
            )
            if result.returncode != 0 or len(result.stdout) > MAX_TEXT_BYTES or b"\x00" in result.stdout:
                continue
            blobs += 1
            source = result.stdout.decode("utf-8", errors="replace")
            findings.extend(findings_for_text("history", f"{commit}:{relative}", source, rules))
    return findings, len(commits), blobs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--history", action="store_true", help="also scan every local reachable commit and metadata")
    parser.add_argument("--include-generated", action="store_true", help="include dist/ files in the current-tree scan")
    parser.add_argument("--pattern", action="append", default=[], help="additional case-insensitive regular expression")
    parser.add_argument("--config", type=Path, help="load privacy.forbiddenPatterns and scanReachableHistory from a small YAML config")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR: root does not exist: {root}")
        return 2
    config_patterns: list[str] = []
    scan_reachable_history = args.history
    if args.config:
        config_path = args.config if args.config.is_absolute() else root / args.config
        try:
            privacy = parse_minimal_yaml(config_path).get("privacy", {})
        except (OSError, ValueError) as exc:
            print(f"ERROR: could not read configuration: {exc}")
            return 2
        if not isinstance(privacy, dict) or not isinstance(privacy.get("forbiddenPatterns", []), list):
            print("ERROR: privacy.forbiddenPatterns must be a list")
            return 2
        config_patterns = privacy["forbiddenPatterns"]
        if not all(isinstance(pattern, str) for pattern in config_patterns):
            print("ERROR: privacy.forbiddenPatterns must contain only strings")
            return 2
        scan_reachable_history = scan_reachable_history or privacy.get("scanReachableHistory") is True
    try:
        rules = compile_rules([*args.pattern, *config_patterns])
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 2
    if args.config:
        print(f"PASS: configuration loaded ({len(config_patterns)} custom pattern(s))")
    findings, file_count = scan_current_tree(root, rules, args.include_generated)
    print(f"PASS: current tree scanned ({file_count} text file(s))")
    if scan_reachable_history:
        try:
            history_findings, commit_count, blob_count = scan_history(root, rules)
        except RuntimeError as exc:
            print(f"ERROR: reachable history could not be scanned: {exc}")
            return 2
        findings.extend(history_findings)
        print(f"PASS: reachable history scanned ({commit_count} commit(s), {blob_count} text blob(s))")
    if findings:
        for finding in findings:
            print(f"FAIL: {finding.scope}:{finding.location}:{finding.line}:{finding.rule}")
        return 1
    print("PASS: no configured public-risk markers found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
