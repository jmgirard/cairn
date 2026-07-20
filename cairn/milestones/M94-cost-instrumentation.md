<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M94: Cost instrumentation — measure what a milestone spends before governing it

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m94-cost-instrumentation` · https://github.com/jmgirard/cairn/pull/93   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Measure what a milestone actually costs — cache-read tokens, fresh input, and
turn counts by phase — so the next weight mechanism is aimed at a term that was
measured rather than assumed.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A mechanical extractor over the Claude Code session JSONL store
(`~/.claude/projects/<slug>/*.jsonl`; 114 files present 2026-07-19) reporting
per-phase cache-read / cache-creation / fresh-input / output tokens and
assistant-turn counts, attributed to milestone IDs; a dated synthesis note
recording method and baseline; an always-read cost line in the `/milestone`
audit.

**Out:**
- Any threshold, cap, or gate on the numbers produced → M96 (the ratchet)
  consumes this milestone's output; this one reports and never judges.
- Rulebook slimming → M95. Bounded `DECISIONS.md` read → M97.
- Per-file attribution of context growth. A shared prompt cache cannot
  cleanly apportion cache reads between files; attempting it would produce a
  number with no oracle, the failure this re-cut exists to avoid. Revisit only
  if the phase-level split proves too coarse to act on.
- Verify-suite subprocess cost → candidate row, unchanged.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1: A script reports, per session and per phase (`plan` / `implement` /
      `review`), the four token classes and the assistant-turn count, keyed to
      milestone IDs where the transcript names one. Correctness is evidenced
      against one session hand-checked line-by-line, not against its own output.
- [x] AC2: The report **separates `cache_read_input_tokens` from
      `input_tokens`** and never sums them into one "input" figure. Measured
      2026-07-19 over the last 12 sessions: 501,114,833 cache-read vs 32,576
      fresh (98.70% vs 0.01%) — a collapsed figure would misattribute the cost
      by four orders of magnitude. A guard asserts the two stay distinct.
- [x] AC3: A dated synthesis note under `cairn/references/` records the
      extraction method, the store's schema, the known limits of phase
      attribution, and a baseline table over the most recent milestones, with
      an extraction status per the M85 template shape and its `INDEX.md` line.
- [x] AC4: `/milestone`'s audit output gains one always-read cost line
      (mass + turns/tokens for the most recent milestone). No threshold, no
      verdict, no new tracking file — a reporting surface only.
- [x] AC5: Guards cover the phase attributor and the cache/fresh split,
      asserting against the classifier rather than the rendered report (M93),
      each paired with a positive signal that the path ran (M84), and the guard
      file carries its mutation registration (M53).
- [x] AC6: The active profile's `verify` slot is clean — all three suites
      green, run from the repo root with exit codes checked individually and
      never behind a pipe (M56).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T2
- AC3 → T4
- AC4 → T3
- AC5 → T5
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Map the JSONL schema and write the phase attributor — how a record
      is assigned to `plan`/`implement`/`review` and to a milestone ID, and
      what is unattributable. Record the unattributable share; a method that
      hides it is not acceptable.
- [x] T2: Write the token/turn extractor over the four classes. Hand-check one
      session line-by-line as AC1's evidence.
- [x] T3: Add the `/milestone` audit line.
- [x] T4: Write the dated synthesis note (method, schema, limits, baseline) and
      its INDEX entry.
- [x] T5: Write the guards (attributor + cache/fresh split), register in the
      mutation harness, run all three suites from the repo root.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-19: created by /milestone-plan. Scope from a measured slowdown investigation — plan→review wall clock rose from a ~23 min median (M63–M68) to ~39 min (M88–M93); the three verify suites contribute ~10% (37s × ~6 runs) while `tracking-rules.md` grew +56% and `DECISIONS.md` +103% over the same 30 milestones, both ungoverned by any cap.
- 2026-07-19: start — branch cut (`m94-always-read-weight`), status in-progress.
- 2026-07-19: implement gate — user rejected the ratchet basis as incoherent with the milestone's own premise (a threshold above current size blesses the state the investigation flagged). Hard-fail at a firing threshold deadlocks verify (AC6 unreachable until the deferred slimming lands), so an AC3 amendment to advisory-at-the-M63-baseline was drafted and is HELD, not applied.
- 2026-07-19: escalating to /milestone-brief on a no-oracle tripwire at user request. Evidence: 9 weight-management milestones (M32, M55, M69, M77, M84, M87, M92, M93, M94), 5 of them 2026-07-18/19, with M87 existing only to re-derive M84's thresholds — wrong on both files 3 days after shipping. Two gate rounds here produced no defensible threshold basis. Question is architectural, not the number.
- 2026-07-19: blocked on RB02. Collision found while drafting: RR01 §5 already ruled on rulebook size at 545 lines — rejected per-skill splitting (rec 15), prescribed ONE extraction (rec 9, executed by M58/D-031) plus a norm. Net effect 545→532 lines, erased within 3 days; today 765 (+44% over the state that triggered RR01, vs its projected ~460 core). RB02 therefore asks why the prescription failed to govern, not whether to split.
- 2026-07-19: deviation logged — RB02 and this status change committed on the milestone branch, not main as /milestone-brief step 2 prescribes. Reason: M94's ROADMAP row and header mirror live on the branch at in-progress, so a docs-only main commit would diverge the mirror it is meant to sync. Tracking-travels-with-code kept them in one commit.
- 2026-07-19: RR02 ingested. Load-bearing claims re-verified against the implementation before ingestion (M75): Weight-caps section 21→80 lines (+59, vs the rec 9 extraction's −53); LESSONS.md 20,494 chars vs the 20,500 threshold; 52 `### D-` headings totalling 5,378 chars (5.6% of the file); D-049 present as cited. RR02's section table counts one line higher per section (heading-boundary convention); every delta matches.
- 2026-07-19: CORRECTION to this log's 2026-07-19 creation entry — that entry books the ~23→~39 min slowdown against re-read growth. RR02 Q6 finds the causal claim unsupported: the slow window is dominated by weight-management meta-milestones carrying extra gate rounds (M94 itself burned two), and the only causally isolated figure is the suites' ~10%, which exonerates them. The growth is a real GP1 defect on its own merits; the latency attribution is withdrawn pending token instrumentation.
- 2026-07-19: returned to planned for a re-cut (user gate). Branch `m94-always-read-weight` carried docs only and landed on main under the docs-only carve-out; branch deleted. Criteria below are superseded per the Decisions section and are the re-cut's input, not a live plan.
- 2026-07-19: re-cut start — branch `m94-cost-instrumentation`, status in-progress. Implement gate: milestone-ID attribution is branch-derived only (main-side plan work reported at phase level with its unattributable share stated); subagent turns leave no store record at all, so each phase reports its spawn count beside the token figures to label the gap. Both user-accepted.
- 2026-07-19: T1 — `scripts/cairn_cost.py` maps the store schema and attributes by `attributionSkill` (phase) and `gitBranch` (milestone), both runtime-written, so neither is a heuristic. Measured unattributable share over 22,771 assistant records: 40.7% no milestone (33.9% of cache-read), 15.6% no phase.
- 2026-07-19: T2 — extractor + by-phase/by-milestone report. AC1 hand-check on session `1601be2a` (M93 implement): three independent methods (jq aggregate, per-record jq→awk sum, raw Python line loop) all return 162 turns / 24,213,467 cache-read / 185,894 cache-create / 301 fresh / 119,840 output / 0 agents, matching the module exactly. Corroboration: the `agents` column reads exactly 4 for every reviewed milestone — the M17 fan-out. Verify clean (441/209/72).
- 2026-07-19: T3 — `/milestone` §2 gains `cairn_cost.py --audit-line`, reported verbatim, with the no-threshold/no-verdict boundary stated in the skill prose and the governing mechanism deferred to M96. Verify clean.
- 2026-07-19: T4 — `cairn/references/session-cost-notes.md` + INDEX line: schema, attribution ledger A1–A6 (A3 plan-phase `refused`, A4 subagent tokens `absent`, A6 per-file share `refused`), ten-milestone baseline, and the cache-read-per-turn trend (166,451 → 184,351, +10.8% M63–M68 → M88–M93) against +56%/+103% file growth. Two existing guards caught real defects on first run — a wrapped `Extraction:` line and the pinned page-state ledger — both fixed, not worked around. Verify clean.
- 2026-07-19: T5 — `scripts/tests/test_cairn_cost.py` (18 behavioural guards on the classifier functions, not the rendered report) + `skills/tests/test_cost_audit_line.py` (6 prose guards, 3 blocks registered in the mutation harness and mutation-verified). The phase-map coverage guard caught a real gap on first run: `design-interview` was a shipped skill missing from `PHASES`, so its turns would have landed in `unattributed`. Verify clean: 447 / 227 / 72, `cairn_validate` exit 0.
- 2026-07-19: all tasks complete, status review. Branch diff: 10 files, +913/-8. Suites 447/227/72 green, `cairn_validate` exit 0.
- 2026-07-19: review FAILED AC1, returned to in-progress. AC1 requires the report be keyed "per session and per phase"; the shipped report emits BY PHASE and BY MILESTONE only — no per-session breakdown exists, though `read_records` already stamps `_session` on every record. Nothing else failed: AC2-AC6 evidence gathered clean, `cairn_validate` exit 0, suites 447/227/72. Not amended — the criterion is right and the work was short of it.
- 2026-07-19: merge gate — user directed F4 (78, sub-threshold) be fixed before merge. `--audit-line` honours `--milestone`; `--attribution` refuses it with exit 2 rather than reporting a share that filtering makes 0.0% by construction. Verify 447/236/72, cairn_validate exit 0.
- 2026-07-19: review — five findings scored >=80 fixed on the branch (F5 false-coverage guard, F8 unregistered mutation blocks, F3 filtered-attribution false zero, F6 note overclaim, F2 session count); three below threshold logged. All six criteria verified with fresh evidence. Verify 447/233/72, cairn_validate exit 0.
- 2026-07-19: AC1 gap closed — `session_of` + a `BY SESSION` report section keyed by session, milestone(s), and phase(s), so a session spanning implement and review names both rather than being labelled by its first. Four guards added (22 in the cost suite). Back to review. Verify clean: 449/231/72, `cairn_validate` exit 0.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->


Full reasoning and evidence: `cairn/reviews/archive/RR02-weight-management-architecture.md`
(answers by question number). Recorded here as findings, not restatements.

- 2026-07-19 (Q1/Q5): RR01 rec 9 failed **structurally** — a one-time extraction
  is a stock remedy for a flow problem (+7.6 lines/milestone, no outflow), and
  D-031's norm governs the wrong margin. Dominant inflow is **rationale, not
  rules**, against the rulebook's own `tracking-rules.md:11-13` boundary.
- 2026-07-19 (Q2): the family splits — outflow (M32, M92) and cap-boundary
  (M55, M69, M77) work is settled and right; the character-mass family
  (M84→M87→M93→M94) is the wrong mechanism class for prose files, because
  D-049's doctrine makes its thresholds nonstationary by design.
- 2026-07-19 (Q3): "threshold" is the wrong instrument at n=1. Replacement is a
  growth-since-last-editorial-pass ratchet. Supersedes AC2/AC3 and the held
  AC3 amendment.
- 2026-07-19 (Q4): `DECISIONS.md` mass is legitimate; the read is the defect.
  The 52 `### D-` headings are already a zero-divergence index. Carries an IP2
  recall trade requiring a user gate. Supersedes AC4.
- 2026-07-19 (Q5): RR01 rec 15 **upheld**; the size fix is evicting
  non-contract content, never reading the contract partially.
- 2026-07-19 (Q6): this milestone's own latency premise is **unsupported**
  (composition + sample confounds). Growth stays a GP1 defect on
  context-pressure and instruction-dilution grounds. Instrument before
  shipping further weight machinery.
- 2026-07-19 (triage): apply rec 1 (slimming), rec 2 (ratchet, replaces
  AC2/AC3), rec 3 (bounded read — user gate, annotates IP2), rec 4
  (instrument, sequenced FIRST); consider recs 5-6; recs 7-9 rejected by RR02
  with reasons.

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->

Reviewed 2026-07-19 · PR #93 · branch `m94-cost-instrumentation`.

### Evidence per criterion

- **AC1 — PASS (after a send-back).** First pass FAILED: the report emitted
  `BY PHASE` and `BY MILESTONE` only, with no per-session breakdown, though
  `read_records` already stamped `_session`. Returned to `in-progress`; the
  criterion was not reinterpreted. Fixed by `session_of` + a `BY SESSION`
  section keyed by session, milestone(s) and phase(s). Fresh evidence: session
  `1601be2a` rendered as `1601be2a  M93,—  implement,plan,review  368
  60,038,238  599,146  685  303,094  4`, matching an independent `jq -s`
  aggregate over the raw file digit-for-digit on all six figures; the
  implement-phase slice (162 / 24,213,467) additionally agrees with a
  per-record `jq`→`awk` sum and a raw Python line loop. Three methods, none
  the script's own output.
- **AC2 — PASS.** `TOKEN_CLASSES` is a 4-tuple of distinct keys; `tokens_of`,
  `aggregate`, `_row` and `audit_line` keep them apart on every path. Guarded
  by `TestCacheFreshSplit` (4 tests), including a bucket-level assertion that
  no accumulator carries a collapsed sum, and a report-level assertion that
  the two render as separate columns. Store-wide ratio 719:1.
- **AC3 — PASS.** `cairn/references/session-cost-notes.md` records the schema,
  the A1–A6 attribution ledger, the phase-attribution limits, and a
  ten-milestone baseline; `Extraction:` is one physical line carrying
  `— observed 2026-07-19`; `INDEX.md` line present. `cairn_validate`:
  `references index<->disk` PASS, `references staleness` OK.
- **AC4 — PASS.** `skills/milestone/SKILL.md` §2 runs
  `cairn_cost.py --audit-line` and reports it verbatim, with the
  no-threshold/no-verdict boundary stated and the governing mechanism deferred
  to M96. Live output: `cost: M94 — … turns · … cache-read · … fresh-in · …
  output · N subagents spawned (their tokens unrecorded)`. No new tracking file.
- **AC5 — PASS.** `scripts/tests/test_cairn_cost.py` — 26 guards asserting
  against the classifier functions (`phase_of`, `milestone_of`, `session_of`,
  `agents_spawned`, `tokens_of`, `aggregate`, `attribution`), each negative
  paired with a positive proving the path ran.
  `skills/tests/test_cost_audit_line.py` — 6 prose guards, **all 6** blocks
  registered in the mutation harness (3 at implement, 3 more at review per F8)
  and mutation-verified by `TestRegisteredGuardsFailWhenBlanked`.
- **AC6 — PASS.** Run from the repo root, exit codes checked individually, no
  pipe: `skills` 447 exit 0 · `scripts` 233 exit 0 · `hooks` 72 exit 0.

### Consistency gate

`cairn_validate.py` exit 0 — 22 checks PASS/OK, zero FAIL, zero WARN. Profile
is `generic`, whose `consistency-gate` slot names no toolchain checks, so that
half is a clean no-op. No `DESIGN.md` principle changed, so `cairn_impact` was
not run. This repo has no CI (PROFILE.md): `gh pr checks` reports none.

### Independent review — three lenses + scorer

[O] diff-bug: 7 findings. [S] blame-history: 0 findings (verified RR02
conformance — M94 implements rec 4 and defers recs 1/2/3 to M95/M96/M97).
[S] prior-PR-comments: 1 finding; no GitHub PR-thread evidence exists
(threads empty), so the archived `## Review` sections were the surface.

**Actioned (score ≥ 80), all fixed on the branch:**

- **F5 (91) — false coverage in the new per-session guard.** `assertIn("M94")`
  / `("implement")` / `("12,345")` ran against the whole report, where those
  strings also render in `BY MILESTONE` and `BY PHASE`; stripping the session
  row's labels entirely left the test green. Fixed by asserting against the
  session row itself. Re-verified by mutation: with labels stripped the guard
  now FAILS.
- **F8 (90) — the prose-guard docstring overclaimed its own coverage**,
  claiming every assertion was mutation-registered when 3 of 6 were. The
  identical overclaim was caught by M53's own review. Fixed by registering the
  three missing blocks rather than weakening the claim, so all 6 are now real.
- **F3 (88) — `--milestone` reported the unattributable share as 0.0%.**
  `attribution()` ran over the already-filtered list, making the share zero by
  construction — the method reporting its own blind spot as absent, which T1
  forbids outright. Fixed: the share is always computed store-wide and the
  line now says so. Regression test added.
- **F6 (85) — the note's Disposition overclaimed A6** as "surfaced in the
  report output"; A3 and A4 are, A6 is not. Split into two entries stating
  that A6 has no figure to caveat because the per-file share is never computed.
- **F2 (82) — `report()` counted sessions from the real store** while
  rendering a filtered table, so `--milestone M85` announced "115 sessions".
  Fixed to count the sessions actually rendered. Regression test added.

**Logged below threshold (surfaced, not actioned — IP3):**

- **F4 (78) — FIXED at user instruction at the merge gate** (2026-07-19),
  overriding the sub-threshold default. `--milestone` was accepted and then
  silently ignored in `--audit-line` and `--attribution`. The two modes needed
  opposite answers: `--audit-line` now honours it (and says so when the named
  milestone has no records), while `--attribution` **refuses** it with exit 2,
  because filtering a whole-store share is precisely the F3 category error.
  Three guards added.
- **F7 (60)** — `report()`'s docstring omitted the `BY SESSION` section.
  Corrected in passing while rewriting that docstring for F3.
- **F1 (55)** — the module docstring advertised a `--store` option that does
  not exist. Corrected in passing while editing that comment block.

F7 and F1 were stale-text lines inside comment blocks being rewritten for
actioned findings; leaving them knowingly wrong while editing the lines around
them was the worse option. F4 was left alone at first as a behaviour change,
then fixed on the user's instruction at the merge gate.

One defect was caught by the review's own new regression test rather than by a
reviewer: the first form of F3's guard asserted `"0.0% not keyed to a
milestone"`, which is a suffix of `"50.0% not keyed to a milestone"` and so was
vacuous. Re-anchored with a digit-boundary regex.
