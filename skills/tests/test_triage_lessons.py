"""Regression guard: the M263 lessons pass of `/cairn-triage` (D-169, D-177).

`/cairn-triage lessons` reads every `cairn/LESSONS.md` lesson and proposes
one disposition each at the triage gate. Each rule the pass rests on is
pinned on its own (M165 lesson):

  1. The argument: no argument means no lesson, any other argument stops.
  2. The item shape and the empty case.
  3. The pin check before any proposal, both directions.
  4. The seven lesson dispositions, the six drop exits, the maturation bar,
     the false-lesson `correct`, the planner test (M270), and the `split`
     disposition, the length rule, and the rank rule (M320).
  5. Apply and record: no line left behind, the two-file limit check, the
     gate count, the stamp and commit naming, the guest arm, no decision
     entry.
  6. The rulebook and README name the pass, and the rulebook states the
     lesson limits and the rank (M320).

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
            "`keep`, its reason naming that file, unless the length rule "
            "below applies to it.",
            section(),
        )

    def test_no_edit_writes_an_absent_string(self):
        self.assertIn(
            "No accepted edit writes a string that a pin file asserts is "
            "absent.",
            section(),
        )


class TestLessonDispositions(unittest.TestCase):
    def test_seven_dispositions_only(self):
        self.assertIn(
            "A lesson takes one of seven dispositions, and never `route` or "
            "`retitle`",
            section(),
        )

    def test_split_disposition(self):
        self.assertIn(
            "| `split` | Broken into two or more lessons, each one line of at "
            "most 450 bytes and each on one subject. Each new line keeps the "
            "original date and only the provenance ids its text came from.",
            section(),
        )

    def test_drop_names_one_of_six_exits(self):
        text = section()
        self.assertIn("The reason names one of six exits.", text)
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
        self.assertIn(
            "`rank`: the reason names the lesson's rank, the milestone id "
            "that sets it (the rank rule, below).",
            text,
        )
        self.assertIn("lesson leaves only by the six exits above", text)

    def test_evidence_exits_need_evidence(self):
        text = section()
        self.assertIn(
            "A lesson without such evidence is not dropped as `refuted` or "
            "`obsolete`, so a lesson merely disputed stays.",
            text,
        )
        self.assertIn(
            "The reads behind a `refuted`, `obsolete`, or `correct` proposal "
            "run at that ref too. There a code path is checked with `git "
            "cat-file -e` at that ref in place of `ls`. A "
            "`cairn/` path is checked on disk, since `cairn/` is untracked at "
            "that ref. A commit that an `obsolete` drop names is reachable "
            "from that ref.",
            text,
        )
        self.assertNotIn(
            "A lesson about a path or tool the repo no longer has is `keep`",
            text,
        )

    def test_a_kept_false_lesson_reaches_the_stamp(self):
        self.assertIn(
            "A pin or a live milestone makes a lesson `keep` before any other "
            "rule but the length rule. If such a lesson is false or obsolete, "
            "steps 4 to 6 still run for the stamp, even when every proposal "
            "is `keep`. The stamp names the lesson and the evidence.",
            section(),
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
            "after its date.",
            text,
        )
        self.assertIn(
            "A false lesson with no such part is `drop` with the `refuted` "
            "exit.",
            text,
        )
        self.assertNotIn("A lesson the pass finds false is `keep`", text)
        self.assertIn(
            "The table shows the corrected line verbatim. Its reason quotes "
            "the evidence for the false part, as a `refuted` drop does.",
            text,
        )
        self.assertIn(
            "The pass has no milestone id, so its mark takes the date. A "
            "`corrected` mark already on the line stays, and the new mark "
            "follows it.",
            text,
        )

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

    def test_length_rule(self):
        text = section()
        self.assertIn(
            "Last, count the lessons and measure each lesson's bytes against "
            "the limits of tracking-rules \"Weight caps\": at most 25 "
            "lessons, each at most 450 bytes.",
            text,
        )
        self.assertIn(
            "The length rule: each lesson whose step-1 byte length is over "
            "450 gets `compress` or `split`, with its new line or lines shown "
            "verbatim in the table. A long lesson is never kept as it is.",
            text,
        )
        self.assertIn(
            "For such a lesson, the string the pin file asserts present, or "
            "the text the milestone quotes, stays whole in one resulting "
            "line.",
            text,
        )
        self.assertIn(
            "A merge whose survivor would pass 450 bytes is not proposed.",
            text,
        )
        self.assertNotIn("The other is `keep`, with a reason that", text)

    def test_rank_rule(self):
        text = section()
        self.assertIn(
            "The rank rule: after the other proposals, count the lessons that "
            "would remain, each line of a split counting as one. If more than "
            "20 would remain, propose `drop` with the `rank` exit for the "
            "lowest-ranked of them",
            text,
        )
        self.assertIn(
            "until 20 remain or every remaining lesson is kept for a pin, a "
            "live milestone, or as a merge survivor.",
            text,
        )
        # Retired phrases are spelled by concatenation so a repo grep for
        # them does not hit these guards (M320 review).
        self.assertNotIn("never proposes pruning the oldest " "lesson", text)


class TestLessonsApplyAndRecord(unittest.TestCase):
    def test_no_line_left_behind(self):
        self.assertIn(
            "A dropped or merged-away lesson leaves no line in "
            "`cairn/LESSONS.md`, and no breadcrumb.",
            section(),
        )

    def test_cap_check_covers_both_files(self):
        self.assertIn(
            "After the edits, `cairn/ROADMAP.md` stays under its line cap and "
            "byte budget, the stamp included, and `cairn/LESSONS.md` stays "
            "within its limits",
            section(),
        )

    def test_gate_warning(self):
        self.assertIn(
            "Each time the chip is posed, Amend rounds included, count the "
            "lessons that `cairn/LESSONS.md` would hold with the proposals "
            "then standing all applied, and find any lesson that would be "
            "over 450 bytes. The chip's question text gives the count in one "
            "sentence. It also says when the count is over 20 or a lesson is "
            "over 450 bytes.",
            section(),
        )

    def test_correct_applies_the_gate_text(self):
        text = section()
        self.assertIn(
            "A `correct`, a `compress`, and a `split` show the new line or "
            "lines verbatim.",
            text,
        )
        self.assertIn(
            "An Amend that makes a lesson `correct`, `compress`, or `split` "
            "names its new line or lines. In every Amend round, the pass "
            "shows that line again before it poses the chip. A lesson the "
            "user moves to `keep` at an Amend takes the reason `kept at the "
            "gate`.",
            text,
        )
        self.assertIn(
            "A `correct` replaces the line with the text the gate showed, and "
            "a `split` replaces it with the lines the gate showed, in its "
            "place.",
            text,
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
            "lesson with its survivor, each corrected or split lesson by its "
            "date and provenance, and each `rank` drop with its rank. The "
            "commit message also gives the evidence for "
            "each `refuted` or `obsolete` drop and each `correct`. In guest "
            "mode the stamp alone names them, with their evidence.",
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
        text = read("shared/tracking-rules.md")
        self.assertIn(
            "and over the whole file only when the user runs `/cairn-triage "
            "lessons`",
            text,
        )
        self.assertIn("At review hygiene, three exits:", text)
        self.assertIn(
            "The whole-file pass adds four drop exits, each decided at its "
            "gate: `refuted` and `obsolete`, each with evidence read in the "
            "pass, `planner test`, for a line a planner does not need, and "
            "`rank`, which evicts the lowest-ranked lessons down to 20.",
            text,
        )
        self.assertIn("It also corrects a false lesson in place", text)

    def test_rulebook_states_the_limits_and_the_rank(self):
        text = read("shared/tracking-rules.md")
        self.assertIn(
            "`LESSONS.md` holds at most 25 lessons, each one line of at most "
            "450 bytes, newline excluded.",
            text,
        )
        self.assertIn(
            "A lesson's **rank** is the highest milestone number among the "
            "ids in its parenthesized provenance, except an id that follows "
            "`trimmed` or `corrected` in the same comma-separated part. A tie "
            "goes to the later date, then to the line later in the file.",
            text,
        )
        self.assertNotIn("`LESSONS.md` < 20,000 bytes", text)
        self.assertNotIn("stal" "est", text)

    def test_rulebook_states_use_marks_and_one_in_one_out(self):
        text = read("shared/tracking-rules.md")
        self.assertIn(
            "`/milestone-plan` names the lessons that shaped its plan in a "
            "`lessons used:` work-log line, and review hygiene marks each of "
            "those, and each lesson whose trap the milestone met, `used "
            "M<NNN>`.",
            text,
        )
        self.assertIn(
            "At the 25-lesson limit review capture is one-in-one-out: it "
            "evicts the lowest-ranked lesson that no pin file holds and no "
            "live milestone quotes.",
            text,
        )

    def test_readme_names_the_pass(self):
        text = norm((ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn(
            "`/cairn-triage lessons` does the same for each lesson in "
            "`cairn/LESSONS.md`, and can drop a false or obsolete lesson or "
            "correct one",
            text,
        )


if __name__ == "__main__":
    unittest.main()
