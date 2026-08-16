"""Fixture tests for the cairn guardrail hooks.

Each test runs a hook script as a real subprocess (stdin JSON in,
stdout JSON out) against a throwaway git repo, mirroring how Claude
Code invokes hooks. Run from the repo root:

    python3 -m unittest discover -s hooks/tests -v

METHODOLOGY NOTE (learned the hard way, M07 review attempt 1): these
tests assert the *shape of the JSON a hook prints*, not that Claude
Code honors that shape. A wrong-but-self-consistent contract (e.g. a
Stop block nested under hookSpecificOutput instead of top-level) passes
here while doing nothing live. So the asserted shapes below are pinned
to the official hooks contract (references/claude-code-hooks.md):
  - SessionStart / PreToolUse: event output nested under hookSpecificOutput.
  - Stop / SubagentStop block: TOP-LEVEL decision/reason.
Changing an asserted envelope requires re-checking it against the docs
and a live-fire, not just making the test green.
"""

import ast
import atexit
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

HOOKS_DIR = pathlib.Path(__file__).resolve().parent.parent

ROADMAP = """\
# Roadmap

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M07 | Test milestone | in-progress | — | high | milestones/M07-test.md |
| M01 | Old milestone | done | — | high | milestones/archive/M01-old.md |
"""

MILESTONE_SENTINEL = "UNIQUE-ACTIVE-MILESTONE-SENTINEL"


