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
# idea_guard). Ship a new hook, extend this tuple: it is the only check that
# DESIGN's inventory keeps pace with hooks/ (M48).
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


class TestTemplateBoundaryRule(unittest.TestCase):
    def test_template_names_the_lessons_home(self):
        self.assertIn("Lessons → LESSONS", read(TEMPLATE))


if __name__ == "__main__":
    unittest.main()
