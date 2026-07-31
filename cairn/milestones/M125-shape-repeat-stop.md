# M125: Certification loops stop on a repeated defect shape

- **Status:** review
- **Priority:** normal
- **Depends on:** M124
- **Driving RR:** —
- **Principles touched:** IP4
- **Branch/PR:** m125-shape-repeat-stop · https://github.com/jmgirard/cairn/pull/125

## Goal

End a certification loop by rule when consecutive rounds return the same shape
of defect, converting the obligation to a class-closing structural remedy, so
termination never again requires maintainer override.

## Scope

**In:** a stop rule in `guard-doctrine.md` §8 — two consecutive rounds
returning the same defect shape end the rounds — with the two obligation
sentences amended to acknowledge the new class, the falsifier framing updated,
and the stop rule's own falsifier clause stated; a recorded-counts rule in §6
at verbatim-reproducible grade; a D-entry narrowly superseding D-085's
clause-(i) gloss; pins, harness registration, and §8 ledger regeneration with
the diff read. Absorbs the §8-stop-condition candidate row (M124 §8 round 7,
maintainer override). M125's own §8 certification runs under the stop rule it
ships, as M124's ran under M123's rebuild.

**Out:** applying the stop rule to the plan-time criteria audit → not planned;
the audit is already incremental and closed itself at four passes in M124;
revisit only if an audit loop fails to close on its own. Retiring §8 or
folding it into the review fan-out → standing rejection (RR09 recs 8–9, RR10;
D-085 part 4), untouched — the falsifier clauses stay the retirement path.
New verification apparatus of any kind → D-090 closes that door at this plan
gate; the falsifier-state-disclosure and audit-over-falsifiers rows park
behind it. The disclosing-clause row's window condition is arguably met by
AC2's edit paying its re-anchoring cost; it stays parked behind D-090 rather
than absorbed (gate decision 2026-07-30).

## Acceptance criteria

- [x] AC1 — `guard-doctrine.md` §8 contains a stop rule: when a finding that
      clears both lines repeats the defect shape of the previous round's
      reopening finding — shape identity being the judgment D-064's trigger (b)
      applies to review returns, applied here to certification rounds — the
      certification convenes no further round. That second same-shape finding
      forms its own finding class, whose one
      confirmation obligation is a structural remedy closing the shape's class
      rather than its instance, confirmed by operation (the suite, the harness,
      the sweeps); the stop, the shape, and the remedy are disclosed in
      work-log lines before `status -> review`. §8's two obligation sentences —
      "a finding that clears both lines is a reopening finding, carrying that
      class's obligation: a further fresh-context round" and "Each class
      carries exactly one confirmation obligation, and no class carries two" —
      are amended to acknowledge this class, so neither ships as a contradicted
      sentence.
- [x] AC2 — The stop rule states its interaction with §8's falsifier: a
      shape-stopped certification counts toward the falsifier window exactly
      as run — the rounds it convened and their findings count where found,
      and no round it declined to convene is imputed or estimated — and §8's
      framing sentence attributing the falsifier's counted quantity to "the
      two rules above" is updated to count the stop rule among the rules that
      act on the round count. The stop rule carries its own falsifier in
      clause (ii)'s form: if a structural remedy authored under the stop rule
      is later found — by the three-lens review or a subsequent milestone —
      not to have closed its shape's class, the stop rule returns that shape
      to round-opening. Tolerance: one occurrence.
- [x] AC3 — `guard-doctrine.md` §6 contains a rule that a count recorded in a
      milestone record — a work-log line, a docstring, a comment, or a
      D-entry — carries the procedure that produced it at verbatim-reproducible
      grade: the command as run, or the committed artifact it is read from,
      stated at the granularity that discriminates it from a disagreeing
      record. The rule names M124's measured case: three records disagreeing
      on one count, with the one discriminator — whether bullet paragraphs are
      re-wrapped — stated in none of them.
- [x] AC4 — `cairn/DECISIONS.md` gains one appended entry recording the stop
      rule and the count rule: it narrowly supersedes D-085's clause-(i) gloss
      ("anything the two reopening rules have not already disposed of"), which
      the stop rule makes incomplete, with everything else in D-085 standing;
      it records the stop rule as a third way a certification ends — beside
      the gate opening at zero unresolved and the falsifier clauses retiring
      rounds across the window — reusing D-064 trigger (b)'s shape judgment
      beyond review returns; and it records the promotion of the ROADMAP's
      §8-stop-condition candidate row at the user's 2026-07-30 decision as a
      logged deviation from that row's second-override promotion condition.
      No existing entry is edited (IP4).
