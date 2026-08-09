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
    the audit's questions of a binding-criteria set before it is ingested
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


def implement():
    return read("milestone-implement", "SKILL.md")


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

    def test_audit_question_is_asked_of_the_domain_not_a_proxy(self):
        # M132: this sentence is byte-identical to the RR-ingestion surface's
        # copy, which `test_the_domain_match_sentence_is_identical_at_both_surfaces`
        # is what actually enforces — this guard only pins it here.
        self.assertRegex(
            plan(),
            r"The third question is asked of the\s+domain the claim quantifies "
            r"over, never of a proxy the named procedure\s+happens to "
            r"enumerate \(M132\)",
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

    def test_the_procedure_must_cover_the_promises_own_domain(self):
        # M132: intraclass M102's AC2 named an enumerated set and so answered
        # "does it name a procedure?" yes, while the set enumerated command
        # spellings rather than the domain "commands that read history".
        self.assertRegex(
            plan(),
            r"\*\*The procedure must enumerate the domain the criterion's own "
            r"universal\s+quantifies over, not a proxy for it\.\*\*",
        )

    def test_naming_a_procedure_does_not_pass_the_domain_match_test(self):
        # The failing form is identified by its property — membership fixed by
        # author recall — never by the examples, which are non-exhaustive so a
        # family-enumeration (intraclass's pass-3 fix) cannot escape the list.
        self.assertRegex(
            plan(),
            r"Naming a procedure is not passing\s+this test: an enumeration "
            r"whose membership is fixed by what the author\s+recalled, rather "
            r"than decided by a procedure over the domain, is a proxy",
        )

    def test_the_instance_enumeration_examples_are_non_exhaustive(self):
        self.assertRegex(
            plan(),
            r"however long its list — spellings, renderings, known cases and "
            r"whole\s+families among others, never only those",
        )

    def test_the_remedy_is_to_narrow_the_promise_not_widen_the_enumeration(self):
        # Both halves: guard-doctrine §9 already holds that the remedy is not a
        # fifth matcher; M132 adds where a rejected criterion actually goes.
        self.assertRegex(
            plan(),
            r"A counterexample defeating such\s+an enumeration is therefore "
            r"not answered by a wider one; the repair is to\s+narrow the "
            r"promise until a stated procedure settles it",
        )

    def test_audit_asks_the_form_coverage_question(self):
        # M138: circumplex M81's AC1 was "mutation-verified" by one planted
        # exemplar varying location while the parse walk's blind spot was
        # form — a one-exemplar mutation clause is a proxy *verification*,
        # which the domain-match test (a proxy *enumeration* catch) passes.
        self.assertRegex(
            plan(),
            r"Where a criterion cites a mutation, inversion, or planted-defect\s+"
            r"verification, the audit asks whether the probes vary every axis the\s+"
            r"verified domain is free in — form as well as location — or stand one\s+"
            r"exemplar in for the family \(guard-doctrine §1's inversion protocol and\s+"
            r"§4's fixture rule applied to criteria\)",
        )

    def test_the_rule_carries_its_measured_failure(self):
        self.assertRegex(
            plan(),
            r"intraclass M102's\s+\"no command reads git history\", built as a "
            r"set of refused command forms,\s+took three returns beaten by a "
            r"ref spelling, an argument-order bug, and\s+then `awk`, which is "
            r"no git command at all\.",
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

    def test_ingest_audit_states_the_questions_at_this_surface(self):
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

    def test_ingest_audit_carries_the_domain_match_test(self):
        # M132: the sentence is byte-identical to the plan-gate surface's, so a
        # reader meeting either question meets the same test. Review found the
        # first draft differed ("the third question asked" vs "The third
        # question is asked") while two comments claimed identity, and that it
        # had been interjected mid-sentence, repurposing the em-dash that closed
        # the three-question list so "asked of the set as well as of each
        # criterion" attached to the third question alone.
        self.assertRegex(
            brief(),
            r"The third question is asked of the\s+domain the claim quantifies "
            r"over, never of a proxy the named procedure\s+happens to "
            r"enumerate \(M132\)\.",
        )

    def test_the_domain_match_sentence_is_identical_at_both_surfaces(self):
        # Nothing else enforces this: each surface's guard reads only its own
        # file, so without this the two copies drift apart with both green.
        sentence = (
            "The third question is asked of the\n   domain the claim "
            "quantifies over, never of a proxy the named procedure\n   "
            "happens to enumerate (M132)."
        )
        self.assertEqual(plan().count(sentence), 1)
        self.assertEqual(brief().count(sentence), 1)

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

    def test_ingest_audit_carries_the_form_coverage_question(self):
        # M138: the ingest surface carries the same extension, so a
        # binding-criteria set citing a one-exemplar mutation clause is
        # caught before ingestion exactly as at the plan gate.
        self.assertRegex(
            brief(),
            r"Where a criterion cites a mutation, inversion, or planted-defect\s+"
            r"verification, the audit asks whether the probes vary every axis the\s+"
            r"verified domain is free in — form as well as location — or stand one\s+"
            r"exemplar in for the family \(guard-doctrine §1's inversion protocol and\s+"
            r"§4's fixture rule applied to criteria\)",
        )

    def test_the_form_coverage_sentence_is_identical_at_both_surfaces(self):
        # Nothing else enforces this: each surface's guard reads only its own
        # file, so without this the two copies drift apart with both green
        # (the M132 identity guard's reason, applied to the new sentence).
        sentence = (
            "Where a criterion cites a mutation, inversion, or planted-defect\n"
            "   verification, the audit asks whether the probes vary every axis the\n"
            "   verified domain is free in — form as well as location — or stand one\n"
            "   exemplar in for the family (guard-doctrine §1's inversion protocol and\n"
            "   §4's fixture rule applied to criteria)."
        )
        self.assertEqual(plan().count(sentence), 1)
        self.assertEqual(brief().count(sentence), 1)


class TestAmendmentReaudit(unittest.TestCase):
    """M138: `/milestone-implement` step 6 is the audit's third surface —
    amended criterion wording re-enters the questions by pointer to
    `/milestone-plan` step 3, so it inherits later question extensions."""

    def test_criterion_wording_change_is_substantive_by_definition(self):
        # Without this, a criterion edit routes through the Minor arm and
        # escapes the re-audit — the same escape one door over.
        self.assertRegex(
            implement(),
            r"a change to\s+acceptance-criterion wording is \*Substantive\* "
            r"by definition",
        )

    def test_minor_arm_excludes_the_amendment_gated_sections(self):
        self.assertRegex(
            implement(),
            r"refine wording outside the amendment-gated\s+sections — Goal, "
            r"Scope, Acceptance criteria —",
        )

    def test_amended_wording_is_asked_the_three_questions_before_written(self):
        self.assertRegex(
            implement(),
            r"Amended acceptance-criterion wording — an amendment return from\s+"
            r"`/milestone-review` included — is asked the criteria audit's three\s+"
            r"questions as `/milestone-plan` step 3 states them",
        )

    def test_reaudit_reader_is_fresh_context_and_not_the_author(self):
        # The candidate row proposed the session asking its own questions;
        # the plan gate chose the fresh reader because self-reading
        # just-authored wording is the measured failure (D-067).
        self.assertRegex(
            implement(),
            r"by a fresh-context\s+\*\*\[O\]\*\* reader that did not author "
            r"the amended wording, before the\s+amended text is written to "
            r"the milestone file",
        )

    def test_ingest_cleared_wording_is_exempt(self):
        # Session identity is not a recorded fact; the ingest audit's
        # work-log line is (stateless resume, GP2).
        self.assertRegex(
            implement(),
            r"Wording whose clearance the `/milestone-brief` ingest audit's "
            r"work-log\s+line already covers is exempt",
        )

    def test_reentry_is_once_per_criterion_with_its_own_fresh_reader(self):
        # Both the bound and the stop count per criterion (D-097's unit),
        # and round 2 gets its own reader — round 1's is no longer fresh.
        self.assertRegex(
            implement(),
            r"Per criterion, wording fixed at the mini gate re-enters the "
            r"questions\s+once with its own fresh reader, and further churn "
            r"on that criterion\s+goes to the user",
        )


if __name__ == "__main__":
    unittest.main()
