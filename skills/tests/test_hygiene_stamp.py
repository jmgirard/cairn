"""Lock: M93/D-052 — the `Last hygiene check` stamp is replaced, not appended.

The defect this guards against is an instruction gap, not a code bug. All
three write sites said only "update" the stamp, which reads as "add to", so
each pass prepended a parenthetical and demoted the last to `Prior:`/`Earlier:`
— reaching 3,152 chars on one line in an adopting repo (2026-07-19) while both
weight axes read green. cairn's own instance was pruned by hand once
(`dbf1068`) with no rule or guard behind it, which is exactly why it came back.

So the rule has to exist in the rulebook AND at every surface that writes the
stamp, and this file pins both. It also pins the stated<->enforced coupling for
`NON_ITEM_LINE_CAP`: the number lives in `cairn_scripts.py` and is restated in
the rulebook, and two encodings of one number drift (M87 F1/90).

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import sys
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent


def read(path):
    return path.read_text()


class TestHygieneStampRule(unittest.TestCase):
    def setUp(self):
        # Read per-test, never cached in setUpClass: the mutation harness runs
        # a guard as a single method and skips setUpClass, so a class-level
        # cache reads the unmutated file and reports false coverage (M61).
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")

    def test_rule_pairs_the_stamp_with_the_replace_operation(self):
        # Label and rule on ONE physical line. Pinning the label alone would
        # survive the rule being swapped out beneath it, and a wrapped
        # sentence is the usual way that anchor is lost (M74/M92).
        self.assertIn(
            "**The `Last hygiene check` stamp is replaced each pass, "
            "never appended to** — it records the CURRENT check only, "
            "and no `Prior:` or `Earlier:` chain accumulates behind it.",
            self.rules,
        )

    def test_rule_grounds_replacement_in_the_current_knowledge_split(self):
        # Without this, the rule reads as licence to rewrite history. The
        # stamp is replaceable BECAUSE it is current knowledge (D-045), and
        # git plus the archive hold what it replaces.
        self.assertIn("The stamp is current knowledge (D-045), not history", self.rules)

    def test_narrowing_is_stated_as_non_item_only(self):
        # D-052 narrows M84 rather than overturning it; the scope of the
        # narrowing is the whole content of the decision, so it is pinned
        # with its label on one line.
        self.assertIn(
            "**The per-line axis covers non-item lines only, and deliberately "
            "never item lines** (D-052, narrowing M84's blanket rejection).",
            self.rules,
        )

    def test_m84_original_rationale_survives_the_narrowing(self):
        # The reason item lines stay exempt is M84's, kept verbatim. If this
        # sentence is ever dropped, the narrowing reads as a reversal and the
        # next milestone re-litigates a decision that was never overturned.
        self.assertIn(
            "pressure on individual line length would reward splitting an item",
            self.rules,
        )


class TestStampWriteSites(unittest.TestCase):
    """Every surface that writes the stamp must say REPLACE.

    The rulebook stating it is not enough: these are the steps an agent
    actually follows at audit and post-merge hygiene, and "update" at any one
    of them regrows the chain. circumplex proved it — its `review M42: done`
    pass rewrote the stamp on 2026-07-19 and still left 2,568 chars, because
    the instruction it read said "update"."""

    def site(self, *parts):
        return read(SKILLS.joinpath(*parts))

    def test_milestone_audit_says_replace(self):
        text = self.site("milestone", "SKILL.md")
        self.assertIn(
            '**Replace** "Last hygiene check: YYYY-MM-DD" in ROADMAP.md — '
            "overwrite the previous text, never append to it and never demote "
            "it to a `Prior:` or `Earlier:` clause.",
            text,
        )

    def test_post_merge_hygiene_says_replace(self):
        text = self.site("milestone-review", "SKILL.md")
        self.assertIn(
            '**replace** "Last hygiene check" — overwrite the previous text, '
            "never append to it and never demote it to a `Prior:` clause "
            "(D-052)",
            text,
        )

    def test_shipped_skeleton_teaches_the_shape(self):
        # An adopting repo learns the format from the scaffold it is given,
        # so the skeleton carries the rule inline rather than relying on the
        # author having read the rulebook first.
        text = self.site("cairn-init", "SKILL.md")
        self.assertIn(
            "_Last hygiene check: YYYY-MM-DD (one short line, replaced each "
            "pass — never appended to; D-052)_",
            text,
        )

    def test_no_write_site_still_says_only_update(self):
        # The negative direction, paired with the three positive asserts
        # above so it is not vacuous (M54: blanking cannot restore an
        # absence, so a lone assertNotIn cannot be mutation-proven).
        for parts in (
            ("milestone", "SKILL.md"),
            ("milestone-review", "SKILL.md"),
        ):
            with self.subTest(site="/".join(parts)):
                self.assertNotIn('update "Last hygiene check', self.site(*parts))


class TestStatedCapMatchesEnforcedCap(unittest.TestCase):
    """Two encodings of one number, paired.

    `NON_ITEM_LINE_CAP` is enforced in `cairn_scripts.py` and restated in the
    rulebook so an author reads it without opening the source. M87 F1/90 is
    the precedent: a threshold lived in three places while the guard paired
    two, and a header went on teaching the retired number with validate
    green."""

    def test_rulebook_states_the_enforced_cap(self):
        rules = read(SKILLS / "shared" / "tracking-rules.md")
        stated = re.search(
            r"capped at `NON_ITEM_LINE_CAP` \(< ([\d,]+) characters\)", rules
        )
        self.assertIsNotNone(stated, "the rulebook states no non-item line cap")
        scripts_dir = ROOT / "scripts"
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        import cairn_scripts

        self.assertEqual(
            int(stated.group(1).replace(",", "")),
            cairn_scripts.NON_ITEM_LINE_CAP,
            "the rulebook and cairn_scripts disagree on NON_ITEM_LINE_CAP",
        )


if __name__ == "__main__":
    unittest.main()
