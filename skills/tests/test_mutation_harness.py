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
TEMPLATE = "skills/shared/templates/milestone.md"
DOCTRINE = "skills/shared/validation-doctrine.md"
GUARD_DOCTRINE = "skills/shared/guard-doctrine.md"
RECORDS_HYGIENE = "skills/shared/records-hygiene.md"
SOURCE_NOTE = "skills/shared/templates/source-note.md"
SYNTHESIS_NOTE = "skills/shared/templates/synthesis-note.md"

REGISTRY = [
    Mutation(
        guard="test_search_first_candidates",
        test="TestSearchFirstCandidateRule.test_rule_names_all_three_sweep_targets",
        target=RULES,
        block="sweep existing candidates + `milestones/archive/`",
    ),
    # M71 (D-042): one entry per positive assert's block — the enumeration,
    # the pairing requirement, and the named enforcement arm each carry the
    # rule independently, so each needs its own mutation proof.
    Mutation(
        guard="test_idea_intake_gate",
        test="TestOutOfBandIdeaCaptureRule.test_rule_names_the_capture_channels_generically",
        target=RULES,
        block="a background-task chip, a scratch TODO, an ad-hoc note",
    ),
    Mutation(
        guard="test_idea_intake_gate",
        test="TestOutOfBandIdeaCaptureRule.test_rule_requires_the_paired_candidate_row",
        target=RULES,
        block="The idea also lands as a `candidate` ROADMAP row",
    ),
    Mutation(
        guard="test_idea_intake_gate",
        test="TestOutOfBandIdeaCaptureRule.test_rule_names_its_runtime_enforcement_arm",
        target=RULES,
        block="`idea_guard.py` PreToolUse hook injects this reminder",
    ),
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
    Mutation(
        guard="test_ac_traceability",
        test="TestRulesDiscipline.test_review_discipline_states_incremental_checkoff",
        target=RULES,
        block="The tick is incremental",
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
        block="779 lines / 53,751 chars",
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
        test="TestReleaseTimingRule.test_rule_forbids_all_three_agent_initiatives",
        target=RULES,
        block="never proposes a release, never plans a release milestone unprompted, and never nominates one as the next action",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestReleaseTimingRule.test_rule_rejects_the_dependency_graph_as_a_readiness_signal",
        target=RULES,
        block="a maintainer judgment about when to ship, never a dependency graph going green",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestReleaseTimingRule.test_rule_names_blocked_as_the_parking_state",
        target=RULES,
        block="is parked as `blocked`, where no routing surface nominates it",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestBlockedCoversTheReleaseWindow.test_blocked_row_names_the_unopened_release_window",
        target=RULES,
        block="a maintainer who has not opened the release window counts",
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
        block="Park M<NN> as `blocked` → the release window is not open",
    ),
    Mutation(
        guard="test_release_timing",
        test="TestMilestoneAuditWiring.test_park_leads_the_chip_only_when_cairn_next_names_that_release",
        target=MILESTONE,
        block="lead the chip with it only when `cairn_next`'s own recommendation names that same release milestone",
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
    Mutation(
        guard="test_chapter_marker_mandate",
        test="TestChapterMarkerMandate.test_rulebook_declares_the_per_phase_mandate",
        target=RULES,
        block="Mark a chapter at each phase transition",
    ),
    Mutation(
        guard="test_default_branch_parameterized",
        test="TestDefaultBranchParameterized.test_git_model_uses_default_branch",
        target=RULES,
        block="The default branch (`main`/`master`) is a distribution",
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
        guard="test_gate_wording",
        test="TestMergeGateIsAChip.test_rulebook_declares_merge_gate_a_chip",
        target=RULES,
        block="merge-approval gate is itself an AskUserQuestion chip",
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
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_the_decisions_advisory_is_stated_with_its_subject",
        target=RULES,
        block="advisory WARNs on — pasted output or a fenced transcript block, never entry",
    ),
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_stated_decisions_advisory_label_matches_the_emitted_label",
        target=RULES,
        block="that paste rule is what `cairn_validate`'s `decisions format`",
    ),
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
        test="TestLessonRetirement.test_enforcement_criterion_pins_its_discriminating_test",
        target=RULES,
        block="**enforcement — a test fails on the mistake the lesson warns about**",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_enforcement_rules_out_a_guard_merely_existing",
        target=RULES,
        block="discriminating word is *fails* and never *exists*",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_ownership_criterion_pins_its_discriminating_test",
        target=RULES,
        block="**ownership — another tracking file's slot owns the content**",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_ownership_permits_moving_content_to_its_owner",
        target=RULES,
        block=(
            "**the retiring milestone may *move* the content there rather "
            "than only find it already duplicated**"
        ),
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_partial_coverage_trims_rather_than_keeping_whole",
        target=RULES,
        block="**A lesson covered only in part is trimmed to its uncovered remainder**",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_tombstone_is_the_archive_summary_and_nothing_else",
        target=RULES,
        block=(
            "**A retired lesson leaves no line behind — the retiring "
            "milestone's archive summary names what it graduated**"
        ),
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_retirement_is_distinguished_from_correction",
        target=RULES,
        block=(
            "**Retirement is not correction: a retired lesson is redundant, "
            "a corrected one was false**"
        ),
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_check_is_scoped_to_what_shipped",
        target=RULES,
        block="**scoped to what the milestone shipped, never as a full re-sweep**",
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
    Mutation(
        guard="test_lessons_loop",
        test="TestLessonRetirement.test_file_map_row_names_retirement",
        target=RULES,
        block="retired once a test enforces it, another file owns it, or a matured family graduates whole into a doctrine module",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_current_knowledge_is_corrected_in_place",
        target=RULES,
        block="current knowledge is corrected in place",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_history_is_superseded_never_edited",
        target=RULES,
        block="history is superseded and never edited",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_rule_rules_out_leaving_the_wrong_text_readable",
        target=RULES,
        block="appending a correction while leaving the wrong text readable",
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
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_history_set_names_its_remaining_members",
        target=RULES,
        block="milestone IDs, `milestones/archive/`, `reviews/archive/`, entombed `legacy/`",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_current_knowledge_set_is_enumerated_under_its_own_label",
        target=RULES,
        block="Current knowledge — `LESSONS.md`, `references/` pages, `DESIGN.md`, `ROADMAP.md` — records what is true *now* and is read to act on,",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_design_principles_are_carved_out_of_in_place_correction",
        target=RULES,
        block="wrong *principle* is not a wrong fact",
    ),
    Mutation(
        guard="test_lessons_loop",
        test="TestRecordCorrectionRule.test_file_map_names_the_lessons_write_mode",
        target=RULES,
        block="a lesson proven false is corrected in place",
    ),
    # M55: the milestone cap exempts the review-exclusive `## Review` section.
    # Two blocks — the exemption rationale and the plan-owned-body cap number —
    # each guarded by its own assert (one Mutation entry per positive assertIn).
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_weight_caps_states_review_exemption",
        target=RULES,
        block="review evidence never scrambles plan-owned content",
    ),
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
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_weight_caps_states_cross_reference_not_restate",
        target=RULES,
        block="cross-reference a durable record",
    ),
    # M77/D-046: the work-log exemption. One entry per new positive assert
    # (M53). Blanking proves deletion is caught; the set-membership assert
    # additionally survives a SWAP, which blanking cannot simulate (M76) —
    # that half is proven by the by-hand swap recorded in the work log.
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_weight_caps_names_the_exempt_set_with_all_three_members",
        target=RULES,
        block="The cap-exempt sections are exactly `## Review` (review-owned, M55), `## Work log` (history under D-045, D-046) and `## Decisions` (history under D-074)",
    ),
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_weight_caps_states_the_work_log_exemption_reason",
        target=RULES,
        block="The `## Work log` is exempt because D-045 makes it history — never edited — so counting it could leave an over-cap file fixable only by an edit IP4 forbids (D-046).",
    ),
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_weight_caps_states_the_wrapped_entry_advisory_warns",
        target=RULES,
        block="advisory WARNs on any work-log line that is not a one-line `- ` entry",
    ),
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_remedy_never_aims_at_an_exempt_section",
        target=RULES,
        block="all three cap-exempt sections are omitted, so the remedy can never aim",
    ),
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
        test="TestMilestoneCapExemption.test_the_cap_definition_itself_names_both_subtracted_sections",
        target=RULES,
        block="the review-exclusive `## Review` section, less the `## Work log` and `## Decisions` sections.",
    ),
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_weight_caps_states_the_decisions_exemption_reason",
        target=RULES,
        block="D-074 makes its dated dispositions history, superseding D-046's choice (3), so the cap may not aim there either.",
    ),
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_always_read_frame_names_all_three_exempt_sections",
        target=RULES,
        block="(`## Work log`, `## Decisions`, `## Review`) by reading less of them",
    ),
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
    Mutation(
        guard="test_milestone_cap_exemption",
        test="TestMilestoneCapExemption.test_stated_advisory_label_matches_the_emitted_label",
        target=RULES,
        block="of a budget it no longer pays into, so `cairn_validate`'s `work-log format`",
    ),
    # M84: the second weight axis. One entry per positive assert on a prose
    # block (M53). The axis->remedy entry is deliberately pair-INCLUSIVE per
    # M74/M76 — both mappings on one physical line, since registration is per
    # file and the sound entries above would mask a mechanism-only pin. The
    # stated<->enforced THRESHOLD assert carries no entry, following its
    # `test_stated_cap_matches_enforced_cap` sibling: both of its halves are
    # computed numbers, not prose a blanking could remove. The LABEL assert
    # does register — its rulebook half is a prose block.
    Mutation(
        guard="test_record_density",
        test="TestRecordDensityRule.test_rule_names_both_axes_with_their_opposite_remedies",
        target=RULES,
        block="The two axes take opposite remedies: an over-count file graduates or prunes items, an over-cap non-item line is replaced by a shorter rewrite, never appended to.",
    ),
    Mutation(
        guard="test_record_density",
        test="TestRecordDensityRule.test_rule_states_why_the_item_axis_cannot_see_weight",
        target=RULES,
        block="structurally blind to prose accumulating",
    ),
    Mutation(
        guard="test_record_density",
        test="TestRecordDensityRule.test_rule_states_that_density_warns_rather_than_fails",
        target=RULES,
        block="Density warns because",
    ),
    Mutation(
        guard="test_record_density",
        test="TestRecordDensityRule.test_rule_maps_each_axis_to_its_label_and_severity",
        target=RULES,
        block="the item axis is the hard `weight caps` CHECK and still FAILs the gate, while the per-line axis is the `record density` advisory and only ever WARNs",
    ),
    Mutation(
        guard="test_record_density",
        test="TestRecordDensityRule.test_rule_records_why_a_per_line_warn_was_rejected",
        target=RULES,
        block="pressure on individual line length would reward splitting an item",
    ),
    Mutation(
        guard="test_record_density",
        test="TestRecordDensityRule.test_stated_advisory_label_matches_the_emitted_label",
        target=RULES,
        block="`cairn_validate`'s `record density` advisory",
    ),
    # M101 (D-058): the whole-file axis's decommissioning is itself a rule —
    # stated as the retirement sentence, which is the positive framing the
    # no-threshold negative asserts pair with (guard-doctrine §3).
    Mutation(
        guard="test_record_density",
        test="TestRecordDensityRule.test_rule_states_no_whole_file_threshold",
        target=RULES,
        block="D-058 retired it",
    ),
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
    Mutation(
        guard="test_narration_discipline",
        test="TestNarrationDisciplineRule.test_rule_present_with_deliberation_bar",
        target=RULES,
        block="never a running readout of reasoning",
    ),
    Mutation(
        guard="test_narration_discipline",
        test="TestNarrationDisciplineRule.test_preview_carveout",
        target=RULES,
        block="This never licenses compressing mandated substance",
    ),
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
        test="TestModuleExtraction.test_rulebook_states_the_module_norm",
        target=RULES,
        block="gets a module, not a rulebook",
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
    Mutation(
        guard="test_phase_header_levels",
        test="TestPhaseHeaderLevels.test_rulebook_declares_h1_unit_h2_phase",
        target=RULES,
        block="A `#` names the unit of work",
    ),
    # M57: the two references/ page types + the page⇒INDEX-line rule. One
    # Mutation entry per positive assertIn (M53 discipline).
    Mutation(
        guard="test_references_pages",
        test="TestReferencesPages.test_file_map_names_both_page_types",
        target=RULES,
        block="Source notes (`<citekey>.md`), synthesis notes",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestReferencesPages.test_ingestion_defines_synthesis_notes",
        target=RULES,
        block="the second committed `references/` page type",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestReferencesPages.test_every_committed_page_carries_an_index_line",
        target=RULES,
        block="Every committed `references/` page carries its",
    ),
    # M80: the authoring trigger — WHEN a page is owed — lives in core, not in
    # the numeric-gated module (LESSONS :49). One entry per positive assertIn;
    # the absence-assert on the module has no entry, since blanking cannot
    # restore an absence (M54) — its positive twin below is what locks it.
    Mutation(
        guard="test_references_pages",
        test="TestAuthoringTrigger.test_core_states_when_a_source_owes_a_page",
        target=RULES,
        block="A page is owed once the repo *relies* on the source",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestAuthoringTrigger.test_core_states_when_analysis_earns_a_synthesis_note",
        target=RULES,
        block="an analysis that will outlive its milestone",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestAuthoringTrigger.test_core_names_both_shipped_templates",
        target=RULES,
        block="Author from the shipped templates:",
    ),
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
        test="TestExploratorySources.test_exploration_is_named_a_legitimate_activity",
        target=RULES,
        block="is supply-push exploration, a legitimate activity",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestExploratorySources.test_exploration_always_produces_candidate_rows",
        target=RULES,
        block="It always produces ROADMAP candidate rows for the promising oracles or methods it finds",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestExploratorySources.test_survey_note_only_when_it_outlives_the_exploration",
        target=RULES,
        block="committed survey synthesis note only when the triage will outlive its exploration",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestExploratorySources.test_per_source_pages_stay_demand_pull",
        target=RULES,
        block="withholds a per-source `<citekey>.md` page: those stay demand-pull, earned only once a candidate graduates",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestExploratorySources.test_exploration_restates_the_m56_guardrail",
        target=RULES,
        block="no committed raw sources, no references log, no query op or graph tooling",
    ),
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
    Mutation(
        guard="test_source_note_template",
        test="TestClaimSplitDoctrine.test_standing_fact_label_carries_its_members",
        target=RULES,
        block="A **standing fact** is a claim about the *source*: an extracted value, a printed formula, a verbatim wording, a page or table anchor.",
    ),
    Mutation(
        guard="test_source_note_template",
        test="TestClaimSplitDoctrine.test_dated_observation_label_carries_its_members",
        target=RULES,
        block="A **dated observation** is a claim about the *repo's own state*: what is on the shelf, what has or has not been read, what another page does or does not yet say, what a later task must still check.",
    ),
    Mutation(
        guard="test_source_note_template",
        test="TestClaimSplitDoctrine.test_undated_absence_claim_is_named_as_the_failure",
        target=RULES,
        block="undated absence claim",
    ),
    # M81: the re-verification expectation and its recording location. Two
    # entries, because the expectation without the location reads as satisfied
    # by the central ledger M56 rejected.
    Mutation(
        guard="test_references_pages",
        test="TestReVerification.test_core_states_the_re_verification_expectation",
        target=RULES,
        block="a page the repo still relies on is re-checked against its source as it gets old, and a page never checked against its source at all keeps saying so.",
    ),
    Mutation(
        guard="test_references_pages",
        test="TestReVerification.test_a_re_check_marks_inline_and_nowhere_else",
        target=RULES,
        block="A re-check marks inline in the provenance block, on the extraction status itself — never in a new file, a new section, or a log.",
    ),
    Mutation(
        guard="test_source_note_template",
        test="TestClaimSplitDoctrine.test_provenance_block_is_prose_not_frontmatter",
        target=RULES,
        block="The block is prose in the page's own idiom, not frontmatter.",
    ),
    Mutation(
        guard="test_source_note_template",
        test="TestClaimSplitDoctrine.test_extraction_status_must_carry_its_own_date",
        target=RULES,
        block="an extraction status carries its own",
    ),
    Mutation(
        guard="test_source_note_template",
        test="TestClaimSplitDoctrine.test_module_defers_the_universal_rules_to_the_rulebook",
        target="skills/shared/validation-doctrine.md",
        block='are universal file-family rules and live in tracking-rules',
    ),
    Mutation(
        guard="test_review_fanout",
        test="TestReviewFanout.test_fanout_states_why_a_fresh_model_reviews",
        target=RULES,
        block="fresh-context subagents",
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
    Mutation(
        guard="test_rulebook_polish",
        test="TestRulebookPolish.test_copy_run_commands_get_their_own_fenced_block",
        target=RULES,
        block="Handing the user a command to run → its own fenced code block",
    ),
    # M86 (D-048): the three handoff steps each carry the directive
    # independently — one skill losing it must not be masked by the other two.
    Mutation(
        guard="test_copy_run_handoffs",
        test="TestReviewCloseIsAHandoff.test_close_directs_the_commands_into_a_fenced_block",
        target=REVIEW,
        block="emit the commands in a fenced block, never inline backticks",
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
        test="TestChangelogSlot.test_rulebook_states_the_none_semantics",
        target=RULES,
        block='"none" is legal — hotfix skips the changelog entry',
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
        guard="test_git_safety_hooks",
        test="TestForcePushLine.test_never_force_push_names_its_mechanical_backing",
        target=RULES,
        block="force_push_guard hook mechanically denies",
    ),
    Mutation(
        guard="test_git_safety_hooks",
        test="TestForcePushLine.test_feature_branches_stay_unblocked",
        target=RULES,
        block="(feature branches are not blocked)",
    ),
    Mutation(
        guard="test_git_safety_hooks",
        test="TestMarkerRestoreLifecycle.test_marker_paragraph_records_the_restore",
        target=RULES,
        block="restored automatically (merge_guard_post)",
    ),
    Mutation(
        guard="test_git_safety_hooks",
        test="TestMarkerRestoreLifecycle.test_single_use_semantics_survive",
        target=RULES,
        block="survives failed retries but never a successful merge",
    ),
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
        test="TestDurableRecordPreviewRule.test_rule_present_with_mechanic",
        target=RULES,
        block="Newly authored durable-record text",
    ),
    Mutation(
        guard="test_durable_record_preview",
        test="TestDurableRecordPreviewRule.test_rule_present_with_mechanic",
        target=RULES,
        block="is shown verbatim in chat immediately before",
    ),
    Mutation(
        guard="test_durable_record_preview",
        test="TestDurableRecordPreviewRule.test_rule_names_the_covered_record_types",
        target=RULES,
        block="a LESSONS line, an archive summary, a ROADMAP",
    ),
    Mutation(
        guard="test_durable_record_preview",
        test="TestDurableRecordPreviewRule.test_rule_names_the_exemptions",
        target=RULES,
        block="noise: work-log one-liners, checkbox ticks, status-mirror updates",
    ),
    Mutation(
        guard="test_durable_record_preview",
        test="TestDurableRecordPreviewRule.test_deltas_not_dumps_names_the_carve_out",
        target=RULES,
        block="not a dump — see the Durable-record preview rule below.",
    ),
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
        block="verbatim in chat before its commit (durable-record preview).",
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
        test="TestAcceptanceChipsRule.test_rule_present_with_verbatim_bar",
        target=RULES,
        block="requires that conclusion's substance",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAcceptanceChipsRule.test_rule_present_with_verbatim_bar",
        target=RULES,
        block="verbatim in chat above the chip (D-037): the verdict and each actioned",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAcceptanceChipsRule.test_rule_present_with_verbatim_bar",
        target=RULES,
        block="verbatim plus the file path for the rest; a paraphrase never stands in",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAcceptanceChipsRule.test_chips_carry_choices_rule_present",
        target=RULES,
        block="Chips carry choices, not evidence.** Supporting detail and technical",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAcceptanceChipsRule.test_cross_reference_present",
        target=RULES,
        block="a summary never substitutes for the accepted text.",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAccessibleLanguageRule.test_rule_present_and_scopes_the_decision_surface",
        target=RULES,
        block="Accessible language on the decision surface.",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAccessibleLanguageRule.test_rule_present_and_scopes_the_decision_surface",
        target=RULES,
        block="an AskUserQuestion question's text, the prose framing a",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAccessibleLanguageRule.test_rule_glosses_jargon_and_names_the_failure",
        target=RULES,
        block="A technical term is glossed at first use, never assumed",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAccessibleLanguageRule.test_rule_glosses_jargon_and_names_the_failure",
        target=RULES,
        block="jargon-led framing, where the user must already know the",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAccessibleLanguageRule.test_rule_reconciles_with_chips_carry_choices",
        target=RULES,
        block="leads with its plain-language meaning rather than standing in for it.",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAccessibleLanguageRule.test_cross_reference_from_chips_carry_choices",
        target=RULES,
        block="the Accessible language rule below carries that plain-language",
    ),
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
        block="conclusion shows its substance verbatim above the chip.",
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
        block="the RR's conclusions/verdict section is shown verbatim above the chip.",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestPerSkillDirectives.test_milestone_route_triage",
        target="skills/milestone/SKILL.md",
        block="Acceptance chips (tracking-rules): a triage option that accepts an audit",
    ),
    Mutation(
        guard="test_gate_conclusion_preview",
        test="TestAcceptanceChipsRule.test_enumeration_names_proposals",
        target=RULES,
        block="a proposed disposition or action plan awaiting confirmation (D-038)",
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
        block="verbatim in chat above the merge-approval chip — the PR description",
    ),
    # M72 (D-043): the boundary passage and the PR binding each carry a
    # distinct rule, and the README half is a separate target — one entry
    # per positive assert's block, per the M53 per-block discipline.
    Mutation(
        guard="test_collaboration_boundary",
        test="TestEnforcementBoundary.test_rulebook_states_the_boundary",
        target=RULES,
        block="Enforcement boundary — what survives a merge made outside a cairn session.",
    ),
    Mutation(
        guard="test_collaboration_boundary",
        test="TestEnforcementBoundary.test_boundary_names_the_paths_that_escape_the_guards",
        target=RULES,
        block="or by a contributor without the plugin installed is invisible to",
    ),
    Mutation(
        guard="test_collaboration_boundary",
        test="TestEnforcementBoundary.test_boundary_states_the_single_operator_assumption",
        target=RULES,
        block="governed by that operator's session, never the contributor's.",
    ),
    Mutation(
        guard="test_collaboration_boundary",
        test="TestPRBinding.test_rulebook_states_the_binding",
        target=RULES,
        block="the guard refuses a `gh pr merge` whose PR the marker does not name",
    ),
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
        test="TestAdoptionPath.test_rulebook_carries_the_same_exemption",
        target=RULES,
        block="**An adopted external PR is the exception:**",
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
    Mutation(
        guard="test_external_pr_intake",
        test="TestIntakeRouting.test_leave_never_absorbs_a_genuinely_new_item",
        target=RULES,
        block="never anything genuinely new (D-044)",
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
        test="TestDeprecationMigration.test_closing_check_does_not_claim_to_verify_the_directory",
        target="skills/cairn-init/SKILL.md",
        block="**A quiet advisory confirms the entry, not the directory** — `check_gitignore_deprecations` reads `.gitignore` alone and never the filesystem,",
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
    Mutation(
        guard="test_hygiene_stamp",
        test="TestHygieneStampRule.test_rule_pairs_the_stamp_with_the_replace_operation",
        target=RULES,
        block="**The `Last hygiene check` stamp is replaced each pass, never appended to** — it records the CURRENT check only, and no `Prior:` or `Earlier:` chain accumulates behind it.",
    ),
    Mutation(
        guard="test_hygiene_stamp",
        test="TestHygieneStampRule.test_narrowing_is_stated_as_non_item_only",
        target=RULES,
        block="**The per-line axis covers non-item lines only, and deliberately never item lines** (D-052, narrowing M84's blanket rejection).",
    ),
    Mutation(
        guard="test_hygiene_stamp",
        test="TestStampWriteSites.test_milestone_audit_says_replace",
        target="skills/milestone/SKILL.md",
        block="overwrite the previous text, never append to it and never demote it to a `Prior:` or `Earlier:` clause.",
    ),
    Mutation(
        guard="test_hygiene_stamp",
        test="TestStampWriteSites.test_post_merge_hygiene_says_replace",
        target="skills/milestone-review/SKILL.md",
        block="overwrite the previous text, never append to it and never demote it to a `Prior:` clause (D-052)",
    ),
    Mutation(
        guard="test_hygiene_stamp",
        test="TestStampWriteSites.test_shipped_skeleton_teaches_the_shape",
        target="skills/cairn-init/SKILL.md",
        block="(one short line, replaced each pass — never appended to; D-052)",
    ),
    # M98 (D-055): maturation is the third outflow, and the graduated family
    # moved to a new module. Entries span all three surfaces the guard pins —
    # the module itself, the rulebook pointer, and the retirement rule — one
    # per positive assert (M53 discipline).
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_anchor_section_states_the_one_physical_line_rule",
        target=GUARD_DOCTRINE,
        block="pin the label\ntogether with its members on one physical line",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_harness_section_states_registration_is_per_file",
        target=GUARD_DOCTRINE,
        block="**Registration is per file (≥1 exemplar block), never per assertion.**",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_absence_section_states_the_vacuous_crash_rule",
        target=GUARD_DOCTRINE,
        block="A guard whose only assertion is an `assertNotIn` is vacuous against a\ncrash.",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_fixture_section_states_the_vary_every_axis_rule",
        target=GUARD_DOCTRINE,
        block="**Vary every axis the prose is free in, and vary it where the value under\ntest lives.**",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_sweep_section_states_the_exclusion_list_rule",
        target=GUARD_DOCTRINE,
        block="An exclusion list may name only history files",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestRulebookPointer.test_rulebook_points_at_the_module",
        target=RULES,
        block="The craft of making a guard falsifiable lives in a module of this rulebook",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestThirdOutflow.test_rulebook_counts_three_retirement_criteria",
        target=RULES,
        block="Three criteria retire a lesson (D-051, D-055)",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestThirdOutflow.test_rulebook_names_maturation_with_its_mechanism_on_one_line",
        target=RULES,
        block="**maturation — a stabilized family graduates whole into a doctrine module**",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestThirdOutflow.test_rulebook_distinguishes_maturation_from_the_rejected_second_record",
        target=RULES,
        block="the source line is deleted in the same pass, so exactly one record exists at every moment",
    ),
    # M99. Four blocks across four targets, because the budget wiring fails in
    # four independent ways: the budgets could stop reading as guidance and
    # become a second cap (the shape D-030 declined); the archive template could
    # stop being named as the summary's source; and either drafting step could
    # lose its handed-over command while the other kept one.
    Mutation(
        guard="test_budget_first_drafting",
        test="TestMilestoneTemplateBudgets.test_the_budgets_are_marked_guidance_rather_than_a_gate",
        target=TEMPLATE,
        block="DRAFTING BUDGETS (M99) — guidance, not a gate; the only size check that",
    ),
    # M118/D-074: the reserve became an exemption; the spend-none instruction
    # survived it. Registered now that the assert has been re-anchored.
    Mutation(
        guard="test_budget_first_drafting",
        test="TestMilestoneTemplateBudgets.test_the_decisions_section_is_named_cap_exempt_and_not_plan_s_to_spend",
        target=TEMPLATE,
        block="## Decisions reserves nothing: D-074 made it cap-exempt, so it costs the",
    ),
    Mutation(
        guard="test_budget_first_drafting",
        test="TestMilestoneTemplateBudgets.test_the_decisions_section_is_named_cap_exempt_and_not_plan_s_to_spend",
        target=TEMPLATE,
        block="budget nothing and plan still spends none of it.",
    ),
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
    Mutation(
        guard="test_budget_first_drafting",
        test="TestDraftingStepsHandOverTheCounter.test_plan_step_4_fences_the_counter_command",
        target="skills/milestone-plan/SKILL.md",
        block='python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_budget.py"',
    ),
    # M108 (D-060): the always-read governance frame. Each of the three
    # element labels, the completeness-only boundary, each worked table row,
    # and the two audit-bullet asserts carries the frame independently, so
    # each gets its own mutation proof. M113 (D-063) adds the fifth row and
    # the two claims that distinguish it.
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_names_inflow_test_element",
        target=RULES,
        block="- **Inflow test** — what content belongs in the file.",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_names_outflow_or_read_bound_element",
        target=RULES,
        block="- **Outflow or read-bound** — how content leaves, or, where it may not leave,",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_names_attention_signal_element",
        target=RULES,
        block="- **Attention signal** — what reports growth so a human notices.",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_frame_is_completeness_only",
        target=RULES,
        block="never measures or gates a file's mass (size governance is closed — D-057).",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_enumerates_the_always_read_files_with_their_elements",
        target=RULES,
        block="| `ROADMAP.md` | a milestone or candidate | terminal-row retention + candidate triage/graduation | 60-line item cap |",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_enumerates_the_always_read_files_with_their_elements",
        target=RULES,
        block="| `LESSONS.md` | a durable \"how this repo behaves\" note | retire by enforcement / ownership / maturation (D-051, D-055) | 50-line item cap + `record density` |",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_enumerates_the_always_read_files_with_their_elements",
        target=RULES,
        block="| `tracking-rules.md` | the placement steps under \"What gets a test\" (D-071) | editorial pass; growth governed at the door (D-057) | `/milestone` audit mass+growth line |",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_enumerates_the_always_read_files_with_their_elements",
        target=RULES,
        block="| `DECISIONS.md` | a cross-cutting choice among alternatives | bounded heading read — history read less, never shrunk (D-054) | none needed once read-bounded |",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_enumerates_the_always_read_files_with_their_elements",
        target=RULES,
        block="| the active `milestones/M<NN>-<slug>.md` | the milestone-file section ownership table | capped sections: the 150-line plan-owned cap; cap-exempt sections: newest-content injection — history read less, never shrunk (D-063); the file leaves the set at `done` | `weight caps` CHECK + `work-log format` + `decisions format`; none needed for the cap-exempt sections once read-bounded |",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_names_the_surface_that_leaves_the_always_read_set",
        target=RULES,
        block="It is **the only always-read surface that leaves the set**: a milestone stops",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameRulebook.test_names_the_split_across_two_gp1_mechanisms",
        target=RULES,
        block="only one split across two of GP1's mechanisms within one file** — its",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameAudit.test_audit_applies_the_frame",
        target=MILESTONE,
        block="- **Always-read governance (frame completeness):** apply the rulebook's",
    ),
    Mutation(
        guard="test_always_read_frame",
        test="TestAlwaysReadFrameAudit.test_audit_reports_never_fixes",
        target=MILESTONE,
        block="a judgment for the user — never auto-fixed, never a `FAIL`, the form of the",
    ),
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
    Mutation(
        guard="test_fable_gate_retained",
        test="TestPerInstanceApprovalGate.test_rulebook_gates_fable_per_instance",
        target=RULES,
        block="only after a per-instance approval gate",
    ),
    Mutation(
        guard="test_fable_gate_retained",
        test="TestRbRrOnlyPath.test_rulebook_keeps_rbrr_only_path",
        target=RULES,
        block="only through the RB/RR brief protocol",
    ),
    Mutation(
        guard="test_fable_gate_retained",
        test="TestRbRrOnlyPath.test_rulebook_keeps_rbrr_only_path",
        target=RULES,
        block="Ad-hoc Fable spawning is still prohibited",
    ),
    Mutation(
        guard="test_fable_gate_retained",
        test="TestRbRrOnlyPath.test_lowered_bar_stays_gated_not_a_standing_menu",
        target=RULES,
        block="never a standing menu item",
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
        test="TestPlanGateCriteriaAudit.test_audit_block_is_present_and_precedes_the_questions",
        target="skills/milestone-plan/SKILL.md",
        block="**Criteria audit (runs before the questions are composed).**",
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
        test="TestPlanGateCriteriaAudit.test_step_4_writes_the_audited_wording_and_reaudits_a_change",
        target="skills/milestone-plan/SKILL.md",
        block="**Write the wording\n     step 3's audit read**; a criterion the gate changed goes back through the\n     audit's two questions",
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
        test="TestRRIngestionCriteriaAudit.test_ingest_audit_states_both_questions_at_this_surface",
        target=BRIEF,
        block="and the same\n   two questions — *what state of the world satisfies this exactly as\n   written*, and *does any IP or D-entry make that state unreachable*",
    ),
    # M115: description-layer certification. §8's diagnosis and its remedy
    # are pinned separately, and each of the three checks separately again —
    # a reader told to certify with one check missing certifies less, and a
    # diagnosis with no remedy is what let one defect class recur for passes.
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_exists_under_its_own_heading",
        target=GUARD_DOCTRINE,
        block="## 8. The author never certifies its own guard's coverage",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_separates_operation_from_certification",
        target=GUARD_DOCTRINE,
        block="**Running a guard and certifying that it covers what you claim are different\njobs, and only the first one survives being done by its author.**",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_states_the_diagnosis",
        target=GUARD_DOCTRINE,
        block="the author checks the description against its generative\nmodel of the artifact rather than against the artifact",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_places_the_step_before_review_with_a_fresh_reader",
        target=GUARD_DOCTRINE,
        block="**So before `status -> review`, a guard-authoring milestone hands the\ndescription layer to a fresh-context [O] reader that authored no part of it.**",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_names_the_coverage_check",
        target=GUARD_DOCTRINE,
        block="**AC-clause-to-assert coverage** — every clause of every acceptance\n  criterion maps to an assert that actually pins it",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_names_the_claim_accuracy_check",
        target=GUARD_DOCTRINE,
        block="**Claim-vs-file accuracy** — every docstring, comment, work-log line, and\n  record claim about the guard is true of the file it describes",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_names_the_anchor_fidelity_check",
        target=GUARD_DOCTRINE,
        block="**Anchor-vs-shipped-bytes fidelity** — every multi-word anchor matches the\n  bytes actually shipped",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_requires_zero_unresolved_and_forbids_arguing_down",
        target=GUARD_DOCTRINE,
        block="The gate is entered at zero unresolved: every discrepancy is fixed, never\nargued down as imprecision",
    ),
    # M121 (narrows D-067, first instrument). Three entries across two files:
    # the record requirement, the sentence making a missing line evidence, and
    # the ingest surface's cross-reference to the one home that states it.
    Mutation(
        guard="test_fresh_context_readers",
        test="TestPlanGateCriteriaAudit.test_audit_records_a_work_log_line_even_when_it_finds_nothing",
        target="skills/milestone-plan/SKILL.md",
        block="**The audit records one work-log line either way** — what it returned, or\n   that it returned nothing",
    ),
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
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_moves_certification_not_operation",
        target=GUARD_DOCTRINE,
        block="The author still runs everything —\nthis moves certification, not operation",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_carries_its_own_falsifier",
        target=GUARD_DOCTRINE,
        block="**This step carries its own falsifier.** It counts yield and not\nrounds, because the round count is precisely what the two rules above change,\nand a measure its own subject can satisfy by construction measures nothing.",
    ),
    # M116 (D-069). Two entries: the exclusion itself, and the reason it is a
    # convergence fix. Losing the second leaves the clause readable as a
    # comfort measure, which invites tuning the round count — the move D-059
    # exists to forbid.
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_reader_checks_three_things_and_reports_verbatim",
        target=GUARD_DOCTRINE,
        block="The reader checks three things and reports discrepancies verbatim:",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_section_bounds_the_certified_scope_against_regress",
        target=GUARD_DOCTRINE,
        block="**The certified scope is the work and the records describing the work; a record\nwhose subject is a certification round itself — the final round's own report\nincluded — sits outside it** (D-069)",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_scope_bound_states_why_it_is_convergence_not_convenience",
        target=GUARD_DOCTRINE,
        block="the gate cannot converge\nrather than merely being hard to reach",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_checked_and_fixed_is_drawn_by_subject_matter",
        target=GUARD_DOCTRINE,
        block='**What the reader checks and the author fixes** is drawn\nby *subject matter*: the work and every record about the work are inside,\nnarrative about the certifying process is outside (D-069, as narrowed by\nD-070).',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_fix_authored_record_names_the_four_record_kinds",
        target=GUARD_DOCTRINE,
        block="A fix-authored record is a docstring, a comment, a work-log line, or a record\nclaim that a previous round's own fix wrote in this same certification.",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_class_has_exactly_one_name",
        target=GUARD_DOCTRINE,
        block='That\nname is the only one this section gives the class, and where it means anything\nwider it says so',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_fix_code_and_original_records_stay_round_opening",
        target=GUARD_DOCTRINE,
        block="A fix's code, its asserts and its fixtures\nare not records and stay ordinary round-opening surface; so does every record\nthat existed before round 1",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_an_original_false_claim_still_reopens",
        target=GUARD_DOCTRINE,
        block='a false claim in an original docstring is\nthe defect this section was built on and it reopens a round no matter who\nwrote it',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_mandate_boundary_limits_reopening_to_the_three_checks",
        target=GUARD_DOCTRINE,
        block='**A round reopens only on a finding within the three named checks above.**',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_out_of_mandate_observations_route_to_sections_one_to_seven",
        target=GUARD_DOCTRINE,
        block='is real work, and it is recorded and fixed as ordinary\nmilestone work under §§1–7 and the mutation harness. It does not reopen\ncertification',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_a_finding_reopens_only_if_it_clears_both_lines",
        target=GUARD_DOCTRINE,
        block='**A finding reopens a round only if it clears both lines** — it falls within\nthe three checks, and its only subject is not a fix-authored record',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_each_class_carries_exactly_one_confirmation_obligation",
        target=GUARD_DOCTRINE,
        block='**Each class carries exactly one confirmation obligation, and no class carries\ntwo.**',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_no_confirmation_obligation_falls_on_the_author",
        target=GUARD_DOCTRINE,
        block="no confirmation\nobligation falls on the author, because D-067 rejected instructing an author's\nown re-check",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_falsifier_counts_where_a_finding_was_found",
        target=GUARD_DOCTRINE,
        block='A finding\n  counts where it was **found**, never where it was fixed, so routing one to\n  §§1–7 does not remove it from the count',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_falsifier_window_carries_a_non_vacuity_floor",
        target=GUARD_DOCTRINE,
        block='the window counts only if at least one of its three milestones convened a\n  round after its first — a window that never ran a later round has not measured\n  one',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_falsifier_second_clause_counts_in_place_fixes_found_false",
        target=GUARD_DOCTRINE,
        block='If any fix-authored record corrected in place is later found false —\n  by the three-lens review, or by a subsequent milestone — then the in-place\n  route has failed, and that class returns to round-opening',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_evidence_states_the_provenance_rule_saves_no_rounds",
        target=GUARD_DOCTRINE,
        block="On M119's record the provenance rule alone changes the round count by **zero**",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_gate_is_reachable_with_records_not_yet_confirmed",
        target=GUARD_DOCTRINE,
        block='The gate is therefore reachable with fix-authored records corrected but not yet\nindependently confirmed',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_evidence_is_grounded_on_record_churn",
        target=GUARD_DOCTRINE,
        block="**What grounds the provenance rule is record churn, not M119's round count.**",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_provenance_rule_does_not_narrow_the_certified_scope",
        target=GUARD_DOCTRINE,
        block='**being a fix-authored record never removes it from the\ncertified scope**, which D-069 draws on subject matter alone',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_out_of_mandate_findings_do_not_hold_the_gate",
        target=GUARD_DOCTRINE,
        block='**and it does not hold the gate**: the zero-unresolved bar is met\nwhen every discrepancy has been fixed under the obligation its own class\ncarries',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_out_of_mandate_class_is_enumerated",
        target=GUARD_DOCTRINE,
        block="a surviving mutation, a one-directional\npin, a near-miss control's uncovered signature, a fixture weak on an axis no\ncriterion names",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_three_checks_are_the_whole_mandate",
        target=GUARD_DOCTRINE,
        block="Those three are the whole of this step's mandate.",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_a_reopening_finding_obliges_a_further_round",
        target=GUARD_DOCTRINE,
        block='A **reopening finding** obliges a further fresh-context round, and that\nround is what confirms its fix.',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_a_fix_authored_record_is_confirmed_by_reader_or_review",
        target=GUARD_DOCTRINE,
        block="A **fix-authored record** is fixed in place and\nconfirmed by the next round's reader where a further round occurs, and otherwise\nby `/milestone-review`'s three-lens fan-out at the merge gate",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_an_out_of_mandate_observation_is_confirmed_by_operation",
        target=GUARD_DOCTRINE,
        block='An **out-of-mandate robustness observation** is\nconfirmed by operation: the harness, the sweeps and the suite',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_falsifier_names_its_window",
        target=GUARD_DOCTRINE,
        block='Measured over the next three guard-authoring milestones that run §8, the window\nclosing when the third completes',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_falsifier_names_both_counted_quantities_and_clause_i_consequence",
        target=GUARD_DOCTRINE,
        block='zero shipped-behaviour defects and zero findings whose subject is\n  pre-round-1 surface, then the rounds after the first have stopped earning\n  their cost — retire them and run §8 as a single certification pass',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_falsifier_carries_both_tolerances",
        target=GUARD_DOCTRINE,
        block='Tolerance: exact zero on both counts,',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_clause_two_carries_its_tolerance",
        target=GUARD_DOCTRINE,
        block='Tolerance: one\n  occurrence.',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_reopening_is_drawn_by_provenance",
        target=GUARD_DOCTRINE,
        block='**What a finding reopens** is drawn by *provenance*: a finding whose\nonly subject is a **fix-authored record** is not grounds for a further round.',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_provenance_rule_is_a_shield_and_not_a_licence",
        target=GUARD_DOCTRINE,
        block='That is\na shield and never a licence — it says which findings cannot reopen a round, and\nnever that anything else must.',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_shield_costs_only_round_opening_power",
        target=GUARD_DOCTRINE,
        block='What it loses is\nonly the power to force another round, and never the reading and correcting\nitself.',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_forward_reference_states_the_rule_it_points_at",
        target=GUARD_DOCTRINE,
        block='the classes are set out below — each carries exactly\none, and none carries two.',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_compatibility_with_d070_is_stated",
        target=GUARD_DOCTRINE,
        block='D-070 rules on the first axis and says nothing about the second, which is\nwhy this is compatible with it rather than a partial supersession of it.',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_clearing_both_lines_is_sufficient_to_reopen",
        target=GUARD_DOCTRINE,
        block="**And a finding that clears both lines is a reopening finding**, carrying that\nclass's obligation: a further fresh-context round.",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_reopening_rule_runs_in_both_directions",
        target=GUARD_DOCTRINE,
        block='Stated as a bound alone it\nsays only which findings cannot reopen a round and never that any must',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_falsifier_carries_a_whole_step_retirement_clause",
        target=GUARD_DOCTRINE,
        block='then round 1 has stopped earning its reader and\n  **the step retires whole**',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_clause_three_counts_anchor_fidelity_findings",
        target=GUARD_DOCTRINE,
        block='and\n  zero anchor-fidelity findings',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_clause_three_names_its_first_three_counted_quantities",
        target=GUARD_DOCTRINE,
        block="returns zero\n  shipped-behaviour defects, zero false claims in records predating that\n  milestone's round 1, zero acceptance-criterion clauses found unpinned, and",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_clause_three_is_totalled_across_the_window",
        target=GUARD_DOCTRINE,
        block='If, totalled across the same window, **round 1 itself**',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_clause_three_carries_its_tolerance",
        target=GUARD_DOCTRINE,
        block='Tolerance: exact zero on all four counts, totalled\n  across the window',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_the_overlap_is_settled_by_definition_without_a_tie_break",
        target=GUARD_DOCTRINE,
        block='The definition settles the apparent overlap without a\ntie-break: a one-directional pin that leaves an acceptance-criterion clause\nunpinned is a check-1 finding and reopens, while one that merely hardens an\nassert no criterion names is out of mandate.',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_what_decides_the_overlap_is_the_criterion_clause_at_stake",
        target=GUARD_DOCTRINE,
        block='What decides is whether a criterion\nclause is at stake, never how the finding is phrased.',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestDescriptionLayerCertification.test_clauses_one_and_three_cannot_both_fire",
        target=GUARD_DOCTRINE,
        block='Clauses (i) and\n  (iii) cannot both fire: (i)\n  requires some milestone to have convened a later round',
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestImplementRoutesToCertification.test_completion_step_routes_to_the_certifier_at_zero_unresolved",
        target=IMPLEMENT,
        block="if this milestone authored or edited a\n   prose-guard, hand its description layer to a fresh-context [O] reader first",
    ),
    Mutation(
        guard="test_fresh_context_readers",
        test="TestImplementRoutesToCertification.test_completion_step_cites_the_doctrine_section_and_the_bar",
        target=IMPLEMENT,
        block="`skills/shared/guard-doctrine.md` §8, the author never certifies its own\n   guard's coverage — and enter the gate only at zero unresolved",
    ),
]

