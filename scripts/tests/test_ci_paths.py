"""Tests for scripts/cairn_ci_paths.py (M178).

Drives the script as a subprocess against a temporary git root whose
`.github/workflows/` holds one fixture at a time, from
`ci_paths_fixtures/`: `apply/<shape>.in.yml` → `<shape>.out.yml` pairs for
each recognized `on:` shape, and `refuse/<reason>.yml` inputs, one per named
refusal. Applied outputs are byte-equal to their expected fixture; refused
inputs are byte-identical after `--apply`. Block-map applies add lines only;
the scalar and flow-list rewrites change the `on:` region alone. When PyYAML
is importable each expected fixture is parsed semantically (the `on` key
reads as `True` under YAML 1.1, or as `"on"`); otherwise that assertion is
skipped and says so.

Run: python3 -m unittest discover -s scripts/tests
"""

import difflib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE.parent / "cairn_ci_paths.py"
FIXTURES = HERE / "ci_paths_fixtures"
APPLY = FIXTURES / "apply"
REFUSE = FIXTURES / "refuse"

BLOCK_SHAPES = [
    "block_map", "block_bare_push", "block_branches",
    "block_existing_ignore", "block_pr_filtered", "block_crlf",
]
REWRITE_SHAPES = ["scalar", "flow_list"]

REFUSALS = {
    "push_paths": "already carries `paths`",
    "already_ignored": "already ignores `cairn/**`",
    "flow_paths_ignore": "`paths-ignore` is a flow list",
    "push_flow_mapping": "holds a flow mapping",
    "push_flow_mapping_filled": "holds a flow mapping",
    "quoted_on_double": "a quoted `on:` key",
    "quoted_on_single": "a quoted `on:` key",
    "comment_on_line": "a comment on the `on:` line",
    "comment_in_block": "a comment inside the `on:` block",
    "unrecognized": "unrecognized",
    "no_push": "no `push` trigger",
}

try:
    import yaml  # noqa: F401
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


def on_value(doc):
    """The `on:` mapping of a PyYAML-loaded document, under either key."""
    return doc[True] if True in doc else doc["on"]


def trigger_set(value):
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return set(value)
    return set(value.keys())


class TestFixturesExist(unittest.TestCase):
    """The fixture domain is non-empty and complete (check discrimination)."""

    def test_every_expected_shape_has_a_pair(self):
        for shape in BLOCK_SHAPES + REWRITE_SHAPES:
            self.assertTrue((APPLY / f"{shape}.in.yml").is_file(), shape)
            self.assertTrue((APPLY / f"{shape}.out.yml").is_file(), shape)

    def test_every_named_refusal_has_an_input(self):
        for name in REFUSALS:
            self.assertTrue((REFUSE / f"{name}.yml").is_file(), name)

    def test_no_stray_fixture(self):
        pairs = {p.name.split(".")[0] for p in APPLY.iterdir()}
        self.assertEqual(pairs, set(BLOCK_SHAPES + REWRITE_SHAPES))
        self.assertEqual({p.stem for p in REFUSE.iterdir()}, set(REFUSALS))

    def test_crlf_fixture_is_crlf(self):
        data = (APPLY / "block_crlf.in.yml").read_bytes()
        self.assertIn(b"\r\n", data)
        self.assertNotIn(b"\r\n", (APPLY / "block_map.in.yml").read_bytes())


