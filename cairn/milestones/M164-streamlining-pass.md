# M164: Streamlining pass over shipped code (RB14)

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m164-streamlining-pass · https://github.com/jmgirard/cairn/pull/165

## Goal

Run the one-shot Fable streamlining audit (RB14, advisory) over the shipped
code corpus and apply the accepted recommendations. Surface tier:
user-facing — `scripts/` and `hooks/` run in adopting repos.

## Scope

**In:** author RB14 (advisory; corpus = the 22 files under
`scripts/*.py`, `scripts/tests/*.py`, `hooks/*.py`, `hooks/tests/*.py`);
the gated Fable run; RR14 ingestion and per-recommendation triage; applying
`apply`-dispositioned recommendations with their coupled-surface ripples
(`hooks/hooks.json` registration, skills/DESIGN prose restating touched
behavior); conditional fold-in of the env-prefix `CMD_POS` alignment if an
applied recommendation touches `hooks/commit_guard.py` or
`hooks/force_push_guard.py` (plan gate 2026-08-29; the row's own fold-in
trigger).

**Out:** skills-prose reduction → behind D-114's reopened door, unplanned;
milestone-sized recommendations → candidate rows at ingest; a recurring
end-of-implement `/simplify` mandate → declined 2026-08-05 (recorded in the
source candidate row), stays declined.

## Acceptance criteria

- [x] AC1: Each recommendation numbered in RR14 that the ingestion triage
      dispositions `apply` is implemented in the milestone branch's diff
      against main; the triage's domain is RR14's numbered recommendation
      list, re-read from RR14 at review.
- [x] AC2: With all applied changes on the branch,
      `python3 -m unittest discover -s scripts/tests` and
      `python3 -m unittest discover -s hooks/tests` both exit 0, and each
      suite's test count is at or above its count at the branch's
      merge-base with main, except where a test removal is itself an
      applied RR14 recommendation.

## Coverage

- AC1 → T3, T4, T5
- AC2 → T4, T5

## Tasks

- [x] T1: Author `cairn/reviews/RB14-streamlining-pass.md` from the brief
      template via the Write tool (M163: quoted guarded commands at line
      start trip merge_guard inside heredocs): self-contained; advisory —
      records that no `## Binding criteria` section is requested; embeds
      the corpus file list from `git ls-files` over the four Scope globs;
      numbered questions on length, directness, and simplification
      requiring numbered, file:line-cited recommendations;
      second-escalation sweep of `cairn/reviews/` + archive; output path
      `cairn/reviews/RR14-streamlining-pass.md`. Set status blocked;
      commit `brief RB14: streamlining pass`.
- [x] T2: RB approval gate per `/milestone-brief` (spawn Fable / manual /
      cancel); never spawn without the gate.
- [x] T3: Ingest RR14: disposition every numbered recommendation
      apply / consider / reject-with-reason in Decisions; milestone-sized
      items → candidate rows; if any `apply` touches
      `hooks/commit_guard.py` or `hooks/force_push_guard.py`, fold the
      env-prefix `CMD_POS` alignment in via the implement step-6 amendment
      gate; archive the RB/RR pair (plain `mv` + `git add`); status back
      to in-progress.
- [x] T4: Apply the `apply` recommendations; run both gating suites after
      each batch from the repo root with exit codes checked individually
      (M56); a whole-file deletion dispositions every class the file
      carries (M127); ripple coupled surfaces (`hooks/hooks.json`, both
      `TestNonCairnNoOp` payload collections, skills/DESIGN prose
      restating touched behavior).
- [x] T5: Verify: re-read RR14's numbered list against the triage (AC1);
      run both suites; compare per-suite test counts to the merge-base
      counts (AC2); record in Decisions the source row's hypothesis
      evaluation — whether the pass returned accepted changes neither the
      review lenses nor `/simplify` would have surfaced — for the row's
      graduation note at hygiene.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046). -->

