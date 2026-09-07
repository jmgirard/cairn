"""Tests for scripts/cairn_ci_paths.py (M178 report, M181 apply).

Drives the script as a subprocess against a temporary git root whose
`.github/workflows/` holds one fixture at a time. `--report` runs over
`ci_paths_fixtures/report/`: each fixture has a recorded verdict (the change
detector); every run leaves the file byte-identical; and when PyYAML is
importable each verdict is compared with PyYAML's own reading of the file
(the `on` key reads as `True` under YAML 1.1, or as `"on"`) — the oracle the
line reader is held to. `--apply` runs over `ci_paths_fixtures/apply/`:
`pairs/<stem>.yml` is edited to `pairs/<stem>.expected.yml` byte-for-byte,
each `refused/<stem>.yml` is left byte-identical with its recorded reason,
`--dry-run` writes nothing, each pair's diff adds lines only, and each
expected fixture `safe_load`s to the input with `cairn/**` appended under
`push` → `paths-ignore`. Without PyYAML the apply and agreement tests are
skipped and say so; one test shadows `yaml` to see `--apply` exit 3.

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
PAIRS = HERE / "ci_paths_fixtures" / "apply" / "pairs"
REFUSED = HERE / "ci_paths_fixtures" / "apply" / "refused"
RETURN_PAIRS = HERE / "ci_paths_fixtures" / "apply" / "returns" / "pairs"
RETURN_REFUSED = HERE / "ci_paths_fixtures" / "apply" / "returns" / "refused"

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

# apply pair stems (AC3's twelve forms): `<stem>.yml` edits to `<stem>.expected.yml`
PAIR_STEMS = (
    "bare_push", "push_branches", "ignore_deeper", "ignore_flush",
    "comment_in_block", "comment_column0", "quoted_on_double", "quoted_on_single",
    "indent4_bare_push", "crlf", "pr_own_ignore", "third_key_between",
)

# refused fixture stem -> the reason `--apply` prints, one per AC2 reason
# other than `post-edit check failed`
REFUSALS = {
    "cannot_parse": "PyYAML cannot parse the file",
    "two_documents": "more than one document",
    "no_on_key": "no `on` key",
    "on_scalar": "`on` is not a block mapping",
    "on_anchor": "`on` holds an anchor, alias, or merge key",
    "no_push": "no `push` trigger",
    "push_flow_mapping": "`push` holds a flow mapping",
    "push_paths": "`push` carries `paths`",
    "ignore_flow_sequence": "`paths-ignore` is not a block sequence",
    "already_ignores": "already ignores `cairn/**`",
}
POST_EDIT = "post-edit check failed"
UNWRITABLE = "the file cannot be written"

# M181 review return 1 (F1, F4, F6, F7 and the anchor/alias/merge-key reach
# F2, F3, F5): `returns/pairs/<stem>.yml` edits to its expected fixture;
# `returns/refused/<stem>.yml` is left byte-identical with its reason
RETURN_PAIR_STEMS = (
    "quoted_on_true_key",     # F1: `"on":` plus a top-level key loading truthy
    "ignore_flow_last_item",  # F4: a flow collection as the last item
    "branches_at_eof",        # F6: the push mapping ends the file, no final newline
    "ignore_at_eof",          # F6: the sequence ends the file, no final newline
)
RETURN_REFUSALS = {
    "merge_key_under_push": REFUSALS["on_anchor"],         # F3
    "ignore_alias": REFUSALS["on_anchor"],                 # F5
    "on_alias": REFUSALS["on_anchor"],                     # the whole `on` aliased
    "on_anchored": REFUSALS["on_anchor"],                  # `on: &x`
    "already_ignores_block_scalar": REFUSALS["already_ignores"],  # F7
    "plain_on_true_key": POST_EDIT,  # safe_load folds `on` and `true` onto one key
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
            cases = (
                [], ["--report", "--apply"], ["--report", "a", "b"], ["--x"],
                ["--dry-run"], ["--report", "--dry-run"], ["--apply", "--apply"],
            )
            for args in cases:
                with self.subTest(args=args):
                    proc = run(d, *args)
                    self.assertEqual(proc.returncode, 2, args)
                    self.assertIn("usage:", proc.stderr)

    def test_apply_with_no_workflows_dir_exits_0(self):
        with tempfile.TemporaryDirectory() as d:
            os.mkdir(os.path.join(d, ".git"))
            for args in (["--apply"], ["--apply", "--dry-run"]):
                proc = run(d, *args)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertIn("no workflow files under", proc.stdout)


# --- --apply (M181) ---------------------------------------------------------

def apply(case, src, *flags):
    """Run `--apply` (plus `flags`) on one fixture; returns (repo, stdout line)."""
    repo = Repo(src)
    case.addCleanup(repo.cleanup)
    proc = run(repo.dir, "--apply", *flags)
    case.assertEqual(proc.returncode, 0, proc.stderr)
    line = proc.stdout.strip()
    case.assertTrue(line.startswith("ci.yml: "), line)
    return repo, line[len("ci.yml: "):]


def on_key(text):
    """The key `safe_load` gives the file's `on`: `True` when plain (YAML 1.1), `"on"` when quoted."""
    quoted = any(line.startswith(('"on":', "'on':")) for line in text.split("\n"))
    return "on" if quoted else True


