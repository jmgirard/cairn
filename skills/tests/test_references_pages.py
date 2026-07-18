"""Regression guard: the references/ page-type doctrine (M57).

M56 found practice had outgrown the file map's "Source summaries" phrasing —
cross-source synthesis notes (competitive-landscape.md, migration-pilot-notes.md)
already live in `references/` unnamed. M57 legitimizes the second page type:
the file map names both committed page types (source notes + synthesis notes),
defined under the same one-line-in-INDEX rule, mechanized by `cairn_validate`'s
references check. M58 moved the definitions from the (extracted)
Source-ingestion section to the rulebook's own "References pages" section —
the page-type rules are universal file-family rules, not numeric-conditional
doctrine, so they stay in core.

Guard tests read the file as one string, so an asserted phrase must live on one
physical line (M23 lesson); phrases are lowercased before matching.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def rulebook():
    return (SKILLS / "shared" / "tracking-rules.md").read_text().lower()


def module():
    return (SKILLS / "shared" / "validation-doctrine.md").read_text().lower()


SYNTHESIS_TEMPLATE = SKILLS / "shared" / "templates" / "synthesis-note.md"


class TestReferencesPages(unittest.TestCase):
    def test_file_map_names_both_page_types(self):
        # The file-map row names source notes AND synthesis notes as the two
        # committed page types — not the outgrown "source summaries" alone.
        self.assertIn(
            "source notes (`<citekey>.md`), synthesis notes", rulebook()
        )

    def test_ingestion_defines_synthesis_notes(self):
        # The "References pages" section defines the second page type (M58
        # moved it there from Source ingestion; the rule itself is unchanged).
        self.assertIn(
            "the second committed `references/` page type", rulebook()
        )

    def test_every_committed_page_carries_an_index_line(self):
        # The rule the references check mechanizes: page on disk ⇒ INDEX line.
        self.assertIn(
            "every committed `references/` page carries its", rulebook()
        )


class TestAuthoringTrigger(unittest.TestCase):
    """M80: when a page is owed lives in CORE, not the numeric-gated module.

    LESSONS :49 — a new rule's home is decided by "would a repo with NO
    numeric work need this?". The trigger fires for any repo that relies on
    any source, so a repo with no numeric work needs it; putting it in
    `validation-doctrine.md` would hide it from exactly the non-numeric
    sessions that write most of these pages.
    """

    def test_core_states_when_a_source_owes_a_page(self):
        self.assertIn(
            "a page is owed once the repo *relies* on the source", rulebook()
        )

    def test_core_states_when_analysis_earns_a_synthesis_note(self):
        self.assertIn(
            "an analysis that will outlive its milestone", rulebook()
        )

    def test_core_names_both_shipped_templates(self):
        self.assertIn(
            "author from the shipped templates:", rulebook()
        )
        for path in (
            "`skills/shared/templates/source-note.md`",
            "`skills/shared/templates/synthesis-note.md`",
        ):
            with self.subTest(template=path):
                self.assertIn(path, rulebook())

    def test_module_defers_the_trigger_instead_of_restating_it(self):
        # Positive framing assert, mutation-registered. Its negative twin
        # below cannot be mutation-proven — blanking cannot restore an
        # absence (M54) — so the pair is what makes the rule falsifiable.
        self.assertIn(
            "do not restate the trigger here", module()
        )

    def test_trigger_sentence_is_absent_from_the_conditional_module(self):
        # The D-031 boundary: the module carries the numeric instance only.
        self.assertNotIn(
            "a page is owed once the repo *relies* on the source", module()
        )


class TestShippedSynthesisTemplate(unittest.TestCase):
    """Reads the SHIPPED template, not a fixture — M77's pairing rule."""

    # (field name, phrase that must appear in the shipped template)
    FIELDS = (
        ("owning milestone in the heading", "# <what this analyses> (m<nn>)"),
        ("provenance block", "**provenance.**"),
        ("ingested date", "ingested yyyy-mm-dd"),
        ("ingesting milestone", "by m<nn>"),
        ("pagination basis", "pagination:"),
        ("extraction status", "extraction:"),
        ("evidence snapshot", "**evidence snapshot.**"),
        ("tracking disclaimer", "status lives in `roadmap.md`, decisions in `decisions.md`,"),
        ("gap-ledger tag vocabulary", "`fix-here` | `candidate` | `out` — for a gap ledger."),
        ("stable row ids", "every row carries a stable id (`e1`, `g-c2`, `g-i3`)."),
        ("disposition section", "## disposition"),
        ("source-note differentiator", "a page that owns one primary source uses templates/source-note.md."),
    )

    def setUp(self):
        # Read per-test, never cached in setUpClass: the mutation harness runs
        # a guard as a single method and skips setUpClass, which would make
        # this guard report false coverage on itself (M61).
        self.text = SYNTHESIS_TEMPLATE.read_text().lower()

    def test_template_exists(self):
        self.assertTrue(
            SYNTHESIS_TEMPLATE.is_file(), f"{SYNTHESIS_TEMPLATE} is not shipped"
        )

    def test_every_required_field_is_present(self):
        for field, phrase in self.FIELDS:
            with self.subTest(field=field):
                self.assertIn(phrase, self.text, f"missing field: {field}")

    def test_dated_observation_form_is_carried(self):
        # These pages are bound by the standing-facts/dated-observations split
        # exactly as source notes are.
        self.assertIn("— observed yyyy-mm-dd", self.text)

    def test_derived_extraction_status_is_expressible(self):
        # A synthesis note has no external source to re-read against, so the
        # field is repurposed to a currency claim about the derivation. A
        # template offering only "verified against the source" would not fit.
        self.assertIn("derived — no external source of its own", self.text)


if __name__ == "__main__":
    unittest.main()
