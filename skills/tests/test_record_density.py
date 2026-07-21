"""Lock: M84/M93/M101 — the tracking-file caps and their per-line density axis.

The tracking-rules weight-caps text must state that `ROADMAP.md` and
`LESSONS.md` are measured on two axes — item count (lines, because both files
are parsed one item per line; the hard CHECK) and a per-line cap on non-item
lines (the `record density` advisory) — that the item axis is structurally
blind to prose growing inside a line, that the two axes take OPPOSITE
remedies (graduate/prune items vs. replace an over-cap non-item line), and
why the advisory only WARNs. It must also record why a per-line warn was
rejected FOR ITEM LINES — D-052 (M93) narrowed that rejection rather than
overturning it, and M84's reason still binds item lines. The narrowing
itself is guarded in `test_hygiene_stamp.py`.

M101 (D-058) removed the whole-file character axis on measured grounds, so
the text must state NO per-file character threshold — the negative is paired
with positive framing asserts on the surviving axes (guard-doctrine §3).

Two stated<->enforced agreements ride along: the stated per-line cap must
equal `NON_ITEM_LINE_CAP` in `cairn_scripts.py` and the files the rulebook
names must equal `DENSITY_FILES`; and the stated label must equal the one
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
        # take opposite remedies") leaves the pairing swappable — prune a
        # bloated stamp, rewrite a candidate row — with every other assert
        # here still green, and the mutation harness cannot catch a swap
        # because blanking is not swapping.
        self.assertIn(
            "The two axes take opposite remedies: an over-count file graduates or prunes items, an over-cap non-item line is replaced by a shorter rewrite, never appended to.",
            self.rules,
        )

    def test_rule_states_why_the_item_axis_cannot_see_weight(self):
        # The load-bearing justification: without it the second axis reads as
        # belt-and-braces on the first, and the next cap squeeze drops it.
        self.assertIn("structurally blind to prose accumulating", self.rules)

    def test_rule_states_that_density_warns_rather_than_fails(self):
        # The severity IS the decision (M84 Scope, distinguishing D-018): an
        # item count is a structural fact, density is a judgment about prose.
        self.assertIn("Density warns because", self.rules)

    def test_rule_maps_each_axis_to_its_label_and_severity(self):
        # M84 review F4: "weight" names the section AND the hard CHECK, so a
        # reader hitting `FAIL weight caps` could read the advisory's severity
        # as covering it. Pinned label-WITH-severity for BOTH axes on one
        # physical line (M74/M76): pinning one pair alone leaves the other
        # swappable, which is the inversion that misleads.
        self.assertIn(
            "the item axis is the hard `weight caps` CHECK and still FAILs the gate, while the per-line axis is the `record density` advisory and only ever WARNs",
            self.rules,
        )

    def test_rule_records_why_a_per_line_warn_was_rejected(self):
        # A rejected alternative recorded once, so it is not re-litigated: a
        # per-line warn would pay authors to split an item across lines, which
        # is the one thing that breaks both parsers. D-052 narrowed this to
        # item lines; the reason must survive the M101 removal of the
        # whole-file axis untouched.
        self.assertIn(
            "pressure on individual line length would reward splitting an item",
            self.rules,
        )

    def test_rule_states_no_whole_file_threshold(self):
        # M101/D-058: the whole-file character axis is decommissioned, so the
        # rulebook must state no per-file character threshold. Negative
        # asserts are paired with a positive framing assert (guard-doctrine
        # §3) — the retirement sentence itself — so a crash or an empty read
        # cannot satisfy this test.
        self.assertIn("whole-file mass axis ran", self.rules)
        self.assertIn("D-058 retired it", self.rules)
        self.assertNotIn("per-file character thresholds", self.rules)
        self.assertNotIn("21,000", self.rules)
        self.assertNotIn("20,500", self.rules)

    def test_stated_per_line_cap_matches_enforced_cap(self):
        # Two encodings of one number; drift is the defect (M59/M78). The
        # rulebook states the cap beside the constant's own name, so parse it
        # from that pairing and compare against cairn_scripts.
        stated = re.search(
            r"`NON_ITEM_LINE_CAP` \(< (\d+) characters\)", self.rules
        )
        self.assertIsNotNone(stated, "the weight-caps text states no per-line cap")
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        enforced = re.search(r"^NON_ITEM_LINE_CAP = (\d+)$", scripts, re.M)
        self.assertIsNotNone(enforced, "NON_ITEM_LINE_CAP is not defined")
        self.assertEqual(int(stated.group(1)), int(enforced.group(1)))

    def test_measured_file_roster_matches_enforced_roster(self):
        # Membership, not just the cap value: a third file added to
        # DENSITY_FILES without a rulebook mention (or dropped from it with
        # the rulebook still naming it) would otherwise pass silently. The
        # two-axes bullet names the measured files; DENSITY_FILES is the
        # roster the advisory iterates.
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        body = re.search(r"DENSITY_FILES = \((.*?)\)", scripts, re.S)
        self.assertIsNotNone(body, "DENSITY_FILES is not defined in cairn_scripts.py")
        enforced = set(re.findall(r'"cairn/([^"]+)"', body.group(1)))
        block = re.search(
            r"\*\*Two axes, one file\.\*\*(.*?)\n- ", self.rules, re.S
        )
        self.assertIsNotNone(block, "the two-axes bullet is missing")
        stated = {
            name for name in ("ROADMAP.md", "LESSONS.md", "PROFILE.md")
            if f"`{name}`" in block.group(1)
        }
        self.assertEqual(stated, enforced)

    def test_lessons_header_states_its_own_enforced_cap(self):
        # The header is what a maintainer reads at post-merge hygiene while
        # deciding whether to prune (M87 review F1's lesson: a stale figure
        # there sends them on the wrong remedy with validate reporting OK
        # throughout). Since M101 the item cap is the only whole-file cap, so
        # the header must teach it — and must state no character threshold.
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        line_caps = re.search(r"LINE_CAPS\s*=\s*\{(.*?)\}", scripts, re.S).group(1)
        enforced = int(re.search(r'"cairn/LESSONS\.md":\s*(\d+)', line_caps).group(1))
        header = read(ROOT / "cairn" / "LESSONS.md")[:1200]
        self.assertIn(f"{enforced} lines", header)
        self.assertNotIn("characters, met by", header)

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