class TestApply(unittest.TestCase):
    def _apply(self, shape):
        repo = Repo(APPLY / f"{shape}.in.yml")
        self.addCleanup(repo.cleanup)
        before = repo.read()
        proc = run(repo.dir, "--apply")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("applied: ci.yml", proc.stdout)
        return before, repo.read()

    def test_each_recognized_shape_matches_its_expected_fixture(self):
        for shape in BLOCK_SHAPES + REWRITE_SHAPES:
            with self.subTest(shape=shape):
                _, after = self._apply(shape)
                self.assertEqual(after, (APPLY / f"{shape}.out.yml").read_bytes())

    def test_block_map_applies_add_lines_only(self):
        for shape in BLOCK_SHAPES:
            with self.subTest(shape=shape):
                before, after = self._apply(shape)
                diff = list(difflib.unified_diff(
                    before.decode().splitlines(True),
                    after.decode().splitlines(True), n=0,
                ))
                body = [l for l in diff[2:] if not l.startswith("@@")]
                self.assertTrue(body, "diff is empty")
                self.assertTrue(all(l.startswith("+") for l in body), diff)
                self.assertIn("- 'cairn/**'", "".join(body))

    def test_scalar_and_flow_rewrites_touch_only_the_on_region(self):
        for shape in REWRITE_SHAPES:
            with self.subTest(shape=shape):
                before, after = self._apply(shape)
                b = before.decode().split("\n")
                a = after.decode().split("\n")
                (i,) = [k for k, l in enumerate(b) if l.startswith("on:")]
                self.assertEqual(a[:i], b[:i])
                self.assertEqual(a[-(len(b) - i - 1):], b[i + 1:])
                block = a[i: len(a) - (len(b) - i - 1)]
                self.assertEqual(block[0], "on:")
                self.assertIn("    paths-ignore:", block)
                self.assertIn("      - 'cairn/**'", block)

    def test_crlf_endings_are_preserved(self):
        _, after = self._apply("block_crlf")
        self.assertNotIn(b"\n", after.replace(b"\r\n", b""))

    def test_apply_is_idempotent_by_refusal(self):
        repo = Repo(APPLY / "block_map.in.yml")
        self.addCleanup(repo.cleanup)
        run(repo.dir, "--apply")
        once = repo.read()
        proc = run(repo.dir, "--apply")
        self.assertIn("already ignores `cairn/**`", proc.stdout)
        self.assertEqual(repo.read(), once)


class TestApplySemantics(unittest.TestCase):
    """Each expected fixture, parsed by PyYAML, ignores cairn/** under push
    with the trigger set unchanged and pull_request untouched."""

    def setUp(self):
        if not HAVE_YAML:
            self.skipTest("PyYAML not importable: semantic assertion skipped")

    def test_expected_fixtures_parse_to_the_added_ignore(self):
        import yaml
        for shape in BLOCK_SHAPES + REWRITE_SHAPES:
            with self.subTest(shape=shape):
                src = yaml.safe_load((APPLY / f"{shape}.in.yml").read_bytes())
                out = yaml.safe_load((APPLY / f"{shape}.out.yml").read_bytes())
                before, after = on_value(src), on_value(out)
                self.assertIsInstance(after, dict)
                self.assertIn("cairn/**", after["push"]["paths-ignore"])
                self.assertEqual(trigger_set(after), trigger_set(before))
                if shape in BLOCK_SHAPES and "pull_request" in before:
                    self.assertEqual(after["pull_request"], before["pull_request"])
                # the only change under push is the appended ignore
                push_before = before.get("push") if isinstance(before, dict) else None
                expected = dict(push_before or {})
                expected["paths-ignore"] = list(expected.get("paths-ignore", [])) + ["cairn/**"]
                self.assertEqual(after["push"], expected)


class TestRefuse(unittest.TestCase):
    def test_each_named_refusal_leaves_the_file_byte_identical(self):
        for name, reason in REFUSALS.items():
            with self.subTest(name=name):
                repo = Repo(REFUSE / f"{name}.yml")
                self.addCleanup(repo.cleanup)
                before = repo.read()
                proc = run(repo.dir, "--apply")
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertIn("refused: ci.yml", proc.stdout)
                self.assertIn(reason, proc.stdout)
                self.assertNotIn("applied:", proc.stdout)
                self.assertEqual(repo.read(), before)

    def test_report_predicts_each_refusal(self):
        for name, reason in REFUSALS.items():
            with self.subTest(name=name):
                repo = Repo(REFUSE / f"{name}.yml")
                self.addCleanup(repo.cleanup)
                proc = run(repo.dir, "--report")
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertIn(f"would refuse: ", proc.stdout)
                self.assertIn(reason, proc.stdout)
                self.assertNotIn("applicable", proc.stdout)


