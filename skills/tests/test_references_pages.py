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

import datetime
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


class TestExploratorySources(unittest.TestCase):
    """M103: supply-push exploration — reading a corpus of uncited sources to
    DISCOVER new oracles or methods — is a legitimate activity, distinct from
    the demand-pull "owed" trigger above. The circumplex incident: an agent
    handed uncited PDFs dismissed them all because nothing cited them. The
    doctrine lives in core "References pages" (universal — a repo with no
    numeric work still explores), reusing candidate rows + the synthesis-note
    survey type and adding no machinery (the M56 rejection).

    rulebook() lowercases, so each anchor here is lowercased; each is one
    physical line (the mutation harness blanks by line — LESSONS :37).
    """

    def test_exploration_is_named_a_legitimate_activity(self):
        # AC1: distinct from the demand-pull "owed" trigger — triaged, not
        # dismissed for want of a citation.
        self.assertIn(
            "is supply-push exploration, a legitimate activity", rulebook()
        )

    def test_exploration_always_produces_candidate_rows(self):
        # AC2 output 1: candidate rows always, search-first (the D-042 pattern).
        self.assertIn(
            "it always produces roadmap candidate rows for the promising "
            "oracles or methods it finds",
            rulebook(),
        )

    def test_survey_note_only_when_it_outlives_the_exploration(self):
        # AC2 output 2: the committed survey synthesis note is conditional on
        # the existing "owed applied to time" test — a one-shot triage stays
        # in the milestone file and earns no page.
        self.assertIn(
            "only when the triage will outlive its exploration", rulebook()
        )

    def test_per_source_pages_stay_demand_pull(self):
        # AC2 output 3: exploration withholds the per-citekey page; those are
        # still earned only on graduation plus a trace back to the source.
        self.assertIn(
            "those stay demand-pull, earned only once a candidate graduates",
            rulebook(),
        )

    def test_exploration_restates_the_m56_guardrail(self):
        # AC3: reuse existing records, add no machinery — the shapes M56
        # rejected, named so a later milestone cannot quietly rebuild one.
        self.assertIn(
            "no committed raw sources, no references log, no query op or "
            "graph tooling",
            rulebook(),
        )

    def test_each_anchor_sits_on_one_physical_line(self):
        # The mutation harness blanks by physical line; an anchor spanning two
        # would "found 0"-error rather than redden (LESSONS :37).
        lines = [ln.lower() for ln in
                 (SKILLS / "shared" / "tracking-rules.md").read_text().splitlines()]
        for anchor in (
            "is supply-push exploration, a legitimate activity",
            "it always produces roadmap candidate rows for the promising "
            "oracles or methods it finds",
            "only when the triage will outlive its exploration",
            "those stay demand-pull, earned only once a candidate graduates",
            "no committed raw sources, no references log, no query op or "
            "graph tooling",
        ):
            hits = [ln for ln in lines if anchor in ln]
            with self.subTest(anchor=anchor[:40]):
                self.assertEqual(len(hits), 1, f"{anchor!r} must sit on one line")


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


