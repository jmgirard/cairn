"""Lock: what counts as a rule, and what guard-reddening does and does not buy
(M95, D-056).

RR02 prescribed "state the rule, cite the D-entry, delete the defense". M95's
first implement run stopped when its ledger found 9 of 21 targeted blocks had
no D-entry home at all — the rulebook is their sole home — and 14 were
guard-pinned. D-056 replaces that bar: the rulebook is current knowledge, so
the test is behavioral (does deleting this change what a compliant agent
does?), and guard-pinning screens deletions without licensing keeps.

Both statements live in the ALWAYS-READ rulebook rather than in the
conditionally-read `guard-doctrine.md`, because their consumer is an editorial
session that may write no guard at all — M98 drafted them into the module and
removed them at review for exactly that reason (M98 review F4/82).

Assertions are positive so they can be mutation-proven, and each target is read
per test rather than cached at class level, since the harness runs a guard as a
single method and skips `setUpClass` (M53/M61 discipline).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent

RULES = SKILLS / "shared" / "tracking-rules.md"
MODULE = SKILLS / "shared" / "guard-doctrine.md"


def read(path):
    return path.read_text()


class TestBehavioralInversionTest(unittest.TestCase):
    """The definition of a rule is stated, with its proof procedure."""

    def setUp(self):
        self.rules = read(RULES)

    def test_rulebook_states_the_behavioral_inversion_test(self):
        self.assertIn(
            "**A rule is what changes compliant behavior when deleted or inverted.**",
            self.rules,
        )

    def test_test_names_both_operative_classes_with_the_label(self):
        # Label -> members (M74/M86): "operative" must travel with what it
        # covers, or the predicate carrying the meaning can be deleted with
        # every assert still green. The mapping spans a wrap here, so pin the
        # span verbatim — that reddens on deletion AND on a reflow.
        self.assertIn(
            "is operative — a rule, or the\ndoctrine for applying one",
            self.rules,
        )

    def test_rulebook_names_the_alternative_the_test_screens_out(self):
        # Without this half the test reads as "keep everything operative" and
        # the deletion licence disappears.
        self.assertIn(
            "or is justification the file does not owe and git\nalready holds",
            self.rules,
        )

    def test_rulebook_cites_the_decision_that_licenses_deletion(self):
        self.assertIn(
            "(D-056, which classifies the rulebook as current knowledge and\nstates the three-step placement test)",
            self.rules,
        )

    def test_rulebook_states_the_inversion_proof_procedure(self):
        self.assertIn(
            "relabel, negate,\nor transpose the rule in place, run the suite, require red, restore and diff",
            self.rules,
        )

    def test_rulebook_covers_the_unguarded_case(self):
        # A procedure that only works where a guard exists would leave every
        # unpinned rule unprovable — the gap that made B18 undecidable.
        self.assertIn(
            "where no guard exists, record a by-hand inversion", self.rules
        )


class TestReddeningAsymmetry(unittest.TestCase):
    """Reddening blocks careless deletion; it never justifies keeping."""

    def setUp(self):
        self.rules = read(RULES)

    def test_rulebook_states_the_screen_not_licence_rule(self):
        self.assertIn(
            "**Guard-reddening is a deletion screen, never a licence to keep**",
            self.rules,
        )

    def test_all_three_asymmetry_clauses_are_pinned_together(self):
        # The asymmetry is only meaningful as a triple: any one clause alone
        # reads as its opposite ("reddening is sufficient" without "never
        # sufficient to keep" is the very inversion RR03 warns against). Pin
        # the whole span so dropping any one clause reddens.
        self.assertIn(
            "sufficient\n"
            "to block a careless deletion, never necessary to justify one, and never\n"
            "sufficient to keep prose that fails the behavioral test above.",
            self.rules,
        )

    def test_rulebook_states_the_ownership_direction(self):
        self.assertIn("The text owns\nthe guard, not the reverse", self.rules)

    def test_rulebook_states_why_pinned_does_not_mean_doctrine(self):
        # RR03 §2: anchors are picked for matchability, so a guard can pin
        # scaffolding. Without this, "pinned" reads as "load-bearing".
        self.assertIn(
            "anchors are exemplar blocks chosen partly for\nmatchability, so a guard can pin scaffolding",
            self.rules,
        )

    def test_rulebook_names_the_failure_mode_the_asymmetry_prevents(self):
        self.assertIn(
            "reading pinned as frozen is\nhow a rulebook's editability dies one guard at a time",
            self.rules,
        )

    def test_rulebook_states_what_happens_to_a_pinned_block_that_fails(self):
        self.assertIn(
            "A pinned block that\nfails the test is shortened *with* re-anchoring, never skipped",
            self.rules,
        )


class TestPlacedWhereItsConsumersRead(unittest.TestCase):
    """The doctrine is in the always-read core, not the conditional module."""

    def setUp(self):
        self.rules = read(RULES)

    def test_both_statements_precede_the_guard_obligation(self):
        # They define what a rule is; the guard obligation then says how to
        # lock one. Order carries the argument, so pin it positionally.
        rule_def = self.rules.index("A rule is what changes compliant behavior")
        asymmetry = self.rules.index("Guard-reddening is a deletion screen")
        obligation = self.rules.index("A guard must fail when the rule it locks is deleted")
        self.assertLess(rule_def, asymmetry)
        self.assertLess(asymmetry, obligation)

    def test_statements_live_in_the_what_gets_a_test_section(self):
        section = self.rules.split("## What gets a test")[1]
        self.assertIn("A rule is what changes compliant behavior", section)
        self.assertIn("Guard-reddening is a deletion screen", section)

    def test_module_does_not_become_the_sole_home(self):
        # M98 F4: a conditionally-read module hides these from the editorial
        # session that is their consumer. A positive control pairs with this
        # absence-assert so it cannot pass on an empty read (M84 vacuity trap).
        module = read(MODULE)
        self.assertIn("a module of `tracking-rules.md`", module)
        self.assertNotIn(
            "A rule is what changes compliant behavior when deleted or inverted", module
        )


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
