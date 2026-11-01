# Automatic website workflow

An installable, local-only workflow for researching a business, planning and building a static SiteGround website, testing it, and drafting outreach.

**Current execution:** Python launches independent Antigravity `agy` worker conversations. These are **not native parent/child subagents**. Native subagents are deferred until after distribution of this working version.

**Repository visibility:** private. Installing agents need authenticated Git access to `jacobg-git/automatic-website-workflow`; model authentication is separate.

## Install into a new project

**Agents: read [INSTALL.md](INSTALL.md) first.** It contains Windows/macOS/Linux commands, private-repository authentication requirements, safe setup, and the exact business-run procedure.

From a target project, using its Python 3.11+ virtual environment:

```bash
python -m pip install "local-website-workflow @ git+https://github.com/jacobg-git/automatic-website-workflow.git@v0.2.0"
python -m website_workflow setup --project .
python -m website_workflow doctor --project .
```

Pip installs Python dependencies, including Playwright. `setup` installs project-local instructions/registrations and downloads Chromium. It does not install Python/Git, authenticate a proprietary agent account, collect credentials, or make model calls. Check `agy models` separately for account access/model availability. Linux may need approved browser system libraries.

Setup preserves existing `AGENTS.md` content, appending one marked pointer to `.website-workflow/AGENT_GUIDE.md`. It does not replace your README or unrelated agents. Ownership hashes protect edited managed files; configuration edits survive reinstall. Use `--dry-run` to preview setup without writes/downloads.

## Tell your agent

> Install this workflow from the private repository `jacobg-git/automatic-website-workflow` using `INSTALL.md`, without replacing this project's existing instructions. Read the installed guide and run the workflow for **BUSINESS NAME in LOCATION**. Verify the business, existing web presence, facts, and CTA first. Stop before uploading, publishing, or sending anything.

Any coding agent can operate the CLI, but worker execution currently requires authenticated **Antigravity**. Native Pi/Codex worker adapters are not implemented.

## Start a business run

```bash
python -m website_workflow new-business --project . --name "Business Name" --location "City, Region"
```

This creates an unverified intake under `.website-workflow/businesses/business-name/`. Your operating agent follows `.website-workflow/AGENT_GUIDE.md` to establish identity, public sources, verified facts, and a useful verified CTA. It must not invent missing details or set verification flags just to pass validation.

```bash
python -m website_workflow validate-intake --intake .website-workflow/businesses/business-name/intake.json
python -m website_workflow run --project .website-workflow/businesses/business-name
python -m website_workflow status --project .website-workflow/businesses/business-name
python -m website_workflow serve --project .website-workflow/businesses/business-name
```

Local configuration is discovered automatically at `.website-workflow/workflow.config.json`. Installed projects default to a 600-second task timeout. Model runs consume quota; structural intake validation is not independent factual verification.

## What runs

1. **Parallel research:** Flash Low workers gather business and competitor findings with source references and uncertainties.
2. **Planning:** Argon Medium specifies purpose, CTA, page structure, copy, visual direction, assets, and acceptance checks.
3. **Building:** Argon High returns self-contained HTML/CSS/JS/original SVG assets. Python validates and writes them.
4. **Browser QA:** real Chromium at 390/768/1440px checks functionality, missing resources, errors, overflow, and captures screenshots.
5. **Independent visual review:** Argon Medium must actually open each required image. Successful image-view events and matching PNG hashes are required; self-reports are insufficient.
6. **Bounded corrections:** findings go back to Argon, followed by fresh QA/review.
7. **Local handoff:** a static ZIP, SiteGround instructions, QA evidence, and an unsent Flash-written outreach draft. The terminal state is `awaiting_approval`, not deployed.

The conversational coordinator and Python backend own shared docs/state; workers return assigned artifacts. Canonical roles are in `roles/*/AGENTS.md`, with generated Antigravity registrations. Project installation includes versioned role snapshots and a primary-only coordinator persona. The coordinator persona still uses the process scheduler, not `invoke_subagent`.

## Outputs

```text
.website-workflow/businesses/<slug>/
  intake.json, state.json
  tasks/<task>/result.json            # validated results and per-attempt traces
  research/*.md                      # reports and evidence ledger
  plan/website-brief.md
  plan/asset-provenance.md
  site/                              # plain static files
  qa/                                # audits, image evidence, screenshots
  outreach/draft.md                   # never sent
  delivery/siteground-static.zip     # only after release gates pass
  delivery/SITEGROUND.md
  docs/progress.md, docs/handoff.md
```

The installer adds a Git-ignore rule for business outputs because traces may contain client/contact information. Keep separate backups. Package instructions/configuration can be committed; generated clients, credentials, and `.env` must not be committed accidentally.

Resume using the same `run` command. Do not launch duplicates, reset attempt/call counters, or remove locks before confirming processes stopped. Modified site/result/package hashes are not silently trusted or overwritten. Changed intake/models/instructions can require a new run directory; retain an older package environment for in-flight work when upgrading.

## Safety and limitations

- No upload, publish, purchase, DNS/domain, or email-sending commands. Separate explicit approval is required for those actions.
- Draft HTML stays noindex. Preview/sender placeholders and internal notes must be reviewed before any approved outreach.
- Plain static output only: no application server, contact backend, remote runtime dependencies, or analytics included.
- Research must respect source restrictions, uncertainty, identity conflicts, privacy, and asset rights. Empty search results do not prove nonexistence or registration status.
- Token budgets are accounting/pre-launch limits, not provider billing caps; failed/in-flight work may consume unreported quota.
- The sandbox/tool policies are safeguards, not a security guarantee for arbitrary agent code. No global auto-approval settings are changed.
- Chromium checks are not complete WCAG/contrast/Lighthouse/cross-browser certification. Missing browser/image evidence blocks delivery.
- Native subagents, deeper research corroboration, and additional recovery/QA hardening remain future work. See [native migration plan](docs/workflow/native-subagents.md).

## Proven baseline and development

The earlier fictional pilot completed real parallel research, Argon planning/building, two correction cycles, receipt-backed visual review, ZIP packaging, and outreach drafting. Its completed rerun made no model calls. This is not a production guarantee for arbitrary real clients.

Source development:

```bash
python -m pip install -e .
python -m website_workflow sync-agents
python -m unittest discover -s tests -v
python -m pip wheel --no-deps --wheel-dir dist .
```

Wheels bundle canonical roles, examples, default configuration, and the project guide; they do not depend on this source checkout at runtime. `scripts/check_installed.py` runs with an installed wheel (`python -I scripts/check_installed.py`) and exercises a fresh host, real Chromium, packaging, and cached verification with explicitly simulated model/visual responses and zero inference. CI is configured to build and test on Linux/Windows with Python 3.11/3.13; check the actual run status before claiming a remote pass.

Source-checkout legacy runs under `projects/` remain supported and Git-ignored. See [documentation index](docs/index.md) and [implementation handoff](docs/workflow/implementation-handoff.md).
