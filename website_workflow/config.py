from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

from .contracts import WorkflowError, public_url
from .storage import read_json

ROOT = Path(__file__).resolve().parent.parent
ROLES = ("researchers", "planner", "builder", "reviewer", "outreach")


def resource_path(relative):
    """Locate wheel-bundled assets, or canonical assets in a source checkout."""
    assets = Path(__file__).resolve().parent / "_assets"
    path = assets / relative if assets.is_dir() else ROOT / relative
    if not path.is_file():
        raise WorkflowError(f"Required workflow asset missing: {relative}. Reinstall the package.")
    return path


def find_workspace(project=None):
    start = Path(project or Path.cwd()).resolve()
    for parent in (start, *start.parents):
        if (parent / ".website-workflow" / "installation.json").is_file():
            return parent
        if (parent / "workflow.config.json").is_file() and (parent / ".agents" / "agents" / "website-builder.md").is_file():
            return parent
    return start


def default_config_path(workspace=None):
    installed = Path(workspace or Path.cwd()) / ".website-workflow" / "workflow.config.json"
    return installed if installed.is_file() else resource_path("workflow.config.json")


def load_config(path=None):
    config = read_json(path or default_config_path())
    if config.get("adapter") not in ("antigravity", "command", "fixture"):
        raise WorkflowError("adapter must be antigravity, command, or fixture")
    for key, low, high in (("concurrency", 1, 8), ("max_competitors", 0, 5),
                           ("max_fix_cycles", 0, 5), ("max_calls", 1, 100),
                           ("max_total_tokens", 1, 10000000), ("task_timeout_seconds", 1, 3600),
                           ("max_prompt_chars", 1000, 500000), ("max_stream_bytes", 1000, 10000000)):
        value = config.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or not low <= value <= high:
            raise WorkflowError(f"Invalid config {key}: expected integer {low}..{high}")
    for key in ("require_browser", "require_visual_review"):
        if not isinstance(config.get(key), bool):
            raise WorkflowError(f"Invalid config {key}: expected boolean")
    if set(config.get("models", {})) != set(ROLES) or any(not isinstance(v, str) or not v for v in config["models"].values()):
        raise WorkflowError("Config must provide a nonempty model for every role")
    if config["adapter"] == "command" and (not isinstance(config.get("command"), list) or not config["command"] or any(not isinstance(v, str) for v in config["command"])):
        raise WorkflowError("command adapter requires a nonempty argv string array")
    return config


def validate_intake(value):
    if not isinstance(value, dict):
        raise WorkflowError("Intake must be an object")
    required = ("slug", "business_name", "location", "description", "verified_facts", "primary_cta", "source_urls", "competitors", "demo")
    if any(key not in value for key in required):
        raise WorkflowError("Intake requires: " + ", ".join(required))
    if not isinstance(value["slug"], str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value["slug"]):
        raise WorkflowError("slug must be lowercase kebab-case")
    for key in ("business_name", "location", "description"):
        if not isinstance(value[key], str) or not value[key].strip() or len(value[key]) > 4000:
            raise WorkflowError(f"Invalid intake {key}")
    if not isinstance(value["demo"], bool):
        raise WorkflowError("demo must be boolean")
    facts = value["verified_facts"]
    if not isinstance(facts, list) or not facts or len(facts) > 30 or any(not isinstance(f, str) or not f.strip() or len(f) > 2000 for f in facts):
        raise WorkflowError("Supply 1..30 explicitly verified intake facts")
    cta = value["primary_cta"]
    if not isinstance(cta, dict) or set(cta) != {"label", "href", "verified"} or cta["verified"] is not True:
        raise WorkflowError("A verified primary_cta {label, href, verified:true} is required")
    if not isinstance(cta["label"], str) or not cta["label"].strip() or not isinstance(cta["href"], str):
        raise WorkflowError("Invalid CTA label/href")
    href = cta["href"]
    parsed = urlsplit(href)
    valid = public_url(href)
    if parsed.scheme == "tel":
        valid = bool(re.fullmatch(r"tel:\+?[0-9 ()-]{7,30}", href))
    elif parsed.scheme == "mailto":
        valid = bool(re.fullmatch(r"mailto:[^\s@?]+@[^\s@?]+\.[^\s@?]+", href))
    elif href.startswith("#"):
        valid = bool(re.fullmatch(r"#[A-Za-z][\w-]*", href))
    if not valid:
        raise WorkflowError("CTA must be a safe verified HTTPS/HTTP, tel, mailto, or internal anchor link")
    urls, competitors = value["source_urls"], value["competitors"]
    if not isinstance(urls, list) or len(urls) > 12 or any(not isinstance(u, str) or not public_url(u) for u in urls):
        raise WorkflowError("source_urls must contain at most 12 public HTTP(S) URLs")
    if not isinstance(competitors, list) or len(competitors) > 5:
        raise WorkflowError("competitors must contain at most 5 entries")
    for competitor in competitors:
        if not isinstance(competitor, dict) or set(competitor) != {"name", "url"} or not isinstance(competitor["name"], str) or not competitor["name"].strip() or not public_url(competitor.get("url", "")):
            raise WorkflowError("Each competitor requires a name and public URL")
    return value
