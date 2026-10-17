"""Regression guard: the M263 lessons pass of `/cairn-triage` (D-169, D-177).

`/cairn-triage lessons` reads every `cairn/LESSONS.md` lesson and proposes
one disposition each at the triage gate. Each rule the pass rests on is
pinned on its own (M165 lesson):

  1. The argument: no argument means no lesson, any other argument stops.
  2. The item shape and the empty case.
  3. The pin check before any proposal, both directions.
  4. The six lesson dispositions, the five drop exits, the maturation bar,
     the false-lesson `correct`, the planner test, and the near-cap rule
     (M270).
  5. Apply and record: no line left behind, the two-file cap check, the
     gate warning, the stamp and commit naming, the guest arm, no decision
     entry.
  6. The rulebook and README name the pass.

The pinned phrases wrap across source lines, so this guard collapses
whitespace on read, as `test_guest_triage` does. Each target is read per
test, never cached on the class (M61).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent


def norm(text):
    return " ".join(text.split())


def read(rel):
    return norm((SKILLS / rel).read_text(encoding="utf-8"))


def section():
    text = read("cairn-triage/SKILL.md")
    start = text.index("## The lessons pass (`/cairn-triage lessons`)")
    end = text.index("## Workflow", start)
    return text[start:end]


class TestLessonsArgument(unittest.TestCase):
    def test_no_argument_means_no_lesson(self):
        self.assertIn(
            "With no argument the pass enumerates the candidates and Known "
            "issues and no lesson.",
            section(),
        )

    def test_any_other_argument_stops(self):
        self.assertIn(
            "An argument other than `lessons` stops before enumeration with a "
            "close block that names `lessons` as the one accepted value.",
            section(),
        )

    def test_same_preconditions_gate_and_commit(self):
        self.assertIn(
            "The lessons pass runs the same preconditions, gate, apply, "
            "stamp, and commit as the default pass",
            section(),
        )

    def test_frontmatter_names_the_argument(self):
        text = read("cairn-triage/SKILL.md")
        self.assertIn('argument-hint: "[lessons]"', text)
        self.assertIn("or with the argument `lessons` every cairn/LESSONS.md lesson", text)


class TestLessonItems(unittest.TestCase):
    def test_item_shape(self):
        text = section()
        self.assertIn(
            "A lesson item is one line of `cairn/LESSONS.md` that opens with "
            "`- ` and a `YYYY-MM-DD` date.",
            text,
        )
        self.assertIn(
            "the text after the first `): `, or after the date when the line "
            "has none, trimmed to about 80 characters.",
            text,
        )
        self.assertIn("Its priority is `—`.", text)

    def test_missing_file_yields_no_items(self):
        self.assertIn(
            "A missing `cairn/LESSONS.md`, or one with no such line, yields "
            "zero items with no failure.",
            section(),
        )


class TestPinCheck(unittest.TestCase):
    def test_pin_files_are_found_by_git_grep(self):
        self.assertIn(
            "each file that `git grep -l \"LESSONS.md\"` lists whose path "
            "contains `test`. None listed means no pins and no failure.",
            section(),
        )

    def test_a_pinned_lesson_is_keep(self):
        self.assertIn(
            "A lesson that holds a string a pin file asserts is present is "
            "`keep`, its reason naming that file.",
            section(),
        )

    def test_no_edit_writes_an_absent_string(self):
        self.assertIn(
            "No accepted edit writes a string that a pin file asserts is "
            "absent.",
            section(),
        )


class TestLessonDispositions(unittest.TestCase):
    def test_six_dispositions_only(self):
        self.assertIn(
            "A lesson takes one of six dispositions, and never `split`, "
            "`route`, or `retitle`",
            section(),
        )

    def test_drop_names_one_of_five_exits(self):
        text = section()
        self.assertIn("The reason names one of five exits.", text)
        self.assertIn(
            "Enforcement: a test, by file and test name, with the assertion "
            "quoted that fails on the mistake the lesson warns about.",
            text,
        )
        self.assertIn(
            "Ownership: a `cairn/` tracking file and the section that already "
            "holds the lesson's content. The pass moves nothing into it.",
            text,
        )
        self.assertIn(
            "`refuted`: the reason quotes a file and line, or a command and "
            "its output, read in this pass, that shows the lesson's premise "
            "false.",
            text,
        )
        self.assertIn(
            "`obsolete`: the reason names the path, tool, or command the "
            "lesson is about. It quotes an `ls`, `git grep`, or `git log` "
            "result, read in this pass, that shows the repo no longer has "
            "it. Or it names the commit that removed it.",
            text,
        )
        self.assertIn(
            "`planner test`: the reason says why a planner loses nothing "
            "without the line",
            text,
        )
        self.assertIn("A lesson leaves only by the five exits above", text)

    def test_evidence_exits_need_evidence(self):
        text = section()
        self.assertIn(
            "A lesson without such evidence is not dropped as `refuted` or "
            "`obsolete`, so a lesson merely disputed stays.",
            text,
        )
        self.assertIn(
            "The reads behind a `refuted` or `obsolete` exit run at that ref "
            "too.",
            text,
        )

    def test_promote_states_the_maturation_bar(self):
        self.assertIn(
            "The family teaches transferable craft about authoring or "
            "verifying, not a fact about this repo's tools or runtime. It was "
            "extended or consolidated at least twice. No other exit applies",
            section(),
        )

    def test_prefix_and_marks_survive(self):
        self.assertIn(
            "A compressed, merged, or corrected lesson keeps its "
            "`- YYYY-MM-DD (M…)` prefix and any `corrected` or `trimmed` "
            "mark.",
            section(),
        )

    def test_a_false_lesson_is_corrected_or_dropped(self):
        text = section()
        self.assertIn(
            "A lesson the pass finds false is `correct` when a part of it "
            "that a planner needs stays true.",
            text,
        )
        self.assertIn(
            "adds `corrected YYYY-MM-DD`, the pass date, to the line's "
            "parenthesized provenance. A line with no provenance gets one "
            "after its date. A false lesson with no such part is `drop` with "
            "the `refuted` exit.",
            text,
        )
        self.assertNotIn("A lesson the pass finds false is `keep`", text)

    def test_planner_test(self):
        text = section()
        self.assertIn(
            "or else what a planner loses without the line (the planner "
            "test, below).",
            text,
        )
        self.assertIn(
            "A `keep` whose reason is already fixed needs no answer: a pin "
            "file, a live milestone, or `survivor of <subject>`.",
            text,
        )
        self.assertIn(
            "Sometimes the pass can name no loss, and no tracking file holds "
            "the lesson, so ownership does not apply. Then the pass proposes "
            "`drop` with the `planner test` exit.",
            text,
        )

    def test_near_cap_rule(self):
        text = section()
        self.assertIn(
            "A file at 45 lines or more, or 18,000 bytes or more, is near its "
            "caps",
            text,
        )
        self.assertIn(
            "Below the near-cap figures, length alone never fires a "
            "`compress`.",
            text,
        )
        self.assertIn(
            "Each lesson whose step-1 byte length is over 400 gets one of two "
            "proposals. One is `compress`, with its shortened line shown "
            "verbatim in the table. The other is `keep`, with a reason that "
            "names why each clause stays. The rule skips a lesson proposed "
            "`drop`, `merge`, `correct`, or `promote`. It also skips a merge "
            "survivor and a lesson kept for a pin or a live milestone.",
            text,
        )


class TestLessonsApplyAndRecord(unittest.TestCase):
    def test_no_line_left_behind(self):
        self.assertIn(
            "A dropped or merged-away lesson leaves no line in "
            "`cairn/LESSONS.md`, and no breadcrumb.",
            section(),
        )

    def test_cap_check_covers_both_files(self):
        self.assertIn(
            "`wc -l -c cairn/LESSONS.md cairn/ROADMAP.md` stays under both "
            "files' line caps and byte budgets",
            section(),
        )

    def test_gate_warning(self):
        self.assertIn(
            "Each time the chip is posed, Amend rounds included, count the "
            "lines and bytes that `cairn/LESSONS.md` has with the proposals "
            "then standing all applied. If the count is 45 lines or more, or "
            "18,000 bytes or more, the chip's question text says so. One "
            "sentence names both counts.",
            section(),
        )

    def test_correct_applies_the_gate_text(self):
        self.assertIn(
            "A `correct` replaces the line with the text the gate showed.",
            section(),
        )

    def test_record_names_drops_merges_and_corrections(self):
        text = section()
        self.assertIn(
            "A lesson drop, merge, or correction writes no decision entry.",
            text,
        )
        self.assertIn(
            "The stamp and the commit message name each dropped lesson by its "
            "date and provenance with its exit. They name each merged-away "
            "lesson with its survivor, and each corrected lesson by its date "
            "and provenance. In guest mode the stamp alone names them, with "
            "their evidence.",
            text,
        )

    def test_one_plan_per_family(self):
        self.assertIn(
            "The close block fences one `/milestone-plan <family>` per "
            "promoted family, not one per lesson.",
            section(),
        )


class TestSurfacesNameThePass(unittest.TestCase):
    def test_rulebook_names_the_on_demand_pass(self):
        self.assertIn(
            "and over the whole file only when the user runs `/cairn-triage "
            "lessons`",
            read("shared/tracking-rules.md"),
        )

    def test_readme_names_the_pass(self):
        text = norm((ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn(
            "`/cairn-triage lessons` does the same for each lesson in "
            "`cairn/LESSONS.md`",
            text,
        )


if __name__ == "__main__":
    unittest.main()
