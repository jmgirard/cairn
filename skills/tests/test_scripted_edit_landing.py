"""Regression guard: the M131 verify-an-edit-landed rule.

Locks the three-clause conduct rule in `tracking-rules.md` "Universal
tracking rules" (AC1): verify before you claim, anchor on text unique in
the target file, and sequence a tick strictly after its evidence write.

The rule exists because the class fired three times — M126 (a `str.replace`
matched a second occurrence and dropped a work-log line into a plan-owned
section), a separately reported session, and M130 review D13 (a non-unique
`## Review` anchor failed while its sibling tick-script landed, ticking a
criterion before its evidence existed). Each was caught by a reader, never
by the author.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23) and steers clear of `**bold**` splits
(M26); phrases are matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def rules():
    return SKILLS.joinpath("shared", "tracking-rules.md").read_text().lower()


class TestScriptedEditLandingRule(unittest.TestCase):
    def test_rule_requires_verification_before_the_claiming_record(self):
        # The whole rule: a record may not assert a change until the aimed
        # site has been re-read. Without this the other two clauses are
        # anchor hygiene with nothing obliging anyone to look.
        self.assertIn(
            "verify an edit landed before writing the record that claims it did",
            rules(),
        )

    def test_rule_requires_a_unique_anchor_for_a_section_edit(self):
        # Uniqueness, not a ban on bare headings — the M130 instance was a
        # NON-unique `## Review`, and the plan gate declined the wider ban.
        self.assertIn(
            "anchors on text that occurs exactly once in the target file",
            rules(),
        )

    def test_rule_sequences_a_tick_after_its_evidence_write_succeeds(self):
        t = rules()
        self.assertIn(
            "sequenced strictly after the write of the evidence it depends on has succeeded",
            t,
        )
        # The prohibition is the operative half: without it "sequenced after"
        # reads as an ordering preference a single batched turn satisfies.
        self.assertIn("never in the same unverified batch", t)


if __name__ == "__main__":
    unittest.main()