- [x] AC5 — Every rule this milestone adds to or amends in `guard-doctrine.md`
      is pinned by an assert that fails when that rule is inverted in place;
      each such assert is registered in `skills/tests/test_mutation_harness.py`,
      and every block this milestone registers fails when blanked. An assert
      pins the AC4 entry's existence, so deleting that entry reds the suite.
      The §8 ledger `skills/tests/ledgers/guard-doctrine-8.txt` is regenerated
      from the edited section, its diff read sentence by sentence, and the
      reading recorded in the work log.
- [x] AC6 — `python3 -m unittest discover` over `skills/tests`,
      `scripts/tests`, and `hooks/tests` each exit 0, and `cairn_validate`
      exits 0.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T1, T4
- AC6 → T5

## Tasks

- [x] T1 — Author §8's stop rule: the new finding class and its one
      obligation; amend the two obligation sentences (`guard-doctrine.md:342-345`,
      `:347-348`) and re-read the licence rationale clause (`:344-345`) for
      coherence under the exception (audit pass 2, finding 1a); update the
      falsifier framing sentence (`:373-375`) and add the stop rule's own
      falsifier clause. Expect breakage in the falsifier-neighborhood pins
      M124 just re-anchored (`test_the_falsifier_counts_where_a_finding_was_found`,
      `..._non_vacuity_floor`, `..._both_tolerances`); 69 of §8's ~85 registry
      blocks carry literal newlines, so re-anchor from shipped bytes (M95).
      Regenerate `skills/tests/ledgers/guard-doctrine-8.txt`, read the diff
      sentence by sentence, record the reading (AC1, AC2, AC5).
- [x] T2 — Author §6's recorded-counts rule; phrase the M124 case so the
      third record (which stated no procedure at all) is not claimed to have
      stated one (audit pass 2, finding 3) (AC3).
