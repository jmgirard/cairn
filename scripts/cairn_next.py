#!/usr/bin/env python3
"""cairn next — deterministic next-action routing over cairn/ROADMAP.md.

Surfaces the most sensible next action (resume in-progress / review /
start a workable planned milestone), lists planned milestones whose
dependencies are all done, and lists those still blocked by dependencies.
Read-only; exits 0 on success, 2 outside a cairn repo.

    python3 scripts/cairn_next.py [ROOT]
"""

import sys

import cairn_scripts as cs


def done_ids(root, rows):
    """Canonical ids of done milestones. A dependency is satisfied if it is a
    done row OR a done milestone whose ROADMAP row was pruned under
    terminal-row retention but whose archive file remains (matches
    cairn_validate's dependency check)."""
    return {cs.canon_id(r["id"]) for r in rows if r["status"] == "done"} | {
        cs.canon_id(mid) for mid in cs.archive_files(root)
    }


def workable(root, rows):
    """Planned rows whose dependencies are all done, by priority then id.
    The status band's reader (hooks/status/reader.ts) mirrors this, held to
    it by scripts/tests/test_status_fixtures.py (M199)."""
    return _workable(rows, done_ids(root, rows))


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
    """Planned rows with a dependency not yet done, in ROADMAP order. Each is
    a dict of `id`, `title`, and `unmet`, the undone dependencies as written,
    each with its row's status or `unknown`. The cairn pane mirrors this
    (M205)."""
    by_id = {cs.canon_id(r["id"]): r for r in rows}
    done = done_ids(root, rows)
    return [
        {"id": r["id"], "title": r["title"], "unmet": _unmet_list(r, done, by_id)}
        for r in rows
        if r["status"] == "planned" and not _deps_done(r, done)
    ]


def render(root):
    rows = cs.rows(cs.read_roadmap(root))
    lines = [f"cairn next — {root}", ""]

    blocked = [r for r in rows if r["status"] == "blocked"]

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

    if blocked:
        lines.append("Externally blocked (see work-log):")
        for r in blocked:
            lines.append(f"  {r['id']} — {r['title']}")
    return "\n".join(lines)


def _deps_done(row, done):
    return all(cs.canon_id(dep) in done for dep in row["depends"])


def _workable(rows, done):
    return cs.sort_by_priority(
        [r for r in rows if r["status"] == "planned" and _deps_done(r, done)]
    )


def _unmet_list(row, done, by_id):
    parts = []
    for dep in row["depends"]:
        dep_c = cs.canon_id(dep)
        if dep_c in done:
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
