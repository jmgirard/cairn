"""Guard: the copy-run handoff rule is wired at the steps that hand over (M86).

The rule ("Copy-run commands get their own fenced block") shipped central-only
in M35 and drifted — `/milestone-review` step 10 came to instruct the inline
form outright. D-048 wires a directive into the three skills that actually hand
the user a command, and holds `/milestone-implement`'s `/clear` line as a
*mention* so a later over-fire is caught here rather than left to judgment.

Skill-prose guards read the file as one string, so every asserted phrase lives
on a single source line (M23) and steers clear of `**bold**` splits (M26);
phrases are matched case-insensitively. Each negative assert is paired with a
positive one so it can carry a mutation entry (M53) — blanking cannot restore
an absence.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def skill(name):
    return SKILLS.joinpath(name, "SKILL.md").read_text().lower()


def fenced_regions(text):
    """Yield the body of each ``` / ~~~ fenced block, ignoring indentation."""
    body, fence = [], None
    for line in text.splitlines():
        marker = line.strip()[:3]
        if fence is None:
            if marker in ("```", "~~~"):
                fence, body = marker, []
        elif marker == fence:
            yield "\n".join(body)
            fence = None
        else:
            body.append(line)


class TestReviewCloseIsAHandoff(unittest.TestCase):
    def test_close_directs_the_commands_into_a_fenced_block(self):
        self.assertIn(
            "emit the commands in a fenced block, never inline backticks",
            skill("milestone-review"),
        )

    def test_the_superseded_inline_instruction_is_gone(self):
        """The exact wording D-048 removed must not creep back."""
        text = skill("milestone-review")
        self.assertIn("as copyable lines", text)  # positive: the fix is present
        self.assertNotIn("naming the obvious next action inline", text)


class TestBriefManualRunIsAHandoff(unittest.TestCase):
    def test_manual_run_prompt_goes_in_a_fenced_block(self):
        self.assertIn(
            "fenced block, never a blockquote or inline backticks",
            skill("milestone-brief"),
        )

    def test_the_blockquote_form_is_gone(self):
        text = skill("milestone-brief")
        self.assertIn("emit the prompt as its own copyable block", text)
        self.assertNotIn("> open a fresh fable session", text)


class TestReleaseChecklistIsAHandoff(unittest.TestCase):
    def test_terminal_actions_checklist_names_the_fenced_form(self):
        self.assertIn(
            "so each goes in a fenced block, never inline backticks",
            skill("cairn-release"),
        )


class TestImplementClearLineStaysAMention(unittest.TestCase):
    """D-048 (3): a line observing that a moment is safe is not a handoff.

    Pinned so a later uniform-fencing sweep trips a red test instead of
    silently pushing a copy button at the user for a situational note.
    """

    def test_the_clear_line_is_present_and_inline(self):
        text = skill("milestone-implement")
        self.assertIn("a safe `/clear` point", text)

    def test_implement_does_not_fence_the_clear_mention(self):
        """Structural, not phrase-based: no fenced region may carry `/clear`.

        An earlier form banned the literal words "fenced block" anywhere in the
        file. That was wrong in both directions — an edit that actually fenced
        the recap need not use those words, and a legitimate fourth handoff
        site elsewhere in this skill (D-048 anticipates one) would have turned
        it red for an unrelated reason, inviting deletion of the guard.
        """
        text = skill("milestone-implement")
        self.assertIn("a safe `/clear` point", text)  # positive anchor
        for region in fenced_regions(text):
            self.assertNotIn("/clear", region)

    def test_the_fence_detector_would_catch_an_over_fire(self):
        """Proves the check above is not vacuous (M84).

        `milestone-implement` has no fenced regions today, so the loop body
        never executes — an absence-assert that never runs proves nothing.
        This pins that the detector fires on the shape it is watching for.
        """
        over_fired = "note this is a safe `/clear` point:\n```\n/clear\n```\n"
        self.assertEqual(list(fenced_regions(over_fired)), ["/clear"])
        self.assertEqual(list(fenced_regions("no fences here")), [])


if __name__ == "__main__":
    unittest.main()
