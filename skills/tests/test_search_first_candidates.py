"""Regression guard: the M39 search-first candidate-creation rule.

Locks the rule text in `tracking-rules.md` (AC1/AC3) and the one-line
pointers at the two ad-hoc candidate-creation steps that run outside the
plan-time collision check (AC2): `/hotfix` step 7 and the
`/milestone-review` follow-up-candidate triage step.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23) and steers clear of `**bold**` splits
(M26); phrases are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text().lower()


def rules():
    return read("shared", "tracking-rules.md")


class TestSearchFirstCandidateRule(unittest.TestCase):
    def test_rule_present_in_tracking_rules(self):
        t = rules()
        self.assertIn("search-first candidate creation", t)
        self.assertIn("sweep existing candidates", t)
        self.assertIn("absorb into or cross-reference", t)

    def test_rule_names_all_three_sweep_targets(self):
        t = rules()
        self.assertIn("milestones/archive/", t)
        self.assertIn("decisions.md", t)
        # existing candidates is the third target
        self.assertIn("sweep existing candidates", t)


class TestSearchFirstPointers(unittest.TestCase):
    def test_hotfix_points_to_the_rule(self):
        self.assertIn(
            "search-first candidate-creation rule",
            read("hotfix", "SKILL.md"),
        )

    def test_milestone_review_points_to_the_rule(self):
        self.assertIn(
            "search-first candidate-creation rule",
            read("milestone-review", "SKILL.md"),
        )


if __name__ == "__main__":
    unittest.main()
