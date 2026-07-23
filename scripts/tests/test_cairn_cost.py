"""Guards for cairn_cost.py — the M94 cost instrumentation.

Two properties are load-bearing and everything the script reports rests on
them, so both are asserted against the **classifier functions** rather than
the rendered report (M93: a guard that reads the rendered string passes over a
classifier that has silently changed behind an unchanged format).

1. ATTRIBUTION. `phase_of` and `milestone_of` read runtime-written fields.
   A regression here would silently re-key every figure.
2. THE CACHE/FRESH SPLIT. `cache_read_input_tokens` and `input_tokens` differ
   by ~three orders of magnitude in the real store, so a change that summed
   them into one "input" figure would not look wrong — it would look
   plausible and be off by ~99.9%. The guards below fail if any accumulator
   ever carries their sum.

Every negative assertion is paired with a positive one proving the path
actually ran (M84): a test that only checks "X is absent" passes just as
happily when nothing executed at all.

Run from the repo root:

    python3 -m unittest discover -s scripts/tests -k cost
"""

import pathlib
import re
import sys
import unittest

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import cairn_cost as cost  # noqa: E402  (after sys.path shim)


def rec(skill=None, branch=None, usage=None, content=None):
    """A minimal `assistant` record in the store's real shape."""
    return {
        "type": "assistant",
        "attributionSkill": skill,
        "gitBranch": branch,
        "message": {"usage": usage or {}, "content": content or []},
    }


def agent_block(name="Agent"):
    return {"type": "tool_use", "name": name, "input": {}}


class TestPhaseAttribution(unittest.TestCase):
    """`attributionSkill` -> phase. A lookup over a runtime-written field."""

    def test_the_three_milestone_phases_map_to_their_canonical_names(self):
        self.assertEqual(cost.phase_of(rec(skill="cairn:milestone-plan")), "plan")
        self.assertEqual(
            cost.phase_of(rec(skill="cairn:milestone-implement")), "implement"
        )
        self.assertEqual(cost.phase_of(rec(skill="cairn:milestone-review")), "review")

    def test_the_other_cairn_skills_keep_their_own_phase_names(self):
        # Real work with a real cost, just not a milestone phase — folding
        # them into `unattributed` would hide it.
        self.assertEqual(cost.phase_of(rec(skill="cairn:hotfix")), "hotfix")
        self.assertEqual(cost.phase_of(rec(skill="cairn:milestone")), "milestone")
        self.assertEqual(
            cost.phase_of(rec(skill="cairn:cairn-release")), "cairn-release"
        )

    def test_a_record_outside_any_cairn_skill_is_unattributed(self):
        # Paired positive: the same classifier does attribute a known skill,
        # so this is a real negative and not a dead code path.
        self.assertEqual(cost.phase_of(rec(skill=None)), cost.UNATTRIBUTED)
        self.assertEqual(cost.phase_of(rec(skill="some-other-plugin:thing")), cost.UNATTRIBUTED)
        self.assertEqual(cost.phase_of(rec(skill="cairn:milestone-plan")), "plan")

    def test_the_phase_map_covers_every_shipped_cairn_skill(self):
        # A new operational skill whose turns land in `unattributed` would
        # quietly shrink every phase figure.
        shipped = {
            p.parent.name
            for p in (SCRIPTS_DIR.parent / "skills").glob("*/SKILL.md")
            if p.parent.name != "shared"
        }
        mapped = {k.split(":", 1)[1] for k in cost.PHASES}
        self.assertTrue(shipped, "no shipped skills discovered — vacuous")
        self.assertEqual(
            shipped - mapped,
            set(),
            "shipped cairn skills missing from cairn_cost.PHASES",
        )


