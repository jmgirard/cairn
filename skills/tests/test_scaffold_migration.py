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
        # M80/F5: the label occurs several times in §3, so asserting it bare is
        # satisfiable by prose that merely mentions it. Pin it to the ONE
        # instruction that consumes it, script and label fused on one line.
        self.assertIn(
            'Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py"` '
            f"and read its `{ADVISORY}` advisory.",
            self.section,
        )

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

    def test_successor_entry_is_added_without_an_ask(self):
        self.assertIn(
            "**Add the successor entry, no ask.** `<new>` joins `.gitignore` and `<old>` stays for now.",
            self.section,
        )
        self.assertIn("touches nothing git tracks — so it needs no gate.", self.section)

    def test_superseded_entry_survives_until_its_directory_is_gone(self):
        # F1: removing `<old>` while the shelf still holds files un-ignores
        # untracked contents a repo may keep out of git deliberately. The
        # removal rule and its trigger are fused on one line (M74/M76).
        self.assertIn(
            "**Remove `<old>` from `.gitignore` only once the old directory is gone from disk.**",
            self.section,
        )
        self.assertIn("both entries keep the shelf ignored", self.section)

    def test_directory_move_is_gated_on_an_explicit_ask(self):
        self.assertIn(
            "**Only the old directory present: move it only after an explicit ask.** The shelf is gitignored, so its contents are untracked and git cannot restore them.",
            self.section,
        )
        self.assertIn("via AskUserQuestion before moving anything", self.section)

    def test_both_directories_present_is_never_clobbered(self):
        self.assertIn(
            "**Both directories present: surface, never clobber.** Never merge or overwrite one shelf with the other unasked.",
            self.section,
        )

    def test_cases_are_mutually_exclusive_and_chosen_before_any_move(self):
        # F3: as a numbered sequence, the move was reached before the
        # clobber check. The exclusivity and its timing are the rule.
        self.assertIn(
            "Then take **exactly one** of the cases below, chosen by what is on disk",
            self.section,
        )
        self.assertIn("*before* anything moves", self.section)
        self.assertIn("mutually exclusive states, not a sequence", self.section)
        # the clobber case must precede the move case in reading order too
        self.assertLess(
            self.section.index("**Both directories present:"),
            self.section.index("**Only the old directory present:"),
        )

    def test_absent_old_directory_completes_without_an_ask(self):
        self.assertIn("**Old directory absent: the entry change *is* the migration.**", self.section)

    def test_closing_check_does_not_claim_to_verify_the_directory(self):
        # F2/AC5: check_gitignore_deprecations reads .gitignore alone, so a
        # quiet advisory cannot distinguish a completed move from a declined
        # one. The prose must say so rather than claim a verified outcome.
        self.assertIn(
            "**A quiet advisory confirms the entry, not the directory** — `check_gitignore_deprecations` reads `.gitignore` alone and never the filesystem,",
            self.section,
        )
        self.assertIn("Report the directory outcome on its own", self.section)
        # the superseded false claim must not come back
        self.assertNotIn("a still-firing advisory means a step above", self.section)

    def test_repair_commit_cannot_sweep_an_unmigrated_shelf(self):
        self.assertIn(
            "**stage the files repair touched by path, never `git add -A` or `.`**",
            self.section,
        )


if __name__ == "__main__":
    unittest.main()
