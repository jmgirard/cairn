"""Lock: M108/D-060 — the always-read governance frame.

Two surfaces carry the frame and this file pins both:

  1. The rulebook (`tracking-rules.md` "Always-read governance") states the
     frame — every always-read file names three governance elements (inflow
     test, outflow-or-read-bound, attention signal) — enumerates the
     always-read surfaces with those elements filled (the worked case), and
     bounds itself to completeness, never mass (D-057's closed size program).
  2. The `/milestone` §2 audit applies it as a judgment that reports a gap and
     never auto-fixes, never `FAIL`s.

M113/D-063 added the fifth row (the active milestone file) plus the two claims
that make it unlike the four above it, each pinned on its own.

Anchors are copied from the target files' actual bytes (M95/M100), each a
single physical line so a reflow cannot silently unpin it (M74/M92/M104). The
table rows bind each file NOUN to its elements, so swapping a file's
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

    def test_enumerates_the_always_read_files_with_their_elements(self):
        # AC2: each row binds a file to its three elements; a swapped
        # disposition reddens because the whole row is pinned (M103).
        for row in (
            "| `ROADMAP.md` | a milestone or candidate | terminal-row "
            "retention + candidate triage/graduation | 60-line item cap |",
            "| `LESSONS.md` | a durable \"how this repo behaves\" note | retire "
            "by enforcement / ownership / maturation (D-051, D-055) | 50-line "
            "item cap + `record density` |",
            "| `tracking-rules.md` | the placement steps under \"What gets a "
            "test\" (D-071) | editorial pass; growth governed at the door "
            "(D-057) | `/milestone` audit mass+growth line |",
            "| `DECISIONS.md` | a cross-cutting choice among alternatives | "
            "bounded heading read — history read less, never shrunk (D-054) | "
            "none needed once read-bounded |",
            # M113/D-063 — the fifth surface. Its read-bound cell names BOTH
            # halves of the split: the cap for what the cap governs, the
            # newest-content injection for what it exempts. Dropping either
            # half leaves the row saying something the hook does not do.
            "| the active `milestones/M<NN>-<slug>.md` | the milestone-file "
            "section ownership table | capped sections: the 150-line "
            "plan-owned cap; cap-exempt sections: newest-content injection — "
            "history read less, never shrunk (D-063); the file leaves the set "
            "at `done` | `weight caps` CHECK + `work-log format` + "
            "`decisions format`; none needed "
            "for the cap-exempt sections once read-bounded |",
            # M126 — the sixth surface. Its FIRST cell is the load-bearing
            # one: it names the `## Project tracking` section and not the
            # file, because all three of its dispositions are section-scoped
            # (D-018/D-009) and a file-named cell would overclaim every one
            # of them against a file cairn does not own.
            "| `CLAUDE.md`'s `## Project tracking` section | routing only — "
            "classify and invoke the skill, never conduct (D-009) | the "
            "weight-caps remedy: trim the section back to the template | "
            "30-line section cap, `cairn_validate`'s `weight caps` CHECK |",
        ):
            with self.subTest(row=row[:20]):
                self.assertIn(row, self.rules)

    def test_names_the_surface_that_leaves_the_always_read_set(self):
        # M113 AC5: the milestone file is the one surface with a lifecycle —
        # it stops being read at `done`. Pinned separately from the row
        # because the row states the mechanism and this states why it is
        # unlike the four above it.
        self.assertIn(
            "It is **the only always-read surface that leaves the set**: a "
            "milestone stops",
            self.rules,
        )

    def test_names_the_split_across_two_gp1_mechanisms(self):
        # M113 AC5: one file, two of GP1's three mechanisms — a cap for the
        # capped sections, reading less for the cap-exempt ones. This is what
        # keeps D-053's "fits none of the three" supersession trigger unmet.
        self.assertIn(
            "only one split across two of GP1's mechanisms within one file**",
            self.rules,
        )

    def test_names_the_section_scoped_surface(self):
        # M126 AC3, first half: the sixth surface's governed unit is a
        # SECTION. Pinned apart from the row because the row states the three
        # dispositions and this states why they stop at the section.
        self.assertIn(
            "cells describe cairn's `## Project tracking` section and never "
            "the whole file:",
            self.rules,
        )

    def test_names_the_ungoverned_remainder_of_the_file(self):
        # M126 AC3, second half — pinned separately because round 1 of the §8
        # certification found the first assert stops at its colon, leaving
        # this predicate negatable green: "governed by cairn too, and every
        # cell in that row reaches it" passed the whole suite. The D-018 cite
        # rides on the same physical line so the remainder claim cannot lose
        # its authority while the assert still matches.
        self.assertIn(
            "governed by nothing cairn owns (D-018), so no cell in that row "
            "reaches it.",
            self.rules,
        )

    def test_contrasts_the_milestone_file_whose_exempt_sections_stay_governed(
        self,
    ):
        # M126 AC3: the contrast that makes the section-scoping a real
        # difference rather than a restatement of D-063 — a milestone file's
        # cap-exempt sections are still governed, by a read-bound instead of
        # a cap, where `CLAUDE.md`'s remainder is governed by nothing. The
        # read-bound and the cap it stands against sit on one physical line,
        # so dropping either half reddens.
        self.assertIn(
            "The milestone file's cap-exempt sections stay governed by a "
            "read-bound rather than by a cap (D-063),",
            self.rules,
        )

    def test_claims_no_uniqueness_for_the_split_unit(self):
        # M126 AC3: the statement may not claim that differing always-read
        # and governed units are unique to either surface — the
        # false-uniqueness shape the plan's criteria audit caught in the
        # step-2 draft. The whole claim is one physical line, because §8
        # round 1 negated the predicate ("a shape only this sixth surface
        # carries") with a head-only anchor still matching.
        self.assertIn(
            "No uniqueness is claimed for either: an always-read unit and a "
            "governed unit that differ is a shape both surfaces carry.",
            self.rules,
        )

    def test_the_sixth_row_is_appended_below_the_fifth(self):
        # M126 AC2: the row is APPENDED, never inserted — an insert above the
        # fifth row falsifies the sentence beneath the table, which nothing
        # pinned until §8 round 1 probed it (inserting a row above the sixth
        # left all 827 tests green). Both halves live here: the ordering, and
        # the sentence whose truth the ordering preserves.
        fifth = "| the active `milestones/M<NN>-<slug>.md` |"
        sixth = "| `CLAUDE.md`'s `## Project tracking` section |"
        self.assertIn(
            "The fifth surface differs from the four above it in two ways "
            "worth naming.",
            self.rules,
        )
        # `.index` raises on an absent row, so a deleted row reddens here too.
        self.assertLess(self.rules.index(fifth), self.rules.index(sixth))


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
