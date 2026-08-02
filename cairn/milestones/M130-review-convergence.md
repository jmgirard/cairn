# M130: Review returns are reserved for breaches of bounded promises

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3, GP1
- **Branch/PR:** m130-review-convergence

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

- [ ] AC1: `skills/milestone-plan/SKILL.md` ships the bounded-promise rule —
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
- [ ] AC2: `skills/milestone-review/SKILL.md` states a return floor over the
      actioned (score ≥80) findings list: a finding moves the milestone back
      to `in-progress` only when it demonstrates an acceptance criterion
      failing — inside its named procedure's domain, where it names one — or
      when scored ≥90 on a defect in what the repo's deliverables do for
      their users (for this plugin: what the skills, hooks, and scripts do,
      not doctrine prose); every other actioned finding takes the existing
      fix-now / follow-up / reject triage with no status change and is
      logged; the amendment return (AC3) is the named exception to "only
      when".
- [ ] AC3: the same floor text routes the unbounded-criterion case: a
      finding that falsifies a criterion only outside its named procedure's
      domain is evidence the criterion is unbounded and routes to the gated
      criterion-amendment protocol (`/milestone-implement` step 6) and
      re-review, the amendment the only work convened, status set to
      `in-progress` for it; the work-log line carries a fixed shape — the
      criterion's positional id plus the amended clause quoted verbatim —
      counted per milestone on its own track, never reset by a re-cut,
      outside the defect-return count; a second amendment return on the same
      positional id stops and goes to the user.
- [ ] AC4: `skills/shared/guard-doctrine.md` §6 states the delete-first
      remedy: for a claim proven false in prose the branch in hand added,
      the first remedy weighed is deleting the claim, where a search over
      the repo for the claim's subject finds no dependent; correction is the
      remedy where one exists; merged current knowledge stays
      corrected-in-place and marked (D-045); IP4 history stays superseded,
      never edited.
- [ ] AC5: every sentence added to the four touched prose files by
      `git diff <default-branch>..HEAD` is dispositioned in an Inversion
      table authored by review inside `## Review`: each guard-pinned
      sentence inverted in place (relabel/negate/transpose) with the suite
      required red, then restored, its result recorded; each unpinned added
      sentence listed as unguarded-by-design with its reason.
- [ ] AC6: the active profile's `verify` slot suites, as `cairn/PROFILE.md`
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
- [ ] T5: Author the §6 delete-first sentence in
      `skills/shared/guard-doctrine.md`; add its guard and registry block.
- [ ] T6: Append the D-entry narrowing D-064's counting clause (amendment
      returns tracked on their own per-milestone track, never reset by a
      re-cut; second same-id occurrence stops).
- [ ] T7: Pre-review, run the AC5 inversion sweep once and close any gaps
      found (review re-runs it fresh for the table).
- [ ] T8: Run the `verify` suites and `cairn_validate`; all exit 0.

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

## Decisions

## Review
