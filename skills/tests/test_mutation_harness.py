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
    Mutation(
        guard="test_migration_guidance",
        test="TestMigrationGuidance.test_reference_sweep_names_two_dispositions",
        target="skills/cairn-init/SKILL.md",
        block="Reference sweep",
    ),
    Mutation(
        guard="test_oracle_doctrine",
        test="TestOracleDoctrine.test_states_the_two_independent_types_bar",
        target=RULES,
        block="≥2 *independent* oracle types",
    ),
    Mutation(
        guard="test_phase_header_levels",
        test="TestPhaseHeaderLevels.test_rulebook_declares_h1_unit_h2_phase",
        target=RULES,
        block="A `#` names the unit of work",
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
