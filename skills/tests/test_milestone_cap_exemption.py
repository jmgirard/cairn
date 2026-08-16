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


    def test_weight_caps_states_the_plan_owned_body_cap(self):
        self.assertIn("plan-owned body < 150 lines", self.rules)


    def test_weight_caps_states_single_pass_compression(self):
        # M69: over-cap trimming is one targeted pass driven by the breakdown,
        # never a nibble-and-recount loop — the discipline that keeps a session
        # from slowing to a crawl at the cap.
        self.assertIn("never a nibble-and-recount loop", self.rules)


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


    def test_template_work_log_comment_states_the_exemption(self):
        # The template is where an author actually meets the rule.
        template = read(SKILLS / "shared" / "templates" / "milestone.md")
        self.assertIn("EXEMPT from the 150-line cap (D-046)", template)


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