class TestTemplatesTeachTheShapeRule(unittest.TestCase):
    """M85 AC1 — both templates state the SHAPE, not a list of phrases.

    The candidate row this milestone came from proposed listing the forms the
    repo writes. M83's classifier reads a shape, so a list would be wrong the
    moment someone writes a sixth phrasing; what an author needs is the rule
    the classifier actually applies. These are prose-guards over shipped
    templates, so each asserted phrase sits on one physical line (M23), and
    the verb set is pinned together with its label on that line (M74/M76: a
    label→SET guard that pins only the label leaves the members swappable).
    """

    TEMPLATES = (
        ("source", SKILLS / "shared" / "templates" / "source-note.md"),
        ("synthesis", SKILLS / "shared" / "templates" / "synthesis-note.md"),
    )

    def text(self, template):
        """Read per-test, never cached on the class — a setUpClass cache reads
        the unmutated file under the mutation harness (M61)."""
        return template.read_text()

    def test_each_template_states_the_three_way_shape(self):
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                self.assertIn(
                    "claim a verification, or carry a date, or say there is "
                    "nothing to re-verify.",
                    self.text(template),
                )

    def test_each_template_names_the_verb_set_with_its_label(self):
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                self.assertIn(
                    "A verification claim is one of these verbs — `verified`, "
                    "`checked against`, `read against`, `read directly`.",
                    self.text(template),
                )

    def test_each_template_marks_unverified_as_self_negating(self):
        """M85 review F2/80. The first draft listed `unverified` among the four
        affirmative verbs and then said a verb is negated only when a negator
        precedes it — wrong for the one member that carries its own negation
        (`_UNVERIFIED` in cairn_validate adds "never" unconditionally, before
        the negator loop runs). An author following that rule would write
        `unverified pending a second pass`, expect an affirmative, and get
        `never`. The rule is the deliverable, so the exception is stated and
        guarded rather than left for the author to discover.
        """
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                self.assertIn(
                    "`unverified` is the exception — it carries its own "
                    "negation and always reads as never-verified, with or "
                    "without a negator.",
                    self.text(template),
                )

    def test_each_template_names_the_partiality_set_with_its_label(self):
        """M89. Pinned label→SET, exactly like the verb-set guard above: a
        guard that pinned only "a partiality qualifier" would leave the four
        members swappable, which is the M74/M76 trap."""
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                self.assertIn(
                    "A partiality qualifier before the verb in that same "
                    "clause — `partly`, `partially`, `in part`, "
                    "`spot-checked` — makes the claim a PARTIAL verification.",
                    self.text(template),
                )

    def test_each_template_says_a_partial_claim_is_never_cleared(self):
        """The consequence half. Naming the state without saying it cannot be
        aged out leaves an author expecting a fresh date to close it — which
        is precisely what the defect did on their behalf."""
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                self.assertIn(
                    "A partial claim is reported, never cleared: no date "
                    "closes it, because what is missing is coverage rather "
                    "than freshness.",
                    self.text(template),
                )

    # Each taught qualifier is run through the classifier in several clause
    # SHAPES, because one shape is not a test of the rule (review F1, scored
    # 95). The original guard used only the first of these: it hands the
    # qualifier an independent verb, so it passed on
    # `spot-checked verified against the source` — a string no author writes —
    # while the phrasing the templates actually teach,
    # `spot-checked against the source`, classified as a full verification.
    # The second shape is the one that catches a qualifier OVERLAPPING its
    # verb; the third pairs it with a different verb entirely.
    QUALIFIER_SHAPES = (
        "{q} verified against the source",
        "{q} against the source",
        "{q} read against the source",
    )

    def test_each_taught_partiality_qualifier_classifies_as_partial(self):
        """The taught set run through the REAL classifier, one member at a
        time (M75/M85): a set tested as a whole passes on its first member and
        says nothing about the rest, so a qualifier the templates teach but
        the implementation cannot read would ship unnoticed.

        The invariant is that no taught qualifier may ever yield a bare
        `verified` — that is the false green AC1 exists to close — and that
        each one reaches `partial` in at least one shape an author would
        actually write. A shape that makes no claim at all (no verb) is not a
        failure; a shape that makes a FULL verification claim is.

        The members are lifted OUT of the template line, not restated, so a
        template that renamed one is tested on the new name — a hardcoded copy
        here would keep testing the old one and pass.
        """
        validate = _load_validate()
        template = SKILLS / "shared" / "templates" / "source-note.md"
        line = next(
            ln for ln in self.text(template).splitlines()
            if "makes the claim a PARTIAL verification" in ln
        )
        taught = re.findall(r"`([^`]+)`", line)
        self.assertEqual(len(taught), 4, f"expected four qualifiers in {line!r}")
        for qualifier in taught:
            reached = []
            for shape in self.QUALIFIER_SHAPES:
                clause = shape.format(q=qualifier)
                with self.subTest(qualifier=qualifier, clause=clause):
                    state = validate._resolve_claims(
                        validate._clause_claims(clause)
                    )
                    self.assertNotEqual(
                        state, "verified",
                        f"{clause!r} reads as a FULL verification — the "
                        f"templates teach this qualifier as partial",
                    )
                    reached.append(state)
            self.assertIn(
                "partial", reached,
                f"no shape reached `partial` for {qualifier!r}, so this "
                f"member is taught but unreadable",
            )

    def test_each_template_says_the_alternatives_are_not_the_accepted_list(self):
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                self.assertIn(
                    "The alternatives below are examples of that shape, not "
                    "the accepted list.",
                    self.text(template),
                )

    def test_each_template_says_an_unreadable_status_is_reported(self):
        """The consequence half of the rule. Without it the shape reads as
        advice; with it the author knows the advisory will say so."""
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                self.assertIn(
                    "it is reported rather than assumed verified.",
                    self.text(template),
                )


