r"""Regression guard: the M134 derived-claims rule.

Target: the "Branch-added behavior claims are derived, never composed."
bullet in tracking-rules.md's "Universal tracking rules" section — three
operative clauses, each pinned separately because each is separately
deletable: (a) derive-don't-compose (a branch-added claim about what an
artifact does or contains is written against an execution's observed output
or a same-session read of the artifact), (b) restatement-is-not-written, and
(c) pointer-over-enumeration. The motivating failure is intraclass M103: two
review returns whose actioned defects were all prose composed from the
author's model — an evidence line claiming a seeded run that ran unseeded, a
NEWS sentence false whenever the caller sets a seed, a stale comment, a
wrong @details claim — while the code survived both passes.

Reads are scoped to the section the acceptance criterion names, with both
bounds asserted (M123: an anchor proves the phrase exists SOMEWHERE in what
you handed it). Clause (a) spans line wraps and is matched with `\s+` across
the breaks (M95); clauses (b) and (c) sit on one physical line each so their
blocks stay registrable in the mutation harness (M118).

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

    def test_clause_a_derive_dont_compose(self):
        s = universal_rules_section()
        self.assertIn(
            "**Branch-added behavior claims are derived, never composed.**", s
        )
        # Subject (which prose, on which surfaces), predicate (written
        # against execution output or a same-session read), and tail (the
        # negative) pinned together so no half survives alone (M131).
        self.assertRegex(
            s,
            r"A prose claim\s+the branch adds about what an artifact does or "
            r"contains — in tracking\s+records, code comments, docstrings, "
            r"changelog entries, or docs — is written\s+against an "
            r"execution's observed output or a same-session read of the\s+"
            r"artifact, never composed from recollection or expectation\.",
        )

    def test_clause_b_restatement_is_not_written(self):
        self.assertIn(
            "Branch-added prose that restates what its cited artifact "
            "already shows is not written — a cross-reference replaces it.",
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

    def test_changelog_claims_are_documented_claims(self):
        # Scoped to the "What gets a test" section (M123, both bounds via
        # the same slice discipline: heading unique, no later `## ` before
        # the sentence).
        text = read("shared", "tracking-rules.md")
        self.assertEqual(text.count("\n## What gets a test"), 1)
        section = text[text.index("\n## What gets a test") :]
        nxt = section[1:].find("\n## ")
        if nxt != -1:
            section = section[: nxt + 1]
        self.assertIn(
            "A changelog entry asserting a behavior requires a test that "
            "fails without that behavior, or the entry narrows to what a "
            "named test enforces.",
            section,
        )

    def test_clause_c_pointer_over_enumeration(self):
        self.assertIn(
            "A claim that would enumerate an artifact's members is written "
            "as a pointer to the artifact, except where the enumeration is "
            "itself the deliverable.",
            universal_rules_section(),
        )


if __name__ == "__main__":
    unittest.main()