def expected_after(doc, key=True):
    """The input document with `cairn/**` appended under on → push → paths-ignore."""
    push = doc[key].get("push")
    if push is None:
        push = doc[key]["push"] = {}
    push.setdefault("paths-ignore", []).append(ENTRY)
    return doc


class TestApplyFixtureSet(unittest.TestCase):
    """The apply fixture set is exactly the recorded one."""

    def test_pairs_are_exactly_the_recorded_stems_each_with_an_expected(self):
        names = {p.name for p in PAIRS.iterdir()}
        want = {f"{s}.yml" for s in PAIR_STEMS} | {f"{s}.expected.yml" for s in PAIR_STEMS}
        self.assertEqual(names, want)
        self.assertEqual(len(PAIR_STEMS), 12)

    def test_refused_are_exactly_the_recorded_stems(self):
        self.assertEqual({p.stem for p in REFUSED.iterdir()}, set(REFUSALS))

    def test_refusals_cover_every_reason_but_post_edit_and_unwritable(self):
        self.assertEqual(len(set(REFUSALS.values())), 10)
        self.assertNotIn(POST_EDIT, REFUSALS.values())
        self.assertNotIn(UNWRITABLE, REFUSALS.values())

    def test_fixture_axes_are_present(self):
        self.assertIn(b"\r\n", (PAIRS / "crlf.yml").read_bytes())
        self.assertIn(b"\r\n", (PAIRS / "crlf.expected.yml").read_bytes())
        self.assertNotIn(b"\r\n", (PAIRS / "push_branches.yml").read_bytes())
        self.assertIn("\n    push:\n", (PAIRS / "indent4_bare_push.yml").read_text())
        self.assertIn('\n"on":\n', (PAIRS / "quoted_on_double.yml").read_text())
        self.assertIn("\n'on':\n", (PAIRS / "quoted_on_single.yml").read_text())
        lines = (PAIRS / "comment_column0.yml").read_text().split("\n")
        self.assertTrue(any(l.startswith("#") for l in lines[lines.index("on:"):lines.index("jobs:")]))
        self.assertIn("    - README.md\n", (PAIRS / "ignore_flush.yml").read_text())
        self.assertIn("      - README.md\n", (PAIRS / "ignore_deeper.yml").read_text())
        self.assertIn("  workflow_dispatch:\n  pull_request:", (PAIRS / "third_key_between.yml").read_text())
        self.assertIn("  pull_request:\n    paths-ignore:", (PAIRS / "pr_own_ignore.yml").read_text())
        self.assertIn("- cairn/**\n", (REFUSED / "already_ignores.yml").read_text())
        anchor = (REFUSED / "on_anchor.yml").read_text()
        self.assertIn("push: &", anchor)
        self.assertIn("pull_request: *", anchor)