- 2026-08-29: created by /milestone-plan; promoted from the "Streamlining pass over existing shipped code, possibly on Fable" candidate row (added 2026-08-05, conversational); promotion taken on the maintainer's selection at this plan gate — the row's RB-run trigger is circular against the milestone that runs the RB (criteria-audit pass 2 F6); row graduates at post-merge hygiene (records-hygiene §1).
- 2026-08-29: criteria audit (full mode, fresh [O] reader, two passes): pass 1 returned F1–F6 — the frozen-scope clause was cut (it authored a file list D-066 says is derived, and `hooks.json`/skills coupling made the set jointly unsatisfiable), AC1's instrument clauses and AC3's run-conduct clause moved to tasks/verify (D-118/D-120); pass 2 returned F1–F6 on the repaired set — the RR-existence criterion was dropped at the gate as record-binding, AC1 re-bound its triage domain to RR14's numbered list re-read at review, the logged-reason clause moved to T3, AC2 gained the merge-base test-count floor closing the delete-tests loophole, and the promotion circularity was recorded.
- 2026-08-29: plan gate chose the code+tests corpus over runtime-only and code+tests+skills-prose because the test suites are exactly the unserved no-branch-touches surface while a prose pass is a doctrinally separate program (D-114); falsified by an RB Fable cannot usefully read in one pass.
- 2026-08-29: plan gate chose an advisory RR over binding criteria because streamlining recommendations are judgment-weighted and triage keeps the maintainer's call per item; falsified by triage disputes a string-compared criterion would have settled.
- 2026-08-29: plan gate chose dropping the RR-existence criterion over keeping it narrowed because two fresh readers called it record-binding (D-120) and the brief procedure already enforces the RB/RR lifecycle; falsified by a review gate unable to certify the pass ran from tasks and procedure alone.
- 2026-08-29: plan gate chose the conditional env-prefix fold-in over leaving the row because the row's own wording names "the next milestone touching either guard"; falsified by a fold-in that pushes T4 past one session.
- 2026-08-29: implement started; branch m164-streamlining-pass; step-3 question gate skipped — the plan gate settled corpus, advisory form, and fold-in condition, and T2 is itself the user gate.
- 2026-08-29: T1 done — RB14 authored (advisory, no Binding-criteria request; 22-file corpus list with `git ls-files` line counts embedded; 5 numbered questions: length, directness, simplification, test-suite streamlining, not-worth-it; second-escalation sweep of reviews/ + archive found no prior brief on this subject, so no removal question owed); blocked on RB14.
- 2026-08-29: T2 done — gate approved Spawn Fable; [F] subagent read RB14 and wrote RR14 (19 numbered recommendations; both suites confirmed green at baseline: scripts 327, hooks 121).
- 2026-08-29: T3 done — RR14 ingested; triage in Decisions (15 apply, 4 reject, none milestone-sized needing new candidate rows; fold-in condition not fired); RB14/RR14 archived; status back to in-progress.
- 2026-08-29: T4 batch A (runtime: R8–R13) applied — status counts init, next's single `_workable` call, cost's single record filter, validate's `token = slot` drop, `resolve_start` + both fake-argv call sites, `_base_commit` on `cc.git`; suites after batch: scripts 327 OK exit 0, hooks 121 OK exit 0.
- 2026-08-29: T4 batch B (scripts tests: R1–R6, R15, R16) applied — `_days_ago` dup deleted, one cached `_load_validate` loader replacing the per-call exec + `_validate_module` cache + the profile test's inline loader, duplicate future-date and non-ISO-date tests removed (survivors carry the moved comments), the ingest-form positive twin removed (mkdtemp leak gone with it), the two legacy-gitignore scaffold tests merged, test_cairn_cost imports hoisted; suites after batch: scripts 323 OK exit 0 (−4 = the four accepted removals/merges), hooks 121 OK exit 0.
- 2026-08-29: T4 batch C (hooks tests: R7) applied — the three duplicated sys.path shims + direct imports hoisted to module level, the three setUps shrunk to assignments; SessionStart-matcher comment added to `commands()` (RR14 Beyond-the-brief); ripple check: hooks.json and TestNonCairnNoOp untouched (no hook added/removed), no skills/DESIGN prose names a touched internal; T4 done; suites after batch: scripts 323 OK exit 0, hooks 121 OK exit 0.
- 2026-08-29: T5 done — RR14's numbered list (R1–R19, re-read from the archived RR) checked against the triage: every item dispositioned, all 15 apply items present in the branch diff (11 files, +80/−154); suites: scripts 323 OK exit 0 (merge-base 327; −4 all from applied removals R4/R5/R6/R15), hooks 121 OK exit 0 (merge-base 121); validate green; hypothesis evaluation recorded in Decisions; status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. EXEMPT from the 150-line cap
     (D-074). -->

