# BOOMKALAKASHA Open-source Productization Design

## Objective

Upgrade `ai-first-vibe-coding-skill` and `icarus-ai-spring-scaffold` from sound first public releases into approachable, evidence-led open-source products, and create a reusable `icarus-open-source-governance` Skill that can repeat the process without hard-coding personal or company information.

## Operating boundary

| Item | Allowed | Boundary |
| --- | --- | --- |
| Local files | Yes | Three isolated repositories/worktrees only |
| Tests/builds/containers | Yes | Local verification artifacts may be created and cleaned |
| Git branches/commits/push | Yes | Feature branches; no direct push to existing `main` |
| GitHub repository creation/settings/PR/release | Yes | Only after local gates pass; authenticated browser required |
| Personal GitHub avatar change | No implicit change | Deliver the avatar file; request action-time confirmation before changing the public profile |
| Secrets | No | Never read, print, store, or transmit secret values |
| Image API | Conditionally allowed | CLI fallback was approved, but the current machine has no `OPENAI_API_KEY`; use deterministic SVG/PNG fallback and keep ImageGen enhancement blocked |

## Baseline facts

- AI Skill `main`/`v1.0.0` is `7b57db5`; current validation checks 37 text files successfully.
- Icarus `main`/`v1.0.0` is `e77a04b`; current baseline passes 33 Java tests, 7 Python tests with one Windows symlink skip, generated six-module sample tests, and tree/history public-content scans.
- Both public repositories have empty topics and no active rulesets.
- Icarus public description contains broken words (`multi-modul`, `elivery`), and its English README has no Chinese entry.
- AI Skill v1.0.0 release assets and release copy are not fully aligned; Icarus v1.0.0 assets exist and its release is immutable.

## Product architecture

### Shared brand contract

The personal brand is `BOOMKALAKASHA`, represented by a warm energy core and a kinetic circuit/orbit mark. The primary mark must remain recognizable at 40 px. The avatar contains the symbol only. Wordmarks render `BOOMKALAKASHA` as live/vector text so spelling is deterministic.

Palette: midnight `#10162F`, electric cyan `#35D6FF`, amber `#FFB65A`, coral `#FF6B6B`, warm white `#F7F4EC`.

Canonical assets:

- `brand-mark.svg`: scalable source.
- `avatar.png`: square GitHub avatar.
- `watermark-dark.svg` and `watermark-light.svg`: horizontal transparent wordmarks.
- `brand-preview.png`: reference for the personal artifact-template.
- `brand-guidelines.md` and `brand-preview.html`: usage and visual QA.

Each project keeps a local stable copy under `docs/assets/brand/`. The governance Skill also carries the kit as an example. Its configuration can disable branding or replace every asset and owner field.

### AI-first Vibe Coding Skill v1.1.0

- Add a 60-second quick start and truthful status summary.
- Document pinned installation, checksum verification, upgrade, rollback, and uninstall in both languages.
- Make one canonical package command produce `.zip`, `.skill`, and checksums from the exact same staged tree.
- Add deterministic package-content tests and an eval runner/rubric without claiming unrun host compatibility.
- Link the specialized Icarus governance Skill for deep open-source readiness while retaining the existing lightweight GitHub delivery profile.
- Add subtle brand assets, CI/release/license badges, support navigation, and synchronized bilingual headings.

### Icarus Spring Scaffold v1.1.0

- Put language and quick-start links at the top of both READMEs.
- Add a secure CLI `--output <filename.zip>` option. Only a single filename under the current working directory is accepted; absolute, nested, parent-traversal, non-ZIP, and existing targets are rejected. Stdout remains the default contract.
- Provide release-asset and source-build paths for PowerShell and POSIX shells.
- Align JDK/Maven requirements and add stable architecture, CLI, REST, generated-layout, compatibility, and troubleshooting docs.
- Extend generated-sample verification from `test` to `package`, runtime health/greeting smoke, Compose parse, image build, and container health when Docker is available. Docker-unavailable states remain explicit rather than silently passing.
- Repair the generated container healthcheck and add public LICENSE/SUPPORT guidance without pretending a downstream owner has configured a private contact.
- Keep arbitrary output paths, overwrite, custom shell commands, and template-directory injection out of scope.

### Icarus Open-source Governance Skill v1.0.0

Trigger when a user wants to open-source, sanitize, publish, brand, license, or establish GitHub governance for a repository. It complements, rather than duplicates, general implementation workflows.

Core phases:

1. Establish ownership, provenance, repository, history, artifact, and side-effect boundaries.
2. Classify current claims as FACT, INFERENCE, or NOT_VERIFIED.
3. Evaluate license/third-party obligations and stop for legal ownership ambiguity.
4. Scan current tree, reachable history, generated artifacts, image metadata, and release bundles for public risks.
5. Create bilingual user and contributor documentation with stable navigation.
6. Apply optional brand configuration without requiring personal attribution.
7. Configure GitHub Flow, Conventional Commits, SemVer, CI/security, rulesets, releases, checksums, SBOM, and provenance.
8. Run local, package, public-host, and release evidence gates separately.

Configuration file: `.icarus-open-source.yml`. Required sections are project identity, languages, license decision state, privacy policy, brand mode, Git workflow, release mode, and evidence gates. All BOOMKALAKASHA values live in the example profile only.

## Documentation design

README first screen order:

1. Brand mark, project name, one-sentence value.
2. Language/navigation links and live badges.
3. A copyable 60-second path.
4. What it does / when to use / what it deliberately does not promise.
5. Architecture or workflow.
6. Installation, usage, troubleshooting, support, contribution, security, release, license.

Friendly tone comes from short sentences, small callouts, realistic examples, and restrained iconography. It must not become marketing copy that outruns evidence.

## Verification matrix

| Gate | AI Skill | Icarus | Governance Skill | Brand |
| --- | --- | --- | --- | --- |
| Static | frontmatter, links, JSON, UTF-8, package manifest | Java/Python/style/public scan | schema, links, templates, scan rules | SVG/XML, alpha, dimensions, spelling |
| Behavior | package parity, eval runner/rubric | CLI negative/positive, REST contracts | baseline vs with-skill scenarios | 40 px legibility, dark/light contrast |
| Runtime | Codex explicit/natural trigger where available | generated jar health/greeting and optional container | validator/package execution | browser specimen desktop/mobile |
| Public | branch, PR, CI/CodeQL, exact-tag assets | branch, PR, CI/CodeQL, SBOM/checksum | new repo, PR, CI/CodeQL, packaged Skill | README rendering and social-preview readiness |
| Governance | no claim drift, rollback documented | no unsafe path/overwrite regression | privacy/license/brand all configurable | no forced personal attribution |

Release is blocked while any P0/P1 is open. P2 items may remain only when documented with owner, evidence, and follow-up.

## Rollback

- Existing `main` and `v1.0.0` tags remain untouched.
- Work occurs in isolated feature branches/worktrees.
- Public changes arrive through PRs; the pre-change release remains downloadable.
- Repository settings changes are recorded so rulesets, topics, descriptions, and social assets can be restored.

