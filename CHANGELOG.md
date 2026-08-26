# Changelog

All notable changes are documented here. Releases use immutable SemVer tags after their local and remote evidence gates are satisfied.

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
