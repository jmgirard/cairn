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


def render(root):
    rows = cs.rows(cs.read_roadmap(root))
    by_id = {r["id"]: r for r in rows}
    # A dependency is satisfied if it is a done row OR a done milestone whose
    # ROADMAP row was pruned under done-row retention but whose archive file
    # remains (matches cairn_validate's dependency check).
    done = {r["id"] for r in rows if r["status"] == "done"} | set(cs.archive_files(root))
    lines = [f"cairn next — {root}", ""]

    in_progress = [r for r in rows if r["status"] == "in-progress"]
    review = [r for r in rows if r["status"] == "review"]
    blocked = [r for r in rows if r["status"] == "blocked"]

    # Single recommended action, in precedence order.
    if review:
        r = review[0]
        rec = f"review {r['id']} → /milestone-review {r['id']}"
    elif in_progress:
        r = in_progress[0]
        rec = f"resume {r['id']} → /milestone-implement {r['id']}"
    else:
        workable_now = _workable(rows, done)
        if workable_now:
            r = workable_now[0]
            rec = f"implement {r['id']} → /milestone-implement {r['id']}"
        else:
            rec = "plan the next milestone → /milestone-plan"
    lines.append(f"Recommended: {rec}")
    lines.append("")

    workable = _workable(rows, done)
    lines.append("Workable planned (dependencies satisfied):")
    if workable:
        for r in workable:
            lines.append(f"  {r['id']} ({r['priority']}) — {r['title']}")
    else:
        lines.append("  none")

    stuck = [r for r in rows if r["status"] == "planned" and not _deps_done(r, done)]
    if stuck:
        lines.append("Blocked by dependencies:")
        for r in stuck:
            lines.append(f"  {r['id']} — {_unmet(r, done, by_id)}")

    if blocked:
        lines.append("Externally blocked (see work-log):")
        for r in blocked:
            lines.append(f"  {r['id']} — {r['title']}")
    return "\n".join(lines)


def _deps_done(row, done):
    return all(dep in done for dep in row["depends"])


def _workable(rows, done):
    return cs.sort_by_priority(
        [r for r in rows if r["status"] == "planned" and _deps_done(r, done)]
    )


def _unmet(row, done, by_id):
    parts = []
    for dep in row["depends"]:
        if dep in done:
            continue
        state = by_id[dep]["status"] if dep in by_id else "unknown"
        parts.append(f"{dep} ({state})")
    return "waiting on " + ", ".join(parts)


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
