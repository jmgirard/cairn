#!/usr/bin/env python3
"""cairn status — deterministic project snapshot over cairn/ROADMAP.md.

Prints milestone counts by status, the active milestone(s), the next
planned milestones by priority, the candidate count, and the last hygiene
check date. Read-only; exits 0 on success, 2 outside a cairn repo.

    python3 scripts/cairn_status.py [ROOT]
"""

import sys

import cairn_scripts as cs


def render(root):
    roadmap = cs.read_roadmap(root)
    rows = cs.rows(roadmap)
    lines = [f"cairn status — {root}", ""]

    counts = {s: [] for s in cs.STATUSES}
    for r in rows:
        counts.setdefault(r["status"], []).append(r["id"])
    lines.append("Milestones by status:")
    for status in ("in-progress", "review", "blocked", "planned", "done", "dropped"):
        ids = counts.get(status, [])
        suffix = f"   {', '.join(ids)}" if ids else ""
        lines.append(f"  {status:<12} {len(ids)}{suffix}")
    lines.append(f"  (candidates  {cs.candidate_count(roadmap)})")
    lines.append("")

    active = [r for r in rows if r["status"] in cs.ACTIVE]
    if active:
        for r in active:
            lines.append(f"Active: {r['id']} ({r['status']}) — {r['title']}")
    else:
        lines.append("Active: none")

    planned = cs.sort_by_priority([r for r in rows if r["status"] == "planned"])
    if planned:
        nxt = ", ".join(f"{r['id']} ({r['priority']})" for r in planned)
        lines.append(f"Next planned (by priority): {nxt}")
    else:
        lines.append("Next planned (by priority): none")

    hygiene = cs.last_hygiene_check(roadmap)
    lines.append(f"Last hygiene check: {hygiene or 'unknown'}")
    return "\n".join(lines)


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
