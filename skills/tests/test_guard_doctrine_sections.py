"""M127: guard-doctrine.md's sections after §8's retirement — the numbering,
gapped, and §9's surviving doctrine.

M127 removed §8 (the description-layer certification step) whole and kept §9
under its own number — retired numbers are never reused, exactly as milestone
IDs and IP/GP numbers stay retired. The (number, title) pairs are pinned, not
the numbers alone: M124's certification measured that number-only pinning is
insufficient — swapping two sections' bodies while relabelling the numbers
preserves an unbroken sequence and ships green while silently staling every
cross-file citation of the swapped pair. Committed expected output, compared
against what the file says now.

`TestSectionNineDoctrine` re-homes the §9 content pins that were collateral
of deleting `test_section_ledger.py` whole (M127 review F1: that file's §9
doctrine class was not §8 ledger machinery, and §9 survives). Anchors are
copied from the shipped bytes — the M127-rewritten tail included — with
cross-wrap phrases matched via `\\s+` (M105) and each anchor opening on the
subject that carries the rule (M123 round 4's lesson).

The guard reads its target per test, never at class level (M61), via
`Path.read_text` because the mutation engine patches only that call (M100).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import unittest

GUARD_DOCTRINE = (
    pathlib.Path(__file__).resolve().parent.parent
    / "shared" / "guard-doctrine.md"
)


def section9():
    """§9's own bytes, heading to EOF (it is the last section)."""
    text = GUARD_DOCTRINE.read_text()
    head = "## 9. Presence is not consistency"
    if head not in text:
        raise AssertionError(f"guard-doctrine.md has no {head!r} section")
    return text[text.index(head):]


class TestSectionNumbering(unittest.TestCase):
    def test_the_sections_are_numbered_with_eight_retired(self):
        headings = re.findall(
            r"^## (\d+)\. (.+)$", GUARD_DOCTRINE.read_text(), re.M
        )
        self.assertEqual(headings, [
            ("1", "What an assert must pin"),
            ("2", "What the mutation harness does and does not catch"),
            ("3", "Absence assertions"),
            ("4", "Fixtures"),
            ("5", "Matchers and parsers over human-written markdown"),
            ("6", "Restatement, and numbers"),
            ("7", "Scoping a sweep or a grep-shaped criterion"),
            ("9", "Presence is not consistency"),
        ])


class TestSectionNineDoctrine(unittest.TestCase):
    """Every rule §9 still ships, pinned — re-homed from the deleted
    `test_section_ledger.py` and re-anchored to the post-M127 bytes."""

    def test_presence_is_distinguished_from_consistency(self):
        self.assertRegex(
            section9(),
            r"\*\*A\s+prose-guard\s+pins\s+that\s+a\s+sentence\s+is\s+present\.\s+It\s+"
            r"does\s+not\s+pin\s+that\s+the\s+section\s+around\s+it\s+still\s+agrees\s+"
            r"with\s+itself\.\*\*",
        )

    def test_the_three_shapes_are_declared_as_three(self):
        self.assertRegex(
            section9(),
            r"An\s+anchor\s+is\s+a\s+claim\s+about\s+a\s+sentence;\s+a\s+rule\s+is"
            r"\s+a\s+claim\s+the\s+section\s+makes\.\s+They\s+come\s+apart\s+three"
            r"\s+ways\.",
        )

    def test_the_contradicting_sentence_shape_is_named(self):
        self.assertRegex(
            section9(),
            r"\*\*A\s+contradicting\s+sentence\s+added\s+elsewhere\s+in\s+the\s+"
            r"section\.\*\*[\s\S]{0,200}?the\s+section\s+now\s+says\s+both",
        )

    def test_the_rename_shape_is_named(self):
        # Anchor spans the polarity carrier: "is defeated by" (M123 round 4's
        # lesson, carried over from the deleted original).
        self.assertRegex(
            section9(),
            r"\*\*A\s+rename\s+reusing\s+no\s+word\s+of\s+the\s+term\.\*\*[\s\S]{0,160}?"
            r"is\s+defeated\s+by\s+a\s+coinage\s+sharing\s+neither",
        )

    def test_the_relocation_shape_is_named(self):
        self.assertRegex(
            section9(),
            r"\*\*A\s+relocation\s+falsifying\s+a\s+back-reference\.\*\*[\s\S]{0,120}?"
            r"true\s+of\s+a\s+position,\s+not\s+of\s+a\s+phrase",
        )

    def test_the_check_is_derived_never_enumerated(self):
        self.assertRegex(
            section9(),
            r"\*\*So\s+derive\s+the\s+check\s+from\s+the\s+section,\s+never\s+from\s+a"
            r"\s+list\s+of\s+what\s+to\s+look\s+for\.\*\*",
        )

    def test_no_section_term_reached_the_extractor(self):
        # The rewritten (retrospective) form of the deleted original's pin.
        self.assertRegex(
            section9(),
            r"with\s+no\s+term\s+drawn\s+from\s+the\s+section\s+"
            r"written\s+into\s+the\s+extractor\s+—\s+so\s+a\s+coinage\s+nobody\s+"
            r"anticipated\s+was\s+still\s+a\s+difference",
        )

    def test_the_judgment_disclaimer_survives_the_rewrite(self):
        self.assertRegex(
            section9(),
            r"is\s+not\s+a\s+question\s+a\s+diff\s+can\s+answer,\s+and\s+building"
            r"\s+it\s+to\s+answer\s+one\s+would\s+rebuild\s+the\s+judgment\s+D-059"
            r"\s+retired",
        )

    def test_the_defeating_failure_mode_is_still_disclosed(self):
        self.assertRegex(
            section9(),
            r"The\s+one\s+failure\s+mode\s+that\s+defeated\s+the\s+instrument\s+was"
            r"\s+a\s+ledger\s+updated\s+without\s+its\s+diff\s+being\s+read,\s+which"
            r"\s+no\s+guard\s+can\s+detect",
        )

    def test_the_closing_paragraph_records_the_deletion_and_its_home(self):
        # M127 review H3: the new closing record shipped unpinned. Both the
        # git-home clause and the tests-only-itself ground are load-bearing —
        # they are what a later reader restores the machinery from, and why
        # it left.
        self.assertRegex(
            section9(),
            r"was\s+deleted\s+with\s+it,\s+restorable\s+from\s+git,\s+because\s+a"
            r"\s+consistency\s+instrument\s+whose\s+only\s+subject\s+is\s+gone\s+"
            r"tests\s+nothing\s+but\s+itself",
        )


if __name__ == "__main__":
    unittest.main()
