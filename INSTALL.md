# Install and run this workflow in another project

**Agent-facing quickstart.** This is the packaged **process-worker** workflow. Native subagents are intentionally deferred. Any coding agent can operate the CLI; worker inference still uses Antigravity `agy`.

Private repository: `https://github.com/jacobg-git/automatic-website-workflow`.

## 1. Check prerequisites

- Python **3.11+** (and pip/venv).
- Git with permission to read this **private** GitHub repository. An authenticated browser/MCP session does not necessarily authenticate command-line Git. Use the owner's existing SSH/Git Credential Manager/GitHub CLI setup. If missing, ask the owner to authenticate; never request or embed a token/password in chat, URLs, project files, or logs.
- Installed Antigravity CLI with an authenticated model account and sufficient quota. The owner handles authentication. Runtime documentation: <https://antigravity.google/docs/cli/using/>.
- Network access for package dependencies and the Chromium download.

The repository supplies the workflow code, roles, defaults, examples, project installer, agent guide, and tests. Pip resolves the Python dependencies; `setup` downloads Chromium. It cannot distribute/authenticate a proprietary model account, install Python itself, or guarantee model access/quota. Linux may need approved OS libraries for Chromium.

## 2. Install into the target project's virtual environment

From the **target project**, not this source checkout:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install "local-website-workflow @ git+https://github.com/jacobg-git/automatic-website-workflow.git@v0.2.0"
.\.venv\Scripts\python.exe -m website_workflow setup --project .
.\.venv\Scripts\python.exe -m website_workflow doctor --project .
```

### macOS / Linux

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install "local-website-workflow @ git+https://github.com/jacobg-git/automatic-website-workflow.git@v0.2.0"
./.venv/bin/python -m website_workflow setup --project .
./.venv/bin/python -m website_workflow doctor --project .
```

No environment activation is required. Use the same environment's Python for subsequent commands. Do not reinstall into or overwrite an unrelated existing environment blindly.

If HTTPS Git is not configured but approved SSH access is, substitute `git+ssh://git@github.com/jacobg-git/automatic-website-workflow.git@v0.2.0` in the install requirement.

`doctor` makes no model calls and checks browser launch/resources/registrations/executable. It does **not** verify authentication, model entitlements, or quota: check `agy models` separately. Do not silently downgrade model selection.

If browser installation is blocked, resolve the reported network/platform dependency problem. Do not bypass required QA. On Linux, `python -m playwright install-deps chromium` may require privileged package-manager access; request approval before running it.

## 3. Read the installed guide

Read `.website-workflow/AGENT_GUIDE.md` and follow the host project's other instructions. Setup creates:

```text
AGENTS.md                             # appends one marked pointer; retains existing content
.gitignore                            # appends a marked private-business-data exclusion
.agents/agents/website-*.md            # project-local Antigravity role registrations
.website-workflow/
  installation.json                   # package version and managed-file ownership hashes
  AGENT_GUIDE.md                       # business-specific operating instructions
  workflow.config.json                # user-editable model routing/limits; 600s task timeout
  intake-template.json
  roles/<role>/AGENTS.md               # versioned instruction snapshots
  businesses/<slug>/                  # private runtime outputs; Git-ignored
```

Other agent files and README content are untouched. Reinstallation is idempotent. Edited managed files/unrelated name collisions cause a conflict instead of overwrite; changed configuration is preserved. Host instruction bytes outside the marked block are preserved, including BOM/CRLF. Review conflicts manually—there is deliberately no force-overwrite flag.

Preview without writes/downloads: `python -m website_workflow setup --project . --dry-run`.

Install instructions only, without downloading browsers: `python -m website_workflow install --project .`.

## 4. Run for a specific business

Use the environment's Python (abbreviated as `python` below):

```bash
python -m website_workflow new-business --project . --name "Business Name" --location "City, Region"
```

This creates an **incomplete, unverified** intake under `.website-workflow/businesses/business-name/`; it does not start inference. Optional `--slug` distinguishes similarly named businesses or locations.

Follow the installed guide to research the exact business and complete verified facts, source URLs, description, and a useful verified CTA. Check whether an official website already exists. Never set verification flags just to pass validation or invent missing details. Ask only when essential information cannot be established safely.

```bash
python -m website_workflow validate-intake --intake .website-workflow/businesses/business-name/intake.json
python -m website_workflow run --project .website-workflow/businesses/business-name
python -m website_workflow status --project .website-workflow/businesses/business-name
python -m website_workflow serve --project .website-workflow/businesses/business-name
```

The installed host configuration is discovered automatically. Model runs consume real quota. A completed run stops at `awaiting_approval` with a static ZIP and unsent email draft. There are no upload/publish/send commands. Business details still need responsible source corroboration; structural intake validation is not proof of truth.

## Suggested user instruction to an agent

> Install the current workflow from the private GitHub repository `jacobg-git/automatic-website-workflow`, following `INSTALL.md`, into this project without replacing its existing instructions. Use the pinned release. Then read the installed guide and run it for **BUSINESS NAME in LOCATION**. Verify its identity, existing web presence, facts, and CTA first; ask only for essential missing information. Stop before any upload, publication, or sending. This is the current Python-managed worker version, not native subagents.

The installing agent needs access to the private repository and an already authenticated `agy` account. Other coding-agent runtimes can coordinate this workflow but are not interchangeable worker backends yet.

## Upgrades and existing runs

Install an explicitly chosen newer release with pip, then rerun `install`/`setup`. Do not update registrations during an active business run. Keep the older environment/version available for an in-flight run: changed instructions/models/contracts can invalidate its task fingerprints and require a new business directory. Do not reset attempts or budget counters.

Generated business data is deliberately not distributed through Git. Keep separate backups. Never commit `.env`, credentials, raw client traces, or a preview ZIP by accident.
