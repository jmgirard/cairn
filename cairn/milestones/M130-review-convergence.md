# M130: Review returns are reserved for breaches of bounded promises

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3, GP1, GP3
- **Branch/PR:** m130-review-convergence · https://github.com/jmgirard/cairn/pull/130

## Goal

A milestone's review converges by construction: criteria may promise only
what a named procedure can check, and review returns work only for real
breaches of such promises — ending the fix-the-instance, falsify-the-repair
loop measured in intraclass M100 (three returns, three lenses per pass).

## Scope

**In:** three rule changes and their guards. (1) Plan side: a
bounded-promise rule in `/milestone-plan` — universal-claim criteria name
their enumerating procedure — asked as a third mechanical question by the
step-3 criteria audit (and by the same reader at `/milestone-brief`
ingestion). (2) Review side: a return floor in `/milestone-review` over the
actioned findings list, with a distinct amendment-return route for
unbounded criteria, its own work-log shape, its own second-occurrence stop,
and a D-entry narrowing D-064's counting clause accordingly. (3) Doctrine:
a delete-first remedy sentence in `guard-doctrine.md` §6 for false claims
in unshipped prose. Trigger discharged at the D-090 door: the defect is in
shipped behavior — what `/milestone-review` did for a downstream repo's
users (intraclass M100's measured three-return thrash).

**Out:** sub-threshold self-shipped-doctrine disposition → existing RR06
rec 6 candidate row (distinct: it governs sub-80 findings). Advisory-mode
rollout → dropped at the 2026-08-01 plan gate (floor loosens the gate; the
merge-approval gate remains the safety net). Delete-first over merged
current knowledge → dropped at the same gate (D-045's corrected-in-place
rule stands). Any new instrument, checker, or audit step → none (D-090).

## Acceptance criteria

- [x] AC1: `skills/milestone-plan/SKILL.md` ships the bounded-promise rule —
      an acceptance criterion making a universal claim ("no X", "every Y")
      names the procedure (a search, sweep, or test run) that enumerates its
      domain, and where no stated procedure can enumerate the domain the
      criterion instead claims what a procedure it names actually swept —
      and its step-3 criteria audit asks this as a third mechanical question
      of each criterion; `skills/milestone-brief/SKILL.md`'s same-reader
      sentence counts three questions; the two existing reader guards in
      `skills/tests/test_fresh_context_readers.py` (and their
      mutation-registry blocks) are updated; each newly pinned sentence has
      its own registered block.
- [x] AC2: `skills/milestone-review/SKILL.md` states a return floor over the
      actioned (score ≥80) findings list: a finding moves the milestone back
      to `in-progress` only when it demonstrates an acceptance criterion
      failing — inside its named procedure's domain, where it names one — or
      when scored ≥90 on a defect in what the repo's deliverables do for
      their users (for this plugin: what the skills, hooks, and scripts do,
      not doctrine prose); every other actioned finding takes the existing
      fix-now / follow-up / reject triage with no status change and is
      logged; the amendment return (AC3) is the named exception to "only
      when".
- [x] AC3: the same floor text routes the unbounded-criterion case: a
      finding that falsifies a criterion only outside its named procedure's
      domain is evidence the criterion is unbounded and routes to the gated
      criterion-amendment protocol (`/milestone-implement` step 6) and
      re-review, the amendment the only work convened, status set to
      `in-progress` for it; the work-log line carries a fixed shape — the
      criterion's positional id plus the amended clause quoted verbatim —
      counted per milestone on its own track, never reset by a re-cut,
      outside the defect-return count; a second amendment return on the same
      positional id stops and goes to the user.
- [x] AC4: `skills/shared/guard-doctrine.md` §6 states the delete-first
      remedy: for a claim proven false in prose the branch in hand added,
      the first remedy weighed is deleting the claim, where a search over
      the repo for the claim's subject finds no dependent; correction is the
      remedy where one exists; merged current knowledge stays
      corrected-in-place and marked (D-045); IP4 history stays superseded,
      never edited.
- [x] AC5: every sentence added to the four touched prose files by
      `git diff <default-branch>..HEAD` is dispositioned in an Inversion
      table authored by review inside `## Review`: each guard-pinned
      sentence inverted in place (relabel/negate/transpose) with the suite
      required red, then restored, its result recorded; each unpinned added
      sentence listed as unguarded-by-design with its reason.
- [x] AC6: the active profile's `verify` slot suites, as `cairn/PROFILE.md`
      states them, and `python3 scripts/cairn_validate.py` all exit 0.

## Coverage

- AC1 → T1, T2
- AC2 → T3, T4
- AC3 → T3, T4, T6
- AC4 → T5
- AC5 → T7
- AC6 → T8

## Tasks

- [x] T1: Author the bounded-promise drafting rule and the third audit
      question in `skills/milestone-plan/SKILL.md` (steps 2–4); update
      `skills/milestone-brief/SKILL.md`'s same-reader sentence to three
      questions. Copy anchor bytes from the shipped files, never from
      drafts (M95 lesson).
- [x] T2: Update `skills/tests/test_fresh_context_readers.py` (the two
      question-count guards) and their mutation-registry blocks
      (`test_mutation_harness.py`); add one registered block per newly
      pinned AC1 sentence.
- [x] T3: Author the return floor, the amendment-return route, its fixed
      work-log shape, and its second-occurrence stop in
      `skills/milestone-review/SKILL.md` (steps 4–5), composing with the
      step-4 gate text and the thrash rule rather than contradicting them.
- [x] T4: Add registered guard blocks for each T3 rule sentence.
- [x] T5: Author the §6 delete-first sentence in
      `skills/shared/guard-doctrine.md`; add its guard and registry block.
- [x] T6: Append the D-entry narrowing D-064's counting clause (amendment
      returns tracked on their own per-milestone track, never reset by a
      re-cut; second same-id occurrence stops).
