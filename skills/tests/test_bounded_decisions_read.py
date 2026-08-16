"""The bounded `DECISIONS.md` read (M97, D-054).

`DECISIONS.md` is append-only and can never shrink, so the sweep scans its
`### D-` headings instead of the whole file. That trades recall for read cost,
and the trade is only safe while four clauses hold together — each is pinned
here on its own physical line (M74/M78: a wrapped anchor stops at the break,
before the predicate carrying the meaning).

The clauses, and what each stops:

- read-whole-before-surfacing — stops a heading being quoted as if it were the
  entry, which is how a bounded read silently becomes a shallower one.
- back-reference-by-id — covers D-012/D-014/D-019, which hide a supersession in
  their body where IP4 forbids repairing the heading.
- quote-from-the-full-entry — IP2's requirement, unchanged by the narrowing.
- heading names its subject and its relationships — the property the whole
  bound rests on.

Dropping any one of them leaves a rule that reads reasonable and recalls
wrongly, so each gets its own assert rather than one assert over the block.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    # Read per-test, never cached in setUpClass: the mutation harness runs a
    # guard as a single method and skips setUpClass, so a cached read would
    # see the unmutated file and report false coverage on itself (M61).
    return SKILLS.joinpath(*parts).read_text()


class TestPlanSkillWiresTheProtocol(unittest.TestCase):
    """Central rule plus per-skill wiring — the D-021/D-036 pattern, because
    conduct at specific steps drifted under central-only rules before."""

    @property
    def plan(self):
        return read("milestone-plan", "SKILL.md")

    def test_session_start_reads_headings_not_the_whole_file(self):
        self.assertIn("scan the `### D-` headings, never the whole file", self.plan)

    def test_session_start_also_states_read_whole_and_back_reference(self):
        # M97 review F7: session start stated only the headings clause, which
        # read alone is exactly "headings are enough" — the failure mode the
        # protocol exists to prevent. AC2 requires BOTH sweep sites to state
        # read-whole-before-surfacing, and the original guard checked only the
        # first half, so the gap was invisible.
        self.assertIn(
            "Read every matched entry whole before surfacing it, and "
            "back-reference it by",
            self.plan,
        )
        self.assertIn(
            "the headings decide what to open, never what to report", self.plan
        )

    def test_collision_check_cites_the_bounded_read(self):
        self.assertIn("bounded `DECISIONS.md` read", self.plan)

    def test_collision_check_states_read_whole_and_back_reference(self):
        self.assertIn("read every matched entry whole before", self.plan)
        self.assertIn("back-reference each match by its own `D-0NN` id", self.plan)

    def test_collision_check_forbids_quoting_from_the_heading(self):
        self.assertIn(
            "Quote a collision verbatim from the full entry, never from the "
            "heading.",
            self.plan,
        )


if __name__ == "__main__":
    unittest.main()
