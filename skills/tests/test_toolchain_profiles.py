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


def section_body(text, heading):
    """The body of a `## <heading>` section, up to the next `## ` heading."""
    lines = text.splitlines()
    out, capturing = [], False
    for line in lines:
        if line.startswith("## "):
            if capturing:
                break
            capturing = line[3:].strip().lower() == heading.lower()
            continue
        if capturing:
            out.append(line)
    return "\n".join(out)


# R-toolchain gate tokens that M46 relocated out of the universal rulebook
# sections into the r-package profile — they must not reappear in the
# universal "What gets a test" floor (AC3).
R_GATE_TOKENS = (
    "devtools",
    "roxygen",
    "NAMESPACE",
    "cli::cli_abort",
    "_pkgdown",
    ".Rbuildignore",
    "vdiffr",
    "covr",
)


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

    def test_r_package_profile_holds_relocated_commands(self):
        """AC6 text-equivalence, source-of-truth flipped by M46: the r-package
        profile is now the single home for the R command strings (relocated out
        of the operational skills and the rulebook), so the profile — not the
        skills — must reproduce each token."""
        profile = read("shared", "profiles", "r-package.md")
        for tok in R_COMMAND_TOKENS:
            self.assertIn(tok, profile, f"r-package profile missing relocated token {tok}")

    def test_generic_profile_has_no_r_toolchain(self):
        text = read("shared", "profiles", "generic.md").lower()
        for tok in ("devtools", "roxygen", "pkgdown", "cran"):
            self.assertNotIn(tok, text, f"generic profile should carry no {tok}")


class TestRulebookRelocation(unittest.TestCase):
    """AC3: the R-mechanical guardrails + the R half of "What gets a test" are
    relocated into the r-package profile; the universal rulebook keeps only the
    language-agnostic floor. The old "## R package guardrails" section is gone,
    and the R gate tokens do not appear in the universal test-rules section."""

    def test_r_package_guardrails_section_removed(self):
        rules = read("shared", "tracking-rules.md")
        self.assertNotIn("## R package guardrails", rules,
                         "R package guardrails section should be relocated to the r-package profile")

    def test_what_gets_a_test_has_no_r_gate_tokens(self):
        body = section_body(read("shared", "tracking-rules.md"), "What gets a test")
        self.assertTrue(body, "could not locate the 'What gets a test' section")
        for tok in R_GATE_TOKENS:
            self.assertNotIn(tok, body,
                             f"universal 'What gets a test' still carries R gate token {tok}")

    def test_r_gate_tokens_live_in_r_package_profile(self):
        profile = read("shared", "profiles", "r-package.md")
        for tok in R_GATE_TOKENS:
            self.assertIn(tok, profile,
                          f"r-package profile missing relocated gate token {tok}")


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
