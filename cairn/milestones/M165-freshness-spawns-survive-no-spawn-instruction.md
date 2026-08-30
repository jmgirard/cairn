<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M165: Freshness spawns survive a no-unrequested-subagents harness instruction

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** IP2, GP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m165-freshness-spawns-survive-no-spawn-instruction · https://github.com/jmgirard/cairn/pull/166   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Sessions under a harness instruction restricting subagent spawns to ones the
user requested resolve the conflict with cairn's freshness-mandated readers
and reviewers by asking the user at the pending gate, never by silently
degrading to an author-inline run.

## Scope
<!-- owner: plan · create/amend-via-gate -->

Surface tier: **user-facing** — the deliverable is skill conduct for every
adopter of the plugin, and adopter repos (hitop M048–M067, quarto-index
M30/M31, tidymedia M089) have run degraded author-inline reviews and criteria
audits under this instruction since 2026-08-23. That degradation is the
shipped-behavior defect D-090/D-108's door requires as trigger (recorded at
the plan gate; hosted per D-098).

**In:** Some Claude Code surfaces append two bare lines to the system prompt
— verbatim: "Do not call the AgentTool unless the user requested it" and "Do
not use workflows or deep-research unless the user requested it" (quoted from
a live affected session, 2026-08-30). This milestone adds one clause to
`skills/shared/tracking-rules.md` "Model and agent strategy" resolving the
first line's conflict with the freshness spawns (the line's own carve-out is
user request), pointers at the spawn-mandating sites, a hand-run prose guard,
and a README consistency sweep.

**Out:** covering the second line (workflows/deep-research) — cairn mandates
neither, so it gates nothing of ours; revisit only on defect evidence.
Retroactive re-review of the nine degraded adopter milestones — left as
logged deviations at the user's 2026-08-30 gate choice. The user-side
`~/.claude/CLAUDE.md` line — handed to the user at this plan's close, their
edit, not plugin work (GP4 puts the shared fix here, not there).
Pre-committed classification for AC2's sweep: `milestone-review/SKILL.md:392`
("the natural next step is a fresh context") is close-block prose about the
user clearing session context, not a spawn mandate — outside AC2's "prose
mandating a spawn" filter.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: The "Model and agent strategy" section of
  `skills/shared/tracking-rules.md` states all three: (a) a user's invocation
  of a cairn skill is the user's request for the subagent spawns that skill's
  steps mandate, satisfying a harness instruction restricting subagent spawns
  to ones the user requested; (b) a session that still cannot or will not
  spawn a freshness-mandated reader or reviewer surfaces the conflict at its
  phase's pending user gate — for review, the merge-approval chip, with the
  review declared degraded (author-inline) — asking the user to request the
  spawns in so many words; (c) an inline author-run is permitted only as a
  user-accepted, logged deviation naming the instruction, never silent.
  Evidence: the section's shipped text.
- [x] AC2: Every line returned by `grep -rni 'fresh[- ]context'
  skills/*/SKILL.md skills/shared/*.md` that sits inside prose mandating a
  spawn either carries, at that site, a pointer to the "Model and agent
  strategy" clause AC1 names, or lies inside that clause's own host section
  (Scope pre-commits the one non-mandating hit). Evidence: the grep output
  read against the shipped files.
- [x] AC3: Every line returned by `grep -rniE 'reviewer|fan-out|fresh
  session|criteria audit' README.md` (non-empty today; state the hit count at
  the gate) states conduct consistent with AC1's clause. Evidence: the grep
  output read against the clause.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T3
- AC2 → T2
- AC3 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Author AC1's clause (a)–(c) in `skills/shared/tracking-rules.md`
  "Model and agent strategy", beside the freshness-warrant bullet (~line
  361). Note: chip text carries what "degraded (author-inline)" means in
  plain words, no record identifiers (Accessible-language rule).
- [x] T2: Run AC2's grep; add the pointer at every spawn-mandating hit
  outside the host section (`milestone-plan` step 3, `milestone-brief` ingest
  audit ~line 105, `milestone-implement` step 6 ~line 109, `milestone-review`
  step 5 ~lines 149–160); disposition every hit in the work log, the Scope
  pre-commit included.
