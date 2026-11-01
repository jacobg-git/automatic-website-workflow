# Implementation handoff

## Read first

The user authorized autonomous local implementation with minimal questions. Earlier time-boxed pauses are over; work has resumed. **Never launch a duplicate runner.** Start with [current state](../current.md), the actual project `state.json`/lock/processes, then this page.

**Latest user priority: [installable distribution with public repository access](distribution.md) of the current process-worker version first; native subagents later.** Version 0.2.0 bundles runtime assets and provides safe project setup/business-specific commands; 0.2.1 corrects CI fixture portability and is the published, verified installation pin. All four remote CI jobs and authenticated installation passed before the repository's public-access request. Public exposure requires the audit/settings described in `SECURITY.md`; GitHub installation credentials are no longer required once public. Read [INSTALL.md](../../INSTALL.md) for usage. Native parent-controlled orchestration remains planned, not implemented; neither packaging nor the old pilot proves native delegation.

Approval boundaries remain local-only: no uploads, public deployment, email sending, purchases, DNS changes, or expanded credential use without separate explicit approval.

## Latest pilot snapshot — 2026-11-01

Project: `projects/live-demo-001/` (Git-ignored, local machine only). It represents a clearly fictional bicycle workshop, not a real business.

Completed real tasks:

- `business`, `competitor-1`, `competitor-2`: concurrent Flash Low research.
- `plan`: Argon Medium planning.
- `build`: Argon High, attempt 2. Original attempt 1 was intentionally interrupted at a user-requested handoff. The successful build generated `index.html`, `styles.css`, `script.js`, and `assets/workshop-emblem.svg` (~70 KB).
- Static checks and real Chromium QA passed at 390/768/1440px; mobile navigation and service-tab visibility checks passed.
- `review-0`: Argon Medium genuinely opened all five screenshots. Successful tool-event receipts and PNG hashes are in `state.tasks.review-0.usage.viewed_images`. It requested fixes for selected-tab text contrast, cramped mobile specification labels, a keyboard-focused skip-link overlap, and minor desktop header spacing.

**Terminal result:** `awaiting_approval`. Both `fix-1` and `fix-2` completed. `review-1` caught a skip-link focus/layout-shift regression that prevented a menu click; `fix-2` corrected it. Final `review-2` genuinely opened all five screenshots and returned **pass with no issues**. The static ZIP and unsent outreach draft were created. Runner and workers exited; the project lock is released.

Final counters: **12 started pilot calls, 423,411 reported completed-task tokens**. Interrupted generations and separate smoke tests consumed additional/unknown quota. Do not reset these counters.

Deliverables: `site/`, `delivery/siteground-static.zip`, `delivery/SITEGROUND.md`, `qa/cycle-2.json`, five final images under `qa/cycle-2/`, `qa/targeted-regressions.json`, `outreach/draft.md`, and `docs/handoff.md` within the project.

The ZIP's CRC, four-file manifest, root `index.html`, and content hashes were verified. Re-running the completed project retained 12 calls (zero inference). Temporary-copy tests rejected changed site/ZIP files without overwriting edits or calling models. Independent targeted browser checks passed for all tab label states (sampled contrast minimum 7.57:1), mobile table stacking, no focus-induced layout shift/disclosure-text overlap, keyboard-to-mouse menu click, Escape/focus return, and tab arrow/End-key navigation.

The outreach artifact is deliberately unsent. It retains `[APPROVED_PREVIEW_URL]`, `[SENDER_NAME]`, and an internal sender note; clean up the note and replace placeholders only after appropriate approval.

Two prompt-size blockers were fixed:

1. Full site code in reviewer input exceeded 70K characters. Review now receives complete readable copy, screenshots/hashes, audits, provenance, and optional source-file paths.
2. Full code repeated in revision input also exceeded the budget. Revision now references the current source files and manifest; the builder reads them through `view_file` and still returns a complete static file set.

For lengthy full-code revisions, `projects/live-demo-001/run-config.json` sets an explicit **600-second task timeout**. Model routing, call/token budgets, and QA requirements are unchanged. The repository default remains 300 seconds.

## Continue safely

Inspect first:

```bash
python -m website_workflow status --project projects/live-demo-001
```

The completed pilot has no active runner. The following command now verifies cached artifacts without new model calls. If a future runner is active, do not launch it concurrently:

```bash
python -m website_workflow --config projects/live-demo-001/run-config.json run --project projects/live-demo-001
```

Task traces: `tasks/<task>/attempt-<n>/{prompt,schema,stdout,stderr}.*`. Validated task JSON is `tasks/<task>/result.json`. QA reports/screenshots are under `qa/`; progress is `docs/progress.md` within the project. Model calls use incremental trace persistence.

