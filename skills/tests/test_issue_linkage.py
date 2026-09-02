"""Regression guard: GitHub issues are linked at plan time and closed at
merge (M166, issue #168).

The nestedtune record showed five issues acknowledged nowhere for two days
while work on them was under way, an issue left open because a PR body said
`Answers #36` instead of a closing keyword, and a partial delivery whose
remainder existed only as the GitHub issue. Four skills carry the fix, each
pinned here:

  1. `/milestone-plan` fills the `Resolves:` slot from the issues the scope
     absorbs, rows a `partial` entry's remainder, and offers — never
     defaults to — an acknowledgement comment at the gate.
  2. `/milestone-review` ends the draft PR body with `Closes`/`Refs` lines,
     enumerates the post-merge issue writes in the merge chip, and reads
     each `closes` issue's state after the merge, closing what the keyword
     missed; an unreachable `gh` is reported, never a hygiene failure.
  3. `/hotfix` runs the same post-merge read for a `Fixes #N` PR.
  4. `/milestone` reports an issue still open after its closing milestone is
     done as an orphan, bounded to the retained terminal rows, and closes it
     only at the triage chip.

Phrases crossing the file's hard wrap are matched with `\\s+` (M105);
targets are read per test via `Path.read_text` so the mutation engine can
patch the read (M100, M61).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def plan():
    return SKILLS.joinpath("milestone-plan", "SKILL.md").read_text()


def review():
    return SKILLS.joinpath("milestone-review", "SKILL.md").read_text()


def hotfix():
    return SKILLS.joinpath("hotfix", "SKILL.md").read_text()


def milestone():
    return SKILLS.joinpath("milestone", "SKILL.md").read_text()


def template():
    return SKILLS.joinpath("shared", "templates", "milestone.md").read_text()


def archive_template():
    return SKILLS.joinpath("shared", "templates", "archive-summary.md").read_text()


class TestTemplateSlot(unittest.TestCase):
    """AC1: the slot exists on the milestone template and the archive
    summary's status line carries the entries after archiving."""

    def test_milestone_template_carries_the_slot_with_both_entry_forms(self):
        t = template()
        self.assertIn("- **Resolves:** —", t)
        self.assertIn("`#N closes`", t)
        self.assertIn("`#N partial`", t)

    def test_archive_status_line_carries_a_resolves_clause(self):
        self.assertRegex(archive_template(), r"\*\*Status:\*\*[^\n]*resolves <")


class TestPlanFillsTheSlot(unittest.TestCase):
    """AC2: step 4's trigger and the partial-remainder row."""

    def test_slot_is_filled_from_the_issues_the_scope_absorbs(self):
        # The trigger: without it the slot is a field nobody fills.
        self.assertRegex(
            plan(),
            r"the slot is filled from the issues the scope\s+absorbs — a "
            r"promoted candidate row citing one, or an issue the user\s+names",
        )

    def test_both_entry_forms_are_defined(self):
        self.assertRegex(
            plan(),
            r"`#N closes` when this milestone's PR closes\s+it, `#N partial` "
            r"when only part of it ships",
        )

    def test_partial_remainder_is_rowed_in_the_same_plan_commit(self):
        # nestedtune #33: the remainder's only record was the GitHub issue.
        self.assertRegex(
            plan(),
            r"A `partial` entry's\s+remainder is recorded as a `candidate` row "
            r"in the same plan commit",
        )
        self.assertRegex(plan(), r"listed in step 5's remainder ledger")

    def test_step_5_ledger_lists_the_partial_remainder(self):
        self.assertRegex(
            plan(),
            r"A `partial`\s+entry in the `Resolves:` slot lists its remainder "
            r"here with the candidate\s+row that holds it",
        )


class TestPlanGateAcknowledgement(unittest.TestCase):
    """AC2: one gate option, body shown first, posted only on selection."""

    def test_gate_poses_one_option_for_all_slotted_issues(self):
        self.assertRegex(
            plan(),
            r"the gate poses one option offering an\s+acknowledgement comment "
            r"on all slotted issues",
        )

    def test_comment_body_is_fixed_and_shown_before_selection(self):
        self.assertIn("`Queued as M<NNN>: <title>`", plan())
        self.assertRegex(
            plan(),
            r"for a `partial` entry, the remainder's\s+candidate-row text — "
            r"shown verbatim in the chat before selection",
        )

    def test_posted_only_on_selection_never_by_default(self):
        # The gate condition: every GitHub write stays behind a user gate.
        self.assertRegex(
            plan(),
            r"posted with `gh issue comment <N> --body` only on selection, "
            r"never by\s+default, and a declined option writes nothing to GitHub",
        )


if __name__ == "__main__":
    unittest.main()
