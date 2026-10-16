"""Regression guard: stacked guest milestones (M268).

In guest mode with `# Push remote: base`, a milestone can depend on one
handed-off milestone (a stack base) and build on its branch. These things
have to survive:

  1. The rulebook's definition: a stack base, the at-most-one rule, the
     `stack base:` work-log line, a stacked milestone, and the restack.
  2. `/milestone-implement` step 1: the stops on two or more stack bases,
     on a stack-base PR that is not open, and on a branch missing from the
     base repo; step 2: the cut, the `--onto` sync from the recorded tip,
     and the restack with its conditional retarget.
  3. `/milestone-review` step 8: `--base` while the base PR is open, and
     the route to the restack once it merged.
  4. `/milestone` §2: the merged-stack-base route.

A second test removes each clause and sees the check fail on it alone.
The pinned phrases wrap across source lines, so this guard collapses
whitespace on read (the M171 exception to the one-line convention, M23).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

CLAUSES = {
    "shared/tracking-rules.md": [
        "a **stack base** is a dependency whose ROADMAP row is `blocked` and whose milestone file's `Branch/PR` header names a PR URL.",
        "If each dependency of a `planned` milestone is `done` or a stack base, and at most one is a stack base, the milestone is workable",
        "Owner mode, and guest mode without the line, never stack: a dependency there must be `done`.",
        "It writes the work-log line `stack base: <branch> at <sha>` at the cut and at each sync.",
        "A **stacked milestone** is one whose newest `stack base:` line names a branch other than the default branch.",
        "(workable only when dependencies are `done`, or in guest mode when one of them is a stack base and the rest are `done`",
        "Once `<base-pr>` merges, the **restack** rebases the branch onto the default branch and retargets the PR:",
        "An archived dependency is `done`, so it is met as `done`, not as a stack base.",
        "Read each PR with `gh pr view <n> --repo <base-repo> --json headRefName`. The match is `<base-pr>`.",
        "Its stack base stays the dependency whose PR's `headRefName` is the branch that its first `stack base:` line names, also after that dependency turns `done`.",
        "(or from a stack base's branch, below)",
        "and an open stacked one whose stack base's PR merged to `/milestone-implement` for the restack",
    ],
    "milestone-implement/SKILL.md": [
        "A milestone with two or more stack-base dependencies stops with a close block naming them",
        "If that URL's owner and repo are not `<base-repo>`, ignoring case, stop with a close block naming the URL.",
        "A state other than `OPEN` stops, and its next command is `/milestone`",
        "A `baseRefName` other than the default branch stops, because the stack base is itself stacked",
        "A `headRepositoryOwner` login other than the base repo's owner, ignoring case, stops",
        "When `git ls-remote <base> <stack-base-branch>` prints no `refs/heads/<stack-base-branch>` line, stop with a close block naming the branch",
        "`git checkout -b <slug> <base>/<stack-base-branch>`, then a work-log line `stack base: <stack-base-branch> at <sha>`",
        "A stacked milestone runs the stacked sync below instead of that rebase.",
        "`<old>` is the base tip that the newest `stack base:` line names.",
        "While it is `OPEN`, run `git rebase --onto <base>/<stack-base-branch> <old> <slug>`.",
        "restack), run `git rebase --onto <base>/<default-branch> <old> <slug>`.",
        "A branch never pushed stays local. The lease names the remote branch tip that the check read, never `<old>`.",
        "`<N>` is the milestone's own PR, from its header.",
        "It writes the line last, after its rebase, push, and any retarget are done. A sync that stops writes no line",
        "After any stacked sync, re-run the active profile's `verify` slot before continuing.",
        "If that still names the stack-base branch, run `gh pr edit <N> --repo <base-repo> --base <default-branch>`.",
        "A `blocked` stacked milestone whose stack base's PR is `MERGED` resumes for the restack",
    ],
    "milestone-review/SKILL.md": [
        "read the stack base's PR with `gh pr view <base-pr> --repo <base-repo> --json state`. If it is `MERGED`, push nothing and open no PR.",
        "stop with a close block whose next command is `/milestone-implement M<NNN>`, whose stacked sync does the restack.",
        "If it is `OPEN`, the create below adds `--base <stack-base-branch>`, and its body names the stack base's PR (`#<base-pr>`)",
        "If it is `CLOSED`, push nothing, open no PR, change no status, and stop with a close block naming the closed PR",
        "A stacked milestone takes that step's stacked sync instead of the plain rebase, whether or not the default branch moved, but only while the stack base's PR is `OPEN`.",
    ],
    "milestone/SKILL.md": [
        "`OPEN` on a stacked milestone (tracking-rules \"Collaboration mode\") whose stack base's PR reads `MERGED`",
        "the restack is owed: route to `/milestone-implement M<NNN>`",
        "`OPEN` on a stacked milestone whose stack base's PR reads `CLOSED` → report it with no route",
    ],
}


def norm(text):
    return " ".join(text.split())


def read(rel):
    return norm(SKILLS.joinpath(rel).read_text(encoding="utf-8"))


def missing(text, clauses):
    return [c for c in clauses if c not in text]


class TestStackedClauses(unittest.TestCase):
    def test_present(self):
        for rel, clauses in CLAUSES.items():
            with self.subTest(file=rel):
                self.assertEqual(missing(read(rel), clauses), [])

    def test_each_removed_clause_fails(self):
        for rel, clauses in CLAUSES.items():
            text = read(rel)
            for clause in clauses:
                with self.subTest(file=rel, clause=clause):
                    self.assertEqual(missing(text.replace(clause, ""), clauses), [clause])


if __name__ == "__main__":
    unittest.main()
