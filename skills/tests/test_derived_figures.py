r"""Regression guard: the M137 derived-figures rule.

Target: the "A derived figure is pinned or procedural, never free-standing."
bullet in tracking-rules.md's "Universal tracking rules" section — four
operative clauses, each pinned separately because each is separately
deletable: the domain sentence (which figures, on which surfaces), the
pinned form, the procedural form, and the free-standing defect. The
motivating failure class is D-099's: hand-written derived counts stranded
by the next edit to what they measure.

Reads are scoped to the rule's own bullet via a marker locator that returns
'' when the marker is missing, so downstream asserts FAIL rather than crash
(M117/M136); the marker is asserted unique in the file (M126) and the slice
is tested at both bounds (M123).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

HEADLINE = "**A derived figure is pinned or procedural, never free-standing.**"


def read(*parts):
    # Path.read_text, not open() — the mutation engine patches only the
    # former, so a guard reading any other way is invisible to it (M100).
    return SKILLS.joinpath(*parts).read_text()


def figures_bullet():
    """The rule's own bullet — headline marker to the next bullet start —
    or '' when the marker is missing, so asserts FAIL rather than crash."""
    text = read("shared", "tracking-rules.md")
    start = text.find("- " + HEADLINE)
    if start == -1:
        return ""
    rest = text[start + 2 :]
    end = rest.find("\n- **")
    return text[start : start + 2 + end] if end != -1 else text[start:]


class TestDerivedFiguresRule(unittest.TestCase):
    def test_bullet_slice_holds_at_both_bounds(self):
        # The marker must be unique in the file, or find() binds a decoy
        # first occurrence silently (M126); the slice must start at the
        # headline and stop before the next bullet — proven by content on
        # both sides of the upper bound (M123/M136: relocation to a
        # following bullet must not read as coverage).
        text = read("shared", "tracking-rules.md")
        self.assertEqual(text.count("- " + HEADLINE), 1)
        s = figures_bullet()
        self.assertTrue(s.startswith("- " + HEADLINE))
        self.assertNotIn("\n- **", s[2:])
        self.assertIn("free-standing hand-written figure", s)
        self.assertNotIn("An observed failure backs a claim", s)

    def test_domain_sentence(self):
        # Subject and surfaces pinned with the headline's own tail so no
        # half survives alone (M131); spans wraps with \s+ (M95).
        s = figures_bullet()
        self.assertIn(HEADLINE, s)
        self.assertRegex(
            s,
            r"A\s+count or figure derived from the repo's artifacts — in "
            r"tracking records,\s+code comments, docstrings, changelog "
            r"entries, or docs — takes one of two\s+forms\.",
        )

    def test_pinned_form(self):
        self.assertIn(
            "Pinned: the figure stands beside the procedure that produced "
            "it and the commit or dated artifact it was measured at, a "
            "dated observation rather than a standing fact.",
            figures_bullet(),
        )

    def test_procedural_form(self):
        self.assertIn(
            'Procedural: the figure is replaced by its derivation ("the '
            "sites matched by `grep -n <pattern>`\"), and no figure is "
            "stated.",
            figures_bullet(),
        )

    def test_free_standing_defect(self):
        self.assertIn(
            "The free-standing hand-written figure is the defect this rule "
            "deletes: the next edit to what it measures strands it, and it "
            "reads as current until a review reds on it.",
            figures_bullet(),
        )


if __name__ == "__main__":
    unittest.main()
