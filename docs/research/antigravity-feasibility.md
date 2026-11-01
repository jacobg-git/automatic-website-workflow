# Antigravity feasibility

Research date: **2026-10-31** (environment clock). Scope of this initial investigation: official public documentation plus non-generating, local CLI inspection. No model inference, website build, worker launch, browser session, upload, email, or permission configuration was performed during that investigation.

**Implementation follow-up (2026-11-01):** The first full live fictional Antigravity pilot passed parallel research, Argon planning/building, two browser/visual correction cycles, image-tool receipt checks, ZIP packaging, unsent outreach, and a no-inference completed rerun. There are 39 passing automated tests. See the [implementation handoff](../workflow/implementation-handoff.md) for current evidence and remaining limits; the original pre-implementation investigation below remains historical context.

Related: [workflow requirements](../workflow/overview.md), [local CLI evidence](../raw/antigravity-cli-inspection-2026-10-31.md).

## Verdict

**Yes: Antigravity CLI is a credible first runtime for this workflow.** Official documentation explicitly supports parallel custom subagents, different model tiers, clean worker contexts, browser testing, scoped permissions, and structured headless execution. The installed `agy models` command lists Gemini 4 Argon and Gemini 3.8 Flash.

This establishes capability-level feasibility, not a tested autonomous website pipeline. Browser activation, exact worker model mapping, permission enforcement, and task completion still require controlled smoke tests.

## Evidence matrix

| Requirement | Evidence | Conclusion |
| --- | --- | --- |
| Strong Argon builder | Local `agy models` lists `gemini-4-argon-high`, `-medium`, `-low`; official model/headless docs name Argon | Available in the local model catalog; no inference tested |
| Cheaper research models | Local catalog lists `gemini-3.8-flash-low`, `-medium`, `-high`; custom agent frontmatter supports `model: flash` versus `pro`/`inherit` | Tier routing documented; actual cost/quota benefit and tier-to-model mapping need validation |
| Parallel specialist workers | Custom subagent docs describe concurrent `invoke_subagent`, clean context windows, asynchronous returns | Supported by design; not exercised locally |
| Orchestrator and worker personas | Native Markdown agent definitions support system prompts, primary/subagent flags, tool lists, and command policies | Supported; repository definitions not created yet |
| Portable Markdown instructions | `AGENTS.md`/`GEMINI.md` discovery is documented | Supported with important directory-scope limits below |
| Browser visual/functional QA | `/browser` docs describe Chrome DevTools, screenshots, interactions, console/network inspection, emulation, and Lighthouse | Supported but on-demand activation affects unattended operation |
| Scripted stage runner | Local help and headless docs expose `--print`, model selection, JSON/NDJSON, schema output, resume IDs, and timeout | Appropriate for a portable adapter |
| Durable docs/state and approval gates | File tools and permission rules exist | Project must implement state/contracts and enforce business-level approvals; not automatic platform features |

## 1. Native workers, not just nested instruction files

