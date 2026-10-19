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
        self.assertIn("orders its rows high → normal → low → parked", rules())

    def test_parked_is_the_fourth_level(self):
        # M284/D-184: a row whose promotion condition has not held.
        self.assertIn("a row may instead open with `[parked]`, the fourth level", rules())

    def test_token_is_the_fact(self):
        self.assertIn("the token is the fact the order derives from", rules())


class TestInitSkeleton(unittest.TestCase):
    def skeleton(self):
        text = read("cairn-init", "SKILL.md")
        start = text.index("## candidates\n<!--")
        return text[start : text.index("-->", start)]

    def test_skeleton_shows_the_tagged_shape(self):
        self.assertIn("- [high] short title: detail — added yyyy-mm-dd — links", self.skeleton())

    def test_skeleton_names_the_token_as_optional(self):
        self.assertIn("`[high]`/`[low]`/`[parked]` or absent (`normal`)", self.skeleton())

    def test_skeleton_states_the_four_level_order(self):
        self.assertIn("ordered high → normal → low → parked:", self.skeleton())


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
            "a `keep`, `compress`, or `retitle` row may also carry a priority change", self.step(3)
        )

    def test_priority_change_is_the_carve_out(self):
        self.assertIn(
            "an accepted priority change on a `keep`, `compress`, or `retitle` row is one edit this rule carves out",
            self.step(3),
        )

    def test_apply_orders_by_token_then_advisory(self):
        self.assertIn(
            "ordered by token — high → normal → low → parked — then advisory within a level",
            self.step(4),
        )

    def test_enumeration_lists_the_parked_level(self):
        # M284/D-184: the fourth level is read, not taken for a misspelling.
        self.assertIn("its priority (`high` / `normal` / `low` / `parked`", self.step(1))
        self.assertIn("opening `[high]`, `[low]`, or `[parked]` token", self.step(1))


class TestTriageReRatesParked(unittest.TestCase):
    """M284: a priority change adds or removes `[parked]`, and a promote of a
    parked row writes `[high]`. These sentences wrap, so each step is read
    with its whitespace collapsed (M171)."""

    def step(self, n):
        return " ".join(TestTriageReadsTheToken.step(self, n).split())

    triage = TestTriageReadsTheToken.triage

    def test_a_condition_not_held_adds_parked(self):
        self.assertIn("does not open with `[parked]`, gets `priority: <level> → parked`", self.step(3))

    def test_a_condition_held_removes_parked(self):
        self.assertIn("a parked row whose condition held gets `priority: parked → normal`", self.step(3))

    def test_a_promote_of_a_parked_row_names_it(self):
        self.assertIn("or `priority: parked → high`", self.step(3))

    def test_review_hygiene_unparks_only_the_rows_it_names(self):
        text = " ".join(read("milestone-review", "SKILL.md").split())
        self.assertIn(
            "check each `[parked]` candidate row whose short title the milestone file quotes, "
            "or whose text names this milestone's id",
            text,
        )
        self.assertIn("leave every other parked row as it is", text)

    def test_apply_writes_the_parked_token(self):
        self.assertIn("(`[high]`/`[low]`/`[parked]`; `normal` is no token)", self.step(4))


class TestPromoteCarriesHigh(unittest.TestCase):
    """M271: an accepted promote of a candidate row writes `[high]`.

    These sentences wrap across source lines, so each step is read with its
    whitespace collapsed, a departure from the one-line convention above
    (M171).
    """

    def step(self, n):
        return " ".join(TestTriageReadsTheToken.step(self, n).split())

    triage = TestTriageReadsTheToken.triage

    def test_promote_of_a_candidate_row_carries_high(self):
        self.assertIn(
            "every `promote` of a candidate row whose opening token is not `[high]` "
            "carries the priority change to `high`",
            self.step(3),
        )

    def test_promote_set_at_amend_carries_it_too(self):
        self.assertIn("for a proposed `promote` and for one the user sets at *amend*", self.step(3))

    def test_known_issues_promote_carries_none(self):
        self.assertIn("a `promote` of a known issues entry carries no priority change", self.step(3))

    def test_amend_cannot_decline_it_alone(self):
        self.assertIn("a promote's change to `high` is not declined alone", self.step(3))

    def test_apply_writes_the_token(self):
        self.assertIn(
            "`promote` changes nothing of its own beyond the priority change a candidate row's promote carries",
            self.step(4),
        )

    def test_skip_needs_no_priority_change(self):
        self.assertIn(
            "every item `keep` or `promote` with no priority change and no token change", self.step(4)
        )

    def test_table_row_states_it(self):
        self.assertIn(
            "a promoted candidate row whose opening token is not `[high]` also takes the priority change to `high`",
            self.step(2),
        )

    def test_readiness_class_states_it(self):
        self.assertIn(
            "a promoted candidate row that does not open with `[high]` takes the priority change to `high`",
            self.step(2),
        )

    def test_it_replaces_another_proposed_change(self):
        self.assertIn("it replaces any other priority change proposed for that row", self.step(3))

    def test_chip_names_the_new_level_once(self):
        self.assertIn("is named once, with its new level `high`, beside the promote", self.step(3))

    def test_it_is_the_fourth_carve_out(self):
        self.assertIn("a promoted row's change to `high` is a fourth", self.step(3))

    def test_nothing_applied_needs_no_priority_change(self):
        self.assertIn(
            "an accept of only `keep` and `promote` items with no priority or token change", self.step(7)
        )

    def test_fences_put_candidates_before_known_issues(self):
        self.assertIn(
            "the candidate rows first, in table order, then the known issues entries, in table order",
            self.step(7),
        )


if __name__ == "__main__":
    unittest.main()
