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


class TestRulebookStatesTheBoundedRead(unittest.TestCase):
    @property
    def rules(self):
        return read("shared", "tracking-rules.md")

    def test_rule_is_named_and_scoped_to_headings(self):
        self.assertIn("**Bounded `DECISIONS.md` read.**", self.rules)
        self.assertIn(
            "it is read by scanning its `### D-` headings — never whole (D-054)",
            self.rules,
        )

    def test_matched_entry_is_read_whole_before_surfacing(self):
        self.assertIn(
            "**A matched heading's entry is read whole before anything is surfaced.**",
            self.rules,
        )

    def test_match_is_back_referenced_by_its_own_id(self):
        # Label and mechanism on one line: pinning "back-referenced" alone
        # would survive dropping the id search, which is the whole mechanism.
        self.assertIn(
            "**A match is back-referenced — its own `D-0NN` id searched across "
            "the file**",
            self.rules,
        )

    def test_back_reference_names_the_entries_it_covers(self):
        # The three legacy gaps are why the step exists; without them the rule
        # reads as belt-and-braces and is the first thing an editor trims.
        self.assertIn("D-012, D-014, and D-019 each omit one", self.rules)

    def test_collision_is_quoted_from_the_full_entry_not_the_heading(self):
        self.assertIn(
            "**A collision is quoted verbatim from the full entry, never from "
            "the heading.**",
            self.rules,
        )

    def test_ip2_obligation_is_stated_as_unchanged(self):
        # The narrowing is recall-only. Transposing this to "IP2 is narrowed"
        # would license surfacing less, which the D-entry explicitly refuses.
        self.assertIn("what narrows is recall, not the obligation", self.rules)

    def test_heading_quality_rule_pins_subject_and_relationships(self):
        self.assertIn(
            "**A `### D-` heading names its subject and any entry it "
            "supersedes, annotates, or narrows.**",
            self.rules,
        )

    def test_heading_advisory_is_prospective_and_warns(self):
        self.assertIn("`decision heading quality` advisory WARNs", self.rules)
        self.assertIn("D-054 onward that do not", self.rules)


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

    def test_search_first_rule_points_at_the_bounded_read(self):
        rules = read("shared", "tracking-rules.md")
        self.assertIn(
            "Its `DECISIONS.md` sweep follows the bounded read below.", rules
        )


if __name__ == "__main__":
    unittest.main()