@unittest.skipUnless(HAVE_YAML, "PyYAML not importable: --apply tests skipped")
class TestApply(unittest.TestCase):
    def test_each_pair_applies_to_its_expected_bytes(self):
        for stem in PAIR_STEMS:
            with self.subTest(fixture=stem):
                repo, verdict = apply(self, PAIRS / f"{stem}.yml")
                self.assertEqual(verdict, "applied")
                self.assertEqual(repo.read(), (PAIRS / f"{stem}.expected.yml").read_bytes())

    def test_each_refused_input_is_byte_identical_with_its_reason(self):
        for stem, reason in REFUSALS.items():
            with self.subTest(fixture=stem):
                src = REFUSED / f"{stem}.yml"
                repo, verdict = apply(self, src)
                self.assertEqual(verdict, f"refused: {reason}")
                self.assertEqual(repo.read(), src.read_bytes())

    def test_dry_run_writes_nothing_and_names_exactly_the_editable_files(self):
        for stem in PAIR_STEMS:
            with self.subTest(fixture=stem):
                src = PAIRS / f"{stem}.yml"
                repo, verdict = apply(self, src, "--dry-run")
                self.assertEqual(verdict, "would apply")
                self.assertEqual(repo.read(), src.read_bytes())
        for stem, reason in REFUSALS.items():
            with self.subTest(fixture=stem):
                src = REFUSED / f"{stem}.yml"
                repo, verdict = apply(self, src, "--dry-run")
                self.assertEqual(verdict, f"refused: {reason}")
                self.assertEqual(repo.read(), src.read_bytes())

    def test_each_pair_diff_adds_lines_only(self):
        import difflib
        for stem in PAIR_STEMS:
            with self.subTest(fixture=stem):
                a = (PAIRS / f"{stem}.yml").read_bytes().decode().splitlines(keepends=True)
                b = (PAIRS / f"{stem}.expected.yml").read_bytes().decode().splitlines(keepends=True)
                body = list(difflib.unified_diff(a, b, "in", "out", n=0))[2:]
                self.assertTrue(body, "the pair differs")
                self.assertFalse([l for l in body if l.startswith("-")], body)
                self.assertTrue(all(l.startswith(("+", "@@")) for l in body), body)
                self.assertTrue(any(l.startswith("+") and ENTRY in l for l in body), body)

    def test_each_expected_loads_as_the_input_plus_the_entry(self):
        for stem in PAIR_STEMS:
            with self.subTest(fixture=stem):
                before = yaml.safe_load((PAIRS / f"{stem}.yml").read_bytes())
                after = yaml.safe_load((PAIRS / f"{stem}.expected.yml").read_bytes())
                self.assertEqual(after, expected_after(before, on_key((PAIRS / f"{stem}.yml").read_text())))

    def test_the_oracle_discriminates(self):
        # an item placed under `pull_request` instead would fail the oracle
        wrong = yaml.safe_load((PAIRS / "pr_own_ignore.yml").read_bytes())
        wrong[True]["pull_request"]["paths-ignore"].append(ENTRY)
        before = yaml.safe_load((PAIRS / "pr_own_ignore.yml").read_bytes())
        self.assertNotEqual(wrong, expected_after(before))

    def test_a_second_apply_refuses_as_already_ignoring(self):
        repo, verdict = apply(self, PAIRS / "bare_push.yml")
        self.assertEqual(verdict, "applied")
        after = repo.read()
        proc = run(repo.dir, "--apply")
        self.assertEqual(proc.stdout.strip(), f"ci.yml: refused: {REFUSALS['already_ignores']}")
        self.assertEqual(repo.read(), after)

    def test_one_line_per_file_and_exit_0_whatever_the_verdicts(self):
        repo = Repo(PAIRS / "bare_push.yml", name="a.yml")
        self.addCleanup(repo.cleanup)
        wf = os.path.dirname(repo.path)
        shutil.copyfile(REFUSED / "no_push.yml", os.path.join(wf, "b.yaml"))
        shutil.copyfile(REFUSED / "cannot_parse.yml", os.path.join(wf, "c.yml"))
        proc = run(repo.dir, "--apply")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip().split("\n"), [
            "a.yml: applied",
            f"b.yaml: refused: {REFUSALS['no_push']}",
            f"c.yml: refused: {REFUSALS['cannot_parse']}",
        ])

    @unittest.skipIf(os.geteuid() == 0, "root writes read-only files")
    def test_an_unwritable_file_is_refused_after_a_would_apply(self):
        # M181 return 1, re-audit finding: a read-only file is a refusal, never exit 1
        repo = Repo(PAIRS / "bare_push.yml")
        self.addCleanup(repo.cleanup)
        before = repo.read()
        os.chmod(repo.path, stat.S_IRUSR)
        self.addCleanup(os.chmod, repo.path, stat.S_IRUSR | stat.S_IWUSR)
        proc = run(repo.dir, "--apply", "--dry-run")
        self.assertEqual(proc.stdout.strip(), "ci.yml: would apply")
        proc = run(repo.dir, "--apply")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), f"ci.yml: refused: {UNWRITABLE}")
        self.assertEqual(repo.read(), before)

    @unittest.skipIf(os.geteuid() == 0, "root reads unreadable files")
    def test_an_unreadable_file_is_refused(self):
        repo = Repo(PAIRS / "bare_push.yml")
        self.addCleanup(repo.cleanup)
        os.chmod(repo.path, 0)
        self.addCleanup(os.chmod, repo.path, stat.S_IRUSR | stat.S_IWUSR)
        proc = run(repo.dir, "--apply")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), f"ci.yml: refused: {REFUSALS['cannot_parse']}")


