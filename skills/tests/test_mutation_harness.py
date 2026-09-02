"""Prose-guard mutation harness (M53).

Two jobs:
  1. Prove the engine detects false coverage in *both* directions — a sound
     guard fails when its rule is blanked; a weak (false-coverage) guard does
     not. (`TestEngineOracle`.)
  2. Drive the registry: for every registered (guard, block) pair, blanking
     the block must make the guard fail — a guard that survives its rule's
     deletion is false coverage. (`TestRegisteredGuardsFailWhenBlanked`.)
  3. Enforce completeness: every prose-guard file under `skills/tests/` is
     registered or explicitly exempted. (`TestRegistryCompleteness`.)

Run: python3 -m unittest discover -s skills/tests
"""

import collections
import pathlib
import tempfile
import unittest

import mutation_engine as me


# --------------------------------------------------------------------------
# Registry: one entry per protected rule block. `block` is an exact substring
# of `target` (repo-relative) that the named guard depends on; blanking it must
# make `guard`.`test` fail. `test` is "ClassName.method". A guard file may have
# several entries (one per distinct block it protects).
# --------------------------------------------------------------------------
Mutation = collections.namedtuple("Mutation", "guard test target block")

RULES = "skills/shared/tracking-rules.md"
HOTFIX = "skills/hotfix/SKILL.md"
MILESTONE = "skills/milestone/SKILL.md"
REVIEW = "skills/milestone-review/SKILL.md"
IMPLEMENT = "skills/milestone-implement/SKILL.md"
BRIEF = "skills/milestone-brief/SKILL.md"
RELEASE = "skills/cairn-release/SKILL.md"
GENERIC_PROFILE = "skills/shared/profiles/generic.md"
R_PROFILE = "skills/shared/profiles/r-package.md"
TEMPLATE = "skills/shared/templates/milestone.md"
DOCTRINE = "skills/shared/validation-doctrine.md"
RECORDS_HYGIENE = "skills/shared/records-hygiene.md"
PLAN = "skills/milestone-plan/SKILL.md"
ARCHIVE_TEMPLATE = "skills/shared/templates/archive-summary.md"
README = "README.md"
SOURCE_NOTE = "skills/shared/templates/source-note.md"
SYNTHESIS_NOTE = "skills/shared/templates/synthesis-note.md"

