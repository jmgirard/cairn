"""Regression guards for the M45 toolchain-profile spine.

Locks: the six slots present + non-empty in both shipped profiles (AC1); the
r-package profile reproducing the live R command strings, i.e. token-level
text-equivalence with the current skills (AC2); the generic profile carrying
no R toolchain tokens; cairn-init's profile selection + repair backfill (AC3);
and — the M45 boundary — the operational skills still hardcoding their commands
with no profile read yet (AC6). M46/M47 rewire the skills and will update the
AC6 guard.

Skill-prose guards read the file as one string, so asserted phrases live on a
single source line (M23) and steer clear of `**bold**` splits (M26).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


SLOTS = (
    "verify",
    "consistency-gate",
    "test-doctrine",
    "release-walk",
    "init-detection",
    "greenfield-openers",
)

# R command strings that appear in the live skills today; the r-package profile
# must reproduce each (AC2 text-equivalence). The test also asserts each is
# still present in the current skills, so token drift on either side trips it.
R_COMMAND_TOKENS = (
    "devtools::document()",
    "devtools::test()",
    "devtools::check()",
    "devtools::build_readme()",
    "pkgdown::check_pkgdown()",
    ".Rbuildignore",
    "_pkgdown.yml",
    "cli::cli_abort()",
    "submit_cran()",
    "NEWS.md",
)

OPERATIONAL_SKILLS = (
    ("milestone-implement", "SKILL.md"),
    ("milestone-review", "SKILL.md"),
    ("hotfix", "SKILL.md"),
    ("cairn-release", "SKILL.md"),
)


class TestShippedProfiles(unittest.TestCase):
    def test_both_profiles_define_all_six_slots(self):
        for name in ("r-package", "generic"):
            text = read("shared", "profiles", f"{name}.md").lower()
            for slot in SLOTS:
                self.assertIn(f"## {slot}", text, f"{name} missing slot {slot}")

    def test_r_package_reproduces_live_commands(self):
        profile = read("shared", "profiles", "r-package.md")
        live = "".join(
            read(a, b) for (a, b) in OPERATIONAL_SKILLS
        ) + read("shared", "tracking-rules.md")
        for tok in R_COMMAND_TOKENS:
            self.assertIn(tok, profile, f"r-package profile missing live token {tok}")
            self.assertIn(tok, live, f"{tok} not in current skills — token drift")

    def test_generic_profile_has_no_r_toolchain(self):
        text = read("shared", "profiles", "generic.md").lower()
        for tok in ("devtools", "roxygen", "pkgdown", "cran"):
            self.assertNotIn(tok, text, f"generic profile should carry no {tok}")


class TestInitSelection(unittest.TestCase):
    def test_init_selects_and_backfills_profile(self):
        text = read("cairn-init", "SKILL.md")
        # DESCRIPTION -> r-package else generic, and a repair-mode backfill.
        self.assertIn("DESCRIPTION", text)
        self.assertIn("r-package", text)
        self.assertIn("generic", text)
        self.assertIn("backfill", text.lower())
        self.assertIn("cairn/PROFILE.md", text)


class TestOperationalSkillsUnchanged(unittest.TestCase):
    """AC6: M45 ships the mechanism but does NOT rewire the operational skills —
    they still hardcode their commands and read no profile. M46/M47 flip this;
    this guard is expected to change then."""

    def test_operational_skills_still_hardcode_devtools(self):
        for a, b in OPERATIONAL_SKILLS:
            text = read(a, b)
            self.assertIn("devtools::", text, f"{a} lost its hardcoded devtools command")

    def test_operational_skills_do_not_yet_read_profile(self):
        for a, b in OPERATIONAL_SKILLS:
            text = read(a, b)
            self.assertNotIn("PROFILE.md", text, f"{a} reads the profile before M46/M47")


if __name__ == "__main__":
    unittest.main()
