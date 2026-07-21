"""The `binding criteria` CHECK (M100, RR04 rec 8).

A review finding softened by the session implementing it is the failure this
check exists to stop: an RR's Binding criteria must appear verbatim
(whitespace-normalized) in the constrained milestone's Acceptance criteria
section, or be named in its "Deviations from RR<NN>" table. The check FAILs
the gate — a softened criterion is a red check, not a reading.

Fixtures vary each axis independently (M57/M81) and prove the check reddens
for EACH input it covers (M90): verbatim-but-rewrapped, softened bare,
softened-but-tabled, no slot, em-dash slot, RR without the section, missing
RR file, archived RR, and mixed verbatim/softened criteria.

    python3 -m unittest discover -s scripts/tests -v
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cairn_validate as cv  # noqa: E402


RR_BODY = """# RR05: Fixture review

## Answers

Prose the check must ignore.

## Binding criteria

Preamble prose before the first item is not a criterion.

- BC1: The frobnicator rejects negative input with a typed error and a
  message naming the offending argument.
- BC2: The gate prints measured-vs-projected side by side before approval.

## Recommendations

- BC3: not a criterion — outside the section.
"""

RR_NO_SECTION = """# RR05: Fixture review

## Answers

No binding criteria anywhere.
"""


def milestone(slot, ac_body):
    return (
        "# M50: Fixture\n\n"
        f"- **Status:** in-progress\n{slot}"
        "- **Principles touched:** —\n\n"
        "## Goal\n\nA fixture.\n\n"
        "## Acceptance criteria\n\n" + ac_body + "\n\n"
        "## Tasks\n\n- [ ] T1: do it\n"
    )


SLOT = "- **Driving RR:** RR05\n"
NO_SLOT = ""
DASH_SLOT = "- **Driving RR:** —\n"

# BC1's text re-wrapped at different points, checkbox-framed: verbatim under
# whitespace normalization.
AC_VERBATIM = (
    "- [ ] AC1: The frobnicator rejects negative\n"
    "      input with a typed error and a message naming the offending\n"
    "      argument.\n"
    "- [ ] AC2: The gate prints measured-vs-projected side by side before\n"
    "      approval.\n"
)

# BC1 softened ("typed error" dropped), BC2 verbatim.
AC_SOFTENED = (
    "- [ ] AC1: The frobnicator rejects negative input with an error.\n"
    "- [ ] AC2: The gate prints measured-vs-projected side by side before\n"
    "      approval.\n"
)

AC_SOFTENED_TABLED = AC_SOFTENED + (
    "\nDeviations from RR05:\n\n"
    "| BC | departure |\n|---|---|\n"
    "| BC1 | typed-error requirement dropped: profile has no error typing |\n"
)


def build(tmp, ac_body, slot=SLOT, rr_body=RR_BODY, rr_dir="reviews",
          rr_name="RR05-fixture.md"):
    md = os.path.join(tmp, "cairn", "milestones")
    os.makedirs(md, exist_ok=True)
    with open(os.path.join(md, "M50-fixture.md"), "w", encoding="utf-8") as f:
        f.write(milestone(slot, ac_body))
    if rr_body is not None:
        rd = os.path.join(tmp, "cairn", rr_dir)
        os.makedirs(rd, exist_ok=True)
        with open(os.path.join(rd, rr_name), "w", encoding="utf-8") as f:
            f.write(rr_body)
    return tmp


class TestBindingCriteria(unittest.TestCase):
    def check(self, **kw):
        with tempfile.TemporaryDirectory() as tmp:
            return cv.check_binding_criteria(build(tmp, **kw))

    def test_verbatim_rewrapped_is_quiet(self):
        self.assertEqual(self.check(ac_body=AC_VERBATIM), [])

    def test_softened_criterion_fires_naming_the_bc(self):
        out = self.check(ac_body=AC_SOFTENED)
        self.assertEqual(len(out), 1)
        self.assertIn("BC1", out[0])
        self.assertIn("RR05", out[0])

    def test_softened_but_tabled_is_quiet(self):
        self.assertEqual(self.check(ac_body=AC_SOFTENED_TABLED), [])

    def test_bc_reference_before_the_marker_does_not_count(self):
        # A stray "BC1" above the Deviations marker is not a tabled deviation.
        body = AC_SOFTENED.replace(
            "an error.", "an error (was BC1)."
        )
        out = self.check(ac_body=body)
        self.assertEqual(len(out), 1, "pre-marker BC token must not excuse")

    def test_no_slot_is_quiet_even_with_softened_ac(self):
        # Absence-assert paired with its positive twin above (M84): the same
        # softened AC fires when the slot is present.
        self.assertEqual(self.check(ac_body=AC_SOFTENED, slot=NO_SLOT), [])

    def test_dash_slot_is_quiet(self):
        self.assertEqual(self.check(ac_body=AC_SOFTENED, slot=DASH_SLOT), [])

    def test_rr_without_binding_section_binds_nothing(self):
        self.assertEqual(
            self.check(ac_body=AC_SOFTENED, rr_body=RR_NO_SECTION), []
        )

    def test_missing_rr_file_fires(self):
        out = self.check(ac_body=AC_VERBATIM, rr_body=None)
        self.assertEqual(len(out), 1)
        self.assertIn("no file", out[0])

    def test_archived_rr_still_binds(self):
        out = self.check(
            ac_body=AC_SOFTENED,
            rr_dir=os.path.join("reviews", "archive"),
        )
        self.assertEqual(len(out), 1)
        self.assertIn("BC1", out[0])

    def test_only_the_softened_criterion_fires(self):
        out = self.check(ac_body=AC_SOFTENED)
        self.assertTrue(all("BC2" not in line for line in out))

    def test_items_outside_the_section_do_not_bind(self):
        # RR_BODY's BC3 sits under Recommendations; no finding names it.
        out = self.check(ac_body=AC_SOFTENED)
        self.assertTrue(all("BC3" not in line for line in out))


class TestWiring(unittest.TestCase):
    def test_registered_as_a_failing_check_not_an_advisory(self):
        self.assertIn("binding criteria", [label for label, _ in cv.CHECKS])
        self.assertNotIn(
            "binding criteria", [label for label, _ in cv.ADVISORIES]
        )

    def test_current_tree_is_quiet(self):
        # No live milestone names a Driving RR yet; the check must no-op on
        # the real repo so the gate stays green at ship time.
        root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        self.assertEqual(cv.check_binding_criteria(root), [])


if __name__ == "__main__":
    unittest.main()