def run_hook(script, payload):
    return subprocess.run(
        [sys.executable, str(HOOKS_DIR / script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=30,
    )


def hook_json(proc):
    """Event output nested under hookSpecificOutput (SessionStart, PreToolUse)."""
    return json.loads(proc.stdout)["hookSpecificOutput"]


def hook_toplevel(proc):
    """Full stdout JSON — for Stop/SubagentStop, whose block is top-level."""
    return json.loads(proc.stdout)


# Each committed-clean repo shape is built ONCE (git init/config/add/commit =
# 5 spawns) and copytree'd per test, instead of re-running those 5 spawns in
# every setUp across 72 tests (M102). In-test git calls (branch, remote, push)
# still run live on the copy — only the identical baseline is shared.
_TEMPLATE_TMP = None
_TEMPLATES = {}


def _build_template(cairn):
    global _TEMPLATE_TMP
    if _TEMPLATE_TMP is None:
        _TEMPLATE_TMP = tempfile.TemporaryDirectory()
        atexit.register(_TEMPLATE_TMP.cleanup)
    root = pathlib.Path(_TEMPLATE_TMP.name) / ("cairn" if cairn else "plain")
    root.mkdir()

    def git(*args):
        subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "hooks@test.invalid")
    git("config", "user.name", "Hook Tests")
    if cairn:
        (root / "cairn" / "milestones").mkdir(parents=True)
        (root / "cairn" / "ROADMAP.md").write_text(ROADMAP)
        (root / "cairn" / "milestones" / "M07-test.md").write_text(
            f"# M07: Test milestone\n\n{MILESTONE_SENTINEL}\n"
        )
    (root / "code.txt").write_text("hello\n")
    git("add", "-A")
    git("commit", "-q", "-m", "init")
    return root


def _template(cairn):
    key = bool(cairn)
    if key not in _TEMPLATES:
        _TEMPLATES[key] = _build_template(key)
    return _TEMPLATES[key]


class RepoFixture(unittest.TestCase):
    """A temp git repo, cairn-tracked or not, committed clean."""

    cairn = True

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        # Copy the once-built committed-clean template (incl. its .git) rather
        # than re-running git init/config/add/commit here (M102). The hook is
        # still invoked as a real subprocess below — only setUp's git spawns go.
        shutil.copytree(_template(self.cairn), self.root, dirs_exist_ok=True)

    def git(self, *args):
        subprocess.run(
            ["git", *args], cwd=self.root, check=True, capture_output=True
        )

    def payload(self, **extra):
        base = {"session_id": "test", "cwd": str(self.root)}
        base.update(extra)
        return base


class TestSessionContext(RepoFixture):
    def test_injects_roadmap_and_active_milestone(self):
        proc = run_hook(
            "session_context.py",
            self.payload(hook_event_name="SessionStart", source="startup"),
        )
        self.assertEqual(proc.returncode, 0)
        out = hook_json(proc)
        self.assertEqual(out["hookEventName"], "SessionStart")
        self.assertIn("| M07 | Test milestone | in-progress |", out["additionalContext"])
        self.assertIn(MILESTONE_SENTINEL, out["additionalContext"])
        # only the active milestone's file is injected, not archived ones
        self.assertEqual(out["additionalContext"].count("## cairn/milestones/"), 1)

    def test_injects_profile_name_when_present(self):
        (self.root / "cairn" / "PROFILE.md").write_text(
            "# Toolchain profile: r-package\n\n## verify\n- x\n"
        )
        proc = run_hook(
            "session_context.py",
            self.payload(hook_event_name="SessionStart", source="startup"),
        )
        out = hook_json(proc)
        self.assertIn("Active toolchain profile", out["additionalContext"])
        self.assertIn("`r-package`", out["additionalContext"])

    def test_no_profile_section_when_absent(self):
        # RepoFixture writes no PROFILE.md — a pre-profile repo; the hook
        # no-ops the profile section (AC4) and still injects the ROADMAP.
        proc = run_hook(
            "session_context.py",
            self.payload(hook_event_name="SessionStart", source="startup"),
        )
        out = hook_json(proc)
        self.assertNotIn("Active toolchain profile", out["additionalContext"])
        self.assertIn("## cairn/ROADMAP.md", out["additionalContext"])


class TestSessionContextReadBound(RepoFixture):
    """M113/D-063 — cap-exempt sections are read-bounded newest-first.

    The bound exists because the old `[:MAX_CHARS]` tail chop discarded the
    NEWEST work-log entries, which are the ones carrying current state: a
    resuming session was told what a milestone finished days ago and never
    what it is blocked on. Sections the 150-line cap governs are injected
    whole; sections it exempts (`## Work log`, `## Decisions`, `## Review`)
    are bounded — the third member joined the set at M118/D-074.
    """

    def milestone(self, work_log=(), review=(), tasks=(), relpath=None,
                  decisions=(), decisions_heading="## Decisions"):
        """Write cairn/<relpath> with the given section bodies."""
        relpath = relpath or "milestones/M07-test.md"
        body = ["# M07: Test milestone", "", MILESTONE_SENTINEL, ""]
        if tasks:
            body += ["## Tasks", ""] + list(tasks) + [""]
        if decisions:
            body += [decisions_heading, ""] + list(decisions) + [""]
        body += ["## Work log", ""] + list(work_log) + [""]
        if review:
            body += ["## Review", ""] + list(review) + [""]
        path = self.root / "cairn" / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(body))
        return path

    def inject(self):
        proc = run_hook(
            "session_context.py",
            self.payload(hook_event_name="SessionStart", source="startup"),
        )
        self.assertEqual(proc.returncode, 0)
        return hook_json(proc)["additionalContext"]

    def test_long_work_log_keeps_the_newest_entries_and_drops_the_oldest(self):
        # Shaped on this repo's own worst case: M95's work log ran 23,147
        # chars across 65 entries. Both directions are pinned — asserting
        # only that the newest survives would pass against no bound at all.
        entries = [f"- 2026-07-{i % 28 + 1:02d}: entry-{i:03d} " + "x" * 300
                   for i in range(65)]
        self.milestone(work_log=entries)
        ctx = self.inject()
        self.assertIn("entry-064", ctx)
        self.assertNotIn("entry-000", ctx)

    def test_bounded_section_names_what_it_elided_and_where_to_read_it(self):
        entries = [f"- 2026-07-01: entry-{i:03d} " + "x" * 300 for i in range(65)]
        self.milestone(work_log=entries)
        ctx = self.inject()
        self.assertIn("of 65 entries shown", ctx)
        self.assertIn("read cairn/milestones/M07-test.md for the rest", ctx)

    def test_section_under_budget_is_injected_whole_with_no_marker(self):
        entries = [f"- 2026-07-01: entry-{i:03d}" for i in range(6)]
        self.milestone(work_log=entries)
        ctx = self.inject()
        for i in range(6):
            self.assertIn(f"entry-{i:03d}", ctx)
        self.assertNotIn("entries shown", ctx)

    def test_the_review_section_is_bounded_by_the_same_rule(self):
        # The generalization: the bound is derived from the cap, so EVERY
        # cap-exempt section gets it — not the work log alone.
        review = [f"- AC{i}: evidence-{i:03d} " + "y" * 300 for i in range(40)]
        self.milestone(work_log=["- 2026-07-01: one"], review=review)
        ctx = self.inject()
        self.assertIn("evidence-039", ctx)
        self.assertNotIn("evidence-000", ctx)

    def test_the_decisions_section_is_bounded_by_the_same_rule(self):
        # M118/D-074: the milestone-local `## Decisions` section joins the
        # cap-exempt set, and D-063 scopes the read-bound to that set — so it
        # follows automatically. Both directions pinned: asserting only that
        # the newest survives would pass against no bound at all.
        decisions = [f"- 2026-07-27: choice-{i:03d} " + "z" * 300
                     for i in range(40)]
        self.milestone(work_log=["- 2026-07-01: one"], decisions=decisions)
        ctx = self.inject()
        self.assertIn("choice-039", ctx)
        self.assertNotIn("choice-000", ctx)

    def test_bounded_decisions_section_names_what_it_elided(self):
        decisions = [f"- 2026-07-27: choice-{i:03d} " + "z" * 300
                     for i in range(40)]
        self.milestone(work_log=["- 2026-07-01: one"], decisions=decisions)
        ctx = self.inject()
        self.assertIn("of 40 entries shown", ctx)
        self.assertIn("read cairn/milestones/M07-test.md for the rest", ctx)

    def test_a_decisions_prefixed_heading_is_not_bounded(self):
        # The hook matches the exempt headings by equality, never prefix, by
        # the same rule the cap counters use — `## Decisions notes` is capped
        # plan-owned content, so the cap is already its bound and the
        # injection must not bound it a second time.
        notes = [f"- note-{i:03d} " + "z" * 300 for i in range(40)]
        self.milestone(work_log=["- 2026-07-01: one"], decisions=notes,
                       decisions_heading="## Decisions notes")
        ctx = self.inject()
        self.assertIn("note-000", ctx)
        self.assertIn("note-039", ctx)

    def test_capped_sections_are_injected_whole(self):
        # ## Tasks is plan-owned and counts against the 150-line cap, so the
        # cap is already its bound; the injection must not bound it again.
        tasks = [f"- [ ] T{i}: task-{i:03d} " + "z" * 300 for i in range(30)]
        self.milestone(tasks=tasks, work_log=["- 2026-07-01: one"])
        ctx = self.inject()
        self.assertIn("task-000", ctx)
        self.assertIn("task-029", ctx)

    def test_no_active_milestone_vanishes_when_the_total_budget_binds(self):
        # The old chop concatenated then sliced, so a later milestone could
        # disappear entirely — no header, no path, no trace.
        rows = [
            "| M07 | A | in-progress | — | high | milestones/M07-test.md |",
            "| M08 | B | review | — | high | milestones/M08-b.md |",
            "| M09 | C | blocked | — | high | milestones/M09-c.md |",
            "| M10 | D | blocked | — | high | milestones/M10-d.md |",
        ]
        (self.root / "cairn" / "ROADMAP.md").write_text(
            "# Roadmap\n\n| ID | Title | Status | Depends on | Priority | File/Archive |\n"
            "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
        )
        for rel in ("milestones/M07-test.md", "milestones/M08-b.md",
                    "milestones/M09-c.md", "milestones/M10-d.md"):
            self.milestone(
                relpath=rel,
                tasks=[f"- [ ] T{i}: " + "z" * 300 for i in range(40)],
                work_log=[f"- 2026-07-01: e{i} " + "x" * 300 for i in range(40)],
            )
        ctx = self.inject()
        for rel in ("M07-test.md", "M08-b.md", "M09-c.md", "M10-d.md"):
            with self.subTest(rel=rel):
                self.assertIn(f"## cairn/milestones/{rel}", ctx)

    def test_active_milestones_are_injected_in_progress_first(self):
        rows = [
            "| M09 | C | blocked | — | high | milestones/M09-c.md |",
            "| M07 | A | in-progress | — | high | milestones/M07-test.md |",
        ]
        (self.root / "cairn" / "ROADMAP.md").write_text(
            "# Roadmap\n\n| ID | Title | Status | Depends on | Priority | File/Archive |\n"
            "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
        )
        self.milestone(relpath="milestones/M09-c.md", work_log=["- 2026-07-01: c"])
        self.milestone(work_log=["- 2026-07-01: a"])
        ctx = self.inject()
        self.assertLess(
            ctx.index("## cairn/milestones/M07-test.md"),
            ctx.index("## cairn/milestones/M09-c.md"),
        )

    def test_prose_above_a_sections_first_entry_is_bounded_and_marked(self):
        # F1 (review round 1): everything above the first `- ` used to be an
        # exempt preamble — uncharged against the budget and uncounted — so a
        # section whose prose precedes one closing bullet injected whole with
        # no marker. One bullet was worse than none: a prose-only section fell
        # to line-blocking and bounded correctly.
        prose = [f"paragraph-{i:03d} " + "p" * 400 for i in range(40)]
        self.milestone(review=prose + ["- **Verdict** — ship it."],
                       work_log=["- 2026-07-01: one"])
        ctx = self.inject()
        self.assertNotIn("paragraph-000", ctx)
        self.assertIn("**Verdict** — ship it.", ctx)
        self.assertIn("read cairn/milestones/M07-test.md for the rest", ctx)

    def test_one_enormous_entry_still_leaves_the_injection_bounded(self):
        # The floors mean neither pass can bound a section made of ONE huge
        # unit — an entry, or a line. That is deliberate (half an entry is
        # noise), so the guarantee has to hold at the layer above: the
        # injection stays under budget and still points at the file.
        self.milestone(work_log=["- 2026-07-01: " + "w" * 40000])
        ctx = self.inject()
        self.assertLessEqual(len(ctx), 30000)
        self.assertIn("read cairn/milestones/M07-test.md", ctx)

    def test_milestone_headers_survive_an_oversized_roadmap(self):
        # F2 (review round 1): the shed loop only shrank milestone parts, and
        # the final chop cut from the end of the joined context — which is
        # where those parts live. A ROADMAP big enough on its own took every
        # milestone header with it, telling a resuming session nothing about
        # what is in flight. The ROADMAP's 60-line cap counts LINES and D-052
        # leaves item-line length uncapped, so this needs no gate to redden.
        rows = [
            "| M07 | A | in-progress | — | high | milestones/M07-test.md |",
            "| M08 | B | review | — | high | milestones/M08-b.md |",
        ]
        fat = "\n".join(
            f"| M{i:03d} | {'t' * 500} | done | — | high | milestones/archive/x.md |"
            for i in range(56)
        )
        (self.root / "cairn" / "ROADMAP.md").write_text(
            "# Roadmap\n\n| ID | Title | Status | Depends on | Priority | File/Archive |\n"
            "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n" + fat + "\n"
        )
        for rel in ("milestones/M07-test.md", "milestones/M08-b.md"):
            self.milestone(relpath=rel, work_log=["- 2026-07-01: one"])
        ctx = self.inject()
        self.assertIn("## cairn/milestones/M07-test.md", ctx)
        self.assertIn("## cairn/milestones/M08-b.md", ctx)
        self.assertIn("ROADMAP truncated", ctx)
        # The truncated ROADMAP part keeps the heading naming the file it
        # replaced, and the rewrite stays inside its own allowance — reserving
        # the notice at zero-width let it overshoot and re-fire the whole-
        # context chop, cutting a milestone's path mid-marker (round 2).
        self.assertIn("## cairn/ROADMAP.md", ctx)
        self.assertNotIn("injection truncated", ctx)
        self.assertLessEqual(len(ctx), 30000)

    def test_roadmap_truncation_reserves_its_notice_at_full_width(self):
        # Round 2 reproduced this at exactly 1 char over: the reserve used
        # `format(0, 0)` while the real line carried three-digit numbers.
        rows = [
            "| M07 | A | in-progress | — | high | milestones/M07-test.md |",
            "| M08 | B | review | — | high | milestones/M08-b.md |",
        ]
        fat = "\n".join(
            f"| M{i:03d} | {'t' * 59} | done | — | high | milestones/archive/x.md |"
            for i in range(400)
        )
        (self.root / "cairn" / "ROADMAP.md").write_text(
            "# Roadmap\n\n| ID | Title | Status | Depends on | Priority | File/Archive |\n"
            "|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n" + fat + "\n"
        )
        for rel in ("milestones/M07-test.md", "milestones/M08-b.md"):
            self.milestone(relpath=rel, work_log=["- 2026-07-01: one"])
        ctx = self.inject()
        self.assertLessEqual(len(ctx), 30000)
        self.assertNotIn("injection truncated", ctx)
        self.assertIn("read cairn/milestones/M08-b.md.", ctx)

    def test_a_cap_exempt_heading_is_matched_as_the_cap_matches_it(self):
        # F3/F4 (review round 1): `scripts/cairn_scripts.py` matches these
        # headings case-insensitively and fence-aware, and says it shares
        # those rules with the wrapped-entry advisory on purpose. A hook that
        # matched raw strings left `## Work Log` cap-exempt to the scripts but
        # injected WHOLE — the exact gap the read-bound exists to close.
        entries = [f"- 2026-07-01: entry-{i:03d} " + "x" * 300 for i in range(65)]
        path = self.root / "cairn" / "milestones" / "M07-test.md"
        path.write_text(
            "# M07\n\n## Work Log\n\n" + "\n".join(entries) + "\n"
        )
        ctx = self.inject()
        self.assertNotIn("entry-000", ctx)
        self.assertIn("entry-064", ctx)

    def test_reviewers_is_not_review(self):
        # M55's boundary bug, the invariant the matcher is written for: a
        # prefix match would bound `## Reviewers` as though it were `## Review`.
        prose = [f"- reviewer-{i:03d} " + "r" * 300 for i in range(40)]
        path = self.root / "cairn" / "milestones" / "M07-test.md"
        path.write_text(
            "# M07\n\n## Reviewers\n\n" + "\n".join(prose)
            + "\n\n## Work log\n\n- 2026-07-01: one\n"
        )
        ctx = self.inject()
        self.assertIn("reviewer-000", ctx)
        self.assertIn("reviewer-039", ctx)

    def test_a_fenced_heading_is_content_not_a_section(self):
        # M45's rule: a `## Work log` quoted inside a fence is content. Left
        # unhandled it counted as a real section, diluting the real one's share
        # of the budget and letting a marker land inside the code fence.
        example = [f"- YYYY-MM-{i:02d}: example-{i:03d} " + "e" * 300
                   for i in range(40)]
        path = self.root / "cairn" / "milestones" / "M07-test.md"
        path.write_text(
            "# M07\n\n## Scope\n\n```markdown\n## Work log\n\n"
            + "\n".join(example) + "\n```\n\n"
            "## Work log\n\n- 2026-07-01: real-entry\n"
        )
        ctx = self.inject()
        fenced = ctx.split("```markdown\n")[1].split("\n```")[0]
        self.assertIn("example-000", fenced)
        self.assertNotIn("_cairn:", fenced)
        self.assertIn("real-entry", ctx)

    def test_hard_truncation_is_marked_never_silent(self):
        # ROADMAP alone over budget: nothing else can be shed, so the cut
        # must announce itself (M100 — an enforcement path fails loud).
        rows = "\n".join(
            f"| M{i:03d} | {'t' * 400} | done | — | high | milestones/archive/x.md |"
            for i in range(120)
        )
        (self.root / "cairn" / "ROADMAP.md").write_text(
            "# Roadmap\n\n| ID | Title | Status | Depends on | Priority | File/Archive |\n"
            "|---|---|---|---|---|---|\n" + rows + "\n"
        )
        ctx = self.inject()
        self.assertIn("ROADMAP truncated", ctx)
        self.assertIn("read cairn/ROADMAP.md for the rest", ctx)
        self.assertLessEqual(len(ctx), 30000)


