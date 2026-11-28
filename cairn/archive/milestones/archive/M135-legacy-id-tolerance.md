# M135: Legacy-id tolerance for check_dangling_ids

**Status:** done (2026-08-06, PR #135 https://github.com/jmgirard/cairn/pull/135)

**Goal:** `check_dangling_ids` stops WARNing on a migrated repo's references
to its pre-migration milestone ids, so a real dangler is visible again.

**Outcome:** third D-023 tolerance shipped in `cairn_validate.py`: with
`cairn/legacy/` present, unresolved M-tokens at or below the legacy ceiling —
the highest legacy M-token strictly below the live max, scanned recursively
over legacy `.md` files with `errors="replace"` — are skipped; the ceiling is
`None` (no skip) when the directory is absent or holds no counted token, so
no-legacy behavior is byte-identical to before. Nine fixture tests cover the
boundary, stray-high, id-zero, and non-UTF-8 cases; the M115 LESSONS line was
corrected in place; intraclass measured 322 → 0 WARNs, all ≤ its legacy max.

**Decisions:** none milestone-local; the plan gate's choices (M-token-only
scope, scanned ceiling over a declared one) are in the work log with falsifiers.

**Review:** two rounds. R1: 22 findings, 3 actioned — an unbounded ceiling let
one stray high legacy token silently disable the whole M-check (92), id-zero
skipped with no legacy dir (87), non-UTF-8 legacy dropped the tolerance (85) —
one floor return, fixed red-first. R2 mutation-verified the fixes; 2 record
defects (82/85) took a gated Scope/AC1/T2 amendment and fresh evidence; 27
sub-threshold logged. Nothing graduated/retired.
