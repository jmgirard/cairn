"""Tests for scripts/cairn_versions.py (M303).

Drives the script as a subprocess against a temporary git repo whose history
is built per test: a marker file `_extensions/x/_extension.yml` whose
`version:` line changes over first-parent commits on `main`. The cases are
the ones M303's AC3 names: three versions with one tagged, a commit that
leaves the version unchanged, a version raised, reverted, and raised again,
a quoted value, an annotated and a lightweight tag, early commits without
the file, and a tip file with no `version:` line.

Run: python3 -m unittest discover -s scripts/tests
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE.parent / "cairn_versions.py"
MARKER = "_extensions/x/_extension.yml"
WHO = ["-c", "user.email=t@t", "-c", "user.name=t", "-c", "commit.gpgsign=false", "-c", "tag.gpgsign=false"]


@unittest.skipUnless(shutil.which("git"), "git not available")
class VersionsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name) / "repo"
        self.root.mkdir()
        self.clock = 0
        self.git("init", "-q", "-b", "main")

    def tearDown(self):
        self.tmp.cleanup()

    def git(self, *args):
        # Each call moves a fixed clock one minute on, so commit dates follow
        # creation order and a date-ordered walk is predictable.
        self.clock += 1
        stamp = f"{1700000000 + 60 * self.clock} +0000"
        env = {**os.environ, "GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp}
        out = subprocess.run(["git", "-C", str(self.root), *WHO, *args], check=True, capture_output=True, text=True, env=env)
        return out.stdout.strip()

    def commit(self, message, version=None, other=None, line=None, raw=None):
        """Commit a change: a marker `version:` value (or a whole `line`, or
        the file's `raw` text), or a change to an unrelated file. Returns the
        new commit's sha."""
        if version is not None or line is not None or raw is not None:
            path = self.root / MARKER
            path.parent.mkdir(parents=True, exist_ok=True)
            body = line if line is not None else f"version: {version}"
            text = raw if raw is not None else f"title: X\nauthor: T\n{body}\ncontributes:\n  filters:\n    - x.lua\n"
            path.write_text(text, encoding="utf-8")
        if other is not None:
            (self.root / "README.md").write_text(other)
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), MARKER, "--root", str(self.root), *args],
            capture_output=True,
            text=True,
        )

    def tip(self, *args):
        proc = self.run_script(*args)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return dict(line.split(" ", 1) for line in proc.stdout.splitlines())

    def test_three_versions_one_tagged(self):
        first = self.commit("one", version="0.1.0")
        self.git("tag", "v0.1.0", first)
        self.commit("two", version="0.2.0")
        third = self.commit("three", version="0.3.0")
        self.assertEqual(self.tip(), {"version": "0.3.0", "start": third, "tag": "absent"})
        # --at reads an earlier tip: the tagged version, its run start, present.
        self.assertEqual(self.tip("--at", first), {"version": "0.1.0", "start": first, "tag": "present"})

    def test_unchanged_commit_keeps_the_run_start(self):
        raised = self.commit("raise", version="1.0.0")
        plain = self.commit("docs", other="hello\n")
        self.assertEqual(self.tip()["start"], raised)
        self.assertEqual(self.run_script("--changed-by", plain).stdout, "")
        self.assertEqual(self.run_script("--changed-by", raised).stdout, "1.0.0\n")

    def test_raised_reverted_raised_again_starts_at_the_last_raise(self):
        self.commit("base", version="0.3.0")
        self.commit("raise", version="0.4.0")
        reverted = self.commit("revert", version="0.3.0")
        again = self.commit("raise again", version="0.4.0")
        self.assertEqual(self.tip(), {"version": "0.4.0", "start": again, "tag": "absent"})
        # The revert set 0.3.0, and its run start is the revert itself.
        self.assertEqual(self.run_script("--changed-by", reverted).stdout, "0.3.0\n")
        self.assertEqual(self.tip("--at", reverted)["start"], reverted)

    def test_quoted_values(self):
        double = self.commit("double", line='version: "1.2.3"')
        self.assertEqual(self.tip(), {"version": "1.2.3", "start": double, "tag": "absent"})
        single = self.commit("single", line="version: '1.2.4' # bump")
        self.assertEqual(self.tip()["version"], "1.2.4")
        # A quoting change alone leaves the version the same.
        self.commit("unquote", line="version: 1.2.4")
        self.assertEqual(self.tip()["start"], single)

    def test_a_byte_order_mark_before_the_first_line_is_ignored(self):
        bom = self.commit("bom", raw="﻿version: 3.0.0\ntitle: X\n")
        self.assertEqual(self.tip(), {"version": "3.0.0", "start": bom, "tag": "absent"})

    def test_a_version_that_is_not_a_plain_version_is_an_error(self):
        # The value reaches `git tag` in the release walk, so a value outside
        # the plain-version shape is refused rather than printed.
        sha = self.commit("odd", line="version: 1.0;touch_x")
        proc = self.run_script()
        self.assertEqual(proc.returncode, 2)
        self.assertIn("1.0;touch_x", proc.stderr)
        self.assertEqual(proc.stdout, "")
        proc = self.run_script("--changed-by", sha)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")

    def test_the_shape_check_takes_real_versions_and_refuses_bad_tags(self):
        # Each refused value would make a tag git refuses, a `vv` prefix, or
        # a part that does not start and end with a letter or digit.
        for bad in ("1.0.", "1..0", "1.0.lock", "v1.0.0", ".1.0", "1.0-"):
            with self.subTest(value=bad):
                self.commit(f"bad {bad}", line=f"version: '{bad}'")
                proc = self.run_script()
                self.assertEqual(proc.returncode, 2)
                self.assertIn(bad, proc.stderr)
        for good in ("1.0.0-rc.1", "2024.10.1", "1.0.0+build.5", "0.1.0.9000"):
            with self.subTest(value=good):
                self.commit(f"good {good}", line=f"version: {good}")
                self.assertEqual(self.tip()["version"], good)

    def test_a_shallow_clone_is_an_error(self):
        for v in ("0.1.0", "0.2.0", "0.3.0"):
            self.commit(v, version=v)
        shallow = pathlib.Path(self.tmp.name) / "copy"
        subprocess.run(
            ["git", "clone", "-q", "--depth", "1", f"file://{self.root}", str(shallow)],
            check=True,
            capture_output=True,
        )
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), MARKER, "--root", str(shallow)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("is a shallow clone", proc.stderr)
        self.assertNotIn("not a git repository", proc.stderr)
        self.assertEqual(proc.stdout, "")

    def test_annotated_and_lightweight_tags_both_count(self):
        light = self.commit("light", version="2.0.0")
        self.git("tag", "v2.0.0", light)
        self.assertEqual(self.tip()["tag"], "present")
        annotated = self.commit("annotated", version="2.0.1")
        self.assertEqual(self.tip()["tag"], "absent")
        self.git("tag", "-a", "v2.0.1", annotated, "-m", "v2.0.1")
        self.assertEqual(self.tip()["tag"], "present")

    def test_early_commits_without_the_file_are_skipped(self):
        empty = self.commit("readme", other="start\n")
        added = self.commit("add the extension", version="0.0.1")
        self.assertEqual(self.tip(), {"version": "0.0.1", "start": added, "tag": "absent"})
        # The commit that adds the file sets its first version.
        self.assertEqual(self.run_script("--changed-by", added).stdout, "0.0.1\n")
        self.assertEqual(self.run_script("--changed-by", empty).stdout, "")

    def test_early_commit_without_the_line_is_skipped(self):
        self.commit("no line yet", line="# version comes later")
        added = self.commit("line", version="0.1.0")
        self.assertEqual(self.tip()["start"], added)

    def test_tip_without_a_version_line_is_an_error_naming_the_file(self):
        self.commit("one", version="0.1.0")
        self.commit("drop it", line="# no version here")
        proc = self.run_script()
        self.assertEqual(proc.returncode, 2)
        self.assertIn(MARKER, proc.stderr)
        self.assertEqual(proc.stdout, "")

    def test_first_parent_history_ignores_a_merged_side_branch(self):
        base = self.commit("base", version="1.0.0")
        self.commit("main docs", other="x\n")
        self.git("checkout", "-q", "-b", "side", base)
        side_raise = self.commit("side raise", version="1.1.0")
        (self.root / "NOTES.md").write_text("y\n")
        self.commit("side docs")
        self.git("checkout", "-q", "main")
        self.git("merge", "-q", "--no-ff", "-m", "merge side", "side")
        merge = self.git("rev-parse", "HEAD")
        # By date the side commits come right after the merge, so a walk
        # without --first-parent would start 1.1.0 at the side raise. On
        # first-parent history the merge is where 1.1.0 enters main.
        self.assertEqual(self.tip(), {"version": "1.1.0", "start": merge, "tag": "absent"})
        self.assertNotEqual(self.tip()["start"], side_raise)
        self.assertEqual(self.run_script("--changed-by", merge).stdout, "1.1.0\n")

    def test_tip_without_the_file_is_an_error_naming_it(self):
        self.commit("readme only", other="x\n")
        proc = self.run_script()
        self.assertEqual(proc.returncode, 2)
        self.assertIn(MARKER, proc.stderr)
        self.assertIn("missing", proc.stderr)

    def test_root_that_is_not_a_repository_is_an_error_naming_it(self):
        with tempfile.TemporaryDirectory() as other:
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), MARKER, "--root", other],
                capture_output=True,
                text=True,
            )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("not a git repository", proc.stderr)
        self.assertIn(other, proc.stderr)

    def test_at_with_changed_by_is_a_usage_error(self):
        sha = self.commit("one", version="0.1.0")
        proc = self.run_script("--at", sha, "--changed-by", sha)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("usage:", proc.stderr)

    def test_unknown_revision_is_an_error(self):
        self.commit("one", version="0.1.0")
        proc = self.run_script("--changed-by", "0" * 40)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("0" * 40, proc.stderr)


if __name__ == "__main__":
    unittest.main()
