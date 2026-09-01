# Open-source Productization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver two verified v1.1.0 feature branches, a reusable BOOMKALAKASHA brand kit and artifact-template, and a publish-ready `icarus-open-source-governance` Skill repository.

**Architecture:** Three repositories have disjoint write sets. Shared brand assets follow one documented contract and are copied into each consumer. The governance Skill owns reusable public-readiness rules; the AI workflow Skill links to it, and the Spring scaffold focuses on project generation and runtime evidence.

**Tech Stack:** Markdown, YAML, Python 3, PowerShell, Java 17, Maven 3.9 wrapper, Spring Boot, Docker/Compose, SVG/HTML/PNG, GitHub Actions.

---

### Task 1: Brand kit and visual specimen

**Files:**
- Create: `assets/brand/boomkalakasha/brand-mark.svg`
- Create: `assets/brand/boomkalakasha/avatar.svg`
- Create: `assets/brand/boomkalakasha/avatar.png`
- Create: `assets/brand/boomkalakasha/watermark-dark.svg`
- Create: `assets/brand/boomkalakasha/watermark-light.svg`
- Create: `assets/brand/boomkalakasha/brand-preview.png`
- Create: `assets/brand/boomkalakasha/brand-guidelines.md`
- Create: `docs/brand/preview.html`
- Create: `scripts/validate_brand.py`
- Test: `scripts/test_validate_brand.py`

- [ ] Write failing tests for required SVG viewBox, exact wordmark, palette, PNG dimensions/alpha, asset existence, and forbidden embedded metadata.
- [ ] Run `python -m unittest scripts.test_validate_brand -v`; expect failures for missing assets.
- [ ] Implement the SVG sources and HTML specimen using the approved Warm Pulse Circuit direction.
- [ ] Render PNG derivatives with the bundled workspace graphics runtime; do not rasterize by screenshot when a direct renderer is available.
- [ ] Run brand tests and inspect the avatar at 40/96/256 px plus light/dark watermark previews.
- [ ] Use `frontend-design` through a Luna Max implementation agent and have the main Sol controller perform browser visual QA.
- [ ] Create the personal artifact-template from `brand-preview.png` through the official Template Creator script and verify its manifest/reference/preview.

### Task 2: AI-first Vibe Coding v1.1.0

**Worktree:** `<workspace>/worktrees/ai-first-v1.1-productization`

**Files:**
- Modify: `README.md`, `README.zh-CN.md`, `CHANGELOG.md`, `SKILL.md`, `compatibility.md`, `evals/README.md`
- Modify: `scripts/package.ps1`, `scripts/validate.py`, `.github/workflows/ci.yml`, `.github/workflows/release.yml`
- Create: `scripts/test_package.py`, `scripts/run_evals.py`, `docs/quick-start.md`, `docs/quick-start.zh-CN.md`
- Create: `assets/brand/brand-mark.svg`, `assets/brand/avatar.png`, `assets/brand/watermark-dark.svg`, `assets/brand/watermark-light.svg`
- Create: `docs/assets/brand/brand-mark.svg`, `docs/assets/brand/watermark-dark.svg`, `docs/assets/brand/watermark-light.svg`
- Modify or create eval cases under `evals/`

- [ ] Add failing package tests requiring one staged tree to produce ZIP, `.skill`, and SHA-256 entries with matching file manifests.
- [ ] Add failing validation/eval tests for bilingual section parity, support navigation, install/upgrade/rollback/uninstall instructions, and governance-skill handoff.
- [ ] Run the focused tests and retain expected RED output.
- [ ] Implement canonical packaging and CI/release upload from the same `dist/manifest.json`.

The manifest contract is:

```json
{
  "schemaVersion": 1,
  "version": "1.1.0",
  "sourceCommit": "0000000000000000000000000000000000000000",
  "artifacts": [
    {"name": "ai-first-vibe-coding-1.1.0.zip", "sha256": "1111111111111111111111111111111111111111111111111111111111111111"},
    {"name": "ai-first-vibe-coding.skill", "sha256": "2222222222222222222222222222222222222222222222222222222222222222"}
  ]
}
```

