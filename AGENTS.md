## Git Rules

* Run `git status` before starting work.
* Do not overwrite or remove existing user changes.
* Only commit when the current task is fully complete and working.
* Before committing, review `git diff`.
* Do not include unrelated changes in the commit.
* Never commit secrets, `.env` files, temporary files, or debug files.
* Use a short, clear commit message that describes what was completed.
* If the task is incomplete or broken, do not commit.

### Commit example

```bash
git status
git diff
git add <relevant-files>
git commit -m "Add responsive mobile navigation"
```

---

# Project Workflow and Role Ownership

- Read `docs/workflow/overview.md` for requirements and approval boundaries. Before continuing implementation, read `docs/workflow/implementation-handoff.md` for exact progress, live test findings, paused pilot state, known gaps, and next commands. `docs/research/antigravity-feasibility.md` is the earlier capability investigation.
- Current user priority: distribute/install the working process-worker workflow from the public GitHub repository; read `INSTALL.md` and `docs/workflow/distribution.md`. Native subagents are explicitly deferred until afterward (`docs/workflow/native-subagents.md`). Do not describe independent `agy` processes as native delegation; native migration remains unimplemented.
- Public repository security: follow `SECURITY.md`. Never commit client runs, traces, credentials, or generated site ZIPs; preserve the read-only CI/token and explicit external-action approval boundaries. No GitHub credentials are needed for public HTTPS installs; model authentication is separate.
- The orchestrator is the user-facing coordinator and sole maintainer of shared wiki documentation and workflow state. The wiki-maintenance rules below apply to it.
- Delegated workers write only assigned task artifacts and report durable findings to the orchestrator; they must not edit shared wiki/state unless the user explicitly changes this ownership policy.
- Version 1 stops after local research, planning, building, testing, deployment packaging, and outreach drafting. Any preview upload, public deployment, email sending, purchase, or expanded credential use requires explicit user approval.
- Do not assume nested role `AGENTS.md` files activate automatically. Antigravity root-started sessions require explicit role loading or native agent registrations.
- The first full live Antigravity local demo passed on 2026-11-01 after two correction cycles, with its original 39 passing automated tests. Distribution adds installer/package tests; see current documentation for the latest suite count. Its state is `awaiting_approval`; nothing was uploaded or sent. Inspect actual state/processes before launching work. Do not equate a fictional pilot or test-double success with arbitrary-client production readiness, complete source corroboration, or tested native Pi/Codex support.

---

# LLM Wiki Rules

## What this wiki is

This project uses `docs/` as a persistent LLM-maintained knowledge base. The wiki preserves useful project knowledge so future humans and agents do not have to rediscover it from chat history, raw files, implementation details, tests, or scattered notes.

The human provides direction, decisions, and source material. Agents keep the documentation accurate, organized, linked, and current.

`AGENTS.md` is the primary operational contract. Read `docs/raw/karpathy-llm-wiki.md` when clarification about the underlying LLM wiki model is needed.

## Wiki invariants

1. Raw sources are never modified unless the user explicitly asks.
2. Every documentation folder must be discoverable from `docs/index.md`.
3. Important durable project knowledge should not exist only in conversation history.
4. `docs/current.md` represents the present state, not historical states.
5. `docs/log.md` is append-only.
6. Related documentation should be linked when the relationship is useful.
7. Decide whether new knowledge belongs in an existing page or needs a dedicated file; create a new file when the topic is distinct or likely to expand.
8. Distinguish established information, uncertainty, disagreement, and inference.
9. Use as many documentation files as needed for clarity, while limiting edits to the knowledge actually affected.

## Start here

Before working with documentation:

1. Read `docs/index.md` first to understand the documentation structure.
2. Read `docs/current.md` for current status, focus, issues, and next steps.
3. Use `docs/log.md` only when you need the history of documentation changes.
4. Read only the additional documentation relevant to your task.

## How knowledge enters the wiki

Durable knowledge can enter the wiki through two main paths:

1. **Source ingestion** — raw files placed in `docs/raw/`, such as client briefs, articles, transcripts, research, external documentation, imported notes, and captured reference material.
2. **Project learning** — user decisions, requirements, preferences, implementation discoveries, debugging conclusions, test results, architecture decisions, workflow changes, research conclusions, and other important knowledge learned during normal agent work.

Important project knowledge does not need to originate from a raw source before it can be documented. If information learned during conversation, implementation, research, testing, or debugging will be useful to future agents, preserve it in the maintained wiki instead of leaving it only in chat history.

## When to update documentation

Update the wiki whenever new information changes the project knowledge base.

Examples include:

- new requirements, decisions, constraints, or preferences
- new architecture, workflow, or setup knowledge
- changed project status, focus, known issues, or next steps
- new source material added under `docs/raw/`
- important conclusions from research, debugging, testing, or implementation
- corrections to outdated or misleading documentation

Do not let important knowledge live only in the conversation. If future agents should know it, document it.

