"""Prose guard: the opt-in Copilot review round (M231).

`skills/shared/copilot-review.md` states the round once, and `/hotfix` and
`/milestone-review` cite it. With the round on, owner mode opens the PR
before the approval chip or the merge question (D-152). With the round off,
the post-approval push-and-open stays as the off arm (D-138). This file
pins the two skills' citations of the module (M231 AC1) and both arms in
each skill (M231 AC3).

Clauses run across wrapped lines, so targets are read with whitespace
collapsed (the M171 lesson). Hand-run only (M144, D-109):

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
MODULE = "skills/shared/copilot-review.md"


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def flat(text):
    return re.sub(r"\s+", " ", text)


def section(text, start, end):
    """The slice of `text` between the first `start` and the next `end`.
    Both anchors must be present, so a renamed heading fails loudly rather
    than slicing to the end of the file (the M182 lesson)."""
    head, sep, rest = text.partition(start)
    if not sep:
        raise AssertionError(f"start anchor missing: {start!r}")
    body, sep, _ = rest.partition(end)
    if not sep:
        raise AssertionError(f"end anchor missing: {end!r}")
    return body


class TestModuleCitations(unittest.TestCase):
    """AC1: each skill's round arm cites the module. The arm sentence is
    pinned, not the bare path, because the path recurs in each skill."""

    def test_review_round_arm_cites_the_module(self):
        self.assertIn(
            f"the round on per `{MODULE}` §1; D-152). After step 5's",
            flat(read("milestone-review", "SKILL.md")),
        )

    def test_hotfix_round_arm_cites_the_module(self):
        self.assertIn(
            f"the round on per `{MODULE}` §1; D-152). Before the approval",
            flat(read("hotfix", "SKILL.md")),
        )


class TestReviewArms(unittest.TestCase):
    """AC3: `/milestone-review` opens the PR at step 6 with the round on,
    and keeps step 8's post-approval open as the off arm."""

    def setUp(self):
        self.text = flat(read("milestone-review", "SKILL.md"))

    def test_round_arm_sits_in_step_six_before_the_merge_question(self):
        step6 = section(self.text, "6. Checkpoint commit on the branch",
                        "7. **The merge question.**")
        self.assertIn("**Copilot round arm** (owner mode, the round on", step6)
        self.assertIn("push the branch and open the PR", step6)
        self.assertIn("asking for Balanced", step6)

    def test_off_arm_keeps_the_post_approval_open(self):
        step8 = section(self.text, "8. **On approval — and only then:**",
                        "**Companion arm")
        self.assertIn("push the branch and open the PR", step8)
        self.assertIn("skipped when the header already names an open PR",
                      step8)


class TestHotfixArms(unittest.TestCase):
    """AC3: `/hotfix` opens the PR before its approval chip with the round
    on, and keeps the post-approval open as the off arm."""

    def setUp(self):
        self.step = flat(section(read("hotfix", "SKILL.md"),
                                 "6. **Approval gate:**",
                                 "7. If the fix revealed"))

    def test_round_arm_runs_before_the_gate(self):
        arm = section(self.step, "**Copilot round arm**", "**The gate:**")
        self.assertIn("Before the approval gate below, push and open the PR",
                      arm)
        self.assertIn("asking for Lite", arm)

    def test_off_arm_keeps_the_post_approval_open(self):
        gate = self.step.split("**The gate:**", 1)[1]
        self.assertIn("On approval of an authored fix, push and open the PR",
                      gate)


if __name__ == "__main__":
    unittest.main()
