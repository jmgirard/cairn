# M137: Derived figures are pinned or procedural, never free-standing

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP4
- **Branch/PR:** m137-derived-figures · https://github.com/jmgirard/cairn/pull/137

## Goal

A derived count or figure written into branch-added prose ships pinned —
beside the procedure that produced it and the commit or dated artifact it
was measured at — or replaced by its derivation; the free-standing
hand-written figure, the record-defect class the 2026-08-08 effort audit
(`references/effort-experiment-notes.md`) found dominant across M113–M136's
actioned review findings, stops being a legal write.

## Scope

**In:** the derived-figures rule in `skills/shared/tracking-rules.md`
"Universal tracking rules" beside the derived-claims rule, under a distinct
name, over that rule's domain; guard-doctrine §6's recorded-counts
paragraph trimmed to defer to it — the M124 story and its citation
retained, the universal-claim corollary's identification and fallback kept,
the §6 counts pointer (`guard-doctrine.md:231`) re-pointed; a D-entry
narrowly superseding D-091 part 3's placement clause; guards, harness
registrations and inversion probes for the added clauses; a full-diff
compliance sweep of the branch's own added figures.

**Out:** any checker or validator over figures — declined at the candidate
row (delete-over-govern; a validator reaches machine-derivable figures
only), revisit only via D-090's trigger. A retroactive sweep of
pre-existing free-standing figures in live tracking files — the
correcting-a-record rule owns each as it is next touched; no milestone.
False or unverified claims, as opposed to stale figures — owned by the
shipped derived-claims rule (M134) and failure-identity rule (M136).

## Acceptance criteria

- [x] AC1: The "Universal tracking rules" section of
      `skills/shared/tracking-rules.md` states the derived-figures rule,
      under a name distinct from the derived-claims rule's and governing
      that rule's domain (tracking records, code comments, docstrings,
      changelog entries, docs): a derived count or figure written there
      takes one of two forms — pinned, stating beside the figure the
      procedure that produced it and the commit or dated artifact it was
      measured at, or procedural, the figure replaced by its derivation
      with no figure stated — and the free-standing form is not written.
      Evidence: the shipped bytes, read out at review.
- [x] AC2: Guard-doctrine §6's recorded-counts paragraph defers to the
      tracking-rules derived-figures rule by cross-reference rather than
      stating a parallel weaker form, the M124 evidence story retained with
      its citation
      (`git show a5a7007:cairn/milestones/M124-section-consistency-ledger.md`)
      traveling beside it, and the §6 counts pointer
      (`guard-doctrine.md:231`) re-pointed to the derived-figures rule; the
      universal-claim corollary keeps its identification sentence and its
      unenumerable-domain fallback, deferring only its procedure-grade
      clause. A D-entry narrowly supersedes D-091 part 3's placement
      clause — the operative rule now lives in tracking-rules, widened to
      derived figures across the derived-claims domain and strengthened by
      the pin requirement — with D-091's decision otherwise standing.
      Evidence: the shipped bytes of both files and the appended D-entry.
- [x] AC3: Every rule clause this milestone adds to
      `skills/shared/tracking-rules.md` or
      `skills/shared/guard-doctrine.md` — candidate sites enumerated by
      `git diff main...HEAD -- skills/shared/tracking-rules.md skills/shared/guard-doctrine.md`,
      read added-line by added-line with each line's rule-clause-or-not
      classification recorded — is pinned by a guard registered in the
      mutation harness, and each such guard reddens under blanking and
      under three inversion-probe kinds (negation, relocation, dispersal),
      the probe commands and results recorded with the procedure that
      produced them.
- [x] AC4: Every derived figure the branch adds — candidate sites
      enumerated by `git diff main...HEAD`, read added-line by
      added-line — either complies with the rule AC1 states (pinned or
      procedural) or is classified as a site the rule does not govern, the
      per-hit classification recorded; a non-compliant figure in an
      append-only record is remedied by a superseding pinned restatement
      noted in the sweep, never by an edit. The sweep is recorded with its
      command.
- [x] AC5: The generic profile's verify clean — the three unittest suites
      (`skills/tests`, `scripts/tests`, `hooks/tests`) pass from the repo
      root, each exit code checked singly.

