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
        # Two asserts, because the title and the instruction fail separately:
        # the title alone left the only operative sentence deletable green
        # (review F2/F3a). Pin the duty, not just its heading.
        t = rules()
        self.assertIn(
            "verify a batched or scripted edit landed before writing the record that claims it did",
            t,
        )
        self.assertIn(
            "re-read the aimed site and confirm the change is present before any record claiming it is written",
            t,
        )

    def test_rule_requires_a_unique_anchor_for_a_section_edit(self):
        # Uniqueness, not a ban on bare headings — the M130 instance was a
        # NON-unique `## Review`, and the plan gate declined the wider ban.
        # The SUBJECT is inside the anchor: it sits on the same physical line,
        # and pinning the predicate alone left "a scratch note" swappable in
        # green (review F3d, guard-doctrine §1's label-with-its-members rule).
        self.assertIn(
            "an edit targeting a document section anchors on text that occurs exactly once in the target file",
            rules(),
        )

    def test_rule_sequences_a_tick_after_its_evidence_write_succeeds(self):
        t = rules()
        # Subject inside the anchor, same reason as clause (ii) — the
        # predicate alone left "an optional courtesy tick" green (F3e).
        self.assertIn(
            "a check-off or tick write is sequenced strictly after the write of the evidence it depends on has succeeded",
            t,
        )
        # The prohibition is the operative half: without it "sequenced after"
        # reads as an ordering preference a single batched turn satisfies.
        self.assertIn("never in the same unverified batch", t)


if __name__ == "__main__":
    unittest.main()
