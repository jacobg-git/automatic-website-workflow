"""Non-destructive, project-local workflow installation and dependency bootstrap."""
from __future__ import annotations

import os
import re
import stat
import subprocess
import sys
from pathlib import Path

from . import __version__
from .adapters import render_agents
from .config import ROLES, resource_path
from .contracts import WorkflowError
from .storage import ProjectLock, digest, read_json, write_json

DIRECTORY = ".website-workflow"
BEGIN = b"<!-- BEGIN website-workflow -->"
END = b"<!-- END website-workflow -->"


def is_linked(path):
    if path.is_symlink():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    # Covers junctions on Python 3.11, before Path.is_junction was available.
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def safe_destination(root, relative):
    path = root / relative
    if not path.is_relative_to(root):
        raise WorkflowError("Installation path escapes project")
    for parent in (path, *path.parents):
        if parent == root.parent:
            break
        if is_linked(parent):
            raise WorkflowError(f"Refusing linked installation path: {parent}")
        if parent.exists() and parent != path and not parent.is_dir():
            raise WorkflowError(f"Installation parent is not a directory: {parent}")
    if path.exists() and not path.is_file():
        raise WorkflowError(f"Installation destination is not a file: {path}")
    return path


def canonical_bytes(text):
    return text.replace("\r\n", "\n").encode("utf-8")


def managed_hash(data):
    # Git may transport managed text as CRLF without a semantic user edit.
    return digest(data.replace(b"\r\n", b"\n"))


def append_block(original, block, previous_hash, name):
    """Preserve all host bytes outside our owned marker block, including BOM/CRLF."""
    if original.count(BEGIN) != original.count(END) or original.count(BEGIN) > 1:
        raise WorkflowError(f"Malformed or duplicate workflow markers in {name}")
    if BEGIN not in original:
        separator = b"\n\n" if original and not original.endswith(b"\n\n") else b""
        return original + separator + block + b"\n"
    start = original.index(BEGIN); stop = original.index(END) + len(END)
    if stop < start:
        raise WorkflowError(f"Malformed workflow marker order in {name}")
    owned = original[start:stop]
    if managed_hash(owned) == managed_hash(block):
        return original
    if managed_hash(owned) != previous_hash:
        raise WorkflowError(f"Workflow instruction block was edited in {name}; refusing overwrite")
    return original[:start] + block + original[stop:]


def _install(root, dry_run):
    control = root / DIRECTORY
    marker = safe_destination(root, f"{DIRECTORY}/installation.json")
    marker_temp = safe_destination(root, f"{DIRECTORY}/installation.json.tmp")
    if marker_temp.exists():
        raise WorkflowError(f"Existing installation temporary file requires inspection: {marker_temp}")
    business_root = control / "businesses"
    if business_root.exists() and any(business_root.glob("*/.workflow.lock")):
        raise WorkflowError("A business run is locked; stop/inspect it before updating project registrations")
    previous = read_json(marker) if marker.exists() else {"version": 1, "files": {}, "blocks": {}}
    if previous.get("version") != 1 or not isinstance(previous.get("files"), dict) or not isinstance(previous.get("blocks"), dict):
        raise WorkflowError("Invalid installation ownership manifest")
    defaults = read_json(resource_path("workflow.config.json"))
    defaults["task_timeout_seconds"] = 600
    import json
    contents = {
        f"{DIRECTORY}/AGENT_GUIDE.md": (Path(__file__).parent / "templates" / "PROJECT_GUIDE.md").read_bytes(),
        f"{DIRECTORY}/workflow.config.json": (json.dumps(defaults, indent=2) + "\n").encode(),
        f"{DIRECTORY}/intake-template.json": resource_path("examples/intake-template.json").read_bytes(),
    }
    for role in (*ROLES, "orchestrator"):
        contents[f"{DIRECTORY}/roles/{role}/AGENTS.md"] = canonical_bytes(resource_path(f"roles/{role}/AGENTS.md").read_text(encoding="utf-8"))
    for name, body in render_agents().items():
        contents[f".agents/agents/{name}"] = canonical_bytes(body)
    plan, hashes = [], {}
    for relative, desired in contents.items():
        path = safe_destination(root, relative)
        current = path.read_bytes() if path.exists() else None
        old_hash = previous["files"].get(relative)
        if current is not None and managed_hash(current) == managed_hash(desired):
            desired = current  # Preserve transport-only CRLF differences.
        elif current is not None:
            # Configuration is intentionally user-editable after a known installation.
            if relative.endswith("/workflow.config.json") and old_hash:
                desired = current
            elif not old_hash or managed_hash(current) != old_hash:
                raise WorkflowError(f"Installation conflict: {relative} was not installed by this version or was edited; no files changed")
        hashes[relative] = managed_hash(desired)
        plan.append((relative, path, current, desired))
    blocks = {
        "AGENTS.md": BEGIN + b"\n## Website workflow\n\nWhen asked to create a business website, read `.website-workflow/AGENT_GUIDE.md` and follow it. Respect this project's other instructions. Current execution uses Python-managed agy workers, not native subagents. Stop before any upload, publication, or sending.\n" + END,
        ".gitignore": BEGIN + b"\n# Private business evidence, prompts, screenshots, model traces, and delivery files\n.website-workflow/businesses/\n.workflow.lock\n.venv/\n__pycache__/\n" + END,
    }
    for name, block in blocks.items():
        path = safe_destination(root, name)
        current = path.read_bytes() if path.exists() else b""
        desired = append_block(current, block, previous["blocks"].get(name), name)
        plan.append((name, path, current if path.exists() else None, desired))
    report = {"project": str(root), "package_version": __version__, "mode": "process-workers",
              "dry_run": dry_run, "files": [{"path": name, "action": "unchanged" if current == desired else "create" if current is None else "update"} for name, _, current, desired in plan],
              "guide": str(control / "AGENT_GUIDE.md"), "model_calls": 0}
    for _, path, current, desired in plan:
        if current != desired:
            temporary = path.with_name(path.name + ".website-workflow-tmp")
            safe_destination(root, temporary.relative_to(root))
            if temporary.exists():
                raise WorkflowError(f"Unexpected existing installer temporary file: {temporary}")
    if dry_run:
        return report
    # Conflict checks finish before any writes. Same-directory replacements avoid partial files.
    for _, path, current, desired in plan:
        if current == desired:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".website-workflow-tmp")
        safe_destination(root, temporary.relative_to(root))
        if temporary.exists():
            raise WorkflowError(f"Unexpected existing installer temporary file: {temporary}")
        try:
            with temporary.open("xb") as stream:
                stream.write(desired)
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
    write_json(marker, {"version": 1, "package_version": __version__, "mode": "process-workers",
                        "files": hashes, "blocks": {name: managed_hash(block) for name, block in blocks.items()}})
    return report


