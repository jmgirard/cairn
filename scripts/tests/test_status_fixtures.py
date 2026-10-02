"""The status mod's fixtures, held to the Python helpers (M191 AC4).

Each directory under hooks/status/fixtures/ is a small project tree with an
`expected.json`. The TypeScript reader is tested against these fixtures by
`claude plugin test` through the generated `hooks/status/fixtures.gen.ts`.
This file holds the same `expected.json` to the Python helpers the
validator uses: `cairn_scripts.rows` for the ROADMAP rows, and `_AC_ITEM`
over `_section_body(text, "Tasks")` for the task counts. It also fails
when the generated module is stale.
"""

import json
import os
import pathlib
import re
import shutil
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO / "scripts"
STATUS_DIR = REPO / "hooks" / "status"
FIXTURES = STATUS_DIR / "fixtures"

for _path in (SCRIPTS_DIR, STATUS_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import cairn_scripts as cs  # noqa: E402
import cairn_validate as cv  # noqa: E402
import gen_fixtures  # noqa: E402

ACTIVE = ("in-progress", "review")
CHECKED = re.compile(r"^\s*-\s*\[[xX]\]")


def python_rows(start):
    """The rows the band shows for a session started in `start`, by the
    Python helpers."""
    root = cs.cc.find_cairn_root(str(start))
    if root is None:
        return []
    with open(os.path.join(root, "cairn", "ROADMAP.md"), encoding="utf-8") as f:
        roadmap = f.read()
    out = []
    for row in cs.rows(roadmap):
        if row["status"] not in ACTIVE:
            continue
        path = os.path.join(root, "cairn", row["relpath"])
        checked = total = None
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                body = cv._section_body(f.read(), "Tasks")
            items = [line for line in body if cv._AC_ITEM.match(line)]
            total = len(items)
            checked = sum(1 for line in items if CHECKED.match(line))
        out.append(
            {
                "id": row["id"],
                "title": row["title"],
                "status": row["status"],
                "checked": checked,
                "total": total,
            }
        )
    return out


class StatusFixtureAgreement(unittest.TestCase):
    def test_fixture_domain_is_not_empty(self):
        names = [p.name for p in gen_fixtures.cases()]
        for name in ("mixed", "missing-file", "no-active", "no-roadmap", "subdirectory"):
            self.assertIn(name, names)

    def test_python_helpers_match_expected(self):
        for case_dir in gen_fixtures.cases():
            with self.subTest(fixture=case_dir.name):
                expected = json.loads((case_dir / "expected.json").read_text(encoding="utf-8"))
                # A copy in a temp dir, so the upward walk cannot reach this
                # repo's own cairn/ROADMAP.md.
                with tempfile.TemporaryDirectory() as tmp:
                    copy = pathlib.Path(tmp) / case_dir.name
                    shutil.copytree(case_dir, copy)
                    start = copy / expected["cwd"] if expected["cwd"] else copy
                    self.assertEqual(python_rows(start), expected["rows"])

    def test_generated_module_is_current(self):
        module = STATUS_DIR / "fixtures.gen.ts"
        self.assertTrue(module.is_file(), "run python3 hooks/status/gen_fixtures.py")
        self.assertEqual(module.read_text(encoding="utf-8"), gen_fixtures.render())


if __name__ == "__main__":
    unittest.main()
