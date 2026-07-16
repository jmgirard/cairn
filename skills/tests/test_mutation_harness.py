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

REGISTRY = [
    Mutation(
        guard="test_search_first_candidates",
        test="TestSearchFirstCandidateRule.test_rule_names_all_three_sweep_targets",
        target=RULES,
        block="sweep existing candidates + `milestones/archive/`",
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
