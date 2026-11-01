from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from website_workflow import __version__
from website_workflow.adapters import Adapter, render_agents
from website_workflow.cli import main
from website_workflow.config import default_config_path, find_workspace, load_config, resource_path, validate_intake
from website_workflow.contracts import WorkflowError
from website_workflow.installation import install_project, new_business, setup_project
from website_workflow.storage import digest, read_json, write_json


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = (Path(self.temporary.name) / "host").resolve()
        self.root.mkdir()
    def tearDown(self):
        self.temporary.cleanup()

    def test_install_preserves_host_instructions_and_is_idempotent(self):
        original = b"\xef\xbb\xbf# Existing project\r\nKeep the user's instructions.\r\n"
        (self.root / "AGENTS.md").write_bytes(original)
        (self.root / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
        report = install_project(self.root)
        self.assertEqual(report["mode"], "process-workers")
        self.assertTrue((self.root / "AGENTS.md").read_bytes().startswith(original))
        self.assertTrue((self.root / ".gitignore").read_text().startswith("node_modules/\n"))
        first = (self.root / "AGENTS.md").read_bytes()
        again = install_project(self.root)
        self.assertEqual(first, (self.root / "AGENTS.md").read_bytes())
        self.assertTrue(all(f["action"] == "unchanged" for f in again["files"]))
        self.assertEqual(first.count(b"<!-- BEGIN website-workflow -->"), 1)
        self.assertFalse((self.root / ".workflow.lock").exists())
        self.assertEqual(len(list((self.root / ".agents/agents").glob("*.md"))), 6)

    def test_crlf_transport_is_not_mistaken_for_user_edits(self):
        install_project(self.root)
        paths = [self.root / "AGENTS.md", self.root / ".agents/agents/website-builder.md", self.root / ".website-workflow/AGENT_GUIDE.md"]
        for path in paths:
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        before = {str(path): path.read_bytes() for path in paths}
        install_project(self.root)
        self.assertEqual(before, {str(path): path.read_bytes() for path in paths})

    def test_uninstalled_workspace_does_not_fall_back_to_source_repo(self):
        self.assertEqual(find_workspace(self.root), self.root)

    def test_dry_run_does_not_create_directories_or_files(self):
        target = self.root / "new-project"
        report = install_project(target, dry_run=True)
        self.assertTrue(report["dry_run"])
        self.assertFalse(target.exists())

    def test_conflicting_agent_stops_before_any_installer_writes(self):
        path = self.root / ".agents/agents/website-builder.md"
        path.parent.mkdir(parents=True)
        path.write_text("Existing unrelated agent", encoding="utf-8")
        with self.assertRaisesRegex(WorkflowError, "conflict"):
            install_project(self.root)
        self.assertEqual(path.read_text(), "Existing unrelated agent")
        self.assertFalse((self.root / ".website-workflow").exists())
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_edited_managed_file_is_not_overwritten(self):
        install_project(self.root)
        guide = self.root / ".website-workflow/AGENT_GUIDE.md"
        guide.write_text("User's custom guide", encoding="utf-8")
        before = (self.root / "AGENTS.md").read_bytes()
        with self.assertRaises(WorkflowError): install_project(self.root)
        self.assertEqual(guide.read_text(), "User's custom guide")
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), before)

    def test_custom_configuration_is_preserved_on_reinstallation(self):
        install_project(self.root)
        path = self.root / ".website-workflow/workflow.config.json"
        config = read_json(path); config["concurrency"] = 1; write_json(path, config)
        install_project(self.root)
        self.assertEqual(read_json(path)["concurrency"], 1)
        self.assertEqual(load_config(path)["task_timeout_seconds"], 600)

    def test_upgrades_replace_only_unedited_owned_files(self):
        install_project(self.root)
        guide = self.root / ".website-workflow/AGENT_GUIDE.md"
        guide.write_text("Old generated guide", encoding="utf-8")
        manifest = self.root / ".website-workflow/installation.json"
        data = read_json(manifest); data["files"][".website-workflow/AGENT_GUIDE.md"] = digest(guide.read_bytes()); write_json(manifest, data)
        install_project(self.root)
        self.assertIn("instructions for the installing/operating agent", guide.read_text(encoding="utf-8"))

    def test_host_instruction_edits_outside_owned_block_survive(self):
        install_project(self.root)
        path = self.root / "AGENTS.md"
        path.write_bytes(b"# New host policy\n" + path.read_bytes() + b"\nAdditional host policy\n")
        before = path.read_bytes(); install_project(self.root)
        self.assertEqual(path.read_bytes(), before)

    def test_edited_pointer_block_is_not_overwritten(self):
        install_project(self.root)
        path = self.root / "AGENTS.md"
        path.write_text(path.read_text().replace("## Website workflow", "## User-edited block"), encoding="utf-8")
        with self.assertRaisesRegex(WorkflowError, "instruction block was edited"):
            install_project(self.root)

    def test_active_business_lock_blocks_registration_updates(self):
        install_project(self.root)
        lock = self.root / ".website-workflow/businesses/example/.workflow.lock"
        lock.parent.mkdir(parents=True); lock.write_text("active", encoding="utf-8")
        with self.assertRaisesRegex(WorkflowError, "business run is locked"):
            install_project(self.root)

    def test_symlink_installation_target_is_rejected(self):
        outside = self.root.parent / "outside"; outside.mkdir()
        try:
            (self.root / ".agents").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Symlink creation unavailable: {exc}")
        with self.assertRaisesRegex(WorkflowError, "linked installation"):
            install_project(self.root)
        self.assertFalse(list(outside.iterdir()))

    def test_link_guard_without_os_symlink_privileges(self):
        original = Path.is_symlink
        def simulated(path):
            return path == self.root / ".agents" or original(path)
        with patch.object(Path, "is_symlink", simulated):
            with self.assertRaisesRegex(WorkflowError, "linked installation"):
                install_project(self.root)
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_windows_reparse_flags_are_rejected_on_older_python(self):
        original = Path.lstat
        def simulated(path):
            if path == self.root / ".agents":
                return type("ReparseDirectory", (), {"st_file_attributes": 0x400, "st_mode": 0o040755})()
            return original(path)
        with patch.object(Path, "lstat", simulated):
            with self.assertRaisesRegex(WorkflowError, "linked installation"):
                install_project(self.root)
        self.assertFalse((self.root / "AGENTS.md").exists())

    def test_existing_installer_temp_stops_before_other_files_change(self):
        temporary = self.root / ".website-workflow/AGENT_GUIDE.md.website-workflow-tmp"
        temporary.parent.mkdir(); temporary.write_text("Inspect this before recovery", encoding="utf-8")
        with self.assertRaisesRegex(WorkflowError, "temporary file"):
            install_project(self.root)
        self.assertFalse((self.root / "AGENTS.md").exists())
        self.assertEqual(temporary.read_text(), "Inspect this before recovery")

    def test_new_business_is_a_safe_unverified_scaffold(self):
        install_project(self.root)
        report = new_business(self.root, "Example Workshop", "Portland, Oregon")
        self.assertEqual(report["status"], "needs_verified_intake")
        intake = read_json(report["intake"])
        self.assertEqual(intake["business_name"], "Example Workshop")
        self.assertEqual(intake["verified_facts"], [])
        self.assertFalse(intake["primary_cta"]["verified"])
        with self.assertRaises(WorkflowError): validate_intake(intake)
        with self.assertRaises(WorkflowError): new_business(self.root, "Example Workshop", "Portland")
        with self.assertRaises(WorkflowError): new_business(self.root, "Other", "Portland", "../escape")

    def test_setup_dry_run_does_not_download_or_invoke_models(self):
        with patch("website_workflow.installation.subprocess.run") as run:
            report = setup_project(self.root, dry_run=True)
        run.assert_not_called()
        self.assertEqual(report["model_calls"], 0)
        self.assertFalse((self.root / ".website-workflow").exists())

    def test_setup_uses_current_python_and_no_global_permission_changes(self):
        with patch("website_workflow.installation.subprocess.run", return_value=subprocess.CompletedProcess([], 0)) as run:
            setup_project(self.root)
        args = run.call_args.args[0]
        self.assertEqual(args[1:], ["-m", "playwright", "install", "chromium"])
        self.assertNotIn("--with-deps", args)

    def test_installed_workspace_is_used_for_worker_registration_and_cwd(self):
        install_project(self.root)
        business = Path(new_business(self.root, "Sample", "Location")["project"])
        self.assertEqual(find_workspace(business), self.root)
        config = load_config(default_config_path(self.root))
        adapter = Adapter(config, workspace=find_workspace(business))
        response = {"status": "blocked", "summary": "fixture", "facts": [], "sources": [], "observations": [], "uncertainties": []}
        events = [{"event": "init", "init": {"model": config["models"]["researchers"], "agent": "website-researchers"}},
                  {"event": "result", "result": {"status": "SUCCESS", "structured_output": response, "usage": {}}}]
        work = business / "attempt"; work.mkdir()
        with patch("website_workflow.adapters.shutil.which", return_value="mock-agy"), patch.object(adapter, "_execute", return_value=events) as execute:
            result, _ = adapter.run("researchers", "fixture prompt", work, "fixture")
        self.assertEqual(result, response)
        self.assertEqual(execute.call_args.args[1], self.root)

    def test_cli_install_new_business_and_validation_have_no_inference(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["install", "--project", str(self.root)]), 0)
            self.assertEqual(main(["new-business", "--project", str(self.root), "--name", "Specific Business", "--location", "City"]), 0)
            self.assertEqual(main(["validate-intake", "--intake", str(self.root / ".website-workflow/businesses/specific-business/intake.json")]), 1)
        self.assertEqual(read_json(self.root / ".website-workflow/installation.json")["package_version"], __version__)
        self.assertTrue(resource_path("roles/builder/AGENTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
