"""Fixture tests for the cairn deterministic tracking scripts.

Each test builds a throwaway ``cairn/`` tree in a temp dir and runs a
script as a real subprocess (``python3 <script> <root>``), mirroring how
the /milestone skill invokes them. Run from the repo root:

    python3 -m unittest discover -s scripts/tests -v

The validate tests inject exactly one defect per case and assert both the
specific FAIL line and the non-zero exit — a green "all checks passed" on a
known-bad tree would be the failure that matters.
"""

import ast
import copy
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent.parent


def live(status):
    return f"# M: Test milestone\n\n- **Status:** {status}   <!-- mirror -->\n\n## Goal\nx\n"


def archived(status):
    return f"# M — {status}\n\n**Status:** {status} · approved 2026-07-11\n\n## Outcome\nx\n"


def live_slot(status, slot):
    """A live milestone header carrying a `Principles touched:` slot."""
    return (
        f"# M: Test milestone\n\n- **Status:** {status}   <!-- mirror -->\n"
        f"- **Principles touched:** {slot}\n\n## Goal\nx\n"
    )


def live_cov(status, n_criteria, coverage_refs):
    """A live milestone body with `n_criteria` acceptance criteria and a
    Coverage section citing each AC number in `coverage_refs`."""
    acs = "\n".join(f"- [ ] criterion {i}" for i in range(1, n_criteria + 1))
    cov = "\n".join(f"- AC{r} → T1" for r in coverage_refs)
    return (
        f"# M: Test milestone\n\n- **Status:** {status}   <!-- mirror -->\n\n"
        f"## Acceptance criteria\n{acs}\n\n## Coverage\n{cov}\n\n## Tasks\n- [ ] T1\n"
    )


def live_sized(status, n_criteria, n_tasks):
    """A live milestone body with `n_criteria` fully-mapped acceptance criteria
    and `n_tasks` tasks — for the sizing advisory (M44). Coverage maps every
    criterion so coverage-complete passes and only the advisory can fire."""
    acs = "\n".join(f"- [ ] criterion {i}" for i in range(1, n_criteria + 1))
    cov = "\n".join(f"- AC{i} → T1" for i in range(1, n_criteria + 1))
    tasks = "\n".join(f"- [ ] T{i}" for i in range(1, n_tasks + 1))
    return (
        f"# M: Test milestone\n\n- **Status:** {status}   <!-- mirror -->\n\n"
        f"## Acceptance criteria\n{acs}\n\n## Coverage\n{cov}\n\n## Tasks\n{tasks}\n"
    )


# id, title, status, depends, priority, relpath
BASE_ROWS = [
    ("M03", "Live planned", "planned", "M01", "high", "milestones/M03-live.md"),
    ("M02", "Active", "in-progress", "—", "normal", "milestones/M02-active.md"),
    ("M01", "Old done", "done", "—", "high", "milestones/archive/M01-old.md"),
]
BASE_FILES = {
    "milestones/M03-live.md": live("planned"),
    "milestones/M02-active.md": live("in-progress"),
    "milestones/archive/M01-old.md": archived("done"),
}


def _load_validate():
    """Import cairn_validate for the rare direct-function test (most tests use
    the subprocess `run` below). Needs SCRIPTS_DIR on the path for its
    `import cairn_scripts`."""
    import importlib.util

    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    spec = importlib.util.spec_from_file_location(
        "cairn_validate", SCRIPTS_DIR / "cairn_validate.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_scripts():
    """Import cairn_scripts for direct-function tests of its helpers."""
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    import cairn_scripts

    return cairn_scripts


def run(script, root):
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script), str(root)],
        capture_output=True,
        text=True,
        timeout=30,
    )


def run_impact(args, cwd=None):
    """cairn_impact takes principle ids as positionals and the root via
    --root (not the positional-root convention), so it needs its own runner."""
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "cairn_impact.py"), *args],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=cwd,
    )


class Tree:
    """A mutable cairn/ fixture; call build() to write it, then run scripts."""

    def __init__(self, tmp):
        self.root = pathlib.Path(tmp)
        self.rows = copy.deepcopy(BASE_ROWS)
        self.files = dict(BASE_FILES)
        self.candidates = ["Idea one", "Idea two"]
        self.hygiene = "2026-07-11"

    def roadmap_text(self):
        header = (
            "# Roadmap\n\n"
            f"_Last hygiene check: {self.hygiene}_\n\n"
            "| ID | Title | Status | Depends on | Priority | File/Archive |\n"
            "|---|---|---|---|---|---|\n"
        )
        rows = "".join(
            f"| {i} | {t} | {s} | {d} | {p} | {rel} |\n"
            for (i, t, s, d, p, rel) in self.rows
        )
        cands = "\n## Candidates\n\n" + "".join(f"- {c}\n" for c in self.candidates)
        return header + rows + cands

    def build(self):
        (self.root / "CLAUDE.md").write_text("# repo\n\ncairn section here\n")
        cairn = self.root / "cairn"
        (cairn / "milestones" / "archive").mkdir(parents=True, exist_ok=True)
        (cairn / "ROADMAP.md").write_text(self.roadmap_text())
        # §1 scaffold pieces the drift check (M24) requires — a valid cairn
        # repo carries these, so the shared fixture must too. Empty scaffold
        # dirs (reviews/, references/pdf/) are intentionally left uncreated:
        # git drops empty dirs, and the check tolerates their absence.
        (cairn / "DESIGN.md").write_text("# Design\n\nx\n")
        (cairn / "DECISIONS.md").write_text("# Decisions\n\nx\n")
        (cairn / "LESSONS.md").write_text("# Lessons\n\nx\n")
        (cairn / "references").mkdir(parents=True, exist_ok=True)
        (cairn / "references" / "INDEX.md").write_text("# Index\n")
        (self.root / ".gitignore").write_text(
            "cairn/references/pdf/\ncairn/.merge-approved\n"
            "cairn/.merge-approved.pending\n"
        )
        for rel, body in self.files.items():
            (cairn / rel).write_text(body)
        return self.root


class ScriptCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tree = Tree(self._tmp.name)


class TestStatus(ScriptCase):
    def test_snapshot(self):
        root = self.tree.build()
        proc = run("cairn_status.py", root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = proc.stdout
        self.assertIn("in-progress  1   M02", out)
        self.assertIn("planned      1   M03", out)
        self.assertIn("done         1   M01", out)
        self.assertIn("(candidates  2)", out)
        self.assertIn("Active: M02 (in-progress) — Active", out)
        self.assertIn("Next planned (by priority): M03 (high)", out)
        self.assertIn("Last hygiene check: 2026-07-11", out)


class TestNext(ScriptCase):
    def test_recommends_resume_when_in_progress(self):
        root = self.tree.build()
        out = run("cairn_next.py", root).stdout
        self.assertIn("Recommended: resume M02 → /milestone-implement M02", out)
        # M03 depends on M01 (done) → workable.
        self.assertIn("M03 (high) — Live planned", out)

    def test_archived_done_dependency_is_satisfied(self):
        # Regression: a dep on a done milestone whose ROADMAP row was pruned
        # under terminal-row retention (archive file only) must count as satisfied.
        self.tree.rows = [
            ("M20", "New", "planned", "M05", "high", "milestones/M20-new.md"),
        ]
        self.tree.files = {
            "milestones/M20-new.md": live("planned"),
            "milestones/archive/M05-old.md": archived("done"),  # no ROADMAP row
        }
        root = self.tree.build()
        out = run("cairn_next.py", root).stdout
        self.assertIn("Recommended: implement M20 → /milestone-implement M20", out)
        self.assertIn("M20 (high) — New", out)
        self.assertNotIn("Blocked by dependencies", out)

    def test_ids_sort_numerically_past_m99(self):
        self.tree.rows = [
            ("M9", "Nine", "planned", "—", "normal", "milestones/M9.md"),
            ("M100", "Hundred", "planned", "—", "normal", "milestones/M100.md"),
        ]
        self.tree.files = {
            "milestones/M9.md": live("planned"),
            "milestones/M100.md": live("planned"),
        }
        out = run("cairn_next.py", self.tree.build()).stdout
        self.assertLess(out.index("M9 (normal)"), out.index("M100 (normal)"))

    def test_blocked_dependency_reported_not_workable(self):
        # M03 now depends on M02 (in-progress, not done) → not workable.
        self.tree.rows[0] = ("M03", "Live planned", "planned", "M02", "high", "milestones/M03-live.md")
        # remove the in-progress one so the recommendation falls through to plan
        self.tree.rows[1] = ("M02", "Active", "planned", "—", "normal", "milestones/M02-active.md")
        self.tree.files["milestones/M02-active.md"] = live("planned")
        root = self.tree.build()
        out = run("cairn_next.py", root).stdout
        self.assertIn("Blocked by dependencies:", out)
        self.assertIn("M03 — waiting on M02 (planned)", out)


class TestValidateClean(ScriptCase):
    def test_clean_tree_passes(self):
        root = self.tree.build()
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("all checks passed", proc.stdout)

    def test_mature_claude_md_whole_file_not_capped(self):
        # D-018: a mature repo's own dev doctrine is not cairn's to cap. A
        # 200+-line CLAUDE.md (would FAIL the old whole-file <80) passes so
        # long as the appended cairn section is within its own cap.
        root = self.tree.build()
        (root / "CLAUDE.md").write_text(
            "# Big mature repo\n\n"
            + "legit dev doctrine line\n" * 200
            + "\n## Project tracking (cairn)\n"
            + "cairn router line\n" * 10
        )
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("all checks passed", proc.stdout)

    def test_fully_mapped_coverage_passes(self):
        # Every criterion referenced in Coverage → coverage-complete passes.
        self.tree.files["milestones/M03-live.md"] = live_cov("planned", 3, [1, 2, 3])
        proc = run("cairn_validate.py", self.tree.build())
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  coverage complete", proc.stdout)

    def test_archived_file_with_criteria_is_exempt(self):
        # An archived (compressed) summary is never scanned: criteria but no
        # Coverage section must not trip the check.
        self.tree.files["milestones/archive/M01-old.md"] = (
            "# M01 — done\n\n**Status:** done · approved 2026-07-11\n\n"
            "## Acceptance criteria\n- [x] one\n- [x] two\n\n## Outcome\nx\n"
        )
        proc = run("cairn_validate.py", self.tree.build())
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  coverage complete", proc.stdout)


class TestReferencesCheck(ScriptCase):
    """M57: the references index<->disk check — every committed top-level
    references note has an INDEX.md line and every INDEX line's target exists
    (the references sibling of roadmap<->disk orphans). Dedicated fixtures on
    top of the base tree (M34 pattern); the base Tree.build() ships an empty
    INDEX + no notes, which must stay valid for this check."""

    def test_orphan_note_fails(self):
        root = self.tree.build()
        (root / "cairn" / "references" / "stray.md").write_text("# stray\n")
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("FAIL  references index<->disk", proc.stdout)
        self.assertIn(
            "cairn/references/stray.md has no INDEX.md line", proc.stdout
        )

    def test_missing_target_fails(self):
        root = self.tree.build()
        (root / "cairn" / "references" / "INDEX.md").write_text(
            "# Index\n\n- gone.md — a note that was deleted\n"
        )
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn(
            "INDEX.md lists gone.md but no such file", proc.stdout
        )

    def test_agreement_passes(self):
        root = self.tree.build()
        (root / "cairn" / "references" / "notes.md").write_text("# notes\n")
        (root / "cairn" / "references" / "INDEX.md").write_text(
            "# Index\n\n- notes.md — a real note\n"
        )
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  references index<->disk", proc.stdout)

    def test_decorated_index_lines_pass(self):
        # Review F1 (85): a semantically correct entry with a backticked or
        # markdown-linked filename must not trip the hard CHECK (D-023 — no
        # false positive on formatting alone).
        root = self.tree.build()
        (root / "cairn" / "references" / "tick.md").write_text("# t\n")
        (root / "cairn" / "references" / "link.md").write_text("# l\n")
        (root / "cairn" / "references" / "INDEX.md").write_text(
            "# Index\n\n- `tick.md` — backticked entry\n"
            "- [link.md](link.md) — linked entry\n"
        )
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  references index<->disk", proc.stdout)

    def test_absent_index_no_ops(self):
        # Independence: a missing INDEX.md is scaffold-present's failure; the
        # references check itself stays PASS (M45 validate-if-present pattern).
        root = self.tree.build()
        (root / "cairn" / "references" / "INDEX.md").unlink()
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("PASS  references index<->disk", proc.stdout)
        self.assertIn("FAIL  scaffold present", proc.stdout)


class TestDanglingIds(ScriptCase):
    """M57: the dangling-ID-token advisory. Known IDs = ROADMAP rows ∪
    live/archive milestone files ∪ D-entry headers; a bare unresolvable token
    WARNs (exit-neutral). Tolerance rules per D-023: above-max tokens skip
    (the M99 example-prose class), and unresolved tokens on a line carrying an
    owner/repo slug skip (the "ackwards M57" cross-repo class). Fixtures use a
    *gapped* known-ID set — M05 exists but M04 was never assigned here — the
    shape a migrated adopter repo can carry."""

    def _gap(self):
        # Extend the base tree (M01–M03) with archived M05: max=5, gap at M04.
        self.tree.rows.append(
            ("M05", "Old thing", "done", "—", "normal",
             "milestones/archive/M05-old.md")
        )
        self.tree.files["milestones/archive/M05-old.md"] = (
            "# M05: Old thing (done 2026-07-11)\n\n**Goal:** old.\n"
        )

    def test_true_dangler_warns_but_stays_exit_neutral(self):
        self._gap()
        self.tree.files["milestones/M03-live.md"] += "\nSee M04 for background.\n"
        proc = run("cairn_validate.py", self.tree.build())
        self.assertEqual(proc.returncode, 0, proc.stdout)  # WARN, never FAIL
        self.assertIn("WARN  dangling id tokens", proc.stdout)
        self.assertIn(
            "M04 resolves to no ROADMAP row, milestone file, or D-entry",
            proc.stdout,
        )

    def test_above_max_example_token_is_silent(self):
        # The M99 class: an ID never assigned anywhere (99 > max) is example
        # or forward prose, not a broken link.
        self.tree.files["milestones/M03-live.md"] += "\nIDs grow past M99.\n"
        proc = run("cairn_validate.py", self.tree.build())
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("OK    dangling id tokens", proc.stdout)

    def test_repo_qualified_cite_is_silent(self):
        # The "ackwards M57" class: same gapped M04, but the line carries an
        # owner/repo slug — a cross-repo cite, not a local dangler.
        self._gap()
        self.tree.files["milestones/M03-live.md"] += (
            "\nSee jmgirard/otherrepo M04 for the upstream fix.\n"
        )
        proc = run("cairn_validate.py", self.tree.build())
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("OK    dangling id tokens", proc.stdout)

    def test_d_token_dangler_warns(self):
        root_ = self.tree.build()
        (root_ / "cairn" / "DECISIONS.md").write_text(
            "# Decisions\n\n### D-001 (2026-07-11): a\n\nx\n\n"
            "### D-003 (2026-07-11): b\n\nx\n"
        )
        (root_ / "cairn" / "DESIGN.md").write_text(
            "# Design\n\nPer D-002 we do X.\n"
        )
        proc = run("cairn_validate.py", root_)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("WARN  dangling id tokens", proc.stdout)
        self.assertIn(
            "D-002 resolves to no ROADMAP row, milestone file, or D-entry",
            proc.stdout,
        )

    def test_legacy_is_excluded(self):
        # Entombed pre-migration files are never scanned (D-005).
        self._gap()
        root_ = self.tree.build()
        legacy = root_ / "cairn" / "legacy"
        legacy.mkdir()
        (legacy / "OLD_BOARD.md").write_text("# old\n\nSee M04 someday.\n")
        proc = run("cairn_validate.py", root_)
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("OK    dangling id tokens", proc.stdout)


VALID_PROFILE = (
    "# Toolchain profile: generic\n\n"
    "## verify\n- run tests\n\n"
    "## consistency-gate\nnone\n\n"
    "## test-doctrine\nnone beyond universal\n\n"
    "## release-walk\nbump + tag\n\n"
    "## init-detection\nfallback\n\n"
    "## greenfield-openers\nnone\n\n"
    "## changelog\nnone\n"
)


class TestValidateProfile(ScriptCase):
    """M45: cairn_validate's profile check is validate-if-present — it no-ops
    when cairn/PROFILE.md is absent (back-compat) and FAILs on a missing,
    empty, or unrecognized slot when present."""

    def _profile(self, text):
        root = self.tree.build()
        (root / "cairn" / "PROFILE.md").write_text(text)
        return root

    def test_absent_profile_noops(self):
        proc = run("cairn_validate.py", self.tree.build())
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  profile valid", proc.stdout)

    def test_valid_profile_passes(self):
        proc = run("cairn_validate.py", self._profile(VALID_PROFILE))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  profile valid", proc.stdout)

    def test_missing_slot_fails(self):
        text = VALID_PROFILE.replace("## release-walk\nbump + tag\n\n", "")
        proc = run("cairn_validate.py", self._profile(text))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("FAIL  profile valid", proc.stdout)
        self.assertIn("missing slot '## release-walk'", proc.stdout)

    def test_empty_slot_fails(self):
        text = VALID_PROFILE.replace("## verify\n- run tests\n", "## verify\n")
        proc = run("cairn_validate.py", self._profile(text))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("slot '## verify' is empty", proc.stdout)

    def test_changelog_slot_missing_fails(self):
        # M68: changelog is the required seventh slot (D-040) — a PROFILE.md
        # without it FAILs like any other missing slot.
        text = VALID_PROFILE.replace("\n## changelog\nnone\n", "")
        proc = run("cairn_validate.py", self._profile(text))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("missing slot '## changelog'", proc.stdout)

    def test_changelog_slot_empty_fails(self):
        # M68 review F1 (scored 80): AC1's "empty" leg gets its own changelog
        # fixture rather than riding the slot-generic empty check.
        text = VALID_PROFILE.replace("## changelog\nnone\n", "## changelog\n")
        proc = run("cairn_validate.py", self._profile(text))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("slot '## changelog' is empty", proc.stdout)

    def test_changelog_declares_file_passes(self):
        # M68: a file-name declaration is as valid as the "none" the base
        # fixture pins (both are non-empty bodies).
        text = VALID_PROFILE.replace("## changelog\nnone\n", "## changelog\nCHANGELOG.md\n")
        proc = run("cairn_validate.py", self._profile(text))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  profile valid", proc.stdout)

    def test_unrecognized_slot_fails(self):
        proc = run("cairn_validate.py", self._profile(VALID_PROFILE + "\n## verfiy\ntypo\n"))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("unrecognized slot '## verfiy'", proc.stdout)

    def test_fenced_command_block_body_not_a_slot(self):
        # Review finding (scored 91): a `## ` comment inside a fenced command
        # block in a slot body must be body content, not a new slot.
        text = VALID_PROFILE.replace(
            "## verify\n- run tests\n",
            "## verify\n```sh\n## build first\nmake test\n```\n",
        )
        proc = run("cairn_validate.py", self._profile(text))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  profile valid", proc.stdout)

    def test_shipped_reference_profiles_are_valid(self):
        # The plugin's own r-package + generic references must satisfy the check.
        import importlib.util

        plugin_root = pathlib.Path(__file__).resolve().parents[2]
        spec = importlib.util.spec_from_file_location(
            "cairn_validate", plugin_root / "scripts" / "cairn_validate.py"
        )
        cv = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(plugin_root / "scripts"))
        try:
            spec.loader.exec_module(cv)
            for name in ("r-package", "python", "generic"):
                text = (plugin_root / "skills" / "shared" / "profiles" / f"{name}.md").read_text()
                slots = cv._profile_slots(text)
                for slot in cv._REQUIRED_SLOTS:
                    self.assertIn(slot, slots, f"{name} missing {slot}")
                    self.assertTrue(any(l.strip() for l in slots[slot]), f"{name} {slot} empty")
                for slot in slots:
                    self.assertIn(slot, cv._REQUIRED_SLOTS, f"{name} unrecognized {slot}")
                # M61: cairn-init copies the reference verbatim into
                # cairn/PROFILE.md, so every shipped profile must fit the
                # instantiation cap or a fresh adopter fails validate on
                # first contact (the pre-M61 latent bug: 97 lines vs <90).
                import cairn_scripts as cs_mod
                cap = cs_mod.LINE_CAPS["cairn/PROFILE.md"]
                n = len(text.splitlines())
                self.assertLess(n, cap, f"{name}.md is {n} lines (cap <{cap})")
        finally:
            sys.path.pop(0)


