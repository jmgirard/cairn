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
    def test_rule_present_in_tracking_rules(self):
        t = rules()
        self.assertIn("out-of-band idea capture", t)
        self.assertIn("is never the", t)
        self.assertIn("record of record for an idea", t)

    def test_rule_names_the_capture_channels_generically(self):
        # Channel-agnostic by decision (D-042 choice 3): the rule enumerates
        # exemplars, so a future channel inherits it without a rulebook edit.
        # Anchored on the rule's own contiguous list, not a bare "chip" —
        # that substring occurs throughout the output-discipline section.
        self.assertIn(
            "a background-task chip, a scratch todo, an ad-hoc note", rules()
        )

    def test_rule_requires_the_paired_candidate_row(self):
        # The load-bearing half: pairing, not prohibition. A rule that only
        # disapproved of the chip would satisfy the phrases above.
        t = rules()
        self.assertIn("the idea also lands as a `candidate` roadmap row", t)
        self.assertIn("the channel stays usable", t)

    def test_rule_names_its_runtime_enforcement_arm(self):
        self.assertIn(
            "`idea_guard.py` pretooluse hook injects this reminder", rules()
        )

    def test_the_named_hook_actually_ships(self):
        # stated<->enforced: the rulebook names a hook by filename, so a
        # rename that misses the prose leaves the rule citing a dead file.
        self.assertTrue((HOOKS / "idea_guard.py").is_file())


if __name__ == "__main__":
    unittest.main()
