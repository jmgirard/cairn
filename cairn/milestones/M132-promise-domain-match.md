<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M132: A criterion's enumerating procedure covers the domain its promise quantifies over

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
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

- [x] AC1: `/milestone-plan` step 4's bounded-promise rule states that the
      procedure a universal criterion names must enumerate the domain that
      criterion's own universal quantifies over, and identifies the failing
      form by its property — a list whose membership is fixed by what the
      author recalled rather than decided by a procedure over the domain —
      with any examples given marked non-exhaustive.
- [x] AC2: The same rule states both halves of the remedy: that a counterexample
      defeating such an enumeration is not answered by a wider enumeration, and
      that the repair is to narrow the promise until a stated procedure settles
      it.
- [x] AC3: The criteria audit's third question states the domain-match test at
      both surfaces that carry it — `/milestone-plan` step 3 and
      `/milestone-brief`'s binding-criteria ingestion audit.
- [x] AC4: The amended rule is applied to two criteria and the classification
      recorded for each: intraclass M102's AC2 quoted verbatim, and a second
      criterion drawn from a cairn or downstream archive by a reader who has
      not seen the amended wording. Both classifications, and a rewrite of each
      that the amended rule passes, are produced by a fresh-context reader that
      authored none of the rule text. A classification of "passes" on M102's AC2
      is a failure of this criterion.
- [x] AC5: Every rule sentence this branch adds or changes is pinned by a guard
      that fails when that sentence is blanked. The domain is enumerated by
      `git diff --name-only <base>..HEAD` over the whole repo, filtered to
      `skills/**/*.md`; every added or changed non-blank line in those files is
      in-domain unless listed as exempt with its reason in the Review section.
      Evidence is the per-sentence mapping from each in-domain sentence to the
      registry entry covering it, plus the mutation-harness run over those
      entries — never the harness run alone.
- [x] AC6: The amended sections are inversion-proven as units — each relabelled,
      negated, or transposed in place, the suite run, red required, then
      restored and diffed — with one result recorded per section, not per
      sentence.
