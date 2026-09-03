r"""Regression guard: the M142 stakes-tier rules in `/milestone-plan`.

Four rules, one target file: the step-2 surface-tier rule, the step-2
internal-tier criteria standard, the step-3 criteria audit's proportionality
question, and the step-2 collision check's checker-regress clause. Each was
authored at M142 from the measured failure that the plan gate as shipped
accepted internal-tier scopes whose criteria demand unbounded specification
(intraclass M120's four returns in one day; circumplex M72–M86's
fifteen-milestone checker arc).

The properties asserted here are each separately deletable and so separately
pinned; no count of them is stated. Per rule:

  - the surface-tier rule CLASSIFIES every deliverable as user-facing or
    internal, DEFINES internal by the absence of an external consumer with
    its example enumeration, DEFAULTS unclear-or-spanning deliverables to
    user-facing, and RECORDS the tier in the milestone file;
  - the internal-tier standard bounds a criterion's promise to a domain its
    named procedure enumerates directly, NAMES the three prohibited forms,
    directs repair by NARROWING or descoping and never widening, and stops
    at the promise/guard boundary (a detector's per-rendering positive
    controls stay mandated by their own doctrine);
  - the proportionality question is asked of EACH criterion, against the
    DECLARED tier, disposes an out-of-standard internal-tier criterion as a
    finding at the gate, and never relaxes the one-exemplar probe question
    it sits beside;
  - the checker-regress clause names the SHAPE (extending or hardening a
    previously-shipped checker over repo-internal artifacts), poses deletion
    as the RECOMMENDED option with hardening present but non-recommended,
    and carries the repair DISCRIMINATOR both ways — promise-unchanged
    repairs stay outside the shape, promise-widening ones are inside it
    however framed.

Each rule is read from a marker-bounded slice, not the whole file (M139: a
whole-file read proves a phrase exists SOMEWHERE, never that it is still in
the rule it belongs to). A missing marker returns "", so the asserts FAIL
rather than crash; a crash is weak red (M117). Marker uniqueness is asserted
(M126: an `index(marker)` locator silently binds to a decoy's first
occurrence until something says otherwise).

Skill-prose guards read the file as one string and match case-insensitively.
An asserted phrase that can cross a line wrap is matched with `\s+` over the
break rather than truncated to its pre-wrap half (M105).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def plan():
    # Path.read_text, not open() — the mutation engine patches only the
    # former, so a guard reading its target any other way is invisible to
    # it (M100).
    return (
        SKILLS.joinpath("milestone-plan", "SKILL.md").read_text().lower()
    )


SURFACE_START = "**surface tier (mandatory).**"
STANDARD_START = "**internal-tier criteria standard.**"
STANDARD_END = "**exploring a source corpus.**"
# The proportionality slice starts AFTER the one-exemplar probe sentence it
# sits beside, so the question's own opening clause is contained in the
# slice rather than serving as its bound — a registered block that doubles
# as a slice bound proves nothing about its own assert (M142 return, D9).
PROPORTION_START = "fixture rule applied to criteria)."
PROPORTION_END = "dispose of what it returns"
REGRESS_START = "**checker-regress shape.**"
REGRESS_END = "**harvest recent lessons"
# Step bounds: each rule slice is taken INSIDE its owning step's slice, not
# the whole file — a bare find() from position 0 resolves a rule relocated
# upward, entirely out of its step, and every whole-file anchor stays green
# (M142 return, D4: verified against the first cut of this file). The
# bounds are the steps' bold labels alone, without their ordinals — a
# renumbering of the workflow is unrelated to these rules and must not
# false-red them (M142 pass-2 R4).
STEP2_START = "**investigate first.**"
STEP2_END = "**question gate**"
STEP3_END = "**solidify autonomously**"
COLLISION_START = "**collision check (mandatory).**"


def slice_between(text, start, end):
    i = text.find(start)
    j = text.find(end)
    if i == -1 or j == -1 or j <= i:
        return ""
    return text[i:j]


def step2():
    """Step 2's whole slice — the surface-tier rule, the standard, and the
    collision check must all live inside it."""
    return slice_between(plan(), STEP2_START, STEP2_END)


def step3():
    """Step 3's whole slice — the criteria audit lives inside it."""
    return slice_between(plan(), STEP2_END, STEP3_END)


def surface_rule():
    """The surface-tier rule alone, scoped inside step 2 — its slice ends
    where the standard's begins, so a sentence drifting between the two
    rules reds (M139: the slice is per rule, not per step)."""
    return slice_between(step2(), SURFACE_START, STANDARD_START)


