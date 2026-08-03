<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M132: A criterion's enumerating procedure covers the domain its promise quantifies over

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate -->
- **Principles touched:** GP3, GP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m132-promise-domain-match`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The bounded-promise rule rejects a criterion whose named procedure enumerates a
proxy for its domain rather than the domain itself, and names the repair.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `/milestone-plan` step 4's bounded-promise rule gains the domain-match
test, the property that identifies an instance-enumeration, and the positive
repair (narrow the promise until a stated procedure settles it) beside the
existing refusal. The criteria audit's third question carries the domain-match
test at both surfaces that state it (`/milestone-plan` step 3,
`/milestone-brief`'s binding-criteria ingestion). Guards and mutation-registry
entries for every rule sentence the branch adds or changes. A D-entry recording
the cross-repo host question D-090 leaves open.

**Out:** any `cairn_validate` check or other mechanical detector for the rule —
D-064 (6) rejected checks for this family as judgment, and no evidence here
supersedes that; a fix to intraclass M102 itself → intraclass's own re-cut,
which its pass-3 disposition already scopes. Rewording `guard-doctrine.md` §6/§9
→ not needed: both already state the stronger test, and this milestone's defect
is that `/milestone-plan`'s copy states a weaker one; if the branch does touch
them, AC5/AC6's domain covers those sentences by construction.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: `/milestone-plan` step 4's bounded-promise rule states that the
      procedure a universal criterion names must enumerate the domain that
      criterion's own universal quantifies over, and identifies the failing
      form by its property — a list whose membership is fixed by what the
      author recalled rather than decided by a procedure over the domain —
      with any examples given marked non-exhaustive.
- [ ] AC2: The same rule states both halves of the remedy: that a counterexample
      defeating such an enumeration is not answered by a wider enumeration, and
      that the repair is to narrow the promise until a stated procedure settles
      it.
- [ ] AC3: The criteria audit's third question states the domain-match test at
      both surfaces that carry it — `/milestone-plan` step 3 and
      `/milestone-brief`'s binding-criteria ingestion audit.
- [ ] AC4: The amended rule is applied to two criteria and the classification
      recorded for each: intraclass M102's AC2 quoted verbatim, and a second
      criterion drawn from a cairn or downstream archive by a reader who has
      not seen the amended wording. Both classifications, and a rewrite of each
      that the amended rule passes, are produced by a fresh-context reader that
      authored none of the rule text. A classification of "passes" on M102's AC2
      is a failure of this criterion.
- [ ] AC5: Every rule sentence this branch adds or changes is pinned by a guard
      that fails when that sentence is blanked. The domain is enumerated by
      `git diff --name-only <base>..HEAD` over the whole repo, filtered to
      `skills/**/*.md`; every added or changed non-blank line in those files is
      in-domain unless listed as exempt with its reason in the Review section.
      Evidence is the per-sentence mapping from each in-domain sentence to the
      registry entry covering it, plus the mutation-harness run over those
      entries — never the harness run alone.
- [ ] AC6: The amended sections are inversion-proven as units — each relabelled,
      negated, or transposed in place, the suite run, red required, then
      restored and diffed — with one result recorded per section, not per
      sentence.
- [ ] AC7: `python3 -m unittest` clean over the three suites (`skills/tests`,
      `scripts/tests`, `hooks/tests`), and `cairn_validate` all checks passed.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T4
- AC6 → T5
- AC7 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] **T1** — Amend `/milestone-plan` step 4's "Bounded promises only" rule
      (`skills/milestone-plan/SKILL.md:131-143`): the domain-match test, the
      recalled-membership property with non-exhaustive examples, and the two
      remedy halves. Draft against the existing sentence rather than appending
      a second rule beside it.
- [x] **T2** — Carry the domain-match test into the criteria audit's third
      question at `skills/milestone-plan/SKILL.md:95` and
      `skills/milestone-brief/SKILL.md:96`, keeping the two surfaces' wording
      identical so the existing cross-surface guards still bind.
- [x] **T3** — The AC4 classification pass: spawn a fresh-context `[O]` reader
      that has not seen the amended wording to pick the second criterion from
      an archive, then a second `[O]` reader given only the amended rule text
      to classify both and write both rewrites. Record verbatim in the
      milestone-local `## Decisions` section (the Review section is
      review-exclusive).
