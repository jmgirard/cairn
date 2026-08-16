r"""Regression guard: the M134 derived-claims rule, in its M146 reduced form.

Targets: the derived-claims and derived-figures bullets in the reduced
tracking-rules.md "Universal tracking rules" section (headline, the named
tracking-records exemption, and the figures rule's two legal forms — each a
single-line fragment so its block stays registrable in the mutation
harness), plus the /milestone-implement step-4 pointer. The motivating
failure is intraclass M103: review returns whose actioned defects were all
prose composed from the author's model while the code survived both passes.
M146 rewrote the rule text; the pre-M146 per-clause pins are in git.

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


class TestDerivedClaimsRule(unittest.TestCase):
    def test_section_slice_holds_at_both_bounds(self):
        # The heading must be unique in the file, or index() binds a decoy
        # first occurrence silently (M126); the slice must start at the
        # heading and contain no later `## ` heading (M123, both bounds).
        text = read("shared", "tracking-rules.md")
        self.assertEqual(text.count("## Universal tracking rules"), 1)
        s = universal_rules_section()
        self.assertTrue(s.startswith("## Universal tracking rules"))
        self.assertNotIn("\n## ", s[1:])


    def test_rule_states_derive_never_compose(self):
        # The headline and its rule name, inside the sliced section — the
        # fragment sits on one physical line so the harness can blank it.
        self.assertIn(
            "derived, never composed** (the derived-claims rule)",
            universal_rules_section(),
        )

    def test_tracking_records_exemption_names_its_members(self):
        # D-116's narrowing: the exemption names the rules it covers rather
        # than pointing positionally (M146 review finding O13).
        self.assertIn(
            "Tracking records are exempt from this rule and from the "
            "derived-figures and",
            universal_rules_section(),
        )

    def test_derived_figures_rule_states_its_headline(self):
        self.assertIn(
            "pinned or procedural, never free-standing",
            universal_rules_section(),
        )

    def test_implement_step4_carries_the_pointer(self):
        # The rule must be met at the moment prose gets written, so the
        # checkpoint-commit bullet — not only the always-read rulebook —
        # names it (the D-048 per-skill wiring precedent).
        self.assertIn(
            "Prose the commit adds about an artifact's behavior follows the "
            "tracking-rules derived-claims rule: derived from the artifact, "
            "never composed.",
            read("milestone-implement", "SKILL.md"),
        )


if __name__ == "__main__":
    unittest.main()
