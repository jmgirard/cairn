"""Prose-guard: `/milestone`'s cost line is a reporting surface, not a gate.

M94 ships measurement and deliberately ships no judgement — the governing
mechanism over these numbers is M96's. The danger is drift in the other
direction: a later session reads a large cache-read figure in the audit
output and treats it as a finding to act on, or quietly grows a threshold
around it. Two things must therefore survive in `skills/milestone/SKILL.md`:
the instruction to run the script, and the explicit no-threshold boundary.

Each assertion is a distinct block registered in the mutation harness, so
deleting either one fails here rather than passing over a rule that is gone
(the M39/M40 false-coverage trap).
"""

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
MILESTONE = ROOT / "skills" / "milestone" / "SKILL.md"


class TestCostAuditLine(unittest.TestCase):
    def setUp(self):
        self.text = MILESTONE.read_text(encoding="utf-8")

    def test_the_audit_runs_the_cost_script(self):
        self.assertIn("cairn_cost.py --audit-line", self.text)

    def test_the_audit_reports_the_line_verbatim(self):
        self.assertIn("report its one line verbatim", self.text)

    def test_the_cost_line_is_boundaried_as_reporting_only(self):
        self.assertIn("a reporting surface only", self.text)

    def test_the_boundary_names_what_it_forbids(self):
        # "reporting surface" alone is a slogan; the operative words are the
        # two prohibitions, which is what a drifting session would breach.
        self.assertIn(
            "never treat a large figure as a finding to act on, and never "
            "propose a cap from",
            self.text,
        )

    def test_the_governing_mechanism_is_deferred_to_its_owner(self):
        self.assertIn("M96's to define", self.text)

    def test_the_subagent_gap_is_stated_where_the_number_is_read(self):
        # A partial figure read as complete is the specific misreading the
        # spawn count exists to prevent.
        self.assertIn("the store does not record", self.text)


if __name__ == "__main__":
    unittest.main()