class TestSizingAdvisory(ScriptCase):
    """M44: the sizing advisory WARNs over the split tripwires (>7 criteria,
    >10 tasks) but never fails the gate (exit-code neutral)."""

    def _add_sized(self, n_criteria, n_tasks):
        self.tree.rows.append(("M04", "Big", "planned", "—", "normal", "milestones/M04-big.md"))
        self.tree.files["milestones/M04-big.md"] = live_sized("planned", n_criteria, n_tasks)
        return self.tree.build()

    def test_criteria_over_tripwire_warns_but_passes(self):
        # 8 criteria (>7), tasks within → WARN, and the exit code stays 0.
        proc = run("cairn_validate.py", self._add_sized(8, 5))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("WARN  sizing", proc.stdout)
        self.assertIn("M04: 8 acceptance criteria (>7 tripwire)", proc.stdout)
        self.assertNotIn("tasks (>10 tripwire)", proc.stdout)
        self.assertIn("all checks passed", proc.stdout)
        self.assertIn("advisory warning(s) — not gate failures", proc.stdout)

    def test_tasks_over_tripwire_warns_but_passes(self):
        # 11 tasks (>10), criteria within → WARN, exit 0.
        proc = run("cairn_validate.py", self._add_sized(3, 11))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("WARN  sizing", proc.stdout)
        self.assertIn("M04: 11 tasks (>10 tripwire)", proc.stdout)
        self.assertNotIn("acceptance criteria (>7 tripwire)", proc.stdout)

    def test_within_tripwire_no_warn(self):
        # Boundary: 7 criteria and 10 tasks are AT the tripwire, not over it.
        proc = run("cairn_validate.py", self._add_sized(7, 10))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("OK    sizing", proc.stdout)
        self.assertNotIn("consider splitting", proc.stdout)

    def test_advisory_skips_archived(self):
        # An archived summary is never scanned (check_sizing_advisory iterates
        # live_files only). Asserted at the function level: an archived file
        # large enough to exceed the tripwires would also blow the 25-line
        # archive cap, so a full-run assertion is impossible by construction —
        # which is exactly why the advisory only ever needs to see live files.
        self.tree.files["milestones/archive/M01-old.md"] = live_sized("done", 12, 12)
        root = self.tree.build()
        cv = _load_validate()
        self.assertEqual(cv.check_sizing_advisory(str(root)), [])