class TestMilestoneAttribution(unittest.TestCase):
    """`gitBranch` -> milestone id. The branch name is the only authoritative
    key; everything else is refused rather than guessed (M94 ledger A3)."""

    def test_a_milestone_branch_yields_its_id(self):
        self.assertEqual(cost.milestone_of(rec(branch="m94-cost-instrumentation")), "M94")
        self.assertEqual(cost.milestone_of(rec(branch="m07-guardrail-hooks")), "M07")
        self.assertEqual(cost.milestone_of(rec(branch="m100-past-ninety-nine")), "M100")

    def test_default_branch_and_hotfix_work_is_not_keyed_to_a_milestone(self):
        # None is a real answer, never a failure: plan-phase work runs here.
        # Paired positive so the None is not just an unreached branch.
        self.assertIsNone(cost.milestone_of(rec(branch="main")))
        self.assertIsNone(cost.milestone_of(rec(branch="master")))
        self.assertIsNone(cost.milestone_of(rec(branch="hotfix-bad-parse")))
        self.assertIsNone(cost.milestone_of(rec(branch=None)))
        self.assertEqual(cost.milestone_of(rec(branch="m94-x")), "M94")

    def test_a_milestone_id_is_never_imputed_from_prose(self):
        # A plan session legitimately names four milestones; keying off text
        # would credit the cost to all four. The branch is the only input.
        record = rec(branch="main", skill="cairn:milestone-plan")
        record["message"]["content"] = [
            {"type": "text", "text": "planning M94, M95, M96 and M97 together"}
        ]
        self.assertIsNone(cost.milestone_of(record))
        self.assertEqual(cost.phase_of(record), "plan")


