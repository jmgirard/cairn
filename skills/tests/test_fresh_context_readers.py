"""Regression guard: M115's two fresh-context reader instruments.

Both instruments replace an author checking its own work with a reader that
did not write it. This file locks the doctrine text for the first of them —
the acceptance-criteria audit — at its two surfaces:

  * `/milestone-plan`, where the audit runs at the step-3 gate. Three edits
    carry it, because placing the audit alone would have audited a draft:
    step 2 must draft criteria to final wording, step 3 runs the reader, and
    step 4 writes the audited bytes.
  * `/milestone-brief`'s "Ingesting an RR", where the same reader asks the
    same two questions of a binding-criteria set before it is ingested.

Anchors are copied from the shipped bytes, never from the draft that
produced them (M95), and every phrase that crosses the files' hard wrap is
matched with `\\s+` rather than a literal newline, so a future reflow does
not red a rule that is still present (M105). Targets are read with
`Path.read_text` because the mutation engine patches only that call (M100).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def plan():
    return read("milestone-plan", "SKILL.md")


def brief():
    return read("milestone-brief", "SKILL.md")


class TestPlanGateCriteriaAudit(unittest.TestCase):
    """The audit at `/milestone-plan`'s question gate."""

    def test_step_2_drafts_criteria_to_final_wording(self):
        # Without this, the audit reads a draft step 4 then rewrites — the
        # certify-your-model-of-the-artifact failure the instrument exists to
        # stop, reproduced inside the fix for it.
        self.assertRegex(
            plan(),
            r"acceptance criteria are drafted here to their final wording,"
            r"\s+not at\s+step 4",
        )

    def test_audit_block_is_present_and_precedes_the_questions(self):
        self.assertIn(
            "**Criteria audit (runs before the questions are composed).**",
            plan(),
        )

    def test_audit_names_a_fresh_context_reader_that_authored_none_of_them(self):
        # The tier tag and the fresh-context requirement are pinned together:
        # an audit by the plan author is the check already measured to fail,
        # so "reader that authored none of them" is the operative half.
        self.assertRegex(
            plan(),
            r"fresh-context \*\*\[O\]\*\*\s+reader that authored none of them",
        )

    def test_audit_states_the_satisfiability_question(self):
        self.assertIn(
            "*what state of the world satisfies this exactly as written*",
            plan(),
        )

    def test_audit_states_the_ip_and_decision_conflict_question(self):
        self.assertIn(
            "*does any IP or D-entry make that state unreachable*",
            plan(),
        )

    def test_audit_reads_the_shipped_wording_never_a_paraphrase(self):
        self.assertRegex(
            plan(),
            r"It reads the wording\s+step 4 will write, never a paraphrase of it",
        )

    def test_clear_findings_are_fixed_and_the_fix_reported(self):
        self.assertRegex(
            plan(),
            r"a finding with one clear right answer is fixed\s+"
            r"and the fix reported in chat",
        )

    def test_judgment_findings_become_gate_questions_under_the_cap(self):
        # The two dispositions fail independently: dropping this one alone
        # leaves an audit that silently applies the author's own judgment,
        # which is the disposition the instrument replaces.
        self.assertRegex(
            plan(),
            r"becomes one of this round's questions, within the three-marker\s+cap",
        )

    def test_audit_is_a_reader_and_never_a_check(self):
        self.assertIn(
            "The instrument is a reader and never a check", plan()
        )

    def test_step_4_writes_the_audited_wording_and_reaudits_a_change(self):
        self.assertRegex(
            plan(),
            r"\*\*Write the wording\s+step 3's audit read\*\*; a criterion the "
            r"gate changed goes back through the\s+audit's two questions",
        )


