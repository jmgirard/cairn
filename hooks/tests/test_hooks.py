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
