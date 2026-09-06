"""Regression guard: the M179/D-134 optional candidate priority token.

Locks the rulebook paragraph in `tracking-rules.md` (AC1), the cairn-init
ROADMAP skeleton's row shape (AC2), and `/cairn-triage`'s reading of the
token (AC3).

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23) and steers clear of `**bold**` splits
(M26); phrases are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text().lower()


def rules():
    return read("shared", "tracking-rules.md")


class TestRulebookParagraph(unittest.TestCase):
    def test_paragraph_sits_in_sizing_section(self):
        text = rules()
        start = text.index("## sizing and the work tiers")
        end = text.index("## git and approval model")
        section = text[start:end]
        anchor = section.index("**search-first candidate creation.**")
        self.assertIn("**candidate priority token.**", section[anchor:])

    def test_token_vocabulary(self):
        self.assertIn("may open with `[high]` or `[low]`", rules())

    def test_untagged_reads_normal(self):
        self.assertIn("a row with neither reads as `normal`", rules())

    def test_section_order(self):
        self.assertIn("orders its rows high → normal → low", rules())

    def test_token_is_the_fact(self):
        self.assertIn("the token is the fact the order derives from", rules())


class TestInitSkeleton(unittest.TestCase):
    def skeleton(self):
        text = read("cairn-init", "SKILL.md")
        start = text.index("## candidates\n<!--")
        return text[start : text.index("-->", start)]

    def test_skeleton_shows_the_tagged_shape(self):
        self.assertIn("- [high] idea — added yyyy-mm-dd — links", self.skeleton())

    def test_skeleton_names_the_token_as_optional(self):
        self.assertIn("`[high]`/`[low]` or absent (`normal`)", self.skeleton())


class TestTriageReadsTheToken(unittest.TestCase):
    def triage(self):
        return read("cairn-triage", "SKILL.md")

    def step(self, n):
        text = self.triage()
        start = text.index(f"\n{n}. **")
        try:
            end = text.index(f"\n{n + 1}. **", start)
        except ValueError:
            end = len(text)
        return text[start:end]

    def test_enumeration_lists_each_rows_priority(self):
        self.assertIn("its priority (`high` / `normal` / `low`", self.step(1))

    def test_enumeration_reads_untagged_as_normal(self):
        self.assertIn("an untagged row is `normal`", self.step(1))

    def test_proposal_table_may_carry_a_priority_change(self):
        self.assertIn(
            "a `keep` or `compress` row may also carry a priority change", self.step(3)
        )

    def test_priority_change_is_the_carve_out(self):
        self.assertIn(
            "an accepted priority change on a `keep` row is the one edit this rule carves out",
            self.step(3),
        )

    def test_apply_orders_by_token_then_advisory(self):
        self.assertIn(
            "ordered by token — high → normal → low — then advisory within a level",
            self.step(4),
        )


if __name__ == "__main__":
    unittest.main()