# Prose-guard files deliberately NOT in the registry, each with a reason. The
# completeness check (below) treats these as covered.
EXEMPT = {
    "test_mutation_harness": "the harness's own tests, not a prose-guard",
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
        test="TestPlacementTest.test_rulebook_states_the_deletion_retention_test",
        target=RULES,
        block="**A rule is what changes compliant behavior when it is deleted.**",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestPlacementTest.test_rulebook_names_deletion_as_the_only_retention_probe",
        target=RULES,
        block="Deletion is the retention probe and the only\none: inversion detects rule-shaped text, which a duplicate equally is",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestPlacementTest.test_step_zero_requires_a_single_home",
        target=RULES,
        block="One site\nkeeps the statement; every other site carries at most a cross-reference.",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestPlacementTest.test_step_zero_binds_forward_only",
        target=RULES,
        block="binding on text authored or edited from here on, and never\na mandate to sweep the file",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestPlacementTest.test_step_zero_requires_a_single_home",
        target=RULES,
        block="**Step 0 — one home.** Before asking whether a piece of prose belongs in this\nrulebook, ask whether the rulebook already says it somewhere else.",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestPlacementTest.test_inversion_is_assigned_to_guard_verification",
        target=RULES,
        block="Relabel, negate, or transpose the rule in\nplace, run the suite, require red, restore and diff",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestPlacementTest.test_inversion_is_assigned_to_guard_verification",
        target=RULES,
        block="that is the\nguard-verification protocol",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestPlacedWhereItsConsumersRead.test_inflow_cell_points_at_the_test_without_restating_it",
        target=RULES,
        block="| `tracking-rules.md` | the placement steps under \"What gets a test\" (D-071) |",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestPlacementTest.test_rulebook_covers_the_unguarded_case",
        target=RULES,
        block="still needs its own entry or the by-hand\ncheck",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestReddeningAsymmetry.test_rulebook_states_the_screen_not_licence_rule",
        target=RULES,
        block="**Guard-reddening is a deletion screen, never a licence to keep**",
    ),
    Mutation(
        guard="test_rule_placement",
        test="TestReddeningAsymmetry.test_rulebook_states_the_ownership_direction",
        target=RULES,
        block="The text owns\nthe guard, not the reverse",
    ),
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
    Mutation(
        guard="test_bounded_decisions_read",
        test="TestRulebookStatesTheBoundedRead."
             "test_matched_entry_is_read_whole_before_surfacing",
        target=RULES,
        block="**A matched heading's entry is read whole before anything is "
              "surfaced.**",
    ),
    Mutation(
        guard="test_bounded_decisions_read",
        test="TestRulebookStatesTheBoundedRead."
             "test_match_is_back_referenced_by_its_own_id",
        target=RULES,
        block="**A match is back-referenced — its own `D-0NN` id searched "
              "across the file**",
    ),
    Mutation(
        guard="test_bounded_decisions_read",
        test="TestRulebookStatesTheBoundedRead."
             "test_collision_is_quoted_from_the_full_entry_not_the_heading",
        target=RULES,
        block="**A collision is quoted verbatim from the full entry, never "
              "from the heading.**",
    ),
    Mutation(
        guard="test_bounded_decisions_read",
        test="TestRulebookStatesTheBoundedRead."
             "test_heading_quality_rule_pins_subject_and_relationships",
        target=RULES,
        block="**A `### D-` heading names its subject and any entry it "
              "supersedes, annotates, or narrows.**",
    ),
    # M101 (D-059): the advisory is retired; the rule's enforcement sentence
    # now states conduct + back-reference. The retirement statement is the
    # positive framing its assertNotIn pairs with (guard-doctrine §3).
    Mutation(
        guard="test_bounded_decisions_read",
        test="TestRulebookStatesTheBoundedRead."
             "test_heading_rule_is_conduct_with_no_machine_check",
        target=RULES,
        block="retired as measured not to work",
    ),
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
             "test_third_return_is_a_trigger_and_recommends_replan_or_split",
        target=REVIEW,
        block="**(a) The third return, and every return after it**",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers."
             "test_third_return_is_a_trigger_and_recommends_replan_or_split",
        target=REVIEW,
        block="Do not queue another retry; recommend re-plan or split via\n     `/milestone-plan`.",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestThrashTriggers."
             "test_third_return_is_a_trigger_and_recommends_replan_or_split",
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
        test="TestTriggersCompose.test_composition_carries_b_into_the_routing",
        target=REVIEW,
        block="escalation offer carry INTO that routing rather than being discarded",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_composition_names_the_routing_target",
        target=REVIEW,
        block="and the milestone routes through\n   `/milestone-plan` —",
    ),
    Mutation(
        guard="test_thrash_rule",
        test="TestTriggersCompose.test_exhaustion_branch_states_its_composed_remedy",
        target=REVIEW,
        block="Compose the routing chip from an offered\n   `/milestone-brief` escalation, "
              "parking as `blocked` with the blocker named\n   in a work-log line, or "
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
        block="the remedy is no longer re-plan-or-split",
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

# M114: falsifying promotion conditions. Three entries because the heading,
# the positive form, and the prohibition fail independently — drop only the
# prohibition and the rule still reads as a preference that a count satisfies,
# which is the wording that cost intraclass M93 four review returns.
REGISTRY += [
    Mutation(
        guard="test_search_first_candidates",
        test="TestFalsifyingPromotionConditions."
             "test_rule_requires_a_falsifying_class_not_a_count",
        target=RULES,
        block="**Falsifying promotion conditions.**",
    ),
    Mutation(
        guard="test_search_first_candidates",
        test="TestFalsifyingPromotionConditions."
             "test_rule_requires_a_falsifying_class_not_a_count",
        target=RULES,
        block="the class of evidence that\nwould falsify the chosen approach",
    ),
    Mutation(
        guard="test_search_first_candidates",
        test="TestFalsifyingPromotionConditions."
             "test_rule_requires_a_falsifying_class_not_a_count",
        target=RULES,
        block="never as a count of failures",
    ),
]

# M114: two guard-doctrine additions. Each rule's diagnosis and its remedy fail
# independently, and a diagnosis with no remedy is the shape that let
# intraclass M93 rediscover the same sweep defect on three separate review
# passes. Registration is per block, so these are needed even though
# `test_lesson_graduation` is already a registered FILE (M60/M85). The list is
# the count (§6): the count this comment used to state was correct at four and
# would have been stale at five — the same trap the thrash block earlier in
# this file records falling into at seven entries and again at nine.
REGISTRY += [
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_absence_section_states_the_matcher_rendering_rule",
        target=GUARD_DOCTRINE,
        block="**A detector's matcher must be exercised at every rendering its target can\ntake.**",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_absence_section_states_the_matcher_rendering_rule",
        target=GUARD_DOCTRINE,
        block="Carry the renderings INTO the test as positive\ncontrols: append the real value at full precision, rounded, and `signif`-ed,\nand require the detector to see each one.",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_sweep_section_states_the_silent_cell_rule",
        target=GUARD_DOCTRINE,
        block="**A sweep whose cells may legitimately be silent passes for free on silence.**",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_sweep_section_states_the_silent_cell_rule",
        target=GUARD_DOCTRINE,
        block="Assert per cell that it checked a positive number of things, and assert across\nthe sweep that the positive case fired somewhere, so universal silence cannot\nsatisfy it.",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_sweep_section_states_the_silent_cell_rule",
        target=GUARD_DOCTRINE,
        block=(
            "Stronger still, assert the CONVERSE beside the claim — `named ==\n"
            "usable` rather than `named ⇒ usable` — which turns a silent cell "
            "into an\nassertion that nothing admissible would have worked, "
            "rather than an assertion\nabout nothing."
        ),
    ),
]

