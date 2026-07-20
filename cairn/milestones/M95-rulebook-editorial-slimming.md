<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M95: Rulebook editorial slimming — the rulebook states rules, not their legislative history

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, IP4   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** `m95-rulebook-editorial-slimming`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Run the editorial pass on `skills/shared/tracking-rules.md` under the corrected
premise: the rulebook is **current knowledge**, so justification recording no
decision is deletable against git with no backfill. Record that license as a
D-entry, state the inversion test the pass turns on where the rulebook's readers
meet it, and leave M96 its first stamp.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** The D-entry annotating D-045 that licenses the pass (RR03 rec 1);
placing the behavioral inversion test and the reddening asymmetry into the
rulebook's "What gets a test" (M98 F4 — neither phrase exists in
`skills/shared/` today); a section-by-section pass applying RR03 §1's three
removal grounds, with the B1–B21 ledger re-located against the current file as
input; completing RR01 rec 7's prune; re-anchoring every guard the rewording
touches and recording what that cost.

**Out:**
- **Any file but `skills/shared/tracking-rules.md`, its guard files, and
  `cairn/DECISIONS.md`.** `skills/cairn-init/SKILL.md` keeps its default-branch
  recipe — deliberate and guard-locked (`test_default_branch_parameterized.py:68`,
  naming M59 as RR01 rec 7's own implementation). Scoped in at the 2026-07-19
  implement gate and withdrawn unacted; named so the pass does not re-propose it.
- **"Author the missing D-entries, then slim"** — rejected, RR03 rec 9: it buys
  ~3-line deletions with ~1,900 chars of permanent history each, and
  misclassifies operative doctrine as displaced rationale. Only a genuine
  unrecorded cross-cutting *choice* earns an entry beyond rec 1's.
- Removing, weakening, or merging any rule. Zero rules leave the rulebook;
  a slimming that loses a rule is a failed milestone, not a cheaper one.
- Splitting or sectioning the rulebook → rejected, RR01 rec 15, upheld by both
  RR02 Q5 and RR03 Q5; not revisitable here.
- A size threshold or cap on the result, the growth stamp, and the one-sentence
  inflow test → M96.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: Every removal names **exactly one** of three grounds, per block in
      the work log: **(a)** it restates an existing decision record, quoted from
      that record before removal; **(b)** it fails the behavioral inversion test
      and records no decision — deleted against git, no backfill; **(c)** it is
      redundant with directives the skills carry, named. A block matching none stays.
- [ ] AC2: **No rule is lost.** Every rule surviving as a shortened statement
      keeps a guard that reddens when the rule is deleted or inverted, proven
      by inversion — relabel, negate, or transpose the rule in place, run the
      suite, require red, restore and diff (M74). A rule whose guard cannot be
      made to redden is restored to full statement rather than left unpinned.
      Guard-pinning is a **deletion screen only, never keep-verbatim** (RR03
      §2): a pinned block failing the behavioral test is shortened *with*
      re-anchoring, not skipped.
- [ ] AC3: The license is recorded and stated where its consumers read it — one
      D-entry annotating D-045 and citing D-052, carrying the three-step
      placement procedure and the behavioral-inversion doctrine; and both the
      inversion test and the reddening asymmetry stated in "What gets a test"
      and guard-pinned. IP4's wording is untouched.
- [ ] AC4: The mutation harness is green with every reworded anchor
      re-registered: a `block` that reflowed, duplicated, or lost trailing
      punctuation self-reports as "found 0" — the fix is the WRAP, never the
      assert (M65/M78). Registration is per file, so a guard file whose anchors
      all changed still needs its entries checked, not assumed (M53). The
      re-anchoring cost is recorded, making the RR03 rec 8 row judgeable.
- [ ] AC5: RR01 rec 7's prune is completed: the per-skill phase-header
      enumeration is replaced by the two-level convention plus the skills' own
      directives, and the default-branch recipe is stated once *within the
      rulebook*.
- [ ] AC6: The resulting line and character count is **recorded as evidence,
      never as a gate** — no line target is a pass condition (RR03's ~60–100
      lines is an expectation, not a bar). The before/after section breakdown is
      recorded for M96's first stamp, in `cs.char_count` characters, not bytes.
- [ ] AC7: The active profile's `verify` slot is clean — all three suites
      green, run from the repo root with exit codes checked individually and
      never behind a pipe (M56).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T3, T4
- AC2 → T4, T5
- AC3 → T1, T2
- AC4 → T5
- AC5 → T6
- AC6 → T7
- AC7 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Author the D-entry annotating D-045 and citing D-052: the rulebook is
      current knowledge; the three-step placement procedure; the behavioral
      inversion doctrine. Lands **before** any rulebook edit — it is the pass's
      license, not its write-up.
- [x] T2: State the inversion test and the reddening asymmetry in "What gets a
      test"; guard both; register in the mutation harness.
- [ ] T3: Re-locate the B1–B21 ledger against the current file and re-classify
      each block under AC1's three grounds. Its line numbers are stale (765 →
      788 lines) and cairn wraps at ~66 chars, so plain `grep` misses a wrapped
      phrase — B10 and B12 return zero hits while present. No edits here.
