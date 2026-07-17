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


if __name__ == "__main__":
    unittest.main()
