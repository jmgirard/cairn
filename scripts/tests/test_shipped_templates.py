"""Shipped-template integrity (M163 F2): every `templates/<name>.md` a skill
or shared module references must exist in skills/shared/templates/, and the
file-header templates cairn-init's scaffold mandates (LESSONS.md and
DECISIONS.md) must ship — an external adoption otherwise reconstructs those
headers from nothing, inventing a different shape per repo."""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TEMPLATES = REPO / "skills" / "shared" / "templates"


class TestShippedTemplates(unittest.TestCase):
    def referenced_template_names(self):
        pattern = re.compile(r"templates/([A-Za-z0-9_-]+\.md)")
        # Every .md under skills/ — SKILL.md files, shared modules, the
        # templates themselves (source-note references synthesis-note),
        # profiles, and per-skill references (M163 review O7).
        sources = list((REPO / "skills").rglob("*.md"))
        names = set()
        for path in sources:
            names.update(pattern.findall(path.read_text(encoding="utf-8")))
        return names

    def test_reference_sweep_is_nonempty(self):
        # The sweep's domain must not silently empty (check discrimination).
        self.assertGreater(len(self.referenced_template_names()), 3)

    def test_every_referenced_template_ships(self):
        for name in sorted(self.referenced_template_names()):
            self.assertTrue(
                (TEMPLATES / name).is_file(),
                f"skill prose references templates/{name} but it does not ship",
            )

    def test_scaffold_header_templates_ship(self):
        # Stated independently of the reference sweep: the cairn-init §1
        # scaffold creates LESSONS.md and DECISIONS.md, so their file-header
        # templates must exist under skills/shared/templates/.
        for name in ("lessons.md", "decisions.md"):
            self.assertTrue(
                (TEMPLATES / name).is_file(),
                f"templates/{name} (scaffold file-header template) missing",
            )


if __name__ == "__main__":
    unittest.main()
