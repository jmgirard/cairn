# M164: Streamlining pass over shipped code (RB14)

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** —

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

- [ ] AC1: Each recommendation numbered in RR14 that the ingestion triage
      dispositions `apply` is implemented in the milestone branch's diff
      against main; the triage's domain is RR14's numbered recommendation
      list, re-read from RR14 at review.
- [ ] AC2: With all applied changes on the branch,
      `python3 -m unittest discover -s scripts/tests` and
      `python3 -m unittest discover -s hooks/tests` both exit 0, and each
      suite's test count is at or above its count at the branch's
      merge-base with main, except where a test removal is itself an
      applied RR14 recommendation.

## Coverage

- AC1 → T3, T4, T5
- AC2 → T4, T5

## Tasks

- [ ] T1: Author `cairn/reviews/RB14-streamlining-pass.md` from the brief
      template via the Write tool (M163: quoted guarded commands at line
      start trip merge_guard inside heredocs): self-contained; advisory —
      records that no `## Binding criteria` section is requested; embeds
      the corpus file list from `git ls-files` over the four Scope globs;
      numbered questions on length, directness, and simplification
      requiring numbered, file:line-cited recommendations;
      second-escalation sweep of `cairn/reviews/` + archive; output path
      `cairn/reviews/RR14-streamlining-pass.md`. Set status blocked;
      commit `brief RB14: streamlining pass`.
- [ ] T2: RB approval gate per `/milestone-brief` (spawn Fable / manual /
      cancel); never spawn without the gate.
- [ ] T3: Ingest RR14: disposition every numbered recommendation
      apply / consider / reject-with-reason in Decisions; milestone-sized
      items → candidate rows; if any `apply` touches
      `hooks/commit_guard.py` or `hooks/force_push_guard.py`, fold the
      env-prefix `CMD_POS` alignment in via the implement step-6 amendment
      gate; archive the RB/RR pair (plain `mv` + `git add`); status back
      to in-progress.
- [ ] T4: Apply the `apply` recommendations; run both gating suites after
      each batch from the repo root with exit codes checked individually
      (M56); a whole-file deletion dispositions every class the file
      carries (M127); ripple coupled surfaces (`hooks/hooks.json`, both
      `TestNonCairnNoOp` payload collections, skills/DESIGN prose
      restating touched behavior).
- [ ] T5: Verify: re-read RR14's numbered list against the triage (AC1);
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

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. EXEMPT from the 150-line cap
     (D-074). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->
