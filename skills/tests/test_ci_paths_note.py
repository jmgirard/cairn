"""Prose guard: cairn-init names the CI runs tracking-only pushes start (M178)
and applies the ignore under a chip (M181).

A milestone loop's checkpoint pushes start every push-triggered workflow,
and a review appeared to end before CI was green when it was only implement's
tracking-only pushes running. M178 adds a `/cairn-init` §0 environment-check
bullet that reports the fact from `scripts/cairn_ci_paths.py --report` (AC1),
and one git-model bullet in the rulebook plus a pointer in the wait rule's
no-checks clause (AC4). M181 rewrites the bullet's clause (d): a dry run of
`--apply`, one approve/decline chip, a decline writing nothing, the applied
edit left uncommitted, and the by-hand suggestion for refused files. One
phrase per clause is pinned here, each on one physical line of its target
(M148: reword new prose, never a pinned neighbour), and each pin is
registered in the mutation harness. The ignore's two tokens are spelled by
concatenation so the AC5 grep finds them only where they are shipped (M169).

Targets are read with `Path.read_text` because the mutation engine patches
only that call (M100). Hand-run only (M144, D-109):

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

IGNORE = "paths-" + "ignore"
GLOB = "cairn/" + "**"


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def init():
    return read("cairn-init", "SKILL.md")


def rules():
    return read("shared", "tracking-rules.md")


def section(text, start, end):
    """The slice of `text` between the first `start` and the next `end`."""
    return text.split(start, 1)[1].split(end, 1)[0]


class TestInitBulletRunsTheProbe(unittest.TestCase):
    """AC1: the bullet runs the report only where workflows exist."""

    def test_the_bullet_sits_in_section_zero(self):
        zero = section(init(), "## 0. Detect the situation", "## 1. Fresh scaffold")
        self.assertIn("CI runs on tracking-only pushes", zero)

    def test_the_bullet_runs_the_report_probe(self):
        self.assertIn(
            'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_ci_paths.py" --report',
            init(),
        )

    def test_the_bullet_is_silent_without_workflows(self):
        self.assertIn("when it does not, this bullet is silent", init())


class TestInitBulletStatesTheFact(unittest.TestCase):
    """AC1 (a)–(c): what the bullet tells the adopter."""

    def test_clause_a_tracking_only_pushes_start_ci(self):
        self.assertIn("reach the remote on every branch push", init())

    def test_clause_b_pull_request_triggers_are_not_helped(self):
        self.assertIn("skips a tracking-only push only for `push` triggers", init())

    def test_clause_c_branch_protection_blocks(self):
        self.assertIn("that check pending and blocks the merge", init())


class TestInitBulletSuggestsTheEdit(unittest.TestCase):
    """AC1 (d), M178 remainder: a refused file keeps the by-hand suggestion."""

    def test_the_suggestion_targets_push_triggers_lacking_the_ignore(self):
        self.assertIn(f"whose `push` verdict lacks both `{GLOB}` and `paths`", init())

    def test_the_suggestion_names_the_item_to_add(self):
        self.assertIn(f"show the item to add — `- '{GLOB}'` under that trigger's `{IGNORE}`", init())


class TestInitBulletAppliesUnderAChip(unittest.TestCase):
    """AC1 (d), M181: dry run, chip, decline, apply, uncommitted edit."""

    def test_the_bullet_runs_the_dry_run(self):
        self.assertIn(
            'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_ci_paths.py" --apply --dry-run',
            init(),
        )

    def test_the_bullet_poses_one_chip(self):
        self.assertIn("pose one approve/decline chip naming those files", init())

    def test_a_decline_writes_nothing(self):
        self.assertIn("a decline writes nothing to the workflow files", init())

    def test_the_edit_is_left_uncommitted(self):
        self.assertIn("the edited workflow files are left uncommitted for the operator to commit", init())

    def test_missing_pyyaml_keeps_the_by_hand_path(self):
        self.assertIn("installing PyYAML enables the applied edit", init())

    def test_both_commit_bullets_exclude_the_edited_file(self):
        scaffold = section(init(), "## 1. Fresh scaffold", "## 2. Migration protocol")
        repair = init().split("## 3. Repair", 1)[1]
        self.assertIn("never a workflow file §0's chip\n  edited", scaffold)
        self.assertIn("a workflow file §0's chip edited", repair)
        self.assertIn("is never staged", repair)

    def test_both_close_blocks_name_the_edited_file(self):
        self.assertEqual(init().count("§0's chip edited and left\n  uncommitted"), 1)
        self.assertEqual(init().count("§0's chip edited and left uncommitted"), 1)


class TestRulebookGitModelBullet(unittest.TestCase):
    """AC4: the git model states the fact and defers mergeability."""

    def git_model(self):
        return section(rules(), "## Git and approval model", "## Context hygiene")

    def test_a_branch_push_starts_admitted_workflows(self):
        self.assertIn("push-triggered workflows whose `branches` filter admits it", self.git_model())

    def test_the_ignore_helps_push_triggers_only(self):
        self.assertIn(
            "skips such a push for `push` triggers and not for `pull_request` triggers",
            self.git_model(),
        )

    def test_a_pull_request_filter_reads_the_whole_diff(self):
        self.assertIn("whose filter reads the whole PR diff", self.git_model())

    def test_a_tracking_only_head_is_the_no_checks_case(self):
        self.assertIn("head commit carries no check run — the wait rule's no-checks case", self.git_model())

    def test_branch_protection_is_the_carve_out(self):
        self.assertIn("unless branch protection requires that check", self.git_model())

    def test_mergeability_is_deferred_to_the_wait_clause(self):
        self.assertIn("mergeability is the wait clause's to state", self.git_model())

    def test_the_no_checks_clause_points_at_the_bullet(self):
        self.assertIn(f"(one source: the git model's `{GLOB}` bullet)", self.git_model())


if __name__ == "__main__":
    unittest.main()