## How to create or update documentation

- Put documentation in the most relevant subfolder under `docs/`.
- If no appropriate folder exists, create a clear lowercase kebab-case folder and add it to `docs/index.md`.
- Do not create loose Markdown files directly under `docs/` except `index.md`, `current.md`, and `log.md`.
- Determine whether updated information belongs in an existing page or needs a complete file of its own.
- Create a new file when the topic is distinct, needs a focused explanation, or is likely to be expanded later.
- Update an existing page when the information naturally belongs there, and avoid true duplicates.
- Use clear lowercase kebab-case filenames.
- Keep documentation concise, factual, and useful for future agents.
- Preserve uncertainty, disagreement, contradictions, and open questions when they matter.
- Distinguish established project facts, user decisions, implementation evidence, testing/debugging results, external research, and agent inference.
- Never fabricate citations, sources, quotes, dates, or relationships.

## Capture project learning

When important reusable knowledge emerges during normal project work:

1. Determine whether future humans or agents would benefit from knowing it.
2. Find the most relevant existing documentation page.
3. Determine whether the new information belongs on that page or deserves a complete file of its own.
4. Create a new page when the topic is distinct, needs room for a complete explanation, or is likely to be expanded later.
5. Update an existing page when the information naturally belongs there, and avoid true duplicates.
6. Preserve uncertainty and the basis for important conclusions.
7. Add clear cross-links between the new or updated documentation and related pages.
8. Update `docs/index.md` only when navigation or folder structure changes.
9. Update `docs/current.md` only when present project state changes.
10. Append to `docs/log.md` when documentation is materially created or updated.

This workflow covers knowledge arising from conversation, implementation, testing, debugging, research, and explicit user decisions.

## Linking documentation

Documentation should form a clear connected knowledge graph, not a collection of isolated files.

- Link related documentation pages to each other with relative Markdown links.
- Link documentation back to relevant source files in `docs/raw/` when applicable.
- When creating a new page, add useful outbound links and add inbound links from existing relevant pages.
- When updating a page, check whether related pages need links or material updates so the relationship remains clear.
- Prefer explicit, descriptive connections that explain why pages are related.
- Keep links relative so the wiki remains portable.

## Change locality

Wiki maintenance should favor coherent, well-connected mutation: create or update every file needed to represent the knowledge clearly, but avoid unrelated churn.

- Use as many files as needed for clear topic boundaries and future growth.
- Change only the coherent set of files necessary to keep the knowledge base accurate and connected.
- Do not rewrite unrelated pages merely to improve wording.
- Do not perform broad reorganizations unless the current structure is causing a real navigation, duplication, or correctness problem.
- Update related pages only when the new information materially affects them.
- Prefer small, coherent documentation diffs over unnecessary repository-wide cleanup.
- Adding a new page may require the page, related links, and a log entry; it does not automatically require changing `docs/current.md`.
- Updating a factual statement does not automatically require reorganizing its entire folder.
- `docs/index.md` changes only when navigation needs to change.
- Change locality limits unrelated edits; it does not discourage creating a well-justified new documentation file.

## Required maintenance

When documentation changes:

- Update `docs/index.md` if folders are added, renamed, removed, or their purpose changes.
- Update `docs/current.md` if status, focus, issues, next steps, or recent important context changes.
- Append to `docs/log.md` only when documentation is created or materially updated.
- Ensure documentation remains placed in folders and linked to related pages.

## Raw sources

`docs/raw/` contains immutable external or captured source material used as evidence or reference for the maintained wiki.

Appropriate raw sources include client briefs, articles, research papers, meeting transcripts, imported notes, external documentation, and captured reference material.

Normal synthesized project knowledge should not be stored in `docs/raw/`. Put these in maintained documentation instead:

- “The project will use Astro.”
- “The client prefers a premium visual direction.”
- “The navbar breaks below 768px.”
- “The current deployment target is Netlify.”

Treat raw sources as immutable. Read them, cite them, and link to them, but do not rewrite, rename, or delete them unless the user explicitly asks.

## Current state

`docs/current.md` is a concise, continuously rewritten snapshot of the project's present state.

It is not a project history, session transcript, append-only file, or record of every completed task. Rewrite outdated information instead of accumulating historical states. Historical information belongs in maintained documentation, `docs/log.md`, or Git history.

Keep `docs/current.md` focused on current status, active focus, completed high-level milestones, current work in progress, known issues, next steps, and recent context that a new agent needs immediately.

## Log format

`docs/log.md` is an append-only chronological log of meaningful wiki mutations. It records changes to the documentation system itself.

It is not an agent session log, development activity log, Git history, chat transcript, list of every command, or record of every query.

Never rewrite or reorder existing log entries. Append an entry only when documentation is created or materially updated. Use:

```markdown
## [YYYY-MM-DD] docs | Short description

- Source: [relative path](docs/raw/example.md)
- Updated: [page](docs/concepts/example.md)
- Summary: Brief description of what changed.
```