class TestExemptSetMirror(unittest.TestCase):
    """RR08 §BC2 / M119: the hook's `CAP_EXEMPT_SECTIONS` and the cap counters'
    effective exempt set are two encodings of one fact, and nothing but this
    test holds them together — a hook may import only `cairn_common`, so no
    shared constant is reachable across the two packages.

    The failure it exists to catch is silent and one-directional in effect: a
    heading the cap exempts but the hook does not recognize is injected WHOLE,
    which is exactly the unbounded read D-063 added the bound to close. So the
    assert is equality, never containment — it must red whichever side drifts.
    """

    def setUp(self):
        scripts = HOOKS_DIR.parent / "scripts"
        for d in (HOOKS_DIR, scripts):
            sys.path.insert(0, str(d))
            self.addCleanup(sys.path.remove, str(d))
        import cairn_scripts
        import session_context

        self.cs = cairn_scripts
        self.sc = session_context

    def test_the_two_encodings_name_the_same_set(self):
        self.assertEqual(
            set(self.sc.CAP_EXEMPT_SECTIONS),
            set(self.cs.CAP_EXEMPT_SECTIONS),
            "the hook's cap-exempt set and the counters' have drifted apart",
        )

    def test_neither_side_is_empty(self):
        # Non-vacuity: two empty tuples are equal, so the assert above would be
        # satisfied by an import that silently produced nothing. Three members
        # since M118; the count is pinned so a member vanishing from BOTH sides
        # at once — the one drift equality cannot see — still reds.
        self.assertEqual(len(set(self.sc.CAP_EXEMPT_SECTIONS)), 3)
        self.assertEqual(len(set(self.cs.CAP_EXEMPT_SECTIONS)), 3)

    def test_the_counters_effective_set_is_what_the_constant_claims(self):
        # The constant is only worth comparing if it describes what the scan
        # actually does. `## Review` leaves by the body boundary and the other
        # two by subtraction, so a constant-only test would pass over a counter
        # that had stopped exempting one of them. This drives the real scan: a
        # file whose every section is exempt must count only its preamble, and
        # the trimmable breakdown must name nothing.
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "M01-all-exempt.md"
            preamble = "# M01: Title\n\n- **Status:** planned\n"
            body = "".join(
                f"## {h.title()}\nline\nline\n" for h in self.cs.CAP_EXEMPT_SECTIONS
            )
            path.write_text(preamble + body)
            self.assertEqual(
                self.cs.milestone_body_line_count(str(path)),
                len(preamble.splitlines()),
                "a section the constant calls exempt is still being counted",
            )
            self.assertEqual(self.cs.milestone_section_line_counts(str(path)), [])

    def test_a_section_outside_the_set_is_still_counted(self):
        # The positive control. Without it the test above is satisfied by a
        # counter that exempts everything, which would report every milestone
        # as three lines long and never fail the cap.
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "M01-scoped.md"
            path.write_text("# M01: Title\n\n## Scope\nline\nline\n## Work Log\nline\n")
            self.assertEqual(self.cs.milestone_body_line_count(str(path)), 5)
            self.assertEqual(
                [h for h, _ in self.cs.milestone_section_line_counts(str(path))],
                ["Scope"],
            )


