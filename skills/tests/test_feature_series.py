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
            "for the last, it says the change completes the series and names each earlier milestone's pull request by number,",
            self.text(),
        )
        self.assertIn(
            "read from its live milestone file's `branch/pr` header or, for an archived milestone, from its archive summary's status line.",
            self.text(),
        )


class TestReleaseList(unittest.TestCase):
    def step_one(self):
        text = read("cairn-release", "SKILL.md")
        return text[text.index("1. **version decision**") : text.index("2. **changelog consolidation**")]

    def test_lists_half_merged_series(self):
        self.assertIn("**half-merged feature series.** before the question, list each feature", self.step_one())
        self.assertIn("in a milestone file under `cairn/milestones/` (not `archive/`) where the", self.step_one())
        self.assertIn("line names at least one milestone whose roadmap status is `done`.", self.step_one())

    def test_question_names_them(self):
        self.assertIn(
            "the version-decision question names each listed series and its milestones that are not `done`.",
            self.step_one(),
        )
        self.assertIn("it gives each such milestone's roadmap status, so a `dropped` part reads as dropped.", self.step_one())


if __name__ == "__main__":
    unittest.main()