- [x] T3 — Append the D-entry as **D-091** — D-090 is reserved on main by the
      door entry and invisible from this branch, so the naive next id would
      duplicate it (D-067's reserved-not-skipped precedent); supersede
      D-085's clause-(i) gloss narrowly; record the candidate-row promotion
      deviation; run `cairn_validate` and expect the M115 dangling-id
      unmasking batch (AC4).
- [x] T4 — Pin every added or amended rule by in-place inversion restored
      byte-identical; pin the D-entry's existence; register each block;
      blanking sweep green (AC5).
- [x] T5 — Full verify: three suites exit 0, `cairn_validate` exit 0;
      `/milestone-implement` step 8 fires §8 certification, which runs under
      the shipped stop rule (AC6).

## Work log

- 2026-07-30: created by /milestone-plan, from the maintainer's request to diagnose and durably fix certification/review thrash.
- 2026-07-30: absorbs the §8-stop-condition candidate row (added 2026-07-30 from M124 §8 round 7's maintainer override); promoted at the user's decision as a logged deviation from the row's second-override promotion condition (IP2: surfaced, not silently overridden).
- 2026-07-30: the absorbed row lives on M124's unmerged branch, not on main — it will land with M124's squash-merge and M124's post-merge hygiene pass removes it then, this line making the removal owed rather than discovered.
- 2026-07-30: criteria audit (fresh-context [O], authored none of the criteria) pass 1 returned 9 findings: 4 clear, all fixed — the obligation-sentence contradiction, the stale "two rules above" framing, "adds" widened to "adds to or amends", the unpinned D-entry; 2 judgment, both to the gate — D-085 supersede-vs-annotate, count-rule inclusion; 3 satisfiable-as-written confirmations.
- 2026-07-30: plan gate (4 questions): plan ahead of M124's review with `Depends on: M124`; close the verification-apparatus program at the door (D-090, appended with this commit); supersede D-085's clause-(i) gloss narrowly rather than annotate; include the count rule at verbatim-reproducible grade.
- 2026-07-30: criteria audit pass 2 over the revised AC1–AC5 (AC6 unchanged, deliberately not re-read): all five satisfiable as written; residual notes carried into task text (licence-rationale re-read, §6 third-record phrasing, re-anchoring expectation). Pass 2 also confirmed the D-090/D-091 reserved-id handling against D-067's precedent.
- 2026-07-30: AC2's stop-rule falsifier clause was authored AFTER pass 2, on pass 2's own finding 1(b) prescription (§8 states the cost of a narrowing and points it at a falsifier clause; clause (ii) is the form) — the audit loop closes at 2 passes rather than re-opening for it, M124's pass-4 precedent.
- 2026-07-30: plan gate chose a shape-repeat stop over a round-count cap, because D-083 measured the round count as the wrong quantity (satisfiable by construction by the rules it polices); falsified by a certification loop that repeats no shape yet still fails to converge on yield alone.
- 2026-07-30: plan gate chose closing the apparatus program at the door (D-090) over stop-rule-only, because the stop rule alone makes each apparatus milestone cheaper while the queue keeps growing — D-057's measured signature; falsified by a shipped-behavior defect class that a parked apparatus candidate would have prevented.
- 2026-07-30: plan gate chose narrowly superseding D-085's clause-(i) gloss over annotating beside it, following the precedent M124's branch set when it superseded D-083 part 3(a) for the same shape — a description made incomplete by a later addition (that entry is unmerged, so it is named here by description, per the M115 lesson); falsified by the rounds-vs-findings defense proving right — a later reader showing the gloss was never incomplete because the stop rule declines rounds, not findings.
- 2026-07-30: plan gate chose verbatim-grade count procedures over cutting the rule, because M123/M124's correction-of-correction churn fed rounds and the discriminator was procedure granularity; falsified by procedure text bloating records at a cost exceeding the adjudication rounds it prevents.
- 2026-07-30: implement gate (1 question): §8's growth recorded as deliberate rather than offset within the section (user decision, M123's precedent); measured 150 -> 177 lines, both by `awk '/^## 8\. /{f=1} /^## 9\. /{f=0} f' skills/shared/guard-doctrine.md | wc -l` (at main and at the T1 commit; no existing paragraph re-wrapped).
- 2026-07-30: T1 — stop rule, window-counting and own falsifier authored as two paragraphs between the reopening rule and the obligations paragraph; both obligation sentences amended, the licence clause gains the no-such-silence sentence, the framing sentence counts the stop rule among the rules acting on the round count; suites 812/332/103 OK, cairn_validate exit 0.
- 2026-07-30: T1 breakage differed from the plan's expectation: the three falsifier-neighborhood pins held; what broke was the framing pin, the sentence-A pin, the obligations proxy (renamed exactly-three -> exactly-four, M124's rename precedent), and clause (ii)'s bare tolerance anchor — false coverage against the stop rule's identical "Tolerance: one occurrence." phrase, so both tolerance asserts are now anchored on their own clause's words ("that class" vs "that shape").
- 2026-07-30: T1 ledger regenerated and its diff read sentence by sentence: 12 added/amended units, every one deliberately authored; 2 removals, both the pre-amendment forms of the two amended sentences; nothing unintended.
- 2026-07-30: T2 — §6 recorded-counts rule appended at section end; the M124 case phrased per audit pass 2 finding 3 — the two records that named a procedure omitted the discriminator, the third named no procedure at all; skills suite 812 OK.
- 2026-07-30: T3 — D-091 appended (previewed verbatim in chat): four parts — stop rule as a third certification ending, D-085's clause-(i) gloss narrowly superseded, the §6 count rule, the candidate-row promotion deviation; its own Context counts carry their procedures per the rule it records. `cairn_validate` all checks passed — the M115 dangling-id unmasking batch the plan expected did NOT fire (`dangling id tokens` OK); D-090 was already on main when the branch was cut, so the plan's reserved-id premise was moot and D-091 was simply the next id.
- 2026-07-30: T4 — 11 new asserts (10 in the §8 certification class incl. the D-091 existence pin, 1 three-assert §6 test in the module class); 14 new registry entries + 3 re-anchored; 16-case in-place inversion sweep all red with guard-doctrine.md and DECISIONS.md restored byte-identical (sha256 compared, script in session scratchpad); blanking sweep (`-k mutation_harness`) green; the reader-file docstring's "three per-class confirmation obligations" corrected to four and the M125 surface added to its inventory.
- 2026-07-30: §8 certification round 1 (fresh-context [O], authored nothing): 13 findings — 2 coverage, 9 claim-vs-file, 0 anchor-fidelity, 2 self-consistency — plus 2 out-of-mandate observations; the load-bearing one: the stop rule's trigger was CIRCULAR (required two consecutive reopening findings while reclassifying the second out of that class), in the doctrine and in AC1 itself.
- 2026-07-30: AMENDMENT (substantive, gated, user-approved): AC1's trigger re-worded to the well-founded form — a finding that clears both lines repeating the defect shape of the previous round's reopening finding ends the rounds — shown verbatim above the gate chip; doctrine, asserts and registry re-anchored to match; §8 ledger regenerated, diff read: exactly the four amended sentences.
- 2026-07-30: round 1 fixes — sentence B now amended in place ("— the shape-repeat finding included"); framing names "the stop rule" (unmarked second name removed); four test comments/docstrings corrected (three-vs-four counts, AC5-clause misattribution, the fifth locked surface disclosed); D-091 heading pin extended to the full heading plus two substance pins (part-2 gloss, part-4 deviation) with registry entries; D-092 appended (previewed verbatim) superseding four D-091 claims; 6-case inversion sweep red, restores byte-identical; suites 823/332/103 OK, `cairn_validate` exit 0, `cairn_budget` 135/149.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T1 line says "both obligation sentences amended"; at T1 only sentence A was amended, sentence B was byte-identical to main until round 1's fix (round 1 finding 3).
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T1-breakage line groups clause (ii)'s tolerance anchor under "what broke"; that anchor stayed GREEN under the duplicated phrase (false coverage), which is the different fact the line's own trailing clause states (round 1 finding 10).
- 2026-07-30: procedures for the T4 counts, owed by the §6 rule this milestone ships (round 1 observation): 11 asserts = test-name delta `633750b..b901f64` over `grep -h "def test_" skills/tests/test_fresh_context_readers.py skills/tests/test_lesson_graduation.py`; 14+3 registry entries = `git diff 633750b..b901f64 -- skills/tests/test_mutation_harness.py` Mutation-block adds/edits; suite figures from each suite's `Ran N tests` line at those commits.
- 2026-07-30: out-of-mandate, recorded: the regenerated §8 ledger carries its first duplicate unit ("Tolerance: one occurrence." twice, `sort | uniq -d`), the multiset shape M124's review F9 named as unmanifested — inert today (`test_section_matches_its_ledger` green), left with F9's log entry as its record.
- 2026-07-30: §8 certification round 2 (fresh-context [O], authored nothing): 5 reopening-eligible findings (3 coverage, 2 claim-vs-file), 2 fix-authored records, 0 anchor-fidelity; §8's edited text certified self-consistent — no circularity, no contradicted sentence, no unmarked synonym.
- 2026-07-30: STOP — the shipped stop rule fired on its first live run: round 2's findings repeat round 1's defect shapes (trigger (b) judgment), so no round 3 is convened. Shape 1: an AC clause shipped without a redding pin, one instance surfacing per round (r1 F2 -> r2 F1/F2/F3). Shape 2: a pre-existing description of an M125-changed rule left stale (r1 F6/F7 -> r2 F4). Shape 3: a D-091 claim contradicted by its cited artifact (r1 F4/F5/F11 -> r2 F5).
- 2026-07-30: REMEDY A (closes shape 1's class): complete clause-by-clause AC1-AC5 -> assert map authored in one pass — AC1 7 clauses, AC2 4, AC3 4, AC4 6, AC5 5; every clause maps to a redding assert or named operation evidence; gaps closed: §6 asserts re-scoped to a `section6()` slice (relocation now reds — the LESSONS scope-the-read rule), the §6 record-kind enumeration pinned, D-091's three-endings / trigger-(b) / obligation / count-rule sentences pinned (1 new test, 6 new registry entries); relocation probe + 5 inversions red, restores byte-identical.
- 2026-07-30: REMEDY B (closes shape 2's class): corpus sweep for descriptions of every M125-changed sentence — `grep -rn -i 'iff\b|sufficien|three per-class|three obligation|three sentences|shape-repeat|two rules above|three distinct classes' skills/ --include='*.py' --include='*.md'` excluding `__pycache__` and `ledgers/` — every hit checked against shipped doctrine; 3 stale fixed (module docstring's iff claim, the only-if comment, `test_clearing_both_lines_is_sufficient_to_reopen` renamed `..._reopens_absent_a_shape_repeat` with its registry reference), rest verified current.
- 2026-07-30: REMEDY C (closes shape 3's class): one-pass re-verification of D-091/D-092's factual claims against their cited artifacts (round 2's verified list + the rounds-5-7 tally re-read from `git show a5a7007:cairn/milestones/M124-section-consistency-ledger.md` lines 205-219); one false claim found, in both D-090 and D-091 — corrected by D-093, appended (previewed verbatim).
- 2026-07-30: CORRECTION, appended not edited (IP4) — the round-1-fixes line's "`cairn_budget` 135/149" omits the argument that produces it: `python3 scripts/cairn_budget.py cairn/milestones/M125-shape-repeat-stop.md` (round 2 finding 6, fix-authored class).
- 2026-07-30: §8 growth updated after round 1's re-wording: 179 lines at HEAD by the same `awk '/^## 8\. /{f=1} /^## 9\. /{f=0} f' skills/shared/guard-doctrine.md | wc -l` (150 at main, 177 at cf095cc) — still under the implement gate's record-as-deliberate decision.
- 2026-07-30: T5 — final verify: skills 824 / scripts 332 / hooks 103 each OK, `cairn_validate` exit 0, `cairn_budget` 135/149 on this file; certification ended by the stop rule at 2 rounds with all three remedies confirmed by operation (suite, harness blanking, inversion sweeps). Status -> review.
- 2026-07-30: CORRECTION, appended not edited (IP4) — the Remedy B line's recorded sweep command reproduces 0 hits as written (`grep -rn -i` treats `|` as literal); the sweep's hits reproduce with `-E` added (117 hits at HEAD by the same pipeline), so the recorded line is not the command as run — a violation of the §6 rule this milestone ships (review O4, scored 92).
- 2026-07-30: CORRECTION, appended not edited (IP4) — Remedy A's "6 new registry entries" is 5: `git diff ed1b89f..aa41c80 -- skills/tests/test_mutation_harness.py` shows 5 added `Mutation(` blocks; the sixth touch is the renamed `test=` reference inside an existing entry (review O5, scored 90).
- 2026-07-30: CORRECTION, appended not edited (IP4) — the T1 ledger-reading line's "2 removals, both the pre-amendment forms of the two amended sentences" misidentifies them: `git diff main..cf095cc` on the ledger shows the removals were sentence A and the falsifier framing sentence; sentence B was byte-identical to main at T1 (review O6, scored 82).

## Decisions

## Review
- 2026-07-30: M124's post-merge hygiene removed the absorbed §8-stop-condition candidate row from the ROADMAP — the removal this log recorded as owed.
- 2026-07-30: M124's review B5 measured shipped §8 at exactly 150 lines — zero headroom under the size M123 chose deliberately — so T1's additions must offset lines within §8 or record the growth as a deliberate choice the way M123's implement gate did; noted here so implement prices it, procedure: `awk` over the §8 span at M124's merge commit.
- 2026-07-30: review opened — branch pushed, draft PR #125; main unmoved since cut (`git log HEAD..origin/main` empty), tree clean.
- 2026-07-30: AC1 evidence — `git diff main..HEAD -- skills/shared/guard-doctrine.md` read: stop rule sits between the reopening rule and the obligations paragraph, trigger in the amended well-founded form (a finding clearing both lines repeating the previous round's reopening finding's shape), shape identity named as D-064 trigger (b)'s judgment, the shape-repeat class carries one obligation (structural remedy closing the class, confirmed by operation), disclosure-before-review stated; sentence A amended ("— unless it repeats the defect shape…"), sentence B amended ("— the shape-repeat finding included"); work log discloses STOP, the three shapes, and remedies A/B/C before the status->review line. Fresh inversions of the trigger and sentence B red, restored byte-identical (sha256).
- 2026-07-30: AC2 evidence — same diff read: the window-counting paragraph states a shape-stopped certification counts "exactly as run … no round it declined to convene is imputed or estimated"; the framing sentence now attributes the counted quantity to "the rules above — the two lines governing a round, and the stop rule"; the stop rule's own falsifier is in clause (ii)'s form (remedy later found not to have closed its class → shape returns to round-opening) with "Tolerance: one occurrence."; the gate-reachability paragraph discloses the second narrowing. Fresh inversions of the framing sentence and the falsifier clause red, restored byte-identical.
- 2026-07-30: AC3 evidence — §6's recorded-counts rule read in the diff: a count in a work-log line, docstring, comment, or D-entry "carries the procedure that produced it, at verbatim-reproducible grade" — the command as run or the committed artifact, at discriminating granularity; the M124 case is phrased per audit pass 2 finding 3 (three records disagreed, the bullet-re-wrap discriminator stated in none; the two that named a procedure left it out, the third named no procedure at all). Fresh inversion of the rule red (`test_restatement_section_states_the_recorded_counts_rule`), restored byte-identical.
- 2026-07-30: AC4 evidence — D-091 read in full: part 1 the stop rule as a third certification ending reusing D-064 trigger (b); part 2 the narrow supersede of D-085's clause-(i) gloss with everything else standing; part 3 the count rule; part 4 the candidate-row promotion logged as a deviation from its second-override condition. `git diff main..HEAD -- cairn/DECISIONS.md` is append-only: 0 removed lines, 112 added (`grep -c '^-[^-]'` / `'^+[^+]'` over the diff) — no existing entry edited (IP4); D-092/D-093 corrections appended, never edits.
- 2026-07-30: AC5 evidence — fresh 6-case inversion spot-sweep (script in review-session scratchpad): stop-rule trigger, sentence B, framing sentence, stop-rule falsifier, §6 count rule each inverted in place, and D-091's heading blanked — all six red, both files restored byte-identical (sha256 compared); mutation-harness blanking sweep 9 tests OK and section-ledger suite 34 OK (`test_section_matches_its_ledger` green — the committed ledger matches shipped §8) via `python3 -m unittest discover -s skills/tests -p <file>`; the ledger diff readings are the T1 and round-1 work-log lines; implement's 16-case and 6-case sweeps stand logged.
- 2026-07-30: AC6 evidence — fresh this session: skills 824 OK, scripts 332 OK, hooks 103 OK (`python3 -m unittest discover` per suite), `cairn_validate` exit 0 all checks passed.
- 2026-07-30: consistency gate — `cairn_validate` exit 0 (16 PASS, 8 advisories OK); no DESIGN.md change on the branch so `cairn_impact` skips; generic profile's consistency-gate slot names no toolchain checks (clean no-op). Driving RR "—" → projection-vs-outcome no-ops.
- 2026-07-30: fresh-context fan-out — [O] diff-bug 12 findings; [S] blame-history 2 (no reversions of M123/M124 intent); [S] prior-review 0 regressions (probe found no real PR threads; six past defect classes checked clean, M124's owed row-removal confirmed closed); [S] scorer: 4 findings >= 80, 10 below.
- 2026-07-30: triage of the 4 actioned — O4 (92, Remedy B sweep command irreproducible as recorded) and O5 (90, "6 new registry entries" is 5) and O6 (82, T1 ledger-removal referent wrong): each fixed now by an appended work-log correction, independently reproduced by review before recording. O1 (80, mixed-round precedence gap — stop rule's "convenes no further round" vs sentence A's obligation for a co-occurring novel finding, no stated precedence): follow-up candidate row added to ROADMAP — review-side patching declined because the precedence choice (shape-thread-scoped vs certification-wide stop) is a design decision that would amend AC1's absolute wording, milestone-plan material per the never-reinterpret rule; swept first, no existing row/entry covers it.
- 2026-07-30: 10 sub-threshold findings logged, not actioned — B1 (75) stop-rule falsifier's window scope ambiguous (windowed vs perpetual unstated); O2 (72) definite-singular trigger presumes one reopening finding per round, live run used an unstated any-of reading; O7 (62) AC2's "counted quantity" wording inverts what the framing sentence attributes; O10 (60) AC4's "one appended entry" vs three appended (D-092/D-093 are IP4 corrections); O3 (55) amended clause-(i) gloss vs counts-as-run tension — the plan's own named falsified-by defense, knowingly accepted; O12 (55) AC5 evidence line omits Remedy A's relocation-probe sweep (disclosed at its own line); B2 (45) / O9 (40) duplicate ledger unit — M124 F9's multiset shape, disclosed and deliberately left logged; O11 (35) §8 headline looser than its em-dash gloss (house style); O8 (20) one 87-char line from the deliberate no-rewrap splice.
- 2026-07-30: note for the next §8 milestone: B1 and O2 sit in the same neighborhood as O1's row — whoever takes that row up should read all three together (window scope, multi-finding trigger, mixed-round precedence).
