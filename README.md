![BOOMKALAKASHA watermark](assets/brand/boomkalakasha/watermark-auto.svg)

# Icarus Open-source Governance

[简体中文](README.zh-CN.md) · [Skill](SKILL.md) · [Configuration](.icarus-open-source.example.yml) · [Evidence gates](references/evidence-gates.md)

> **先把风险说清楚，再把项目公开。**
>
> **Make the risks visible before making the project public.**

Before publishing an internal prototype, use this Skill to scan reachable history, make privacy and provenance risks explicit, align bilingual documentation, and assemble release evidence for a human-reviewed decision.

Reusable, evidence-led governance for turning a repository into a public open-source candidate without overstating what has been verified.

## 60-second path

```powershell
python scripts/validate.py
python scripts/scan_public_risks.py --history
python scripts/run_evals.py
pwsh -NoProfile -File scripts/package.ps1
```

These commands validate a local candidate. They do not create a repository, push a branch, publish a tag, change GitHub settings, or prove production readiness.

## What it covers

- A small `.icarus-open-source.yml` contract for project, license decision, privacy, brand, Git, release, and evidence gates.
- Current-tree, reachable-history, commit-metadata, package, and generated-artifact risk checks as separate evidence streams.
- Bilingual public documentation and community templates with truthful support, security, and release boundaries.
- Optional branding: the bundled BOOMKALAKASHA kit is an example profile, not a project default or ownership claim.
- GitHub Flow, Conventional Commits, immutable SemVer, checksums, CI, CodeQL, and a release workflow that still requires review and separate authorization.

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
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Support](SUPPORT.md) · [Changelog](CHANGELOG.md) · [License](LICENSE)

For GitHub behavior, use the official [community health](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file), [release](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases), and [CodeQL](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-with-codeql) documentation as the current source of truth.
