"""The status mod's fixtures, held to the Python helpers (M191 AC4).

Each directory under hooks/status/fixtures/ is a small project tree with an
`expected.json`. The TypeScript reader is tested against these fixtures by
`claude plugin test` through the generated `hooks/status/fixtures.gen.ts`.
This file holds the same `expected.json` to the Python helpers the
validator uses: `cairn_scripts.rows` for the ROADMAP rows, and `_AC_ITEM`
over `_section_body` of `Tasks` and of `Acceptance criteria` for the counts
(M193 AC5), and its ordered workable ids to `cairn_next.workable` (M199
AC2). A section's first unchecked line is its first `_AC_ITEM` line
with an open box, less the box prefix. It holds the pane's milestones to a
second implementation here, and the pane's next step to
`cairn_next.recommend` and `cairn_next.waiting` (M205 AC2, AC3), and the
pane's candidate rows to a second reader here, whose count it holds to
`cairn_scripts.candidate_count` where no HTML comment sits in the
Candidates section (M207 AC3). It holds the pane's blocked rows and their
pull request numbers to `cairn_next.blocked` (M223 AC3). The next step's
`title`, the `[high]` row that planning names, is held through
`cairn_next.recommend` too (M272 AC3). A path an
`expected.json` lists under `unreadable` reads as failing on both sides.
It also fails when the generated module is stale.
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

import cairn_next as cn  # noqa: E402
import cairn_scripts as cs  # noqa: E402
import cairn_validate as cv  # noqa: E402
import gen_fixtures  # noqa: E402

ACTIVE = ("in-progress", "review")
CHECKED = re.compile(r"^\s*-\s*\[[xX]\]")
OPEN_BOX = re.compile(r"^\s*-\s*\[ \]\s*")
NO_FILE = {
    "tasksChecked": None,
    "tasksTotal": None,
    "criteriaChecked": None,
    "criteriaTotal": None,
    "nextTask": None,
    "nextCriterion": None,
}


def section_fields(text, heading):
    """(checked, total, first unchecked line less its box) for one section."""
    items = [line for line in cv._section_body(text, heading) if cv._AC_ITEM.match(line)]
    checked = sum(1 for line in items if CHECKED.match(line))
    first = next((OPEN_BOX.sub("", line, count=1) for line in items if OPEN_BOX.match(line)), None)
    return checked, len(items), first


def read_milestone(root, relpath, unreadable):
    """The milestone file's text, or None when it is missing or the fixture
    marks its read as failing (`unreadable` holds absolute paths)."""
    path = os.path.normpath(os.path.join(root, "cairn", relpath))
    if not os.path.isfile(path) or path in unreadable:
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


COMMENT = re.compile(r"<!--.*?-->", re.S)
ITEM_BOX = re.compile(r"^\s*-\s*\[[ xX]\]\s*")
LOG_LINES = 5


def section_text(text, heading):
    """A section's lines with HTML comments removed."""
    return COMMENT.sub("", "\n".join(cv._section_body(text, heading))).splitlines()


def section_items(text, heading):
    """A section's checkbox items; a non-blank indented line that is not an
    item continues the item above it."""
    items = []
    current = None
    for line in section_text(text, heading):
        if cv._AC_ITEM.match(line):
            current = {"text": ITEM_BOX.sub("", line, count=1), "checked": bool(CHECKED.match(line))}
            items.append(current)
        elif current is not None and line[:1].isspace() and line.strip():
            current["text"] += " " + line.strip()
        else:
            current = None
    return items


def python_pane(start, unreadable=()):
    """The pane's milestones for a session started in `start` (M205 AC2)."""
    root = cs.cc.find_cairn_root(str(start))
    if root is None:
        return []
    out = []
    for row in cs.rows(cs.read_roadmap(root)):
        if row["status"] not in ACTIVE:
            continue
        text = read_milestone(root, row["relpath"], unreadable)
        file = None
        if text is not None:
            log = [line for line in section_text(text, "Work log") if line.startswith("- ")]
            file = {
                "goal": "\n".join(section_text(text, "Goal")).strip(),
                "tasks": section_items(text, "Tasks"),
                "criteria": section_items(text, "Acceptance criteria"),
                "log": [line[2:] for line in log[-LOG_LINES:]],
            }
        out.append({"id": row["id"], "title": row["title"], "status": row["status"], "file": file})
    return out