def install_project(project, dry_run=False):
    given = Path(project).absolute()
    if is_linked(given):
        raise WorkflowError("Project root must not be a symlink or junction")
    root = given.resolve()
    if root.exists() and not root.is_dir():
        raise WorkflowError("Project root is not a directory")
    if dry_run:
        return _install(root, True)
    root.mkdir(parents=True, exist_ok=True)
    with ProjectLock(root):
        return _install(root, False)


def setup_project(project, dry_run=False):
    report = install_project(project, dry_run=dry_run)
    if dry_run:
        report["browser_setup"] = "would run python -m playwright install chromium"
        return report
    try:
        result = subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"],
                                timeout=600, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise WorkflowError(f"Project instructions installed, browser setup failed: {exc}. Retry setup; no model calls occurred.") from exc
    if result.returncode:
        raise WorkflowError("Project instructions installed, but Chromium installation failed. Retry setup and check platform dependencies; no model calls occurred.")
    report["browser_setup"] = "Chromium installer completed; run doctor to verify launch"
    return report


def new_business(project, name, location, slug=None):
    root = Path(project).resolve()
    if not (root / DIRECTORY / "installation.json").is_file():
        raise WorkflowError("Install into this project first: website-workflow install --project <root>")
    if not name.strip() or not location.strip() or len(name) > 300 or len(location) > 300:
        raise WorkflowError("Provide a business name and location (each 1..300 characters)")
    slug = slug or re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug or len(slug) > 100 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise WorkflowError("Supply a safe lowercase --slug (up to 100 characters)")
    relative = f"{DIRECTORY}/businesses/{slug}/intake.json"
    destination = safe_destination(root, relative)
    with ProjectLock(root):
        if destination.parent.exists():
            raise WorkflowError(f"Business project already exists: {destination.parent}; inspect/resume it, do not overwrite")
        intake = read_json(resource_path("examples/intake-template.json"))
        intake.update(slug=slug, business_name=name.strip(), location=location.strip(),
                      description="Complete verified business context before running.", verified_facts=[],
                      primary_cta={"label": "", "href": "", "verified": False}, demo=False)
        write_json(destination, intake)
    return {"project": str(destination.parent), "intake": str(destination), "status": "needs_verified_intake",
            "next": "Read .website-workflow/AGENT_GUIDE.md; verify facts and CTA, fill intake, validate-intake, then run", "model_calls": 0}
