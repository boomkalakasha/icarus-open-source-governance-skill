# Repository Guidelines

This repository contains the public `icarus-open-source-governance` Skill. Keep its workflow reusable across public GitHub projects. Personal branding, organization names, private infrastructure, credentials, customer data, and internal policies must remain optional configuration or sanitized examples.

## Structure

- `SKILL.md` is the concise public entrypoint.
- `references/` contains detailed governance, privacy, branding, documentation, license, and release guidance.
- `templates/` contains reusable public-project files and configuration examples.
- `scripts/` contains deterministic validation and public-risk scanning.
- `evals/` contains trigger, pressure, positive, negative, and boundary scenarios.
- `assets/brand/boomkalakasha/` is an example brand kit, not a mandatory default.
- `docs/superpowers/` contains the approved design, implementation plan, and execution ledger.

## Delivery

Use GitHub Flow on a short feature branch. Keep `main` stable, use truthful Conventional Commits, and publish immutable SemVer tags only after current-tree, reachable-history, package, documentation, and eval evidence is recorded. A GitHub Release is not proof of deployment or production cutover.

## Validation

Before a pull request, run the complete local gate from the repository root:

```text
python scripts/validate.py
python scripts/check_history_boundaries.py
python -m unittest discover -s scripts -p "test_*.py"
python scripts/run_evals.py
pwsh -NoProfile -File scripts/package.ps1
python scripts/scan_public_risks.py --history --include-generated
python scripts/audit_target.py --root . --policy .github/ci/self-audit-policy.yml --history
```

The last command exercises this repository's passable CI self-audit policy;
other repositories use their own in-target `.icarus-open-source.yml` policy.
Do not claim legal approval: the Skill supplies engineering governance and
points maintainers to authoritative resources.

## Project/module AI guidance coverage

This root `AGENTS.md` is the project-level guide for the public Skill. The
repository has no independently released source modules with distinct commands
or privileged boundaries, so the current module-level status is `NOT_NEEDED`.
Do not add duplicate per-folder guidance. Reassess when a subarea acquires a
separate build/run command, external or data/security contract, release or
ownership lifecycle, or dependency direction that cannot be safely described
at root scope. Keep a necessary nearest-scope guide brief and linked back here.

