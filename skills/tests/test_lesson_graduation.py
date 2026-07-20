"""Lock: maturation is the third way a lesson leaves `LESSONS.md` (M98, D-055).

D-051 gave the file two outflows — enforcement (a test fails on the mistake)
and ownership (another tracking file's slot holds the content). Neither can
ever retire guard-authoring craft: no test fails on the judgment a guard does
not make, and no slot owned that craft. M98 adds the third, graduation into a
conditionally-read module, and moves the family into
`skills/shared/guard-doctrine.md`.

Three surfaces must not drift apart: the rulebook's retirement rule and its
module pointer, `cairn/LESSONS.md`'s own header, and D-055. Each assertion
here is positive so it can be mutation-proven (M53 discipline), and the
targets are read per test rather than cached at class level, since the
mutation harness runs a guard as a single method and skips `setUpClass`
(M61).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent

MODULE = SKILLS / "shared" / "guard-doctrine.md"


def read(path):
    return path.read_text()


class TestModuleExists(unittest.TestCase):
    """The graduated family has a home, and it covers what it claims to."""

    def setUp(self):
        self.module = read(MODULE)

    def test_module_is_present(self):
        self.assertTrue(MODULE.is_file(), f"{MODULE} is missing")

    def test_module_declares_when_it_is_read(self):
        self.assertIn(
            "Read this whenever authoring or editing a test that locks prose",
            self.module,
        )

    def test_module_declares_itself_a_rulebook_module(self):
        # D-031's shape: domain doctrine is a module, not a rulebook section.
        self.assertIn("a module of `tracking-rules.md`", self.module)

    def test_anchor_section_states_the_one_physical_line_rule(self):
        self.assertIn(
            "pin the label\ntogether with its members on one physical line",
            self.module,
        )

    def test_anchor_section_states_the_inversion_protocol(self):
        self.assertIn(
            "Relabel, negate, or transpose the rule in place, run\nthe suite, require red, restore, and diff.",
            self.module,
        )

    def test_harness_section_states_registration_is_per_file(self):
        self.assertIn(
            "**Registration is per file (≥1 exemplar block), never per assertion.**",
            self.module,
        )

    def test_harness_section_states_only_positives_are_provable(self):
        self.assertIn(
            "**Only a positive assertion can be mutation-proven.**", self.module
        )

    def test_absence_section_states_the_vacuous_crash_rule(self):
        self.assertIn(
            "A guard whose only assertion is an `assertNotIn` is vacuous against a\ncrash.",
            self.module,
        )

    def test_matcher_section_states_the_authorization_switch(self):
        self.assertIn(
            'When a detection regex graduates from "is this\nguarded?" to "is this authorized?", switch to `finditer` and require every\noccurrence to clear.',
            self.module,
        )

    def test_restatement_section_states_the_read_it_out_rule(self):
        self.assertIn(
            "**Run each member of a documented set through the\nimplementation, never the set as a whole.**",
            self.module,
        )


class TestRulebookPointer(unittest.TestCase):
    """The rulebook routes to the module, on a line that stays pinnable."""

    def setUp(self):
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")

    def test_rulebook_points_at_the_module(self):
        self.assertIn(
            "The craft of making a guard falsifiable lives in a module of this rulebook",
            self.rules,
        )

    def test_pointer_maps_the_module_to_its_coverage_on_one_physical_line(self):
        # M74/M76/M86: a label->members mapping split across a line break is
        # unpinnable — the anchor stops at the break, before the predicate
        # carrying the meaning. The rulebook deliberately keeps this mapping on
        # one long physical line; assert it as one, so re-wrapping reddens.
        line = next(
            l for l in self.rules.split("\n") if l.startswith("`skills/shared/guard-doctrine.md` covers")
        )
        for member in (
            "anchors and what an assert must pin",
            "the mutation harness's own blind spots",
            "absence assertions",
            "fixture design",
            "matchers over authored markdown",
            "restatement and numbers",
            "sweep scoping",
        ):
            self.assertIn(member, line, f"{member!r} left the pointer's own line")

    def test_pointer_states_when_to_read_the_module(self):
        self.assertIn(
            "Read it when authoring or editing a prose-guard, a fixture, a matcher, or a",
            self.rules,
        )

    def test_pointer_states_the_module_is_read_conditionally(self):
        self.assertIn("sessions that write no guard never pay for it", self.rules)


class TestThirdOutflow(unittest.TestCase):
    """Maturation is stated as a third criterion, not folded into the other two."""

    def setUp(self):
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")
        self.lessons = read(ROOT / "cairn" / "LESSONS.md")
        self.decisions = read(ROOT / "cairn" / "DECISIONS.md")

    def test_rulebook_counts_three_retirement_criteria(self):
        self.assertIn("Three criteria retire a lesson (D-051, D-055)", self.rules)

    def test_rulebook_names_maturation_with_its_mechanism_on_one_line(self):
        # Label -> rule on one physical line (M74): "maturation" must travel
        # with what it actually does, or the label can be swapped elsewhere
        # with every assert still green.
        self.assertIn(
            "**maturation — a stabilized family graduates whole into a doctrine module**",
            self.rules,
        )

    def test_rulebook_states_the_conjunctive_bar(self):
        line = next(
            l for l in self.rules.split("\n") if "maturation — a stabilized family" in l
        )
        for clause in (
            "teaches transferable authoring or verifying craft",
            "extended or consolidated at least twice",
            "neither enforcement nor ownership can ever retire it",
        ):
            self.assertIn(clause, line, f"{clause!r} left the bar's own line")

    def test_rulebook_distinguishes_maturation_from_the_rejected_second_record(self):
        self.assertIn(
            "the source line is deleted in the same pass, so exactly one record exists at every moment",
            self.rules,
        )

    def test_file_map_row_names_all_three_outflows(self):
        row = next(
            l for l in self.rules.split("\n") if l.startswith("| `cairn/LESSONS.md`")
        )
        self.assertIn("a matured family graduates whole into a doctrine module", row)
        self.assertIn("D-055", row)

    def test_lessons_header_names_the_third_outflow(self):
        self.assertIn(
            "or when a matured family\ngraduates whole into a doctrine module", self.lessons
        )

    def test_decision_entry_exists_and_annotates_d051(self):
        self.assertRegex(
            self.decisions,
            r"### D-055 \(2026-07-20\): Lessons also leave by maturation[^\n]*annotates D-051",
        )

    def test_decision_entry_distinguishes_the_rejected_graduated_lessons_file(self):
        self.assertIn(
            "Graduation\nis the opposite operation: the content moves and the source line is deleted",
            self.decisions,
        )


class TestFamilyActuallyLeft(unittest.TestCase):
    """The graduated lessons are gone from LESSONS.md — no line, no breadcrumb."""

    def setUp(self):
        self.lessons = read(ROOT / "cairn" / "LESSONS.md")

    def test_graduated_guard_craft_is_absent(self):
        # Distinctive phrases from the retired family. A positive control runs
        # alongside (below) so this absence-assert cannot pass on an empty or
        # truncated read — M84's vacuity trap.
        for phrase in (
            "the mutation harness runs a guard as a SINGLE method",
            "a SUBSTRING anchor gives false coverage",
            "negation is a property of a CLAUSE",
            "a two-signal detector is only as strong as its weaker signal",
        ):
            self.assertNotIn(phrase, self.lessons)

    def test_positive_control_lessons_file_still_holds_its_kept_items(self):
        # Proves the read above actually saw content (pairs with the
        # absence-assert; M84/M93).
        self.assertIn("hook *registrations* (hooks.json) snapshot at process start", self.lessons)
        # Inline the multiline flag: assertRegex's third positional arg is
        # `msg`, not `flags`, so a passed re.M is silently discarded.
        self.assertRegex(self.lessons, r"(?m)^- 20\d\d-\d\d-\d\d \(M\d+")

    def test_no_graduation_breadcrumb_was_left_behind(self):
        # D-051 rejected an in-file graduation breadcrumb; D-055 keeps that.
        self.assertNotIn("guard-doctrine.md", self.lessons)

    def test_partial_coverage_was_trimmed_not_deleted(self):
        # Two items were only partly covered by the module; their uncovered
        # remainders stay, marked as trimmed (D-051).
        self.assertIn("trimmed M92/M98", self.lessons)
        self.assertIn("trimmed M98", self.lessons)
        self.assertIn("age a synthesis note from its OLDEST un-re-read input", self.lessons)
        self.assertIn("sync a feature branch with `git rebase main` instead", self.lessons)


if __name__ == "__main__":
    unittest.main()