class TestPrinciplesSlot(ScriptCase):
    DESIGN = "# Design\n\n## Design Principles\n\n- IP1: first\n- GP1: second\n"

    def _build_with_design(self, slot):
        self.tree.files["milestones/M03-live.md"] = live_slot("planned", slot)
        root = self.tree.build()
        (root / "cairn" / "DESIGN.md").write_text(self.DESIGN)
        return root

    def test_valid_slot_passes(self):
        proc = run("cairn_validate.py", self._build_with_design("IP1, GP1"))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  principles slot valid", proc.stdout)

    def test_dash_slot_noops(self):
        # The template default '—' (and pre-slot files) must not trip the check.
        proc = run("cairn_validate.py", self._build_with_design("—"))
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  principles slot valid", proc.stdout)

    def test_bogus_id_fails(self):
        # GP9 is not defined in DESIGN.md → the slot check flags it.
        proc = run("cairn_validate.py", self._build_with_design("IP1, GP9"))
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn("FAIL  principles slot valid", proc.stdout)
        self.assertIn("GP9", proc.stdout)


class TestValidateFailures(ScriptCase):
    def assert_fails(self, check_label, root):
        proc = run("cairn_validate.py", root)
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn(f"FAIL  {check_label}", proc.stdout)
        return proc.stdout

    def test_mirror_mismatch(self):
        self.tree.files["milestones/M02-active.md"] = live("review")
        self.assert_fails("mirror agreement", self.tree.build())

    def test_two_in_progress(self):
        self.tree.rows[0] = ("M03", "Live planned", "in-progress", "M01", "high", "milestones/M03-live.md")
        self.tree.files["milestones/M03-live.md"] = live("in-progress")
        self.assert_fails("at most one in-progress", self.tree.build())

    def test_over_cap_milestone(self):
        self.tree.files["milestones/M03-live.md"] = live("planned") + "\nx" * 160 + "\n"
        self.assert_fails("weight caps", self.tree.build())

    def test_over_cap_milestone_body_still_fails(self):
        # M55/AC2: plan discipline is unchanged — a plan-owned body that is
        # itself over 150 lines still FAILS, even with a Review section present.
        body = live("planned") + "x\n" * 160
        self.tree.files["milestones/M03-live.md"] = body + "## Review\n" + "e\n" * 5
        out = self.assert_fails("weight caps", self.tree.build())
        self.assertIn("plan-owned lines", out)

    def test_review_evidence_over_cap_passes(self):
        # M55/AC1: plan-owned body under 150 but the file total over 150 because
        # of Review evidence — the file PASSES weight-caps (the recurring
        # M19/M22/M33/M50 evidence-vs-cap scramble is gone).
        body = live("planned") + "x\n" * 100
        self.tree.files["milestones/M03-live.md"] = body + "## Review\n" + "e\n" * 200
        proc = run("cairn_validate.py", self.tree.build())
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("PASS  weight caps", proc.stdout)

    def test_over_cap_lessons(self):
        # A LESSONS.md at/over its 50-line cap fails weight-caps. (An absent
        # file is not a cap failure: line_count returns None for a missing
        # path, so check_caps skips it — a missing LESSONS.md is now caught by
        # check_scaffold instead, not by weight-caps.)
        root = self.tree.build()
        (root / "cairn" / "LESSONS.md").write_text("# Lessons\n" + "- x\n" * 55)
        out = self.assert_fails("weight caps", root)
        self.assertIn("cairn/LESSONS.md", out)
        self.assertIn("cap <50", out)

    def test_over_cap_claude_section(self):
        # D-018: a bloated `## Project tracking (cairn)` section (>= 30 lines)
        # still hard-fails — that block is the part cairn owns.
        root = self.tree.build()
        (root / "CLAUDE.md").write_text(
            "# repo\n\nlocal doctrine\n\n## Project tracking (cairn)\n" + "x\n" * 35
        )
        out = self.assert_fails("weight caps", root)
        self.assertIn("CLAUDE.md cairn section", out)
        self.assertIn("cap <30", out)

    def test_non_iso_date_in_lessons(self):
        # LESSONS.md entries carry dates (- YYYY-MM-DD (M<NN>): …); a
        # misformatted one must be flagged by the ISO-date scan.
        root = self.tree.build()
        (root / "cairn" / "LESSONS.md").write_text("# Lessons\n\n- 07/11/2026 (M16): x\n")
        out = self.assert_fails("iso date format", root)
        self.assertIn("LESSONS.md", out)

    def test_terminal_row_retention(self):
        # done rows still count toward the cap after the done→terminal generalization.
        for n in range(4, 10):  # M04..M09 → 7 done rows total with M01
            mid = f"M0{n}"
            rel = f"milestones/archive/{mid}-x.md"
            self.tree.rows.append((mid, "Done x", "done", "—", "normal", rel))
            self.tree.files[rel] = archived("done")
        self.assert_fails("terminal-row retention", self.tree.build())

    def test_dropped_rows_count_toward_retention(self):
        # A dropped row counts like a done row: 5 done (at the cap) plus any
        # dropped rows overflows the terminal cap. The old done-only rule would
        # have passed this (done == 5) — this case fences the generalization.
        for n in range(4, 8):  # M04..M07 done → 5 done total with M01 (== cap)
            mid = f"M0{n}"
            rel = f"milestones/archive/{mid}-x.md"
            self.tree.rows.append((mid, "Done x", "done", "—", "normal", rel))
            self.tree.files[rel] = archived("done")
        for n in range(8, 10):  # M08, M09 dropped → 7 terminal total
            mid = f"M0{n}"
            rel = f"milestones/archive/{mid}-x.md"
            self.tree.rows.append((mid, "Dropped x", "dropped", "—", "normal", rel))
            self.tree.files[rel] = archived("dropped")
        self.assert_fails("terminal-row retention", self.tree.build())

    def test_unknown_status(self):
        self.tree.rows[0] = ("M03", "Live planned", "planed", "M01", "high", "milestones/M03-live.md")
        self.tree.files["milestones/M03-live.md"] = live("planed")  # keep mirror agreeing
        self.assert_fails("status vocabulary", self.tree.build())

    def test_unknown_priority(self):
        # A Priority outside {high, normal, low} fails the priority-vocab check
        # (M44) — priority is not policed by any other check, so this isolates it.
        self.tree.rows[0] = ("M03", "Live planned", "planned", "M01", "urgent", "milestones/M03-live.md")
        out = self.assert_fails("priority vocabulary", self.tree.build())
        self.assertIn("unknown priority 'urgent'", out)

    def test_dangling_dependency(self):
        self.tree.rows[0] = ("M03", "Live planned", "planned", "M99", "high", "milestones/M03-live.md")
        out = self.assert_fails("dependency resolution", self.tree.build())
        self.assertIn("does not exist", out)

    def test_dependency_on_dropped_milestone(self):
        # M03 depends on M04, which exists but is dropped → must be flagged.
        self.tree.rows[0] = ("M03", "Live planned", "planned", "M04", "high", "milestones/M03-live.md")
        self.tree.rows.append(("M04", "Abandoned", "dropped", "—", "normal", "milestones/M04-x.md"))
        self.tree.files["milestones/M04-x.md"] = live("dropped")
        out = self.assert_fails("dependency resolution", self.tree.build())
        self.assertIn("is dropped", out)

    def test_row_points_to_missing_file(self):
        self.tree.rows.append(("M05", "Ghost", "planned", "—", "normal", "milestones/M05-ghost.md"))
        self.assert_fails("roadmap<->disk orphans", self.tree.build())

    def test_unmapped_criterion(self):
        # AC2 has no Coverage line → the coverage-complete check flags it.
        self.tree.files["milestones/M03-live.md"] = live_cov("planned", 2, [1])
        out = self.assert_fails("coverage complete", self.tree.build())
        self.assertIn("M03: AC2 not referenced in Coverage", out)

    def test_dangling_coverage_reference(self):
        # Coverage cites AC3 but only 2 criteria exist → dangling reference.
        self.tree.files["milestones/M03-live.md"] = live_cov("planned", 2, [1, 2, 3])
        out = self.assert_fails("coverage complete", self.tree.build())
        self.assertIn("Coverage references AC3 but file has 2 criteria", out)

    def test_live_file_without_row(self):
        self.tree.files["milestones/M07-extra.md"] = live("planned")
        self.assert_fails("roadmap<->disk orphans", self.tree.build())

    def test_duplicate_row_id(self):
        self.tree.rows.append(("M03", "Dup", "planned", "M01", "high", "milestones/M03-live.md"))
        self.assert_fails("id uniqueness", self.tree.build())

    def test_non_iso_date(self):
        # A misformatted work-log date must be flagged; the clean tree's ISO
        # date (archived M01, "approved 2026-07-11") already proves ISO passes.
        self.tree.files["milestones/M03-live.md"] = live("planned") + "\n- 07/11/2026: did a thing\n"
        out = self.assert_fails("iso date format", self.tree.build())
        self.assertIn("non-ISO date '07/11/2026'", out)

    def test_non_iso_date_formats(self):
        # Each non-ISO branch is flagged: year-last dashed, both month-name
        # orders, the malformed-ISO (missing zero-pad) case, and both slash
        # orders that carry a 4-digit year (year-last and year-first).
        for bad in ("11-07-2026", "Jul 11, 2026", "11 July 2026", "2026-7-11",
                    "07/11/2026", "2026/07/11"):
            with self.subTest(bad=bad):
                self.tree = Tree(self._tmp.name)
                self.tree.files["milestones/M03-live.md"] = live("planned") + f"\n- {bad}: x\n"
                out = self.assert_fails("iso date format", self.tree.build())
                self.assertIn(f"non-ISO date '{bad}'", out)

    def test_valid_iso_and_non_dates_pass(self):
        # Valid ISO plus tokens that must NOT be mistaken for dates.
        self.tree.files["milestones/M03-live.md"] = (
            live("planned") + "\n- 2026-12-31: v4.8 shipped, see p. 12, ratio 1/2, ID M13\n"
        )
        proc = run("cairn_validate.py", self.tree.build())
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_check_result_notation_passes(self):
        # R CMD check count-notation is three slash-separated counts with no
        # 4-digit year (errors/warnings/notes); it must NOT be mistaken for a
        # slash date. A real slash date carries a 4-digit year on one end;
        # count-triples don't, so requiring the year distinguishes them.
        self.tree.files["milestones/M03-live.md"] = (
            live("planned") + "\n- 2026-12-31: R CMD check 0/0/0, earlier run 0/1/2\n"
        )
        proc = run("cairn_validate.py", self.tree.build())
        self.assertEqual(proc.returncode, 0, proc.stdout)