- [x] T3: Add a hand-run prose guard in `skills/tests` pinning AC1's
  operative sentences (mind the M148 locator-uniqueness lesson); run both
  gating suites and hand-run `skills/tests`.
- [x] T4: Run AC3's grep; read each hit against the clause; align any
  contradicting README text (M112 lesson: doctrine wording has more surfaces
  than the skills it edits).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-30: created by /milestone-plan, from the user's report that the new Claude version instructs sessions against spawning subagents; instruction text confirmed verbatim via a live affected session (tidymedia-ad).
- 2026-08-30: criteria audit ran in **full** mode (user-facing tier), fresh-context [O] reader, two passes (initial draft, then the gate-amended wording). Pass 1: 8 findings — 4 fixed (instrument-bound evidence clause; open "of the form" family; AC2's recording-act half; AC2's unshippable referent), 2 posed at the gate (review-phase gate location; sweep width), 1 door-record, 1 coverage note (T4 gained AC3). Pass 2: 3 findings fixed (line-392 classification pre-committed in Scope; AC3's vacuous grep replaced — the original pattern returned zero README lines and would have certified a contradicting README; chip-wording residual moved to T1), 1 judgment taken autonomously (second harness line left Out).
- 2026-08-30: plan gate chose the plugin doctrine clause (plus handing the user a personal CLAUDE.md line) over a user-side-only CLAUDE.md workaround because other adopters would stay degraded (GP4); falsified by sessions still degrading silently after the clause ships.
- 2026-08-30: plan gate chose surfacing the review-phase conflict at the merge-approval chip (review declared degraded) over a fourth user gate at review step 5 because the three-gate rule already provides that chip; falsified by a degraded review accepted at the merge chip shipping a defect a pre-review gate would have blocked.
- 2026-08-30: plan chose covering only the AgentTool instruction line over widening to the workflows/deep-research line because cairn mandates neither workflows nor deep-research, so that line gates nothing of ours; falsified by a cairn skill acquiring a workflow or deep-research mandate, or defect evidence under that line.
- 2026-08-30: T1 done — "Freshness spawns under a spawn-restricting harness instruction" bullet added to tracking-rules "Model and agent strategy" beside the freshness-warrant bullet, stating AC1's (a)–(c) plus the plain-words chip sentence; suites green (scripts 326, hooks 121).
- 2026-08-30: T2 done — AC2 grep returned 8 hits; pointers added at the four spawn-mandating sites (brief:105 ingest audit; implement:109 amendment re-audit; plan:123 criteria audit; review step 5, one pointer for its 149/155/160 block, per the plan's site enumeration); review:393 is the Scope-pre-committed non-mandating hit (close-block prose); tracking-rules:376 lies inside the clause's host section; suites green (scripts 326, hooks 121).
- 2026-08-30: T3 done — `skills/tests/test_freshness_spawn_instruction.py` pins AC1's (a)–(c) plus the chip plain-words sentence, four mutation-registry entries on unique locators; the implement:109 pointer had split `test_fresh_context_readers`' pinned slice (2 reds), relocated past the slice per the M148 lesson (new sentence moved, pinned prose untouched); all suites green (scripts 326, hooks 121, skills 532 hand-run).
- 2026-08-30: T4 done — AC3's grep returned 6 README lines (12, 116–118, 126, 279); each read against the clause: rigor-scaling (12), independent reviewer agents at review (116–118), fresh-session-per-phase advice (126), and fan-out-as-conduct-rule (279) — none contradicts AC1's clause, no README edit needed; suites green.

- 2026-08-30: review — all three ACs passed fresh; fan-out 13/0/0 findings; user triaged fix F2/F4/F5 (D-127; trigger-subject pins; greppable clause name), reject 10; merge approved at the chip.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->

- AC1: PASS — `skills/shared/tracking-rules.md:364-371` ("Freshness spawns under a spawn-restricting harness instruction") states (a) skill invocation is the user's request for the mandated spawns, (b) a still-blocked session surfaces the conflict at its phase's pending user gate (review: merge-approval chip, declared degraded author-inline) asking the user to request the spawns, (c) inline author-runs only as a user-accepted, logged deviation naming the instruction. Read fresh 2026-08-30.
- AC2: PASS — the grep returned 8 hits. Spawn-mandating hits with the pointer at-site: brief:105 (ingest audit), implement:109 (amendment re-audit), plan:123 (criteria audit), review:160-162 (one pointer for the step-5 149/155/160 block). review:393 is the Scope-pre-committed non-mandating hit (close-block prose about clearing context); tracking-rules:376 lies inside the clause's host section. All 8 dispositioned.
- AC3: PASS — the grep returned 6 README lines (12, 116-118, 126, 279); each read against the clause: rigor-scaling (12), independent reviewers at review with stakes routing (116-118), fresh-session-per-phase advice (126), fan-out as conduct rule (279). None contradicts the clause; no edit needed.
- Consistency gate: `cairn_validate` all checks passed (exit 0); no DESIGN.md principle changed → `cairn_impact` skipped; profile `generic` → toolchain half a clean no-op. Suites: scripts 326, hooks 121, skills 532 hand-run — all green.
- Driving RR: none → projection-vs-outcome no-ops.
- Fan-out (full, three lenses; diff includes .py test files): [S] blame-history — no findings (door record, locator relocation, mutation uniqueness, section history all verified). [S] prior-PR-comments — no prior-review evidence (probe found no real PR threads; M148 lesson honored in-branch). [O] diff-bug — 13 ranked findings, triaged below.
- F1 (clause circular in time — chip acceptance follows the inline run): rejected — the plan gate chose the merge-chip location with a recorded falsifier (work log 2026-08-30); acceptance at the chip covers the run before anything merges, and a decline re-runs the review with spawns.
- F2 (the clause narrows two fresh-context absolutes — tracking-rules:376, D-067 — with no D-entry; milestone Decisions empty): fix now — append a D-entry recording the freshness-spawns clause and what it narrows.
- F3 (no pointer at the merge-chip site, review step 7): rejected — the step-5 pointer loads the clause at the moment the conflict is discovered, and the clause itself states the chip conduct; duplicating the pointer at step 7 adds no new load point.
- F4 (prose guard pins only the predicate halves of (a) and (b) — deleting the trigger subjects stays green): fix now — extend both regexes to pin the trigger subjects, with matching mutation-registry entries.
- F5 (pointers name "freshness-spawns" but that token greps to nothing in tracking-rules.md): fix now — make the token findable at the bullet.
- F6 (IP2 tension — happy path reinterprets the harness instruction silently): rejected — clause (a) is definitional (the invocation is the request), so the instruction is satisfied, not overridden; there is no prior state to surface.
- F7 ("logged deviation" has no defined home): rejected — the universal rule "User overrides are logged … in the work-log" already names the home.
- F8 ("cannot or will not spawn" is a self-declared escape hatch): rejected — the hatch leads to the user gate, not past it; nothing merges without explicit acceptance, which is the milestone's goal.
- F9 (review:155 mandates a spawn with the pointer one paragraph below): rejected — the plan's T2 enumerated the 149–160 block as one site; block-level grouping is the plan's recorded call, not a review-side reinterpretation.
- F10 (README 116–118 over-strong given the deviation path): rejected — the README states default conduct and already frames these as promises (line 279); a user-accepted deviation path does not contradict the default.
- F11 (implement:111–113 parenthetical reads as modifying the wrong clause): rejected — placement is forced by the M148 pinned-slice constraint; meaning stays recoverable via the pointer's fixed wording.
- F12 (chip ≤4-option cap could be reached when accept-shortfall and degraded review coincide): rejected — speculative composition; the contextual-chip rule already governs option construction per session.
- F13 (line-wrap widths and wrapped fragments): rejected — style-only, per the out-of-scope taxonomy.
- Gate triage (user, 2026-08-30): fix F2/F4/F5, reject the other 10 as proposed. Applied on the branch: D-127 appended (records the clause and the two fresh-context absolutes clause (c) narrows); both trigger subjects pinned in the prose guard with two new mutation-registry entries; the bullet's closing sentence names it tracking-rules' freshness-spawns clause, so the pointer token greps. Suites re-run green (scripts 326, hooks 121, skills 532 hand-run); validate green.
