# M115: Fresh-context reader instruments — plan-gate criteria audit and independent description-layer certification (RR06 recs 4–5)

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2, GP3, IP4
- **Branch/PR:** `m115-fresh-context-reader-instruments`

## Goal

Adopt RR06's two fresh-context reader instruments — an acceptance-criteria audit at
the plan and RR-ingest gates, and independent certification of the description layer
before a guard-authoring milestone reaches review — retiring author self-certification
of guard coverage as a D-059-shaped move.

## Scope

**In:** rec 4's criteria audit in `skills/milestone-plan/SKILL.md` step 3 and
`skills/milestone-brief/SKILL.md`'s "Ingesting an RR" · rec 5's certification as a new
section of `skills/shared/guard-doctrine.md` plus one line in
`skills/milestone-implement/SKILL.md` step 8 · prose-guards for both in a new
`skills/tests/test_fresh_context_readers.py`, registered in the mutation harness ·
D-067 · the ROADMAP rows.

**Out:** RR06 rec 6's disposition rule → stays a candidate row (its promotion
condition has not fired); the row is transcribed onto `main` by this plan commit so it
does not live only on a parked branch. · M114's open F1/F5 → M114's own eighth pass
after this merges; both sit in files that exist only on its branch. · any
`cairn_validate` mechanization → RR06 rec 9, D-059. · any `tracking-rules.md` edit →
RR06 Q3, D-057. · resuming, rebasing or merging M114, including dropping its duplicate
rec 4/5/6 rows at rebase → M114.

## Acceptance criteria

- [ ] AC1: The criteria audit is stated at both surfaces — `/milestone-plan` step 3 and
      `/milestone-brief`'s "Ingesting an RR" — each naming a fresh-context reader, the
      two mechanical questions per criterion (*what state of the world satisfies this
      exactly as written*; *does any IP or D-entry make that state unreachable*), and
      that its findings reach the user at the gate rather than being resolved silently.
- [ ] AC2: The description-layer certification is a new section of `guard-doctrine.md`
      naming its three checks (AC-clause→assert coverage, claim-vs-file accuracy,
      anchor-vs-shipped-bytes fidelity), the prohibition *the author never certifies its
      own guard's coverage*, and RR06's falsifier — carried inline here because RR06
      itself is unmerged on M114's branch, so this criterion is the referent an
      implementer transcribes from: "if guard-authoring milestones still average
      multiple description-layer returns after adoption, the step didn't work — retire
      it (D-059), don't tune it." `/milestone-implement` step 8 carries one routing
      line firing before `status -> review`.
- [ ] AC3: Every new doctrine clause across AC1 and AC2 carries a doctrine-pinning
      assert in `skills/tests/test_fresh_context_readers.py`, each with its own
      `Mutation(...)` entry whose block is copied from the shipped bytes and resolves
      exactly once in its target; doctrine-pinning assert count equals registered entry
      count, both **measured** out of the files, never projected (tolerance: exact);
      blanking every registered block reds its named test (tolerance: 0 survivors).
- [ ] AC4: Each new assert is inversion-proved in a `git archive` scratch copy whose
      baseline was verified green **first**: deleting or negating its pinned clause reds
      the named test, restoring returns green (tolerance: N/N red, N/N green, target
      byte-identical after each restore, the repo tree never mutated).
- [ ] AC5: This milestone applies AC2's own instrument to itself — before
      `status -> review` a fresh-context reader that authored no part of the
      implementation certifies M115's guards on AC2's three checks, its verdict and
      every discrepancy recorded verbatim in the work log; the gate is entered only at
      zero unresolved.
