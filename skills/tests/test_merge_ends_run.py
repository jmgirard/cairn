"""Guard: a merge ends the run, so the next milestone starts in a fresh context.

Hotfix (2026-10-04, D-148): `/milestone-review` step 10 invoked
`/milestone-implement` for the next milestone of the same plan through the
Skill tool, so one merge started the next milestone in the same context. The
user chose a `/clear` between milestones instead. Step 10 now ends the run
with the close block, and the plan's next milestone is its fenced command.

Phrases live on one source line each (M23) and are matched
case-insensitively. Each negative assert sits beside a positive one.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def skill(name):
    return SKILLS.joinpath(name, "SKILL.md").read_text().lower()


def rules():
    return SKILLS.joinpath("shared", "tracking-rules.md").read_text().lower()


class TestMergeEndsTheRun(unittest.TestCase):
    def test_rulebook_ends_the_run_at_the_merge(self):
        text = rules()
        self.assertIn("a merge ends the run", text)
        self.assertNotIn("after a merge, the run goes on", text)
        self.assertNotIn("crosses phase and milestone seams", text)

    def test_review_step_10_hands_over_instead_of_invoking(self):
        text = skill("milestone-review")
        self.assertIn("a merge ends the run", text)
        self.assertNotIn(
            "`/milestone-implement <next-id>` through the skill tool", text
        )
        self.assertIn("`/milestone-implement <next-id>` as the primary", text)

    def test_plan_no_longer_promises_a_run_across_milestones(self):
        text = skill("milestone-plan")
        self.assertIn("next milestone of the plan", text)
        self.assertNotIn("next milestone of the run", text)


if __name__ == "__main__":
    unittest.main()
