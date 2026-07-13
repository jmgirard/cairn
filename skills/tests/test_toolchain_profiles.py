"""Regression guards for the toolchain-profile mechanism (M45 spine, M46 rewire).

Locks: the six slots present + non-empty in both shipped profiles; the r-package
profile as the single source of truth for the relocated R command strings
(M46 flipped this from the skills); the generic profile carrying no R toolchain
tokens; cairn-init's profile selection + repair backfill; the M46 rewire — the
operational skills (implement/hotfix/review) read the active profile's slot and
no longer hardcode `devtools::`, the review consistency gate splits into
universal + profile halves, the R guardrails are relocated out of the rulebook
into the r-package profile, and the milestone template is de-R'd; plus the M47
rewire — cairn-release now reads the active profile's release-walk slot and no
longer hardcodes the CRAN/devtools walk.

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

    def test_relocated_guardrail_specifics_survive(self):
        """AC6: the guardrail *specifics* moved out of the rulebook must still be
        reproduced by the r-package profile, so no R adopter regresses."""
        profile = read("shared", "profiles", "r-package.md")
        for phrase in ("data-raw", "deprecation", "Imports/Suggests", "assertthat", "edition 3"):
            self.assertIn(phrase, profile,
                          f"r-package profile dropped relocated guardrail '{phrase}'")


class TestInitSelection(unittest.TestCase):
    def test_init_selects_and_backfills_profile(self):
        text = read("cairn-init", "SKILL.md")
        # DESCRIPTION -> r-package else generic, and a repair-mode backfill.
        self.assertIn("DESCRIPTION", text)
        self.assertIn("r-package", text)
        self.assertIn("generic", text)
        self.assertIn("backfill", text.lower())
        self.assertIn("cairn/PROFILE.md", text)


# Skills rewired to read the profile instead of hardcoding R commands: the
# operational trio at M46, and cairn-release at M47 (its release-walk slot).
REWIRED_SKILLS = (
    ("milestone-implement", "SKILL.md"),
    ("hotfix", "SKILL.md"),
    ("milestone-review", "SKILL.md"),
    ("cairn-release", "SKILL.md"),
)


class TestOperationalSkillsReadProfile(unittest.TestCase):
    """AC1/AC2: M45 shipped the mechanism but left the operational skills
    hardcoding their R commands; M46 flipped the operational trio and M47
    cairn-release — the rewired skills name the active profile's slot and no
    longer hardcode a `devtools::` command."""

    def test_rewired_skills_read_a_profile_slot(self):
        for a, b in REWIRED_SKILLS:
            text = read(a, b)
            self.assertIn("PROFILE.md", text, f"{a} should read the profile")
            self.assertNotIn("devtools::", text,
                             f"{a} still hardcodes a devtools command")


class TestReviewGateSplit(unittest.TestCase):
    """AC2: milestone-review's consistency gate splits into the universal
    cairn-file checks (unconditional, every profile) and the profile
    `consistency-gate` slot (toolchain checks). Both halves must be present, and
    the universal checks must not have been gated behind the profile."""

    def test_universal_checks_stay_unconditional(self):
        text = read("milestone-review", "SKILL.md")
        for tok in ("cairn_validate", "Coverage completeness", "cairn_impact"):
            self.assertIn(tok, text, f"review lost the universal cairn-file check {tok}")
        self.assertIn("Universal cairn-file checks", text,
                      "review no longer labels the always-run universal checks")

    def test_review_reads_the_profile_consistency_gate_slot(self):
        text = read("milestone-review", "SKILL.md")
        self.assertIn("consistency-gate", text,
                      "review no longer reads the profile consistency-gate slot")
        self.assertIn("PROFILE.md", text)


class TestTemplateProfileAware(unittest.TestCase):
    """AC4: the milestone template no longer hardcodes `devtools::check()` in
    its acceptance guidance; it references the active profile's verify/check."""

    def test_template_drops_hardcoded_devtools(self):
        text = read("shared", "templates", "milestone.md")
        self.assertNotIn("devtools", text, "template still hardcodes a devtools command")

    def test_template_references_the_profile(self):
        text = read("shared", "templates", "milestone.md")
        self.assertIn("PROFILE.md", text)
        self.assertIn("verify", text)


class TestReleaseSkillReadsProfile(unittest.TestCase):
    """M47: cairn-release reads the active profile's release-walk slot instead
    of hardcoding the CRAN walk (AC1), and gates its toolchain preconditions on
    the profile (AC3); the generic profile's release-walk defines a tag-based
    path with no CRAN (AC2). The "no longer hardcodes devtools::" half of AC1
    and the r-package text-equivalence of AC4 are covered by
    TestOperationalSkillsReadProfile (now includes cairn-release) and
    test_r_package_profile_holds_relocated_commands respectively."""

    def test_skill_reads_the_release_walk_slot(self):
        text = read("cairn-release", "SKILL.md")
        self.assertIn("release-walk", text,
                      "cairn-release should read the profile release-walk slot")
        self.assertIn("PROFILE.md", text)

    def test_skill_gates_preconditions_on_the_profile(self):
        text = read("cairn-release", "SKILL.md")
        # Anchor on the rewire's own single-line, non-bold-split phrasing (M23/M26/M39):
        # this phrase exists only because preconditions now gate on the profile.
        self.assertIn("Toolchain preconditions gate on the profile", text,
                      "cairn-release should gate DESCRIPTION/devtools preconditions on the profile")

    def test_generic_release_walk_defines_a_tag_path(self):
        # Isolate the release-walk slot so an absent tag path fails (M40), rather
        # than matching 'tag'/'version' elsewhere in the profile.
        body = section_body(read("shared", "profiles", "generic.md"), "release-walk").lower()
        self.assertTrue(body, "could not locate the generic release-walk slot")
        self.assertIn("tag", body, "generic release-walk should define a tag-based release")
        self.assertIn("version", body, "generic release-walk should bump the version")
        for tok in ("cran", "devtools"):
            self.assertNotIn(tok, body, f"generic release-walk should carry no {tok}")


if __name__ == "__main__":
    unittest.main()