- [ ] **T4** — Enumerate the in-domain sentences by the AC5 diff command, add a
      registry entry per sentence, and run the mutation harness over exactly
      those entries; record the per-sentence mapping.
- [ ] **T5** — Section-level inversion sweep over each amended section; then the
      three suites and `cairn_validate`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-08-02: created by /milestone-plan. Trigger is a shipped-behavior defect measured downstream: intraclass M102's AC2 passed cairn's plan gate on 2026-08-02 with the M130 bounded-promise rule live, then took three review returns (each a genuinely new counterexample — ref spellings, a flag-value/`--` ordering bug, then `awk 'BEGIN{ … | getline }'`, which is not a git command) and is now parked `blocked`.
- 2026-08-02: criteria audit ([O], fresh context, authored none of the draft) returned ten findings plus a set-level verdict; four fixed before the gate, four taken to it. Fixed: AC1 defined the forbidden form by a three-item list (spellings/renderings/known cases), so intraclass's pass-3 family-enumeration escapes all three and passes the rule as drafted — replaced by the recalled-membership property; AC5/AC6 enumerated their domain by a hand-listed file set ("the three files named by AC1-AC3"), the M118 trap one level up, and that phrase had no referent since AC1-AC3 name two files and three surfaces — replaced by a whole-repo diff filtered by a stated test; AC5's evidence was a harness run over a hand-built registry with nothing mapping diff-enumerated sentences to entries, so one entry could go green while five sentences carried none — now the per-sentence mapping is the evidence. Set-level headline taken to the gate: AC1-AC3 are prose-presence criteria and AC4 was the only criterion connecting the rule to the defect, self-graded on one known example, so the set could ship green while the defect survived.
- 2026-08-02: plan gate chose stating the positive repair beside the refusal over a refusal-only rule because a rule that rejects and cannot repair leaves the planner to reinvent the fix, which is what cost intraclass three passes; falsified by a planner tripping the amended rule and still re-cutting around the same predicate.
- 2026-08-02: plan gate chose a second criterion plus fresh-context classification over one self-graded case because a rule tailored to its one known example passes its own test while the next instance sails through (the audit's set-level verdict); falsified by the second case being classified correctly by the rule's own author, which would show the fresh reader bought nothing.
- 2026-08-02: plan gate chose section-level inversion over per-sentence because the per-sentence form is the certification ceremony D-090/D-091 closed, re-entered as milestone evidence rather than as a shipped step, and the M121 lesson records that sentence-scoped sweeps miss the section's own governing claims; falsified by a section-level sweep passing while a sentence inside it inverts green.
- 2026-08-02: plan gate chose a D-entry annotating D-090 over proceeding silently because D-090 prescribes fixing a doctrine-prose defect "within the milestone that surfaces it", and the surfacing milestone is intraclass M102, in a repo that cannot edit cairn's shipped prose — the prescribed host does not exist for a cross-repo surfacing; falsified by a cross-repo defect that the surfacing repo's own milestone can in fact fix.
- 2026-08-02: start — branch `m132-promise-domain-match` cut from pushed main (`6397cad`), status planned->in-progress.
- 2026-08-02: T1 — the bounded-promise rule gains the domain-match test as a paragraph extending the existing sentence, not a second rule beside it: the named procedure must enumerate the domain the criterion's own universal quantifies over, an enumeration whose membership is fixed by author recall is a proxy however long its list (examples marked non-exhaustive, `families` included so intraclass's pass-3 family-enumeration is named rather than escaping), a counterexample is not answered by a wider enumeration, and the repair is to narrow the promise until a stated procedure settles it. 11 lines added, no existing line reflowed; 729 skills tests green, so no adjacent guard's anchor was split (the M104 trap).
- 2026-08-02: T2 — the domain-match clause lands at both audit surfaces by APPENDING to each existing question rather than rewording it, so every pinned byte sequence survives: the plan guard's `enumerates*\s+(the bounded-promise rule, step 4; M130)`, the brief guard's full three-question sequence, and both mutation-registry blocks including `It reads the wording\n   step 4 will write` (whose exact wrap the insertion preserves). The shared clause `asked of the / domain the claim quantifies over, never of a proxy the named procedure / happens to enumerate (M132)` is byte-identical at both surfaces, verified present exactly once in each file rather than assumed. 729 skills tests green.
- 2026-08-02: T3 — two-reader AC4 pass complete; both verdicts and both rewrites recorded verbatim in this file's `## Decisions` section. Result DISCRIMINATES: intraclass M102 AC2 FAILS (its second universal names no procedure; the checker decides a proxy property), circumplex M68 AC11 PASSES. T3's wording amended (minor, task-owned): it said to record in the Review section, which the ownership table makes review-exclusive — AC4 names no location, so no criterion changed.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

