# Legacy public-history note

Some already-published historical planning commits used a machine-local
workspace path. The current source replaces it with `<workspace>` and new
current-tree validation rejects machine-specific workspace/user-home paths.

Those old commits and immutable release tags remain public provenance. They
contained repository layout, not credentials, customer identifiers or runtime
secrets. Rewriting shared history would invalidate existing tag and release
identity, so 1.1.0 records this as an accepted legacy disclosure and prevents
new current-tree occurrences. A future repository migration may create a clean
lineage only through an explicit, separately reviewed ownership decision.

Pre-migration remote heads also still point to trees containing the same
recorded path introduction. The history gate inspects all fetched refs,
case-insensitively, and reports exposed remote heads instead of treating a
clean working tree as proof that the whole public repository is clean. Merging
1.1.0 cleans `main`; removing or rebasing stale heads remains a separately
authorized remote-maintenance action and cannot erase immutable tag history.