REGISTRY = [
    # M71 (D-042): one entry per positive assert's block — the enumeration,
    # the pairing requirement, and the named enforcement arm each carry the
    # rule independently, so each needs its own mutation proof.
    Mutation(
        guard="test_ac_traceability",
        test="TestTemplateCoverageSection.test_coverage_section_exists",
        target="skills/shared/templates/milestone.md",
        block="## Coverage",
    ),
    # M105: the incremental check-off rule carries independently on two
    # surfaces — the review skill and the rulebook AC-fencing block — so each
    # anchor gets its own mutation proof (M53 per-block discipline).
    Mutation(
        guard="test_ac_traceability",
        test="TestReviewFences.test_checkoff_is_incremental",
        target=REVIEW,
        block="Tick each box as its evidence line is recorded",
    ),
    # M94: the cost line reports and never judges. Three blocks carry the
    # rule independently — the invocation, the reporting-only boundary, and
    # the two prohibitions that give the boundary teeth — so each gets its
    # own mutation proof (M53 per-block discipline).
    Mutation(
        guard="test_cost_audit_line",
        test="TestCostAuditLine.test_the_audit_runs_the_cost_script",
        target=MILESTONE,
        block="cairn_cost.py --audit-line",
    ),
    Mutation(
        guard="test_cost_audit_line",
        test="TestCostAuditLine.test_the_cost_line_is_boundaried_as_reporting_only",
        target=MILESTONE,
        block="a reporting surface only",
    ),
    Mutation(
        guard="test_cost_audit_line",
        test="TestCostAuditLine.test_the_boundary_names_what_it_forbids",
        target=MILESTONE,
        block="never treat a large figure as a finding to act on",
    ),
    # M94 review F8: the remaining three assertions were unregistered while
    # the file's docstring claimed every one was covered — M53's own review
    # caught the identical overclaim. Registered rather than de-claimed: each
    # phrase carries a rule that can otherwise be deleted with the suite green.
    Mutation(
        guard="test_cost_audit_line",
        test="TestCostAuditLine.test_the_audit_reports_the_line_verbatim",
        target=MILESTONE,
        block="report its one line verbatim",
    ),
    Mutation(
        guard="test_cost_audit_line",
        test="TestCostAuditLine.test_no_governing_mechanism_is_owed",
        target=MILESTONE,
        block="D-057 closed",
    ),
    # M101: the rulebook-mass reporting line (D-057's M96 fold) — the
    # measurement instruction, its seeded baseline, and the no-machinery
    # boundary each carry the rule independently (M53 per-block discipline).
    Mutation(
        guard="test_cost_audit_line",
        test="TestCostAuditLine.test_the_audit_reports_rulebook_mass_beside_the_cost_line",
        target=MILESTONE,
        block="report the rulebook's mass the same way",
    ),
    Mutation(
        guard="test_cost_audit_line",
        test="TestCostAuditLine.test_the_rulebook_line_carries_its_seeded_baseline",
        target=MILESTONE,
        block="467 lines / 43,454 chars",
    ),
    Mutation(
        guard="test_cost_audit_line",
        test="TestCostAuditLine.test_the_rulebook_line_is_reporting_only_with_no_machinery",
        target=MILESTONE,
        block="no threshold, no verdict, no pass machinery",
    ),
    Mutation(
        guard="test_cost_audit_line",
        test="TestCostAuditLine.test_the_subagent_gap_is_stated_where_the_number_is_read",
        target=MILESTONE,
        block="the store does not record",
    ),
    # M88 (D-050): release timing is the maintainer's to declare. Three
    # surfaces carry the rule independently — the governance rule, the
    # `blocked` widening plus its transitions, and the two skills that would
    # otherwise nominate a release — so each protected block gets its own
    # mutation proof (M53 per-block discipline).
    Mutation(
        guard="test_release_timing",
        test="TestReleaseTimingRule.test_rule_states_who_declares_release_timing",
        target=RULES,
        block="Release timing is user-declared, never agent-proposed",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestBlockedCoversTheReleaseWindow.test_parking_transitions_are_legal_from_both_routable_states",
        target=RULES,
        block="`planned → blocked` and `review → blocked` are both legal",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestPlanReleaseTripwire.test_tripwire_is_declared_with_its_authority",
        target="skills/milestone-plan/SKILL.md",
        block="Release timing is user-declared, never agent-proposed (tracking-rules; D-050)",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestPlanReleaseTripwire.test_tripwire_default_is_no",
        target="skills/milestone-plan/SKILL.md",
        block="the default answer is no — absent a declaration the work lands as a `candidate` row, never as a `planned` milestone",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestPlanReleaseTripwire.test_tripwire_exempts_release_tooling",
        target="skills/milestone-plan/SKILL.md",
        block="Work *about* release tooling — a release-walk slot, release docs — is ordinary milestone work, not a release.",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_audit_reports_the_warn_without_arguing",
        target=MILESTONE,
        block="A `release window` WARN is reported, never argued with — release timing is the user's to declare (D-050)",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_audit_refuses_to_treat_the_warn_as_a_prompt_to_ship",
        target=MILESTONE,
        block="never treat the WARN as a prompt to get the release moving",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_advisory_owns_idleness_against_the_staleness_bullet",
        target=MILESTONE,
        block="is not re-reported under the Staleness bullet",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_advisory_owns_idleness_against_the_staleness_bullet",
        target=MILESTONE,
        block="idleness question for every release-shaped milestone",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_staleness_signal_discounts_bookkeeping_entries",
        target=MILESTONE,
        block="the last work-log line that records actual progress",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_staleness_signal_discounts_bookkeeping_entries",
        target=MILESTONE,
        block="Clock-neutral bookkeeping — a `Depends-on` amendment, a status/mirror catch-up, and a git-reconciliation catch-up line",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_staleness_signal_discounts_bookkeeping_entries",
        target=MILESTONE,
        block="Release-shaped milestones are exempt",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_a_recommendation_naming_something_else_keeps_the_lead",
        target=MILESTONE,
        block="that recommendation is legitimate and keeps the lead",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_route_offers_the_park_option",
        target=MILESTONE,
        block="Park M<NNN> as `blocked` → the release window is not open",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_park_leads_the_chip_only_when_cairn_next_names_that_release",
        target=MILESTONE,
        block="lead the close block with it only when `cairn_next`'s own recommendation names that same release milestone",
    ),
    # M111: the GitHub-release handoff — /cairn-release step 4 provides a
    # conditional `gh release create`, never runs it. Each protected block
    # carries one facet of the rule independently (M53 per-block discipline):
    # the GitHub+gh condition, the clean off-GitHub skip, provided-not-run,
    # the changelog-section body, the --notes-file mechanism, and the generic
    # profile's parity mention.
    Mutation(
        guard="test_github_release_handoff",
        test="TestGithubReleaseHandoff.test_command_is_gated_on_github_origin_and_gh",
        target=RELEASE,
        block="remote (`git remote get-url origin` names `github.com`) and `gh` is",
    ),
    Mutation(
        guard="test_github_release_handoff",
        test="TestGithubReleaseHandoff.test_command_is_skipped_cleanly_off_github",
        target=RELEASE,
        block="absent, omit this command with no failure — the tag alone is the release.",
    ),
    Mutation(
        guard="test_github_release_handoff",
        test="TestGithubReleaseHandoff.test_cairn_provides_but_never_runs_the_command",
        target=RELEASE,
        block="provides this command; it never runs it",
    ),
    Mutation(
        guard="test_github_release_handoff",
        test="TestGithubReleaseHandoff.test_release_body_is_the_consolidated_changelog_section",
        target=RELEASE,
        block="whose body is the changelog section you just",
    ),
    Mutation(
        guard="test_github_release_handoff",
        test="TestGithubReleaseHandoff.test_notes_are_passed_by_notes_file_matching_the_changelog",
        target=RELEASE,
        block="`--notes-file`, so the published release reads identically to the",
    ),
    Mutation(
        guard="test_github_release_handoff",
        test="TestGithubReleaseHandoff.test_generic_profile_slot_names_the_handoff",
        target=GENERIC_PROFILE,
        block="provides a `gh release create` command whose body is the new changelog",
    ),
    # M171: the per-stretch cadence — one entry per rulebook test method, each
    # pinning its first positive assert (M53 discipline, by-hand check for the
    # rest): the mandate, the carve-out, the title shape, the re-emit.
    Mutation(
        guard="test_chapter_marker_mandate",
        test="TestChapterMarkerMandate.test_rulebook_declares_the_per_stretch_mandate",
        target=RULES,
        block="Mark a chapter at each phase transition",
    ),
    Mutation(
        guard="test_chapter_marker_mandate",
        test="TestChapterMarkerMandate.test_rulebook_keeps_the_session_start_carve_out",
        target=RULES,
        block="(session start implicit)",
    ),
    Mutation(
        guard="test_chapter_marker_mandate",
        test="TestChapterMarkerMandate.test_rulebook_states_the_title_shape",
        target=RULES,
        block="A chapter's title opens with the item's positional label",
    ),
    Mutation(
        guard="test_chapter_marker_mandate",
        test="TestChapterMarkerMandate.test_rulebook_phase_header_re_emits_at_session_start",
        target=RULES,
        block="pair is emitted at each session start",
    ),
    # M59 (RR01 rec 7): cairn-init §0's fallback follows the canonical recipe —
    # one Mutation entry per new positive assert (M53 discipline); the paired
    # assertNotIn("show-current") rides on these positives (M54 lesson).
    Mutation(
        guard="test_default_branch_parameterized",
        test="TestDefaultBranchParameterized.test_cairn_init_fallback_matches_canonical_recipe",
        target="skills/cairn-init/SKILL.md",
        block="git ls-remote --symref origin HEAD",
    ),
    Mutation(
        guard="test_default_branch_parameterized",
        test="TestDefaultBranchParameterized.test_cairn_init_fallback_matches_canonical_recipe",
        target="skills/cairn-init/SKILL.md",
        block="never guess the local current branch",
    ),
    Mutation(
        guard="test_design_interview",
        test="TestDesignInterviewSkill.test_phase1_banks_never_classifies",
        target="skills/design-interview/SKILL.md",
        block="**banked-candidates ledger**",
    ),
    # M63: the note-and-leave ingestion path — one entry per positive assert's
    # primary block (secondary asserts ride along; none passes pre-M63 text).
    Mutation(
        guard="test_design_interview",
        test="TestNoteAndLeaveIngestion.test_session_start_detects_preserved_file",
        target="skills/design-interview/SKILL.md",
        block="check for a migration-preserved",
    ),
    Mutation(
        guard="test_design_interview",
        test="TestNoteAndLeaveIngestion.test_ingestion_section_exists",
        target="skills/design-interview/SKILL.md",
        block="## Ingesting a note-and-leave principles file",
    ),
    Mutation(
        guard="test_design_interview",
        test="TestNoteAndLeaveIngestion.test_ingested_candidates_carry_lineage",
        target="skills/design-interview/SKILL.md",
        block="carries its `#N` lineage",
    ),
    Mutation(
        guard="test_design_interview",
        test="TestNoteAndLeaveIngestion.test_conservation_no_silent_drop",
        target="skills/design-interview/SKILL.md",
        block="**Conservation: no ingested principle is silently dropped.**",
    ),
    Mutation(
        guard="test_design_interview",
        test="TestNoteAndLeaveIngestion.test_writeout_records_lineage_map",
        target="skills/design-interview/SKILL.md",
        block="old-`#N` → new-id mapping table",
    ),
    Mutation(
        guard="test_design_interview",
        test="TestNoteAndLeaveIngestion.test_preserved_file_stays_intact_until_repoint",
        target="skills/design-interview/SKILL.md",
        block="**The preserved file stays intact.**",
    ),
    Mutation(
        guard="test_design_interview",
        test="TestNoteAndLeaveIngestion.test_repoint_banked_never_code_edits",
        target="skills/design-interview/SKILL.md",
        block="**Bank the repoint; never touch code.**",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonsLoop.test_weight_caps_states_lessons_cap",
        target=RULES,
        block="`LESSONS.md` < 50 lines",
    ),
    # M76 (D-045): one entry per positive assert. The two label->rule blocks
    # are deliberately label-INCLUSIVE — registration is per file, so sound
    # entries elsewhere in this file would mask a clause-only pin (M74/F3).
    # The paired `assertNotIn` (file map no longer says append-only) carries
    # no entry: blanking cannot restore an absence (M54).
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_rule_is_named",
        target=RULES,
        block="Correcting a record proven false",
    ),
    # M119 (D-075): the decisions advisory's subject, and its stated↔emitted
    # label coupling — two distinct physical spans of one sentence, so two
    # entries. The label entry follows the precedent set by the work-log
    # `test_stated_advisory_label_matches_the_emitted_label` registration: its
    # rulebook half IS a prose block, so blanking it proves the guard catches
    # the deletion rather than only the registration going missing.
    # M92 (D-051): the retirement rule. One entry per positive assert, since
    # registration is per FILE and the sound entries above would otherwise mask
    # a missing pin (M53). Each criterion block is label-INCLUSIVE for the same
    # reason M76's are: blanking is not swapping, so the label and its
    # discriminating test share one physical line and were additionally
    # verified by INVERSION (M74) — transposing the rule reddens each guard.
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_rule_is_named",
        target=RULES,
        block="Retiring a lesson that no longer earns its line",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_retirement_wired_into_review_hygiene",
        target=REVIEW,
        block="Retire what this milestone covered",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_review_hygiene_forbids_a_full_resweep",
        target=REVIEW,
        block="**Scope this to what the milestone shipped — never re-sweep every lesson.**",
    ),
    # M76/F1: the mechanism asserts left the ENUMERATIONS unguarded — a
    # reviewer proved a set-swap kept all six green. These three pin label
    # and members together, so an inversion breaks the anchor.
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_history_set_is_enumerated_under_its_own_label",
        target=RULES,
        block="History — `DECISIONS.md`, work-logs, the milestone-local `## Decisions` section,",
    ),
    # M119/RR08 BC1: the enumeration's second physical line. Registration is
    # per FILE, so the sound entry above would otherwise mask a wrap-line pin
    # that never existed (M53's reason for one entry per assert).
    # M55: the milestone cap exempts the review-exclusive `## Review` section.
    # Two blocks — the exemption rationale and the plan-owned-body cap number —
    # each guarded by its own assert (one Mutation entry per positive assertIn).
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_weight_caps_states_the_plan_owned_body_cap",
        target=RULES,
        block="plan-owned body < 150 lines",
    ),
    # M69: the single-pass compression remedy — one Mutation entry per new
    # positive assert (M53 discipline); both anchors sit on one physical line.
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_weight_caps_states_single_pass_compression",
        target=RULES,
        block="never a nibble-and-recount loop",
    ),
    # M77/D-046: the work-log exemption. One entry per new positive assert
    # (M53). Blanking proves deletion is caught; the set-membership assert
    # additionally survives a SWAP, which blanking cannot simulate (M76) —
    # that half is proven by the by-hand swap recorded in the work log.
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_template_work_log_comment_states_the_exemption",
        target=TEMPLATE,
        block="EXEMPT from the 150-line cap (D-046)",
    ),
    # M118/D-074: the third exempt member. One entry per new positive assert
    # (M53), same as M77 got for the second.
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_template_decisions_comment_states_the_exemption_and_its_reason",
        target=TEMPLATE,
        block="EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log",
    ),
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_template_review_comment_names_all_three_exempt_sections",
        target=TEMPLATE,
        block="as are the work log (D-046) and the decisions section (D-074)",
    ),
    # The stated↔enforced label coupling registers too, unlike its cap-number
    # sibling: that one compares two computed numbers, but this one's rulebook
    # half IS a prose block, so blanking the label proves the guard catches its
    # deletion. Registered because M77's AC4 says every new assert registers —
    # the "computed couplings are exempt" reading would have been a review-time
    # reinterpretation of the criterion.
    # M84: the second weight axis. One entry per positive assert on a prose
    # block (M53). The axis->remedy entry is deliberately pair-INCLUSIVE per
    # M74/M76 — both mappings on one physical line, since registration is per
    # file and the sound entries above would mask a mechanism-only pin. The
    # stated<->enforced THRESHOLD assert carries no entry, following its
    # `test_stated_cap_matches_enforced_cap` sibling: both of its halves are
    # computed numbers, not prose a blanking could remove. The LABEL assert
    # does register — its rulebook half is a prose block.
    # M101 (D-058): the whole-file axis's decommissioning is itself a rule —
    # stated as the retirement sentence, which is the positive framing the
    # no-threshold negative asserts pair with.
    # M59 (RR01 rec 7): run-and-read — skills never enumerate validate's
    # internals; one entry per positive assert, negatives ride along (M54).
    Mutation(
        guard="test_run_and_read_checks",
        test="TestReviewRunsAndReads.test_review_runs_and_reads_never_restates",
        target="skills/milestone-review/SKILL.md",
        block="restate or recall its internals",
    ),
    Mutation(
        guard="test_run_and_read_checks",
        test="TestReviewRunsAndReads.test_coverage_completeness_is_validate_output_not_manual",
        target="skills/milestone-review/SKILL.md",
        block="mechanical since M34",
    ),
    Mutation(
        guard="test_run_and_read_checks",
        test="TestMilestoneRunsAndReads.test_milestone_audit_runs_and_reads_never_restates",
        target="skills/milestone/SKILL.md",
        block="read its output — one line per check",
    ),
    # M59 (RR01 rec 12): the protocol body moved to its own module — the
    # blanked block moves with it, and the new progressive-disclosure seam
    # gets its own entries (M58 precedent).
    Mutation(
        guard="test_migration_guidance",
        test="TestMigrationGuidance.test_reference_sweep_names_two_dispositions",
        target="skills/shared/migration-protocol.md",
        block="Reference sweep",
    ),
    Mutation(
        guard="test_migration_guidance",
        test="TestProgressiveDisclosure.test_module_carries_the_protocol",
        target="skills/shared/migration-protocol.md",
        block="migrate the living, entomb the dead",
    ),
    Mutation(
        guard="test_migration_guidance",
        test="TestProgressiveDisclosure.test_skill_points_at_module_on_footprint_only",
        target="skills/cairn-init/SKILL.md",
        block="migration-protocol.md",
    ),
    # M67 (D-039): the narration-discipline rule — one entry per positive
    # assert's primary block (M53 discipline); the allowance asserts ride on
    # the bar and carve-out blocks.
    # M58: the doctrine body moved to its own module; the ≥2-types block now
    # lives (and is blanked) there. The rulebook keeps a reference + the
    # placement norm, and the module gains the registry pointer — one
    # Mutation entry per new positive assert (M53 discipline).
    Mutation(
        guard="test_oracle_doctrine",
        test="TestOracleDoctrine.test_states_the_two_independent_types_bar",
        target="skills/shared/validation-doctrine.md",
        block="≥2 *independent* oracle types",
    ),
    Mutation(
        guard="test_oracle_doctrine",
        test="TestModuleExtraction.test_rulebook_points_at_the_module",
        target=RULES,
        block="lives in `skills/shared/validation-doctrine.md`, a module of",
    ),
    Mutation(
        guard="test_oracle_doctrine",
        test="TestRegistryPointer.test_registry_pointer_is_required",
        target="skills/shared/validation-doctrine.md",
        block="declares *where* its oracle records live",
    ),
    Mutation(
        guard="test_oracle_doctrine",
        test="TestRegistryPointer.test_pointer_absence_is_the_audit_finding",
        target="skills/shared/validation-doctrine.md",
        block="absence of the line in a repo with numeric work is itself the audit",
    ),
    # M57: the two references/ page types + the page⇒INDEX-line rule. One
    # Mutation entry per positive assertIn (M53 discipline).
    Mutation(
        guard="test_references_pages",
        test="TestReferencesPages.test_file_map_names_both_page_types",
        target=RULES,
        block="Source notes (`<citekey>.md`), synthesis notes",
    ),
    # M80: the authoring trigger — WHEN a page is owed — lives in core, not in
    # the numeric-gated module (LESSONS :49). One entry per positive assertIn;
    # the absence-assert on the module has no entry, since blanking cannot
    # restore an absence (M54) — its positive twin below is what locks it.
    Mutation(
        guard="test_references_pages",
        test="TestAuthoringTrigger.test_module_defers_the_trigger_instead_of_restating_it",
        target=DOCTRINE,
        block="Do not restate the trigger here",
    ),
    # M103: supply-push exploration doctrine — one entry per positive assertIn
    # in TestExploratorySources. Blocks are the real file bytes (the guard's
    # asserts lowercase; these match the case as written in tracking-rules).
    Mutation(
        guard="test_references_pages",
        test="TestExploratorySources.test_plan_skill_recognizes_exploratory_ingestion",
        target="skills/milestone-plan/SKILL.md",
        block="triage them for prospective oracles or methods rather than dismissing them as uncited",
    ),
    # M78: the standing-fact / dated-observation split + page provenance.
    # Each definition is registered separately and each block is the label
    # WITH its enumeration, so blanking one cannot leave the other's assert
    # standing in for it (M74/M76: a label→SET guard must pin both).
    # M81: the re-verification expectation and its recording location. Two
    # entries, because the expectation without the location reads as satisfied
    # by the central ledger M56 rejected.
    Mutation(
        guard="test_source_note_template",
        test="TestClaimSplitDoctrine.test_module_defers_the_universal_rules_to_the_rulebook",
        target="skills/shared/validation-doctrine.md",
        block='are universal file-family rules and live in tracking-rules',
    ),
    # M101: the prior-PR lens repoint — primary evidence is the archived
    # `## Review` sections, the PR-thread walk is probe-gated, and the no-op
    # contract is restated for the new surfaces. One entry per positive
    # assert's block (M53 discipline).
    Mutation(
        guard="test_review_fanout",
        test="TestPriorPRLens.test_primary_evidence_is_archived_review_sections",
        target=REVIEW,
        block="Primary evidence: archived",
    ),
    Mutation(
        guard="test_review_fanout",
        test="TestPriorPRLens.test_pr_thread_read_is_probe_gated",
        target=REVIEW,
        block="Secondary surface, probe-gated",
    ),
    Mutation(
        guard="test_review_fanout",
        test="TestPriorPRLens.test_always_spawns_and_noops_when_empty",
        target=REVIEW,
        block='reports "no prior-review evidence"',
    ),
    # M86 (D-048): the three handoff steps each carry the directive
    # independently — one skill losing it must not be masked by the other two.
    Mutation(
        guard="test_copy_run_handoffs",
        test="TestReviewCloseIsAHandoff.test_close_directs_the_commands_into_a_fenced_block",
        target=REVIEW,
        block="commands go in fenced blocks, never inline backticks",
    ),
    Mutation(
        guard="test_copy_run_handoffs",
        test="TestBriefManualRunIsAHandoff.test_manual_run_prompt_goes_in_a_fenced_block",
        target=BRIEF,
        block="fenced block, never a blockquote or inline backticks",
    ),
    Mutation(
        guard="test_copy_run_handoffs",
        test="TestReleaseChecklistIsAHandoff.test_terminal_actions_checklist_names_the_fenced_form",
        target=RELEASE,
        block="so each goes in a fenced block, never inline backticks",
    ),
    Mutation(
        guard="test_section_allow_lists",
        test="TestSectionAllowLists.test_write_mode_legend_defines_core_verbs",
        target=RULES,
        block="**mirror-update**",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestPythonProfile.test_python_release_walk_hands_off_and_self_submits_nothing",
        target="skills/shared/profiles/python.md",
        block="self-submits nothing",
    ),
    # Second entry for test_toolchain_profiles — the exact M47-lesson scenario
    # (the generic release-walk `commit` step): a file may carry >1 entry.
    Mutation(
        guard="test_toolchain_profiles",
        test="TestReleaseSkillReadsProfile.test_generic_release_walk_defines_a_tag_path",
        target="skills/shared/profiles/generic.md",
        block="commit the release prep to the default",
    ),
    # M68 (D-040): the changelog seventh slot — one entry per positive assert
    # across the six surfaces the milestone adds (M53 discipline).
    Mutation(
        guard="test_toolchain_profiles",
        test="TestChangelogSlot.test_each_profile_declares_its_changelog",
        target="skills/shared/profiles/r-package.md",
        block="**`NEWS.md`** (the R-package convention)",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestChangelogSlot.test_each_profile_declares_its_changelog",
        target="skills/shared/profiles/python.md",
        block="**`CHANGELOG.md`**",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestChangelogSlot.test_each_profile_declares_its_changelog",
        target="skills/shared/profiles/generic.md",
        block="**declare it here**",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestChangelogSlot.test_hotfix_reads_the_changelog_slot",
        target="skills/hotfix/SKILL.md",
        block="the file the active profile's `changelog` slot",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestChangelogSlot.test_release_reads_the_declared_changelog",
        target="skills/cairn-release/SKILL.md",
        block="the file the active profile's `changelog` slot names",
    ),
    # M70: the docker-image profile — deletion anchors for its two distinctive
    # slots (the verify lint+build gate and the self-pushes-nothing release-walk).
    Mutation(
        guard="test_toolchain_profiles",
        test="TestDockerImageProfile.test_docker_verify_gates_lint_and_build_scan_optional",
        target="skills/shared/profiles/docker-image.md",
        block="`hadolint Dockerfile` clean and `docker build` succeeds",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestDockerImageProfile.test_docker_release_walk_pushes_to_registry_and_self_pushes_nothing",
        target="skills/shared/profiles/docker-image.md",
        block="cairn pushes nothing",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestInitSelection.test_init_selects_docker_and_runs_the_disambiguation_gate",
        target="skills/cairn-init/SKILL.md",
        block="asking which is the primary deliverable",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestRulebookNamesFourProfiles.test_rulebook_names_four_profiles",
        target=RULES,
        block="Four profiles ship",
    ),
    # M58 (RR01 rec 4): universal change-governance stated once in core; one
    # Mutation entry per positive core assert (M53 discipline).
    Mutation(
        guard="test_toolchain_profiles",
        test="TestUniversalChangeGovernance.test_core_states_the_dependency_gate",
        target=RULES,
        block="Dependency changes are never unilateral",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestUniversalChangeGovernance.test_core_states_the_deprecation_cycle",
        target=RULES,
        block="follow a deprecation cycle",
    ),
    # M54 positioning + DESIGN-honesty guards (RR01 recs 1/5). One or more
    # exemplar blocks per protected file; blanking each fails its guard method.
    Mutation(
        guard="test_positioning_guard",
        test="TestOutwardPositioning.test_plugin_json_uses_profile_framing",
        target=".claude-plugin/plugin.json",
        block="language-agnostic core with per-repo toolchain profiles",
    ),
    Mutation(
        guard="test_positioning_guard",
        test="TestOutwardPositioning.test_marketplace_uses_profile_framing",
        target=".claude-plugin/marketplace.json",
        block="language-agnostic core, per-repo toolchain profiles",
    ),
    Mutation(
        guard="test_positioning_guard",
        test="TestOutwardPositioning.test_readme_para1_uses_profile_framing",
        target="README.md",
        block="language-agnostic",
    ),
    Mutation(
        guard="test_positioning_guard",
        test="TestDesignArchitectureHonesty.test_design_lists_all_seven_hooks",
        target="cairn/DESIGN.md",
        block="commit_guard",
    ),
    Mutation(
        guard="test_positioning_guard",
        test="TestDesignArchitectureHonesty.test_design_lists_all_seven_hooks",
        target="cairn/DESIGN.md",
        block="memory_guard",
    ),
    # M60 git-safety hooks: DESIGN must name both new hooks… and the
    # standalone merge_guard mention is registrable only via a longer
    # unique anchor (bare "merge_guard" occurs twice as a substring; the
    # guard's word-bounded regex is what makes blanking this block fail).
    Mutation(
        guard="test_positioning_guard",
        test="TestDesignArchitectureHonesty.test_design_lists_all_seven_hooks",
        target="cairn/DESIGN.md",
        block="`merge_guard` (single-use",
    ),
    Mutation(
        guard="test_positioning_guard",
        test="TestDesignArchitectureHonesty.test_design_lists_all_seven_hooks",
        target="cairn/DESIGN.md",
        block="force_push_guard",
    ),
    Mutation(
        guard="test_positioning_guard",
        test="TestDesignArchitectureHonesty.test_design_lists_all_seven_hooks",
        target="cairn/DESIGN.md",
        block="merge_guard_post",
    ),
    # M62: the governed-LLM-Wiki README framing (M56 verdict) — one entry per
    # new positive assert (M53); both phrases sit on one physical line (M59).
    Mutation(
        guard="test_positioning_guard",
        test="TestOutwardPositioning.test_readme_carries_the_llm_wiki_framing",
        target="README.md",
        block="governed LLM Wiki for project state",
    ),
    Mutation(
        guard="test_positioning_guard",
        test="TestOutwardPositioning.test_readme_carries_the_llm_wiki_framing",
        target="README.md",
        block="the agent maintains it, you gate it",
    ),
    # …and the rulebook must keep recording their mechanical backing
    # (test_git_safety_hooks, one entry per new positive assert — M53).
    Mutation(
        guard="test_positioning_guard",
        test="TestDesignArchitectureHonesty.test_ip1_names_the_default_branch",
        target="cairn/DESIGN.md",
        block="Nothing reaches the default branch",
    ),
    Mutation(
        guard="test_positioning_guard",
        test="TestDesignArchitectureHonesty.test_known_issues_are_current",
        target="cairn/DESIGN.md",
        block="enforced as prose",
    ),
    Mutation(
        guard="test_positioning_guard",
        test="TestTemplateBoundaryRule.test_template_names_the_lessons_home",
        target="skills/shared/templates/claude-md-section.md",
        block="Lessons → LESSONS",
    ),
    # M61: python profile CI-pair parity (graduates the M52-banked
    # candidate) — one entry per new positive assert (M53 discipline); the
    # retention assert rides on the pre-existing line.
    Mutation(
        guard="test_toolchain_profiles",
        test="TestPythonCodecovCI.test_names_the_python_ci_pair",
        target="skills/shared/profiles/python.md",
        block="`pytest --cov` (pytest-cov) and uploads to Codecov",
    ),
    Mutation(
        guard="test_toolchain_profiles",
        test="TestPythonCodecovCI.test_coverage_reporting_is_diagnostic_only",
        target="skills/shared/profiles/python.md",
        block="never gates the merge",
    ),
    # M61: migration dry-run mode (RR01 §10.3) — one entry per positive
    # assert (M53 discipline).
    Mutation(
        guard="test_migration_guidance",
        test="TestMigrationGuidance.test_dry_run_mode_is_read_only_and_offered_at_entry",
        target="skills/shared/migration-protocol.md",
        block="**Dry-run mode (read-only first contact",
    ),
    Mutation(
        guard="test_migration_guidance",
        test="TestMigrationGuidance.test_dry_run_mode_is_read_only_and_offered_at_entry",
        target="skills/shared/migration-protocol.md",
        block="Offer a dry run on",
    ),
    Mutation(
        guard="test_migration_guidance",
        test="TestMigrationGuidance.test_dry_run_mode_is_read_only_and_offered_at_entry",
        target="skills/shared/migration-protocol.md",
        block="no branch, no file moves, no commits",
    ),
    Mutation(
        guard="test_migration_guidance",
        test="TestMigrationGuidance.test_dry_run_mode_is_read_only_and_offered_at_entry",
        target="skills/shared/migration-protocol.md",
        block="unrecognized or outside the known precursor lineages",
    ),
    # M61: cairn-init §0 environment check (RR01 §10.2) — one entry per
    # positive assert (M53 discipline).
    Mutation(
        guard="test_env_check",
        test="TestEnvCheck.test_env_check_opens_section_0",
        target="skills/cairn-init/SKILL.md",
        block="**Environment check (RR01 §10.2).**",
    ),
    Mutation(
        guard="test_env_check",
        test="TestEnvCheck.test_only_git_is_fatal",
        target="skills/cairn-init/SKILL.md",
        block="only a missing `git` is fatal",
    ),
    Mutation(
        guard="test_env_check",
        test="TestEnvCheck.test_only_git_is_fatal",
        target="skills/cairn-init/SKILL.md",
        block="cairn is git-based; there is nothing to adopt",
    ),
    Mutation(
        guard="test_env_check",
        test="TestEnvCheck.test_python3_gap_names_hooks_fallback_and_scripts",
        target="skills/cairn-init/SKILL.md",
        block="unverified on Windows",
    ),
    Mutation(
        guard="test_env_check",
        test="TestEnvCheck.test_python3_gap_names_hooks_fallback_and_scripts",
        target="skills/cairn-init/SKILL.md",
        block="the registered hooks fall back to the `py` launcher",
    ),
    Mutation(
        guard="test_env_check",
        test="TestEnvCheck.test_gh_gap_names_the_honor_system_degradation",
        target="skills/cairn-init/SKILL.md",
        block="the approval model becomes honor-system",
    ),
    Mutation(
        guard="test_env_check",
        test="TestEnvCheck.test_no_remote_names_local_only_mode",
        target="skills/cairn-init/SKILL.md",
        block="local-only mode",
    ),
    # M64 (D-036): the durable-record preview rule + its four per-skill
    # directives — one entry per distinct block (M53 discipline).
    Mutation(
        guard="test_durable_record_preview",
        test="TestPerSkillDirectives.test_plan_commit_step",
        target="skills/milestone-plan/SKILL.md",
        block="Durable-record preview first (tracking-rules):",
    ),
    Mutation(
        guard="test_durable_record_preview",
        test="TestPerSkillDirectives.test_review_hygiene_step",
        target="skills/milestone-review/SKILL.md",
        block="Durable-record preview (tracking-rules): show the archive summary,",
    ),
    Mutation(
        guard="test_durable_record_preview",
        test="TestPerSkillDirectives.test_implement_decisions_and_amendments",
        target="skills/milestone-implement/SKILL.md",
        block="Durable-record preview (tracking-rules): a milestone-local Decisions",
    ),
    Mutation(
        guard="test_durable_record_preview",
        test="TestPerSkillDirectives.test_implement_decisions_and_amendments",
        target="skills/milestone-implement/SKILL.md",
        block="verbatim in a guaranteed-rendered position (durable-record preview).",
    ),
    Mutation(
        guard="test_durable_record_preview",
        test="TestPerSkillDirectives.test_brief_rr_ingestion",
        target="skills/milestone-brief/SKILL.md",
        block="durable-record preview (tracking-rules): show the",
    ),
    # M65 (D-037): the acceptance-chips rule, its cross-reference, the
    # previously-unguarded base chip rule, and the five per-skill
    # directives — one entry per distinct block (M53 discipline).
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestPerSkillDirectives.test_plan_question_gate",
        target="skills/milestone-plan/SKILL.md",
        block="Acceptance chips (tracking-rules): a question resting on a produced",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestPerSkillDirectives.test_implement_gate_and_mini_gate",
        target="skills/milestone-implement/SKILL.md",
        block="conclusion shows its substance compactly in the chip and verbatim in the chat above, best-effort (Mandated-substance rule).",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestPerSkillDirectives.test_implement_gate_and_mini_gate",
        target="skills/milestone-implement/SKILL.md",
        block="mini gate's chip (acceptance chips, tracking-rules)",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestPerSkillDirectives.test_review_approval_gate",
        target="skills/milestone-review/SKILL.md",
        block="Acceptance chips (tracking-rules): each actioned finding's text appears",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestPerSkillDirectives.test_brief_rb_gate_and_rr_routing",
        target="skills/milestone-brief/SKILL.md",
        block="Acceptance chips (tracking-rules): show the drafted RB's",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestPerSkillDirectives.test_brief_rb_gate_and_rr_routing",
        target="skills/milestone-brief/SKILL.md",
        block="The RR's conclusions/verdict section is shown verbatim in the close block's turn (its final rendered text, Mandated-substance rule).",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestPerSkillDirectives.test_milestone_route_triage",
        target="skills/milestone/SKILL.md",
        block="Acceptance chips (tracking-rules): a triage option that accepts an audit",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestMigrationGateDirectives.test_step3_disposition_gate",
        target="skills/shared/migration-protocol.md",
        block="Acceptance chips (tracking-rules): the inventory and each item's",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestMigrationGateDirectives.test_step3_disposition_gate",
        target="skills/shared/migration-protocol.md",
        block="never only inside chip options, and a paraphrase never stands in for",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestMigrationGateDirectives.test_step7_merge_ledger",
        target="skills/shared/migration-protocol.md",
        block="Acceptance chips (tracking-rules): the ledger's substance appears",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestMigrationGateDirectives.test_step7_merge_ledger",
        target="skills/shared/migration-protocol.md",
        block="verbatim in the chat above the merge-approval chip, best-effort, with",
    ),
    # M156: the phase-close rule's four operative clauses each carry the
    # doctrine independently — the close-block mandate, the fenced-command
    # handoff, the safety line, and the decision-gate carve-out.
    Mutation(
        guard="test_gate_wording",
        test="TestPhaseCloseBlock.test_rule_states_close_block_never_a_chip",
        target=RULES,
        block="ends with a **close block**, never a chip",
    ),
    Mutation(
        guard="test_gate_wording",
        test="TestPhaseCloseBlock.test_rule_hands_the_user_the_fenced_command",
        target=RULES,
        block="the next skill — the user runs the fenced command",
    ),
    Mutation(
        guard="test_gate_wording",
        test="TestPhaseCloseBlock.test_rule_carries_the_safety_line",
        target=RULES,
        block="adjusting course or `/clear` are both safe at this point",
    ),
    Mutation(
        guard="test_gate_wording",
        test="TestPhaseCloseBlock.test_rule_spares_decision_gates",
        target=RULES,
        block="unaffected: a gate is a choice, a phase end is a",
    ),
    # M155: the Mandated-substance rule's four operative clauses each carry
    # the doctrine independently (per-block discipline, M53) — the rendering
    # hazard, the two guaranteed positions, the overflow prong, and the
    # restatement prong for previews/handoffs.
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestMandatedSubstanceRule.test_names_the_rendering_hazard",
        target=RULES,
        block="Text emitted before a tool call in the same turn is not reliably displayed",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestMandatedSubstanceRule.test_names_the_two_guaranteed_positions",
        target=RULES,
        block="a chip's own question text and option descriptions, and a turn's final rendered text",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestMandatedSubstanceRule.test_decision_chip_is_same_turn_and_self_sufficient",
        target=RULES,
        block="A decision chip is posed in the same turn as its",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestMandatedSubstanceRule.test_previews_and_handoffs_restate_after_the_tool_resolves",
        target=RULES,
        block="first rendered text after the tool call resolves",
    ),
    # M72 (D-043): the boundary passage and the PR binding each carry a
    # distinct rule, and the README half is a separate target — one entry
    # per positive assert's block, per the M53 per-block discipline.
    Mutation(
        guard="test_collaboration_boundary",
        test="TestReadmeCollaboratorSurface.test_readme_has_the_collaborators_section",
        target="README.md",
        block="## Working with collaborators",
    ),
    # M73 (D-043): the PR door. Entries cover every block whose deletion
    # would silently reopen the gap M73 closes — checkout-not-branch, the
    # naming exemption, the adopted test sequence and its worktree cleanup,
    # the fork fallback (including the user gate on closing someone else's
    # PR, and the never-merge-untested line), and the two routing surfaces
    # (description frontmatter + the Intake paragraph). The remaining asserts
    # in that guard file are corollaries of these blocks; all of its asserted
    # phrases were separately confirmed to occur exactly once in their target.
    Mutation(
        guard="test_external_pr_intake",
        test="TestAdoptionPath.test_branch_step_checks_the_pr_out",
        target=HOTFIX,
        block="*Adopting a PR:* run `gh pr checkout <N>`",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestAdoptionPath.test_branch_step_states_the_naming_exemption",
        target=HOTFIX,
        block="name is **exempt** from the `hotfix-<slug>` contract",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestAdoptedRegressionTest.test_step_names_the_adopted_sequence",
        target=HOTFIX,
        block="on the PR head**. Prove both directions",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestForkFallback.test_step_names_the_no_push_fallback",
        target=HOTFIX,
        block="**When the head branch cannot be pushed to:**",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestForkFallback.test_fallback_asks_the_contributor_first",
        target=HOTFIX,
        block="PR to add the missing pieces — it is their work",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestForkFallback.test_closing_a_contributors_pr_is_user_gated",
        target=HOTFIX,
        block="and irreversible from the contributor's side, so it is **never** done",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestForkFallback.test_second_pr_prohibition_admits_the_fallback",
        target=HOTFIX,
        block="never open a second one, except",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestForkFallback.test_fallback_never_trades_away_the_regression_test",
        target=HOTFIX,
        block="Never merge a fix whose regression test",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestAdoptedRegressionTest.test_worktree_recipe_is_located_and_cleaned_up",
        target=HOTFIX,
        block="throwaway worktree of the default branch created **outside the repo**",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestForkFallback.test_delete_branch_caveat_for_forks",
        target=HOTFIX,
        block="drop `--delete-branch` on a",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestIntakeRouting.test_description_frontmatter_fires_on_an_incoming_pr",
        target=HOTFIX,
        block="or adopt an incoming external PR that fixes one",
    ),
    Mutation(
        guard="test_external_pr_intake",
        test="TestIntakeRouting.test_intake_paragraph_names_hotfix_as_the_door",
        target=RULES,
        block="**`/hotfix` is the door**",
    ),
    # M74 (D-043, third deliverable): the audit's inbox sweep. Four distinct
    # rules, four entries — the commands, the search-first ordering, the
    # degradation floor, and the PR routing each carry the step independently,
    # so a single exemplar would leave three of them unproven.
    Mutation(
        guard="test_issue_triage",
        test="TestInboxEnumeration.test_step_names_the_issue_command",
        target=MILESTONE,
        block="`gh issue list --state open --json number,title,url` for issues,",
    ),
    Mutation(
        guard="test_issue_triage",
        test="TestInboxEnumeration.test_step_applies_search_first_before_proposing",
        target=MILESTONE,
        block="apply the search-first rule to every hit before proposing",
    ),
    Mutation(
        guard="test_issue_triage",
        test="TestDegradation.test_degradation_is_never_an_audit_failure",
        target=MILESTONE,
        block="An unreachable inbox is a reported gap, never an audit `FAIL`.",
    ),
    Mutation(
        guard="test_issue_triage",
        test="TestDispositions.test_pr_routing_reuses_m73s_door",
        target=MILESTONE,
        block="This is the door M73 opened; route to it rather than inventing",
    ),
    # M74 review F1: the own-PR filter is what makes the PR list an inbox
    # rather than a list of cairn's own in-flight work.
    Mutation(
        guard="test_issue_triage",
        test="TestInboxEnumeration.test_own_prs_are_filtered_out_before_the_sweep",
        target=MILESTONE,
        block="drop this session's own work from the PR list",
    ),
    # M74 review F3: the disposition LABEL carries the routing rule. Blanking
    # the label must fail the guard — asserting the clause alone let the label
    # be swapped with every test still green.
    Mutation(
        guard="test_issue_triage",
        test="TestDispositions.test_candidate_row_is_the_default",
        target=MILESTONE,
        block="**candidate row** — the default for anything real but not urgent",
    ),
    # M75 (D-044): the rulebook's fourth disposition. Two entries, because the
    # label→rule mapping and the exclusion carry the rule independently — the
    # narrowing is what keeps `leave` compatible with IP3, and blanking either
    # half alone must fail. Anchors are unique in the rulebook (M58).
    Mutation(
        guard="test_external_pr_intake",
        test="TestIntakeRouting.test_intake_paragraph_names_leave_with_its_narrowing",
        target=RULES,
        block="`leave` is legal only for noise, duplicates, or items already cross-referenced in cairn",
    ),
    # M82: /cairn-init §3 performs the rename its own `scaffold deprecations`
    # advisory names. One entry per independently-load-bearing block: the
    # advisory-driven generality (blanking it re-narrows the step to the one
    # rename D-047 made), and each of the three consent rules, whose label and
    # rule are fused into one bold token so a swap cannot survive (M74/M76).
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_step_is_driven_by_advisory_output_not_a_named_rename",
        target="skills/cairn-init/SKILL.md",
        block="Act on every line the advisory prints, never on a pair named in this text",
    ),
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_successor_entry_is_added_without_an_ask",
        target="skills/cairn-init/SKILL.md",
        block="**Add the successor entry, no ask.**",
    ),
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_directory_move_is_gated_on_an_explicit_ask",
        target="skills/cairn-init/SKILL.md",
        block="**Only the old directory present: move it only after an explicit ask.**",
    ),
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_both_directories_present_is_never_clobbered",
        target="skills/cairn-init/SKILL.md",
        block="**Both directories present: surface, never clobber.**",
    ),
    # M82 review send-back. F1: the shelf must stay covered at every moment, so
    # the removal rule is load-bearing on its own. F3: the cases are only safe
    # as exclusive states — as a sequence the move preceded the clobber check.
    # F2: the closing paragraph must keep saying what the check cannot prove.
    # F6: AC1's §0 pointer was independently load-bearing and unregistered.
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_superseded_entry_survives_until_its_directory_is_gone",
        target="skills/cairn-init/SKILL.md",
        block="**Remove `<old>` from `.gitignore` only once the old directory is gone from disk.**",
    ),
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_cases_are_mutually_exclusive_and_chosen_before_any_move",
        target="skills/cairn-init/SKILL.md",
        block="Then take **exactly one** of the cases below, chosen by what is on disk",
    ),
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_closing_check_covers_both_arms",
        target="skills/cairn-init/SKILL.md",
        block="**A quiet advisory now confirms the entries and the directory both** — the directory arm reads the filesystem, so a superseded shelf still holding files keeps its line firing whatever `.gitignore` says.",
    ),
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_per_line_block_names_both_line_kinds",
        target="skills/cairn-init/SKILL.md",
        block="a directory line — `directory '<old>' still holds files`",
    ),
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_directory_line_is_trigger_not_choice",
        target="skills/cairn-init/SKILL.md",
        block="On a directory line: it is only the trigger for the directory-state cases below — the case is still chosen by what is on disk.",
    ),
    Mutation(
        guard="test_scaffold_migration",
        test="TestDeprecationMigration.test_repair_commit_cannot_sweep_an_unmigrated_shelf",
        target="skills/cairn-init/SKILL.md",
        block="**stage the files repair touched by path, never `git add -A` or `.`**",
    ),
    Mutation(
        guard="test_scaffold_migration",
        test="TestRepairSection.test_repair_has_its_own_section",
        target="skills/cairn-init/SKILL.md",
        block="- Already on cairn → **repair mode** (§3).",
    ),
    # M85: the extraction-status shape rule, in BOTH templates. Registered per
    # (test, template) pair rather than once per test: each guard asserts the
    # rule in both files, so an entry against only one leaves the other's copy
    # deletable with the guard still green — the false-coverage shape M39/M40
    # exist to catch, one file over.
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_states_the_three_way_shape",
        target=SOURCE_NOTE,
        block="claim a verification, or carry a date, or say there is nothing to re-verify.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_states_the_three_way_shape",
        target=SYNTHESIS_NOTE,
        block="claim a verification, or carry a date, or say there is nothing to re-verify.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_names_the_verb_set_with_its_label",
        target=SOURCE_NOTE,
        block="A verification claim is one of these verbs — `verified`, `checked against`, `read against`, `read directly`.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_names_the_verb_set_with_its_label",
        target=SYNTHESIS_NOTE,
        block="A verification claim is one of these verbs — `verified`, `checked against`, `read against`, `read directly`.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_marks_unverified_as_self_negating",
        target=SOURCE_NOTE,
        block="`unverified` is the exception — it carries its own negation and always reads as never-verified, with or without a negator.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_marks_unverified_as_self_negating",
        target=SYNTHESIS_NOTE,
        block="`unverified` is the exception — it carries its own negation and always reads as never-verified, with or without a negator.",
    ),
    # M89: the partial state, same per-(test, template) pairing as above.
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_names_the_partiality_set_with_its_label",
        target=SOURCE_NOTE,
        block="A partiality qualifier before the verb in that same clause — `partly`, `partially`, `in part`, `spot-checked` — makes the claim a PARTIAL verification.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_names_the_partiality_set_with_its_label",
        target=SYNTHESIS_NOTE,
        block="A partiality qualifier before the verb in that same clause — `partly`, `partially`, `in part`, `spot-checked` — makes the claim a PARTIAL verification.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_says_a_partial_claim_is_never_cleared",
        target=SOURCE_NOTE,
        block="A partial claim is reported, never cleared: no date closes it, because what is missing is coverage rather than freshness.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_says_a_partial_claim_is_never_cleared",
        target=SYNTHESIS_NOTE,
        block="A partial claim is reported, never cleared: no date closes it, because what is missing is coverage rather than freshness.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_taught_partiality_qualifier_classifies_as_partial",
        target=SOURCE_NOTE,
        block="A partiality qualifier before the verb in that same clause — `partly`, `partially`, `in part`, `spot-checked` — makes the claim a PARTIAL verification.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_says_the_alternatives_are_not_the_accepted_list",
        target=SOURCE_NOTE,
        block="The alternatives below are examples of that shape, not the accepted list.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_says_the_alternatives_are_not_the_accepted_list",
        target=SYNTHESIS_NOTE,
        block="The alternatives below are examples of that shape, not the accepted list.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_says_an_unreadable_status_is_reported",
        target=SOURCE_NOTE,
        block="it is reported rather than assumed verified.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestTemplatesTeachTheShapeRule.test_each_template_says_an_unreadable_status_is_reported",
        target=SYNTHESIS_NOTE,
        block="it is reported rather than assumed verified.",
    ),
    # M90 README currency — one entry per positive assert (M53). The
    # profile-enumeration guard is NOT registered here: its block is a
    # derived list, not a fixed phrase, and blanking any single label leaves
    # the other three passing. Its falsifiability was proven differentially
    # instead (run red against the pre-fix README) and by the fail-closed
    # unmapped-profile check.
    Mutation(
        guard="test_readme_currency",
        test="TestReferencePagesSection.test_readme_has_the_sources_section",
        target="README.md",
        block="## Keeping track of sources",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestReferencePagesSection.test_readme_states_when_a_page_is_owed",
        target="README.md",
        block="A page is owed when you start relying on the source.",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestReferencePagesSection.test_readme_states_pages_record_whether_they_were_rechecked",
        target="README.md",
        block="whether its extracted values have actually been re-read",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestReferencePagesSection.test_readme_distinguishes_source_facts_from_repo_notes",
        target="README.md",
        block="Facts about the source outlive notes about your repo.",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestReferencePagesSection.test_readme_states_staleness_warnings_are_not_failures",
        target="README.md",
        block="These are warnings, never gate failures:",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestFileMapCurrency.test_readme_tree_lists_the_lessons_file",
        target="README.md",
        block="LESSONS.md             # durable repo lessons",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestFileMapCurrency.test_readme_boundary_rule_names_every_home",
        target="README.md",
        block="Decisions → DECISIONS · Lessons → LESSONS · History →",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestReleaseRowIsProfileNeutral.test_release_row_is_not_cran_only",
        target="README.md",
        block="follows your repo's profile",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestReleaseTimingPromise.test_readme_states_cairn_never_proposes_a_release",
        target="README.md",
        block="Propose, plan, or nominate a release",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestReleaseTimingPromise.test_readme_names_release_timing_as_the_maintainers_call",
        target="README.md",
        block="release timing is yours to declare",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestAdvisoryNudges.test_readme_install_section_names_the_advisory_nudges",
        target="README.md",
        block="and the advisory nudges",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestAdvisoryNudges.test_readme_says_nudges_never_block",
        target="README.md",
        block="none of which block anything",
    ),
    # Each nudge trigger registered separately: blanking any ONE must redden,
    # which a single anchor on the shared preamble would not prove.
    Mutation(
        guard="test_readme_currency",
        test="TestAdvisoryNudges.test_readme_names_each_nudge_trigger",
        target="README.md",
        block="when an idea gets captured somewhere other than the",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestAdvisoryNudges.test_readme_names_each_nudge_trigger",
        target="README.md",
        block="something durable is headed for Claude's memory",
    ),
    Mutation(
        guard="test_readme_currency",
        test="TestAdvisoryNudges.test_readme_names_each_nudge_trigger",
        target="README.md",
        block="when a commit on your default branch reaches outside",
    ),
    # M93/D-052 — the hygiene stamp. One exemplar per target file: the rule
    # in the rulebook, and the two SKILL.md steps that actually write the
    # stamp (a rule stated only in the rulebook is what let the chain regrow).
    # 2026-08-15: replacing the stamp was pinned; VERIFYING it was not, and
    # both overruns that day were correct replacements that went over cap.
    # One entry per site — the clause is carried verbatim by both, so a single
    # registration would leave the other site's copy deletable green.
    Mutation(
        guard="test_hygiene_stamp",
        test="TestStampWriteSites.test_shipped_skeleton_teaches_the_shape",
        target="skills/cairn-init/SKILL.md",
        block="(one short line, replaced each pass — never appended to)",
    ),
    # M98 (D-055): maturation is the third outflow, and the graduated family
    # moved to a new module. Entries span all three surfaces the guard pins —
    # the module itself, the rulebook pointer, and the retirement rule — one
    # per positive assert (M53 discipline).
    # M99. Four blocks across four targets, because the budget wiring fails in
    # four independent ways: the budgets could stop reading as guidance and
    # become a second cap (the shape D-030 declined); the archive template could
    # stop being named as the summary's source; and either drafting step could
    # lose its handed-over command while the other kept one.
    # M118/D-074: the reserve became an exemption; the spend-none instruction
    # survived it. Registered now that the assert has been re-anchored.
    Mutation(
        guard="test_budget_first_drafting",
        test="TestArchiveSummaryTemplate.test_it_exists_and_carries_the_canonical_section_set_in_order",
        target="skills/shared/templates/archive-summary.md",
        block="**Decisions:**",
    ),
    Mutation(
        guard="test_budget_first_drafting",
        test="TestDraftingStepsHandOverTheCounter.test_review_names_the_archive_template_as_the_source",
        target=REVIEW,
        block="skills/shared/templates/archive-summary.md",
    ),
    # M108 (D-060): the always-read governance frame. Each of the three
    # element labels, the completeness-only boundary, each worked table row,
    # and the two audit-bullet asserts carries the frame independently, so
    # each gets its own mutation proof. M113 (D-063) adds the fifth row and
    # the two claims that distinguish it.
    # M112 (D-062): softening the Fable warning retains two invariants — the
    # per-instance approval gate and the RB/RR-only path — one Mutation entry
    # per block each assert depends on (M53 per-block discipline).
    Mutation(
        guard="test_fable_gate_retained",
        test="TestPerInstanceApprovalGate.test_brief_requires_explicit_per_instance_approval",
        target=BRIEF,
        block="explicit user approval, every time",
    ),
    Mutation(
        guard="test_fable_gate_retained",
        test="TestPerInstanceApprovalGate.test_brief_requires_explicit_per_instance_approval",
        target=BRIEF,
        block="only ever through this",
    ),
    # M115: the criteria audit. One entry per clause that carries the rule
    # independently — the audit's placement, its reader, each of its two
    # questions, each disposition arm, and the anti-mechanization line all
    # fail on their own, and a set-level entry cannot prove a per-clause one.
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_step_2_drafts_criteria_to_final_wording",
        target="skills/milestone-plan/SKILL.md",
        block="acceptance criteria are drafted here to their final wording, not at\n   step 4",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_audit_names_a_fresh_context_reader_that_authored_none_of_them",
        target="skills/milestone-plan/SKILL.md",
        block="fresh-context **[O]**\n   reader that authored none of them",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_audit_states_the_satisfiability_question",
        target="skills/milestone-plan/SKILL.md",
        block="*what state of the world satisfies this exactly as written*",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_audit_states_the_ip_and_decision_conflict_question",
        target="skills/milestone-plan/SKILL.md",
        block="*does any IP or D-entry make that state unreachable*",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_audit_reads_the_shipped_wording_never_a_paraphrase",
        target="skills/milestone-plan/SKILL.md",
        block="It reads the wording\n   step 4 will write, never a paraphrase of it",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_clear_findings_are_fixed_and_the_fix_reported",
        target="skills/milestone-plan/SKILL.md",
        block="a finding with one clear right answer is fixed\n   and the fix reported in chat",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_judgment_findings_become_gate_questions_under_the_cap",
        target="skills/milestone-plan/SKILL.md",
        block="becomes one of this round's questions, within the three-marker\n   cap",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_audit_is_a_reader_and_never_a_check",
        target="skills/milestone-plan/SKILL.md",
        block="The instrument is a reader and never a check",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestRRIngestionCriteriaAudit.test_binding_criteria_are_audited_before_ingestion",
        target="skills/milestone-brief/SKILL.md",
        block="**A binding-criteria set is audited before it is ingested**",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestRRIngestionCriteriaAudit.test_ingest_audit_reuses_the_plan_gate_reader",
        target="skills/milestone-brief/SKILL.md",
        block="by the same\n   fresh-context **[O]** reader `/milestone-plan` step 3 spawns",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestRRIngestionCriteriaAudit.test_ingest_audit_asks_the_questions_of_the_set_not_only_each",
        target="skills/milestone-brief/SKILL.md",
        block="asked\n   of the set as well as of each criterion",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestRRIngestionCriteriaAudit.test_ingest_findings_are_raised_never_softened_away",
        target="skills/milestone-brief/SKILL.md",
        block="What the audit returns is raised with the\n   user, never softened away",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestRRIngestionCriteriaAudit.test_ingest_audit_states_the_questions_at_this_surface",
        target=BRIEF,
        block="and the same\n   three questions — *what state of the world satisfies this exactly as\n   written*, *does any IP or D-entry make that state unreachable*, and\n   *does it make a universal claim over a domain no procedure it names enumerates*",
    ),
    # M130: the bounded-promise rule and its audit question. Four blocks —
    # the third question at the plan gate, the rule sentence, its
    # unenumerable-domain fallback, and the hand-list exclusion.
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_audit_asks_the_bounded_promise_question",
        target="skills/milestone-plan/SKILL.md",
        block="*does it make a universal claim over a domain no procedure it names enumerates*\n   (the bounded-promise rule, step 4; M130)",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_drafting_rule_bounds_universal_promises",
        target="skills/milestone-plan/SKILL.md",
        block="**Bounded promises only (M130).** An acceptance criterion that makes a\n     universal claim (\"no X\", \"every Y\", \"nothing Z\") names the procedure —\n     a search, a sweep, or a test run — that enumerates its domain",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_unenumerable_universals_claim_the_swept_domain_instead",
        target="skills/milestone-plan/SKILL.md",
        block="where no\n     stated procedure can enumerate the domain, the criterion instead\n     claims what a procedure it names actually swept",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_a_hand_list_of_sites_is_not_a_procedure",
        target="skills/milestone-plan/SKILL.md",
        block="A hand-list of sites is\n     not a procedure",
    ),
    # M132: the domain-match test. Seven blocks over the five rule sentences
    # the branch adds to step 4 plus the audit clause at each of its two
    # surfaces; the long property sentence takes two blocks, so no part of it
    # deletes green (the M114 partial-pin class, which review found this
    # comment's own first draft had committed on the example sentence).
    # Sentences enumerated by `git diff --name-only main..HEAD` filtered to
    # skills/**/*.md rather than by recall, since a hand-listed file set is
    # the very defect this rule closes. The example sentence is registered
    # too: classifying it "illustrative" would be the author judgment the
    # audit warned reproduces M102's own move.
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_the_procedure_must_cover_the_promises_own_domain",
        target="skills/milestone-plan/SKILL.md",
        block="**The procedure must enumerate the domain the criterion's own universal\n     quantifies over, not a proxy for it.**",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_naming_a_procedure_does_not_pass_the_domain_match_test",
        target="skills/milestone-plan/SKILL.md",
        block="Naming a procedure is not passing\n     this test: an enumeration whose membership is fixed by what the author\n     recalled, rather than decided by a procedure over the domain, is a proxy",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_the_instance_enumeration_examples_are_non_exhaustive",
        target="skills/milestone-plan/SKILL.md",
        block="however long its list — spellings, renderings, known cases and whole\n     families among others, never only those",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_the_remedy_is_to_narrow_the_promise_not_widen_the_enumeration",
        target="skills/milestone-plan/SKILL.md",
        block="A counterexample defeating such\n     an enumeration is therefore not answered by a wider one; the repair is to\n     narrow the promise until a stated procedure settles it",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_the_rule_carries_its_measured_failure",
        target="skills/milestone-plan/SKILL.md",
        block="intraclass M102's\n     \"no command reads git history\", built as a set of refused command forms,\n     took three returns beaten by a ref spelling, an argument-order bug, and\n     then `awk`, which is no git command at all.",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_audit_question_is_asked_of_the_domain_not_a_proxy",
        target="skills/milestone-plan/SKILL.md",
        block="The third question is asked of the\n   domain the claim quantifies over, never of a proxy the named procedure\n   happens to enumerate (M132)",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestRRIngestionCriteriaAudit.test_the_domain_match_sentence_is_identical_at_both_surfaces",
        target=BRIEF,
        block="The third question is asked of the\n   domain the claim quantifies over, never of a proxy the named procedure\n   happens to enumerate (M132).",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestRRIngestionCriteriaAudit.test_ingest_audit_carries_the_domain_match_test",
        target=BRIEF,
        block="The third question is asked of the\n   domain the claim quantifies over, never of a proxy the named procedure\n   happens to enumerate (M132).",
    ),
    # M138: the form-coverage question and the step-6 re-audit. One entry per
    # sentence the branch adds — the byte-identical question at each of its
    # two surfaces, then the six step-6 clauses (Minor narrowing,
    # Substantive-by-definition, the three-questions pointer, the reader, the
    # ingest exemption, the per-criterion bound), each carrying the rule
    # independently. Sentences enumerated by normalized-text absence from the
    # merge base (the milestone's AC4 procedure), not by recall.
    Mutation(
        guard="test_fresh_context_readers",
        test="TestAmendmentReaudit.test_criterion_wording_change_is_substantive_by_definition",
        target=IMPLEMENT,
        block="a change to\n     acceptance-criterion wording is *Substantive* by definition",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestAmendmentReaudit.test_minor_arm_excludes_the_amendment_gated_sections",
        target=IMPLEMENT,
        block="refine wording outside the amendment-gated\n     sections — Goal, Scope, Acceptance criteria —",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestAmendmentReaudit.test_reaudit_reader_is_fresh_context_and_not_the_author",
        target=IMPLEMENT,
        block="by a fresh-context\n     **[O]** reader that did not author the amended wording, before the\n     amended text is written to the milestone file",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestAmendmentReaudit.test_ingest_cleared_wording_is_exempt",
        target=IMPLEMENT,
        block="Wording whose clearance the `/milestone-brief` ingest audit's work-log\n     line already covers is exempt",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestAmendmentReaudit.test_reentry_is_once_per_criterion_with_its_own_fresh_reader",
        target=IMPLEMENT,
        block="Per criterion, wording fixed at the mini gate re-enters the questions\n     once with its own fresh reader, and further churn on that criterion\n     goes to the user",
    ),
    # M121 (narrows D-067, first instrument). Three entries across two files:
    # the record requirement, the sentence making a missing line evidence, and
    # the ingest surface's cross-reference to the one home that states it.
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_absent_audit_line_means_it_did_not_run",
        target="skills/milestone-plan/SKILL.md",
        block="an absent line means the reader did not run,\n   never that it ran and was silent",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_audit_records_how_many_milestones_left_no_line",
        target="skills/milestone-plan/SKILL.md",
        block="Three of the five milestones after\n   this instrument was adopted carry no such line",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestRRIngestionCriteriaAudit.test_ingest_audit_records_its_own_line_on_the_plan_gate_terms",
        target=BRIEF,
        block="The ingest audit\n   records one work-log line either way, on `/milestone-plan` step 3's terms",
    ),
    # M125: §6's recorded-counts rule, re-cut by M137 as a deference to the
    # tracking-rules derived-figures rule — headline, grade clause, the
    # story's citation, and the measured case it is required to name (AC3),
    # each pinned separately.
    # M129 (RR11 BC5): §6's quantified-claim rule — the two load-bearing
    # conjuncts pinned separately.
    # M130: §6's delete-first remedy — the ordering and the D-045 carve-out,
    # pinned separately for the same either-half-deletes-green reason.
    # M142: the four stakes-tier rules in /milestone-plan — the surface-tier
    # rule, the internal-tier criteria standard, the audit's proportionality
    # question, and the collision check's checker-regress clause. One entry
    # per protected block; blocks are contained phrases, never slice bounds
    # (M117: blanking a bound crashes the slice helper, a weak red).
    Mutation(
        guard="test_stakes_tier",
        test="TestSurfaceTierRule.test_rule_classifies_every_deliverable_into_the_two_tiers",
        target="skills/milestone-plan/SKILL.md",
        block="deliverable as user-facing or internal",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestSurfaceTierRule.test_internal_is_defined_by_absence_of_an_external_consumer",
        target="skills/milestone-plan/SKILL.md",
        block="no external consumer of the repo relies on the",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestSurfaceTierRule.test_internal_definition_carries_its_example_enumeration",
        target="skills/milestone-plan/SKILL.md",
        block="dev tooling, data-generation scripts, in-repo checkers",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestSurfaceTierRule.test_unclear_or_spanning_deliverables_default_to_user_facing",
        target="skills/milestone-plan/SKILL.md",
        block="whose tier is unclear or spans both",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestSurfaceTierRule.test_tier_is_recorded_in_the_milestone_file",
        target="skills/milestone-plan/SKILL.md",
        block="one-clause reason in the milestone file's Goal or Scope prose",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestInternalTierStandard.test_promise_is_bounded_to_a_directly_enumerated_domain",
        target="skills/milestone-plan/SKILL.md",
        block="quantifies over a domain its named procedure",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestInternalTierStandard.test_standard_names_the_three_prohibited_forms",
        target="skills/milestone-plan/SKILL.md",
        block="never an exemption registry, a per-rendering",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestInternalTierStandard.test_repair_narrows_or_descopes_and_never_widens",
        target="skills/milestone-plan/SKILL.md",
        block="never by widening the specification",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestInternalTierStandard.test_standard_stops_at_the_promise_guard_boundary",
        target="skills/milestone-plan/SKILL.md",
        block="a criterion's promise, never a guard's construction",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestCheckerRegressClause.test_clause_names_the_shape",
        target="skills/milestone-plan/SKILL.md",
        block="extending or hardening a checker that the ROADMAP or archive records",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestCheckerRegressClause.test_deletion_is_the_recommended_option",
        target="skills/milestone-plan/SKILL.md",
        block="simplifying or deleting the checker as the recommended option",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestCheckerRegressClause.test_hardening_stays_present_but_non_recommended",
        target="skills/milestone-plan/SKILL.md",
        block="hardening it as a present, non-recommended alternative",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestCheckerRegressClause.test_promise_unchanged_repairs_stay_outside_the_shape",
        target="skills/milestone-plan/SKILL.md",
        block="leaves the checker's promise unchanged stays outside the shape",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestCheckerRegressClause.test_promise_widening_is_the_shape_however_framed",
        target="skills/milestone-plan/SKILL.md",
        block="the regress shape however it is framed",
    ),
    # M142 defect return #1: five blocks the first cut left unpinned — the
    # two obligations, the two subjects, and the repair sentence's tail.
    Mutation(
        guard="test_stakes_tier",
        test="TestSurfaceTierRule.test_classification_and_recording_are_obligations",
        target="skills/milestone-plan/SKILL.md",
        block="Every plan classifies the milestone's",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestInternalTierStandard.test_descoping_is_a_legal_repair_alternative",
        target="skills/milestone-plan/SKILL.md",
        block="or by\n   descoping, never by",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestCheckerRegressClause.test_clause_names_the_shape",
        target="skills/milestone-plan/SKILL.md",
        block="an earlier milestone of the same repo shipping",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestCheckerRegressClause.test_deletion_is_the_recommended_option",
        target="skills/milestone-plan/SKILL.md",
        block="On such a hit the gate poses",
    ),
    # M142 defect return #2: whole-slice equality fixtures (D-103's
    # instrument) — one entry per fixture, each anchored on a phrase the
    # pass-2 review proved unpinned by any per-property assert (R1-R3),
    # so the registration proves the fixture catches what the pins miss.
    Mutation(
        guard="test_stakes_tier",
        test="TestWholeSliceFixtures.test_surface_rule_matches_its_fixture",
        target="skills/milestone-plan/SKILL.md",
        block="Internal means no external consumer",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestWholeSliceFixtures.test_standard_rule_matches_its_fixture",
        target="skills/milestone-plan/SKILL.md",
        block="A draft needing those is repaired at this",
    ),
    Mutation(
        guard="test_stakes_tier",
        test="TestWholeSliceFixtures.test_regress_rule_matches_its_fixture",
        target="skills/milestone-plan/SKILL.md",
        block="The sweep also names this shape",
    ),
    # M152: the two plain-style rules. One entry per positive assert's block
    # (M53 per-block discipline) — each clause carries its rule independently.
    Mutation(
        guard="test_plain_style",
        test="TestPlainStyleRule.test_length_matched_to_the_turn",
        target=RULES,
        block="Write for the reader: response length matched to what the turn needs",
    ),
    Mutation(
        guard="test_plain_style",
        test="TestPlainStyleRule.test_plain_words_over_jargon",
        target=RULES,
        block="plain words over jargon — a term of art appears only",
    ),
    Mutation(
        guard="test_plain_style",
        test="TestPlainStyleRule.test_no_filler_or_hype",
        target=RULES,
        block="with no stock filler phrasing, hype adjectives, or",
    ),
    Mutation(
        guard="test_plain_style",
        test="TestPlainStyleRule.test_terms_glossed_or_dropped",
        target=RULES,
        block="glossed at first use or dropped",
    ),
    Mutation(
        guard="test_plain_style",
        test="TestPlainStyleRule.test_padding_clause_and_carveout",
        target=RULES,
        block="padding. The decision surface keeps its stricter",
    ),
    Mutation(
        guard="test_plain_style",
        test="TestRecordProseRule.test_rule_present_under_its_name",
        target=RULES,
        block="**Records are written plain** (the record-prose rule)",
    ),
    Mutation(
        guard="test_plain_style",
        test="TestRecordProseRule.test_no_characterizations",
        target=RULES,
        block="omits characterizations the facts don't need (adjectives, superlatives, hype)",
    ),
    Mutation(
        guard="test_plain_style",
        test="TestRecordProseRule.test_length_standard_cross_referenced",
        target=RULES,
        block="the Plain style rule's length standard, applied to what is written down",
    ),
    # Hotfix 2026-09-01: the r-package release-walk keeps cran-comments.md in
    # its conventional short form and never restates NEWS.
    Mutation(
        guard="test_cran_comments_short_form",
        test="TestCranCommentsShortForm.test_walk_forbids_restating_news",
        target="skills/shared/profiles/r-package.md",
        block="Do not restate NEWS",
    ),
]