Tests supply a deterministic fake commit. Production packaging obtains the real commit from Git and fails when the tree has uncommitted tracked changes during release mode.
- [ ] Add a deterministic eval runner/rubric that records executed versus documented-only cases without inventing model results.
- [ ] Rewrite both READMEs around a 60-second path, evidence boundary, installation lifecycle, support, and brand assets.
- [ ] Bump metadata/changelog to `1.1.0` only after behavior and package contracts are internally consistent.
- [ ] Run `python scripts/validate.py`, package tests, eval runner dry validation, `pwsh -File scripts/package.ps1`, archive inspection, checksum verification, and `git diff --check`.

### Task 3: Icarus Spring Scaffold v1.1.0

**Worktree:** `<workspace>/worktrees/icarus-v1.1-productization`

**Files:**
- Modify: `icarus-scaffold-cli/src/main/java/io/github/boomkalakasha/icarus/scaffold/cli/ScaffoldCli.java`
- Create: `icarus-scaffold-cli/src/main/java/io/github/boomkalakasha/icarus/scaffold/cli/SafeOutputFile.java`
- Modify: `icarus-scaffold-cli/src/test/java/io/github/boomkalakasha/icarus/scaffold/cli/ScaffoldCliContractTest.java`
- Create: `icarus-scaffold-cli/src/test/java/io/github/boomkalakasha/icarus/scaffold/cli/SafeOutputFileTest.java`
- Modify: `scripts/generate-sample.py`, `scripts/test_generate_sample.py`, `.github/workflows/ci.yml`
- Modify: `icarus-scaffold-core/src/main/resources/templates/project/Dockerfile.ftl`
- Modify: `icarus-scaffold-core/src/main/resources/templates/project/compose.yaml.ftl`
- Modify: `icarus-scaffold-core/src/main/resources/templates/project/README.md.ftl`
- Modify: `icarus-scaffold-core/src/main/resources/templates/project/README.zh-CN.md.ftl`
- Modify: `icarus-scaffold-core/src/main/resources/templates/project/SECURITY.md.ftl`
- Modify: `icarus-scaffold-core/src/main/java/io/github/boomkalakasha/icarus/scaffold/core/rendering/TemplateRenderer.java`
- Create: `icarus-scaffold-core/src/main/resources/templates/project/LICENSE.ftl`
- Create: `icarus-scaffold-core/src/main/resources/templates/project/SUPPORT.md.ftl`
- Modify: `README.md`, `README.zh-CN.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `pom.xml`
- Create: `docs/architecture.md`, `docs/cli.md`, `docs/rest-api.md`, `docs/generated-project.md`, `docs/troubleshooting.md`
- Create: `docs/assets/brand/brand-mark.svg`, `docs/assets/brand/avatar.png`, `docs/assets/brand/watermark-dark.svg`, `docs/assets/brand/watermark-light.svg`

- [ ] Add RED tests proving `--output demo.zip` writes a valid ZIP and stdout mode remains byte-compatible.
- [ ] Add RED tests rejecting absolute paths, nested paths, `..`, non-ZIP names, and existing files without deletion or overwrite.
- [ ] Implement the smallest cwd-confined `SafeOutputFile` and CLI integration.

The Java contract is intentionally narrow:

```java
final class SafeOutputFile {
    static Path resolve(Path workingDirectory, String requestedName) {
        // Accept exactly one relative *.zip filename and reject an existing target.
    }
}
```

`ScaffoldCli` receives a working directory in its package-private test constructor, preserves the current stdout constructor, and uses `StandardOpenOption.CREATE_NEW` so a race cannot turn validation into overwrite behavior.
- [ ] Extend sample tests first to specify package, runtime health/greeting, Docker/Compose capability states, and cleanup semantics.
- [ ] Implement runtime smoke with bounded ports/timeouts and cleanup in `finally`; Docker absence must report `NOT_RUN`, while Docker present failures are `FAIL`.
- [ ] Repair image health tooling and generated public governance files; add contract assertions for every new template entry.
- [ ] Add bilingual quick start, release download, PowerShell/POSIX commands, architecture, CLI, REST, troubleshooting, and exact support matrix.
- [ ] Bump Maven/changelog to `1.1.0` after tests specify the new public contract.
- [ ] Run the full Maven reactor, Python tests, generated sample package/runtime, REST smoke, Docker build/Compose health, public tree/history/generated scans, and `git diff --check`.

### Task 4: Icarus Open-source Governance Skill v1.0.0

**Repository:** `<workspace>/open-source/icarus-open-source-governance-skill`

**Files:**
- Create: `SKILL.md`, `README.md`, `README.zh-CN.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md`, `compatibility.md`
- Create: `.icarus-open-source.example.yml`, `schemas/icarus-open-source.schema.json`
- Create: `references/public-readiness.md`, `references/privacy-and-provenance.md`, `references/documentation-and-localization.md`, `references/branding.md`, `references/licensing.md`, `references/github-delivery.md`, `references/evidence-gates.md`
- Create: `templates/README.md`, `templates/README.zh-CN.md`, `templates/CONTRIBUTING.md`, `templates/SECURITY.md`, `templates/SUPPORT.md`, `templates/CHANGELOG.md`
- Create: `scripts/validate.py`, `scripts/scan_public_risks.py`, `scripts/package.ps1`, `scripts/test_validate.py`, `scripts/test_scan_public_risks.py`
- Create: `evals/evals.json`, `evals/trigger-evals.json`, baseline/with-skill evidence summaries
- Create: `.github` issue/PR templates, CODEOWNERS, Dependabot, CI, CodeQL, release workflows

- [ ] Run at least three realistic baseline prompts without the new Skill and record missed boundaries/rationalizations before writing `SKILL.md`.
- [ ] Write failing tests for config schema, privacy scan, bilingual navigation, generic defaults, and absence of forced BOOMKALAKASHA attribution.
- [ ] Implement the smallest Skill and references that close observed baseline failures.

The example configuration must validate this shape without making the example owner a default:

```yaml
schemaVersion: 1
project:
  name: example-project
  languages: [en, zh-CN]
