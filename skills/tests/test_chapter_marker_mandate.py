"""Regression guard: chapter markers are a per-stretch mandate (M28, M171).

The navigable TOC in cairn's Claude Code runtime is built from chapter
markers, not markdown headers (M27/D-020). M28 promoted the output-discipline
"Chapter markers" rule to a hard per-phase mandate; M171 moves the cadence to
per-stretch — a chapter at each phase transition *and* at each stretch a
skill's `Chapter markers:` directive names (tasks, criteria, gate steps), the
session-start-implicit carve-out kept, chapter titles opening with the
`Tn:`/`ACn:` positional label where the stretch is a task or criterion — and
has the "Phase header" rule re-emit the `#`/`##` pair at each session start.

Per skill, the guard pins a stretch token from that skill's own directive
(nine entries replace M28's single shared token), so a skill whose directive
drifts back to the bare per-phase form fails here by name.

Guard tests read each file as one string, so an asserted phrase must live on
one physical line (M23 lesson).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

# The directive's shared opening — every phase skill still carries it, review
# INCLUDED (chapter markers are orthogonal to the phase-close rule).
DIRECTIVE_OPENING = "chapter markers: mark a chapter at each phase transition"

# Per skill, one stretch token from its own `Chapter markers:` directive —
# the stretch list AC2 (M171) promises, matched case-insensitively on one
# physical line.
STRETCH_TOKENS = {
    "milestone-plan": "investigation, the question gate, solidify-and-commit",
    "milestone-implement": "the question gate, each task",
    "milestone-review": "each acceptance criterion in step 3",
    "milestone-brief": "each phase its\n`phase header:` directive names",
    "hotfix": "at each numbered step",
    "cairn-init": "each phase its\n`phase header:` directive names",
    "cairn-release": "at each numbered step",
    "milestone": "each phase its\n`phase header:` directive names",
    "design-interview": "each phase its\n`phase header:` directive names",
}


def read(*parts):
    return (SKILLS.joinpath(*parts)).read_text()


class TestChapterMarkerMandate(unittest.TestCase):
    def test_each_skill_carries_the_chapter_marker_directive(self):
        for skill in STRETCH_TOKENS:
            text = read(skill, "SKILL.md").lower()
            with self.subTest(skill=skill):
                self.assertIn(
                    DIRECTIVE_OPENING,
                    text,
                    f"{skill}: must carry the chapter-marker directive "
                    f"'{DIRECTIVE_OPENING}' on one line",
                )

    def test_each_skill_directive_names_its_own_stretches(self):
        for skill, token in STRETCH_TOKENS.items():
            text = read(skill, "SKILL.md").lower()
            with self.subTest(skill=skill):
                self.assertIn(
                    token,
                    text,
                    f"{skill}: its `Chapter markers:` directive must name "
                    f"the stretch {token!r}",
                )

    def test_rulebook_declares_the_per_stretch_mandate(self):
        # AC1 (a): phase transitions plus directive-named stretch boundaries.
        text = read("shared", "tracking-rules.md").lower()
        self.assertIn("per-stretch mandate", text)
        self.assertIn("mark a chapter at each phase transition", text)
        self.assertIn("at each stretch boundary the", text)

    def test_rulebook_keeps_the_session_start_carve_out(self):
        # AC1 (b).
        text = read("shared", "tracking-rules.md").lower()
        self.assertIn("session start implicit", text)

    def test_rulebook_states_the_title_shape(self):
        # AC1 (c): positional label for a task or criterion, noun phrase else.
        text = read("shared", "tracking-rules.md").lower()
        self.assertIn(
            "a chapter's title opens with the item's positional label", text
        )
        self.assertIn("is a short noun phrase otherwise", text)

    def test_rulebook_phase_header_re_emits_at_session_start(self):
        # AC3: the `#`/`##` pair at each session start, post-`/clear` included.
        text = read("shared", "tracking-rules.md").lower()
        self.assertIn("pair is emitted at each session start", text)
        self.assertIn("a post-`/clear` session included", text)


if __name__ == "__main__":
    unittest.main()
