"""Regression guard: the freshness-spawns clause under a spawn-restricting
harness instruction (M165).

Some Claude Code surfaces append a harness line restricting subagent spawns
to ones the user requested. Adopter repos read that line as forbidding
cairn's freshness-mandated readers and reviewers and silently degraded to
author-inline runs. The clause in tracking-rules "Model and agent strategy"
resolves the conflict in three parts, each pinned here: (a) a cairn skill
invocation IS the user's request for the spawns its steps mandate; (b) a
session that still cannot or will not spawn surfaces the conflict at its
phase's pending user gate; (c) an inline author-run is only ever a
user-accepted, logged deviation.

Anchors are copied from the shipped bytes; phrases crossing the file's hard
wrap are matched with `\\s+` so a reflow does not red a rule still present
(M105). Targets are read with `Path.read_text` because the mutation engine
patches only that call (M100).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def rules():
    return SKILLS.joinpath("shared", "tracking-rules.md").read_text()


class TestFreshnessSpawnInstructionClause(unittest.TestCase):
    """AC1's clause in tracking-rules "Model and agent strategy"."""

    def test_skill_invocation_is_the_users_spawn_request(self):
        # (a) — without this, the harness line reads as forbidding every
        # freshness spawn and the degradation this milestone fixes returns.
        self.assertRegex(
            rules(),
            r"is satisfied by the user's invocation of a cairn skill: that "
            r"invocation is the user's\s+request for the subagent spawns the "
            r"skill's steps mandate",
        )

    def test_a_blocked_session_surfaces_the_conflict_at_the_pending_gate(self):
        # (b) — the gate, not silence; for review that gate is the
        # merge-approval chip with the review declared degraded.
        self.assertRegex(
            rules(),
            r"surfaces the conflict at its phase's pending user gate — for "
            r"review, the\s+merge-approval chip, with the review declared "
            r"degraded \(author-inline\) — asking the user to request the "
            r"spawns in so\s+many words",
        )

    def test_the_chip_explains_author_inline_in_plain_words(self):
        # Accessible-language rule applied to this chip: the decision surface
        # says what a degraded run means, with no record identifiers.
        self.assertRegex(
            rules(),
            r"the chip says in plain words what an author-inline run means "
            r"\(the work was checked only by the session\s+that produced it\)",
        )

    def test_an_inline_author_run_is_a_logged_deviation_never_silent(self):
        # (c) — the operative half is "never silent": a permitted deviation
        # that need not be logged is the silent degradation itself.
        self.assertRegex(
            rules(),
            r"permitted only as a user-accepted, logged deviation naming "
            r"the\s+instruction, never silent",
        )


if __name__ == "__main__":
    unittest.main()
