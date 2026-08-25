# GitHub delivery

Use a focused branch and reviewed PR into protected `main`. Verify real GitHub settings instead of treating repository files as proof: branch/ruleset protection, Actions permissions, private vulnerability reporting, default community files, required checks, CodeQL, and release controls are all remote facts.

Keep fork PRs read-only; do not use `pull_request_target` to execute untrusted checkout code. Pin third-party Actions and images to reviewed immutable identifiers. The included workflows pin their referenced Actions but must still be reviewed and updated deliberately.

Tag only an audited default-branch commit with immutable SemVer. Create the release from that exact tag, attach assets and `SHA256SUMS.txt`, then verify the public release page and an unauthenticated download. GitHub's [release documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) and [CodeQL documentation](https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-with-codeql) are authoritative for current platform behavior.
