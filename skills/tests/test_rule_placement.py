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

Both statements live in the ALWAYS-READ rulebook rather than in the
conditionally-read `guard-doctrine.md`, because their consumer is an editorial
session that may write no guard at all — M98 drafted them into the module and
removed them at review for exactly that reason (M98 review F4/82).

Assertions are positive so they can be mutation-proven; the three absence-asserts
here each pair with a positive control (guard-doctrine §3). Each target is read
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


class TestPlacementTest(unittest.TestCase):
    """The definition of a rule is stated, with its proof procedure."""

    def setUp(self):
        self.rules = read(RULES)

    def test_rulebook_states_the_deletion_retention_test(self):
        # D-071/AC2: the retention arm is deletion ALONE. The old disjunction
        # routed every duplicate to "keep", since inverting a copy contradicts
        # the original and so changes behavior (RR04 section 6).
        self.assertIn(
            "**A rule is what changes compliant behavior when it is deleted.**",
            self.rules,
        )

    def test_rulebook_names_deletion_as_the_only_retention_probe(self):
        # Without this the repaired sentence still reads as compatible with an
        # inversion arm applied to placement — the exact defect D-071 closes.
        self.assertIn(
            "Deletion is the retention probe and the only\none: inversion detects rule-shaped text, which a duplicate equally is",
            self.rules,
        )

    def test_rulebook_does_not_restate_the_superseded_disjunction(self):
        # D-071/AC2 absence clause. Paired with a positive control so it cannot
        # pass on an empty or misdirected read (M84 vacuity trap).
        self.assertIn("**A rule is what changes compliant behavior", self.rules)
        self.assertNotIn("deleted or inverted", self.rules)

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
        # D-071 repairs the test; D-056's part 1 (current knowledge) is what
        # licenses deletion at all, so BOTH ids must survive here.
        self.assertIn(
            "(D-071 repairs the test; D-056's classification of the rulebook\nas current knowledge stands)",
            self.rules,
        )

    def test_step_zero_requires_a_single_home(self):
        # D-071/AC3. The two asserts pin deliberately differently: the regex
        # uses `\s+` because AC3 pins this clause by MEANING, so a reflow must
        # not red it (M105); the assertIn below carries its wrap verbatim
        # because a reflow there SHOULD red, the M74 discipline also used at
        # :75-76. The intra-file scoping clause is the operative half: without
        # "already says it somewhere else" the step reads as a general
        # single-home norm over every cairn file, far larger than D-071 adopts.
        self.assertRegex(
            self.rules,
            r"\*\*Step 0 — one home\.\*\* Before asking whether a piece of prose\s+"
            r"belongs in this\s+rulebook, ask whether the rulebook already says it\s+"
            r"somewhere else",
        )
        self.assertIn(
            "One site\nkeeps the statement; every other site carries at most a cross-reference.",
            self.rules,
        )

    def test_step_zero_binds_forward_only(self):
        # Without this the check reads as a mandate to sweep the file, which is
        # the stock-side work D-057 closed and D-071's Scope explicitly refuses.
        self.assertIn(
            "binding on text authored or edited from here on, and never\na mandate to sweep the file",
            self.rules,
        )

    def test_inversion_is_assigned_to_guard_verification(self):
        # D-071/AC4: the procedure survives verbatim, its OWNER changes.
        self.assertIn(
            "Relabel, negate, or transpose the rule in\nplace, run the suite, require red, restore and diff",
            self.rules,
        )
        self.assertIn(
            "that is the\nguard-verification protocol",
            self.rules,
        )

    def test_rulebook_covers_the_unguarded_case(self):
        # M116 repointed this. Under D-056 the unguarded case mattered because
        # inversion decided rule-ness, so unpinned text was unprovable (B18).
        # D-071 moved that decision to the deletion probe, so what the fallback
        # now covers is guard VERIFICATION: an assert with no registered block
        # still owes a recorded by-hand check, stated with the guard-must-fail
        # rule that owns it rather than restated beside the placement steps.
        self.assertIn(
            "still needs its own entry or the by-hand\ncheck", self.rules
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
            "A rule is what changes compliant behavior when it is deleted", module
        )

    def test_step_zero_precedes_the_retention_test(self):
        # D-071/AC3 states step 0 runs BEFORE the retention test. Order is the
        # whole content of "step 0"; pinning both texts without their sequence
        # leaves a file that states them backwards fully green.
        self.assertLess(
            self.rules.index("**Step 0 — one home.**"),
            self.rules.index("**A rule is what changes compliant behavior"),
        )

    def test_only_two_sites_name_the_placement_steps(self):
        # D-071/AC5: one home (the paragraph), one pointer (the inflow cell).
        # assertNotIn forbids the old phrasing but cannot bound the NUMBER of
        # sites, so a third restating site would ship green without this.
        self.assertEqual(self.rules.count("placement steps"), 1)
        self.assertEqual(
            self.rules.count("**A rule is what changes compliant behavior"), 1
        )

    def test_inflow_cell_points_at_the_test_without_restating_it(self):
        # D-071/AC5: one home (the paragraph), one pointer (the table cell).
        # `blank_block` errors on a locator occurring twice as loudly as on
        # zero (mutation_engine.py:41-49), so a literal shared between the two
        # sites breaks the harness — step 0's own rule, mechanically enforced.
        self.assertIn(
            '| `tracking-rules.md` | the placement steps under "What gets a '
            'test" (D-071) |',
            self.rules,
        )
        self.assertNotIn("three-step placement test", self.rules)


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
