"""Tests for scripts/cairn_ci_paths.py (M178).

Drives the script as a subprocess against a temporary git root whose
`.github/workflows/` holds one fixture at a time from
`ci_paths_fixtures/report/`. Each fixture has a recorded verdict (the change
detector); every run leaves the file byte-identical; and when PyYAML is
importable each verdict is compared with PyYAML's own reading of the file
(the `on` key reads as `True` under YAML 1.1, or as `"on"`) — the oracle the
line reader is held to. Without PyYAML that comparison is skipped and says so.

Run: python3 -m unittest discover -s scripts/tests
"""

import os
import pathlib
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE.parent / "cairn_ci_paths.py"
REPORT = HERE / "ci_paths_fixtures" / "report"

FILTER_KEYS = ("branches", "branches-ignore", "paths", "paths-ignore")
ENTRY = "cairn/**"
NO_TRIGGER = "no push or pull_request trigger"
UNRECOGNIZED = "unrecognized"

# fixture stem -> the verdict `--report` prints for it (recorded from a run
# and cross-checked against PyYAML by TestAgreesWithPyYAML)
VERDICTS = {
    "scalar": "push (no filters)",
    "flow_list": "push (no filters), pull_request (no filters)",
    "block_bare_push": "push (no filters), pull_request (no filters)",
    "block_branches": "push (branches)",
    "block_branches_ignore": "push (branches-ignore), pull_request (branches)",
    "block_paths": "push (paths)",
    "block_ignore_deeper": "push (paths-ignore), pull_request (no filters)",
    "block_ignore_deeper_cairn": "push (paths-ignore, cairn/**)",
    "block_ignore_flush": "push (branches, paths-ignore), pull_request (no filters)",
    "block_ignore_flush_cairn": "push (paths-ignore, cairn/**)",
    "block_double_quoted_item": "push (paths-ignore, cairn/**), pull_request (no filters)",
    "flow_paths_ignore": "push (paths-ignore)",
    "push_flow_mapping_empty": "push (no filters), pull_request (no filters)",
    "push_flow_mapping": "push (branches)",
    "push_flow_mapping_cairn": "push (branches-ignore, paths-ignore, cairn/**), pull_request (paths)",
    "push_flow_sequence": "push (no filters)",
    "block_pr_filtered": "push (branches), pull_request (paths-ignore)",
    "block_third_key_between": "push (branches), pull_request (paths-ignore)",
    "comment_on_line": "push (no filters)",
    "comment_on_flow_line": "push (no filters), pull_request (no filters)",
    "comment_in_block": "push (branches)",
    "comment_deep": "push (branches, paths-ignore), pull_request (paths-ignore, cairn/**)",
    "comment_column0": "push (branches, paths-ignore), pull_request (no filters)",
    "block_crlf": "push (branches), pull_request (no filters)",
    "quoted_on_double": "push (no filters)",
    "quoted_on_single": "push (no filters)",
    "neither_trigger": NO_TRIGGER,
    "no_on_key": UNRECOGNIZED,
}

try:
    import yaml
    HAVE_YAML = True
except ImportError:  # pragma: no cover - environment-dependent
    HAVE_YAML = False


def run(root, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=root, capture_output=True, text=True, timeout=30,
    )


class Repo:
    """A temporary git root with one workflow file."""

    def __init__(self, src, name="ci.yml"):
        self.dir = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.dir, ".git"))
        wf = os.path.join(self.dir, ".github", "workflows")
        os.makedirs(wf)
        self.path = os.path.join(wf, name)
        shutil.copyfile(src, self.path)

    def read(self):
        with open(self.path, "rb") as fh:
            return fh.read()

    def cleanup(self):
        shutil.rmtree(self.dir, ignore_errors=True)


def report(case, src):
    repo = Repo(src)
    case.addCleanup(repo.cleanup)
    before = repo.read()
    proc = run(repo.dir, "--report")
    case.assertEqual(proc.returncode, 0, proc.stderr)
    case.assertEqual(repo.read(), before, "the report wrote to the file")
    line = proc.stdout.strip()
    case.assertTrue(line.startswith("ci.yml: "), line)
    return line[len("ci.yml: "):]


def verdict_from_yaml(doc):
    """The verdict AC3 expects from PyYAML's reading of a loaded document."""
    if not isinstance(doc, dict) or not (True in doc or "on" in doc):
        return UNRECOGNIZED
    on = doc[True] if True in doc else doc["on"]
    if isinstance(on, str):
        triggers = {on: None}
    elif isinstance(on, list):
        triggers = {t: None for t in on}
    elif isinstance(on, dict):
        triggers = on
    else:
        return UNRECOGNIZED
    named = [t for t in triggers if t in ("push", "pull_request")]
    if not named:
        return NO_TRIGGER
    parts = []
    for t in named:
        value = triggers[t]
        present = []
        if isinstance(value, dict):
            present = [k for k in FILTER_KEYS if k in value]
            ignore = value.get("paths-ignore")
            if isinstance(ignore, list) and ENTRY in ignore:
                present.append(ENTRY)
        parts.append(f"{t} ({', '.join(present) if present else 'no filters'})")
    return ", ".join(parts)


