"""Lock: M55/M77/M118 — the milestone weight cap exempts three sections,
`## Review`, `## Work log` and `## Decisions`.

The tracking-rules weight-caps text must state that a live milestone file is
capped on its plan-owned body only, name the exempt set with all three members,
and give each member's reason: `## Review` is review-owned (M55); the
`## Work log` is history under D-045 so counting it could demand an edit IP4
forbids (D-046); the milestone-local `## Decisions` section is history on its
own classification (D-074), which supersedes D-046's choice (3).
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

    def test_the_cap_definition_itself_names_both_subtracted_sections(self):
        # The bullet's DEFINITIONAL line — what the cap actually measures — is
        # a separate physical line from the set-membership sentence below it,
        # so pinning the set left this one free to say "less the `## Work log`"
        # alone with every gate green, contradicting the sentence one line
        # down. Two encodings of one subtraction; this pins the first.
        self.assertIn(
            "the review-exclusive `## Review` section, less the `## Work log` and `## Decisions` sections.",
            self.rules,
        )

    def test_weight_caps_states_single_pass_compression(self):
        # M69: over-cap trimming is one targeted pass driven by the breakdown,
        # never a nibble-and-recount loop — the discipline that keeps a session
        # from slowing to a crawl at the cap.
        self.assertIn("never a nibble-and-recount loop", self.rules)

    def test_weight_caps_states_cross_reference_not_restate(self):
        # M69: the classic overrun is a milestone restating a durable record's
        # substance; the remedy is to cross-reference it, not retype it.
        self.assertIn("cross-reference a durable record", self.rules)

    def test_weight_caps_names_the_exempt_set_with_all_three_members(self):
        # M77/D-046, widened to three at M118/D-074. Pinned label-WITH-members
        # on one physical line, per the M74/M76 lesson: an assert on the
        # mechanism sentence alone leaves the membership swappable (Review
        # counted, Work log exempt) or a member deletable with every other
        # assert still green. The mutation harness cannot catch that — blanking
        # is not swapping — so the set itself is the anchor. Re-anchored whole
        # rather than appended to, or the pre-M118 two-member sentence would
        # still satisfy a substring assert and the widening would be false
        # coverage (M118 AC5).
        self.assertIn(
            "The cap-exempt sections are exactly `## Review` (review-owned, M55), `## Work log` (history under D-045, D-046) and `## Decisions` (history under D-074)",
            self.rules,
        )

    def test_weight_caps_states_the_work_log_exemption_reason(self):
        # The reason is load-bearing: without it the exemption reads as a
        # convenience and the next cap squeeze re-aims at the work log.
        self.assertIn(
            "The `## Work log` is exempt because D-045 makes it history — never edited — so counting it could leave an over-cap file fixable only by an edit IP4 forbids (D-046).",
            self.rules,
        )

    def test_weight_caps_states_the_decisions_exemption_reason(self):
        # M118/D-074. Same load-bearing role as the work log's reason, and it
        # additionally records WHICH decision it supersedes — without that, a
        # later reader meets D-046's live choice (3) declining this exemption
        # and has no way to tell which entry won.
        self.assertIn(
            "D-074 makes its dated dispositions history, superseding D-046's choice (3), so the cap may not aim there either.",
            self.rules,
        )

    def test_always_read_frame_names_all_three_exempt_sections(self):
        # The frame's prose is the second place the rulebook enumerates the
        # set (M113's always-read row and the paragraph under it). A widening
        # that lands in the weight-caps bullet alone leaves the file naming a
        # pair here — the two-encodings drift M118 AC5 exists to close.
        self.assertIn(
            "(`## Work log`, `## Decisions`, `## Review`) by reading less of them",
            self.rules,
        )

    def test_template_decisions_comment_states_the_exemption_and_its_reason(self):
        # The template is where an author actually meets the rule, and the
        # decisions section is the member whose exemption is newest — a
        # template still calling it counted teaches the superseded rule. Pinned
        # label-WITH-reason on one physical line: a bare `(D-074)` assert would
        # let the un-editability ground delete green, and without the ground
        # the exemption reads as a convenience the next squeeze may revoke.
        template = read(SKILLS / "shared" / "templates" / "milestone.md")
        self.assertIn(
            "EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log",
            template,
        )

    def test_template_review_comment_names_all_three_exempt_sections(self):
        # The `## Review` comment is the template's other enumeration site, and
        # it was the one M118 could revert to a pair with the whole suite green
        # — the work-log comment's own `(D-046)` assert covers a different
        # physical line, so nothing pinned this one.
        template = read(SKILLS / "shared" / "templates" / "milestone.md")
        self.assertIn(
            "as are the work log (D-046) and the decisions section (D-074)",
            template,
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
            "all three cap-exempt sections are omitted, so the remedy can never aim", self.rules
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
        # Anchored in the sentence that STATES the advisory, not on the bare
        # label: M113's always-read row names the same label, so a bare match
        # would survive deleting the rule outright — false coverage, and the
        # mutation harness reddened on exactly that (M104's pattern).
        self.assertIn(f"so `cairn_validate`'s `{emitted.group(1)}`", self.rules)

    def test_the_decisions_advisory_is_stated_with_its_subject(self):
        # M119/D-075. The severity and the SUBJECT are both decisions, and the
        # subject is the one D-074 part 3 got wrong: a rulebook naming the
        # advisory without saying it watches pasted output rather than entry
        # length teaches the superseded grammar, which measured at 117 WARNs
        # over the corpus RR08 read. Pinned on one physical line so
        # a revert to entry length cannot leave the sentence green.
        self.assertIn(
            "advisory WARNs on — pasted output or a fenced transcript block, never entry",
            self.rules,
        )

    def test_stated_decisions_advisory_label_matches_the_emitted_label(self):
        # M59's rule, applied to the second counterweight: prose naming a
        # validate finding must use the label the script emits, or run-and-read
        # sends the reader hunting a string that never appears. Anchored in the
        # sentence that STATES the advisory — the always-read frame's row names
        # the same label, so a bare match would survive deleting the rule.
        validate = read(ROOT / "scripts" / "cairn_validate.py")
        emitted = re.search(
            r'\(\s*"([\w -]+)",\s*lambda root, rows: check_decisions_format', validate
        )
        self.assertIsNotNone(
            emitted, "check_decisions_format is not registered in ADVISORIES"
        )
        self.assertIn(f"what `cairn_validate`'s `{emitted.group(1)}`", self.rules)

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
