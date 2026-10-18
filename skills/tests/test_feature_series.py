"""Regression guard: the M274 feature series rule.

Locks the rulebook paragraph in `tracking-rules.md` (AC1), the plan's step 4
bullet (AC2), the four profiles' changelog gate lines (AC3), review's guest
PR sentence (AC4), and the release walk's half-merged series list (AC5).

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23); phrases are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text().lower()


class TestRulebookParagraph(unittest.TestCase):
    def section(self):
        text = read("shared", "tracking-rules.md")
        start = text.index("## sizing and the work tiers")
        return text[start : text.index("work that isn't a milestone", start)]

    def test_defines_the_series(self):
        self.assertIn(
            "**feature series.** a feature series is two or more milestones that one plan splits from one user-facing feature or",
            self.section(),
        )

    def test_earlier_parts_stay_hidden(self):
        self.assertIn("adding no export, user doc, or changelog entry.", self.section())

    def test_out_item_names_the_last(self):
        self.assertIn(
            "(b) each milestone but the last carries an `out:` item naming the last milestone as where the feature's new",
            self.section(),
        )

    def test_later_parts_edit_the_one_entry(self):
        self.assertIn(
            "and each later milestone of the series edits that entry instead of adding one.",
            self.section(),
        )

    def test_guest_stack_limit(self):
        self.assertIn(
            "(d) in guest mode a later part can build on at most one open earlier part (d-173),",
            self.section(),
        )

    def test_work_log_line(self):
        self.assertIn(
            "the plan writes a `feature series: m<a> -> m<b>[ -> …]` work-log line in each milestone of the series.",
            self.section(),
        )

    def test_earlier_parts_obligation(self):
        self.assertIn(
            "fix. (a) each milestone of the series but the last keeps its new behavior out of users' reach where it can,",
            self.section(),
        )

    def test_hidden_part_can_be_a_layer(self):
        self.assertIn(
            "such a part can be an internal layer rather than a vertical slice: it ships tested code that no user can reach yet.",
            self.section(),
        )

    def test_visible_earlier_part_owns_the_entry(self):
        self.assertIn(
            "(c) when a milestone before the last must change user-visible behavior, its changelog entry is the feature's one entry,",
            self.section(),
        )

    def test_guest_without_push_remote_waits(self):
        self.assertIn(
            "without `# push remote: base` a guest part builds on no open part, so every later part waits on those merges.",
            self.section(),
        )


class TestPlanBullet(unittest.TestCase):
    def test_step_four_writes_the_series(self):
        text = read("milestone-plan", "SKILL.md")
        step = text[text.index("4. **solidify autonomously**") : text.index("5. **remainder ledger")]
        self.assertIn("- **feature series.** when a split divides one user-facing feature or", step)
        self.assertIn("work-log line `feature series: m<a> -> m<b>[ -> …]` in each milestone", step)
        self.assertIn("users' reach where they can, each part but the last carries the `out:`", step)
        self.assertIn("item naming the last, every part is a milestone file (never a", step)


class TestProfileGates(unittest.TestCase):
    PROFILES = ("python", "r-package", "claude-plugin", "docker-image")

    def test_membership_and_no_entry_yet(self):
        for name in self.PROFILES:
            with self.subTest(profile=name):
                self.assertIn(
                    "this holds where the series already has an entry. a milestone is in a series when its work log carries a `feature series:` line.",
                    read("shared", "profiles", name + ".md"),
                )

    def test_series_edit_meets_the_gate(self):
        for name in self.PROFILES:
            with self.subTest(profile=name):
                self.assertIn(
                    "a milestone of a feature series (tracking-rules \"feature series\") meets this with an edit to the series' existing entry.",
                    read("shared", "profiles", name + ".md"),
                )

    def test_hidden_part_needs_no_entry(self):
        for name in self.PROFILES:
            with self.subTest(profile=name):
                self.assertIn(
                    "a milestone before the series' last with no user-visible change needs no entry.",
                    read("shared", "profiles", name + ".md"),
                )


class TestReviewGuestSentence(unittest.TestCase):
    def text(self):
        return read("milestone-review", "SKILL.md")

    def test_sentence_has_no_cairn_vocabulary(self):
        self.assertIn(
            "when the milestone's work log carries a `feature series:` line",
            self.text(),
        )
        self.assertIn(
            "(tracking-rules \"feature series\"), the body adds one plain sentence with no cairn vocabulary.",
            self.text(),
        )

    def test_earlier_part_sentence(self):
        self.assertIn(
            "the sentence says the change is one part of a series whose user-facing part comes in a later pull request.",
            self.text(),
        )
        self.assertIn("under rule (c) it says the rest of the user-facing part comes later.", self.text())

    def test_last_part_names_earlier_prs(self):
        self.assertIn(
            "for the last, it says the change completes the series and names by number the merged pull request of each earlier milestone that is `done`.",
            self.text(),
        )
        self.assertIn(
            "read each number from its live milestone file's `branch/pr` header or, for an archived milestone, from its archive summary's status line.",
            self.text(),
        )

    def test_last_part_leaves_out_dropped_parts(self):
        # M275: a part dropped before its PR opened has no number to name.
        self.assertIn("it leaves out each `dropped` earlier milestone,", self.text())


class TestHotfixSeriesEntry(unittest.TestCase):
    # M275: a hotfix to unreleased series behavior edits the series' one entry.
    def text(self):
        return read("hotfix", "SKILL.md")

    def step_five(self):
        text = self.text()
        start = text.index("5. add a changelog entry")
        return text[start : text.index("6. **approval gate:**", start)]

    def reentry_clause(self):
        text = self.text()
        start = text.index("- *changelog:* when the profile's `changelog` slot declares a file and")
        return text[start : text.index("- *owed items land through the pr path only.*", start)]

    def test_step_five_adds_no_second_entry(self):
        self.assertIn(
            "when the bug is in behavior that a feature series' entry under the development version describes, the hotfix adds no new entry.",
            self.step_five(),
        )
        self.assertIn("it edits that entry only where the fix changes what the entry says.", self.step_five())

    def test_step_five_finds_the_series(self):
        self.assertIn(
            "to find the series, read each `feature series:` work-log line in the live milestone files and each such line in the archive summaries.",
            self.step_five(),
        )

    def test_reentry_owes_no_second_entry(self):
        self.assertIn(
            "a bug in behavior that a feature series' entry under the development version describes owes no new entry.",
            self.reentry_clause(),
        )
        self.assertIn(
            "it owes an edit to that entry only where the fix changes what the entry says (step 5).",
            self.reentry_clause(),
        )


class TestReleaseList(unittest.TestCase):
    def step_one(self):
        text = read("cairn-release", "SKILL.md")
        return text[text.index("1. **version decision**") : text.index("2. **changelog consolidation**")]

    def test_lists_half_merged_series(self):
        self.assertIn("**half-merged feature series.** before the question, list each feature", self.step_one())
        self.assertIn("in a milestone file under `cairn/milestones/` (not `archive/`) where the", self.step_one())
        self.assertIn("line names at least one milestone whose status is `done`.", self.step_one())

    def test_status_falls_back_to_the_archive_summary(self):
        # M275: a pruned `done` row must not hide a half-merged series.
        self.assertIn("a named milestone's status is the status in its roadmap row.", self.step_one())
        self.assertIn(
            "for a milestone with no roadmap row, it is the status on the status line of its archive summary under `cairn/milestones/archive/`.",
            self.step_one(),
        )

    def test_status_with_no_source_is_unknown(self):
        self.assertIn(
            "a named milestone with neither a roadmap row nor an archive summary has an unknown status.",
            self.step_one(),
        )

    def test_question_names_them(self):
        self.assertIn(
            "the version-decision question names each listed series and its milestones that are not `done`.",
            self.step_one(),
        )
        self.assertIn(
            "it gives each such milestone's status, so a `dropped` part reads as dropped and an unknown part reads as unknown.",
            self.step_one(),
        )


if __name__ == "__main__":
    unittest.main()