class StatusClassificationMixin:
    """Shared machinery for the two classes below, so the template's own
    alternatives and the unlisted shipped forms are judged by exactly the same
    reader. A plain mixin, not a TestCase: subclassing a TestCase to reuse
    helpers re-runs the parent's tests under every child's name.
    """

    TEMPLATES = (
        ("synthesis", SYNTHESIS_TEMPLATE),
        ("source", SKILLS / "shared" / "templates" / "source-note.md"),
    )
    # Every state the classifier can return, so a typo'd expectation cannot
    # quietly pass by naming a state that does not exist.
    STATES = {
        "ok", "never", "partial", "exempt", "missing", "undated",
        "ambiguous", "unrecognized", "future",
    }

    def instantiate(self, template):
        """The shipped template with its placeholders filled, read from disk
        every call — never a fixture copy (M77/M80)."""
        text = re.sub(r"YYYY-MM-DD", "2026-07-18", template.read_text())
        return text.replace("M<NN>", "M85")

    def alternatives(self, text):
        """The choices offered inside the `Extraction:` field's `<a | b | c>`."""
        line = extraction_line(text)
        self.assertIsNotNone(line, "template yields no Extraction status line")
        offered = re.search(r"<(.+)>", line)
        self.assertIsNotNone(
            offered, f"Extraction field offers no <a | b | c> choice: {line}"
        )
        return [a.strip() for a in offered.group(1).split("|")]

    def choose(self, text, alternative):
        """The page an author produces by keeping one alternative."""
        return re.sub(
            r"^Extraction:.*$",
            f"Extraction: {alternative} — observed 2026-07-18.",
            text, count=1, flags=re.M,
        )

    def classify(self, page_text):
        """The REAL classifier's verdict on a page, via the REAL block reader."""
        validate = _load_validate()
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "page.md"
            path.write_text(page_text)
            block = validate._provenance_block(str(path), for_extraction=True)
        self.assertIsNotNone(block, "no provenance block was read from the page")
        state, _ = validate._last_verified(block, datetime.date(2026, 7, 18))
        # Positive signal that the classifier path actually ran (M84 lesson:
        # an absence-assert alone is satisfied by a crash producing nothing).
        self.assertIn(state, self.STATES, f"classifier returned {state!r}")
        return state


class TestEachSanctionedStatusClassifies(
    StatusClassificationMixin, unittest.TestCase
):
    """M85 AC2/AC3 — instantiating the dates is not instantiating the CHOICE.

    M80's pairing test filled `YYYY-MM-DD` and `M<NN>` and then ran only
    `check_references` and the dated-extraction regex, both of which ask
    existence questions. It never asked the one reader that interprets the
    status — `_last_verified`, the classifier M83 built — so nothing proved a
    page authored from either template says what its author meant. The
    templates classified correctly by luck, not by test.

    What the `<a | b | c>` field offers is a CHOICE, and the classifier reads
    the choice, so the test makes one. Each alternative is selected in turn,
    a page is built from it, and the state the real classifier returns is
    asserted against what that wording intends.
    """

    # What each sanctioned alternative MEANS, keyed by a substring that
    # matches exactly one of them. A new alternative added to a template
    # matches nothing here and fails, which is deliberate: an author adding a
    # status form must say what it should classify as.
    INTENT = {
        "unverified": "never",
        "verified 2026-07-18": "ok",
        "derived": "ok",
        "nothing to re-verify": "exempt",
        "snapshot": "ok",
    }

    def intended(self, alternative):
        hits = [v for k, v in self.INTENT.items() if k in alternative]
        self.assertEqual(
            len(hits), 1,
            f"expected exactly one intent for {alternative!r}, matched {hits}",
        )
        return hits[0]

    def test_every_alternative_classifies_as_its_wording_intends(self):
        for kind, template in self.TEMPLATES:
            text = self.instantiate(template)
            for alternative in self.alternatives(text):
                with self.subTest(template=kind, alternative=alternative[:40]):
                    self.assertEqual(
                        self.classify(self.choose(text, alternative)),
                        self.intended(alternative),
                    )

    def test_no_alternative_is_unreadable(self):
        """The two states that mean "the advisory cannot tell" — neither may be
        reachable by an author who followed the template."""
        for kind, template in self.TEMPLATES:
            text = self.instantiate(template)
            for alternative in self.alternatives(text):
                with self.subTest(template=kind, alternative=alternative[:40]):
                    state = self.classify(self.choose(text, alternative))
                    self.assertNotIn(state, ("ambiguous", "unrecognized"))

    def test_the_unchosen_template_is_what_collapses(self):
        """Non-vacuity, and the reason the templates now say pick ONE.

        Left unchosen, the source template states a verification and its
        absence at once (`ambiguous`), and the synthesis template's
        `nothing to re-verify` clause — searched across the whole status —
        exempts the page from staleness no matter which alternative was meant.
        These are positive assertions on specific states, so they fail rather
        than pass if the classifier path breaks.
        """
        collapse = {"source": "ambiguous", "synthesis": "exempt"}
        for kind, template in self.TEMPLATES:
            with self.subTest(template=kind):
                self.assertEqual(
                    self.classify(self.instantiate(template)), collapse[kind]
                )


