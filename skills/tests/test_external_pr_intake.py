"""Regression guard: the M73/D-043 external-PR intake path.

Locks the door the intake doctrine named but never had. Two halves:

  1. `/hotfix` is **bidirectional** — it can author a fix or adopt one. The
     adopted form is not a cosmetic variant: it checks the contributor's
     branch out instead of cutting its own, and its regression test is
     proved against the default branch rather than against the pre-fix
     state (which no longer exists once the fix is in hand). Losing either
     sentence turns adoption back into "cut a branch and orphan the PR".
  2. The **routing** — the skill's `description:` frontmatter has to fire on
     an incoming PR at all, and the rulebook's Intake paragraph has to name
     `/hotfix` as the door. Before M73 the doctrine named a destination with
     no entry point; a silent revert restores exactly that dead end.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23) and steers clear of `**bold**` splits
(M26); phrases are matched case-insensitively. The target files are read
per-test, never cached on the class — the mutation harness runs a single
method and skips `setUpClass` (M61).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def rules():
    return SKILLS.joinpath("shared", "tracking-rules.md").read_text().lower()


def hotfix():
    return SKILLS.joinpath("hotfix", "SKILL.md").read_text().lower()


class TestAdoptionPath(unittest.TestCase):
    def test_tier_check_reads_the_contributors_diff(self):
        # The bar is applied to *their* diff; without this the step has no
        # way to judge a PR it did not author.
        self.assertIn("`gh pr diff <n>` — and tier-check *that* diff.", hotfix())

    def test_over_bar_prs_keep_todays_disposition(self):
        # Scope guard: M73 added an entry point, not a new disposition.
        self.assertIn("an incoming pr over the hotfix bar takes that same", hotfix())

    def test_branch_step_checks_the_pr_out(self):
        self.assertIn("*adopting a pr:* run `gh pr checkout <n>`", hotfix())

    def test_branch_step_states_the_naming_exemption(self):
        # Without the exemption an operator "fixes" the branch name to match
        # the hotfix-<slug> contract and detaches the PR.
        self.assertIn("name is **exempt** from the `hotfix-<slug>` contract", hotfix())

    def test_rulebook_carries_the_same_exemption(self):
        # stated<->stated: the contract lives in the git model, so the
        # exemption has to be visible to a reader who never opens the skill.
        self.assertIn("**an adopted external pr is the exception:**", rules())


class TestAdoptedRegressionTest(unittest.TestCase):
    def test_step_names_the_adopted_sequence(self):
        # The load-bearing honesty: fail-before-fix is unreachable here, so
        # the test is proved in the other direction instead.
        self.assertIn(
            "on the pr head**. prove both directions: run it on the pr head, then in a",
            hotfix(),
        )

    def test_step_says_the_author_side_sequence_is_unreachable(self):
        self.assertIn('"fails before the fix" sequence is unreachable', hotfix())

    def test_worktree_recipe_is_located_and_cleaned_up(self):
        # A worktree created inside the repo lingers as an untracked dir and
        # trips step 2's own dirty-tree check on the next /hotfix run.
        t = hotfix()
        self.assertIn("throwaway worktree of the default branch created **outside the repo**", t)
        self.assertIn("test file copied in — then `git worktree remove` it.", t)

    def test_contributor_supplied_tests_are_reverified(self):
        # Adopting evidence on trust is how an untested fix reaches main.
        self.assertIn("check — adopting a pr means verifying its evidence", hotfix())


class TestForkFallback(unittest.TestCase):
    def test_step_covers_the_entry_already_present_case(self):
        self.assertIn("duplicate; if none is present, add one.", hotfix())

    def test_step_names_the_no_push_fallback(self):
        self.assertIn("**when the head branch cannot be pushed to:**", hotfix())

    def test_fallback_asks_the_contributor_first(self):
        # Order matters: the contributor's work stays theirs unless they go
        # silent. A re-land-first fallback would take credit by default.
        self.assertIn("pr to add the missing pieces — it is their work", hotfix())

    def test_closing_a_contributors_pr_is_user_gated(self):
        # M73 review finding 2: re-landing closes someone else's PR under the
        # user's GitHub identity. Outward-facing and irreversible from their
        # side, so it never happens without an explicit chip — the same
        # consent discipline the merge itself gets (IP1).
        t = hotfix()
        self.assertIn("and irreversible from the contributor's side, so it is **never** done", t)
        self.assertIn("= re-land, with a decline option), showing the closing comment's text in", t)

    def test_declining_the_re_land_leaves_the_pr_alone(self):
        self.assertIn("declined → leave their pr open and stop.", hotfix())

    def test_second_pr_prohibition_admits_the_fallback(self):
        # Without the carve-out the step forbids at :68 what it requires at
        # :78 — a future agent either deadlocks or reports a rule violation.
        self.assertIn("never open a second one, except", hotfix())

    def test_fallback_never_trades_away_the_regression_test(self):
        self.assertIn("never merge a fix whose regression test", hotfix())

    def test_delete_branch_caveat_for_forks(self):
        self.assertIn("drop `--delete-branch` on a", hotfix())


class TestIntakeRouting(unittest.TestCase):
    def test_description_frontmatter_fires_on_an_incoming_pr(self):
        # Skill descriptions are the only trigger surface; a description that
        # names only bug *reports* leaves the door unreachable in practice.
        self.assertIn("or adopt an incoming external pr that fixes one", hotfix())
        self.assertIn('"adopt pr #12", "review this external pr"', hotfix())

    def test_intake_paragraph_names_hotfix_as_the_door(self):
        self.assertIn("**`/hotfix` is the door**", rules())

    def test_intake_paragraph_keeps_the_larger_pr_route(self):
        self.assertIn("becomes/joins a milestone via `/milestone-plan`", rules())

    def test_no_second_approval_mechanism(self):
        # M73 reuses M72's PR-bound marker; a second marker file or a prose
        # yes/no would fork the approval path IP1 depends on.
        text = hotfix()
        self.assertEqual(text.count("cairn/.merge-approved"), 1)
        self.assertIn("approved yyyy-mm-dd for pr #<n>", text)


if __name__ == "__main__":
    unittest.main()
