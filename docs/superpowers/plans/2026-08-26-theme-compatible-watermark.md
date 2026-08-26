# Theme-compatible Watermark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish one theme-compatible BOOMKALAKASHA watermark contract and synchronize it across the three public repositories.

**Architecture:** Governance owns the canonical SVG and executable contract. AI Skill and Icarus keep byte-identical documentation copies and repository-specific README/tests; embedded CSS improves native theme rendering while a contrasting text keyline is the no-CSS fallback.

**Tech Stack:** SVG 1.1-compatible XML, CSS `prefers-color-scheme`, Python `unittest`, PowerShell packaging, Markdown, GitHub Actions.

---

### Task 1: Lock the canonical failing contract

**Files:**
- Modify: `scripts/validate_brand.py`
- Modify: `scripts/test_validate_brand.py`
- Modify: `assets/brand/boomkalakasha/brand-guidelines.md`
- Modify: `docs/brand/preview.html`

- [x] **Step 1: Add a failing canonical asset test**

Require `watermark-auto.svg`, its exact wordmark, `prefers-color-scheme: dark`, `.wordmark` class, Warm-white fallback stroke, and preview references on both light and dark surfaces.

- [x] **Step 2: Verify RED**

Run `python -m unittest scripts.test_validate_brand -v` from Governance. Expected: failures report missing `watermark-auto.svg` and missing automatic preview references.

- [x] **Step 3: Extend the validator contract**

Add `watermark-auto.svg` to `SVG_NAMES` and require its media query plus theme-neutral keyline without weakening existing forbidden-content or palette checks.

- [x] **Step 4: Re-run the focused test**

Run `python -m unittest scripts.test_validate_brand -v`. Expected: it still fails only because the production SVG and specimen have not yet been created.

### Task 2: Implement and render the canonical asset

**Files:**
- Create: `assets/brand/boomkalakasha/watermark-auto.svg`
- Modify: `assets/brand/boomkalakasha/watermark-dark.svg`
- Modify: `assets/brand/boomkalakasha/brand-guidelines.md`
- Modify: `docs/brand/preview.html`
- Modify: `README.md`
- Modify: `README.zh-CN.md`

- [x] **Step 1: Add the automatic SVG**

Copy the existing geometry, assign the wordmark a `.wordmark` class, use Midnight fill with Warm-white `3` px keyline as fallback, and swap to Warm-white fill with Midnight keyline inside `@media (prefers-color-scheme: dark)`.

- [x] **Step 2: Harden the explicit light-surface asset**

Give `watermark-dark.svg` a Warm-white `3` px keyline so accidental use on a dark surface remains readable without changing its intended Midnight fill.

- [x] **Step 3: Update documentation and specimen**

Point both Governance READMEs to `watermark-auto.svg`; document automatic and explicit usage; render automatic variants on both specimen surfaces.

- [x] **Step 4: Verify GREEN and render**

Run `python -m unittest scripts.test_validate_brand -v`, `python scripts/validate_brand.py`, and `python scripts/validate.py`. Serve `docs/brand/preview.html`, force light/dark color schemes in a real browser, and capture both screenshots. Expected: tests pass and the complete wordmark remains readable in both captures.

### Task 3: Synchronize AI-first Vibe Coding Skill

**Files:**
- Create: `assets/brand/watermark-auto.svg`
- Create: `docs/assets/brand/watermark-auto.svg`
- Modify: `assets/brand/watermark-dark.svg`
- Modify: `docs/assets/brand/watermark-dark.svg`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `docs/brand.md`
- Modify: `scripts/validate.py`
- Modify: `scripts/test_product_docs.py`
- Modify: `scripts/test_package.py`

- [x] **Step 1: Add failing copy and README tests**

Require both automatic copies, byte identity between `assets/` and `docs/assets/`, automatic README references, and package inclusion. Run `python -m unittest discover -s scripts -p "test_*.py"`; expected failure is missing automatic assets/references.

- [x] **Step 2: Copy canonical files and update docs**

Copy Governance `watermark-auto.svg` and hardened `watermark-dark.svg` byte-for-byte into both AI asset directories, then update English/Chinese README and brand guidance.

- [x] **Step 3: Verify AI repository**

Run unit tests, `python scripts/validate.py`, `python scripts/run_evals.py`, `pwsh -NoProfile -File scripts/package.ps1 -Version 1.1.1`, and `git diff --check`. Expected: all pass and the package contains `watermark-auto.svg`.

### Task 4: Synchronize Icarus AI Spring Scaffold

**Files:**
- Create: `docs/assets/brand/watermark-auto.svg`
- Modify: `docs/assets/brand/watermark-dark.svg`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `scripts/test_release_documentation.py`

- [x] **Step 1: Add a failing documentation asset test**

Require both READMEs to embed `docs/assets/brand/watermark-auto.svg`, require its theme contract, and compare its SHA-256 with the supplied canonical path during cross-repository verification. Run the focused Python test; expected failure is missing asset/reference.

- [x] **Step 2: Copy canonical files and update READMEs**

Copy the canonical automatic and hardened explicit files into `docs/assets/brand/`, then add the automatic watermark above the title in both READMEs.

- [x] **Step 3: Verify Icarus repository**

Run Python tests, `python scripts/verify-public-content.py --root .`, `mvnw.cmd -B -ntp test`, and `git diff --check`. Expected: 13 Python checks with the known Windows symlink skip and 40 Java tests pass.

### Task 5: Cross-repository delivery

**Files:**
- Verify: all changed files in the three repositories

- [x] **Step 1: Verify canonical hashes**

Compute SHA-256 for every `watermark-auto.svg` and hardened `watermark-dark.svg`. Expected: automatic files match the Governance canonical, and hardened dark files match it across all copies.

- [x] **Step 2: Commit and push each branch**

Use truthful `fix(brand): 提升水印明暗主题可读性` commits, push `fix/theme-compatible-watermark`, and keep the worktrees for PR feedback.

- [x] **Step 3: Create and merge PRs through required checks**

Open one PR per repository, include light/dark screenshots in evidence, wait for every required check, merge with squash, and verify `main` refs. Do not create or move SemVer tags.

## Delivery evidence

- AI-first Vibe Coding Skill: [PR #4](https://github.com/boomkalakasha/ai-first-vibe-coding-skill/pull/4), merged as `313be1f` after `validate-skill` and `codeql-python` passed.
- Icarus AI Spring Scaffold: [PR #18](https://github.com/boomkalakasha/icarus-ai-spring-scaffold/pull/18), merged as `e35221a` after build/sample/public-content, dependency review and CodeQL checks passed.
- Icarus Open-source Governance Skill: [PR #6](https://github.com/boomkalakasha/icarus-open-source-governance-skill/pull/6), merged as `e6bdd60` after validator and CodeQL checks passed.
- `UI_OBSERVED`: forced light/dark local specimen captures and the GitHub dark-theme AI README branch showed a readable complete wordmark.
- Canonical `watermark-auto.svg` SHA-256: `53D0652428691360E9E92E48EFDFBEA00DADABC7F1CE8C115B55C1A9CCB0D8A7`; all four repository copies matched before delivery.
