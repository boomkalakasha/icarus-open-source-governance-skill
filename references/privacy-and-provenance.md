# Privacy and provenance

Public safety starts with an inventory, not a deletion spree. List source repository/commit, author, rights holder, customer or internal relationship, intended public use, and evidence for every code module, document, template, image, font, generated artifact, and dependency.

Scan the current tree, reachable history, author/committer names and emails, commit messages, branches/tags in scope, generated packages, image metadata, and release assets independently. A current-tree deletion cannot erase an already exposed secret; rotate/revoke a real secret through its owner before deciding how to handle history.

Treat unresolved company ownership, copied text, customer material, personal data, internal hosts, private package registries, or unlicensed images as `BLOCKED`. Do not turn a scanner exclusion into an approval. This is an engineering checklist, not legal advice; use an authorized legal/privacy decision-maker for rights questions.
