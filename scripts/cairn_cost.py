#!/usr/bin/env python3
"""cairn cost — what a milestone spends, measured from the session store.

Reports per-phase token and turn cost over the Claude Code session transcripts
for this repo, so a weight mechanism can be aimed at a term that was measured
rather than assumed (M94). Read-only; reuses the cairn_scripts root resolver.
Exits 0 on success, 2 outside a cairn repo (or on a usage error), matching the
other reporters.

    python3 scripts/cairn_cost.py                # per-milestone + per-phase
    python3 scripts/cairn_cost.py --attribution  # how records were keyed
    python3 scripts/cairn_cost.py --milestone M93

THE STORE. Claude Code appends one JSONL record per event to
``~/.claude/projects/<slug>/<session-uuid>.jsonl``, where ``<slug>`` is the
repo's absolute path with every non-alphanumeric character replaced by ``-``.
Records carry a ``type``; only ``assistant`` records bill tokens, and they
carry ``message.usage`` with the four classes this script reports, plus the
two fields that make attribution mechanical rather than heuristic:
``attributionSkill`` (the cairn skill that was active) and ``gitBranch``.

THE FOUR TOKEN CLASSES ARE NEVER SUMMED. ``cache_read_input_tokens`` and
``input_tokens`` measure different things and differ by orders of magnitude —
719:1 over this repo's own store as of 2026-07-19 — so a collapsed "input"
figure misattributes the cost almost entirely. Every report keeps them in
separate columns; ``test_cairn_cost.py`` guards the separation.

WHAT THIS CANNOT SEE. Subagent turns are absent from the store: no record
under ``~/.claude/projects/`` carries ``isSidechain: true``, so the tokens a
spawned Agent burns are unrecorded everywhere. The review phase spawns the
most (the M17 fan-out is four), so its figures understate by the most. Rather
than publish a partial number unlabelled, every report carries the *spawn
count* beside the tokens — ``agents`` — so a reader knows a figure is partial
and roughly by how much.
"""

import glob
import json
import os
import re
import sys

import cairn_scripts as cs

# The store root. `store_dir(root, home=...)` overrides it for tests; there is
# deliberately no CLI flag — the store location is not a user-facing choice.
STORE_HOME = os.path.expanduser("~/.claude/projects")

# The four billed token classes, in report order. Deliberately a tuple of
# separate keys and never a sum: see the module docstring.
TOKEN_CLASSES = (
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
    "input_tokens",
    "output_tokens",
)

# attributionSkill -> phase. The three milestone phases get their canonical
# names; the other cairn skills keep their own (they are real work with a real
# cost, just not a milestone phase). Anything else is unattributed.
PHASES = {
    "cairn:milestone-plan": "plan",
    "cairn:milestone-implement": "implement",
    "cairn:milestone-review": "review",
    "cairn:milestone": "milestone",
    "cairn:milestone-brief": "milestone-brief",
    "cairn:hotfix": "hotfix",
    "cairn:cairn-init": "cairn-init",
    "cairn:cairn-release": "cairn-release",
    "cairn:design-interview": "design-interview",
}
UNATTRIBUTED = "unattributed"

# A milestone branch is `m<nn>-<slug>` (tracking-rules git model). The branch
# name is the ONLY authoritative milestone key: it is written by
# /milestone-implement and cannot drift. Plan-phase work runs on the default
# branch and is therefore milestone-unattributable by construction — reported
# at phase level, with its share stated, never guessed at from prose (a plan
# session that planned four milestones at once names all four).
_BRANCH_MILESTONE = re.compile(r"^m(\d{2,})-")

# Tool names that spawn a subagent, across Claude Code versions.
AGENT_TOOLS = {"Agent", "Task"}


class Usage(Exception):
    """Bad command-line arguments (exit 2, like the not-a-cairn-repo case)."""


def store_slug(root):
    """The project-store directory name for a repo root: the absolute path
    with every non-alphanumeric character replaced by `-`."""
    return re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(root))


def store_dir(root, home=None):
    """This repo's session-store directory (may not exist)."""
    return os.path.join(home or STORE_HOME, store_slug(root))


def phase_of(record):
    """The phase a record belongs to, from its `attributionSkill`.

    Records written outside a cairn skill — plain conversation, a non-cairn
    skill — are `unattributed`. This is a lookup, not a heuristic: the field
    is written by the runtime.
    """
    return PHASES.get(record.get("attributionSkill"), UNATTRIBUTED)


def milestone_of(record):
    """The milestone id a record belongs to, from its `gitBranch`, or None.

    None is a real answer and never a failure: default-branch work has no
    milestone in the record. Callers report the None share rather than
    imputing one.
    """
    branch = record.get("gitBranch") or ""
    m = _BRANCH_MILESTONE.match(branch)
    if not m:
        return None
    return "M" + m.group(1)


def session_of(record):
    """The session a record belongs to — its JSONL filename stem, stamped by
    `read_records`. One session is one transcript, so this is the finest
    grain the store supports."""
    return record.get("_session")


