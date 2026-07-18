"""Lock: M55/M77 — the milestone weight cap exempts two sections, `## Review`
and `## Work log`.

The tracking-rules weight-caps text must state that a live milestone file is
capped on its plan-owned body only, name the exempt set with both members, and
give each member's reason: `## Review` is review-owned (M55), the `## Work log`
is history under D-045 so counting it could demand an edit IP4 forbids (D-046).
The stated cap (150) must equal the enforced `MILESTONE_CAP` in
`cairn_scripts.py`, and the stated advisory label must equal the one
`cairn_validate` emits — two encodings of one fact that must not drift. The
measurements themselves are enforced by the fixtures in `scripts/tests`; this
guard locks the stated rules and the stated↔enforced agreements.

    python3 -m unittest discover -s skills/tests
"""

import pathlib
import re
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent
ROOT = SKILLS.parent


def read(path):
    return path.read_text()


class TestMilestoneCapExemption(unittest.TestCase):
    def setUp(self):
        self.rules = read(SKILLS / "shared" / "tracking-rules.md")

    def test_weight_caps_states_review_exemption(self):
        # Anchored on the rule's own contiguous phrasing (M39/M23 single-line):
        # the *reason* the exemption exists is the load-bearing sentence.
        self.assertIn(
            "review evidence never scrambles plan-owned content", self.rules
        )

    def test_weight_caps_states_the_plan_owned_body_cap(self):
        self.assertIn("plan-owned body < 150 lines", self.rules)

    def test_weight_caps_states_single_pass_compression(self):
        # M69: over-cap trimming is one targeted pass driven by the breakdown,
        # never a nibble-and-recount loop — the discipline that keeps a session
        # from slowing to a crawl at the cap.
        self.assertIn("never a nibble-and-recount loop", self.rules)

    def test_weight_caps_states_cross_reference_not_restate(self):
        # M69: the classic overrun is a milestone restating a durable record's
        # substance; the remedy is to cross-reference it, not retype it.
        self.assertIn("cross-reference a durable record", self.rules)

    def test_weight_caps_names_the_exempt_set_with_both_members(self):
        # M77/D-046. Pinned label-WITH-members on one physical line, per the
        # M74/M76 lesson: an assert on the mechanism sentence alone leaves the
        # membership swappable (Review counted, Work log exempt) or a member
        # deletable with every other assert still green. The mutation harness
        # cannot catch that — blanking is not swapping — so the set itself is
        # the anchor.
        self.assertIn(
            "The cap-exempt sections are exactly `## Review` (review-owned, M55) and `## Work log` (history under D-045, D-046)",
            self.rules,
        )

    def test_weight_caps_states_the_work_log_exemption_reason(self):
        # The reason is load-bearing: without it the exemption reads as a
        # convenience and the next cap squeeze re-aims at the work log.
        self.assertIn(
            "The `## Work log` is exempt because D-045 makes it history — never edited — so counting it could leave an over-cap file fixable only by an edit IP4 forbids (D-046).",
            self.rules,
        )

    def test_weight_caps_states_the_wrapped_entry_advisory_warns(self):
        # The severity is the decision (D-046): WARN, never a gate failure.
        self.assertIn(
            "advisory WARNs on any work-log line that is not a one-line `- ` entry", self.rules
        )

    def test_remedy_never_aims_at_an_exempt_section(self):
        # M69's breakdown drives the remedy, so it must list only trimmable
        # sections — otherwise the cure points at history (IP4).
        self.assertIn(
            "both cap-exempt sections are omitted, so the remedy can never aim", self.rules
        )

    def test_template_work_log_comment_states_the_exemption(self):
        # The template is where an author actually meets the rule.
        template = read(SKILLS / "shared" / "templates" / "milestone.md")
        self.assertIn("EXEMPT from the 150-line cap (D-046)", template)

    def test_stated_advisory_label_matches_the_emitted_label(self):
        # M59: prose naming a validate finding must use the label the script
        # actually emits, or run-and-read sends the reader hunting for a string
        # that never appears. Two encodings of one label; drift is the defect.
        validate = read(ROOT / "scripts" / "cairn_validate.py")
        emitted = re.search(r'\(\s*"([\w -]+)",\s*lambda root, rows: check_worklog_format', validate)
        self.assertIsNotNone(emitted, "check_worklog_format is not registered in ADVISORIES")
        self.assertIn(f"`{emitted.group(1)}`", self.rules)

    def test_stated_cap_matches_enforced_cap(self):
        # The rulebook's human-readable cap and the scripts' machine-enforced cap
        # are two encodings of one number; drift between them is the defect.
        stated = int(
            re.search(r"plan-owned body < (\d+) lines", self.rules).group(1)
        )
        scripts = read(ROOT / "scripts" / "cairn_scripts.py")
        enforced = int(re.search(r"MILESTONE_CAP\s*=\s*(\d+)", scripts).group(1))
        self.assertEqual(stated, enforced)


if __name__ == "__main__":
    unittest.main()
