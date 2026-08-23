"""Regression guard: the merge-approval gate stays an AskUserQuestion chip,
and phase ends stay chip-less close blocks.

Skills are prose, so this locks two invariants:

1. The merge-approval gate (restored by the /hotfix on 2026-07-11):
   `/milestone-review` and `/hotfix` must present the *merge authorization
   itself* as an AskUserQuestion chip, never a prose "ask plainly for
   authorization" yes/no.

2. The phase-close rule (M156, retiring M26's routing-chip mandate): every
   phase or skill ends with the close block — recap, status, fenced next
   command(s), safety line — and no skill reintroduces the routing-chip
   token; decision-gate chips are unaffected.

Guard tests read each SKILL as one string, so `assertIn` fails across a
newline (M23 lesson) — asserted phrases live on single lines in the source.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return (SKILLS.joinpath(*parts)).read_text()


class TestMergeGateIsAChip(unittest.TestCase):
    def test_review_names_askuserquestion_at_merge_gate(self):
        text = read("milestone-review", "SKILL.md")
        self.assertIn("AskUserQuestion", text)
        # the specific anti-pattern this hotfix removed must not return
        self.assertNotIn("ask plainly for authorization to merge", text)

    def test_hotfix_names_askuserquestion_at_merge_gate(self):
        text = read("hotfix", "SKILL.md")
        self.assertIn("AskUserQuestion", text)


# M156: routing chips are retired — every phase or skill ends with the
# close block, and no skill may reintroduce the routing-chip token. The old
# TestRoutingChipMandate (per-skill chip token, review's sole exception)
# retired with its subject; its merge-gate-survives assert lives on below.
class TestPhaseCloseBlock(unittest.TestCase):
    def test_rule_states_close_block_never_a_chip(self):
        self.assertIn(
            "ends with a **close block**, never a chip",
            read("shared", "tracking-rules.md").lower(),
        )

    def test_rule_hands_the_user_the_fenced_command(self):
        self.assertIn(
            "the next skill — the user runs the fenced command",
            read("shared", "tracking-rules.md").lower(),
        )

    def test_rule_carries_the_safety_line(self):
        self.assertIn(
            "adjusting course or `/clear` are both safe at this point",
            read("shared", "tracking-rules.md").lower(),
        )

    def test_rule_spares_decision_gates(self):
        self.assertIn(
            "unaffected: a gate is a choice, a phase end is a",
            read("shared", "tracking-rules.md").lower(),
        )

    def test_no_skill_reintroduces_the_routing_chip_token(self):
        for path in sorted(SKILLS.glob("*/SKILL.md")):
            self.assertNotIn(
                "routing chip",
                path.read_text(encoding="utf-8").lower(),
                f"{path}: the routing-chip token returned after M156",
            )

    def test_review_keeps_its_merge_gate_chip(self):
        # retiring routing chips removes only phase-end chips; the merge
        # gate stays a chip (IP1's explicit approval surface)
        text = read("milestone-review", "SKILL.md")
        self.assertIn("this is the third gate", text)
        self.assertIn("AskUserQuestion", text)


# The chip is a *user stop* (D-003), but selecting an option is a go: the
# orchestrator, not the user, invokes the target skill (M29). This guard
# locks that imperative and the `→ /skill` notation clarification so the rule
# can't revert to the descriptive "selecting a chip invokes that skill" form.
# Phrases are asserted case-insensitively (M26) and must each live on one
# physical line (M23) — the file is read as a single string.
class TestChipInvocationImperative(unittest.TestCase):
    def test_rulebook_states_invoke_on_selection_imperative(self):
        text = read("shared", "tracking-rules.md").lower()
        self.assertIn(
            "the orchestrator immediately invokes the target skill via the skill tool",
            text,
        )


# M35 AC2: a question gate carries at most 3 prioritized clarification
# markers, so a gate can't balloon past a focused round. Phrase asserted
# case-insensitively on one physical line (M23).


if __name__ == "__main__":
    unittest.main()