class TestHeadingNormalizationContract(unittest.TestCase):
    """M122: the hook and the cap counters must classify a HEADING identically.

    `TestExemptSetMirror` above holds the two `CAP_EXEMPT_SECTIONS` constants
    equal. The constants can agree while the normalization applied to a heading
    *before* it is looked up in them diverges, and that gap was live: measured
    2026-07-30, dropping `.strip()` from `session_context.heading_name` left all
    98 hooks tests green while `##  Work log` (two spaces) and `## Work log `
    (trailing space) went on being cap-exempt to the counters and started being
    injected WHOLE by the hook — M113's original bug on a second axis. Only the
    hook's half of the verdict moves under that mutation; the divergence is what
    the guard catches.

    Three verdicts per row, never two: the counters' (a real file through
    `cairn_scripts.milestone_body_line_count`), the hook's (a real injection
    through `session_context.milestone_part`), and the row's own EXPECTED
    verdict. The expected column is what makes this more than a differential —
    a drift hitting both layers identically satisfies equality alone, the same
    blindness `TestExemptSetMirror` pins its member count against.
    """

    # Strictly greater than session_context.MIN_TAIL_BLOCKS (= 3): at or below
    # it, `bounded_tail` never breaks, so NO budget elides and an exempt section
    # would report as non-exempt against perfectly correct code.
    ENTRIES = 8
    PREAMBLE = "# M07: Test milestone\n\n- **Status:** in-progress\n"
    RELPATH = "milestones/M07-test.md"

    # (heading, expected_exempt), covering two axes.
    # Format: case, a second space after the hashes, a trailing space.
    # Site: the counters normalize at TWO sites — `cairn_scripts.py:375-376`,
    # the `## Review` body boundary, and `:412`, the `EXEMPT_HEADINGS`
    # subtraction — and a work-log-only table never reaches the first
    # (the per-site axis M117 recorded). `## Review `
    # carries the whitespace axis TO the boundary site: every other whitespace
    # rendering lands at the subtraction site, which re-strips independently, so
    # without this row `cairn_scripts.py:375`'s own `.strip()` is unreachable
    # and drops green while the two layers disagree.
    # Controls: `## Reviewers` and `## Decisions notes` are prefix near misses —
    # a prefix must not read as its exempt namesake, the boundary bug M55 hit —
    # and `## Scope` is a plain plan-owned section, the case neither near miss
    # covers.
    TABLE = (
        ("## Work log", True),
        ("## Work Log", True),
        ("## WORK LOG", True),
        ("##  Work log", True),
        ("## Work log ", True),
        ("## Review", True),
        ("## REVIEW", True),
        ("## Review ", True),
        ("## Decisions", True),
        ("##  Decisions", True),
        ("## Reviewers", False),
        ("## Decisions notes", False),
        ("## Scope", False),
        # Prefix and leading-whitespace renderings: `## ` is a normalization
        # step like `.strip()` and `.lower()`, and it was unpinned on BOTH
        # layers until these two rows (review F1/F2). Neither is a heading to
        # either layer today; each diverges the moment one layer's prefix
        # handling moves — loosening `startswith("## ")` to `startswith("##")`
        # makes `### Work log` exempt to that layer alone, and an `lstrip()`
        # added ahead of the check does the same for `  ## Work log`.
        ("### Work log", False),
        ("  ## Work log", False),
    )

    def setUp(self):
        scripts = HOOKS_DIR.parent / "scripts"
        for d in (HOOKS_DIR, scripts):
            sys.path.insert(0, str(d))
            self.addCleanup(sys.path.remove, str(d))
        import cairn_scripts
        import session_context

        self.cs = cairn_scripts
        self.sc = session_context

    def body(self, heading):
        entries = "".join(
            f"- 2026-07-30: entry-{i:03d} " + "x" * 200 + "\n"
            for i in range(self.ENTRIES)
        )
        return self.PREAMBLE + heading + "\n" + entries

    def counters_exempt(self, heading):
        """The cap counters' verdict, driven through the real counter over a
        real file: a section the cap exempts contributes nothing to the
        plan-owned body, so the count falls back to the preamble alone."""
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "M07-test.md"
            path.write_text(self.body(heading))
            count = self.cs.milestone_body_line_count(str(path))
        return count == len(self.PREAMBLE.splitlines()), count

    def hook_exempt(self, heading):
        """The hook's verdict, driven through the real injection path: only a
        cap-exempt section is bounded, and a bounded one says what it elided."""
        part = self.sc.milestone_part(
            "M07", "in-progress", self.RELPATH, self.body(heading), 0
        )
        return "_cairn:" in part, part

    def test_the_two_layers_and_the_expected_verdict_agree_on_every_rendering(self):
        for heading, expected in self.TABLE:
            with self.subTest(heading=heading):
                counted, count = self.counters_exempt(heading)
                marked, part = self.hook_exempt(heading)
                self.assertEqual(
                    counted, expected,
                    f"the cap counters classify {heading!r} wrongly (count {count})",
                )
                self.assertEqual(
                    marked, expected,
                    f"the hook classifies {heading!r} wrongly",
                )
                # Each verdict pairs with a positive signal that the path ran:
                # an absence assert alone is satisfied by a helper that returned
                # nothing at all.
                if expected:
                    self.assertIn("entry-007", part)
                    self.assertNotIn("entry-000", part)
                else:
                    self.assertEqual(
                        count,
                        len(self.PREAMBLE.splitlines()) + 1 + self.ENTRIES,
                    )
                    self.assertIn("entry-000", part)
                    self.assertIn("entry-007", part)

    def test_the_table_exercises_both_verdicts_on_both_layers(self):
        # Non-vacuity, over the OBSERVED verdicts and never the expected
        # column: a table that drifted to one outcome would leave the agreement
        # test above satisfied by a classifier that answers the same way to
        # everything. Both directions, because either half alone leaves the
        # other unproven.
        counters = [self.counters_exempt(h)[0] for h, _ in self.TABLE]
        hook = [self.hook_exempt(h)[0] for h, _ in self.TABLE]
        for label, observed in (("counters", counters), ("hook", hook)):
            self.assertIn(True, observed, f"{label}: no exempt verdict observed")
            self.assertIn(False, observed, f"{label}: no capped verdict observed")

    def test_the_table_still_carries_every_rendering_the_contract_needs(self):
        # Coverage of the table itself, kept apart from the non-vacuity assert
        # above on purpose, and pinned as ONE equality rather than a membership
        # loop: a loop over a hand-written copy of `TABLE` is synced by hand, so
        # deleting a rendering from both places reds nothing and adding one to
        # `TABLE` alone leaves it unpinned (review F3). Order and length ride
        # along, which is what makes an addition red until it is declared here.
        # Raw strings on purpose — normalizing would route the table's own
        # coverage through `heading_name`, the function under test, and a hook
        # mutation would then report as a table defect.
        self.assertEqual(
            [h for h, _ in self.TABLE],
            [
                # format axis
                "## Work log", "## Work Log", "## WORK LOG",
                "##  Work log", "## Work log ",
                # site axis: `review` leaves by the body boundary, `work log`
                # and `decisions` by subtraction, so a work-log-only table
                # exercises one site and reads as full coverage. `## Review `
                # carries whitespace to the boundary site.
                "## Review", "## REVIEW", "## Review ",
                "## Decisions", "##  Decisions",
                # controls
                "## Reviewers", "## Decisions notes", "## Scope",
                # prefix / leading whitespace
                "### Work log", "  ## Work log",
            ],
        )

    def fenced_body(self, opener):
        """A milestone quoting a cap-exempt heading inside a fence, above its
        own real one. Both blocks are long, so a layer that mistakes the quoted
        heading for a section bounds it and gives itself away."""
        quoted = "".join(
            f"- 2026-07-01: quoted-{i:03d} " + "q" * 200 + "\n"
            for i in range(self.ENTRIES)
        )
        real = "".join(
            f"- 2026-07-30: entry-{i:03d} " + "x" * 200 + "\n"
            for i in range(self.ENTRIES)
        )
        return (
            self.PREAMBLE
            + "## Scope\n"
            + f"{opener}markdown\n## Work log\n{quoted}{opener}\n"
            + "## Work log\n"
            + real
        )

    def test_a_heading_quoted_inside_a_fence_is_content_on_both_layers(self):
        # The fence axis of the same contract (M45): both layers track ``` and
        # ~~~, and a heading quoted inside either is content, never a section
        # boundary. Measured 2026-07-30: dropping the hook's `~~~` support left
        # all 101 tests of the then-current file green, because every fence
        # fixture in it used backticks — the same one-rendering blindness the
        # format axis had.
        for opener in ("```", "~~~"):
            with self.subTest(fence=opener):
                body = self.fenced_body(opener)
                with tempfile.TemporaryDirectory() as tmp:
                    path = pathlib.Path(tmp) / "M07-test.md"
                    path.write_text(body)
                    named = [
                        h for h, _ in self.cs.milestone_section_line_counts(str(path))
                    ]
                    counted = self.cs.milestone_body_line_count(str(path))
                self.assertEqual(
                    named, ["Scope"],
                    "the counters split on a heading quoted inside a fence",
                )
                # The count, not just the section list: a quoted heading the
                # counters mistake for a section is SUBTRACTED as cap-exempt, so
                # it never shows up in `named` — only the arithmetic gives it
                # away. Everything but the real work log (its heading + entries)
                # is plan-owned.
                self.assertEqual(
                    counted, len(body.splitlines()) - (1 + self.ENTRIES),
                    "the counters subtracted a work log quoted inside a fence",
                )
                part = self.sc.milestone_part(
                    "M07", "in-progress", self.RELPATH, body, 0
                )
                self.assertEqual(
                    part.count("_cairn:"), 1,
                    "the hook bounded a heading quoted inside a fence",
                )
                self.assertIn("quoted-000", part)
                self.assertIn("entry-007", part)
                self.assertNotIn("entry-000", part)

    def test_the_fixture_is_large_enough_for_a_bound_to_show(self):
        # AC1's fixture clause, pinned rather than asserted in prose: at or below
        # MIN_TAIL_BLOCKS, `bounded_tail` never breaks, so no budget elides and
        # every exempt row would report as non-exempt against correct code.
        self.assertGreater(self.ENTRIES, self.sc.MIN_TAIL_BLOCKS)


