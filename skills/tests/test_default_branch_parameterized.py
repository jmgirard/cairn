"""Regression guard: cairn does not hardcode `main` (M22 / D-018 sibling).

The git model, the CLAUDE.md template, and `/cairn-init` speak of "the default
branch" (glossed `main`/`master`), and cairn-init detects the repo's actual
default branch rather than assuming `main`. A drift back to hardcoded-`main`
doctrine — which contradicts a `master` repo, as the M20 ackwards pilot found
(references/migration-pilot-notes.md G1/G9) — fails here.

Also locks the weight-cap doctrine text to the cairn-section model (D-018),
not the retired whole-file `<80` cap.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return (SKILLS.joinpath(*parts)).read_text()


class TestDefaultBranchParameterized(unittest.TestCase):
    def test_git_model_uses_default_branch(self):
        text = read("shared", "tracking-rules.md")
        self.assertIn("The default branch (`main`/`master`) is a distribution", text)
        self.assertIn("the default branch", text)

    def test_git_model_drops_hardcoded_main(self):
        text = read("shared", "tracking-rules.md")
        for retired in [
            "**main is a distribution channel**",
            "Never implement on main",
            "origin/main is main",
            "up-to-date main",
        ]:
            self.assertNotIn(retired, text)

    def test_cairn_init_detects_default_branch(self):
        text = read("cairn-init", "SKILL.md")
        # Detection instruction present, and no bare-main branching doctrine.
        self.assertIn("symbolic-ref", text)
        self.assertIn("the default branch", text)
        self.assertNotIn("Never on main", text)
        self.assertNotIn("origin/main is main", text)

    def test_claude_md_template_uses_default_branch(self):
        text = read("shared", "templates", "claude-md-section.md")
        self.assertIn("the default branch", text)
        # The template carries no "main session" idiom, so a bare "on main"
        # here can only be the retired hardcoding.
        self.assertNotIn("on main", text)
        self.assertNotIn("directly to main", text)

    def test_weight_cap_doctrine_is_section_scoped(self):
        text = read("shared", "tracking-rules.md")
        self.assertIn("`## Project tracking` section of `CLAUDE.md`", text)
        self.assertNotIn("`CLAUDE.md` < 80", text)


if __name__ == "__main__":
    unittest.main()
