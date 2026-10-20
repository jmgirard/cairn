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
        # names the row and its PRs in the next chip, on every Amend.
        loop = section(self.triage, "**The amend loop.**",
                       "Whatever the answer, **every item not accepted")
        self.assertPhrases((
            "On a PR-named row, the user can set a disposition that removes "
            "the row or changes its short title.",
            "Those are `drop`, `merge` as the absorbed row, `split`, "
            "`route`, `retitle`, and a `compress` that rewrites the title.",
            "The chip posed after that *Amend* names the row and each "
            "naming PR's number in its question text.",
            "It also says that the change breaks that PR's match of the row.",
            "A second or later *Amend*, which shows no table, follows the "
            "same rule.",
        ), loop)
        option = section(self.triage, "2. **Amend**", "3. **Apply nothing**")
        self.assertPhrases((
            "The user can also amend a PR-named row away from `keep`, and "
            "the next chip names the PR (the amend loop below).",
        ), option)

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
        # AC3: the clause opens with ` — ` where the survivor has no title
        # end before it, and it holds no `: `.
        apply = section(self.triage, "4. **Apply.**", "5. **Record.**")
        self.assertPhrases((
            "Where the survivor's text holds neither `: ` nor ` — ` before "
            "that place, the clause opens with ` — `.",
            "The lineage clause, and any trigger it takes from the absorbed "
            "row, hold no `: `, each one written as `; `.",
            "So the survivor's short title stays as it was, a PR-named row "
            "and a row with a started token included.",
            "This holds for every survivor with no `: ` after its first "
            "started token.",
        ), apply)

    def test_retitle_leaves_a_mention_in_a_pr_named_title(self):
        # AC4: the table row, the Title class's search, the step-3 table,
        # and step 4's rewrite each state the exception.
        row = section(self.triage, "| `retitle` | A candidate row only.",
                      "A row carrying a live started token, or missing one")
        self.assertPhrases((
            "A double-quoted mention of the old title that sits inside a "
            "PR-named row's own short title is not rewritten.",
            "The table lists it as left, with the PR's number, as it lists "
            "an ambiguous mention.",
        ), row)
        title = section(self.triage, "**Title → `retitle`.**",
                        "A finding-absorbing row")
        self.assertPhrases((
            "A mention found inside a PR-named row's own short title is "
            "listed as left, with the PR's number.",
        ), title)
        table = section(self.triage, "**The table**", "**The chip**")
        self.assertPhrases((
            "It also names each mention it leaves inside a PR-named row's "
            "short title, with the PR's number.",
        ), table)
        apply = section(self.triage, "4. **Apply.**", "5. **Record.**")
        self.assertPhrases((
            "and none in an item being dropped, nor one inside a PR-named "
            "row's own short title;",
        ), apply)


if __name__ == "__main__":
    unittest.main()
