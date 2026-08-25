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

Before commit, run the repository validator, script tests, Markdown/link checks, package build, public-content scan, and documented eval checks. Do not claim legal approval: the Skill supplies engineering governance and points maintainers to authoritative resources.

