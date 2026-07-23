"""Regression guard: the M111 GitHub-release handoff.

`/cairn-release`'s step 4 provides a conditional `gh release create` command —
provided, never run — so cutting the GitHub release is one copy-run step. Locks
the load-bearing prose on two surfaces:

  * `skills/cairn-release/SKILL.md` step 4 — the condition (GitHub `origin` +
    `gh`), the clean skip, provided-not-run, and the changelog-section body.
  * `skills/shared/profiles/generic.md` release-walk — the one-line mention.

Skill-prose guards read the file as one string, so every asserted phrase lives
on a single source line (M23/M105) and steers clear of `**bold**` splits (M26);
phrases are matched case-insensitively. Each anchor is mutation-registered
(test_mutation_harness).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def release():
    return SKILLS.joinpath("cairn-release", "SKILL.md").read_text().lower()


def generic_profile():
    return SKILLS.joinpath("shared", "profiles", "generic.md").read_text().lower()


class TestGithubReleaseHandoff(unittest.TestCase):
    """The provided-command handoff in /cairn-release step 4 (M111)."""

    def test_command_is_gated_on_github_origin_and_gh(self):
        # Condition pins BOTH the GitHub-remote probe and gh: dropping either
        # would let the command fire on a GitLab / no-gh repo.
        self.assertIn(
            "remote (`git remote get-url origin` names `github.com`) and `gh` is",
            release(),
        )

    def test_command_is_skipped_cleanly_off_github(self):
        self.assertIn(
            "absent, omit this command with no failure — the tag alone is the release.",
            release(),
        )

    def test_cairn_provides_but_never_runs_the_command(self):
        self.assertIn("provides this command; it never runs it", release())

    def test_release_body_is_the_consolidated_changelog_section(self):
        self.assertIn("whose body is the changelog section you just", release())

    def test_notes_are_passed_by_notes_file_matching_the_changelog(self):
        self.assertIn(
            "`--notes-file`, so the published release reads identically to the",
            release(),
        )

    def test_generic_profile_slot_names_the_handoff(self):
        self.assertIn(
            "provides a `gh release create` command whose body is the new changelog",
            generic_profile(),
        )


if __name__ == "__main__":
    unittest.main()