class TestFixtureSet(unittest.TestCase):
    """The fixture set is exactly the recorded one (check discrimination)."""

    def test_every_recorded_fixture_exists_and_no_stray(self):
        self.assertEqual({p.stem for p in REPORT.iterdir()}, set(VERDICTS))

    def test_crlf_fixture_is_crlf(self):
        self.assertIn(b"\r\n", (REPORT / "block_crlf.yml").read_bytes())
        self.assertNotIn(b"\r\n", (REPORT / "block_branches.yml").read_bytes())

    def test_column0_comment_fixture_has_one(self):
        # M178 round-3 finding 1: a column-0 comment inside the `on:` block
        lines = (REPORT / "comment_column0.yml").read_text().split("\n")
        on = lines.index("on:")
        jobs = lines.index("jobs:")
        self.assertTrue(any(l.startswith("#") for l in lines[on:jobs]), lines)


class TestReport(unittest.TestCase):
    def test_each_fixture_reports_its_recorded_verdict(self):
        for stem, verdict in VERDICTS.items():
            with self.subTest(fixture=stem):
                self.assertEqual(report(self, REPORT / f"{stem}.yml"), verdict)

    def test_all_three_verdict_kinds_are_recorded(self):
        kinds = set(VERDICTS.values())
        self.assertIn(NO_TRIGGER, kinds)
        self.assertIn(UNRECOGNIZED, kinds)
        self.assertTrue(any(v.startswith("push (") for v in kinds))

    def test_one_line_per_yml_and_yaml_file_only(self):
        repo = Repo(REPORT / "scalar.yml", name="a.yml")
        self.addCleanup(repo.cleanup)
        wf = os.path.dirname(repo.path)
        shutil.copyfile(REPORT / "flow_list.yml", os.path.join(wf, "b.yaml"))
        pathlib.Path(wf, "notes.txt").write_text("on: push\n")
        os.mkdir(os.path.join(wf, "sub"))
        shutil.copyfile(REPORT / "scalar.yml", os.path.join(wf, "sub", "c.yml"))
        proc = run(repo.dir, "--report")
        lines = proc.stdout.strip().split("\n")
        self.assertEqual([l.split(":")[0] for l in lines], ["a.yml", "b.yaml"])

    @unittest.skipIf(os.geteuid() == 0, "root reads unreadable files")
    def test_an_unreadable_file_reports_unrecognized(self):
        repo = Repo(REPORT / "scalar.yml")
        self.addCleanup(repo.cleanup)
        os.chmod(repo.path, 0)
        self.addCleanup(os.chmod, repo.path, stat.S_IRUSR | stat.S_IWUSR)
        proc = run(repo.dir, "--report")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), f"ci.yml: {UNRECOGNIZED}")

    def test_not_utf8_reports_unrecognized(self):
        with tempfile.TemporaryDirectory() as d:
            src = pathlib.Path(d) / "bin.yml"
            src.write_bytes(b"on: push\n\xff\xfe\n")
            self.assertEqual(report(self, src), UNRECOGNIZED)


class TestAgreesWithPyYAML(unittest.TestCase):
    """AC3: the line reader's verdict equals what PyYAML reads, per fixture."""

    @unittest.skipUnless(HAVE_YAML, "PyYAML not importable: agreement comparison skipped")
    def test_each_fixture_verdict_agrees_with_pyyaml(self):
        for stem in VERDICTS:
            with self.subTest(fixture=stem):
                path = REPORT / f"{stem}.yml"
                doc = yaml.safe_load(path.read_bytes())
                self.assertEqual(report(self, path), verdict_from_yaml(doc))

    @unittest.skipUnless(HAVE_YAML, "PyYAML not importable: agreement comparison skipped")
    def test_the_oracle_discriminates(self):
        # the comparison would catch a truncated block: PyYAML reads the
        # column-0 comment fixture's `paths-ignore`, so the oracle names it
        doc = yaml.safe_load((REPORT / "comment_column0.yml").read_bytes())
        self.assertIn("paths-ignore", verdict_from_yaml(doc))
        self.assertNotEqual(verdict_from_yaml(doc), "push (branches), pull_request (no filters)")


class TestCli(unittest.TestCase):
    def test_root_argument_and_no_workflows_dir(self):
        with tempfile.TemporaryDirectory() as d:
            os.mkdir(os.path.join(d, ".git"))
            proc = run(d, d, "--report")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("no workflow files under", proc.stdout)
            sub = os.path.join(d, "a", "b")
            os.makedirs(sub)
            proc = run(sub, "--report")  # walks up to the .git root
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("no workflow files under", proc.stdout)

    def test_outside_a_git_repository_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            proc = run(d, d, "--report")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("not a git repository", proc.stderr)

    def test_usage_errors_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            os.mkdir(os.path.join(d, ".git"))
            for args in ([], ["--apply"], ["--report", "--apply"], ["--report", "a", "b"], ["--x"]):
                with self.subTest(args=args):
                    proc = run(d, *args)
                    self.assertEqual(proc.returncode, 2, args)
                    self.assertIn("usage:", proc.stderr)

    def test_apply_writes_nothing(self):
        repo = Repo(REPORT / "block_branches.yml")
        self.addCleanup(repo.cleanup)
        before = repo.read()
        proc = run(repo.dir, "--apply")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(repo.read(), before)


if __name__ == "__main__":
    unittest.main()
