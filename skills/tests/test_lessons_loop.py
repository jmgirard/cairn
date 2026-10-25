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


def norm(text):
    return " ".join(text.split())


class TestUseMarksAndCapture(unittest.TestCase):
    """M320 (D-218): plans record the lessons they used, review marks them,
    and a full file evicts by rank. The pinned sentences wrap, so this class
    collapses whitespace on read."""

    def test_plan_writes_the_lessons_used_line(self):
        plan = norm(read(SKILLS / "milestone-plan" / "SKILL.md"))
        self.assertIn(
            "Step 4 writes one work-log line `lessons used: <lessons>` in "
            "each milestone file it writes. It names each lesson that shaped "
            "that milestone's plan by its date and provenance, or it reads "
            "`lessons used: none`.",
            plan,
        )

    def test_review_marks_each_used_lesson(self):
        review = norm(read(SKILLS / "milestone-review" / "SKILL.md"))
        self.assertIn(
            "First mark use: add `used M<NNN>` to the parenthesized "
            "provenance of each lesson that the `lessons used:` lines read "
            "before the deletion name, and of each lesson whose trap the "
            "milestone met. The mark replaces that lesson's earlier `used` "
            "mark, if it has one, and the use adds no other text to the "
            "lesson.",
            review,
        )
        self.assertIn(
            "The mark counts toward that limit, and a lesson that the mark "
            "takes past 450 bytes is shortened in this same pass.",
            review,
        )

    def test_review_reads_the_used_lines_before_the_deletion(self):
        # M321: the live file is gone once the archive summary replaces it,
        # so the read must come first in the step.
        review = norm(read(SKILLS / "milestone-review" / "SKILL.md"))
        read_at = review.index(
            "Before the live file is deleted below, read its `lessons used:` "
            "work-log lines. Also read its work log and Review section for "
            "each lesson whose trap the milestone met."
        )
        delete_at = review.index("**deleting the live")
        self.assertLess(read_at, delete_at)

    def test_mark_shortening_keeps_pinned_text_whole(self):
        review = norm(read(SKILLS / "milestone-review" / "SKILL.md"))
        self.assertIn(
            "The shortening keeps whole each string a pin file asserts "
            "present and each text a live milestone quotes (both defined "
            "below). A lesson that cannot then fit in 450 bytes takes no "
            "`used` mark, and the close block names it beside a fenced "
            "`/cairn-triage lessons`.",
            review,
        )
        self.assertIn(
            "Find the pin files as each file that `git grep -l \"LESSONS.md\"` "
            "lists whose path contains `test`, and read each one for the "
            "strings it asserts present.",
            review,
        )

    def test_hygiene_preview_shows_each_changed_lesson(self):
        review = norm(read(SKILLS / "milestone-review" / "SKILL.md"))
        self.assertIn(
            "show the archive summary, each LESSONS line the pass captures, "
            "marks, shortens, or writes as waiting,",
            review,
        )
        self.assertIn(
            "Name each lesson the pass removes by its date and provenance.",
            review,
        )

    def test_a_long_extension_becomes_its_own_lesson(self):
        review = norm(read(SKILLS / "milestone-review" / "SKILL.md"))
        self.assertIn(
            "An extension that would take a lesson past 450 bytes is not "
            "written into it. The new content becomes a lesson of its own "
            "instead.",
            review,
        )

    def test_review_capture_is_one_in_one_out(self):
        review = norm(read(SKILLS / "milestone-review" / "SKILL.md"))
        self.assertIn(
            "when a captured lesson would leave more than 25 lessons, remove "
            "the lowest-ranked lessons (tracking-rules \"Weight caps\") until "
            "25 remain, in this same pass, and name them all in one line of "
            "the archive summary. Remove no lesson that a pin file holds or a "
            "live milestone quotes.",
            review,
        )
        self.assertIn(
            "When too few lessons can be removed to leave 25, remove none and "
            "capture no lesson. Write each skipped lesson at the end of "
            "`cairn/LESSONS.md` as a waiting line, "
            "`- waiting YYYY-MM-DD (M<NNN>): <lesson>`. A waiting line is not "
            "a lesson. It counts toward the file's line cap and not toward "
            "its 25 lessons. It takes no `used` mark, and it waits for "
            "`/cairn-triage lessons` to admit or drop it.",
            review,
        )
        self.assertIn(
            "If `cairn/LESSONS.md` already holds 49 lines or more, do not "
            "write the line, since it brings the file to 50 lines or more. "
            "Quote that lesson in full in the close block instead.",
            review,
        )
        self.assertNotIn("capture " "nothing", review)
        self.assertIn(
            "In guest mode `cairn/LESSONS.md` has no git copy, so the close "
            "block also quotes each removed lesson in full.",
            review,
        )
        # Spelled by concatenation so a repo grep for the retired word
        # does not hit this guard.
        self.assertNotIn("stal" "est", review)


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


class TestOverLimitRemedy(unittest.TestCase):
    """M321 (D-221): each limit has its own remedy, and a waiting line is
    no lesson. The pinned sentences wrap, so this class collapses whitespace
    on read."""

    REMEDY = (
        "A lesson over 450 bytes is shortened or split. Over 25 lessons, "
        "lessons retire first, and then the lowest-ranked lesson leaves."
    )
    WAITING = (
        "A `- waiting` line at the end is not a lesson. When no lesson can "
        "leave a full file, review writes it. It takes no `used` mark and "
        "waits for `/cairn-triage lessons` to admit or drop it."
    )

    def test_template_states_each_remedy_and_the_waiting_line(self):
        template = norm(read(SKILLS / "shared" / "templates" / "lessons.md"))
        self.assertIn(self.REMEDY, template)
        self.assertIn(self.WAITING, template)

    def test_lessons_header_states_each_remedy_and_the_waiting_line(self):
        lessons = norm(read(ROOT / "cairn" / "LESSONS.md"))
        self.assertIn(self.REMEDY, lessons)
        self.assertIn(self.WAITING, lessons)

    def test_rulebook_states_each_remedy_and_the_waiting_line(self):
        rules = norm(read(SKILLS / "shared" / "tracking-rules.md"))
        self.assertIn(
            "a lesson over 450 bytes → compress or split it; over 25 lessons "
            "→ retire lessons, then evict by rank (\"Retiring a lesson\");",
            rules,
        )
        self.assertIn(
            "A `- waiting YYYY-MM-DD (M<NNN>):` line is not a lesson. It "
            "takes no `used` mark and waits for `/cairn-triage lessons` to "
            "admit or drop it.",
            rules,
        )
        self.assertIn(
            "When none can go, the new lesson goes at the file's end as a "
            "`- waiting` line, which is not a lesson, takes no `used` mark, "
            "and waits for `/cairn-triage lessons`.",
            rules,
        )
        self.assertIn(
            "its `admit` disposition makes a waiting line a lesson", rules
        )


if __name__ == "__main__":
    unittest.main()
