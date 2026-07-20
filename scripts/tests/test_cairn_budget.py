"""Guards for cairn_budget.py — the M99 drafting-time counter.

Three properties are load-bearing.

1. COVERAGE. Every capped artifact class reports, and reports in BOTH
   directions. A counter that silently declines to classify a file reads
   identically to one saying "you have room" — so each class is exercised
   under its cap and over it, against a real file on disk (M74: prove an
   advisory both ways or the quiet direction is unproven).
2. AGREEMENT WITH THE GATE. The body figure is `milestone_body_line_count`
   itself and the caps come from `cairn_scripts`. If the drafting counter and
   `cairn_validate` could ever disagree, the tool would send an author to
   compress prose that was never over, or bless a draft the gate rejects.
   Asserted by comparison against the gate's own helpers, not by re-deriving.
3. THE OPERATOR SPLIT. `check_caps` fails a line cap on `>=` but an archive
   summary on `>`, so `<150` permits 149 while `≤25` permits 25. The boundary
   cases below are the ones that would pass a test written against the cap
   number instead of the operator (M87).

Every over-cap assertion is paired with an under-cap one on the same class, so
"reports OVER" can never pass because the class was never reached (M84).

Run from the repo root:

    python3 -m unittest discover -s scripts/tests -k budget
"""

import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS_DIR = pathlib.Path(__file__).resolve().parent.parent
REPO = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import cairn_budget as budget  # noqa: E402  (after sys.path shim)
import cairn_scripts as cs  # noqa: E402


class Repo:
    """A throwaway cairn repo. Only the scaffold the counter actually reads."""

    def __init__(self):
        self.root = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.root, "cairn", "milestones", "archive"))
        self.write("cairn/ROADMAP.md", "# Roadmap\n")
        self.write("cairn/PROFILE.md", "# Profile\n")
        self.write("cairn/LESSONS.md", "# Lessons\n")

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def report(self, rel):
        return budget.report(self.root, os.path.join(self.root, rel))

    def close(self):
        shutil.rmtree(self.root, ignore_errors=True)


def milestone(body_lines, worklog_lines=0):
    """A milestone file whose plan-owned body is exactly `body_lines` long.

    The blank line separating the last plan-owned section from `## Work log`
    belongs to that section and so counts toward the body — the helper budgets
    for it rather than leaving every caller off by one.
    """
    head = ["# M01: t", "", "- **Status:** planned", "", "## Goal", ""]
    filler = ["x"] * (body_lines - len(head) - 1)
    tail = ["", "## Work log"] + ["- x"] * worklog_lines
    text = "\n".join(head + filler + tail) + "\n"
    return text


class TestEveryCappedClassIsClassified(unittest.TestCase):
    """Dispatch. A class that stops being recognised reports nothing at all."""

    def setUp(self):
        self.r = Repo()
        self.addCleanup(self.r.close)

    def test_each_capped_artifact_resolves_to_its_own_class(self):
        self.r.write("CLAUDE.md", "## Project tracking\n- x\n")
        self.r.write("cairn/milestones/M01-x.md", milestone(10))
        self.r.write("cairn/milestones/archive/M02-x.md", "# M02\n")
        cases = {
            "cairn/ROADMAP.md": "tracking file",
            "cairn/LESSONS.md": "tracking file",
            "cairn/PROFILE.md": "tracking file",
            "CLAUDE.md": "CLAUDE.md cairn section",
            "cairn/milestones/M01-x.md": "live milestone",
            "cairn/milestones/archive/M02-x.md": "archive summary",
        }
        for rel, expected in cases.items():
            kind, _ = budget.classify(self.r.root, os.path.join(self.r.root, rel))
            self.assertEqual(kind, expected, f"{rel} misclassified")

    def test_an_uncapped_path_is_refused_rather_than_reported_as_roomy(self):
        self.r.write("README.md", "# hi\n")
        kind, _ = budget.classify(self.r.root, os.path.join(self.r.root, "README.md"))
        self.assertIsNone(kind)
        text, over = self.r.report("README.md")
        self.assertIsNone(over, "an uncapped path must not report an over/under verdict")
        self.assertIn("no cairn cap applies", text)

    def test_a_path_outside_the_repo_is_refused(self):
        kind, _ = budget.classify(self.r.root, os.path.join(self.r.root, "..", "x.md"))
        self.assertIsNone(kind)


