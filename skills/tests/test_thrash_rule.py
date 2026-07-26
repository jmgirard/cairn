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
so an asserted phrase normally sits on a single source line (M23). Two
assertions deliberately do not: the second trigger wraps in the shipped file
and is matched with `\\s+` across the break (M105), and the one-surface pin
matches over `normalize()` below, which flattens the renderings a doctrine
phrase can legitimately take.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Rendering normalization for the one-surface pin.
#
# Three axes, each learned from a rendering that defeated a PREVIOUS cut of
# this guard rather than imagined up front: a line wrap (review pass 1, F1),
# a blockquote continuation marker (pass 2, G2), and emphasis applied to part
# of the phrase rather than all of it (pass 2, G3). Two cuts widened the
# matcher and each bought the next mechanism, which is the thrash rule's own
# trigger (b) — so the durable part is not this regex but the RENDERINGS
# corpus below, which exercises it per guard-doctrine §3.
# --------------------------------------------------------------------------
_QUOTE_MARK = re.compile(r"^[ \t]*>+[ \t]?", re.M)
_EMPHASIS = re.compile(r"[*_`]+")
_WHITESPACE = re.compile(r"\s+")


def normalize(text):
    """Flatten wrapping, blockquote markers and emphasis; lowercase."""
    text = _QUOTE_MARK.sub("", text.lower())
    text = _EMPHASIS.sub("", text)
    return _WHITESPACE.sub(" ", text)


# Word-bounded, not a bare substring: without `\b` the phrase matches inside a
# longer word, so "never per cutover" reads as a copy of the rule. Found by
# the negative controls below — the positives never could, since normalization
# only deletes characters and so can only ever turn a match INTO a non-match.
_STATES_RULE = re.compile(r"\bper milestone, never per cut\b")


def states_the_rule(text):
    """True if `text` states the rule's counting phrase, in any rendering.

    One definition, used by both the one-surface pin and the controls that
    exercise it — a control checking a different predicate than the pin would
    prove nothing about the pin.
    """
    return _STATES_RULE.search(normalize(text)) is not None


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


PHRASE = "per milestone, never per cut"

# Positive controls (guard-doctrine §3): every rendering the phrase can take
# on the swept surfaces. These live IN the test because external verification
# is discarded the moment it finishes, and because the author of a detector is
# exactly who cannot enumerate the renderings it misses — two cuts of this
# guard proved that twice. A rendering found by a future review is added here,
# not argued about.
RENDERINGS = {
    "plain": "count returns per milestone, never per cut.",
    "shipped form (whole phrase bold)": "Count returns **per milestone, never per cut** — a",
    "wrap after 'per'": "per\n  milestone, never per cut",
    "wrap after the comma": "per milestone,\n     never per cut",
    "wrap before 'cut'": "**per milestone, never per\ncut**",
    "blockquote, wrapped": "> count returns per milestone,\n> never per cut.",
    "nested blockquote": ">> per milestone,\n>>   never per cut",
    "emphasis on part of the phrase": "**per milestone**, never **per cut**",
    "emphasis on one word": "per milestone, **never** per cut",
    "code span": "`per milestone, never per cut`",
    "blockquote + bold + wrap": "> **per milestone,**\n>   never per cut",
}

# Negative controls. Without these the positives could all pass by a
# normalizer that flattened everything into a match — the "positive signal
# must prove the work happened" corollary, applied to normalization itself.
NON_FORKS = {
    "different subject": "count returns per session, never per cut",
    "different unit": "per milestone, never per commit",
    "reversed": "per cut, never per milestone",
    "partial quotation": "returns are counted per milestone, and that is all",
    "words present but not the phrase": (
        "per milestone the count holds; it is never reset, and per cut it is not"
    ),
    # Word-boundary cases. These are the controls that earned their keep: the
    # first cut of this matcher was a bare substring test and reported a copy
    # for every one of them.
    "longer word after the phrase": "per milestone, never per cutover",
    "longer word, mid-sentence": "per milestone, never per cutting corners",
    "longer word before the phrase": "hyper milestone, never per cut",
}


class TestDetectorSeesEveryRendering(unittest.TestCase):
    """§3 positive controls for the one-surface detector's matcher.

    The pin below is only as good as its matcher, and a matcher is only as
    good as the renderings it has actually been run against. Pass 1 shipped a
    literal that missed a wrap; pass 2 shipped `\\s+` that missed a blockquote
    marker and mid-phrase emphasis. Both were verified externally, and both
    verifications were thrown away. These stay.
    """

    def test_every_rendering_is_seen(self):
        for name, text in RENDERINGS.items():
            with self.subTest(rendering=name):
                self.assertTrue(
                    states_the_rule(text),
                    f"the detector cannot see a fork rendered as {name!r} — "
                    "a copy in that form would fork the rule silently",
                )

    def test_non_forks_are_not_seen(self):
        for name, text in NON_FORKS.items():
            with self.subTest(rendering=name):
                self.assertFalse(
                    states_the_rule(text),
                    f"the detector is too loose: {name!r} is not a copy of the "
                    "rule but the detector reports one",
                )


class TestThrashRuleHasOneSurface(unittest.TestCase):

    def surfaces(self):
        # Positively scoped to the plugin's LIVE doctrine prose: every skill and
        # shared module, plus the two always-read root files. README is in scope
        # because M112 found doctrine going stale exactly there; CLAUDE.md
        # because it is the router every session reads (added review pass 1, F2).
        # Two deliberate omissions. `CHANGELOG.md` is a history file, the one
        # thing guard-doctrine §7 says an exclusion list may name. `cairn/` is
        # out because `DECISIONS.md` legitimately quotes the rule it records and
        # IP4 makes that permanent — a literally repo-wide assertion is
        # unsatisfiable today and gets less satisfiable with every D-entry.
        repo = SKILLS.parent
        yield from sorted(SKILLS.rglob("*.md"))
        yield repo / "README.md"
        yield repo / "CLAUDE.md"

    def test_rule_states_itself_in_exactly_one_file(self):
        repo = SKILLS.parent
        hits = sorted(
            p.relative_to(repo).as_posix()
            for p in self.surfaces()
            if states_the_rule(p.read_text())
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
