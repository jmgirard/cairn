"""Regression guard: the M35 rulebook doc-wording polish batch.

Locks the three self-contained `tracking-rules.md` wording additions not
already covered by a topical guard (AC2 lives in `test_gate_wording.py`, AC4
in `test_review_fanout.py`):
  * AC1 — the mature-backlog clustering remedy in the weight-caps remedies
    (cluster related backlog into grouped candidate rows pointing at the
    entombed legacy ROADMAP — the M21 G-C4 case);
  * AC3 — the Explore-subagent reading-list instruction;
  * AC5 — copy-run commands go in their own fenced code block, not inline
    backticks. Widened by M86 into a three-case rule (handoff / naming /
    routing-chip arrow) that also names slash commands and separates a
    handoff from a mention.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23) and steers clear of `**bold**` splits
(M26); phrases are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def rules():
    return read("shared", "tracking-rules.md")


class TestRulebookPolish(unittest.TestCase):
    def test_weight_caps_include_mature_backlog_clustering(self):
        t = rules().lower()
        self.assertIn("grouped candidate rows", t)
        self.assertIn("entombed legacy", t)

    def test_explore_subagents_get_a_reading_list(self):
        self.assertIn("reading list", rules().lower())

    def test_copy_run_commands_get_their_own_fenced_block(self):
        """Each case-label is pinned together with its treatment on one line.

        M74/M76: pinning only the treatment ("its own fenced code block")
        survives swapping the label onto a different case, so the label and
        what it takes must ride the same assert.
        """
        t = rules().lower()
        self.assertIn(
            "handing the user a command to run → its own fenced code block", t
        )
        self.assertIn(
            "naming a command, path, or symbol in prose → inline backticks", t
        )
        self.assertIn(
            "a routing chip's `→ /skill` option → neither fence nor handoff", t
        )

    def test_copy_run_rule_covers_slash_commands(self):
        """Pins the predicate too — a truncated anchor survives inversion."""
        self.assertIn(
            "slash commands (`/clear`, `/milestone-plan`) count as commands here "
            "exactly as shell commands do",
            rules().lower(),
        )

    def test_copy_run_rule_separates_a_handoff_from_a_mention(self):
        """Each subject rides with its verdict, so transposing them goes red."""
        t = rules().lower()
        self.assertIn(
            "a step that ends the turn expecting the user to go run something → "
            "a handoff, and it gets the fence",
            t,
        )
        self.assertIn(
            "a line noting that a moment is a safe `/clear` point, beside a chip "
            "already offering the route → a mention, and it stays inline",
            t,
        )

    def test_copy_run_rule_scopes_the_fence_to_the_runnable_lines(self):
        self.assertIn(
            "the prose framing a handoff stays prose; only the runnable lines get fenced",
            rules().lower(),
        )


if __name__ == "__main__":
    unittest.main()
