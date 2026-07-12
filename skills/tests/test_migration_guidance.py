"""Regression guard: the /cairn-init §2 migration protocol keeps the M23
hardening from the M20 ackwards pilot (references/migration-pilot-notes.md).

The pilot found four migration gaps that live only in skill prose, so a drift
that drops any of them fails here (the same limit as every skill-prose guard:
this locks the *text*, not the runtime behaviour). Locked:
  * rich pre-existing DESIGN — the keep-verbatim vs extract choice
    (Compromise A/B) and invariants routed to /design-interview (G3/G5);
  * the repoint-or-note reference sweep for in-code refs + entombed-skill
    prose (G6/G10);
  * post-move .Rbuildignore prune (G7) and the widened Lineage B detection
    (G2).

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

    def test_rich_design_names_both_dispositions(self):
        # Keep-verbatim vs extract-to-DECISIONS: both compromises named.
        self.assertIn("Compromise A", self.skill)
        self.assertIn("Compromise B", self.skill)

    def test_invariants_route_to_design_interview(self):
        # Hard-constraint invariants are not IP/GP-formalized at migration
        # time; that judgement is routed to /design-interview (G5).
        self.assertIn("forced into IP/GP shape", self.skill)
        self.assertIn("/design-interview", self.skill)

    def test_reference_sweep_names_two_dispositions(self):
        self.assertIn("Reference sweep", self.skill)
        self.assertIn("repoint", self.skill)
        self.assertIn("note-and-leave", self.skill)

    def test_post_move_rbuildignore_prune(self):
        self.assertIn("prune per-file `.Rbuildignore`", self.skill)

    def test_lineage_b_detection_widened(self):
        self.assertIn("forward-only `ROADMAP.md`", self.skill)
        self.assertIn("Current focus", self.skill)


if __name__ == "__main__":
    unittest.main()