# Prose-guard files deliberately NOT in the registry, each with a reason. The
# completeness check (below) treats these as covered.
EXEMPT = {
    "test_mutation_harness": "the harness's own tests, not a prose-guard",
    # M146, 2026-08-16: these six files' registrations died with the rulebook reduction —
    # every pinned block was deliberately reworded or retired. Their surviving
    # asserts pin current text; re-registration is deferred until adopter
    # evidence shows which of the reduced rules still need mutation proof
    # (the suite gates nothing since D-109, so an unregistered guard costs
    # only coverage the hand-run maintainer already accepts).
    "test_gate_wording": "M146 (2026-08-16): registrations died with the rewrite; see above",
    "test_idea_intake_gate": "M146 (2026-08-16): registrations died with the rewrite; see above",
    "test_lesson_graduation": "M146 (2026-08-16): guards LESSONS/DECISIONS graduation state; see above",
    "test_phase_header_levels": "M146 (2026-08-16): registrations died with the rewrite; see above",
    "test_rulebook_polish": "M146 (2026-08-16): registrations died with the rewrite; see above",
    "test_search_first_candidates": "M146 (2026-08-16): registrations died with the rewrite; see above",
}


# M95 (D-056). Five entries, because the placement doctrine fails in five
# independent ways and any one of them silently restores the pre-M95 reading:
# lose the rule definition and "operative" has no test; lose either half of the
# asymmetry and guard-pinning flips back to keep-verbatim (the failure RR03
# names); lose the unguarded case and every unpinned rule becomes unprovable;
# lose D-056's no-backfill clause and the rejected "author the D-entries, then
# slim" remedy becomes licensed by the placement test itself.
#
# M116 (D-071) adds seven. Four are the ways the repair itself fails, each
# restoring the superseded reading: lose the deletion-only clause and the
# inversion arm silently returns, routing every duplicate to "keep"; lose step 0
# and restatement has no test at all; lose its forward-binding clause and the
# check reads as the file-wide sweep D-057 closed; lose the guard-verification
# assignment and the inversion procedure floats back to placement. The other
# three close gaps the repair leaves: the inflow cell, whose literal must stay
# lexically disjoint from the paragraph's or `blank_block` errors on a
# twice-occurring locator, and the Step-0 and Relabel anchors, whose tests would
# otherwise register only their second assert.
REGISTRY += [
    Mutation(
        guard="test_rule_placement",
        test="TestDecisionRecord.test_entry_forbids_the_backfill_sweep",
        target="cairn/DECISIONS.md",
        block="author the entry when the choice is next\n   touched, never as a backfill sweep",
    ),
    # An operative clause M95's inversion sweep found unpinned while the
    # rules around it were guarded. Registered rather than left to the
    # by-hand record, because it is a one-clause rule that a later editorial
    # pass would read as trimmable prose. (Its sibling — D-049's
    # measure-the-mean clause — retired with the whole-file axis at
    # M101/D-058.)
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_the_correction_must_be_marked",
        target=RULES,
        block="the correction marked",
    ),
]

