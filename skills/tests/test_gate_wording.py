"""Regression guard: the merge-approval gate must be an AskUserQuestion chip.

Skills are prose, so this locks the invariant the /hotfix on 2026-07-11
restored: `/milestone-review` and `/hotfix` must present the *merge
authorization itself* as an AskUserQuestion chip, and must not fall back to
a prose "ask plainly for authorization" yes/no. A wording drift that
reintroduces the prose gate fails here.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return (SKILLS.joinpath(*parts)).read_text()


class TestMergeGateIsAChip(unittest.TestCase):
    def test_review_names_askuserquestion_at_merge_gate(self):
        text = read("milestone-review", "SKILL.md")
        self.assertIn("AskUserQuestion", text)
        # the specific anti-pattern this hotfix removed must not return
        self.assertNotIn("ask plainly for authorization to merge", text)

    def test_hotfix_names_askuserquestion_at_merge_gate(self):
        text = read("hotfix", "SKILL.md")
        self.assertIn("AskUserQuestion", text)

    def test_rulebook_declares_merge_gate_a_chip(self):
        text = read("shared", "tracking-rules.md")
        self.assertIn("merge-approval gate is itself an AskUserQuestion chip", text)


if __name__ == "__main__":
    unittest.main()
