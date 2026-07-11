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
import json
import os
import pathlib
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


class RepoFixture(unittest.TestCase):
    """A temp git repo, cairn-tracked or not, committed clean."""

    cairn = True

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "hooks@test.invalid")
        self.git("config", "user.name", "Hook Tests")
        if self.cairn:
            (self.root / "cairn" / "milestones").mkdir(parents=True)
            (self.root / "cairn" / "ROADMAP.md").write_text(ROADMAP)
            (self.root / "cairn" / "milestones" / "M07-test.md").write_text(
                f"# M07: Test milestone\n\n{MILESTONE_SENTINEL}\n"
            )
        (self.root / "code.txt").write_text("hello\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "init")

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


class TestNonCairnNoOp(RepoFixture):
    cairn = False

    def test_every_hook_is_silent_and_permissive(self):
        payloads = {
            "session_context.py": self.payload(hook_event_name="SessionStart"),
            "stop_guard.py": self.payload(),
            "merge_guard.py": self.payload(
                tool_name="Bash", tool_input={"command": "gh pr merge 7"}
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
        for script in ("session_context.py", "stop_guard.py", "merge_guard.py"):
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


class TestStdlibOnly(unittest.TestCase):
    ALLOWED = {"ast", "json", "os", "pathlib", "re", "subprocess", "sys", "cairn_common"}

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
