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
import subprocess
import sys
import tempfile
import unittest

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent.parent


def live(status):
    return f"# M: Test milestone\n\n- **Status:** {status}   <!-- mirror -->\n\n## Goal\nx\n"


def archived(status):
    return f"# M — {status}\n\n**Status:** {status} · approved 2026-07-11\n\n## Outcome\nx\n"


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


def run(script, root):
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script), str(root)],
        capture_output=True,
        text=True,
        timeout=30,
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
        # under done-row retention (archive file only) must count as satisfied.
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

    def test_done_row_retention(self):
        for n in range(4, 10):  # M04..M09 → 7 done rows total with M01
            mid = f"M0{n}"
            rel = f"milestones/archive/{mid}-x.md"
            self.tree.rows.append((mid, "Done x", "done", "—", "normal", rel))
            self.tree.files[rel] = archived("done")
        self.assert_fails("done-row retention", self.tree.build())

    def test_unknown_status(self):
        self.tree.rows[0] = ("M03", "Live planned", "planed", "M01", "high", "milestones/M03-live.md")
        self.tree.files["milestones/M03-live.md"] = live("planed")  # keep mirror agreeing
        self.assert_fails("status vocabulary", self.tree.build())

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

    def test_live_file_without_row(self):
        self.tree.files["milestones/M07-extra.md"] = live("planned")
        self.assert_fails("roadmap<->disk orphans", self.tree.build())

    def test_duplicate_row_id(self):
        self.tree.rows.append(("M03", "Dup", "planned", "M01", "high", "milestones/M03-live.md"))
        self.assert_fails("id uniqueness", self.tree.build())


class TestOutsideCairn(unittest.TestCase):
    def test_all_scripts_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            for script in ("cairn_status.py", "cairn_next.py", "cairn_validate.py"):
                with self.subTest(script=script):
                    proc = run(script, tmp)
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