# M97 (D-054). One entry per clause the bounded read rests on, not one for the
# block: the four clauses fail independently — dropping the back-reference
# leaves a rule that still reads correctly and recalls wrongly on D-012/D-014/
# D-019 — so a single exemplar would let three of them be deleted green.
REGISTRY += [
    # M101 (D-059): the advisory is retired; the rule's enforcement sentence
    # now states conduct + back-reference. The retirement statement is the
    # positive framing its assertNotIn pairs with.
    Mutation(
        guard="test_bounded_decisions_read",
        test="TestPlanSkillWiresTheProtocol."
             "test_collision_check_states_read_whole_and_back_reference",
        target="skills/milestone-plan/SKILL.md",
        block="back-reference each match by its own `D-0NN` id",
    ),
    # M97 review F7. The session-start site had only the headings clause,
    # which alone reads as "headings are enough" — the failure mode the
    # protocol prevents. Its own entry because the collision-check block
    # above can carry its guard while this one is deleted green.
    Mutation(
        guard="test_bounded_decisions_read",
        test="TestPlanSkillWiresTheProtocol."
             "test_session_start_also_states_read_whole_and_back_reference",
        target="skills/milestone-plan/SKILL.md",
        block="Read every matched entry whole before surfacing it, and "
              "back-reference it by",
    ),
]

