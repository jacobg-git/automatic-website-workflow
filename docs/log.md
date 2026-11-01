# Documentation Log

Append-only chronological log of meaningful wiki mutations. Do not rewrite previous entries.

## [2026-10-31] docs | Initialize LLM wiki

- Source: [Karpathy: LLM Wiki](raw/karpathy-llm-wiki.md)
- Created: [index](index.md)
- Created: [current state](current.md)
- Created: [base source](raw/karpathy-llm-wiki.md)
- Summary: Initialized the LLM wiki structure and added the base operating-model source.

## [2026-10-31] docs | Capture workflow and research Antigravity feasibility

- Sources: User requirements and approval decision in conversation; official Antigravity documentation linked in the research; [local CLI inspection](raw/antigravity-cli-inspection-2026-10-31.md).
- Created: [workflow overview](workflow/overview.md), [Antigravity feasibility](research/antigravity-feasibility.md), and local inspection evidence.
- Updated: [current state](current.md), [index](index.md), and [root agent instructions](../AGENTS.md).
- Summary: Recorded static SiteGround website goals, parallel role architecture, orchestrator-only shared documentation ownership, and local-only autonomy. Confirmed capability-level Antigravity feasibility and local Argon/Flash catalog entries; documented nested instruction discovery limits, explicit browser activation, model-tier uncertainty, permission soft denials, and documentation/runtime drift. No model inference or end-to-end execution was performed.

## [2026-10-31] docs | Implement local workflow scaffold and preserve continuation handoff

- Sources: User's implementation request and subsequent time-boxed handoff instruction; local source/tests; live Antigravity smoke tests and paused fictional pilot under Git-ignored `projects/`.
- Created: [README](../README.md), [implementation handoff](workflow/implementation-handoff.md), portable role instructions, native registrations, Python workflow runner, example intake/configuration, and automated tests.
- Updated: [current state](current.md), [workflow overview](workflow/overview.md), [research follow-up](research/antigravity-feasibility.md), [index](index.md), and [root instructions](../AGENTS.md).
- Summary: Documented 26 passing tests, live native role/model/structured-output and deny-rule observations, concurrent research plus Argon planning, and the safely paused Argon build. Captured `finish` tool requirement, stdin transport, semantic cache migration, known vision/evidence/cancellation/budget gaps, and exact next commands. Pilot processes were terminated and checkpointed; no upload, publication, sending, or complete live pipeline success is claimed. Work remains intentionally uncommitted.

## [2026-10-31] docs | Record additional interaction, cache, and live image tests

- Sources: User's five-minute testing request; 29-test regression run; cache-only preflight on a temporary pilot copy; live Flash reviewer image smoke under Git-ignored `projects/vision-smoke/`.
- Updated: [current state](current.md), [implementation handoff](workflow/implementation-handoff.md), and [root instructions](../AGENTS.md).
- Summary: Added passing regressions for working and broken mobile interactions and nested generic-adapter JSON output. Confirmed four real cached tasks reload without model calls or original-checkpoint mutation. Observed a successful native `view_file` event and correct image reading by Flash; recorded the AbsolutePath event shape for future production image-evidence enforcement. Pilot remains paused; no website-level visual approval, upload, or outreach sending occurred.

## [2026-11-01] docs | Fix next-day cache reuse and restart the fictional pilot

- Sources: User restart instruction; next-day resume regression test; live pilot state and worker traces.
- Updated: [current state](current.md), [implementation handoff](workflow/implementation-handoff.md), [root instructions](../AGENTS.md), engine date handling, and regression tests.
- Summary: Preserved original request dates for completed research without rewriting source-access dates. All 30 automated tests pass. Resumed the existing pilot with cached business/competitor/plan results; started Argon build attempt 2 under runner PID 17548. External-action approval boundaries remain unchanged.

## [2026-11-01] docs | Enforce visual evidence and exercise live correction workflow

- Sources: Live Argon build/reviewer task artifacts; successful image-view events and PNG hashes; 38-test regression run; current source and native role registrations.
- Updated: [current state](current.md), [implementation handoff](workflow/implementation-handoff.md), [README](../README.md), and [root instructions](../AGENTS.md).
- Summary: Initial Argon static build and browser QA completed. The independent reviewer opened all five screenshots and identified actionable visual issues. Added mandatory image receipts/hash checks, compact readable-copy/source-reference handoffs to resolve review/revision prompt-budget failures, fail-closed blocked inspection handling, a canonical/native primary-only orchestrator persona, and case-sensitive SiteGround/Windows filename safeguards. A correction run is active with a project-local 600-second timeout; no final live pipeline pass is claimed in this entry.

