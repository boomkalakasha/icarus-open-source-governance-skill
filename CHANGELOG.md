# Changelog

All notable changes are documented here. Releases use immutable SemVer tags after their local and remote evidence gates are satisfied.

## [1.0.5] - 2026-08-28

> Candidate notes for the next release; this version is not public until its
> tag, CI, assets, and release gates are independently verified.

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

> Candidate notes for the next release; this version is not public until its
> tag, CI, assets, and release gates are independently verified.

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
