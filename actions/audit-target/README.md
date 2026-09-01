# Audit a target repository in GitHub Actions

This composite Action runs Icarus's target-repository audit against one checked
out repository and its in-repository policy. It is a CI entry point for the
same evidence boundary as:

```text
python scripts/audit_target.py --root <repository> --policy .icarus-open-source.yml --history
```

It reports source and policy evidence; it is **not legal approval**, ownership
approval, a GitHub-settings check, or authority to publish a release.

## Prerequisites

1. Check out the target repository before invoking the Action.
2. Keep the policy inside that target repository. The policy path is resolved
   below `root`; paths outside the target are rejected.
3. Provide Python on the runner.
4. If the policy marks Gitleaks and REUSE as `required`, install those tools in
   the runner before this step. This Action never downloads them, never accepts
   a policy-supplied executable or shell command, and fails closed when a
   required tool is absent, times out, or exits nonzero.

## Example

After the immutable `v1.1.0` tag is published, pin the Action to that reviewed
version (or a reviewed immutable commit in stricter environments):

```yaml
steps:
  - uses: actions/checkout@<reviewed-immutable-commit>
    with:
      fetch-depth: 0
  - uses: actions/setup-python@<reviewed-immutable-commit>
    with:
      python-version: "3.12"
  - name: Audit the public candidate
    uses: boomkalakasha/icarus-open-source-governance-skill/actions/audit-target@v1.1.0
    with:
      root: .
      policy: .icarus-open-source.yml
      history: "true"
```

`root` defaults to `.`; `policy` defaults to `.icarus-open-source.yml`; and
`history` defaults to `true`. A zero exit means the declared automated checks
returned `PASS`. `HUMAN_REVIEW`, `HOLD`, `NOT_RUN`, or a finding still needs the
maintainer's decision and must not be converted into a release claim.
