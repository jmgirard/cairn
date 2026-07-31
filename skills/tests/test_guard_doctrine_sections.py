"""M127: guard-doctrine.md's section numbering, gapped at the retired §8.

M127 removed §8 (the description-layer certification step) whole and kept §9
under its own number — retired numbers are never reused, exactly as milestone
IDs and IP/GP numbers stay retired. The (number, title) pairs are pinned, not
the numbers alone: M124's certification measured that number-only pinning is
insufficient — swapping two sections' bodies while relabelling the numbers
preserves an unbroken sequence and ships green while silently staling every
cross-file citation of the swapped pair. Committed expected output, compared
against what the file says now.

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


if __name__ == "__main__":
    unittest.main()
