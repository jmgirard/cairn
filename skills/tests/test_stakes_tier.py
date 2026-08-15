r"""Regression guard: the M142 stakes-tier rules in `/milestone-plan`.

Four rules, one target file: the step-2 surface-tier rule, the step-2
internal-tier criteria standard, the step-3 criteria audit's proportionality
question, and the step-2 collision check's checker-regress clause. Each was
authored at M142 from the measured failure that the plan gate as shipped
accepted internal-tier scopes whose criteria demand unbounded specification
(intraclass M120's four returns in one day; circumplex M72–M86's
fifteen-milestone checker arc).

The properties asserted here are each separately deletable and so separately
pinned; no count of them is stated (guard-doctrine §6). Per rule:

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
PROPORTION_START = "the audit also asks a proportionality question"
PROPORTION_END = "dispose of what it returns"
REGRESS_START = "**checker-regress shape.**"
REGRESS_END = "**harvest recent lessons"


def slice_between(text, start, end):
    i = text.find(start)
    j = text.find(end)
    if i == -1 or j == -1 or j <= i:
        return ""
    return text[i:j]


def surface_rule():
    """The surface-tier rule alone — its slice ends where the standard's
    begins, so a sentence drifting between the two rules reds (M139: the
    slice is per rule, not per step)."""
    return slice_between(plan(), SURFACE_START, STANDARD_START)


def standard_rule():
    """The internal-tier criteria standard alone."""
    return slice_between(plan(), STANDARD_START, STANDARD_END)


def proportionality_rule():
    """The audit's proportionality question alone — bounded below by the
    audit's own disposal sentence, which predates M142."""
    return slice_between(plan(), PROPORTION_START, PROPORTION_END)


def regress_rule():
    """The collision check's checker-regress clause alone."""
    return slice_between(plan(), REGRESS_START, REGRESS_END)


class TestMarkersUnique(unittest.TestCase):
    """Each slice marker occurs exactly once, so no decoy can absorb the
    slice while the real rule drifts (M126)."""

    def test_each_marker_occurs_exactly_once(self):
        text = plan()
        for marker in (
            SURFACE_START,
            STANDARD_START,
            STANDARD_END,
            PROPORTION_START,
            PROPORTION_END,
            REGRESS_START,
            REGRESS_END,
        ):
            self.assertEqual(
                text.count(marker), 1, f"marker not unique: {marker!r}"
            )


class TestSurfaceTierRule(unittest.TestCase):
    def test_rule_classifies_every_deliverable_into_the_two_tiers(self):
        self.assertIn("deliverable as user-facing or internal", surface_rule())

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
            "one-clause reason in the milestone file's goal or scope prose",
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

    def test_standard_stops_at_the_promise_guard_boundary(self):
        rule = standard_rule()
        self.assertIn(
            "a criterion's promise, never a guard's construction", rule
        )
        self.assertIn("controls stay mandated by their own doctrine", rule)


class TestProportionalityQuestion(unittest.TestCase):
    def test_question_is_asked_of_each_criterion(self):
        self.assertIn(
            "asks a proportionality question of each criterion",
            proportionality_rule(),
        )

    def test_question_measures_the_domain_against_the_declared_tier(self):
        self.assertIn(
            "is the promise's domain proportionate to the declared"
            " surface tier",
            proportionality_rule(),
        )

    def test_out_of_standard_internal_criterion_is_a_gate_finding(self):
        self.assertIn(
            "is a finding, disposed at this gate", proportionality_rule()
        )

    def test_question_never_relaxes_the_one_exemplar_probe(self):
        self.assertIn(
            "never relaxes the probe question above", proportionality_rule()
        )


class TestCheckerRegressClause(unittest.TestCase):
    def test_clause_names_the_shape(self):
        rule = regress_rule()
        self.assertIn(
            "extending or hardening a checker that the roadmap or archive"
            " records",
            rule,
        )
        self.assertIn("verifies repo-internal artifacts", rule)

    def test_deletion_is_the_recommended_option(self):
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


if __name__ == "__main__":
    unittest.main()
