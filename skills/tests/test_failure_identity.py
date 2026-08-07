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

Reads are scoped to the section the acceptance criterion names, with both
bounds asserted (M123). The intro sentence spans line wraps and is matched
with `\s+` across the breaks (M95); every operative clause sits on one
physical line so its block stays registrable in the mutation harness (M118).

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
    # Slice from the section's own heading to the next `## ` heading; the
    # bounds test below proves the slice held at both ends.
    text = read("shared", "tracking-rules.md")
    start = text.index("## Universal tracking rules")
    rest = text[start + 1 :]
    end = rest.index("\n## ")
    return text[start : start + 1 + end]


def what_gets_a_test_section():
    text = read("shared", "tracking-rules.md")
    start = text.index("\n## What gets a test")
    section = text[start:]
    nxt = section[1:].find("\n## ")
    if nxt != -1:
        section = section[: nxt + 1]
    return section


class TestFailureIdentityRule(unittest.TestCase):
    def test_section_slices_hold_at_both_bounds(self):
        # Heading unique or index() binds a decoy first occurrence (M126);
        # slice starts at the heading and holds no later `## ` (M123).
        text = read("shared", "tracking-rules.md")
        self.assertEqual(text.count("## Universal tracking rules"), 1)
        s = universal_rules_section()
        self.assertTrue(s.startswith("## Universal tracking rules"))
        self.assertNotIn("\n## ", s[1:])
        self.assertEqual(text.count("\n## What gets a test"), 1)

    def test_rule_header_and_premise(self):
        s = universal_rules_section()
        self.assertIn(
            "**An observed failure backs a claim only as the failure it is "
            "verified to be.**",
            s,
        )
        # The premise — indistinguishability of a bare observation — spans
        # wraps; subject, predicate, and consequence pinned together so no
        # half survives alone (M131).
        self.assertRegex(
            s,
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
            universal_rules_section(),
        )

    def test_distinguishing_step_is_explicit(self):
        self.assertIn(
            "The distinguishing step is explicit: confirm the inputs reach "
            "the behavior under test — the same inputs succeed when the "
            "condition under test is removed, or the input contract is "
            "checked against the artifact's own signature first.",
            universal_rules_section(),
        )

    def test_a_test_asserts_which_failure(self):
        self.assertIn(
            "A test asserting a failure asserts which failure, never that "
            "some failure occurred.",
            universal_rules_section(),
        )

    def test_a_control_passes_for_the_claims_reason(self):
        self.assertIn(
            "A discriminating test's passing control is shown to pass for "
            "the claim's reason, never merely to pass.",
            universal_rules_section(),
        )

    def test_error_branch_floor_requires_the_condition(self):
        self.assertIn(
            "every error branch fired with its condition asserted — the "
            "test names which failure, never bare failure — and the "
            "language's edge cases",
            what_gets_a_test_section(),
        )

    def test_r_profile_renders_identity_for_expect_error(self):
        self.assertIn(
            "every `cli_abort()` branch fired and identified — "
            "`expect_error(class = )` or a message matcher, never bare "
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
