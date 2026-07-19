<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M88: Release timing is user-declared — a release milestone stops nominating itself

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP2, GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m88-release-timing-user-declared`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make release timing a maintainer declaration rather than a routable milestone
state, so a release milestone parks silently until its window is opened.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Widen `blocked` so "the maintainer has not opened the release window"
is a legitimate blocker, and legalize the `planned → blocked` and
`review → blocked` transitions that parking requires. Add a release-shaped
tripwire to `/milestone-plan` so release framing cannot become a planned,
high-priority milestone without a declared window. Add a `release window`
advisory to `cairn_validate` that catches the drift back. Wire both into
`/milestone`'s audit and dispositions. Guards, tests, and D-050.

**Out:**
- Repairing intraclass M48 and circumplex M7 → handed back as a repair recipe,
  applied in each repo's own cairn session (separately tracked repos; this
  session does not commit tracking to them).
- A new status vocabulary word (`held`/`deferred`) and a `Release-window:`
  header slot → both declined at the M88 plan gate in favour of reusing
  `blocked`; rationale recorded in D-050, which is the entry to supersede.
- Changes to `/cairn-release` itself → it already never self-submits and the
  investigation found no defect in it; the defect is upstream, in how a
  release milestone is modelled.
- Detecting *whether a declared window is still open* (an expiry model) → no
  row; promote only if a declared window is ever found stale in practice.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `tracking-rules.md` states that a maintainer who has not opened the
      release window is a legitimate `blocked` blocker, and the transition line
      admits `planned → blocked` and `review → blocked`. Verified by inversion
      (LESSONS M74): relabel or negate the rule in place, run the skills suite,
      require red, restore and diff.
- [ ] AC2 — `/milestone-plan` carries a release-shaped tripwire at its question
      gate: a release-framed request must ask the user to declare the window,
      and absent a declaration lands as a `candidate` row, never a `planned`
      milestone. Guard-locked with the label pinned to its rule on one physical
      line (LESSONS M74).
- [ ] AC3 — `cairn_validate` emits a `release window` advisory that WARNs on a
      release-shaped milestone being nominated, and is exit-code neutral in
      every case. The trigger is status-dependent, because idleness means
      different things at different statuses: a `planned` release whose
      dependencies are all satisfied WARNs immediately (a routing surface is
      nominating it *now*, and its work log records only queueing, never work),
      while an `in-progress` or `review` release WARNs once its work log goes
      14+ days idle (work started, then stalled). It prints a positive
      `OK release window` signal on the clean path, so an absence-assert cannot
      pass over a crash (LESSONS M84).
- [ ] AC4 — Detection requires **both** a word-bounded release token and a
      version pattern, so a milestone about release *tooling* raises nothing:
      fixtures in a routable status titled like this repo's own M47
      ("Release-walk slot"), M54 ("Release positioning"), and M62 ("Release
      docs") each produce zero findings, while fixtures titled like intraclass
      M48 ("v0.1.0 release consolidation") and circumplex M7 ("v2.0.0 CRAN
      release preparation") each produce one.
- [ ] AC5 — `/milestone` reports the advisory in its §2 audit and offers a
      park-as-`blocked` disposition in its §3 route; the disposition names the
      work-log line the parked milestone gets. Guard-locked.
- [ ] AC6 — The `generic` profile's `verify` slot is clean: all three suites
      green from the repo root with exit codes checked individually, never
      piped (LESSONS M56+M65).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T6
- AC2 → T2, T6
- AC3 → T3, T5
- AC4 → T3, T5
- AC5 → T4, T6
- AC6 → T5, T6, T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — `tracking-rules.md`: widen the `blocked` row of the status table and
      the surrounding prose to name the unopened release window as a blocker;
      amend the transition line (`:225`) to admit `planned → blocked` and
      `review → blocked`. Author each guarded anchor on its own physical line,
      unwrapped and unique (LESSONS M78/M82).
- [x] T2 — `/milestone-plan` SKILL.md: add the release-shaped tripwire to the
      question-gate step, stating the default (candidate row) and what a
      declared window must say.
- [x] T3 — `scripts/cairn_validate.py`: add `check_release_window` and register
      it in `ADVISORIES`. Word-bounded token match (`\bCRAN\b`, `\brelease\b`,
      `\bsubmission\b`) **and** a version pattern, over title and goal; routable
      status; 14-day work-log recency reusing the existing date parsing.
- [x] T4 — `/milestone` SKILL.md: report the advisory in §2 and add the
      park-as-`blocked` disposition to §3's list, pinned label-with-rule on one
      line.
- [ ] T5 — `scripts/tests/test_scripts.py`: advisory unit tests — parked
      (`blocked`, silent), actively released (recent work log, silent), stale
      routable release (WARN), the three tooling-title false-positive fixtures,
      the two true-positive fixtures, and exit-code neutrality on every path.
- [ ] T6 — `skills/tests/`: prose guards for T1, T2, and T4; register each
      guard *file* in `test_mutation_harness.py` with at least one exemplar
      block, and pair any `assertNotIn` with a positive framing assert
      (LESSONS M53).
- [ ] T7 — Append D-050 recording the mechanism choice and the two declined
      alternatives; ROADMAP hygiene.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-19: created by /milestone-plan.
- 2026-07-19: status planned->in-progress; branch cut; no open implementation choices, question gate skipped.
- 2026-07-19: T1 — rulebook widens `blocked` to the unopened release window, legalizes planned/review -> blocked, and adds the release-timing governance rule; skills suite 386 green.
- 2026-07-19: T2 — /milestone-plan gains the release-shaped tripwire: window declared explicitly or the work lands as a candidate row, never planned/high.
- 2026-07-19: T3 — `release window` advisory added to cairn_validate; AC3 amended at the implement gate (M88-D1) after the planned idle-only rule proved silent on intraclass M48; live-fire: M48 WARNs, circumplex M7 silent (actively shipped), cairn silent; three suites green.
- 2026-07-19: T4 — /milestone §2 reports the `release window` WARN without arguing with it; §3 gains the park-as-`blocked` chip option, which leads the chip when the advisory fired (cairn_next's own recommendation is the nag in that case).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

### M88-D1 (2026-07-19): The release advisory's trigger is status-dependent, not idle-only

**Context:** T3's planned rule — WARN on a routable release-shaped milestone
idle 14+ days — was implemented and then run against the two repos that
motivated M88. It stayed silent on both. circumplex M7 was correct (worked
that day), but intraclass M48 was the exact nag case and went undetected: it
had sat `planned` for a week with all eight dependencies satisfied while every
work-log entry it carried was a `Depends-on` amendment recording that another
milestone had been slotted ahead of it. Each of those refreshed the idle
clock, so "no work log in N days" measured when the *file* was last touched,
never when the *release* was last worked.
**Decision:** Split the trigger by status. A `planned` release WARNs the moment
its dependencies are all satisfied — the moment `cairn_next` begins naming it —
because a planned milestone's log records queueing, never work, so idleness
cannot speak there. `in-progress`/`review` keep the 14-day idle rule, since
work that genuinely started can genuinely stall. Rejected warning on every
routable release regardless of state: it would fire at a maintainer
mid-release, which is the nag fatigue D-017 rejected.
**Consequences:** AC3 amended at the implement gate. Dependency satisfaction is
computed exactly as `cairn_next` computes it (done rows ∪ archive files), so
the advisory and the router agree on what "being nominated" means by
construction.

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
