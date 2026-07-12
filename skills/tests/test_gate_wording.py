"""Regression guard: the merge-approval gate and the end-of-phase routing
chip must both be AskUserQuestion chips.

Skills are prose, so this locks two invariants:

1. The merge-approval gate (restored by the /hotfix on 2026-07-11):
   `/milestone-review` and `/hotfix` must present the *merge authorization
   itself* as an AskUserQuestion chip, never a prose "ask plainly for
   authorization" yes/no.

2. The routing-chip mandate (M26): every phase skill that ends with a
   routing chip must name AskUserQuestion at that step, so a prose list of
   options can't silently stand in for a chip. `/milestone-review` is the one
   deliberate exception — it ends with a plain-prose `/clear` nudge and no
   routing chip, while still keeping its merge-approval chip.

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

    def test_rulebook_declares_merge_gate_a_chip(self):
        text = read("shared", "tracking-rules.md")
        self.assertIn("merge-approval gate is itself an AskUserQuestion chip", text)


# Phase skills whose end-of-phase routing chip must name AskUserQuestion.
# `/milestone-review` is deliberately excluded — its end is chip-less (below).
# `hotfix` has no standalone terminal routing-chip step; `milestone-brief`
# ends its RR-ingest phase on one (an M26 miss, brought under the guard in M28).
NON_REVIEW_CHIP_SKILLS = [
    "milestone-plan",
    "milestone-implement",
    "milestone",
    "cairn-init",
    "cairn-release",
    "design-interview",
    "milestone-brief",
]

# The canonical single-line token a routing-chip step carries; matched
# case-insensitively so a bolded "**Routing chip (AskUserQuestion)**" or a
# mid-sentence "routing chip (AskUserQuestion)" both satisfy it.
CHIP_TOKEN = "routing chip (askuserquestion)"


class TestRoutingChipMandate(unittest.TestCase):
    def test_non_review_skills_name_askuserquestion_at_routing_chip(self):
        for skill in NON_REVIEW_CHIP_SKILLS:
            text = read(skill, "SKILL.md").lower()
            self.assertIn(
                CHIP_TOKEN,
                text,
                f"{skill}: routing-chip step must name AskUserQuestion "
                f"via the token '{CHIP_TOKEN}' on one line",
            )

    def test_review_ends_chipless(self):
        text = read("milestone-review", "SKILL.md")
        # the deliberate exception is marked in prose ...
        self.assertIn("no routing chip", text)
        # ... and review must NOT carry the routing-chip token
        self.assertNotIn(CHIP_TOKEN, text.lower())

    def test_review_keeps_its_merge_gate_chip(self):
        # the exception removes only the *end* chip; the merge gate stays
        text = read("milestone-review", "SKILL.md")
        self.assertIn("this is the third gate", text)
        self.assertIn("AskUserQuestion", text)

    def test_rulebook_declares_prose_list_not_a_chip(self):
        text = read("shared", "tracking-rules.md")
        self.assertIn("a prose list of options is not a routing chip", text)

    def test_rulebook_declares_review_the_chipless_exception(self):
        text = read("shared", "tracking-rules.md")
        self.assertIn("the sole phase whose end is deliberately chip-less", text)


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

    def test_rulebook_says_never_hand_back_to_the_user(self):
        text = read("shared", "tracking-rules.md").lower()
        self.assertIn("does not stop to have the user type the command", text)

    def test_rulebook_clarifies_arrow_notation_names_the_skill(self):
        text = read("shared", "tracking-rules.md").lower()
        self.assertIn(
            "names the skill the orchestrator invokes on selection, "
            "not a command for the user to run",
            text,
        )


if __name__ == "__main__":
    unittest.main()
