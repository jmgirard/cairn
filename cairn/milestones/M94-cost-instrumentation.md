<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M94: Cost instrumentation — measure what a milestone spends before governing it

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m94-cost-instrumentation`   <!-- owner: implement (branch) / review (PR URL) · create -->

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

- [ ] AC1: A script reports, per session and per phase (`plan` / `implement` /
      `review`), the four token classes and the assistant-turn count, keyed to
      milestone IDs where the transcript names one. Correctness is evidenced
      against one session hand-checked line-by-line, not against its own output.
- [ ] AC2: The report **separates `cache_read_input_tokens` from
      `input_tokens`** and never sums them into one "input" figure. Measured
      2026-07-19 over the last 12 sessions: 501,114,833 cache-read vs 32,576
      fresh (98.70% vs 0.01%) — a collapsed figure would misattribute the cost
      by four orders of magnitude. A guard asserts the two stay distinct.
- [ ] AC3: A dated synthesis note under `cairn/references/` records the
      extraction method, the store's schema, the known limits of phase
      attribution, and a baseline table over the most recent milestones, with
      an extraction status per the M85 template shape and its `INDEX.md` line.
- [ ] AC4: `/milestone`'s audit output gains one always-read cost line
      (mass + turns/tokens for the most recent milestone). No threshold, no
      verdict, no new tracking file — a reporting surface only.
- [ ] AC5: Guards cover the phase attributor and the cache/fresh split,
      asserting against the classifier rather than the rendered report (M93),
      each paired with a positive signal that the path ran (M84), and the guard
      file carries its mutation registration (M53).
- [ ] AC6: The active profile's `verify` slot is clean — all three suites
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
- [ ] T4: Write the dated synthesis note (method, schema, limits, baseline) and
      its INDEX entry.
- [ ] T5: Write the guards (attributor + cache/fresh split), register in the
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
