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
    the mandate boundary and its clears-both composition, the three
    per-class confirmation obligations, the record-churn evidence, and the
    yield-based falsifier that replaced the round-count one.
  * `/milestone-implement` step 8, which fires §8 before `status -> review`
    when the milestone authored or edited a prose-guard.

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
        self.assertRegex(
            self.doctrine,
            r"this moves certification, not operation",
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
        self.assertRegex(
            self.doctrine,
            r"It counts yield and not\s+rounds, because the round count is "
            r"precisely what the two rules above change,\s+and a measure its "
            r"own subject can satisfy by construction measures nothing",
        )

    def test_reopening_is_drawn_by_provenance(self):
        # The rule M121 shipped on the wrong object. Stated on what a finding
        # REOPENS, it stops colliding with D-070 (RR09 q1).
        self.assertRegex(
            self.doctrine,
            r"\*\*What\s+a\s+finding\s+reopens\*\*\s+is\s+drawn\s+by\s+\*provenance\*:\s+a\s+finding\s+is\s+grounds\s+for\s+a\s+further\s+round\s+unless\s+its\s+only\s+subject\s+is\s+a\s+\*\*fix\-authored\s+record\*\*\.",
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
        # The compatibility with D-069/D-070: what is lost is round-opening
        # power, never certified scope.
        self.assertRegex(
            self.doctrine,
            r"it\s+never\s+leaves\s+the\s+certified\s+scope,\s+and\s+nothing\s+here\s+narrows\s+that\s+scope",
        )

    def test_mandate_boundary_limits_reopening_to_the_three_checks(self):
        # The rule that actually reaches M119's round count (RR09 rec 5).
        self.assertRegex(
            self.doctrine,
            r"\*\*A\s+round\s+reopens\s+only\s+on\s+a\s+finding\s+within\s+the\s+three\s+named\s+checks\s+above\.\*\*",
        )

    def test_out_of_mandate_observations_route_to_sections_one_to_seven(self):
        # Routed, never dropped. Without the routing clause the boundary reads
        # as licence to ignore a real finding.
        self.assertRegex(
            self.doctrine,
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
        # the confirmation split.
        self.assertRegex(
            self.doctrine,
            r"The\s+gate\s+is\s+therefore\s+reachable\s+with\s+fix\-authored\s+records\s+corrected\s+but\s+not\s+yet\s+independently\s+confirmed\.",
        )

    def test_the_evidence_is_grounded_on_record_churn(self):
        # RR09 q6 defect 2. The withdrawn paragraph offered M119's nine rounds
        # as the measurement for a rule that changes that count by zero; the
        # honest evidence base is the record-churn class.
        self.assertRegex(
            self.doctrine,
            r"\*\*What\s+grounds\s+the\s+provenance\s+rule\s+is\s+record\s+churn,\s+not\s+M119's\s+round\s+count\.\*\*",
        )


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