- [x] T7: Pre-review, run the AC5 inversion sweep once and close any gaps
      found (review re-runs it fresh for the table).
- [x] T8: Run the `verify` suites and `cairn_validate`; all exit 0.

## Work log

- 2026-08-01: created by /milestone-plan (trigger: intraclass M100 thrash — three review returns on an unbounded truthfulness criterion, each pass falsifying its predecessor's repair; D-090 door discharged by naming this shipped-behavior defect).
- 2026-08-01: criteria audit ran twice ([O] fresh reader): pass 1 returned five PROBLEMs (dangling antecedent, floor narrower than pre-existing criteria, amendment route = the pass it forbade, D-045 collision, self-violating AC5 denominator); pass 2 on the reworded set returned five more (restated question-count sites + two guards, sub-80 return leak, amendment-route status unreachability, branch-vs-merged scoping for delete-first, table ownership); all ten fixed in the final wording above.
- 2026-08-01: plan gate chose the two-band return floor (in-domain AC breach ≥80; functional shipped-defect ≥90) over keeping any-80+ returns because the flat bar is what produced the intraclass loop; falsified by an 80–89 non-AC finding later proving a user-visible shipped defect review should have returned on.
- 2026-08-01: plan gate chose a separate amendment-return track with its own second-occurrence stop over one thrash counter because one bad promise should not force a re-plan of sound work; falsified by rewording loops recurring without tripping any stop. Narrows D-064 (T6).
- 2026-08-01: plan gate chose delete-first scoped to branch-added prose over superseding D-045 because the intraclass loop fed on prose being authored, not on merged knowledge; falsified by fix-in-place corrections in merged current knowledge re-staling in a D-083→D-093-shaped cascade.
- 2026-08-01: plan gate chose live-on-merge over a two-milestone advisory period because the floor loosens the gate and the merge-approval gate remains the safety net; falsified by the floor filtering a finding that later ships as a user-visible defect.
- 2026-08-01: plan gate chose third-question-everywhere (brief ingestion included) over plan-only because a two-question brief reader would falsify the shipped same-reader claim; falsified by an RB binding criterion legitimately requiring an unenumerable universal.
- 2026-08-01: T1+T2 done — bounded-promise rule + third question shipped in plan and brief skills; 4 new guards, 2 updated, 4 new registry blocks; repo-wide sweep found one stale count restatement (a test comment), reworded count-free; suites 711/337/103 green.
- 2026-08-01: T3+T4 done — return floor + amendment return shipped in review skill step 5; TestReturnFloor (11 tests) + 12 registry blocks; skills suite green.
- 2026-08-01: T5+T6 done — §6 delete-first remedy (self-compliant wording: passes 2 and 3 named, no bare universal) + guard + 2 registry blocks; D-097 appended narrowing D-064; validate green.
- 2026-08-02: T7+T8 done — inversion sweep 21/21 red then restored (script restores in finally, byte-verified; M124); one gap closed (the delete-first applicability clause was unpinned, now pinned + registered); suites 711+2/337/103 and validate all exit 0; status → review.
- 2026-08-02: correction — the line above's "711+2" and the Review section's first-recorded 713 were undercounts; measured 723 skills tests at the pre-fix review head and 726 after the fix pass (procedure: `python3 -m unittest discover -s skills/tests -q`, count from the "Ran N tests" line); Review section corrected in place (review D12, scored 92).
- 2026-08-02: review fan-out (3 lenses, 26 scored findings) → fix-now pass: amendment-return keying widened to procedure-less criteria (D3/D7), defect-return count restated as step-4 + floor returns (D1/D2/D8), stop + work-log duty added to both return paths (D4/D5), fixed shape wired into /milestone-implement step 6 (D6), counts corrected (D12), test rename + count-free docstring (D16/D17), parenthetical dispositioned (D15), evidence header reworded (D22); guards and registry updated to the revised bytes; inversion sweep re-run 24/24 RED.
- 2026-08-02: minor amendment — Principles touched gains GP3 (review D19: the floor's "for this plugin" gloss instantiates repo-specifics in the portable core; recorded so principle impact is readable from the header).

## Decisions

## Review

Evidence current as of the post-fix review pass, 2026-08-02, branch `m130-review-convergence`, PR #130 (final head named in the work log).

- AC1: bounded-promise rule + third question present once each in plan and brief skills (`grep -c` = 1 per site; "audit's three questions" = 1); `test_fresh_context_readers.py` exit 0; 4 M130 registry entries.
- AC2: "Return floor (M130)" + "Amendment return (M130)" present in review skill (grep = 2); `test_thrash_rule.py` exit 0; 15 TestReturnFloor registry entries after the fix pass.
- AC3: floor text evidence above; keying, fixed shape, own-track counting, and second-occurrence stop inversion-proven (rows 13–21 below); D-097 in DECISIONS.md, cited in the review skill.
- AC4: §6 delete-first sentence present (grep = 1); `test_lesson_graduation.py` exit 0; 3 registry blocks (ordering, applicability, carve-out).
- AC5: inversion sweep run fresh at review and re-run after the fix pass — 24/24 pinned sentences RED under inversion, baseline GREEN after byte-verified restore. Procedure: per (old, new) pair, replace-once, run the named guard file via unittest discover, require nonzero exit, restore in `finally`, assert byte identity.
- AC6: `python3 -m unittest discover -s {skills,scripts,hooks}/tests` exit 0/0/0 — 726/337/103 tests (main baseline 707; +7 readers net, +15 floor net... derived: final skills count measured 726 at the post-fix head; the earlier recorded 713 and the work-log "711+2" were undercounts, corrected per the work-log correction line); `cairn_validate.py` exit 0 all PASS/OK.

Inversion table (pinned sentence inverted → guard → result), post-fix run:
1 plan third question negated (readers) RED · 2 plan reaudit count reverted (readers) RED · 3 bounded-promise rule negated (readers) RED · 4 fallback transposed (readers) RED · 5 hand-list clause inverted (readers) RED · 6 brief third question dropped (readers) RED · 7 floor only-when inverted (thrash) RED · 8 domain limb unconditioned (thrash) RED · 9 shipped-defect band lowered ≥90→≥60 (thrash) RED · 10 doctrine-prose exclusion inverted (thrash) RED · 11 no-status-change clause inverted (thrash) RED · 12 named exception deleted (thrash) RED · 13 defect-count members dropped (thrash) RED · 14 floor-exit stop removed (thrash) RED · 15 thrash-count cross-ref inverted (thrash) RED · 16 keying second case dropped (thrash) RED · 17 amendment-only convening widened (thrash) RED · 18 implement wiring dropped (thrash) RED · 19 fixed shape unfixed (thrash) RED · 20 own track merged (thrash) RED · 21 second-occurrence stop removed (thrash) RED · 22 applicability clause inverted (graduation) RED · 23 delete-first relabeled last (graduation) RED · 24 D-045 carve-out inverted (graduation) RED.

Unguarded-by-design (added sentences/clauses no guard pins, with reasons):
- plan: "asks three mechanical questions" numeral — the question list is the count; pinning the numeral restates a count (§6); the third question is row 1.
- plan: "the list becomes the sweep and every site it omits ships stale (the M118 lesson)" — elaboration restating the LESSONS line; the rule is rows 3–5.
- review: "(for this plugin: what the skills, hooks, and scripts do, …)" — repo-specific gloss AC2 mandated; the operative exclusion is row 10 (surfaced by review D15).
- review: "is evidence about the promise, not the work" — elaboration; the operative keying is row 16.
- review: "Its work-log line carries a fixed shape —" framing — the shape literal is row 19.
- review: "— no further round is convened; the disposition goes to the user" — elaboration of "stops" (row 21).
- review: "(D-097 narrows D-064)" — citation, not rule.
- doctrine: "the measured failure mode is the repair that re-falsifies: intraclass M100's review passes 2 and 3 …" — evidence/motivation; operative clauses are rows 22–24.

Fan-out record: three lenses ([O] diff-bug: 22 findings; [S] blame-history: 9 items, 5 self-marked clean; [S] prior-review: 0 findings, mechanically corroborated all new registry blocks redden when blanked) → [S] scorer over 26 scored findings.

Actioned (≥80), all fix-now under the return floor (none met a return: no in-domain AC breach; none ≥90 on functional shipped behavior):
- D12 (92) — recorded suite counts wrong (713 / "711+2" vs measured). FIXED: Review corrected in place; work-log correction line appended (history supersede).
- D6 (82) — amendment-return fixed shape unstated in the skill that writes it. FIXED: /milestone-implement step 6 names the shape; pinned + registered + inverted (row 18).
- D3 (80) — amendment route unreachable for criteria naming no procedure (the M100 trigger class). FIXED: keying now names both cases via the never-reinterpret rule (row 16); resolves D7's double-route.

Logged sub-80 (count: 23; fixed-in-passing marked):
- D1 (62) count sentence un-counts step-4 returns — FIXED (row 13). D2 (72) thrash rule uncross-referenced — FIXED (row 15). D4 (62) no stop on return paths — FIXED (rows 14, 17). D5 (68) floor return had no work-log duty — FIXED (row 14). D7 (66) double route — FIXED with D3. D8 (60) D-097 narrower than shipped — premise dissolved by D1's fix (step-4 returns count again). D15 (78) unpinned parenthetical — FIXED (unguarded list). D16 (42) docstring numeral — FIXED count-free. D17 (68) test name said "both", asserts three — FIXED (renamed). D19 (74) GP3 touched unrecorded — FIXED (header amended, work-log line). D22 (48) evidence header named a nonexistent commit — FIXED (reworded).
- Logged, no change: D9 (52) doctrine-prose exclusion removes D-064 trigger (b)'s exemplar class — intentional tradeoff, watched by the plan work log's falsifier line. D10 (68) / B3 (68) / B9 (66) D-090 discharge definitional tension — the discharge was made and shown at the plan gate; the merge gate below is the deciding authority; logged. D11 (46) branch/merged split additive to D-045, plan work log records the choice. D13 (55) tick-before-evidence sequencing — disclosed above, order restored this pass. D14 (45) AC5 four-file scope — D-097's prose is dispositioned by T6's durable-record preview, not the inversion table. D18 (62) three §6 properties in one test method — accepted; harness still catches each block. D20 (48) "where one exists" antecedent — contrastive reading; style tier. D21 (32) reflow cosmetics. B2 (65) shipped-vs-doctrine dichotomy strained for prose-artifact repos — same watch as D9. B4 (60) resemblance to retired §8 stop — different subject (promise wording, not certification); D-097 names its own supersede condition.
