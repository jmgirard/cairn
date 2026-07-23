"""Lock: M108/D-060 — the always-read governance frame.

Two surfaces carry the frame and this file pins both:

  1. The rulebook (`tracking-rules.md` "Always-read governance") states the
     frame — every always-read file names three governance elements (inflow
     test, outflow-or-read-bound, attention signal) — enumerates the four
     accumulating files with those elements filled (the worked case), and
     bounds itself to completeness, never mass (D-057's closed size program).
  2. The `/milestone` §2 audit applies it as a judgment that reports a gap and
     never auto-fixes, never `FAIL`s.

Anchors are copied from the target files' actual bytes (M95/M100), each a
single physical line so a reflow cannot silently unpin it (M74/M92/M104). The
four-file table rows bind each file NOUN to its elements, so swapping a file's
disposition reddens (M103).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(path):
    # Per-test read, never cached in setUpClass: the mutation harness runs a
    # guard as a single method and skips setUpClass, so a class-level cache
    # reads the unmutated file and reports false coverage (M61).
    return path.read_text()


class TestAlwaysReadFrameRulebook(unittest.TestCase):
    def setUp(self):
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")

    def test_names_inflow_test_element(self):
        self.assertIn(
            "- **Inflow test** — what content belongs in the file.",
            self.rules,
        )

    def test_names_outflow_or_read_bound_element(self):
        self.assertIn(
            "- **Outflow or read-bound** — how content leaves, or, where it "
            "may not leave,",
            self.rules,
        )

    def test_names_attention_signal_element(self):
        self.assertIn(
            "- **Attention signal** — what reports growth so a human notices.",
            self.rules,
        )

    def test_frame_is_completeness_only(self):
        # AC4: the frame reports element-presence, never mass — the boundary
        # that keeps it clear of D-057's closed stock-side size program.
        self.assertIn(
            "never measures or gates a file's mass (size governance is closed "
            "— D-057).",
            self.rules,
        )

    def test_enumerates_the_four_files_with_their_elements(self):
        # AC2: each row binds a file to its three elements; a swapped
        # disposition reddens because the whole row is pinned (M103).
        for row in (
            "| `ROADMAP.md` | a milestone or candidate | terminal-row "
            "retention + candidate triage/graduation | 60-line item cap |",
            "| `LESSONS.md` | a durable \"how this repo behaves\" note | retire "
            "by enforcement / ownership / maturation (D-051, D-055) | 50-line "
            "item cap + `record density` |",
            "| `tracking-rules.md` | the three-step placement test (D-056) | "
            "editorial pass; growth governed at the door (D-057) | `/milestone` "
            "audit mass+growth line |",
            "| `DECISIONS.md` | a cross-cutting choice among alternatives | "
            "bounded heading read — history read less, never shrunk (D-054) | "
            "none needed once read-bounded |",
        ):
            with self.subTest(row=row[:20]):
                self.assertIn(row, self.rules)


class TestAlwaysReadFrameAudit(unittest.TestCase):
    def setUp(self):
        self.audit = read(SKILLS / "milestone" / "SKILL.md")

    def test_audit_applies_the_frame(self):
        self.assertIn(
            "- **Always-read governance (frame completeness):** apply the "
            "rulebook's",
            self.audit,
        )

    def test_audit_reports_never_fixes(self):
        # AC3: the frame is a judgment surfaced for the user, in the form of
        # the staleness advisories — a gap is reported, never a gate FAIL.
        self.assertIn(
            "a judgment for the user — never auto-fixed, never a `FAIL`, the "
            "form of the",
            self.audit,
        )


if __name__ == "__main__":
    unittest.main()