- 2026-08-29: RR14 triage (domain: its numbered list R1–R19). Apply: R1–R11 (the report's own apply tier, all suite-attested) plus, at the triage gate, R12 (path-based root resolver; behavior identical), R13 (merge-base probes via `cairn_common.git`; accepted with the report's caveat that the helper adds a 10s timeout no test witnesses), R15 (merge the two legacy-gitignore scaffold tests), R16 (hoist function-local imports in test_cairn_cost). Reject: R14 (bare function refs in the check registry — uniform lambda column preferred, the report's own hesitation), R17 (CMD_POS consolidation — guard-behavior change, already a tracked candidate row), R18 (splitting `_provenance_block` — load-bearing flag, M81 F1), R19 (argparse — pinned usage/stderr contract). Beyond-the-brief: the mkdtemp leak is folded into R6's removal; the SessionStart-matcher comment lands with R7's test_hooks touch; the `cwd`→`root` rename is skipped (commit_guard stays untouched under R17's reject).
- 2026-08-29: the env-prefix CMD_POS fold-in condition does not fire — no applied recommendation touches `hooks/commit_guard.py` or `hooks/force_push_guard.py` (R17 rejected); the candidate row stands unchanged.
- 2026-08-29: source-row hypothesis evaluation (for the row's graduation note at hygiene): the pass DID return accepted changes neither the review lenses nor `/simplify` would have surfaced — both instruments are diff-scoped, and all 15 applied changes sit in code no recent branch touched (the triplicated test-module loaders and duplicate tests date to M102-era suites; the runtime redundancies predate the current review machinery); the RR's Q5 list additionally documents ten deliberate non-changes a future diff-scoped pass could not have known were load-bearing.

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->

- 2026-08-29 AC1: RR14 re-read whole from `cairn/reviews/archive/RR14-streamlining-pass.md` — numbered domain R1–R19; triage (milestone Decisions) dispositions 15 apply (R1–R13, R15, R16) and 4 reject (R14, R17, R18, R19), every item covered. Each apply item confirmed in `git diff origin/main..HEAD`: R1 `_days_ago` deleted; R2 one cached `_load_validate` (importlib exec + `_VALIDATE_MOD`/`_validate_module` cache removed); R3 profile test on the shared loaders (inline spec-loader gone); R4/R5/R6 the three duplicate tests removed; R7 test_hooks sys.path shims + imports hoisted to module level, three setUps shrunk; R8 `counts = {}`; R9 single `_workable` call; R10 single filtered `sub` in `audit_line`; R11 `token = slot` dropped; R12 `resolve_start` added with both fake-argv call sites converted; R13 `_base_commit` on `cc.git`; R15 the two legacy-gitignore tests merged; R16 test_cairn_cost imports hoisted. PASS.
- 2026-08-29 AC2: fresh runs on the branch — scripts/tests Ran 323 OK exit 0, hooks/tests Ran 121 OK exit 0 (exit codes checked individually). Merge-base counts measured fresh by `git archive`-exporting the merge-base (10b8bf9) to the scratchpad and discovering both suites there: scripts 327, hooks 121 (the export's single scripts failure is environmental — the M83-provenance test shells out to git and the export has no `.git`; count unaffected). Hooks 121 ≥ 121; scripts 323 vs 327 — the −4 are exactly the applied test removals R4, R5, R6, and R15's two-into-one merge, each an applied RR14 recommendation, so the exception clause covers the full shortfall. PASS.
- 2026-08-29 consistency gate: `cairn_validate.py` exit 0, all checks passed (release-window advisory silent); no `cairn/DESIGN.md` principle changed on the branch → `cairn_impact --changed` skipped; toolchain half — `generic` profile's consistency-gate slot names none → clean no-op. PASS.
- 2026-08-29 three-lens review (executable surface → full fan-out; all fresh-context, ref-based git). [S] prior-PR-comments: no prior-review evidence contradicted (archive swept per touched file; the GitHub probe returned no inline comments, walk skipped). [S] blame-history: no deliberate fix undone, no fixed bug resurrected, no D-entry contradicted; independently confirmed both suites and the −4 accounting; its one carried item folds into F1 below. [O] diff-bug: no correctness bug; both ACs verified independently (including CLI byte-identical stdout/stderr/exit across merge-base vs branch builds, and mutation checks redding R4–R8, R10–R13, R15); 8 ranked findings:
  - F1 `scripts/cairn_impact.py:88` — R13's `cc.git` swallows TimeoutExpired, so a >10s merge-base falls through to "HEAD" silently (no stderr warning fires); the accepted caveat is recorded only in this file, not at the code site.
  - F2 `scripts/cairn_next.py:34-44` — RR14's "all four recommendation branches are pinned" overstates: the `review` and `plan` recommendation lines have no test (mutating them stays green); pre-existing, on restructured lines.
  - F3 `scripts/cairn_validate.py:665` — one of R11's seven rename sites (the "has no file under cairn/reviews/" branch) is unexercised by any test; pre-existing gap on a touched line.
  - F4 `scripts/cairn_impact.py:30` — `import cairn_common` works only via `cairn_scripts`' import-time sys.path shim; comment is the only guard (repo ships no import-sorting tooling).
  - F5 `hooks/tests/test_hooks.py:1806` — the added SessionStart comment documents a clause no caller reaches; deleting the clause would have been smaller (comment was RR14's own Beyond-the-brief proposal).
  - F6 `scripts/tests/test_cairn_cost.py:499` — stray blank line detaches a rationale comment from its statement.
  - F7 `scripts/tests/test_cairn_cost.py:24` — `import re` unused (pre-existing, in the header R16 rewrote).
  - F8 `scripts/tests/test_cairn_cost.py:323,473` — test-side fabricated-argv idiom remains (R12 scoped only the two production call sites).
  Return floor: no finding demonstrates an acceptance criterion failing and none is judged a load-bearing defect in the shipped deliverables — all route to gate triage, no status return. Dispositions recorded at the gate below.
