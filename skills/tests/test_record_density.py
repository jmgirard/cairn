"""Lock: M84 — the item caps gain a second, orthogonal axis.

The tracking-rules weight-caps text must state that `ROADMAP.md` and
`LESSONS.md` are measured on two axes over the same whole file — item count
(lines, because both files are parsed one item per line) and weight (character
mass, the `record density` advisory) — that the item axis is structurally blind
to prose growing inside a line, and that the two axes take OPPOSITE remedies:
graduate/prune for count, compress in place for weight. It must also record
why weight only WARNs, and why a per-line warn was rejected FOR ITEM LINES —
D-052 (M93) narrowed that rejection rather than overturning it, so non-item
lines now do carry a per-line cap and M84's reason still binds everywhere else.
The narrowing itself is guarded in `test_hygiene_stamp.py`.

Two stated<->enforced agreements ride along: the stated thresholds must equal
`CHAR_CAPS` in `cairn_scripts.py`, and the stated label must equal the one
`cairn_validate` emits for `check_record_density` (M59/M78 — prose naming a
finding uses the emitted label verbatim). The measurement itself is enforced
by the fixtures in `scripts/tests`; this guard locks the stated rules.

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent


def read(path):
    return path.read_text()


class TestRecordDensityRule(unittest.TestCase):
    def setUp(self):
        # Read per-test, never cached in setUpClass: the mutation harness runs
        # a guard as a single method, which skips setUpClass, so a class-level
        # cache would read the unmutated file and report false coverage on
        # itself (M61).
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")

    def test_rule_names_both_axes_with_their_opposite_remedies(self):
        # M74/M76: an axis->remedy mapping is pinned with BOTH pairs on one
        # physical line. Pinning the mechanism sentence alone ("the two axes
        # take opposite remedies") leaves the pairing swappable — compress a
        # bloated candidate list, graduate half a lesson — with every other
        # assert here still green, and the mutation harness cannot catch a
        # swap because blanking is not swapping.
        self.assertIn(
            "The two axes take opposite remedies: an over-count file graduates or prunes items, an over-weight file compresses them in place.",
            self.rules,
        )

    def test_rule_states_why_the_item_axis_cannot_see_weight(self):
        # The load-bearing justification: without it the second axis reads as
        # belt-and-braces on the first, and the next cap squeeze drops it.
        self.assertIn("structurally blind to prose accumulating", self.rules)

    def test_rule_requires_the_mean_to_be_measured_never_assumed(self):
        # D-049's application rule, and the one M84-D1 actually broke: a
        # threshold derived from an ASSUMED mean sits below what the line cap
        # permits and silently becomes the real cap, firing at ordinary
        # density. M95's inversion sweep found this operative clause unpinned
        # while every threshold around it was guarded.
        self.assertIn("Measure that mean, never assume one", self.rules)

    def test_rule_states_that_density_warns_rather_than_fails(self):
        # The severity IS the decision (M84 Scope, distinguishing D-018): an
        # item count is a structural fact, density is a judgment about prose.
        self.assertIn("Density warns because", self.rules)

    def test_rule_maps_each_axis_to_its_label_and_severity(self):
        # M84 review F4: "weight" names the section, the hard CHECK, AND the
        # new axis, so a reader hitting `FAIL weight caps` could read the
        # advisory's severity as covering it. Pinned label-WITH-severity for
        # BOTH axes on one physical line (M74/M76): pinning one pair alone
        # leaves the other swappable, which is the inversion that misleads.
        self.assertIn(
            "the item axis is the hard `weight caps` CHECK and still FAILs the gate, while the weight axis is the `record density` advisory and only ever WARNs",
            self.rules,
        )

    def test_rule_records_why_a_per_line_warn_was_rejected(self):
        # A rejected alternative recorded once, so it is not re-litigated: a
        # per-line warn would pay authors to split an item across lines, which
        # is the one thing that breaks both parsers.
        self.assertIn(
            "pressure on individual line length would reward splitting an item",
            self.rules,
        )

    def test_stated_thresholds_match_enforced_thresholds(self):
        # Two encodings of one set of numbers; drift is the defect. Membership
        # is checked too, not just the values — a third file added to
        # CHAR_CAPS without a rulebook line would otherwise pass silently.
        stated = re.search(
            r"per-file character thresholds — `(\w+\.md)` < ([\d,]+) · `(\w+\.md)` < ([\d,]+)",
            self.rules,
        )
        self.assertIsNotNone(stated, "the weight-caps text states no thresholds")
        rulebook = {
            f"cairn/{stated.group(1)}": int(stated.group(2).replace(",", "")),
            f"cairn/{stated.group(3)}": int(stated.group(4).replace(",", "")),
        }
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        body = re.search(r"CHAR_CAPS = \{(.*?)\}", scripts, re.S)
        self.assertIsNotNone(body, "CHAR_CAPS is not defined in cairn_scripts.py")
        enforced = {
            k: int(v) for k, v in re.findall(r'"([^"]+)": (\d+)', body.group(1))
        }
        self.assertEqual(rulebook, enforced)

    def test_lessons_header_states_its_own_enforced_threshold(self):
        # The THIRD encoding of the number (M87 review F1/90). LESSONS.md's own
        # header teaches its two caps, and it is what a maintainer reads at
        # post-merge hygiene while deciding whether to compress — so a stale
        # figure there sends them on the exact compression run the threshold
        # was raised to remove, with `cairn_validate` reporting OK throughout.
        # The coupling above pairs only the rulebook and CHAR_CAPS, which is
        # why this drifted through M87's own first pass.
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        body = re.search(r"CHAR_CAPS = \{(.*?)\}", scripts, re.S)
        enforced = {
            k: int(v) for k, v in re.findall(r'"([^"]+)": (\d+)', body.group(1))
        }["cairn/LESSONS.md"]
        header = read(ROOT / "cairn" / "LESSONS.md")[:1200]
        self.assertIn(f"{enforced:,} characters", header)

    def test_stated_advisory_label_matches_the_emitted_label(self):
        # M59/M78: prose naming a validate finding must use the label the
        # script actually emits, or run-and-read sends the reader hunting for
        # a string that never appears.
        validate = read(ROOT / "scripts" / "cairn_validate.py")
        emitted = re.search(
            r'\(\s*"([\w -]+)",\s*lambda root, rows: check_record_density', validate
        )
        self.assertIsNotNone(
            emitted, "check_record_density is not registered in ADVISORIES"
        )
        # Anchored on the phrase that INTRODUCES the label, not on the bare
        # backticked label: since the F4 severity sentence the label occurs
        # twice in the rulebook, and a block occurring more than once cannot
        # be mutation-registered (blanking one leaves the other, which is
        # false coverage — M60's "register a longer unique anchor").
        self.assertIn(f"`cairn_validate`'s `{emitted.group(1)}` advisory", self.rules)


if __name__ == "__main__":
    unittest.main()