## [2026-11-01] docs | Complete and verify the first live local demo

- Sources: Final real-model `review-2`, native image-view receipts, cycle-2 Chromium audit, targeted live checks, ZIP integrity verification, no-inference rerun, temporary-copy tamper tests, and 39 passing automated tests.
- Updated: [current state](current.md), [implementation handoff](workflow/implementation-handoff.md), [workflow overview](workflow/overview.md), [research follow-up](research/antigravity-feasibility.md), [README](../README.md), and [root instructions](../AGENTS.md).
- Summary: The fictional pilot reached `awaiting_approval` after two correction cycles. Final reviewer inspected all five screenshots and reported no issues; static/browser gates passed. Four-file ZIP contents/CRC/hashes matched the reviewed source. Completed rerun retained 12 calls with no inference; real copied-site/package tampering was rejected. Recorded 423,411 reported successful-task tokens with incomplete overall accounting, remaining source-corroboration/negative-claim concerns, and unsent outreach placeholders/internal note. All pilot processes exited, no lock remains, and nothing was uploaded, published, or sent.

## [2026-11-01] docs | Record requested working-MVP commit scope

- Source: User request to explain the workflow and commit the work.
- Updated: [current state](current.md) and [implementation handoff](workflow/implementation-handoff.md).
- Summary: Defined the local commit as the completed, tested Antigravity MVP, including source, role instructions/registrations, examples/configuration, tests, and documentation. Generated client projects, traces, ZIPs, caches, credentials, and secrets remain excluded. Remaining production-hardening and native Pi/Codex work is explicitly outside the completed milestone; no push or deployment was requested.

## [2026-11-01] docs | Prioritize native parent-controlled subagents

- Source: User clarification that independent CLI workers are not native subagents, followed by an explicit request to make native subagents the next step.
- Created: [native subagent migration plan](workflow/native-subagents.md).
- Updated: [current state](current.md), [implementation handoff](workflow/implementation-handoff.md), [workflow overview](workflow/overview.md), [index](index.md), [README](../README.md), and [root instructions](../AGENTS.md).
- Summary: Distinguished the tested Python/process-worker MVP from the intended native parent-child architecture. Prioritized verified native invocation/concurrency/model/lifecycle support, parent-role migration, deterministic helper reuse, and native smoke/full-pilot acceptance tests. Preserved the existing runner as a labeled baseline and unchanged approval boundaries. This task changes documentation only; native delegation and runtime instructions/registrations were not implemented or modified.

## [2026-11-01] docs | Package current workflow for safe project installation

- Sources: User request for reusable GitHub installation and business-specific operation; explicit choice to keep the existing repository private and defer native subagents; 59-test run and isolated wheel/sdist integration checks.
- Created: [installation quickstart](../INSTALL.md), [distribution design/evidence](workflow/distribution.md), installed agent-guide template, asset build hook/manifest, ownership-aware installer/setup, business-scaffold CLI, installation tests, installed-wheel integration script, and CI configuration.
- Updated: [README](../README.md), [current state](current.md), [handoff](workflow/implementation-handoff.md), [overview](workflow/overview.md), [native roadmap priority](workflow/native-subagents.md), [index](index.md), root/coordinator instructions, package metadata/resources, and worker workspace selection.
- Summary: Version 0.2.0 bundles all runtime roles/examples/defaults for wheel/sdist installation outside the source checkout. Setup installs scoped instructions and Chromium without model calls or global permission changes. Host instructions/configuration are preserved and conflicts fail safely. Verified 58 tests passing with one Windows-privilege symlink skip, plus a fresh-venv/fresh-host real-browser delivery flow with test-double model/visual responses. Private origin publication and pinned-tag installation verification follow; client artifacts and credentials remain excluded.

## [2026-11-01] docs | Verify private GitHub installation and correct CI portability

- Sources: Published private v0.2.0 release/tag; successful authenticated GitHub VCS installation and fresh-host isolated browser/package test; GitHub Actions failure logs for Linux/Windows on Python 3.11/3.13.
- Updated: [current state](current.md), [distribution status](workflow/distribution.md), [handoff](workflow/implementation-handoff.md), install pins, patch-version metadata, CI triggers, and test fixtures.
- Summary: Remote installation passed, but CI exposed tests that assumed a local agy executable and unexpanded Windows temporary paths. Corrected those test fixtures without changing workflow execution behavior. Prepared 0.2.1 rather than moving the existing tag; CI ignores documentation-only pushes/tag duplication and cancels superseded same-ref runs. Repository remains private; package/browser tests use model doubles and no paid inference.
