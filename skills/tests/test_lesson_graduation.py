"""Lock: maturation is the third way a lesson leaves `LESSONS.md` (M98, D-055).

D-051 gave the file two outflows — enforcement (a test fails on the mistake)
and ownership (another tracking file's slot holds the content). M98 added the
third, graduation into a conditionally-read module. The surviving guards pin
the graduation's durable traces — `cairn/LESSONS.md`'s header and the D-055
record — which are stable whatever later became of the module (M146 deleted
it and pruned the module-content pins).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent


def read(path):
    return path.read_text()


class TestThirdOutflow(unittest.TestCase):
    """Maturation is stated as a third criterion, not folded into the other two."""

    def setUp(self):
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")
        self.lessons = read(ROOT / "cairn" / "LESSONS.md")
        self.decisions = read(ROOT / "cairn" / "DECISIONS.md")


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
        # absence-assert; M84/M93). Re-anchored at M127's hygiene pass: the
        # original anchor was the M60 hook-lifecycle line, retired by move
        # into `cairn/references/claude-code-hooks.md` (ownership); the
        # control now rides the oldest surviving lesson.
        self.assertIn('"green" is only as wide as what you ran', self.lessons)
        # Inline the multiline flag: assertRegex's third positional arg is
        # `msg`, not `flags`, so a passed re.M is silently discarded.
        self.assertRegex(self.lessons, r"(?m)^- 20\d\d-\d\d-\d\d \(M\d+")

    def test_no_graduation_breadcrumb_was_left_behind(self):
        # D-051 rejected an in-file graduation breadcrumb; D-055 keeps that.
        # The retired module's name is spelled split so AC2-style reference
        # sweeps for it stay clean while the probe still matches a breadcrumb.
        self.assertNotIn("guard-" + "doctrine.md", self.lessons)

    def test_partial_coverage_was_trimmed_not_deleted(self):
        # Two items were only partly covered by the module; their uncovered
        # remainders stay, marked as trimmed (D-051).
        self.assertIn("trimmed M92/M98", self.lessons)
        self.assertIn("trimmed M98", self.lessons)
        self.assertIn("age a synthesis note from its OLDEST un-re-read input", self.lessons)
        self.assertIn("sync a feature branch with `git rebase main` instead", self.lessons)


if __name__ == "__main__":
    unittest.main()
