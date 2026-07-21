"""Regression guard: the M88/D-050 release-timing rule.

Locks three prose surfaces that together stop cairn nominating a release the
maintainer never queued:

  * `tracking-rules.md` — release timing is user-declared, `blocked` covers an
    unopened release window, and parking is reachable from `planned`/`review`.
  * `/milestone-plan` — the release-shaped tripwire and its candidate-row
    default.
  * `/milestone` — reporting the advisory and offering the park disposition.

Each assert pins a LABEL together with the RULE it maps to, on one physical
source line (LESSONS M74): pinning the label alone survives someone swapping
the rule out from under it, and pinning the mechanism alone survives the label
being relabelled. Skill-prose guards read the file as one string, so every
asserted phrase lives on a single source line (M23) and steers clear of
`**bold**` splits (M26); phrases are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def rules():
    return SKILLS.joinpath("shared", "tracking-rules.md").read_text().lower()


def plan():
    return SKILLS.joinpath("milestone-plan", "SKILL.md").read_text().lower()


def milestone():
    return SKILLS.joinpath("milestone", "SKILL.md").read_text().lower()


class TestReleaseTimingRule(unittest.TestCase):
    """The universal governance rule in tracking-rules.md."""

    def test_rule_states_who_declares_release_timing(self):
        # Label AND rule on one line: "release timing" alone would survive the
        # predicate being inverted to agent-proposed.
        self.assertIn(
            "release timing is user-declared, never agent-proposed", rules()
        )

    def test_rule_forbids_all_three_agent_initiatives(self):
        # The three verbs are the rule's teeth — proposing, planning, and
        # nominating are separate acts and each had to be named.
        self.assertIn(
            "never proposes a release, never plans a release milestone "
            "unprompted, and never nominates one as the next action",
            rules(),
        )

    def test_rule_rejects_the_dependency_graph_as_a_readiness_signal(self):
        # The load-bearing contrast, pinned whole on one line: asserting the
        # first clause alone would survive the "never a dependency graph"
        # predicate being dropped at the line break (LESSONS M74).
        self.assertIn(
            "a maintainer judgment about when to ship, never a dependency "
            "graph going green",
            rules(),
        )

    def test_rule_names_blocked_as_the_parking_state(self):
        self.assertIn(
            "is parked as `blocked`, where no routing surface nominates it",
            rules(),
        )


class TestBlockedCoversTheReleaseWindow(unittest.TestCase):
    """The status-vocabulary widening and the transitions parking needs."""

    def test_blocked_row_names_the_unopened_release_window(self):
        # Pins the `blocked` label to the widened meaning on the table row
        # itself — the row is one physical line by table syntax.
        self.assertIn(
            "a maintainer who has not opened the release window counts", rules()
        )

    def test_parking_transitions_are_legal_from_both_routable_states(self):
        # Both arrows on one line with the word that legalizes them; pinning
        # one arrow alone would let the other be dropped silently.
        self.assertIn(
            "`planned → blocked` and `review → blocked` are both legal", rules()
        )


class TestPlanReleaseTripwire(unittest.TestCase):
    """/milestone-plan's release-shaped tripwire."""

    def test_tripwire_is_declared_with_its_authority(self):
        self.assertIn(
            "release timing is user-declared, never agent-proposed "
            "(tracking-rules; d-050)",
            plan(),
        )

    def test_tripwire_default_is_no(self):
        # The default is what makes the tripwire bite; a tripwire that merely
        # "asks" would satisfy a label-only assert. Default and both
        # consequences on one line, so none can be dropped independently.
        self.assertIn(
            "the default answer is no — absent a declaration the work lands "
            "as a `candidate` row, never as a `planned` milestone",
            plan(),
        )

    def test_tripwire_exempts_release_tooling(self):
        # The false-positive carve-out, mirroring the advisory's token+version
        # discrimination in prose.
        self.assertIn(
            "work *about* release tooling — a release-walk slot, release "
            "docs — is ordinary milestone work, not a release",
            plan(),
        )


class TestMilestoneAuditWiring(unittest.TestCase):
    """/milestone reports the advisory and offers the park disposition."""

    def test_audit_reports_the_warn_without_arguing(self):
        # Label pinned to BOTH halves of its rule on one line: report-not-argue
        # and the refusal to read the WARN as a prompt to ship (M88 review F2
        # moved this out of the "script does not judge these" list, where it
        # contradicted its own heading).
        self.assertIn(
            "a `release window` warn is reported, never argued with — release "
            "timing is the user's to declare (d-050)",
            milestone(),
        )

    def test_audit_refuses_to_treat_the_warn_as_a_prompt_to_ship(self):
        self.assertIn(
            "never treat the warn as a prompt to get the release moving",
            milestone(),
        )

    def test_advisory_owns_idleness_against_the_staleness_bullet(self):
        # Without an owner the same stalled release arrives twice — once as a
        # script WARN, once as a manual staleness item (M88 review F2). M104
        # broadened ownership to EVERY release-shaped milestone, whether or not
        # the advisory fired: else the stricter work-only bullet nags a release
        # the advisory's lenient any-entry rule deliberately spared (M104 F-C).
        text = milestone()
        self.assertIn(
            "is not re-reported under the staleness bullet", text
        )
        self.assertIn(
            "idleness question for every release-shaped milestone", text
        )

    def test_staleness_signal_discounts_bookkeeping_entries(self):
        # M104: the in-progress staleness clock runs from the last entry that
        # records WORK, never the last entry of any kind, or a stalled
        # milestone reads active (M88 T3). Anchor 1 pins the measurement basis.
        # Anchor 2 binds the clock-neutral disposition to its three enumerated
        # members ON ONE LINE — a label-only anchor is false-coverage for the
        # SET, since a member swap stays green (M74/M103, guard-doctrine §1;
        # M104 F-A). Anchor 3 pins the release-shaped exemption (M104 F-C).
        text = milestone()
        self.assertIn(
            "the last work-log line that records actual progress", text
        )
        self.assertIn(
            "clock-neutral bookkeeping — a `depends-on` amendment, a "
            "status/mirror catch-up, and a git-reconciliation catch-up line",
            text,
        )
        self.assertIn("release-shaped milestones are exempt", text)

    def test_route_offers_the_park_option(self):
        self.assertIn(
            "park m<nn> as `blocked` → the release window is not open",
            milestone(),
        )

    def test_park_leads_the_chip_only_when_cairn_next_names_that_release(self):
        # The override is scoped to the case its justification covers: leading
        # with parking whenever the advisory fired would demote a legitimate
        # "resume M<other>" recommendation, since an unrelated in-progress
        # milestone outranks a workable planned one (M88 review F1).
        self.assertIn(
            "lead the chip with it only when `cairn_next`'s own recommendation "
            "names that same release milestone",
            milestone(),
        )

    def test_a_recommendation_naming_something_else_keeps_the_lead(self):
        self.assertIn(
            "that recommendation is legitimate and keeps the lead", milestone()
        )


if __name__ == "__main__":
    unittest.main()
