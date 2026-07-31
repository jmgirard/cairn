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

import ast
import inspect
import pathlib
import re
import tempfile
import unittest

import section_ledger as sl

TESTS = pathlib.Path(__file__).resolve().parent
GUARD_DOCTRINE = TESTS.parent / "shared" / "guard-doctrine.md"
LEDGER = TESTS / "ledgers" / "guard-doctrine-8.txt"
SECTION_8 = "## 8. The author never certifies its own guard's coverage"
SECTION_9 = "## 9. Presence is not consistency"


def committed_ledger():
    return LEDGER.read_text().splitlines()


def section9():
    """§9's own bytes, scoped to §9.

    Scoped deliberately. M123's §8 asserts each read the whole FILE while every
    criterion they served was scoped to the section, so clauses of AC2, AC3,
    AC5 and AC11 could be moved verbatim out of §8 into §7 with the suite green
    and no anchor text touched — a defect M123 records as shared by ~75
    anchors. An anchor proves a phrase exists SOMEWHERE in what it was handed;
    these are handed §9 alone.
    """
    return sl.section_body(GUARD_DOCTRINE, SECTION_9)


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

    def test_the_extraction_signature_takes_only_a_path_and_a_heading(self):
        # AC1 bans a content-drawn enumeration "as a parameter" and AC2 requires
        # the ledger be "never passed into the extraction". Certification round
        # 1 measured both unpinned: adding
        # `terms=("fix-authored record", "shielded entry")` to `sentences`, or a
        # `ledger=None` parameter, each left the suite at 800 tests OK. The
        # signature is the surface both clauses are about, so pin the signature.
        for func in (sl.section_body, sl.sentences):
            self.assertEqual(
                tuple(inspect.signature(func).parameters), ("path", "heading"),
                f"{func.__name__} takes something beyond a path and a heading; "
                f"AC1 bans a content enumeration as a parameter and AC2 bans "
                f"the ledger reaching the extraction",
            )

    def test_each_module_constant_names_the_class_it_closes_over(self):
        # AC1's third clause. Round 1 measured it unpinned: deleting the whole
        # comment block above `_SENTENCE_BOUNDARY` left the suite green, while
        # the clause is live — one closed punctuation class does ship.
        source = pathlib.Path(sl.__file__).read_text().splitlines()
        constants = [
            i for i, line in enumerate(source)
            if re.match(r"^_[A-Z_]+ = ", line)
        ]
        self.assertTrue(constants, "no module-level constants found to check")
        for i in constants:
            preceding = [
                source[j] for j in range(i - 1, -1, -1)
                if source[j].startswith("#") or not source[j].strip()
            ][:1]
            self.assertTrue(
                preceding and preceding[0].startswith("#"),
                f"{source[i]!r} carries no comment naming the class it closes "
                f"over, which AC1 requires of every permitted constant",
            )

    def test_extraction_carries_no_word_constant(self):
        # AC1: no list of terms, phrases, or subjects drawn from any section's
        # content, as a parameter or a module constant. Checked against the
        # shipped module rather than asserted in prose: every compiled pattern
        # in it must be free of letters, so a content word cannot hide in one.
        # A closed grammatical class would be permitted and would need this
        # test widened with a comment naming the class; none is needed today,
        # which is the fact this pins.
        # Round 1: this scanned `re.compile` assignments ONLY, so inserting
        # `_TERMS = ["fix-authored record", "shielded entry"]` at module level
        # left the suite at 800 tests OK — the exact enumeration AC1 bans,
        # invisible to the test meant to ban it. Parsed with `ast` now, so
        # every module-level assignment is reached whatever shape it takes,
        # rather than the one shape the author thought to match.
        tree = ast.parse(pathlib.Path(sl.__file__).read_text())
        patterns = [
            node.value
            for stmt in tree.body if isinstance(stmt, ast.Assign)
            for node in ast.walk(stmt)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        ]
        self.assertTrue(patterns, "no module-level string constants to check")
        for pattern in patterns:
            # Regex escapes are letters to a naive search — `\\s`, `\\n`, `\\w` all
            # trip it, and a first draft red on `\\s+` in the sentence-boundary
            # class. Strip the escapes and check what is left: a content word
            # cannot survive as an escape sequence.
            literal = re.sub(r"\\.", "", pattern)  # noqa: escapes are not words
            self.assertFalse(
                re.search(r"[A-Za-z]", literal),
                f"a module-level pattern carries a word constant: {pattern}",
            )