class TestReturnFixtureSet(unittest.TestCase):
    """The return fixtures hold the shapes the review named (check discrimination)."""

    def test_return_fixtures_are_exactly_the_recorded_stems(self):
        names = {p.name for p in RETURN_PAIRS.iterdir()}
        want = {f"{s}.yml" for s in RETURN_PAIR_STEMS} | {f"{s}.expected.yml" for s in RETURN_PAIR_STEMS}
        self.assertEqual(names, want)
        self.assertEqual({p.stem for p in RETURN_REFUSED.iterdir()}, set(RETURN_REFUSALS))

    def test_return_fixture_shapes_are_present(self):
        f1 = (RETURN_PAIRS / "quoted_on_true_key.yml").read_text()
        self.assertIn('\n"on":\n', f1)
        self.assertIn("\ntrue: ", f1)
        self.assertIn("- {a: b}\n  pull_request:", (RETURN_PAIRS / "ignore_flow_last_item.yml").read_text())
        for stem in ("branches_at_eof", "ignore_at_eof"):
            data = (RETURN_PAIRS / f"{stem}.yml").read_bytes()
            self.assertFalse(data.endswith(b"\n"), stem)
            self.assertTrue((RETURN_PAIRS / f"{stem}.expected.yml").read_bytes().endswith(b"\n"), stem)
        self.assertIn("<<: *", (RETURN_REFUSED / "merge_key_under_push.yml").read_text())
        self.assertIn("paths-ignore: *", (RETURN_REFUSED / "ignore_alias.yml").read_text())
        self.assertIn("\non: *", (RETURN_REFUSED / "on_alias.yml").read_text())
        self.assertIn("\non: &", (RETURN_REFUSED / "on_anchored.yml").read_text())
        self.assertIn("- >-\n        cairn/**\n", (RETURN_REFUSED / "already_ignores_block_scalar.yml").read_text())
        f1p = (RETURN_REFUSED / "plain_on_true_key.yml").read_text()
        self.assertIn("\non:\n", f1p)
        self.assertIn("\ntrue: ", f1p)


