# M144: The prose-guard suites leave the merge gate

- **Status:** in-progress
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m144-guards-leave-the-gate

## Goal

The prose-guard suite (`skills/tests`) stops gating this repo's commits,
merges, and check-offs — `scripts/tests` and `hooks/tests` keep gating; the
guard files stay in the repo, runnable by hand — as RR13's smallest reversible
probe of its reduction verdict, shipping the two decision entries the change
owes. Internal tier: the deliverable is this repo's own gate conduct (a
profile slot, a lessons line, two decision entries); the shipped skills,
profiles, and doctrine modules are untouched, so no external consumer relies
on it.

## Scope

**In:** `cairn/PROFILE.md` `## verify` (two gating commands; a non-gating
hand-run paragraph) and `## test-doctrine` (new rules owe no prose guard
here); a whole-sentence in-place correction of the LESSONS.md trivial-tier
suite-run lesson; two `cairn/DECISIONS.md` entries (the D-090 subject-clause
widening with removal carve-out and self-exception; the probe's exit
falsifier); a bounded sweep of remaining suite-directive text with per-hit
dispositions (`CLAUDE.md`'s verify sentence among them).

**Out:** deleting or editing anything under `skills/tests/` — nothing is
deleted; the probe is a switch (→ reversal is the AC3(b) falsifier's job).
The rulebook/doctrine reduction, incl. the mutation-harness sentence and
`guard-doctrine.md` → RR13 step-2 candidate row. LESSONS/candidate-row diet,
review fan-out scaling, scorer retirement, advisory-RR default → step-2 row.
Classifying `PROFILE.md`'s record class → no rule shipped; the current-
knowledge reading is recorded in the work log only.

## Acceptance criteria

- [ ] AC1: The `## verify` slot of `cairn/PROFILE.md` names exactly two
      commands as gating — `python3 -m unittest discover -s scripts/tests`
      and `python3 -m unittest discover -s hooks/tests` — and no third; a
      separate, explicitly non-gating paragraph names `skills/tests` as
      hand-runnable and keeps the discover-only note; and the
      `## test-doctrine` slot states that a new rulebook or skill rule no
      longer owes a prose guard or mutation registration in this repo, while
      the shipped "What gets a test" doctrine continues to govern adopting
      repos.
- [ ] AC2: The `cairn/LESSONS.md` M56+M65 lesson is corrected in place as a
      whole sentence (no contradictory remainder), naming the two gating
      suites and `skills/tests` as hand-run only, marked in the line's
      leading attribution parens (`… corrected M144`), without adding a line
      (the file sits at 49/50).
- [ ] AC3: `cairn/DECISIONS.md` gains two entries: (a) one superseding
      D-090's Decision subject clause — "No new milestone is planned whose
      deliverable is verification apparatus" — by extending it to new conduct
      rules about verification or records, quoting D-090's trigger clause
      verbatim as retained unchanged, carrying the removal carve-out (a
      milestone whose deliverable removes or narrows such a rule is outside
      the door) and the self-exception (M144 excepted by name; the door binds
      every plan gate after it); (b) one recording the probe's exit
      falsifier — the prose-guard gate re-arms if an unintended prose
      regression reaches main that the review fan-out missed and that a
      guard under `skills/tests` (retained, runnable, no longer gating) reds
      on, decided by running `python3 -m unittest discover -s skills/tests`
      against the shipping tree — closing "If that occurs, this is the entry
      to supersede."
- [ ] AC4: All three suites pass run by hand from the repo root against the
      branch HEAD as pushed for merge (re-run after the final pre-review
      push — M105): each `discover` run exits 0 with tests-ran > 0 (M138),
      each exit code captured directly, never through a pipe (M56).
- [ ] AC5: The sweep `grep -rn -e "skills/tests" -e "three suites"
      --include="*.md" --exclude-dir=milestones --exclude-dir=reviews
      --exclude-dir=legacy --exclude=DECISIONS.md .` — exclusions on the grep
      itself, never a downstream `grep -v` (M137), probed against a
      known-positive hit first — has every hit dispositioned in the Review
      evidence as one of: edited by this milestone / a guard-file citation
      that stays true (guards remain, ungated) / shipped doctrine deferred to
      step 2 / historical narration; no hit is a live gate directive. And
      each of the four gate-directive sites — `cairn/PROFILE.md` `## verify`
      and `## consistency-gate`, the LESSONS.md M56+M65 line, `CLAUDE.md`'s
      verify sentence — read whole, names no suite as gating that no longer
      gates.
- [ ] AC6: `cairn_validate` exits 0 at the branch HEAD as pushed for merge,
      with any dangling-id tokens newly unmasked by the two D-entries (M115)
      dispositioned.

## Coverage

- AC1 → T2
- AC2 → T3
- AC3 → T1
- AC4 → T5
- AC5 → T4
- AC6 → T1, T5

## Tasks

- [x] T1: Author the two DECISIONS.md entries per AC3 (decision template;
      next ids after D-107); run `cairn_validate` and disposition any newly
      unmasked dangling-id tokens.
- [x] T2: Rewrite `cairn/PROFILE.md` `## verify` (two gating commands + a
      non-gating hand-run paragraph keeping the discover-only note) and
      `## test-doctrine` (no prose guard owed for new rules in this repo;
      shipped doctrine untouched for adopters).
- [ ] T3: Correct the LESSONS.md M56+M65 lesson in place per AC2.
- [ ] T4: Run the AC5 sweep (known-positive probe first); disposition every
      hit; edit the live directives it finds (`CLAUDE.md`'s verify sentence;
      PROFILE's "all three must be green" line lands with T2); record the
      disposition ledger for Review.
- [ ] T5: Evidence pass: three suites + `cairn_validate` at the pushed
      branch HEAD, exit codes captured directly; re-run after any later
      pre-review push.

## Work log

- 2026-08-16: created by /milestone-plan from RR13's step-1 candidate row (RR13 recs 1–2, apply; the row graduates with this file).
- 2026-08-16: criteria audit ([O], fresh context): 16 findings — 14 with one clear answer repaired into the AC wording (sweep procedure and disposition categories, marker convention, falsifier decidability, merge-ref naming, the validate/dangler criterion), 2 posed at the gate (guard-authoring duty; door shape).
- 2026-08-16: plan gate chose full ungating over merge/trivial-only because step 2's reduction pays re-anchoring cost at every checkpoint a gating suite touches; falsified by an unintended prose regression reaching main that a retained guard reds on (the AC3(b) falsifier).
- 2026-08-16: plan gate chose no-guard-owed for new rules over owed-but-ungated because keeping the authoring obligation moves the gate without reducing the cost RR13 measured; falsified the same way — a missed regression a retained guard would have caught.
- 2026-08-16: plan gate chose the removal carve-out + self-exception door shape over enumerating RR13's steps as named exceptions because a principled carve-out covers future reductions without per-step supersessions; falsified by a removal-shaped milestone smuggling new verification rules in through the carve-out.
- 2026-08-16: AC1's test-doctrine clause was gate-added using the auditor's own repair wording (finding 6), re-read against the audit's three questions before writing; PROFILE.md read as current knowledge (a live declaration, edited in place), no classifying rule shipped (finding 15).
- 2026-08-16: T1 — D-108 (door widening, carve-out, self-exception) and D-109 (probe falsifier) appended; validate green, no dangling-id tokens unmasked (the M115 batch did not materialize — no forward D-108/D-109 tokens existed).
- 2026-08-16: T2 — PROFILE.md `## verify` rewritten (two gating commands, non-gating skills/tests paragraph with the discover-only note) and `## test-doctrine` (no guard owed for new rules here; shipped doctrine governs adopters); both gating suites exit 0, validate green.

## Decisions