class TestUnlistedShippedFormsSatisfyTheShapeRule(
    StatusClassificationMixin, unittest.TestCase
):
    """M85 AC4 — the vocabulary the repo writes, which neither template lists.

    The M85 candidate row's original framing was that these forms should
    be ADDED to the templates as accepted phrases. The plan gate rejected
    that: M83's classifier reads a shape (a verification verb, a date, or an
    explicit nothing-to-re-verify), not a whitelist, so enumerating more
    phrases would re-open the same gap at the next one. What the templates
    teach instead is the shape — and what this class proves is that the shape
    rule is honest, by classifying each unlisted form through the real
    classifier and showing it is already readable.

    The list shrinks as the corpus changes: M85 opened with four forms and
    M91 retired one by re-reading the pages that wrote it, which is the
    removal rule below working rather than a gap. Count the tuples; this
    prose deliberately names no total.

    Sharing the mixin above is deliberate: these forms must be judged by
    exactly the machinery that judges the template's own alternatives.
    """

    # Each form as a shipped page writes it, paired with a pattern that finds
    # it among this repo's real statuses and the state it must classify as.
    # The pattern is what keeps the list from going fictional: a form no page
    # writes any more fails, rather than sitting here as a phrase the
    # templates are being measured against.
    #
    # "Readable" is the shape rule, not "clean" (M89): the `partly` form was
    # pinned at `ok` here while it meant the opposite, which is how it went on
    # reading as a completed verification. Each form now names its own state.
    FORMS = (
        (
            "verified at ingestion — full source read; not re-read since",
            r"^verified at ingestion",
            "ok",
        ),
        # The `partly verified at ingestion` form was retired from the corpus
        # by M91, which re-read all three pages that wrote it against their
        # sources; no committed page carries it any more, so per this class's
        # own rule it stops being a phrase the templates are measured against.
        # The classifier's reading of it is not lost — `partial` keeps its
        # dedicated coverage in scripts/tests/test_scripts.py
        # (test_partly_verified_pages_report_partial_not_ok and the three
        # fixtures beside it), which is where the state was proven to begin with.
        (
            "read against the ackwards artifacts at assessment time; the "
            "assessed repo has moved on independently since, so the "
            "catalogue is a 2026-07-12 snapshot",
            r"^read against .* at assessment time",
            "ok",
        ),
        (
            "verified by live probe 2026-07-12; a re-probe would be needed "
            "to confirm the mechanism still holds in the current client",
            r"^verified by live probe",
            "ok",
        ),
    )
    SOURCE_TEMPLATE = SKILLS / "shared" / "templates" / "source-note.md"

    def shipped_statuses(self):
        """Every `Extraction:` status this repo's committed pages carry."""
        refs = SKILLS.parent / "cairn" / "references"
        out = []
        for page in sorted(refs.glob("*.md")):
            if page.name == "INDEX.md":
                continue
            line = extraction_line(page.read_text())
            if line:
                out.append(line[len("Extraction:"):].strip())
        self.assertTrue(out, "no shipped references statuses were found")
        return out

    def test_each_unlisted_form_is_readable(self):
        base = self.instantiate(self.SOURCE_TEMPLATE)
        for status, _, state in self.FORMS:
            with self.subTest(form=status[:40]):
                self.assertEqual(
                    self.classify(self.choose(base, status)), state
                )

    def test_each_unlisted_form_is_still_written_by_a_page(self):
        statuses = self.shipped_statuses()
        for status, pattern, _ in self.FORMS:
            with self.subTest(form=status[:40]):
                self.assertTrue(
                    any(re.match(pattern, s, re.I) for s in statuses),
                    f"no committed page writes a status matching {pattern!r} "
                    f"— the form list above has gone stale",
                )

    def test_no_unlisted_form_is_offered_by_a_template(self):
        """These are the forms the templates do NOT list — the premise of the
        class. If one is ever added to a template, it belongs to the class
        above (which asserts an intent for every offered alternative) and this
        one stops being about unlisted vocabulary.

        Matched on the form's distinguishing PREFIX, not by exact string
        equality (M85 review F3/62). Equality only caught a byte-exact paste of
        the whole 60–200-char shipped status; the realistic way one of these
        arrives in a template is shortened or re-dated, and every such variant
        slipped through a premise this test claims to defend.
        """
        offered = []
        for _, template in self.TEMPLATES:
            offered.extend(self.alternatives(self.instantiate(template)))
        for status, pattern, _ in self.FORMS:
            with self.subTest(form=status[:40]):
                self.assertFalse(
                    [a for a in offered if re.match(pattern, a, re.I)],
                    f"a template now offers a form matching {pattern!r}; it "
                    f"belongs to TestEachSanctionedStatusClassifies",
                )


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
