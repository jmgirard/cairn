# M151: The instrument question reaches the reduced audit

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m151-instrument-question-both-modes · https://github.com/jmgirard/cairn/pull/152

## Goal

The plan-gate criteria audit asks its deliverable-vs-instrument question in
both modes and names record properties in the question's genus, so a
recording-clause criterion — the shape that cost circumplex M101 two defect
returns through the reduced audit — is a finding at the gate in every tier.

## Scope

Surface tier: **user-facing** — the deliverable is rule prose in two shipped
skills that every cairn-adopting repo's plan and amendment gates execute
(M148 precedent).

**In:** three prose edits and two records. (1) `/milestone-plan` step 3's
reduced audit gains the instrument question, executing D-118's pre-registered
falsifier on the circumplex M101 evidence. (2) That question's exemplar
genus gains properties of the record the work leaves — a work-log recording
act, a mandated evidence quotation — so the M101 shape is in-domain on the
question's own wording. (3) `/milestone-implement` step 6's re-entry
sentence drops its full-mode qualifier on the instrument question. (4) A
D-entry recording the supersession of D-118's mode clause and D-111's
reduced-mode question enumeration, with the interpretive step stated
explicitly. (5) One candidate ROADMAP row deferring review-side
reclassification of record-binding criterion failures.

**Out:** any change to `/milestone-review`'s return classification or to
`tracking-rules.md`'s review prose → the AC5 candidate row, promoted only on
its falsifying condition. A minimal-diff repair doctrine → dropped at the
user's explicit decision (plan gate 2026-08-21). Retro-repair of milestones
already carrying recording-clause criteria in downstream repos → those
repos' own gates, under the existing amendment protocol.

## Acceptance criteria

- [x] AC1: The shipped step-3 text of `/milestone-plan` assigns the
      deliverable-vs-instrument question to both audit modes: the
      reduced-audit sentence lists it among the questions the reduced audit
      asks, and no step-3 sentence attributes the question to one mode.
- [x] AC2: The instrument question's exemplar list in `/milestone-plan`
      step 3 names a property of the record the work leaves — at minimum a
      work-log recording act or a mandated evidence quotation — among the
      instrument properties whose binding by a criterion is a finding.
- [x] AC3: `/milestone-implement` step 6's re-entry sentence no longer
      conditions the instrument question on full mode: the questions it
      names as asked of amended wording include the instrument question in
      whichever mode the tier assigns.
- [x] AC4: `cairn/DECISIONS.md` carries a new entry that (a) quotes D-118's
      pre-registered falsifier verbatim, (b) states explicitly the reading
      it takes — record properties fall within the question's "among others"
      genus, and circumplex M101's recording-clause criteria are the
      shipped-behavior instance — with the M101 evidence verified against
      and cited to that repo's milestone file (internal tier; reduced audit
      run 2026-08-21; recording clauses costing defect returns 1 and 2),
      (c) stands on D-108's door trigger directly as well as the falsifier,
      and (d) names what it supersedes: D-118's mode clause and D-111's
      reduced-mode question enumeration.
- [x] AC5: The review-side reclassification of record-binding criterion
      failures is captured as exactly one candidate ROADMAP row whose
      promotion condition names the class of evidence that would falsify
      plan-gate-only prevention — a milestone whose criteria passed the
      extended audit still costing a defect return on a record-binding
      clause.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4

## Tasks

- [x] T1: Edit `skills/milestone-plan/SKILL.md` step 3 — the reduced-audit
      sentence (~line 152–156) gains the instrument question; the exemplar
      list (~line 137–145) gains the record properties. Do not echo any
      pinned guard phrase ("The instrument is a reader and never a check";
      the M121 three-of-five sentence); hand-run `skills/tests` after.
- [x] T2: Edit `skills/milestone-implement/SKILL.md` step 6 (~line 104–110)
      — the re-entry sentence drops "and, in full mode," so the instrument
      question rides the assigned mode like the others.
- [x] T3: Re-verify the M101 evidence against
      `circumplex/cairn/milestones/M101-startup-failure-reachability-probe.md`
      (reduced-audit work-log line of 2026-08-21; returns 1 and 2 called on
      recording clauses), then append the AC4 D-entry; `cairn_validate`.
- [x] T4: Add the AC5 candidate ROADMAP row (search-first sweep first), then
      restatement sweep: `grep -rn "instrument question\|reduced audit\|full
      mode\|full-mode"` over `skills/`, `README.md`,
      `skills/shared/templates/`; disposition every hit.
- [x] T5: Run both gating suites (`python3 -m unittest` over `scripts/tests`
      and `hooks/tests`) and hand-run `skills/tests`; record exit codes.

## Work log

