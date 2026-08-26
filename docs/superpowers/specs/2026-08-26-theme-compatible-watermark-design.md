# Theme-compatible BOOMKALAKASHA Watermark Design

## Goal and scope

Make the BOOMKALAKASHA wordmark readable on ordinary light and dark Markdown surfaces, especially GitHub README rendering, without replacing the existing symbol or palette. Governance remains the canonical source; AI-first Vibe Coding Skill and Icarus AI Spring Scaffold receive verified copies. This change updates repository `main` branches through pull requests and does not create new SemVer tags or Releases.

## Current failure

The READMEs embed `watermark-dark.svg`, whose Midnight wordmark is intended for light surfaces and has no contrasting keyline. GitHub dark mode therefore renders the name with insufficient contrast. The explicit light variant is readable on dark surfaces, but Markdown cannot reliably choose it outside GitHub-specific fragment conventions.

## Chosen design

Add `watermark-auto.svg` as the default documentation asset. Its base rendering uses a Midnight wordmark with a Warm-white keyline, so the name remains identifiable even when a renderer ignores embedded CSS. A `prefers-color-scheme: dark` media query swaps the fill and keyline for stronger native dark-mode contrast. The existing `watermark-dark.svg` gains the same fallback keyline; `watermark-light.svg` stays the explicit dark-surface variant.

README files use only `watermark-auto.svg`. Explicit variants remain documented for controlled surfaces. Icarus adds the automatic watermark to both English and Chinese README files so all three public repositories expose the same brand behavior.

## Source and synchronization

- Canonical assets: `assets/brand/boomkalakasha/` in Governance.
- AI copies: `assets/brand/` and `docs/assets/brand/`.
- Icarus copies: `docs/assets/brand/`.
- Canonical and copied `watermark-auto.svg` files must have identical SHA-256 hashes.

## Compatibility and failure behavior

- Modern external-SVG renderers: automatic light/dark fill selection.
- CSS-stripping or media-query-unaware renderers: theme-neutral contrast keyline remains visible.
- Explicit background ownership: callers may continue using `watermark-dark.svg` on light surfaces or `watermark-light.svg` on dark surfaces.
- No JavaScript, remote font, external image, local path, metadata, or raster dependency is introduced.

## Verification

1. RED/GREEN contract tests require the new asset, exact live wordmark, media query, fallback keyline, README references, and canonical-copy hashes.
2. Existing validators continue checking XML, accessibility title/description, palette, forbidden content, UTF-8 and package contents.
3. Render the canonical specimen in forced light and dark browser modes and capture screenshots.
4. Run all three repository test suites, Markdown/public-content checks and `git diff --check`.
5. Push short branches, create PRs, wait for required GitHub checks, then merge without moving existing tags.

## Acceptance

- `BOOMKALAKASHA` is visibly readable in both forced color schemes at README scale.
- README files in all three repositories reference `watermark-auto.svg`.
- All copies match the Governance canonical SHA-256.
- No P0/P1 validator, CI, link, packaging, security or public-content regression remains.