- [ ] AC6: D-067 is appended to `cairn/DECISIONS.md` recording both adoptions, the
      retirement of author self-certification of guard coverage, and the reservation of
      D-064–D-066 for M114's unmerged branch, back-referencing D-059, D-057, D-031 and
      RR06 — naming RR06 as unmerged, since it resolves only when M114 lands
      (tolerance: `git diff main..HEAD -- cairn/DECISIONS.md` contains zero deletion
      lines, and the count of `^### D-064` headings in `cairn/DECISIONS.md` is 0 — read
      the printed count, never `grep`'s exit code, which is 1 on no match).
- [ ] AC7: On the final tree the `verify` slot is clean — three suites from the repo
      root with exit codes captured separately, never piped (tolerance: exit 0 each) —
      `python3 scripts/cairn_validate.py` exits 0; `git diff --name-only main..HEAD`
      names no file under `scripts/` and not `skills/shared/tracking-rules.md`; and the
      M104 adjacency sweep holds (tolerance: 0 guard literals newly wrap-broken
      against `main`).

## Coverage

- AC1 → T1, T2
- AC2 → T3, T4
- AC3 → T2, T4, T7
- AC4 → T7
- AC5 → T6
- AC6 → T5
- AC7 → T1, T3, T4, T7

## Tasks

- [x] T1: Author the criteria audit into `skills/milestone-plan/SKILL.md:73` (step 3)
      and `skills/milestone-brief/SKILL.md:59` ("Ingesting an RR"). Grep the repo for
      restatements of the plan-gate wording first — README and templates go stale
      silently (M112).
- [x] T2: Guard T1 in a new `skills/tests/test_fresh_context_readers.py` — anchors
      copied from the shipped bytes, `\s+` across every wrap (M95/M105), target read via
      `Path.read_text` or the mutation engine cannot see it (M100); one `Mutation(...)`
      entry per doctrine-pinning assert, each block resolving exactly 1x.
- [ ] T3: Author the certification section at the end of `skills/shared/guard-doctrine.md`
      (after its current last section) and the one routing line in
      `skills/milestone-implement/SKILL.md:98` (step 8), before `status -> review`.
- [ ] T4: Guard T3 in the same file, same discipline as T2. Then run both sweeps: grep
      the guards for any short phrase the new prose repeats (M113 — added prose can give
      an existing assert false coverage) and the M104 adjacency check over every guard
      literal near the edited prose.
- [ ] T5: Append D-067. It records the two adoptions, the D-059-shaped retirement, and
      why D-064–D-066 are reserved rather than taken: they are appended on M114's
      unmerged branch and nothing checks D-id uniqueness.
- [ ] T6: Spawn the fresh-context certifier over this milestone's own guards; record its
      verdict and every discrepancy verbatim; re-certify after any rewrite; enter the
      gate only at zero unresolved.
- [ ] T7: Final gate — measure assert/entry parity, run the blanking sweep, replay every
      new probe red-side-up on a verified-green scratch baseline, run the three suites
      from the repo root with exit codes captured separately, and `cairn_validate`.

## Work log

- 2026-07-26: created by /milestone-plan from M114's recorded unblock condition — adoption of RR06 recs 4-5 through their own milestone. Both were banked as candidate rows by RR06 BC8.
- 2026-07-26: `Driving RR` is deliberately `—`, not `RR06`. RR06's binding criteria bound M114; its BC8 banks recs 4-6 *outside* M114, so RR06 carries no criteria for this milestone and setting the slot would red `cairn_validate`'s `binding criteria` string-compare against a BC set that was never about this work.
- 2026-07-26: plan gate — four decisions. Scope is recs 4 and 5 only, the two the unblock condition names; rec 6 stays a candidate, its promotion condition unfired. The criteria audit covers RR ingestion as well as the plan gate, because RB07's own trigger was two RR06 binding criteria that turned out jointly unsatisfiable and surfaced only at the review gate. M114 resumes after this merges rather than folding its leftovers in here. M114's park is mirrored onto `main`'s ROADMAP by this commit.
- 2026-07-26: verified at plan time rather than assumed — everything M114 produced is branch-only. `main`'s `DECISIONS.md` ends at D-063, `main`'s ROADMAP still shows M114 `planned`, and `guard-doctrine.md` §3/§7, the thrash rule, the falsifying-promotion-condition rule and RB05-07/RR05-07 are all absent from `main`. So this milestone may cite none of them as existing doctrine, and its new guard-doctrine section is appended after `main`'s current last section rather than beside M114's edits.
- 2026-07-26: criteria re-read against the artifacts at the user's call, standing in for the plan-gate audit M115 itself builds. Four checks clean and MEASURED, not assumed: all three cited line anchors are exact on `main`; `main`'s `guard-doctrine.md` ends at §7, so T3's new section is §8 and misses M114's in-section edits; `cairn_validate` has no D-id contiguity check, so the D-064→D-067 gap is legal and IP4 forbids reuse, not gaps. Two defects found and amended before implement: AC2 and AC6 cited RR06, which does not exist on `main` (only RB01-04/RR01-04 do), and AC6's tolerance rested on `grep -c`, which prints 0 but EXITS 1 — the M111 `;`-chain lesson in a different costume. AC2 now states it carries the falsifier inline as the implementer's referent; AC6 reads the printed count and names RR06 as unmerged. Caveat recorded honestly: I authored these criteria, so this is the weaker self-check rec 4 exists to replace.
- 2026-07-26: AC3's "every new doctrine clause" is knowingly the softest criterion — `clause` is undefined and the coverage call is judgment. Kept rather than tightened: it is bounded to prose this milestone authors (unlike M114's AC2 `repo-wide`, which was unsatisfiable), its tolerance is the measurable assert-count == entry-count, and the judgment residue is exactly what AC5's certifier is there to check. The interlock is deliberate, not an oversight.
- 2026-07-26: branch `m115-fresh-context-reader-instruments` cut from main (0/0 with origin, clean tree); status -> in-progress.
- 2026-07-26: implement gate — three choices. The criteria audit runs at step 3 over the FINAL acceptance-criteria wording, which moves criteria authoring from step 4 up into step 2: auditing a draft that step 4 then rewrites is the certify-your-model-of-the-artifact failure RR06 diagnosed, reproduced inside the fix for it. Both readers are [O] — RR06 rec 9 rules out mechanizing a judgment about prose meaning, so a weaker reader is the same bet at a discount. Audit findings with one clear answer are fixed and reported; judgment calls become gate questions within the three-marker cap.
- 2026-07-26: file placement chosen to minimize M114's rebase conflict — a new guard file rather than `skills/tests/test_lesson_graduation.py` (M114 edits it heavily), and an appended guard-doctrine section rather than edits inside §3/§7. `test_mutation_harness.py` is unavoidable; registration is mandatory and the conflict there is additive.

