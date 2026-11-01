"""Versioned task contracts and a deliberately small JSON Schema validator."""
from __future__ import annotations

import json
from urllib.parse import urlsplit


class WorkflowError(Exception):
    pass


def obj(properties, required=None):
    return {"type": "object", "properties": properties,
            "required": list(properties) if required is None else required,
            "additionalProperties": False}


def arr(items, minimum=0, maximum=30):
    return {"type": "array", "items": items, "minItems": minimum, "maxItems": maximum}


TEXT = {"type": "string", "minLength": 1, "maxLength": 8000}
SHORT = {"type": "string", "minLength": 1, "maxLength": 500}
URL = {"type": "string", "minLength": 1, "maxLength": 2000}
FACT = obj({"claim": TEXT, "source_url": URL, "evidence": TEXT,
            "confidence": {"enum": ["confirmed", "inference"]}})
SOURCE = obj({"url": URL, "title": SHORT, "accessed": SHORT})
RESEARCH = obj({"status": {"enum": ["complete", "blocked"]}, "summary": TEXT,
                "sources": arr(SOURCE, 0, 15), "facts": arr(FACT, 0, 30),
                "observations": arr(TEXT), "uncertainties": arr(TEXT)})
PLAN = obj({"purpose": TEXT, "audience": TEXT, "primary_cta": SHORT,
            "cta_href": URL, "visual_direction": TEXT,
            "sections": arr(obj({"id": SHORT, "heading": SHORT, "content": TEXT}), 3, 10),
            "publishable_claims": arr(TEXT, 1), "prohibited_claims": arr(TEXT),
            "asset_policy": TEXT, "acceptance_criteria": arr(TEXT, 3),
            "interaction_checks": arr(obj({"name": SHORT, "click_selector": SHORT,
                                           "visible_selector": SHORT}), 0, 8)})
BUILD = obj({"summary": TEXT,
             "files": arr(obj({"path": SHORT, "content": {"type": "string", "maxLength": 120000}}), 1, 25),
             "asset_provenance": arr(obj({"path": SHORT, "origin": TEXT, "license": TEXT}), 0, 25)})
REVIEW = obj({"verdict": {"enum": ["pass", "revise", "blocked"]},
              "screenshots_inspected": arr(SHORT, 0, 40),
              "issues": arr(obj({"severity": {"enum": ["blocker", "major", "minor"]},
                                 "description": TEXT, "fix": TEXT})),
              "summary": TEXT})
OUTREACH = obj({"subject": SHORT, "body": TEXT, "personalization_sources": arr(URL, 0, 10)})
SCHEMAS = {"researchers": RESEARCH, "planner": PLAN, "builder": BUILD,
           "reviewer": REVIEW, "outreach": OUTREACH}


def validate(value, schema, path="$"):
    """Validate only the schema vocabulary used above; reject wrong primitive types."""
    if "enum" in schema and value not in schema["enum"]:
        raise WorkflowError(f"{path}: not an allowed value")
    typ = schema.get("type")
    valid = {"object": lambda: isinstance(value, dict),
             "array": lambda: isinstance(value, list),
             "string": lambda: isinstance(value, str),
             "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
             "boolean": lambda: isinstance(value, bool)}
    if typ and (typ not in valid or not valid[typ]()):
        raise WorkflowError(f"{path}: expected {typ}")
    if typ == "object":
        missing = set(schema.get("required", [])) - value.keys()
        extra = value.keys() - schema.get("properties", {}).keys()
        if missing or (extra and schema.get("additionalProperties") is False):
            raise WorkflowError(f"{path}: missing={sorted(missing)}, unexpected={sorted(extra)}")
        for key, item in value.items():
            if key in schema.get("properties", {}):
                validate(item, schema["properties"][key], f"{path}.{key}")
    if typ == "array":
        if not schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", 100000):
            raise WorkflowError(f"{path}: invalid array length")
        for i, item in enumerate(value):
            validate(item, schema["items"], f"{path}[{i}]")
    if typ == "string" and not schema.get("minLength", 0) <= len(value) <= schema.get("maxLength", 1000000):
        raise WorkflowError(f"{path}: invalid string length")
    return value


def parse_result(text):
    try:
        return json.loads(text)
    except (ValueError, TypeError) as exc:
        raise WorkflowError("Worker did not return a single valid JSON object") from exc


def public_url(url):
    import ipaddress
    try:
        parts = urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.hostname or parts.username or parts.password:
            return False
        host = parts.hostname.lower().rstrip(".")
        if host == "localhost" or "." not in host or host.endswith((".local", ".localhost", ".internal")):
            return False
        try:
            if not ipaddress.ip_address(host).is_global:
                return False
        except ValueError:
            pass
        return True
    except ValueError:
        return False


def validate_research(result):
    validate(result, RESEARCH)
    sources = {s["url"] for s in result["sources"]}
    if any(not public_url(url) for url in sources):
        raise WorkflowError("Research contains a non-public or invalid source URL")
    if any(f["source_url"] not in sources for f in result["facts"]):
        raise WorkflowError("Research fact has no matching source record")
    return result
