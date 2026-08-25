"""Check the documented-only rubric for governance Skill evaluation scenarios."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    data = json.loads((root / "evals" / "evals.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    for case in data["evals"]:
        path = root / "evals" / "with-skill" / case["id"] / "output.md"
        if not path.is_file():
            errors.append(f"missing documented evidence: {path.relative_to(root)}")
            continue
        source = path.read_text(encoding="utf-8")
        if "DOCUMENTED_ONLY" not in source:
            errors.append(f"{case['id']}: evidence level must be DOCUMENTED_ONLY without a host run")
        for marker in case.get("required_markers", []):
            if marker not in source:
                errors.append(f"{case['id']}: missing rubric marker {marker}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: documented-only rubric checked for {len(data['evals'])} scenario(s)")
    print("DOCUMENTED_ONLY: no model host was invoked; this is a static rubric and reference-response check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