# M117: the site axis and the enumeration-count rule, added to the same §3.
# Each paragraph's heading and its operative half fail independently (the site
# paragraph's operative half is a consequence, the count paragraph's is a
# remedy), and both fail independently of the M114 rendering rule above them —
# without that, deleting either one would leave the other satisfying a guard
# that claims to cover both axes.
REGISTRY += [
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_absence_section_states_the_site_axis",
        target=GUARD_DOCTRINE,
        block="**The renderings vary by site as well as by format.**",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_absence_section_states_the_site_axis",
        target=GUARD_DOCTRINE,
        block=(
            "Exercising every number format of\none literal is not coverage "
            "of a surface that has several"
        ),
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_absence_section_states_that_a_count_is_not_coverage",
        target=GUARD_DOCTRINE,
        block="**A count of enumerated entries is not coverage of renderings.**",
    ),
    Mutation(
        guard="test_lesson_graduation",
        test="TestModuleExists.test_absence_section_states_that_a_count_is_not_coverage",
        target=GUARD_DOCTRINE,
        block=(
            "**derive the\nrenderings from the producer rather than listing "
            "them** — sweep the producer's\nown outputs over a grid of inputs "
            "and assert the invariant over what comes back\n(a rendered bullet "
            "contains no number), which covers renderings not yet\nwritten, "
            "with one end-to-end case retained to prove those outputs reach "
            "the\nreal surface unchanged."
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
        test="TestBriefTemplate."
             "test_brief_requests_binding_criteria_as_measurable_assertions",
        target="skills/shared/templates/brief.md",
        block="These are ingested VERBATIM",
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
    Mutation(
        guard="test_finding_enforcement",
        test="TestRulebookSentences.test_script_measurable_preference",
        target=RULES,
        block="**Prefer script-measurable acceptance criteria**",
    ),
    Mutation(
        guard="test_finding_enforcement",
        test="TestRulebookSentences.test_adjudication_asymmetry",
        target=RULES,
        block="The implementing session never authors the durable verdict",
    ),
]

# M107: the amendment paths carry the budget re-check + one-pass-trim rule.
REGISTRY += [
    Mutation(
        guard="test_amendment_budget",
        test="TestBriefIngestRechecksBudget."
             "test_brief_step3_points_at_cairn_budget_and_one_pass_trim",
        target=BRIEF,
        block="re-check the plan-owned body with `cairn_budget`",
    ),
    Mutation(
        guard="test_amendment_budget",
        test="TestImplementAmendmentRechecksBudget."
             "test_step6_points_at_cairn_budget_and_one_pass_trim",
        target=IMPLEMENT,
        block="re-checks the body with `cairn_budget`",
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
        test="TestModuleExists.test_module_declares_itself_a_rulebook_module",
        target=RECORDS_HYGIENE,
        block="a module of `tracking-rules.md`",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestModuleExists.test_module_declares_it_is_read_conditionally",
        target=RECORDS_HYGIENE,
        block="it costs nothing to a session not at such a gate",
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
        test="TestModuleExists.test_section3_rule_home_test",
        target=RECORDS_HYGIENE,
        block="would a repo with NO numeric work need",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestModuleExists.test_section3_run_the_rule_over_your_own_artifacts",
        target=RECORDS_HYGIENE,
        block="runs that rule over the artifacts",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestModuleExists.test_section4_amend_the_ac_without_drift",
        target=RECORDS_HYGIENE,
        block="improves on a planned output token or format, amend the",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestModuleExists.test_section5_scorer_gates_the_actioned_list",
        target=RECORDS_HYGIENE,
        block="sub-threshold confidence score gates the ACTIONED list",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestModuleExists.test_section6_only_a_wrapped_line_lowers_the_count",
        target=RECORDS_HYGIENE,
        block="Only removing a whole *wrapped* physical line lowers a line count.",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestModuleExists.test_section6_compress_what_your_phase_owns",
        target=RECORDS_HYGIENE,
        block="Compress what your phase OWNS, and cross-reference a durable record",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestRulebookPointer.test_rulebook_points_at_the_module",
        target=RULES,
        block="The records-hygiene family graduated by this rule lives in a module of this rulebook",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestRulebookPointer.test_pointer_maps_the_module_to_its_coverage_on_one_physical_line",
        target=RULES,
        block="candidate-row lifecycle, superseding a decision and sweeping the archive",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestRulebookPointer.test_pointer_states_when_to_read_the_module",
        target=RULES,
        block="Read it at a milestone hygiene or plan gate",
    ),
    Mutation(
        guard="test_records_hygiene_graduation",
        test="TestRulebookPointer.test_pointer_states_the_module_is_read_conditionally",
        target=RULES,
        block="a session not at such a gate never pays for it",
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
        test="TestCorrectionNarrationRule.test_rule_states_the_materiality_bar",
        target=RULES,
        block="only when the error would change the user's code, conclusions, or decisions.",
    ),
    Mutation(
        guard="test_narration_discipline",
        test="TestCorrectionNarrationRule.test_rule_requires_plain_correction_then_continue",
        target=RULES,
        block="State the correction plainly and briefly, then continue the task",
    ),
    Mutation(
        guard="test_narration_discipline",
        test="TestCorrectionNarrationRule.test_rule_leaves_an_immaterial_slip_unnarrated",
        target=RULES,
        block="A slip that changes nothing for the user is fixed without narrating it,",
    ),
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
        test="TestDelegationWarrantRule.test_rule_keeps_small_work_inline",
        target=RULES,
        block="in a handful of tool calls is done inline, never delegated",
    ),
    Mutation(
        guard="test_delegation_warrant",
        test="TestDelegationWarrantRule.test_rule_prefers_one_subagent_over_several",
        target=RULES,
        block="spawn one rather than several",
    ),
    Mutation(
        guard="test_delegation_warrant",
        test="TestDelegationWarrantRule.test_rule_reconciles_the_review_fanout",
        target=RULES,
        block="its three reviewers carry distinct evidence bases",
    ),
    # M121. One entry per named class, per AC4. The excluded class is the
    # load-bearing half: the governed class restates the warrant above it,
    # while the exclusion is what stops the guide's third clause from being
    # read onto D-067's fresh-context readers.
    # M121 review pass 2. Two entries for the two rules that inverted with the
    # suite green: the section's lead claim that the warrant reaches one class
    # and not the other, and the measurement motivating the record requirement.
    Mutation(
        guard="test_delegation_warrant",
        test="TestSelfCheckingClassRule.test_rule_states_that_it_reaches_one_class_only",
        target=RULES,
        block="The delegation warrant above\n  reaches one class of checking and not the other",
    ),
    Mutation(
        guard="test_delegation_warrant",
        test="TestSelfCheckingClassRule.test_rule_names_the_governed_class",
        target=RULES,
        block="It governs **an author re-checking work it just produced, in the context that produced it**",
    ),
    Mutation(
        guard="test_delegation_warrant",
        test="TestSelfCheckingClassRule.test_rule_names_the_excluded_class",
        target=RULES,
        block="It does not govern **an independent fresh-context reading of that work by a reader that authored none of it**",
    ),
    # M121 review. Four more entries, from findings the fan-out scored 80+:
    # F-PR1 (the two class asserts stopped at the em-dash, leaving each
    # rationale clause deletable green) and F-B1/F-B2 (the discriminator and
    # the loop-bound sentences inverted with the suite green).
    Mutation(
        guard="test_delegation_warrant",
        test="TestSelfCheckingClassRule.test_governed_class_carries_its_reason",
        target=RULES,
        block="a check already happening unprompted, so instructing it\n  again buys tokens rather than quality",
    ),
    Mutation(
        guard="test_delegation_warrant",
        test="TestSelfCheckingClassRule.test_excluded_class_carries_its_reason",
        target=RULES,
        block="a different instrument against a different failure: an author checks a\n  description against its generative model of the artifact rather than against\n  the artifact",
    ),
    Mutation(
        guard="test_delegation_warrant",
        test="TestSelfCheckingClassRule.test_rule_states_the_discriminator_that_applies_it",
        target=RULES,
        block="The discriminator is *who reads*, never *how often the work is read* — which\n  is the same cut the freshness sentence above makes against the volume test",
    ),
    Mutation(
        guard="test_delegation_warrant",
        test="TestSelfCheckingClassRule.test_rule_leaves_a_fresh_readers_loop_to_its_own_instrument",
        target=RULES,
        block="A fresh reader's own loop is bounded by its instrument, never by this rule",
    ),
]