# M114: the thrash rule, unguarded prose until now. One entry per independent
# failure of the rule — the count is deliberately not stated here, because the
# first version of this comment said "six" against seven entries and was
# staler still at nine (§6: a number fails derived-wrong and restated-stale
# alike; let the list below be the count). The intraclass M93 post-mortem
# shows four of these failing for real: lose "per milestone, never per cut" or the
# increments-never-resets clause and the counter reads per-cut again (M93's
# pass 4 logged as the re-cut's first, and the rule went silent for four more
# returns); lose either half of the second trigger and a wrong design reads as
# ordinary iteration; lose the brief fallback and trigger (b) has no remedy
# when the gate recorded no alternative.
REGISTRY += [
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashCounting.test_returns_are_counted_per_milestone_not_per_cut",
        target=REVIEW,
        block="Count returns **per milestone, never per cut**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashCounting.test_a_recut_increments_the_count_and_never_resets_it",
        target=REVIEW,
        block="increments the count and never resets it",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashCounting.test_the_rule_names_the_work_log_as_the_counting_source",
        target=REVIEW,
        block="**Count them in the work log**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashCounting.test_the_rule_names_the_work_log_as_the_counting_source",
        target=REVIEW,
        block="supersedes the tasks and unticks every\n   criterion",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers."
             "test_third_return_is_a_threshold_and_recommends_descope_or_park",
        target=REVIEW,
        block="**(a) The third return, and every return after it**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers."
             "test_third_return_is_a_threshold_and_recommends_descope_or_park",
        target=REVIEW,
        block="Do not queue another retry; the recommended option is descope-or-park\n     (M143)",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers."
             "test_third_return_is_a_threshold_and_recommends_descope_or_park",
        target=REVIEW,
        block="via the gated amendment protocol (`/milestone-implement` step 6)",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers."
             "test_third_return_is_a_threshold_and_recommends_descope_or_park",
        target=REVIEW,
        block="re-cut is never the recommended one",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers."
             "test_third_return_is_a_threshold_and_recommends_descope_or_park",
        target=REVIEW,
        block="It is a threshold, not a single moment",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_both_firing_composes_rather_than_one_winning",
        target=REVIEW,
        block="**Where both fire they compose.**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_composition_gives_a_the_disposition",
        target=REVIEW,
        block="(a) governs the disposition — no further\n   retry",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_composition_carries_b_into_the_composed_chip",
        target=REVIEW,
        block="escalation offer carry INTO that composed chip rather than being discarded",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_composition_states_where_bs_remedy_lives",
        target=REVIEW,
        block="(b)'s remedy — reconsidering\n   it — rides the present, never-recommended re-cut option",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_composition_names_the_composed_menu",
        target=REVIEW,
        block="the chip composed from (a)'s descope-or-park\n   menu",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_exhaustion_branch_states_its_composed_remedy",
        target=REVIEW,
        block="Descope-or-park stays the recommended\n   option; beside it the chip "
              "carries an offered `/milestone-brief` escalation\n   and "
              "dropping at the user's explicit decision —",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_exhaustion_branch_states_its_diagnosis",
        target=REVIEW,
        block="the work log already records a re-plan or split spent\n   on this milestone",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_exhaustion_branch_states_its_remedy",
        target=REVIEW,
        block="the same-objective re-cut leaves the menu entirely",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_review_thrash_block_matches_its_fixture",
        target=REVIEW,
        block="descope — narrow the milestone to its already-verified criteria",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_review_thrash_block_matches_its_fixture",
        target=REVIEW,
        block="both downstream lineages on record\n     show a re-cut buying further returns",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers."
             "test_second_trigger_is_same_criterion_new_mechanism_same_shape",
        target=REVIEW,
        block="The same acceptance criterion failing twice, each by a new mechanism\n     of the same shape",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers.test_second_trigger_remedy_is_the_recorded_alternative",
        target=REVIEW,
        block="reconsider the alternative the plan gate recorded\n     against",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers.test_no_recorded_alternative_offers_brief_escalation",
        target=REVIEW,
        block="Where it recorded none, offer escalation via `/milestone-brief`",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers.test_no_recorded_alternative_offers_brief_escalation",
        target=REVIEW,
        block="instance, never automatically",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_exhaustion_branch_states_its_remedy",
        target=REVIEW,
        block="never a\n   bare retry as the recommended option",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers.test_review_names_the_work_log_as_where_the_record_is_read",
        target=REVIEW,
        block="step 4 of `/milestone-plan` records it in the work log",
    ),
    # M130: the return floor and the amendment return. One entry per
    # separately deletable property, same discipline as the thrash entries
    # above — the test list is the count.
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_domain_limb_applies_only_where_a_procedure_is_named",
        target=REVIEW,
        block="inside its named procedure's domain, where the\n   criterion names one",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_sub_floor_findings_triage_with_no_status_change_and_are_logged",
        target=REVIEW,
        block="Every other actioned finding takes the triage above — fix now / follow-up\n   / reject — with no status change, and is logged",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_amendment_return_is_the_named_exception",
        target=REVIEW,
        block="The amendment return\n   below is the one named exception",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_defect_return_count_is_step4_plus_floor_returns",
        target=REVIEW,
        block="The defect-return count the thrash rule reads is step-4 gate returns\n   plus returns under this floor; amendment returns stay off it",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_floor_return_takes_step_4_exit",
        target=REVIEW,
        block="A floor return\n   takes step 4's exit — a work-log line naming exactly what failed, stop.",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_thrash_count_is_of_defect_returns",
        target=REVIEW,
        block="The count here is of defect returns; amendment returns run\n   on their own track (the step-5 return floor, M130).",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_amendment_return_keys_on_the_criterion_being_wrong",
        target=REVIEW,
        block="falsifying it only outside the domain of the procedure it\n   names, or showing a criterion that names no procedure to be unbounded\n   (the never-reinterpret rule's case, step 3)",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_amendment_route_convenes_the_amendment_alone",
        target=REVIEW,
        block="routes to the gated\n   criterion-amendment protocol (`/milestone-implement` step 6) and\n   re-review, the amendment the only work convened; status is set to\n   `in-progress` for that amendment alone, and review stops there",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_implement_step_6_writes_the_amendment_return_shape",
        target="skills/milestone-implement/SKILL.md",
        block="amendment executing an amendment return from `/milestone-review` writes\n     its work-log line in that skill's fixed shape",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_amendment_return_work_log_line_has_a_fixed_shape",
        target=REVIEW,
        block='`amendment return: AC<N> — "<amended clause, verbatim>"`',
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_amendment_returns_count_on_their_own_track",
        target=REVIEW,
        block="counted per milestone on their own track: never reset by\n   a re-cut, and never added to the defect-return count",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestReturnFloor.test_second_amendment_return_on_the_same_id_stops",
        target=REVIEW,
        block="A second amendment return naming the same AC<N> on one milestone\n   stops",
    ),
]

