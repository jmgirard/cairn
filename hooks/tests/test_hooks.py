"""Tests for hooks/session_start.py, run as the harness runs it: a
subprocess fed the hook's JSON on stdin.

Each test builds a throwaway git checkout and a throwaway home root (the
CAIRN_HOME variable), so nothing under the real ~/.cairn is read or written.

    python3 -m unittest discover -s hooks/tests
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HOOKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
HOOK = os.path.join(HOOKS, "session_start.py")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


class SessionStart(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = os.path.realpath(self.tmp.name)
        self.home_root = os.path.join(root, "home")
        self.top = os.path.join(root, "checkout")
        os.makedirs(self.top)
        self.git("init", "-q")
        self.git("symbolic-ref", "HEAD", "refs/heads/add-export")
        self.git("remote", "add", "origin", "git@github.com:me/proj.git")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.top, check=True, capture_output=True)

    def run_hook(self, stdin=None, cwd=None):
        if stdin is None:
            stdin = json.dumps({"hook_event_name": "SessionStart", "cwd": self.top})
        env = dict(os.environ, CAIRN_HOME=self.home_root)
        done = subprocess.run(
            [sys.executable, HOOK],
            input=stdin,
            capture_output=True,
            text=True,
            env=env,
            cwd=cwd or self.top,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout

    def context(self, out):
        payload = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(payload["hookEventName"], "SessionStart")
        return payload["additionalContext"]

    def test_silent_outside_a_cairn_repo(self):
        self.assertEqual(self.run_hook(), "")

    def test_own_repo_gets_the_listing(self):
        write(
            os.path.join(self.top, "cairn", "ROADMAP.md"),
            "# Roadmap\n\n- [high] Fix wrong totals (#12): Sums ignore weights.\n",
        )
        home = os.path.join(self.home_root, "me", "proj")
        plan = os.path.join(home, "plans", "add-export.md")
        write(
            plan,
            "# add-export\n\nRoute: road\nBranch: add-export\nIssue:\n"
            "Phase: build\nBlocked on: arrow 15\n\n## What is wrong or wanted\n\n"
            "BODY TEXT THAT MUST NOT BE INJECTED\n",
        )
        text = self.context(self.run_hook())
        self.assertIn("Home folder: %s" % home, text)
        self.assertIn(
            "- add-export · road · build · branch add-export · BLOCKED on: arrow 15",
            text,
        )
        self.assertIn("- Fix wrong totals (#12)", text)
        self.assertIn("Candidates: 1 (1 high, 0 blocked)", text)
        self.assertIn("Plan for this branch (add-export): %s" % plan, text)
        self.assertNotIn("BODY TEXT", text)
        self.assertNotIn("Sums ignore weights", text)

    def test_cwd_comes_from_the_hook_input(self):
        write(os.path.join(self.top, "cairn", "ROADMAP.md"), "# Roadmap\n")
        with tempfile.TemporaryDirectory() as elsewhere:
            out = self.run_hook(cwd=elsewhere)
        self.assertIn("cairn: me/proj (own repo)", self.context(out))

    def test_v2_repo_is_named_and_pointed_to_setup(self):
        write(os.path.join(self.top, "cairn", "ROADMAP.md"), "# Roadmap\n")
        write(os.path.join(self.top, "cairn", "DECISIONS.md"), "# Decisions\n")
        text = self.context(self.run_hook())
        self.assertIn("cairn v2 files", text)
        self.assertIn("`/cairn setup`", text)
        self.assertNotIn("Candidates:", text)

    def test_garbage_input_never_fails(self):
        write(os.path.join(self.top, "cairn", "ROADMAP.md"), "# Roadmap\n")
        for stdin in ("", "not json", "[1, 2]", "null"):
            out = self.run_hook(stdin=stdin)
            self.assertIn("cairn: me/proj (own repo)", self.context(out), stdin)

    def test_hooks_json_wires_only_session_start(self):
        with open(os.path.join(HOOKS, "hooks.json"), encoding="utf-8") as handle:
            wired = json.load(handle)["hooks"]
        self.assertEqual(list(wired), ["SessionStart"])
        command = wired["SessionStart"][0]["hooks"][0]["command"]
        self.assertIn("hooks/session_start.py", command)


if __name__ == "__main__":
    unittest.main()
