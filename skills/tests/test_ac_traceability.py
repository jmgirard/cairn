"""Regression guard: M18 acceptance-criteria traceability.

Traceability is skill-text + template mechanics — nothing at runtime enforces
them — so this test locks the load-bearing pieces against silent regression:
  * the milestone template carries a plan-owned Coverage section mapping each
    criterion to the task(s) that satisfy it, positionally numbered;
  * /milestone-plan authors that map, and treats an unmapped criterion as a
    planning gap;
  * /milestone-review fences a criterion checkbox on recorded evidence and
    fails a criterion mapped to no existing task (AC fencing);
  * tracking-rules lists the Coverage section in the ownership table (owner:
    plan) and states the fencing rule in its review discipline.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def template():
    return read("shared", "templates", "milestone.md")


def plan():
    return read("milestone-plan", "SKILL.md")


def review():
    return read("milestone-review", "SKILL.md")


def rules():
    return read("shared", "tracking-rules.md")


class TestTemplateCoverageSection(unittest.TestCase):
    def test_coverage_section_exists(self):
        self.assertIn("## Coverage", template())

    def test_coverage_sits_between_criteria_and_tasks(self):
        t = template()
        self.assertLess(t.index("## Acceptance criteria"), t.index("## Coverage"))
        self.assertLess(t.index("## Coverage"), t.index("## Tasks"))

    def test_coverage_is_plan_owned(self):
        # ownership comment must name plan as the owner
        seg = template().split("## Coverage", 1)[1].split("## Tasks", 1)[0]
        self.assertIn("owner: plan", seg)

    def test_coverage_is_positional_map(self):
        # positional numbering convention + a sample criterion→task line
        seg = template().split("## Coverage", 1)[1].split("## Tasks", 1)[0]
        self.assertIn("positional", seg)
        self.assertRegex(seg, r"AC1\s*→\s*T1")


class TestPlanAuthorsCoverage(unittest.TestCase):
    def test_plan_authors_the_map(self):
        p = plan()
        self.assertIn("Coverage", p)
        self.assertRegex(p, r"AC1\s*→\s*T1")

    def test_plan_treats_unmapped_criterion_as_a_gap(self):
        p = plan()
        self.assertRegex(p, r"≥1 task")
        self.assertIn("planning gap", p)


class TestReviewFences(unittest.TestCase):
    def test_ac_fencing_named(self):
        self.assertIn("AC fencing", review())

    def test_evidence_before_checkbox(self):
        # a checkbox is ticked only against recorded evidence
        self.assertRegex(review(), r"evidence.*checkbox|no evidence.*no tick")

    def test_coverage_completeness_is_a_gate_failure(self):
        r = review()
        self.assertIn("Coverage completeness", r)
        self.assertRegex(r, r"≥1 task")
        self.assertIn("gate failure", r)


class TestRulesDiscipline(unittest.TestCase):
    def test_ownership_table_lists_coverage(self):
        r = rules()
        self.assertRegex(r, r"\|\s*Coverage.*\|\s*plan\s*\|")

    def test_review_discipline_states_fencing(self):
        r = rules()
        self.assertIn("AC fencing", r)
        self.assertRegex(r, r"no evidence.*no tick|evidence.*gates the")


if __name__ == "__main__":
    unittest.main()
