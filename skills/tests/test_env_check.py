"""Prose-guards for the /cairn-init environment check (M61, RR01 §10.2).

The env check is §0's first bullet: probe git/python3/gh/remote before
anything else and name a degradation path per gap. Locks: the step exists
in §0 (ahead of the fresh-scaffold section), only git is fatal, and each
of the three non-fatal gaps names its degradation path. Each asserted
phrase sits on one physical SKILL line (M23) and is mutation-registered
(M53) in test_mutation_harness.py.

Run: python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILL = pathlib.Path(__file__).resolve().parents[1] / "cairn-init" / "SKILL.md"


class TestEnvCheck(unittest.TestCase):
    # read per-test (never cached at class level): the mutation harness
    # re-runs single methods against a patched read_text, and a setUpClass
    # cache would feed them the unmutated text (M61)
    @property
    def text(self):
        return SKILL.read_text()

    def test_env_check_opens_section_0(self):
        self.assertIn("**Environment check (RR01 §10.2).**", self.text)
        # it must precede situation-detection's other bullets and §1
        self.assertLess(
            self.text.index("**Environment check"),
            self.text.index("**Default branch.**"),
        )
        self.assertLess(
            self.text.index("**Environment check"),
            self.text.index("## 1. Fresh scaffold"),
        )

    def test_only_git_is_fatal(self):
        self.assertIn("only a missing `git` is fatal", self.text)
        self.assertIn("cairn is git-based; there is nothing to adopt", self.text)

    def test_python3_gap_names_hooks_fallback_and_scripts(self):
        self.assertIn("the registered hooks fall back to the `py` launcher", self.text)
        self.assertIn("unverified on Windows", self.text)

    def test_gh_gap_names_the_honor_system_degradation(self):
        self.assertIn("the approval model becomes honor-system", self.text)

    def test_no_remote_names_local_only_mode(self):
        self.assertIn("local-only mode", self.text)
