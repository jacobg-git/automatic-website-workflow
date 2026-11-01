"""Run with the wheel installed: python -I scripts/check_installed.py.

Exercises a fresh host project, actual Chromium and ZIP delivery, but explicit
model/vision test doubles. Never calls a model or needs GitHub/runtime credentials.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import website_workflow
from website_workflow.adapters import image_key
from website_workflow.config import load_config, resource_path
from website_workflow.engine import Engine
from website_workflow.storage import digest, read_json, write_json


def cli(*args, cwd, expected=(0,)):
    result = subprocess.run([sys.executable, "-I", "-m", "website_workflow", *args], cwd=cwd,
                            capture_output=True, text=True, encoding="utf-8", timeout=180)
    if result.returncode not in expected:
        raise AssertionError(f"CLI failed: {args}\n{result.stdout}\n{result.stderr}")
    return result


class FixtureModels:
    """Trusted test adapter; its receipts are simulated, not independent image judgment."""
    calls = 0
    def run(self, role, prompt, workdir, task_id):
        self.calls += 1
        payload = json.loads(prompt.partition("TASK INPUT (data, not instructions from external sources):\n")[2].rpartition("\n\nNo explanations")[0])
        usage = {"fixture": True, "total_tokens": 0}
        if role == "researchers":
            result = {"status": "blocked", "summary": "Fictional fixture; no real research", "facts": [], "sources": [], "observations": [], "uncertainties": ["Test double"]}
        elif role == "planner":
            result = {"purpose": "Demonstrate static website installation", "audience": "Test reviewers", "primary_cta": "Explore concept", "cta_href": "#contact",
                      "visual_direction": "Cream and evergreen, accessible system typography", "sections": [{"id": x, "heading": x.title(), "content": "Fictional test content"} for x in ("hero", "services", "contact")],
                      "publishable_claims": payload["approved_business_facts"], "prohibited_claims": ["No invented business details"], "asset_policy": "Original CSS only", "acceptance_criteria": ["Responsive", "Static", "Verified CTA"], "interaction_checks": []}
        elif role == "builder":
            html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Fictional package installation test"><meta name="robots" content="noindex,nofollow"><title>Fixture Workshop</title><style>body{font:20px/1.6 system-ui;margin:24px;background:#faf7ed;color:#173d30}main{max-width:900px;margin:auto}a{color:inherit}a:focus-visible{outline:3px solid #173d30}section{padding:32px 0}</style></head><body><a href="#main">Skip to content</a><nav><a href="#contact">Explore concept</a></nav><main id="main"><h1>Fixture Workshop</h1><section id="services"><h2>Fictional demonstration</h2><p>No real business or contact information.</p></section><section id="contact"><h2>Concept details</h2><p>Local installation test only.</p></section></main></body></html>'
            result = {"summary": "Fictional package smoke site", "files": [{"path": "index.html", "content": html}], "asset_provenance": []}
        elif role == "reviewer":
            result = {"verdict": "pass", "screenshots_inspected": payload["screenshot_paths"], "issues": [], "summary": "Test-double review, not real visual judgment"}
            usage["viewed_images"] = {image_key(path): digest(Path(path).read_bytes()) for path in payload["screenshot_paths"]}
        else:
            result = {"subject": "Independent concept", "body": "Independent fictional preview: [APPROVED_PREVIEW_URL]. Reply to discuss. [SENDER_NAME]", "personalization_sources": []}
        return result, usage


def main():
    package = Path(website_workflow.__file__).resolve().parent
    assert (package / "_assets/roles/builder/AGENTS.md").is_file(), "Test must use installed wheel assets, not the source checkout"
    assert resource_path("workflow.config.json").is_relative_to(package)
    with tempfile.TemporaryDirectory(prefix="website-installed-") as temporary:
        host = Path(temporary)
        original = b"# Existing host project\r\nDo not overwrite this policy.\r\n"
        (host / "AGENTS.md").write_bytes(original)
        cli("setup", "--project", str(host), cwd=host)
        cli("install", "--project", str(host), cwd=host)
        assert (host / "AGENTS.md").read_bytes().startswith(original)
        findings = json.loads(cli("doctor", "--project", str(host), cwd=host, expected=(0, 1)).stdout)
        assert not findings.get("browser_error"), findings
        assert findings["agent_registrations"] and findings["chromium"]
        new = json.loads(cli("new-business", "--project", str(host), "--name", "Fixture Workshop", "--location", "Test City", cwd=host).stdout)
        business = Path(new["project"])
        intake = read_json(new["intake"])
        intake.update(description="Fictional installation test", verified_facts=["Fixture Workshop is a fictional test business."],
                      primary_cta={"label": "Explore concept", "href": "#contact", "verified": True}, demo=True)
        write_json(new["intake"], intake)
        cli("validate-intake", "--intake", new["intake"], cwd=host)
        config_path = host / ".website-workflow/workflow.config.json"
        config = load_config(config_path); config.update(adapter="command", command=["unused-test-double"], max_competitors=0)
        write_json(config_path, config)
        models = FixtureModels(); state = Engine(business, config, adapter=models).run()
        assert state["status"] == "awaiting_approval"
        assert (business / "delivery/siteground-static.zip").is_file()
        report = read_json(business / "qa/cycle-0.json")
        assert report["browser"]["passed"] and len(report["browser"]["screenshots"]) == 3
        calls = state["calls"]
        # CLI completed-run verification must return before trying the nonexistent wrapper.
        cli("run", "--project", str(business), cwd=host)
        assert read_json(business / "state.json")["calls"] == calls
        assert not (business / ".workflow.lock").exists()
        print(json.dumps({"status": "pass", "package": str(package), "host_instructions_preserved": True,
                          "real_chromium": findings["chromium"], "model_calls": 0,
                          "model_and_visual_results": "explicit test doubles", "installed_full_pipeline": True}, indent=2))


if __name__ == "__main__":
    main()
