"""Regression guards for the two chat-output rules in `tracking-rules.md`'s
Output & interaction discipline: the M67 narration-discipline rule (D-039) and
the M120 correction-narration rule. Both govern what the session says in chat
rather than what it writes to a record, which is why they share a file.

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


    def test_rule_separates_chat_slips_from_durable_records(self):
        self.assertIn("a chat slip never reaches a durable record", rules())


if __name__ == "__main__":
    unittest.main()
