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

# The store root. Overridable for tests; a caller may also pass --store.
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