- [ ] T4: Edit section by section, heaviest first (Weight caps → References
      pages → Output discipline → Universal rules → Git model). **Targeted
      `Edit` calls only — never an ad-hoc string script over a tracking file
      (M61), never `replace_all` where indentation or context differs between
      occurrences (M90).** Cut content, don't rephrase: only removing a whole
      *wrapped* line lowers the count (M51/M87). Run the skills suite per section.
- [ ] T5: Re-anchor and re-register guards; run the mutation harness; prove
      AC2's inversion for each shortened rule; record the re-anchoring cost.
- [ ] T6: Complete RR01 rec 7's prune.
- [ ] T7: Record before/after counts and the section breakdown; run all three
      suites from the repo root with exit codes checked.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN. -->

- 2026-07-19: created by /milestone-plan, re-cutting M94 per RR02 rec 1. Absorbs the "Rulebook read-cost reduction" candidate row (graduates at completion, M35). RR02 Q1 verified the growth mode: no new domain doctrine entered after M58, yet the file grew 44% — the inflow is rationale, not rules.
- 2026-07-19: in-progress; branch `m95-rulebook-editorial-slimming`. Implement gate: residue form is a BARE parenthetical D-cite, not cite-plus-clause — settled by RR02 rec 1 ("the rule plus a parenthetical D-cite") and §5's "state the rule; cite the D-entry; delete the defense"; the Goal already said so, so the question was not open and should not have been asked.
- 2026-07-19: implement gate: how-to-apply clauses are arbitrated by AC2's guard-inversion test, not by judgment. Three of RR02 §1(c)'s five named cut targets at `:187-199` are guard-pinned and mutation-registered (test_lessons_loop.py:165-218; mutation entries :338/:359/:375), so cutting them would lose rules against Scope Out. RR02's "13 lines where the rule is ~5" counted guard-pinned rule text as defense; its own "estimates, not commitments" and AC5 (counts are evidence, not a gate) govern. ~550-600 lines is expected to be missed and is not a failure condition.
- 2026-07-19: SCOPE AMENDED at the implement gate (user-selected): the RR01 rec 7 prune extends to `skills/cairn-init/SKILL.md:35-44`, whose full restatement of the default-branch recipe is what makes "stated once" false. Rulebook keeps the canonical recipe; cairn-init becomes a pointer. Only file outside tracking-rules.md this milestone edits.
- 2026-07-19: T1 done — baseline measured 765 lines / 52,316 chars via `cs.char_count` (characters, not bytes; RR02's 52,797 was `wc -c`, a units mismatch M96's stamp must not inherit). Section breakdown recorded for AC5/M96: File map 72, Weight caps 81, Universal 72, Milestone IDs 32, Sizing 51, Git model 77, Context hygiene 25, Question gates 39, Output discipline 98, Model strategy 57, Toolchain profiles 35, Validation doctrine 11, References 67, What gets a test 40, preamble 8.
- 2026-07-19: T2 done — 21-block ledger verified against DECISIONS.md by an [S] subagent, load-bearing findings re-verified by hand. Headline: the milestone's premise is refuted on the sample. Only ~8 blocks are both D-homed and guard-free; ~9 have NO D-entry home (AC1 forbids removal) and ~14 are guard-pinned (Scope Out forbids removal).
- 2026-07-19: LEDGER B1 :91-94 LESSONS "49 lines / 13% mass / nothing reported it" — NO-HOME. Verified by hand: D-049 Context states the CONTRARY fact ("held 36 lessons from M41 through M83 and 29 since, never approaching 50") and D-051's "49 lines" is a different fact (both axes maxed and both reporting). RR02 §1(c) cited this as its flagship D-049 restatement; RR02 is wrong. NOT REMOVED.
- 2026-07-19: LEDGER B2 :96-104 threshold derivation — CONFIRMED D-049 ("non-item mass + capacity × the measured mean item length, rounded up to the next 500"). Removable: the M87 parenthetical + derivation narrative. KEEP: "measure that mean, never assume one" (operative; D-049 states it too but it governs application).
- 2026-07-19: LEDGER B3 :106-109 "density warns because an item count is a structural fact but 'too dense' is a judgment" — NO-HOME. D-049 Consequences carries the WARN-not-FAIL severity but no entry carries this reasoning. NOT REMOVED.
- 2026-07-19: LEDGER B4 :110-118 — SPLIT. Incident (3,152/2,568) CONFIRMED D-052 Context → removable. Exemption reason GUARD-PINNED `test_hygiene_stamp.py:69` (the M84 "reward splitting an item" sentence) → kept; D-052 itself says that rationale is "kept, not overturned".
- 2026-07-19: LEDGER B5 :121-127 cap exemptions — CONFIRMED D-030/D-046 but GUARD-PINNED heavily (`test_milestone_cap_exemption.py:36,61,69`, three sentences verbatim). NOT REMOVED — removal reddens guards, i.e. these are rules.
- 2026-07-19: LEDGER B6 :128-133 "a wrap is untidiness, not damage" — CONFIRMED D-046 ("once the section costs no budget a wrap is untidiness, not damage"), because-clause unpinned. REMOVABLE.
- 2026-07-19: LEDGER B7 :154-160 hygiene-stamp IP4 defense — PARTIAL/CONFIRMED D-052 ("not an IP4 history edit — `git log` holds every earlier stamp verbatim"). The trailing "same boundary terminal-row retention already runs on" has no home; label + "current knowledge" sentence GUARD-PINNED `test_hygiene_stamp.py:42,53`. Partially removable.
- 2026-07-19: LEDGER B8 :170-186 correcting-a-record — PARTIAL. ROADMAP re-derivation CONFIRMED D-052(2). But the IP/GP-exception sentence has NO home and is GUARD-PINNED `test_lessons_loop.py:116`, and the "Ruled out" sentence is pinned at :121. Only the re-derivation is removable.
- 2026-07-19: LEDGER B9 :187-199 lesson retirement — CONFIRMED D-051 but GUARD-PINNED across `test_lessons_loop.py:163-218`, one assert per clause, three mutation-registered. NOT REMOVED. RR02 §1(c)'s "13 lines where the rule is ~5" counted guard-pinned rule text as defense.
- 2026-07-19: LEDGER B10 :216-221 release timing — CONFIRMED D-050. The "extends the same authority upstream" argumentation is unpinned and removable; the rule + `blocked` parking are GUARD-PINNED `test_release_timing.py:47-72`.
- 2026-07-19: LEDGER B11 :323-337 default-branch recipe — no D-entry exists for the recipe at all. GUARD-PINNED in TWO files: rulebook at `test_default_branch_parameterized.py:94`, and cairn-init at :68, whose comment reads "M59 (RR01 rec 7): §0 carries the rulebook's ls-remote rung and the no-guessing rule". The cairn-init duplication is DELIBERATE and rec-7-sanctioned.
- 2026-07-19: LEDGER B12 :340-344 "ahead N, behind 1" failure mode — NO-HOME (searched "ahead N, behind 1", "local-only default branch"). NOT REMOVED.
- 2026-07-19: LEDGER B13 :372-382 enforcement boundary — CONFIRMED D-043 (ledger's presumed home was unknown; D-043 is the actual home) but GUARD-PINNED heavily `test_collaboration_boundary.py:41-66`. NOT REMOVED — it states enforcement scope, which is rule not defense.
- 2026-07-19: LEDGER B14 :468-472 phase-header D-020 narrative — CONFIRMED D-020, parenthetical unpinned. REMOVABLE.
- 2026-07-19: LEDGER B15 :473-479 per-skill phase-header enumeration — NO D-ENTRY (it is a mapping list, never a recorded decision). Removal rests on REDUNDANCY (all 9 skills carry their own `Phase header:` directive; rulebook guard pins only the milestone mapping), not on D-entry evidence — so AC1 as written forbids the milestone's cleanest win. AC1 gap.
- 2026-07-19: LEDGER B16 :714-724 re-verification — no dedicated D-entry (D-051's "divergence vector M56 rejected" is a different subject: a graduated-lessons file, not a references ledger). GUARD-PINNED `test_references_pages.py:676-724`. NOT REMOVED.
- 2026-07-19: LEDGER B17 :686-697 standing facts vs dated observations — NO-HOME (zero hits for "standing fact"/"dated observation" in DECISIONS.md) AND GUARD-PINNED + mutation-registered (`test_source_note_template.py:81-119`, `test_mutation_harness.py:719-731`). Reclassified: operative doctrine with zero DECISIONS footprint, not a rationale candidate.
- 2026-07-19: LEDGER B18 :704-712 provenance justification — NO-HOME, unpinned. AC1 forbids removal despite it reading as pure justification. NOT REMOVED.
- 2026-07-19: LEDGER B19 :430-435 merge-chip rationale — NO-HOME for the rationale (D-003/D-019 do not carry "outward-facing and irreversible" or "weaker consent"); the opening label IS pinned `test_gate_wording.py:46`. NOT REMOVED.
- 2026-07-19: LEDGER B20 :451-456 review chip-less exception — CONFIRMED D-019 verbatim; one sentence pinned `test_gate_wording.py:99`. Narrative partially removable.
- 2026-07-19: LEDGER B21 :583-586 fan-out diff-blindness — NO-HOME ("M17" is not a D-entry; D-016 references M17 for an unrelated cost decision). GUARD-PINNED `test_review_fanout.py:88`. NOT REMOVED.
- 2026-07-19: STOPPED at the implement gate, status back to `planned` for a re-cut (user decision, /milestone-implement step 6 "the goal itself is wrong"). The Goal's premise — "the always-read core carries history `DECISIONS.md` already owns", and Scope Out's "the rationale is *already* there — RR02 Q1(c) verified it block by block" — is refuted by T2: 9 of 21 blocks have NO D-entry home and 14 are guard-pinned. For much of the targeted text the rulebook is the SOLE home, so "delete the restatement" has nothing to delete back to. Measured removable yield ~35-40 lines (~5%) vs RR02's projected 22-28%.
- 2026-07-19: the real remedy the ledger points at is the one this milestone's Scope Out forbids — author the missing D-entries, THEN slim. That is the re-cut's problem to shape, not an amendment to this one. Zero edits were made to `skills/shared/tracking-rules.md`; the branch carried tracking files only and was landed docs-only, then deleted.
- 2026-07-19: T1/T2 boxes are left ticked though status is `planned` — the work was genuinely done and the ledger is its committed output. The re-cut should treat the ledger as input and re-number tasks from scratch.
- 2026-07-19: blocked on RB03 — escalated to a Fable architectural audit of rationale accumulation across `tracking-rules.md`, `DECISIONS.md`, and `LESSONS.md` (tripwire: ip-touching — IP4, GP1). The re-cut waits on RR03 rather than proceeding on RR02's framing, which M95's own ledger falsified. New evidence carried into the brief: LESSONS.md sits at 20,484/20,500 chars with 31 items averaging 630 chars, having grown NET since M92 gave it a retirement outflow — the weight axis's prescribed remedy (consolidate in place) is the mechanism that drives the weight axis, which D-049 states outright without following through.
- 2026-07-19: RR03 ingested — unblocked to `planned` for a re-cut. RR03 answers all seven questions with hand-verified evidence (it re-derived every measurement and spot-checked ledger entries B9 and B17 against the guard files). Headline: M95's stop was correct given AC1, but AC1 itself was the defect — it conflated 'preserved somewhere' with 'recorded as a decision', and the rulebook is current knowledge, so justification is deletable against git with no backfill. Honest re-cut yield ~60-100 lines. RB03/RR03 archived; 12 recommendations triaged (8 apply, 2 consider, 4 reject — rec 9 rejects this milestone's own proposed remedy).
- 2026-07-20: RE-CUT by /milestone-plan per RR03 rec 3. Goal, Scope, AC and Tasks authored fresh; the B1–B21 ledger stays as input and tasks re-number from scratch (the old T1/T2 ticks go with them). AC1's single D-entry-home bar is replaced by RR03 §1's three removal grounds. Scope reversal at the plan gate (user-selected): writing to `DECISIONS.md` moves from Out to In — one entry annotating D-045, authored FIRST as the pass's license (rec 1). Inversion test + reddening asymmetry placed in "What gets a test" (user-selected; RR03 §2's first-named home, M98 F4 the owing finding).
- 2026-07-20: measured drift since the ledger was written — `tracking-rules.md` is now 788 lines / 54,584 chars, up from T1's 765 / 52,316 across M97–M99 (+23 lines, +2,268 chars in three milestones). Every ledger line number is stale, and re-location must be wrap-aware: cairn hard-wraps at ~66 chars, so B10 ("extends the same authority upstream") and B12 ("ahead N, behind 1") both return zero `grep` hits while sitting in the file. Recorded as T3's premise.
- 2026-07-20: plan-gate collision sweep — D-053 already amended GP1 at the RR03 ingest gate, so rec 6 is discharged and M95 inherits "recorded editorial passes bound the rulebook" as its criterion; M97 and M98 are `done`, so RR03's order has reached M95. RR03 rec 9's rejection of "author the missing D-entries, then slim" is carried into Scope Out so the pass cannot re-propose it. Plan-owned body 142/149 after compressing AC/Scope/Tasks (M87: compress what your phase owns) — headroom left deliberately for implement's `## Decisions` appends, which the cap counts.
- 2026-07-20: in-progress; branch `m95-rulebook-editorial-slimming` cut from a synced main. No implement question gate: the plan gate settled scope, the DECISIONS reversal, and the inversion-test placement in the same session, and nothing else is open that the ACs do not already arbitrate.
- 2026-07-20: T1 done — D-056 authored, the pass's license. Three parts: the rulebook is current knowledge under D-045 (plugin logic, a class both of D-045's lists omitted, fixed the way D-052(2) fixed ROADMAP.md); the three-step placement test (inversion → decision → default delete); guard-pinning as a deletion screen only, with the reddening asymmetry stated. IP4 untouched and explicitly confirmed. Both rejections carried in: "author the D-entries then slim" (RR03 rec 9) and any IP4 change. `decision heading quality` OK on the new heading.
- 2026-07-20: T2 done — both statements placed in "What gets a test", immediately before the guard obligation they qualify (order pinned positionally, since it carries the argument). New guard `skills/tests/test_rule_placement.py`, 20 tests, 4 classes; 5 blocks registered in the mutation harness, which is the inversion proof for each. Net +16 rulebook lines before the pass subtracts — recorded so AC6's before/after is honest about what M95 added as well as removed.
- 2026-07-20: T2 note — my first draft of the guard asserted three spans at guessed wrap points and failed on all three; the file's actual wrapping is authoritative and the asserts were rewritten against it. Also dropped a `[:34]` slice hack that would have pinned a truncated clause. This is M65/M78 from the other side: the harness catches a reflowed anchor, but nothing catches an anchor authored against text that was never read out.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

