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

import importlib.util
import pathlib
import re
import sys
import tempfile
import unittest

from test_source_note_template import DATED_EXTRACTION, extraction_line

SKILLS = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = SKILLS.parent / "scripts"


def _load_validate():
    """The REAL cairn_validate, so AC3's pairing test runs the shipped checker
    rather than a reimplementation of it."""
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(
        "cairn_validate", SCRIPTS / "cairn_validate.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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

    def test_extraction_status_is_a_real_provenance_field(self):
        # NOT a substring anchor on "extraction:" — that phrase also occurs in
        # the header comment, so deleting the actual Provenance field line left
        # the field guard green (review F3). Pin the line itself, at column 0,
        # which is the only form the dated-extraction guard can read.
        line = extraction_line(SYNTHESIS_TEMPLATE.read_text())
        self.assertIsNotNone(
            line, "no `Extraction: ` field line in the Provenance block"
        )

    def test_dated_observation_form_is_carried(self):
        # These pages are bound by the standing-facts/dated-observations split
        # exactly as source notes are.
        self.assertIn("— observed yyyy-mm-dd", self.text)

    def test_derived_extraction_status_is_expressible(self):
        # A synthesis note has no external source to re-read against, so the
        # field is repurposed to a currency claim about the derivation. A
        # template offering only "verified against the source" would not fit.
        self.assertIn("derived — no external source of its own", self.text)


class TestTemplateProducesAValidPage(unittest.TestCase):
    """AC3 — the M77 pairing rule: one task authored the template, another
    authored nothing that checks it, so nothing proved a page written from it
    would survive the checkers already in the repo. This instantiates the
    SHIPPED template and runs the REAL `check_references` and the REAL
    dated-extraction guard over the result.

    The template itself cannot pass: its dates are `YYYY-MM-DD` placeholders,
    which the date regex rightly refuses. Instantiating is what a page author
    does, so instantiating is what the pairing test does (AC3 amended at the
    implement gate, 2026-07-18).
    """

    # Both shipped templates, so neither can regress alone. AC7 was added at
    # the implement gate after this test's synthesis half proved the
    # source-note template — shipped by M78 — emits a page that fails the
    # dated-extraction guard M78 shipped in the same milestone.
    TEMPLATES = (
        ("synthesis", SYNTHESIS_TEMPLATE),
        ("source", SKILLS / "shared" / "templates" / "source-note.md"),
    )

    def instantiate(self, template):
        """The shipped template with its placeholders filled, as an author
        would. Read from disk every call — never a fixture copy."""
        text = template.read_text()
        text = re.sub(r"YYYY-MM-DD", "2026-07-18", text)
        text = text.replace("M<NN>", "M80")
        return text

    def _tree(self, tmp, template, page):
        root = pathlib.Path(tmp)
        refs = root / "cairn" / "references"
        refs.mkdir(parents=True)
        (refs / page).write_text(self.instantiate(template))
        (refs / "INDEX.md").write_text(
            f"# References index\n\n- {page} — an instantiated note.\n"
        )
        return root

    def test_instantiated_page_passes_the_real_references_check(self):
        validate = _load_validate()
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                page = f"{kind}-example.md"
                with tempfile.TemporaryDirectory() as tmp:
                    findings = validate.check_references(
                        str(self._tree(tmp, template, page))
                    )
                self.assertEqual(
                    findings, [],
                    f"a page authored from the {kind} template fails: {findings}",
                )

    def test_instantiated_page_passes_the_real_extraction_guard(self):
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                line = extraction_line(self.instantiate(template))
                self.assertIsNotNone(
                    line, f"{kind} template yields no Extraction status line"
                )
                self.assertRegex(line, DATED_EXTRACTION)

    def test_uninstantiated_template_is_what_fails(self):
        # Proves the test above is not vacuous: the placeholder form really
        # does fail the date guard, which is why instantiation is the subject.
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                line = extraction_line(template.read_text())
                self.assertIsNotNone(line)
                self.assertNotRegex(line, DATED_EXTRACTION)


class TestReVerification(unittest.TestCase):
    """M81: the extraction status gets a reader, and the rulebook states the
    expectation behind it. Both anchors are pinned WITH the thing they rule
    out — a re-check marks inline, never in a new file — because a guard on
    the expectation alone survives the recording location being moved to the
    central ledger M56 rejected (M74/M76: pin the label with its members)."""

    def test_core_states_the_re_verification_expectation(self):
        self.assertIn(
            "a page the repo still relies on is re-checked against its source "
            "as it gets old, and a page never checked against its source at "
            "all keeps saying so",
            rulebook(),
        )

    def test_a_re_check_marks_inline_and_nowhere_else(self):
        # The location half. Without "never in a new file, a new section, or a
        # log", the rule reads as satisfied by a references/log.md.
        self.assertIn(
            "a re-check marks inline in the provenance block, on the "
            "extraction status itself — never in a new file, a new section, "
            "or a log",
            rulebook(),
        )

    def test_each_anchor_sits_on_one_physical_line(self):
        # The mutation harness blanks by physical line; a reflow would
        # "found 0"-error both entries (LESSONS :27).
        lines = [ln.lower() for ln in
                 (SKILLS / "shared" / "tracking-rules.md").read_text().splitlines()]
        for anchor in (
            "a page the repo still relies on is re-checked",
            "a re-check marks inline in the provenance block",
        ):
            hits = [ln for ln in lines if anchor in ln]
            self.assertEqual(len(hits), 1, f"{anchor!r} must sit on one line")

    def test_advisory_is_named_by_its_emitted_label(self):
        # M28/LESSONS :27: prose naming a validate finding uses the emitted
        # label verbatim, so a reader can grep the output for it.
        self.assertIn("`references staleness` advisory", rulebook())
        self.assertIn(
            "references staleness",
            [name for name, _ in _load_validate().ADVISORIES],
        )

    def test_severity_is_advisory_not_a_check(self):
        # M81-D1 / D-029: the rulebook states WHY this is not a gate, so a
        # later milestone cannot promote it by forgetting the reasoning.
        self.assertIn(
            "it stays an advisory and never a check", rulebook()
        )

    def test_the_threshold_prose_matches_the_shipped_constant(self):
        # The pairing rule (M77) applied to a NUMBER: prose stating 180 days
        # over code comparing something else is the drift this catches.
        self.assertIn("more than 180 days ago", rulebook())
        self.assertEqual(_load_validate()._STALE_DAYS, 180)


if __name__ == "__main__":
    unittest.main()