class TestSessionAttribution(unittest.TestCase):
    """Per-session is the finest grain the store supports, and AC1 requires
    the report carry it alongside the per-phase view."""

    def test_session_id_comes_from_the_transcript_filename(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            (pathlib.Path(tmp) / "aaaa1111.jsonl").write_text(
                '{"type":"assistant","message":{"usage":{"output_tokens":3}}}\n',
                encoding="utf-8",
            )
            records = list(cost.read_records(tmp))
        self.assertTrue(records, "fixture store produced no records — vacuous")
        self.assertEqual({cost.session_of(r) for r in records}, {"aaaa1111"})

    def test_aggregating_by_session_keeps_sessions_apart(self):
        a = rec(skill="cairn:milestone-implement", branch="m94-x",
                usage={"cache_read_input_tokens": 10})
        b = rec(skill="cairn:milestone-review", branch="m94-x",
                usage={"cache_read_input_tokens": 400})
        a["_session"], b["_session"] = "sess-a", "sess-b"
        buckets = cost.aggregate([a, b], cost.session_of)
        self.assertEqual(set(buckets), {"sess-a", "sess-b"})
        self.assertEqual(buckets["sess-a"]["cache_read_input_tokens"], 10)
        self.assertEqual(buckets["sess-b"]["cache_read_input_tokens"], 400)

    def test_the_report_renders_a_per_session_section(self):
        a = rec(skill="cairn:milestone-implement", branch="m94-x",
                usage={"cache_read_input_tokens": 12345})
        a["_session"] = "deadbeef-1111"
        text = cost.report(str(SCRIPTS_DIR.parent), [a])
        self.assertIn("BY SESSION", text)
        # Assert against the SESSION ROW ITSELF, not the whole report: "M94",
        # "implement" and "12,345" all also render in the BY MILESTONE and
        # BY PHASE sections, so asserting them against `text` would pass with
        # the session row's labels stripped entirely — false coverage
        # (mutation-proven at review, M94 F5).
        row = next(
            ln for ln in text.splitlines() if ln.startswith("deadbeef")
        )
        self.assertIn("M94", row)
        self.assertIn("implement", row)
        self.assertIn("12,345", row)

    def test_a_session_spanning_phases_names_every_phase_it_carried(self):
        # The real case: one session runs implement then review. Labelling it
        # with only the first would misattribute the review fan-out's cost.
        recs = []
        for skill in ("cairn:milestone-implement", "cairn:milestone-review"):
            r = rec(skill=skill, branch="m94-x", usage={"output_tokens": 1})
            r["_session"] = "spanning"
            recs.append(r)
        text = cost.report(str(SCRIPTS_DIR.parent), recs)
        self.assertIn("implement,review", text)


class TestCacheFreshSplit(unittest.TestCase):
    """The four billed classes stay four. Never summed, never collapsed."""

    def test_the_two_input_classes_are_distinct_named_columns(self):
        self.assertIn("cache_read_input_tokens", cost.TOKEN_CLASSES)
        self.assertIn("input_tokens", cost.TOKEN_CLASSES)
        self.assertEqual(len(cost.TOKEN_CLASSES), len(set(cost.TOKEN_CLASSES)))
        self.assertEqual(len(cost.TOKEN_CLASSES), 4)

    def test_tokens_of_keeps_cache_read_and_fresh_input_apart(self):
        got = cost.tokens_of(
            rec(usage={"cache_read_input_tokens": 500_000, "input_tokens": 7})
        )
        self.assertEqual(got["cache_read_input_tokens"], 500_000)
        self.assertEqual(got["input_tokens"], 7)
        self.assertNotIn(500_007, got.values(), "the two input classes were summed")

    def test_aggregate_never_produces_a_bucket_holding_their_sum(self):
        records = [
            rec(
                skill="cairn:milestone-implement",
                branch="m94-x",
                usage={
                    "cache_read_input_tokens": 1_000_000,
                    "cache_creation_input_tokens": 20,
                    "input_tokens": 3,
                    "output_tokens": 400,
                },
            )
        ] * 2
        bucket = cost.aggregate(records, cost.phase_of)["implement"]
        # Positive: the path ran and each class accumulated on its own.
        self.assertEqual(bucket["cache_read_input_tokens"], 2_000_000)
        self.assertEqual(bucket["input_tokens"], 6)
        self.assertEqual(bucket["turns"], 2)
        # Negative: no accumulator carries any collapsed input figure.
        self.assertNotIn(2_000_006, bucket.values())
        self.assertNotIn(2_000_046, bucket.values())

    def test_the_report_renders_the_two_as_separate_columns(self):
        records = [
            rec(
                skill="cairn:milestone-review",
                branch="m94-x",
                usage={"cache_read_input_tokens": 900_001, "input_tokens": 11},
            )
        ]
        text = cost.report(str(SCRIPTS_DIR.parent), records)
        self.assertIn("cache-read", text)
        self.assertIn("fresh-in", text)
        self.assertIn("900,001", text)
        self.assertIn("11", text)
        self.assertNotIn("900,012", text, "the report printed a collapsed input figure")


class TestSubagentBlindSpot(unittest.TestCase):
    """Subagent tokens are absent from the store, so the spawn count is what
    labels a partial figure (M94 ledger A4/A5)."""

    def test_spawned_agents_are_counted_under_every_known_tool_name(self):
        self.assertEqual(cost.agents_spawned(rec(content=[agent_block("Agent")])), 1)
        self.assertEqual(cost.agents_spawned(rec(content=[agent_block("Task")])), 1)
        self.assertEqual(
            cost.agents_spawned(
                rec(content=[agent_block("Agent"), agent_block("Agent")])
            ),
            2,
        )

    def test_non_spawning_tools_and_plain_text_count_zero(self):
        self.assertEqual(cost.agents_spawned(rec(content=[agent_block("Bash")])), 0)
        self.assertEqual(cost.agents_spawned(rec(content=[{"type": "text", "text": "Agent"}])), 0)
        self.assertEqual(cost.agents_spawned(rec(content=None)), 0)
        # Paired positive: the counter does fire on a real spawn.
        self.assertEqual(cost.agents_spawned(rec(content=[agent_block()])), 1)

    def test_every_report_surface_carries_the_spawn_count(self):
        records = [
            rec(
                skill="cairn:milestone-review",
                branch="m94-x",
                usage={"cache_read_input_tokens": 5},
                content=[agent_block()],
            )
        ]
        root = str(SCRIPTS_DIR.parent)
        self.assertIn("agents", cost.report(root, records))
        line = cost.audit_line(root, records)
        self.assertIn("M94", line)
        self.assertIn("1 subagent spawned", line)
        self.assertIn("unrecorded", line)


class TestMilestoneFlagIsHonouredOrRefused(unittest.TestCase):
    """M94 review F4: a flag that is accepted and then silently ignored
    answers a different question than the one asked."""

    def test_audit_line_honours_an_explicit_milestone(self):
        records = [
            rec(skill="cairn:milestone-review", branch="m94-x",
                usage={"output_tokens": 9}),
            rec(skill="cairn:milestone-implement", branch="m85-y",
                usage={"output_tokens": 4}),
        ]
        root = str(SCRIPTS_DIR.parent)
        # Default: the most recent milestone.
        self.assertIn("cost: M94", cost.audit_line(root, records))
        # Explicit: the one asked for, not the most recent.
        line = cost.audit_line(root, records, milestone="M85")
        self.assertIn("cost: M85", line)
        self.assertNotIn("M94", line)

    def test_audit_line_says_so_when_the_named_milestone_has_no_records(self):
        records = [rec(skill="cairn:milestone-review", branch="m94-x",
                       usage={"output_tokens": 1})]
        line = cost.audit_line(str(SCRIPTS_DIR.parent), records, milestone="M42")
        self.assertIn("M42", line)
        self.assertIn("no milestone-keyed sessions", line)

    def test_attribution_mode_refuses_the_milestone_filter(self):
        # Honouring it would reintroduce F3: the share is a whole-store
        # property and filtering makes it 0.0% by construction.
        #
        # Driven against a FIXTURE store through the `home=` seam (M109), so
        # neither the refusal nor the success path scans the real ~26k-record
        # store. A spy over `read_records` proves the real store was never
        # touched — the fixture under `home` is the only store read.
        import tempfile
        from unittest import mock

        import cairn_scripts as cs  # same-dir import; resolves the store root

        root = cs.resolve_root(["cairn_cost"])
        real_store = cost.store_dir(root)
        with tempfile.TemporaryDirectory() as home:
            store = cost.store_dir(root, home)
            pathlib.Path(store).mkdir(parents=True)
            (pathlib.Path(store) / "sess.jsonl").write_text(
                '{"type":"assistant","attributionSkill":"cairn:milestone-implement",'
                '"gitBranch":"m94-x","message":{"usage":'
                '{"cache_read_input_tokens":5}}}\n',
                encoding="utf-8",
            )
            seen = []
            orig = cost.read_records

            def spy(s):
                seen.append(s)
                return orig(s)

            with mock.patch.object(cost, "read_records", spy):
                # Refused: exit 2, and (AC2) the refusal precedes read_records.
                self.assertEqual(
                    cost.main(
                        ["cairn_cost.py", "--attribution", "--milestone", "M94"],
                        home=home,
                    ),
                    2,
                )
                # Paired positive: the same mode succeeds unfiltered, running
                # real attribution over the fixture's records.
                self.assertEqual(
                    cost.main(["cairn_cost.py", "--attribution"], home=home), 0
                )
            # The success path ran (spy fired) and read only the fixture — the
            # real store path was never opened.
            self.assertTrue(seen, "read_records never ran — success path skipped")
            self.assertNotIn(real_store, seen)
            self.assertTrue(all(s.startswith(home) for s in seen), seen)

    def test_attribution_refusal_reads_no_store_even_with_none_present(self):
        # AC2: the --attribution --milestone refusal precedes both the isdir
        # check and read_records — with `home` pointed at an empty dir (no
        # store at all) it still returns 2, not the no-store branch's 0.
        import tempfile

        with tempfile.TemporaryDirectory() as home:
            self.assertEqual(
                cost.main(
                    ["cairn_cost.py", "--attribution", "--milestone", "M94"],
                    home=home,
                ),
                2,
            )


class TestUnattributableShareIsReported(unittest.TestCase):
    """A method that hid its unattributable share would not be acceptable
    evidence (M94 T1)."""

    def test_attribution_counts_both_unkeyed_dimensions_and_their_token_mass(self):
        records = [
            rec(skill="cairn:milestone-implement", branch="m94-x",
                usage={"cache_read_input_tokens": 100}),
            rec(skill="cairn:milestone-plan", branch="main",
                usage={"cache_read_input_tokens": 300}),
            rec(skill=None, branch="main", usage={"cache_read_input_tokens": 600}),
        ]
        stats = cost.attribution(records)
        self.assertEqual(stats["records"], 3)
        self.assertEqual(stats["no_milestone"], 2)
        self.assertEqual(stats["no_phase"], 1)
        self.assertEqual(stats["cache_read_input_tokens"], 1000)
        # The token-mass share differs from the record share — reporting only
        # the record count would understate the cost that went unkeyed.
        self.assertEqual(stats["no_milestone_cache_read"], 900)
        self.assertEqual(stats["no_phase_cache_read"], 600)

    def test_filtering_to_one_milestone_does_not_zero_the_share(self):
        # Regression (M94 review F3): running attribution over the FILTERED
        # set makes the share 0.0% by construction — the method reporting its
        # own blind spot as zero, which T1 forbids outright.
        records = [
            rec(skill="cairn:milestone-implement", branch="m94-x",
                usage={"cache_read_input_tokens": 100}),
            rec(skill="cairn:milestone-plan", branch="main",
                usage={"cache_read_input_tokens": 300}),
        ]
        text = cost.report(str(SCRIPTS_DIR.parent), records, milestone="M94")
        self.assertIn("filtered to M94", text)
        self.assertIn("50.0% not keyed to a milestone", text)
        self.assertIn("whole store", text)
        # Digit-anchored: a bare "0.0%" substring also matches the "50.0%"
        # this test wants to see, which would make the negative vacuous.
        self.assertNotRegex(text, r"(?<!\d)0\.0% not keyed to a milestone")

    def test_the_session_count_describes_the_rows_actually_rendered(self):
        # Regression (M94 review F2): counting *.jsonl on disk while the
        # tables are filtered describes a different population than the one
        # printed underneath it.
        a = rec(skill="cairn:milestone-implement", branch="m94-x",
                usage={"output_tokens": 1})
        b = rec(skill="cairn:milestone-implement", branch="m95-y",
                usage={"output_tokens": 1})
        a["_session"], b["_session"] = "s-a", "s-b"
        self.assertIn("1 sessions", cost.report(str(SCRIPTS_DIR.parent), [a, b], milestone="M94"))
        self.assertIn("2 sessions", cost.report(str(SCRIPTS_DIR.parent), [a, b]))

    def test_the_report_states_the_unattributable_share(self):
        records = [
            rec(skill="cairn:milestone-plan", branch="main",
                usage={"cache_read_input_tokens": 300}),
            rec(skill="cairn:milestone-implement", branch="m94-x",
                usage={"cache_read_input_tokens": 100}),
        ]
        text = cost.report(str(SCRIPTS_DIR.parent), records)
        self.assertIn("not keyed to a milestone", text)
        self.assertIn("50.0%", text)
        self.assertIn("75.0% of cache-read", text)


class TestStoreLocation(unittest.TestCase):
    def test_the_slug_is_the_absolute_path_with_separators_replaced(self):
        self.assertEqual(
            cost.store_slug("/Users/x/GitHub/cairn"), "-Users-x-GitHub-cairn"
        )
        self.assertEqual(cost.store_slug("/a/b_c.d"), "-a-b-c-d")

    def test_read_records_skips_malformed_lines_without_dying(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "s.jsonl"
            path.write_text(
                '{"type":"assistant","message":{"usage":{"output_tokens":5}}}\n'
                "not json at all\n"
                '{"type":"user"}\n'
                '{"type":"assistant","message":{"usage":{"output_tokens":7}}}\n',
                encoding="utf-8",
            )
            got = list(cost.read_records(tmp))
        # Positive: both good assistant records survived, in order.
        self.assertEqual(len(got), 2)
        self.assertEqual(
            [cost.tokens_of(r)["output_tokens"] for r in got], [5, 7]
        )


if __name__ == "__main__":
    unittest.main()
