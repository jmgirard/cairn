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

M146 rewrote the rule to its reduced form; the pre-M146 per-clause pins are
in git. The surviving reads: the rule's own bullet sliced from the reduced
Universal-rules section (identity clause + passing-control clause, each a
single-line fragment so its block stays registrable), the r-package
profile's `expect_error` rendering, and the /milestone-implement step-4
pointer — the last two whole-file assertIns, each pinned sentence occurring
once in its file.

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
    # A missing bullet MARKER returns "" so every clause assert FAILS
    # rather than the locator crashing — a crash is weak red (M117). (A
    # mutated section heading still errors these tests; the bounds test
    # fails properly there, the by-hand case.)
    s = universal_rules_section()
    marker = (
        "- **An observed failure backs a claim only as the failure it is "
        "verified to be** (the failure-identity rule)"
    )
    if marker not in s:
        return ""
    start = s.index(marker)
    rest = s[start + 1 :]
    end = rest.index("\n- **")
    return s[start : start + 1 + end]


class TestFailureIdentityRule(unittest.TestCase):

    def test_rule_bullet_present_with_identity_clause(self):
        b = failure_identity_bullet()
        self.assertTrue(b, "failure-identity bullet not found in the section")
        self.assertIn("condition class, message, or signaling site", b)

    def test_passing_control_clause_present(self):
        # Restored at the M146 review (finding O9): a discriminating test's
        # control passes for the claim's reason, never merely passes.
        self.assertIn(
            "discriminating test's passing control is shown to pass for the "
            "claim's reason",
            failure_identity_bullet(),
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
