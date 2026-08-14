r"""Regression guard: the M114 thrash rule, and the plan-time record it reads.

Three targets: `/milestone-review`'s step-4 thrash rule, `/milestone-plan`'s
step-4 obligation to record the alternative the gate rejected (M117), and the
milestone template that shows that record's form.

The rule was unguarded prose until M114 — every phrase of it (`third trip`,
`queue another retry`, `mis-planned`, `re-plan or split`) occurred in the skill
and in no test, so deleting it outright kept the suite green. That is the gap
this file closes.

The properties asserted here are each separately deletable and so separately
pinned. No count of them is stated, here or anywhere: a stated count goes
stale against the file it describes and did so twice in this very file
(guard-doctrine §6). The test methods are the enumeration — this list names
the review-side properties only, and M117's plan-side and template-side ones
are enumerated nowhere for the same reason:

  - returns are counted PER MILESTONE, not per cut, and the work log is named
    as the record a re-cut leaves standing;
  - a `/milestone-plan` re-cut increments that count and never resets it —
    the reading that cost intraclass M93 four of its seven returns;
  - trigger (a) is a THRESHOLD, holding on the third return and every one
    after, not a single moment;
  - trigger (b) is one criterion failing twice by a NEW MECHANISM OF THE SAME
    SHAPE, remedied by reconsidering the recorded alternative, or by an
    offered `/milestone-brief` escalation where none was recorded;
  - trigger (b) names WHERE that alternative is read from — the work log, at
    step 4 of `/milestone-plan` — since a remedy naming a record with no home
    is how the escalation fallback fired instead of the remedy (M117);
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


def implement():
    return read("milestone-implement", "SKILL.md")


# M139: a whole-file read proves a phrase exists SOMEWHERE, never that it is
# still in the rule it belongs to — relocating a sentence to another section
# leaves every such anchor matching (M123). The M139 asserts read a marker-
# bounded slice instead. A missing marker returns "", so the asserts that use
# it FAIL rather than crash; a crash is weak red (M117).
#
# The slice is per RULE, not per step (M139 review return 2). A first cut
# bounded it to the whole of step 5, which holds three rules — the return
# floor, the amendment return and the widening test — so a sentence moved from
# one of them into another stayed inside the slice and every assert stayed
# green. One such move left the section asserting both that returns under the
# floor join the defect count and that they never do, with the suite green.
# A slice coarser than the rule it localizes does not localize it.
REVIEW_FLOOR_START = "**return floor (m130).**"
REVIEW_AMENDMENT_START = "**amendment return (m130).**"
REVIEW_WIDENING_START = "**widening test (m139).**"
REVIEW_WIDENING_END = "6. final checkpoint commit on the branch."
IMPLEMENT_SUBSTANTIVE_START = "- *substantive* (a criterion or scope must change"
IMPLEMENT_SUBSTANTIVE_END = "- *the goal itself is wrong*"


def slice_between(text, start, end):
    i = text.find(start)
    j = text.find(end)
    if i == -1 or j == -1 or j <= i:
        return ""
    return text[i:j]


def review_floor():
    """The Return floor rule alone — step 5's first rule."""
    return slice_between(review(), REVIEW_FLOOR_START, REVIEW_AMENDMENT_START)


def review_amendment():
    """The Amendment return rule alone — step 5's second."""
    return slice_between(review(), REVIEW_AMENDMENT_START, REVIEW_WIDENING_START)


def review_widening():
    """The Widening test rule alone — step 5's third."""
    return slice_between(review(), REVIEW_WIDENING_START, REVIEW_WIDENING_END)


def implement_substantive():
    """The *Substantive* amendment bullet alone — step 6's second bullet."""
    return slice_between(
        implement(), IMPLEMENT_SUBSTANTIVE_START, IMPLEMENT_SUBSTANTIVE_END
    )


def normalize(text):
    """Collapse all whitespace to single spaces. The equality guards' one
    declared blind spot: a mutation expressible purely in collapsed
    whitespace passes (RR12)."""
    return " ".join(text.split())


