"""Regression guard: the M274 feature series rule.

Locks the rulebook paragraph in `tracking-rules.md` (AC1), the plan's step 4
bullet (AC2), the four profiles' changelog gate lines (AC3), review's guest
PR sentence (AC4), and the release walk's half-merged series list (AC5).
M275 adds the release walk's archive-summary status fallback, the hotfix rule
that keeps a series' one entry, the last-part sentence's dropped-part rule,
the series line in both templates, and the `/milestone` snapshot's report
of half-merged series.

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
        # M275: a dropped part shipped nothing for the series to complete.
        self.assertIn("it leaves out each `dropped` earlier milestone,", self.text())

    def test_last_part_names_blocked_parts(self):
        # M275 review: an open stack base, or a part merged before hygiene.
        self.assertIn(
            "it also names the pull request of each earlier milestone that is `blocked` on the maintainers.",
            self.text(),
        )
        self.assertIn(
            "a part's status comes from its roadmap row, else from its archive summary, as `/cairn-release` step 1 states under \"half-merged feature series\".",
            self.text(),
        )


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

    def test_adopted_pr_folds_a_second_entry(self):
        self.assertIn(
            "drop a contributor's separate entry for that behavior, and edit the series' entry only where the fix changes what it says.",
            self.step_five(),
        )

    def test_released_behavior_takes_its_own_entry(self):
        self.assertIn(
            "a bug in behavior that an earlier release shipped is outside this rule and takes its own entry.",
            self.step_five(),
        )

    def test_adopted_pr_keeps_the_credit(self):
        self.assertIn(
            "keep any credit that the dropped entry gives the contributor, in the series' entry.",
            self.step_five(),
        )

    def test_reentry_removes_a_merged_second_entry(self):
        self.assertIn(
            "if the merged diff added a separate entry for that behavior, its removal is owed.",
            self.reentry_clause(),
        )

    def test_downstream_sites_carry_the_rule(self):
        self.assertIn("there (step 5's feature series rule applies), open", self.text())
        self.assertIn("series bug the edited series entry or a note that it needed no edit)", self.text())

    def test_nothing_owed_accepts_the_series_entry(self):
        self.assertIn(
            "changelog entry present (for a series bug, the series' entry already describes the fixed behavior) or the slot `none`",
            self.text(),
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


class TestSeriesNamedElsewhere(unittest.TestCase):
    # M275: the templates and the status snapshot name the series.
    def test_milestone_template_names_the_line(self):
        self.assertIn(
            "`feature series: m<a> -> m<b>[ -> …]` line (tracking-rules \"feature series\").",
            read("shared", "templates", "milestone.md"),
        )

    def test_archive_summary_copies_the_line(self):
        self.assertIn(
            "copy its `feature series: …` text verbatim here, on its own line after the **goal:** line. leave out the line's date and bullet.",
            read("shared", "templates", "archive-summary.md"),
        )

    def test_status_snapshot_cites_the_release_rule(self):
        text = read("milestone", "SKILL.md")
        snapshot = text[text.index("## 1. snapshot") : text.index("## 2. health audit")]
        self.assertIn(
            "in owner mode, also report each half-merged feature series and the status of each of its parts that is not `done`, by the rule `/cairn-release` step 1 states under \"half-merged feature series\".",
            snapshot,
        )
        self.assertIn(
            "for that report, read `${claude_plugin_root}/skills/cairn-release/skill.md` step 1, every live milestone file, and the archive summaries the rule names.",
            snapshot,
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


class TestCutSeries(unittest.TestCase):
    """M276: a series formed by a scope cut at implement or review.

    Departs from the one-physical-line convention above: wrapped skill prose
    is whitespace-collapsed on read (the M171 lesson), so a sentence is
    matched whole however its lines wrap.
    """

    def flat(self, *parts):
        return " ".join(read(*parts).split())

    def rules(self):
        text = self.flat("shared", "tracking-rules.md")
        start = text.index("## sizing and the work tiers")
        return text[start : text.index("work that isn't a milestone", start)]

    def test_rulebook_defines_the_cut_series(self):
        self.assertIn("**a cut series.** a series also forms through a scope cut.", self.rules())
        self.assertIn(
            "a scope cut is a substantive amendment that moves work a user-facing milestone's goal or scope `in:` promised to later work.",
            self.rules(),
        )
        self.assertIn("it comes at implement, or it carries out a review descope.", self.rules())
        self.assertIn(
            "the cut milestone and the milestone later planned for that work are the series.",
            self.rules(),
        )

    def test_rulebook_cut_milestone_owns_the_entry(self):
        self.assertIn("rules (a) and (b) do not bind the cut milestone.", self.rules())
        self.assertIn(
            "its changelog entry, where it has one, is the series' one entry under (c).",
            self.rules(),
        )

    def test_rulebook_only_the_later_milestone_carries_the_line(self):
        self.assertIn(
            "the cut records that work as a candidate row carrying `split from m<nnn>` (`/milestone-implement` step 6).",
            self.rules(),
        )
        self.assertIn("only the later milestone carries the `feature series:` line.", self.rules())

    def test_implement_marks_the_row(self):
        text = self.flat("milestone-implement", "SKILL.md")
        step = text[text.index("6. **plan amendments**") : text.index("7. **claim audit**")]
        self.assertIn(
            "a substantive amendment of a user-facing milestone can move work that its goal or scope `in:` promised to later work. a review descope is one such amendment.",
            step,
        )
        self.assertIn(
            "the amendment records that work as a candidate row whose lineage carries ` — split from m<nnn>`, naming this milestone. if the work's home is a split milestone, the amendment writes the same row,",
            step,
        )
        self.assertIn(
            "a follow-up row for a narrowed criterion's finding (the rule above) carries no marker. a remainder row of an internal-tier milestone carries none either.",
            step,
        )

    def test_plan_writes_the_line_for_a_marked_row(self):
        text = self.flat("milestone-plan", "SKILL.md")
        step = text[text.index("4. **solidify autonomously**") : text.index("5. **remainder ledger")]
        self.assertIn(
            "a milestone the plan creates from a candidate row carrying `split from m<nnn>` (a cut series) gets the work-log line `feature series: m<nnn> -> m<new>`. the cut milestone's file gets no line.",
            step,
        )
        self.assertIn(
            "where the cut milestone has a changelog entry, the new milestone's changelog task edits that entry under rule (c).",
            step,
        )

    def test_release_names_marked_rows(self):
        text = self.flat("cairn-release", "SKILL.md")
        step = text[text.index("1. **version decision**") : text.index("2. **changelog consolidation**")]
        self.assertIn(
            "the question also names each unplanned part of a cut series (tracking-rules \"feature series\") as a part of m<nnn>'s feature.",
            step,
        )
        self.assertIn(
            "such a part is a row of the candidates section of `cairn/roadmap.md` whose text carries `split from m<nnn>`, where m<nnn> is `done` by the rule above.",
            step,
        )
        self.assertIn(
            "the question leaves out a row whose ` — started m<x>` token names a `planned`, `in-progress`, `blocked`, or `review` milestone by that rule.",
            step,
        )
        self.assertIn("no such series or row → the question says nothing about series.", step)


if __name__ == "__main__":
    unittest.main()