@unittest.skipUnless(HAVE_YAML, "PyYAML not importable: --apply return tests skipped")
class TestApplyReturns(unittest.TestCase):
    """M181 review return 1: each named shape applies or refuses as recorded."""

    def test_each_return_pair_applies_to_its_expected_bytes(self):
        for stem in RETURN_PAIR_STEMS:
            with self.subTest(fixture=stem):
                repo, verdict = apply(self, RETURN_PAIRS / f"{stem}.yml")
                self.assertEqual(verdict, "applied")
                self.assertEqual(repo.read(), (RETURN_PAIRS / f"{stem}.expected.yml").read_bytes())

    def test_each_return_refused_input_is_byte_identical_with_its_reason(self):
        for stem, reason in RETURN_REFUSALS.items():
            with self.subTest(fixture=stem):
                src = RETURN_REFUSED / f"{stem}.yml"
                repo, verdict = apply(self, src)
                self.assertEqual(verdict, f"refused: {reason}")
                self.assertEqual(repo.read(), src.read_bytes())

    def test_dry_run_agrees_over_the_return_fixtures(self):
        for stem in RETURN_PAIR_STEMS:
            with self.subTest(fixture=stem):
                src = RETURN_PAIRS / f"{stem}.yml"
                repo, verdict = apply(self, src, "--dry-run")
                self.assertEqual(verdict, "would apply")
                self.assertEqual(repo.read(), src.read_bytes())
        for stem, reason in RETURN_REFUSALS.items():
            with self.subTest(fixture=stem):
                src = RETURN_REFUSED / f"{stem}.yml"
                repo, verdict = apply(self, src, "--dry-run")
                self.assertEqual(verdict, f"refused: {reason}")
                self.assertEqual(repo.read(), src.read_bytes())

    def test_each_return_pair_adds_lines_only(self):
        # compared without line endings: the two EOF pairs' last line gains
        # the ending the inserted lines follow, its content unchanged
        import difflib
        for stem in RETURN_PAIR_STEMS:
            with self.subTest(fixture=stem):
                a = (RETURN_PAIRS / f"{stem}.yml").read_text().splitlines()
                b = (RETURN_PAIRS / f"{stem}.expected.yml").read_text().splitlines()
                body = list(difflib.unified_diff(a, b, "in", "out", n=0, lineterm=""))[2:]
                self.assertTrue(body, "the pair differs")
                self.assertFalse([l for l in body if l.startswith("-")], body)
                self.assertTrue(any(l.startswith("+") and ENTRY in l for l in body), body)

    def test_each_return_expected_loads_as_the_input_plus_the_entry(self):
        for stem in RETURN_PAIR_STEMS:
            with self.subTest(fixture=stem):
                text = (RETURN_PAIRS / f"{stem}.yml").read_text()
                before = yaml.safe_load(text)
                after = yaml.safe_load((RETURN_PAIRS / f"{stem}.expected.yml").read_bytes())
                self.assertEqual(after, expected_after(before, on_key(text)))

    def test_the_return_oracle_discriminates(self):
        # F1's shape: keyed on the loaded `True` the oracle would look at the
        # wrong top-level key, so the key is read from the text instead
        text = (RETURN_PAIRS / "quoted_on_true_key.yml").read_text()
        doc = yaml.safe_load(text)
        self.assertIn(True, doc)
        self.assertEqual(on_key(text), "on")
        with self.assertRaises(AttributeError):
            expected_after(yaml.safe_load(text), True)

    def test_an_alias_reaching_pull_request_is_refused_not_edited(self):
        # F2: the edit under an anchored `push` would land in `pull_request` too
        src = REFUSED / "on_anchor.yml"
        doc = yaml.safe_load(src.read_bytes())
        self.assertIs(doc[True]["push"], doc[True]["pull_request"])
        repo, verdict = apply(self, src)
        self.assertEqual(verdict, f"refused: {REFUSALS['on_anchor']}")
        self.assertEqual(repo.read(), src.read_bytes())


@unittest.skipUnless(HAVE_YAML, "PyYAML not importable: --apply return-2 tests skipped")
class TestApplyReturn2(unittest.TestCase):
    """M181 review return 2: no raise past composing reaches the exit code (G1);
    a complex-key `on` is judged by the post-edit check, not pre-empted (G6)."""

    def test_deep_nesting_refuses_as_unparseable_and_later_files_still_run(self):
        # G1: a 500-deep flow value makes PyYAML raise RecursionError while
        # composing; the file refuses as unparseable, exit 0, next file processed
        deep = "on:\n  push:\n    branches: [main]\n    x: " + "[" * 500 + "1" + "]" * 500 + "\n"
        repo = Repo(PAIRS / "bare_push.yml", name="b.yml")
        self.addCleanup(repo.cleanup)
        wf = os.path.dirname(repo.path)
        pathlib.Path(wf, "a.yml").write_text(deep)
        for flags in (["--apply", "--dry-run"], ["--apply"]):
            with self.subTest(flags=flags):
                proc = run(repo.dir, *flags)
                self.assertEqual(proc.returncode, 0, proc.stderr[-500:])
                self.assertNotIn("RecursionError", proc.stderr)
                lines = proc.stdout.strip().split("\n")
                self.assertEqual(lines[0], f"a.yml: refused: {REFUSALS['cannot_parse']}")
                self.assertEqual(lines[1], "b.yml: " + ("would apply" if "--dry-run" in flags else "applied"))
                self.assertEqual(pathlib.Path(wf, "a.yml").read_text(), deep)
        with self.assertRaises(RecursionError):  # the failure's identity, not a bare error
            yaml.compose(deep)

    def test_complex_key_on_is_judged_by_the_check(self):
        # G6: `? on` with a null `push` puts the created key at `push`'s own
        # column, a sibling not a child — the check refuses it; with a mapping
        # `push` the same key form applies and loads as expected
        null_push = "? on\n: push:\n"
        with tempfile.TemporaryDirectory() as d:
            src = pathlib.Path(d, "null.yml"); src.write_text(null_push)
            repo, verdict = apply(self, src)
            self.assertEqual(verdict, f"refused: {POST_EDIT}")
            self.assertEqual(repo.read().decode(), null_push)
        mapping_push = "? on\n: push:\n    branches: [main]\n"
        with tempfile.TemporaryDirectory() as d:
            src = pathlib.Path(d, "map.yml"); src.write_text(mapping_push)
            repo, verdict = apply(self, src)
            self.assertEqual(verdict, "applied")
            after = repo.read().decode()
            self.assertEqual(after, mapping_push + "    paths-ignore:\n      - 'cairn/**'\n")
            self.assertEqual(yaml.safe_load(after), expected_after(yaml.safe_load(mapping_push), True))


