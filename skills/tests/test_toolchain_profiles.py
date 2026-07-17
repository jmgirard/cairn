"""Regression guards for the toolchain-profile mechanism (M45 spine, M46 rewire).

Locks: the seven slots present + non-empty in both shipped profiles; the r-package
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
    "changelog",
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

# Python-toolchain opinionation tokens the python profile must carry at
# R-parity (M48 AC2) — one blessed pick per category, verifiable by token.
PYTHON_TOOLCHAIN_TOKENS = (
    "pyproject.toml",
    "PEP 621",
    "pytest",
    "ruff",
    "mypy",
    "python -m build",
    "twine",
    "coverage.py",
)

# Python toolchain tokens that must NOT bleed into the generic profile (M48).
# Deliberately excludes "pytest", which generic names as a bare *example*
# verify command — the negative assertion keys on the python-specific picks.
PYTHON_TOKENS_ABSENT_FROM_GENERIC = ("ruff", "mypy", "twine", "pyproject")


class TestShippedProfiles(unittest.TestCase):
    def test_all_profiles_define_all_seven_slots(self):
        for name in ("r-package", "python", "generic"):
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


class TestPythonProfile(unittest.TestCase):
    """M48: the python profile ships at R-parity opinionation (AC1/AC2), the
    generic profile stays free of the python toolchain, and the release-walk
    hands off `twine upload` to the user and self-submits nothing."""

    def test_python_profile_defines_exactly_the_seven_slots(self):
        """AC1: same schema cairn_validate enforces on a repo PROFILE.md — the
        seven known slots and no unrecognized `## ` heading."""
        text = read("shared", "profiles", "python.md")
        headings = [ln[3:].strip().lower() for ln in text.splitlines()
                    if ln.startswith("## ")]
        self.assertEqual(sorted(headings), sorted(SLOTS),
                         f"python profile slots {headings} != the seven known slots")

    def test_python_profile_holds_its_toolchain_tokens(self):
        """AC2: one blessed pick per category, verifiable by token."""
        profile = read("shared", "profiles", "python.md")
        for tok in PYTHON_TOOLCHAIN_TOKENS:
            self.assertIn(tok, profile, f"python profile missing toolchain token {tok}")

    def test_python_release_walk_hands_off_and_self_submits_nothing(self):
        """AC2: the release-walk hands `twine upload` to the user and self-submits
        nothing (parallel to the CRAN handoff)."""
        body = section_body(read("shared", "profiles", "python.md"), "release-walk").lower()
        self.assertTrue(body, "could not locate the python release-walk slot")
        self.assertIn("twine upload", body, "release-walk should hand off twine upload")
        self.assertIn("self-submits nothing", body,
                      "release-walk should state cairn self-submits nothing")

    def test_generic_profile_has_no_python_toolchain(self):
        text = read("shared", "profiles", "generic.md").lower()
        for tok in PYTHON_TOKENS_ABSENT_FROM_GENERIC:
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


class TestUniversalChangeGovernance(unittest.TestCase):
    """M58 (RR01 rec 4): dependency-change gating and the deprecation-cycle
    policy are universal governance, stated once in the core rulebook's
    Universal tracking rules; the r-package/python profiles keep only the
    mechanical renderings (dependency surface, deprecation mechanism). Before
    M58 both rules sat near-verbatim in two `test-doctrine` slots and were
    absent from generic — a generic adopter had no stated dependency gate."""

    def test_core_states_the_dependency_gate(self):
        rules = read("shared", "tracking-rules.md")
        self.assertIn("Dependency changes are never unilateral", rules,
                      "core rulebook must state the universal dependency-change gate")

    def test_core_states_the_deprecation_cycle(self):
        rules = read("shared", "tracking-rules.md")
        self.assertIn("follow a deprecation cycle", rules,
                      "core rulebook must state the deprecation-cycle policy")
        self.assertIn("pre-1.0", rules,
                      "the deprecation-cycle policy must carry the pre-1.0 waiver")

    def test_profiles_do_not_restate_the_gate(self):
        # Negative regression guard (not mutation-registrable — M54 lesson);
        # its positive pair is the two core asserts above.
        for name in ("r-package.md", "python.md"):
            body = section_body(read("shared", "profiles", name), "test-doctrine")
            self.assertNotIn("never unilateral", body,
                             f"{name} test-doctrine restates the universal gate")

    def test_profiles_keep_the_mechanical_renderings(self):
        r = section_body(read("shared", "profiles", "r-package.md"), "test-doctrine")
        py = section_body(read("shared", "profiles", "python.md"), "test-doctrine")
        self.assertIn("Imports/Suggests", r,
                      "r-package rendering must name the dependency surface")
        self.assertIn("deprecation cycle", r,
                      "r-package rendering must name the deprecation mechanics")
        self.assertIn("dependencies/optional-dependencies", py,
                      "python rendering must name the dependency surface")
        self.assertIn("DeprecationWarning", py,
                      "python rendering must name the deprecation mechanism")


class TestRPackageFixtureProvenance(unittest.TestCase):
    """M49: the r-package test-doctrine mandates reproducible fixture provenance
    — source + committed generator + any seed per fixture — while leaving the
    *shape* (attr / embedded field / header) to the adopting repo. This is the
    R-mechanical concretization of the universal Reproducibility hard-stop; the
    content-not-shape choice and its two-exemplar rationale are recorded in
    DECISIONS.md (D-028)."""

    def test_test_doctrine_mandates_provenance_content(self):
        body = section_body(read("shared", "profiles", "r-package.md"), "test-doctrine")
        self.assertTrue(body, "could not locate the r-package test-doctrine slot")
        self.assertIn("reproducible provenance", body,
                      "test-doctrine should mandate reproducible fixture provenance")
        self.assertIn("committed generator", body,
                      "provenance mandate should require a committed generator")
        self.assertIn("seed", body, "provenance mandate should require any seed")

    def test_provenance_shape_is_left_to_the_repo(self):
        body = section_body(read("shared", "profiles", "r-package.md"), "test-doctrine")
        self.assertIn("the shape is the repo's choice", body,
                      "provenance mandate should leave the fixture shape to the repo")
        for shape in ("attribute", "embedded", "header"):
            self.assertIn(shape, body,
                          f"provenance mandate should name the {shape} shape option")


class TestRPackageCodecovCI(unittest.TestCase):
    """M52: the r-package test-doctrine documents the standard R GitHub Actions
    CI pair — `use_github_action("check-standard")` (R CMD check) and
    `use_github_action("test-coverage")` (covr → Codecov) — with coverage
    reporting framed diagnostic-only (never a merge gate), coherent with the
    retained "covr is a diagnostic, never a gate" line and tracking-rules' "no
    coverage-percentage target". `check-standard`, `test-coverage`, `codecov`,
    and "never gates the merge" are all absent from the pre-M52 profile, so each
    assertion doubles as the M39/M40 deletion sanity-check: removing the CI-pair
    block makes them fail (mentally deleting the feature ⇒ red)."""

    def _doctrine(self):
        body = section_body(read("shared", "profiles", "r-package.md"), "test-doctrine")
        self.assertTrue(body, "could not locate the r-package test-doctrine slot")
        return body

    def test_names_the_standard_ci_pair(self):
        body = self._doctrine().lower()
        self.assertIn("check-standard", body,
                      "test-doctrine should name the R CMD check GitHub Action")
        self.assertIn("test-coverage", body,
                      "test-doctrine should name the test-coverage GitHub Action")
        self.assertIn("codecov", body,
                      "test-doctrine should name Codecov as the coverage-report sink")

    def test_coverage_reporting_is_diagnostic_only(self):
        body = self._doctrine().lower()
        self.assertIn("never gates the merge", body,
                      "coverage reporting must be framed diagnostic-only (never a merge gate)")

    def test_retains_the_covr_is_a_diagnostic_line(self):
        # AC2: the pre-existing doctrine line stays — the CI addition must not
        # silently drop it (this token predates M52, so it is a *retention*
        # check, deliberately NOT the deletion anchor for the new guidance).
        body = self._doctrine()
        self.assertIn("`covr` is a diagnostic, never a gate", body,
                      "the existing 'covr is a diagnostic, never a gate' line must be retained")


class TestPythonCodecovCI(unittest.TestCase):
    """M61 (graduating the M52-banked candidate): the python test-doctrine
    mirrors the r-package CI pair — a pytest test workflow and a
    pytest-cov → Codecov coverage workflow — framed diagnostic-only (never a
    merge gate), coherent with the retained "coverage.py is a diagnostic,
    never a gate" line. `pytest --cov`, `codecov`, and "never gates the
    merge" are all absent from the pre-M61 python profile, so each assertion
    doubles as the M39/M40 deletion sanity-check."""

    def _doctrine(self):
        body = section_body(read("shared", "profiles", "python.md"), "test-doctrine")
        self.assertTrue(body, "could not locate the python test-doctrine slot")
        return body

    def test_names_the_python_ci_pair(self):
        body = self._doctrine().lower()
        self.assertIn("pytest --cov", body,
                      "test-doctrine should name the pytest-cov coverage run")
        self.assertIn("codecov", body,
                      "test-doctrine should name Codecov as the coverage-report sink")

    def test_coverage_reporting_is_diagnostic_only(self):
        body = self._doctrine().lower()
        self.assertIn("never gates the merge", body,
                      "coverage reporting must be framed diagnostic-only (never a merge gate)")

    def test_retains_the_coverage_py_diagnostic_line(self):
        # the pre-existing doctrine line stays — the CI addition must not
        # silently drop it (retention check, not the deletion anchor).
        body = self._doctrine()
        self.assertIn("`coverage.py` is a diagnostic, never a gate", body)


class TestInitSelection(unittest.TestCase):
    def test_init_selects_and_backfills_profile(self):
        text = read("cairn-init", "SKILL.md")
        # DESCRIPTION -> r-package else generic, and a repair-mode backfill.
        self.assertIn("DESCRIPTION", text)
        self.assertIn("r-package", text)
        self.assertIn("generic", text)
        self.assertIn("backfill", text.lower())
        self.assertIn("cairn/PROFILE.md", text)

    def test_init_selects_and_backfills_python(self):
        """AC3: cairn-init selects `python` on a pyproject.toml (or setup.py/
        setup.cfg) marker, DESCRIPTION retains precedence for a hybrid repo, and
        the repair-mode backfill inference names the python branch."""
        text = read("cairn-init", "SKILL.md")
        self.assertIn("python", text)
        self.assertIn("pyproject.toml", text)
        for legacy in ("setup.py", "setup.cfg"):
            self.assertIn(legacy, text, f"cairn-init should recognize {legacy}")
        # DESCRIPTION still wins a hybrid, stated on one source line.
        self.assertIn("outranks a `pyproject.toml`", text,
                      "cairn-init should give DESCRIPTION precedence over pyproject in a hybrid")


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


class TestRulebookNamesThreeProfiles(unittest.TestCase):
    """AC4: tracking-rules "Toolchain profiles" states three profiles ship and
    its absent-PROFILE inference names `pyproject.toml → python` in the stated
    order (DESCRIPTION → r-package, pyproject.toml → python, else generic)."""

    def test_rulebook_names_three_profiles_and_python_inference(self):
        body = section_body(read("shared", "tracking-rules.md"), "Toolchain profiles")
        self.assertTrue(body, "could not locate the 'Toolchain profiles' section")
        self.assertIn("Three profiles ship", body,
                      "rulebook should state three profiles ship")
        self.assertIn("pyproject.toml", body,
                      "rulebook inference should name pyproject.toml")
        self.assertIn("python", body)
        # Order: DESCRIPTION precedes pyproject precedes the generic fallback.
        desc_i = body.find("DESCRIPTION")
        pyproj_i = body.find("pyproject.toml")
        self.assertTrue(0 <= desc_i < pyproj_i,
                        "inference should list DESCRIPTION -> r-package before pyproject -> python")


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
        # Lock T1's enrichment into a followable walk, not just the AC2 surface:
        # the commit-to-default-branch step is unique to the multi-step walk (the
        # pre-M47 one-line summary had bump/consolidate/tag but no commit step).
        self.assertIn("commit", body, "generic release-walk should be a followable walk (commit step)")
        for tok in ("cran", "devtools"):
            self.assertNotIn(tok, body, f"generic release-walk should carry no {tok}")


class TestChangelogSlot(unittest.TestCase):
    """M68 (D-040): changelog is the required seventh slot — each shipped
    profile declares its file (or the generic declare-or-none instructions),
    the consistency-gate bullets read the declaration instead of restating a
    file name, the rulebook states the "none" semantics, and both consumers
    (/hotfix, /cairn-release) read the slot."""

    def test_each_profile_declares_its_changelog(self):
        r = section_body(read("shared", "profiles", "r-package.md"), "changelog")
        self.assertIn("NEWS.md", r, "r-package changelog slot should declare NEWS.md")
        py = section_body(read("shared", "profiles", "python.md"), "changelog")
        self.assertIn("CHANGELOG.md", py, "python changelog slot should declare CHANGELOG.md")
        g = section_body(read("shared", "profiles", "generic.md"), "changelog")
        self.assertIn("declare it here", g, "generic changelog slot should instruct declaration")
        self.assertIn('"none"', g, "generic changelog slot should permit a none declaration")

    def test_consistency_gates_read_the_declared_changelog(self):
        for name in ("r-package", "python"):
            body = section_body(read("shared", "profiles", f"{name}.md"), "consistency-gate")
            self.assertIn("The declared changelog (`## changelog` slot)", body,
                          f"{name} consistency-gate should read the declaration")

    def test_rulebook_states_the_none_semantics(self):
        rules = read("shared", "tracking-rules.md")
        self.assertIn("Seven slots:", rules)
        self.assertIn('"none" is legal — hotfix skips the changelog entry', rules)
        self.assertIn("derives the version bump from git history", rules)

    def test_hotfix_reads_the_changelog_slot(self):
        skill = read("hotfix", "SKILL.md")
        self.assertIn("the file the active profile's `changelog` slot", skill)
        self.assertIn('a slot value of "none" → skip the entry', skill)

    def test_release_reads_the_declared_changelog(self):
        skill = read("cairn-release", "SKILL.md")
        self.assertIn("the file the active profile's `changelog` slot names", skill)
        self.assertIn('a "none" declaration skips', skill)


# M50: the greenfield-openers slot is filled with concrete openers per profile.
# Each token below is introduced by M50's fill — deleting the opener content
# makes the assertion fail (M39/M40 false-coverage guard), and the shared
# placeholder marker "downstream candidate" must be gone from every slot.
GREENFIELD_OPENER_TOKENS = {
    "r-package": ("Compiled code", "Rcpp", "RcppArmadillo", "reversible default"),
    "python": ("Typing strictness", "mypy --strict", "src/", "flat", "reversible default"),
    "generic": ("no language-specific openers", "universal opener layer"),
}


class TestGreenfieldOpeners(unittest.TestCase):
    """M50: the greenfield-openers slot of every shipped profile is filled with
    concrete, askable language-specific openers (not the M45 placeholder). The
    universal openers (distribution ambition, oracle-on) live in cairn-init's
    layer, not the slots, so each slot names only its language-specific
    question(s) — or, for generic, states the universal layer is the whole
    flow."""

    def test_each_slot_names_its_openers_and_drops_the_placeholder(self):
        for name, tokens in GREENFIELD_OPENER_TOKENS.items():
            body = section_body(read("shared", "profiles", f"{name}.md"),
                                "greenfield-openers")
            self.assertTrue(body, f"could not locate {name} greenfield-openers slot")
            self.assertNotIn("downstream candidate", body,
                             f"{name} greenfield-openers still carries the placeholder")
            for tok in tokens:
                self.assertIn(tok, body,
                              f"{name} greenfield-openers missing opener token {tok}")

    def test_language_slots_defer_universal_openers_to_cairn_init(self):
        """The universal openers (distribution ambition, oracle-verification) are
        asked once by cairn-init's layer, not restated as a profile's own
        question — the language slots say so explicitly ("not repeated here")."""
        for name in ("r-package", "python"):
            body = section_body(read("shared", "profiles", f"{name}.md"),
                                "greenfield-openers").lower()
            self.assertIn("not repeated here", body,
                          f"{name} slot should defer the universal openers to cairn-init")


class TestGreenfieldInitFlow(unittest.TestCase):
    """M50: cairn-init runs a greenfield flow in a new/empty repo — a project-type
    chip picks the profile, a universal opener layer + the profile's slot openers
    are asked, answers land in durable homes, undecided takes a reversible default
    + a candidate row, and the flow stays tracking-only (no package skeleton),
    bounded distinct from /design-interview. Each phrase below is introduced by
    M50; anchored on a single source line (M23) and clear of bold-splits (M26)."""

    def setUp(self):
        self.text = read("cairn-init", "SKILL.md")

    def test_greenfield_trigger_and_project_type_chip(self):
        self.assertIn("greenfield", self.text.lower(),
                      "cairn-init should define a greenfield trigger")
        self.assertIn("project-type chip", self.text,
                      "greenfield detection should present a project-type chip")

    def test_universal_opener_layer(self):
        self.assertIn("universal", self.text.lower(),
                      "greenfield flow should ask a universal opener layer")
        self.assertIn("numeric-work-needs-oracle-verification", self.text,
                      "universal layer should ask the oracle-verification opener")

    def test_undecided_takes_reversible_default_and_banks_a_candidate_row(self):
        self.assertIn("reversible default", self.text,
                      "an undecided opener should take a reversible default")
        self.assertIn("candidate` row", self.text,
                      "an undecided opener should bank a candidate row (IP3 conservation)")

    def test_stays_tracking_only_and_bounded_from_design_interview(self):
        self.assertIn("tracking-only", self.text,
                      "greenfield flow should stay tracking-only")
        self.assertIn("package skeleton", self.text,
                      "the skeleton should be surfaced as the first milestone, not scaffolded")
        self.assertIn("toolchain-config only", self.text,
                      "openers should be bounded distinct from /design-interview principle work")


if __name__ == "__main__":
    unittest.main()
