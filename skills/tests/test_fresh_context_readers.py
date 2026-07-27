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


if __name__ == "__main__":
    unittest.main()
