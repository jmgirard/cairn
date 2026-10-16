#!/usr/bin/env python3
"""cairn next — deterministic next-action routing over cairn/ROADMAP.md.

Surfaces the most sensible next action (resume in-progress / review /
start a workable planned milestone), lists planned milestones whose
dependencies are all done, or in guest mode one a stack base (M268), lists
those still blocked by dependencies, and
lists the `blocked` milestones, each with the number of the pull request
its header names (M223).
Read-only; exits 0 on success, 2 outside a cairn repo.

    python3 scripts/cairn_next.py [ROOT]
"""

import os
import re
import sys

import cairn_scripts as cs

# A milestone header's `Branch/PR` line, and a pull request URL in it (M223).
# Spaces and tabs are spelled out, since Python's `\s` and JavaScript's take
# different characters, and hooks/status/reader.ts mirrors these.
BRANCH_PR = re.compile(r"^[ \t]*-[ \t]*\*\*Branch/PR:\*\*(.*)$")
# At most 15 digits, so the number is exact in JavaScript too.
PR_URL = re.compile(r"https://github\.com/[^/ \t]+/[^/ \t]+/pull/([0-9]{1,15})(?![0-9])")
# A line of only spaces and tabs ends an archive summary's Status paragraph,
# and the paragraph of a done milestone starts with `done` (M246).
BLANK = re.compile(r"^[ \t]*$")
STATUS_DONE = re.compile(r"^\*\*Status:\*\*[ \t]*done")


def done_ids(root, rows):
    """Canonical ids of done milestones. A dependency is satisfied if it is a
    done row OR a done milestone whose ROADMAP row was pruned under
    terminal-row retention but whose archive file remains (matches
    cairn_validate's dependency check)."""
    return {cs.canon_id(r["id"]) for r in rows if r["status"] == "done"} | {
        cs.canon_id(mid) for mid in cs.archive_files(root)
    }


def stack_bases(root, rows, read=None):
    """Canonical ids of the stack bases (M268): in guest mode, when
    cairn/PROFILE.md carries `# Push remote: base`, each `blocked` row that
    is not archived and whose milestone file's `Branch/PR` header names a
    pull request URL. Empty in owner mode or without the line. `read` is as
    in `blocked`."""
    if cs.cc.collaboration_mode(root) != "guest" or cs.cc.push_remote(root) != "base":
        return set()
    return {cs.canon_id(r["id"]) for r in blocked(root, rows, read) if r["url"] is not None and not r["archived"]}


def workable(root, rows):
    """Planned rows whose dependencies are each done or a stack base, with
    at most one a stack base (M268), by priority then id. The status band's
    reader (hooks/status/reader.ts) mirrors this, held to it by
    scripts/tests/test_status_fixtures.py (M199)."""
    return _workable(rows, done_ids(root, rows), stack_bases(root, rows))


def recommend(root, rows):
    """The single recommended action, in precedence order: the first review
    row, else the first in-progress row, else the first workable row, else
    planning. A dict of `action`, `command`, and `id` (None for planning).
    The cairn pane (hooks/status/reader.ts) mirrors this (M205)."""
    review = [r for r in rows if r["status"] == "review"]
    in_progress = [r for r in rows if r["status"] == "in-progress"]
    ready = workable(root, rows)
    if review:
        return {"action": "review", "command": "/milestone-review", "id": review[0]["id"]}
    if in_progress:
        return {"action": "resume", "command": "/milestone-implement", "id": in_progress[0]["id"]}
    if ready:
        return {"action": "implement", "command": "/milestone-implement", "id": ready[0]["id"]}
    return {"action": "plan the next milestone", "command": "/milestone-plan", "id": None}


def waiting(root, rows):
    """Planned rows that are not workable, in ROADMAP order. Each is a dict
    of `id`, `title`, and `unmet`, the dependencies `_met` leaves out, as
    written, each with its row's status or `unknown`. The cairn pane mirrors
    this (M205)."""
    by_id = {cs.canon_id(r["id"]): r for r in rows}
    done = done_ids(root, rows)
    bases = stack_bases(root, rows)
    return [
        {"id": r["id"], "title": r["title"], "unmet": _unmet_list(r, _met(r, done, bases), by_id)}
        for r in rows
        if r["status"] == "planned" and not _deps_met(r, done, bases)
    ]


def read_file(path):
    """A regular file's text, or None when it is not one or its read fails."""
    if not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return None


def _pr_match(text):
    """The match of the pull request URL that a milestone file's first
    `Branch/PR` header line names: the first `https://github.com/<owner>/
    <repo>/pull/<n>` URL before any `companion:` entry, or None (M223). The
    header is the text before the first `## ` heading."""
    for line in text.splitlines():
        if line.startswith("## "):
            return None
        m = BRANCH_PR.match(line)
        if m:
            return PR_URL.search(m.group(1).split("companion:", 1)[0])
    return None


def pr_number(text):
    """The number of the pull request that `_pr_match` finds, or None."""
    url = _pr_match(text)
    return int(url.group(1)) if url else None


def pr_url(text):
    """The URL of the pull request that `_pr_match` finds, up to its number,
    so with no trailing path or anchor, or None (M224)."""
    url = _pr_match(text)
    return url.group(0) if url else None