- 2026-08-02 (T3, AC4): the amended rule applied to two criteria by a
  fresh-context [O] reader given only the rule text and the two criteria,
  blind to which was the motivating case. The second criterion was picked by
  a different [O] reader that had not seen the amended wording, from a
  mechanical sweep of three repos' milestone files (25 universal-claim
  criteria collected, intraclass M102 excluded, longest-by-character-count
  taken as the tiebreak) — circumplex M68 AC11 (BC5), 1,936 characters.

  **intraclass M102 AC2 — FAILS.** Deciding clause: "The procedure must
  enumerate the domain the criterion's own universal quantifies over, not a
  proxy for it." The reader decomposed it into two universals and found they
  differ: "a command naming any of an enumerated set of history-dependent
  forms ... is refused" PASSES, because the quantifier is explicitly
  restricted to the enumerated set, so the list is the domain rather than a
  proxy for one — this half is already the rule's prescribed repair. The
  second, "no command in the committed ledger reads git history", names no
  procedure at all; the checker decides a different property ("names one of
  three enumerated forms"), a proxy whose membership is author-recalled, so
  "any route to history outside the three forms (a hook, an alias or
  subcommand that consults history internally, a config-supplied default, an
  env var, a shelled-out helper) ships unrefused while the criterion reads as
  satisfied." Rewrite: the checker refuses every command naming one of the
  three enumerated forms, each with a sample and a test exercising it, and is
  then run over every command in the committed ledger — that run being the
  sweep — wired into `verify`. What it gives up, stated: "the semantic
  guarantee ... A command that reads git history by a route outside those
  forms now passes both the checker and the criterion, and the milestone no
  longer claims otherwise."

  **circumplex M68 AC11 — PASSES**, borderline on one clause. Every universal
  is quantified over an artifact set the criterion names exhaustively (three
  named surfaces, one named string constant, the diff), and each empirical
  claim that would have quantified over an open domain is restated as what the
  named fixture sweep measured — including the in-place retraction "(a
  single-population sweep; not stated as a universal threshold)" and the
  refusal to extend rejection-rate claims to the unmeasured FIML tail. The
  borderline: "All documented rates are the committed fixture's values" reads
  broadly as quantifying over the whole package's documentation; the reader's
  offered tightening is "All rates stated in (i)-(iii) are the committed
  fixture's values (rounded); BC3's regeneration check is what keeps them tied
  to it."

  **Why this is the evidence AC4 asks for:** the two verdicts differ. A rule
  failing both would be over-broad — rejecting a sound criterion — and one
  passing both would not fire on its own motivating case. The discriminating
  outcome is what shows the rule is neither.

## Review
<!-- owner: review · exclusive -->
