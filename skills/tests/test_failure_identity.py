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
heading-to-next-heading with both bounds asserted (M123). The premise and
the four operative-clause reads are sliced to the rule's own bullet so
dispersing any of them across unrelated bullets reds (round-1 F D19; the
header alone is section-read — it is the bullet locator, M117). The floor read anchors the
clause inside its "Always:" sentence via a wrap-spanning regex, because the
"What gets a test" section runs to EOF and a bare section-slice assertIn
passed with the clause relocated to an appended line (round-1 F D1). The
r-package and SKILL.md reads are whole-file assertIns, unscoped — each
pinned sentence occurs once in a file that has no competing section of the
same name. Heading locators are \n-anchored so a demoted `###` heading
cannot satisfy them (round-1 F D14). The intro premise spans line wraps and
is matched with `\s+` across the breaks (M95); every operative clause sits
on one physical line so its block stays registrable (M118). The slice-bounds
test's own asserts are heading-locator bounds, which take the by-hand
check instead of registry entries — blanking a bound crashes
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
    # A missing bullet MARKER returns "" so every clause assert FAILS
    # rather than the locator crashing — a crash is weak red (M117). (A
    # mutated section heading still errors these tests; the bounds test
    # fails properly there, the by-hand case.)
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
