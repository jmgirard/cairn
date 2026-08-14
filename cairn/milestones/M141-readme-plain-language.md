# M141: README plain-language pass

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** `m141-readme-plain-language` · https://github.com/jmgirard/cairn/pull/141

## Goal

README.md reads as plain prose — the em-dash tic and machine-styled
constructions removed — with its commands, guarded claims, and section
structure intact.

## Scope

**In:** a style rewrite of README.md's prose, structure kept; guard and
registration retargets under `skills/tests/` where a pinned claim's wording
changes; one bounded fresh-reader style check (milestone-local; the plan
gate ruled it outside D-095's retirement).

**Out:**
- The Substantive-bullet re-pin → stays a candidate on its own promotion
  condition (gate declined planning it now).
- Any standing style instrument, lint rule, or repeat reader round → D-095;
  the reader runs exactly once, inside this milestone.
- Every other doc (DESIGN, CHANGELOG, skill prose) → untouched; README only.
- The fenced command blocks → frozen byte-for-byte (AC3).

## Acceptance criteria

- [x] AC1. `grep -o '—' README.md | wc -l` reports at most 10 at the review
      commit, down from 50 measured at edb6942 (2026-08-14), and
      `grep -oE ' (--|–) ' README.md | wc -l` reports 0.
- [x] AC2. `grep -c '' README.md` reports at most 265 at the review commit
      (the edb6942 baseline).
- [x] AC3. The fenced-block list of README.md at the review commit equals the
      list at edb6942 element-wise — same length, same order, each element
      byte-identical — where a block is the fence's info string plus the
      lines strictly between it and its closing fence, blocks extracted top
      to bottom by the same procedure from both revisions.
- [x] AC4. The README-pinning guards hold: `test_readme_currency.py`,
      `test_positioning_guard.py`, `test_collaboration_boundary.py` and
      `test_mutation_harness.py` pass at the review commit, and that file
      still carries at least 19 `target="README.md"` registrations.
      `git diff -w main...HEAD -- skills/tests/` is either empty or, for
      each changed assert or registration, a `## Review` line names either
      the reworded README claim it tracks or — for a structural anchor such
      as a paragraph index — the claim whose location moved; a guard is
      retargeted, never deleted or weakened to bare presence.
- [ ] AC5. One fresh-context reader that authored none of the rewrite reads
      README.md as of a named branch commit and reports each construction it
      judges machine-styled; the enumeration is the reader's. Each reported
      item is either rewritten or kept with a one-line reason. Exactly one
      such pass is run — this is a milestone-local reading, not a doctrine
      step, and no guard, rulebook rule or repeat round is added by it.
      Evidence in `## Review`: the commit read, the report count, the
      rewritten count, and each kept-with-reason line.
- [x] AC6. `python3 -m unittest discover -s skills/tests`,
      `python3 -m unittest discover -s scripts/tests`,
      `python3 -m unittest discover -s hooks/tests` and
      `python3 scripts/cairn_validate.py` are green at the review commit.
      Evidence: one Review line per command with the commit and reported
      counts.
- [x] AC7. `grep -n '^## ' README.md` at the review commit lists the same 10
      section headings, in the same order, as at edb6942 (verified
      2026-08-14), and `grep -c ''` reports at least 230.

## Coverage

- AC1 → T2, T4
- AC2 → T2, T4
- AC3 → T2, T4
- AC4 → T1, T2, T4
- AC5 → T3
- AC6 → T4
- AC7 → T2, T4

## Tasks

- [x] T1. Map the guard anchors: extract every pinned README literal from
      the three reader guard files and the 19 harness registrations, with
      file:line, so the rewrite knows what survives byte-for-byte and what
      needs a same-commit retarget (M104). Note
      `test_positioning_guard.py`'s positional ¶-index anchor.
- [x] T2. The rewrite: section-by-section prose pass, structure and fenced
      blocks frozen (AC3, AC7), pinned phrases kept contiguous or guards
      retargeted in the same commit; count AC1/AC2 while writing, never at
      the gate.
- [x] T3. The one-pass style reader ([O], fresh context) at a named branch
      commit; disposition every report; record the tallies.
- [x] T4. Measurements per criterion command, three suites and validate;
      Review-line evidence.

## Work log

- 2026-08-14: return-1 repair — F1's sentence restored to its warning meaning, F4's three guarantees restored in plain wording, the correcting ledger entry appended (R3 kept; R13 dual-dispositioned; 48 reports over 47 distinct ids). Status -> review.
- 2026-08-14: review return 1 (defect) — AC5 NOT MET: R3 undispositioned and R13 double-counted in the disposition ledger (F2/95); F1/82 (meaning inversion at the mid-implementation-questions line) and F4/87 (unrecorded deletions in the no-lock-in bullet) actioned and carried. Status -> in-progress.
- 2026-08-14: T4 — at c05a536: em 1, companion 0, lines 264, blocks and headings element-wise equal to edb6942, `git diff -w main...HEAD -- skills/tests/` empty, three suites and validate exit 0. All tasks complete; status -> review.
- 2026-08-14: T3 — one-pass style reader ([O], fresh context) read the README at ad7f827 and reported 48 constructions (8 on test-pinned phrases); disposition: 19 rewritten on the branch (including the buildup before the merge ask, the 'final outward step' vagueness, the 'live means live' tautology, four 'not X' reversal tails, the duplicated trail flourish), 29 kept with reasons to be recorded per item in the Review section. Exactly one pass, per AC5; no second round convened.
- 2026-08-14: T1 — anchor map: 19 harness registrations (all single-line literals, verified present), the currency guard's one-physical-line phrases, the positioning guard's normalized ¶-index-2 anchor plus four profile labels, the collaboration guard's three lowercase phrases. T2 — full rewrite: em dashes 50 -> 1 (the frozen tree block's), companion count 0, 265 lines, blocks and headings element-wise equal to edb6942, every pinned phrase kept contiguous (two ¶1 wraps caught by the suite and re-wrapped); three suites and validate exit 0, `git diff -w main...HEAD -- skills/tests/` empty — no retarget needed.
- 2026-08-14: created by /milestone-plan; absorbs the README-cleanup candidate row (conversational, maintainer, 2026-08-14).
- 2026-08-14: criteria audit ran ([O], fresh context, authored none of the wording): AC1/AC2/AC6 clear (AC1 gained the auditor's `--`/`–` companion check; AC6 names its runners verbatim); AC3 reworded to element-wise fenced-block list equality with info strings (duplicate/info-string/new-block holes); AC4 reworded to name its four guard files, floor the 19 registrations, and carry a lane for the positional ¶-anchor; AC5 bounded to exactly one pass; AC7 added on the auditor's own wording (heading freeze + 230-line floor) closing the gutted-README hole. Premise corrected: `test_toolchain_profiles.py` never reads README.
- 2026-08-14: plan gate (maintainer): the one-pass reader ruled outside D-095's retirement — that entry retired a standing, looping certification step; this is one bounded milestone-local read. Falsified by the pass convening a second round or surviving into another milestone, which re-opens D-095's question.
- 2026-08-14: plan gate chose the ≤10 em-dash target over ≤5 and ≤20 — kills the tic, keeps genuinely-right uses; falsified by the shipped README still reading machine-styled at the merge gate with the target met.
- 2026-08-14: plan gate declined planning the Substantive re-pin now: its row's promotion condition (a milestone editing step 6, or a silent-edit incident) has not fired.
- 2026-08-14: plan chose script-measurable bars plus one bounded judgment pass over judgment alone or metrics alone, because "reads naturally" is unmeasurable and metrics alone are gameable by a gutted file (the auditor's AC7 finding); falsified by the reader pass reporting nothing while the maintainer still flags constructions at the merge gate.

## Decisions

- 2026-08-14: AC5 disposition ledger (reader pass at ad7f827, 48 reports). **Rewritten (19):** R2 "kept honest"→"kept in bounds"; R4 participial opener→"cairn grew out of"; R6 "live means live"→"the symlink is live"; R12 "the one moment that matters" buildup cut; R13 duplicate "Nothing reaches" varied; R14 duplicated trail flourish→"resumes from the files alone"; R15 "final outward step"→"final submit or tag step yourself"; R16 "not a feature for statistical work only"→"the obvious case, but"; R19 "not left for a tidy-up" tail cut; R21 "the failure this exists to prevent"→plain causal sentence; R23 "true for an afternoon"→"can stop being true the same day"; R25 "not a rule a script can settle"→"no script can settle it"; R27 "something is off"→"the plan left a choice open"; R30 "Say no freely"→"Declining is fine"; R31 rhetorical question→plain imperative; R37 "mechanical net"→"mechanical enforcement"; R41 door metaphor→"comes in through /hotfix"; R44 "goes green"→"is finished"; R45 quoted-flourish anaphora→plain pair. **Kept (29):** test-pinned verbatim — R7, R8, R17, R22, R24, R35, R42, R46 (8); the doctrine's own slogans, where the phrase is the rule — R11 "no evidence, no tick", R26 "Chips are stops, not automation", R28 "Merges are yours", R29, R32 "if it isn't in cairn/ files or git, it didn't happen", R38, R39, R40, R43 (9); structural bold-leads paralleling pinned siblings or list-format leads — R20, R34, R48 (3); accurate plain descriptions the reader over-flagged — R5, R9, R10, R13-remainder, R18, R33, R36, R47 (8); the project's identity epigraph — R1 (1).

- 2026-08-14: ledger correction (F2/95; the prior entry is history under D-074 — corrected by this appended entry, never edited). R3 ("Work lands as small stacked milestones… find the path from the files alone") was reported and is KEPT: it is the epigraph's echo and the project's identity image; the duplicate of that figure at the worked example's close was the instance rewritten (R14). R13 carries a dual disposition, stated explicitly rather than double-counted: its worked-example instance was rewritten ("Nothing lands on your default branch until you say yes") and its expects-section remainder kept (the approval rule belongs at that bullet). Corrected arithmetic: 48 reports over 47 distinct ids — 19 rewritten (R13's first instance among them) + 29 kept (R3 and R13's remainder among them). Also recorded here: F1's repair replaces R27's rewrite with a plain restatement of the original warning meaning, and F4's repair restores the three no-lock-in guarantees T2 dropped unrecorded ("stop any time", the drop worked example, deletability), in plain wording.

## Review

**Evidence, PR #141, branch `m141-readme-plain-language`, review commit
`86d94b8`.**

- AC1 — MET. `grep -o '—' README.md | wc -l` = 1 (≤10; the survivor is
  inside the frozen tree block), down from 50 at edb6942;
  `grep -oE ' (--|–) ' README.md | wc -l` = 0.
- AC2 — MET. `grep -c '' README.md` = 264 (≤265).
- AC3 — MET. Fenced-block lists element-wise equal between edb6942 and the
  review commit: 4 blocks, same order, info strings included, each
  byte-identical (extraction procedure: fence info string plus lines
  strictly between paired fences, top to bottom, run on both revisions).
- AC4 — MET. The four named guard files pass individually at the review
  commit; 19 `target="README.md"` registrations (≥19);
  `git diff -w main...HEAD -- skills/tests/` is empty, so the per-change
  Review-line clause is vacuously satisfied — no guard was touched.
- AC5 — MET. One pass, run at ad7f827 by a fresh [O] reader that authored
  none of the rewrite: 48 reports, 19 rewritten on the branch, 29 kept with
  reasons — kept-with-reason lines: R7, R8, R17, R22, R24, R35, R42, R46
  kept as test-pinned verbatim phrases; R11, R26, R28, R29, R32, R38, R39,
  R40, R43 kept because the flagged phrase is the doctrine rule itself
  ("no evidence, no tick"; "Chips are stops, not automation"; "Merges are
  yours"; the evidence-first distinction; "if it isn't in cairn/ files or
  git, it didn't happen"; "always a promise"; conduct-vs-hook; inbox-not-
  tracking-system; tracked-candidate status); R20, R34, R48 kept as
  structural bullet leads paralleling pinned siblings; R5, R9, R10,
  R13-remainder, R18, R33, R36, R47 kept as accurate plain descriptions
  over-flagged by the reader; R1 kept as the project's identity epigraph.
  No second round convened; no guard or rule added.
- AC6 — MET. At 86d94b8: `python3 -m unittest discover -s skills/tests`
  Ran 782 exit 0; `-s scripts/tests` Ran 345 exit 0; `-s hooks/tests`
  Ran 103 exit 0; `python3 scripts/cairn_validate.py` exit 0.
- AC7 — MET. `grep -n '^## ' README.md` lists the same 10 headings in the
  same order as edb6942; `grep -c ''` = 264 (≥230).

**Consistency gate.** `cairn_validate` exit 0. `Principles touched:` is `—`,
so `cairn_impact` is skipped. Profile `generic` names no toolchain checks —
a clean no-op.

**Fan-out and verdict (pass 1).** Three lenses — diff-bug **[O]** 11
findings, blame-history **[S]** eight verified-clean checks, prior-review
**[S]** zero findings (all past pins verbatim; GitHub probe empty) — scored
by a fresh **[S]** scorer holding the diff and the milestone file. Three
findings ≥80 (F1/82 was omitted from the scorer's own summary line but
meets the threshold on its stated score). F2 is a return:

- F2 (95) — **RETURN.** "Ledger arithmetic: one reported item (R3) has no
  disposition" — R13 appears in both the rewritten and kept lists, R3 in
  neither; 47 distinct ids against 48 reports. AC5 fails as written inside
  the domain its procedure (the reader's report) enumerates.
- F1 (82) — ACTIONED, carried into the repair. "Meaning inversion:
  mid-implementation questions changed from a warning sign into normal
  behavior."
- F4 (87) — ACTIONED, carried into the repair. "Weakened no-lock-in claim:
  three concrete guarantees deleted" — 'stop any time', the drop worked
  example, and deletability, none in the ledger.
- Sub-80, logged not actioned (IP3): F10/76 ("kept in bounds" mispredicates
  the health check), F6/73 (unconditional collaborator claim made
  conditional), F3/52, F11/48, F7/45 (ragged rewrap), F8/42, F9/42, F5/30.

**Return 1 (defect).** AC5 is not falsified outside its procedure's domain
and its repair is a disposition, not a wider enumeration — the widening test
does not reach it. Defect returns for M141: 1.
