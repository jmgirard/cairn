"""Regression guard: every skill that reads `${CLAUDE_PLUGIN_ROOT}` states the
base-directory fallback.

Under the symlink / skills-directory install (README "Dev install"), Claude
Code leaves `CLAUDE_PLUGIN_ROOT` unset in the shell — it is expanded in
hooks.json `command` fields only (references/claude-code-hooks.md). A skill
step spelled `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py"`
then runs against `/scripts/...` and fails. Each skill must therefore tell
the reader to resolve the plugin root from the harness-printed
`Base directory for this skill:` line whenever the variable is empty, before
its first `${CLAUDE_PLUGIN_ROOT}` use.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
VAR = "${CLAUDE_PLUGIN_ROOT}"


def normalized(text):
    return re.sub(r"\s+", " ", text)


class TestPluginRootFallback(unittest.TestCase):
    def skills_using_var(self):
        found = []
        for skill in sorted(SKILLS.glob("*/SKILL.md")):
            text = skill.read_text()
            if VAR in text:
                found.append((skill, text))
        self.assertTrue(found, "no skill references the plugin-root variable")
        return found

    def test_every_var_user_states_the_base_directory_fallback(self):
        for skill, text in self.skills_using_var():
            with self.subTest(skill=skill.parent.name):
                flat = normalized(text)
                self.assertIn(
                    "Base directory for this skill:",
                    flat,
                    "fallback must name the harness's base-directory line",
                )
                self.assertRegex(
                    flat,
                    r"unset or empty",
                    "fallback must name the unset/empty variable case",
                )

    def test_fallback_is_the_first_plugin_root_mention(self):
        for skill, text in self.skills_using_var():
            with self.subTest(skill=skill.parent.name):
                paragraphs = re.split(r"\n\s*\n", text)
                first = next(p for p in paragraphs if VAR in p)
                self.assertIn(
                    "Base directory for this skill:",
                    normalized(first),
                    "the first plugin-root mention must be the fallback rule",
                )


if __name__ == "__main__":
    unittest.main()
