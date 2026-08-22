"""Regression guards for the two M152 plain-style rules in
`tracking-rules.md`: the "Plain style" chat-output bullet (Output &
interaction discipline) and the "Records are written plain" record-prose
bullet (Universal tracking rules). Both were adopted from the user-reported
verbosity defect with the length clauses sourced to `prompting-opus-5`.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23/M64), matches through `**bold**`
markers rather than across them (M26), and is read per-test, never cached
at class level (M61); phrases are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def rules():
    return (SKILLS / "shared" / "tracking-rules.md").read_text().lower()


class TestPlainStyleRule(unittest.TestCase):
    """M152: the chat-output style rule. Five asserts: the length standard,
    the jargon bar, the glossing clause, the filler bar, and the padding
    clause with its carve-out opener — the review fan-out found the original
    three left the glossing and padding clauses deletable with the suite
    green."""

    def test_length_matched_to_the_turn(self):
        self.assertIn(
            "write for the reader: response length matched to what the turn needs",
            rules(),
        )

    def test_plain_words_over_jargon(self):
        self.assertIn("plain words over jargon — a term of art appears only", rules())

    def test_no_filler_or_hype(self):
        self.assertIn(
            "with no stock filler phrasing, hype adjectives, or", rules()
        )

    def test_terms_glossed_or_dropped(self):
        self.assertIn("glossed at first use or dropped", rules())

    def test_padding_clause_and_carveout(self):
        self.assertIn("padding. the decision surface keeps its stricter", rules())


class TestRecordProseRule(unittest.TestCase):
    """M152: the record-prose rule. Three asserts: the rule exists under its
    name, the no-characterizations clause (the M114 lesson's standard), and
    the cross-referenced length standard."""

    def test_rule_present_under_its_name(self):
        self.assertIn("**records are written plain** (the record-prose rule)", rules())

    def test_no_characterizations(self):
        self.assertIn(
            "omits characterizations the facts don't need (adjectives, superlatives, hype)",
            rules(),
        )

    def test_length_standard_cross_referenced(self):
        self.assertIn(
            "the plain style rule's length standard, applied to what is written down",
            rules(),
        )


if __name__ == "__main__":
    unittest.main()