class TestSectionNineDoctrine(unittest.TestCase):
    """Every rule §9 adds, pinned. Anchors copied from the shipped bytes (M95),
    every cross-wrap phrase matched with `\\s+` so a reflow does not red a rule
    still present (M105), and each opens on the SUBJECT rather than after it —
    M123 round 4 found three anchors that opened past the clause carrying the
    rule, leaving the rule itself invertible with the suite green."""

    def test_section_exists_under_its_own_heading(self):
        self.assertIn(SECTION_9, GUARD_DOCTRINE.read_text())

    def test_presence_is_distinguished_from_consistency(self):
        self.assertRegex(
            section9(),
            r"\*\*A\s+prose-guard\s+pins\s+that\s+a\s+sentence\s+is\s+present\.\s+It\s+"
            r"does\s+not\s+pin\s+that\s+the\s+section\s+around\s+it\s+still\s+agrees\s+"
            r"with\s+itself\.\*\*",
        )

    def test_the_contradicting_sentence_shape_is_named(self):
        self.assertRegex(
            section9(),
            r"\*\*A\s+contradicting\s+sentence\s+added\s+elsewhere\s+in\s+the\s+"
            r"section\.\*\*[\s\S]{0,200}?the\s+section\s+now\s+says\s+both",
        )

    def test_the_rename_shape_is_named(self):
        self.assertRegex(
            section9(),
            r"\*\*A\s+rename\s+reusing\s+no\s+word\s+of\s+the\s+term\.\*\*[\s\S]{0,160}?"
            r"defeated\s+by\s+a\s+coinage\s+sharing\s+neither",
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

    def test_no_section_term_reaches_the_extractor(self):
        self.assertRegex(
            section9(),
            r"No\s+term\s+drawn\s+from\s+the\s+section\s+is\s+written\s+into\s+the\s+"
            r"extractor,\s+so\s+a\s+coinage\s+nobody\s+anticipated\s+is\s+still\s+a\s+"
            r"difference",
        )

    def test_the_instrument_detects_and_never_judges(self):
        self.assertRegex(
            section9(),
            r"\*\*The\s+instrument\s+detects\s+a\s+change\s+and\s+never\s+judges\s+it\.\*\*",
        )

    def test_the_remedy_is_operation_never_adjudication(self):
        # AC5's clause, and the one criteria-audit pass 4 found underdetermined:
        # a §9 attributing the remedy to the INSTRUMENT would satisfy "states
        # the remedy" while falsifying the detect-never-judge clause above.
        self.assertRegex(
            section9(),
            r"\*\*The\s+remedy\s+is\s+operation\s+the\s+author\s+runs,\s+never\s+"
            r"adjudication\s+the\s+guard\s+performs\.\*\*",
        )

    def test_the_remedy_names_its_three_steps(self):
        # AC5 requires §9 state the remedy as operation the author RUNS, and
        # criteria-audit pass 4 added that clause precisely because a §9 stating
        # only the headline would satisfy "states the remedy" while leaving the
        # operation unspecified. Round 1 then measured the steps unpinned:
        # deleting the sentence carrying them left the suite at 800 tests OK,
        # with §8's routing enumerations pointing findings at a remedy §9 had
        # stopped stating.
        self.assertRegex(
            section9(),
            r"discharged\s+by\s+regenerating\s+it,\s+reading\s+the\s+reported"
            r"\s+diff\s+sentence\s+by\s+sentence,\s+and\s+then\s+repairing\s+"
            r"the\s+section\s+or\s+accepting\s+the\s+change",
        )

    def test_the_defeating_failure_mode_is_disclosed(self):
        self.assertRegex(
            section9(),
            r"failure\s+mode\s+that\s+defeats\s+the\s+instrument\s+is\s+a\s+ledger\s+"
            r"updated\s+without\s+its\s+diff\s+being\s+read,\s+and\s+no\s+guard\s+can\s+"
            r"detect\s+that",
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

    def test_the_failure_message_names_a_move(self):
        # AC2's third reported category. Round 1 measured it unpinned: dropping
        # "moved" from `describe`'s loop left the suite at 800 tests OK, so a
        # relocation — the third defeat shape §9 names — would have failed the
        # guard with an empty message body. `TestAlignment` exercised `diff`,
        # never `describe`, which is where the message is rendered.
        report = sl.describe(["A.", "B.", "C."], ["B.", "C.", "A."])
        self.assertIn("MOVED   A.", report)

    def test_a_substitution_reports_both_sides(self):
        delta = sl.diff(["A.", "B."], ["A.", "Z."])
        self.assertEqual(delta["added"], ["Z."])
        self.assertEqual(delta["removed"], ["B."])


if __name__ == "__main__":
    unittest.main()
