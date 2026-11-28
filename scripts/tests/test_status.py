"""Tests for scripts/cairn_status.py.

Each test builds a throwaway git checkout and a throwaway home root (the
CAIRN_HOME variable), so nothing under the real ~/.cairn is read or written.

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

import cairn_status as cs  # noqa: E402


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


PLAN = """# {slug}

Route: {route}
Branch: {branch}
Issue: {issue}
Phase: {phase}
Blocked on: {blocked}

## What is wrong or wanted

Route: road
"""


def plan_text(slug, route="trail", branch=None, issue="", phase="build", blocked=""):
    return PLAN.format(
        slug=slug, route=route, branch=branch or slug, issue=issue,
        phase=phase, blocked=blocked,
    )


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
        self.addCleanup(self._restore, old)
        self.git("init", "-q")
        self.branch("main")

    @staticmethod
    def _restore(old):
        if old is None:
            os.environ.pop("CAIRN_HOME", None)
        else:
            os.environ["CAIRN_HOME"] = old

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.top, check=True, capture_output=True)

    def branch(self, name):
        self.git("symbolic-ref", "HEAD", "refs/heads/" + name)

    def remote(self, name, url):
        self.git("remote", "add", name, url)

    def own(self, roadmap="# Roadmap\n", url="git@github.com:me/proj.git"):
        if url:
            self.remote("origin", url)
        write(os.path.join(self.top, "cairn", "ROADMAP.md"), roadmap)
        return os.path.join(self.home_root, "me", "proj")

    def guest(self, roadmap="# Roadmap\n", profile="# Profile\n"):
        self.remote("origin", "https://github.com/me/host-repo.git")
        self.remote("upstream", "https://github.com/hosts/host-repo")
        home = os.path.join(self.home_root, "hosts", "host-repo")
        write(os.path.join(home, "ROADMAP.md"), roadmap)
        if profile is not None:
            write(os.path.join(home, "PROFILE.md"), profile)
        return home

    def listing(self):
        return cs.render(cs.resolve(self.top))

    def run_main(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            code = cs.main(["cairn_status.py", "-C", self.top, *args])
        return code, out.getvalue().strip()


class RemoteSlug(unittest.TestCase):
    def test_url_forms(self):
        for url in (
            "git@github.com:me/proj.git",
            "https://github.com/me/proj.git",
            "https://github.com/me/proj",
            "https://github.com/me/proj/",
            "ssh://git@github.com/me/proj.git",
        ):
            self.assertEqual(cs.remote_slug(url), ("me", "proj"), url)

    def test_dots_and_dashes_are_kept(self):
        self.assertEqual(
            cs.remote_slug("git@github.com:my-org/a.b_c.git"), ("my-org", "a.b_c")
        )

    def test_unusable_urls(self):
        for url in ("", "proj", "git@github.com:../proj.git", None):
            self.assertIsNone(cs.remote_slug(url), url)


class Resolve(Base):
    def test_outside_a_checkout(self):
        with tempfile.TemporaryDirectory() as plain:
            self.assertIsNone(cs.resolve(plain))

    def test_checkout_without_cairn_files(self):
        self.remote("origin", "git@github.com:me/proj.git")
        repo = cs.resolve(self.top)
        self.assertIsNone(repo.kind)
        self.assertIsNone(cs.render(repo))

    def test_own_repo_uses_origin(self):
        home = self.own()
        self.remote("upstream", "https://github.com/other/proj")
        repo = cs.resolve(self.top)
        self.assertEqual((repo.kind, repo.slug, repo.home), ("own", "me/proj", home))

    def test_guest_repo_uses_upstream(self):
        home = self.guest()
        repo = cs.resolve(self.top)
        self.assertEqual(
            (repo.kind, repo.slug, repo.home), ("guest", "hosts/host-repo", home)
        )

    def test_guest_repo_without_upstream_uses_origin(self):
        self.remote("origin", "https://github.com/hosts/host-repo")
        home = os.path.join(self.home_root, "hosts", "host-repo")
        write(os.path.join(home, "ROADMAP.md"), "# Roadmap\n")
        self.assertEqual(cs.resolve(self.top).kind, "guest")

    def test_subdirectory_resolves_to_the_same_repo(self):
        self.own()
        sub = os.path.join(self.top, "src", "pkg")
        os.makedirs(sub)
        self.assertEqual(cs.resolve(sub).top, self.top)

    def test_v2_repo_gets_the_notice_only(self):
        self.own()
        write(os.path.join(self.top, "cairn", "DECISIONS.md"), "# Decisions\n")
        self.assertEqual(self.listing(), cs.V2_NOTICE)
        os.remove(os.path.join(self.top, "cairn", "DECISIONS.md"))
        os.makedirs(os.path.join(self.top, "cairn", "milestones"))
        self.assertEqual(self.listing(), cs.V2_NOTICE)

    def test_own_repo_without_a_remote_says_so(self):
        self.own(url=None)
        text = self.listing()
        self.assertIn("Home folder: not found", text)
        self.assertIn("Problems (1):", text)
        self.assertIn("home folder cannot be found", text)


class Roadmap(Base):
    def rows(self, text):
        path = os.path.join(self.top, "ROADMAP.md")
        write(path, text)
        return cs.read_roadmap(path)

    def test_rows_marks_and_titles(self):
        rows, problems = self.rows(
            "# Roadmap\n\n"
            "- [high] Fix wrong totals for weighted counts (#12): Sums ignore weights.\n"
            "- [blocked] Add a parquet export: Users ask for it. Waits for arrow 15 (apache/arrow#9).\n"
            "- [blocked] [high] Fix the date parser: Dates shift. Waits for the tz release.\n"
            "- Add a dark theme: Some users want one.\n"
        )
        self.assertEqual(problems, [])
        self.assertEqual(
            [r["title"] for r in rows],
            [
                "Fix wrong totals for weighted counts (#12)",
                "Add a parquet export",
                "Fix the date parser",
                "Add a dark theme",
            ],
        )
        self.assertEqual(
            [r["marks"] for r in rows],
            [["high"], ["blocked"], ["blocked", "high"], []],
        )
        self.assertEqual(rows[1]["waits"], "arrow 15 (apache/arrow#9)")
        self.assertEqual(rows[2]["waits"], "the tz release")
        self.assertIsNone(rows[0]["waits"])

    def test_wrapped_row_is_one_row(self):
        rows, problems = self.rows(
            "- [blocked] Add a parquet export: Users ask for it.\n"
            "  Waits for arrow 15.\n"
            "\nSome prose.\n  indented prose is not a row\n"
        )
        self.assertEqual(problems, [])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["waits"], "arrow 15")

    def test_unknown_mark_is_a_problem_and_the_row_still_counts(self):
        rows, problems = self.rows("- [parked] Add a thing: Because.\n")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Add a thing")
        self.assertEqual(len(problems), 1)
        self.assertIn("line 1", problems[0])
        self.assertIn("[parked]", problems[0])

    def test_row_without_a_title_is_a_problem(self):
        rows, problems = self.rows("# Roadmap\n\n- just some words\n")
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(problems), 1)
        self.assertIn("line 3", problems[0])

    def test_tables_and_headings_are_not_rows(self):
        rows, problems = self.rows(
            "# Roadmap\n\n## Milestones\n| ID | Title |\n|---|---|\n| M1 | x |\n"
        )
        self.assertEqual((rows, problems), ([], []))

    def test_unreadable_roadmap_is_a_problem(self):
        rows, problems = cs.read_roadmap(os.path.join(self.top, "missing.md"))
        self.assertEqual(rows, [])
        self.assertEqual(len(problems), 1)
        self.assertIn("cannot be read", problems[0])


class Plans(Base):
    def test_labeled_lines_stop_at_the_first_heading(self):
        home = self.own()
        write(
            os.path.join(home, "plans", "fix-totals.md"),
            plan_text("fix-totals", issue="#12", blocked="arrow 15"),
        )
        plans, problems = cs.read_plans(home)
        self.assertEqual(problems, [])
        plan = plans[0]
        self.assertEqual(plan["slug"], "fix-totals")
        self.assertEqual(plan["Route"], "trail")  # not the `Route: road` in the body
        self.assertEqual(plan["issue_number"], "12")
        self.assertEqual(plan["Blocked on"], "arrow 15")

    def test_empty_and_none_values_read_as_absent(self):
        home = self.own()
        write(
            os.path.join(home, "plans", "a-plan.md"),
            plan_text("a-plan", issue="none", blocked=""),
        )
        plans, problems = cs.read_plans(home)
        self.assertEqual(problems, [])
        self.assertIsNone(plans[0]["Issue"])
        self.assertIsNone(plans[0]["Blocked on"])

    def test_missing_lines_and_bad_values_are_problems(self):
        home = self.own()
        write(os.path.join(home, "plans", "bare.md"), "# bare\n\nSome text.\n")
        write(
            os.path.join(home, "plans", "odd.md"),
            plan_text("odd", route="hotfix", issue="the tracker one"),
        )
        _, problems = cs.read_plans(home)
        text = "\n".join(problems)
        for needle in (
            "plans/bare.md: no `Route:` line",
            "plans/bare.md: no `Branch:` line",
            "plans/bare.md: no `Phase:` line",
            "plans/odd.md: `Route:` is `hotfix`",
            "plans/odd.md: `Issue:` is `the tracker one`",
        ):
            self.assertIn(needle, text)
        self.assertEqual(len(problems), 5)

    def test_planned_work_needs_no_branch(self):
        home = self.own()
        text = plan_text("later-work", phase="plan").replace("Branch: later-work", "Branch:")
        write(os.path.join(home, "plans", "later-work.md"), text)
        plans, problems = cs.read_plans(home)
        self.assertEqual(problems, [])
        self.assertIsNone(plans[0]["Branch"])
        write(os.path.join(home, "plans", "later-work.md"), text.replace("Phase: plan", "Phase: build"))
        self.assertEqual(len(cs.read_plans(home)[1]), 1)

    def test_unreadable_plan_is_a_problem(self):
        home = self.own()
        path = os.path.join(home, "plans", "broken.md")
        os.makedirs(os.path.dirname(path))
        with open(path, "wb") as handle:
            handle.write(b"\xff\xfe\x00bad")
        plans, problems = cs.read_plans(home)
        self.assertEqual(len(plans), 1)
        self.assertEqual(len(problems), 1)
        self.assertIn("plans/broken.md: cannot be read", problems[0])

    def test_no_plans_folder_is_not_a_problem(self):
        home = self.own()
        self.assertEqual(cs.read_plans(home), ([], []))

    def test_files_that_are_not_plans_are_skipped(self):
        home = self.own()
        write(os.path.join(home, "plans", "notes.txt"), "x")
        write(os.path.join(home, "plans", ".hidden.md"), "x")
        self.assertEqual(cs.read_plans(home), ([], []))


class Listing(Base):
    def test_own_repo_listing(self):
        home = self.own(
            "# Roadmap\n\n"
            "- [high] Fix wrong totals (#12): Sums ignore weights in `total()`.\n"
            "- [blocked] Add a parquet export: Asked for. Waits for arrow 15.\n"
            "- Add a dark theme: Asked for.\n"
        )
        write(
            os.path.join(home, "plans", "fix-totals.md"),
            plan_text("fix-totals", issue="#12", phase="build"),
        )
        write(
            os.path.join(home, "plans", "new-export.md"),
            plan_text("new-export", route="road", phase="plan", blocked="arrow 15"),
        )
        self.branch("fix-totals")
        self.assertEqual(
            self.listing(),
            "\n".join(
                [
                    "cairn: me/proj (own repo)",
                    "Home folder: %s" % home,
                    "",
                    "Work in flight (2):",
                    "- fix-totals · trail · build · branch fix-totals · issue #12",
                    "- new-export · road · plan · branch new-export · BLOCKED on: arrow 15",
                    "",
                    "`[high]` candidates (1):",
                    "- Fix wrong totals (#12)",
                    "",
                    "`[blocked]` candidates (1):",
                    "- Add a parquet export: waits for arrow 15",
                    "",
                    "Candidates: 3 (1 high, 1 blocked)",
                    "",
                    "Plan for this branch (fix-totals): %s"
                    % os.path.join(home, "plans", "fix-totals.md"),
                ]
            ),
        )

    def test_empty_repo_listing(self):
        home = self.own()
        self.assertEqual(
            self.listing(),
            "\n".join(
                [
                    "cairn: me/proj (own repo)",
                    "Home folder: %s" % home,
                    "",
                    "Work in flight: none",
                    "",
                    "Candidates: 0 (0 high, 0 blocked)",
                    "",
                    "Plan for this branch (main): none",
                ]
            ),
        )

    def test_problems_are_listed_once_each(self):
        home = self.own("- [low] Add a thing: Because.\n")
        write(os.path.join(home, "plans", "bare.md"), "# bare\n")
        text = self.listing()
        self.assertIn("Problems (4):", text)
        self.assertIn("- ROADMAP.md line 1: `[low]` is not a mark", text)
        self.assertIn("- bare · no route · no phase · branch none", text)

    def test_guest_listing_reads_the_home_folder(self):
        home = self.guest("- Add a thing: Because.\n")
        text = self.listing()
        self.assertIn("cairn: hosts/host-repo (guest repo)", text)
        self.assertIn("Home folder: %s" % home, text)
        self.assertIn("Candidates: 1 (0 high, 0 blocked)", text)
        self.assertNotIn("Problems", text)

    def test_guest_maintainer_line(self):
        self.guest(profile="# Profile\n\nMaintainer: yes\n\n## Verify\n")
        self.assertIn("(guest repo, `Maintainer: yes`)", self.listing())

    def test_maintainer_line_below_a_heading_does_not_count(self):
        self.guest(profile="# Profile\n\n## Verify\nMaintainer: yes\n")
        self.assertIn("(guest repo)", self.listing())

    def test_guest_without_a_profile_is_a_problem(self):
        self.guest(profile=None)
        self.assertIn("- PROFILE.md: cannot be read", self.listing())

    def test_two_plans_on_one_branch(self):
        home = self.own()
        for slug in ("one-plan", "two-plan"):
            write(
                os.path.join(home, "plans", slug + ".md"),
                plan_text(slug, branch="shared"),
            )
        self.branch("shared")
        self.assertIn(
            "Plan for this branch (shared): 2 plans name it: one-plan, two-plan",
            self.listing(),
        )


class FindPlan(Base):
    def setUp(self):
        super().setUp()
        self.home = self.own()
        self.paths = {}
        for slug, kwargs in (
            ("fix-totals", {"issue": "#12", "branch": "t3/thread-41"}),
            ("fix-dates", {"phase": "pr #30"}),
            ("new-export", {"route": "road"}),
        ):
            path = os.path.join(self.home, "plans", slug + ".md")
            write(path, plan_text(slug, **kwargs))
            self.paths[slug] = path

    def test_current_branch(self):
        self.branch("t3/thread-41")
        self.assertEqual(self.run_main("plan"), (0, self.paths["fix-totals"]))

    def test_current_branch_without_a_plan(self):
        code, out = self.run_main("plan")
        self.assertEqual(code, 1)
        self.assertIn("no plan for branch `main`", out)

    def test_unique_start_of_a_slug(self):
        self.assertEqual(self.run_main("plan", "new"), (0, self.paths["new-export"]))
        self.assertEqual(self.run_main("plan", "fix-t"), (0, self.paths["fix-totals"]))

    def test_ambiguous_start_names_the_matches(self):
        code, out = self.run_main("plan", "fix")
        self.assertEqual(code, 1)
        self.assertIn("2 plans match `fix`: fix-dates, fix-totals", out)

    def test_exact_slug_wins_over_a_longer_one(self):
        path = os.path.join(self.home, "plans", "fix.md")
        write(path, plan_text("fix"))
        self.assertEqual(self.run_main("plan", "fix"), (0, path))

    def test_issue_number(self):
        self.assertEqual(self.run_main("plan", "#12"), (0, self.paths["fix-totals"]))
        self.assertEqual(self.run_main("plan", "12"), (0, self.paths["fix-totals"]))

    def test_pr_number_from_the_phase_line(self):
        self.assertEqual(self.run_main("plan", "#30"), (0, self.paths["fix-dates"]))

    def test_number_with_no_plan(self):
        code, out = self.run_main("plan", "#99")
        self.assertEqual(code, 1)
        self.assertIn("no plan for #99", out)

    def test_outside_a_cairn_repo(self):
        with tempfile.TemporaryDirectory() as plain:
            out = io.StringIO()
            with redirect_stdout(out):
                code = cs.main(["cairn_status.py", "-C", plain, "plan"])
            self.assertEqual(code, 1)
            self.assertIn("not a cairn v3 repo", out.getvalue())


class Main(Base):
    def test_listing_exit_codes(self):
        self.assertEqual(self.run_main()[0], 1)
        self.own()
        code, out = self.run_main()
        self.assertEqual(code, 0)
        self.assertIn("cairn: me/proj (own repo)", out)

    def test_usage_errors(self):
        self.own()
        self.assertEqual(self.run_main("bogus")[0], 2)
        self.assertEqual(self.run_main("plan", "a", "b")[0], 2)


if __name__ == "__main__":
    unittest.main()