def python_next(start):
    """`cairn_next.recommend` and `cairn_next.waiting` for a session started
    in `start`, or None outside a cairn repo (M205 AC3)."""
    root = cs.cc.find_cairn_root(str(start))
    if root is None:
        return None
    rows = cs.rows(cs.read_roadmap(root))
    return {**cn.recommend(root, rows), "waiting": cn.waiting(root, rows)}


def python_blocked(start, unreadable=()):
    """`cairn_next.blocked` for a session started in `start`, its file reads
    failing for the paths in `unreadable` (M223 AC3)."""
    root = cs.cc.find_cairn_root(str(start))
    if root is None:
        return []
    rows = cs.rows(cs.read_roadmap(root))
    return cn.blocked(root, rows, read=lambda path: None if os.path.normpath(path) in unreadable else cn.read_file(path))


PRIORITY = re.compile(r"\[(high|low|parked)\] ")

# The characters JavaScript's String.prototype.trim removes (ECMAScript's
# WhiteSpace and LineTerminator), so the twin trims as `candidateRows` does.
# Python's bare strip() keeps U+FEFF and removes U+001F; the other characters
# it adds (U+001C-U+001E, U+0085) break lines first, so they never reach the
# trim (M251 review).
JS_TRIM = "\t\n\v\f\r \u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"


def python_candidates(start):
    """The pane's candidate rows for a session started in `start` (M207 AC3):
    the lines that open with `- ` in the sections `candidate_count` walks
    (not the indented ones it also counts), each section read after its own
    HTML comments are removed, each row its priority and the text after the
    token before its first `: `, else before its first ` — `, else all of it
    (M251), and its whole text after the token, trimmed the same way (M293)."""
    root = cs.cc.find_cairn_root(str(start))
    if root is None:
        return []
    sections = []
    current = None
    for line in cs.read_roadmap(root).splitlines():
        if line.startswith("## "):
            current = [] if line.strip().lower().startswith("## candidates") else None
            if current is not None:
                sections.append(current)
            continue
        if current is not None:
            current.append(line)
    out = []
    for section in sections:
        for line in COMMENT.sub("", "\n".join(section)).splitlines():
            if not line.startswith("- "):
                continue
            text = line[2:]
            m = PRIORITY.match(text)
            priority = m.group(1) if m else "normal"
            if m:
                text = text[m.end():]
            cut = ": " if ": " in text else " — "
            out.append({
                "priority": priority,
                "title": text.split(cut, 1)[0].strip(JS_TRIM),
                "text": text.strip(JS_TRIM),
            })
    return out


def python_rows(start, unreadable=()):
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
        fields = dict(NO_FILE)
        text = read_milestone(root, row["relpath"], unreadable)
        if text is not None:
            t_checked, t_total, t_first = section_fields(text, "Tasks")
            c_checked, c_total, c_first = section_fields(text, "Acceptance criteria")
            fields = {
                "tasksChecked": t_checked,
                "tasksTotal": t_total,
                "criteriaChecked": c_checked,
                "criteriaTotal": c_total,
                "nextTask": t_first,
                "nextCriterion": c_first,
            }
        out.append({"id": row["id"], "title": row["title"], "status": row["status"], **fields})
    return out


def python_workable(start):
    """The ordered workable ids for a session started in `start`, by
    `cairn_next.workable` itself (M199 AC2)."""
    root = cs.cc.find_cairn_root(str(start))
    if root is None:
        return []
    return [row["id"] for row in cn.workable(root, cs.rows(cs.read_roadmap(root)))]


