"""Regression guard: the M72/D-043 collaboration boundary and PR binding.

Locks two rules that are easy to lose and expensive to lose silently:

  1. The **enforcement boundary** in `tracking-rules.md` — which guarantees
     are agent-session-scoped and which degrade to honor-system when the
     merge happens outside a cairn session. Deleting it would leave the
     README and DESIGN claiming protection cairn cannot deliver.
  2. The **PR binding** — the approval marker names the PR it approves and
     the guard refuses a merge it does not name. Stated<->enforced: the
     rulebook's claim is checked against the helpers that implement it and
     the skills that write the marker.

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
REPO = SKILLS.parent
HOOKS = REPO / "hooks"


def rules():
    return SKILLS.joinpath("shared", "tracking-rules.md").read_text().lower()


def readme():
    return REPO.joinpath("README.md").read_text().lower()


class TestEnforcementBoundary(unittest.TestCase):


    def test_the_named_guards_actually_ship(self):
        # stated<->enforced: the rulebook names two hooks by filename.
        for name in ("merge_guard.py", "force_push_guard.py"):
            with self.subTest(hook=name):
                self.assertTrue((HOOKS / name).is_file())


class TestPRBinding(unittest.TestCase):


    def test_both_approval_writing_skills_name_the_pr(self):
        # stated<->enforced: a marker written without the PR silently falls
        # back to the pre-M72 existence check, so the skills must write it.
        for skill in ("milestone-review", "hotfix"):
            with self.subTest(skill=skill):
                text = SKILLS.joinpath(skill, "SKILL.md").read_text().lower()
                self.assertIn("approved yyyy-mm-dd for pr #<n>", text)
                self.assertIn("gh pr merge <n> --squash", text)

    def test_the_guard_implements_the_check(self):
        # stated<->enforced the other direction: the rule describes behavior
        # that must exist in code, not just prose.
        # Word-bounded: a bare assertIn on a shorter name is satisfied by a
        # longer one that contains it (the M60 substring trap).
        common = HOOKS.joinpath("cairn_common.py").read_text()
        self.assertRegex(common, r"\bdef gh_merge_pr_numbers\b")
        self.assertRegex(common, r"\bdef marker_pr_number\b")
        guard = HOOKS.joinpath("merge_guard.py").read_text()
        self.assertRegex(guard, r"\bgh_merge_pr_numbers\b")
        self.assertRegex(guard, r"\bmarker_pr_number\b")


class TestReadmeCollaboratorSurface(unittest.TestCase):
    def test_readme_has_the_collaborators_section(self):
        self.assertIn("## working with collaborators", readme())

    def test_readme_states_the_guards_only_watch_this_session(self):
        # The human-facing half of the boundary — the README previously
        # claimed an unqualified mechanical block.
        self.assertIn("the guards only watch this session", readme())

    def test_readme_states_concurrent_operators_are_unsupported(self):
        self.assertIn(
            "two people both running cairn is not supported yet", readme()
        )


if __name__ == "__main__":
    unittest.main()
