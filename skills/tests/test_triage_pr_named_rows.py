"""Regression guard: triage guards a PR-named row's title on Amend, merge, and retitle (M298).

Pins `/cairn-triage`'s rules for a candidate row that an open PR's
`Candidate row:` line names: the amend loop names the PR when the user
changes such a row, and marks a row set at Amend after a failed or capped
open-PR read (AC1, AC2); a `merge` survivor's lineage clause keeps the
survivor's short title (AC3); a `retitle` leaves a mention inside a
PR-named row's own short title (AC4). Each sentence is its own subtest, so
a removed sentence fails alone. Text is whitespace-collapsed on read
(M171), so a phrase may wrap across lines.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def flat(path):
    return re.sub(r"\s+", " ", path.read_text())


def section(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


class TestTriagePrNamedRows(unittest.TestCase):
    def setUp(self):
        self.triage = flat(SKILLS / "cairn-triage" / "SKILL.md")

    def assertPhrases(self, phrases, text):
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_amend_names_the_pr_of_a_changed_row(self):
        # AC1: a title-changing disposition set at Amend on a PR-named row
        # names the row and its PRs in the next chip, on every Amend, and
        # on each later chip while the change stands (review return 1).
        loop = section(self.triage, "**The amend loop.**",
                       "Whatever the answer, **every item not accepted")
        self.assertPhrases((
            "On a PR-named row, the user can set a disposition that removes "
            "the row or changes its short title.",
            "Those are `drop`, `merge` as the absorbed row, `split`, "
            "`route`, `retitle`, and a `compress` that rewrites the title.",
            "A `compress` on a PR-named row keeps its short title, unless "
            "the user's *Amend* says to rewrite it.",
            "The chip posed after that *Amend* names the row and each "
            "naming PR's number in its question text.",
            "It also says that the change breaks that PR's match of the row.",
            "A second or later *Amend*, which shows no table, follows the "
            "same rule.",
            "Each later chip names the row and its PRs again while that "
            "change stands.",
        ), loop)
        option = section(self.triage, "2. **Amend**", "3. **Apply nothing**")
        self.assertPhrases((
            "The user can also amend a PR-named row to remove it or change "
            "its short title.",
            "The next chip then names the PR (the amend loop below).",
        ), option)
        keep = section(self.triage,
                       "As that rule also says, a PR-named row is `keep`",
                       "**Started tokens → a token change.**")
        self.assertPhrases((
            "The user can still change it at *Amend* (step 3).",
        ), keep)

    def test_amend_marks_rows_after_a_failed_or_capped_read(self):
        # AC2: a disposition set at Amend after a failed or capped open-PR
        # read is marked as a proposed one is.
        loop = section(self.triage, "**The amend loop.**",
                       "Whatever the answer, **every item not accepted")
        self.assertPhrases((
            "After a session-start open-PR read that failed or returned 100 "
            "PRs, a non-`keep` disposition set at *Amend* is marked as a "
            "proposed one is.",
            "On the first *Amend*, its table reason carries the same "
            "not-checked mark.",
            "On every *Amend*, the chip's question text names that row as "
            "not checked.",
        ), loop)

    def test_merge_lineage_clause_keeps_the_survivor_title(self):
        # AC3: the clause goes first, at the row's end where the title runs
        # past the started token, opens with ` — ` where the survivor has
        # no title end before it, and holds no `: ` (review return 1).
        apply = section(self.triage, "4. **Apply.**", "5. **Record.**")
        self.assertPhrases((
            "merge survivor's lineage clause, and then any trigger it takes "
            "from the absorbed row, go before the row's first started token.",
            "They go at the row's end instead in three cases: the row has "
            "no started token, it has no text before that token, or its "
            "first `: ` comes after that token.",
            "Where the survivor's text holds neither `: ` nor ` — ` before "
            "that place, the lineage clause opens with ` — `.",
            "The lineage clause, and any trigger it takes from the absorbed "
            "row, hold no `: `, each one written as `; `.",
            "So the survivor's short title stays as it was, for every "
            "survivor, a PR-named row and a row with a started token "
            "included.",
        ), apply)

    def test_retitle_leaves_a_mention_in_a_pr_named_title(self):
        # AC4: the table row, the Title class's search, the step-3 table,
        # and step 4's rewrite each state the exception.
        row = section(self.triage, "| `retitle` | A candidate row only.",
                      "A row carrying a live started token, or missing one")
        self.assertPhrases((
            "A double-quoted mention of the old title that sits inside a "
            "PR-named row's own short title is not rewritten.",
            "The table lists it as left, with each naming PR's number, as "
            "it lists an ambiguous mention.",
            "That short title is the one session start read, whatever the "
            "row's own disposition.",
        ), row)
        title = section(self.triage, "**Title → `retitle`.**",
                        "A finding-absorbing row")
        self.assertPhrases((
            "A mention found inside a PR-named row's own short title is "
            "listed as left, with each naming PR's number.",
        ), title)
        keep = section(self.triage,
                       "As that rule also says, a PR-named row is `keep`",
                       "**Started tokens → a token change.**")
        self.assertPhrases((
            "A `retitle`'s reason also says that the mentions it rewrites "
            "were not checked.",
        ), keep)
        table = section(self.triage, "**The table**", "**The chip**")
        self.assertPhrases((
            "It also names each mention it leaves inside a PR-named row's "
            "short title, with each naming PR's number.",
        ), table)
        apply = section(self.triage, "4. **Apply.**", "5. **Record.**")
        self.assertPhrases((
            "and none in an item being dropped, nor one inside a PR-named "
            "row's own short title as session start read it;",
        ), apply)


if __name__ == "__main__":
    unittest.main()
