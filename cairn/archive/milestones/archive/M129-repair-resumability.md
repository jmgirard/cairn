# M129: Repair re-surfaces a declined shelf migration

**Status:** done (2026-07-31, PR #129 https://github.com/jmgirard/cairn/pull/129)

**Goal:** A superseded shelf directory left on disk stays visible — the validate
advisory reports it and a `/cairn-init` repair re-run resumes the migration.

**Outcome:** `check_gitignore_deprecations` gained a filesystem arm: a
non-empty superseded shelf directory warns in every `.gitignore` state
(`directory '<old>' still holds files`), degrading to silence on any OSError;
empty leftovers deliberately invisible; declined moves warn persistently by
design. `/cairn-init`'s deprecations step split per-line into entry-line and
directory-line arms (the line triggers, disk chooses the case); the "quiet
advisory confirms the entry, not the directory" clause retired across all
restatement sites (ledger V06 annotated as historical). Rider (D-090 ordinary
work): guard-doctrine §6 quantified-claim rule (RR11 BC5) — a universal over a
milestone's own artifacts is a zero-exception count carrying the procedure
obligation; an unenumerable domain forbids the universal — pinned per conjunct.

**Decisions:** F17 declined without superseding D-047 — its "goes quiet" clause describes a completed migration and stays true for it.

**Review:** 3 lenses: diff-bug 21 findings, blame-history 0, prior-review 0;
scorer actioned 2 (F1/82 PermissionError crash → `except OSError` + test;
F11/83 wrap-spanning anchors → target re-wrapped, single-line pins); 19 logged
sub-threshold. Nothing graduated or retired at hygiene.
