# M76: Record correction — history vs. current knowledge, and the correct-in-place protocol

**Status:** done · 2026-07-18 · PR https://github.com/jmgirard/cairn/pull/74

**Goal.** Give cairn a stated rule for correcting a durable record proven false.
**Outcome.** `tracking-rules.md` splits the tracking files by purpose and lets
the split set the remedy: current knowledge (`LESSONS.md`, `references/`,
`DESIGN.md`) is corrected in place and marked; history (`DECISIONS.md`,
work-logs, IDs, both archives, `legacy/`) is superseded and never edited. A
carve-out keeps `DESIGN.md`'s IP/GP block on the D-entry gate — a wrong
principle is not a wrong fact. Retroactively sanctions M75's in-place fix and
ends the contradiction standing since M16, where the rulebook called
`LESSONS.md` append-only while capping and pruning it. All four live
"append-only" labels corrected (the sweep found one more than planned); the
stale M71 matcher rule swept from its last two homes.

**Key decisions.** D-045 records the split, the mechanism, and the reading
that IP4 never covered `LESSONS.md`, so IP4 was left untouched (`DESIGN.md`
never appears in the diff). A `cairn_validate` CHECK for markers: declined.

**Review.** Two trips. Trip 1 failed AC3 (its exemption list omitted the
guards' own `assertNotIn` — the M59 trap); amended via the implement gate.
Trip 2 passed 6/6. F1 (88) proved the guards locked the rule's mechanism but
not its enumerations — a set-swap left all six green; fixed and re-proved.
F2 (42) and F3 (55) fixed on operator judgment (M73); F4 (32) rejected.
