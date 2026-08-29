<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M163: External adoption pass (RR13 step 3)

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR13 is advisory (no Binding criteria); lineage in Goal -->
- **Principles touched:** IP3, GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m163-external-adoption-pass   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Run cairn's first external adoption pass (RR13 step 3; promoted from the
RR13 Q10 candidate row): `/cairn-init` and one full milestone loop on
**bsync** — a repo not shaped around cairn's assumptions, carrying a
precursor milestone system (`MILESTONES.md`, `DESIGN.md`), so init takes
its never-exercised migration path — logging every friction event and
fixing in cairn what the pass breaks.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**Tier: user-facing** — the fixes land in surfaces external adopters
consume (`/cairn-init`, README, rulebook); the pass record is internal, and
the spanning deliverable takes the user-facing tier (full audit mode).

**In:** the init/migration run on bsync (r-package profile); one genuine
bsync backlog item through plan → implement → review → merge there; an
`F<n>` friction ledger in this file's work log; a disposition for every
F-entry; in-scope fixes landed in cairn tests-first.

Findings capture is honor-system by construction: no procedure enumerates
"friction events that occurred", and a friction observation logged without
an `F<n>` marker escapes AC3's domain — accepted at the plan gate (no
minimum-findings floor; a quota would manufacture findings, the M130
shape). AC3 is likewise satisfiable with zero fixes (every disposition
"declined") — dispositions are the promised mechanism; which fixes land is
implement-time judgment under the gate's small-fixes-here answer.
Review evidence for AC1/AC2 lives in bsync: review quotes it into this
file's Review section with the bsync refs it read, so verification never
rests on ambient access.

**Out:** second-person-driven pass → new candidate row (this commit);
contributor-scaffold and branch-protection work → their existing candidate
rows, cross-referenced (T4 checks whether pass findings fire their
promote-conditions); README-flow-diagram fallback → not taken (external
repo available; RR13 prose remains its record); fixes exceeding this
milestone's sessions → routed as candidate rows at T3.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: bsync's default branch, at the commit completing the
      `/cairn-init` run, holds the cairn scaffold — the `cairn/` tracking
      files, the CLAUDE.md cairn section, and an instantiated
      `cairn/PROFILE.md` (r-package profile); every milestone entry
      bsync's pre-init `MILESTONES.md` holds — enumerated by reading that
      file at the pre-init commit from git history — appears in the
      migrated tracking records or in the init run's migration ledger with
      a disposition; and `cairn_validate` run in bsync at the
      init-completing commit exits 0.
- [ ] AC2: bsync's default branch holds one completed cairn milestone: a
      milestone file carrying cairn's template sections, its archive
      summary under bsync's `cairn/milestones/archive/`, a `done` row in
      bsync's ROADMAP, and a merge commit landing that milestone's branch
      on the default branch.
- [ ] AC3: Every friction finding numbered `F<n>` in this milestone file's
      work log — the domain a sweep of the work log for `F<n>` markers
      enumerates — carries exactly one current disposition: fixed (naming
      the cairn commit that landed the fix), routed (naming the ROADMAP
      candidate row added), or declined (with a stated reason); a later
      appended entry supersedes an earlier one.
- [ ] AC4: The generic profile's verify slot clean — `python3 -m unittest`
      over `scripts/tests` and `hooks/tests` both exit 0 at the review ref
      (template-mandated for code milestones; fixes may touch
      `scripts/`/`hooks/`).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1
- AC2 → T2
- AC3 → T1, T2, T3, T4
- AC4 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: In bsync, run `/cairn-init` (migration path expected for
      `MILESTONES.md`/`DESIGN.md`; r-package profile), land the result on
      bsync's default branch through its approval gate; log each friction
      observation as an `F<n>` work-log entry here as it occurs.
- [x] T2: In bsync, take one genuine backlog item through the full loop —
      `/milestone-plan` → `/milestone-implement` → `/milestone-review` →
      merge + archive — logging friction as F-entries here as it occurs.
