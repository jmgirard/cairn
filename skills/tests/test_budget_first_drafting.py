"""Guards for M99's budget-first drafting wiring.

Three surfaces, three failure modes.

1. THE MILESTONE TEMPLATE'S BUDGET BLOCK IS SELF-REFERENTIAL. It states the
   preamble length of the very file it sits in, so editing the block changes
   the number the block asserts. That is a fixed point, and it drifted twice
   while being authored. The guard here re-derives every figure from the
   template on disk rather than pinning the digits, so an edit that moves the
   preamble reddens until the arithmetic is restored — a pinned-digit guard
   would instead have to be hand-updated and would silently bless a wrong sum.
2. THE ARCHIVE TEMPLATE MUST STAY COMMENT-FREE. Its whole reason for existing
   in this shape (M99 gate) is that a house-style comment block would spend a
   fifth of a 25-line budget, and a template whose scaffolding must be deleted
   by hand is one forgotten deletion away from doing exactly that.
3. THE TWO DRAFTING STEPS MUST HAND OVER A RUNNABLE COMMAND. D-048: a command
   the user is expected to run gets its own fenced block, because a fence
   renders a copy button and inline backticks do not. Asserted as a fence
   containing the command, never as the command's mere presence.

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
COUNTER = "scripts/cairn_budget.py"


def read(p):
    return p.read_text(encoding="utf-8")


def flat(text):
    """Whitespace-normalized text, for presence checks over prose that
    legitimately re-wraps (guard-doctrine "Fix the wrap, never the assert" —
    which scopes the one-line demand to mutation blocks and label→rule
    pairings, and permits normalizing here). Normalizing is what lets the
    assertions below pin a rule together with the predicate that carries its
    meaning, instead of stopping at the line break in front of it."""
    return re.sub(r"\s+", " ", text)


def fenced_blocks(text):
    return re.findall(r"```(.*?)```", text, flags=re.DOTALL)


class TestMilestoneTemplateBudgets(unittest.TestCase):
    """The budget block, checked against the template it describes."""

    def setUp(self):
        self.text = read(TEMPLATE)

    def test_the_block_states_a_budget_for_every_plan_owned_section(self):
        for section in ("Goal", "Scope", "AC", "Coverage", "Tasks"):
            self.assertRegex(
                self.text,
                rf"{section} \d+",
                f"no drafting budget stated for {section}",
            )

    def test_the_stated_preamble_matches_the_templates_actual_preamble(self):
        """The self-referential figure. Re-derived, never pinned."""
        body = cs.milestone_body_line_count(str(TEMPLATE))
        sections = cs.milestone_section_line_counts(str(TEMPLATE))
        actual = body - sum(n for _, n in sections)
        stated = int(re.search(r"this (\d+)-line preamble", self.text).group(1))
        self.assertEqual(
            stated,
            actual,
            "the budget block states a preamble length the template no longer "
            "has; re-measure and restate (it describes the file it sits in)",
        )

    def test_the_stated_total_is_the_sum_of_the_stated_parts(self):
        parts = [
            int(re.search(rf"{s} (\d+)", self.text).group(1))
            for s in ("Goal", "Scope", "AC", "Coverage", "Tasks")
        ]
        preamble = int(re.search(r"this (\d+)-line preamble", self.text).group(1))
        reserve = int(re.search(r"≥(\d+) RESERVED", self.text).group(1))
        total, permitted = map(
            int, re.search(r"(\d+) of (\d+) permitted", self.text).groups()
        )
        self.assertEqual(sum(parts), 97, "section budgets no longer sum to 97")
        self.assertEqual(total, sum(parts) + preamble + reserve)
        self.assertEqual(permitted, cs.MILESTONE_CAP - 1, "permitted must track the cap")

    def test_the_stated_spare_is_the_gap_to_the_cap(self):
        total, permitted = map(
            int, re.search(r"(\d+) of (\d+) permitted", self.text).groups()
        )
        spare = int(re.search(r"(\d+) spare", self.text).group(1))
        self.assertEqual(spare, permitted - total)
        self.assertGreater(spare, 0, "the budget must leave the cap some room")

    def test_the_decisions_reserve_is_named_as_a_reserve_not_a_budget(self):
        """`## Decisions` is implement/review-owned and grows after plan time,
        so plan must be told to spend none of it. A guard on the word alone
        would pass if the block said 'Decisions 21' — a budget, not a reserve."""
        self.assertIn("RESERVED for ## Decisions", flat(self.text))
        self.assertIn("so plan spends none of it", flat(self.text))

    def test_the_budgets_are_marked_guidance_rather_than_a_gate(self):
        """M99 Scope forbids a second cap. If this block ever reads as
        enforcement, the split-budget shape D-030 declined is back. Pinned with
        the predicate attached — 'guidance, not a gate' alone would survive the
        sentence naming a different, stricter thing as the check that fails."""
        self.assertIn(
            "guidance, not a gate; the only size check that can fail is "
            "cairn_validate's <150 over the plan-owned body",
            flat(self.text),
        )


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

    def test_plan_step_4_fences_the_counter_command(self):
        blocks = fenced_blocks(read(PLAN))
        self.assertTrue(
            any(COUNTER in b for b in blocks),
            f"{COUNTER} is not handed over in a fenced block in /milestone-plan",
        )

    def test_review_step_9_fences_the_counter_command(self):
        blocks = fenced_blocks(read(REVIEW))
        self.assertTrue(
            any(COUNTER in b for b in blocks),
            f"{COUNTER} is not handed over in a fenced block in /milestone-review",
        )

    def test_plan_tells_the_author_to_count_while_drafting_not_at_the_gate(self):
        text = read(PLAN)
        self.assertIn("Draft against the budget, not against the gate", flat(text))
        self.assertIn("count while writing", flat(text))

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
            "**deleting the live `cairn/milestones/M<NN>-<slug>.md`**", text
        )
        self.assertIn("summary REPLACES the milestone file", text)

    def test_the_archive_allocation_matches_the_templates_actual_fixed_lines(self):
        """M99 review F3. The stated allocation and the skeleton it budgets are
        two records of one number, so they are compared rather than both
        trusted — the work log's first pass said 5 fixed lines when the skeleton
        has 7, and nothing caught it. Derived from the template on disk."""
        skeleton = read(ARCHIVE_TEMPLATE).splitlines()
        blanks = sum(1 for line in skeleton if not line.strip())
        labelled = len(re.findall(r"^\*\*[A-Za-z ]+:\*\*", read(ARCHIVE_TEMPLATE), re.M))
        title = 1
        fixed = title + blanks + 1  # +1 for the Status line, itself a fixed line
        stated = int(re.search(r"over the (\d+) fixed lines", read(REVIEW)).group(1))
        self.assertEqual(
            stated,
            fixed,
            "the stated fixed-line count disagrees with the archive template",
        )
        parts = [
            int(n)
            for n in re.findall(
                r"(?:Goal|Outcome|Decisions|Review) (\d+)",
                re.search(r"Goal \d+ · .*?Review \d+", read(REVIEW)).group(0),
            )
        ]
        self.assertEqual(len(parts), labelled - 1, "one budget per non-Status label")
        self.assertEqual(
            sum(parts) + fixed, 22, "the allocation must sum to the stated 22"
        )
        self.assertLess(sum(parts) + fixed, cs.ARCHIVE_CAP)

    def test_review_states_the_archive_allocation_and_its_censoring_evidence(self):
        """The allocation is set BELOW the measured median on purpose: the
        distribution is censored at the cap, so its percentiles measure the
        ceiling. A guard on the numbers alone would survive deleting the
        reasoning that makes them defensible."""
        text = read(REVIEW)
        self.assertIn("Goal 2 · Outcome 7 · Decisions 3 · Review 3", flat(text))
        self.assertIn("55 sit at *exactly* 25", flat(text))
        self.assertIn("a distribution censored at the cap", flat(text))


class TestCounterIsAdvertisedWhereItIsDocumented(unittest.TestCase):
    def test_the_design_inventory_names_the_counter(self):
        text = read(REPO / "cairn/DESIGN.md")
        self.assertIn("cairn_budget", text)


if __name__ == "__main__":
    unittest.main()
