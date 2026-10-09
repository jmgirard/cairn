"""Regression guard: `/hotfix` reads and applies DESIGN.md's Conventions.

The rulebook says rules in `cairn/DESIGN.md` bind in addition to its own, but
`/hotfix` read only ROADMAP and DECISIONS. A repo whose Conventions require a
development-version bump on every PR (a guest repo copying its maintainers'
contributor docs, for example) got a hotfix PR with no bump. The milestone
path catches this at review, where the diff reviewer reads DESIGN.md
conventions; a hotfix has no reviewer, so the skill must read them itself.

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


def hotfix():
    return SKILLS.joinpath("hotfix", "SKILL.md").read_text().lower()


def step(text, start, end):
    """The text of one numbered workflow step, bounded by the next one."""
    lo = text.index(start)
    return text[lo:text.index(end, lo)]


class TestHotfixReadsConventions(unittest.TestCase):
    def test_session_start_reads_the_conventions_section(self):
        head = hotfix().split("## workflow")[0]
        self.assertIn("`cairn/design.md`'s conventions section", head)

    def test_step_five_applies_a_version_bump_convention(self):
        five = step(hotfix(), "5. add a changelog entry", "6. **approval gate")
        self.assertIn("conventions section", five)
        self.assertIn("development-version bump", five)

    def test_no_convention_means_no_bump(self):
        # D-041: cairn never bumps a version on its own cadence; only the
        # repo's stated convention triggers one.
        five = step(hotfix(), "5. add a changelog entry", "6. **approval gate")
        self.assertIn("states none, no version is bumped", five)

    def test_approval_gate_shows_the_bump(self):
        six = step(hotfix(), "6. **approval gate", "7. if the fix revealed")
        self.assertIn("the version bump", six)


if __name__ == "__main__":
    unittest.main()
