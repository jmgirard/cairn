"""Regression guard: the M65 acceptance-chips rule (D-037).

Locks the "Acceptance chips show what's accepted" rule in
`tracking-rules.md` (AC1), the cross-reference from "Chips carry choices,
not evidence" (AC2), and the one-line directives at the five
conclusion-feeding chip steps (AC3): `/milestone-plan` question gate,
`/milestone-implement` question gate + amendment mini-gate,
`/milestone-review` approval gate, `/milestone-brief` RB gate +
RR-ingestion routing, `/milestone` Route triage. Also anchors the
previously-unguarded "Chips carry choices, not evidence" rule itself.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23/M64), steers clear of `**bold**` splits
(M26), and is read per-test, never cached at class level (M61); phrases
are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text().lower()


def rules():
    return read("shared", "tracking-rules.md")


class TestAcceptanceChipsRule(unittest.TestCase):
    def test_rule_present_with_verbatim_bar(self):
        t = rules()
        self.assertIn("requires that conclusion's substance", t)
        self.assertIn(
            "verbatim in chat above the chip (d-037): the verdict and each actioned",
            t,
        )
        self.assertIn(
            "verbatim plus the file path for the rest; a paraphrase never stands in",
            t,
        )

    def test_chips_carry_choices_rule_present(self):
        # The base rule the M65 rule extends — previously unguarded.
        self.assertIn(
            "chips carry choices, not evidence.** supporting detail and technical",
            rules(),
        )

    def test_cross_reference_present(self):
        self.assertIn(
            "a summary never substitutes for the accepted text.",
            rules(),
        )

    def test_enumeration_names_proposals(self):
        # M66/D-038: closes the proposal-isn't-a-conclusion loophole.
        self.assertIn(
            "a proposed disposition or action plan awaiting confirmation (d-038)",
            rules(),
        )


class TestPerSkillDirectives(unittest.TestCase):
    def test_plan_question_gate(self):
        self.assertIn(
            "acceptance chips (tracking-rules): a question resting on a produced",
            read("milestone-plan", "SKILL.md"),
        )

    def test_implement_gate_and_mini_gate(self):
        t = read("milestone-implement", "SKILL.md")
        self.assertIn(
            "conclusion shows its substance verbatim above the chip.",
            t,
        )
        self.assertIn(
            "mini gate's chip (acceptance chips, tracking-rules)",
            t,
        )

    def test_review_approval_gate(self):
        self.assertIn(
            "acceptance chips (tracking-rules): each actioned finding's text appears",
            read("milestone-review", "SKILL.md"),
        )

    def test_brief_rb_gate_and_rr_routing(self):
        t = read("milestone-brief", "SKILL.md")
        self.assertIn(
            "acceptance chips (tracking-rules): show the drafted rb's",
            t,
        )
        self.assertIn(
            "the rr's conclusions/verdict section is shown verbatim above the chip.",
            t,
        )

    def test_milestone_route_triage(self):
        self.assertIn(
            "acceptance chips (tracking-rules): a triage option that accepts an audit",
            read("milestone", "SKILL.md"),
        )


class TestMigrationGateDirectives(unittest.TestCase):
    """M66/D-038: cairn-init's migration gates join the wired set —
    the step-3 disposition proposal and the step-7 merge ledger are
    produced content, not user-known options (hit live, hitop repo)."""

    def test_step3_disposition_gate(self):
        t = read("shared", "migration-protocol.md")
        self.assertIn(
            "acceptance chips (tracking-rules): the inventory and each item's",
            t,
        )
        self.assertIn(
            "never only inside chip options, and a paraphrase never stands in for",
            t,
        )

    def test_step7_merge_ledger(self):
        t = read("shared", "migration-protocol.md")
        self.assertIn(
            "acceptance chips (tracking-rules): the ledger's substance appears",
            t,
        )
        self.assertIn(
            "verbatim in chat above the merge-approval chip — the pr description",
            t,
        )


class TestAccessibleLanguageRule(unittest.TestCase):
    """M106: the decision surface leads in plain words, glossing jargon
    rather than assuming it — extends "Chips carry choices, not evidence"
    without displacing its above-the-chip justification clause."""

    def test_rule_present_and_scopes_the_decision_surface(self):
        t = rules()
        self.assertIn("accessible language on the decision surface.", t)
        self.assertIn(
            "an askuserquestion question's text, the prose framing a",
            t,
        )

    def test_rule_glosses_jargon_and_names_the_failure(self):
        t = rules()
        self.assertIn(
            "a technical term is glossed at first use, never assumed",
            t,
        )
        self.assertIn(
            "jargon-led framing, where the user must already know the",
            t,
        )

    def test_rule_reconciles_with_chips_carry_choices(self):
        self.assertIn(
            "leads with its plain-language meaning rather than standing in for it.",
            rules(),
        )

    def test_cross_reference_from_chips_carry_choices(self):
        self.assertIn(
            "the accessible language rule below carries that plain-language",
            rules(),
        )


if __name__ == "__main__":
    unittest.main()
