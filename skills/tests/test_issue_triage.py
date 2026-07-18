"""Regression guard: the M74/D-043 issue-triage sweep in `/milestone`.

D-043's third deliverable. Before M74 the audit carried an *unenumerable*
bullet — "open GitHub issues or external PRs with no candidate row / hotfix
disposition → list them for triage" — which named a duty with no way to
discharge it: no command, no cross-check, and no answer for the common case
where `gh` simply is not there. Three things have to survive:

  1. The **enumeration** is concrete. Both inboxes get a real command, and
     every hit goes through the search-first sweep before a row is proposed.
     Losing the commands returns the step to "somehow know what is open";
     losing the cross-check is how the same idea lands as a second row.
  2. The **degradation** is stated. `gh` missing, unauthenticated, or no
     remote is the ordinary case in a local-only repo, and it must skip the
     sweep rather than fail the audit — an audit that FAILs on a missing
     optional binary trains operators to ignore it.
  3. The **dispositions** are named and PR-routing points at M73's door.
     A disposition list that omits `/hotfix` re-opens the dead end M73
     closed; a second intake mechanism is the thing D-043 rejected.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23) and steers clear of `**bold**` splits
(M26); phrases are matched case-insensitively. The target is read per-test,
never cached on the class — the mutation harness runs a single method and
skips `setUpClass` (M61).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def milestone():
    return SKILLS.joinpath("milestone", "SKILL.md").read_text().lower()


class TestInboxEnumeration(unittest.TestCase):
    def test_step_names_the_issue_command(self):
        # Without a command the bullet is a duty with no discharge — the
        # exact defect M74 exists to fix.
        self.assertIn(
            "`gh issue list --state open --json number,title,url` for issues,",
            milestone(),
        )

    def test_step_names_the_pr_command(self):
        # Both inboxes, not just issues: external PRs are half of D-043's
        # intake surface.
        self.assertIn(
            "`gh pr list --state open --json number,title,url,author` for prs",
            milestone(),
        )

    def test_step_applies_search_first_before_proposing(self):
        # Ordering is the rule: sweep, *then* propose. Reversed, the sweep
        # becomes a dedup pass after the duplicate row already exists.
        self.assertIn("apply the search-first rule to every hit before proposing", milestone())

    def test_step_names_all_three_sweep_targets(self):
        # Dropping any one target silently narrows the search-first rule the
        # rulebook states in full.
        self.assertIn(
            "the existing `candidate` rows, `milestones/archive/`, and `decisions.md`,",
            milestone(),
        )

    def test_own_prs_are_filtered_out_before_the_sweep(self):
        # M74 review F1: the bullet says "external" PRs and fetches `author`,
        # but nothing used it — so the audit enumerated cairn's own in-review
        # milestone PR as an inbox item and could propose adopting a PR this
        # session authored. The filter is what makes the list an *inbox*.
        t = milestone()
        self.assertIn("drop this session's own work from the pr list", t)
        self.assertIn("is cairn's own in-flight work", t)

    def test_own_pr_filter_names_the_branch_shapes(self):
        # Author alone is not enough: an operator's own milestone PR is
        # authored by them, so the branch shape is the reliable signal.
        self.assertIn("one whose head branch is `m<nn>-*` or", milestone())

    def test_sweep_is_read_only_against_github(self):
        # Scope guard: cairn reads the inbox, it never manages it.
        self.assertIn("never write to", milestone())
        self.assertIn("github (no labels, comments, or closes)", milestone())


class TestDegradation(unittest.TestCase):
    def test_step_names_all_three_failure_modes(self):
        self.assertIn(
            "when `gh` is missing, unauthenticated, or the repo has no remote:",
            milestone(),
        )

    def test_degradation_reports_which_mode_it_hit(self):
        # "Skipped" without a reason is indistinguishable from "found
        # nothing" — the operator can't tell an empty inbox from no `gh`.
        self.assertIn(
            "name which of the three it was, skip the sweep, and finish the audit.",
            milestone(),
        )

    def test_degradation_is_never_an_audit_failure(self):
        # The load-bearing line: an optional binary's absence must not turn
        # the health audit red.
        self.assertIn("an unreachable inbox is a reported gap, never an audit `fail`.", milestone())


class TestDispositions(unittest.TestCase):
    def test_sweep_resolves_at_the_route_step(self):
        self.assertIn("the §2 inbox sweep resolves here, and nowhere else.", milestone())

    def test_each_item_takes_exactly_one_disposition(self):
        # "exactly one" is the rule; asserting the bare prefix would survive
        # an edit to "exactly two dispositions".
        self.assertIn("each item takes exactly one disposition", milestone())

    def test_candidate_row_is_the_default(self):
        # The LABEL is the routing rule, so it is part of the assertion: a
        # clause pinned without its label survives having the label swapped
        # (caught at M74 review — the guard passed against `candidate row`
        # rewritten to `do nothing`).
        self.assertIn(
            "**candidate row** — the default for anything real but not urgent",
            milestone(),
        )

    def test_hotfix_disposition_covers_bugs_and_external_prs(self):
        self.assertIn(
            "**`/hotfix`** — a user-visible bug, or an external pr that meets the",
            milestone(),
        )

    def test_pr_routing_reuses_m73s_door(self):
        # AC4 / D-043: the door already exists. A second intake mechanism is
        # the thing that decision explicitly rejected.
        self.assertIn("this is the door m73 opened; route to it rather than inventing", milestone())

    def test_larger_work_routes_to_milestone_plan(self):
        self.assertIn(
            "**`/milestone-plan`** — anything larger than the hotfix bar.",
            milestone(),
        )

    def test_leave_disposition_requires_a_reason(self):
        self.assertIn("**leave** — no row, no action, with the reason stated.", milestone())


class TestVerbatimBar(unittest.TestCase):
    def test_dispositions_are_shown_verbatim_above_the_chip(self):
        self.assertIn(
            "show every proposed disposition verbatim above the chip, never a count or a",
            milestone(),
        )

    def test_rationale_for_the_verbatim_bar_survives(self):
        # The *why* is what stops a future compression pass from trading the
        # rule for a summary line.
        self.assertIn("paraphrase would have them approve text they never saw.", milestone())

    def test_route_step_still_carries_exactly_one_routing_chip(self):
        # M74 extended the existing triage option rather than adding a second
        # chip. Scope of this guard, stated honestly (M74 review F4): it pins
        # the singular framing and that the token appears once — it cannot
        # detect an unrelated AskUserQuestion block added elsewhere, and does
        # not claim to. A bare assertIn on the token would have been a
        # presence check on pre-existing text, locking nothing M74 added.
        t = milestone()
        self.assertIn("end with\none routing chip (askuserquestion)", t)
        self.assertEqual(t.count("routing chip (askuserquestion)"), 1)


if __name__ == "__main__":
    unittest.main()
