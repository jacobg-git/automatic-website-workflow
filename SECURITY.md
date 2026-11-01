# Security policy

## Reporting a vulnerability

Use **Report a vulnerability** in the repository's Security tab (GitHub private vulnerability reporting):

https://github.com/jacobg-git/automatic-website-workflow/security/advisories/new

Do not post working credentials, private business evidence, model traces, or sensitive reproduction data in a public issue. No guaranteed response timeframe or security certification is implied. Prefer the latest documented release and check advisories before installation.

## Public source is not public client data

This repository contains reusable code, instructions, fictional examples, tests, and documentation. Business outputs, raw model traces, screenshots, local environments, `.env`, certificates, and credentials must remain outside Git. Both the development repository and installed-project guide exclude generated business directories. Git-ignore rules do not remove already committed data: review staged changes and history before publishing your own project.

The pre-publication audit scanned all six existing commits with Gitleaks 8.30.1, inventoried every historical tracked path, and scanned extracted wheel/source archives from both published releases. No secrets were detected, and generated business/client files were absent. This is a bounded audit, not proof that no vulnerability or undiscovered sensitive value exists. Historical setup/research notes retain local filesystem paths, and Git contains GitHub noreply author metadata; history was not rewritten or represented as fully anonymized.

## Runtime boundaries

- The current workflow uses independent `agy` worker processes, not native subagents.
- Model login/entitlement and provider quota are external prerequisites. Never put access tokens in repository URLs, prompts, intake files, or committed configuration. Public GitHub installation needs no GitHub credentials; model authentication is still required.
- Run in a dedicated, low-privilege project environment without unrelated secrets accessible to agents. Model providers receive task context under their own policies. Session tool/command restrictions and sandboxing reduce risk but are not a complete security boundary for arbitrary agent code.
- Treat public pages, search results, reviews, source files, and generated code as untrusted data. Do not follow instructions embedded in research sources or bypass platform restrictions.
- Static checks, localhost browser QA, restricted normal network requests, and receipt-backed screenshot inspection are quality gates, not a complete browser/network sandbox or penetration test. Do not execute unfamiliar generated code with production credentials or privileged access.
- No automatic preview upload, publishing, email sending, purchases, domain changes, or expanded credential use. These require separate explicit approval. A successful local draft is not authorization to perform them.
- Structural fact/source validation is not independent corroboration. Do not infer registration status or nonexistence from absent web results. Review factual claims, assets, privacy, licensing, and accessibility before real-client publication.
- Token limits are soft accounting, not provider billing caps. Monitor your account and stop unexpected loops.

## Installation and supply chain

Use a project virtual environment and the pinned release in [INSTALL.md](INSTALL.md), not an unreviewed fork or arbitrary script piped into a shell. Immutable commit pins offer stronger provenance than movable branch names. Existing release tags are not silently rewritten. Old release archives may mention the repository's previous private visibility; the current installation guide is authoritative about public access.

The installer preserves existing host instructions, checks managed-file ownership, rejects linked destinations/conflicts, and does not change global agent permissions. It is not a whole-filesystem transaction or protection against an adversarial process modifying the filesystem concurrently. Keep backups and inspect interrupted installations before retrying.

CI has read-only repository permissions, pinned action revisions, no persisted checkout credentials, and no model-account secrets. The secret-scan job downloads a pinned scanner with a fixed checksum and redacts findings; reports are not published as artifacts. Dependency updates are proposed through pull requests, not automatically merged. Maintainers must review workflow/dependency changes and untrusted fork contributions before approving CI execution.

If a secret is ever committed, revoke/rotate it immediately, then review Git history, release assets, logs, and forks. Merely deleting it in a new commit is not sufficient.