class TestBothDirectionsPerClass(unittest.TestCase):
    """Each class under its cap and over it. The under case is what proves the
    over case reached the class rather than falling through dispatch."""

    def setUp(self):
        self.r = Repo()
        self.addCleanup(self.r.close)

    def assertUnder(self, rel):
        text, over = self.r.report(rel)
        self.assertFalse(over, f"{rel} should be within budget:\n{text}")
        self.assertIn("headroom", text)
        return text

    def assertOver(self, rel):
        text, over = self.r.report(rel)
        self.assertTrue(over, f"{rel} should be over budget:\n{text}")
        self.assertIn("shed ≥", text)
        return text

    def test_tracking_file_item_axis_both_ways(self):
        cap = cs.LINE_CAPS["cairn/ROADMAP.md"]
        self.r.write("cairn/ROADMAP.md", "x\n" * (cap - 1))
        self.assertUnder("cairn/ROADMAP.md")
        self.r.write("cairn/ROADMAP.md", "x\n" * cap)
        self.assertOver("cairn/ROADMAP.md")

    def test_tracking_file_mass_axis_both_ways(self):
        cap = cs.CHAR_CAPS["cairn/LESSONS.md"]
        # One long item line: mass without item count, the blind spot M84 named.
        self.r.write("cairn/LESSONS.md", "- " + "x" * (cap - 4) + "\n")
        self.assertUnder("cairn/LESSONS.md")
        self.r.write("cairn/LESSONS.md", "- " + "x" * cap + "\n")
        text = self.assertOver("cairn/LESSONS.md")
        self.assertIn("chars", text)

    def test_live_milestone_body_both_ways(self):
        cap = cs.MILESTONE_CAP
        self.r.write("cairn/milestones/M01-x.md", milestone(cap - 1))
        self.assertUnder("cairn/milestones/M01-x.md")
        self.r.write("cairn/milestones/M01-x.md", milestone(cap))
        self.assertOver("cairn/milestones/M01-x.md")

    def test_archive_summary_both_ways(self):
        cap = cs.ARCHIVE_CAP
        self.r.write("cairn/milestones/archive/M02-x.md", "x\n" * cap)
        self.assertUnder("cairn/milestones/archive/M02-x.md")
        self.r.write("cairn/milestones/archive/M02-x.md", "x\n" * (cap + 1))
        self.assertOver("cairn/milestones/archive/M02-x.md")

    def test_a_claude_md_with_no_cairn_section_is_clean_not_unreadable(self):
        """M99 review F2: it exited 2 — this repo's not-a-cairn-repo signal —
        over a readable file. check_caps passes a missing section silently
        (claude_section_line_count's own docstring says so), so this must too."""
        self.r.write("CLAUDE.md", "# My project\n\nSome docs.\n")
        text, over = self.r.report("CLAUDE.md")
        self.assertFalse(over, "a missing cairn section is not a cap failure")
        self.assertIn("no cairn section", text)
        self.assertNotIn("unreadable", text)

    def test_a_genuinely_absent_claude_md_is_still_reported_unreadable(self):
        """The paired direction: F2's fix must not swallow a real absence."""
        text, over = self.r.report("CLAUDE.md")
        self.assertIsNone(over)
        self.assertIn("unreadable", text)

    def test_claude_section_both_ways(self):
        cap = cs.CLAUDE_SECTION_CAP
        self.r.write("CLAUDE.md", "## Project tracking\n" + "x\n" * (cap - 2))
        self.assertUnder("CLAUDE.md")
        self.r.write("CLAUDE.md", "## Project tracking\n" + "x\n" * (cap - 1))
        self.assertOver("CLAUDE.md")

    def test_non_item_line_axis_both_ways(self):
        cap = cs.NON_ITEM_LINE_CAP
        self.r.write("cairn/ROADMAP.md", "x" * (cap - 1) + "\n")
        self.assertIn("headroom 0", self.r.report("cairn/ROADMAP.md")[0])
        self.r.write("cairn/ROADMAP.md", "x" * cap + "\n")
        self.assertIn("OVER by 1", self.r.report("cairn/ROADMAP.md")[0])

    def test_an_over_length_non_item_line_reaches_the_exit_code(self):
        """M99 review F1: the per-line axis printed OVER and returned clean, so
        a wrapper checking $? read green on a file the tool had just called
        over. Asserted on the VERDICT, not the rendered text — the text was
        already right when the bug was live."""
        self.r.write("cairn/ROADMAP.md", "_" + "x" * (cs.NON_ITEM_LINE_CAP + 100) + "\n")
        text, over = self.r.report("cairn/ROADMAP.md")
        self.assertIn("OVER by", text)
        self.assertTrue(over, "an over-length non-item line must set the verdict")
        # Paired direction: a short line leaves the verdict clean, proving the
        # assertion above is not passing because some other axis is over.
        self.r.write("cairn/ROADMAP.md", "_short_\n")
        self.assertFalse(self.r.report("cairn/ROADMAP.md")[1])


