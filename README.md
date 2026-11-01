# Local website workflow

A portable, local-only agent workflow for researching a business, planning and building a static SiteGround-ready website, testing it, and drafting outreach. **The first live Antigravity demo passes end to end locally.** Further research/reliability hardening and native Pi/Codex wrappers remain; see the [continuation handoff](docs/workflow/implementation-handoff.md).

## Current capabilities

- Python orchestration with concurrent, isolated Antigravity worker conversations and exact model selection.
- Portable role instructions in `roles/*/AGENTS.md`; generated Antigravity registrations in `.agents/agents/`.
- JSON task/result validation, durable checkpoints, two attempts per task, bounded calls/time/output, and resume protection.
- Workers return data and file contents; only the orchestrator writes project artifacts and shared state/docs.
- Static HTML/CSS/JS validation and real Playwright Chromium screenshots/functionality checks at 390, 768, and 1440px.
- Independent vision-review stage with successful image-view tool receipts and screenshot-hash checks, correction loops, ZIP packaging, SiteGround handoff, and outreach draft.
- Compact reviewer/revision briefs use readable page copy and source paths rather than repeatedly embedding full code bundles.
- No upload, publishing, purchase, domain, or email-sending commands.

**Verified:** a fictional pilot completed real parallel research, Argon planning/building, two correction cycles, receipt-backed visual review, static packaging, and an unsent outreach draft. A repeated completed run made no new model calls. **39 automated tests pass.** This is not a guarantee of factual, legal, accessibility, or production readiness for arbitrary real businesses.

## Requirements

Python 3.11+, authenticated `agy`, and Playwright with Chromium. Run commands from this repository (or use an editable install; a standalone wheel is not currently supported because role/config resources live in the repository).

```bash
python -m pip install -e ".[qa]"
python -m playwright install chromium
python -m website_workflow sync-agents
python -m website_workflow doctor
python -m unittest discover -s tests -v
```

`doctor` makes no model calls and does not change global Antigravity settings. Worker sessions use explicit session-only deny rules, never `--dangerously-skip-permissions`.

## Conversational orchestrator

To coordinate the workflow from Antigravity interactively:

```bash
agy --agent website-orchestrator --model gemini-4-argon-medium --sandbox --settings '{"toolPermission":"request-review"}'
```

Its canonical instructions live in `roles/orchestrator/AGENTS.md`. It talks with you, uses the Python backend for scheduling/checkpoints, and maintains documentation. It does not launch duplicate native workers for engine-managed tasks. The launch command explicitly requests session-only permission review and sandboxing rather than relying on potentially permissive inherited defaults; no global auto-approval setting is changed. The registration is generated and statically tested; a complete interactive orchestrator session has not yet been tested.

## Fictional pilot

```bash
python -m website_workflow init --project projects/my-demo --demo
python -m website_workflow run --project projects/my-demo
python -m website_workflow status --project projects/my-demo
python -m website_workflow serve --project projects/my-demo
```

The demo deliberately represents no real business. Running it calls paid/quota-consuming models. Read `workflow.config.json` before running. Default routing uses Flash Low for research/outreach, Argon Medium for planning/review, and Argon High for building.

## Real business

Copy `examples/intake-template.json` outside the examples folder, replace the fields with verified information, provide a real useful CTA, and set `primary_cta.verified` to true only after checking it. Source URLs and optional competitor URLs must be public HTTP(S). Intake facts are operator assertions, not independently verified facts. Do not put credentials in intake.

```bash
python -m website_workflow init --project projects/business-slug --intake path/to/intake.json
python -m website_workflow run --project projects/business-slug
```

Resume with the same `run` command. Changing intake, model routing, adapter, or QA policy requires a new project. Modified site files and modified cached results are not silently overwritten or trusted. If a crashed process leaves `.workflow.lock`, confirm the process and all its workers are stopped before removing it.

## Outputs

```text
projects/<business>/
  intake.json
  state.json
  tasks/<task>/result.json          # validated outputs, per-attempt traces
  research/*.md                    # source-backed reports and evidence ledger
  plan/website-brief.md
  plan/asset-provenance.md
  site/                            # generated static files
  qa/                              # audits and screenshot sets
  outreach/draft.md                 # never sent
  delivery/siteground-static.zip   # created only after release gates pass
  delivery/SITEGROUND.md
  docs/progress.md
  docs/handoff.md
```

Generated projects are Git-ignored because traces can contain business/contact information. Keep local backups if needed. A future clone will not contain your local pilot state.

The successful terminal status is `awaiting_approval`, never deployed. The outreach preview/sender placeholders are intentional and must be replaced only after appropriate approvals. Draft HTML stays `noindex`. Local success does not certify legal compliance, licensing, accessibility, or factual accuracy.

## Portability

The workflow contracts and roles are runtime-independent. The tested native adapter is Antigravity. A generic `command` adapter executes an argv array without a shell, sends the task prompt on stdin, and expects JSON on stdout (or a configurable envelope field). This can host wrappers for other agents; **Pi/Codex-specific integrations have not been implemented or tested**. See [implementation details and handoff](docs/workflow/implementation-handoff.md).

## Safety and practical limits

- Plain static files only; no application server, build dependency, contact form backend, analytics, or remote runtime assets.
- Research websites are untrusted data. Do not bypass access restrictions or reuse unlicensed assets.
- The runner has no credentials or external-action integrations, but agent CLI access is not a security sandbox for arbitrary code. Review session permissions and runtime behavior before using sensitive environments.
- Token limits are post-response accounting/pre-launch checks, not a hard provider billing cap; in-flight work and failed/unreported calls can consume extra quota.
- Playwright blocks non-local requests during QA and does not activate contact links or submit forms.
- Stop on missing browser/vision capability, exhausted budget, incomplete evidence, or failed release gates rather than claiming success.

Start with [docs/index.md](docs/index.md).
