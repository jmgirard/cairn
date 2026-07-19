"""Positioning + DESIGN-honesty guards (M54).

Locks two things M54 fixed against reversion to the state that produced it:
  1. Outward positioning (RR01 rec 1) — the surfaces an external adopter reads
     first (`plugin.json`, `marketplace.json`, README ¶1) frame cairn by
     toolchain profile, not as an R-package-only tool.
  2. DESIGN.md architecture honesty (RR01 rec 5) — all five hooks listed, IP1
     names "the default branch", Known-issues is the current honest list.
Plus the same-family template drift (Lessons → LESSONS in the boundary rule).

Registered in `test_mutation_harness.py`: blanking any protected block must
fail its guard. Every asserted phrase is on a single line (M23) and outside
`**bold**` markers (M26) so `assertIn` can match.
"""

import pathlib
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]

PLUGIN = ".claude-plugin/plugin.json"
MARKETPLACE = ".claude-plugin/marketplace.json"
README = "README.md"
DESIGN = "cairn/DESIGN.md"
TEMPLATE = "skills/shared/templates/claude-md-section.md"

# The eight shipped hooks (DESIGN Architecture must name each — the M54 fix
# added commit_guard + memory_guard, which the stale three-hook bullet
# omitted; M60 added force_push_guard + merge_guard_post; M71 added
# idea_guard). Ship a new hook, extend this tuple by hand — it is checked
# against DESIGN's prose only, NOT derived from hooks/, so a new hook missing
# from here leaves DESIGN's inventory silently stale (M48 registered-kind
# trap; deriving it from the directory is a live candidate).
HOOKS = (
    "session_context",
    "stop_guard",
    "merge_guard",
    "commit_guard",
    "memory_guard",
    "force_push_guard",
    "merge_guard_post",
    "idea_guard",
)


def read(rel):
    return (REPO / rel).read_text()


class TestOutwardPositioning(unittest.TestCase):
    def test_plugin_json_uses_profile_framing(self):
        text = read(PLUGIN)
        self.assertIn("language-agnostic core with per-repo toolchain profiles", text)
        self.assertNotIn("for R packages", text)

    def test_marketplace_uses_profile_framing(self):
        text = read(MARKETPLACE)
        self.assertIn("language-agnostic core with per-repo toolchain profiles", text)
        self.assertIn("language-agnostic core, per-repo toolchain profiles", text)
        self.assertNotIn("for R packages", text)

    def test_readme_para1_uses_profile_framing(self):
        text = read(README)
        self.assertIn("language-agnostic", text)
        self.assertIn("toolchain profile", text)
        self.assertNotIn("milestone-driven R package development", text)

    def test_readme_carries_the_llm_wiki_framing(self):
        # M62: the governed-LLM-Wiki positioning (M56 verdict,
        # cairn/references/llm-wiki.md) — each phrase on one line (M23).
        text = read(README)
        self.assertIn("governed LLM Wiki for project state", text)
        self.assertIn("the agent maintains it, you gate it", text)


class TestDesignArchitectureHonesty(unittest.TestCase):
    def test_design_lists_all_seven_hooks(self):
        # Word-bounded: `merge_guard` inside `merge_guard_post` must NOT
        # satisfy the standalone merge_guard check (M60 review F1 — the
        # M39/M40 substring-shadowing false-coverage trap).
        text = read(DESIGN)
        for hook in HOOKS:
            self.assertRegex(
                text, rf"\b{hook}\b", f"DESIGN.md hooks list missing {hook}"
            )

    def test_ip1_names_the_default_branch(self):
        text = read(DESIGN)
        self.assertIn("Nothing reaches the default branch", text)

    def test_known_issues_are_current(self):
        text = read(DESIGN)
        self.assertNotIn("Unpiloted", text)          # the stale placeholder is gone
        self.assertIn("Single-author", text)          # the honest env limitation
        self.assertIn("enforced as prose", text)      # the honor-system bet, noted plainly


class TestShippedProfilesAreAdvertised(unittest.TestCase):
    """M90: the profile ENUMERATION is derived, not hand-listed.

    M54 pinned ¶1's framing (`language-agnostic`, `toolchain profile`) but
    never the list, so when M70 shipped `docker-image` all three positioning
    surfaces stayed green while still saying "R, Python, or generic". The
    trigger here is the shipped-profiles directory itself: add a profile and
    this guard fails until every surface names it.

    LABELS maps a profile filename to the human label the prose uses. It is
    hand-maintained BY DESIGN and fail-closed — an unmapped profile file is a
    hard failure telling you to add its label, never a silent skip. That is
    the difference from the HOOKS tuple above, which goes stale silently.
    """

    def shipped(self):
        d = REPO / "skills/shared/profiles"
        return sorted(p.stem for p in d.glob("*.md"))

    # profile filename -> the label an adopter reads in prose
    LABELS = {
        "r-package": "R",
        "python": "Python",
        "docker-image": "Docker image",
        "generic": "generic",
    }

    def test_every_shipped_profile_has_a_label(self):
        unmapped = [p for p in self.shipped() if p not in self.LABELS]
        self.assertEqual(
            unmapped, [], f"shipped profile(s) with no prose label: {unmapped}"
        )

    def test_readme_para1_names_every_shipped_profile(self):
        # Whitespace is normalized before matching: a two-word label like
        # "Docker image" straddles a line break whenever anyone reflows the
        # paragraph, and reddening on a cosmetic re-wrap would train the next
        # author to loosen the assert. The LABEL is still matched exactly —
        # this is not the M64 one-physical-line rule (that binds
        # mutation-registered blocks) nor the M74 label->rule pairing rule
        # (where collapsing lines could pair a label with a distant rule).
        para1 = " ".join(read(README).split("\n\n")[2].split())
        # Unmapped profiles are the dedicated label test's business; skipping
        # them here keeps that one failure clean instead of adding KeyErrors.
        for profile in (p for p in self.shipped() if p in self.LABELS):
            self.assertIn(
                self.LABELS[profile],
                para1,
                f"README ¶1 does not name the {profile} profile",
            )

    def test_manifests_name_every_shipped_profile(self):
        for rel in (PLUGIN, MARKETPLACE):
            text = " ".join(read(rel).split())
            # Unmapped profiles are the dedicated label test's business; skipping
        # them here keeps that one failure clean instead of adding KeyErrors.
        for profile in (p for p in self.shipped() if p in self.LABELS):
                self.assertIn(
                    self.LABELS[profile],
                    text,
                    f"{rel} does not name the {profile} profile",
                )


class TestTemplateBoundaryRule(unittest.TestCase):
    def test_template_names_the_lessons_home(self):
        self.assertIn("Lessons → LESSONS", read(TEMPLATE))


if __name__ == "__main__":
    unittest.main()
