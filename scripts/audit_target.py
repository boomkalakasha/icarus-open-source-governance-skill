"""Audit a selected public target repository using an in-target Icarus policy."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from external_tools import FIXED_TOOLS, run_fixed_tool
from scan_public_risks import compile_rules, scan_current_tree, scan_history
from validate import parse_minimal_yaml, resolve_inside, safe_relative_path, validate_config, validate_links


TOOL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET = {
    "requiredFiles": ["README.md", "README.zh-CN.md", "LICENSE", "SECURITY.md"],
    "readme": "README.md",
    "readmeZh": "README.zh-CN.md",
}


def safe_target_path(value: object) -> bool:
    return safe_relative_path(value)


def finding(check: str, *, location: str, rule: str, line: int = 0) -> dict[str, Any]:
    return {"check": check, "location": location, "line": line, "rule": rule}


def resolve_policy(root: Path, supplied: Path) -> Path:
    candidate = supplied.resolve() if supplied.is_absolute() else (root / supplied).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("policy must be inside target") from exc
    if not candidate.is_file():
        raise ValueError(f"policy does not exist: {candidate}")
    return candidate


def license_check(policy: dict[str, Any]) -> dict[str, Any]:
    license_config = policy["license"]
    assert isinstance(license_config, dict)
    decision = license_config["decision"]
    assert isinstance(decision, str)
    status = "HUMAN_REVIEW" if decision == "review-required" else "PASS"
    return {
        "name": "license-decision",
        "status": status,
        "decision": decision,
        "boundary": "configuration records a maintainer decision; it is not legal approval",
    }


def integration_checks(root: Path, policy: dict[str, Any]) -> list[dict[str, Any]]:
    integrations = policy.get("integrations", {})
    assert isinstance(integrations, dict)
    checks: list[dict[str, Any]] = []
    for name in FIXED_TOOLS:
        mode = integrations.get(name, "disabled")
        assert isinstance(mode, str)
        if mode == "disabled":
            checks.append({"name": name, "status": "NOT_CONFIGURED", "mode": mode})
            continue
        result = run_fixed_tool(name, root)
        if result["status"] == "PASS":
            status = "PASS"
        elif mode == "required":
            status = "HOLD"
        else:
            status = "HUMAN_REVIEW"
        checks.append(
            {
                "name": name,
                "status": status,
                "mode": mode,
                "toolStatus": result["status"],
                **({"returnCode": result["returnCode"]} if "returnCode" in result else {}),
            }
        )
    return checks


def audit(root: Path, policy_path: Path, force_history: bool) -> tuple[dict[str, Any], int]:
    try:
        policy = parse_minimal_yaml(policy_path)
    except (OSError, ValueError) as exc:
        raise ValueError(f"invalid policy: {exc}") from exc
    config_errors = validate_config(policy)
    if config_errors:
        raise ValueError("invalid policy: " + "; ".join(config_errors))

    findings: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    target = policy.get("target", DEFAULT_TARGET)
    assert isinstance(target, dict)
    required_files = target["requiredFiles"]
    assert isinstance(required_files, list)
    for relative in required_files:
        resolved = resolve_inside(root, root, relative)
        if resolved is None:
            findings.append(finding("target-contract", location=str(relative), rule="unsafe-required-path"))
        elif not resolved.is_file():
            findings.append(finding("target-contract", location=relative, rule=f"missing-required-file:{relative}"))

    readme = target["readme"]
    readme_zh = target["readmeZh"]
    english_path = resolve_inside(root, root, readme)
    chinese_path = resolve_inside(root, root, readme_zh)
    if english_path is not None and chinese_path is not None:
        if english_path.is_file() and chinese_path.is_file():
            english = english_path.read_text(encoding="utf-8")
            chinese = chinese_path.read_text(encoding="utf-8")
            if Path(readme_zh).name not in english or Path(readme).name not in chinese:
                findings.append(
                    finding(
                        "documentation",
                        location=f"{readme},{readme_zh}",
                        rule="bilingual-navigation",
                    )
                )
    else:
        findings.append(finding("target-contract", location="target.readme", rule="unsafe-readme-path"))

    for error in validate_links(root):
        findings.append(finding("documentation", location=error, rule="broken-relative-link"))

    privacy = policy["privacy"]
    assert isinstance(privacy, dict)
    extra_patterns = privacy.get("forbiddenPatterns", [])
    assert isinstance(extra_patterns, list)
    try:
        rules = compile_rules(extra_patterns)
    except ValueError as exc:
        raise ValueError(f"invalid policy: {exc}") from exc
    risk_findings, file_count = scan_current_tree(root, rules, include_generated=False)
    checks.append({"name": "current-tree", "status": "PASS", "files": file_count})
    for item in risk_findings:
        findings.append(
            finding("privacy", location=item.location, line=item.line, rule=item.rule)
            | {"scope": item.scope}
        )

    scan_reachable_history = force_history or privacy.get("scanReachableHistory") is True
    if scan_reachable_history:
        try:
            history_findings, commit_count, blob_count = scan_history(root, rules)
        except RuntimeError as exc:
            raise ValueError(f"reachable history could not be scanned: {exc}") from exc
        checks.append(
            {
                "name": "reachable-history",
                "status": "PASS",
                "commits": commit_count,
                "textBlobs": blob_count,
            }
        )
        for item in history_findings:
            findings.append(
                finding("privacy", location=item.location, line=item.line, rule=item.rule)
                | {"scope": item.scope}
            )
    else:
        checks.append({"name": "reachable-history", "status": "NOT_RUN"})

    checks.append(license_check(policy))
    checks.extend(integration_checks(root, policy))

    status = "HOLD" if findings or any(check["status"] == "HOLD" for check in checks) else "PASS"
    if status == "PASS" and any(check["status"] == "HUMAN_REVIEW" for check in checks):
        status = "HUMAN_REVIEW"
    for check in checks:
        if findings and check["name"] in {"current-tree", "reachable-history"}:
            relevant_scope = "current-tree" if check["name"] == "current-tree" else "history"
            if any(str(item.get("scope", "")).startswith(relevant_scope) for item in findings):
                check["status"] = "HOLD"
    payload = {
        "toolVersion": (TOOL_ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "target": root.name,
        "policy": str(policy_path.relative_to(root).as_posix()),
        "checks": checks,
        "findings": findings,
        "status": status,
    }
    return payload, 0 if status == "PASS" else 1


def print_text(payload: dict[str, Any]) -> None:
    if payload["status"] == "PASS":
        print(f"PASS: target audit ({payload['target']})")
    elif payload["status"] == "HUMAN_REVIEW":
        print(f"HUMAN_REVIEW: target audit ({payload['target']})")
    else:
        for item in payload["findings"]:
            scope = item.get("scope", item["check"])
            print(f"FAIL: {scope}:{item['location']}:{item['line']}:{item['rule']}")
        print(f"HOLD: target audit ({len(payload['findings'])} finding(s))")
    for check in payload["checks"]:
        details = []
        for key in ("mode", "decision", "toolStatus", "returnCode"):
            if key in check:
                details.append(f"{key}={check[key]}")
        suffix = f" ({', '.join(details)})" if details else ""
        print(f"EVIDENCE: {check['name']}={check['status']}{suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--policy", type=Path, default=Path(".icarus-open-source.yml"))
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR: target root does not exist: {root}", file=sys.stderr)
        return 2
    try:
        policy_path = resolve_policy(root, args.policy)
        payload, exit_code = audit(root, policy_path, args.history)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_text(payload)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
