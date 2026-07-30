"""Regression guard: M115's two fresh-context reader instruments.

Both instruments replace an author checking its own work with a reader that
did not write it. This file locks the doctrine text for both, at four
surfaces, including the criteria audit's record requirement at the plan
and ingest surfaces, which M121 added (D-079 clause 2).

The **acceptance-criteria audit** (`TestPlanGateCriteriaAudit`,
`TestRRIngestionCriteriaAudit`):

  * `/milestone-plan`, where the audit runs at the step-3 gate. Three edits
    carry it, because placing the audit alone would have audited a draft:
    step 2 must draft criteria to final wording, step 3 runs the reader, and
    step 4 writes the audited bytes.
  * `/milestone-brief`'s "Ingesting an RR", where the same reader asks the
    same two questions of a binding-criteria set before it is ingested.

**Description-layer certification** (`TestDescriptionLayerCertification`,
`TestImplementRoutesToCertification`):

  * `skills/shared/guard-doctrine.md` §8 — its heading, the
    operation-vs-certification cut, the diagnosis, the before-review
    placement, each of the three checks, the zero-unresolved bar, the
    certification-not-operation clause, the section's own falsifier, and D-069's
    certified-scope bound. M123 (D-083) rebuilds the section and adds the rest:
    the two-axis discriminator, the `fix-authored record` class and the two
    surfaces it does NOT shield (a fix's code/asserts/fixtures, and any record
    predating round 1), the compatibility clause that keeps D-070 untouched,
    the mandate boundary with its clears-both composition, its enumerated
    out-of-mandate class and its does-not-hold-the-gate clause, each of the
    three per-class confirmation obligations, the record-churn grounding and
    the pointers standing where its derivations used to (§8 cites no revision
    of its own — they moved to D-085 at T10), and the yield-based falsifier's
    window and all three clauses: six counted quantities, three consequences
    and three tolerances. RR10's two amendments are here too — the sufficiency
    arm that makes reopening an iff, and clause (iii), which retires the whole
    step on round-1 yield decay.
  * `/milestone-implement` step 8, which fires §8 before `status -> review`
    when the milestone authored or edited a prose-guard.

Four properties OF §8 are checked structurally rather than by anchor, because
no single phrase can carry them: the class is defined and bounded in one
paragraph, it is defined in the paragraph immediately after its first use, it
is never named by a synonym in either direction, and its obligations paragraph
carries one bold label per class with the author named only in the exclusion
clause. Each first shipped in a form that survived its own inversion, and each
comment records how. The last is a disclosed PROXY: AC4's no-second-obligation
clause is section-wide, and what the test enforces is paragraph-scoped.

Anchors are copied from the shipped bytes, never from the draft that
produced them (M95), and every phrase that crosses the files' hard wrap is
matched with `\\s+` rather than a literal newline, so a future reflow does
not red a rule that is still present (M105). Targets are read with
`Path.read_text` because the mutation engine patches only that call (M100).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
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

    def test_ingest_audit_states_both_questions_at_this_surface(self):
        # AC1 requires BOTH surfaces to state the two questions, and the two
        # asserts either side of this clause anchor past it: deleting the
        # questions from the brief left every other assert here green, so
        # `..._asks_the_questions_of_the_set...` reads as covering them and
        # does not. Found by M115's own certifier against its own guard.
        self.assertRegex(
            brief(),
            r"and the same\s+two questions — \*what state of the world "
            r"satisfies this exactly as\s+written\*, and \*does any IP or "
            r"D-entry make that state unreachable\*",
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
            r"the\s+description layer to a fresh-context \[O\] reader that "
            r"authored no part of it",
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
            r"The gate is entered at zero unresolved: every discrepancy is "
            r"fixed, never\s+argued down as imprecision",
        )

    def test_section_moves_certification_not_operation(self):
        # Round 3's F10, re-derived at return 1: the anchor pinned only the
        # consequence, so "The author runs none of it" inverted green — which
        # is the rule the whole section is scoped by, since banning the author
        # from RUNNING its own guard is the wrong rule this clause exists to
        # rule out. The anchor now opens on the premise.
        self.assertRegex(
            self.doctrine,
            r"The\s+author\s+still\s+runs\s+everything\s+—\s+"
            r"this moves certification, not operation",
        )

    def test_the_reader_checks_three_things_and_reports_verbatim(self):
        # Round 3's F10, re-derived at return 1. F10 named this the
        # "fresh-reader placement"; the placement sentence is pinned above and
        # reds. What actually inverted green was the reader's own mandate —
        # "checks any two of three things and reports discrepancies in
        # summary" — which is both the count the mandate boundary calls "the
        # three named checks above" and the verbatim-reporting rule that stops
        # a certifier's report becoming the author's paraphrase of it.
        self.assertRegex(
            self.doctrine,
            r"The\s+reader\s+checks\s+three\s+things\s+and\s+reports\s+"
            r"discrepancies\s+verbatim:",
        )

    def test_section_bounds_the_certified_scope_against_regress(self):
        # M116/D-069: without the exclusion the gate cannot converge — each
        # round must record a verdict, that record is append-only under IP4,
        # so every round manufactures uncertified surface for the next.
        self.assertRegex(
            self.doctrine,
            r"\*\*The certified scope is the work and the records describing "
            r"the work; a record\s+whose subject is a certification round "
            r"itself — the final round's own report\s+included — sits outside "
            r"it\*\* \(D-069\)",
        )

    def test_scope_bound_states_why_it_is_convergence_not_convenience(self):
        # Stated as "hard to reach" the clause reads as a comfort measure and
        # invites tuning the round count instead; the defect is structural.
        self.assertRegex(
            self.doctrine,
            r"the gate cannot converge\s+rather than merely being hard to reach",
        )

    def test_section_carries_its_own_falsifier(self):
        # An adopted step with no stated exit is how a mechanism measured not
        # to work gets tuned instead of retired (D-059). D-083 replaced the
        # round-count falsifier with a yield-based pair; the quantity it counts
        # is the rule, because a round count is what this section's own rules
        # change and so is satisfiable by construction (RR09 q4).
        # A19 (return 1): the anchor started at "It counts yield", so deleting
        # the declarative sentence this test is NAMED for left it green — §8
        # shipped a falsifier nothing said it carried. The anchor now opens on
        # that sentence.
        self.assertRegex(
            self.doctrine,
            r"\*\*This\s+step\s+carries\s+its\s+own\s+falsifier\.\*\*\s+"
            r"It counts yield and not\s+rounds, because the round count is "
            r"precisely what the two rules above change,\s+and a measure its "
            r"own subject can satisfy by construction measures nothing",
        )

    def test_reopening_is_drawn_by_provenance(self):
        # D9 (round 2): stated as 'a finding is grounds for a further round unless
        # ...', provenance read as SUFFICIENT for reopening, contradicting the
        # mandate boundary for an out-of-mandate finding on original text.
        self.assertRegex(
            self.doctrine,
            r"\*\*What\s+a\s+finding\s+reopens\*\*\s+is\s+drawn\s+by\s+\*provenance\*:\s+a\s+finding\s+whose\s+only\s+subject\s+is\s+a\s+\*\*fix\-authored\s+record\*\*\s+is\s+not\s+grounds\s+for\s+a\s+further\s+round\.",
        )

    def test_checked_and_fixed_is_drawn_by_subject_matter(self):
        # The first axis, cited to the entries that drew it. Without both axes
        # named apart, one rule reads as narrowing the other's object.
        self.assertRegex(
            self.doctrine,
            r"\*\*What\s+the\s+reader\s+checks\s+and\s+the\s+author\s+fixes\*\*\s+is\s+drawn\s+by\s+\*subject\s+matter\*:\s+the\s+work\s+and\s+every\s+record\s+about\s+the\s+work\s+are\s+inside,\s+narrative\s+about\s+the\s+certifying\s+process\s+is\s+outside\s+\(D\-069,\s+as\s+narrowed\s+by\s+D\-070\)\.",
        )

    def test_fix_authored_record_names_the_four_record_kinds(self):
        # The excluded class is description-layer records only. Enumerating the
        # kinds is what stops 'text' being read back into it.
        self.assertRegex(
            self.doctrine,
            r"A\s+fix\-authored\s+record\s+is\s+a\s+docstring,\s+a\s+comment,\s+a\s+work\-log\s+line,\s+or\s+a\s+record\s+claim\s+that\s+a\s+previous\s+round's\s+own\s+fix\s+wrote\s+in\s+this\s+same\s+certification\.",
        )

    def test_the_class_has_exactly_one_name(self):
        # Positive framing of the no-unmarked-synonym rule (guard-doctrine section 2:
        # a negative assert is satisfied by blanking, so pin the positive).
        self.assertRegex(
            self.doctrine,
            r"That\s+name\s+is\s+the\s+only\s+one\s+this\s+section\s+gives\s+the\s+class,\s+and\s+where\s+it\s+means\s+anything\s+wider\s+it\s+says\s+so",
        )

    def test_fix_code_and_original_records_stay_round_opening(self):
        # The shield reaches records only. Losing this makes a fix-introduced
        # code regression unable to reopen a round - RR09 q3's broken instrument.
        self.assertRegex(
            self.doctrine,
            r"A\s+fix's\s+code,\s+its\s+asserts\s+and\s+its\s+fixtures\s+are\s+not\s+records\s+and\s+stay\s+ordinary\s+round\-opening\s+surface;\s+so\s+does\s+every\s+record\s+that\s+existed\s+before\s+round\s+1",
        )

    def test_an_original_false_claim_still_reopens(self):
        # M114's seventh-return defect. A draft of this rule deleted it by
        # drawing the class on layer alone rather than on provenance.
        self.assertRegex(
            self.doctrine,
            r"a\s+false\s+claim\s+in\s+an\s+original\s+docstring\s+is\s+the\s+defect\s+this\s+section\s+was\s+built\s+on\s+and\s+it\s+reopens\s+a\s+round\s+no\s+matter\s+who\s+wrote\s+it",
        )

    def test_the_provenance_rule_does_not_narrow_the_certified_scope(self):
        # D6 (round 1): the old wording said a fix-authored record 'never leaves
        # the certified scope', which contradicts D-069 for a record whose subject
        # IS a certification round. Stated as a non-removal rule, both hold.
        self.assertRegex(
            self.doctrine,
            r"\*\*being\s+a\s+fix\-authored\s+record\s+never\s+removes\s+it\s+from\s+the\s+certified\s+scope\*\*,\s+which\s+D\-069\s+draws\s+on\s+subject\s+matter\s+alone",
        )

    def test_mandate_boundary_limits_reopening_to_the_three_checks(self):
        # The rule that actually reaches M119's round count (RR09 rec 5).
        self.assertRegex(
            self.doctrine,
            r"\*\*A\s+round\s+reopens\s+only\s+on\s+a\s+finding\s+within\s+the\s+three\s+named\s+checks\s+above\.\*\*",
        )

    def test_out_of_mandate_observations_route_to_sections_one_to_seven(self):
        # Routed, never dropped. Without the routing clause the boundary reads
        # as licence to ignore a real finding. F1 (round 4): the anchor opened
        # at the PREDICATE, leaving AC3's discriminator — WHICH observations
        # are out of mandate — on no assert, so "an acceptance-criterion clause
        # pins" routed pinned findings out of certification, suite green.
        self.assertRegex(
            self.doctrine,
            r"A\s+robustness\s+observation\s+that\s+no\s+acceptance\-criterion"
            r"\s+clause\s+pins\s+—\s+a\s+surviving\s+mutation,\s+a\s+"
            r"one\-directional\s+pin,\s+a\s+near\-miss\s+control's\s+uncovered"
            r"\s+signature,\s+a\s+fixture\s+weak\s+on\s+an\s+axis\s+no\s+"
            r"criterion\s+names\s+—\s+"
            r"is\s+real\s+work,\s+and\s+it\s+is\s+recorded\s+and\s+fixed\s+as\s+ordinary\s+milestone\s+work\s+under\s+§§1–7\s+and\s+the\s+mutation\s+harness\.\s+It\s+does\s+not\s+reopen\s+certification",
        )

    def test_a_finding_reopens_only_if_it_clears_both_lines(self):
        # The composition. Two independent shields conjoin; either one failing
        # closes the round.
        self.assertRegex(
            self.doctrine,
            r"\*\*A\s+finding\s+reopens\s+a\s+round\s+only\s+if\s+it\s+clears\s+both\s+lines\*\*\s+—\s+it\s+falls\s+within\s+the\s+three\s+checks,\s+and\s+its\s+only\s+subject\s+is\s+not\s+a\s+fix\-authored\s+record",
        )

    def test_each_class_carries_exactly_one_confirmation_obligation(self):
        # The reconciliation RR09 q6 defect 1 names: the section used to carry
        # 'fixed and re-certified' and 'fixed in place' with no rule for which governs.
        self.assertRegex(
            self.doctrine,
            r"\*\*Each\s+class\s+carries\s+exactly\s+one\s+confirmation\s+obligation,\s+and\s+no\s+class\s+carries\s+two\.\*\*",
        )

    def test_no_confirmation_obligation_falls_on_the_author(self):
        # D-067 rejected instructing an author's own re-check; an author
        # re-reading its own corrected record is that move under another name.
        self.assertRegex(
            self.doctrine,
            r"no\s+confirmation\s+obligation\s+falls\s+on\s+the\s+author,\s+because\s+D\-067\s+rejected\s+instructing\s+an\s+author's\s+own\s+re\-check",
        )

    def test_the_falsifier_counts_where_a_finding_was_found(self):
        # Without this the mandate boundary satisfies the falsifier by
        # construction - it routes the very findings the falsifier counts.
        self.assertRegex(
            self.doctrine,
            r"A\s+finding\s+counts\s+where\s+it\s+was\s+\*\*found\*\*,\s+never\s+where\s+it\s+was\s+fixed,\s+so\s+routing\s+one\s+to\s+§§1–7\s+does\s+not\s+remove\s+it\s+from\s+the\s+count",
        )

    def test_the_falsifier_window_carries_a_non_vacuity_floor(self):
        # A window that convened no later round would otherwise retire the
        # later rounds having measured none of them.
        self.assertRegex(
            self.doctrine,
            r"the\s+window\s+counts\s+only\s+if\s+at\s+least\s+one\s+of\s+its\s+three\s+milestones\s+convened\s+a\s+round\s+after\s+its\s+first\s+—\s+a\s+window\s+that\s+never\s+ran\s+a\s+later\s+round\s+has\s+not\s+measured\s+one",
        )

    def test_the_falsifier_second_clause_counts_in_place_fixes_found_false(self):
        # Clause (ii) counts the cost the in-place route creates, which the
        # round-count falsifier could not see.
        self.assertRegex(
            self.doctrine,
            r"If\s+any\s+fix\-authored\s+record\s+corrected\s+in\s+place\s+is\s+later\s+found\s+false\s+—\s+by\s+the\s+three\-lens\s+review,\s+or\s+by\s+a\s+subsequent\s+milestone\s+—\s+then\s+the\s+in\-place\s+route\s+has\s+failed,\s+and\s+that\s+class\s+returns\s+to\s+round\-opening",
        )

    def test_the_evidence_states_the_provenance_rule_saves_no_rounds(self):
        # RR09 q6 defect 2: the withdrawn paragraph offered M119's nine rounds
        # as its supporting measurement for a rule that changes that count by zero.
        self.assertRegex(
            self.doctrine,
            r"On\s+M119's\s+record\s+the\s+provenance\s+rule\s+alone\s+changes\s+the\s+round\s+count\s+by\s+\*\*zero\*\*",
        )

    def test_the_gate_is_reachable_with_records_not_yet_confirmed(self):
        # D-083 part 3. Stated explicitly so the narrowing of D-067's
        # zero-unresolved bar is a disclosed consequence, not an accident of
        # the confirmation split. Re-anchored at T10 when the sentence was
        # compressed and its justification moved to D-085.
        self.assertRegex(
            self.doctrine,
            r"The gate is therefore reachable with fix-authored records "
            r"corrected but not yet\s+independently confirmed",
        )

    def test_the_evidence_is_grounded_on_record_churn(self):
        # RR09 q6 defect 2. The withdrawn paragraph offered M119's nine rounds
        # as the measurement for a rule that changes that count by zero; the
        # honest evidence base is the record-churn class.
        self.assertRegex(
            self.doctrine,
            r"\*\*What\s+grounds\s+the\s+provenance\s+rule\s+is\s+record\s+churn,\s+not\s+M119's\s+round\s+count\.\*\*",
        )

    def test_out_of_mandate_findings_do_not_hold_the_gate(self):
        # D8 (round 1): D-083 part 3(a) claimed the boundary means such a finding
        # does not hold the gate; the shipped text said only that it does not
        # REOPEN. Not-reopening and not-holding-the-gate are different claims.
        self.assertRegex(
            self.doctrine,
            r"\*\*and\s+it\s+does\s+not\s+hold\s+the\s+gate\*\*:\s+the\s+zero\-unresolved\s+bar\s+is\s+met\s+when\s+every\s+discrepancy\s+has\s+been\s+fixed\s+under\s+the\s+obligation\s+its\s+own\s+class\s+carries",
        )

    def test_the_boundary_assigns_the_out_of_mandate_class_its_obligation(self):
        # F4 (round 4): the does-not-hold-the-gate anchor stopped at "under the
        # obligation its own class carries", leaving §8's FOURTH
        # obligation-stating sentence unpinned. Transposed to "discharged by a
        # further round rather than by operation", §8 carried two obligations
        # for one class — AC4's "no class carries two" defeated with the suite
        # green, and outside T14's disclosed residue, which is scoped to
        # clauses added inside the three obligation sentences.
        self.assertRegex(
            self.doctrine,
            r"and\s+this\s+class's\s+obligation\s+is\s+discharged\s+by\s+"
            r"operation\s+rather\s+than\s+by\s+a\s+further\s+round\.",
        )

    def test_the_out_of_mandate_class_is_enumerated(self):
        # D10 (round 1): AC3 names four class members; deleting the whole list left
        # the suite green, so the boundary shipped with no stated extension.
        self.assertRegex(
            self.doctrine,
            r"a\s+surviving\s+mutation,\s+a\s+one\-directional\s+pin,\s+a\s+near\-miss\s+control's\s+uncovered\s+signature,\s+a\s+fixture\s+weak\s+on\s+an\s+axis\s+no\s+criterion\s+names",
        )

    def test_the_three_checks_are_the_whole_mandate(self):
        # D10 (round 1): without this the boundary reads as one limit among
        # several rather than as the exhaustive statement of what reopens.
        self.assertRegex(
            self.doctrine,
            r"Those\s+three\s+are\s+the\s+whole\s+of\s+this\s+step's\s+mandate\.",
        )

    def test_a_reopening_finding_obliges_a_further_round(self):
        # D1 (round 1): invertible to 'obliges nothing further, and the author
        # confirms its own fix' with the whole suite green.
        self.assertRegex(
            self.doctrine,
            r"A\s+\*\*reopening\s+finding\*\*\s+obliges\s+a\s+further\s+fresh\-context\s+round,\s+and\s+that\s+round\s+is\s+what\s+confirms\s+its\s+fix\.",
        )

    def test_a_fix_authored_record_is_confirmed_by_reader_or_review(self):
        # D1 (round 1): the gate-amended route. Invertible to 'confirmed by the
        # author's own re-read ... and otherwise by nobody at all' with the suite
        # green — the criterion the implement gate had just changed.
        self.assertRegex(
            self.doctrine,
            r"A\s+\*\*fix\-authored\s+record\*\*\s+is\s+fixed\s+in\s+place\s+and\s+confirmed\s+by\s+the\s+next\s+round's\s+reader\s+where\s+a\s+further\s+round\s+occurs,\s+and\s+otherwise\s+by\s+`/milestone\-review`'s\s+three\-lens\s+fan\-out\s+at\s+the\s+merge\s+gate",
        )

    def test_an_out_of_mandate_observation_is_confirmed_by_operation(self):
        # D1 (round 1): invertible to 'confirmed by the author's assertion alone'
        # with the suite green.
        self.assertRegex(
            self.doctrine,
            r"An\s+\*\*out\-of\-mandate\s+robustness\s+observation\*\*\s+is\s+confirmed\s+by\s+operation:\s+the\s+harness,\s+the\s+sweeps\s+and\s+the\s+suite",
        )

    def test_the_falsifier_names_its_window(self):
        # D3 (round 1): AC5 requires the window be named; it was changeable to a
        # single milestone with the suite green.
        self.assertRegex(
            self.doctrine,
            r"Measured\s+over\s+the\s+next\s+three\s+guard\-authoring\s+milestones\s+that\s+run\s+§8,\s+the\s+window\s+closing\s+when\s+the\s+third\s+completes",
        )

    def test_the_falsifier_names_both_counted_quantities_and_clause_i_consequence(self):
        # D3 (round 1): both quantities and clause (i)'s consequence inverted green
        # — 'any ... or any ...' and 'keep them and run §8 with unbounded rounds'.
        # F2 (round 4): return 1's A3 fix went to the COPY. Clause (iii) gained
        # its round and window scopes at T13; clause (i) — the clause the defect
        # was FOUND in — kept an anchor opening after both, so "in any single
        # milestone" and "including each milestone's first" both stayed green.
        self.assertRegex(
            self.doctrine,
            r"If\s+the\s+rounds\s+after\s+each\s+milestone's\s+first\s+return,"
            r"\s+totalled\s+across\s+the\s+window,\s+"
            r"zero\s+shipped\-behaviour\s+defects\s+and\s+zero\s+findings\s+whose\s+subject\s+is\s+pre\-round\-1\s+surface,\s+then\s+the\s+rounds\s+after\s+the\s+first\s+have\s+stopped\s+earning\s+their\s+cost\s+—\s+retire\s+them\s+and\s+run\s+§8\s+as\s+a\s+single\s+certification\s+pass",
        )

    def test_the_falsifier_carries_both_tolerances(self):
        # D3 (round 1): the tolerance was changeable to 'at most three on either
        # count' with the suite green. Clause (ii)'s is pinned separately below.
        self.assertRegex(
            self.doctrine,
            r"Tolerance:\s+exact\s+zero\s+on\s+both\s+counts,",
        )

    def test_clause_two_carries_its_tolerance(self):
        # D3 (round 1): changeable to 'five occurrences' with the suite green.
        self.assertRegex(
            self.doctrine,
            r"Tolerance:\s+one\s+occurrence\.",
        )

    def test_the_provenance_rule_is_a_shield_and_not_a_licence(self):
        # D9 (round 2): the sentence that stops the shield being read as a second,
        # competing test for what DOES reopen.
        self.assertRegex(
            self.doctrine,
            r"That\s+is\s+a\s+shield\s+and\s+never\s+a\s+licence\s+—\s+it\s+says\s+which\s+findings\s+cannot\s+reopen\s+a\s+round,\s+and\s+never\s+that\s+anything\s+else\s+must\.",
        )

    def test_the_shield_costs_only_round_opening_power(self):
        # D11 (round 2): invertible to 'the power to be read and corrected at all',
        # which contradicts the bolded non-removal clause one sentence earlier.
        self.assertRegex(
            self.doctrine,
            r"What\s+it\s+loses\s+is\s+only\s+the\s+power\s+to\s+force\s+another\s+round,\s+and\s+never\s+the\s+reading\s+and\s+correcting\s+itself\.",
        )

    def test_the_forward_reference_states_the_rule_it_points_at(self):
        # D12 (round 2): §8 states the exactly-one rule twice; only the second was
        # pinned, so the first inverted to 'at least one' with the suite green.
        self.assertRegex(
            self.doctrine,
            r"the\s+classes\s+are\s+set\s+out\s+below\s+—\s+each\s+carries\s+exactly\s+one,\s+and\s+none\s+carries\s+two\.",
        )

    def test_the_compatibility_with_d070_is_stated(self):
        # D10 (round 2): rewritable to 'D-070 rules on both axes ... a partial
        # supersession' with the suite green — the exact claim D-083 part 4 rests on.
        self.assertRegex(
            self.doctrine,
            r"D\-070\s+rules\s+on\s+the\s+first\s+axis\s+and\s+says\s+nothing\s+about\s+the\s+second,\s+which\s+is\s+why\s+this\s+is\s+compatible\s+with\s+it\s+rather\s+than\s+a\s+partial\s+supersession\s+of\s+it\.",
        )

    def test_clearing_both_lines_is_sufficient_to_reopen(self):
        # RR10 BC1. Reopening carried only NECESSARY conditions, so a reader deep
        # in a loop could derive 'nothing must reopen' with every rule intact.
        self.assertRegex(
            self.doctrine,
            r"\*\*And\s+a\s+finding\s+that\s+clears\s+both\s+lines\s+is\s+a\s+reopening\s+finding\*\*,\s+carrying\s+that\s+class's\s+obligation:\s+a\s+further\s+fresh\-context\s+round\.",
        )

    def test_the_reopening_rule_runs_in_both_directions(self):
        # RR10 q6's live two-readings residue. This sentence is the reason the
        # only-if is stated as an iff rather than left implied.
        self.assertRegex(
            self.doctrine,
            r"Stated\s+as\s+a\s+bound\s+alone\s+it\s+says\s+only\s+which\s+findings\s+cannot\s+reopen\s+a\s+round\s+and\s+never\s+that\s+any\s+must",
        )

    def test_the_falsifier_carries_a_whole_step_retirement_clause(self):
        # RR10 BC2. After D-083 no condition anywhere retired the whole step —
        # round 1 had become unfalsifiable, which is the deficiency RR10 found
        # in what M123 shipped.
        self.assertRegex(
            self.doctrine,
            r"then\s+round\s+1\s+has\s+stopped\s+earning\s+its\s+reader\s+and\s+\*\*the\s+step\s+retires\s+whole\*\*",
        )

    def test_clause_three_counts_anchor_fidelity_findings(self):
        # Deviation from RR10 BC2 (audit F9): as RR10 wrote it, clause (iii)
        # omitted §8's third check, so a window of only anchor-fidelity findings
        # read zero and retired a working instrument.
        self.assertRegex(
            self.doctrine,
            r"and\s+zero\s+anchor\-fidelity\s+findings",
        )

    def test_clause_three_names_its_first_three_counted_quantities(self):
        # A3 (return 1): only the FOURTH quantity was pinned, so the other
        # three inverted green — "returns any shipped-behaviour defects" left
        # the suite passing. This is round 1's D3 defect, found in clause (i)
        # and reproduced in the clause added after it.
        self.assertRegex(
            self.doctrine,
            r"returns\s+zero\s+shipped-behaviour\s+defects,\s+zero\s+false\s+"
            r"claims\s+in\s+records\s+predating\s+that\s+milestone's\s+round\s+"
            r"1,\s+zero\s+acceptance-criterion\s+clauses\s+found\s+unpinned,"
            r"\s+and",
        )

    def test_clause_three_is_totalled_across_the_window(self):
        # A3 (return 1): the window scope inverted green to "in any single
        # milestone", which retires the whole step on one quiet milestone
        # rather than on three.
        self.assertRegex(
            self.doctrine,
            r"If,\s+totalled\s+across\s+the\s+same\s+window,\s+\*\*round\s+1"
            r"\s+itself\*\*",
        )

    def test_clause_three_carries_its_tolerance(self):
        # A3 (return 1): changeable to "at most three on any count" with the
        # suite green. Clause (i)'s and (ii)'s tolerances are pinned above;
        # this was the third, and it was the unpinned one.
        self.assertRegex(
            self.doctrine,
            r"Tolerance:\s+exact\s+zero\s+on\s+all\s+four\s+counts,\s+totalled"
            r"\s+across\s+the\s+window",
        )

    def test_the_overlap_is_settled_by_definition_without_a_tie_break(self):
        # A7 (return 1): AC3 requires §8 state how the mandate boundary
        # composes with the provenance rule. The composition sentence was
        # rewritable to "A separate tie-break rule settles the apparent
        # overlap" — the option the plan gate explicitly declined — green.
        self.assertRegex(
            self.doctrine,
            r"The\s+definition\s+settles\s+the\s+apparent\s+overlap\s+without"
            r"\s+a\s+tie-break:\s+a\s+one-directional\s+pin\s+that\s+leaves\s+"
            r"an\s+acceptance-criterion\s+clause\s+unpinned\s+is\s+a\s+check-1"
            r"\s+finding\s+and\s+reopens,\s+while\s+one\s+that\s+merely\s+"
            r"hardens\s+an\s+assert\s+no\s+criterion\s+names\s+is\s+out\s+of"
            r"\s+mandate\.",
        )

    def test_what_decides_the_overlap_is_the_criterion_clause_at_stake(self):
        # A7 (return 1): the decider transposed green to "what decides is how
        # the finding is phrased" — which is precisely the reading the
        # subject-matter/provenance split exists to forbid.
        self.assertRegex(
            self.doctrine,
            r"What\s+decides\s+is\s+whether\s+a\s+criterion\s+clause\s+is\s+at"
            r"\s+stake,\s+never\s+how\s+the\s+finding\s+is\s+phrased\.",
        )

    def test_clauses_one_and_three_cannot_both_fire(self):
        # Deviation from RR10 BC2 (audit F10): with the sufficiency arm in place,
        # (i) and (iii) had a route to firing on one window with opposite
        # consequences and no stated precedence.
        self.assertRegex(
            self.doctrine,
            r"Clauses\s+\(i\)\s+and\s+\(iii\)\s+cannot\s+both\s+fire:\s+\(i\)\s+requires\s+some\s+milestone\s+to\s+have\s+convened\s+a\s+later\s+round",
        )

    # --- F7 (round 4): the out-of-mandate survivors, FIXED and not merely
    # recorded. §8's own boundary says such a finding "is recorded and fixed as
    # ordinary milestone work under §§1–7", and return 1's A9 established that
    # the round-3 record calling recorded-and-not-fixed what the boundary
    # prescribes was the half that was wrong.

    def test_the_two_axes_compose_rather_than_compete(self):
        self.assertRegex(
            self.doctrine,
            r"The\s+two\s+axes\s+compose\s+rather\s+than\s+compete\.",
        )

    def test_the_two_lines_are_drawn_on_different_axes(self):
        self.assertRegex(
            self.doctrine,
            r"\*\*Two\s+lines\s+govern\s+a\s+round,\s+and\s+they\s+are\s+"
            r"drawn\s+on\s+different\s+axes\*\*",
        )

    def test_failing_either_line_still_closes_the_round(self):
        self.assertRegex(
            self.doctrine,
            r"Failing\s+either,\s+it\s+is\s+fixed\s+under\s+the\s+obligation"
            r"\s+named\s+below\s+and\s+the\s+round\s+still\s+closes\.",
        )

    def test_which_confirmation_applies_depends_on_the_class(self):
        self.assertRegex(
            self.doctrine,
            r"Which\s+confirmation\s+that\s+fix\s+then\s+takes\s+depends\s+on"
            r"\s+the\s+finding's\s+class,",
        )

    def test_the_mandate_boundary_is_what_reaches_the_round_count(self):
        self.assertRegex(
            self.doctrine,
            r"The\s+mandate\s+boundary\s+is\s+the\s+rule\s+that\s+reaches"
            r"\s+that\s+count",
        )

    def test_the_provenance_rule_never_shields_a_coverage_gap(self):
        self.assertRegex(
            self.doctrine,
            r"a\s+coverage\s+gap\s+is\s+a\s+finding\s+about\s+executable"
            r"\s+surface,\s+which\s+the\s+rule\s+never\s+shields\.",
        )

    def test_the_evidence_pointers_name_the_entry_that_holds_them(self):
        # F7 (round 4): AC12 relocated §8's derivations behind pointers, and
        # every pointer's TARGET was unpinned — retargeting D-085 to D-084 left
        # the suite green and `dangling id tokens` clean, because D-084 exists.
        # A pointer to the wrong entry is worse than no pointer: it reads as a
        # citation and resolves.
        self.assertRegex(
            self.doctrine,
            r"The\s+three\s+measured\s+cases\s+and\s+the\s+revisions\s+they"
            r"\s+are\s+read\s+from\s+are\s+recorded\s+at\s+D-085\.",
        )
        self.assertRegex(
            self.doctrine,
            r"What\s+each\s+clause\s+counts\s+is\s+recorded\s+at\s+D-085,"
            r"\s+with\s+the\s+argument\s+that\s+replacing",
        )

    # --- structural properties, which no single-phrase anchor can carry ---
    # These are the "bounded property" cases guard-doctrine §2 sends to a
    # by-hand check. They are automated here instead, because each is a
    # property OF §8 that can be derived from §8 rather than enumerated.

    @property
    def section8(self):
        d = self.doctrine
        return d[d.index("## 8. The author never certifies"):]

    def _paragraph_containing(self, needle):
        # Matched against the whitespace-normalized paragraph and returned
        # raw. A22 (return 1): matching the raw text made every caller's
        # needle a literal-hard-space match, so a content-preserving reflow
        # located no paragraph at all and red a rule still present.
        for para in self.section8.split("\n\n"):
            if needle in " ".join(para.split()):
                return para
        self.fail(f"no §8 paragraph contains {needle!r}")

    def test_the_class_is_defined_and_bounded_in_one_paragraph(self):
        # D16 (round 1): every anchor uses `\s+`, which matches a blank line,
        # so splitting the definition paragraph left AC1's two locality clauses
        # ("defined at first use", "the same paragraph states") unpinned.
        # The property is co-location and is wrap-independent, so the paragraph
        # is whitespace-normalized first — pinning the wrap here would red on
        # any reflow of prose the test is not about (it did, at T10).
        para = " ".join(
            self._paragraph_containing("A fix-authored record is a docstring").split()
        )
        self.assertIn("are not records and stay ordinary", para)
        self.assertIn("every record that existed before round 1", para)
        for marker in (
            "is not grounds for a further round",     # the two-axis paragraph
            "is a docstring, a comment",              # the definition
            "never removes it from the",              # the shield
            "is fixed in place and",                  # the obligations
        ):
            # A22 (return 1): this containment ran against the RAW paragraph
            # and matched a literal hard space, so a content-preserving reflow
            # putting "fix-authored" and "record" on either side of the wrap
            # RED a rule still present — the M105 false-red this file's own
            # docstring warns about, in the loop checking for it. Normalized
            # for the same reason the co-location check above is: naming is
            # wrap-independent.
            para = " ".join(self._paragraph_containing(marker).split())
            self.assertRegex(
                para, r"fix-authored record",
                f"the paragraph at {marker!r} states a rule about the class "
                f"without naming it",
            )

    def test_the_class_is_never_called_by_a_synonym(self):
        # D5 (round 1), D4 (round 2), and DELETED IN ERROR at T10/T11 —
        # restored at round 3's F1, which is the finding that caught it. AC1
        # forbids alternating the class name with an unmarked synonym. Three
        # ways that has been defeated so far: a synonym at the start of a
        # sentence escaping a case-sensitive search; a synonym dropping the
        # prefix entirely ("A shielded record is still read"), unreachable by
        # any search keyed on "fix-authored"; and the compression retiring this
        # test with the evidence asserts, after which "Fix-authored text is
        # neither read nor corrected" shipped green.
        # A4 (return 1): the restored version searched only FORWARD from the
        # prefix, so the very defeat its comment names as fixed still worked —
        # "A shielded record loses only the power to force another round"
        # shipped green. Both directions are checked now.
        flat = " ".join(self.section8.split())
        tails = re.findall(r"fix-authored\W+(\w+)", flat, re.I)
        self.assertTrue(tails, "no occurrences of the class name found")
        self.assertEqual(
            sorted({x.lower() for x in tails}), ["record", "records"],
            f"§8 names the class by a synonym: {sorted(set(tails))}",
        )
        # The other direction: a coined class name is a content-word modifier
        # on "record". Function words and determiners are a closed grammatical
        # class and pass; anything hyphenated or participial is the shape a
        # coinage takes ("shielded", "excluded", "non-reopening"), and only
        # "fix-authored" is licensed. Derived from §8's own modifiers, never
        # from a list of synonyms to look for — that enumeration is the
        # failure §3 names and round 1 already reproduced here once.
        heads = {
            m.group(1).lower()
            for m in re.finditer(r"(\w[\w-]*)\s+records?\b", flat, re.I)
        }
        coined = {
            h for h in heads
            if h != "fix-authored" and ("-" in h or h.endswith(("ed", "ing")))
        }
        self.assertEqual(
            coined, set(),
            f"§8 gives the class a second name: {sorted(coined)}",
        )

    def test_the_class_is_defined_where_it_is_first_used(self):
        # D6 (round 2): AC1 requires the term be "defined at first use". The
        # co-location test pins the definition paragraph's contents, not its
        # position — moving that whole paragraph to the end of the file left
        # every anchor matching and the suite green, with first use 100 lines
        # ahead of the definition.
        # A5 (return 1): "first use" was located by searching for the BOLD
        # rendering, so an earlier unbolded use — the shape a drafting edit
        # actually produces — was invisible and the definition stayed
        # "immediately after" a use that was no longer the first.
        paras = self.section8.split("\n\n")
        first_use = next(
            i for i, para in enumerate(paras)
            if re.search(r"fix-authored", para, re.I)
        )
        defined = next(
            i for i, para in enumerate(paras)
            if "is a docstring, a comment" in " ".join(para.split())
        )
        self.assertEqual(
            defined, first_use + 1,
            f"the class is first used in §8 paragraph {first_use} but defined "
            f"in paragraph {defined}; the definition must immediately follow",
        )

    def test_exactly_three_confirmation_obligations_are_assigned(self):
        # D2 (round 1): AC4's "no class carries two" is a property, not a
        # phrase. Counting known obligation PHRASINGS was the first attempt and
        # it survived its own inversion — a fourth obligation worded any other
        # way was simply not one of the phrasings counted, which is the
        # enumerate-the-renderings failure guard-doctrine §3 names. So count
        # the paragraph's own structure instead: one bold label per class plus
        # the header, and the author named only inside the exclusion clause.
        # This is a PROXY and is disclosed as one (D2/D3, round 2): an
        # unbolded sentence adding an obligation to an existing class, and
        # naming no author, is not reachable by it. AC4's clause is
        # section-wide; what is enforced here is paragraph-scoped.
        para = self._paragraph_containing("Each class carries exactly one")
        self.assertEqual(
            para.count("**") // 2, 4,
            "§8's obligations paragraph should carry the header plus exactly "
            "three bold class labels",
        )
        self.assertEqual(
            len(re.findall(r"\bauthors?\b", para)), 3,
            "a fourth obligation placed on the author would add a mention; "
            "the three here are the exclusion clause and its two grounds",
        )
        # A17 (return 1): the two counts above did not cover the proxy's OWN
        # paragraph — appending an unbolded sentence that names no author
        # ("A reopening finding is in addition confirmed by a re-read at the
        # merge gate.") left both counts unchanged and the suite green. The
        # paragraph's structure is one sentence per class after the header, so
        # count the sentences and require each to open on its class label.
        flat = " ".join(para.split())
        sentences = re.split(r"(?<=\.)\s+|(?<=\.\*\*)\s+", flat)
        self.assertEqual(
            len(sentences), 4,
            "§8's obligations paragraph should be the header plus exactly one "
            f"sentence per class; found {len(sentences)}: {sentences}",
        )
        for sentence in sentences[1:]:
            self.assertRegex(
                sentence, r"^An?\s+\*\*",
                "every sentence after the header states one class's "
                "obligation and opens on that class's bold label",
            )
        # DISCLOSED RESIDUE, narrower than before but not closed: a clause
        # added INSIDE one of the three sentences, naming no author and using
        # no bold, still escapes all four checks. AC4's clause is section-wide
        # and what is enforced here is paragraph-scoped (D2/D3, round 2).


class TestImplementRoutesToCertification(unittest.TestCase):
    """`/milestone-implement` step 8 fires the step §8 defines."""

    def test_completion_step_routes_to_the_certifier_at_zero_unresolved(self):
        self.assertRegex(
            read("milestone-implement", "SKILL.md"),
            r"if this milestone authored or edited a\s+prose-guard, hand its "
            r"description layer to a fresh-context \[O\] reader first",
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
