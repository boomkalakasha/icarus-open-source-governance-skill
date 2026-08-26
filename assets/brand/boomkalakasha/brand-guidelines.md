# BOOMKALAKASHA brand kit

BOOMKALAKASHA is a warm, technical personal mark for open-source work. The visual idea is **Warm Pulse Circuit**: human energy in the centre, precise systems around it. The mark suggests a `B` and `K` through opposing angular paths and orbit lines without spelling either letter.

## Canonical palette

| Token | Hex | Use |
| --- | --- | --- |
| Midnight | `#10162F` | dark surfaces, outlines, dark wordmark |
| Electric cyan | `#35D6FF` | primary orbit and active links |
| Amber | `#FFB65A` | pulse, nodes, warmth |
| Coral | `#FF6B6B` | secondary orbit, dividers, emphasis |
| Warm white | `#F7F4EC` | dark-surface wordmark and pulse highlight |

The colour values are deliberately flat. Do not add gradients, glossy effects, 3D lighting, or a drop shadow that changes the silhouette at small sizes.

## Asset roles

- `brand-mark.svg` is the transparent source symbol. Use it when a square mark is needed on a light or transparent surface.
- `avatar.svg` is the square composition with a Midnight background. `avatar.png` is the 1024 × 1024 raster derivative for GitHub and other square profile surfaces.
- `watermark-dark.svg` is for light backgrounds; its wordmark is Midnight.
- `watermark-light.svg` is for Midnight or other dark backgrounds; its wordmark is Warm white with a Midnight keyline.
- `watermark-auto.svg` is the default for README and unknown surfaces. It follows the host colour scheme and retains an opposite-colour keyline when CSS media queries are unavailable.
- `brand-preview.png` is a fixed 1600 × 900 reference board. It is a visual reference, not a replacement for the source SVGs.
- `docs/brand/preview.html` is a self-contained specimen for visual review at realistic sizes.

## Clear space and minimum size

Keep a clear space around the square mark equal to at least one pulse radius (the inner Warm white circle) on every side. For a watermark, keep the same distance above and below the mark and at least half a pulse radius between mark and wordmark.

| Asset | Recommended minimum |
| --- | ---: |
| Square mark / avatar | 40 px |
| Horizontal watermark | 240 px wide |
| Wordmark in a README header | 16 px cap height |

At 40 px, use the avatar composition or `brand-mark.svg` without additional strokes, cropping, or animation. Never redraw the mark from a screenshot.

## Accessibility

- Use `watermark-auto.svg` for README and unknown surfaces. Use `watermark-dark.svg` on controlled light surfaces and `watermark-light.svg` on controlled Midnight or dark surfaces. The specimen shows every pairing.
- Preserve the Warm white and Midnight contrast for wordmarks; do not place the cyan/coral strokes behind body copy.
- Keep the SVG `<title>` and `<desc>` elements intact when embedding the source files.
- Provide adjacent text or an accessible label when the mark is used as navigation. The symbol alone is decorative if the same link already has a visible project name.
- Do not rely on coral versus cyan alone to communicate state; pair colour with text, shape, or a status icon.

## Approved usage

- Keep the wordmark exactly `BOOMKALAKASHA`, with expanded tracking and a geometric sans-serif stack available on the host machine.
- Use the symbol only in square contexts and the horizontal watermark for headers, README sections, or restrained signatures.
- Scale proportionally and keep the mark on a quiet surface. A single small orbit accent is acceptable in a document divider.
- Personal attribution is optional. Projects may use the kit as an example profile or replace the owner and brand configuration entirely.

## Misuse to avoid

- Do not alter the spelling, rotate or stretch the wordmark, or substitute a mascot, emoji, wings, weapons, explosions, or literal letter logo.
- Do not add remote font/image dependencies, embedded base64 images, editor metadata, scripts, or local filesystem references to the SVGs.
- Do not remove the automatic watermark keyline or its theme media query. Explicit variants still need the intended surface even though their keyline provides a misuse fallback.
- Do not reduce the avatar below 40 px, crop the nodes, or overlay it with busy photography.