class TestApplyWithoutPyYAML(unittest.TestCase):
    """AC2: a failing `import yaml` exits 3, names PyYAML, writes nothing."""

    def test_shadowed_yaml_module_exits_3(self):
        repo = Repo(PAIRS / "bare_push.yml")
        self.addCleanup(repo.cleanup)
        before = repo.read()
        with tempfile.TemporaryDirectory() as shadow:
            pathlib.Path(shadow, "yaml.py").write_text('raise ImportError("shadowed")\n')
            env = dict(os.environ, PYTHONPATH=shadow, PYTHONDONTWRITEBYTECODE="1")
            for flags in (["--apply"], ["--apply", "--dry-run"]):
                with self.subTest(flags=flags):
                    proc = subprocess.run(
                        [sys.executable, str(SCRIPT), *flags],
                        cwd=repo.dir, capture_output=True, text=True, timeout=30, env=env,
                    )
                    self.assertEqual(proc.returncode, 3, proc.stderr)
                    self.assertIn("PyYAML", proc.stderr)
                    self.assertEqual(proc.stdout, "")
                    self.assertEqual(repo.read(), before)

    def test_a_yaml_module_raising_anything_else_exits_3(self):
        # M181 re-review 3, H1: a broken install whose import raises past
        # ImportError is the same failing import — exit 3, never a traceback
        repo = Repo(PAIRS / "bare_push.yml")
        self.addCleanup(repo.cleanup)
        before = repo.read()
        with tempfile.TemporaryDirectory() as shadow:
            pathlib.Path(shadow, "yaml.py").write_text('raise ValueError("broken install")\n')
            env = dict(os.environ, PYTHONPATH=shadow, PYTHONDONTWRITEBYTECODE="1")
            for flags in (["--apply"], ["--apply", "--dry-run"]):
                with self.subTest(flags=flags):
                    proc = subprocess.run(
                        [sys.executable, str(SCRIPT), *flags],
                        cwd=repo.dir, capture_output=True, text=True, timeout=30, env=env,
                    )
                    self.assertEqual(proc.returncode, 3, proc.stderr)
                    self.assertIn("PyYAML", proc.stderr)
                    self.assertNotIn("Traceback", proc.stderr)
                    self.assertEqual(proc.stdout, "")
                    self.assertEqual(repo.read(), before)

    def test_report_still_runs_without_pyyaml(self):
        repo = Repo(PAIRS / "bare_push.yml")
        self.addCleanup(repo.cleanup)
        with tempfile.TemporaryDirectory() as shadow:
            pathlib.Path(shadow, "yaml.py").write_text('raise ImportError("shadowed")\n')
            env = dict(os.environ, PYTHONPATH=shadow, PYTHONDONTWRITEBYTECODE="1")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--report"],
                cwd=repo.dir, capture_output=True, text=True, timeout=30, env=env,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(proc.stdout.strip(), "ci.yml: push (no filters), pull_request (no filters)")


if __name__ == "__main__":
    unittest.main()
