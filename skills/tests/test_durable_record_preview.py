"""Regression guard: the M64 durable-record preview rule (D-036).

Locks the Output & interaction discipline rule in `tracking-rules.md` (AC1),
the Deltas-not-dumps carve-out (AC2), and the one-line preview directives at
the four durable-record commit steps (AC3): `/milestone-plan` step 6,
`/milestone-review` post-merge hygiene, `/milestone-implement` task loop +
substantive amendments, `/milestone-brief` RR ingestion.

Skill-prose guards read the file as one string, so every asserted phrase
lives on a single source line (M23), steers clear of `**bold**` splits
(M26), and is read per-test, never cached at class level (M61); phrases are
matched case-insensitively.

    python3 -m unittest discover -s skills/tests -v
"""

import pathlib
import unittest

SKILLS = pathlib.Path(__file__).resolve().parent.parent


def read(*parts):
    return SKILLS.joinpath(*parts).read_text().lower()


def rules():
    return read("shared", "tracking-rules.md")


class TestDurableRecordPreviewRule(unittest.TestCase):
    def test_rule_present_with_mechanic(self):
        t = rules()
        self.assertIn("newly authored durable-record text", t)
        self.assertIn("is shown verbatim in chat immediately before", t)
        self.assertIn("same turn, no added stop", t)

    def test_rule_names_the_covered_record_types(self):
        t = rules()
        self.assertIn(
            "d-entry, a milestone file's plan-owned sections (new or via a gated",
            t,
        )
        self.assertIn("a lessons line, an archive summary, a roadmap", t)

    def test_rule_names_the_exemptions(self):
        self.assertIn(
            "noise: work-log one-liners, checkbox ticks, status-mirror updates",
            rules(),
        )

    def test_deltas_not_dumps_names_the_carve_out(self):
        self.assertIn(
            "not a dump — see the durable-record preview rule below.",
            rules(),
        )


class TestPerSkillDirectives(unittest.TestCase):
    def test_plan_commit_step(self):
        self.assertIn(
            "durable-record preview first (tracking-rules):",
            read("milestone-plan", "SKILL.md"),
        )

    def test_review_hygiene_step(self):
        self.assertIn(
            "preview (tracking-rules): show the archive summary, each lessons line,",
            read("milestone-review", "SKILL.md"),
        )

    def test_implement_decisions_and_amendments(self):
        t = read("milestone-implement", "SKILL.md")
        self.assertIn(
            "durable-record preview (tracking-rules): a milestone-local decisions",
            t,
        )
        self.assertIn(
            "verbatim in chat before its commit (durable-record preview).",
            t,
        )

    def test_brief_rr_ingestion(self):
        self.assertIn(
            "durable-record preview (tracking-rules): show the",
            read("milestone-brief", "SKILL.md"),
        )


if __name__ == "__main__":
    unittest.main()
