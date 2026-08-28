# Release documentation synchronization

GitHub Releases are the public publication fact. A source version, tag, README
sentence, or successful local package is supporting evidence, but none should
independently claim to be the latest public release.

## README contract

Each public language README must contain:

```markdown
<!-- icarus-release-fact: dynamic -->
[Latest GitHub Release](https://github.com/OWNER/REPOSITORY/releases/latest)
[Complete release history](https://github.com/OWNER/REPOSITORY/releases)
```

Do not write a sentence such as “the latest public stable release is v1.2.3”.
That text becomes stale immediately after the next Release. Version-specific
installation instructions may still name an immutable tag when the surrounding
text clearly identifies it as that tag, not as “latest”.

## Local check

```bash
python scripts/check_release_docs.py \
  --tag v1.2.3 \
  --version 1.2.3 \
  --repository OWNER/REPOSITORY \
  --readme README.md \
  --readme README.zh-CN.md
```

The checker uses only the Python standard library. It validates stable SemVer,
tag/source-version equality, both dynamic links, the shared marker, and the
absence of a hard-coded latest-version claim.

## Reusable GitHub Action

This repository owns `actions/release-doc-sync/action.yml`. Its inputs are
`tag`, `version`, `repository`, `readme`, and `readme_zh`. The
Governance release workflow consumes the action locally.

Another repository should adopt it only after the Governance change is merged
and publicly reachable:

1. Review and publish the Governance change through its normal protected-main
   flow.
2. Resolve the reviewed commit to its full 40-character SHA.
3. Add the external `uses:` reference at that exact SHA; do not use a branch,
   moving tag, abbreviated SHA, or an unpublished future reference.
4. Run the consumer repository's pull-request and release workflows.
5. Record the remote workflow URL and conclusion as public-host evidence.

This ordering prevents a consumer workflow from depending on an action that
does not exist remotely yet. A local passing test is
`STATIC_PASS_PENDING_REMOTE_CI`; it is not proof that the shared action was
fetched or executed by GitHub.
