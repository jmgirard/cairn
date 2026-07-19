"""README currency guards (M90).

The README is the outward front door, and it went stale in a way no guard
caught: M70 shipped a fourth toolchain profile while ¶1 still advertised
three (that axis is now locked by the derived guard in
`test_positioning_guard.py`). These guards lock the three things M90 ADDED,
so a later edit cannot quietly drop them:

  1. the reference-pages section (the 1.1.0 headline had one parenthetical),
  2. the promise that cairn never proposes a release (D-050),
  3. the advisory hook nudges in the install section.

Registered in `test_mutation_harness.py`: blanking any protected block must
fail its guard. Every asserted phrase sits on a single physical line (M64)
and outside `**bold**` markers (M26) so `assertIn` can match.

Case discipline: this module matches against the RAW text, unlike
`test_collaboration_boundary.py`, whose helper lowercases. Anchors here are
therefore chosen to be case-stable — lowercase mid-sentence prose.
"""

import pathlib
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]


def readme():
    return (REPO / "README.md").read_text()


class TestReferencePagesSection(unittest.TestCase):
    def test_readme_has_the_sources_section(self):
        self.assertIn("## Keeping track of sources", readme())

    def test_readme_states_when_a_page_is_owed(self):
        # The trigger rule. Pinned WITH its condition on one line: pinning
        # "a page is owed" alone would survive swapping the condition for a
        # different one (M74 label->rule pairing).
        self.assertIn(
            "A page is owed when you start relying on the source.", readme()
        )

    def test_readme_states_pages_record_whether_they_were_rechecked(self):
        # The load-bearing field: an unverified extraction must not read as
        # a confirmed one.
        self.assertIn(
            "whether its extracted values have actually been re-read", readme()
        )

    def test_readme_distinguishes_source_facts_from_repo_notes(self):
        self.assertIn(
            "Facts about the source outlive notes about your repo.", readme()
        )

    def test_readme_states_staleness_warnings_are_not_failures(self):
        # Both halves on one line: that the check warns, AND that warning is
        # not failing. Pinning only the first would survive a rewrite that
        # promoted these to gate failures.
        self.assertIn("These are warnings, never gate failures:", readme())


class TestFileMapCurrency(unittest.TestCase):
    def test_readme_tree_lists_the_lessons_file(self):
        self.assertIn("LESSONS.md             # durable repo lessons", readme())

    def test_readme_boundary_rule_names_every_home(self):
        # M74: pin the LABEL with its MEMBERS on one physical line — pinning
        # "Lessons → LESSONS" alone would survive dropping any other member,
        # and pinning the sentence alone would survive swapping a home.
        self.assertIn(
            "**Architecture → DESIGN · Status → ROADMAP · Tasks → milestone "
            "files · Decisions → DECISIONS · Lessons → LESSONS · History → "
            "archive + git log.**",
            readme(),
        )


class TestReleaseRowIsProfileNeutral(unittest.TestCase):
    def test_release_row_is_not_cran_only(self):
        # Positive framing carries the mutation entry; the absence-assert
        # below cannot be mutation-proven (blanking cannot restore an
        # absence), so it rides along rather than standing alone.
        self.assertIn("follows your repo's profile", readme())
        self.assertNotIn("| Prepare a CRAN release |", readme())


class TestReleaseTimingPromise(unittest.TestCase):
    def test_readme_states_cairn_never_proposes_a_release(self):
        # D-050's user-facing half. The existing "auto-release" line covers
        # the release ACT; this covers whether one is ever SUGGESTED.
        self.assertIn(
            "Propose, plan, or nominate a release", readme()
        )

    def test_readme_names_release_timing_as_the_maintainers_call(self):
        self.assertIn("release timing is yours to declare", readme())


class TestAdvisoryNudges(unittest.TestCase):
    def test_readme_install_section_names_the_advisory_nudges(self):
        # The install section previously listed only blocking guards, so the
        # nudges an adopter actually sees fire were undocumented.
        self.assertIn("and the advisory nudges", readme())

    def test_readme_names_each_nudge_trigger(self):
        # Named, never counted. DESIGN.md already owns the nudge COUNT
        # ("The three nudges are advisory"); restating a number here would
        # make README a second encoding of it — the stale-number trap M90-D1
        # exists to avoid, and the M87 lesson that prose restating a number
        # IS an encoding. Review caught this shipping as a wrong count that a
        # mutation-registered guard would then have pinned in place.
        text = readme()
        self.assertIn("when an idea gets captured somewhere other than the", text)
        self.assertIn("something durable is headed for Claude's memory", text)
        self.assertIn("when a commit on your default branch reaches outside", text)

    def test_readme_says_nudges_never_block(self):
        self.assertIn("none of which block anything", readme())


if __name__ == "__main__":
    unittest.main()
