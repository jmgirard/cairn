"""Regression guard: the migration protocol keeps the M23 hardening from the
M20 ackwards pilot (references/migration-pilot-notes.md).

M59 (RR01 rec 12): the protocol body moved from cairn-init §2 to
`skills/shared/migration-protocol.md`, read only on footprint detection —
protocol-content tests read the module; §0 detection and §1 scaffold tests
still read the skill.

The pilot found four migration gaps that live only in skill prose, so a drift
that drops any of them fails here (the same limit as every skill-prose guard:
this locks the *text*, not the runtime behaviour). Locked:
  * rich pre-existing DESIGN — the keep-verbatim vs extract choice
    (Compromise A/B) and invariants routed to /design-interview (G3/G5);
  * the repoint-or-note reference sweep for in-code refs + entombed-skill
    prose (G6/G10);
  * post-move .Rbuildignore prune (G7) and the widened Lineage B detection
    (G2).

The M41 intraclass pilot (first Lineage A) added four more, locked by
TestLineageAGuidance below (references/migration-pilot-notes.md Pilot 3):
  * concern-split precursor → cairn-home mapping + thin DESIGN seed (G-I1);
  * numbered-principle forced note-and-leave (G-I2, headline);
  * coupled-vs-clean repo-local skill classification + keep/entomb gate (G-I4);
  * pointer-only DECISIONS for large decision logs (G-I5).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


class TestMigrationGuidance(unittest.TestCase):
    def setUp(self):
        self.skill = read("cairn-init", "SKILL.md")
        self.protocol = read("shared", "migration-protocol.md")

    def test_rich_design_names_both_dispositions(self):
        # Keep-verbatim vs extract-to-DECISIONS: both compromises named.
        self.assertIn("Compromise A", self.protocol)
        self.assertIn("Compromise B", self.protocol)

    def test_invariants_route_to_design_interview(self):
        # Hard-constraint invariants are not IP/GP-formalized at migration
        # time; that judgement is routed to /design-interview (G5).
        self.assertIn("forced into IP/GP shape", self.protocol)
        self.assertIn("/design-interview", self.protocol)

    def test_reference_sweep_names_two_dispositions(self):
        self.assertIn("Reference sweep", self.protocol)
        self.assertIn("repoint", self.protocol)
        self.assertIn("note-and-leave", self.protocol)

    def test_post_move_rbuildignore_prune(self):
        self.assertIn("prune per-file `.Rbuildignore`", self.protocol)

    def test_lineage_b_detection_widened(self):
        # §0 detection text — stays in the skill.
        self.assertIn("forward-only `ROADMAP.md`", self.skill)
        self.assertIn("Current focus", self.skill)

    # --- M21 circumplex-pilot fixes ---

    def test_scaffold_creates_lessons_file(self):
        # G-C1: the §1 fresh-scaffold tree must list LESSONS.md (a top-level
        # tracking file per D-015) — the circumplex pilot found it omitted.
        self.assertIn("LESSONS.md", self.skill)

    def test_translate_planned_needs_criteria_else_candidate(self):
        # G-C3: a legacy "planned" item without criteria/tasks maps to a
        # candidate, not `planned` (no-invention).
        self.assertIn("acceptance criteria and ordered tasks", self.protocol)
        self.assertIn("inventing criteria violates no-invention", self.protocol)

    def test_dry_run_mode_is_read_only_and_offered_at_entry(self):
        # M61 (RR01 §10.3): a read-only inventory+ledger pass, offered on the
        # migration-entry chip, recommended for unrecognized footprints,
        # writing nothing.
        self.assertIn("**Dry-run mode (read-only first contact", self.protocol)
        self.assertIn("Offer a dry run on", self.protocol)
        self.assertIn("no branch, no file moves, no commits", self.protocol)
        self.assertIn("unrecognized or outside the known precursor lineages",
                      self.protocol)


class TestProgressiveDisclosure(unittest.TestCase):
    """M59 (RR01 rec 12): the protocol is its own module, read only when §0
    detects a precursor footprint — the common scaffold path never loads it."""

    def test_module_carries_the_protocol(self):
        mod = read("shared", "migration-protocol.md")
        self.assertIn("migrate the living, entomb the dead", mod)

    def test_skill_points_at_module_on_footprint_only(self):
        skill = read("cairn-init", "SKILL.md")
        self.assertIn("migration-protocol.md", skill)
        self.assertIn("when (and only when)", skill)


class TestLineageAGuidance(unittest.TestCase):
    """M41 intraclass pilot (first Lineage A) — four §2 additions. Each phrase
    below is one the addition *uniquely* introduces on a single line, so
    deleting the addition fails its assertion (M23 newline trap + M39/M40
    false-coverage trap)."""

    def setUp(self):
        self.skill = read("shared", "migration-protocol.md")

    def test_concern_split_precursor_mapping(self):
        # G-I1: no single DESIGN.md → map to cairn homes, keep repo-specific,
        # author a thin DESIGN seed pointing to them.
        self.assertIn("Concern-split precursor", self.skill)
        self.assertIn("thin `DESIGN.md` seed", self.skill)

    def test_numbered_principle_forced_note_and_leave(self):
        # G-I2 (headline): principles cited by number in package code are a
        # forced note-and-leave — keep the file, defer IP/GP + in-code repoint.
        self.assertIn("forced note-and-leave", self.skill)
        self.assertIn("the eventual in-code repoint", self.skill)

    def test_coupled_vs_clean_skill_classification(self):
        # G-I4: tracking-coupled skills entomb; clean domain skills are
        # surfaced at the step-3 gate for a keep/entomb decision.
        self.assertIn("classify, then entomb or ask", self.skill)
        self.assertIn("an explicit keep-or-entomb decision", self.skill)
        self.assertIn("surfaced here too", self.skill)

    def test_pointer_only_decisions_for_large_logs(self):
        # G-I5: pointer-only is an explicit disposition for large decision logs.
        self.assertIn("pointer-only", self.skill)
        self.assertIn("pure pointer at the entombed legacy log", self.skill)


if __name__ == "__main__":
    unittest.main()
