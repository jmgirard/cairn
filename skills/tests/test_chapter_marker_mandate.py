"""Regression guard: chapter markers are a per-phase mandate (M28).

The navigable TOC in cairn's Claude Code runtime is built from chapter
markers, not markdown headers (M27/D-020). M28 promotes the output-discipline
"Chapter markers" rule from "where the harness supports it" to a hard
per-phase mandate: every phase skill carries a one-line chapter-marker
directive, and tracking-rules declares both the mandate and the no-mechanism
fallback (so a chapter-less harness degrades to the phase headers, not to a
broken call).

Guard tests read each file as one string, so an asserted phrase must live on
one physical line (M23 lesson).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

# Every phase skill carries the chapter-marker directive — review INCLUDED:
# chapter markers are orthogonal to the routing-chip exception (review is
# chip-less but still has phases worth navigating). This list is therefore
# the full nine, unlike NON_REVIEW_CHIP_SKILLS in test_gate_wording.py.
SKILLS_WITH_CHAPTER_DIRECTIVE = [
    "milestone-plan",
    "milestone-implement",
    "milestone-review",
    "milestone-brief",
    "hotfix",
    "cairn-init",
    "cairn-release",
    "milestone",
    "design-interview",
]

# The single-line directive token each skill carries, matched
# case-insensitively (mirrors how each skill carries a `Phase header:` line).
DIRECTIVE_TOKEN = "chapter markers: mark a chapter at each phase transition"


def read(*parts):
    return (SKILLS.joinpath(*parts)).read_text()


class TestChapterMarkerMandate(unittest.TestCase):
    def test_each_skill_carries_the_chapter_marker_directive(self):
        for skill in SKILLS_WITH_CHAPTER_DIRECTIVE:
            text = read(skill, "SKILL.md").lower()
            with self.subTest(skill=skill):
                self.assertIn(
                    DIRECTIVE_TOKEN,
                    text,
                    f"{skill}: must carry the chapter-marker directive "
                    f"'{DIRECTIVE_TOKEN}' on one line",
                )

    def test_rulebook_declares_the_per_phase_mandate(self):
        text = read("shared", "tracking-rules.md").lower()
        self.assertIn("per-phase mandate", text)
        self.assertIn("mark a chapter at each phase transition", text)

    def test_rulebook_declares_the_no_mechanism_fallback(self):
        text = read("shared", "tracking-rules.md").lower()
        self.assertIn("where the runtime provides no chapter mechanism", text)
        self.assertIn("phase headers are the visual fallback", text)


if __name__ == "__main__":
    unittest.main()