# M139/M140: the step-5 return rules and the implement-side repair direction,
# guarded by whole-slice equality (D-103, RR12). Per slice, two entries name
# the equality method: an exemplar block inside the slice (blanking changes
# the normalized slice, so equality reds) and the slice's start marker
# (blanking collapses the slice to "", the vacuity case BC7 requires
# demonstrated). The uniqueness methods keep their own marker entries below
# (M126 decoy defense).
REGISTRY += [
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_review_amendment_matches_its_fixture",
        target=REVIEW,
        block="or meeting the widening\n   test below, which carves that third case out of this clause's \"only\n   outside\"",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_review_amendment_matches_its_fixture",
        target=REVIEW,
        block="**Amendment return (M130).**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_implement_m139_matches_its_fixture",
        target=IMPLEMENT,
        block="a wider enumeration is not an admissible\n     amendment",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_implement_m139_matches_its_fixture",
        target=IMPLEMENT,
        block="An amendment executing a return reclassified",
    ),
    # The slice markers, each asserted unique in its host file. Blanking one
    # drops its count to 0, so the uniqueness assert reds.
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_review_floor_marker_is_unique",
        target=REVIEW,
        block="**Return floor (M130).**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_review_amendment_marker_is_unique",
        target=REVIEW,
        block="**Amendment return (M130).**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_review_widening_marker_is_unique",
        target=REVIEW,
        block="**Widening test (M139).**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_implement_substantive_start_marker_is_unique",
        target=IMPLEMENT,
        block="- *Substantive* (a criterion or scope must change",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_implement_substantive_end_marker_is_unique",
        target=IMPLEMENT,
        block="- *The goal itself is wrong*",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_implement_m139_start_marker_is_unique",
        target=IMPLEMENT,
        block="An amendment executing a return reclassified",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestWideningTest.test_implement_m139_end_marker_is_unique",
        target=IMPLEMENT,
        block="An amendment\n     that grows a plan-owned section",
    ),    # M140: the guard-craft banking (RR12 Q5) — one entry per added claim.
]

# M117: the upstream half of trigger (b) — /milestone-plan creates the record
# (b) reads. One entry per independently-deletable span across the obligation,
# its placement, its cardinality, its absence case, and the template surface;
# the entries below are the enumeration, and this comment deliberately is not
# one — a list here goes stale on the next append, and a count of it goes
# stale faster (§6). The absence case is the subtle span: without it "no line"
# is ambiguous between "none was weighed" and "the plan forgot", and only the
# first makes (b)'s escalation fallback the correct read.
REGISTRY += [
    Mutation(
        guard="test_thrash_rule",
        test="TestPlanRecordsTheRejectedAlternative."
             "test_plan_obliges_recording_the_rejected_alternative",
        target="skills/milestone-plan/SKILL.md",
        block="**Record the alternative the gate rejected.**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestPlanRecordsTheRejectedAlternative."
             "test_plan_obliges_recording_the_rejected_alternative",
        target="skills/milestone-plan/SKILL.md",
        block=(
            "append a work-log line naming the alternative rejected, why\n"
            "     it lost, and the class of evidence that would falsify the "
            "choice"
        ),
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestPlanRecordsTheRejectedAlternative."
             "test_a_plan_weighing_no_alternative_writes_no_line",
        target="skills/milestone-plan/SKILL.md",
        block=(
            "A plan that weighed\n     no alternative writes no line: absence "
            "means none was weighed"
        ),
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestPlanRecordsTheRejectedAlternative."
             "test_the_obligation_states_its_cardinality",
        target="skills/milestone-plan/SKILL.md",
        block="one\n     line per approach choice the gate actually weighed",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestPlanRecordsTheRejectedAlternative."
             "test_the_template_shows_the_record_and_its_cardinality",
        target=TEMPLATE,
        block=(
            "one per approach choice the\n     gate actually weighed, none "
            "where it weighed none"
        ),
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestPlanRecordsTheRejectedAlternative."
             "test_the_template_shows_the_record_and_its_cardinality",
        target=TEMPLATE,
        block=(
            "plan gate chose <approach> over <alternative> because\n     "
            "<reason>; falsified by <evidence class>."
        ),
    ),
]