- 2026-08-21: created by /milestone-plan, from the circumplex M101 thrash question (two defect returns on recording-clause criteria through the reduced audit).
- 2026-08-21: criteria audit (full mode, fresh [O] reader, user-facing tier) returned five findings, all fixed in the drafted wording before the gate: AC5 split off its git-diff scope guard (instrument property + proxy domain — the guard moved to Scope Out and the gate's diff read); AC4 gained the explicit interpretive step curing its circular warrant (falsifier terms supplied by this milestone's own genus widening) plus direct reliance on D-108's door trigger; AC2's evidence dependency answered by T3's re-verification clause; AC1's negative clause strengthened from "names it as omitted" to "attributes the question to one mode"; AC3 clean.
- 2026-08-21: plan gate chose extending the plan-gate question (mode + genus) over shipping a review-side reclassification now because one new verification rule per milestone is the growth bound the repo has been burned past, and plan-time prevention should prove itself first; falsified by a milestone whose criteria passed the extended audit still costing a defect return on a record-binding clause (the AC5 row's promotion condition).
- 2026-08-21: plan gate chose dropping the minimal-diff repair doctrine over a candidate row because record-binding criteria are the dominant generator of repair rounds and the doctrine is hard to state without new judgment surface; falsified by a repair's own rewrites causing a further return on a milestone with no record-binding criteria.
- 2026-08-21: checker-regress shape dispositioned not-fired: the criteria audit is a reader whose findings are disposed at a gate, never a check ("The instrument is a reader and never a check", D-059's retirement precedent); the simplify pole was still posed at the gate as the do-nothing option and declined.
- 2026-08-21: collision sweep — D-118's mode clause and D-111's reduced-mode enumeration are superseded by design (D-118's own falsifier prescribes it); D-108's door trigger satisfied per D-098's cross-repo pattern (shipped reduced-audit behavior measured costing circumplex M101 two returns); the "Stakes-tier follow-through" and "Standing-instrument adoption discipline" candidate rows are adjacent, not overlapping — no instrument is adopted and no tier mechanics change.

- 2026-08-21: T1+T2 — step 3's instrument question now opens "The audit — in both modes —", its exemplar list gains "a work-log recording act, a mandated evidence quotation" and cites D-120; the reduced-audit sentence lists bounded-promise, proportionality, and instrument, omitting satisfiability/reachability/probe; step 6's re-entry sentence reads "the proportionality and instrument questions included in either mode". No pinned guard phrase touched; suites skills/scripts/hooks exit 0/0/0 (513 prose guards OK).
- 2026-08-21: T3 — M101 evidence re-verified against circumplex's milestone file (internal tier in Scope; reduced-audit work-log line dated 2026-08-21; return 1 the G7/G8 "unmet as written" repairs of AC2's named-command and AC3's per-case recording clauses; return 2 the F1 repair of AC5's quotation clause); D-120 appended; `cairn_validate` exit 0, all checks passed, dangling-ids OK with the SKILL.md forward reference now resolved.
- 2026-08-21: T4 — candidate row added (search-first: no existing row, archive entry, or D-heading covers review-side reclassification; the Stakes-tier and Standing-instrument rows re-checked as adjacent only); restatement sweep over skills/, README.md, templates: five hits, three are this milestone's own new text, milestone-brief:126 names the ingest audit's full mode which D-111 keeps full-audited (correct as stands), milestone-plan:122 is the mode-selector sentence (unchanged by design).
- 2026-08-21: T5 — explicit exit codes on the merged working tree: skills/tests 0 (513 tests), scripts/tests 0, hooks/tests 0, `cairn_validate` 0; all tasks checked; status → review.

## Decisions

## Review

**AC evidence (fresh, 2026-08-21, read from the working tree at the review pass).**

- AC1: step 3 re-read whole — the reduced-audit sentence reads "The reduced audit asks only the bounded-promise, proportionality, and instrument questions"; the question paragraph opens "The audit — in both modes — also asks"; the only step-3 sentences containing "instrument" besides these use it for the audit-as-reader ("The instrument is a reader and never a check", the M121 sentence), and the two "in the mode that asks it" clauses attach to the probe question, which stays full-mode. No sentence attributes the instrument question to one mode. Met.
- AC2: the shipped exemplar list reads "— a test harness, a floor, a plant matrix, a checker's own prose, a work-log recording act, a mandated evidence quotation, among others (D-118, extended by D-120)", and the property clause reads "or of the record the work leaves". Both named record properties present. Met.
- AC3: `skills/milestone-implement/SKILL.md` step 6 re-read fresh — the re-entry sentence reads "the proportionality and instrument questions included in either mode"; no full-mode qualifier remains on the instrument question in that file (`grep -n "full mode" skills/milestone-implement/SKILL.md` returns nothing — run at this pass, exit 1, zero hits). Met.
- AC4: D-120 re-read whole and checked mechanically (whitespace-normalized string comparison, run at this pass): D-118's falsifier sentence appears in D-120 verbatim (True); the entry states the "among others" genus reading and the M101 instance explicitly; cites the evidence to the circumplex milestone file (internal tier; reduced audit 2026-08-21; two defect returns with the G7/G8 and F1 repairs named); stands on D-108's door trigger directly, hosted per D-098; names both supersessions (D-118's mode clause quoted, D-111's reduced-mode enumeration quoted). Met.
- AC5: `grep -c "Review-side reclassification of record-binding" cairn/ROADMAP.md` = 1 (run at this pass) — exactly one row; its promotion condition reads "Promote when a milestone whose criteria passed the extended audit (D-120) still costs a defect return on a record-binding clause — never on a count of legacy-milestone returns", the falsifying evidence class. Scope-Out cross-check: `git diff main...HEAD --name-only` (run at this pass) lists five files, none of them `skills/milestone-review/SKILL.md` or `skills/shared/tracking-rules.md`. Met.

**Consistency gate (2026-08-21).** `cairn_validate` exit 0, all checks passed. No DESIGN.md principle changed — `cairn_impact` skipped. Generic profile: consistency-gate slot names no toolchain checks; the two gating suites plus the hand-run prose guards re-run fresh at this pass, explicit exits scripts 0 / hooks 0 / skills 0. Caps: ROADMAP 45/60 lines, 12,434/24,000 bytes; LESSONS 42/50 lines, 11,789/20,000 bytes. No changelog entry owed (release-time consolidation per the changelog slot). No CI on this repo (PROFILE consistency-gate note) — mergeable on local green.
