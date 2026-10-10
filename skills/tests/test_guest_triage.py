"""Regression guard: the M235 guest arm of `/cairn-triage`.

In guest mode `cairn/` is never committed, so a triage pass cannot end in
its owner-mode docs-only commit. Before M235 the skill stopped at session
start for that reason. Now it runs, and its accepted edits stay on disk.
Two things have to survive:

  1. The pass runs in guest mode. The skill states the guest arm, the old
     stop sentence is gone, and the rulebook names the arm.
  2. The guest pass makes no commit and no push.

The pinned phrases wrap across source lines, so this guard collapses
whitespace on read, as `test_guest_fork_remote` does. The target is read
per-test, never cached on the class (M61).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

OLD_STOP = "stopped before enumeration: guest collaboration mode"


def norm(text):
    return " ".join(text.split())


def read(rel):
    return norm((SKILLS / rel).read_text(encoding="utf-8"))


class TestGuestTriageRuns(unittest.TestCase):
    def test_skill_states_the_guest_arm(self):
        text = read("cairn-triage/SKILL.md")
        self.assertIn("**Guest mode runs on disk**", text)
        self.assertIn(
            "the pass skips the clean-tree, default-branch, and sync "
            "preconditions below, because it moves no ref and commits nothing",
            text,
        )
        self.assertIn(
            "It runs steps 1–4 as written and step 5 with the stamp standing "
            "in for the commit message",
            text,
        )

    def test_old_stop_sentence_is_gone(self):
        self.assertNotIn(OLD_STOP, read("cairn-triage/SKILL.md"))

    def test_rulebook_names_the_guest_arm(self):
        text = read("shared/tracking-rules.md")
        self.assertIn(
            "**`/cairn-triage` runs** with its accepted edits written to "
            "`cairn/` on disk, never committed or pushed",
            text,
        )
        self.assertNotIn("**`/cairn-release` and `/cairn-triage` stop**", text)

    def test_readme_states_the_guest_arm(self):
        text = norm((SKILLS.parent / "README.md").read_text(encoding="utf-8"))
        self.assertIn(
            "**Triage stays on disk.** `/cairn-triage` runs as usual, but it "
            "skips the clean-tree, default-branch, and sync checks",
            text,
        )
        self.assertNotIn("No release walk, no triage pass", text)

    def test_step_two_reads_the_base_default_branch(self):
        text = read("cairn-triage/SKILL.md")
        self.assertIn(
            "`git cat-file -e <base>/<default-branch>:<path>`", text
        )


class TestGuestTriageCommitsNothing(unittest.TestCase):
    def test_step_six_guest_arm_makes_no_commit_or_push(self):
        text = read("cairn-triage/SKILL.md")
        self.assertIn("The guest pass makes no commit and no push", text)

    def test_stamp_carries_the_drop_evidence(self):
        text = read("cairn-triage/SKILL.md")
        self.assertIn(
            "the stamp also names, beside each refuted-premise or "
            "already-shipped drop, the record or path that holds its evidence",
            text,
        )


if __name__ == "__main__":
    unittest.main()