# M100 (RR04 rec 8): finding-enforcement prose. One entry per target file the
# guard reads, plus separate entries where blocks fail independently (the
# review-section juxtaposition and the merge-chip shortfall option each carry
# a distinct mechanism).
REGISTRY += [
    Mutation(
        guard="test_finding_enforcement",
        test="TestIngestRule.test_ingest_rule_requires_verbatim_travel",
        target=BRIEF,
        block="**Binding criteria travel verbatim:**",
    ),
    Mutation(
        guard="test_finding_enforcement",
        test="TestIngestRule.test_ingest_rule_prescribes_the_numbered_form",
        target=BRIEF,
        block="counts every AC checkbox positionally",
    ),
    Mutation(
        guard="test_finding_enforcement",
        test="TestIngestRule.test_archive_move_is_robust_to_untracked",
        target=BRIEF,
        block="`git mv` fails on an untracked file",
    ),
    Mutation(
        guard="test_finding_enforcement",
        test="TestMilestoneTemplate.test_template_carries_the_driving_rr_slot",
        target=TEMPLATE,
        block="- **Driving RR:** —",
    ),
    Mutation(
        guard="test_finding_enforcement",
        test="TestMilestoneTemplate.test_template_prescribes_the_ingest_form",
        target=TEMPLATE,
        block="coverage-complete counts AC checkboxes positionally",
    ),
    Mutation(
        guard="test_finding_enforcement",
        test="TestReviewSurfaces."
             "test_review_section_juxtaposes_projection_and_outcome",
        target=REVIEW,
        block="**Projection-vs-outcome (Driving RR).**",
    ),
    Mutation(
        guard="test_finding_enforcement",
        test="TestReviewSurfaces."
             "test_merge_chip_repeats_the_pairs_and_offers_accept_shortfall",
        target=REVIEW,
        block='**"accept shortfall, recorded as such"**',
    ),
    Mutation(
        guard="test_finding_enforcement",
        test="TestPlanBullet."
             "test_plan_sets_slot_ingests_verbatim_and_copies_projections",
        target="skills/milestone-plan/SKILL.md",
        block="- **Driving RR** (header slot):",
    ),
]


# M110 (D-061): maturation's second application — the records-hygiene family
# graduated into a second module. Entries span the three registered surfaces —
# the module, the rulebook pointer beside the retirement rule, and D-061 —
# one per positive assert (M53). The fourth surface the guard pins, LESSONS.md,
# carries no entry: its absence asserts can't be mutation-proven, since
# blanking cannot restore a line that left (M54/M84).
REGISTRY += [
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestModuleExists.test_module_declares_when_it_is_read",
        target=RECORDS_HYGIENE,
        block="Read this whenever you are at a milestone hygiene or plan gate",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestModuleExists.test_section1_candidate_rows_graduate_at_completion",
        target=RECORDS_HYGIENE,
        block="Candidates graduate at *completion*",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestModuleExists.test_section2_collision_sweep_greps_the_archive",
        target=RECORDS_HYGIENE,
        block="collision sweep greps `milestones/archive/` for *decisions*",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestDecisionEntry.test_decision_entry_exists_and_annotates_d055",
        target="cairn/DECISIONS.md",
        block="### D-061 (2026-07-23): The records-hygiene lesson family graduates",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestDecisionEntry.test_decision_entry_states_graduate_not_ownership",
        target="cairn/DECISIONS.md",
        block="graduate into the module rather than",
    ),
]

# M146 review fix pass (2026-08-16): content pins for the three surviving
# records rules in the reduced rulebook, and the two live stamp write sites —
# restoring mutation proof for rules D-116 keeps binding (review findings
# B1/O9/O13 and the prune-verification sweep's SEVERE 1-4).
REGISTRY += [
    Mutation(
        guard="test_derived_claims",
        test="TestDerivedClaimsRule.test_rule_states_derive_never_compose",
        target=RULES,
        block="derived, never composed** (the derived-claims rule)",
    ),
    Mutation(
        guard="test_derived_claims",
        test="TestDerivedClaimsRule.test_tracking_records_exemption_names_its_members",
        target=RULES,
        block="Tracking records are exempt from this rule and from the derived-figures and",
    ),
    Mutation(
        guard="test_derived_claims",
        test="TestDerivedClaimsRule.test_derived_figures_rule_states_its_headline",
        target=RULES,
        block="pinned or procedural, never free-standing",
    ),
    Mutation(
        guard="test_failure_identity",
        test="TestFailureIdentityRule.test_rule_bullet_present_with_identity_clause",
        target=RULES,
        block="condition class, message, or signaling site",
    ),
    Mutation(
        guard="test_failure_identity",
        test="TestFailureIdentityRule.test_passing_control_clause_present",
        target=RULES,
        block="discriminating test's passing control is shown to pass for the claim's reason",
    ),
    Mutation(
        guard="test_hygiene_stamp",
        test="TestStampWriteSites.test_milestone_audit_write_site_says_replace",
        target=MILESTONE,
        block="never append to the previous stamp or demote it",
    ),
    Mutation(
        guard="test_hygiene_stamp",
        test="TestStampWriteSites.test_review_write_site_says_replace",
        target=REVIEW,
        block="never append to it or demote it to a `Prior:` clause",
    ),
]


# --------------------------------------------------------------------------
# Engine mechanics
# --------------------------------------------------------------------------
class TestBlankBlock(unittest.TestCase):
    def test_removes_the_single_occurrence(self):
        self.assertEqual(me.blank_block("a RULE b", "RULE "), "a b")

    def test_absent_block_is_a_hard_error(self):
        with self.assertRaises(ValueError):
            me.blank_block("nothing here", "MISSING")

    def test_ambiguous_block_is_a_hard_error(self):
        # A locator that matches twice must fail loudly, not blank one of two.
        with self.assertRaises(ValueError):
            me.blank_block("dup and dup", "dup")


# --------------------------------------------------------------------------
# The harness's own oracle: catch a sound guard's failure, flag a weak guard
# that survives deletion. Both fixture guards read the same temp file the same
# way real guards read their sources (pathlib read_text).
# --------------------------------------------------------------------------
# A rule sentence whose token ("sweep") ALSO appears in an unrelated decoy
# line — the exact shape of the false-coverage trap.
_FIXTURE_SRC = (
    "Intro line.\n"
    "- Rule: always sweep existing candidates before adding one.\n"
    "Unrelated: the janitor will sweep the floor nightly.\n"
)
_RULE_BLOCK = "always sweep existing candidates before adding one"


class TestEngineOracle(unittest.TestCase):
    """Fixture guards are defined *locally* (not module-level TestCase
    subclasses), so `discover` never collects them as standalone tests — they
    exist only to be driven by the engine here."""

    def setUp(self):
        _fd, path = tempfile.mkstemp(suffix=".md")
        self.path = pathlib.Path(path)
        self.path.write_text(_FIXTURE_SRC)
        self.addCleanup(self.path.unlink)

        target = self.path

        class SoundGuard(unittest.TestCase):
            # Anchors on the rule's own contiguous phrasing (M39 discipline).
            def test_rule(self):
                text = target.read_text()
                self.assertIn("sweep existing candidates before adding one", text)

        class WeakGuard(unittest.TestCase):
            # Anchors on a bare token that recurs in the decoy — false coverage.
            def test_rule(self):
                text = target.read_text()
                self.assertIn("sweep", text)

        self.SoundGuard = SoundGuard
        self.WeakGuard = WeakGuard

    def test_sound_guard_is_caught_failing_on_deletion(self):
        # Blanking the rule block must make the sound guard fail.
        self.assertTrue(
            me.guard_fails_when_blanked(
                str(self.path), _RULE_BLOCK, self.SoundGuard, "test_rule"
            )
        )

    def test_weak_guard_is_flagged_surviving_deletion(self):
        # The weak guard still passes after the rule is blanked (its token
        # survives in the decoy line) — the engine must report False.
        self.assertFalse(
            me.guard_fails_when_blanked(
                str(self.path), _RULE_BLOCK, self.WeakGuard, "test_rule"
            )
        )


def prose_guard_modules():
    """Every `test_*.py` under skills/tests. This directory holds only
    prose-guards by design, so each file must be registered or exempted."""
    return {p.stem for p in me.ENGINE_DIR.glob("test_*.py")}


def unregistered(discovered, registered, exempt):
    """Prose-guard modules that are neither registered nor exempt."""
    return set(discovered) - set(registered) - set(exempt)


class TestRegistryCompleteness(unittest.TestCase):
    def test_every_prose_guard_is_registered_or_exempt(self):
        missing = unregistered(
            prose_guard_modules(), {m.guard for m in REGISTRY}, EXEMPT
        )
        self.assertEqual(
            missing,
            set(),
            f"prose-guard files not covered by the mutation harness — add a "
            f"Mutation entry or an EXEMPT reason: {sorted(missing)}",
        )

    def test_no_registry_or_exempt_entry_points_at_a_missing_file(self):
        discovered = prose_guard_modules()
        stale = ({m.guard for m in REGISTRY} | set(EXEMPT)) - discovered
        self.assertEqual(
            stale, set(), f"registry/EXEMPT names a nonexistent guard: {sorted(stale)}"
        )

    def test_completeness_flags_an_unregistered_guard(self):
        # The mechanism itself: an unregistered, unexempted module is reported.
        self.assertEqual(
            unregistered({"test_a", "test_b"}, {"test_a"}, {}), {"test_b"}
        )
        self.assertEqual(
            unregistered({"test_a", "test_b"}, {"test_a"}, {"test_b": "why"}), set()
        )


# M120: the correction-narration rule adopted from the Opus 5 prompting guide.
# One entry per assert, not per guard file: the rule's four claims — the
# materiality bar, the plain-and-continue form, the unremarked slip, and the
# boundary against D-045's record repair — each carry it independently, so a
# single entry would leave three asserts unproven (M53 per-block discipline).
REGISTRY += [
    Mutation(
        guard="test_narration_discipline",
        test="TestCorrectionNarrationRule.test_rule_separates_chat_slips_from_durable_records",
        target=RULES,
        block="A chat slip never reaches a durable record",
    ),
]


# M120: the delegation-warrant test. One entry per assert — the inline floor,
# the one-not-several bar, and the fan-out reconciliation each carry the rule
# independently, and the third is not commentary: without it the rule and the
# three-reviewer fan-out sit in one section unreconciled.
REGISTRY += [
    Mutation(
        guard="test_delegation_warrant",
        test="TestDelegationWarrantRule.test_rule_prefers_one_subagent_over_several",
        target=RULES,
        block="spawn one rather than several",
    ),
    # M121. One entry per named class, per AC4. The excluded class is the
    # load-bearing half: the governed class restates the warrant above it,
    # while the exclusion is what stops the guide's third clause from being
    # read onto D-067's fresh-context readers.
    # M121 review pass 2. Two entries for the two rules that inverted with the
    # suite green: the section's lead claim that the warrant reaches one class
    # and not the other, and the measurement motivating the record requirement.
    # M121 review. Four more entries, from findings the fan-out scored 80+:
    # F-PR1 (the two class asserts stopped at the em-dash, leaving each
    # rationale clause deletable green) and F-B1/F-B2 (the discriminator and
    # the loop-bound sentences inverted with the suite green).
]


# M134: the derived-claims rule — three clauses, each separately deletable.
# The intraclass M103 post-mortem is the failure mode: lose clause (a) and an
# evidence line composed from the author's expectation reads as compliant;
# lose (b) and narration restating the code returns; lose (c) and an
# enumeration drifts the first time its artifact changes.
REGISTRY += [
    Mutation(
        guard="test_derived_claims",
        test="TestDerivedClaimsRule.test_implement_step4_carries_the_pointer",
        target=IMPLEMENT,
        block="Prose the commit adds about an artifact's behavior follows the tracking-rules derived-claims rule: derived from the artifact, never composed.",
    ),
]


# The tidymedia M54 post-mortem is the failure mode: lose the header or
# premise and a schema error reads as the behavior under test; lose the
# identity clause and a claim rests on a bare observation; lose the
# distinguishing step and confounded inputs pass unexamined; lose either
# test-form line and a vacuous control certifies an unrelated pass; lose a
# rendering or the pointer and the rule never reaches the site that writes.
REGISTRY += [
    Mutation(
        guard="test_failure_identity",
        test="TestFailureIdentityRule.test_r_profile_renders_identity_for_expect_error",
        target=R_PROFILE,
        block="every `cli_abort()` branch fired and identified — `expect_error(class =)` or a message matcher, never bare `expect_error()`",
    ),
    Mutation(
        guard="test_failure_identity",
        test="TestFailureIdentityRule.test_implement_step4_carries_the_pointer",
        target=IMPLEMENT,
        block="A claim resting on an observed failure follows the tracking-rules failure-identity rule: verified to be the failure the claim is about, never read off a bare error.",
    ),
]


# M165: the freshness-spawns clause under a spawn-restricting harness
# instruction — four blocks, each separately deletable. Lose (a) and the
# harness line reads as forbidding every freshness spawn; lose (b) and a
# blocked session degrades with no gate; lose the chip sentence and the gate
# stops saying what a degraded run means; lose (c) and a permitted inline run
# need not be logged — the silent degradation itself.
REGISTRY += [
    Mutation(
        guard="test_freshness_spawn_instruction",
        test="TestFreshnessSpawnInstructionClause.test_skill_invocation_is_the_users_spawn_request",
        target=RULES,
        block="request for the subagent spawns the skill's steps mandate",
    ),
    Mutation(
        # the trigger subject of (a) — its own entry per the one-entry-per-
        # assertion rule (M165 review F4).
        guard="test_freshness_spawn_instruction",
        test="TestFreshnessSpawnInstructionClause.test_skill_invocation_is_the_users_spawn_request",
        target=RULES,
        block="A harness instruction restricting subagent spawns",
    ),
    Mutation(
        guard="test_freshness_spawn_instruction",
        test="TestFreshnessSpawnInstructionClause.test_a_blocked_session_surfaces_the_conflict_at_the_pending_gate",
        target=RULES,
        block="asking the user to request the spawns in so",
    ),
    Mutation(
        # the condition subject of (b) — its own entry (M165 review F4).
        guard="test_freshness_spawn_instruction",
        test="TestFreshnessSpawnInstructionClause.test_a_blocked_session_surfaces_the_conflict_at_the_pending_gate",
        target=RULES,
        block="A session that still cannot or will not spawn a",
    ),
    Mutation(
        guard="test_freshness_spawn_instruction",
        test="TestFreshnessSpawnInstructionClause.test_the_chip_explains_author_inline_in_plain_words",
        target=RULES,
        block="the chip says in plain words what an author-inline run means",
    ),
    Mutation(
        guard="test_freshness_spawn_instruction",
        test="TestFreshnessSpawnInstructionClause.test_an_inline_author_run_is_a_logged_deviation_never_silent",
        target=RULES,
        block="user-accepted, logged deviation naming the",
    ),
]


