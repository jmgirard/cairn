<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M129: Repair re-surfaces a declined shelf migration

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** RR11
- **Principles touched:** —
- **Branch/PR:** m129-repair-resumability

## Goal

A superseded shelf directory left on disk stays visible — the validate
advisory reports it and a `/cairn-init` repair re-run resumes the migration —
instead of going silent the moment the successor `.gitignore` entry lands.

## Scope

**In:** a filesystem arm in `check_gitignore_deprecations`
(`scripts/cairn_validate.py:880`) reporting a non-empty superseded shelf
directory regardless of `.gitignore` state, plus its docstring and new test
arms; the `/cairn-init` scaffold-deprecations step rewritten so the per-line
block has an entry-line arm and a directory-line arm
(`skills/cairn-init/SKILL.md:202-247`); the restatement sweep for the retired
"quiet advisory confirms the entry, not the directory" clause; and, as the
D-090 ordinary-work rider, RR11 BC5's quantified-claim paragraph in
`guard-doctrine.md` §6 with per-conjunct pins.

**Out:** an empty leftover directory (the advisory fires on non-empty only —
nothing is lost by its silence); any suppression marker for a declined move
(the persistent WARN is the accepted consequence, stated in AC1); driving
repair from the deprecation map instead of the advisory (rejected — work
log); RR11's other criteria (BC1–BC4 shipped by M126, BC6 mooted by D-095 —
Deviations table).

## Acceptance criteria

- [ ] AC1: With a fixture repo where `cairn/references/pdf/` exists as a
      non-empty directory on disk, `cairn_validate`'s `scaffold deprecations`
      advisory emits a line naming that directory and its successor
      `cairn/references/sources/` in all four `.gitignore` entry states
      (neither, old only, new only, both); with the directory absent or empty
      it emits no directory line; the new line does not contain the substring
      `is superseded by`; the four pre-existing `TestGitignoreDeprecation`
      arms pass unmodified. The persistent WARN on a declined move is the
      accepted consequence — no suppression marker; the only silencing states
      are the directory moved or removed.
- [ ] AC2: The `/cairn-init` repair step's scaffold-deprecations
      instructions are entered per advisory line of either kind, so a
      directory line alone (both `.gitignore` entries already present) still
      reaches the three directory-state cases — which continue to be chosen
      by what is on disk, the advisory line being only the trigger — and a
      repair run in a repo with a declined or deferred move re-surfaces the
      leftover directory. The per-line block is split into an entry-line arm
      and a directory-line arm, the line-format sentence describes both
      genres, the "quiet advisory confirms the entry, not the directory"
      clause is rewritten to describe the new advisory, and every restatement
      of the retired clause is re-derived —
      `cairn/references/self-verification-ledger.md` row V06,
      `check_gitignore_deprecations`'s docstring,
      `skills/tests/test_scaffold_migration.py`, and the mutation-REGISTRY
      block quoting the clause — with the mutation harness green and no
      orphaned anchors.
- [ ] AC-3 (BC5): `guard-doctrine.md` §6 contains the quantified-claim rule
      (universal = zero-exception count carrying the procedure obligation;
      unenumerable domain → universal not written), pinned by one new assert
      and one REGISTRY entry, mutation-red when blanked.
- [ ] AC4: One recorded inversion probe: negating the new §6 rule's polarity
      in place while preserving the surrounding sentence shape reds the
      skills suite; the probe's work-log line records the exact edit, the run
      command as run, and the restoring `git diff --stat` output showing
      clean.

Deviations from RR11:

| BC | Disposition |
|---|---|
| BC1 | Shipped by M126 (archived); not re-ingested here. |
| BC2 | Shipped by M126; not re-ingested here. |
| BC3 | Shipped by M126; not re-ingested here. |
| BC4 | Shipped by M126; not re-ingested here. |
| BC5 | Ingested verbatim as AC-3 and strengthened in implementation: one assert + one REGISTRY entry per load-bearing conjunct (≥2 total, guard-doctrine §1) — the letter's "one" is a floor, recorded so the surplus reads as intent, not departure. |
| BC6 | Mooted by D-095 — §8 and its shape-repeat remedy clause were retired whole by M127. |

