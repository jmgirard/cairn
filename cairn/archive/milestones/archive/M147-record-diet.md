# M147: The records shrink to their jobs

**Status:** done (2026-08-16, PR #148 https://github.com/jmgirard/cairn/pull/148)

**Goal:** cairn's own always-read records shrink to their jobs — one lesson (or
one named family) per LESSONS line, idea/parking/promotion per candidate row —
against a committed per-entry disposition ledger (RR13 rec 8).

**Outcome:** LESSONS.md 49→39 lines, 32 entries→22 (16 kept, 6 trimmed, 10
retired — guard-craft families by RR13-reduction/maturation into the
git-archived doctrine, two by ownership); ROADMAP candidate rows 27→20, each
stating idea/parked/promotion/source only — 5 gate-approved machinery drops,
2 moot (subjects deleted at M146); retired-artifact names swept from both
files (M146's AC2/AC4 greps re-run without their exclusions: zero hits); the
L01–L32/R01–R27 disposition ledger, baseline f767109, is in the archived
file via git. D-117 redirects D-115's fallback for the dropped stamp row.

**Decisions:** the per-entry disposition ledger (archived file via git);
cross-cutting: D-117.

**Review:** single [O] diff-bug lens (internal tier, markdown-only diff): 14
findings — 12 fixed at the gate (operative clauses restored to L01/L06/L07,
row-fidelity repairs, six ledger grounds corrected), 1 rejected with reason,
1 noted deliberate; suites 308+103 green, validate exit 0. Hygiene: nothing
graduated or retired (M147 shipped no guards and moved no slot content).
