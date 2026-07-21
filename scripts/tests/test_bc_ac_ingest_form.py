"""The binding-criterion ingest FORM and its interaction with two checks (M107).

milestone-brief ingests each of a Driving RR's Binding criteria verbatim into
the constrained milestone's `## Acceptance criteria`. `check_binding_criteria`
(M100) only needs the verbatim BC body *somewhere* in that section, so any
shape satisfies it. But `check_coverage_complete` (M34) is POSITIONAL: it
counts every `- [ ]` item in the AC section and demands Coverage reference
AC1..ACn. So a BC ingested as a bare checkbox pushes n past the mapped set and
reds `coverage-complete` — the intraclass failure, where six ingested BCs
counted as AC8..AC13 with no Coverage line.

M107's resolution is a FORM, not a code change: ingest each BC as a numbered
acceptance criterion carrying its trace tag — `- [ ] AC-N (BCn): <verbatim>` —
and add its Coverage line. These tests pin both verdicts: the prescribed form
is quiet on BOTH checks; the bare-ingest shape reds `coverage-complete` while
`binding criteria` stays quiet (so the binding check alone cannot catch it).

    python3 -m unittest discover -s scripts/tests -v
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cairn_validate as cv  # noqa: E402


BC1 = ("The frobnicator rejects negative input with a typed error and a "
       "message naming the offending argument.")
BC2 = "The gate prints measured-vs-projected side by side before approval."

RR_BODY = (
    "# RR05: Fixture review\n\n"
    "## Binding criteria\n\n"
    f"- BC1: {BC1}\n"
    f"- BC2: {BC2}\n"
)

SLOT = "- **Driving RR:** RR05\n"


def milestone(ac_body, coverage_body):
    return (
        "# M50: Fixture\n\n"
        f"- **Status:** in-progress\n{SLOT}"
        "- **Principles touched:** —\n\n"
        "## Goal\n\nA fixture.\n\n"
        "## Acceptance criteria\n\n" + ac_body + "\n"
        "## Coverage\n\n" + coverage_body + "\n"
        "## Tasks\n\n- [ ] T1: do it\n"
    )


# Prescribed form: a normal AC1 plus the two BCs ingested as numbered criteria
# carrying their (BCn) trace tag, each given a Coverage line.
AC_PRESCRIBED = (
    "- [ ] AC1: the normal criterion the milestone already had.\n"
    f"- [ ] AC2 (BC1): {BC1}\n"
    f"- [ ] AC3 (BC2): {BC2}\n"
)
COV_PRESCRIBED = "- AC1 → T1\n- AC2 → T1\n- AC3 → T1\n"

# The intraclass mistake: the BC bodies are pasted verbatim as bare checkboxes,
# neither numbered nor added to Coverage. The verbatim text is still present,
# so the binding check is satisfied — but n=3 while Coverage maps only AC1.
AC_BARE = (
    "- [ ] AC1: the normal criterion the milestone already had.\n"
    f"- [ ] {BC1}\n"
    f"- [ ] {BC2}\n"
)
COV_BARE = "- AC1 → T1\n"


def build(tmp, ac_body, coverage_body):
    md = os.path.join(tmp, "cairn", "milestones")
    os.makedirs(md, exist_ok=True)
    with open(os.path.join(md, "M50-fixture.md"), "w", encoding="utf-8") as f:
        f.write(milestone(ac_body, coverage_body))
    rd = os.path.join(tmp, "cairn", "reviews")
    os.makedirs(rd, exist_ok=True)
    with open(os.path.join(rd, "RR05-fixture.md"), "w", encoding="utf-8") as f:
        f.write(RR_BODY)
    return tmp


class TestPrescribedFormIsQuietOnBoth(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = build(self.tmp.name, AC_PRESCRIBED, COV_PRESCRIBED)

    def tearDown(self):
        self.tmp.cleanup()

    def test_binding_criteria_quiet(self):
        self.assertEqual(cv.check_binding_criteria(self.root), [])

    def test_coverage_complete_quiet(self):
        self.assertEqual(cv.check_coverage_complete(self.root), [])


class TestBareIngestRedsCoverageOnly(unittest.TestCase):
    """The regression: pinned to red before M107's form prescription existed.
    A BC pasted as a bare checkbox satisfies `binding criteria` yet reds
    `coverage-complete`, which is exactly why binding enforcement alone did not
    protect the intraclass session."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = build(self.tmp.name, AC_BARE, COV_BARE)

    def tearDown(self):
        self.tmp.cleanup()

    def test_binding_criteria_stays_quiet(self):
        # The verbatim BC bodies are present, so the binding check is content.
        self.assertEqual(cv.check_binding_criteria(self.root), [])

    def test_coverage_complete_fires_on_the_unmapped_bcs(self):
        out = cv.check_coverage_complete(self.root)
        # n=3 criteria, Coverage maps only AC1 -> AC2 and AC3 unreferenced.
        joined = "\n".join(out)
        self.assertIn("AC2", joined)
        self.assertIn("AC3", joined)
        self.assertTrue(all("AC1 " not in line for line in out),
                        "the mapped AC1 must not be reported")

    def test_numbering_and_mapping_together_clear_the_red(self):
        # Positive twin: the same milestone under the prescribed form is quiet,
        # proving the form (numbering + Coverage line) is what resolves it.
        root = build(tempfile.mkdtemp(), AC_PRESCRIBED, COV_PRESCRIBED)
        self.assertEqual(cv.check_coverage_complete(root), [])
        self.assertEqual(cv.check_binding_criteria(root), [])


if __name__ == "__main__":
    unittest.main()
