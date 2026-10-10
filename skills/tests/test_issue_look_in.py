"""Regression guard: the M232 issue look-in in `/milestone` §4.

An issue argument runs §4 in place of the snapshot, audit, and route. Three
things have to survive:

  1. The report's two scales. A verdict is exactly one of `reply`, `hotfix`,
     or `milestone`, and the maintainer-input level is one of `none`,
     `confirm`, or `decide`. A lost value turns a fixed scale back into free
     text that the chip cannot carry.
  2. The reply hand-off. cairn drafts the reply and shows the
     `gh issue comment` command line for the user to run, pinned verbatim
     and once, with `--repo <base-repo>` so a guest-mode reply reaches the
     upstream repo.
  3. The section's remote reach. A `gh issue|pr|api` line in §4 is a read or
     the one hand-off line, never a second write. The check is the plan's
     own grep, run over §4 only, and it is shown to fail on a planted write.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23). The target is read per-test, never
cached on the class, because the mutation harness runs a single method and
skips `setUpClass` (M61).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

HANDOFF = "gh issue comment <N> --repo <base-repo> --body '<reply>'"
GH_LINE = re.compile(r"gh (issue|pr|api)")
READ = re.compile(r"gh (issue view|issue list|pr list|pr view) ")


def milestone():
    return SKILLS.joinpath("milestone", "SKILL.md").read_text()


def look_in(text):
    """§4 from its heading to EOF, or "" when the heading is gone."""
    start = text.find("## 4. Issue look-in")
    return "" if start < 0 else text[start:]


def gh_lines(section):
    return [line.strip() for line in section.splitlines() if GH_LINE.search(line)]


def stray_gh_lines(section):
    """The `gh` lines that are neither a read nor the one hand-off line."""
    return [l for l in gh_lines(section) if not READ.search(l) and l != HANDOFF]


class TestEntry(unittest.TestCase):
    def test_section_exists(self):
        self.assertNotEqual(look_in(milestone()), "")

    def test_argument_test_names_both_forms(self):
        t = milestone()
        self.assertIn("An argument that is an issue number", t)
        self.assertIn("runs §4 in place of §1–§3.", t)

    def test_frontmatter_names_the_trigger(self):
        t = milestone()
        self.assertIn('"look into issue N"', t)
        self.assertIn('argument-hint: "[issue number or URL]"', t)


class TestScales(unittest.TestCase):
    def test_three_verdicts(self):
        s = look_in(milestone())
        self.assertIn("Give exactly one verdict:", s)
        for verdict in ("`reply`:", "`hotfix`:", "`milestone`:"):
            self.assertIn("- " + verdict, s)

    def test_three_levels(self):
        s = look_in(milestone())
        self.assertIn("Give exactly one level on this scale:", s)
        for level in ("`none`:", "`confirm`:", "`decide`:"):
            self.assertIn("- " + level, s)

    def test_guest_mode_maintainer_is_upstream(self):
        self.assertIn(
            "In guest mode the maintainer is the upstream maintainers",
            look_in(milestone()),
        )


class TestHandOff(unittest.TestCase):
    def test_handoff_line_present_once(self):
        lines = [l.strip() for l in look_in(milestone()).splitlines()]
        self.assertEqual(lines.count(HANDOFF), 1)

    def test_handoff_is_shown_never_run(self):
        self.assertIn(
            "The section shows this command and never runs it",
            look_in(milestone()),
        )

    def test_reply_follows_guest_vocabulary_rule(self):
        self.assertIn("guest-mode rule of no cairn vocabulary", look_in(milestone()))


class TestRemoteReach(unittest.TestCase):
    def test_domain_is_non_empty(self):
        # Three reads plus the hand-off. An empty match would pass the stray
        # check below for the wrong reason.
        self.assertGreaterEqual(len(gh_lines(look_in(milestone()))), 4)

    def test_only_reads_and_the_handoff(self):
        self.assertEqual(stray_gh_lines(look_in(milestone())), [])

    def test_every_command_names_the_base_repo(self):
        for line in gh_lines(look_in(milestone())):
            self.assertIn("--repo <base-repo>", line)

    def test_planted_write_is_caught(self):
        # Discrimination: a write the section must not run turns the check red.
        planted = look_in(milestone()) + "\n`gh issue close <N> --repo <base-repo>`\n"
        self.assertEqual(
            stray_gh_lines(planted), ["`gh issue close <N> --repo <base-repo>`"]
        )

    def test_planted_second_handoff_is_caught(self):
        # A second comment command with another shape is a stray, not the
        # counted hand-off line.
        planted = look_in(milestone()) + "\ngh issue comment <N> --body '<x>'\n"
        self.assertEqual(stray_gh_lines(planted), ["gh issue comment <N> --body '<x>'"])


if __name__ == "__main__":
    unittest.main()
