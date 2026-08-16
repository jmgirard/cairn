"""Lock: the records-hygiene family is maturation's second application (M110, D-061).

D-055 built maturation — the third way a lesson leaves `LESSONS.md` — and
delivered the first doctrine module, banking the records-hygiene
family (8 items firing at a hygiene or plan gate, not guard-authoring) as a
candidate. M110 graduates that family into `skills/shared/records-hygiene.md`,
the second module, exercising D-055's mechanism rather than changing it.

Four surfaces must not drift apart: the module, the rulebook pointer beside the
retirement rule, `cairn/LESSONS.md` (the family is gone), and D-061. Each
positive assertion is mutation-proven (M53); absence asserts are not (blanking
satisfies them). Targets are read per test, not cached at class level, since
the mutation harness runs a guard as a single method and skips `setUpClass`
(M61). Anchors are copied from the files' actual bytes (M95); wrapped anchors
use a `\\s+` matcher rather than a literal newline (M105).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent

MODULE = SKILLS / "shared" / "records-hygiene.md"


def read(path):
    return path.read_text()


class TestModuleExists(unittest.TestCase):
    """The graduated family has a home that declares itself and covers the family."""

    def setUp(self):
        self.module = read(MODULE)

    def test_module_is_present(self):
        self.assertTrue(MODULE.is_file(), f"{MODULE} is missing")

    def test_module_declares_when_it_is_read(self):
        self.assertIn(
            "Read this whenever you are at a milestone hygiene or plan gate",
            self.module,
        )


    # One anchor per section, binding the rule's subject to its disposition
    # (M103), so a swap between sections cannot stay green.

    def test_section1_candidate_rows_graduate_at_completion(self):
        self.assertIn("Candidates graduate at *completion*", self.module)

    def test_section2_collision_sweep_greps_the_archive(self):
        self.assertIn(
            "collision sweep greps `milestones/archive/` for *decisions*",
            self.module,
        )


class TestDecisionEntry(unittest.TestCase):
    """D-061 records the second maturation and the M69/M77 disposition."""

    def setUp(self):
        self.decisions = read(ROOT / "cairn" / "DECISIONS.md")

    def test_decision_entry_exists_and_annotates_d055(self):
        self.assertRegex(
            self.decisions,
            r"### D-061 \(2026-07-23\): The records-hygiene lesson family graduates[^\n]*annotates D-055",
        )

    def test_decision_entry_states_graduate_not_ownership(self):
        # The plan-gate fork: M69/M77 graduate rather than ownership-retire.
        self.assertRegex(
            self.decisions,
            r"graduate into the module rather than\s+retire by D-051 ownership",
        )


class TestFamilyActuallyLeft(unittest.TestCase):
    """The graduated lessons are gone from LESSONS.md — no line, no breadcrumb."""

    def setUp(self):
        self.lessons = read(ROOT / "cairn" / "LESSONS.md")

    def test_graduated_lessons_are_absent(self):
        # Phrases in the ORIGINAL lesson wording (distinct from the module's
        # rewording), so each proves its own line left. A positive control
        # below proves the read saw content — M84's vacuity trap.
        for phrase in (
            "those rows are NOT pruned at plan time",
            "trimming prose only reduces a line count",
            "amend the AC via the implement step-6 gate",
            "the fork fallback closes a contributor's PR",
            "the plan-time collision sweep must grep",
            "wrote a universal references-page rule into the conditionally-read",
        ):
            self.assertNotIn(phrase, self.lessons)

    def test_positive_control_lessons_file_still_holds_a_kept_item(self):
        # Pairs with the absence-assert: proves the read actually saw content.
        # Re-anchored at M127's hygiene pass: the original anchor (the M60
        # hook-lifecycle line) retired by move into
        # `cairn/references/claude-code-hooks.md`; the control now rides the
        # oldest surviving lesson.
        self.assertIn(
            '"green" is only as wide as what you ran',
            self.lessons,
        )

    def test_no_graduation_breadcrumb_was_left_behind(self):
        # D-051 rejected an in-file breadcrumb; D-055 keeps that.
        self.assertNotIn("records-hygiene", self.lessons)

    def test_lessons_file_is_back_under_its_cap(self):
        # Graduation returned headroom to the <50 item cap (M110: 49 -> 41).
        self.assertLess(len(self.lessons.splitlines()), 50)


if __name__ == "__main__":
    unittest.main()
