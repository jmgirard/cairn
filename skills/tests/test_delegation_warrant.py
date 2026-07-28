"""Regression guards for two rules in "Model and agent strategy".

M120's delegation warrant (`TestDelegationWarrantRule`, three asserts) and
M121's self-checking-class rule (`TestSelfCheckingClassRule`, two).

Adopted from `cairn/references/prompting-opus-5.md` (§ Controlling subagent
spawning), which reports that Claude Opus 5 — the tier cairn runs its
orchestrator on — "delegates to subagents more readily than prior models".
Before M120 the rulebook decided *which* tier a spawn got — the Sonnet/Opus/
Fable bullets — and, for Fable alone, whether it happened (the RB/RR protocol
and its per-instance gate). Nothing stated when work should stay inline, so the
cheapest wrong answer — spawn an Opus subagent for a two-grep question — was
tier-correct and violated no rule.

The warrant takes three asserts, because it carries three claims
independently:

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


class TestSelfCheckingClassRule(unittest.TestCase):
    """M121: which class of self-checking the warrant above governs.

    The guide's delegation instruction carries a third clause M120 did not
    take — "do not use subagents to verify or double-check your own work" —
    which reads, unqualified, as a standing rejection of D-067's two
    fresh-context readers. It is not: the guide's own stated mechanism is that
    the model "verifies its own work without being told to", which is a claim
    about the AUTHOR re-reading, and says nothing about a reader that authored
    none of what it reads. The rule names both classes so the clause cannot be
    applied to the wrong one.

    Two asserts, one per named class, each a phrase on a single physical line
    of the shipped file — the AC4 shape. A single assert covering only the
    governed class would leave the exclusion deletable with the guard green,
    which is the false coverage the guard-must-fail rule exists to stop: the
    exclusion is the half that does work here, since the governed class alone
    is already implied by the warrant above it.

    Each assert pins its class phrase TOGETHER WITH the verb that assigns it —
    `it governs` / `it does not govern` — on one physical line. Pinning the
    two phrases alone left the rule invertible with both asserts green: swap
    the two lines and the guide's third delegation clause reaches D-067's
    fresh-context readers, which is exactly what this rule blocks. That is
    guard-doctrine §1's label-to-set trap, and the harness does not catch it
    because blanking is not swapping (§2)."""

    def test_rule_names_the_governed_class(self):
        self.assertIn(
            "it governs **an author re-checking work it just produced, in "
            "the context that produced it**",
            rules(),
        )

    def test_rule_names_the_excluded_class(self):
        self.assertIn(
            "it does not govern **an independent fresh-context reading of "
            "that work by a reader that authored none of it**",
            rules(),
        )


if __name__ == "__main__":
    unittest.main()