class TestReport(unittest.TestCase):
    def _report(self, src):
        repo = Repo(src)
        self.addCleanup(repo.cleanup)
        proc = run(repo.dir, "--report")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout.strip()

    def test_each_recognized_shape_reports_applicable(self):
        for shape in BLOCK_SHAPES + REWRITE_SHAPES:
            with self.subTest(shape=shape):
                line = self._report(APPLY / f"{shape}.in.yml")
                self.assertTrue(line.startswith("ci.yml: "), line)
                self.assertTrue(line.endswith(" — applicable"), line)

    def test_verdict_names_triggers_and_filter_presence(self):
        line = self._report(APPLY / "block_pr_filtered.in.yml")
        self.assertIn("push (branches)", line)
        self.assertIn("pull_request (paths-ignore)", line)
        line = self._report(REFUSE / "already_ignored.yml")
        self.assertIn("push (paths-ignore, cairn/**)", line)
        line = self._report(APPLY / "flow_list.in.yml")
        self.assertIn("push (no filters), pull_request (no filters)", line)

    def test_verdict_for_a_file_with_neither_trigger(self):
        with tempfile.TemporaryDirectory() as d:
            src = pathlib.Path(d) / "wd.yml"
            src.write_text("name: manual\non:\n  workflow_dispatch:\njobs: {}\n")
            line = self._report(src)
        self.assertIn(": no push or pull_request trigger — would refuse:", line)

    def test_verdict_for_an_unrecognized_file(self):
        line = self._report(REFUSE / "unrecognized.yml")
        self.assertIn(": unrecognized — would refuse:", line)

    def test_one_line_per_yml_and_yaml_file_only(self):
        repo = Repo(APPLY / "scalar.in.yml", name="a.yml")
        self.addCleanup(repo.cleanup)
        wf = os.path.dirname(repo.path)
        shutil.copyfile(APPLY / "flow_list.in.yml", os.path.join(wf, "b.yaml"))
        pathlib.Path(wf, "notes.txt").write_text("on: push\n")
        os.mkdir(os.path.join(wf, "sub"))
        shutil.copyfile(APPLY / "scalar.in.yml", os.path.join(wf, "sub", "c.yml"))
        proc = run(repo.dir, "--report")
        lines = proc.stdout.strip().split("\n")
        self.assertEqual([l.split(":")[0] for l in lines], ["a.yml", "b.yaml"])

    def test_report_does_not_write(self):
        repo = Repo(APPLY / "scalar.in.yml")
        self.addCleanup(repo.cleanup)
        before = repo.read()
        run(repo.dir, "--report")
        self.assertEqual(repo.read(), before)


class TestCli(unittest.TestCase):
    def test_root_argument_and_no_workflows_dir(self):
        with tempfile.TemporaryDirectory() as d:
            os.mkdir(os.path.join(d, ".git"))
            proc = run(d, d, "--report")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("no workflow files", proc.stdout)
            # a nested start walks up to the git root
            nested = os.path.join(d, "a", "b")
            os.makedirs(nested)
            proc = run(nested, "--report")
            self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_outside_a_git_repository_exits_2(self):
        with tempfile.TemporaryDirectory() as d:
            # a temp dir is never inside a repo unless the tmp root is one
            if any(os.path.exists(os.path.join(p, ".git"))
                   for p in pathlib.Path(d).resolve().parents):
                self.skipTest("temp dir sits inside a git repository")
            proc = run(d, "--report")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("not a git repository", proc.stderr)

    def test_usage_errors_exit_2(self):
        with tempfile.TemporaryDirectory() as d:
            os.mkdir(os.path.join(d, ".git"))
            for args in ([], ["--report", "--apply"], ["--bogus"], [d, d, "--report"]):
                with self.subTest(args=args):
                    proc = run(d, *args)
                    self.assertEqual(proc.returncode, 2)
                    self.assertIn("usage:", proc.stderr)


if __name__ == "__main__":
    unittest.main()