## Coverage

- AC1 → T1
- AC2 → T2, T3
- AC3 → T4
- AC4 → T5
- AC5 → T5

## Tasks

- [x] T1: Author the derived-figures rule in
      `skills/shared/tracking-rules.md` "Universal tracking rules",
      directly after the derived-claims bullet (`tracking-rules.md:228`):
      distinct name, the derived-claims domain phrase, the two legal forms
      and the free-standing defect named. Grep the repo for surfaces
      restating the recorded-counts rule (M112 lesson) and confirm no
      nearby guard's anchored phrase reflows (M104/M113 lessons).
- [x] T2: Trim guard-doctrine §6: the recorded-counts paragraph
      (`guard-doctrine.md:234`) defers by cross-reference with the M124
      story and citation retained; the universal-claim corollary
      (`guard-doctrine.md:243`) keeps its identification sentence and
      unenumerable-domain fallback, deferring only its procedure-grade
      clause; the `:231` counts pointer re-points to the derived-figures
      rule. Re-anchor the two existing pins
      (`skills/tests/test_lesson_graduation.py:249`,
      `skills/tests/test_mutation_harness.py:2541`).
- [x] T3: Append the D-entry narrowly superseding D-091 part 3's placement
      clause: rule relocated to tracking-rules, widened to derived figures
      over the derived-claims domain, strengthened by the pin requirement;
      D-091's decision otherwise stands.
- [x] T4: Guards + mutation-harness registrations for every added rule
      clause; run blanking and the three inversion-probe kinds (negation,
      relocation, dispersal — the M136 lesson's vocabulary,
      marker-locator scoping) and record AC3's sweep with its per-line
      clause classification.
- [x] T5: Run AC4's full-diff compliance sweep, classify each added-figure
      hit, fix or supersede per the rule; settle numeric records last
      (guard-doctrine §6); run the three suites singly and record AC5.

## Work log

- 2026-08-08: created by /milestone-plan from the 2026-08-08 candidate row (lineage: effort-audit classification, `references/effort-experiment-notes.md`); promoted under the condition-met reading — the row's condition ("next review whose defect return or ≥80 actioned finding is a stale free-standing figure") read as already satisfied by M134's D14/88 stale work-log count and M135's two record defects, both on the record in the row's own motivation (gate Q1; the logged-deviation reading was the rejected alternative); falsified by showing M134 D14/88 was not a stale free-standing figure.
- 2026-08-08: criteria audit ([O] fresh-context reader, two rounds). Round 1 returned 2 clear-fixes (the §6 corollary's identification and fallback sentences would be lost by a pure cross-reference — kept in §6; AC4 unsatisfiable under IP4 for append-only sites — supersede pathway added), 4 judgments (D-091 relation → gate Q2; rule domain → gate Q3; AC3's clause-hood classification recorded per line — applied; the M124 story's citation travels with it — applied) and a naming observation (distinct rule name — adopted into AC1). Round 2, on the gate-revised wording, returned 1 clear-fix (the `guard-doctrine.md:231` counts pointer becomes determinately wrong under the distinct name — re-point folded into AC2) and 1 judgment (the widened domain exceeded AC4's two-tree pathspec — sweep widened to the full diff; the recorded-exclusion alternative rejected as a gap with no offsetting saving).
- 2026-08-08: plan gate chose narrow supersession of D-091 part 3's placement clause over annotation-with-overlap because a relocation-plus-widening leaving two live statements is the drift class this milestone exists to kill, and D-091 part 2 is the precedent shape (gate Q2); falsified by a case §6's original scope governed that the widened rule does not.
- 2026-08-08: plan gate chose the derived-claims domain phrase over tracking-plus-milestone-records-only because one shared domain keeps the sibling rules coherent and leaves no orphaned D-091 scope (gate Q3); falsified by sweep-judgment cost on docs/comments hits exceeding the pin's value there.
- 2026-08-08: plan chose always-read placement (tracking-rules) over a records-hygiene module home because the rule binds every record write and a conditional read misses most of them (the M134 precedent); falsified by a measured cairn_cost regression attributable to the addition. The no-checker choice is the candidate row's own and was not re-weighed here.

