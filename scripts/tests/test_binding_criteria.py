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


AC_SOFTENED_COMMENT_TABLED = AC_SOFTENED + (
    "\n<!--\nDeviations from RR05:\n| BC1 | dropped in a comment |\n-->\n"
)

AC_SOFTENED_COMMENT_VERBATIM = AC_SOFTENED + (
    "\n<!-- The frobnicator rejects negative input with a typed error and a "
    "message naming the offending argument. -->\n"
)

RR_BOLD_HEADS = RR_BODY.replace("- BC1:", "- **BC1**:").replace(
    "- BC2:", "- **BC2**:"
)

RR5_BODY = RR_BODY.replace("# RR05", "# RR5")

AC_SOFTENED_RR50_TABLE = AC_SOFTENED + (
    "\nDeviations from RR50:\n\n| BC | departure |\n|---|---|\n"
    "| BC1 | a different review's table |\n"
)


class TestFailLoudAndUnslippable(unittest.TestCase):
    """M100 review F1-F4: the check fails loud, never open, and a departure
    the ingest gate never shows (an HTML comment) can neither excuse nor
    satisfy. Each fixture was confirmed to pass [] against the pre-fix
    check — these are regression tests."""

    def check(self, **kw):
        with tempfile.TemporaryDirectory() as tmp:
            return cv.check_binding_criteria(build(tmp, **kw))

    def test_deviation_hidden_in_comment_does_not_excuse(self):
        out = self.check(ac_body=AC_SOFTENED_COMMENT_TABLED)
        self.assertEqual(len(out), 1)
        self.assertIn("BC1", out[0])

    def test_verbatim_only_inside_comment_does_not_satisfy(self):
        out = self.check(ac_body=AC_SOFTENED_COMMENT_VERBATIM)
        self.assertEqual(len(out), 1)
        self.assertIn("BC1", out[0])

    def test_unparseable_binding_section_fails_loud(self):
        out = self.check(ac_body=AC_VERBATIM, rr_body=RR_BOLD_HEADS)
        self.assertEqual(len(out), 1)
        self.assertIn("no parseable", out[0])

    def test_prefix_rr_table_does_not_excuse(self):
        out = self.check(
            ac_body=AC_SOFTENED_RR50_TABLE,
            slot="- **Driving RR:** RR5\n",
            rr_body=RR5_BODY,
            rr_name="RR5-fixture.md",
        )
        self.assertEqual(len(out), 1)
        self.assertIn("BC1", out[0])

    def test_own_rr_table_still_excuses(self):
        # Positive twin of the prefix case: the same table naming RR5 itself.
        out = self.check(
            ac_body=AC_SOFTENED_RR50_TABLE.replace(
                "Deviations from RR50:", "Deviations from RR5:"
            ),
            slot="- **Driving RR:** RR5\n",
            rr_body=RR5_BODY,
            rr_name="RR5-fixture.md",
        )
        self.assertEqual(out, [])

    def test_malformed_slot_fires(self):
        out = self.check(ac_body=AC_VERBATIM,
                         slot="- **Driving RR:** RR05,\n")
        self.assertEqual(len(out), 1)
        self.assertIn("neither RR<NN> nor —", out[0])


# --- Labeled-bold BC heads: a real RR (circumplex RR09) authored all its
# binding criteria as `- **BC1 (Layer A, reliability).** assertion.` The
# delimiter is the period *inside* the bold; the parseable assertion is the
# text after the closing `.**`, and the parenthetical label is not part of it.
# RR09 is IP4 history in its own repo and cannot be reformatted, so the parser
# reconciles. The twin proves both directions on this newly-accepted form:
# verbatim ACs stay quiet, a softened criterion still fires naming the BC —
# never a silent accept. The M100 fail-loud case (`- **BC1**:`, bold closing
# before any delimiter) stays unparseable; TestFailLoudAndUnslippable owns it.
RR_LABELED_BOLD = """# RR09: Axes reliability review

## Answers

Prose the check must ignore.

## Binding criteria

- **BC1 (Layer A, reliability).** The axes achieve Spearman-Brown
  reliability at or above 0.80 in every octant.
- **BC2 (Layer B, validity).** The projection preserves the rank order of
  the circumplex angles.
"""

RR09_SLOT = "- **Driving RR:** RR09\n"

# Both assertions carried verbatim (checkbox- and BC-labelled, re-wrapped):
# quiet under whitespace normalization. The `(BCn)` AC label and the RR head's
# `(Layer …)` label are both outside the asserted text.
AC_LABELED_VERBATIM = (
    "- [ ] AC1 (BC1): The axes achieve Spearman-Brown reliability at or\n"
    "      above 0.80 in every octant.\n"
    "- [ ] AC2 (BC2): The projection preserves the rank order of the\n"
    "      circumplex angles.\n"
)

# BC1 softened (the 0.80 floor dropped), BC2 verbatim.
AC_LABELED_SOFTENED = (
    "- [ ] AC1 (BC1): The axes achieve decent reliability.\n"
    "- [ ] AC2 (BC2): The projection preserves the rank order of the\n"
    "      circumplex angles.\n"
)


class TestLabeledBoldBindingCriteria(unittest.TestCase):
    """The labeled-bold head `- **BCn (label).** assertion` parses, and the
    check still enforces it verbatim. Positive/negative twin: verbatim ACs
    stay quiet; a softened criterion fires naming its BC and no other. Both
    fixtures were confirmed to MISfire against the pre-fix parser (which read
    the section as unparseable and emitted the 'no parseable' finding for
    every case), so this is a genuine regression pair, not a silent accept."""

    def check(self, ac_body):
        with tempfile.TemporaryDirectory() as tmp:
            return cv.check_binding_criteria(
                build(tmp, ac_body=ac_body, slot=RR09_SLOT,
                      rr_body=RR_LABELED_BOLD, rr_name="RR09-axes.md")
            )

    def test_labeled_bold_parses_into_clean_assertions(self):
        # Proves the parse: the assertion is the text after `.**`, label
        # excluded — so a milestone can carry it verbatim in an AC.
        crits = cv._binding_criteria(RR_LABELED_BOLD)
        self.assertEqual(set(crits), {1, 2})
        self.assertEqual(
            crits[1],
            "The axes achieve Spearman-Brown reliability at or above 0.80 "
            "in every octant.",
        )
        self.assertNotIn("Layer A", crits[1])

    def test_labeled_bold_verbatim_is_quiet(self):
        self.assertEqual(self.check(AC_LABELED_VERBATIM), [])

    def test_labeled_bold_softened_fires_naming_the_bc(self):
        out = self.check(AC_LABELED_SOFTENED)
        self.assertEqual(len(out), 1)
        self.assertIn("BC1", out[0])
        self.assertIn("RR09", out[0])
        self.assertNotIn("BC2", out[0])


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