license:
  decision: review-required
privacy:
  scanReachableHistory: true
  forbiddenPatterns: []
brand:
  mode: none
  profile: null
git:
  flow: github-flow
  commits: conventional-commits
release:
  versioning: semver
  immutable: true
evidence:
  requireLocal: true
  requirePublicHost: true
```
- [ ] Run the same prompts with the Skill, grade objective assertions, and record limitations; use `DOCUMENTED_ONLY` for hosts not executed.
- [ ] Validate all templates, links, schema, scripts, package contents, current tree, reachable history, and brand configuration variants (`none`, `subtle`, `full`).
- [ ] Package `.skill` plus checksum from one staged tree and prepare immutable `v1.0.0` release notes.

### Task 5: Cross-repository review and public delivery

- [ ] Main controller performs spec compliance review for each repository before code-quality review.
- [ ] Fix all Critical/Important findings and re-run affected tests.
- [ ] Copy the exact canonical brand assets to consumers and compare hashes.
- [ ] Verify no absolute local paths, internal domains, credentials, customer data, or unlicensed assets exist in tree, reachable history, or packages.
- [ ] Commit each repository with truthful Conventional Commit subjects and explanatory bodies where needed.
- [ ] Push feature branches; create PRs; require green CI/CodeQL before merge.
- [ ] Create the new GitHub repository through an authenticated session, apply description/topics/rulesets, and record settings evidence.
- [ ] Merge only after P0/P1 reaches zero; publish exact-tag immutable releases and validate every downloadable checksum.
- [ ] Do not change the public GitHub avatar without a separate action-time confirmation.
