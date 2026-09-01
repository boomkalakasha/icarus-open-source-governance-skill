"""Run only fixed mature-tool checks without accepting policy-supplied commands."""

from __future__ import annotations

import subprocess
from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from typing import Any, Callable


FIXED_TOOLS = ("gitleaks", "reuse")
DEFAULT_TIMEOUT_SECONDS = 60


def run_fixed_tool(
    name: str,
    root: Path,
    *,
    locate: Callable[[str], str | None] = which,
    invoke: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Run one allow-listed tool and return redacted outcome metadata only."""
    if name not in FIXED_TOOLS:
        raise ValueError(f"unsupported fixed tool: {name}")
    executable = locate(name)
    if not executable:
        return {"name": name, "status": "UNAVAILABLE", "reason": "not-found"}

    with TemporaryDirectory(prefix="icarus-governance-") as directory:
        report_path = Path(directory) / "gitleaks.json"
        if name == "gitleaks":
            arguments = [
                executable,
                "detect",
                "--no-banner",
                "--redact",
                "--source",
                str(root),
                "--report-format",
                "json",
                "--report-path",
                str(report_path),
            ]
        else:
            arguments = [executable, "lint"]
        try:
            completed = invoke(
                arguments,
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
                timeout=timeout_seconds,
                shell=False,
            )
        except subprocess.TimeoutExpired:
            return {"name": name, "status": "TIMEOUT", "reason": "timeout"}
        except OSError:
            return {"name": name, "status": "ERROR", "reason": "execution-error"}

    if completed.returncode == 0:
        return {"name": name, "status": "PASS", "returnCode": 0}
    return {
        "name": name,
        "status": "NONZERO",
        "returnCode": completed.returncode,
        "reason": "nonzero-exit",
    }
