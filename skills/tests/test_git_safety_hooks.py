"""Git-safety hook wording guards (M60).

Locks the rulebook lines that record the two hooks' mechanical backing
against reversion to the honor-system-only wording that predated them:
  1. "Never force-push" names force_push_guard as its enforcement
     (RR01 rec 8) — deleting the hook's mention silently demotes the rule
     back to honor-system prose.
  2. The approval-marker paragraph records the restore-on-failure half of
     the lifecycle (merge_guard_post, RR01 rec 13) — without it, the M33
     "rewrite the marker before each retry" manual step reads as current.

DESIGN.md's seven-hook list is guarded by test_positioning_guard (HOOKS).
Registered in `test_mutation_harness.py`; every asserted phrase is on a
single line (M23) and outside `**bold**` markers (M26).
"""

import pathlib
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
RULES = REPO / "skills" / "shared" / "tracking-rules.md"


class TestForcePushLine(unittest.TestCase):
    def test_never_force_push_names_its_mechanical_backing(self):
        text = RULES.read_text()
        self.assertIn("Never force-push", text)
        self.assertIn(
            "force_push_guard hook mechanically denies a force-push to the default branch",
            text,
        )

    def test_feature_branches_stay_unblocked(self):
        # the false-positive-free half of the deny: the rule must keep
        # saying what is NOT blocked, or the guard reads broader than it is
        self.assertIn("(feature branches are not blocked)", RULES.read_text())


class TestMarkerRestoreLifecycle(unittest.TestCase):
    def test_marker_paragraph_records_the_restore(self):
        text = RULES.read_text()
        self.assertIn("restored automatically (merge_guard_post)", text)

    def test_single_use_semantics_survive(self):
        # restore must not read as reusable approval: one approval survives
        # failed retries only, never a successful merge
        self.assertIn(
            "survives failed retries but never a successful merge",
            RULES.read_text(),
        )


if __name__ == "__main__":
    unittest.main()
