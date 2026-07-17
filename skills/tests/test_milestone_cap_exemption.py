"""Lock: M55 — the milestone weight cap exempts the review-exclusive `## Review`
section.

The tracking-rules weight-caps text must state that a live milestone file is
capped on its plan-owned body only (the `## Review` section is exempt), and the
stated cap (150) must equal the enforced `MILESTONE_CAP` in `cairn_scripts.py` —
two encodings of one number that must not drift. The measurement itself is
enforced by the over-cap fixtures in `scripts/tests`; this guard locks the
stated rule and the stated↔enforced agreement.

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent


def read(path):
    return path.read_text()


class TestMilestoneCapExemption(unittest.TestCase):
    def setUp(self):
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")

    def test_weight_caps_states_review_exemption(self):
        # Anchored on the rule's own contiguous phrasing (M39/M23 single-line):
        # the *reason* the exemption exists is the load-bearing sentence.
        self.assertIn(
            "review evidence never scrambles plan-owned content", self.rules
        )

    def test_weight_caps_states_the_plan_owned_body_cap(self):
        self.assertIn("plan-owned body < 150 lines", self.rules)

    def test_weight_caps_states_single_pass_compression(self):
        # M69: over-cap trimming is one targeted pass driven by the breakdown,
        # never a nibble-and-recount loop — the discipline that keeps a session
        # from slowing to a crawl at the cap.
        self.assertIn("never a nibble-and-recount loop", self.rules)

    def test_weight_caps_states_cross_reference_not_restate(self):
        # M69: the classic overrun is a milestone restating a durable record's
        # substance; the remedy is to cross-reference it, not retype it.
        self.assertIn("cross-reference a durable record", self.rules)

    def test_stated_cap_matches_enforced_cap(self):
        # The rulebook's human-readable cap and the scripts' machine-enforced cap
        # are two encodings of one number; drift between them is the defect.
        stated = int(
            re.search(r"plan-owned body < (\d+) lines", self.rules).group(1)
        )
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        enforced = int(re.search(r"MILESTONE_CAP\s*=\s*(\d+)", scripts).group(1))
        self.assertEqual(stated, enforced)


if __name__ == "__main__":
    unittest.main()