A leftover `.workflow.lock` must not be removed until the runner and all descendants are confirmed stopped. There is not yet a graceful pause command. Do not silently reset exhausted attempts/budgets. Two attempts per task are enforced across resumes.

If the project is absent in a fresh clone:

```bash
python -m website_workflow init --project projects/my-demo --demo
python -m website_workflow run --project projects/my-demo
```

This calls real, quota-consuming models.

## Implemented architecture

- `website_workflow/cli.py`: setup, install, new-business, validate-intake, init, doctor, run, status, qa, serve, sync-agents.
- `installation.py`: ownership-aware, non-destructive host installation and Chromium bootstrap.
- `build_assets.py` / `MANIFEST.in`: bundle canonical roles/examples/defaults into wheels and sdists; package `templates/PROJECT_GUIDE.md` supplies installed operating instructions.
- `config.py` / adapter workspace selection: locate bundled assets and launch workers from their actual installed host, not the development checkout.
- `engine.py`: deterministic stage scheduling, parallel research, evidence/planning artifacts, cache/retries, build/QA corrections, packaging/outreach handoff.
- `adapters.py`: Antigravity exact-model stdin/NDJSON sessions, session-only permissions, tool-event monitoring, image receipts, time/output/process controls, native registration generation, generic command adapter.
- `contracts.py`: JSON schemas, supported-vocabulary validator, research/source-reference matching.
- `quality.py`: safe paths/static checks, readable-copy extraction, localhost server, real Chromium tests/screenshots/interactions, remote-request blocking.
- `storage.py`: hashes, atomic JSON writes, exclusive project lock.
- `config.py`: validated intake/config and repository resource paths.
- `roles/*/AGENTS.md`: portable canonical worker/coordinator instructions.
- `.agents/agents/website-*.md`: generated registrations; run `sync-agents` after editing roles.
- `workflow.config.json`: model routing and limits; `examples/`: intake template and fictional demo.

The conversational coding agent is the user-facing coordinator, but **current scheduling is Python-led**. Parallel workers are independent `agy` CLI processes/conversations with exact model slugs; they are not native children launched through `invoke_subagent`. Custom/native role registration alone does not establish parent-child delegation. The next milestone transfers orchestration to the parent agent while retaining deterministic Python helpers.

Interactive Antigravity entry point:

```bash
agy --agent website-orchestrator --model gemini-4-argon-medium --sandbox --settings '{"toolPermission":"request-review"}'
```

The existing coordinator persona is primary-only and currently instructs the agent to use the Python scheduler; its registration does not expose `invoke_subagent`. It has not yet been migrated to the target native-parent role. Registration/instruction synchronization tests do not prove native orchestration.

## Proven runtime details

- Native role discovery and exact Flash/Argon selection are verified live.
- **Enable `finish` in role tool lists.** Without it, the initial structured-output smoke repeated its answer and attempted unrelated task management. Enabling it fixed the run.
- Prompts go through one stdin NDJSON turn, then stdin closes. This avoids Windows' ~32K command-line limit.
- `--settings` applies session-only `toolPermission: request-review` and deny rules for commands, writes, browser actuation, and MCP. No global permissions are edited; no `--dangerously-skip-permissions` is used.
- A harmless shell-denial probe actually hit a deny rule while the terminal status was still SUCCESS. Exit code/success prose is not enough.
- `init.tools` advertises the full registry even for a restricted custom role. Actual tool-call monitoring is detection, not a pre-execution security boundary. Native role tool lists and permission rules remain necessary.
- Completed research retains its original request date across midnight. Fresh research uses the current date; cached access dates are not rewritten. Legacy records recover their date from the integrity-checked original prompt.
- Semantic task fingerprints ignore dictionary arrival order and safely migrate legacy fingerprints only after verifying original prompt hashes.

## Enforced visual evidence contract

The native adapter derives `usage.viewed_images` from successful **DONE `view_file` events**, reading `tool_info.parameters.AbsolutePath`. Paths are resolved/normalized and PNG bytes are hashed. Model prose cannot create these receipts.

The engine requires:

1. Every expected screenshot is reported inspected.
2. Every expected screenshot hash has a matching adapter receipt.
3. Screenshot bytes still match after review.

Hashes are included in the review task input/cache identity. Missing evidence blocks release; the engine does not waste builder cycles trying to fix unavailable inspection. Successful native review of all five real pilot screenshots has verified this path.

A separate earlier Flash smoke read a test image, identified `VISUAL CHECKPOINT 731` and a forest-green panel, and produced a successful image-view event. Its local evidence lives under `projects/vision-smoke/`.

## Validation

