"""Lock: the lessons loop (M16) stays wired end to end.

`cairn/LESSONS.md` is the durable, capped, correct-in-place lessons home; the
capture step lives in `/milestone-review` post-merge hygiene, the harvest step
in `/milestone-plan` before the gate, and the 50-line cap is stated in two
places that must not drift — the tracking-rules weight-caps line and
`cairn_scripts.LINE_CAPS`. (The cap is *enforced* by the over-cap fixture in
scripts/tests; this test locks the wiring and the stated↔enforced agreement.)

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent


def read(path):
    return path.read_text()


class TestLessonsLoop(unittest.TestCase):
    def setUp(self):
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")

    def test_file_map_documents_lessons_home(self):
        self.assertRegex(self.rules, r"\|\s*`cairn/LESSONS\.md`\s*\|")

    def test_weight_caps_states_lessons_cap(self):
        self.assertRegex(self.rules, r"`LESSONS\.md`\s*<\s*50\s*lines")

    def test_stated_cap_matches_enforced_cap(self):
        # The rulebook's human-readable cap and the scripts' machine-enforced
        # cap are two encodings of one number; drift between them is the defect.
        # Anchored to the LINE_CAPS block, not to the bare key: since M84 the
        # key `"cairn/LESSONS.md"` also appears in CHAR_CAPS, so an unanchored
        # search reads whichever dict is declared first and would compare this
        # LINE cap against the CHARACTER threshold if the two were ever
        # reordered (M84 review F3).
        stated = int(re.search(r"`LESSONS\.md`\s*<\s*(\d+)\s*lines", self.rules).group(1))
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        line_caps = re.search(r"LINE_CAPS\s*=\s*\{(.*?)\}", scripts, re.S).group(1)
        enforced = int(re.search(r'"cairn/LESSONS\.md":\s*(\d+)', line_caps).group(1))
        self.assertEqual(stated, enforced)

    def test_lessons_home_exists_with_entry_format(self):
        lessons = read(ROOT / "cairn" / "LESSONS.md")
        self.assertIn("# Lessons", lessons)
        self.assertIn("YYYY-MM-DD (M<NN>)", lessons)  # documented one-line format

    def test_capture_wired_into_review(self):
        # Anchor on the step text, not a bare "LESSONS.md" mention — the file
        # is named elsewhere, so a substring check wouldn't lock the step.
        review = read(SKILLS / "milestone-review" / "SKILL.md")
        self.assertIn("Capture durable lessons", review)
        self.assertIn("LESSONS.md", review)

    def test_harvest_wired_into_plan(self):
        # Likewise: LESSONS.md appears twice in plan (session-start read +
        # harvest step); lock the harvest step by its own heading text.
        plan = read(SKILLS / "milestone-plan" / "SKILL.md")
        self.assertIn("Harvest recent lessons", plan)
        self.assertIn("LESSONS.md", plan)


class TestRecordCorrectionRule(unittest.TestCase):
    """M76 (D-045): the rulebook states how a record proven false is fixed.

    Every assert here is LABEL-INCLUSIVE (M74/F3): each block carries the
    category name *and* its remedy on one physical line, so swapping the two
    labels — inverting the rule — fails the guard. Pinning only "corrected in
    place" would survive that inversion, which is exactly the false coverage
    the M74 review proved live.
    """

    def setUp(self):
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")

    def test_rule_is_named(self):
        self.assertIn("Correcting a record proven false", self.rules)

    def test_current_knowledge_is_corrected_in_place(self):
        self.assertIn("current knowledge is corrected in place", self.rules)

    def test_history_is_superseded_never_edited(self):
        self.assertIn("history is superseded and never edited", self.rules)

    def test_history_set_is_enumerated_under_its_own_label(self):
        # AC1 requires the rule to name the SETS, not just the mechanism.
        # Label and members share one physical line, so swapping the two
        # enumerations breaks this anchor — the M76/F1 gap, which the
        # mechanism asserts alone did not cover.
        self.assertIn(
            "History — `DECISIONS.md`, work-logs, milestone IDs, "
            "`milestones/archive/`,",
            self.rules,
        )

    def test_current_knowledge_set_is_enumerated_under_its_own_label(self):
        self.assertIn(
            "Current knowledge — `LESSONS.md`, `references/` pages, "
            "`DESIGN.md` —",
            self.rules,
        )

    def test_design_principles_are_carved_out_of_in_place_correction(self):
        # Without this, the rule would authorise editing an IP/GP line in
        # place, bypassing the user-decision + D-entry gate (M76/F2).
        self.assertIn("wrong *principle* is not a wrong fact", self.rules)

    def test_rule_rules_out_leaving_the_wrong_text_readable(self):
        # The whole point: appending a correction is not enough, because a
        # false lesson is harvested into every later plan.
        self.assertIn(
            "appending a correction while leaving the wrong text readable",
            self.rules,
        )

    def test_file_map_no_longer_calls_lessons_append_only(self):
        # Paired with the positive assert below: the negative alone can't be
        # mutation-proven (blanking cannot restore an absence — M54).
        row = next(
            line for line in self.rules.splitlines()
            if line.startswith("| `cairn/LESSONS.md`")
        )
        self.assertNotIn("append-only", row.lower())

    def test_file_map_names_the_lessons_write_mode(self):
        self.assertIn("a lesson proven false is corrected in place", self.rules)


class TestLessonRetirement(unittest.TestCase):
    """M92 (D-051): `LESSONS.md` has an outflow, not only a ceiling.

    Every assert here is LABEL-INCLUSIVE (M74/F3): each criterion's name and the
    test that discriminates it sit on one physical line, so relabelling
    enforcement as ownership — or softening "fails" to "exists" — breaks the
    anchor. Pinning the mechanism sentence alone would survive both swaps, which
    is the false coverage M74/M76/M86 proved live three times.

    Targets are read per-test, never cached in `setUpClass`: the mutation
    harness runs a guard as a single method and skips `setUpClass`, so a
    class-level cache reads the unmutated file and reports false coverage on
    itself (M61).
    """

    @property
    def rules(self):
        return read(SKILLS / "shared" / "tracking-rules.md")

    @property
    def review(self):
        return read(SKILLS / "milestone-review" / "SKILL.md")

    def test_rule_is_named(self):
        self.assertIn("Retiring a lesson that no longer earns its line", self.rules)

    def test_enforcement_criterion_pins_its_discriminating_test(self):
        self.assertIn(
            "**enforcement — a test fails on the mistake the lesson warns about**",
            self.rules,
        )

    def test_enforcement_rules_out_a_guard_merely_existing(self):
        # The entire weight of the criterion is on *fails* rather than *exists*:
        # most guard-naming lessons here teach the judgment the guard does not
        # make, so "a guard covers this area" would retire them wrongly.
        self.assertIn(
            "discriminating word is *fails* and never *exists*", self.rules
        )

    def test_ownership_criterion_pins_its_discriminating_test(self):
        self.assertIn(
            "**ownership — another tracking file's slot owns the content**",
            self.rules,
        )

    def test_ownership_permits_moving_content_to_its_owner(self):
        # M92 review F1/92: the label assert above stops at the label, so
        # rewording this clause to "must already be duplicated in its owner"
        # left every other assert green and silently reverted ownership to the
        # duplication-only reading the plan gate rejected — a reading that
        # would have blocked both of this milestone's own retirements.
        self.assertIn(
            "**the retiring milestone may *move* the content there rather "
            "than only find it already duplicated**",
            self.rules,
        )

    def test_partial_coverage_trims_rather_than_keeping_whole(self):
        self.assertIn(
            "**A lesson covered only in part is trimmed to its uncovered remainder**",
            self.rules,
        )

    def test_tombstone_is_the_archive_summary_and_nothing_else(self):
        self.assertIn(
            "**A retired lesson leaves no line behind — the retiring milestone's "
            "archive summary names what it graduated**",
            self.rules,
        )

    def test_retirement_is_distinguished_from_correction(self):
        # D-045 correction vs D-051 retirement. Both halves share one physical
        # line, so transposing "redundant" and "was false" — which would license
        # deleting a lesson merely disputed — fails this guard.
        self.assertIn(
            "**Retirement is not correction: a retired lesson is redundant, "
            "a corrected one was false**",
            self.rules,
        )

    def test_check_is_scoped_to_what_shipped(self):
        # Label-inclusive: the scope and its prohibition share one physical
        # line, so dropping "never as a full re-sweep" — the half that costs
        # every milestone a judgment pass over records it never touched —
        # breaks this anchor (M92 review F1, lower-priority relative).
        self.assertIn(
            "**scoped to what the milestone shipped, never as a full re-sweep**",
            self.rules,
        )

    def test_retirement_wired_into_review_hygiene(self):
        self.assertIn("Retire what this milestone covered", self.review)

    def test_review_hygiene_forbids_a_full_resweep(self):
        self.assertIn(
            "**Scope this to what the milestone shipped — never re-sweep "
            "every lesson.**",
            self.review,
        )

    def test_file_map_row_names_retirement(self):
        row = next(
            line
            for line in self.rules.splitlines()
            if line.startswith("| `cairn/LESSONS.md`")
        )
        self.assertIn(
            "retired once a test enforces it or another file owns it", row
        )


if __name__ == "__main__":
    unittest.main()
