# Changelog

All notable changes are documented here. Releases use immutable SemVer tags after their local and remote evidence gates are satisfied.

## [1.1.0] - Unreleased

### Added

- Add a distinct target-repository audit command and reusable composite action.
- Validate target-required files, bilingual navigation, current tree and
  optional reachable history without requiring the target to look like this
  Governance package.
- Keep 1.0.x policy files compatible by applying documented target defaults
  when the new optional `target` section is absent.
- Redact machine-local paths from current public planning sources, record the
  already-published low-sensitivity history without rewriting tags, and reject
  future unrecorded history occurrences with a deterministic boundary gate.
- Add fixed Gitleaks and REUSE adapters with no policy-supplied executable,
  shell, or argument surface. Required tools fail closed; optional missing
  tools and `review-required` license decisions are explicit `HUMAN_REVIEW`.

### Changed

- Make package self-validation explicit and keep target auditing separate.
- Exercise the reusable target-audit Action with an explicit passable CI
  self-policy, while retaining the strict example policy for real release
  candidates; document how consumers can use the Action without treating its
  result as legal or publication approval.
- Create exactly one draft GitHub Release, reject pre-existing release state,
  and verify the exact asset set; publication remains separately authorized.

## [1.0.5] - 2026-08-28

> Public release verified for `v1.0.5` while preparing the 1.1.0 candidate.

### Added

- Added a reusable composite action that checks stable SemVer alignment and
  bilingual README release facts before packaging.
- Added deterministic tests and guidance for adopting the release-documentation
  gate from another repository through an immutable reviewed commit SHA.
- Added an illustrative, redacted release-evidence summary so maintainers can
  see the expected decision output before reading the detailed references.

### Changed

- Replaced hard-coded "latest release" claims with dynamic GitHub Release links
  and packaged the reusable action with the Skill artifact.
- Tightened the bilingual first-glance description around privacy, provenance,
  documentation, licensing, and inspectable release evidence.

## [1.0.4] - 2026-08-27

> Public release verified for `v1.0.4` while preparing the 1.1.0 candidate.

### Changed

- Reworked the English and Chinese READMEs around a core-feature table and a
  dependency-free 60-second review path, so a new maintainer can understand
  the Skill's value and produce inspectable evidence without guessing the
  workflow.
- Added regression coverage for the value proposition, first-review commands,
  and finding-classification guidance in both language editions.

## [1.0.3] - 2026-08-26

### Added

- Added a first-glance bilingual value proposition, a concrete pre-publication scenario, and companion links to the AI-first and Icarus projects.

## [1.0.2] - 2026-08-26

### Fixed

- Add one repository `VERSION` source for default package naming and require an exact stable tag match during release publication.
- De-duplicate unchanged Git blobs during reachable-history risk scanning while retaining a concrete first-seen finding location.
- Record the theme-compatible brand delivery work in the immutable release line.

## [1.0.1] - 2026-08-26

### Fixed

- Remove stale versioned ZIP files before packaging and upload only the archive matching the release tag.
- Preserve top-level dot-prefixed files in Linux release archives without relying on Pillow for brand validation.

## [1.0.0] - 2026-08-25

### Added

- Public-readiness Skill, configuration schema, validator, risk scanner, packaged artifact contract, bilingual documentation, templates, eval rubric, and GitHub community workflow files.
- Optional BOOMKALAKASHA example brand kit with deterministic local contract checks.

### Boundaries

- Local validation and package evidence are not public-host, legal, or production/cutover approval.
