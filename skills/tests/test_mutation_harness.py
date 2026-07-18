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
    Mutation(
        guard="test_review_fanout",
        test="TestReviewFanout.test_fanout_states_why_a_fresh_model_reviews",
        target=RULES,
        block="fresh-context subagents",
    ),
    Mutation(
        guard="test_rulebook_polish",
        test="TestRulebookPolish.test_copy_run_commands_get_their_own_fenced_block",
        target=RULES,
        block="own fenced code block",
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
]

# Prose-guard files deliberately NOT in the registry, each with a reason. The
# completeness check (below) treats these as covered.
EXEMPT = {
    "test_mutation_harness": "the harness's own tests, not a prose-guard",
}


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