- 2026-07-19 (RR03 ingest): the rulebook is **current knowledge** under D-045, not history — plugin logic edited in place every milestone, guarded by tests, with git holding every prior state. This dissolves AC1's problem: class-4 justification is deletable against git with no D-entry backfill, by D-052's own hygiene-stamp reasoning. To be recorded as a D-entry annotating D-045 by the re-cut, which needs it as its license (RR03 rec 1).
- 2026-07-19 (RR03 ingest): "rationale" is four classes, not one — rules, application doctrine, decision records, free-floating justification. RR03 §1's three-step placement procedure (inversion test → decision test → default delete) replaces AC1's single D-entry-home bar. B17/B3/B12 are application doctrine and correctly owe no D-entry; B1/B18/B10's tail are justification, deletable with no backfill.
- 2026-07-19 (RR03 ingest): guard-pinned⇒rule is sound only as a deletion screen, never as keep-verbatim — the text owns the guard, not the reverse. The behavioral inversion test is the doctrine; guard-reddening is its proof procedure where a guard exists. M95 read pinned as frozen, which RR03 calls over-conservative and the route by which a rulebook's editability dies one guard at a time.
- 2026-07-19 (RR03 ingest): consolidation is a deferral by construction — mass conserved, item axis relaxed. D-049's weight threshold is a treadmill: re-derived at today's measured mean (631) it RISES to ~21,500, above the current 20,500. So re-measuring the LESSONS threshold after a consolidation pass would ratify accretion and is rejected (RR03 rec 12); D-049's derivation is sound for its actual purpose.
- 2026-07-19 (RR03 ingest): LESSONS' missing outflow is GRADUATION TO DOCTRINE — 18 of 31 items (12,232 of 19,560 item-chars, 63% of item mass) are matured guard-authoring craft failing both D-051 criteria forever by construction: no test fails on the mistake (they teach the judgment guards cannot make) and no tracking-file slot owns guard craft. Banked as a candidate row this turn (RR03 rec 4).
- 2026-07-19 (RR03 ingest): IP4 is the RIGHT constraint and is untouched — DECISIONS' accumulation is structural, but its cost is entirely a read cost and M97 bounds it without touching the principle. RR03 looked for the case against IP4 and found none: the supersession chains are what made RR01, RR02, M95's ledger, and RR03 itself possible. Archival-with-tombstone stays parked on its stated trigger (RR03 rec 11).
- 2026-07-20 (from M98 review, F4/82): RR03 rec 1's behavioral-inversion test — "a rule is what changes compliant behavior when deleted or inverted" — and the reddening asymmetry ("sufficient to block a careless deletion, never necessary to justify one, never sufficient to keep prose that fails the behavioral test") are M95's to place in the ALWAYS-READ rulebook. M98 drafted both into `guard-doctrine.md` and removed them at review: a conditionally-read guard-authoring module hides them from the editorial-slimming session that is their consumer. Neither phrase exists in `tracking-rules.md` today.
- 2026-07-19 (RR03 ingest): three fitted mechanisms under one shared frame, not one unified lifecycle (RR03 rec 10 rejects unification — the files' type signatures differ, and a model general enough for all three constrains none). The frame: every always-read file names an inflow test, an outflow or read-bound, and an attention signal. The rulebook had NONE of the three; per-file governance was never the defect.
- 2026-07-19 (RR03 ingest): REJECTED — "author the missing D-entries, then slim", the remedy this milestone's own work log proposed on 2026-07-19. It converts editable mass into permanent history mass at ~1,900 chars per entry to license ~3-line deletions, and misclassifies operative doctrine (B17) as displaced rationale (RR03 rec 9). Rec 1 makes it unnecessary.
- 2026-07-19 (RR03 ingest): milestone order set to M97 → M98 (new: lesson graduation) → M95′ (re-cut) → M96 (kept, editorial rule amended). M95 returns to `planned`, NOT `in-progress` as the brief protocol's default step 5 assumes: AC1 must be replaced through `/milestone-plan`, which an implement-side amendment cannot do.
- 2026-07-19 (RR03 ingest): GP1 is false as stated; RR03 rec 6 recommends AMENDING it (not retiring — the item caps and archive discipline it licenses are the parts that work) with exact wording supplied at RR03 §6. NOT actioned here — a principle change requires an explicit user decision recorded as a D-entry, surfaced at the ingest routing gate.

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as is the work log (D-046); evidence never scrambles plan-owned content. -->
