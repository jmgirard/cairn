"""Regression guard: every `gh pr` and `gh issue` command in `/milestone`
names its repo (M234).

In a checkout with two remotes, a bare `gh pr` or `gh issue` command can
read the fork or ask which remote to use, so every such command in
`skills/milestone/SKILL.md` carries `--repo <base-repo>`. §2 states the rule
for §2 and §3, and §4 states it for §4.

The scan takes fenced blocks from the raw text, then collapses whitespace in
the rest and takes inline backtick spans, so a span that wraps across
source lines is still one span. A span counts as a command when it carries
an argument or flag after the subcommand. A bare name such as `gh pr diff`
in prose is a mention, not a command. The target is read per-test, never
cached on the class (M61).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent

FENCE = re.compile(r"^[ \t]*(`{3,})[^\n]*\n(.*?)^[ \t]*\1[ \t]*$", re.M | re.S)
INLINE = re.compile(r"`([^`]+)`")
COMMAND = re.compile(r"\bgh (pr|issue) \S+ \S")
REPO = "--repo <base-repo>"
RULE_2 = (
    "**The repo.** Every issue and pull-request command in this section and in "
    "§3 carries `--repo <base-repo>`, in both modes."
)


def milestone():
    return SKILLS.joinpath("milestone", "SKILL.md").read_text(encoding="utf-8")


def gh_commands(text):
    """Every `gh pr`/`gh issue` command span, fenced lines and inline spans,
    whitespace-collapsed."""
    spans = []
    for m in FENCE.finditer(text):
        spans += [" ".join(l.split()) for l in m.group(2).splitlines()]
    rest = " ".join(FENCE.sub(" ", text).split())
    spans += [" ".join(s.split()) for s in INLINE.findall(rest)]
    return [s for s in spans if COMMAND.search(s)]


def bare(text):
    return [s for s in gh_commands(text) if REPO not in s]


class TestMilestoneGhRepo(unittest.TestCase):
    def test_domain_not_empty(self):
        self.assertGreaterEqual(len(gh_commands(milestone())), 15)

    def test_every_command_names_repo(self):
        self.assertEqual(bare(milestone()), [])

    def test_section_two_states_rule(self):
        self.assertIn(RULE_2, " ".join(milestone().split()))

    def test_planted_bare_inline_span_fails(self):
        planted = milestone() + "\nread it with `gh pr\n  view <N> --json state`.\n"
        self.assertEqual(bare(planted), ["gh pr view <N> --json state"])

    def test_planted_bare_fenced_line_fails(self):
        planted = milestone() + "\n```bash\ngh issue view 7 --json state\n```\n"
        self.assertEqual(bare(planted), ["gh issue view 7 --json state"])

    def test_planted_bare_prefixed_span_fails(self):
        planted = milestone() + "\nrun `cd <p> && gh pr view <N> --json state`.\n"
        self.assertEqual(bare(planted), ["cd <p> && gh pr view <N> --json state"])

    def test_bare_name_mention_is_not_a_command(self):
        self.assertEqual(gh_commands("a `gh pr diff` that fails"), [])


if __name__ == "__main__":
    unittest.main()
