"""Lock: M93/D-052 — the `Last hygiene check` stamp is replaced, not appended.

The defect this guards against is an instruction gap, not a code bug. All
three write sites said only "update" the stamp, which reads as "add to", so
each pass prepended a parenthetical and demoted the last to `Prior:`/`Earlier:`
— reaching 3,152 chars on one line in an adopting repo (2026-07-19) while both
weight axes read green. cairn's own instance was pruned by hand once
(`dbf1068`) with no rule or guard behind it, which is exactly why it came back.

So the rule has to exist at every surface that writes the stamp, and this
file pins the write sites' replace-shape (M146 pruned the retired
density-machinery pins).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import sys
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent

def read(path):
    return path.read_text()


class TestStampWriteSites(unittest.TestCase):
    """Every surface that writes the stamp must say REPLACE.

    The rulebook stating it is not enough: these are the steps an agent
    actually follows at audit and post-merge hygiene, and "update" at any one
    of them regrows the chain. circumplex proved it — its `review M42: done`
    pass rewrote the stamp on 2026-07-19 and still left 2,568 chars, because
    the instruction it read said "update"."""

    def site(self, *parts):
        return read(SKILLS.joinpath(*parts))


    def test_shipped_skeleton_teaches_the_shape(self):
        # An adopting repo learns the format from the scaffold it is given,
        # so the skeleton carries the rule inline rather than relying on the
        # author having read the rulebook first. (The D-052 citation left
        # the shipped line at the M146 review — a cairn-internal id in an
        # adopter's ROADMAP, finding O15.)
        text = self.site("cairn-init", "SKILL.md")
        self.assertIn(
            "_Last hygiene check: YYYY-MM-DD (one short line, replaced each "
            "pass — never appended to)_",
            text,
        )

    def test_milestone_audit_write_site_says_replace(self):
        # Restored at the M146 review fix pass: the audit's write site says
        # replace, never append or demote (the D-052 lineage's live half).
        self.assertIn(
            "never append to the previous stamp or demote it to a "
            "`Prior:` clause",
            self.site("milestone", "SKILL.md"),
        )

    def test_review_write_site_says_replace(self):
        self.assertIn(
            "never append to it or demote it to a `Prior:` clause",
            self.site("milestone-review", "SKILL.md"),
        )

    def test_no_write_site_still_says_only_update(self):
        # The negative direction, paired with the positive write-site
        # asserts above so it is not vacuous (M54: blanking cannot restore
        # an absence, so a lone assertNotIn cannot be mutation-proven).
        for parts in (
            ("milestone", "SKILL.md"),
            ("milestone-review", "SKILL.md"),
        ):
            with self.subTest(site="/".join(parts)):
                self.assertNotIn('update "Last hygiene check', self.site(*parts))


if __name__ == "__main__":
    unittest.main()