- [ ] T3: Disposition every F-entry (fixed / routed / declined); land
      in-scope fixes in cairn tests-first per the universal test floor
      (test scope: each fixed friction's changed behavior), both gating
      suites green; route larger findings as candidate rows.
- [ ] T4: Update the DESIGN.md Known-issues single-author/no-external-
      adopter bullet to reflect the pass; check the contributor-scaffold
      and branch-protection candidate rows against the F-ledger — promote
      any whose stated condition fired, else record checked-and-standing.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-29: created by /milestone-plan; promoted from the RR13 Q10 candidate row (row stays until completion per records-hygiene §1).
- 2026-08-29: plan-gate criteria audit ran in full mode (user-facing tier), fresh [O] reader, two passes — pass 1: 18 findings (AC2 provenance→artifact rebind; AC3 "exactly one disposition" vs IP4 fixed with the currency rule; draft AC4 test-per-fix dropped as instrument-binding, moved to T3; empty-ledger vacuity posed at the gate); pass 2 over revised wording: 14 findings, fixed as prescribed (migration conservation rebound from the run's own ledger to pre-init `MILESTONES.md` read from git history; "authored from template"→"carrying template sections"; honor-system capture and zero-fix satisfiability acknowledged in Scope). Shipped AC4 (verify slot) retained on the template's code-milestone mandate notwithstanding the pass-1 instrument shape.
- 2026-08-29: plan gate chose bsync over facs/rlmstudio/glmmTMB-fork because it pairs the never-run migration path and r-package profile with real ownership through merge; falsified by the migration path dominating the signal (most F-entries migration-only).
- 2026-08-29: plan gate chose solo-driven over second-person because no second driver is lined up; falsified by the solo pass missing author-blind friction classes; deferred as a candidate row.
- 2026-08-29: plan gate chose loop-through-merge over stop-at-review because merge/archive/hygiene held past defects (M105, M111 lessons); falsified by the merge leg yielding no findings at material session cost.
- 2026-08-29: plan gate chose small-fixes-here over observation-only because same-session fixes keep the demand signal actionable; falsified by T3 fix work crowding out the pass (thrash on T3).
- 2026-08-29: plan gate chose acknowledge-no-floor over a minimum-findings quota because no procedure enumerates friction events (M130); falsified by a demonstrably frictionful pass logging zero F-entries.
- 2026-08-29: implement gate: T2 item = bsync M8 (phase synchrony, roadmap's next); driving mode = this session, cwd in bsync (M162 cross-repo contract), F-entries logged here as they occur.
- 2026-08-29: T1 in progress: /cairn-init on bsync detected the migration path (root MILESTONES.md/DESIGN.md, status-in-CLAUDE, 3 tracking-coupled skills); disposition gate accepted run-as-proposed; migration committed on bsync branch cairn-init-migration, PR jmgirard/bsync#2 open with ledger, cairn_validate green in bsync; awaiting CI then merge gate.
- 2026-08-29: F1: multi-repo driving — the harness resets shell cwd to the primary repo after every Bash call, so every bsync command needs a cd prefix and the tracking-rules multi-repo clause ("a secondary repo's merge runs from a session cwd inside that repo") is easy to get wrong; whether merge_guard accepts the compound `cd <repo> && gh pr merge` spelling needs verification at the bsync merge.
- 2026-08-29: F3: cross-repo merge denial confirmed live (F1's concern): with session cwd in cairn, `cd bsync && gh pr merge 2` was denied twice — merge_guard resolves the repo from the hook payload's session cwd, so it checked cairn's marker, not bsync's (the documented M162 `cd ../other` limitation, hit on the contract's own recommended path in a harness that resets cwd); the denial's remediation text ("recreate it and rerun") invites recreating the marker in the wrong repo, which would let the primary repo's marker authorize the secondary repo's merge; correct path taken: move the session cwd into bsync (change_directory) and merge plain.
- 2026-08-29: T1 done: bsync PR #2 squash-merged at user approval (bsync main 5112c2f); all 8 CI checks green pre-merge; cairn_validate exits 0 on bsync main; marker consumed by the guard. F3 addendum: the correct path (session cwd inside bsync) required change_directory, which applies only at a user turn boundary — the merge stalled until the user nudged, so an autonomous multi-repo session cannot complete a secondary repo's merge unaided.
- 2026-08-29: F2: cairn-init §1 mandates LESSONS.md ("header + correct-in-place note") and the DECISIONS.md file header, but no template ships for either (decision.md shows only the entry shape; templates/ has no lessons or decisions-header file), so the session reconstructed both from cairn's own dogfood files — a surface an external adopter's session does not have; header shapes would be invented per adoption.

- 2026-08-29: T2 in progress: bsync M008 (phase synchrony) planned via /milestone-plan cross-repo (bsync main 52b7b2e); full-mode criteria audit ran twice with fresh [O] readers (both passes returned substantive findings, all disposed); two user gates (4+2 questions), all recommendations accepted; sizing advisory (8 ACs) accepted as one vertical slice.
- 2026-08-29: T2 progress: bsync M008 implemented through status review (branch m008-phase-synchrony, 8 commits): wphase estimator + surrogate wrapper, 3-oracle-type suite (closed-form Dirichlet, frozen MNE pin, simulation calibration; live pure-R as depth), check() 0/0/0; no new F-entries — the cairn implement loop ran clean cross-repo (gates, checkpoints, verify slot all as documented).

- 2026-08-29: T2 done: bsync M008 merged (PR bsync#3 squashed as a8f269a, CI 8/8, all 8 ACs fresh-evidenced, 3-lens review with 18 findings triaged) and archived with post-merge hygiene (done row, 25-line archive summary, 3 LESSONS lines, validate green) — the full loop plan→implement→review→merge→archive ran cross-repo; the merge-approval marker + `gh pr merge 3 --squash` worked first try from the bsync session cwd.


## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md. -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->