class TestRegisteredGuardsFailWhenBlanked(unittest.TestCase):
    def test_each_registered_guard_fails_when_its_block_is_blanked(self):
        self.assertTrue(REGISTRY, "registry is empty")
        for m in REGISTRY:
            with self.subTest(guard=m.guard, test=m.test):
                cls, method = me.load_case(m.guard, m.test)
                self.assertTrue(
                    me.guard_fails_when_blanked(m.target, m.block, cls, method),
                    f"{m.guard}.{m.test} PASSED after blanking {m.block!r} in "
                    f"{m.target} — false coverage. Re-anchor the guard on the "
                    f"rule's own unique phrasing (M39/M40 discipline).",
                )


if __name__ == "__main__":
    unittest.main()


REGISTRY += [
    # M166: issue linkage — one entry per positive assert's block.
    Mutation(
        guard="test_issue_linkage",
        test="TestTemplateSlot.test_milestone_template_carries_the_slot_with_both_entry_forms",
        target=TEMPLATE,
        block="- **Resolves:** —",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestTemplateSlot.test_archive_status_line_carries_a_resolves_clause",
        target=ARCHIVE_TEMPLATE,
        block="; resolves <the",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestPlanFillsTheSlot.test_slot_is_filled_from_the_issues_the_scope_absorbs",
        target=PLAN,
        block="the slot is filled from the issues the scope",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestPlanFillsTheSlot.test_both_entry_forms_are_defined",
        target=PLAN,
        block="`#N closes` when this milestone's PR closes",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestPlanFillsTheSlot.test_partial_remainder_is_rowed_in_the_same_plan_commit",
        target=PLAN,
        block="remainder is recorded as a `candidate` row in the same plan commit",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestPlanFillsTheSlot.test_step_5_ledger_lists_the_partial_remainder",
        target=PLAN,
        block="entry in the `Resolves:` slot lists its remainder here with the candidate",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestPlanGateAcknowledgement.test_gate_poses_one_option_for_all_slotted_issues",
        target=PLAN,
        block="the gate poses one option offering an",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestPlanGateAcknowledgement.test_comment_body_is_fixed_and_shown_before_selection",
        target=PLAN,
        block="`Queued as M<NNN>: <title>`",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestPlanGateAcknowledgement.test_posted_only_on_selection_never_by_default",
        target=PLAN,
        block="only on selection, never by",
    ),
]

REGISTRY += [
    # M166 T3–T5: review, hotfix, and audit blocks.
    Mutation(
        guard="test_issue_linkage",
        test="TestReviewPRBody.test_pr_body_ends_with_closes_and_refs_lines_from_the_slot",
        target=REVIEW,
        block="`Closes #N` line per `closes` entry and one `Refs #N` line per `partial`",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReviewPRBody.test_dash_slot_adds_no_lines",
        target=REVIEW,
        block="a slot of `—` adds no lines",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReviewMergeChipAuthorizes.test_chip_text_enumerates_the_issue_writes_it_authorizes",
        target=REVIEW,
        block="writes it authorizes — close-if-open per `closes`",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReviewMergeChipAuthorizes.test_no_other_issue_write_is_made",
        target=REVIEW,
        block="no other issue write is made",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReviewPostMergeRead.test_each_closes_entry_is_read_after_the_merge",
        target=REVIEW,
        block="after the merge, for each `closes` entry of",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReviewPostMergeRead.test_a_still_open_issue_is_closed_naming_the_merged_pr",
        target=REVIEW,
        block="`gh issue close <N> --comment` carrying a one-line comment naming the\n   merged PR",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReviewPostMergeRead.test_partial_comments_are_posted",
        target=REVIEW,
        block="entry post the comment naming what shipped and the remainder's candidate",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReviewPostMergeRead.test_unreachable_gh_is_reported_and_never_fails_hygiene",
        target=REVIEW,
        block="an unreachable `gh` never fails the hygiene pass",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReviewPostMergeRead.test_done_recap_reports_the_state_reads",
        target=REVIEW,
        block="The done recap reports each entry's state read",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestHotfixPostMergeRead.test_fixes_line_triggers_the_read_and_close_if_open",
        target=HOTFIX,
        block="When the PR body carries a `Fixes #N`",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestHotfixPostMergeRead.test_no_fixes_line_is_a_noop",
        target=HOTFIX,
        block="a PR with no such line is a no-op here",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestHotfixPostMergeRead.test_unreachable_gh_is_reported_never_a_failure",
        target=HOTFIX,
        block="was in the recap — never a failure",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_reads_are_bounded_to_the_retained_terminal_rows",
        target=MILESTONE,
        block="terminal rows bound the reads",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_a_closes_entry_is_read_with_state_and_url",
        target=MILESTONE,
        block="`gh issue view <N> --json state,url`",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_a_still_open_issue_is_an_orphan",
        target=MILESTONE,
        block="one still open is reported as",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_no_entry_and_partial_only_read_nothing_multi_entry_reads_each",
        target=MILESTONE,
        block="`resolves` clause, or with `partial` entries only, reads nothing",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_orphan_read_writes_nothing",
        target=MILESTONE,
        block="the orphan read writes nothing",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_unreachable_gh_rule_applies_unchanged",
        target=MILESTONE,
        block="unreachable-`gh` rule applies unchanged",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_never_write_sentence_is_narrowed_to_the_reads",
        target=MILESTONE,
        block="the sweep and the orphan",
    ),
    Mutation(
        # the pointer at the one gated write — its own entry.
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_never_write_sentence_is_narrowed_to_the_reads",
        target=MILESTONE,
        block="the one audit-path write is §3's close disposition",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_close_disposition_fires_only_on_selection_naming_the_pr",
        target=MILESTONE,
        block="**close** — an orphaned issue from §2's orphan bullet",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestAuditOrphanBullet.test_close_disposition_fires_only_on_selection_naming_the_pr",
        target=MILESTONE,
        block="Not selected → the issue stays open and nothing is written",
    ),
]

REGISTRY += [
    # M166 T6: README states the three behaviors.
    Mutation(
        guard="test_issue_linkage",
        test="TestReadmeStatesTheThreeBehaviors.test_plan_time_acknowledgement_offer",
        target=README,
        block="plan gate offers one option to post `Queued as M<NNN>: <title>`",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReadmeStatesTheThreeBehaviors.test_plan_time_acknowledgement_offer",
        target=README,
        block="posted only if you select it, never by default",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReadmeStatesTheThreeBehaviors.test_pr_closing_keyword",
        target=README,
        block="draft PR body ends with `Closes #N`",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReadmeStatesTheThreeBehaviors.test_post_merge_check_and_audit_orphan",
        target=README,
        block="reads the state of each issue slotted `closes` and closes",
    ),
    Mutation(
        guard="test_issue_linkage",
        test="TestReadmeStatesTheThreeBehaviors.test_post_merge_check_and_audit_orphan",
        target=README,
        block="and offers to close it at the",
    ),
]

REGISTRY += [
    # M169: criteria and tasks carry positional labels. One entry per pinned
    # block — the template's labeled examples, each section comment's
    # position rule, the unified ingest form at both prose sites, plan step
    # 4's labeling rule, and implement step 6's obligation on each branch.
    Mutation(
        guard="test_positional_labels",
        test="TestTemplateLabelsItsExamples."
             "test_acceptance_criteria_examples_are_labeled",
        target=TEMPLATE,
        block="AC1: Each objectively checkable",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestTemplateLabelsItsExamples.test_task_examples_are_labeled",
        target=TEMPLATE,
        block="T1: Ordered concrete steps",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestTemplateCommentsStateThePositionRule."
             "test_acceptance_criteria_comment_states_the_rule",
        target=TEMPLATE,
        block="Every item opens with its positional label — `ACn:` — the "
              "item's\n     position counted top-to-bottom, the number "
              "Coverage cites",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestTemplateCommentsStateThePositionRule."
             "test_acceptance_criteria_comment_states_the_rule",
        target=TEMPLATE,
        block="insertion, removal, or reorder renumbers the labels and the "
              "Coverage\n     lines together",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestTemplateCommentsStateThePositionRule."
             "test_tasks_comment_states_the_rule",
        target=TEMPLATE,
        block="Every item opens with its positional label —\n     `Tn:` — "
              "the item's position counted top-to-bottom",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestTemplateCommentsStateThePositionRule."
             "test_tasks_comment_states_the_rule",
        target=TEMPLATE,
        block="reorder renumbers the labels and the\n     Coverage lines "
              "together",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestIngestFormIsUnified.test_template_comment_shows_the_unified_form",
        target=TEMPLATE,
        block="`- [ ] ACn (BCm): <verbatim>`",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestIngestFormIsUnified.test_brief_ingest_rule_shows_the_unified_form",
        target=BRIEF,
        block="`- [ ] ACn (BCm): <verbatim>`",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestPlanStepFourStatesTheLabelingRule."
             "test_every_bullet_opens_with_its_label",
        target=PLAN,
        block="every criterion and task bullet\n     opens with its "
              "positional label (`ACn:` / `Tn:`)",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestPlanStepFourStatesTheLabelingRule."
             "test_label_equals_position_counted_top_to_bottom",
        target=PLAN,
        block="the label equal to\n     the item's position counted "
              "top-to-bottom",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestPlanStepFourStatesTheLabelingRule."
             "test_edits_renumber_labels_and_coverage_together",
        target=PLAN,
        block="any insertion, removal, or reorder renumbers the labels\n"
              "     and the Coverage lines together",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestImplementStepSixRenumbersOnBothBranches."
             "test_minor_branch_renumbers",
        target=IMPLEMENT,
        block="renumbers the `ACn:` /\n     `Tn:` labels and the Coverage "
              "lines together",
    ),
    Mutation(
        guard="test_positional_labels",
        test="TestImplementStepSixRenumbersOnBothBranches."
             "test_substantive_branch_renumbers",
        target=IMPLEMENT,
        block="renumbers\n     the `ACn:` / `Tn:` labels and the Coverage "
              "lines together",
    ),
]


REGISTRY += [
    # M170: the wait rule's trigger clause and stop-point clause in
    # tracking-rules; the retired-spelling check has no block to mutate.
    Mutation(
        guard="test_wait_rule",
        test="TestWaitRuleTrigger.test_one_watcher_per_wait",
        target=RULES,
        block="One\nwatcher per wait: a run, command, or subagent is watched "
              "by one mechanism at a time, never two on the same thing.",
    ),
    Mutation(
        guard="test_wait_rule",
        test="TestWaitRuleStopPoint.test_no_watcher_left_armed_at_a_stop_point",
        target=RULES,
        block="no watcher is left armed at a commit, a turn end, or a "
              "`/clear` point",
    ),
]


REGISTRY += [
    # M172: the resume route's trigger and its four branches in the review
    # skill's Session start (the list pinned whole, M171 lesson), step 7's
    # approval line, the audit's merged-but-review bullet, and the hotfix
    # merged-PR re-entry. Blocks embed the physical wrap; the guard reads
    # with whitespace collapsed.
    Mutation(
        guard="test_resume_routing",
        test="TestReviewResumeRoute.test_reads_pr_state_before_step_one",
        target=REVIEW,
        block="read that PR's state before step 1 — `gh pr view <N>\n"
              "--json state,mergedAt` (N from the URL)",
    ),
    Mutation(
        guard="test_resume_routing",
        test="TestReviewResumeRoute."
             "test_route_a_merged_and_reviewed_goes_to_step_nine",
        target=REVIEW,
        block="then step 9\n  with steps 1–8 skipped — the recorded approval "
              "stands as step 9's\n  issue-write authorization.",
    ),
    Mutation(
        guard="test_resume_routing",
        test="TestReviewResumeRoute."
             "test_route_b_merged_unreviewed_verifies_post_hoc",
        target=REVIEW,
        block="a decline logs\n  the requested changes as tasks and sets "
              "status `in-progress` (step 7's\n  decline exit); on "
              "acceptance, step 9 with step 8 skipped.",
    ),
    Mutation(
        guard="test_resume_routing",
        test="TestReviewResumeRoute."
             "test_route_c_open_and_approved_reposes_the_gate",
        target=REVIEW,
        block="(c) `OPEN`, every box ticked, and a recorded approval → step "
              "1 re-run,\n  the step-7 chip re-posed, and on approval step 8 "
              "from the marker write\n  onward.",
    ),
    Mutation(
        guard="test_resume_routing",
        test="TestReviewResumeRoute."
             "test_route_d_everything_else_goes_to_step_one",
        target=REVIEW,
        block="A `gh` that is missing, unauthenticated, or has no remote → "
              "step\n  1, the recap naming which of the three it was.",
    ),
    Mutation(
        guard="test_resume_routing",
        test="TestReviewResumeRoute.test_step_seven_records_the_approval_line",
        target=REVIEW,
        block="Approval appends one work-log line naming the PR\n   number "
              "it approved (`step-7 approval: PR #<N> approved for merge`)",
    ),
    Mutation(
        guard="test_resume_routing",
        test="TestMilestoneAuditMergedReview."
             "test_merged_review_milestone_is_hygiene_owed",
        target=MILESTONE,
        block="post-merge hygiene owed: report it as such and route to\n"
              "  `/milestone-review M<NNN>`",
    ),
    Mutation(
        guard="test_resume_routing",
        test="TestHotfixMergedPrReentry.test_merged_pr_runs_step_seven_only",
        target=HOTFIX,
        block="runs step 7 only, steps\n   2–6 skipped",
    ),
    Mutation(
        guard="test_resume_routing",
        test="TestHotfixMergedPrReentry.test_reentry_names_its_three_moves",
        target=HOTFIX,
        block="one chip authorizing the issue close before any issue\n"
              "   write (step 6's chip never ran for it)",
    ),
]
