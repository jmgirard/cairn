"""M100 (RR04 rec 8): review findings travel verbatim and outcomes meet
projections — the prose side of the enforcement machinery.

Guards pin: the ingest rule in /milestone-brief (verbatim ingestion, the
deviations table, the check's teeth), the brief template's Binding-criteria
request, the milestone template's Driving RR slot, review's
projection-vs-outcome surfaces (Review section + merge chip, with the
accept-shortfall option), plan's Driving RR bullet, and the two rulebook
sentences (script-measurable ACs; adjudication asymmetry). The runtime arm
is check_binding_criteria (scripts/tests/test_binding_criteria.py).

Anchors are copied from the target files' actual bytes (M95).

Run: python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    # pathlib read_text, never open(): the mutation engine redirects reads by
    # patching Path.read_text, and an open()-based guard is invisible to it.
    return SKILLS.joinpath(*parts).read_text(encoding="utf-8")


class TestIngestRule(unittest.TestCase):
    def setUp(self):
        self.text = read("milestone-brief", "SKILL.md")

    def test_ingest_rule_requires_verbatim_travel(self):
        self.assertIn("**Binding criteria travel verbatim:**", self.text)
        self.assertIn("ingests each criterion\n   verbatim into its "
                      "`## Acceptance criteria`", self.text)

    def test_ingest_rule_prescribes_the_numbered_form(self):
        # M107: each BC ingests as a numbered, coverage-mappable criterion, not
        # a bare checkbox — else coverage-complete reds on the unmapped items.
        self.assertIn("`- [ ] AC-N (BCn): <verbatim>`", self.text)
        self.assertIn("counts every AC checkbox positionally", self.text)

    def test_archive_move_is_robust_to_untracked(self):
        # M107: an in-session-generated or hand-dropped RR is untracked, so the
        # archive move uses plain mv + git add, never git mv.
        self.assertIn("an in-session-generated or hand-dropped RR is",
                      self.text)
        self.assertIn("`git mv` fails on an untracked file", self.text)

    def test_departures_go_through_the_shown_table(self):
        self.assertIn('Any departure is a row in the "Deviations from '
                      'RR<NN>" table', self.text)
        self.assertIn("shown verbatim at this ingestion's preview,\n"
                      "   never slipped — IP3 applied to review findings",
                      self.text)

    def test_softening_is_a_red_check_not_a_reading(self):
        self.assertIn("a softened criterion is a red check, not a\n"
                      "   reading", self.text)

    def test_unstated_tolerance_is_strict(self):
        self.assertIn("an unstated tolerance is strict — any shortfall\n"
                      "   forces the accept-shortfall option at the merge "
                      "gate", self.text)


class TestBriefTemplate(unittest.TestCase):
    def test_brief_requests_binding_criteria_as_measurable_assertions(self):
        text = read("shared", "templates", "brief.md")
        self.assertIn("`## Binding criteria` section: numbered `BC1…`, each "
                      "a measurable assertion", text)
        self.assertIn("These are ingested VERBATIM", text)


class TestMilestoneTemplate(unittest.TestCase):
    def test_template_carries_the_driving_rr_slot(self):
        text = read("shared", "templates", "milestone.md")
        self.assertIn("- **Driving RR:** —", text)
        self.assertIn("Driving RR set → its Binding criteria appear "
                      "VERBATIM here", text)

    def test_template_prescribes_the_ingest_form(self):
        # M107: the template teaches the same numbered, coverage-mapped form.
        text = read("shared", "templates", "milestone.md")
        self.assertIn("`- [ ] AC-N (BCn): <verbatim>`", text)
        self.assertIn("coverage-complete counts AC checkboxes positionally",
                      text)


class TestReviewSurfaces(unittest.TestCase):
    def setUp(self):
        self.text = read("milestone-review", "SKILL.md")

    def test_review_section_juxtaposes_projection_and_outcome(self):
        self.assertIn("**Projection-vs-outcome (Driving RR).**", self.text)
        self.assertIn('("measured X against projected Y"), never one without'
                      "\n   the other", self.text)

    def test_no_driving_rr_noops(self):
        self.assertIn("No driving RR, or none of its\n"
                      "   criteria numeric → this no-ops cleanly.", self.text)

    def test_merge_chip_repeats_the_pairs_and_offers_accept_shortfall(self):
        self.assertIn("repeat the measured-vs-projected pairs verbatim in "
                      "chat above the merge\n   chip", self.text)
        self.assertIn('**"accept shortfall, recorded as such"**', self.text)
        self.assertIn("the maintainer decides seeing\n   the gap", self.text)


class TestPlanBullet(unittest.TestCase):
    def test_plan_sets_slot_ingests_verbatim_and_copies_projections(self):
        text = read("milestone-plan", "SKILL.md")
        self.assertIn("- **Driving RR** (header slot):", text)
        self.assertIn("copies the RR's numeric projections beside the", text)


class TestRulebookSentences(unittest.TestCase):
    def setUp(self):
        self.text = read("shared", "tracking-rules.md")

    def test_script_measurable_preference(self):
        self.assertIn("**Prefer script-measurable acceptance criteria**; "
                      "where judgment is\n  unavoidable, commit the "
                      "classification ledger as evidence", self.text)

    def test_adjudication_asymmetry(self):
        self.assertIn("The implementing session never authors the durable "
                      "verdict on the review\n  constraining it", self.text)


if __name__ == "__main__":
    unittest.main()
