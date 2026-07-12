# M15: Sync Impact Report on principle changes — done 2026-07-11

**Goal:** when a DESIGN.md principle (IPn/GPn) changes, list every tracked
`cairn/` file:line citing it so downstream references reconcile in the same
change.

**Outcome:** `scripts/cairn_impact.py`, a fourth deterministic reporter
(alongside status/next/validate). Takes principle ids (`IP2 GP4`) or
`--changed`, which derives edited principles from the DESIGN.md diff since the
branch **merge-base** (so committed edits are seen at the review gate).
Read-only, stdlib-only, exit 2 outside a cairn repo / on usage error. Wired
into the `/milestone-review` consistency gate (runs when a milestone touches a
principle; skips otherwise). Word-boundary matching (`IP2` ≠ `IP20`). 8
fixture cases.

**Review:** CHANGES NEEDED → resolved. F1 (major): `--changed` diffed `HEAD`,
so committed principle edits reported nothing at the gate — fixed to diff from
the merge-base, locked by a committed-branch test. F2–F6: stricter arg parsing
(unknown flags / empty `--root` → usage error), git-absent warning, whole-word
non-match test, docstring. No D-entries.

PR #13 (squash-merged).
