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

    def test_hooks_json_wires_the_two_hooks(self):
        with open(os.path.join(HOOKS, "hooks.json"), encoding="utf-8") as handle:
            wired = json.load(handle)["hooks"]
        self.assertEqual(sorted(wired), ["PreToolUse", "SessionStart"])
        self.assertIn("hooks/session_start.py", wired["SessionStart"][0]["hooks"][0]["command"])
        guard = wired["PreToolUse"][0]
        self.assertIn("hooks/guest_guard.py", guard["hooks"][0]["command"])
        self.assertRegex("Bash", "^(%s)$" % guard["matcher"])
        self.assertRegex("mcp__t3-code__pull_request_merge", "^(%s)$" % guard["matcher"])
        self.assertNotRegex("mcp__t3-code__pull_request_create", "^(%s)$" % guard["matcher"])


GUARD = os.path.join(HOOKS, "guest_guard.py")
MERGE_TOOL = "mcp__t3-code__pull_request_merge"


class GuestGuard(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = os.path.realpath(self.tmp.name)
        self.home_root = os.path.join(root, "home")
        self.top = os.path.join(root, "checkout")
        os.makedirs(self.top)
        self.git("init", "-q")
        self.git("remote", "add", "origin", "https://github.com/hosts/proj.git")
        self.git("remote", "add", "fork", "https://github.com/me/proj.git")
        self.git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/trunk")
        self.branch("fix-thing")
        self.home = os.path.join(self.home_root, "hosts", "proj")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.top, check=True, capture_output=True)

    def branch(self, name):
        self.git("symbolic-ref", "HEAD", "refs/heads/" + name)

    def guest(self, profile="# Profile\n\n## Verify\n"):
        write(os.path.join(self.home, "ROADMAP.md"), "# Roadmap\n")
        write(os.path.join(self.home, "PROFILE.md"), profile)

    def maintainer(self):
        self.guest("# Profile\n\nMaintainer: yes\n\n## Verify\n")

    def ask(self, command=None, tool="Bash", stdin=None):
        if stdin is None:
            data = {"hook_event_name": "PreToolUse", "tool_name": tool, "cwd": self.top,
                    "tool_input": {"command": command} if command is not None else {"number": 12}}
            stdin = json.dumps(data)
        done = subprocess.run(
            [sys.executable, GUARD], input=stdin, capture_output=True, text=True,
            env=dict(os.environ, CAIRN_HOME=self.home_root), cwd=self.top)
        self.assertEqual(done.returncode, 0, done.stderr)
        if not done.stdout:
            return None
        answer = json.loads(done.stdout)["hookSpecificOutput"]
        self.assertEqual((answer["hookEventName"], answer["permissionDecision"]), ("PreToolUse", "deny"))
        return answer["permissionDecisionReason"]

    def assertDenied(self, command, word):
        reason = self.ask(command)
        self.assertIsNotNone(reason, command)
        self.assertIn(word, reason)

    def assertAllowed(self, command):
        self.assertIsNone(self.ask(command), command)

    def test_nothing_is_denied_outside_a_guest_repo(self):
        for command in ("git push origin trunk", "gh pr merge 12 --squash", "git push --force"):
            self.assertAllowed(command)
        write(os.path.join(self.top, "cairn", "ROADMAP.md"), "# Roadmap\n")  # the user's own repo
        self.branch("trunk")
        for command in ("git push origin trunk", "git push", "gh pr merge 12 --squash"):
            self.assertAllowed(command)
        self.assertIsNone(self.ask(tool=MERGE_TOOL))

    def test_a_push_that_names_the_default_branch_is_denied(self):
        self.guest()
        for command in (
            "git push origin trunk",
            "git push origin HEAD:trunk",
            "git push origin fix-thing:refs/heads/trunk",
            "git push -f origin +trunk",
            "git push origin fix-thing trunk",
            "git push origin --delete trunk",
            "cd pkg && git push origin trunk",
            "GIT_TRACE=1 git push origin trunk",
            "git --no-verify push origin 'trunk'",
            "git push --all origin",
        ):
            self.assertDenied(command, "default branch")

    def test_a_push_of_a_work_branch_is_let_through(self):
        self.guest()
        for command in (
            "git push",
            "git push -u fork fix-thing",
            "git push origin fix-thing",
            "git push origin HEAD",
            "git push fork HEAD:fix-thing --force-with-lease",
            "git push origin main",  # this repo's default branch is trunk
            "echo git push origin trunk",
            "git push origin fix-thing -o trunk",
            "git log origin/trunk..HEAD",
        ):
            self.assertAllowed(command)

    def test_a_bare_push_on_the_default_branch_is_denied(self):
        self.guest()
        self.branch("trunk")
        for command in ("git push", "git push origin", "git push origin HEAD", "git push -u origin"):
            self.assertDenied(command, "default branch")
        self.assertAllowed("git push --tags")
        self.assertAllowed("git push fork trunk:fix-thing")

    def test_main_and_master_stand_in_when_the_default_is_unknown(self):
        self.guest()
        self.git("symbolic-ref", "--delete", "refs/remotes/origin/HEAD")
        self.assertDenied("git push origin main", "default branch")
        self.assertDenied("git push origin master", "default branch")
        self.assertAllowed("git push origin trunk")

    def test_a_merge_is_denied_without_the_maintainer_line(self):
        self.guest()
        for command in (
            "gh pr merge 12 --squash",
            "gh pr merge",
            "gh pr checks 12 && gh pr merge 12 --merge",
            "gh api -X PUT repos/hosts/proj/pulls/12/merge",
        ):
            self.assertDenied(command, "Maintainer: yes")
        self.assertIn("Maintainer: yes", self.ask(tool=MERGE_TOOL))

    def test_other_pr_commands_are_let_through(self):
        self.guest()
        for command in ("gh pr view 12", "gh pr create --fill", "gh pr checks 12",
                        "gh api repos/hosts/proj/pulls/12", "echo gh pr merge 12"):
            self.assertAllowed(command)
        self.assertIsNone(self.ask(tool="mcp__t3-code__pull_request_create"))

    def test_a_maintainer_may_merge_and_still_may_not_push_the_default_branch(self):
        self.maintainer()
        self.assertAllowed("gh pr merge 12 --squash")
        self.assertIsNone(self.ask(tool=MERGE_TOOL))
        self.assertDenied("git push origin trunk", "default branch")
        self.assertDenied("git push origin trunk && gh pr merge 12", "default branch")

    def test_a_maintainer_line_that_is_not_yes_does_not_count(self):
        self.guest("# Profile\n\nMaintainer: no\n")
        self.assertDenied("gh pr merge 12", "Maintainer: yes")

    def test_garbage_input_never_fails_and_never_denies(self):
        self.guest()
        for stdin in ("", "not json", "[1]", "null", json.dumps({"tool_name": "Bash"}),
                      json.dumps({"tool_name": "Bash", "tool_input": {"command": 5}})):
            self.assertIsNone(self.ask(stdin=stdin), stdin)


if __name__ == "__main__":
    unittest.main()