class TestMilestoneBodyLineCount(unittest.TestCase):
    """M55: the milestone weight cap measures the plan-owned body only — every
    line before the `## Review` heading — so review evidence never counts
    against the plan-discipline cap. A file with no Review section counts whole
    (back-compat); a fenced `## Review` in the body is not the boundary (M45)."""

    def setUp(self):
        self.cs = _load_scripts()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = pathlib.Path(self._tmp.name) / "M.md"

    def count(self, text):
        self.path.write_text(text)
        return self.cs.milestone_body_line_count(str(self.path))

    def test_review_section_is_exempt(self):
        body = "# M\n\n## Goal\nx\n\n"  # 5 lines
        n_body = len(body.splitlines())
        text = body + "## Review\n" + "e\n" * 200
        self.assertEqual(self.count(text), n_body)

    def test_no_review_section_counts_whole_file(self):
        text = "# M\n\n## Goal\nx\n## Tasks\n- [ ] T1\n"
        self.assertEqual(self.count(text), len(text.splitlines()))

    def test_fenced_review_heading_is_not_the_boundary(self):
        # The body quotes `## Review` inside a fenced block; the real section
        # comes after. Without fence tracking this would stop at the fenced line.
        body_lines = ["# M", "", "## Tasks", "- [ ] T1", "```", "## Review",
                      "```", "after fence", ""]
        body = "\n".join(body_lines) + "\n"
        text = body + "## Review\n" + "e\n" * 50
        self.assertEqual(self.count(text), len(body_lines))

    def test_fenced_review_without_real_section_counts_whole(self):
        lines = ["# M", "", "## Tasks", "```", "## Review", "```", "done", ""]
        text = "\n".join(lines) + "\n"
        self.assertEqual(self.count(text), len(lines))

    def test_review_prefixed_heading_is_not_the_boundary(self):
        # Only an exact `## Review` heading is the boundary — a plan-body H2 that
        # merely starts with "review" (e.g. `## Reviewers`) must not truncate the
        # body, or an oversized plan could silently pass the cap (M55 review).
        body_lines = ["# M", "", "## Reviewers", "- alice", "- bob", ""]
        body = "\n".join(body_lines) + "\n"
        text = body + "## Review\n" + "e\n" * 50
        self.assertEqual(self.count(text), len(body_lines))

    def test_unreadable_returns_none(self):
        missing = pathlib.Path(self._tmp.name) / "nope.md"
        self.assertIsNone(self.cs.milestone_body_line_count(str(missing)))


