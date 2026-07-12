"""Regression guard: the M17 /milestone-review fan-out + confidence scorer.

The review gate's independent review is a two-lens fan-out (distinct evidence
bases) followed by a generate-then-verify confidence scorer. These are
skill-text mechanics — nothing at runtime enforces them — so this test locks
the load-bearing pieces against silent regression:
  * two reviewers with *distinct* evidence bases, tier-tagged (Opus diff-bug,
    Sonnet blame-history);
  * a Sonnet confidence scorer, independent of finding generation, with a
    numeric threshold;
  * sub-threshold findings excluded from the actioned list but *logged*, never
    silently dropped (IP2);
  * the false-positive taxonomy handed to the reviewers;
  * the model-strategy section describing the fan-out while keeping the blanket
    "Never Haiku" rule (D-016).

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text()


def review():
    return read("milestone-review", "SKILL.md")


def rules():
    return read("shared", "tracking-rules.md")


class TestReviewFanout(unittest.TestCase):
    def test_two_distinct_evidence_lenses(self):
        t = review()
        self.assertRegex(t, r"diff-bug reviewer \(Opus\)")
        self.assertRegex(t, r"blame-history reviewer \(Sonnet\)")

    def test_evidence_bases_are_distinct_by_design(self):
        # the whole point of the fan-out — a shared base finds things twice
        self.assertIn("distinct evidence base", review())

    def test_blame_lens_reads_history_not_just_diff(self):
        t = review()
        self.assertIn("git blame", t)
        self.assertIn("git log", t)

    def test_confidence_scorer_present_with_threshold(self):
        t = review()
        self.assertIn("scorer", t.lower())
        self.assertIn("confidence", t.lower())
        self.assertRegex(t, r"\b80\b")

    def test_scorer_is_independent_of_generation(self):
        # generate-then-verify: the scorer must not be the finding generator
        self.assertRegex(review(), r"did \*?not\*? generate")

    def test_subthreshold_findings_logged_not_dropped(self):
        t = review()
        self.assertRegex(t, r"below 80.*excluded")
        self.assertIn("logged", t)
        self.assertRegex(t, r"never\s+silently\s+dropped")

    def test_false_positive_taxonomy_handed_to_reviewers(self):
        t = review()
        self.assertIn("Not a finding", t)
        for token in ("pre-existing", "linter", "nitpick",
                      "unmodified line", "intentional change"):
            with self.subTest(token=token):
                self.assertIn(token, t)

    def test_model_strategy_describes_fanout_and_keeps_never_haiku(self):
        r = rules()
        self.assertIn("Never Haiku", r)
        self.assertIn("fan-out", r)
        self.assertRegex(r, r"scorer \(Sonnet\)")


if __name__ == "__main__":
    unittest.main()