- [x] AC7: `python3 -m unittest` clean over the three suites (`skills/tests`,
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
- [x] **T4** — Enumerate the in-domain sentences by the AC5 diff command, add a
      registry entry per sentence, and run the mutation harness over exactly
      those entries; record the per-sentence mapping.
- [x] **T5** — Section-level inversion sweep over each amended section; then the
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
- 2026-08-02: T4 — 7 guards + 7 mutation registrations over the 5 added rule sentences and both audit-clause surfaces; per-sentence mapping in `## Decisions`. Each registration blanked individually and confirmed RED rather than inferred from the suite being green. skills suite 729 -> 736 tests, all green.
- 2026-08-02: T5 — all three amended sections inverted as units and RED, restored SHA-verified; gate clean: skills 736, scripts 337, hooks 103, `cairn_validate` all checks passed. Status in-progress -> review.
- 2026-08-02: review — prior-review lens found a partial pin on the M102 example sentence (its tail deleted green, the M114 class this milestone's own record claimed to avoid); confirmed by probe, fixed on the branch, and the whole diff swept for the class with no second instance. No status change: it demonstrates no acceptance criterion failing and is apparatus coverage rather than user-facing skill behaviour, so M130's return floor takes it as triage.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

- 2026-08-02 (T5, AC6): section-level inversion sweep, one result per
  section. Each section inverted as a unit in place — governing claim negated
  AND its subject transposed, per M131's finding that negation alone leaves a
  swapped subject green — then the skills suite run, then restored.

  | section | inverted suite |
  |---|---|
  | S1 `/milestone-plan` step-3 audit clause | RED |
  | S2 `/milestone-plan` step-4 bounded-promise rule | RED |
  | S3 `/milestone-brief` ingest audit clause | RED |

  Controls the sweep carried: baseline suite GREEN before the first mutation
  and GREEN after the last restore; each anchor asserted unique in its file
  before mutating (a non-unique anchor binds to the first occurrence — the
  M126 class); restoration written in a `finally:` and verified by SHA-256
  against the pre-sweep bytes for both files, not by eye (the M124 class,
  where a crash between mutate and restore silently contaminated every later
  measurement). `git diff --stat` over both files is empty after the sweep.

  S2's inversion was substantive rather than a relabel: "must enumerate the
  domain … not a proxy" → "may enumerate a proxy", "is a proxy however long
  its list" → "is a procedure over the domain, never a proxy", and the remedy
  reversed to "answered by a wider one … widen the enumeration until no
  counterexample remains" — i.e. the section was rewritten to say the thing
  the milestone exists to forbid, and the suite caught it.

- 2026-08-02 (T4, AC5): per-sentence mapping from the AC5 domain to the
  registry entry covering each. Domain enumerated by
  `git diff --name-only main..HEAD` filtered to `skills/**/*.md` — two files
  (`skills/milestone-plan/SKILL.md`, `skills/milestone-brief/SKILL.md`), 17
  added non-blank lines, 5 added rule sentences. No exemptions taken: the
  illustrative M102 sentence is registered like the operative ones, since
  classifying it "gloss" would be exactly the author judgment the criteria
  audit warned reproduces M102's own move.

  | added sentence | registry block → guard |
  |---|---|
  | "The procedure must enumerate the domain the criterion's own universal quantifies over, not a proxy for it." | `test_the_procedure_must_cover_the_promises_own_domain` |
  | "Naming a procedure is not passing this test: … is a proxy" | `test_naming_a_procedure_does_not_pass_the_domain_match_test` |
  | "…however long its list — spellings, renderings, known cases and whole families among others, never only those." | `test_the_instance_enumeration_examples_are_non_exhaustive` |
  | "A counterexample defeating such an enumeration is therefore not answered by a wider one; the repair is to narrow the promise until a stated procedure settles it." | `test_the_remedy_is_to_narrow_the_promise_not_widen_the_enumeration` |
  | "intraclass M102's \"no command reads git history\" … then `awk`" | `test_the_rule_carries_its_measured_failure` |
  | plan-gate audit clause "The third question is asked of the domain …" | `test_audit_question_is_asked_of_the_domain_not_a_proxy` |
  | brief-ingest audit clause "the third question asked of the domain …" | `test_ingest_audit_carries_the_domain_match_test` |

  Seven blocks over five sentences: the long property sentence is pinned
  twice (the property clause and the non-exhaustive examples clause
  separately), because a single assert over part of it would leave the rest
  deletable — the M114 partial-pin class.

  **Blanking result, run per entry rather than read off a green suite**
  (the M100/M117 blind spot: an all-green harness can mean the engine cannot
  see the entries): all 7 RED. Registry total 516.

  Two fragments the sentence-splitter flagged as unpinned are pre-existing
  text, not additions — `(the bounded-promise rule, step 4; M130)` and
  `It reads the wording` appear in the diff only because their lines rewrapped
  around the insertion. Both verified present in `main:skills/milestone-plan/SKILL.md`
  and already covered, by `test_audit_asks_the_bounded_promise_question` and
  `test_audit_reads_the_shipped_wording_never_a_paraphrase` respectively —
  checked against the registry, not assumed.

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

Fresh evidence, gathered by command at review time (2026-08-02, branch tip
`3618549`, PR #132). No `.github/workflows` exists, so the repo runs no CI and
the three local suites are the gate — the `generic` profile names no further
consistency-gate check.

**AC1 — MET.** All three clauses present exactly once in
`skills/milestone-plan/SKILL.md`, verified by substring count over the shipped
bytes: the domain-match test ("The procedure must enumerate the domain the
criterion's own universal quantifies over, not a proxy for it."), the
recalled-membership property ("an enumeration whose membership is fixed by what
the author recalled, rather than decided by a procedure over the domain, is a
proxy"), and the non-exhaustive marking ("spellings, renderings, known cases and
whole families among others, never only those").

**AC2 — MET.** Both remedy halves present: "A counterexample defeating such an
enumeration is therefore not answered by a wider one" and "the repair is to
narrow the promise until a stated procedure settles it".

**AC3 — MET.** The shared clause `asked of the / domain the claim quantifies
over, never of a proxy the named procedure / happens to enumerate (M132)` occurs
exactly once in each of `skills/milestone-plan/SKILL.md` (step 3) and
`skills/milestone-brief/SKILL.md` (ingestion audit) — byte-identical, so a
reader meeting either question meets the same test.

**AC4 — MET, and it discriminates.** Two `[O]` readers, neither having authored
the rule. Reader 1 saw no rule text at all and picked the second case
mechanically: 25 universal-claim criteria swept from three repos' milestone
files, intraclass M102 excluded, longest-by-character-count taken — circumplex
M68 AC11 (BC5), 1,936 chars. Reader 2 received only the rule text and the two
criteria, blind to which was the motivating case. Verdicts: **intraclass M102
AC2 FAILS** (AC4's stated failure condition was a verdict of "passes"; it was
not returned), **circumplex M68 AC11 PASSES**. Both rewrites recorded. Full
classification verbatim in this file's `## Decisions` section. The differing
verdicts are the load-bearing part: failing both would mean the rule rejects
sound criteria, passing both would mean it never fires on its own motivating
case.

**AC5 — MET.** Domain enumerated by `git diff --name-only main..HEAD` filtered
to `skills/**/*.md`, never by a hand-listed file set: two files, 17 added
non-blank lines, 5 added rule sentences. No exemptions taken. 7 registry blocks
cover them (the long property sentence pinned twice, so no part of it deletes
green — the M114 partial-pin class). Each block blanked INDIVIDUALLY and
confirmed RED, rather than inferred from a green suite (the M100/M117 blind
spot); each block also verified to occur exactly once in its target, so no
guard binds to a first match (the M126 class). Registry total 516.
Two fragments a sentence-splitter flagged are pre-existing text whose lines
merely rewrapped — both verified present in `main:skills/milestone-plan/SKILL.md`
and already covered by M130-era blocks.

**AC6 — MET.** Section-level inversion re-run fresh at review. Baseline suite
GREEN; S1 (plan step-3 audit clause) RED, S2 (plan step-4 bounded-promise rule)
RED, S3 (brief ingest audit clause) RED; restores SHA-256-verified byte-identical
against pre-sweep bytes and the post-sweep suite GREEN, with `git status` clean
over `skills/`. Anchors asserted unique before mutating.

**AC7 — MET.** `skills` 736 tests OK, `scripts` 337 OK, `hooks` 103 OK;
`cairn_validate` exit 0, all checks passed.

### Findings — prior-review lens (2026-08-02)

**PR1 — ACTIONED, fixed on the branch. Partial pin on the example sentence.**
The guard `test_the_rule_carries_its_measured_failure` and its registry block
both stopped at ``then `awk` ``, leaving the sentence's tail — `, which is no
git command at all.` — referenced by no guard, no registry entry and no other
test. **Verified before acting, not taken on report:** deleting that clause left
all 736 skills tests GREEN. This is the M114 partial-pin class that this
milestone's own T4 record claims to have avoided, and the lens noted the
adjacent long sentence WAS split into two blocks to cover its full length — so
the discipline was applied to one sentence and missed on the other.
Fix: guard regex and registry block both extended through `at all.`;
re-probed, the deletion is now RED. All 7 registrations still RED, each block
still unique in its target.

**Sweep for the same class across the whole diff, not just the reported
instance.** Every added sentence was probed by deleting whatever tail falls
beyond the last registered block covering it: two tails RED (pinned), three
sentences FULLY PINNED. No second instance. Restores SHA-verified.

**PR2 — no other prior-review regression.** The lens cleared the diff against
five classes past reviews raised on these files: false coverage (each of the 7
phrases occurs exactly once in its target), `index()`-bound blocks that crash
rather than fail (none — all plain containment blocks over prose), anchors
authored from draft rather than shipped bytes, a rule forking into two wordings
across surfaces (the shared clause is byte-identical; the two guards differ only
where the host grammar legitimately differs), and enumerations widened rather
than replaced (this diff replaces list-widening with the domain-match property,
which is its point).
