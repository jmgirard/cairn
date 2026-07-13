"""Regression guard: the /design-interview skill keeps its two-phase shape.

M12 encoded the openac-pilot interview (references/design-interview-notes.md,
items 1-11) as a standalone skill (D-013). This locks the load-bearing
invariants so wording drift can't quietly hollow the skill out: two phases
(facts -> principles), the bank-before-classify rule, the checkpoint seam,
and full registration. It does NOT judge interview quality — that is the
live openac pilot (criterion 6), which no test can stand in for.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def norm(*parts):
    """Whitespace-collapsed, lowercased text of a skill/tracking file."""
    text = SKILLS.joinpath(*parts).read_text()
    return re.sub(r"\s+", " ", text).lower()


class TestDesignInterviewSkill(unittest.TestCase):
    def setUp(self):
        self.skill = norm("design-interview", "SKILL.md")

    def test_reads_the_rulebook_first(self):
        self.assertIn("tracking-rules.md", self.skill)

    def test_phase_header_maps_facts_and_principles(self):
        self.assertIn("# design interview", self.skill)
        self.assertIn("## facts", self.skill)
        self.assertIn("## principles", self.skill)

    def test_facts_before_principles_is_declared(self):
        # The one-way dependency is the reason the phases exist in order.
        self.assertIn("facts before principles", self.skill)

    def test_phase1_disciplines_present(self):
        for anchor in [
            "elicit, don't classify",       # item 1
            "chain rounds on prior answers",  # item 2
            "ground every option in repo evidence",  # item 3
            "hypotheses that do work",       # item 4
            "wart",                          # item 5
        ]:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.skill)

    def test_phase1_banks_never_classifies(self):
        # Anchor on the bolded introduction, not a bare "banked-candidates
        # ledger": that phrase also occurs (whitespace-wrapped) further down,
        # so a bare assert survives deletion of the actual rule — false
        # coverage the M53 mutation harness flags.
        self.assertIn("**banked-candidates ledger**", self.skill)
        # Phase 1 must not ask for a principle commitment.
        self.assertIn("never ask", self.skill)

    def test_recommends_running_on_fable(self):
        # D-014: the interview defaults to Fable (openac pilot found Opus's
        # questions too technical). Lock the steer so it can't silently drift
        # back to an Opus default.
        self.assertIn("fable", self.skill)
        self.assertIn("d-014", self.skill)

    def test_seam_checkpoints_and_routes(self):
        self.assertIn("checkpoint-commit", self.skill)
        self.assertIn("continue into principles", self.skill)

    def test_phase2_candidates_arrive_classified_with_recommendation(self):
        self.assertIn("every candidate arrives classified", self.skill)
        self.assertIn("marked recommendation", self.skill)
        # The IP / GP / skip strength triad.
        for strength in ["inviolable", "guiding", "skip"]:
            with self.subTest(strength=strength):
                self.assertIn(strength, self.skill)

    def test_phase2_stress_tests_and_mines_sources(self):
        for anchor in [
            "stress-test",                        # item 6
            "essence from accident",              # item 7
            "scope of each ip",                   # item 8
            "mine git history",                   # item 9
            "derive candidates from the domain",  # item 10
        ]:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.skill)

    def test_phase2_writes_principles_with_ip_ordering(self):
        self.assertIn("ip block first", self.skill)
        self.assertIn("never reused or renumbered", self.skill)

    def test_skill_is_registered_everywhere(self):
        # Phase-header guard covers it.
        self.assertIn('"design-interview"',
                      SKILLS.joinpath("tests",
                                      "test_phase_header_levels.py").read_text())
        # DESIGN.md architecture count bumped to nine.
        self.assertIn("× 9", SKILLS.parent.joinpath("cairn", "DESIGN.md").read_text())
        # cairn-init hands off to the skill.
        self.assertIn("/design-interview", norm("cairn-init", "SKILL.md"))


if __name__ == "__main__":
    unittest.main()
