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
        # Anchored to the LINE_CAPS block, not to the bare key: the key
        # `"cairn/LESSONS.md"` also appears elsewhere in cairn_scripts (the
        # retired density roster; CHAR_CAPS before M101), so an unanchored
        # search reads whichever declaration comes first and would compare
        # this LINE cap against an unrelated number if the blocks were ever
        # reordered (M84 review F3).
        stated = int(re.search(r"`LESSONS\.md`\s*<\s*(\d+)\s*lines", self.rules).group(1))
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        line_caps = re.search(r"LINE_CAPS\s*=\s*\{(.*?)\}", scripts, re.S).group(1)
        enforced = int(re.search(r'"cairn/LESSONS\.md":\s*(\d+)', line_caps).group(1))
        self.assertEqual(stated, enforced)

    def test_lessons_home_exists_with_entry_format(self):
        lessons = read(ROOT / "cairn" / "LESSONS.md")
        self.assertIn("# Lessons", lessons)
        self.assertIn("YYYY-MM-DD (M<NNN>)", lessons)  # documented one-line format

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


    def test_the_correction_must_be_marked(self):
        # "Corrected in place" without the marking requirement is the option
        # D-045 explicitly rejected — same end state, loses the visible link
        # between the wrong text and its fix. M95's inversion sweep found the
        # mechanism pinned and the marking clause unpinned.
        self.assertIn("the correction marked", self.rules)


    def test_history_set_is_enumerated_under_its_own_label(self):
        # AC1 requires the rule to name the SETS, not just the mechanism.
        # Label and members share one physical line, so swapping the two
        # enumerations breaks this anchor — the M76/F1 gap, which the
        # mechanism asserts alone did not cover.
        #
        # M119/RR08 BC1 added the milestone-local `## Decisions` section, and
        # the line is RE-ANCHORED whole rather than gaining a second assert:
        # the pre-M119 wording is a substring of nothing here, so a revert to
        # the six-member list reds. Appending an assert would have left the old
        # enumeration satisfying this one — the false coverage M118 AC5 hit.
        self.assertIn(
            "History — `DECISIONS.md`, work-logs, the milestone-local "
            "`## Decisions` section,",
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


    def test_retirement_wired_into_review_hygiene(self):
        self.assertIn("Retire what this milestone covered", self.review)

    def test_review_hygiene_forbids_a_full_resweep(self):
        self.assertIn(
            "**Scope this to what the milestone shipped — never re-sweep "
            "every lesson.**",
            self.review,
        )


if __name__ == "__main__":
    unittest.main()
