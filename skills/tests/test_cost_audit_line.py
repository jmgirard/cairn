"""Prose-guard: `/milestone`'s §2 reporting lines are surfaces, not gates.

M94 ships cost measurement and deliberately ships no judgement; M101 adds
the rulebook-mass line beside it (D-057's M96 fold) under the same boundary.
The danger is drift in the judging direction: a later session reads a large
figure in the audit output and treats it as a finding to act on, or quietly
grows a threshold around it. What must survive in
`skills/milestone/SKILL.md`: the instructions to run/measure, and the
explicit no-threshold boundary on both lines.

Each assertion is a distinct block registered in the mutation harness, so
deleting any one fails here rather than passing over a rule that is gone
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

    def test_no_governing_mechanism_is_owed(self):
        # M101: D-057 closed the stock-side program, so the text must say no
        # mechanism is coming — the prior deferral ("M96's to define") named
        # an owner that no longer exists and read as a promise.
        self.assertIn("D-057 closed", self.text)
        self.assertNotIn("M96's to define", self.text)

    def test_the_subagent_gap_is_stated_where_the_number_is_read(self):
        # A partial figure read as complete is the specific misreading the
        # spawn count exists to prevent.
        self.assertIn("the store does not record", self.text)

    def test_the_audit_reports_rulebook_mass_beside_the_cost_line(self):
        # M101 (D-057's M96 fold): the rulebook line is the growth-visibility
        # surface the ratchet milestone folded down to.
        self.assertIn("report the rulebook's mass the same way", self.text)
        self.assertIn("`wc -l -m`", self.text)

    def test_the_rulebook_line_carries_its_seeded_baseline(self):
        # Growth is reported against a recorded figure, not a remembered one;
        # the seed is the M95 archive measurement.
        self.assertIn("779 lines / 53,751 chars", self.text)

    def test_the_rulebook_line_is_reporting_only_with_no_machinery(self):
        # The fold's whole point (D-057): visibility without pass machinery.
        self.assertIn("no threshold, no verdict, no pass machinery", self.text)


if __name__ == "__main__":
    unittest.main()
