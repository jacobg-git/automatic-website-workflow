# Current Project State

## Current Priority and Status

The user requested a reusable GitHub-installable version of the **current process-worker workflow**, explicitly deferred native subagents, and subsequently requested **public repository access after a security review**: `jacobg-git/automatic-website-workflow`.

**Version 0.2.1 is published and verified** at the [GitHub release](https://github.com/jacobg-git/automatic-website-workflow/releases/tag/v0.2.1). Authenticated installation directly from its GitHub tag passed in a fresh environment. It preserves the 0.2.0 runtime and fixes CI-only test assumptions (missing `agy`, Windows short/long temporary-path aliases). The original v0.2.0 tag was not moved. Read [INSTALL.md](../INSTALL.md) for the agent-facing install/run procedure and [distribution details](workflow/distribution.md) for implementation and evidence. Native parent/child delegation is still unimplemented; the [migration plan](workflow/native-subagents.md) follows distribution.

## Implemented Distribution

- Standard wheel/sdist includes canonical roles, default configuration, examples, and the installed operating guide; runtime does not depend on this source checkout.
- Pip installs Playwright; `setup --project ROOT` installs project-local instructions/registrations and downloads Chromium using the selected Python environment.
- Ownership-aware installer preserves host instructions, unrelated agents, README, custom configuration, and CRLF/BOM bytes outside owned blocks. Conflicts/links/active-run locks stop installation instead of overwriting.
- Installed resources live under `.website-workflow/`, registrations under `.agents/agents/`, and private business outputs under Git-ignored `.website-workflow/businesses/`.
- `new-business` scaffolds an unverified intake for a specific name/location; the operating agent verifies identity/facts/CTA before `validate-intake` and `run`. It must not invent missing facts or bypass verification flags.
- Worker processes now run from the actual host workspace rather than the development repository/site-packages.
- Prerequisites not supplied by the repo: Python/Git/public network access, authenticated Antigravity CLI/model entitlement/quota, and any privileged Linux browser system libraries. No credentials are collected or global agent permissions changed.

## Validation

- **59 tests executed: 58 passed, one real-symlink case skipped on Windows due to missing privileges.** A simulated link-guard test passes; CI can exercise the real case on Linux.
- Built wheel and sdist, including a wheel rebuilt from sdist.
- Installed into a fresh virtual environment outside the checkout, with dependencies resolved independently (Playwright 1.64.1 / Chromium 156.0.8078.4).
- Isolated installed-wheel test preserved host instructions, ran setup/doctor and business scaffolding, then completed real Chromium screenshots, ZIP packaging, and a no-inference completed rerun using explicitly simulated model/visual results. No new paid inference was used for distribution validation.
- [GitHub Actions run 41338403058](https://github.com/jacobg-git/automatic-website-workflow/actions/runs/41338403058) passed all four Linux/Windows × Python 3.11/3.13 jobs, including isolated fresh-project wheel tests. It tested release source commit `65bc431`.
- Final authenticated `pip install` from `v0.2.1`, followed by isolated fresh-host setup/browser/delivery checks, passed with zero model calls. That verification occurred while the repository was private; only workflow distribution assets were attached. The latest user request makes public access the target, with client data still excluded.

## Existing Live Baseline

The earlier fictional pilot at `projects/live-demo-001/` completed real parallel Flash research, Argon planning/building, two correction cycles, native image-view receipts, static packaging, and an unsent email draft. It remains `awaiting_approval`, with no active worker or lock at its last verification. Its 12 started calls reported 423,411 successful-task tokens, excluding interrupted work and separate smoke tests.

This baseline uses independent `agy` processes, **not native subagents**. Nothing was uploaded, published as a client website, or sent. Generated projects/traces/ZIPs are local and Git-ignored, not part of the reusable repository.

## Next Steps

1. Use [INSTALL.md](../INSTALL.md) to install the pinned public release in target projects and operate it for named businesses; keep client data excluded and stop locally for approval.
2. When requested, return to [native subagent migration](workflow/native-subagents.md), preserving deterministic helpers, receipts, budgets, and approval gates. This release remains process-worker execution.
3. Before real-client production, strengthen source corroboration/conflict/negative-claim handling. Empty search results are not proof of nonexistence or registration status.
4. Additional reliability/QA work remains: graceful pause/cancel, transactional site writes, clearer cost accounting, long-page crops, broader accessibility/performance/cross-browser tests, and actual Pi/Codex worker integrations. CI also reports non-failing deprecated Node 20 action warnings to address in maintenance.

## Approval Boundary

The workflow stops locally. Client preview uploads, public deployment, email sending, purchases, domain changes, and expanded credential use require separate approval. Publishing the reusable workflow source publicly to GitHub is distinct from publishing client websites. Follow [SECURITY.md](../SECURITY.md); public read access does not grant repository write access, model-account access, or access to local client files. Passed tests/fictional pilots are not factual, legal, licensing, full accessibility, or production guarantees.