class TestRRIngestionCriteriaAudit(unittest.TestCase):
    """The same audit at `/milestone-brief`'s RR ingestion."""

    def test_binding_criteria_are_audited_before_ingestion(self):
        self.assertIn(
            "**A binding-criteria set is audited before it is ingested**",
            brief(),
        )

    def test_ingest_audit_reuses_the_plan_gate_reader(self):
        self.assertRegex(
            brief(),
            r"by the same\s+fresh-context \*\*\[O\]\*\* reader "
            r"`/milestone-plan` step 3 spawns",
        )

    def test_ingest_audit_asks_the_questions_of_the_set_not_only_each(self):
        # The set-level read is the half RB07's trigger needed: two criteria
        # can each be satisfiable and still be jointly unsatisfiable, which a
        # per-criterion pass cannot see.
        self.assertRegex(
            brief(),
            r"asked\s+of the set as well as of each criterion",
        )

    def test_ingest_findings_are_raised_never_softened_away(self):
        self.assertRegex(
            brief(),
            r"What the audit returns is raised with the\s+user, never softened away",
        )


class TestDescriptionLayerCertification(unittest.TestCase):
    """`guard-doctrine.md` §8 — the author never certifies its own coverage."""

    @property
    def doctrine(self):
        return read("shared", "guard-doctrine.md")

    def test_section_exists_under_its_own_heading(self):
        self.assertIn(
            "## 8. The author never certifies its own guard's coverage",
            self.doctrine,
        )

    def test_section_separates_operation_from_certification(self):
        # The distinction is the whole cut: banning the author from running
        # its own guard would be the wrong rule, and this sentence is what
        # keeps the retirement scoped to certification.
        self.assertRegex(
            self.doctrine,
            r"Running a guard and certifying that it covers what you claim are "
            r"different\s+jobs, and only the first one survives being done by "
            r"its author",
        )

    def test_section_states_the_diagnosis(self):
        self.assertRegex(
            self.doctrine,
            r"the author checks the description against its generative\s+"
            r"model of the artifact rather than against the artifact",
        )

    def test_section_places_the_step_before_review_with_a_fresh_reader(self):
        self.assertRegex(
            self.doctrine,
            r"So before `status -> review`, a guard-authoring milestone hands "
            r"the\s+description layer to a fresh-context reader that authored "
            r"no part of it",
        )

    def test_section_names_the_coverage_check(self):
        self.assertRegex(
            self.doctrine,
            r"\*\*AC-clause-to-assert coverage\*\* — every clause of every "
            r"acceptance\s+criterion maps to an assert that actually pins it",
        )

    def test_section_names_the_claim_accuracy_check(self):
        self.assertRegex(
            self.doctrine,
            r"\*\*Claim-vs-file accuracy\*\* — every docstring, comment, "
            r"work-log line, and\s+record claim about the guard is true of the "
            r"file it describes",
        )

    def test_section_names_the_anchor_fidelity_check(self):
        self.assertRegex(
            self.doctrine,
            r"\*\*Anchor-vs-shipped-bytes fidelity\*\* — every multi-word anchor "
            r"matches the\s+bytes actually shipped",
        )

    def test_section_requires_zero_unresolved_and_forbids_arguing_down(self):
        self.assertRegex(
            self.doctrine,
            r"The gate is entered at zero unresolved: a discrepancy is fixed and\s+"
            r"re-certified, never argued down as imprecision",
        )

    def test_section_moves_certification_not_operation(self):
        self.assertRegex(
            self.doctrine,
            r"this moves certification, not operation",
        )

    def test_section_carries_its_own_falsifier(self):
        # An adopted step with no stated exit is how a mechanism measured not
        # to work gets tuned instead of retired (D-059).
        self.assertRegex(
            self.doctrine,
            r"if guard-authoring\s+milestones still average multiple "
            r"description-layer returns after adoption,\s+the step didn't work "
            r"— retire it \(D-059\), don't tune it",
        )


class TestImplementRoutesToCertification(unittest.TestCase):
    """`/milestone-implement` step 8 fires the step §8 defines."""

    def test_completion_step_routes_to_the_certifier_at_zero_unresolved(self):
        self.assertRegex(
            read("milestone-implement", "SKILL.md"),
            r"if this milestone authored or edited a\s+prose-guard, hand its "
            r"description layer to a fresh-context reader first",
        )

    def test_completion_step_cites_the_doctrine_section_and_the_bar(self):
        self.assertRegex(
            read("milestone-implement", "SKILL.md"),
            r"`skills/shared/guard-doctrine\.md` §8, the author never certifies "
            r"its own\s+guard's coverage — and enter the gate only at zero "
            r"unresolved",
        )


if __name__ == "__main__":
    unittest.main()
