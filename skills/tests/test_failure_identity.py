r"""Regression guard: the M136 failure-identity rule.

Target: the "An observed failure backs a claim only as the failure it is
verified to be." bullet in tracking-rules.md's "Universal tracking rules"
section, its test-floor rendering in "What gets a test", the r-package
profile's `expect_error` rendering, and the write-time pointer in
/milestone-implement step 4. The motivating failure is tidymedia M54
review 2: a wrong argument name produced a jobs-schema error that was read
as blame-attribution behavior, and the false claim propagated into NEWS,
that repo's ROADMAP, and a control test that passed on the schema error
independent of the behavior claimed.

Scoping, stated per read (round-1 F D2: a blanket both-bounds claim here
was false for three of four targets). The Universal-rules read is sliced
heading-to-next-heading with both bounds asserted (M123), and the five
clause reads are sliced to the rule's own bullet so dispersing the clauses
across unrelated bullets reds (round-1 F D19). The floor read anchors the
clause inside its "Always:" sentence via a wrap-spanning regex, because the
"What gets a test" section runs to EOF and a bare section-slice assertIn
passed with the clause relocated to an appended line (round-1 F D1). The
r-package and SKILL.md reads are whole-file assertIns, unscoped — each
pinned sentence occurs once in a file that has no competing section of the
same name. Heading locators are \n-anchored so a demoted `###` heading
cannot satisfy them (round-1 F D14). The intro premise spans line wraps and
is matched with `\s+` across the breaks (M95); every operative clause sits
on one physical line so its block stays registrable (M118). The slice-bounds
test's own asserts are heading-locator bounds, which take guard-doctrine
§2's by-hand check instead of registry entries — blanking a bound crashes
`index()` rather than failing the assert (M117; round-1 F D13 disposition).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    # Path.read_text, not open() — the mutation engine patches only the
    # former, so a guard reading any other way is invisible to it (M100).
    return SKILLS.joinpath(*parts).read_text()


def universal_rules_section():
    # Slice from the section's own \n-anchored heading to the next `## `
    # heading; the bounds test below proves the slice held at both ends.
    text = read("shared", "tracking-rules.md")
    start = text.index("\n## Universal tracking rules")
    rest = text[start + 1 :]
    end = rest.index("\n## ")
    return text[start + 1 : start + 1 + end]


def failure_identity_bullet():
    # Slice the rule's own bullet: from its `- **` line to the next
    # top-level `- **` bullet, so a clause asserted here must sit inside
    # this bullet, not merely somewhere in the section (round-1 F D19).
    # A missing bullet returns "" so every clause assert FAILS rather than
    # the locator crashing — a crash is weak red (M117).
    s = universal_rules_section()
    marker = (
        "- **An observed failure backs a claim only as the failure it is "
        "verified to be.**"
    )
    if marker not in s:
        return ""
    start = s.index(marker)
    rest = s[start + 1 :]
    end = rest.index("\n- **")
    return s[start : start + 1 + end]


class TestFailureIdentityRule(unittest.TestCase):
    def test_section_and_bullet_slices_hold_at_both_bounds(self):
        # \n-anchored heading must be unique in the file, or index() binds
        # a decoy first occurrence silently (M126); the slice must start at
        # the heading and contain no later `## ` heading (M123).
        text = read("shared", "tracking-rules.md")
        self.assertEqual(text.count("\n## Universal tracking rules"), 1)
        s = universal_rules_section()
        self.assertTrue(s.startswith("## Universal tracking rules"))
        self.assertNotIn("\n## ", s[1:])
        # The bullet slice: starts at the rule's own line, excludes the
        # following bullet ("Correcting a record proven false"), and holds
        # exactly one top-level bullet marker.
        b = failure_identity_bullet()
        self.assertTrue(b.startswith("- **An observed failure"))
        self.assertNotIn("Correcting a record proven false", b)
        self.assertEqual(b.count("\n- **"), 0)
        # The What-gets-a-test heading is likewise unique; its slice runs
        # to EOF today, so the floor test anchors inside the "Always:"
        # sentence rather than trusting the slice (round-1 F D1).
        self.assertEqual(text.count("\n## What gets a test"), 1)

    def test_rule_header_and_premise(self):
        # The header is asserted in the SECTION slice, not the bullet: the
        # header line is the bullet locator itself, so a bullet-scoped read
        # of it could only crash-red on header mutations (M117 weak red).
        b = universal_rules_section()
        self.assertIn(
            "**An observed failure backs a claim only as the failure it is "
            "verified to be.**",
            b,
        )
        # The premise — indistinguishability of a bare observation — spans
        # wraps; subject, predicate, and consequence pinned together so no
        # half survives alone (M131).
        self.assertRegex(
            b,
            r"An error, a refusal, or a red test reads the same whether it "
            r"is the behavior\s+under test or an artifact of malformed "
            r"inputs, so the observation alone\s+attributes nothing\.",
        )

    def test_identity_is_verified_before_the_claim(self):
        self.assertIn(
            "A claim resting on an observed failure verifies the failure's "
            "identity — its condition class, message, or signaling site — "
            "against the failure the claim is about, before the claim is "
            "written.",
            failure_identity_bullet(),
        )

    def test_distinguishing_step_is_explicit(self):
        self.assertIn(
            "The distinguishing step is explicit: confirm the inputs reach "
            "the behavior under test — the same inputs succeed when the "
            "condition under test is removed, or the input contract is "
            "checked against the artifact's own signature first.",
            failure_identity_bullet(),
        )

    def test_a_test_asserts_which_failure(self):
        self.assertIn(
            "A test asserting a failure asserts which failure, never that "
            "some failure occurred.",
            failure_identity_bullet(),
        )

    def test_a_control_passes_for_the_claims_reason(self):
        self.assertIn(
            "A discriminating test's passing control is shown to pass for "
            "the claim's reason, never merely to pass.",
            failure_identity_bullet(),
        )

    def test_error_branch_floor_requires_the_condition(self):
        # Anchored inside the "Always:" sentence, spanning its wrap: the
        # clause relocated anywhere else in the file no longer satisfies
        # this (round-1 F D1 showed a bare section assertIn did).
        self.assertRegex(
            read("shared", "tracking-rules.md"),
            r"Always: every exported/public function \(happy path,\s+every "
            r"error branch fired with its condition asserted — the test "
            r"names which failure, never bare failure — and the language's "
            r"edge cases\)",
        )

    def test_r_profile_renders_identity_for_expect_error(self):
        self.assertIn(
            "every `cli_abort()` branch fired and identified — "
            "`expect_error(class =)` or a message matcher, never bare "
            "`expect_error()`",
            read("shared", "profiles", "r-package.md"),
        )

    def test_implement_step4_carries_the_pointer(self):
        # The rule must be met at the moment a failure-backed claim gets
        # written, so the checkpoint-commit bullet — not only the
        # always-read rulebook — names it (the D-048 per-skill wiring
        # precedent, beside the derived-claims pointer).
        self.assertIn(
            "A claim resting on an observed failure follows the "
            "tracking-rules failure-identity rule: verified to be the "
            "failure the claim is about, never read off a bare error.",
            read("milestone-implement", "SKILL.md"),
        )


if __name__ == "__main__":
    unittest.main()
