"""The `decision heading quality` advisory (M97, D-054).

The bounded DECISIONS read (D-054) decides what to open from the `### D-`
headings alone, so a heading that hides a supersession costs recall the
whole-file sweep used to buy. This advisory reports such headings by id.

Two scoping facts drive every test here:

- **Prospective.** Three legacy headings hide a supersession — D-012 omits
  D-010, D-014 omits D-013, D-019 omits D-003 — and IP4 forbids repairing
  them. The advisory starts at `HEADING_QUALITY_FROM` so it can reach OK on
  the real file; an advisory that can never go green is one people learn to
  ignore.
- **WARN, never FAIL.** Heading quality is a judgment about prose, the same
  call `record density` and `references staleness` already make (D-049/D-052).

Tests assert against the classifier itself, never only the rendered report
(M93): a filtered channel makes an absence-assert unfalsifiable. Every
absence-assert is paired with a positive signal that the path actually ran
(M84) — a crash returning `[]` would otherwise read as a clean file.

    python3 -m unittest discover -s scripts/tests -v
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cairn_validate as cv  # noqa: E402


GOOD = """# Decisions

### D-100 (2026-07-19): A subject that stands alone — supersedes D-031

**Decision:** Supersedes D-031's earlier reading.
"""

BAD = """# Decisions

### D-100 (2026-07-19): A subject that stands alone

**Decision:** Supersedes D-031's earlier reading.
"""

LEGACY_BAD = """# Decisions

### D-012 (2026-07-11): Phase headers shift up one level

**Consequences:** Supersedes D-010's level choice.
"""

NON_CLAIMS = """# Decisions

### D-100 (2026-07-19): A subject that stands alone

**Context:** The entomb-verbatim rule (D-005) is the precedent here, and it
is a symmetric move to D-028.
**Consequences:** Leaves D-049's thresholds untouched. If that ever needs
changing, this is the entry to supersede. A weakening requires a superseding
D-entry.
"""


def write(tmp, text):
    d = os.path.join(tmp, "cairn")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "DECISIONS.md"), "w", encoding="utf-8") as f:
        f.write(text)
    return tmp


class TestClassifier(unittest.TestCase):
    """Direct tests of the classifier, not of the rendered report (M93)."""

    def test_heading_naming_its_supersession_is_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cv.check_decision_heading_quality(write(tmp, GOOD)), [])

    def test_heading_omitting_its_supersession_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = cv.check_decision_heading_quality(write(tmp, BAD))
        # Positive signal: the path ran and produced a finding (M84) — an
        # empty list here would be indistinguishable from a crash.
        self.assertEqual(len(out), 1)
        # The finding names the offending entry AND the omitted one, so the
        # report is actionable rather than a bare count (AC3).
        self.assertIn("D-100", out[0])
        self.assertIn("D-031", out[0])

    def test_legacy_entries_are_out_of_scope(self):
        # D-012 genuinely hides a supersession; IP4 forbids fixing it, so the
        # advisory must not report it. Paired with the BAD case above, which
        # proves the classifier fires at all — otherwise this passes vacuously.
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                cv.check_decision_heading_quality(write(tmp, LEGACY_BAD)), []
            )

    def test_incidental_mentions_are_not_claims(self):
        # The three false-positive shapes found on the real file: a cited
        # precedent, a "symmetric move to", a "leaves X untouched", and the
        # forward-looking "entry to supersede" / "a superseding D-entry".
        with tempfile.TemporaryDirectory() as tmp:
            out = cv.check_decision_heading_quality(write(tmp, NON_CLAIMS))
        self.assertEqual(out, [])

    def test_missing_file_is_silent(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(cv.check_decision_heading_quality(tmp), [])


class TestRealFile(unittest.TestCase):
    """Runs over the REAL cairn/DECISIONS.md, never a fixture copy (M77/M80)."""

    @property
    def root(self):
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    def test_real_decisions_file_is_clean(self):
        out = cv.check_decision_heading_quality(self.root)
        self.assertEqual(out, [], "in-scope headings hide a supersession: %r" % out)

    def test_real_file_actually_has_in_scope_entries(self):
        # Pairs with the assertion above (M84): "clean" is only meaningful if
        # the advisory had entries in scope to judge. When this fails, the
        # cleanliness result above has become vacuous.
        path = os.path.join(self.root, "cairn", "DECISIONS.md")
        with open(path, encoding="utf-8") as f:
            ids = cv._DQ_HEADING.findall(f.read())
        in_scope = [i for i in ids if int(i) >= cv.HEADING_QUALITY_FROM]
        self.assertTrue(
            in_scope, "no entry at or past D-%03d — advisory is vacuous"
            % cv.HEADING_QUALITY_FROM
        )


    def test_scope_is_the_only_thing_suppressing_the_legacy_findings(self):
        # The strongest available proof that the advisory is not vacuously
        # silent: drop the prospective scope and the classifier must find
        # exactly the three known legacy gaps on the REAL file — and none of
        # the three shapes that merely mention a D-id (D-029's "symmetric move
        # to D-028", D-032's cited D-005, D-052's "leaves D-049 untouched").
        original = cv.HEADING_QUALITY_FROM
        try:
            cv.HEADING_QUALITY_FROM = 1
            out = cv.check_decision_heading_quality(self.root)
        finally:
            cv.HEADING_QUALITY_FROM = original
        found = sorted(f.split(":")[0] for f in out)
        self.assertEqual(found, ["D-012", "D-014", "D-019"])


class TestWiring(unittest.TestCase):
    def test_registered_as_an_advisory_not_a_check(self):
        names = [n for n, _ in cv.ADVISORIES]
        self.assertIn("decision heading quality", names)
        self.assertNotIn(
            "decision heading quality", [n for n, _ in cv.CHECKS]
        )

    def test_advisory_never_changes_the_exit_code(self):
        # WARN tier: findings must not fail the gate (D-049/D-052 severity
        # split). Asserted through run(), which is where the exit code is set.
        with tempfile.TemporaryDirectory() as tmp:
            write(tmp, BAD)
            for name in ("ROADMAP.md",):
                open(os.path.join(tmp, "cairn", name), "w").close()
            report, failures = cv.run(tmp)
        self.assertIn("decision heading quality", report)
        self.assertIn("WARN", report)


if __name__ == "__main__":
    unittest.main()
