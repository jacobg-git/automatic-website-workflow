# Next milestone: native subagent orchestration

## Decision and priority

On 2026-11-01 the user clarified that independent `agy` worker processes are not the intended subagent architecture and requested **native subagents as the next implementation milestone**.

**Subsequent user decision:** first distribute the current process-worker workflow as an installable private GitHub package, then return to native subagents. See [distribution status](distribution.md) and [INSTALL.md](../../INSTALL.md). Once distribution is verified, this migration remains the next architecture milestone ahead of broader runtime wrappers or further scheduler expansion. Necessary safety/verification work stays part of migration acceptance, not something to bypass for speed.

**Status: planned, not implemented or tested.** The existing MVP remains a useful working baseline; its pilot and 39 tests do not establish native delegation.

## Current versus target

| Responsibility | Current implementation | Target architecture |
| --- | --- | --- |
| User conversation | Coding agent / registered coordinator persona | Native parent orchestrator agent |
| Launch workers | Python starts independent `agy` CLI processes | Parent invokes actual native children through `invoke_subagent` |
| Schedule and hand off | Python stage loop | Parent agent controls stage dependencies, bounded concurrency, and result synthesis |
| Parallel research | Concurrent independent CLI conversations | Concurrent native business/competitor children with observable parent-child relationships |
| Worker models | Exact CLI `--model` slugs | Verified native per-child model selection; do not assume tier-to-model mapping |
| Documentation | Conversational orchestrator / backend | Parent orchestrator owns shared docs/state; children return assigned results |
| Deterministic operations | Python engine and helpers | Reused Python validation, browser QA, hashing, artifact persistence, and packaging helpers |

Registering a custom agent or giving a subprocess a role prompt is **not** evidence of native delegation. Invoking the existing full Python `run` command from a parent persona still uses the old scheduler.

## Intended flow

```text
User ↔ native parent orchestrator
         ├─ business researcher ─┐
         ├─ competitor worker A ├─ concurrent native children
         └─ competitor worker B ┘
                    ↓
         Parent reconciles evidence / records decisions
                    ↓
         Native planning child → parent validates brief
                    ↓
         Native building child → deterministic artifact validation
                    ↓
         Python browser QA → native visual-review child
                    ↓
         Parent requests bounded builder fixes, then repeats QA
                    ↓
         Native outreach-draft child + Python ZIP packaging
                    ↓
         Parent presents local handoff and requests approval
```

The parent must remain the user's conversational contact. Children must not maintain the shared wiki or silently spawn uncontrolled additional workers.

## Implementation sequence

### 1. Verify the current native API and permissions

Read current official Antigravity subagent/custom-agent/model/tool documentation and inspect the installed runtime before implementation. The earlier [feasibility investigation](../research/antigravity-feasibility.md) is a starting point, not proof of current tool schemas.

Confirm:

- How `invoke_subagent` launches custom roles and how child results are returned.
- Whether multiple children genuinely run concurrently and how the parent waits, messages, cancels, or resumes them.
- Native child model configuration and the actual resolved model identifiers.
- Parent/child tool and permission inheritance, workspace isolation, and approval propagation.
- Where parent/child IDs, tool traces, token usage, and successful image-view evidence can be observed.

The current coordinator registration does **not** expose `invoke_subagent` and its instructions explicitly route scheduling through Python. Both must change deliberately; a documentation label alone is insufficient.

If required model routing or native functionality is unavailable, document the blocker and ask for a decision. Do not silently replace children with more CLI subprocesses and call that native delegation.

### 2. Add a native orchestration entry point

Update the canonical orchestrator role and generated registration to use verified native delegation. Keep existing worker role instructions/contracts where suitable, with bounded scopes and least-privilege tools. Regenerate registrations rather than editing generated copies independently.

The parent should provide explicit task IDs, input references, output contracts, relevant constraints, budgets, and completion conditions. Children do not inherit every useful fact from the parent automatically.

Keep the existing Python scheduler available as an explicitly labeled legacy/fallback execution mode during migration. Do not delete the working baseline or silently change the meaning of existing commands/checkpoints.

### 3. Separate deterministic helpers from scheduling

Expose suitable stage-level operations for the parent to call without launching another agent process:

- Validate intake, evidence/results, plans, file paths, and static builds.
- Persist task artifacts/checkpoints and render Markdown reports on the parent's behalf.
- Run localhost browser checks and capture screenshots.
- Verify successful native child image-view events against expected image hashes.
- Package the reviewed static output and generate the local handoff.

Reuse `contracts.py`, `quality.py`, and storage/hash logic where possible. Refactor engine-only operations as needed. Calling the entire Python stage loop would retain Python-led orchestration and would not satisfy this milestone.

### 4. Make native execution observable and resumable

Persist stage/task IDs, parent-child conversation IDs, resolved models, result hashes, errors, attempts, usage when available, and decisions. Distinguish legacy process-worker checkpoints from native ones; do not rewrite old test evidence as native evidence.

Verify child termination/cancellation and recoverable failures. Keep concurrency, retry, correction-loop, elapsed-time, and call/token limits bounded. Unknown usage must remain unknown, not zero. Missing evidence must block release rather than weakening gates.

### 5. Run native smoke tests, then a complete fictional pilot

Start with two small, concurrent research children. Observe their native parent-child relationships and model selection before spending quota on a whole website. Then exercise planning, building, deterministic browser testing, receipt-backed visual review, corrections, unsent outreach, and packaging through the parent-led flow.

Do not use a real business to prove new orchestration mechanics. Research corroboration/negative-claim problems must be addressed before a real-client pilot.

## Acceptance criteria

- The user speaks with a parent agent that actually invokes native children, rather than a Python scheduler that starts role-specific `agy` processes.
- At least two research children overlap in execution and have observable native child IDs linked to the parent.
- Research/economy and strong-build model routing is verified from actual child configuration/events, not merely requested in prose.
- All specialist stages can return validated structured results to the parent; shared wiki/state ownership remains with the parent and deterministic helpers.
- Browser QA, screenshot hashes, successful image-view receipts, static-only output checks, and bounded correction loops still gate delivery.
- A native fictional pilot reaches a local approval-ready handoff, with its execution mode clearly distinguished from the existing process-based pilot.
- Failure/cancellation, cache/restart behavior, and no unintended duplicate launches are tested.
- No preview upload, deployment, sending, purchasing, domain change, or expanded credential use occurs without separate explicit approval.
- Documentation and tests describe what actually executed; subprocess-worker success is never presented as native-subagent success.

## Deferred work

After the native Antigravity path is proven: stronger research corroboration, additional reliability hardening, broader QA, and native Pi/Codex integrations. Portable role instructions and artifact contracts should remain runtime-neutral; each runtime's actual native delegation requires its own adapter and verification.

Related: [current state](../current.md), [workflow overview](overview.md), [implementation handoff](implementation-handoff.md).
