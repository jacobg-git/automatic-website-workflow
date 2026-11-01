"""Build-time only: copy canonical repository assets into wheels (no source duplication)."""
from pathlib import Path

from setuptools.command.build_py import build_py


class BuildAssets(build_py):
    def run(self):
        super().run()
        root = Path(__file__).resolve().parent.parent
        destination = Path(self.build_lib) / "website_workflow" / "_assets"
        sources = [root / "workflow.config.json", *sorted((root / "roles").glob("*/AGENTS.md")),
                   *sorted((root / "examples").glob("*.json"))]
        for source in sources:
            relative = source.relative_to(root)
            target = destination / relative
            self.mkpath(str(target.parent))
            self.copy_file(str(source), str(target))
