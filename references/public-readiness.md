# Public-readiness workflow

## 1. Establish the candidate boundary

Record the intended public repository, baseline commit, allowed modules, excluded material, dirty files, and all separately authorized side effects. A private repository request is a non-trigger: retain its internal delivery process.

## 2. Classify evidence

Use `FACT` for observed source or command output, `INFERENCE` for a supported but unproven conclusion, and `NOT_VERIFIED` for anything not observed. Keep local candidate, public-host release, and production/cutover states separate.

## 3. Run local gates

Run the validator, current-tree and reachable-history scanner, project build/tests, generated/package scan, documentation checks, package build, and checksum verification. Investigate scanner findings; a pass is not a legal approval or proof that a scanner covers every risk.

## 4. Prepare the public contract

Document project purpose, non-goals, installation, support, contribution, security, license, release, upgrade/rollback boundaries, and bilingual navigation. Use templates as starting points, not claims that channels or support arrangements already exist.

## 5. Use remote gates

After local gates and explicit authority, create or update GitHub resources through reviewed GitHub Flow. Verify the actual PR, required checks, CodeQL, settings, immutable tag, release assets, checksums, and anonymous download. See [GitHub delivery](github-delivery.md).
