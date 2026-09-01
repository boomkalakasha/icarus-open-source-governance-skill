#!/usr/bin/env python3
"""Reject new machine-local paths while recording known public legacy history."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKED_PATHS = (".", ":!dist")
MACHINE_PATH = re.compile(
    r"(?i)[A-Z]:[\\/]+(?:Users[\\/]+[^<>/\\]+|BO[\\/]+IdeaProjects)(?:[\\/]|$)"
)
GIT_EXPRESSION = r"[A-Za-z]:[/\\](Users[/\\][^/\\]+|BO[/\\]IdeaProjects)"
KNOWN_LEGACY_CHANGE_COMMITS = {
    "f5212b292b84d06cebd95423b360db8e41037b54",
}


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )


def current_tree_has_machine_path() -> bool:
    from validate import iter_text_files

    return any(
        MACHINE_PATH.search(path.read_text(encoding="utf-8"))
        for path in iter_text_files(ROOT)
    )


def commit_tree_has_machine_path(commit: str) -> bool:
    result = git("grep", "-q", "-i", "-E", GIT_EXPRESSION, commit, "--", *TRACKED_PATHS)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or "git grep failed")
    return result.returncode == 0


def remote_heads_with_machine_path() -> list[str]:
    refs = git(
        "for-each-ref", "--format=%(refname)", "refs/remotes/origin"
    )
    if refs.returncode != 0:
        raise RuntimeError(refs.stderr.strip() or "git for-each-ref failed")
    exposed: list[str] = []
    for ref in (line.strip() for line in refs.stdout.splitlines() if line.strip()):
        if ref.endswith("/HEAD"):
            continue
        if commit_tree_has_machine_path(ref):
            exposed.append(ref.removeprefix("refs/remotes/"))
    return exposed


def main() -> int:
    if current_tree_has_machine_path():
        print("FAIL: current public source contains a machine-local absolute path")
        return 1
    top_level = git("rev-parse", "--show-toplevel")
    if (
        top_level.returncode != 0
        or Path(top_level.stdout.strip()).resolve() != ROOT.resolve()
    ):
        print("NOT_RUN: Git history is unavailable in this package checkout")
        return 0

    changed = git(
        "log",
        "--all",
        "--regexp-ignore-case",
        "--format=%H",
        "-G",
        GIT_EXPRESSION,
        "--",
        *TRACKED_PATHS,
    )
    if changed.returncode != 0:
        print("FAIL: could not inspect reachable Git history")
        return 1

    unexpected: list[str] = []
    remediation: list[str] = []
    for commit in (line.strip() for line in changed.stdout.splitlines() if line.strip()):
        if commit in KNOWN_LEGACY_CHANGE_COMMITS:
            continue
        try:
            still_present = commit_tree_has_machine_path(commit)
        except RuntimeError as exc:
            print(f"FAIL: {exc}")
            return 1
        if still_present:
            unexpected.append(commit)
        else:
            remediation.append(commit)

    if unexpected:
        for commit in unexpected:
            print(f"FAIL: unexpected machine-path change remains present at {commit}")
        return 1
    print("PASS: current public source is free of machine-local absolute paths")
    print("ACCEPTED_LEGACY: one already-public path-change commit is recorded")
    try:
        exposed_heads = remote_heads_with_machine_path()
    except RuntimeError as exc:
        print(f"FAIL: {exc}")
        return 1
    if exposed_heads:
        print(
            "ACCEPTED_LEGACY: remote heads still exposing the recorded history: "
            + ", ".join(exposed_heads)
        )
    if remediation:
        print(f"PASS: {len(remediation)} remediation commit(s) remove the paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())