- 2026-07-26: T1 — the criteria audit lands at both surfaces. `/milestone-plan` step 3 gains a `Criteria audit` block running BEFORE the questions are composed, and step 2 now requires the criteria be drafted to final wording, with step 4 writing the audited bytes and re-auditing anything the gate changed — three edits, because placing the audit without moving criteria authoring would have audited a draft that step 4 rewrites. `/milestone-brief`'s RR ingestion gains the same reader and the same two questions, asked of the SET as well as each criterion, since jointly-unsatisfiable criteria are what the ingest audit exists to catch. RR06 is deliberately not cited in the shipped prose: only RR01 and RR04 are cited anywhere under `skills/`, and both are archived on `main` while RR06 is not, so its rule travels in full instead of behind a pointer that resolves to nothing.
- 2026-07-26: T1 sweeps, MEASURED against the asserts and not by eye. M112 surface sweep: `README.md`'s plan row and `DESIGN.md:127` are category summaries that this does not falsify, and no template restates the plan gate — nothing outside the two skill files to update. M113 false-coverage sweep: two guards do read the edited files (`test_bounded_decisions_read.py:106` and `test_gate_conclusion_preview.py:72,93`), so I read their asserted strings rather than grepping the file — none of the five phrases they pin occurs in the new prose. M104 adjacency: all three suites green after the edit, which is the check (a reflowed anchor reds its own guard).

- 2026-07-26: T2 — `skills/tests/test_fresh_context_readers.py` pins T1's doctrine with 14 asserts, one per clause that carries the rule independently: the audit's placement at step 2/3/4, its fresh-context reader, each of its two questions, each disposition arm, the anti-mechanization line, and the four ingest-side clauses. Mechanism confirmed FIRST, not assumed — the completeness meta-test redded on the unregistered file before I registered anything. Every block was copied from the shipped bytes and machine-checked to resolve exactly 1x in its target before insertion (14/14); every wrapped phrase is matched with `\s+` rather than a literal newline (M105), and the file reads targets with `Path.read_text` so the mutation engine can see it (M100). Parity MEASURED by AST, not counted by eye: 14 doctrine-pinning asserts against 14 registered entries. The harness's blanking sweep passes, so all 14 red on deletion. Suites 624/280/91 exit 0 each, skills up exactly the 14 new methods; `cairn_validate` exit 0.

## Decisions

## Review
