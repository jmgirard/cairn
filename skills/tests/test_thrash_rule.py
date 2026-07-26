"""Regression guard: the M114 thrash rule in `/milestone-review` step 4.

The rule was unguarded prose until M114 — every phrase of it (`third trip`,
`queue another retry`, `mis-planned`, `re-plan or split`) occurred in the skill
and in no test, so deleting it outright kept the suite green. That is the gap
this file closes.

Four properties, each separately deletable and so separately asserted:

  1. returns are counted PER MILESTONE, not per cut;
  2. a `/milestone-plan` re-cut increments that count and never resets it —
     the reading that cost intraclass M93 four of its seven returns;
  3. the second trigger is one criterion failing twice by a NEW MECHANISM OF
     THE SAME SHAPE, remedied by reconsidering the recorded alternative;
  4. where no alternative was recorded, escalation via `/milestone-brief` is
     offered instead.

Plus a one-surface pin: the rule must live in exactly one file (M112 — a
doctrine change has more surfaces than the skill you edited; M113 — a phrase
occurring twice hands an existing guard false coverage).

Skill-prose guards read the file as one string and match case-insensitively,
so every asserted phrase sits on a single source line (M23) — except the
second trigger, which wraps in the shipped file and is matched with `\\s+`
across the break rather than truncated to the pre-wrap half (M105).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    # Path.read_text, not open() — the mutation engine patches only the former,
    # so a guard reading its target any other way is invisible to it (M100).
    return SKILLS.joinpath(*parts).read_text().lower()


def review():
    return read("milestone-review", "SKILL.md")


class TestThrashCounting(unittest.TestCase):
    def test_returns_are_counted_per_milestone_not_per_cut(self):
        self.assertIn("count returns **per milestone, never per cut**", review())

    def test_a_recut_increments_the_count_and_never_resets_it(self):
        # The load-bearing half. Without it "per milestone" is still readable
        # as "per milestone, restarting at each re-cut", which is exactly how
        # M93's counter was read: its pass 4 logged as the re-cut's first.
        self.assertIn("increments the count and never resets it", review())


class TestThrashTriggers(unittest.TestCase):
    def test_third_return_is_a_trigger_and_recommends_replan_or_split(self):
        t = review()
        self.assertIn("**a third return** — a mis-planned milestone", t)
        self.assertIn("recommend re-plan or split via `/milestone-plan`", t)

    def test_second_trigger_is_same_criterion_new_mechanism_same_shape(self):
        # Anchored across the shipped line break: truncating this to the
        # pre-wrap half would leave "of the same shape" deletable in silence,
        # and that clause is what separates a wrong design from three
        # unrelated defects.
        self.assertRegex(
            review(),
            r"the same acceptance criterion failing twice, each by a new mechanism of\s+"
            r"the same shape",
        )

    def test_second_trigger_remedy_is_the_recorded_alternative(self):
        self.assertIn(
            "reconsider the alternative the plan gate recorded against",
            review(),
        )

    def test_no_recorded_alternative_offers_brief_escalation(self):
        t = review()
        self.assertIn(
            "where it recorded none, offer escalation via `/milestone-brief`",
            t,
        )
        # Gated per instance, never automatic — D-004 survives this new door.
        self.assertIn("instance, never automatically", t)


class TestThrashRuleHasOneSurface(unittest.TestCase):
    PHRASE = "per milestone, never per cut"

    def surfaces(self):
        # Positively scoped to the plugin's own doctrine prose — every skill
        # and shared module, plus the README. The README is in scope because
        # that is exactly where M112 found doctrine going stale silently: a
        # milestone edited the skills and shipped a README saying the old
        # thing. `cairn/` is not swept — a tracking record quoting doctrine is
        # a legitimate record, not a second copy of the rule.
        repo = SKILLS.parent
        yield from sorted(SKILLS.rglob("*.md"))
        yield repo / "README.md"

    def test_rule_states_itself_in_exactly_one_file(self):
        repo = SKILLS.parent
        hits = sorted(
            p.relative_to(repo).as_posix()
            for p in self.surfaces()
            if self.PHRASE in p.read_text().lower()
        )
        # Bound the identity, not only the tally: a phrase that vanished from
        # review and reappeared elsewhere would still count one (M103 — bind
        # the record to its disposition, never assert the count alone).
        self.assertEqual(
            ["skills/milestone-review/SKILL.md"],
            hits,
            "the thrash rule must state itself in exactly one file — a second "
            "copy forks the rule and silently outlives an edit to the first",
        )


if __name__ == "__main__":
    unittest.main()
