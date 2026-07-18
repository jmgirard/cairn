"""Prose-guards for /cairn-init's §3 Repair section (M82).

D-047 renamed the source shelf behind a non-failing `scaffold deprecations`
advisory, but nothing performed the rename: `/milestone`'s audit surfaces
advisories and never auto-fixes them, and repair mode saw a complete scaffold
because `check_scaffold` accepts the legacy entry. §3 is where cairn acts on
the advisory it emits.

Locks: the section exists and §0 points at it; the step consumes the advisory's
own output rather than a rename named in the prose (so a later
DEPRECATED_GITIGNORE entry needs no skill edit); and each of the three
consent rules stays bound to the action it governs. The label and its rule are
fused into one bold token per M74/M76 — swapping two rules cannot leave these
asserts green — and each sits on one physical SKILL line (M23),
mutation-registered (M53) in test_mutation_harness.py.

Run: python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "cairn-init" / "SKILL.md"
VALIDATE = ROOT / "scripts" / "cairn_validate.py"

# The advisory's emitted label, verbatim. Prose naming a validate finding uses
# the emitted label (M78) — so this guard fails if either side is renamed
# without the other.
ADVISORY = "scaffold deprecations"


class TestRepairSection(unittest.TestCase):
    # read per-test, never cached at class level: the mutation harness re-runs
    # single methods against a patched read_text, and a setUpClass cache would
    # feed them the unmutated text (M61)
    @property
    def text(self):
        return SKILL.read_text()

    def test_repair_has_its_own_section(self):
        self.assertIn("## 3. Repair", self.text)
        # §0 dispatches to it rather than carrying the substance inline
        self.assertIn("- Already on cairn → **repair mode** (§3).", self.text)
        self.assertLess(
            self.text.index("**repair mode** (§3)"),
            self.text.index("## 3. Repair"),
        )

    def test_repair_keeps_the_scaffold_piece_and_profile_backfill(self):
        # moved out of §0, not dropped: both must land inside §3
        section = self.text.split("## 3. Repair", 1)[1]
        self.assertIn("**Missing §1 pieces.**", section)
        self.assertIn("A **missing `cairn/PROFILE.md`**", section)
        self.assertIn("is backfilled by inference", section)


class TestDeprecationMigration(unittest.TestCase):
    @property
    def text(self):
        return SKILL.read_text()

    @property
    def section(self):
        return self.text.split("## 3. Repair", 1)[1]

    def test_step_names_the_emitting_script_and_the_advisory_label(self):
        self.assertIn(
            'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py"',
            self.section,
        )
        self.assertIn(f"`{ADVISORY}`", self.section)

    def test_advisory_label_matches_the_one_validate_emits(self):
        # pairs the authored prose with the real checker it consumes (M77):
        # a rename on either side breaks this, not just the skill's copy
        self.assertIn(f'"{ADVISORY}"', VALIDATE.read_text())

    def test_step_is_driven_by_advisory_output_not_a_named_rename(self):
        # narrowing §3 back to the one pdf/ -> sources/ pair fails here
        self.assertIn(
            "Act on every line the advisory prints, never on a pair named in this text",
            self.section,
        )
        self.assertIn("migrates with no edit here", self.section)

    def test_entry_rewrite_needs_no_ask(self):
        self.assertIn("**Rewrite the entry, no ask.**", self.section)
        self.assertIn("rewrite touches nothing git tracks — so it needs no gate.", self.section)

    def test_directory_move_is_gated_on_an_explicit_ask(self):
        self.assertIn(
            "**Move the directory only after an explicit ask.** The shelf is gitignored, so its contents are untracked and git cannot restore them.",
            self.section,
        )
        self.assertIn("via AskUserQuestion before moving anything", self.section)

    def test_both_directories_present_is_never_clobbered(self):
        self.assertIn(
            "**Both directories present: surface, never clobber.** Never merge or overwrite one shelf with the other unasked.",
            self.section,
        )

    def test_absent_old_directory_completes_without_an_ask(self):
        self.assertIn("**Old directory absent:** the entry rewrite *is* the migration.", self.section)

    def test_step_confirms_the_advisory_went_quiet(self):
        self.assertIn("Report the verified result, not", self.section)
        self.assertIn("advisory is quiet", self.section)


if __name__ == "__main__":
    unittest.main()