Official [custom subagent documentation](https://antigravity.google/docs/subagents/) says:

> A parent agent can invoke multiple subagents concurrently.

It documents independent context windows, asynchronous results, peer/parent messaging, and workspace options including inherited workspaces and isolated Git worktrees. A worker does not inherit the parent's conversation history: every task must explicitly identify inputs, output path, scope, and acceptance criteria.

Native repository agent discovery locations:

```text
.agents/agents/<name>.md
.agents/agents/<name>/agent.md
```

Personal definitions live under `~/.gemini/config/agents/`. Frontmatter includes `name`, `description`, `tools`, `mainAgent`, `subagent`, `model`, and `commandExecutionPolicy`. The docs list worker model tiers as `inherit`, `flash`, and `pro`; **they do not establish that arbitrary exact CLI model slugs are accepted in worker frontmatter**.

Therefore, pin exact models for CLI sessions, but verify native worker tier resolution before relying on it. If exact per-stage selection cannot be guaranteed natively, launch separate headless worker processes with explicit `--model` values and bounded external concurrency.

Tool lists must use actual available tool identifiers. The documentation warns that misspelled/unmapped tools can hang workers. Inspect the runtime's advertised tool list before producing role configurations. The built-in `research` worker is described as codebase research, not an automatically configured business-web researcher.

## 2. Critical discovery limitation

Official [customization discovery](https://antigravity.google/docs/customization-discovery/) and [rules](https://antigravity.google/docs/rules/) explain that Antigravity reads workspace and ancestor instructions up to the repository root, **not descendant instructions merely because the agent edits files there**:

> It doesn't search subfolders below the workspace folder.

For a root-started session, `roles/researchers/AGENTS.md` is not automatically activated when that directory is read.

Recommended arrangement:

```text
AGENTS.md                              # shared constraints and orchestrator entry
roles/researchers/AGENTS.md             # portable canonical role instructions
roles/planner/AGENTS.md
roles/builder/AGENTS.md
roles/reviewer/AGENTS.md
roles/outreach/AGENTS.md
.agents/agents/business-researcher.md   # Antigravity registration/shim
.agents/agents/website-builder.md
adapters/antigravity/                   # explicit role loading and execution
```

Make the shim/task explicitly load its canonical role file, or generate native definitions from the portable source. Do not maintain two independent copies of role logic. Starting a CLI inside a role directory changes discovery but also changes the workspace; it is not a complete scheduling or isolation solution.

Antigravity-specific file include syntax exists for rule files, but should not be assumed portable to other runtimes or supported identically in agent definition bodies.

## 3. Model allocation

Locally observed exact identifiers:

- Builder candidate: `gemini-4-argon-high`.
- Planning/orchestration candidate: `gemini-4-argon-medium`, subject to pilot cost/quality results.
- Research/extraction candidate: `gemini-3.8-flash-low` or `gemini-3.8-flash-medium`.

These assignments are recommendations, not benchmark results. Low reasoning effort is not automatically the lowest total cost: retries, missed evidence, context size, quota weighting, and tool calls matter. Use concise handoffs and bounded worker scopes.

The official [model page](https://antigravity.google/docs/models/) lists plan-dependent access. A local catalog listing is not proof of remaining quota or a successful generation. No account plan, balance, or credentials were inspected.

## 4. Browser testing: supported, unattended loop not yet proven

The official [browser command documentation](https://antigravity.google/docs/commands/browser/) applies to the CLI and describes:

- Chrome controlled through an automatically started Chrome DevTools MCP server.
- Navigation, clicks, typing, and form interaction.
- Accessibility snapshots, screenshots, console and network inspection.
- Viewport/device/network emulation, performance traces, and Lighthouse.
- Session recordings saved as artifacts.

Important constraints:

1. The built-in browser worker is hidden from ordinary delegation and used only when `/browser` is invoked.
2. First connection requires accepting Chrome's remote-debugging prompt. Organization policy can disable browser access.
3. Browser JavaScript evaluation prompts by default; the permissions documentation also describes domain read/actuation controls. Their interaction must be tested rather than assuming all operations are unattended.
4. A top-level `/browser` task is documented; a builder spontaneously invoking browser QA in a later autonomous turn is **not established** by these sources.

Recommended pilot: use a stage runner to initiate explicit `/browser` tasks against localhost, collect results, then pass a bounded fix list to the builder. Headless slash-command expansion exists, but `/browser` activation and browser lifetime across headless stages still need testing.

If that path is unreliable, use a project-controlled Playwright harness for repeatable screenshots/interactions and send captured images to a vision-capable reviewer. This is a proposed fallback, not an implemented dependency.

## 5. Headless execution and completion contracts

Local `agy --help` confirms:

- `--print`, `--agent`, `--model`, `--effort`.
- `--output-format text|json|stream-json`.
- `--json-schema`, `--print-timeout`, `--sandbox`.
- Resume/continue flags and MCP management.

Official [headless documentation](https://antigravity.google/docs/cli/headless/) describes structured final responses, token/cache accounting, subagent event metadata, and an initial stream event containing available tools. These provide useful adapter integration points.

**Exit code zero is not enough:** headless permission requests can be soft-denied while the process still exits successfully. Validate required artifacts, explicit task status, QA reports, and stderr/tool failures. A successful response is not proof that a website was built or tested.

**Version/documentation drift observed:** local help says `--print-timeout` defaults to `0s` (wait until completion), whereas the headless page states five minutes. The permissions page mentions newer auto-mode versions not advertised by local help; the retrieved changelog begins at `1.2.17`, but a changelog is not a definitive installed-version query. Use explicit timeouts and only locally verified flags. Do not assume newer documented auto mode is available.

## 6. Permissions and local-only approvals

Official [permissions documentation](https://antigravity.google/docs/permissions/) covers file access, commands, URL reads, browser actuation, and MCP tools. Rule precedence is **Deny > Ask > Allow**. A blanket `ask: command(*)` defeats more specific command allows; do not copy example policies without checking precedence.

For this project:

- Allow only approved local build/test tools and project output locations.
- Bound public research access separately from local browser interaction.
- Provide no deployment/email credentials or sending tools in v1.
- Do not use `--dangerously-skip-permissions` to obtain unattended execution.
- Avoid broad shell/interpreter/network grants that bypass action-level restrictions.
- Test inheritance and denials in harmless scenarios before trusting a worker policy.

An instruction saying “do not publish” is useful but is not a security boundary. No-preview-upload/no-sending approvals must also be represented by tools, credentials, network policy, and runner behavior.

## 7. Recommended implementation sequence

1. Define portable task/result contracts, evidence format, approval gates, and one pilot intake.
2. Add one native orchestrator and one bounded researcher; verify discovery and actual selected model tier.
3. Launch two independent research tasks concurrently; verify output isolation and failure handling.
4. Test a tiny localhost page with explicit browser invocation, screenshots, one interaction, and console inspection. Complete initial Chrome setup with the user.
5. Confirm headless structured output, timeout behavior, permission soft-denial detection, and worker termination.
6. Build the full local-only pilot with checkpointed state and bounded correction loops.
7. Add other runtime adapters after the first complete pipeline passes.

Start with custom roles rather than `/boost` or `/teamwork`. Those are documented orchestration products, but introduce plan requirements and platform-specific behavior; they are unnecessary to prove this portable staged workflow.

## Sources and evidence limits

Official pages retrieved directly over HTTPS on the research date:

- [Custom subagents](https://antigravity.google/docs/subagents/)
- [Customization discovery](https://antigravity.google/docs/customization-discovery/)
- [Rules](https://antigravity.google/docs/rules/)
- [Choose a model](https://antigravity.google/docs/models/)
- [Browser command](https://antigravity.google/docs/commands/browser/)
- [Headless CLI](https://antigravity.google/docs/cli/headless/)
- [Permissions](https://antigravity.google/docs/permissions/)
- [Agents command](https://antigravity.google/docs/cli/commands/agents/)

Local observations: executable discovery, `agy --help`, `agy models`, `agy agents`, and `agy changelog`. `agy agents` returned no visible output in this non-interactive shell; this does not prove that no agents exist. Local help/model excerpts are preserved in the [inspection record](../raw/antigravity-cli-inspection-2026-10-31.md).

Not verified: actual model generations, exact native worker model resolution, authenticated source research, browser connectivity, concurrency behavior, SiteGround deployment, numerical costs, or end-to-end unattended operation.