The original 39-test workflow suite passed with real Chromium. Distribution expands the current suite to **59 tests: 58 passing and one privileged real-symlink test skipped on Windows**, with a separate simulated link-guard case passing. Isolated wheel/sdist installation and a fresh-host real-browser pipeline with test-double models also passed; see [distribution evidence](distribution.md). Coverage includes a complete engine run with real Chromium and test-double models, interaction success/failure, network blocking, exact lowercase SiteGround entry filename, non-portable Windows paths, missing/wrong image receipts, large-source compact handoffs, cache migration, next-day resume, bounded retries/budgets, lock behavior, and package/site tampering.

```bash
python -m unittest discover -s tests -v
python -m compileall -q website_workflow
python -m website_workflow doctor
git diff --check
```

Full orchestration tests inject clearly labeled model/browser doubles. They establish control-flow behavior, not genuine visual quality. Native image receipts and the real pilot are separate live evidence.

Generated projects, prompts, screenshots, model traces, caches, and package metadata are Git-ignored. Preserve local backups if needed. The user requested a local Git commit of the completed, tested Antigravity MVP on 2026-11-01. Its commit scope is source, canonical/generated role instructions, configuration/examples, tests, and documentation—not the unfinished production-hardening backlog or generated client data. Existing user setup files are preserved.

## Priority remaining work

### Distribution completed; native migration remains deferred

The current version is reusable from GitHub `v0.2.1`; the user subsequently requested public access after security checks. The corrected four-job CI matrix and authenticated fresh-environment GitHub installation passed; see [distribution evidence](distribution.md). Agents should use [INSTALL.md](../../INSTALL.md) for new projects/businesses. When the user returns to native work, follow [the migration plan](native-subagents.md) before further scheduler features or broader runtime wrappers. Verify native tools/model selection, update canonical/generated parent instructions and permissions, expose deterministic helpers, record native child IDs/results, then run concurrent child smoke tests and a complete parent-led fictional pilot. Preserve the existing working process mode and its evidence as a labeled baseline, not as native acceptance evidence.

### Existing process-based live milestone completed

The first full real-model/local-browser pipeline, two correction cycles, final image receipts, ZIP verification, unsent outreach artifact, no-inference completed rerun, and real-artifact tamper checks all passed. `awaiting_approval` is a local handoff, never approval to upload/send.

The next implementation step is native migration above; the research/reliability issues below remain required before a real-business pilot. Existing generated projects remain Git-ignored; preserve them locally.

### Reliability and research hardening

- Source references are validated, but the engine does not independently fetch/corroborate every quote or resolve conflicting facts. Research-confirmed claims are source-backed, not human-approved. Competitor facts remain separate. **Observed issue:** the fictional demo researcher classified 'no matching web results' as proof of nonexistence/registration status. That inference is not valid evidence for real businesses; add a corroboration/negative-claim gate before a real-client pilot.
- Stronger source-access-date validation and inaccessible Maps/review handling are needed; no Maps API integration exists.
- Add graceful pause/cancel, process-tree cleanup, and transactional site application. Multi-file site writes can fail closed on a manifest mismatch after a crash; do not overwrite mismatches blindly.
- Token cap is pre-launch/post-response accounting, **not** a provider billing hard cap. In-flight/failed/unreported calls can exceed it.
- Current QA is a Chromium baseline, not full accessibility/contrast/Lighthouse/performance scoring/cross-browser coverage. Screenshots currently include keyboard-focused baseline state; avoid confusing QA-induced focus with default-load layout.
- Consider viewport/section image crops for long pages; full-page mobile screenshots can be difficult to inspect after image downscaling.
- Test complete interactive coordinator operation. Wheel/sdist resource handling and installed-host discovery are now covered by the distribution validation; retain those checks during native migration.

### Portability

The generic `command` adapter accepts an argv array without a shell, sends prompts on stdin, and expects JSON stdout. Supported substitutions: `{model}`, `{role}`, `{prompt_file}`, `{schema_file}`, `{workdir}`. Optional dotted `result_key` unwraps an envelope; JSON text in that field is parsed once. Diagnostics go to stderr.

**Pi/Codex-specific wrappers remain unimplemented/untested.** Read their current docs before implementing. The current generic adapter does not produce trusted image-tool receipts, so its visual release stays blocked; a trusted wrapper/event adapter must implement this contract rather than forwarding model self-reports. Runtime-specific permissions, image support, and external-action restrictions are the wrapper's responsibility.

The `fixture` adapter is development-only, not evidence of real model capability.

## Delivery boundary

The ZIP and `SITEGROUND.md` are manual handoff artifacts, not a hosting integration test. Drafts retain noindex. No contact backend, analytics, credentials, sending connector, or deployment connector is included. Resolve factual/licensing/privacy/accessibility uncertainties with the client before any approved publication.
