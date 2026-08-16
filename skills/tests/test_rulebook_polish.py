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

    def test_explore_subagents_get_a_reading_list(self):
        self.assertIn("reading list", rules().lower())


if __name__ == "__main__":
    unittest.main()
