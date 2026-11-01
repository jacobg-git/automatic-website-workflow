# Website workflow: instructions for the installing/operating agent

This project uses the **current process-worker workflow**, not native parent/child subagents. Any coding agent may coordinate these CLI commands, but worker execution still requires an installed, authenticated Antigravity `agy` CLI and model quota. Native subagents are deferred.

Respect the host project's existing instructions. Installation must not replace its AGENTS.md, README, Git configuration, or other agents. Never read or collect credentials. GitHub access is needed for installation/upgrades; the model account is authenticated separately by the owner.

## Prerequisites and setup

Use the Python environment where `local-website-workflow` was installed. If using a project virtual environment, replace `python` below with that environment's Python; no shell activation is required.

- `python -m website_workflow setup --project .` safely installs project instructions/registrations and downloads Playwright Chromium. It does not install/authenticate proprietary runtimes or call models.
- `python -m website_workflow doctor --project .` checks package resources, role registrations, runtime executable, and whether Chromium launches. It does not establish authentication or remaining quota.
- Check `agy models` before a paid run. Do not silently change model routing when the selected models are unavailable.
- If Linux browser system libraries are missing, explain the required platform setup and request approval before privileged system-package installation. Do not bypass safeguards.

The setup is scoped to this directory. Do not modify global agent permissions or install global agent personas. Local model routing and limits are in `.website-workflow/workflow.config.json`; the initial installed timeout is 600 seconds. Token accounting limits are not provider billing caps.

## Run for a specific business

When the user says “run the website workflow for BUSINESS in LOCATION”:

1. Create a draft intake without inventing missing facts:

   `python -m website_workflow new-business --project . --name "BUSINESS" --location "LOCATION"`

   This returns a business directory under `.website-workflow/businesses/` and an incomplete intake. It does not call a model or start the workflow.
2. Using your available research tools, establish the exact business identity, public source links, and a useful verified CTA (telephone, existing booking/contact link, or another justified action). Check for an existing official website and flag an unsuitable prospect. Add only facts you actually verified; distinguish user-provided statements from independent evidence. Do not infer registration status or nonexistence from empty search results.
3. Complete that directory's `intake.json`: meaningful description, verified facts, source URLs, optional competitors, and `primary_cta` with a verified label/href. Set `verified: true` only after checking the destination. Do not invent testimonials, prices, opening hours, staff, contact details, or licensed assets. If essential information cannot be verified, stop and ask one focused question rather than fabricate it.
4. Validate before spending quota:

   `python -m website_workflow validate-intake --intake .website-workflow/businesses/SLUG/intake.json`
5. Start the current process-based workflow:

   `python -m website_workflow run --project .website-workflow/businesses/SLUG`

   The installed project configuration is discovered automatically. Default roles use Flash for research/outreach and Argon for planning/build/review. Python launches independent CLI worker conversations and controls their stage handoffs.
6. Monitor state with `python -m website_workflow status --project .website-workflow/businesses/SLUG`. Do not launch a duplicate runner or remove a lock while its owner/children are alive. Resume with the same run command; do not reset usage/attempts to bypass limits.
7. If blocked, inspect state, attempt stderr/stdout, and QA results. Do not weaken image receipts, static-only checks, permission limits, or approval gates to force success. Report unresolved evidence and runtime failures honestly.
8. At `awaiting_approval`, present the site, research uncertainties, QA report/screenshots, static ZIP, and unsent outreach draft. Preview with `python -m website_workflow serve --project .website-workflow/businesses/SLUG` (localhost only; stop the server when finished).

For a fictional smoke/pilot instead: `python -m website_workflow init --project .website-workflow/businesses/demo --demo`, then run that directory. Inference consumes real account quota even for fictional businesses.

## Outputs and ownership

Each business directory contains intake/state, research Markdown, a website brief, static `site/`, browser QA/screenshots, outreach draft, and a `delivery/siteground-static.zip` after all release gates pass. Only the user-facing orchestrator/backend maintains shared documentation/state; specialist workers return assigned artifacts. The host project controls its own wiki policy.

Business directories and raw traces are Git-ignored by the installer because they may contain client/contact data. Keep separate backups; they will not appear in a fresh clone. Installation resources and configuration can be versioned. Preserve modified local configuration on updates. Managed role/registration files must not be silently overwritten if edited.

## Approval boundary

Everything stops locally. No preview upload, public deployment, email sending, purchase, DNS/domain change, or expanded credential use without separate explicit user approval. There are no upload/publish/send commands. Do not add ad hoc shell/network steps to bypass this boundary. Do not use `--dangerously-skip-permissions`.

Draft HTML remains noindex. The email retains preview/sender placeholders; remove internal sender notes and replace placeholders only after appropriate approval. A passed fictional demo or automated audit is not a factual, legal, licensing, full accessibility, or production guarantee.
