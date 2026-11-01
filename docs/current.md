# Current Project State

## Status

**First full live local demo completed and independently reviewed.** `projects/live-demo-001/state.json` is `awaiting_approval`. No runner/worker is left active, the lock is released, and nothing was uploaded, published, or sent.

This proves the Antigravity local pipeline, not production readiness for arbitrary real clients or native Pi/Codex integration.

## Confirmed Direction

- Static SiteGround websites: parallel research → planning → Argon build → browser/visual QA and fixes → ZIP and unsent outreach draft.
- The conversational orchestrator uses Python for scheduling/checkpoints. Workers return artifacts; only the orchestrator/backend maintain shared docs/state.
- Separate explicit approval remains required for uploads, publication, sending, purchases, domain changes, or expanded credential use.

## Implemented / Verified

- Validated intake/contracts, concurrent exact-model workers, date-stable cache/resume, bounded retries, hash integrity, browser/visual correction loop, packaging and outreach stages.
- Canonical portable roles and native registrations, including primary-only `website-orchestrator`. A full interactive coordinator session remains untested; its registration/instruction synchronization is tested.
- **39 automated tests pass**, including real Chromium integration, working/broken interactions, external-request blocking, image receipts, compact large-source handoffs, next-day resume, and SiteGround/Windows filename portability.
- Image inspection requires successful native `view_file` receipts and matching PNG hashes; model self-reports alone cannot pass release.
- Compact review/revision briefs use readable copy and source references instead of repeating whole code bundles.
- Dependency inspection, compilation, documentation-link checks, and whitespace checks pass. Global runtime permissions were not changed.

## Live Demo Results — 2026-11-01

Project: `projects/live-demo-001/` (Git-ignored fictional bicycle workshop).

- Flash Low researched the business concept and two competitors concurrently; Argon Medium planned; Argon High built and performed two correction cycles.
- Real Chromium checks passed at 390/768/1440px, including mobile navigation and service tabs. Final Argon Medium review opened all five final screenshots and returned **pass with no issues**.
- Independent targeted checks verified tab contrast (minimum sampled ratio 7.57:1), stacked mobile labels, no skip-focus layout shift or disclosure-text overlap, menu click after keyboard focus, Escape/focus return, and tab keyboard behavior. These are targeted checks, not full WCAG certification.
- ZIP contents/CRC/hashes match the reviewed four-file static source manifest, with exact `index.html` at archive root.
- A second completed run used no new inference (call counter stayed 12). Temporary-copy tests rejected both site and ZIP tampering without overwriting edits or calling models.
- Reported successful-task tokens: 423,411. Usage is incomplete because interrupted generations and separate smoke tests are additional/unknown. Token limits are not billing hard caps.

## Local Deliverables

- Site: `projects/live-demo-001/site/`
- ZIP: `projects/live-demo-001/delivery/siteground-static.zip`
- QA: `projects/live-demo-001/qa/latest.md`, `qa/cycle-2.json`, and five final screenshots under `qa/cycle-2/`
- Additional checks: `projects/live-demo-001/qa/targeted-regressions.json`
- Unsent email draft: `projects/live-demo-001/outreach/draft.md` (preview/sender placeholders and an internal sender note still require editing before sending)
- Handoff: `projects/live-demo-001/docs/handoff.md`

## Next Steps

1. Present/review the fictional demo locally; do not upload or send it without explicit approval.
2. Before a real-business pilot, harden source corroboration/conflict handling. Empty search results do not prove business nonexistence or registration status; the demo researcher overclaimed this despite the intake explicitly being fictional.
3. Add graceful pause/cancel, transactional site application, and clearer provider-cost accounting.
4. Improve long-page screenshot crops and broader accessibility/performance/cross-browser coverage.
5. Implement/test native Pi/Codex wrappers and their image receipts; the generic adapter does not yet supply a trusted visual-evidence channel.

See [implementation handoff](workflow/implementation-handoff.md) for commands, runtime details, and remaining gaps. Commit scope is the tested Antigravity MVP, with the remaining hardening work explicitly tracked above. Generated project artifacts are local-only and Git-ignored.