class TestOperatorNotCapNumber(unittest.TestCase):
    """The `>=` / `>` split. These are the cases a test written against the cap
    number rather than the comparison would get backwards."""

    def test_a_strict_cap_permits_one_less_than_its_number(self):
        a = budget.Axis("x", cs.MILESTONE_CAP - 1, cs.MILESTONE_CAP, strict=True)
        self.assertEqual(a.permitted, cs.MILESTONE_CAP - 1)
        self.assertFalse(a.over)
        self.assertTrue(budget.Axis("x", cs.MILESTONE_CAP, cs.MILESTONE_CAP).over)

    def test_a_non_strict_cap_permits_its_own_number(self):
        a = budget.Axis("x", cs.ARCHIVE_CAP, cs.ARCHIVE_CAP, strict=False)
        self.assertEqual(a.permitted, cs.ARCHIVE_CAP)
        self.assertFalse(a.over, "≤25 must permit exactly 25")
        self.assertTrue(
            budget.Axis("x", cs.ARCHIVE_CAP + 1, cs.ARCHIVE_CAP, strict=False).over
        )

    def test_the_two_operators_render_different_markers(self):
        strict = budget.Axis("x", 1, cs.MILESTONE_CAP, strict=True).render()
        loose = budget.Axis("x", 1, cs.ARCHIVE_CAP, strict=False).render()
        self.assertIn("cap <", strict)
        self.assertIn("cap ≤", loose)