class TestBoundedTail(unittest.TestCase):
    """Direct-import tests for the read-bound's pure helpers.

    The subprocess rule above exists for the hook CONTRACT — the shape of the
    JSON it prints. These are pure functions with no contract to get wrong,
    and driving `budget` to a specific value through a whole repo fixture
    would test the allocator instead of the bound.
    """

    def setUp(self):
        sys.path.insert(0, str(HOOKS_DIR))
        import session_context

        self.sc = session_context
        self.addCleanup(sys.path.remove, str(HOOKS_DIR))

    def section(self, n=40, width=280):
        return [""] + [
            f"- 2026-07-01: entry-{i:03d} " + "e" * width for i in range(n)
        ]

    def test_the_newest_entries_survive_however_tight_the_budget(self):
        # Review round 2: a line-level second pass undid the entry floor, so
        # at budget 100-304 the section showed ZERO entries and reported
        # "newest 1 of 42 lines shown" — the shown line being blank. Entry
        # count must never fall as the budget rises, and never below the floor.
        seen = []
        for budget in (0, 100, 304, 610, 1000, 6000):
            kept, _, _, _, _ = self.sc.bounded_tail(self.section(), budget)
            seen.append(sum(1 for line in kept if line.startswith("- ")))
        self.assertEqual(seen, sorted(seen), f"entry count fell: {seen}")
        self.assertGreaterEqual(min(seen), self.sc.MIN_TAIL_BLOCKS)

    def test_prose_above_the_first_entry_is_charged_and_reported(self):
        lines = [f"paragraph-{i}" + "p" * 400 for i in range(40)] + ["- newest"]
        kept, _, _, _, cut_head = self.sc.bounded_tail(lines, 6000)
        self.assertTrue(cut_head)
        self.assertNotIn("paragraph-0" + "p" * 400, kept)
        self.assertIn("- newest", kept)

    def test_a_blank_only_head_is_not_reported_as_elided_prose(self):
        _, _, _, _, cut_head = self.sc.bounded_tail(self.section(n=2), 10)
        self.assertFalse(cut_head)

    def test_degenerate_sections_round_trip(self):
        for lines in ([], [""], ["   "], ["- only"]):
            with self.subTest(lines=lines):
                kept, k, t, _, _ = self.sc.bounded_tail(lines, 6000)
                self.assertLessEqual(k, t)
                self.assertEqual(kept, lines)


class TestStopGuard(RepoFixture):
    def test_blocks_on_dirty_tracking(self):
        (self.root / "cairn" / "ROADMAP.md").write_text(ROADMAP + "edited\n")
        proc = run_hook("stop_guard.py", self.payload(stop_hook_active=False))
        self.assertEqual(proc.returncode, 0)
        out = hook_toplevel(proc)
        # block MUST be top-level, not nested (a nested decision no-ops live)
        self.assertNotIn("hookSpecificOutput", out)
        self.assertEqual(out["decision"], "block")
        self.assertIn("cairn/ROADMAP.md", out["reason"])

    def test_blocks_on_untracked_tracking_file(self):
        (self.root / "cairn" / "milestones" / "M99-new.md").write_text("draft\n")
        out = hook_toplevel(run_hook("stop_guard.py", self.payload()))
        self.assertEqual(out["decision"], "block")
        self.assertIn("M99-new.md", out["reason"])

    def test_passes_on_clean_tree(self):
        proc = run_hook("stop_guard.py", self.payload(stop_hook_active=False))
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")

    def test_dirty_code_outside_cairn_passes(self):
        (self.root / "code.txt").write_text("changed\n")
        proc = run_hook("stop_guard.py", self.payload())
        self.assertEqual(proc.stdout.strip(), "")

    def test_stop_hook_active_never_reblocks(self):
        (self.root / "cairn" / "ROADMAP.md").write_text(ROADMAP + "edited\n")
        proc = run_hook("stop_guard.py", self.payload(stop_hook_active=True))
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")

    def test_merge_marker_alone_never_blocks(self):
        # The ephemeral approval marker must not block turn-end even when it
        # is NOT gitignored (a repo that adopted the workflow without
        # re-running /cairn-init) — otherwise the user is tempted to commit it.
        (self.root / "cairn" / ".merge-approved").write_text("M07 approved 2026-07-11\n")
        proc = run_hook("stop_guard.py", self.payload())
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "", "marker alone must not block")

    def test_marker_does_not_mask_other_dirty_tracking(self):
        (self.root / "cairn" / ".merge-approved").write_text("x\n")
        (self.root / "cairn" / "ROADMAP.md").write_text(ROADMAP + "edited\n")
        out = hook_toplevel(run_hook("stop_guard.py", self.payload()))
        self.assertEqual(out["decision"], "block")
        self.assertIn("cairn/ROADMAP.md", out["reason"])
        self.assertNotIn(".merge-approved", out["reason"])


