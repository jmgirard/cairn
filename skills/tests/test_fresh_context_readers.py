"""Regression guard: the acceptance-criteria audit — the fresh-context
reader instrument at the plan and ingest gates (D-067, as narrowed at M127).

The instrument replaces an author checking its own criteria with a reader
that authored none of them. Two surfaces, including the audit's record
requirement, which M121 added (D-079 clause 2):

  * `/milestone-plan`, where the audit runs at the step-3 gate
    (`TestPlanGateCriteriaAudit`). Three edits carry it, because placing the
    audit alone would have audited a draft: step 2 must draft criteria to
    final wording, step 3 runs the reader, and step 4 writes the audited
    bytes.
  * `/milestone-brief`'s "Ingesting an RR", where the same reader asks the
    same three questions of a binding-criteria set before it is ingested
    (`TestRRIngestionCriteriaAudit`).

Until M127 this file also locked D-067's other instrument — the
description-layer certification, `guard-doctrine.md` §8, and the
`/milestone-implement` completion clause that fired it. M127 retired that
step whole; its guard classes and their mutation-registry entries retired
with it, and D-067 is narrowed to the criteria audit alone.

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

    def test_audit_records_a_work_log_line_even_when_it_finds_nothing(self):
        # M121 narrows D-067's first instrument. D-067 was adopted BY M115, so
        # the five milestones after it are M116-M120, and three of those —
        # M117, M119, M120 — carry no audit line at all, so "did not run" and
        # "ran and found nothing" are indistinguishable in the record, which is
        # what makes the instrument's yield unmeasurable. (D-079's evidence
        # reports two, over the narrower M115-M119 window AC3 names.)
        self.assertRegex(
            plan(),
            r"\*\*The audit records one work-log line either way\*\* — what it "
            r"returned, or\s+that it returned nothing",
        )

    def test_absent_audit_line_means_it_did_not_run(self):
        # The operative half: without it the requirement reads as bookkeeping
        # rather than as what makes a missing line evidence.
        self.assertRegex(
            plan(),
            r"an absent line means the reader did not run,\s+never that it ran "
            r"and was silent",
        )

    def test_audit_records_how_many_milestones_left_no_line(self):
        # M121 review pass 2, F-E3 (83). The record requirement's asserts pin
        # the rule; nothing pinned the measurement that motivates it, so
        # "Three of the five ... carry no such line" inverted to "All five ...
        # so the record is complete" with the suite green — turning the
        # evidence for the rule into a claim that the rule is unnecessary.
        self.assertRegex(
            plan(),
            r"Three of the five milestones after\s+this instrument was "
            r"adopted carry no such line",
        )

    def test_step_4_writes_the_audited_wording_and_reaudits_a_change(self):
        self.assertRegex(
            plan(),
            r"\*\*Write the wording\s+step 3's audit read\*\*; a criterion the "
            r"gate changed goes back through the\s+audit's three questions",
        )

    def test_audit_asks_the_bounded_promise_question(self):
        # M130: the third mechanical question — intraclass M100's three-return
        # thrash traced to a criterion no stated procedure could check, so an
        # unbounded promise is caught at drafting, not at pass three.
        self.assertRegex(
            plan(),
            r"\*does it make a universal claim over a domain no procedure "
            r"it names enumerates\*\s+\(the bounded-promise rule, step 4; M130\)",
        )

    def test_drafting_rule_bounds_universal_promises(self):
        self.assertRegex(
            plan(),
            r"\*\*Bounded promises only \(M130\)\.\*\* An acceptance criterion "
            r"that makes a\s+universal claim \(\"no X\", \"every Y\", "
            r"\"nothing Z\"\) names the procedure —\s+a search, a sweep, or a "
            r"test run — that enumerates its domain",
        )

    def test_unenumerable_universals_claim_the_swept_domain_instead(self):
        self.assertRegex(
            plan(),
            r"where no\s+stated procedure can enumerate the domain, the "
            r"criterion instead\s+claims what a procedure it names actually swept",
        )

    def test_a_hand_list_of_sites_is_not_a_procedure(self):
        # M118's lesson carried into the rule: a criterion that lists its
        # sites becomes the sweep, and every omitted site ships stale.
        self.assertRegex(
            plan(),
            r"A hand-list of sites is\s+not a procedure",
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

    def test_ingest_audit_states_both_questions_at_this_surface(self):
        # AC1 requires BOTH surfaces to state the audit's questions, and the two
        # asserts either side of this clause anchor past it: deleting the
        # questions from the brief left every other assert here green, so
        # `..._asks_the_questions_of_the_set...` reads as covering them and
        # does not. Found by M115's own certifier against its own guard.
        self.assertRegex(
            brief(),
            r"and the same\s+three questions — \*what state of the world "
            r"satisfies this exactly as\s+written\*, \*does any IP or "
            r"D-entry make that state unreachable\*, and\s+\*does it make a "
            r"universal claim over a domain no procedure it names enumerates\*",
        )

    def test_ingest_audit_asks_the_questions_of_the_set_not_only_each(self):
        # The set-level read is the half RB07's trigger needed: two criteria
        # can each be satisfiable and still be jointly unsatisfiable, which a
        # per-criterion pass cannot see.
        self.assertRegex(
            brief(),
            r"asked\s+of the set as well as of each criterion",
        )

    def test_ingest_audit_records_its_own_line_on_the_plan_gate_terms(self):
        # M121: the record requirement is stated once at `/milestone-plan`
        # step 3, and this surface carries only a cross-reference to it —
        # the rulebook's step-0 single-home check (D-071), not a step of
        # `/milestone-brief`, whose ingest audit is its own step 3.
        self.assertRegex(
            brief(),
            r"The ingest audit\s+records one work-log line either way, on "
            r"`/milestone-plan` step 3's terms",
        )

    def test_ingest_findings_are_raised_never_softened_away(self):
        self.assertRegex(
            brief(),
            r"What the audit returns is raised with the\s+user, never softened away",
        )


if __name__ == "__main__":
    unittest.main()