class TestAgreementWithTheGate(unittest.TestCase):
    """The drafting counter and the gate counter must never disagree."""

    def setUp(self):
        self.r = Repo()
        self.addCleanup(self.r.close)

    def test_the_fixture_builder_is_exact(self):
        """The boundary tests above are only meaningful if `milestone(N)` really
        has a body of N. Asserted directly so a fixture drift fails HERE rather
        than surfacing as a confusing off-by-one in every boundary case."""
        for n in (20, cs.MILESTONE_CAP - 1, cs.MILESTONE_CAP):
            path = self.r.write("cairn/milestones/M09-x.md", milestone(n))
            self.assertEqual(cs.milestone_body_line_count(path), n)

    def test_the_reported_body_is_the_gates_own_measure(self):
        path = self.r.write("cairn/milestones/M01-x.md", milestone(120, worklog_lines=9))
        kind, rel = budget.classify(self.r.root, path)
        (axis,) = budget.axes(self.r.root, kind, rel)
        self.assertEqual(axis.value, cs.milestone_body_line_count(path))

    def test_the_work_log_is_excluded_exactly_as_the_gate_excludes_it(self):
        """D-046's exemption is the gate's, not a second rule stated here."""
        short = self.r.write("cairn/milestones/M01-x.md", milestone(40, worklog_lines=0))
        n_short = budget.axes(self.r.root, "live milestone", "cairn/milestones/M01-x.md")[0].value
        self.r.write("cairn/milestones/M01-x.md", milestone(40, worklog_lines=30))
        n_long = budget.axes(self.r.root, "live milestone", "cairn/milestones/M01-x.md")[0].value
        self.assertEqual(n_short, n_long, "30 work-log lines must cost no budget")
        self.assertIsNotNone(short)

    def test_every_cap_comes_from_cairn_scripts_and_none_is_restated(self):
        """A literal cap here could drift from the gate's. The counter must
        carry none — asserted over the source, since a drifted literal produces
        a perfectly plausible report."""
        src = (SCRIPTS_DIR / "cairn_budget.py").read_text(encoding="utf-8")
        code = "\n".join(
            line for line in src.splitlines() if not line.strip().startswith("#")
        )
        code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)
        caps = set(cs.LINE_CAPS.values()) | set(cs.CHAR_CAPS.values()) | {
            cs.MILESTONE_CAP,
            cs.ARCHIVE_CAP,
            cs.NON_ITEM_LINE_CAP,
            cs.CLAUDE_SECTION_CAP,
        }
        for cap in sorted(caps):
            self.assertNotRegex(
                code,
                rf"(?<![\w.]){cap}(?![\w])",
                f"cap {cap} is restated in cairn_budget.py; read it from cairn_scripts",
            )
        # Paired positive: the caps really are reachable through cs (M84).
        self.assertGreater(len(caps), 5)
        self.assertIn("cs.MILESTONE_CAP", src)
        self.assertIn("cs.ARCHIVE_CAP", src)


class TestCommandLineContract(unittest.TestCase):
    """The argv shape, which deliberately differs from the sibling reporters."""

    def run_cli(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "cairn_budget.py"), *args],
            capture_output=True,
            text=True,
            cwd=cwd or str(REPO),
        )

    def test_no_argument_prints_usage_and_exits_2(self):
        p = self.run_cli()
        self.assertEqual(p.returncode, 2)
        self.assertIn("usage:", p.stderr)
        self.assertIn("FILE", p.stderr, "usage must say the argument is not a repo root")

    def test_a_file_within_budget_exits_0_and_one_over_exits_1(self):
        r = Repo()
        self.addCleanup(r.close)
        under = r.write("cairn/milestones/M01-x.md", milestone(cs.MILESTONE_CAP - 1))
        over = r.write("cairn/milestones/M03-x.md", milestone(cs.MILESTONE_CAP))
        self.assertEqual(self.run_cli(under).returncode, 0)
        self.assertEqual(self.run_cli(over).returncode, 1)

    def test_outside_a_cairn_repo_it_exits_2(self):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        stray = os.path.join(d, "ROADMAP.md")
        with open(stray, "w") as f:
            f.write("x\n")
        p = self.run_cli(stray, cwd=d)
        self.assertEqual(p.returncode, 2)

    def test_it_runs_against_this_repos_own_live_milestone_files(self):
        """The fixtures above are synthetic; this proves the real shape parses."""
        import glob

        seen = 0
        for path in glob.glob(str(REPO / "cairn" / "milestones" / "M*.md")):
            text, over = budget.report(str(REPO), path)
            self.assertIn("plan-owned body", text)
            self.assertIsNotNone(over)
            seen += 1
        self.assertGreater(seen, 0, "no live milestone files found to check")


if __name__ == "__main__":
    unittest.main()
