"""Regression guard: phase headers are H1 (unit of work) / H2 (phase).

Skills are prose, so this locks the convention M11 shifted (superseding
D-010): the unit-of-work header is `#` and the phase header is `##`, so both
land in Claude Desktop's table of contents (it indexes only H1/H2). A wording
drift back to the old `## Milestone` / `### Plan` levels fails here.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

# Every skill and the one-line `Phase header:` directive it carries.
SKILLS_WITH_PHASE_HEADER = [
    "milestone-plan",
    "milestone-implement",
    "milestone-review",
    "milestone-brief",
    "hotfix",
    "cairn-init",
    "cairn-release",
    "milestone",
    "design-interview",
]

# Old-form phase levels that must never reappear as a directive.
FORBIDDEN_PHASE_LEVELS = ["### Plan", "### Implement", "### Review",
                          "### <step>", "### Scaffold", "### Repair",
                          "### Draft", "### Gate", "### Ingest",
                          "### Snapshot", "### Audit", "### Route",
                          "### Migration"]


def read(*parts):
    return (SKILLS.joinpath(*parts)).read_text()


def phase_header_line(text):
    for line in text.splitlines():
        if line.strip().startswith("Phase header:"):
            return line
    raise AssertionError("no `Phase header:` line found")


class TestPhaseHeaderLevels(unittest.TestCase):
    def test_each_skill_phase_header_is_h1_unit_h2_phase(self):
        for skill in SKILLS_WITH_PHASE_HEADER:
            line = phase_header_line(read(skill, "SKILL.md"))
            unit, arrow, phase = line.partition("→")
            with self.subTest(skill=skill):
                self.assertTrue(arrow, "phase-header directive lacks `→`")
                # Unit of work is H1 (`# Name`), never H2.
                self.assertIn("`# ", unit)
                self.assertNotIn("`## ", unit)
                # Phase is H2 (`## Name`): present, and neither over-shifted
                # to H1 nor left at the old H3.
                self.assertIn("`## ", phase)
                self.assertNotIn("`# ", phase)
                self.assertNotIn("###", phase)

    def test_rulebook_declares_h1_unit_h2_phase(self):
        text = read("shared", "tracking-rules.md")
        self.assertIn("A `#` names the unit of work", text)
        self.assertIn("`# Milestone <NN>: <title>`", text)
        self.assertIn("`## Plan`", text)

    def test_rulebook_drops_old_h2_h3_forms(self):
        text = read("shared", "tracking-rules.md")
        self.assertNotIn("`## Milestone <NN>: <title>`", text)
        for forbidden in FORBIDDEN_PHASE_LEVELS:
            # Leading backtick only — the trailing token varies (e.g.
            # `### Migration §n`), so a closing backtick would miss it.
            self.assertNotIn("`%s" % forbidden, text)


if __name__ == "__main__":
    unittest.main()