def status_paragraph(text):
    """An archive summary's `**Status:**` paragraph (M246): the first line
    that starts with `**Status:**`, through the line before the next line of
    only spaces and tabs, or the end of the text. None when no line starts
    so."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if not line.startswith("**Status:**"):
            continue
        out = [line]
        for rest in lines[i + 1 :]:
            if BLANK.match(rest):
                break
            out.append(rest)
        return "\n".join(out)
    return None


def archived_text(root, row, read):
    """The text of a row's archive file when the fallback applies (M246):
    exactly one file under `cairn/milestones/archive/` has the row's
    canonical id, its read succeeds, and its Status paragraph starts with
    `done`. None otherwise."""
    want = cs.canon_id(row["id"])
    # A listing, not a glob, so a root holding `[` or `*` lists as the TS
    # side's `list` does (M246 review).
    folder = os.path.join(root, "cairn", "milestones", "archive")
    try:
        names = os.listdir(folder)
    except OSError:
        names = []
    found = []
    for name in names:
        m = cs._ID_RE.match(name)
        if name.startswith("M") and name.endswith(".md") and m and cs.canon_id(m.group(1)) == want:
            found.append(os.path.join(folder, name))
    if len(found) != 1:
        return None
    text = read(found[0])
    para = None if text is None else status_paragraph(text)
    return text if para is not None and STATUS_DONE.match(para) else None


def blocked(root, rows, read=None):
    """The `blocked` rows in ROADMAP order. Each is a dict of `id`, `title`,
    `pr`, the number `pr_number` reads from the row's milestone file, `url`,
    the URL `pr_url` reads (M224), and `archived` (M246). `pr` and `url` are
    None when the file is missing and no archive file applies, or when its
    read fails. When the row's file is not a
    regular file and `archived_text` finds its archive file, `archived` is
    True and `pr` and `url` come from the first URL in that file's Status
    paragraph. `read` takes a path and gives its text or None (`read_file`
    by default). The cairn pane (hooks/status/reader.ts) mirrors this
    (M223)."""
    read = read or read_file
    out = []
    for r in rows:
        if r["status"] != "blocked":
            continue
        path = os.path.join(root, "cairn", r["relpath"])
        archive = None if os.path.isfile(path) else archived_text(root, r, read)
        if archive is not None:
            url = PR_URL.search(status_paragraph(archive))
            out.append(
                {
                    "id": r["id"],
                    "title": r["title"],
                    "pr": int(url.group(1)) if url else None,
                    "url": url.group(0) if url else None,
                    "archived": True,
                }
            )
            continue
        text = read(path)
        out.append(
            {
                "id": r["id"],
                "title": r["title"],
                "pr": None if text is None else pr_number(text),
                "url": None if text is None else pr_url(text),
                "archived": False,
            }
        )
    return out


def render(root):
    rows = cs.rows(cs.read_roadmap(root))
    lines = [f"cairn next — {root}", ""]

    held = blocked(root, rows)

    ready = workable(root, rows)

    rec = recommend(root, rows)
    target = f"{rec['command']} {rec['id']}" if rec["id"] else rec["command"]
    label = f"{rec['action']} {rec['id']}" if rec["id"] else rec["action"]
    lines.append(f"Recommended: {label} → {target}")
    lines.append("")

    lines.append("Workable planned (dependencies satisfied):")
    if ready:
        for r in ready:
            lines.append(f"  {r['id']} ({r['priority']}) — {r['title']}")
    else:
        lines.append("  none")

    stuck = waiting(root, rows)
    if stuck:
        lines.append("Blocked by dependencies:")
        for r in stuck:
            lines.append(f"  {r['id']} — waiting on " + ", ".join(r["unmet"]))

    if held:
        lines.append("Externally blocked (see work-log):")
        for r in held:
            notes = ([] if r["pr"] is None else [f"PR #{r['pr']}"]) + (["archived"] if r["archived"] else [])
            suffix = f" ({', '.join(notes)})" if notes else ""
            lines.append(f"  {r['id']} — {r['title']}{suffix}")
    return "\n".join(lines)


def _met(row, done, bases):
    """The ids that count as met for `row`'s dependencies: the done ids, and
    its stack-base dependency when it has exactly one (M268). A row on two
    or more stack bases has none of them met."""
    on_bases = {cs.canon_id(dep) for dep in row["depends"]} & (bases - done)
    return done | on_bases if len(on_bases) <= 1 else done


def _deps_met(row, done, bases):
    met = _met(row, done, bases)
    return all(cs.canon_id(dep) in met for dep in row["depends"])


def _workable(rows, done, bases):
    return cs.sort_by_priority(
        [r for r in rows if r["status"] == "planned" and _deps_met(r, done, bases)]
    )


def _unmet_list(row, met, by_id):
    parts = []
    for dep in row["depends"]:
        dep_c = cs.canon_id(dep)
        if dep_c in met:
            continue
        state = by_id[dep_c]["status"] if dep_c in by_id else "unknown"
        parts.append(f"{dep} ({state})")
    return parts


def main(argv):
    try:
        root = cs.resolve_root(argv)
    except cs.NotCairn as e:
        cs.die_not_cairn(str(e))
        return 2
    print(render(root))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