# M140: the M139 repair-direction sentence gets its own sub-slice because the
# *Substantive* bullet holds six rules other milestones edit — a fixture over
# the whole bullet would freeze all of them (RR12 rec 3, D-103).
IMPLEMENT_M139_START = "an amendment executing a return reclassified"
IMPLEMENT_M139_END = "that grows a plan-owned section"


def implement_m139():
    """The M139 repair-direction sentence alone — a sub-slice of the
    *Substantive* bullet."""
    return slice_between(implement(), IMPLEMENT_M139_START, IMPLEMENT_M139_END)


# Fixtures: verbatim copies of each rule's text, taken from the target files'
# actual bytes (M95/M118) and compared modulo the read pipeline (lowercase +
# whitespace collapse). Editing a guarded rule reds the suite until the
# fixture is updated in the same commit — the two-site act D-103 chooses.
FLOOR_FIXTURE = normalize("""\
**Return floor (M130).** Over the actioned (≥80) list, a finding moves the
   milestone back to `in-progress` only when it demonstrates an acceptance
   criterion failing — inside its named procedure's domain, where the
   criterion names one, save where the widening test below carves that
   failure out as an amendment return —
   or when scored **≥90** on a defect in what the
   repo's deliverables do for their users (for this plugin: what the skills,
   hooks, and scripts do, not the doctrine prose about how work is verified),
   save where that same test carves that finding out.
   Every other actioned finding takes the triage above — fix now / follow-up
   / reject — with no status change, and is logged. The amendment return
   below is the one named exception to this "only when". A floor return
   takes step 4's exit — a work-log line naming exactly what failed, stop.
   The defect-return count the thrash rule reads is step-4 gate returns
   plus returns under this floor; amendment returns stay off it.
""".lower())

AMENDMENT_FIXTURE = normalize("""\
**Amendment return (M130).** A finding that shows the criterion itself
   is wrong — falsifying it only outside the domain of the procedure it
   names, or showing a criterion that names no procedure to be unbounded
   (the never-reinterpret rule's case, step 3), or meeting the widening
   test below, which carves that third case out of this clause's "only
   outside" — is evidence about the
   promise, not the work. It routes to the gated
   criterion-amendment protocol (`/milestone-implement` step 6) and
   re-review, the amendment the only work convened; status is set to
   `in-progress` for that amendment alone, and review stops there. Its
   work-log line carries a fixed
   shape — `amendment return: AC<N> — "<amended clause, verbatim>"` — and
   these lines are counted per milestone on their own track: never reset by
   a re-cut, and never added to the defect-return count (D-097 narrows
   D-064). A second amendment return naming the same AC<N> on one milestone
   stops — no further round is convened; the disposition goes to the user.
""".lower())

WIDENING_FIXTURE = normalize("""\
**Widening test (M139).** A finding demonstrating an acceptance criterion
   failing *inside* the domain its promise quantifies over is an amendment
   return rather than a defect return when the only repair available to it
   widens an enumeration whose membership is fixed by author recall rather
   than decided by a procedure over that domain. That discriminator is
   `/milestone-plan` step 4's, and the repair such a return takes is the one
   step 4 states; read it there rather than here. A return reclassified this
   way carries the fixed work-log shape above, counts on the amendment-return
   track under its second-occurrence stop, and never increments the
   defect-return count the thrash rule reads.
""".lower())

IMPLEMENT_M139_FIXTURE = normalize("""\
An amendment executing a return reclassified under `/milestone-review`'s
     widening test takes the narrowing repair `/milestone-plan` step 4's
     bounded-promise rule states; a wider enumeration is not an admissible
     amendment. An amendment
""".lower())


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
        t = review()
        self.assertIn("step 4 of `/milestone-plan` records it in the work log", t)
        # ...and it sits in trigger (b), not merely somewhere in the skill:
        # moved to (a) or to the composition paragraph, the whole-file assert
        # above stays green while the criterion naming trigger (b) goes false.
        trigger_b = t[t.index("- **(b) the same acceptance criterion"):
                      t.index("**where both fire they compose.**")]
        self.assertIn("records it in the work log", trigger_b)



