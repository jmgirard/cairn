"""Regression guard: cairn does not hardcode `main` (M22 / M25 / D-018 sibling).

The git model, the CLAUDE.md template, and `/cairn-init` speak of "the default
branch" (glossed `main`/`master`), and cairn-init detects the repo's actual
default branch rather than assuming `main`. A drift back to hardcoded-`main`
doctrine — which contradicts a `master` repo, as the M20 ackwards pilot found
(references/migration-pilot-notes.md G1/G9) — fails here.

M25 extends the lock to the *operational* skill steps: `/milestone-implement`,
`/milestone-review`, `/hotfix`, and `/cairn-release` issue no hardcoded-`main`
git command and each detects the branch at runtime via the canonical recipe in
the tracking-rules git model.

Also locks the weight-cap doctrine text to the cairn-section model (D-018),
not the retired whole-file `<80` cap.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

# Skills whose *steps* issue default-branch git commands (M25).
OPERATIONAL_SKILLS = [
    "milestone-implement",
    "milestone-review",
    "hotfix",
    "cairn-release",
]


def read(*parts):
    return (SKILLS.joinpath(*parts)).read_text()


def normalized(*parts):
    # Collapse whitespace so asserted phrases match across line wraps
    # (M23 lesson: assertIn on raw text fails across a newline).
    return re.sub(r"\s+", " ", read(*parts))


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


class TestDetectionRecipeInGitModel(unittest.TestCase):
    """The tracking-rules git model carries one canonical runtime recipe (M25 T1)."""

    def test_recipe_command_present(self):
        norm = normalized("shared", "tracking-rules.md")
        self.assertIn("git symbolic-ref --short refs/remotes/origin/HEAD", norm)

    def test_recipe_states_runtime_detection(self):
        norm = normalized("shared", "tracking-rules.md")
        # Operational skills re-detect at runtime; cairn stores no branch name.
        self.assertIn("re-detects it at runtime", norm)


class TestOperationalSkillsParameterized(unittest.TestCase):
    """The four operational skills' git steps are branch-name-agnostic (M25)."""

    def test_no_hardcoded_main_branch_name(self):
        # Whole-word `main` in these skills can only be the retired branch name
        # (substrings like "remaining"/"domain" carry no word boundary).
        for skill in OPERATIONAL_SKILLS:
            with self.subTest(skill=skill):
                text = read(skill, "SKILL.md")
                self.assertIsNone(
                    re.search(r"\bmain\b", text),
                    f"{skill}/SKILL.md hardcodes the branch name 'main'; use the "
                    "detected default branch (tracking-rules git model)",
                )

    def test_speaks_of_the_default_branch(self):
        for skill in OPERATIONAL_SKILLS:
            with self.subTest(skill=skill):
                self.assertIn("default branch", normalized(skill, "SKILL.md"))

    def test_references_canonical_detection_recipe(self):
        for skill in OPERATIONAL_SKILLS:
            with self.subTest(skill=skill):
                self.assertIn(
                    "tracking-rules git model",
                    normalized(skill, "SKILL.md"),
                    f"{skill}/SKILL.md must point at the canonical detection recipe",
                )


if __name__ == "__main__":
    unittest.main()
