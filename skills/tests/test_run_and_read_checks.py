"""M59 (RR01 rec 7): run-and-read — skills run cairn_validate and READ its
output; they never enumerate its internal check list. A restated list is a
stale-count trap (M28): the script grows a check and the skill's
parenthetical silently trails it (both /milestone-review step 4 and
/milestone §2 had, by M58, drifted behind the real 15-check list).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def normalized(*parts):
    # Collapse whitespace so asserted phrases match across line wraps (M23).
    return re.sub(r"\s+", " ", SKILLS.joinpath(*parts).read_text())


class TestReviewRunsAndReads(unittest.TestCase):
    def test_review_runs_and_reads_never_restates(self):
        norm = normalized("milestone-review", "SKILL.md")
        self.assertIn("never restate or recall its internals", norm)
        # The retired parenthetical enumeration's signature.
        self.assertNotIn("(mirror, single in-progress", norm)

    def test_coverage_completeness_is_validate_output_not_manual(self):
        norm = normalized("milestone-review", "SKILL.md")
        # The disposition stays (a Coverage FAIL is a plan gap, gated
        # amendment) but as validate output — not a manual reviewer bullet.
        self.assertIn("mechanical since M34", norm)
        self.assertNotIn("- **Coverage completeness** —", norm)


class TestMilestoneRunsAndReads(unittest.TestCase):
    def test_milestone_audit_runs_and_reads_never_restates(self):
        norm = normalized("milestone", "SKILL.md")
        self.assertIn("read its output — one line per check", norm)
        # The retired enumeration's framing.
        self.assertNotIn("deterministically checks:", norm)


if __name__ == "__main__":
    unittest.main()