class TestPlanRecordsTheRejectedAlternative(unittest.TestCase):
    """M117: the upstream half — trigger (b)'s referent is created at plan time.

    Nothing obliged `/milestone-plan` to record the loser when it chose
    between approaches, so trigger (b) degraded to its escalation fallback on
    every milestone that had never recorded one. Each span of the obligation
    is pinned by its own method — the methods below are the enumeration, and
    no sentence here restates them, since such a restatement drifts against
    the class the moment a span is added (M116; it drifted here once already).
    The absence case carries the most: without it "no line" is ambiguous
    between "none was weighed" and "the plan forgot", and only the first is a
    correct read for trigger (b)'s fallback.
    """

    def test_plan_obliges_recording_the_rejected_alternative(self):
        # `read()` lowercases, so anchors here are lowercase; the mutation
        # registry blanks the real file and keeps the shipped case.
        t = plan()
        self.assertIn("**record the alternative the gate rejected.**", t)
        self.assertRegex(
            t,
            r"append a work-log line naming the alternative rejected, why\s+it "
            r"lost, and the class of evidence that would falsify the choice",
        )

    def test_the_obligation_states_its_cardinality(self):
        # Without this the trailing clause deletes green and the obligation
        # reads as unbounded — "record the alternative" with no count is
        # satisfiable by one line per milestone, which is the granularity that
        # loses the second approach choice when a plan makes two.
        self.assertRegex(
            plan(),
            r"one\s+line per approach choice the gate actually weighed",
        )

    def test_the_obligation_sits_in_step_4(self):
        # The cross-file coupling breaks in exactly one direction: review's
        # pointer says "step 4 of `/milestone-plan`" and IS pinned, while the
        # bullet it points at was pinned only as free-floating text — movable
        # to any step, or out of the workflow entirely, with every other
        # assert green. Bound by the surrounding numbered steps rather than by
        # a line number, which drifts on any edit above.
        t = plan()
        start = t.index("4. **solidify autonomously**")
        end = t.index("5. **remainder ledger")
        self.assertIn(
            "**record the alternative the gate rejected.**", t[start:end]
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
        # Scoped to the work-log section's HTML comment, not the whole file:
        # as a template BODY line the form ships a placeholder into every
        # instantiated milestone, which is the state this assert exists to
        # keep out — and a whole-file match cannot tell the two apart.
        comment = t[t.index("## work log"):t.index("- yyyy-mm-dd: created by")]
        self.assertRegex(
            comment,
            r"one per approach choice the\s+gate actually weighed, none where "
            r"it weighed none",
        )
        self.assertRegex(
            comment,
            r"plan gate chose <approach> over <alternative> because\s+<reason>; "
            r"falsified by <evidence class>",
        )
        self.assertTrue(comment.rstrip().endswith("-->"), "form escaped the comment")
        # ...and appears ONLY there. Bounding the slice catches the form moving
        # up out of the body, but not a COPY left in the body below the
        # created-by line — which ships the placeholder just as surely, with
        # the slice asserts still green.
        self.assertEqual(
            1, t.count("plan gate chose <approach>"),
            "the example form must appear once, inside the work-log comment",
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


class TestReturnFloor(unittest.TestCase):
    """M130: review returns are reserved for breaches of bounded promises.

    Trigger: intraclass M100 — three full returns on an unbounded
    truthfulness criterion, each pass falsifying its predecessor's repair.
    The floor scopes returns to the actioned list; the amendment return
    routes the unbounded-criterion case without burning a defect strike.
    """

    def test_floor_governs_the_actioned_list_and_names_only_when(self):
        self.assertRegex(
            review(),
            r"\*\*return floor \(m130\)\.\*\* over the actioned \(≥80\) list, "
            r"a finding moves the\s+milestone back to `in-progress` only when "
            r"it demonstrates an acceptance\s+criterion failing",
        )

    def test_domain_limb_applies_only_where_a_procedure_is_named(self):
        self.assertRegex(
            review(),
            r"inside its named procedure's domain, where the\s+criterion names one",
        )

    def test_shipped_defect_limb_needs_90_and_excludes_doctrine_prose(self):
        # Without the exclusion, in this repo — whose shipped artifact IS
        # prose — limb 2 re-admits the prose-truthiness class the floor
        # exists to filter.
        t = review()
        self.assertRegex(
            t,
            r"scored \*\*≥90\*\* on a defect in what the\s+repo's deliverables "
            r"do for their users",
        )
        self.assertIn("not the doctrine prose about how work is verified", t)

    def test_sub_floor_findings_triage_with_no_status_change_and_are_logged(self):
        # IP3: filtered from the return path, never from the record.
        self.assertRegex(
            review(),
            r"every other actioned finding takes the triage above — fix now / "
            r"follow-up\s+/ reject — with no status change, and is logged",
        )

    def test_amendment_return_is_the_named_exception(self):
        # Without the named exception, the floor's "only when" forbids the
        # status change the amendment route requires — the unreachability the
        # M130 plan audit caught in the draft wording.
        self.assertRegex(
            review(),
            r"the amendment return\s+below is the one named exception",
        )

    def test_defect_return_count_is_step4_plus_floor_returns(self):
        # M130 review D1/D2/D8: the first cut said "only a return under this
        # floor joins the count", which read literally un-counted step-4 gate
        # returns — D-064's canonical case.
        self.assertRegex(
            review(),
            r"the defect-return count the thrash rule reads is step-4 gate "
            r"returns\s+plus returns under this floor; amendment returns "
            r"stay off it",
        )

    def test_floor_return_takes_step_4_exit(self):
        # M130 review D4/D5: a return with no stop and no work-log line is
        # both uncountable and followed by a merge chip.
        self.assertRegex(
            review(),
            r"a floor return\s+takes step 4's exit — a work-log line naming "
            r"exactly what failed, stop",
        )

    def test_thrash_count_is_of_defect_returns(self):
        self.assertRegex(
            review(),
            r"the count here is of defect returns; amendment returns run\s+on "
            r"their own track \(the step-5 return floor, m130\)",
        )

    def test_amendment_return_keys_on_the_criterion_being_wrong(self):
        # M130 review D3/D7: keyed only on "outside its named procedure's
        # domain", the route missed every criterion naming no procedure —
        # including the intraclass M100 trigger case — and collided with the
        # never-reinterpret rule; the keying now names both cases.
        self.assertRegex(
            review(),
            r"falsifying it only outside the domain of the procedure it\s+"
            r"names, or showing a criterion that names no procedure to be "
            r"unbounded\s+\(the never-reinterpret rule's case, step 3\)",
        )

    def test_amendment_route_convenes_the_amendment_alone(self):
        self.assertRegex(
            review(),
            r"routes to the gated\s+criterion-amendment protocol "
            r"\(`/milestone-implement` step 6\) and\s+re-review, the amendment "
            r"the only work convened; status is set to\s+`in-progress` for "
            r"that amendment alone, and review stops there",
        )

    def test_implement_step_6_writes_the_amendment_return_shape(self):
        # M130 review D6: the fixed shape was stated only in the skill that
        # never writes it; the producing skill now names it too.
        t = implement()
        self.assertRegex(
            t,
            r"amendment executing an amendment return from `/milestone-review` "
            r"writes\s+its work-log line in that skill's fixed shape",
        )
        self.assertIn(
            '`amendment return: ac<n> — "<amended clause, verbatim>"`', t
        )

    def test_amendment_return_work_log_line_has_a_fixed_shape(self):
        # The fixed shape is what makes the second-occurrence stop decidable
        # from the work log: the positional id names "the same criterion" and
        # the verbatim clause survives renumbering (M130 plan audit).
        self.assertRegex(
            review(),
            r'`amendment return: ac<n> — "<amended clause, verbatim>"`',
        )

    def test_amendment_returns_count_on_their_own_track(self):
        self.assertRegex(
            review(),
            r"counted per milestone on their own track: never reset by\s+a "
            r"re-cut, and never added to the defect-return count",
        )

    def test_second_amendment_return_on_the_same_id_stops(self):
        self.assertRegex(
            review(),
            r"a second amendment return naming the same ac<n> on one "
            r"milestone\s+stops",
        )


class TestWideningTest(unittest.TestCase):
    """M139/M140: the step-5 return rules and the implement-side repair
    direction, guarded by whole-slice equality (D-103, RR12).

    Trigger: intraclass M117's AC2 took four defect returns, the first three
    each answering a counterexample with a wider matcher. The narrowing repair
    existed at `/milestone-plan` step 4 the whole time; nothing at the return
    surface reached it, so getting there cost a full re-cut. M139 shipped the
    widening test and repair direction — and its fragment-regex guards then
    failed three review passes by one shape, an anchor's reach differing from
    the extent of the rule it pins: an unpinned subject and tail, a slice
    spanning three rules, text inserted between two pinned fragments
    inverting the rule with the suite green.

    RR12's diagnosis: a fragment-anchor family always leaves an unpinned
    complement, and the complement carries the next inversion. The fixed
    point is whole-slice equality — per rule, one method holding one
    assertEqual(normalize(<slice>), <fixture>) against a verbatim in-test
    copy. Totality: the pinned extent equals the slice. Granularity: the
    slice equals one rule.

    One assertion per test method: the mutation harness blanks a block and
    runs the whole named method, so a second assertion in the same method can
    red for the first and leave it unproven.
    """

    def test_review_floor_matches_its_fixture(self):
        self.assertEqual(normalize(review_floor()), FLOOR_FIXTURE)

    def test_review_amendment_matches_its_fixture(self):
        self.assertEqual(normalize(review_amendment()), AMENDMENT_FIXTURE)

    def test_review_widening_matches_its_fixture(self):
        self.assertEqual(normalize(review_widening()), WIDENING_FIXTURE)

    def test_implement_m139_matches_its_fixture(self):
        self.assertEqual(normalize(implement_m139()), IMPLEMENT_M139_FIXTURE)

    def test_review_floor_marker_is_unique(self):
        # A marker occurring twice binds its slice to the first occurrence, and
        # a decoy above the real block absorbs every check (M126). The markers
        # bounding the per-rule slices are each asserted unique on their own.
        self.assertEqual(review().count(REVIEW_FLOOR_START), 1)

    def test_review_amendment_marker_is_unique(self):
        self.assertEqual(review().count(REVIEW_AMENDMENT_START), 1)

    def test_review_widening_marker_is_unique(self):
        self.assertEqual(review().count(REVIEW_WIDENING_START), 1)

    def test_review_widening_end_marker_is_unique(self):
        self.assertEqual(review().count(REVIEW_WIDENING_END), 1)

    def test_implement_substantive_start_marker_is_unique(self):
        self.assertEqual(implement().count(IMPLEMENT_SUBSTANTIVE_START), 1)

    def test_implement_substantive_end_marker_is_unique(self):
        self.assertEqual(implement().count(IMPLEMENT_SUBSTANTIVE_END), 1)

    def test_implement_m139_start_marker_is_unique(self):
        self.assertEqual(implement().count(IMPLEMENT_M139_START), 1)

    def test_implement_m139_end_marker_is_unique(self):
        self.assertEqual(implement().count(IMPLEMENT_M139_END), 1)


class TestGuardDoctrineBanking(unittest.TestCase):
    """M140: the transferable lesson RR12 Q5 banks in guard-doctrine —
    the two-invariant statement (§1) and two blind-spot bullets (§2).
    One assertion per method, as above."""

    def doctrine(self):
        return read("shared", "guard-doctrine.md")

    def test_doctrine_states_totality(self):
        self.assertIn(
            "totality — the pinned extent equals the slice, leaving no "
            "unpinned complement between its boundaries —",
            self.doctrine(),
        )

    def test_doctrine_states_granularity(self):
        self.assertIn(
            "granularity — the slice equals one rule, so no position "
            "inside it changes which rule owns a sentence.",
            self.doctrine(),
        )

    def test_doctrine_names_the_insertion_blind_spot(self):
        self.assertRegex(
            self.doctrine(),
            r"\*\*blanking is not inserting either\.\*\* a registered block "
            r"proves deletion\s+reacts",
        )

    def test_doctrine_declares_the_normalization_blind_spot(self):
        self.assertRegex(
            self.doctrine(),
            r"\*\*whitespace normalization is a declared blind spot of "
            r"equality guards\.\*\*",
        )


if __name__ == "__main__":
    unittest.main()