def agents_spawned(record):
    """How many subagents this record launched — the labelled blind spot.

    Subagent turns are absent from the store entirely, so this count is what
    tells a reader a token figure is partial.
    """
    content = (record.get("message") or {}).get("content")
    if not isinstance(content, list):
        return 0
    return sum(
        1
        for b in content
        if isinstance(b, dict)
        and b.get("type") == "tool_use"
        and b.get("name") in AGENT_TOOLS
    )


def tokens_of(record):
    """The four billed classes for one record, as a dict. Missing usage reads
    as zeros; the classes are never combined."""
    usage = (record.get("message") or {}).get("usage") or {}
    return {k: usage.get(k, 0) or 0 for k in TOKEN_CLASSES}


def read_records(store):
    """Every billable (`assistant`) record in the store, oldest file first.

    Malformed lines are skipped rather than fatal — the store is a live append
    log and its tail can be a partial write.
    """
    for path in sorted(glob.glob(os.path.join(store, "*.jsonl"))):
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                if record.get("type") == "assistant":
                    record["_session"] = os.path.basename(path)[: -len(".jsonl")]
                    yield record


def attribution(records):
    """How the records keyed: total, and the share with no milestone / no phase.

    The unattributable share is reported, never hidden — a method that
    concealed it would not be acceptable evidence (M94 T1).
    """
    out = {
        "records": 0,
        "no_milestone": 0,
        "no_phase": 0,
        "cache_read_input_tokens": 0,
        "no_milestone_cache_read": 0,
        "no_phase_cache_read": 0,
    }
    for record in records:
        cache_read = tokens_of(record)["cache_read_input_tokens"]
        out["records"] += 1
        out["cache_read_input_tokens"] += cache_read
        if milestone_of(record) is None:
            out["no_milestone"] += 1
            out["no_milestone_cache_read"] += cache_read
        if phase_of(record) == UNATTRIBUTED:
            out["no_phase"] += 1
            out["no_phase_cache_read"] += cache_read
    return out


def pct(part, whole):
    """A percentage, or 0.0 when there is nothing to divide."""
    return (100.0 * part / whole) if whole else 0.0


def _empty():
    bucket = {k: 0 for k in TOKEN_CLASSES}
    bucket["turns"] = 0
    bucket["agents"] = 0
    return bucket


def aggregate(records, key):
    """Sum the four classes, turns, and spawned agents into buckets.

    `key` maps a record to its bucket name (or None to drop it), so the same
    accumulator serves the by-phase and by-milestone views.
    """
    out = {}
    for record in records:
        name = key(record)
        if name is None:
            continue
        bucket = out.setdefault(name, _empty())
        for cls, value in tokens_of(record).items():
            bucket[cls] += value
        bucket["turns"] += 1
        bucket["agents"] += agents_spawned(record)
    return out


def _table(header, rows):
    """A fixed-width table. Column 0 is left-aligned, the rest right."""
    widths = [
        max(len(str(r[i])) for r in [header] + rows) for i in range(len(header))
    ]
    lines = []
    for row in [header] + rows:
        cells = [
            str(c).ljust(widths[i]) if i == 0 else str(c).rjust(widths[i])
            for i, c in enumerate(row)
        ]
        lines.append("  ".join(cells).rstrip())
    lines.insert(1, "  ".join("-" * w for w in widths))
    return "\n".join(lines)


_HEADER = ("", "turns", "cache-read", "cache-create", "fresh-in", "output", "agents")


def _row(name, bucket):
    return (
        name,
        f"{bucket['turns']:,}",
        f"{bucket['cache_read_input_tokens']:,}",
        f"{bucket['cache_creation_input_tokens']:,}",
        f"{bucket['input_tokens']:,}",
        f"{bucket['output_tokens']:,}",
        f"{bucket['agents']:,}",
    )


