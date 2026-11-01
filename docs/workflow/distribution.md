# Reusable private-repository distribution

## Decision

The user requested installation of the **current process-worker workflow** into other projects and deferred native subagents until later. They explicitly chose to **keep the existing repository private**:

`https://github.com/jacobg-git/automatic-website-workflow`

The installation entry point for humans and agents is [INSTALL.md](../../INSTALL.md). Git access and model authentication are separate prerequisites; do not collect or embed credentials.

## Release layout

Version `0.2.0` introduced a standard installable Python distribution. Patch `0.2.1` retains the same runtime, corrects environment-dependent test fixtures for missing `agy` and Windows temporary-path aliases, and becomes the recommended install pin once verified. Pip installs Playwright as a core dependency; the old `[qa]` extra remains a compatibility alias. The build hook copies canonical root role files, examples, and defaults into wheel `_assets/` without maintaining duplicate source copies. Source distributions include those canonical assets so wheels built from sdists work too.

`resource_path` locates wheel assets or canonical source assets. Runtime operations no longer require executing from this development checkout or writing into site-packages.

## Project-local commands

- `setup --project ROOT`: ownership-aware project installation plus `python -m playwright install chromium`, using the current Python environment. No model calls, runtime authentication, privileged OS package installation, or global agent permission changes.
- `install --project ROOT`: same project files, without browser download.
- `setup/install --dry-run`: preview without creating directories, downloading, or invoking models.
- `new-business --project ROOT --name NAME --location LOCATION [--slug SLUG]`: safe incomplete intake scaffold; no inference and no fabricated verification.
- `validate-intake --intake FILE`: structural validation before model spending, not independent factual verification.
- `doctor --project ROOT`: resources/registrations/executable/browser-launch checks. Authentication, model entitlement, and quota require separate checks.
- Existing `run/status/qa/serve/init` commands operate on business directories. Installed host configuration is discovered automatically.

## Preservation and ownership

The installer creates `.website-workflow/AGENT_GUIDE.md`, default configuration, intake template, role snapshots, and project-local `.agents/agents/website-*.md` registrations. It appends one marked pointer to the host `AGENTS.md` and exclusions to `.gitignore`, preserving existing bytes outside owned blocks, including BOM and CRLF.

An installation manifest records managed-file/block hashes and package version. All conflicts are checked before writes. Identical reinstall is idempotent. Owned unedited files can update; edited/unrelated managed-file collisions fail instead of being overwritten. Configuration is intentionally preserved on updates. CRLF transport differences are not treated as semantic edits. Linked destinations and unexpected temporary files are rejected. Active business locks block role updates.

The installer does not replace the host README, import this repository's wiki rules into the host, initialize Git, or touch unrelated agent definitions. Per-file replacement is atomic; whole-install transactions/rollback are not claimed. Preserve backups and inspect any interrupted-install conflict.

Business output lives under `.website-workflow/businesses/` and is Git-ignored. The worker adapter runs from the actual host workspace, so installed registrations and local screenshot/source paths remain in the worker's workspace scope. The Python scheduler still launches independent `agy` processes; this packaging change does not implement native subagents.

## Verification evidence

- 59 tests executed locally: 58 passed, one real filesystem-symlink case skipped because Windows lacks symlink privileges. A separate simulated-link guard test passes. The original workflow/browser tests continue to pass.
- Built both sdist and wheel, including a wheel rebuilt from the sdist.
- Installed the wheel and all dependencies into a fresh, isolated virtual environment outside the checkout.
- Ran `python -I scripts/check_installed.py` against the installed wheel from a fresh host project. It exercised setup/Chromium download, preserved host instructions, idempotent install, doctor, named-business intake, validation, real Chromium screenshots, ZIP delivery, and no-inference completed verification. Model/visual judgments were explicit test doubles; zero inference occurred.
- Fresh environment used Playwright 1.64.1 and Chromium 156.0.8078.4; the original development environment used Playwright 1.61.0. This is packaging compatibility evidence, not a new live-business/model pilot.
- GitHub Actions is configured for Linux/Windows and Python 3.11/3.13. Remote CI status must be inspected; configuration alone is not a passed run.

## Publishing and future changes

Version `v0.2.0` was published to the existing private origin and authenticated GitHub-tag installation passed in a fresh environment. Its first CI run exposed test-fixture assumptions, not an installed runtime failure. Publish the corrected `v0.2.1` after verifying the matrix; do not move the original release tag. Do not publish generated business projects, model traces, test virtual environments, caches, credentials, or client ZIPs. GitHub release/package files, if attached, must contain only the workflow distribution, not generated client deliverables.

After distribution verification, the next architecture milestone remains [native subagent migration](native-subagents.md). Additional factual corroboration is required before real-client production use. Role/model/contract upgrades can invalidate in-flight task fingerprints; retain an older environment for old runs rather than resetting their counters or silently rewriting evidence.