## Coverage

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T5

## Tasks

- [x] T1: Tests first — add directory-arm cases to `TestGitignoreDeprecation`
      (`scripts/tests/test_scaffold_check.py:93`): non-empty
      `cairn/references/pdf/` × four `.gitignore` entry states expect the
      directory line; empty and absent directory expect silence; assert the
      new line lacks `is superseded by`; record the red run.
- [x] T2: Implement the directory arm in `check_gitignore_deprecations`
      (`scripts/cairn_validate.py:880`) and re-derive its docstring (the
      "reads `.gitignore` alone" premise retires); scripts suite green.
- [x] T3: Rewrite the scaffold-deprecations step
      (`skills/cairn-init/SKILL.md:202-247`): two per-line arms, line-format
      sentence covering both genres, quiet-advisory clause replaced; sweep
      and re-derive the restatement sites (ledger row V06,
      `skills/tests/test_scaffold_migration.py:139-143`, the
      mutation-REGISTRY block near `test_mutation_harness.py:1803`); skills
      suite + mutation harness green.
- [x] T4: Author the quantified-claim paragraph in `guard-doctrine.md` §6;
      pin per load-bearing conjunct in
      `skills/tests/test_lesson_graduation.py` with matching REGISTRY
      entries; harness blanking-red for each.
- [ ] T5: Run AC4's inversion probe and write its work-log line at procedure
      grade; run all three suites + `cairn_validate` from the repo root with
      exit codes checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-31: created by /milestone-plan. Early promotion logged: the source rows' conditions ("second repo adopts the new shelf"; "next guard-authoring milestone opens") had not fired — the user chose promotion at the plan gate (IP2: surfaced, not silently overridden).
- 2026-07-31: plan gate chose widening the advisory (a filesystem arm in `check_gitignore_deprecations`) over the candidate row's map+filesystem-driven repair because it keeps M82's advisory-driven design and lets `/milestone`'s audit surface the leftover too; falsified by a repair state the advisory line cannot express.
- 2026-07-31: plan gate chose carrying BC5 as a rider over a standalone BC5 milestone because D-090's door permits doctrine work only as ordinary work inside a milestone whose deliverable is a shipped-behavior fix; falsified by a superseding D-entry reopening standalone apparatus milestones.
- 2026-07-31: criteria audit ([O], fresh context) returned 15 findings, 5 blocking (empty-dir unsatisfiability, step entry condition misdescribed, two-genre per-line block, restatement sites outside guards, permanent-WARN consequence unstated) — all disposed by adopting the auditor's own proposed wordings into AC1/AC2/AC4 plus the BC5 strengthening row in the Deviations table; none needed a user question.
- 2026-07-31: plan gate dropped the robustness-read candidate row as mooted by D-095 — §8 and its rounds no longer exist, so the row's mechanism and promotion condition were both unreachable.
- 2026-07-31: T1+T2 done — directory arm added to `check_gitignore_deprecations` (fires on a non-empty superseded shelf in all four entry states; empty/absent silent; line avoids `is superseded by`), docstring re-derived; new `TestGitignoreDeprecationDirectory` red first (2 failures/3 errors) then green; three suites green (scripts 336, skills 704, hooks 103), exits checked.
- 2026-07-31: T3 done — SKILL.md per-line block split into entry-line/directory-line arms with a two-genre format sentence; closing clause rewritten (quiet advisory now confirms entries AND directory); guards renamed/re-anchored (`test_closing_check_covers_both_arms`, + two new tests), three REGISTRY entries re-pointed/added, ledger row V06 annotated (quote stays historical at 684e53a); skills 706 OK, scripts 336 OK, exits checked.
- 2026-07-31: T4 done — quantified-claim paragraph added to guard-doctrine §6 (two bold conjuncts; cites RR11 BC5 + the M118 lesson); pinned per conjunct in `test_restatement_section_states_the_quantified_claim_rule` with two REGISTRY entries, anchors copied from the shipped bytes; skills suite 707 OK, exit checked.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074). -->
