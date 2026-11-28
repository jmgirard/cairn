"""Tests for scripts/cairn_migrate.py.

Each test builds a throwaway v2 repo and a throwaway home root (the
CAIRN_HOME variable), so nothing under the real ~/.cairn is touched.

    python3 -m unittest discover -s scripts/tests
"""

import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import cairn_migrate as cm  # noqa: E402
import cairn_status as cs  # noqa: E402

ROADMAP = """# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-11-01_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M004 | Add a parquet export | in-progress | — | high | milestones/M004-add-export.md |
| M005 | Do a later thing | planned | M004 | normal | milestones/M005-later-thing.md |
| M006 | Wait for the export | blocked | M004 | normal | milestones/M006-wait-thing.md |
| M003 | An old thing | done | — | normal | milestones/archive/M003-old-thing.md |

## Candidates
<!-- unnumbered ideas; one line each -->
_Ordered high, normal, low, parked._
- [high] Fix wrong totals for weighted counts (#12): Sums ignore weights.
- Add a dark theme: Some users want one,
  and it would be simple.
- [low] Tidy the print method: The output wraps badly.
- [parked] Support the arrow backend: Promote when arrow 15 ships.
"""

PROFILE = """# Toolchain profile: r-package
# Collaboration mode: guest
# Push remote: base

<!-- a comment -->
Some prose about the toolchain.

## verify
Run `devtools::test()`.

## consistency-gate
- `devtools::check()` clean.

## test-doctrine
Layered rules.

## release-walk
The CRAN walk.

## init-detection
DESCRIPTION.

## greenfield-openers
None.

## changelog
`NEWS.md`.
"""

CLAUDE = """# CLAUDE.md for proj

## Dev workflow

Run the tests.

<!-- Appended to the repo's CLAUDE.md by /cairn-init. Keep the section body
     under ~25 lines. -->

## Project tracking (cairn)

This repo uses the cairn plugin. Invoke `/milestone-plan` first.

- **User-visible bug**: invoke `/hotfix`.

## Out of scope

Nothing else.
"""


