"""Regression guard for M120's delegation warrant in "Model and agent strategy".

`TestDelegationWarrantRule` holds one assert, on the one-not-several bar
(corrected M285: this docstring once named a second class and three asserts
that the file no longer holds).

Adopted from `cairn/references/prompting-opus-5.md` (§ Controlling subagent
spawning), which reports that Claude Opus 5 — the tier cairn runs its
orchestrator on — "delegates to subagents more readily than prior models".
Before M120 the rulebook decided *which* tier a spawn got — the Sonnet/Opus/
Fable bullets — and, for Fable alone, whether it happened (the RB/RR protocol
and its per-instance gate). Nothing stated when work should stay inline, so the
cheapest wrong answer — spawn an Opus subagent for a two-grep question — was
tier-correct and violated no rule.

The assert pins the one-not-several bar WITH its predicate: an anchor stopping
at `spawn one` would leave `rather than several` on the next physical line and
survive inverting the rule.

Skill-prose guards read the file as one string, so every asserted phrase lives
on a single source line (M23/M64), matches through `**bold**` markers rather
than across them (M26), and is read per-test, never cached at class level
(M61); phrases are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def rules():
    return (SKILLS / "shared" / "tracking-rules.md").read_text().lower()


class TestDelegationWarrantRule(unittest.TestCase):

    def test_rule_prefers_one_subagent_over_several(self):
        self.assertIn("spawn one rather than several", rules())


if __name__ == "__main__":
    unittest.main()
