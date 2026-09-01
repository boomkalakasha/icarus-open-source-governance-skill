"""Validate the portable Icarus Open-source Governance Skill contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "SKILL.md",
    "VERSION",
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    "CODE_OF_CONDUCT.md",
    "compatibility.md",
    ".icarus-open-source.example.yml",
    "schemas/icarus-open-source.schema.json",
    "references/public-readiness.md",
    "references/privacy-and-provenance.md",
    "references/documentation-and-localization.md",
    "references/branding.md",
    "references/licensing.md",
    "references/github-delivery.md",
    "references/evidence-gates.md",
    "references/release-documentation-sync.md",
    "references/legacy-public-history.md",
    "scripts/scan_public_risks.py",
    "scripts/audit_target.py",
    "scripts/external_tools.py",
    "scripts/check_history_boundaries.py",
    "scripts/check_release_docs.py",
    "scripts/package.ps1",
    "scripts/run_evals.py",
    "actions/release-doc-sync/action.yml",
    "actions/audit-target/action.yml",
    "evals/evals.json",
    "evals/trigger-evals.json",
    "templates/README.md",
    "templates/README.zh-CN.md",
    "templates/CONTRIBUTING.md",
    "templates/SECURITY.md",
    "templates/SUPPORT.md",
    "templates/CHANGELOG.md",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/ci.yml",
    ".github/workflows/codeql.yml",
    ".github/workflows/release.yml",
)
REQUIRED_SECTIONS = {"project", "license", "privacy", "brand", "git", "release", "evidence"}
ALLOWED_CONFIG_KEYS = {
    "<root>": {"schemaVersion", *REQUIRED_SECTIONS, "target", "integrations"},
    "project": {"name", "languages"},
    "target": {"requiredFiles", "readme", "readmeZh"},
    "license": {"decision"},
    "privacy": {"scanReachableHistory", "forbiddenPatterns"},
    "brand": {"mode", "profile"},
    "git": {"flow", "commits"},
    "release": {"versioning", "immutable"},
    "evidence": {"requireLocal", "requirePublicHost"},
    "integrations": {"gitleaks", "reuse"},
}
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".ps1", ".svg", ".html"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
STABLE_SEMVER = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
    if value.isdigit():
        return int(value)
    return value.strip("'\"")


def parse_minimal_yaml(path: Path) -> dict[str, Any]:
    """Read the intentionally small mapping-only subset used by this config."""
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if "\t" in raw[:indent] or ":" not in raw:
            raise ValueError(f"{path}:{number}: expected an indented key: value mapping")
        while indent <= stack[-1][0]:
            stack.pop()
        key, value = raw.strip().split(":", 1)
        if not key or key.strip() != key:
            raise ValueError(f"{path}:{number}: invalid key")
        target = stack[-1][1]
        if key in target:
            raise ValueError(f"{path}:{number}: duplicate key {key!r}")
        if value.strip():
            target[key] = parse_scalar(value)
        else:
            child: dict[str, Any] = {}
            target[key] = child
            stack.append((indent, child))
    return root


def validate_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    unknown = set(config) - ALLOWED_CONFIG_KEYS["<root>"]
    if unknown:
        errors.append(f"unknown top-level keys: {', '.join(sorted(unknown))}")
    if config.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    missing = REQUIRED_SECTIONS - set(config)
    if missing:
        errors.append(f"missing sections: {', '.join(sorted(missing))}")
        return errors
    for section in REQUIRED_SECTIONS:
        if not isinstance(config[section], dict):
            errors.append(f"{section} must be a mapping")
    if errors:
        return errors
    for section in REQUIRED_SECTIONS:
        unknown = set(config[section]) - ALLOWED_CONFIG_KEYS[section]
        if unknown:
            errors.append(
                f"unknown {section} keys: {', '.join(sorted(unknown))}"
            )
    project = config["project"]
    if not isinstance(project.get("name"), str) or not project["name"].strip():
        errors.append("project.name must be a non-empty string")
    languages = project.get("languages")
    if not isinstance(languages, list) or not languages or any(item not in {"en", "zh-CN"} for item in languages):
        errors.append("project.languages must be a non-empty list of en and/or zh-CN")
    target = config.get("target")
    if target is not None:
        if not isinstance(target, dict):
            errors.append("target must be a mapping")
        else:
            unknown = set(target) - ALLOWED_CONFIG_KEYS["target"]
            if unknown:
                errors.append(f"unknown target keys: {', '.join(sorted(unknown))}")
            required_files = target.get("requiredFiles")
            if not isinstance(required_files, list) or not required_files or not all(isinstance(item, str) for item in required_files):
                errors.append("target.requiredFiles must be a non-empty list of strings")
            for key in ("readme", "readmeZh"):
                if not isinstance(target.get(key), str) or not target[key].strip():
                    errors.append(f"target.{key} must be a non-empty string")
    if config["license"].get("decision") not in {"review-required", "approved", "not-applicable"}:
        errors.append("license.decision is invalid")
    privacy = config["privacy"]
    if not isinstance(privacy.get("scanReachableHistory"), bool):
        errors.append("privacy.scanReachableHistory must be boolean")
    if not isinstance(privacy.get("forbiddenPatterns"), list) or not all(isinstance(item, str) for item in privacy["forbiddenPatterns"]):
        errors.append("privacy.forbiddenPatterns must be a list of strings")
    brand = config["brand"]
    if brand.get("mode") not in {"none", "subtle", "full"}:
        errors.append("brand.mode must be none, subtle, or full")
    if brand.get("profile") is not None and not isinstance(brand.get("profile"), str):
        errors.append("brand.profile must be a string or null")
    if brand.get("mode") == "none" and brand.get("profile") is not None:
        errors.append("brand.profile must be null when brand.mode is none")
    if config["git"].get("flow") != "github-flow" or config["git"].get("commits") != "conventional-commits":
        errors.append("git.flow and git.commits must use the documented public defaults")
    if config["release"].get("versioning") != "semver" or config["release"].get("immutable") is not True:
        errors.append("release must require semver and immutable tags")
    evidence = config["evidence"]
    if not isinstance(evidence.get("requireLocal"), bool) or not isinstance(evidence.get("requirePublicHost"), bool):
        errors.append("evidence gates must be booleans")
    integrations = config.get("integrations")
    if integrations is not None:
        if not isinstance(integrations, dict):
            errors.append("integrations must be an object")
        else:
            unknown_integration_keys = set(integrations) - ALLOWED_CONFIG_KEYS["integrations"]
            if unknown_integration_keys:
                errors.append(
                    "unknown integrations keys: " + ", ".join(sorted(unknown_integration_keys))
                )
            for tool in ALLOWED_CONFIG_KEYS["integrations"]:
                if tool in integrations and integrations[tool] not in {"disabled", "optional", "required"}:
                    errors.append(f"integrations.{tool} must be disabled, optional, or required")
    return errors


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file() or any(part in {".git", "dist", "__pycache__"} for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", "SKILL.md"}:
            yield path


def safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if "\\" in value or ":" in value or any(ord(character) < 32 for character in value):
        return False
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    return (
        not posix.is_absolute()
        and ".." not in posix.parts
        and not windows.is_absolute()
        and not windows.drive
        and not windows.root
    )


def resolve_inside(
    root: Path,
    base: Path,
    value: object,
    *,
    allow_parent_segments: bool = False,
) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    if "\\" in value or ":" in value or any(ord(character) < 32 for character in value):
        return None
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if (
        posix.is_absolute()
        or windows.is_absolute()
        or windows.drive
        or windows.root
        or (not allow_parent_segments and ".." in posix.parts)
    ):
        return None
    root = root.resolve()
    candidate = (base / str(value)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def validate_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*.md"):
        if any(part in {".git", "dist"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target = target.strip().strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            local = target.split("#", 1)[0]
            if not local:
                continue
            # Markdown links may legitimately walk up from references/ or docs/.
            # The resolved-path containment check still rejects an escape from root.
            resolved = resolve_inside(
                root, path.parent, local, allow_parent_segments=True
            )
            if resolved is None:
                errors.append(f"{path.relative_to(root)}: unsafe relative link {target}")
            elif not resolved.exists():
                errors.append(f"{path.relative_to(root)}: broken relative link {target}")
    return errors


def validate_repository(root: Path, config_path: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")
    if errors:
        return errors
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not STABLE_SEMVER.fullmatch(version):
        errors.append("VERSION must be stable SemVer")
    for path in iter_text_files(root):
        if path.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"{path.relative_to(root)}: UTF-8 BOM is not allowed")
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?i)[A-Z]:[\\/]+(?:Users[\\/]+[^<>/\\]+|BO[\\/]+IdeaProjects)(?:[\\/]|$)", text):
            errors.append(f"{path.relative_to(root)}: machine-local absolute path is forbidden")
    errors.extend(validate_links(root))
    readme = (root / "README.md").read_text(encoding="utf-8")
    chinese_readme = (root / "README.zh-CN.md").read_text(encoding="utf-8")
    if "README.zh-CN.md" not in readme or "README.md" not in chinese_readme:
        errors.append("README language navigation is not reciprocal")
    if "## 60-second path" not in readme or "## 60 秒路径" not in chinese_readme:
        errors.append("README quick-start headings are not behaviorally aligned")
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    if "optional" not in skill.lower() or "可选" not in skill:
        errors.append("SKILL.md must make personal branding optional in both languages")
    if "mode: none" not in config_path.read_text(encoding="utf-8"):
        errors.append("the default example configuration must disable branding")
    for template in (root / "templates").glob("*.md"):
        if "BOOMKALAKASHA" in template.read_text(encoding="utf-8"):
            errors.append(f"{template.relative_to(root)}: template forces example personal branding")
    for workflow in (root / ".github" / "workflows").glob("*.yml"):
        source = workflow.read_text(encoding="utf-8")
        if "pull_request_target" in source:
            errors.append(f"{workflow.relative_to(root)}: pull_request_target is forbidden")
        for line in source.splitlines():
            if "uses:" not in line:
                continue
            action_reference = line.split("uses:", 1)[1].split("#", 1)[0].strip().strip("'\"")
            if action_reference.startswith("./"):
                action_path = (root / action_reference).resolve()
                try:
                    action_path.relative_to(root)
                except ValueError:
                    errors.append(
                        f"{workflow.relative_to(root)}: local action escapes the repository: {action_reference}"
                    )
                    continue
                if not action_path.is_dir() or not any(
                    (action_path / filename).is_file() for filename in ("action.yml", "action.yaml")
                ):
                    errors.append(
                        f"{workflow.relative_to(root)}: local action is missing action.yml/action.yaml: {action_reference}"
                    )
                continue
            match = re.search(r"uses:\s*[^@\s]+@([0-9a-f]{40})\b", line)
            if match is None:
                errors.append(f"{workflow.relative_to(root)}: action reference must be pinned to a 40-character commit")
    try:
        schema = json.loads((root / "schemas" / "icarus-open-source.schema.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"schema is invalid: {exc}")
    else:
        if not ({"schemaVersion", *REQUIRED_SECTIONS}.issubset(set(schema.get("required", [])))):
            errors.append("schema required sections do not match the public configuration contract")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--config", type=Path, default=Path(".icarus-open-source.example.yml"))
    args = parser.parse_args()
    root = args.root.resolve()
    config_path = args.config if args.config.is_absolute() else root / args.config
    errors: list[str] = []
    try:
        config = parse_minimal_yaml(config_path)
    except (OSError, ValueError) as exc:
        errors.append(f"configuration error: {exc}")
    else:
        errors.extend(validate_config(config))
    if not errors:
        errors.extend(validate_repository(root, config_path))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: configuration contract")
    print("PASS: bilingual navigation")
    print("PASS: optional brand configuration")
    print("PASS: required files, UTF-8, schema, and relative links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
