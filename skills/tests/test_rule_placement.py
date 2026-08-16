"""Lock: what counts as a rule, and what guard-reddening does and does not buy
(M95, D-056; the placement test repaired by D-071 at M116).

RR02 prescribed "state the rule, cite the D-entry, delete the defense". M95's
first implement run stopped when its ledger found 9 of 21 targeted blocks had
no D-entry home at all — the rulebook is their sole home — and 14 were
guard-pinned. D-056 replaced that bar: the rulebook is current knowledge, so
the test is behavioral, and guard-pinning screens deletions without licensing
keeps. D-071 then narrowed the test itself — RR04 §6 found "deleted **or**
inverted" defective, since inverting a duplicate creates a contradiction and so
any rule-shaped text, copies included, passes the inversion arm. Retention now
takes the deletion arm alone; inversion is the guard-verification protocol; and
a step-0 single-home check runs ahead of both. D-056's parts 1 and 3 stand, so
the classification and asymmetry assertions below are unchanged.

M146 reduced the rulebook to operative rules; the surviving guards here pin
the D-071 decision record, which is history and stable. Each target is read
per test rather than cached at class level, since the harness runs a guard as
a single method and skips `setUpClass` (M53/M61 discipline).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent


def read(path):
    return path.read_text()


class TestDecisionRecord(unittest.TestCase):
    """D-056 exists, annotates D-045, and carries what the rulebook cites."""

    def setUp(self):
        self.decisions = read(ROOT / "cairn" / "DECISIONS.md")

    def test_entry_exists_and_annotates_d045(self):
        self.assertRegex(
            self.decisions,
            r"### D-056 \(2026-07-20\): `tracking-rules\.md` is current knowledge[^\n]*annotates D-045",
        )

    def test_entry_classifies_the_rulebook_as_current_knowledge(self):
        self.assertIn(
            "**(1) `skills/shared/tracking-rules.md` is current knowledge under D-045.**",
            self.decisions,
        )

    def test_entry_states_all_three_placement_steps(self):
        for step in (
            "**Inversion test.**",
            "**Decision test.**",
            "**Neither → free-floating justification**",
        ):
            self.assertIn(step, self.decisions)

    def test_entry_forbids_the_backfill_sweep(self):
        # The rejected maximalist reading (RR03 rec 9) — without this, step 2
        # licenses exactly the remedy the entry rejects.
        self.assertIn(
            "author the entry when the choice is next\n   touched, never as a backfill sweep",
            self.decisions,
        )

    def test_entry_leaves_ip4_untouched(self):
        self.assertIn(
            "IP4's wording is untouched, and the clarification runs the other\nway",
            self.decisions,
        )


if __name__ == "__main__":
    unittest.main()