class TestMilestoneSectionLineCounts(unittest.TestCase):
    """M69: the diagnostic breakdown of an over-cap plan-owned body — each
    `## ` section with its line count, so trimming targets the heaviest section
    in one pass instead of a nibble-and-recount loop. Shares the plan-owned/
    `## Review` boundary and fence logic with `milestone_body_line_count`."""

    def setUp(self):
        self.cs = _load_scripts()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.path = pathlib.Path(self._tmp.name) / "M.md"

    def counts(self, text):
        self.path.write_text(text)
        return self.cs.milestone_section_line_counts(str(self.path))

    def body(self, text):
        self.path.write_text(text)
        return self.cs.milestone_body_line_count(str(self.path))

    def test_counts_each_section_in_document_order(self):
        text = "# M\n\n## Goal\nx\n\n## Tasks\n- [ ] T1\n- [ ] T2\n\n## Review\n" + "e\n" * 50
        self.assertEqual(self.counts(text), [("Goal", 3), ("Tasks", 4)])

    def test_review_section_excluded(self):
        text = "# M\n\n## Goal\nx\n\n## Review\n" + "e\n" * 50
        headings = [h for h, _ in self.counts(text)]
        self.assertNotIn("Review", headings)

    def test_preamble_plus_sections_sum_to_body_count(self):
        # The invariant that makes the breakdown trustworthy: nothing is
        # double-counted or lost — preamble (title + status block) + section
        # counts == the authoritative plan-owned body total.
        text = "# M\n\n- **Status:** planned\n\n## Goal\nx\ny\n\n## Tasks\n- [ ] T1\n\n## Review\n" + "e\n" * 9
        sections = self.counts(text)
        # preamble = lines before the first `## ` heading.
        lines = text.splitlines()
        preamble = next(i for i, ln in enumerate(lines) if ln.startswith("## "))
        self.assertEqual(preamble + sum(n for _, n in sections), self.body(text))

    def test_fenced_review_heading_is_not_the_boundary(self):
        body_lines = ["# M", "", "## Tasks", "- [ ] T1", "```", "## Review",
                      "```", "after fence", ""]
        text = "\n".join(body_lines) + "\n## Review\n" + "e\n" * 50
        # The whole fenced block stays inside the Tasks section (7 lines: heading
        # through the blank before the real `## Review`).
        self.assertEqual(self.counts(text), [("Tasks", 7)])

    def test_review_prefixed_heading_is_not_the_boundary(self):
        text = "# M\n\n## Reviewers\n- alice\n- bob\n\n## Review\n" + "e\n" * 50
        self.assertEqual(self.counts(text), [("Reviewers", 4)])

    def test_no_sections_returns_empty(self):
        self.assertEqual(self.counts("# M\n\njust prose, no H2\n"), [])

    def test_unreadable_returns_none(self):
        missing = pathlib.Path(self._tmp.name) / "nope.md"
        self.assertIsNone(self.cs.milestone_section_line_counts(str(missing)))


