"""Regression guard: the M67 narration-discipline rule (D-039).

Locks the "Narrate outcomes, not deliberation" rule in
`tracking-rules.md`: the no-deliberation-readout bar, the signpost and
summaries-for-questions allowances, and the carve-out naming the
Durable-record preview and Acceptance chips rules as mandated substance.
Central rule only — D-039 deliberately wires no per-skill directives
(narration discipline is continuous conduct with no step to anchor to).

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


class TestNarrationDisciplineRule(unittest.TestCase):
    def test_rule_present_with_deliberation_bar(self):
        t = rules()
        self.assertIn(
            "narrate outcomes, not deliberation.** between tool calls, chat carries",
            t,
        )
        self.assertIn("never a running readout of reasoning", t)
        self.assertIn("no italicized play-by-play commentary", t)

    def test_signpost_and_summary_allowances(self):
        t = rules()
        self.assertIn("a one-line signpost before a long step is fine;", t)
        self.assertIn(
            "a compact summary where a question needs context is fine (d-039).",
            t,
        )

    def test_preview_carveout(self):
        # D-036/D-037 previews are mandated substance, not chattiness —
        # the rule must say it never licenses summarizing them away.
        self.assertIn(
            "this never licenses compressing mandated substance: the durable-record",
            rules(),
        )


class TestCorrectionNarrationRule(unittest.TestCase):
    """M120: the correction-narration rule adopted from `prompting-opus-5`.

    The guide reports that Claude Opus 5 "narrates corrections to its earlier
    statements more than prior models do" (§ Self-correction) and cairn had no
    rule saying which corrections earn a sentence — the nearest, "Correcting a
    record proven false", governs tracking records rather than chat.

    Four asserts because the rule carries four claims independently: the
    materiality bar, the plain-and-continue form, the unremarked slip, and the
    boundary against the D-045 repair rule. The last is not decoration — with
    it deleted the rule reads as licensing a chat-shaped fix for a false
    tracking record, which is the remedy D-045 rules out.
    """

    def test_rule_states_the_materiality_bar(self):
        self.assertIn(
            "only when the error would change the user's code, conclusions,",
            rules(),
        )

    def test_rule_requires_plain_correction_then_continue(self):
        self.assertIn(
            "state the correction plainly and briefly, then continue the",
            rules(),
        )

    def test_rule_leaves_an_immaterial_slip_unnarrated(self):
        self.assertIn(
            "a slip that changes nothing for the user is fixed without "
            "narrating it,",
            rules(),
        )

    def test_rule_separates_chat_slips_from_durable_records(self):
        self.assertIn("a chat slip never reaches a durable record", rules())


if __name__ == "__main__":
    unittest.main()