def plan_file(number, title, status, where="—", resolves="—"):
    return (
        "# M%s: %s\n\n- **Status:** %s\n- **Priority:** normal\n- **Depends on:** —\n"
        "- **Resolves:** %s\n- **Branch/PR:** %s\n\n## Goal\n\nOne sentence.\n\n"
        "## Work log\n\n- 2026-11-01: created.\n" % (number, title, status, resolves, where)
    )


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = os.path.realpath(self.tmp.name)
        self.home_root = os.path.join(root, "home")
        self.top = os.path.join(root, "checkout")
        os.makedirs(self.top)
        old = os.environ.get("CAIRN_HOME")
        os.environ["CAIRN_HOME"] = self.home_root
        self.addCleanup(lambda: os.environ.pop("CAIRN_HOME", None) if old is None
                        else os.environ.__setitem__("CAIRN_HOME", old))
        self.git("init", "-q", "-b", "main")
        self.git("remote", "add", "origin", "https://github.com/hosts/proj.git")

    def git(self, *args, cwd=None):
        done = subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
            cwd=cwd or self.top, capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout

    def path(self, *parts):
        return os.path.join(self.top, *parts)

    def cairn_files(self):
        write(self.path("cairn", "ROADMAP.md"), ROADMAP)
        write(self.path("cairn", "PROFILE.md"), PROFILE)
        write(self.path("cairn", "DECISIONS.md"), "# Decisions\n")
        write(self.path("cairn", "LESSONS.md"), "# Lessons\n")
        write(self.path("cairn", "DESIGN.md"), "# Design\n\n## Known issues\n\n- One.\n")
        write(self.path("cairn", "milestones", "M004-add-export.md"), plan_file(
            "004", "Add a parquet export", "in-progress",
            where="add-export — https://github.com/hosts/proj/pull/12", resolves="#9 closes, #8 partial"))
        write(self.path("cairn", "milestones", "M005-later-thing.md"), plan_file(
            "005", "Do a later thing", "planned"))
        write(self.path("cairn", "milestones", "M006-wait-thing.md"), plan_file(
            "006", "Wait for the export", "blocked", where="`wait-thing`"))
        write(self.path("cairn", "milestones", "archive", "M003-old-thing.md"), "# M003\n")
        write(self.path("cairn", "reviews", "archive", "RB01.md"), "# RB01\n")
        write(self.path("cairn", "references", "INDEX.md"), "# References index\n\n- a.md — a source\n")
        write(self.path("cairn", "references", "a.md"), "# a\n")
        write(self.path("cairn", "references", "sources", "a.pdf"), "pdf bytes")

    def own(self):
        self.cairn_files()
        write(self.path("CLAUDE.md"), CLAUDE)
        write(self.path(".gitignore"), "cairn/references/sources/\n")
        write(self.path("R", "code.R"), "x <- 1\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "v2 state")
        return os.path.join(self.home_root, "hosts", "proj")

    def guest(self):
        write(self.path("R", "code.R"), "x <- 1\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "host state")
        self.cairn_files()
        write(self.path("cairn", "drafts", "note.md"), "a draft\n")
        self.exclude = self.path(".git", "info", "exclude")
        write(self.exclude, "# git ls-files --others\n*.tmp\ncairn/\n.claude/worktrees/\n")
        return os.path.join(self.home_root, "hosts", "proj")

    def run_main(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = cm.main(["cairn_migrate.py", "-C", self.top, *args])
        return code, out.getvalue()


class Conversions(unittest.TestCase):
    def test_roadmap_keeps_candidates_and_drops_old_tags(self):
        text, rows, tags = cm.convert_roadmap(ROADMAP)
        self.assertEqual(text, (
            "# Roadmap\n\n"
            "- [high] Fix wrong totals for weighted counts (#12): Sums ignore weights.\n"
            "- Add a dark theme: Some users want one, and it would be simple.\n"
            "- Tidy the print method: The output wraps badly.\n"
            "- Support the arrow backend: Promote when arrow 15 ships.\n"
        ))
        self.assertEqual((rows, tags), (4, 2))

    def test_roadmap_with_no_candidates(self):
        self.assertEqual(cm.convert_roadmap("# Roadmap\n\n## Milestones\n- not a row\n"), ("# Roadmap\n", 0, 0))

    def test_profile_keeps_three_sections_as_written(self):
        self.assertEqual(cm.convert_profile(PROFILE), (
            "# Profile\n\n"
            "## Verify\n\nRun `devtools::test()`.\n\n- `devtools::check()` clean.\n\n"
            "## Changelog\n\n`NEWS.md`.\n\n"
            "## Release\n\nThe CRAN walk.\n"
        ))

    def test_profile_section_that_is_missing_says_none(self):
        self.assertIn("## Release\n\nnone\n", cm.convert_profile("# x\n\n## verify\nmake test\n"))

    def test_claude_section_is_swapped_and_the_rest_kept(self):
        text, swapped = cm.swap_section(CLAUDE, "## Project tracking (cairn)\n\nNEW TEXT\n")
        self.assertTrue(swapped)
        self.assertEqual(text, (
            "# CLAUDE.md for proj\n\n## Dev workflow\n\nRun the tests.\n\n"
            "## Project tracking (cairn)\n\nNEW TEXT\n\n"
            "## Out of scope\n\nNothing else.\n"
        ))

    def test_claude_section_at_the_end_of_the_file(self):
        text, swapped = cm.swap_section(
            "## Project tracking (cairn)\n\nold\n- old\n", "## Project tracking (cairn)\n\nNEW\n")
        self.assertEqual((text, swapped), ("## Project tracking (cairn)\n\nNEW\n", True))

    def test_claude_without_the_section_is_left_alone(self):
        self.assertEqual(cm.swap_section("# Notes\n\nSee Project tracking (cairn).\n", "x"),
                         ("# Notes\n\nSee Project tracking (cairn).\n", False))

    def test_an_unrelated_comment_above_the_section_is_kept(self):
        text, _ = cm.swap_section(
            "<!-- keep me -->\n\n## Project tracking (cairn)\n\nold\n", "## Project tracking (cairn)\n\nNEW\n")
        self.assertTrue(text.startswith("<!-- keep me -->\n"))

    def test_plan_slug_drops_the_number(self):
        self.assertEqual(cm.plan_slug("milestones/M007-ordinal-tied-map-ses.md"), "ordinal-tied-map-ses")

    def test_blocked_work_with_no_branch_has_not_started(self):
        row = {"id": "M163", "title": "Forms", "status": "blocked", "depends": "M162",
               "path": "milestones/M163-pid5ffbf-forms.md"}
        slug, text = cm.convert_plan(plan_file("163", "Forms", "blocked"), row, {"M163": "Forms"})
        self.assertEqual(slug, "pid5ffbf-forms")
        self.assertIn("\nBranch:\nIssue:\nPhase: plan\nBlocked on: M162, a v2 plan now in the archive\n", text)

    def test_blocked_work_with_an_open_pr_waits_on_github(self):
        row = {"id": "M007", "title": "Tied", "status": "blocked", "depends": "—",
               "path": "milestones/M007-tied-map.md"}
        _, text = cm.convert_plan(plan_file(
            "007", "Tied", "blocked", where="tied-map — https://github.com/h/p/pull/1371"), row, {})
        self.assertIn("\nBranch: tied-map\nIssue:\nPhase: pr #1371\nBlocked on:\n", text)

    def test_shipped_section_template_has_the_heading(self):
        self.assertTrue(cm.template("claude-md-section.md").startswith(cm.SECTION_HEADING + "\n"))


class OwnRepo(Base):
    def test_a_dry_run_changes_nothing(self):
        home = self.own()
        code, out = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("hosts/proj (the user's own repo)", out)
        self.assertIn("Would do:", out)
        self.assertIn("Nothing was changed.", out)
        self.assertEqual(self.git("status", "--short"), "")
        self.assertFalse(os.path.exists(home))
        self.assertTrue(os.path.isfile(self.path("cairn", "references", "sources", "a.pdf")))

    def test_apply_converts_and_stages_without_committing(self):
        home = self.own()
        head = self.git("rev-parse", "HEAD")
        code, out = self.run_main("--apply")
        self.assertEqual(code, 0, out)
        self.assertIn("The changes are staged and not committed.", out)
        self.assertEqual(self.git("rev-parse", "HEAD"), head)

        for gone in ("DECISIONS.md", "LESSONS.md", "milestones", "reviews", os.path.join("references", "sources")):
            self.assertFalse(os.path.exists(self.path("cairn", gone)), gone)
        for kept in (("DECISIONS.md",), ("LESSONS.md",), ("milestones", "archive", "M003-old-thing.md"),
                     ("reviews", "archive", "RB01.md")):
            self.assertTrue(os.path.isfile(self.path("cairn", "archive", *kept)), kept)
        self.assertFalse(os.path.exists(self.path("cairn", "archive", "milestones", "M004-add-export.md")))

        self.assertEqual(read(self.path("cairn", "ROADMAP.md")), cm.convert_roadmap(ROADMAP)[0])
        self.assertEqual(read(self.path("cairn", "PROFILE.md")), cm.convert_profile(PROFILE))
        claude = read(self.path("CLAUDE.md"))
        self.assertIn("`/cairn start`", claude)
        self.assertNotIn("/milestone-plan", claude)
        self.assertNotIn("cairn-init", claude)
        self.assertIn("## Dev workflow\n\nRun the tests.", claude)
        self.assertTrue(claude.endswith("## Out of scope\n\nNothing else.\n"))

        self.assertEqual(read(os.path.join(home, "shelf", "a.pdf")), "pdf bytes")
        self.assertEqual(sorted(os.listdir(os.path.join(home, "plans"))),
                         ["add-export.md", "later-thing.md", "wait-thing.md"])
        status = self.git("status", "--short")
        self.assertNotRegex(status, r"(?m)^.[MD?]")  # everything staged, nothing left unstaged
        self.assertIn("D  cairn/milestones/M004-add-export.md", status)

    def test_plans_get_their_labeled_lines_and_keep_their_body(self):
        home = self.own()
        self.run_main("--apply")
        plans, problems = cs.read_plans(home)
        self.assertEqual(problems, [])
        by = {p["slug"]: p for p in plans}
        self.assertEqual(
            [by["add-export"][k] for k in ("Route", "Branch", "Issue", "Phase", "Blocked on")],
            ["road", "add-export", "#9", "pr #12", None])
        self.assertEqual(
            [by["later-thing"][k] for k in ("Branch", "Phase", "Blocked on")], [None, "plan", None])
        self.assertEqual(
            [by["wait-thing"][k] for k in ("Branch", "Phase", "Blocked on")],
            ["wait-thing", "build", "Add a parquet export"])
        text = read(os.path.join(home, "plans", "add-export.md"))
        self.assertTrue(text.startswith("# add-export\n\nRoute: road\n"))
        self.assertTrue(text.endswith(plan_file(
            "004", "Add a parquet export", "in-progress",
            where="add-export — https://github.com/hosts/proj/pull/12", resolves="#9 closes, #8 partial")))

    def test_the_status_listing_has_no_problem_lines_afterwards(self):
        self.own()
        self.run_main("--apply")
        listing = cs.render(cs.resolve(self.top))
        self.assertIn("cairn: hosts/proj (own repo)", listing)
        self.assertIn("Work in flight (3):", listing)
        self.assertIn("Candidates: 4 (1 high, 0 blocked)", listing)
        self.assertNotIn("Problems", listing)

    def test_notes_tell_the_session_what_is_left_to_judge(self):
        self.own()
        _, out = self.run_main()
        self.assertIn("2 rows lost a `[low]` or `[parked]` tag", out)
        self.assertIn("Check the `Blocked on:` line of plan wait-thing.", out)
        self.assertIn("DESIGN.md has a Known issues section", out)

    def test_a_plan_already_in_the_home_folder_stops_everything(self):
        home = self.own()
        write(os.path.join(home, "plans", "add-export.md"), "mine\n")
        code, out = self.run_main("--apply")
        self.assertEqual(code, 1)
        self.assertIn("already exists", out)
        self.assertEqual(self.git("status", "--short"), "")
        self.assertEqual(read(os.path.join(home, "plans", "add-export.md")), "mine\n")

    def test_a_linked_worktree_is_refused(self):
        self.own()
        other = os.path.join(os.path.dirname(self.top), "linked")
        self.git("worktree", "add", "-q", other, "-b", "side")
        out = io.StringIO()
        with redirect_stdout(out):
            code = cm.main(["cairn_migrate.py", "-C", other, "--apply"])
        self.assertEqual(code, 1)
        self.assertIn("main checkout", out.getvalue())

    def test_a_repo_that_is_not_v2_is_refused(self):
        write(self.path("cairn", "ROADMAP.md"), "# Roadmap\n")
        code, out = self.run_main("--apply")
        self.assertEqual(code, 1)
        self.assertIn("not cairn v2 files", out)

    def test_no_usable_remote_is_refused(self):
        self.own()
        self.git("remote", "remove", "origin")
        code, out = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("home folder cannot be found", out)

    def test_usage(self):
        self.assertEqual(self.run_main("--bogus")[0], 2)


class GuestRepo(Base):
    def test_a_dry_run_changes_nothing(self):
        home = self.guest()
        code, out = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("hosts/proj (a guest repo)", out)
        self.assertTrue(os.path.isdir(self.path("cairn")))
        self.assertIn("cairn/\n", read(self.exclude))
        self.assertFalse(os.path.exists(home))

    def test_apply_leaves_nothing_of_cairn_in_the_checkout(self):
        home = self.guest()
        code, out = self.run_main("--apply")
        self.assertEqual(code, 0, out)
        self.assertFalse(os.path.exists(self.path("cairn")))
        self.assertEqual(read(self.exclude), "# git ls-files --others\n*.tmp\n.claude/worktrees/\n")
        self.assertEqual(self.git("status", "--short"), "")
        self.assertFalse(os.path.exists(self.path("CLAUDE.md")))

        self.assertEqual(read(os.path.join(home, "ROADMAP.md")), cm.convert_roadmap(ROADMAP)[0])
        self.assertEqual(read(os.path.join(home, "PROFILE.md")), cm.convert_profile(PROFILE))
        for kept in (("DESIGN.md",), ("references", "INDEX.md"), ("references", "a.md"), ("shelf", "a.pdf"),
                     ("plans", "add-export.md"), ("archive", "DECISIONS.md"), ("archive", "LESSONS.md"),
                     ("archive", "ROADMAP-v2.md"), ("archive", "PROFILE-v2.md"),
                     ("archive", "milestones", "archive", "M003-old-thing.md"),
                     ("archive", "reviews", "archive", "RB01.md"), ("archive", "drafts", "note.md")):
            self.assertTrue(os.path.isfile(os.path.join(home, *kept)), kept)
        self.assertEqual(read(os.path.join(home, "archive", "ROADMAP-v2.md")), ROADMAP)
        self.assertFalse(os.path.exists(os.path.join(home, "references", "sources")))

    def test_the_status_listing_reads_the_guest_home_afterwards(self):
        self.guest()
        self.run_main("--apply")
        listing = cs.render(cs.resolve(self.top))
        self.assertIn("cairn: hosts/proj (guest repo)", listing)
        self.assertIn("Work in flight (3):", listing)
        self.assertNotIn("Problems", listing)

    def test_upstream_names_the_home_folder_when_it_exists(self):
        self.guest()
        self.git("remote", "add", "upstream", "git@github.com:realhost/proj.git")
        code, out = self.run_main("--apply")
        self.assertEqual(code, 0, out)
        self.assertTrue(os.path.isfile(os.path.join(self.home_root, "realhost", "proj", "ROADMAP.md")))

    def test_a_home_folder_that_already_holds_files_stops_everything(self):
        home = self.guest()
        write(os.path.join(home, "ROADMAP.md"), "mine\n")
        code, out = self.run_main("--apply")
        self.assertEqual(code, 1)
        self.assertTrue(os.path.isfile(self.path("cairn", "ROADMAP.md")))
        self.assertIn("cairn/\n", read(self.exclude))


if __name__ == "__main__":
    unittest.main()
