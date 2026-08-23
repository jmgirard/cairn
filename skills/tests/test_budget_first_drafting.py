"""Guards for the archive-summary template and its review wiring (M99;
M146 pruned the retired drafting-budget pins).

THE ARCHIVE TEMPLATE MUST STAY COMMENT-FREE: a house-style comment block
would spend a fifth of a 25-line cap, and a template whose scaffolding must
be deleted by hand is one forgotten deletion away from doing exactly that.

Run: python3 -m unittest discover -s skills/tests -k budget_first
"""

import pathlib
import re
import sys
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent.parent
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

import cairn_scripts as cs  # noqa: E402  (after sys.path shim)

TEMPLATE = REPO / "skills/shared/templates/milestone.md"
ARCHIVE_TEMPLATE = REPO / "skills/shared/templates/archive-summary.md"
PLAN = REPO / "skills/milestone-plan/SKILL.md"
REVIEW = REPO / "skills/milestone-review/SKILL.md"


def read(p):
    return p.read_text(encoding="utf-8")


def flat(text):
    """Whitespace-normalized text, for presence checks over prose that
    legitimately re-wraps. Normalizing is what lets the assertions below pin
    a rule together with the predicate that carries its meaning, instead of
    stopping at the line break in front of it."""
    return re.sub(r"\s+", " ", text)


def fenced_blocks(text):
    return re.findall(r"```(.*?)```", text, flags=re.DOTALL)


class TestArchiveSummaryTemplate(unittest.TestCase):
    def setUp(self):
        self.text = read(ARCHIVE_TEMPLATE)

    def test_it_exists_and_carries_the_canonical_section_set_in_order(self):
        labels = re.findall(r"^\*\*([A-Za-z ]+):\*\*", self.text, flags=re.M)
        self.assertEqual(labels, ["Status", "Goal", "Outcome", "Decisions", "Review"])

    def test_it_is_comment_free(self):
        """The M99 gate's reason: a comment block would cost a fifth of the
        budget, and one forgotten deletion puts it in the artifact."""
        self.assertNotIn("<!--", self.text)

    def test_the_skeleton_fits_inside_the_budget_it_teaches(self):
        n = len(self.text.splitlines())
        self.assertLessEqual(
            n,
            cs.ARCHIVE_CAP,
            "the archive template must itself fit the cap it is a template for",
        )

    def test_it_routes_cross_cutting_decisions_out_rather_than_restating_them(self):
        self.assertIn("promoted to DECISIONS.md", flat(self.text))
        self.assertIn("never restated here", flat(self.text))


class TestDraftingStepsHandOverTheCounter(unittest.TestCase):
    """D-048: a command the user runs gets a fence, not inline backticks."""


    def test_review_names_the_archive_template_as_the_source(self):
        text = read(REVIEW)
        self.assertIn("templates/archive-summary.md", text)
        self.assertIn("comment-free skeleton", flat(text))

    def test_review_step_9_still_disposes_of_the_live_milestone_file(self):
        """M99 review F4. Authoring the summary from a template made this an
        explicit step: when the summary was produced by compressing the file in
        place, the move removed the live copy implicitly. The rewrite dropped
        it, so following step 9 literally orphaned the milestone file."""
        text = flat(read(REVIEW))
        self.assertIn(
            "**deleting the live `cairn/milestones/M<NNN>-<slug>.md`**", text
        )
        self.assertIn("summary REPLACES the milestone file", text)


if __name__ == "__main__":
    unittest.main()
