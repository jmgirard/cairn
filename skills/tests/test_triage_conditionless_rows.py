"""Regression guard: M326/D-227, candidate rows with no promotion condition.

Locks `/cairn-triage`'s No condition class and its fourth drop class (AC2),
the condition change's wiring and placement (AC3, AC4), the drop's record
(AC5), and the
review rule in the rulebook and both review skills (AC1). Each step is read
with its whitespace collapsed, so wrapped sentences match (M171).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return " ".join(SKILLS.joinpath(*parts).read_text().lower().split())


def step(n):
    text = SKILLS.joinpath("cairn-triage", "SKILL.md").read_text().lower()
    start = text.index(f"\n{n}. **")
    try:
        end = text.index(f"\n{n + 1}. **", start)
    except ValueError:
        end = len(text)
    return " ".join(text[start:end].split())


class TestNoConditionClass(unittest.TestCase):
    def test_class_sits_between_readiness_and_title(self):
        text = step(2)
        readiness = text.index("**readiness → `promote`.**")
        no_condition = text.index("**no condition → `drop` or a condition change.**")
        title = text.index("**title → `retitle`.**")
        self.assertLess(readiness, no_condition)
        self.assertLess(no_condition, title)

    def test_class_skips_high_rows(self):
        self.assertIn("that does not open with `[high]`, and that states no promotion condition", step(2))

    def test_class_proposes_a_condition_and_parked(self):
        text = step(2)
        self.assertIn("the pass drafts one condition, `promote when <condition>`", text)
        self.assertIn("the row takes `priority: <level> → parked`", text)

    def test_compress_and_group_keep_take_a_condition_too(self):
        self.assertIn("or that §7's options leave `keep`, takes a condition change too", step(2))

    def test_class_never_keeps_by_default(self):
        self.assertIn("the class never leaves such a row `keep` with no change", step(2))

    def test_fourth_drop_class_reads_the_row_alone(self):
        text = step(2)
        self.assertIn("its reason is one of four classes", text)
        self.assertIn("*not worth keeping* (only the no condition class below proposes it", text)
        self.assertIn("its test reads the row alone", text)
        self.assertIn("either only a rare input reaches it or it changes no output", text)
        self.assertIn("a wrong result with no error or warning never passes", text)


class TestConditionChangeWiring(unittest.TestCase):
    def test_placement_keeps_the_short_title(self):
        text = step(4)
        self.assertIn("the condition goes right before that text, opened with `; `", text)
        self.assertIn("opened with ` — `. either way the row's short title stays the same", text)

    def test_decline_drops_parked_too(self):
        self.assertIn("decline a condition change alone, which declines its move to parked too", step(3))

    def test_skip_test_counts_it(self):
        self.assertIn("no token change, and no condition change", step(4))


class TestNotWorthKeepingRecord(unittest.TestCase):
    def test_decision_entry_lists_the_drop(self):
        text = step(5)
        self.assertIn("is *rejected on principle* or *not worth keeping*", text)
        self.assertIn("each item dropped as not worth keeping by subject", text)

    def test_commit_body_names_it(self):
        self.assertIn("refuted-premise, already-shipped, and not-worth-keeping drops", step(6))


class TestReviewRule(unittest.TestCase):
    def test_rulebook_states_the_default(self):
        text = read("shared", "tracking-rules.md")
        self.assertIn("files for a review finding states its promotion condition", text)
        self.assertIn("the condition is `promote when a user reports it`", text)

    def test_review_follow_up_states_it(self):
        self.assertIn("each row filed for a finding states `promote when <condition>`", read("milestone-review", "SKILL.md"))

    def test_copilot_follow_up_points_to_the_rule(self):
        self.assertIn("the row states its promotion condition", read("copilot-review", "SKILL.md"))


if __name__ == "__main__":
    unittest.main()
