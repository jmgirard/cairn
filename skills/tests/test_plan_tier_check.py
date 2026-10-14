"""Regression guard: the plan checks the work tier before it plans (M250).

Pins the `/milestone-plan` step 1 tier check (the three tiers, the
mixed-request rule, the read bound, the two already-tiered sources, and the
no-work exemption), the tier chip and each option's effect, the `tier
check:` work-log line, step 4's pointer to it, and the rulebook sentence
that puts the chip before the run. Text is whitespace-collapsed on read
(M171), so a phrase may wrap across lines.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def flat(path):
    return re.sub(r"\s+", " ", path.read_text())


def section(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


class TestPlanTierCheck(unittest.TestCase):
    def setUp(self):
        plan = flat(SKILLS / "milestone-plan" / "SKILL.md")
        self.step1 = section(plan, "1. Confirm nothing else is `in-progress`",
                             "2. **Investigate first.**")
        self.step4 = section(plan, "4. **Solidify autonomously**",
                             "5. **Remainder ledger")
        self.rules = flat(SKILLS / "shared" / "tracking-rules.md")

    def test_tiers_are_defined_before_step_2(self):
        for phrase in (
            "**Tier check (before step 2).** Before it investigates, the plan "
            "checks that the request needs a milestone, by the tiers of "
            "tracking-rules \"Sizing and the work tiers\".",
            "It puts the request as a whole in exactly one tier:",
            "`hotfix`: a user-visible bug whose fix restores documented "
            "behavior in one sitting with no design decision.",
            "`trivial`: no runtime surface (a typo, a comment, a tracking "
            "edit), one sitting, no design decision, and, in guest mode, "
            "only files under `cairn/`.",
            "`milestone`: anything else, a small change to running code that "
            "is not a bug included.",
            "A request whose parts fall in more than one tier, or any of "
            "whose parts is `milestone`, is a milestone.",
            "The check can read the code and docs the request names. It does "
            "not run step 2's sweeps or spawn subagents.",
        ):
            self.assertIn(phrase, self.step1)

    def test_routed_sources_and_no_work_requests(self):
        for phrase in (
            "The check runs on every source of request that names work: "
            "typed text, a candidate row, a pane press, an issue.",
            "The first is an invocation from `/milestone` §4's `milestone` "
            "verdict.",
            "The second is a `/milestone-plan` for work that `/hotfix` found "
            "over the hotfix bar earlier in this session, whether that hotfix "
            "stopped at step 1 or closed at step 7 after a merged-PR "
            "re-entry.",
            "The check classifies both `milestone` without re-judging, and "
            "the work-log reason names the router.",
            "A request that names no work is not checked: its work is chosen "
            "at step 3's question set and planned as a milestone.",
        ):
            self.assertIn(phrase, self.step1)

    def test_tier_chip_and_its_options(self):
        for phrase in (
            "On a `milestone` finding the plan asks nothing and goes on.",
            "On a `hotfix` or `trivial` finding it poses one chip before "
            "step 2. The chip's question text names, in plain words, the tier "
            "found and the reason.",
            "The chip comes before the run's question set and is not part "
            "of it",
            "**The tier's route** (recommended).",
            "`hotfix`: invoke `/hotfix` through the Skill tool with the "
            "request as its argument, in `/milestone` §4's form. The argument "
            "opens with a one-line summary of the bug. An issue is then named "
            "as `issue <URL>`, never as a bare `#N`, which `/hotfix` reads as "
            "a pull request. The plan writes no file.",
            "In owner mode it is committed and pushed to the default branch. "
            "In guest mode it is left uncommitted on disk.",
            "The description also names any other uncommitted paths, which "
            "the commit leaves alone.",
            "the plan runs `git status` and `git fetch <base>`, then edits and "
            "commits only the files the edit touches and pushes at once.",
            "If the checkout is not on the default branch, or one of those "
            "files holds uncommitted changes, the plan makes no edit and ends "
            "with a close block naming why.",
            "It also refuses in three other cases: the repo has no remote, the "
            "default branch is ahead of or behind `<base>/<default-branch>`, "
            "or a file is already staged.",
            "The plan shows the edit verbatim in chat, commits by path (`git "
            "commit -m \"<one-line summary>\" -- <paths>`), and pushes.",
            "If the push is rejected, it never forces, and the close block "
            "names the local commit.",
            "On success it ends with a close block naming the commit.",
            "In guest mode it writes the edit on disk with no commit and ends "
            "with a close block.",
            "**Plan a milestone anyway.** The plan goes on to step 2.",
            "**Stop.** The close block, and nothing written.",
        ):
            self.assertIn(phrase, self.step1)

    def test_tier_check_work_log_line(self):
        for phrase in (
            "Step 4 writes one work-log line in the first milestone file it "
            "writes: `tier check: milestone — <reason>` after a `milestone` "
            "finding, `tier check: <tier> — planned as a milestone at the "
            "user's choice` after the plan-anyway option, or `tier check: not "
            "run — work named at the question set` for a request that named "
            "no work.",
        ):
            self.assertIn(phrase, self.step1)
        self.assertIn("**Tier-check line.** Write the `tier check:` work-log "
                      "line that step 1's tier check names.", self.step4)

    def test_rulebook_puts_the_chip_before_the_run(self):
        self.assertIn(
            "A run begins at the plan question set. `/milestone-plan`'s tier "
            "chip comes before it and is not a run gate. That chip is posed "
            "only when the plan's step-1 tier check finds a hotfix or a "
            "trivial edit",
            self.rules)


if __name__ == "__main__":
    unittest.main()
