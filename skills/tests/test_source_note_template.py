"""Regression guard: the source-note shape — dated observations + provenance (M78).

The intraclass repo ingested PDFs heavily and kept hitting the same staleness:
a page asserting something about the REPO'S OWN state ("appendices not present
on the shelf", "saha2005 must still be checked") recorded as a standing fact,
then false by merge time. M65 scored two at 95 and 92, and both were literal
repeats of lessons already written down at M63 and M64 — a lesson re-learned
three milestones running is a doctrine gap, not an operator lapse.

M78 splits a page's claims by how they age — standing facts about the SOURCE
vs. dated observations about the REPO'S STATE, the latter marked inline with
`— observed YYYY-MM-DD` — and ships the source-note template that carries the
shape plus a seven-field Provenance block.

Two distinct guards live here:

  TestClaimSplitDoctrine   — prose guards on validation-doctrine.md. Each
      label is asserted TOGETHER WITH its members, so swapping the two
      definitions fails (M74/M76: pinning only the mechanism sentence leaves
      the sets swappable AND deletable with every assert green).
  TestShippedTemplate      — runs the real field check over the REAL shipped
      template file, not a fixture copy (M77: when one task authors content
      and another authors its checker, nothing pairs them unless a test reads
      the shipped artifact).

Doctrine text is read with whitespace normalized, so an assert survives a
reflow of the wrapped prose; the mutation-registered anchors are separately
pinned to one physical line each (M59/M64).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = SKILLS / "shared" / "templates" / "source-note.md"
DOCTRINE = SKILLS / "shared" / "validation-doctrine.md"


def doctrine_flat():
    """Doctrine text, lowercased, with runs of whitespace collapsed to one
    space — so an assert pins wording, not line breaks."""
    return re.sub(r"\s+", " ", DOCTRINE.read_text().lower())


def doctrine_lines():
    """Physical lines, lowercased — for asserts that must prove a phrase sits
    on ONE line (the mutation harness blanks by physical line)."""
    return [ln.lower() for ln in DOCTRINE.read_text().splitlines()]


class TestClaimSplitDoctrine(unittest.TestCase):
    def test_standing_fact_label_carries_its_members(self):
        # Label AND enumeration together: a guard on the mechanism sentence
        # alone survives the two definitions being swapped (M76 lesson).
        self.assertIn(
            "a **standing fact** is a claim about the *source*: an extracted "
            "value, a printed formula, a verbatim wording, a page or table "
            "anchor.",
            doctrine_flat(),
        )

    def test_dated_observation_label_carries_its_members(self):
        self.assertIn(
            "a **dated observation** is a claim about the *repo's own state*: "
            "what is on the shelf, what has or has not been read, what another "
            "page does or does not yet say, what a later task must still check.",
            doctrine_flat(),
        )

    def test_each_definition_sits_on_one_physical_line(self):
        # The mutation harness blanks a block by physical line; a definition
        # that reflows across lines can no longer be registered (M59/M64).
        for label in ("**standing fact**", "**dated observation**"):
            hits = [ln for ln in doctrine_lines() if label in ln]
            self.assertEqual(
                len(hits), 1, f"{label} must appear on exactly one line"
            )
            self.assertTrue(
                hits[0].rstrip().endswith("."),
                f"{label}'s definition must be complete on its own line",
            )

    def test_observation_marker_is_the_inline_dated_form(self):
        self.assertIn("`— observed yyyy-mm-dd` inline on the claim", doctrine_flat())

    def test_rule_binds_both_committed_page_types(self):
        self.assertIn("source note and synthesis note alike", doctrine_flat())

    def test_undated_absence_claim_is_named_as_the_failure(self):
        self.assertIn(
            'the undated absence claim — "not present", "not retrieved", '
            '"not yet checked", "must be verified when x is written" — is the '
            "specific failure this rule exists to stop",
            doctrine_flat(),
        )

    def test_ingestion_names_the_template_path(self):
        # Without this the shipped shape is unreachable from the doctrine
        # that mandates it.
        self.assertIn(
            "skills/shared/templates/source-note.md", doctrine_flat()
        )

    def test_provenance_block_is_prose_not_frontmatter(self):
        self.assertIn("the block is prose in the page's own idiom, not frontmatter", doctrine_flat())


class TestShippedTemplate(unittest.TestCase):
    """Reads the SHIPPED template, not a fixture — M77's pairing rule."""

    # (field name, phrase that must appear in the shipped template)
    FIELDS = (
        ("citekey", "# <citekey>"),
        ("full citation", "**citation.**"),
        ("source pointer", "cairn/references/pdf/<citekey>.pdf"),
        ("non-pdf source pointer", "the url plus how it was retrieved"),
        ("ingested date", "ingested yyyy-mm-dd"),
        ("ingesting milestone", "by m<nn>"),
        ("pagination basis", "pagination:"),
        ("extraction-verified status", "extraction:"),
    )

    def setUp(self):
        # Read per-test, never cached in setUpClass: the mutation harness runs
        # a guard as a single method and skips setUpClass, which would make
        # this guard report false coverage on itself (M61).
        self.text = TEMPLATE.read_text().lower()

    def test_template_exists(self):
        self.assertTrue(TEMPLATE.is_file(), f"{TEMPLATE} is not shipped")

    def test_every_provenance_field_is_present(self):
        for field, phrase in self.FIELDS:
            with self.subTest(field=field):
                self.assertIn(phrase, self.text, f"missing provenance field: {field}")

    def test_provenance_block_is_present(self):
        self.assertIn("**provenance.**", self.text)

    def test_unpaginated_source_has_a_legal_value(self):
        # A non-PDF source has no pagination basis; the field takes an em dash
        # rather than being omitted (AC2, amended at the M78 implement gate).
        self.assertRegex(self.text, r"pagination:.*\|\s*—")

    def test_unverified_extraction_is_an_expressible_state(self):
        # The field that flags an unchecked subagent pass is the whole point;
        # a template offering only "verified" would defeat it.
        self.assertIn("unverified", self.text)

    def test_open_questions_section_carries_the_dated_form(self):
        self.assertIn("## open questions", self.text)
        self.assertIn("— observed yyyy-mm-dd", self.text)

    def test_traces_to_section_names_files_and_lines(self):
        # The backlink surface a corrector walks when a value here changes.
        self.assertIn("## traces to", self.text)
        self.assertIn("`path/to/file:line`", self.text)


if __name__ == "__main__":
    unittest.main()