def standard_rule():
    """The internal-tier criteria standard alone, scoped inside step 2."""
    return slice_between(step2(), STANDARD_START, STANDARD_END)


def proportionality_rule():
    """The audit's proportionality question alone, scoped inside step 3 —
    bounded above by the one-exemplar probe sentence and below by the
    audit's own disposal sentence, both of which predate M142."""
    return slice_between(step3(), PROPORTION_START, PROPORTION_END)


def regress_rule():
    """The collision check's checker-regress clause alone, scoped inside
    step 2's collision check: the tail of the collision slice from the
    clause's own label (the collision slice already ends at the harvest
    marker, so no second end-bound is needed)."""
    collision = slice_between(step2(), COLLISION_START, REGRESS_END)
    i = collision.find(REGRESS_START)
    return "" if i == -1 else collision[i:]


class TestSurfaceTierRule(unittest.TestCase):
    def test_rule_classifies_every_deliverable_into_the_two_tiers(self):
        self.assertIn("deliverable as user-facing or internal", surface_rule())

    def test_classification_and_recording_are_obligations(self):
        # "Every plan classifies … and records" — softening either verb to
        # a "may"/"need not" form must red (M142 return, D7: the obligation
        # survived its own negation under the first cut).
        self.assertRegex(
            surface_rule(),
            r"every plan classifies the milestone's\s+"
            r"deliverable as user-facing or internal, and records the tier"
            r" and a\s+one-clause reason",
        )

    def test_internal_is_defined_by_absence_of_an_external_consumer(self):
        self.assertIn(
            "no external consumer of the repo relies on the", surface_rule()
        )

    def test_internal_definition_carries_its_example_enumeration(self):
        rule = surface_rule()
        self.assertIn(
            "dev tooling, data-generation scripts, in-repo checkers", rule
        )
        self.assertIn("over internal artifacts, tracking records", rule)

    def test_unclear_or_spanning_deliverables_default_to_user_facing(self):
        # The default direction is the deletable property: user-facing is
        # everything else, INCLUDING the unclear and the spanning case.
        self.assertRegex(
            surface_rule(),
            r"user-facing is everything\s+else, including any deliverable"
            r" whose tier is unclear or spans both",
        )

    def test_tier_is_recorded_in_the_milestone_file(self):
        self.assertIn(
            "one-clause reason in the milestone file's `surface tier:` header slot",
            surface_rule(),
        )


class TestInternalTierStandard(unittest.TestCase):
    def test_promise_is_bounded_to_a_directly_enumerated_domain(self):
        # The subject rides in the regex (M131: negating a phrase is not
        # inverting a rule — transpose the SUBJECT too).
        self.assertRegex(
            standard_rule(),
            r"an internal-tier acceptance\s+criterion's promise "
            r"quantifies over a domain its named procedure\s+"
            r"enumerates directly",
        )

    def test_standard_names_the_three_prohibited_forms(self):
        rule = standard_rule()
        self.assertIn("never an exemption registry, a per-rendering", rule)
        self.assertRegex(
            rule,
            r"a demonstration family spanning process or\s+"
            r"environment boundaries",
        )

    def test_repair_narrows_or_descopes_and_never_widens(self):
        rule = standard_rule()
        self.assertIn(
            "narrowing the promise (step 4's bounded-promise rule)", rule
        )
        self.assertIn("never by widening the specification", rule)

    def test_descoping_is_a_legal_repair_alternative(self):
        # The sentence's tail beyond the bounded-promise clause — deletable
        # green under the first cut (M142 return, P1: the M131/M132
        # prefix-without-tail class).
        self.assertRegex(
            standard_rule(),
            r"narrowing the promise \(step 4's bounded-promise rule\)"
            r" or by\s+descoping, never by",
        )

    def test_standard_stops_at_the_promise_guard_boundary(self):
        rule = standard_rule()
        self.assertIn(
            "a criterion's promise, never a guard's construction", rule
        )
        self.assertIn("controls stay mandated by their own doctrine", rule)


