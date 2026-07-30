"""M124: the section-consistency ledger, and the extractor behind it.

A prose-guard pins that a sentence is present. `guard-doctrine.md` §9 states
why that is not the same as the section staying consistent with itself, and
this file is the enforcement: `guard-doctrine.md` §8's sentence sequence is
committed to `ledgers/guard-doctrine-8.txt`, and `TestSectionEightLedger`
fails when the section and the ledger disagree.

The guard catches what an anchor cannot — measured against the four mutations
M123's certification recorded. Two of them already red the shipped suite by
other means and are carried here as controls; the other two, a contradicting
sentence appended to the mandate paragraph and a relocation of the three-checks
list, defeat all 777 pre-existing tests and are what this guard is for.

`TestExtraction` and `TestAlignment` cover the helper. The extractor takes no
list of terms, phrases, or subjects from the section it reads — that
enumeration is the failure `guard-doctrine.md` §3 names, and over §8 alone it
has already beaten five successive hand-extended matchers. Its only lexical
constant is a punctuation class, and `test_extraction_carries_no_word_constant`
holds that to the shipped bytes rather than to intent.

The ledger is deliberately NOT passed into the extractor: the extraction is
committed output compared downstream, so it cannot be tuned to agree with what
it is checked against.

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import tempfile
import unittest

import section_ledger as sl

TESTS = pathlib.Path(__file__).resolve().parent
GUARD_DOCTRINE = TESTS.parent / "shared" / "guard-doctrine.md"
LEDGER = TESTS / "ledgers" / "guard-doctrine-8.txt"
SECTION_8 = "## 8. The author never certifies its own guard's coverage"


def committed_ledger():
    return LEDGER.read_text().splitlines()


class TestSectionEightLedger(unittest.TestCase):
    """The prose-guard: §8 must still say exactly what the ledger records."""

    def test_section_matches_its_ledger(self):
        current = sl.sentences(GUARD_DOCTRINE, SECTION_8)
        report = sl.describe(committed_ledger(), current)
        self.assertEqual(report, "", report)

    def test_the_ledger_is_not_empty(self):
        # A guard whose corpus is empty passes for free — the failure
        # `guard-doctrine.md` §7 names, and the one M114's fork detector died
        # of. An empty ledger would agree with an empty section.
        self.assertGreater(len(committed_ledger()), 40)

    def test_the_failure_message_names_what_differs(self):
        # The message IS the remedy §9 assigns: the author reads the diff.
        # A guard that failed without saying what moved would leave the author
        # regenerating and re-committing blind.
        ledger = committed_ledger()
        report = sl.describe(ledger, ledger[:-1] + ["A sentence nothing pins."])
        self.assertIn("ADDED   A sentence nothing pins.", report)
        self.assertIn("REMOVED", report)
        self.assertIn("regenerate the ledger and read this diff", report)


class TestExtraction(unittest.TestCase):
    def _tmp(self, text):
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        )
        handle.write(text)
        handle.close()
        return pathlib.Path(handle.name)

    def test_heading_is_excluded_from_the_body(self):
        # Including it splits `## 8.` off as a spurious first "sentence",
        # because the heading ends in a numeral-period. Measured: 51 units with
        # the heading, 50 without.
        path = self._tmp("## 3. A title\n\nOne. Two.\n")
        self.assertNotIn("## 3.", sl.section_body(path, "## 3. A title"))
        self.assertEqual(sl.sentences(path, "## 3. A title"), ["One.", "Two."])

    def test_body_bounds_at_the_next_section(self):
        path = self._tmp("## 3. A\n\nInside.\n\n## 4. B\n\nOutside.\n")
        self.assertEqual(sl.sentences(path, "## 3. A"), ["Inside."])

    def test_body_runs_to_eof_when_the_section_is_last(self):
        # §8 was the last section until M124 appended §9; both bounds ship.
        path = self._tmp("## 3. A\n\nOnly. Sentences.\n")
        self.assertEqual(sl.sentences(path, "## 3. A"), ["Only.", "Sentences."])

    def test_a_reflow_that_preserves_tokens_yields_the_same_sequence(self):
        # The property that makes the ledger usable: re-wrapping prose must not
        # red a rule still present (M105's false-red). Both bodies below carry
        # the identical tokens at different wrap points.
        wide = self._tmp("## 3. A\n\nOne sentence that is wrapped here. Two.\n")
        narrow = self._tmp("## 3. A\n\nOne sentence\nthat is wrapped\nhere. Two.\n")
        self.assertEqual(
            sl.sentences(wide, "## 3. A"), sl.sentences(narrow, "## 3. A")
        )

    def test_a_hyphen_break_is_a_real_difference(self):
        # The converse, and the reason M124's criterion says "token sequence
        # unchanged" rather than "no word changed": a wrap that breaks a
        # hyphenated compound changes the tokens, and §8 is dense with them.
        joined = self._tmp("## 3. A\n\nThe zero-unresolved bar.\n")
        broken = self._tmp("## 3. A\n\nThe zero-\nunresolved bar.\n")
        self.assertNotEqual(
            sl.sentences(joined, "## 3. A"), sl.sentences(broken, "## 3. A")
        )

    def test_extraction_carries_no_word_constant(self):
        # AC1: no list of terms, phrases, or subjects drawn from any section's
        # content, as a parameter or a module constant. Checked against the
        # shipped module rather than asserted in prose: every compiled pattern
        # in it must be free of letters, so a content word cannot hide in one.
        # A closed grammatical class would be permitted and would need this
        # test widened with a comment naming the class; none is needed today,
        # which is the fact this pins.
        source = pathlib.Path(sl.__file__).read_text()
        # The `r` prefix sits OUTSIDE the capture group: a first draft included
        # it and the test red on its own raw-string marker, reporting a word
        # constant in `r"\n## "`. The letters checked must be the pattern's, not
        # Python's syntax around it.
        patterns = re.findall(r'^_[A-Z_]+ = re\.compile\(r?(".*?")\)',
                              source, re.M)
        self.assertTrue(patterns, "no module-level patterns found to check")
        for pattern in patterns:
            # Regex escapes are letters to a naive search — `\\s`, `\\n`, `\\w` all
            # trip it, and a first draft red on `\\s+` in the sentence-boundary
            # class. Strip the escapes and check what is left: a content word
            # cannot survive as an escape sequence.
            literal = re.sub(r"\\.", "", pattern)
            self.assertFalse(
                re.search(r"[A-Za-z]", literal),
                f"a module-level pattern carries a word constant: {pattern}",
            )


class TestAlignment(unittest.TestCase):
    def test_agreement_describes_nothing(self):
        self.assertEqual(sl.describe(["A.", "B."], ["A.", "B."]), "")

    def test_a_pure_insertion_reports_one_addition(self):
        # Why alignment and not index comparison: measured on §8, comparing by
        # index reports a one-sentence insertion as `added=1, moved=35`, which
        # buries the real change under every sentence that merely shifted.
        delta = sl.diff(["A.", "B.", "C."], ["A.", "N.", "B.", "C."])
        self.assertEqual(delta["added"], ["N."])
        self.assertEqual(delta["removed"], [])
        self.assertEqual(delta["moved"], [])

    def test_a_relocation_reports_a_move(self):
        # The third defeat shape §9 names: a list moved out from under its
        # back-reference. Nothing is added or removed, so a guard reporting
        # only additions and deletions would call this "no change".
        delta = sl.diff(["A.", "B.", "C."], ["B.", "C.", "A."])
        self.assertIn("A.", delta["moved"])
        self.assertEqual(delta["added"], [])
        self.assertEqual(delta["removed"], [])

    def test_a_substitution_reports_both_sides(self):
        delta = sl.diff(["A.", "B."], ["A.", "Z."])
        self.assertEqual(delta["added"], ["Z."])
        self.assertEqual(delta["removed"], ["B."])


if __name__ == "__main__":
    unittest.main()