- 2026-08-08: T1 — derived-figures rule authored in tracking-rules "Universal tracking rules" after the derived-claims bullet, pinnable sentences on single physical lines; restatement sweep (`grep -rn -i 'recorded-counts\|carries the procedure that produced' --include='*.md' skills/ README.md`, non-test hits) found only guard-doctrine §6's two paragraphs, T2's target; skills suite green after insertion.
- 2026-08-08: T2 — §6's recorded-counts paragraph re-cut as a deference headline + verbatim-reproducible grade clause + M124 story now carrying its `git show a5a7007` citation; the `:231` counts pointer and the corollary headline re-pointed; guard test re-anchored (3 asserts, one added for the citation) and 4 harness blocks re-registered to the new bytes; skills suite green (752, harness blank-checks included).
- 2026-08-08: T3 — D-099 appended (previewed in chat), narrowly superseding D-091 part 3's placement clause; validate green with no unmasked danglers at the raised id ceiling.
- 2026-08-08: T4 — test_derived_figures.py (5 tests, bullet-scoped via a unique-marker locator returning '' when missing) + 5 harness registrations; §6's two guard tests re-scoped from section6() to paragraph slices so dispersal within §6 reds (the M136 trap); AC3 sweep: `git diff main...HEAD -- skills/shared/tracking-rules.md skills/shared/guard-doctrine.md` adds 12 lines, of which 11 carry or wrap the 9 rule clauses and 1 is the re-pointed `:231` cross-reference connective (not a clause); inversion probes = 9 clauses × (negation, relocation-to-EOF, dispersal-to-another-bullet/paragraph) + 2 subject transpositions on the headlines, all RED as failures with zero errors, targets restored hash-verified (scratchpad probe script; mutations restated per clause for review's re-run); skills suite green (757).
- 2026-08-08: T5 — AC4 sweep: `git diff main...HEAD | grep '^+[^+]' | grep -nE '[0-9]'`, every hit read; hits are record ids, dates, and test code, plus derived figures that each stand beside their named procedure, committed artifact, or citation (suite counts beside the named suite runs, assert/registration counts beside the files the same commit ships, D-099's audit figures beside the cited effort-audit page, §6's three-records story beside its `git show a5a7007` citation); no free-standing figure, no supersession needed. Three suites green singly (757/345/103), validate all checks passed, budget 125/149. Status → review.
- 2026-08-08: correction (review F19, via the AC4 append-only pathway): the T2 line's "3 asserts, one added for the citation" went stale when later work rewrote the same test twice (T4's paragraph re-scoping, review's F12/F22 fixes); the shipped method carries 6 asserts, counted at the review working tree by `re.findall(r"self\.assert", <method slice>)` over `test_restatement_section_states_the_recorded_counts_rule`; the earlier figure is superseded, never edited.

## Decisions

## Review

