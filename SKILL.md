---
name: icarus-open-source-governance
description: Use when a repository may be sanitized, open-sourced, branded, licensed, published, or prepared for GitHub community and release governance. Route clearly private/internal delivery work away from this Skill.
---

# Icarus Open-source Governance

Turn a public-repository proposal into an evidence-led candidate. This Skill is engineering governance, **not legal advice** and not authority to publish.

## Trigger and boundary

Use for public GitHub extraction, provenance/privacy cleanup, OSS docs, optional branding, releases, or public community files. Do not use it to force an internal repository into an OSS workflow: keep private delivery, Jenkins, customer branches, and internal releases under their own rules.

Before changing anything, record `FACT`, `INFERENCE`, and `NOT_VERIFIED`; current branch/dirty files; desired public scope; and separately authorized side effects. Never infer approval for a repository creation, push, tag, release, settings change, or personal-profile change.

## Minimal workflow

1. **Classify** — confirm the project is intended for public release; stop for unknown ownership, privacy, or third-party asset rights.
2. **Configure** — start with `.icarus-open-source.example.yml`; `brand.mode: none` is the default. `subtle` and `full` are optional project choices, never forced personal attribution. 品牌为可选配置，不是默认归属声明。
3. **Audit locally** — self-check this tool with `python scripts/validate.py`;
   audit a candidate with `python scripts/audit_target.py --root <repository>
   --policy .icarus-open-source.yml --history`. Inspect current tree, reachable
   history, commit metadata, generated artifacts, and packages separately.
4. **Document** — make English/Chinese navigation and behavior agree; add only accurate installation, support, contribution, security, release, and license statements.
5. **Package and evaluate** — run `python scripts/run_evals.py` and `pwsh -NoProfile -File scripts/package.ps1`; record checksums and what remains `DOCUMENTED_ONLY`.
6. **Publish only after local gates** — use GitHub Flow, reviewed PRs, immutable SemVer tags, checked CI/CodeQL, and an independently verified release page. A release never proves production deployment.

## Required outputs

Return a small evidence ledger: scope, configuration, current-tree/history/package results, P0/P1 findings, local status, remote status, rollback, and the next separately authorized action. Keep unresolved legal/ownership questions `BLOCKED`; link maintainers to official resources rather than interpreting law.

## Progressive references

- [Public-readiness workflow](references/public-readiness.md)
- [Privacy and provenance](references/privacy-and-provenance.md)
- [Bilingual documentation](references/documentation-and-localization.md)
- [Optional branding](references/branding.md)
- [Licensing boundaries](references/licensing.md)
- [GitHub delivery](references/github-delivery.md)
- [Evidence gates](references/evidence-gates.md)