class TestMergeGuard(RepoFixture):
    def merge_payload(self, command, **extra):
        return self.payload(
            hook_event_name="PreToolUse",
            tool_name="Bash",
            tool_input={"command": command},
            **extra,
        )

    def marker(self):
        return self.root / "cairn" / ".merge-approved"

    def test_denies_gh_pr_merge_without_marker(self):
        proc = run_hook("merge_guard.py", self.merge_payload("gh pr merge 7 --squash"))
        self.assertEqual(proc.returncode, 0)
        out = hook_json(proc)
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertIn("approval", out["permissionDecisionReason"])

    def test_allows_and_consumes_marker(self):
        self.marker().write_text("M07 approved 2026-07-11\n")
        proc = run_hook("merge_guard.py", self.merge_payload("gh pr merge 7 --squash"))
        self.assertEqual(proc.stdout.strip(), "")
        self.assertFalse(self.marker().exists(), "marker must be single-use")
        # consumption is a rename, not a delete: merge_guard_post resolves
        # the pending file by outcome (restore on failure, delete on success)
        pending = self.root / "cairn" / ".merge-approved.pending"
        self.assertEqual(
            pending.read_text(), "M07 approved 2026-07-11\n",
            "consumed marker must move to .pending intact",
        )

    # --- PR binding (M72): the marker names the PR it approves ---

    APPROVAL_PR7 = "M72 approved 2026-07-18 for PR #7\n"

    def test_denies_merge_of_a_pr_the_marker_does_not_name(self):
        self.marker().write_text(self.APPROVAL_PR7)
        out = hook_json(
            run_hook("merge_guard.py", self.merge_payload("gh pr merge 9 --squash"))
        )
        self.assertEqual(out["permissionDecision"], "deny")
        reason = out["permissionDecisionReason"]
        self.assertIn("#7", reason, "deny reason must name the approved PR")
        self.assertIn("#9", reason, "deny reason must name the attempted PR")
        self.assertEqual(
            self.marker().read_text(), self.APPROVAL_PR7,
            "a denied merge must not consume the approval",
        )

    def test_denies_bare_merge_that_names_no_pr(self):
        self.marker().write_text(self.APPROVAL_PR7)
        out = hook_json(
            run_hook(
                "merge_guard.py",
                self.merge_payload("gh pr merge --squash --delete-branch"),
            )
        )
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertIn("does not name a PR", out["permissionDecisionReason"])
        self.assertEqual(
            self.marker().read_text(), self.APPROVAL_PR7,
            "a denied merge must not consume the approval",
        )

    def test_allows_and_consumes_when_pr_matches(self):
        self.marker().write_text(self.APPROVAL_PR7)
        proc = run_hook(
            "merge_guard.py",
            self.merge_payload("gh pr merge 7 --squash --delete-branch"),
        )
        self.assertEqual(proc.stdout.strip(), "")
        self.assertFalse(self.marker().exists())
        pending = self.root / "cairn" / ".merge-approved.pending"
        self.assertEqual(pending.read_text(), self.APPROVAL_PR7)

    def test_pr_number_survives_url_and_value_flags(self):
        for command in (
            "gh pr merge https://github.com/o/r/pull/7 --squash",
            'gh pr merge --subject "fix issue 9" 7 --squash',
            "gh pr merge -t 'bump to 9' 7",
        ):
            with self.subTest(command=command):
                self.marker().write_text(self.APPROVAL_PR7)
                proc = run_hook("merge_guard.py", self.merge_payload(command))
                self.assertEqual(proc.stdout.strip(), "", command)
                (self.root / "cairn" / ".merge-approved.pending").unlink()

    def test_branch_name_argument_is_treated_as_naming_no_pr(self):
        # `gh pr merge <branch>` is legal but the guard cannot resolve a
        # branch to a PR offline — it must deny, not guess.
        self.marker().write_text(self.APPROVAL_PR7)
        out = hook_json(
            run_hook(
                "merge_guard.py", self.merge_payload("gh pr merge m72-branch --squash")
            )
        )
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertTrue(self.marker().exists())

    def test_chained_merge_cannot_ride_on_the_first_approval(self):
        # M72 review F4: checking only the first `gh pr merge` let a second,
        # unapproved merge through on the strength of the first.
        self.marker().write_text(self.APPROVAL_PR7)
        out = hook_json(
            run_hook(
                "merge_guard.py",
                self.merge_payload(
                    "gh pr merge 7 --squash && gh pr merge 9 --squash"
                ),
            )
        )
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertIn("#9", out["permissionDecisionReason"])
        self.assertEqual(self.marker().read_text(), self.APPROVAL_PR7)

    def test_chained_bare_merge_is_denied_too(self):
        # The same bypass against the deny-on-unnamed rule.
        self.marker().write_text(self.APPROVAL_PR7)
        out = hook_json(
            run_hook(
                "merge_guard.py",
                self.merge_payload("gh pr merge 7 --squash && gh pr merge --squash"),
            )
        )
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertIn("does not name a PR", out["permissionDecisionReason"])
        self.assertEqual(self.marker().read_text(), self.APPROVAL_PR7)

    def test_repeated_merge_of_the_approved_pr_still_allowed(self):
        # Not every chain is an escape: the same approved PR twice is odd
        # but authorized, and must not be denied by the multi-occurrence
        # check (guards against over-correcting F4 into a false positive).
        self.marker().write_text(self.APPROVAL_PR7)
        proc = run_hook(
            "merge_guard.py",
            self.merge_payload("gh pr merge 7 --squash || gh pr merge 7 --admin"),
        )
        self.assertEqual(proc.stdout.strip(), "")

    def test_unrelated_reference_in_the_marker_label_is_not_the_pr(self):
        # M72 review F1: a first-match regex read the label's issue number
        # instead of the approved PR, denying the approved merge (and, with
        # the numbers reversed, authorizing an unapproved one).
        self.marker().write_text(
            "hotfix #43-null-deref approved 2026-07-18 for PR #70\n"
        )
        proc = run_hook("merge_guard.py", self.merge_payload("gh pr merge 70 --squash"))
        self.assertEqual(proc.stdout.strip(), "", "approved merge must not be denied")
        self.assertFalse(self.marker().exists())

    def test_unrelated_reference_cannot_authorize_an_unapproved_merge(self):
        self.marker().write_text("hotfix #70-crash approved 2026-07-18 for PR #71\n")
        out = hook_json(
            run_hook("merge_guard.py", self.merge_payload("gh pr merge 70 --squash"))
        )
        self.assertEqual(out["permissionDecision"], "deny")
        self.assertIn("#71", out["permissionDecisionReason"])

    def test_repo_flag_value_is_not_mistaken_for_the_pr(self):
        # M72 review F2 (--repo/-R take a value) and F5 (-m is boolean).
        for command in (
            "gh pr merge --repo jmgirard/cairn 7 --squash",
            "gh pr merge -R jmgirard/cairn 7 --squash",
            "gh pr merge -m 7",
        ):
            with self.subTest(command=command):
                self.marker().write_text(self.APPROVAL_PR7)
                proc = run_hook("merge_guard.py", self.merge_payload(command))
                self.assertEqual(proc.stdout.strip(), "", command)
                (self.root / "cairn" / ".merge-approved.pending").unlink()

    def test_git_merge_is_exempt_from_the_pr_check(self):
        # A `git merge` has no PR to name; the marker's existence governs it.
        self.marker().write_text(self.APPROVAL_PR7)
        proc = run_hook("merge_guard.py", self.merge_payload("git merge m72-branch"))
        self.assertEqual(proc.stdout.strip(), "")
        self.assertFalse(self.marker().exists(), "marker is still single-use")

    def test_denies_git_merge_while_on_main(self):
        out = hook_json(
            run_hook("merge_guard.py", self.merge_payload("git merge m07-branch"))
        )
        self.assertEqual(out["permissionDecision"], "deny")

    def test_allows_syncing_main_into_feature_branch(self):
        self.git("checkout", "-q", "-b", "m07-feature")
        proc = run_hook("merge_guard.py", self.merge_payload("git merge main"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_allows_merge_housekeeping(self):
        proc = run_hook("merge_guard.py", self.merge_payload("git merge --abort"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_ignores_non_merge_and_lookalike_commands(self):
        for cmd in ("git status", "git merge-base main HEAD", "echo git merge"):
            with self.subTest(cmd=cmd):
                proc = run_hook("merge_guard.py", self.merge_payload(cmd))
                self.assertEqual(proc.stdout.strip(), "", cmd)

    def test_ignores_other_tools(self):
        proc = run_hook(
            "merge_guard.py",
            self.payload(tool_name="Edit", tool_input={"file_path": "x"}),
        )
        self.assertEqual(proc.stdout.strip(), "")


class TestMergeGuardPost(RepoFixture):
    """The PostToolUse/PostToolUseFailure companion (M60). For Bash, a
    nonzero exit fires PostToolUseFailure and PostToolUse fires only on
    success (official hooks docs; references/claude-code-hooks.md) — so
    the hook keys on the event name, never an exit-code field."""

    APPROVAL = "M07 approved 2026-07-11\n"

    def post_payload(self, command, event="PostToolUseFailure", **extra):
        return self.payload(
            hook_event_name=event,
            tool_name="Bash",
            tool_input={"command": command},
            **extra,
        )

    def marker(self):
        return self.root / "cairn" / ".merge-approved"

    def pending(self):
        return self.root / "cairn" / ".merge-approved.pending"

    def test_failure_restores_consumed_marker(self):
        self.pending().write_text(self.APPROVAL)
        proc = run_hook(
            "merge_guard_post.py",
            self.post_payload("gh pr merge 7 --squash"),
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(self.marker().read_text(), self.APPROVAL,
                         "failed attempt must restore the marker intact")
        self.assertFalse(self.pending().exists())
        out = hook_json(proc)
        self.assertEqual(out["hookEventName"], "PostToolUseFailure")
        self.assertIn("restored", out["additionalContext"])

    def test_success_deletes_pending_marker_stays_consumed(self):
        self.pending().write_text(self.APPROVAL)
        proc = run_hook(
            "merge_guard_post.py",
            self.post_payload("gh pr merge 7 --squash", event="PostToolUse"),
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")
        self.assertFalse(self.marker().exists(),
                         "a successful merge's approval stays consumed")
        self.assertFalse(self.pending().exists())

    def test_never_mints_without_pending(self):
        # No pending file (no real approval was consumed): a failed guarded
        # merge must NOT create a marker out of thin air.
        proc = run_hook(
            "merge_guard_post.py",
            self.post_payload("gh pr merge 7 --squash"),
        )
        self.assertEqual(proc.stdout.strip(), "")
        self.assertFalse(self.marker().exists(), "must never mint approval")

    def test_noop_on_non_merge_commands(self):
        self.pending().write_text(self.APPROVAL)
        for cmd in ("git status", "git merge --abort", "echo gh pr merge"):
            for event in ("PostToolUse", "PostToolUseFailure"):
                with self.subTest(cmd=cmd, event=event):
                    proc = run_hook(
                        "merge_guard_post.py",
                        self.post_payload(cmd, event=event),
                    )
                    self.assertEqual(proc.stdout.strip(), "")
        self.assertTrue(self.pending().exists(),
                        "non-merge commands must not touch the pending file")
        self.assertFalse(self.marker().exists())

    def test_noop_on_other_events_and_tools(self):
        self.pending().write_text(self.APPROVAL)
        proc = run_hook(
            "merge_guard_post.py",
            self.post_payload("gh pr merge 7", event="PreToolUse"),
        )
        self.assertEqual(proc.stdout.strip(), "")
        proc = run_hook(
            "merge_guard_post.py",
            self.payload(
                hook_event_name="PostToolUseFailure",
                tool_name="Edit",
                tool_input={"file_path": "x"},
            ),
        )
        self.assertEqual(proc.stdout.strip(), "")
        self.assertTrue(self.pending().exists())

    def test_failed_git_merge_on_main_restores(self):
        # the git-merge form of a guarded merge (sitting on main)
        self.pending().write_text(self.APPROVAL)
        proc = run_hook(
            "merge_guard_post.py",
            self.post_payload("git merge m07-branch"),
        )
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(self.marker().exists())

    def test_stop_guard_ignores_pending_marker(self):
        # the transient pending state must not block turn-end, marker-style
        self.pending().write_text(self.APPROVAL)
        proc = run_hook("stop_guard.py", self.payload())
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "",
                         "pending marker alone must not block")


class TestForcePushGuard(RepoFixture):
    def push_payload(self, command, **extra):
        return self.payload(
            hook_event_name="PreToolUse",
            tool_name="Bash",
            tool_input={"command": command},
            **extra,
        )

    def assert_denied(self, command):
        proc = run_hook("force_push_guard.py", self.push_payload(command))
        self.assertEqual(proc.returncode, 0)
        out = hook_json(proc)
        self.assertEqual(out["permissionDecision"], "deny", command)
        self.assertIn("force-push", out["permissionDecisionReason"])

    def assert_passes(self, command):
        proc = run_hook("force_push_guard.py", self.push_payload(command))
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "", command)

    def test_denies_force_flag_variants_to_default(self):
        # explicit-ref form: every force spelling, either flag order
        for cmd in (
            "git push --force origin main",
            "git push -f origin main",
            "git push origin main --force",
            "git push --force-with-lease origin main",
            "git push --force-with-lease=main:abc123 origin main",
            "git push --force-if-includes --force-with-lease origin main",
            "git push -uf origin main",
        ):
            with self.subTest(cmd=cmd):
                self.assert_denied(cmd)

    def test_denies_plus_refspec_force_syntax(self):
        # the flagless force form; also qualified and src:dst spellings
        for cmd in (
            "git push origin +main",
            "git push origin +refs/heads/main",
            "git push -f origin feature:main",
            "git push -f origin HEAD:main",
        ):
            with self.subTest(cmd=cmd):
                self.assert_denied(cmd)

    def test_denies_on_default_branch_form(self):
        # no refspec: the push targets the branch we're sitting on
        self.assert_denied("git push --force")
        self.assert_denied("git push -f origin")
        self.assert_denied("git push -f origin HEAD")

    def test_passes_feature_branch_force_pushes(self):
        for cmd in (
            "git push -f origin m07-feature",
            "git push --force-with-lease origin m07-feature",
            "git push origin +m07-feature",
            "git push -f origin fix:renamed-fix",
        ):
            with self.subTest(cmd=cmd):
                self.assert_passes(cmd)

    def test_passes_on_feature_branch_no_refspec_form(self):
        self.git("checkout", "-q", "-b", "m07-feature")
        self.assert_passes("git push --force")
        self.assert_passes("git push -f origin HEAD")

    def test_passes_plain_pushes_and_non_push(self):
        for cmd in (
            "git push origin main",
            "git push -u origin main",
            "git push",
            "echo git push --force origin main",
            "git pushx --force origin main",
            "git status",
        ):
            with self.subTest(cmd=cmd):
                self.assert_passes(cmd)

    def test_default_branch_resolved_via_remote_head(self):
        # default branch `trunk` advertised via refs/remotes/origin/HEAD:
        # force-pushing trunk is denied, and `main` (now just a feature
        # name) passes — detection, not hardcoding (commit_guard's fixture).
        bare = tempfile.TemporaryDirectory()
        self.addCleanup(bare.cleanup)
        subprocess.run(
            ["git", "init", "-q", "--bare", bare.name],
            check=True, capture_output=True,
        )
        self.git("branch", "-m", "trunk")
        self.git("remote", "add", "origin", bare.name)
        self.git("push", "-q", "-u", "origin", "trunk")
        self.git("remote", "set-head", "origin", "trunk")
        self.assert_denied("git push --force origin trunk")
        self.assert_passes("git push --force origin main")

    def test_compound_command_push_segment_is_caught(self):
        self.assert_denied("git fetch && git push --force origin main")

    def test_subshell_wrapped_force_push_is_caught(self):
        # M60 review F4a: `)` must end the span, not glue onto the refspec
        self.assert_denied("(git push -f origin main)")

    def test_separate_value_flag_never_invents_a_deny(self):
        # M60 review F4b: -o's value token is not a refspec — this is a
        # feature-branch force-push and must pass
        self.assert_passes("git push -f origin my-feature -o main")
        self.assert_denied("git push -f origin main -o ci.skip")

    def test_ignores_other_tools(self):
        proc = run_hook(
            "force_push_guard.py",
            self.payload(tool_name="Edit", tool_input={"file_path": "x"}),
        )
        self.assertEqual(proc.stdout.strip(), "")


class TestMemoryGuard(RepoFixture):
    # A per-user memory path (independent of the repo) that should trip the
    # guard when cwd is a cairn repo.
    MEMORY_PATH = "/home/u/.claude/projects/-home-u-proj/memory/note.md"

    def write_payload(self, file_path, **extra):
        return self.payload(
            hook_event_name="PreToolUse",
            tool_name="Write",
            tool_input={"file_path": file_path},
            **extra,
        )

    def test_nudges_on_memory_write_in_cairn_repo(self):
        proc = run_hook("memory_guard.py", self.write_payload(self.MEMORY_PATH))
        self.assertEqual(proc.returncode, 0)
        out = hook_json(proc)
        self.assertEqual(out["hookEventName"], "PreToolUse")
        self.assertIn("GP4", out["additionalContext"])
        # Softest non-blocking lever: additionalContext with NO
        # permissionDecision, so the Write is neither blocked, asked, nor
        # force-allowed — the normal permission flow is untouched.
        self.assertNotIn("permissionDecision", out)

    def test_silent_on_non_memory_path(self):
        proc = run_hook(
            "memory_guard.py",
            self.write_payload(str(self.root / "cairn" / "note.md")),
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")

    def test_silent_on_memory_lookalike_without_memory_segment(self):
        # .claude/projects/<slug>/ but not under memory/ — must not fire.
        proc = run_hook(
            "memory_guard.py",
            self.write_payload("/home/u/.claude/projects/-home-u-proj/todo.md"),
        )
        self.assertEqual(proc.stdout.strip(), "")

    def test_silent_on_non_write_tool(self):
        proc = run_hook(
            "memory_guard.py",
            self.payload(
                tool_name="Edit", tool_input={"file_path": self.MEMORY_PATH}
            ),
        )
        self.assertEqual(proc.stdout.strip(), "")


class TestIdeaGuard(RepoFixture):
    """The chip is paired with a candidate row, never blocked (D-042)."""

    CHIP_TOOL = "mcp__ccd_session__spawn_task"

    def chip_payload(self, tool_name, **extra):
        return self.payload(
            hook_event_name="PreToolUse",
            tool_name=tool_name,
            tool_input={"title": "Fix the thing", "prompt": "..."},
            **extra,
        )

    def test_nudges_on_chip_creation_in_cairn_repo(self):
        proc = run_hook("idea_guard.py", self.chip_payload(self.CHIP_TOOL))
        self.assertEqual(proc.returncode, 0)
        out = hook_json(proc)
        self.assertEqual(out["hookEventName"], "PreToolUse")
        # The nudge must name the durable home it is redirecting toward,
        # not merely disapprove of the chip.
        self.assertIn("candidate", out["additionalContext"])
        self.assertIn("cairn/ROADMAP.md", out["additionalContext"])
        # Softest non-blocking lever (D-042 choice 4, D-017's shape): the
        # chip is created through the normal permission flow untouched.
        self.assertNotIn("permissionDecision", out)

    def test_fires_regardless_of_mcp_server_name(self):
        # The matcher is suffix-shaped so a server rename cannot silently
        # unwire the guard.
        proc = run_hook(
            "idea_guard.py", self.chip_payload("mcp__some_other_server__spawn_task")
        )
        self.assertIn("candidate", hook_json(proc)["additionalContext"])

    def test_silent_on_non_chip_tool(self):
        for tool in ("Write", "mcp__ccd_session__mark_chapter", "spawn_task"):
            with self.subTest(tool=tool):
                proc = run_hook("idea_guard.py", self.chip_payload(tool))
                self.assertEqual(proc.returncode, 0)
                self.assertEqual(proc.stdout.strip(), "")

    def test_silent_on_missing_tool_name(self):
        proc = run_hook("idea_guard.py", self.payload(hook_event_name="PreToolUse"))
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout.strip(), "")


class TestCommitGuard(RepoFixture):
    def commit_payload(self, command, **extra):
        return self.payload(
            hook_event_name="PreToolUse",
            tool_name="Bash",
            tool_input={"command": command},
            **extra,
        )

    def test_nudges_on_noncairn_commit_on_default(self):
        (self.root / "code.txt").write_text("changed\n")
        self.git("add", "code.txt")
        proc = run_hook("commit_guard.py", self.commit_payload("git commit -m wip"))
        self.assertEqual(proc.returncode, 0)
        out = hook_json(proc)
        self.assertEqual(out["hookEventName"], "PreToolUse")
        self.assertIn("default branch", out["additionalContext"])
        # softest lever: additionalContext with NO permissionDecision
        self.assertNotIn("permissionDecision", out)

    def test_silent_on_cairn_only_commit(self):
        (self.root / "cairn" / "ROADMAP.md").write_text(ROADMAP + "edit\n")
        self.git("add", "cairn/ROADMAP.md")
        proc = run_hook("commit_guard.py", self.commit_payload("git commit -m track"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_silent_on_feature_branch(self):
        self.git("checkout", "-q", "-b", "m99-feature")
        (self.root / "code.txt").write_text("changed\n")
        self.git("add", "code.txt")
        proc = run_hook("commit_guard.py", self.commit_payload("git commit -m wip"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_stage_all_counts_modified_tracked(self):
        # code.txt is modified but NOT staged; -am stages+commits it, so the
        # guard must count modified-tracked files, not just the (empty) index.
        (self.root / "code.txt").write_text("changed\n")
        proc = run_hook("commit_guard.py", self.commit_payload("git commit -am wip"))
        out = hook_json(proc)
        self.assertIn("default branch", out["additionalContext"])

    def test_unstaged_modified_ignored_without_dash_a(self):
        # same modified-not-staged file, but a plain commit only takes the
        # index — nothing non-cairn is staged, so stay silent.
        (self.root / "code.txt").write_text("changed\n")
        proc = run_hook("commit_guard.py", self.commit_payload("git commit -m wip"))
        self.assertEqual(proc.stdout.strip(), "")

    def test_command_position_and_non_commit_ignored(self):
        (self.root / "code.txt").write_text("changed\n")
        self.git("add", "code.txt")
        for cmd in ("echo git commit", "git status", "git commit-tree x"):
            with self.subTest(cmd=cmd):
                proc = run_hook("commit_guard.py", self.commit_payload(cmd))
                self.assertEqual(proc.stdout.strip(), "", cmd)

    def test_default_branch_resolved_via_remote_head(self):
        # A repo whose default branch is `trunk`, advertised through
        # refs/remotes/origin/HEAD — the guard must detect it (not hardcode
        # main/master) and nudge on a non-cairn commit made on trunk.
        bare = tempfile.TemporaryDirectory()
        self.addCleanup(bare.cleanup)
        subprocess.run(
            ["git", "init", "-q", "--bare", bare.name],
            check=True, capture_output=True,
        )
        self.git("branch", "-m", "trunk")
        self.git("remote", "add", "origin", bare.name)
        self.git("push", "-q", "-u", "origin", "trunk")
        self.git("remote", "set-head", "origin", "trunk")
        (self.root / "code.txt").write_text("changed\n")
        self.git("add", "code.txt")
        proc = run_hook("commit_guard.py", self.commit_payload("git commit -m wip"))
        out = hook_json(proc)
        self.assertIn("default branch", out["additionalContext"])

    def test_ignores_other_tools(self):
        proc = run_hook(
            "commit_guard.py",
            self.payload(tool_name="Edit", tool_input={"file_path": "x"}),
        )
        self.assertEqual(proc.stdout.strip(), "")


class TestNonCairnNoOp(RepoFixture):
    cairn = False

    def test_every_hook_is_silent_and_permissive(self):
        payloads = {
            "session_context.py": self.payload(hook_event_name="SessionStart"),
            "stop_guard.py": self.payload(),
            "merge_guard.py": self.payload(
                tool_name="Bash", tool_input={"command": "gh pr merge 7"}
            ),
            "merge_guard_post.py": self.payload(
                hook_event_name="PostToolUseFailure",
                tool_name="Bash",
                tool_input={"command": "gh pr merge 7"},
            ),
            "commit_guard.py": self.payload(
                tool_name="Bash", tool_input={"command": "git commit -m x"}
            ),
            "force_push_guard.py": self.payload(
                tool_name="Bash",
                tool_input={"command": "git push --force origin main"},
            ),
            # a genuine memory path: the ONLY reason to no-op here is the
            # non-cairn cwd, so this exercises that branch specifically.
            "memory_guard.py": self.payload(
                tool_name="Write",
                tool_input={
                    "file_path": "/home/u/.claude/projects/x/memory/n.md"
                },
            ),
            # a genuine chip tool name: the ONLY reason to no-op here is the
            # non-cairn cwd, so this exercises that branch specifically.
            "idea_guard.py": self.payload(
                tool_name="mcp__ccd_session__spawn_task",
                tool_input={"title": "Fix the thing"},
            ),
        }
        (self.root / "junk.txt").write_text("dirty\n")  # dirty tree, still no-op
        for script, payload in payloads.items():
            with self.subTest(script=script):
                proc = run_hook(script, payload)
                self.assertEqual(proc.returncode, 0)
                self.assertEqual(proc.stdout.strip(), "")
                self.assertEqual(proc.stderr.strip(), "")

    def test_garbage_stdin_is_permissive(self):
        for script in (
            "session_context.py",
            "stop_guard.py",
            "merge_guard.py",
            "merge_guard_post.py",
            "commit_guard.py",
            "force_push_guard.py",
            "memory_guard.py",
            "idea_guard.py",
        ):
            with self.subTest(script=script):
                proc = subprocess.run(
                    [sys.executable, str(HOOKS_DIR / script)],
                    input="not json{",
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                self.assertEqual(proc.returncode, 0)
                self.assertEqual(proc.stdout.strip(), "")


class TestHooksRegistration(unittest.TestCase):
    """hooks.json registers every guard with the python3/timeout envelope
    (M60 AC3). Hooks snapshot at process start, so a registration gap
    fails silently live — this is the mechanical check."""

    def setUp(self):
        self.config = json.loads((HOOKS_DIR / "hooks.json").read_text())["hooks"]

    def commands(self, event, matcher):
        return [
            h["command"]
            for entry in self.config.get(event, ())
            if entry.get("matcher", "*") == matcher or event == "SessionStart"
            for h in entry["hooks"]
        ]

    def test_force_push_guard_registered_pretooluse_bash(self):
        cmds = self.commands("PreToolUse", "Bash")
        self.assertTrue(
            any("force_push_guard.py" in c for c in cmds), cmds
        )

    def test_merge_guard_post_registered_on_both_post_events(self):
        # the outcome signal is the event name, so BOTH events are needed:
        # PostToolUse alone never restores; PostToolUseFailure alone never
        # finalizes a success
        for event in ("PostToolUse", "PostToolUseFailure"):
            with self.subTest(event=event):
                cmds = self.commands(event, "Bash")
                self.assertTrue(
                    any("merge_guard_post.py" in c for c in cmds), (event, cmds)
                )

    def test_idea_guard_registered_with_a_regex_mcp_matcher(self):
        matchers = [
            entry.get("matcher", "*")
            for entry in self.config.get("PreToolUse", ())
            if any("idea_guard.py" in h["command"] for h in entry["hooks"])
        ]
        self.assertEqual(len(matchers), 1, matchers)
        matcher = matchers[0]
        self.assertTrue(matcher.endswith("spawn_task"), matcher)
        # Documented matcher semantics (references/claude-code-hooks.md,
        # read out of binary 2.1.207): a matcher of only letters, digits,
        # `_`, `-`, spaces, `,` and `|` takes the LITERAL path — it is split
        # on `|`/`,` and each alternative is exact-matched, so `|` buys more
        # alternatives, never regex treatment. A bare
        # `mcp__ccd_session__spawn_task` would therefore wire the guard to one
        # server and silently miss a renamed one; only a metacharacter reaches
        # `new RegExp`. This asserts the matcher keeps one.
        self.assertRegex(matcher, r"[^\w\-, |]", matcher)

    def test_every_registered_hook_uses_the_standard_envelope(self):
        for event, entries in self.config.items():
            for entry in entries:
                for h in entry["hooks"]:
                    with self.subTest(event=event, command=h.get("command")):
                        self.assertEqual(h["type"], "command")
                        self.assertTrue(
                            h["command"].startswith(
                                'python3 "${CLAUDE_PLUGIN_ROOT}/hooks/'
                            )
                        )
                        self.assertIsInstance(h["timeout"], int)

    def test_every_hook_chains_the_windows_py_fallback(self):
        # M61 (RR01 §10.2): stock Windows has no `python3` on PATH, so each
        # command chains `|| py -3 <same script>`. Safe on macOS/Linux: every
        # hook exits 0 and denies via JSON stdout — each guard suite asserts
        # returncode 0 on its deny path (e.g. TestMergeGuard.
        # test_denies_gh_pr_merge_without_marker) — so the fallback fires
        # only when python3 itself is missing or crashes.
        for event, entries in self.config.items():
            for entry in entries:
                for h in entry["hooks"]:
                    with self.subTest(event=event, command=h["command"]):
                        first, sep, fallback = h["command"].partition(" || ")
                        self.assertTrue(sep, "command must chain a py fallback")
                        self.assertTrue(
                            fallback.startswith('py -3 "${CLAUDE_PLUGIN_ROOT}/hooks/')
                        )
                        self.assertEqual(
                            fallback.split(" ", 2)[2],
                            first.split(" ", 1)[1],
                            "fallback must invoke the same script",
                        )

    def test_every_hook_script_is_registered(self):
        registered = "".join(
            h["command"]
            for entries in self.config.values()
            for entry in entries
            for h in entry["hooks"]
        )
        scripts = {
            p.name for p in HOOKS_DIR.glob("*.py") if p.name != "cairn_common.py"
        }
        for script in scripts:
            with self.subTest(script=script):
                self.assertIn(script, registered)


class TestStdlibOnly(unittest.TestCase):
    ALLOWED = {
        "ast", "json", "os", "pathlib", "re", "shlex", "subprocess", "sys",
        "cairn_common",
    }

    def test_hook_imports_are_stdlib_only(self):
        for script in HOOKS_DIR.glob("*.py"):
            tree = ast.parse(script.read_text())
            for node in ast.walk(tree):
                names = []
                if isinstance(node, ast.Import):
                    names = [a.name.split(".")[0] for a in node.names]
                elif isinstance(node, ast.ImportFrom):
                    names = [(node.module or "").split(".")[0]]
                for name in names:
                    self.assertIn(name, self.ALLOWED, f"{script.name} imports {name}")


if __name__ == "__main__":
    unittest.main()
