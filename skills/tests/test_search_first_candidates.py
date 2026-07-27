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
        # Anchor on the rule's own contiguous sweep-list phrasing, not bare
        # `milestones/archive/` / `decisions.md` — those substrings occur
        # elsewhere in the file (file-map table, append-only rule) and would
        # pass even if the rule dropped them from its sweep list.
        t = rules()
        self.assertIn("sweep existing candidates + `milestones/archive/`", t)
        self.assertIn("`decisions.md` for overlap", t)


class TestFalsifyingPromotionConditions(unittest.TestCase):
    """M114: how a candidate's promotion condition is WORDED.

    Search-first governs whether a row exists; this governs whether the row,
    once read years later, fires at the right moment. A count-shaped condition
    ("promote if a fifth mechanism appears") is met exactly as written, so it
    pre-commits to paying for the four failures below it.
    """

    def test_rule_requires_a_falsifying_class_not_a_count(self):
        t = rules()
        self.assertIn("falsifying promotion conditions", t)
        # Spans the shipped line break, so `\s+` rather than a literal newline:
        # a byte-exact copy embeds today's wrap point and breaks on reflow.
        self.assertRegex(
            t, r"the class of evidence that\s+would falsify the chosen approach"
        )
        # The prohibition is the operative half — without it the rule reads as
        # a preference and a count still satisfies it.
        self.assertIn("never as a count of failures", t)


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
