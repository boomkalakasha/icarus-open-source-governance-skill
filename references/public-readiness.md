# Public-readiness workflow

## 1. Establish the candidate boundary

Record the intended public repository, baseline commit, allowed modules, excluded material, dirty files, and all separately authorized side effects. A private repository request is a non-trigger: retain its internal delivery process.

## 2. Classify evidence

Use `FACT` for observed source or command output, `INFERENCE` for a supported but unproven conclusion, and `NOT_VERIFIED` for anything not observed. Keep local candidate, public-host release, and production/cutover states separate.

## 3. Run local gates

Use `python scripts/validate.py` only to self-check the Governance package.
Audit the selected repository with `python scripts/audit_target.py --root
<repository> --policy .icarus-open-source.yml --history`; this checks its
declared target contract and risk streams without requiring Governance's own
files. Then run the target project's build/tests, generated/package scan,
documentation checks, package build, and checksum verification. Investigate
scanner findings; a pass is not legal approval or proof that a scanner covers
every risk.

When the target policy enables `integrations.gitleaks` or `integrations.reuse`,
the audit invokes only those fixed tool names with fixed argument lists. It
does not install tools or execute policy-provided commands. A missing, timed-out
or nonzero `required` tool is `HOLD`; the same `optional` condition is
`HUMAN_REVIEW`; an omitted integrations section is `NOT_CONFIGURED` and cannot
be cited as external-tool evidence.

## 4. Prepare the public contract

Document project purpose, non-goals, installation, support, contribution, security, license, release, upgrade/rollback boundaries, and bilingual navigation. Use templates as starting points, not claims that channels or support arrangements already exist.

## 5. Use remote gates

After local gates and explicit authority, create or update GitHub resources through reviewed GitHub Flow. Verify the actual PR, required checks, CodeQL, settings, immutable tag, release assets, checksums, and anonymous download. See [GitHub delivery](github-delivery.md).