def report(root, records, milestone=None):
    """The full cost report: attribution, by-phase, by-session, by-milestone.

    `--milestone` filters the *tables*, never the attribution line. Running
    the share over the filtered set would make it 0.0% by construction — a
    method that reported its own blind spot as zero would be exactly the
    hiding T1 forbids, so the share is always the store-wide truth and says
    so when the tables below it are narrower.
    """
    all_records = list(records)
    records = (
        [r for r in all_records if milestone_of(r) == milestone]
        if milestone
        else all_records
    )
    out = [f"cairn cost — {root}"]
    # Count the sessions actually rendered, not whatever is on disk — a
    # header derived from the store while the tables are filtered describes
    # a different population than the one below it.
    sessions = len({session_of(r) for r in records} - {None})
    scope = f" (filtered to {milestone})" if milestone else ""
    out.append(f"store: {store_dir(root)} — {sessions} sessions{scope}")

    stats = attribution(all_records)
    if not stats["records"]:
        out.append("\nno billable records found")
        return "\n".join(out) + "\n"
    out.append(
        "\nattribution (whole store, never the filtered subset): "
        "{r:,} assistant turns · "
        "{nm:.1f}% not keyed to a milestone ({nmc:.1f}% of cache-read) · "
        "{np:.1f}% not keyed to a phase".format(
            r=stats["records"],
            nm=pct(stats["no_milestone"], stats["records"]),
            nmc=pct(stats["no_milestone_cache_read"], stats["cache_read_input_tokens"]),
            np=pct(stats["no_phase"], stats["records"]),
        )
    )
    out.append(
        "  cache-read and fresh-in are never summed; `agents` counts spawned "
        "subagents, whose own tokens the store does not record."
    )

    by_phase = aggregate(records, phase_of)
    rows = [
        _row(name, by_phase[name])
        for name in sorted(by_phase, key=lambda n: -by_phase[n]["turns"])
    ]
    out.append("\nBY PHASE\n" + _table(_HEADER, rows))

    by_session = aggregate(records, session_of)
    if by_session:
        # A session can span phases and (rarely) branches, so each row names
        # what it actually carried rather than assuming one of each.
        labels = {}
        for record in records:
            sid = session_of(record)
            if sid is None:
                continue
            seen = labels.setdefault(sid, {"phases": set(), "milestones": set()})
            seen["phases"].add(phase_of(record))
            seen["milestones"].add(milestone_of(record) or "—")
        rows = []
        for sid in sorted(by_session, key=lambda s: -by_session[s]["turns"]):
            seen = labels.get(sid, {"phases": set(), "milestones": set()})
            rows.append(
                (f"{sid[:8]}  {','.join(sorted(seen['milestones']))}"
                 f"  {','.join(sorted(seen['phases']))}",)
                + _row("", by_session[sid])[1:]
            )
        out.append(
            "\nBY SESSION (session · milestone(s) · phase(s))\n"
            + _table(("session  milestone  phase",) + _HEADER[1:], rows)
        )

    by_ms = aggregate(records, milestone_of)
    if by_ms:
        rows = [
            _row(name, by_ms[name])
            for name in sorted(by_ms, key=cs.id_num, reverse=True)
        ]
        out.append(
            "\nBY MILESTONE (branch-derived; plan-phase work runs on the "
            "default branch and is not keyed to a milestone)\n"
            + _table(_HEADER, rows)
        )
    return "\n".join(out) + "\n"


def latest_milestone(records):
    """The highest-numbered milestone any record names, or None."""
    ids = {milestone_of(r) for r in records} - {None}
    return max(ids, key=cs.id_num) if ids else None


def audit_line(root, records, milestone=None):
    """One always-read cost line for `/milestone`'s audit — the most recent
    milestone's mass, or a named one. A reporting surface only: no threshold,
    no verdict."""
    records = list(records)
    mid = milestone or latest_milestone(records)
    if mid is None:
        return "cost: no milestone-keyed sessions in the store"
    if not any(milestone_of(r) == mid for r in records):
        return f"cost: {mid} — no milestone-keyed sessions in the store"
    bucket = aggregate([r for r in records if milestone_of(r) == mid], lambda r: mid)[mid]
    agents = bucket["agents"]
    return (
        "cost: {mid} — {t:,} turns · {cr:,} cache-read · {fi:,} fresh-in · "
        "{o:,} output · {a} subagent{s} spawned (their tokens unrecorded)".format(
            mid=mid,
            t=bucket["turns"],
            cr=bucket["cache_read_input_tokens"],
            fi=bucket["input_tokens"],
            o=bucket["output_tokens"],
            a=agents,
            s="" if agents == 1 else "s",
        )
    )


def parse_args(argv):
    mode, milestone, root_arg = "report", None, None
    rest = list(argv[1:])
    while rest:
        arg = rest.pop(0)
        if arg == "--attribution":
            mode = "attribution"
        elif arg == "--audit-line":
            mode = "audit-line"
        elif arg == "--milestone":
            if not rest:
                raise Usage("--milestone needs a milestone id")
            milestone = rest.pop(0)
        elif arg.startswith("-"):
            raise Usage(f"unknown option {arg}")
        elif root_arg is None:
            root_arg = arg
        else:
            raise Usage("at most one ROOT")
    return mode, milestone, root_arg


def main(argv):
    try:
        mode, milestone, root_arg = parse_args(argv)
    except Usage as e:
        sys.stderr.write(
            "usage: cairn_cost.py [--attribution|--audit-line] "
            f"[--milestone M<NN>] [ROOT]\n{e}\n"
        )
        return 2
    try:
        root = cs.resolve_root(["cairn_cost"] + ([root_arg] if root_arg else []))
    except cs.NotCairn as e:
        cs.die_not_cairn(str(e))
        return 2
    store = store_dir(root)
    if not os.path.isdir(store):
        print(f"cairn cost — {root}\n\nno session store at {store}")
        return 0
    records = list(read_records(store))
    if mode == "audit-line":
        print(audit_line(root, records, milestone))
    elif mode == "attribution":
        # Deliberately refused rather than honoured: the unattributable share
        # is a property of the whole store, and computing it over one
        # milestone's records makes it 0.0% by construction (the F3 defect).
        if milestone:
            sys.stderr.write(
                "usage: --attribution reports the whole store; it cannot be "
                "filtered with --milestone (the share would be 0.0% by "
                "construction)\n"
            )
            return 2
        stats = attribution(records)
        for key in sorted(stats):
            print(f"{key}: {stats[key]:,}")
    else:
        print(report(root, records, milestone), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