Fresh evidence, 2026-08-08, branch head 8da036a (PR #137):

- AC1: `grep -n -A9 'A derived figure is pinned or procedural' skills/shared/tracking-rules.md` — the bullet sits at :235–241 in "Universal tracking rules": distinct name, the derived-claims domain phrase, the pinned and procedural forms, the free-standing defect named. VERIFIED.
- AC2: `sed -n '228,244p' skills/shared/guard-doctrine.md` — the `:231` pointer now reads "the tracking-rules derived-figures rule applies" (wraps :231–232); the deference headline (:234), grade clause (:235), M124 story with its `git show a5a7007` citation (:236), and re-pointed corollary headline (:241) all present; `grep -c '### D-099' cairn/DECISIONS.md` = 1, the narrow supersession of D-091 part 3's placement clause. VERIFIED.
- AC3: sweep re-run at review — the two-file diff's added lines classified in the T4 work-log line (11 of 12 carry/wrap the 9 clauses, 1 cross-reference connective); all 9 clauses guard-pinned and harness-registered (blanking exercised by the suite run below); fresh probe run: 29/29 RED as failures, 0 errors, restoration hash-verified (9 clauses × negation/relocation/dispersal + 2 subject transpositions). VERIFIED.
- AC4: fresh sweep `git diff main...HEAD | grep '^+[^+]' | grep -nE '[0-9]'` re-read at review head; every derived figure stands beside its named procedure, committed artifact, or citation; no free-standing figure; no append-only supersession needed. The Review section's own figures name their procedures inline. VERIFIED.
- AC5: three suites run singly at review, each exit checked: skills 757 OK (exit 0), scripts 345 OK (exit 0), hooks 103 OK (exit 0). VERIFIED.

Consistency gate: `cairn_validate` exit 0, all checks passed (output read, not recalled); no DESIGN.md principle changed → `cairn_impact --changed` skipped; generic profile → no toolchain checks. Driving RR: — → projection-vs-outcome no-ops.

Fan-out 2026-08-08 (three lenses + scorer): diff-bug [O] 26 candidates, blame-history [S] 0, prior-review [S] 2; scorer actioned 9 at ≥80, logged 19 below. All 9 fixed on the branch this pass:

- F19/87 — T2 work-log assert-count stale, the milestone's own defect class: superseded by the dated correction line in the work log (append-only pathway).
- F1/85, F3/85 — D-099's "otherwise stands" enumeration false against D-095; classification misattributed to the effort page: both superseded narrowly by D-100.
- F12/84 — the M124-story assert still read section6(), a dispersal hole: re-scoped to the rule's paragraph slice.
- F5/82 — pin conjunction mismatch (tracking-rules "and" vs §6 grade "or"): grade clause reworded to govern the procedure half explicitly, beside the pinned form's anchor; guard assert + harness block re-anchored.
- F10/82 — corollary body still stated the grade term: now "at the same grade as any other count", full deference.
- F13/82 — vacuous upper-bound assert in test_derived_figures deleted; the next-bullet content check carries the bound.
- F22/80 — the re-pointed `:231` counts pointer was unpinned: wrap-spanning assert + harness registration added.
- F27/80 — AC4's executed sweep was a digit-line proxy (the M132 unit-mismatch shape): re-run over every added line including word-form numbers; corrected evidence below.

Logged (<80, surfaced not dropped): F28/78 (universal on the proxy sweep — remedied with F27), F2/74 (D-100 now cites D-095), F21/72 (AC3 classification re-derived fresh below), F20/66 (probe script uncommitted; mutations restated in the T4 line, fresh run recorded here), F8/66 (no branch-added limiter — conduct rule for writes; Scope Out routes pre-existing figures), F4/62 (D-100 quotes the row's "roughly half"), F14/60 (startswith tautological under the uniqueness assert), F11/58 (informal antecedent "count rule's pin obligation above"), F6/52 (deference headline restates the operative form — AC2 forbids only a weaker parallel), F25/48 (D-090 revisit path uncited in D-099), F18/45 (legacy test name), F9/40 ("hand-written" qualifier), F24/40 (single-line wrap for pin matchability, the M118 remedy), F15/35 (docstring's four doctrine clauses vs five registrations — headline pinned separately), F17/35 (twin registration discrimination), F16/32 (locator vs future non-bold sibling), F26/32 ("placement clause" is AC2's own framing), F23/30 (pre-existing enumeration), F7/30 (domain-phrase repetition is AC1's requirement).

Corrected evidence (supersedes the AC3/AC4 lines above where they conflict):

- AC3, re-derived at the review working tree: `git diff main -- skills/shared/tracking-rules.md skills/shared/guard-doctrine.md` adds 13 lines — 11 carry or wrap the 9 rule clauses, 1 is the now-guard-pinned cross-reference pointer, 1 a reflow fragment of the corollary's pre-existing sentence; probes re-run on final bytes: 29/29 RED as failures, 0 errors, restoration hash-verified.
- AC4, full-domain sweep: every added line (`git diff main | grep '^+[^+]'`) — digit-bearing lines re-read, word-form lines swept with `grep -iE '\b(one|two|three|four|five|six|seven|eight|nine|ten|both|half|dozen)\b' | grep -viE '[0-9]'` (the first attempt's `-n` flag poisoned the digit-exclusion filter — caught by probing the instrument against a known hit, then removed); six word-form hits, each a definitional enumeration beside its own list, a code string quoting the rule, or non-figure prose. One non-compliant figure found on the branch — T2's stale assert count (F19) — superseded by the work-log correction line per the append-only pathway. No other free-standing figure.
