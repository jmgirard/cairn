"""M107: the RR-ingest and implement-amendment paths carry the budget re-check
+ one-pass-trim discipline that /milestone-plan step 4 already has.

An amendment that grows a plan-owned section (a binding-criterion ingest, an
AC/scope change) can push a milestone past the <150 cap. These paths must point
at `cairn_budget` and the tracking-rules one-pass-trim rule, so the overrun is
caught while writing rather than nibble-and-recounted at cairn_validate time.

Anchors copied from the target files' actual bytes (M95); the two-word span
uses `\\s+` so a future reflow across the wrap does not silently unpin it
(M105).

Run: python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    # pathlib read_text, never open(): the mutation engine patches Path.read_text
    # (M100), so an open()-based guard is invisible to the blanking.
    return SKILLS.joinpath(*parts).read_text(encoding="utf-8")


class TestBriefIngestRechecksBudget(unittest.TestCase):
    def test_brief_step3_points_at_cairn_budget_and_one_pass_trim(self):
        text = read("milestone-brief", "SKILL.md")
        self.assertIn("re-check the plan-owned body with `cairn_budget`", text)
        self.assertRegex(
            text, r"single heaviest plan-owned section\s+in one pass")


class TestImplementAmendmentRechecksBudget(unittest.TestCase):
    def test_step6_points_at_cairn_budget_and_one_pass_trim(self):
        text = read("milestone-implement", "SKILL.md")
        self.assertIn("re-checks the body with `cairn_budget`", text)
        self.assertRegex(
            text, r"single heaviest plan-owned\s+section in one pass")


if __name__ == "__main__":
    unittest.main()
