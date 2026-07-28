"""Regression guard: the M120 delegation-warrant test (Model and agent strategy).

Adopted from `cairn/references/prompting-opus-5.md` (§ Controlling subagent
spawning), which reports that Claude Opus 5 — the tier cairn runs its
orchestrator on — "delegates to subagents more readily than prior models".
Before M120 the rulebook decided *which* tier a spawn got — the Sonnet/Opus/
Fable bullets — and, for Fable alone, whether it happened (the RB/RR protocol
and its per-instance gate). Nothing stated when work should stay inline, so the
cheapest wrong answer — spawn an Opus subagent for a two-grep question — was
tier-correct and violated no rule.

Three asserts, because the rule carries three claims independently:

- the inline floor — work finishable in a handful of tool calls is not
  delegated;
- the one-not-several bar, pinned WITH its predicate: an anchor stopping at
  `spawn one` would leave `rather than several` on the next physical line and
  survive inverting the rule (guard-doctrine §1's "usual cause");
- the review fan-out's standing, which is load-bearing rather than
  explanatory. The fan-out is described three bullets below this rule in the
  same section, and with this clause deleted a reader meets "spawn one rather
  than several" and then three reviewers with no stated reconciliation. The
  clause says the fan-out is not the forbidden case (distinct evidence bases,
  not one task done three times) rather than an exception to be traded off.

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
    def test_rule_keeps_small_work_inline(self):
        self.assertIn(
            "in a handful of tool calls is done inline, never delegated",
            rules(),
        )

    def test_rule_prefers_one_subagent_over_several(self):
        self.assertIn("spawn one rather than several", rules())

    def test_rule_reconciles_the_review_fanout(self):
        self.assertIn(
            "its three reviewers carry distinct evidence bases", rules()
        )


if __name__ == "__main__":
    unittest.main()
