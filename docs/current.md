# Current Project State

## Current Priority and Status

The user requested a reusable GitHub-installable version of the **current process-worker workflow**, explicitly deferred native subagents, and chose to **keep the existing repository private**: `jacobg-git/automatic-website-workflow`.

Version **0.2.0** packages the workflow for installation in new projects. Read [INSTALL.md](../INSTALL.md) for the agent-facing install/run procedure and [distribution details](workflow/distribution.md) for implementation and evidence. Native parent/child delegation is still unimplemented; the [migration plan](workflow/native-subagents.md) follows distribution.

## Implemented Distribution

- Standard wheel/sdist includes canonical roles, default configuration, examples, and the installed operating guide; runtime does not depend on this source checkout.
- Pip installs Playwright; `setup --project ROOT` installs project-local instructions/registrations and downloads Chromium using the selected Python environment.
- Ownership-aware installer preserves host instructions, unrelated agents, README, custom configuration, and CRLF/BOM bytes outside owned blocks. Conflicts/links/active-run locks stop installation instead of overwriting.
- Installed resources live under `.website-workflow/`, registrations under `.agents/agents/`, and private business outputs under Git-ignored `.website-workflow/businesses/`.
- `new-business` scaffolds an unverified intake for a specific name/location; the operating agent verifies identity/facts/CTA before `validate-intake` and `run`. It must not invent missing facts or bypass verification flags.
- Worker processes now run from the actual host workspace rather than the development repository/site-packages.
- Prerequisites not supplied by the repo: Python/Git, private GitHub read access, authenticated Antigravity CLI/model entitlement/quota, and any privileged Linux browser system libraries. No credentials are collected or global agent permissions changed.

## Validation

- **59 tests executed: 58 passed, one real-symlink case skipped on Windows due to missing privileges.** A simulated link-guard test passes; CI can exercise the real case on Linux.
- Built wheel and sdist, including a wheel rebuilt from sdist.
- Installed into a fresh virtual environment outside the checkout, with dependencies resolved independently (Playwright 1.64.1 / Chromium 156.0.8078.4).
- Isolated installed-wheel test preserved host instructions, ran setup/doctor and business scaffolding, then completed real Chromium screenshots, ZIP packaging, and a no-inference completed rerun using explicitly simulated model/visual results. No new paid inference was used for distribution validation.
- GitHub Actions is configured for Linux/Windows and Python 3.11/3.13; inspect remote run status before claiming CI success.

## Existing Live Baseline

The earlier fictional pilot at `projects/live-demo-001/` completed real parallel Flash research, Argon planning/building, two correction cycles, native image-view receipts, static packaging, and an unsent email draft. It remains `awaiting_approval`, with no active worker or lock at its last verification. Its 12 started calls reported 423,411 successful-task tokens, excluding interrupted work and separate smoke tests.

This baseline uses independent `agy` processes, **not native subagents**. Nothing was uploaded, published as a client website, or sent. Generated projects/traces/ZIPs are local and Git-ignored, not part of the reusable repository.

## Next Steps

1. Publish/verify the reviewed source and pinned `v0.2.0` distribution in the existing private origin; do not change visibility or include client data.
2. Verify authenticated installation from that GitHub tag in a fresh environment and inspect CI status.
3. Then return to [native subagent migration](workflow/native-subagents.md), preserving deterministic helpers, receipts, budgets, and approval gates.
4. Before real-client production, strengthen source corroboration/conflict/negative-claim handling. Empty search results are not proof of nonexistence or registration status.
5. Additional reliability/QA work remains: graceful pause/cancel, transactional site writes, clearer cost accounting, long-page crops, broader accessibility/performance/cross-browser tests, and actual Pi/Codex worker integrations.

## Approval Boundary

The workflow stops locally. Client preview uploads, public deployment, email sending, purchases, domain changes, and expanded credential use require separate approval. Publishing the reusable workflow source privately to GitHub is distinct from publishing client websites. Passed tests/fictional pilots are not factual, legal, licensing, full accessibility, or production guarantees.