class TestImpact(ScriptCase):
    """cairn_impact: principle → citing cairn/ file:line."""

    def _impact_tree(self):
        root = self.tree.build()
        cairn = self.tree.root / "cairn"
        (cairn / "DESIGN.md").write_text(
            "# Design\n\n- IP2: prior state is surfaced.\n"
            "- GP4: fixes live in the shared artifact.\n"
        )
        (cairn / "DECISIONS.md").write_text(
            "# Decisions\n\n### D-1\n\nThis one leans on GP4 here.\n"
        )
        (cairn / "milestones" / "M50-cite.md").write_text(
            "IP2 appears on line 1 of this file.\n\n## Goal\nx\n"
        )
        return root

    def test_named_principles_reported_with_lines(self):
        root = self._impact_tree()
        proc = run_impact(["IP2", "GP9", "--root", str(root)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = proc.stdout
        self.assertIn("cairn/DESIGN.md:3", out)          # IP2 definition
        self.assertIn("milestones/M50-cite.md:1", out)   # IP2 citation, line 1
        self.assertIn("GP9 — no references", out)        # absent principle

    def test_decisions_citation_reported(self):
        out = run_impact(["GP4", "--root", str(self._impact_tree())]).stdout
        self.assertIn("cairn/DESIGN.md:4", out)
        self.assertIn("cairn/DECISIONS.md:5", out)

    def test_slot_reference_tagged_declared(self):
        # A reference on a `Principles touched:` slot line is tagged
        # (declared); an incidental prose citation of the same id is not (M38).
        root = self.tree.build()
        cairn = self.tree.root / "cairn"
        (cairn / "DESIGN.md").write_text("# Design\n\n- IP2: prior state is surfaced.\n")
        (cairn / "milestones" / "M51-slot.md").write_text(
            "# M51\n\n- **Status:** planned\n- **Principles touched:** IP2\n\n"
            "## Goal\nAlso mentions IP2 in prose here.\n"
        )
        out = run_impact(["IP2", "--root", str(root)]).stdout
        cited = [ln for ln in out.splitlines() if "M51-slot.md" in ln]
        declared = [ln for ln in cited if ln.rstrip().endswith("(declared)")]
        prose = [ln for ln in cited if not ln.rstrip().endswith("(declared)")]
        self.assertEqual(len(declared), 1, out)   # the slot line
        self.assertEqual(len(prose), 1, out)      # the prose line, untagged

    def test_changed_derives_from_design_diff(self):
        if not shutil.which("git"):
            self.skipTest("git not available")
        root = self._impact_tree()
        git = ["git", "-C", str(root)]
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(
            git + ["-c", "user.email=t@t", "-c", "user.name=t",
                   "commit", "-q", "-m", "init"],
            check=True,
        )
        # Edit only GP4's line; IP2 is untouched.
        (root / "cairn" / "DESIGN.md").write_text(
            "# Design\n\n- IP2: prior state is surfaced.\n"
            "- GP4: fixes live in the shared artifact, never per-user memory.\n"
        )
        proc = run_impact(["--changed", "--root", str(root)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("GP4 —", proc.stdout)                 # changed → reported
        self.assertIn("cairn/DECISIONS.md:5", proc.stdout)  # its downstream ref
        self.assertNotIn("IP2 —", proc.stdout)              # unchanged → absent

    def test_changed_sees_committed_branch_edit(self):
        # The review-gate scenario: the principle edit is already committed on
        # a milestone branch cut from the default branch. --changed must diff
        # from the merge-base, not HEAD, or it reports nothing.
        if not shutil.which("git"):
            self.skipTest("git not available")
        root = self._impact_tree()
        git = ["git", "-C", str(root)]
        who = ["-c", "user.email=t@t", "-c", "user.name=t"]
        subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + who + ["commit", "-q", "-m", "base"], check=True)
        subprocess.run(git + ["checkout", "-q", "-b", "m99-x"], check=True)
        (root / "cairn" / "DESIGN.md").write_text(
            "# Design\n\n- IP2: prior state is surfaced.\n"
            "- GP4: fixes live in the shared artifact, never per-user memory.\n"
        )
        subprocess.run(git + who + ["commit", "-qam", "edit GP4"], check=True)
        proc = run_impact(["--changed", "--root", str(root)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("GP4 —", proc.stdout)                 # committed change seen
        self.assertIn("cairn/DECISIONS.md:5", proc.stdout)  # its downstream ref
        self.assertNotIn("IP2 —", proc.stdout)              # unchanged → absent

    def test_whole_word_non_match(self):
        root = self._impact_tree()
        (self.tree.root / "cairn" / "milestones" / "M51-ip20.md").write_text(
            "IP20 is a different, unrelated token.\n"
        )
        out = run_impact(["IP2", "--root", str(root)]).stdout
        self.assertNotIn("M51-ip20.md", out)  # IP2 must not match IP20

    def test_unknown_flag_is_usage_error(self):
        # A typo'd flag must not read as a clean all-clear at the gate.
        proc = run_impact(["--changd", "--root", str(self.tree.build())])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown option", proc.stderr)

    def test_no_args_is_usage_error(self):
        proc = run_impact(["--root", str(self.tree.build())])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("usage:", proc.stderr)


class TestOutsideCairn(unittest.TestCase):
    def test_all_scripts_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            for script in ("cairn_status.py", "cairn_next.py", "cairn_validate.py"):
                with self.subTest(script=script):
                    proc = run(script, tmp)
                    self.assertEqual(proc.returncode, 2)
                    self.assertIn("not a cairn repo", proc.stderr)

    def test_impact_exits_2_outside_cairn(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = run_impact(["IP1", "--root", tmp])
            self.assertEqual(proc.returncode, 2)
            self.assertIn("not a cairn repo", proc.stderr)


class TestStdlibOnly(unittest.TestCase):
    ALLOWED = {
        "ast", "copy", "glob", "json", "os", "pathlib", "re",
        "subprocess", "sys", "tempfile", "unittest",
        "cairn_common", "cairn_scripts",
    }

    def test_script_imports_are_stdlib_plus_shared(self):
        for script in SCRIPTS_DIR.glob("*.py"):
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