# M120: the false-positive taxonomy moves out of the reviewers' instruction and
# into the scorer's rubric (D-078). One entry per CONTAINED phrase — a taxonomy
# member, the disposition sentence, and the report-everything instruction.
#
# Deliberately NOT registered: `Score 0-100 your confidence`, the string
# `_scorer_rubric()` uses to locate its slice. Blanking a locator reds the test
# by StopIteration whether or not the taxonomy sits inside the rubric, so it
# would pass identically with the taxonomy moved back upstream — a tautology,
# not coverage. That is LESSONS 2026-07-27 (M117): register the CONTAINED
# phrase, never the bound. The location claim is not mutation-provable at all,
# because the harness blanks and never MOVES (guard-doctrine §2, "Blanking is
# not swapping"); it rests on the slice construction, and inversion — not
# blanking — is what verifies it.
#
# The report-everything entry is the positive framing registered on behalf of
# the paired `assertNotIn`, which is satisfied by blanking and cannot be
# mutation-proven itself (guard-doctrine §3).
REGISTRY += [
    Mutation(
        guard="test_review_fanout",
        test="TestReviewFanout.test_false_positive_taxonomy_lives_in_the_scorer_rubric",
        target=REVIEW,
        block="a pre-existing issue the diff did not introduce",
    ),
    Mutation(
        guard="test_review_fanout",
        test="TestReviewFanout.test_taxonomy_carries_its_scoring_disposition",
        target=REVIEW,
        block="Score anything matching this list below 60",
    ),
    Mutation(
        guard="test_review_fanout",
        test="TestReviewFanout.test_reviewers_report_everything_and_filter_nothing",
        target=REVIEW,
        block="report every candidate finding",
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
