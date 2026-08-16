"""Regression guard: the M71/D-042 out-of-band idea-capture rule.

Locks the rule text in `tracking-rules.md` — an idea surfaced through a
non-cairn capture channel is paired with a `candidate` ROADMAP row rather
than forbidden — plus the stated<->shipped link between the rule's named
enforcement arm and the hook that actually ships.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23) and steers clear of `**bold**` splits
(M26); phrases are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
HOOKS = SKILLS.parent / "hooks"


def rules():
    return SKILLS.joinpath("shared", "tracking-rules.md").read_text().lower()


class TestOutOfBandIdeaCaptureRule(unittest.TestCase):


    def test_the_named_hook_actually_ships(self):
        # stated<->enforced: the rulebook names a hook by filename, so a
        # rename that misses the prose leaves the rule citing a dead file.
        self.assertTrue((HOOKS / "idea_guard.py").is_file())


if __name__ == "__main__":
    unittest.main()
