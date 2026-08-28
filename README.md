![BOOMKALAKASHA watermark](assets/brand/boomkalakasha/watermark-auto.svg)

# Icarus Open-source Governance

[简体中文](README.zh-CN.md) · [Skill](SKILL.md) · [Configuration](.icarus-open-source.example.yml) · [Evidence gates](references/evidence-gates.md)

> **先把风险说清楚，再把项目公开。**
>
> **Make the risks visible before making the project public.**

Before publishing an internal prototype, use this Skill to scan reachable history, make privacy and provenance risks explicit, align bilingual documentation, and assemble release evidence for a human-reviewed decision.

Turn privacy, provenance, documentation, licensing, and release evidence into one executable, reviewable path from internal repository to public open-source candidate.

<!-- icarus-release-fact: dynamic -->
Public packages and status are available from the
[latest GitHub Release](https://github.com/boomkalakasha/icarus-open-source-governance-skill/releases/latest)
and the [complete release history](https://github.com/boomkalakasha/icarus-open-source-governance-skill/releases).
An untagged source tree remains a candidate until its review, tag, CI, assets,
and Release evidence are complete.

The local scripts use Python's standard library and PowerShell; no project-specific package installation is required for this first review path.

## At a glance

| If you need to... | This Skill helps you... | The decision it supports |
| --- | --- | --- |
| Decide whether a repository is safe to publish | Validate the project contract, privacy, license, brand and release inputs | Separate a reviewable candidate from an unsafe “ready” claim |
| Understand what history exposes | Scan reachable commits, metadata, generated files and package contents | Turn hidden provenance or privacy surprises into findings to investigate |
| Make public documentation feel intentional | Keep Chinese and English navigation aligned and make branding optional | Publish docs that are readable without making personal defaults look mandatory |
| Assemble a release that others can inspect | Build an evidence bundle with package, manifest, checksums and CI/security gates | Give a human reviewer concrete release evidence, not a green command alone |

Common uses include preparing an internal prototype for GitHub, checking a
repository before handing it to a client or community, or teaching a team why
source, history, metadata and release assets need separate review. The Skill
organizes evidence; it does not make legal, ownership or production decisions.

## 60-second path

For a first review, follow this order:

1. Copy the example configuration and replace only facts you can support.
2. Validate the contract, then scan current files and reachable history.
3. Read every finding and decide privacy, license, bilingual-doc and branding
   actions instead of treating a passing scan as approval.
4. Run evaluations and package the candidate; review `dist/manifest.json` and
   `SHA256SUMS.txt` before requesting a PR, tag or GitHub Release.

```powershell
Copy-Item .icarus-open-source.example.yml .icarus-open-source.yml
python scripts/validate.py --config .icarus-open-source.yml
python scripts/scan_public_risks.py --history
python scripts/run_evals.py
pwsh -NoProfile -File scripts/package.ps1
```

These commands validate a local candidate. They do not create a repository, push a branch, publish a tag, change GitHub settings, or prove production readiness.

When a scan reports a finding, classify it before editing: current-tree findings
usually need a source change; reachable-history findings may require a removal,
history rewrite decision or an explicit exception; metadata findings need an
author/committer review. Re-run the relevant scan after the decision and keep
the human review record with the candidate.

## What you get

**Illustrative evidence summary — redacted sample, not a scan result for this
repository:**

| Evidence stream | Example finding | Gate |
| --- | --- | --- |
| Current tree | No configured private-host pattern found | `PASS` |
| Reachable history | One token-shaped value: `[REDACTED_SECRET]` | `P1 HOLD` pending provenance review |
| Bilingual docs | Navigation and release-fact markers aligned | `PASS` |
| Package | Manifest and SHA-256 generated from one staged tree | `LOCAL_PASS` |
| Public host | Tag, CI run, assets and repository settings | `NOT_OBSERVED` |

Example decision: **HOLD public release** until the history finding is resolved
or explicitly accepted by an authorized reviewer. A local green scan alone
never upgrades the public-host evidence.

## What it covers

- A small `.icarus-open-source.yml` contract for project, license decision, privacy, brand, Git, release, and evidence gates.
- Current-tree, reachable-history, commit-metadata, package, and generated-artifact risk checks as separate evidence streams.
- Bilingual public documentation and community templates with truthful support, security, and release boundaries.
- Optional branding: the bundled BOOMKALAKASHA kit is an example profile, not a project default or ownership claim.
- GitHub Flow, Conventional Commits, immutable SemVer, checksums, CI, CodeQL, and a release workflow that still requires review and separate authorization.
- A reusable release-documentation gate that keeps README release facts dynamic and checks tag/source-version alignment before packaging.

## Companion projects

- [AI-first Vibe Coding Skill](https://github.com/boomkalakasha/ai-first-vibe-coding-skill) — use it when agents are implementing and reviewing the project before the open-source gate.
- [Icarus AI Spring Scaffold](https://github.com/boomkalakasha/icarus-ai-spring-scaffold) — use it when a new Java 17 service needs a safe, reviewable starting structure.

## What it deliberately does not promise

- It is not legal advice and cannot decide copyright, trademark, employment, privacy, or third-party license rights.
- It cannot prove a remote GitHub setting, CI result, release asset, or a production/cutover state from local files.
- It does not authorize destructive history rewrites, public publication, or any personal GitHub-profile mutation.

## Configure a project

Copy the example to the candidate repository and replace only facts you can support:

```powershell
Copy-Item .icarus-open-source.example.yml .icarus-open-source.yml
python scripts/validate.py --config .icarus-open-source.yml
```

`brand.mode` defaults to `none`. Use `subtle` or `full` only when the project owner intentionally chooses a replaceable brand profile. See [branding guidance](references/branding.md).

## Local evidence and package

`scripts/scan_public_risks.py --history` scans local reachable commits and author/committer metadata, de-duplicating unchanged text blobs while retaining a first-seen finding location. It is a deterministic marker scan, not a complete secret or rights assessment. Add project-specific patterns with `--pattern` or load `privacy.forbiddenPatterns` and its history preference with `--config .icarus-open-source.yml`; investigate every finding.

`scripts/package.ps1` stages the same source tree once, then creates `.skill`, `.zip`, `manifest.json`, and `SHA256SUMS.txt` under `dist/`. The manifest marks the source tree `clean` or `dirty`; only a clean exact-tag package is eligible for release review. Verify release assets again from the exact reviewed tag before publishing.

`VERSION` declares the local package version. GitHub Releases remain the source of truth for whether that version has been publicly published; an untagged candidate is not a public release.

## References and support

- [Public-readiness workflow](references/public-readiness.md)
- [Privacy and provenance](references/privacy-and-provenance.md)
- [Documentation and localization](references/documentation-and-localization.md)
- [GitHub delivery](references/github-delivery.md)
- [Release documentation synchronization](references/release-documentation-sync.md)
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Support](SUPPORT.md) · [Changelog](CHANGELOG.md) · [License](LICENSE)

For GitHub behavior, use the official [community health](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file), [release](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases), and [CodeQL](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-with-codeql) documentation as the current source of truth.
