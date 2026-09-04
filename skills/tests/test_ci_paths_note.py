"""Prose guard: cairn-init names the CI runs tracking-only pushes start (M178).

A milestone loop's checkpoint pushes start every push-triggered workflow,
and a review appeared to end before CI was green when it was only implement's
tracking-only pushes running. M178 adds a `/cairn-init` §0 environment-check
bullet that reports the fact from `scripts/cairn_ci_paths.py --report` and
offers its `--apply` under a chip (AC1), and one git-model bullet in the
rulebook plus a pointer in the wait rule's no-checks clause (AC4). One phrase
per AC1 clause and per AC4 claim is pinned here, each on one physical line of
its target (M148: reword new prose, never a pinned neighbour), and each pin
is registered in the mutation harness. The ignore's two tokens are spelled
by concatenation so the AC5 grep finds them only where they are shipped
(M169).

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


class TestInitBulletOffersTheApply(unittest.TestCase):
    """AC1 (d): the apply is offered under a chip, applicable files only."""

    def test_the_apply_is_offered_for_applicable_files_only(self):
        self.assertIn("only for the files the report marks `applicable`", init())

    def test_the_apply_rides_the_confirmation_round_or_its_own_chip(self):
        self.assertIn("else as its own single approve/decline chip", init())

    def test_the_apply_names_the_ignore_it_adds(self):
        self.assertIn(f"adds `- '{GLOB}'` under each `push` trigger's `{IGNORE}`", init())


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