class TestCheckerRegressClause(unittest.TestCase):
    def test_clause_names_the_shape(self):
        rule = regress_rule()
        self.assertIn(
            "extending or hardening a checker that the roadmap or archive"
            " records",
            rule,
        )
        # Same-repo provenance is part of the shape (AC4) — "any repo at
        # any time" transposed green under the first cut (M142 return, D5).
        self.assertIn("an earlier milestone of the same repo shipping", rule)
        self.assertIn("verifies repo-internal artifacts", rule)

    def test_deletion_is_the_recommended_option(self):
        # "the gate poses" is an obligation — "may pose" softened green
        # under the first cut (M142 return, D8).
        self.assertIn("on such a hit the gate poses", regress_rule())
        self.assertIn(
            "simplifying or deleting the checker as the recommended option",
            regress_rule(),
        )

    def test_hardening_stays_present_but_non_recommended(self):
        self.assertIn(
            "hardening it as a present, non-recommended alternative",
            regress_rule(),
        )

    def test_promise_unchanged_repairs_stay_outside_the_shape(self):
        self.assertIn(
            "leaves the checker's promise unchanged stays outside the shape",
            regress_rule(),
        )

    def test_promise_widening_is_the_shape_however_framed(self):
        self.assertRegex(
            regress_rule(),
            r"one that widens the checker's promise is\s+"
            r"the regress shape however it is framed",
        )


# Fixtures: verbatim copies of each rule's text, taken from the target
# file's actual bytes (M95/M118) and compared modulo the read pipeline
# (lowercase + whitespace collapse). Editing a guarded rule reds the suite
# until the fixture is updated in the same commit — the two-site act D-103
# chooses. Adopted at M142 defect return #2: two rounds of per-property
# pins each left members of the mutation family unpinned (R1-R3 after
# D4-D8/P1); equality over the slice settles the in-slice domain by
# procedure. The pins above stay for defect LOCALIZATION; the fixtures
# catch what they leave unpinned (M143 F10). Declared blind spot: a
# mutation expressible purely in collapsed whitespace passes (RR12).


def normalize(text):
    """Collapse all whitespace to single spaces."""
    return " ".join(text.split())


SURFACE_FIXTURE = normalize("""\
**Surface tier (mandatory).** Every plan classifies the milestone's
   deliverable as user-facing or internal, and records the tier and a
   one-clause reason in the milestone file's `Surface tier:` header slot.
   Internal means no external consumer of the repo relies on the
   deliverable — dev tooling, data-generation scripts, in-repo checkers
   over internal artifacts, tracking records; user-facing is everything
   else, including any deliverable whose tier is unclear or spans both.
""".lower())

STANDARD_FIXTURE = normalize("""\
**Internal-tier criteria standard.** An internal-tier acceptance
   criterion's promise quantifies over a domain its named procedure
   enumerates directly — never an exemption registry, a per-rendering
   enumeration, or a demonstration family spanning process or
   environment boundaries. A draft needing those is repaired at this
   gate by narrowing the promise (step 4's bounded-promise rule) or by
   descoping, never by widening the specification. The standard governs
   a criterion's promise, never a guard's construction — a detector's
   per-rendering positive controls stay mandated by their own doctrine.
""".lower())

PROPORTION_FIXTURE = normalize("""\
fixture rule applied to criteria).
   The audit also asks a proportionality question of each criterion:
   is the promise's domain proportionate to the declared surface tier
   (the step-2 rule)? An internal-tier criterion outside the
   internal-tier criteria standard is a finding, disposed at this gate
   like the audit's other findings; the question governs promises and
   never relaxes the probe question above.
""".lower())

REGRESS_FIXTURE = normalize("""\
**Checker-regress shape.** The sweep also names this shape: a scope
   extending or hardening a checker that the ROADMAP or archive records
   an earlier milestone of the same repo shipping, where that checker
   verifies repo-internal artifacts. On such a hit the gate poses
   simplifying or deleting the checker as the recommended option and
   hardening it as a present, non-recommended alternative. A repair that
   leaves the checker's promise unchanged stays outside the shape
   (D-090's Untouched clause); one that widens the checker's promise is
   the regress shape however it is framed.
""".lower())


class TestWholeSliceFixtures(unittest.TestCase):
    """Byte-equality (modulo the read pipeline) per rule slice — any
    in-slice mutation reds, enumerated or not."""

    def test_surface_rule_matches_its_fixture(self):
        self.assertEqual(normalize(surface_rule()), SURFACE_FIXTURE)

    def test_standard_rule_matches_its_fixture(self):
        self.assertEqual(normalize(standard_rule()), STANDARD_FIXTURE)


    def test_regress_rule_matches_its_fixture(self):
        self.assertEqual(normalize(regress_rule()), REGRESS_FIXTURE)


if __name__ == "__main__":
    unittest.main()
