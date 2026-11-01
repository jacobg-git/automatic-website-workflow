# Documentation Index

Use this file as the first stop for navigating project documentation.

This index lists the folders under `docs/`, explains what belongs in each folder, and points agents toward the right place to read or write documentation. Important hub or overview pages may be listed as entry points, but this file should not become a complete catalog of every Markdown file.

## How to navigate

1. Start here before opening other documentation.
2. Read `current.md` for the current project state and next steps.
3. Choose the relevant folder from the folder list below.
4. Read only the files relevant to your task.
5. If documentation is missing, add it to the correct folder.
6. If no appropriate folder exists, create a clear lowercase kebab-case folder and add it to this index.

## Standard files

- [current.md](current.md) — Concise, continuously rewritten snapshot of the project's present state.
- [log.md](log.md) — Append-only chronological log of meaningful wiki mutations.

## Folders

- [raw/](raw/) — Immutable source material, including [Karpathy: LLM Wiki](raw/karpathy-llm-wiki.md) and [local Antigravity CLI inspection](raw/antigravity-cli-inspection-2026-10-31.md).
- [workflow/](workflow/) — Requirements, architecture, role ownership, approval boundaries, and implementation progress. Start with the [workflow overview](workflow/overview.md), [private installation/distribution](workflow/distribution.md), [native subagent roadmap](workflow/native-subagents.md), and [continuation handoff](workflow/implementation-handoff.md).
- [research/](research/) — Source-backed capability investigations and implementation caveats. Start with [Antigravity feasibility](research/antigravity-feasibility.md).

## Folder entry format

Use this format when adding documentation folders:

```markdown
## Architecture

[architecture/](architecture/) — Technical architecture and implementation decisions.

Key pages:
- [Overview](architecture/overview.md)
- [Deployment](architecture/deployment.md)
```

## Index rules

- Keep this index focused on folders and navigation.
- Add every documentation folder under `docs/` to the folder list.
- Give each folder a one-sentence description of what belongs there.
- Important hub or overview pages may be listed beneath their folder as key pages.
- Do not list every individual documentation page.
- Do not create loose Markdown files directly under `docs/` except `index.md`, `current.md`, and `log.md`.
