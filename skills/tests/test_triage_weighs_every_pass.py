"""Regression guard: each triage pass weighs every item again (hotfix).

Pins `/cairn-triage` step 2's rule that an earlier pass is not evidence: a
`keep` reason cites no earlier triage commit, stamp, or park date, and no
item is skipped because nothing changed since then. Only a kept mark holds
a row on the user's earlier choice. Text is whitespace-collapsed on read
(M171), so a phrase may wrap across lines.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def flat(path):
    return re.sub(r"\s+", " ", path.read_text())


class TestTriageWeighsEveryPass(unittest.TestCase):
    def setUp(self):
        text = flat(SKILLS / "cairn-triage" / "SKILL.md")
        i = text.index("2. **Assess.**")
        self.assess = text[i:text.index("3. **Propose and gate.**", i)]

    def test_earlier_pass_is_not_evidence(self):
        for phrase in [
            "Each pass weighs every item again on what it reads now",
            "An earlier pass is not evidence",
            "never cites an earlier triage commit, the stamp, or the date "
            "a row was parked or last weighed",
            "never skips an item because nothing changed since then",
            "Only a kept mark (below) holds a row on the user's earlier choice",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.assess)


if __name__ == "__main__":
    unittest.main()
