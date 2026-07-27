r"""Regression guard: the M114 thrash rule in `/milestone-review` step 4.

The rule was unguarded prose until M114 — every phrase of it (`third trip`,
`queue another retry`, `mis-planned`, `re-plan or split`) occurred in the skill
and in no test, so deleting it outright kept the suite green. That is the gap
this file closes.

The properties asserted here, each separately deletable and so separately
pinned — the list IS the count, which is stated nowhere, because a stated
count goes stale against the file it describes and did so twice in this very
file (guard-doctrine §6):

  - returns are counted PER MILESTONE, not per cut, and the work log is named
    as the record a re-cut leaves standing;
  - a `/milestone-plan` re-cut increments that count and never resets it —
    the reading that cost intraclass M93 four of its seven returns;
  - trigger (a) is a THRESHOLD, holding on the third return and every one
    after, not a single moment;
  - trigger (b) is one criterion failing twice by a NEW MECHANISM OF THE SAME
    SHAPE, remedied by reconsidering the recorded alternative, or by an
    offered `/milestone-brief` escalation where none was recorded;
  - where both fire they COMPOSE — (a) takes the disposition, (b)'s diagnosis
    and escalation offer carry into the routing;
  - once a re-plan or split is spent, the exhaustion branch replaces the
    remedy, with its diagnosis and its remedy pinned separately.

This file once also carried a one-surface pin — an assert that the rule's
phrase occurs in exactly one file, so a restatement would red rather than
silently fork it. It was re-cut out at M114's third return: detecting a fork
by searching for its phrase needs the searcher to enumerate every rendering
the phrase can take, and each cut missed one the next review found. It is a
ROADMAP candidate, to be promoted on a rendering-independent approach rather
than a wider matcher.

Skill-prose guards read the file as one string and match case-insensitively.
An asserted phrase that can cross a line wrap is matched with `\s+` over the
break rather than truncated to its pre-wrap half (M105); adding a label to a
bullet reflowed two such anchors while this file was being written, and the
guards caught it (M104).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    # Path.read_text, not open() — the mutation engine patches only the former,
    # so a guard reading its target any other way is invisible to it (M100).
    return SKILLS.joinpath(*parts).read_text().lower()


def review():
    return read("milestone-review", "SKILL.md")


def plan():
    return read("milestone-plan", "SKILL.md")


class TestThrashCounting(unittest.TestCase):
    def test_returns_are_counted_per_milestone_not_per_cut(self):
        self.assertIn("count returns **per milestone, never per cut**", review())

    def test_the_rule_names_the_work_log_as_the_counting_source(self):
        # Without a named source, a reviewer arriving after a re-cut reads
        # current file state — unticked criteria, superseded tasks — and sees a
        # first pass. That is the per-cut reading the rule exists to stop, so
        # naming the surviving record is part of the rule, not commentary.
        t = review()
        self.assertIn("**count them in the work log**", t)
        self.assertRegex(t, r"supersedes the tasks and unticks every\s+criterion")

    def test_a_recut_increments_the_count_and_never_resets_it(self):
        # The load-bearing half. Without it "per milestone" is still readable
        # as "per milestone, restarting at each re-cut", which is exactly how
        # M93's counter was read: its pass 4 logged as the re-cut's first.
        self.assertIn("increments the count and never resets it", review())


class TestThrashTriggers(unittest.TestCase):
    def test_third_return_is_a_trigger_and_recommends_replan_or_split(self):
        t = review()
        self.assertRegex(
            t, r"\*\*\(a\) the third return, and every return after it\*\*"
        )
        # A threshold, not a moment. Without this the predicate reads as
        # "exactly the third", which reinstates the fire-once-then-go-silent
        # signature the rule exists to stop (RR05 Q1).
        self.assertIn("it is a threshold, not a single moment", t)
        # Pins the remedy WITH its routing target. Narrowed to the pre-wrap
        # half at pass 5, which let the target be changed to `/hotfix` green
        # (L1) — the M105 rule this file states, broken in this file.
        self.assertRegex(
            t,
            r"do not queue another retry; recommend re-plan or split via\s+`/milestone-plan`\.",
        )

    def test_second_trigger_is_same_criterion_new_mechanism_same_shape(self):
        # Anchored across the shipped line break: truncating this to the
        # pre-wrap half would leave "of the same shape" deletable in silence,
        # and that clause is what separates a wrong design from three
        # unrelated defects.
        self.assertRegex(
            review(),
            r"the same acceptance criterion failing twice, each by a new mechanism\s+"
            r"of the same shape",
        )

    def test_second_trigger_remedy_is_the_recorded_alternative(self):
        self.assertRegex(
            review(), r"reconsider the alternative the plan gate recorded\s+against"
        )

    def test_no_recorded_alternative_offers_brief_escalation(self):
        t = review()
        self.assertIn(
            "where it recorded none, offer escalation via `/milestone-brief`",
            t,
        )
        # Gated per instance, never automatic — D-004 survives this new door.
        self.assertIn("instance, never automatically", t)

    def test_review_names_the_work_log_as_where_the_record_is_read(self):
        # M117. Trigger (b)'s remedy needs a referent, and a referent needs a
        # place. Without the pointer the remedy names a record with no home,
        # which is how the fallback fired rather than the remedy downstream.
        self.assertIn("step 4 of `/milestone-plan` records it in the work log", review())



class TestPlanRecordsTheRejectedAlternative(unittest.TestCase):
    """M117: the upstream half — trigger (b)'s referent is created at plan time.

    Nothing obliged `/milestone-plan` to record the loser when it chose
    between approaches, so trigger (b) degraded to its escalation fallback on
    every milestone that had never recorded one. The obligation, its
    cardinality, its absence case and the template showing the form are pinned
    separately — described by a pointer rather than a count, since a stated
    count drifts against the class it describes (M116). The absence case
    carries the most: without it "no line" is ambiguous between "none was
    weighed" and "the plan forgot", and only the first is a correct read for
    trigger (b)'s fallback.
    """

    def test_plan_obliges_recording_the_rejected_alternative(self):
        # `read()` lowercases, so anchors here are lowercase; the mutation
        # registry blanks the real file and keeps the shipped case.
        t = plan()
        self.assertIn("**record the alternative the gate rejected.**", t)
        self.assertRegex(
            t,
            r"append a work-log line naming the\s+alternative rejected, why it "
            r"lost, and the class of evidence that would\s+falsify the choice",
        )

    def test_the_obligation_states_its_cardinality(self):
        # Without this the trailing clause deletes green and the obligation
        # reads as unbounded — "record the alternative" with no count is
        # satisfiable by one line per milestone, which is the granularity that
        # loses the second approach choice when a plan makes two.
        self.assertRegex(
            plan(),
            r"one line per approach choice the gate actually\s+weighed",
        )

    def test_a_plan_weighing_no_alternative_writes_no_line(self):
        self.assertRegex(
            plan(),
            r"a plan that weighed\s+no alternative writes no line: absence means "
            r"none was weighed",
        )

    def test_the_template_shows_the_record_and_its_cardinality(self):
        # AC4's template half. The template is what a plan author instantiates,
        # so an obligation stated only in the skill is one the author never
        # meets at the moment of writing the work log.
        t = read("shared", "templates", "milestone.md")
        self.assertRegex(
            t,
            r"the rejected-alternative record \(/milestone-plan\s+step 4\): one "
            r"per approach choice the gate actually weighed",
        )
        self.assertIn(
            "plan gate chose <approach> over <alternative> because <reason>", t
        )


class TestTriggersCompose(unittest.TestCase):
    """RR05 Q2/Q3: the two triggers compose; the remedy branches on exhaustion.

    The clause this replaced said trigger (a) won unconditionally. Because (a)
    is a threshold that never stops holding, that made (b)'s escalation offer
    unreachable from the third return onward while (a)'s only remedy was
    already spent — the trap review pass 4 found (J2).
    """

    def test_both_firing_composes_rather_than_one_winning(self):
        self.assertIn("**where both fire they compose.**", review())

    def test_composition_gives_a_the_disposition(self):
        self.assertRegex(
            review(), r"\(a\) governs the disposition — no further\s+retry"
        )

    def test_composition_names_the_routing_target(self):
        # The other half of the disposition sentence: without it the clause
        # prohibits a retry and names no destination (L3).
        self.assertRegex(
            review(), r"and the milestone routes through\s+`/milestone-plan` —"
        )

    def test_composition_carries_b_into_the_routing(self):
        # The half that was lost: (b)'s diagnosis and escalation offer must
        # survive the routing, not be discarded by (a) winning.
        self.assertRegex(
            review(),
            r"escalation offer carry into that routing rather than being\s+discarded",
        )

    def test_exhaustion_branch_states_its_diagnosis(self):
        # Diagnosis pinned separately from remedy (BC6): a rule that names the
        # exhausted case but prescribes nothing is the shape that trapped M114.
        self.assertRegex(
            review(),
            r"the work log already records a re-plan or split spent\s+on this milestone",
        )

    def test_exhaustion_branch_states_its_composed_remedy(self):
        # The positive half. Pass 5 pinned only the negation and the
        # prohibition, so the enumeration of what to actually DO could be
        # replaced by vague prose green (L2) — diagnosis with no remedy, the
        # shape this branch exists to forbid.
        self.assertRegex(
            review(),
            r"compose the routing chip from an offered\s+`/milestone-brief` escalation, "
            r"parking as `blocked` with the blocker named\s+in a work-log line, or "
            r"dropping at the user's explicit decision —",
        )

    def test_exhaustion_branch_states_its_remedy(self):
        t = review()
        self.assertIn("the remedy is no longer re-plan-or-split", t)
        self.assertRegex(t, r"never a\s+bare retry as the recommended option")


if __name__ == "__main__":
    unittest.main()
