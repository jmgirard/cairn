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


class TestReviewPRBody(unittest.TestCase):
    """AC3: step 2's closing lines come from the slot."""

    def test_pr_body_ends_with_closes_and_refs_lines_from_the_slot(self):
        self.assertRegex(
            review(),
            r"The PR body ends with one\s+`Closes #N` line per `closes` entry "
            r"and one `Refs #N` line per `partial`\s+entry of the milestone's "
            r"`Resolves:` slot",
        )

    def test_dash_slot_adds_no_lines(self):
        self.assertIn("a slot of `—` adds no lines", review())


class TestReviewMergeChipAuthorizes(unittest.TestCase):
    """AC3: step 7's chip enumerates the post-merge issue writes."""

    def test_chip_text_enumerates_the_issue_writes_it_authorizes(self):
        self.assertRegex(
            review(),
            r"the chip's question text enumerates\s+the post-merge issue "
            r"writes it authorizes — close-if-open per `closes`\s+entry; a "
            r"comment naming what shipped and the remainder's candidate row"
            r"\s+per `partial` entry",
        )

    def test_no_other_issue_write_is_made(self):
        self.assertIn("no other issue write is made", review())


class TestReviewPostMergeRead(unittest.TestCase):
    """AC3: step 9 reads each `closes` issue and closes what the keyword
    missed; an unreachable `gh` is reported, never a hygiene failure."""

    def test_each_closes_entry_is_read_after_the_merge(self):
        self.assertRegex(
            review(),
            r"after the merge, for each `closes` entry of\s+the `Resolves:` "
            r"slot read the issue's state with\s+`gh issue view <N> --json state`",
        )

    def test_a_still_open_issue_is_closed_naming_the_merged_pr(self):
        self.assertRegex(
            review(),
            r"one still open is closed with\s+`gh issue close <N> --comment` "
            r"carrying a one-line comment naming the\s+merged PR",
        )

    def test_partial_comments_are_posted(self):
        self.assertRegex(
            review(),
            r"For each `partial`\s+entry post the comment naming what shipped "
            r"and the remainder's candidate\s+row",
        )

    def test_unreachable_gh_is_reported_and_never_fails_hygiene(self):
        self.assertRegex(
            review(),
            r"When `gh` is missing,\s+unauthenticated, or the repo has no "
            r"remote, name which of the three it\s+was in the done recap; an "
            r"unreachable `gh` never fails the hygiene pass",
        )

    def test_done_recap_reports_the_state_reads(self):
        self.assertIn("The done recap reports each entry's state read", review())


class TestHotfixPostMergeRead(unittest.TestCase):
    """AC3: `/hotfix` step 7 runs the same read for a `Fixes #N` PR."""

    def test_fixes_line_triggers_the_read_and_close_if_open(self):
        self.assertRegex(
            hotfix(),
            r"When the PR body carries a `Fixes #N`\s+line, read that issue's "
            r"state after the merge with\s+`gh issue view <N> --json state`; "
            r"one still open is closed with\s+`gh issue close <N> --comment`",
        )

    def test_no_fixes_line_is_a_noop(self):
        self.assertIn("a PR with no such line is a no-op here", hotfix())

    def test_unreachable_gh_is_reported_never_a_failure(self):
        self.assertRegex(
            hotfix(),
            r"When `gh` is missing,\s+unauthenticated, or the repo has no "
            r"remote, name which of the three it\s+was in the recap — never a "
            r"failure",
        )


class TestAuditOrphanBullet(unittest.TestCase):
    """AC5: the §2 orphan read, bounded and read-only, and the §3 close."""

    def test_reads_are_bounded_to_the_retained_terminal_rows(self):
        self.assertRegex(
            milestone(),
            r"for each `done` row still in the ROADMAP table — the\s+retained "
            r"terminal rows bound the reads",
        )

    def test_a_closes_entry_is_read_with_state_and_url(self):
        self.assertRegex(
            milestone(),
            r"carries a `resolves` entry marked `closes`, read that issue's "
            r"state\s+with `gh issue view <N> --json state,url`",
        )

    def test_a_still_open_issue_is_an_orphan(self):
        self.assertRegex(
            milestone(), r"one still open is reported as\s+an orphan"
        )

    def test_no_entry_and_partial_only_read_nothing_multi_entry_reads_each(self):
        # The archive-fixture variants: no clause, partial only, several.
        self.assertRegex(
            milestone(),
            r"A row with no\s+`resolves` clause, or with `partial` entries "
            r"only, reads nothing; a row\s+with several `closes` entries "
            r"reads each",
        )

    def test_orphan_read_writes_nothing(self):
        self.assertIn("the orphan read writes nothing", milestone())

    def test_unreachable_gh_rule_applies_unchanged(self):
        self.assertRegex(
            milestone(),
            r"The inbox bullet's\s+unreachable-`gh` rule applies unchanged: "
            r"name which of the three it was,\s+skip the reads, finish the audit",
        )

    def test_never_write_sentence_is_narrowed_to_the_reads(self):
        # M74's rule now names its subjects — the sweep and the orphan read —
        # and points at the one gated write.
        self.assertRegex(
            milestone(),
            r"the sweep and the orphan\s+read below never write to\s+GitHub",
        )
        self.assertRegex(
            milestone(),
            r"the one audit-path write is §3's close disposition, at the user's"
            r"\s+selection",
        )

    def test_close_disposition_fires_only_on_selection_naming_the_pr(self):
        self.assertRegex(
            milestone(),
            r"\*\*close\*\* — an orphaned issue from §2's orphan bullet: only "
            r"on the\s+user's selection in the triage chip, close it with"
            r"\s+`gh issue close <N> --comment` carrying a one-line comment "
            r"naming the\s+archived milestone's PR",
        )
        self.assertIn("Not selected → the issue stays open and nothing is written", milestone())


class TestReadmeStatesTheThreeBehaviors(unittest.TestCase):
    """AC6: the collaborators section states each behavior the skills ship."""

    def readme(self):
        return SKILLS.parent.joinpath("README.md").read_text()

    def test_plan_time_acknowledgement_offer(self):
        self.assertRegex(
            self.readme(),
            r"plan gate offers one option to post `Queued as M<NNN>: <title>`",
        )
        self.assertRegex(self.readme(), r"posted only if you select it, never by default")

    def test_pr_closing_keyword(self):
        self.assertRegex(
            self.readme(),
            r"draft PR body ends with `Closes #N` \(or `Refs #N` for an issue"
            r"\s+only partly resolved\)",
        )

    def test_post_merge_check_and_audit_orphan(self):
        self.assertRegex(
            self.readme(),
            r"review reads each issue's state and closes one still open with"
            r"\s+a comment naming the merged PR",
        )
        self.assertRegex(
            self.readme(),
            r"audit reports an issue\s+still open after its milestone is done "
            r"and offers to close it at the\s+triage chip",
        )


if __name__ == "__main__":
    unittest.main()
