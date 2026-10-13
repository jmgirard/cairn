"""Regression guard: a hotfix graduates the candidate row it fixes (M249).

Pins the `/hotfix` step 1 match clause, the two chips that name a matched
row, the step 7 remove-or-narrow clause with its one docs-only commit, the
guest arm, and the records-hygiene and README sentences. Text is
whitespace-collapsed on read (M171), so a phrase may wrap across lines.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
REPO = SKILLS.parent


def flat(path):
    return re.sub(r"\s+", " ", path.read_text())


def section(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


class TestHotfixCandidateGraduation(unittest.TestCase):
    def setUp(self):
        self.hotfix = flat(SKILLS / "hotfix" / "SKILL.md")
        self.step1 = section(self.hotfix, "1. **Tier check first.**",
                             "2. **Branch")
        self.step6 = section(self.hotfix, "6. **Approval gate:**",
                             "7. If the fix revealed deeper work")
        self.step7 = section(self.hotfix, "7. If the fix revealed deeper work",
                             "End with the close block")

    def test_step1_matches_rows_on_every_entry(self):
        for phrase in (
            "Step 1 also finds the candidate rows this hotfix fixes.",
            "It runs on every entry to step 1, PR-reference re-entries "
            "included, and never from memory.",
            "whose title the argument quotes, or a row that describes the "
            "bug being fixed.",
            "read the PR's title, body and `Fixes #N` line against the rows.",
            "Name each matched row's title in chat, or say that no row "
            "matched.",
            "A row's title is its text after the `- ` and any "
            "`[high]`/`[low]` token, up to the first `: `.",
            "Within a hotfix, only step 7, after a merge, removes or narrows "
            "a matched row. A search-first absorb on another path can add to "
            "the row, but it never removes or narrows it.",
        ):
            self.assertIn(phrase, self.step1)

    def test_chips_name_each_matched_row(self):
        nothing_owed = section(self.hotfix, "*Nothing owed*", "2. **Branch")
        self.assertIn(
            "In both modes the acceptance chip's question text also names "
            "each matched row's title and says whether step 7 removes the "
            "row or narrows it.",
            nothing_owed,
        )
        self.assertIn(
            "the question text also names each matched row's title and says "
            "whether the merge removes the row or narrows it to the part the "
            "fix leaves (step 7).",
            self.step6,
        )
        self.assertIn("The guest handoff chip below carries no row text.",
                      self.step6)

    def test_step7_removes_or_narrows_after_a_merge(self):
        for phrase in (
            "In owner mode, after a merge whose diff passed the hotfix bar, "
            "edit each row step 1 matched.",
            "an authored fix, an adopted PR, a re-landed PR, and the "
            "merged-PR re-entry once its post-hoc verification is accepted, "
            "or, where items were owed, once the follow-up PR merges.",
            "Delete each row that the fix covers in full.",
            "Narrow each row that the fix covers in part to the part left,",
            "The part left is that narrowing, never a second new row.",
            "with a `narrowed YYYY-MM-DD by the PR #N hotfix` note, where "
            "`#N` is the merged PR that carried the fix.",
            "On step 1's over-the-bar disposition, step 7 neither removes "
            "nor narrows a matched row.",
            "In owner mode, every ROADMAP edit step 7 makes on any path, the "
            "candidate row added above included, lands in one docs-only "
            "commit on the default branch.",
            "Run step 2's `git status` check first, then check out the "
            "default branch, bring it up to date (fetch, pull ff-only), "
            "commit, and push at once.",
            "Show each deleted, narrowed, and new row verbatim in chat",
        ):
            self.assertIn(phrase, self.step7)

    def test_guest_arm_waits_for_the_maintainers_merge(self):
        self.assertIn(
            "The handoff leaves each matched candidate row unchanged.",
            self.step6,
        )
        for phrase in (
            "*Guest arm:* the handoff leaves each matched row unchanged.",
            "When the merged-PR re-entry finds that the maintainers merged "
            "the PR, and its post-hoc verification is accepted, remove or "
            "narrow each matched row on disk with no commit, judged against "
            "the merged diff, and show each deleted and narrowed row "
            "verbatim in chat.",
            "A PR closed without a merge leaves the row.",
        ):
            self.assertIn(phrase, self.step7)

    def test_records_hygiene_and_readme_say_so(self):
        hygiene = section(flat(SKILLS / "shared" / "records-hygiene.md"),
                          "## 1. Candidate rows graduate", "## 2.")
        for phrase in (
            "the row stays through planning and implementation",
            "A hotfix graduates the same way: step 7 removes or narrows its "
            "row after merge.",
        ):
            self.assertIn(phrase, hygiene)
        readme_row = [line for line in (REPO / "README.md").read_text()
                      .splitlines()
                      if line.startswith("| Fix a reported bug quickly |")]
        self.assertEqual(len(readme_row), 1)
        self.assertIn(
            "After the merge it removes the candidate row it fixed, or "
            "narrows it to the part left.",
            readme_row[0],
        )


if __name__ == "__main__":
    unittest.main()
