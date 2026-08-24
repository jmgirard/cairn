# M160: Phase-close routing recommends implement for already-planned work

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m160-phase-close-routing · https://github.com/jmgirard/cairn/pull/161   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Phase-close blocks route an already-planned workable milestone to
`/milestone-implement`, taking their next command from `cairn_next.py`'s
recommendation instead of prose that lumps planned work with candidates.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**Tier:** user-facing — the deliverable is skill prose adopting repos
execute at every review close and status route.

**In:** `/milestone-review` step 9 (explicit post-hygiene `cairn_validate.py`
run, replacing the "fires later in this same step" allusion), step 10
(`cairn_next.py`-led next command with the D-050 release-parking
displacement), and `/milestone` §3's state-conditional example list. A
repo-wide grep found these as the only two skill files carrying the
plan-for-planned wording ("planned or candidate").

**Out:** `scripts/cairn_next.py` — already correct and test-pinned
(`scripts/tests/test_scripts.py:264`), untouched. A prose-guard test pinning
the new wording — declined at the plan gate (test-bar question), not
deferred anywhere.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: `/milestone-review` step 9 explicitly instructs running
      `cairn_validate.py` over the completed hygiene edits before the
      docs-only commit, in place of the current allusion ("fires later in
      this same step"), and its `release window` advisory is named as the
      signal step 10 reads.
- [x] AC2: `/milestone-review` step 10 instructs running `cairn_next.py`
      after the step-9 hygiene commit lands and leading the close block's
      fenced next command with its recommendation — displaced by the
      release-parking offer exactly as `/milestone` §3 prescribes when
      step 9's `cairn_validate.py` run fired the `release window` advisory
      and the recommendation names that same release milestone (D-050) —
      and step 10's text no longer names `/milestone-plan` as the route for
      existing planned work.
- [x] AC3: `/milestone` §3's state-conditional example list offers
      `/milestone-implement M<NNN>` for a workable planned milestone as an
      entry distinct from the resume entry, and the `/milestone-plan`
      entry's stated condition no longer includes planned items.
- [x] AC4: The active profile's `verify` slot clean — both gating unittest
      suites green — and `skills/tests` hand-run green (skill-file edits;
      LESSONS M56/M148).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1
- AC2 → T2, T4
- AC3 → T3, T4
- AC4 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: In `skills/milestone-review/SKILL.md` step 9 (~line 333), replace
      the "fires later in this same step" allusion with an explicit
      instruction to run `cairn_validate.py` over the completed hygiene
      edits before the docs-only commit, naming the `release window`
      advisory as step 10's signal.
- [x] T2: Rewrite step 10's next-action clause (~line 382): run
      `cairn_next.py` after the hygiene commit lands, lead the fenced next
      command with its recommendation, add the D-050 displacement clause
      deferring to `/milestone` §3's prescription, and delete the
      "`/milestone-plan` when planned or candidate work exists" wording.
- [x] T3: In `skills/milestone/SKILL.md` §3's example list (~line 156), add
      `/milestone-implement M<NNN>` — implement (a workable planned
      milestone exists) — as its own entry and narrow the `/milestone-plan`
      entry's condition to exclude planned items.
- [x] T4: Sweep `grep -rn "planned or candidate" skills/` (expect zero
      hits), run both gating suites checking each exit code explicitly, and
      hand-run `skills/tests` (edits sit near guarded regions — LESSONS
      M148).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-24: created by /milestone-plan.
- 2026-08-24: criteria audit ran in full mode ([O] fresh reader, three rounds): round 1 flagged AC2's unconditional cairn_next lead colliding with D-050 (fixed with the §3 displacement clause); round 2 flagged the displacement condition's missing instrument (fixed by mandating step 9's explicit validate run, which became AC1); round 3 passed every criterion on all five questions.
- 2026-08-24: plan gate chose a cairn_next.py-led step 10 over a corrected prose enumeration because the script is the single test-pinned routing authority and prose enumerations re-drift; falsified by a review close where the script's recommendation misroutes or cannot be run.
- 2026-08-24: plan gate chose an explicit step-9 cairn_validate run as the D-050 displacement signal over prose judgment of release-shape because the condition needs the mechanical instrument §3 already uses; falsified by the run proving too heavy or firing spurious advisories at review close.
- 2026-08-24: plan gate chose no new prose-guard test over pinning the new wording because a two-span prose fix does not warrant guard upkeep (pinned slices are brittle near future edits — LESSONS M148); falsified by a later edit reintroducing plan-for-planned routing unnoticed.
- 2026-08-24: implement started; branch m160-phase-close-routing; question gate skipped (plan gate settled all three open choices, no tripwires).
- 2026-08-24: T1 done — step 9 now instructs an explicit cairn_validate.py run over the hygiene edits before the docs-only commit, naming the release-window advisory as step 10's signal; both gating suites green (324 + 103, OK).
- 2026-08-24: T2 done — step 10 now runs cairn_next.py after the hygiene commit, leads the fenced next command with its recommendation, defers the D-050 release-parking displacement to /milestone §3, and no longer names /milestone-plan for existing planned work; both gating suites green (324 + 103, OK).
- 2026-08-24: T3 done — /milestone §3's example list gains an implement entry (workable planned milestone: deps done, nothing in-progress) distinct from resume, and /milestone-plan's condition narrows to exclude planned items; both gating suites green (324 + 103, OK).
- 2026-08-24: T4 done — `grep -rn "planned or candidate" skills/` zero hits (exit 1); hand-run skills/tests caught the T2 rewrap splitting the guarded phrase "as copyable lines" across a line break (test_copy_run_handoffs red), fixed by rewrapping; all suites green after fix: scripts 324 OK exit 0, hooks 103 OK exit 0, skills 528 OK. Status → review.
- 2026-08-24: review — AC1–AC4 verified fresh, gate clean; three-lens fan-out returned 11 findings (one lens), three fixed at the gate (F1/F2: step-10 displacement clause carries both halves of §3's prescription and names the parking chip carve-out; F4: §3 plan entry's candidate condition dropped), eight rejected with reasons; all suites re-run green.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->

PR: https://github.com/jmgirard/cairn/pull/161 (draft; branch current with origin/main at review start).

- AC1: verified 2026-08-24 — `git diff origin/main..HEAD -- skills/milestone-review/SKILL.md` shows step 9's "fires later in this same step" allusion replaced with an explicit instruction to run `cairn_validate.py` over the completed hygiene edits before the docs-only commit ("it must pass"), and names the `release window` advisory as the signal step 10's displacement clause reads.
- AC2: verified 2026-08-24 — same diff shows step 10 now instructs running `cairn_next.py` after the step-9 hygiene commit lands, leads the close block's fenced next command with its recommendation, carries the D-050 displacement clause deferring to `/milestone` §3's prescription (conditioned on step 9's `cairn_validate.py` run firing the `release window` advisory and the recommendation naming that release milestone), and `grep -n "milestone-plan" skills/milestone-review/SKILL.md` confirms step 10 no longer names `/milestone-plan` as the route for existing planned work (the "planned or candidate" clause is deleted).
- AC3: verified 2026-08-24 — `git diff origin/main..HEAD -- skills/milestone/SKILL.md` shows §3's example list gains `/milestone-implement M<NNN>` — implement (a workable planned milestone exists — its dependencies `done`, nothing `in-progress`) — as an entry distinct from the resume entry above it, and the `/milestone-plan` entry's condition reads "nothing in flight and no workable planned milestone; candidate items exist", excluding planned items.
- AC4: verified 2026-08-24 — fresh runs at review: `python3 -m unittest discover -s scripts/tests` 324 tests OK exit 0; `hooks/tests` 103 tests OK exit 0; hand-run `skills/tests` 528 tests OK exit 0.

Consistency gate 2026-08-24: `cairn_validate.py` all checks passed (exit 0; `release window` advisory quiet). No DESIGN.md principle changed → `cairn_impact --changed` skipped. Toolchain half: `generic` profile's `consistency-gate` slot names no checks — clean no-op. Sweep: `grep -rn "planned or candidate" skills/` zero hits (exit 1).

Independent review (user-facing tier → three-lens fan-out, 2026-08-24). [S] blame-history: no findings — both deleted passages traced (step 10 to M156/D-124, step 9's allusion to M99), neither deletion reverses a recorded decision; §3's displacement prescription predates M160. [S] prior-PR-comments: no prior-review evidence — archived reviews touching these files (M37, M40, M158) concern untouched regions; GitHub probe found zero inline PR comments. [O] diff-bug: 11 ranked findings, triaged:

- F1 (step 10 defers to §3's parking offer without naming its mechanism, colliding with the no-chip close): fixed at gate — clause now states the offer is a decision put to the user that keeps its chip (tracking-rules decision-gate carve-out), and the no-chip sentence carries the carve-out.
- F2 (step 10 adopted only the "lead" half of §3's prescription, dropping "offer whenever the advisory fired"): fixed at gate — clause now offers parking whenever the advisory fired and displaces the lead only when the recommendation names the flagged release milestone, matching §3.
- F3 (empty-backlog close now hands `/milestone-plan` where old prose handed `/milestone`): rejected — intentional; the plan gate chose cairn_next as the single routing authority and its empty-backlog recommendation is test-pinned (`test_scripts.py`).
- F4 (§3 plan entry's "candidate items exist" condition disagrees with cairn_next's empty-backlog behavior): fixed at gate — condition dropped; entry now reads "nothing in flight and no workable planned milestone", matching the script.
- F5 (cairn_next emits a label→command line, not a bare command): rejected — the line names its command explicitly; the recorded plan-gate falsifier (misroutes / cannot be run) has not fired.
- F6 (no degradation path for a missing python3): rejected — pre-existing repo-wide convention (step 4's validate run has none either; degradation documented once in /cairn-init), not introduced by this diff.
- F7 (review skill never rosters cairn_next.py in its header): rejected — style; the call site carries the full path and purpose inline.
- F8 (§3 implement entry's condition omits the review-outranks precedent): rejected — the list is declared state-conditional examples, not a precedence statement; cairn_next's pinned ladder governs the lead.
- F9 (duplicate command text resume/implement; list order ≠ script ladder): rejected — same basis as F8; parentheticals distinguish the entries.
- F10 (step 10's displacement paraphrase unguarded while §3's is pinned): rejected — the deliberate, logged plan-gate choice (no new prose-guard test), falsifier recorded in the work log.
- F11 (one 85-char line; `/clear` fenced vs tracking-rules' inline-mention classing): fixed in passing (the F1/F2 rewrap rewrapped the long line) / rejected (the `/clear` fence tension is pre-existing and unmodified).

Return floor: no finding demonstrates an acceptance criterion failing; no status change. Post-fix re-verification 2026-08-24: scripts 324 OK, hooks 103 OK, skills 528 OK (all exit 0); `cairn_validate.py` all checks passed; sweep still zero hits.