class StatusFixtureAgreement(unittest.TestCase):
    def test_fixture_domain_is_not_empty(self):
        names = [p.name for p in gen_fixtures.cases()]
        for name in (
            "mixed",
            "missing-file",
            "nested-first",
            "no-active",
            "no-roadmap",
            "states-implement",
            "states-review",
            "subdirectory",
        ):
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
                    # The fixture's paths are from its own root, which the
                    # copy now sits at, whatever directory the walk finds.
                    unreadable = [os.path.normpath(str(copy) + path) for path in expected.get("unreadable", [])]
                    self.assertEqual(python_rows(start, unreadable), expected["rows"])
                    self.assertEqual(python_workable(start), expected["workable"])
                    self.assertEqual(python_pane(start, unreadable), expected["pane"])
                    self.assertEqual(python_next(start), expected["next"])
                    self.assertEqual(python_candidates(start), expected["candidates"])
                    self.assertEqual(python_blocked(start, unreadable), expected.get("blocked", []))

    def test_python_candidates_cut_and_trim_edges(self):
        # The same rows and titles as three cases in
        # hooks/status/reader.test.ts, written out by hand on both sides: the
        # M251 AC1 empty title, and the two M251 review trim edges where
        # Python's bare strip() differs from JavaScript's trim(), plus the
        # M293 row whose text opens with a byte-order mark and ends with a
        # unit separator, built from code points (LESSONS M272).
        bom, us = chr(0xFEFF), chr(0x1F)
        rows = [
            ": an empty short title — added 2026-01-04",
            "Trailing byte-order mark\ufeff: x — added 2026-01-05",
            "Trailing unit separator\u001f: x — added 2026-01-06",
            f"{bom}Leading byte-order mark: x{us}",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "repo"
            (root / "cairn").mkdir(parents=True)
            text = "# Roadmap\n\n## Candidates\n\n" + "".join(f"- {row}\n" for row in rows)
            (root / "cairn" / "ROADMAP.md").write_text(text, encoding="utf-8")
            self.assertEqual(
                python_candidates(root),
                [
                    {"priority": "normal", "title": "", "text": ": an empty short title — added 2026-01-04"},
                    {"priority": "normal", "title": "Trailing byte-order mark",
                     "text": f"Trailing byte-order mark{bom}: x — added 2026-01-05"},
                    {"priority": "normal", "title": f"Trailing unit separator{us}",
                     "text": f"Trailing unit separator{us}: x — added 2026-01-06"},
                    {"priority": "normal", "title": "Leading byte-order mark",
                     "text": f"Leading byte-order mark: x{us}"},
                ],
            )

    def test_pr_number_header_forms(self):
        # The forms reader.test.ts gives `prNumber`, held to `pr_number`.
        def header(value):
            return f"# M1: x\n\n- **Status:** blocked\n- **Branch/PR:** {value}\n\n## Goal\n"

        cases = [
            ("b, https://github.com/o/r/pull/7", 7),
            ("b, https://github.com/o/r/pull/7, https://github.com/o/r/pull/8", 7),
            ("b, https://github.com/o/r/pull/7/files", 7),
            ("b, https://github.com/o/r/pull/7#discussion_r1", 7),
            ("b, companion: /x b https://github.com/o/s/pull/9", None),
            ("b, https://github.com/o/r/pull/7, companion: /x b https://github.com/o/s/pull/9", 7),
            ("b, https://github.com/o/r/issues/7", None),
            ("b", None),
        ]
        for value, want in cases:
            with self.subTest(value=value):
                self.assertEqual(cn.pr_number(header(value)), want)
        self.assertIsNone(cn.pr_number("# M1: x\n\nhttps://github.com/o/r/pull/7 in the body\n"))
        # A BOM before the dash reads no number on either side, and a tab does.
        self.assertIsNone(cn.pr_number("﻿- **Branch/PR:** b, https://github.com/o/r/pull/7\n"))
        self.assertEqual(cn.pr_number("\t- **Branch/PR:** b, https://github.com/o/r/pull/7\n"), 7)
        # Only the first Branch/PR line counts, only above the first `## `
        # heading, and a number past 15 digits reads as none.
        self.assertIsNone(cn.pr_number("- **Branch/PR:** b\n- **Branch/PR:** c, https://github.com/o/r/pull/7\n"))
        self.assertIsNone(cn.pr_number("# M1: x\n\n## Review\n\n- **Branch/PR:** b, https://github.com/o/r/pull/7\n"))
        self.assertEqual(cn.pr_number(header("b, https://github.com/o/r/pull/123456789012345")), 123456789012345)
        self.assertIsNone(cn.pr_number(header("b, https://github.com/o/r/pull/1234567890123456")))

    def test_pr_url_header_forms(self):
        # The URL `pr_number` reads its number from, less any trailing path
        # or anchor, as reader.test.ts gives `prUrl` (M224). The pane runs
        # `gh pr view` on it.
        def header(value):
            return f"# M1: x\n\n- **Status:** blocked\n- **Branch/PR:** {value}\n\n## Goal\n"

        cases = [
            ("b, https://github.com/o/r/pull/7", "https://github.com/o/r/pull/7"),
            ("b, https://github.com/o/r/pull/7, https://github.com/o/r/pull/8", "https://github.com/o/r/pull/7"),
            ("b, https://github.com/o/r/pull/7/files", "https://github.com/o/r/pull/7"),
            ("b, https://github.com/o/r/pull/7#discussion_r1", "https://github.com/o/r/pull/7"),
            ("b, companion: /x b https://github.com/o/s/pull/9", None),
            ("b, https://github.com/o/r/issues/7", None),
            ("b", None),
        ]
        for value, want in cases:
            with self.subTest(value=value):
                self.assertEqual(cn.pr_url(header(value)), want)
        self.assertIsNone(cn.pr_url(header("b, https://github.com/o/r/pull/1234567890123456")))

    def test_blocked_fixtures_hold_the_row_shapes(self):
        # The row shapes M223 AC1 and AC2 name, stated apart from the
        # helper: the numbers and the null rows, with an active milestone
        # beside a blocked row in one fixture and none in the other.
        def load(name):
            return json.loads((FIXTURES / name / "expected.json").read_text(encoding="utf-8"))

        prs = {row["id"]: row["pr"] for row in load("blocked-prs")["blocked"]}
        self.assertEqual(
            prs,
            {"M101": 12, "M102": 34, "M103": None, "M104": 90, "M105": None, "M106": None, "M107": None},
        )
        self.assertFalse((FIXTURES / "blocked-prs" / "cairn" / "milestones" / "M107-missing.md").exists())
        self.assertIn("/cairn/milestones/M106-unreadable.md", load("blocked-prs")["unreadable"])
        self.assertEqual(load("blocked-prs")["pane"], [])
        active = load("blocked-active")
        self.assertEqual([row["id"] for row in active["pane"]], ["M110"])
        self.assertEqual(
            active["blocked"],
            [
                {
                    "id": "M111",
                    "title": "Handed to the maintainers",
                    "pr": 1250,
                    "url": "https://github.com/upstream/repo/pull/1250",
                    "archived": False,
                }
            ],
        )
        # M246 AC1: the archive fallback's nine cases, stated apart from
        # the helper. Only a single done archive file whose read succeeds,
        # under a row with no live file, is archived, and its PR comes from
        # the Status paragraph.
        held = {row["id"]: (row["pr"], row["archived"]) for row in load("blocked-archived")["blocked"]}
        archive = FIXTURES / "blocked-archived" / "cairn" / "milestones" / "archive"
        self.assertEqual(
            held,
            {
                "M201": (11, False),
                "M202": (21, True),
                "M203": (32, True),
                "M204": (None, True),
                "M057": (57, True),
                "M206": (None, False),
                "M207": (None, False),
                "M208": (None, False),
                "M209": (None, False),
                "M210": (101, True),
                "M211": (None, True),
            },
        )
        # A done archive beside M201's live file, so the live file is shown
        # to win (M246 review).
        self.assertTrue((archive / "M201-live.md").exists())
        self.assertEqual(sorted(p.name for p in archive.glob("M*207*")), ["M0207-b.md", "M207-a.md"])
        self.assertIn("/cairn/milestones/archive/M208-unreadable.md", load("blocked-archived")["unreadable"])
        # Each row's URL beside its number (M224): the trailing path cut,
        # and null wherever the number is.
        urls = {row["id"]: row["url"] for row in load("blocked-prs")["blocked"]}
        self.assertEqual(
            urls,
            {
                "M101": "https://github.com/upstream/repo/pull/12",
                "M102": "https://github.com/upstream/repo/pull/34",
                "M103": None,
                "M104": "https://github.com/upstream/repo/pull/90",
                "M105": None,
                "M106": None,
                "M107": None,
            },
        )

    def test_candidate_rows_match_candidate_count(self):
        # Where no HTML comment sits in the Candidates section, the pane
        # reads as many rows as `candidate_count` counts (M207 AC3).
        checked = []
        for case_dir in gen_fixtures.cases():
            roadmap_path = case_dir / "cairn" / "ROADMAP.md"
            if not roadmap_path.is_file():
                continue
            roadmap = roadmap_path.read_text(encoding="utf-8")
            section = re.search(r"^## Candidates.*?(?=^## |\Z)", roadmap, re.S | re.M | re.I)
            if section is not None and "<!--" in section.group(0):
                continue
            expected = json.loads((case_dir / "expected.json").read_text(encoding="utf-8"))
            with self.subTest(fixture=case_dir.name):
                self.assertEqual(len(expected["candidates"]), cs.candidate_count(roadmap))
            checked.append(case_dir.name)
        self.assertIn("candidates", checked)

    def test_candidate_fixtures_hold_the_shapes_ac3_names(self):
        def load(name):
            return json.loads((FIXTURES / name / "expected.json").read_text(encoding="utf-8"))

        levels = {row["priority"] for row in load("candidates")["candidates"]}
        self.assertEqual(levels, {"high", "normal", "low"})
        self.assertNotIn("## Candidates", (FIXTURES / "no-active" / "cairn" / "ROADMAP.md").read_text(encoding="utf-8"))
        skeleton = (FIXTURES / "candidates-skeleton" / "cairn" / "ROADMAP.md").read_text(encoding="utf-8")
        # The `/cairn-init` skeleton's comment holds two indented `- `
        # placeholder lines, and a second comment holds a flush-left row.
        # `candidate_count` counts all three, and the pane reads none.
        self.assertEqual(cs.candidate_count(skeleton), 3)
        self.assertEqual(load("candidates-skeleton")["candidates"], [])

    def test_a_fixture_names_a_high_row_for_planning(self):
        # M272 AC3, stated apart from the helpers: at least one compared
        # fixture gives a non-null title, and in `high-candidate` it is the
        # first `[high]` row that is neither inside a comment nor named by a
        # live token: the row before it carries `M2`, the planned M002 at
        # another padding, and its own token names the done M001 (M273).
        titled = {}
        for case_dir in gen_fixtures.cases():
            expected = json.loads((case_dir / "expected.json").read_text(encoding="utf-8"))
            if expected["next"] is not None and expected["next"]["title"] is not None:
                titled[case_dir.name] = expected["next"]["title"]
        # `candidates-order` (M280) names its first `[high]` row in file
        # order. Every row there has a short title, so the pane's level sort
        # draws that row first too.
        self.assertEqual(titled, {"high-candidate": "Chosen row", "candidates-order": "Late high"})
        roadmap = (FIXTURES / "high-candidate" / "cairn" / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertLess(roadmap.index("- Untagged first:"), roadmap.index("- [high] Taken row:"))
        self.assertIn("- [high] Taken row: work has started on it — added 2026-01-02 — started M2\n", roadmap)
        self.assertIn("| M002 | Open work | planned | M077 |", roadmap)
        self.assertIn(" — started M001\n- [high] Later high:", roadmap)
        self.assertLess(roadmap.index("- [high] Commented row:"), roadmap.index("- [high] Chosen row:"))

    def test_workable_fixtures_are_present_and_discriminating(self):
        # The two idle fixtures exist, and each holds a planned row that a
        # reader ignoring dependencies or priority would put first.
        names = [p.name for p in gen_fixtures.cases()]
        self.assertIn("idle-order", names)
        self.assertIn("idle-deps", names)
        deps = json.loads((FIXTURES / "idle-deps" / "expected.json").read_text(encoding="utf-8"))
        self.assertNotIn("M050", deps["workable"])
        order = json.loads((FIXTURES / "idle-order" / "expected.json").read_text(encoding="utf-8"))
        # M500's `High` sorts it first only when the cell is case-folded.
        self.assertEqual(order["workable"][:2], ["M500", "M030"])

    def test_stack_base_fixtures_hold_the_cases(self):
        # M268 AC1, stated apart from the helpers: M302 waits on M301 in
        # each tree, and only the guest repo with `# Push remote: base`, a
        # `blocked` M301, and a PR URL in M301's header makes it workable.
        # In the two-base tree M302 builds on two and waits, while M305
        # builds on one of them and is workable.
        def workable(name):
            return json.loads((FIXTURES / name / "expected.json").read_text(encoding="utf-8"))["workable"]

        self.assertIn("M302", workable("stack-base"))
        for name in ("stack-owner", "stack-no-push-line", "stack-no-pr", "stack-in-progress", "stack-two-bases"):
            with self.subTest(fixture=name):
                self.assertNotIn("M302", workable(name))
        self.assertIn("M305", workable("stack-two-bases"))
        root = FIXTURES / "stack-owner" / "cairn"
        self.assertIn("# Push remote: base", (root / "PROFILE.md").read_text(encoding="utf-8"))
        self.assertNotIn("Collaboration mode", (root / "PROFILE.md").read_text(encoding="utf-8"))
        held = (FIXTURES / "stack-no-pr" / "cairn" / "milestones" / "M301-waits.md").read_text(encoding="utf-8")
        self.assertIsNone(cn.pr_url(held))
        self.assertIn("| M301 | Back in work after review | in-progress |", (FIXTURES / "stack-in-progress" / "cairn" / "ROADMAP.md").read_text(encoding="utf-8"))

    def test_generated_module_is_current(self):
        module = STATUS_DIR / "fixtures.gen.ts"
        self.assertTrue(module.is_file(), "run python3 hooks/status/gen_fixtures.py")
        self.assertEqual(module.read_text(encoding="utf-8"), gen_fixtures.render())


if __name__ == "__main__":
    unittest.main()
