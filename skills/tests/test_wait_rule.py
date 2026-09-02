"""Prose guard: waiting on CI and background work follows a tested rule (M170).

The rulebook's wait paragraph once prescribed one blocking `gh pr checks
--watch` wait resolved within the turn. M170's experiment
(`cairn/references/wait-mechanisms.md`) showed a foreground call at the
harness ceiling is moved to the background rather than killed, so that
wording produced the stale watcher it meant to prevent. The replacement rule
has two load-bearing clauses pinned here: the trigger (what a wait is and
that each thing waited on has one watcher) and the stop point (no watcher
left armed at a commit, turn end, or `/clear` point — stopped with TaskStop
first). Each is registered in the mutation harness. The negative check that
the superseded spelling is gone from the shipped prose spells the retired
token by concatenation (M169 lesson) and is unregistered — there is no block
to mutate.

Anchors are copied from the shipped bytes; phrases crossing a hard wrap are
matched with `\\s+` so a reflow does not red a rule still present (M105).
Targets are read with `Path.read_text` because the mutation engine patches
only that call (M100). Hand-run only (M144, D-109):

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def rules():
    return read("shared", "tracking-rules.md")


def section(text, start, end):
    """The slice of `text` between the first `start` and the next `end`."""
    return text.split(start, 1)[1].split(end, 1)[0]


class TestWaitRuleTrigger(unittest.TestCase):
    """AC2: the rule names what it applies to — one watcher per thing
    waited on — under its own heading in the git and approval section."""

    def setUp(self):
        self.para = section(rules(), "**Waiting on CI and background work**",
                            "## Context hygiene")

    def test_one_watcher_per_wait(self):
        self.assertRegex(
            self.para,
            r"One\s+watcher\s+per\s+wait:\s+a\s+run,\s+command,\s+or\s+subagent\s+is"
            r"\s+watched\s+by\s+one\s+mechanism\s+at\s+a\s+time,\s+never\s+two\s+on"
            r"\s+the\s+same\s+thing\.",
        )

    def test_rule_cites_the_observation_page(self):
        self.assertIn("`cairn/references/wait-mechanisms.md`", self.para)


class TestWaitRuleStopPoint(unittest.TestCase):
    """AC2: the stop-point clause — no watcher armed at a commit, turn end,
    or `/clear` point; the session stops it with TaskStop first."""

    def setUp(self):
        self.para = section(rules(), "**Waiting on CI and background work**",
                            "## Context hygiene")

    def test_no_watcher_left_armed_at_a_stop_point(self):
        self.assertRegex(
            self.para,
            r"no\s+watcher\s+is\s+left\s+armed\s+at\s+a\s+commit,\s+a\s+turn\s+end,"
            r"\s+or\s+a\s+`/clear`\s+point",
        )

    def test_session_stops_it_with_taskstop_first(self):
        self.assertRegex(
            self.para,
            r"the session stops it with `TaskStop` first",
        )


class TestSupersededWordingIsGone(unittest.TestCase):
    """AC3: the retired spelling no longer appears in the shipped rulebook
    or the three skill sites (spelled by concatenation here so this guard
    is not itself a hit for the milestone's sweep)."""

    def test_old_spelling_is_gone(self):
        retired = "blocking" + " wait"
        for parts in (("shared", "tracking-rules.md"),
                      ("hotfix", "SKILL.md"),
                      ("milestone-review", "SKILL.md"),
                      ("cairn-release", "SKILL.md")):
            self.assertNotIn(retired, read(*parts))


if __name__ == "__main__":
    unittest.main()
