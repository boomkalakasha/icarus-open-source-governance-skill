# Evidence gates

| Gate | Required evidence | Status when unavailable |
| --- | --- | --- |
| Local | validator, scanner, project build/tests, docs, package, checksums | `NOT_RUN` or `FAIL` |
| Package | staged manifest, archive contents, checksum verification, generated risk scan | `NOT_RUN` or `FAIL` |
| Public host | PR, CI/CodeQL, settings, exact tag, release assets, public download | `DOCUMENTED_ONLY` until inspected |
| Production | deployment, configuration, data, operational and cutover acceptance | separate from OSS release |

`LOCAL_CANDIDATE_PASS` means only the declared local gates passed. `PUBLIC_RELEASE_PASS` needs observed remote evidence. `PRODUCTION_READY` cannot be inferred from either. Any unresolved P0/P1 privacy, ownership, security, or package finding keeps public release `BLOCKED`.
