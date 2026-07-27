# M114: Review-loop escape hatches — thrash counted per milestone, falsifying promotion conditions, detector-precision guard doctrine

- **Status:** blocked
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP4, IP2
- **Branch/PR:** —

## Goal

Close the three gaps the intraclass M93 post-mortem exposed — a thrash rule that
resets on a re-cut and counts trips rather than recurrences, a candidate promotion
condition that may be written as a failure count, and a guard doctrine with no rule
about whether a detector can see its target.

## Scope

**In:** the thrash rule at `skills/milestone-review/SKILL.md:101-105` rewritten to
count returns per milestone (a `/milestone-plan` re-cut increments, never resets) with
two triggers — a third return, and the same acceptance criterion failing twice by a new
mechanism of the same shape — the second remedied by reconsidering the alternative the
plan gate recorded, or, where none was recorded, by an offered `/milestone-brief`
escalation · a new prose-guard over that rule, registered in the mutation harness,
pinning also that the rule has exactly one surface · one rule in
`skills/shared/tracking-rules.md` beside search-first candidate creation: a promotion
condition names the class of evidence that would falsify the chosen approach, never a
count of failures · two additions to `skills/shared/guard-doctrine.md` — §3 on
exercising a detector's matcher at every rendering its target can take, §7 on sweep
non-vacuity — each guarded and registered · a D-entry superseding the counting rule.

**Out:** any `cairn_validate` check or advisory for the three rules — the counting half
is mechanical but inert and the shape-recurrence half is a judgment; precedent is D-059
retiring an advisory measured not to work → stays prose doctrine, revisited only on
evidence the prose fails · changes to the `/milestone-review` fan-out, which caught
every M93 failure before merge → no milestone; it is working · size or cost governance,
closed by D-057 · an obligation on `/milestone-plan` to always record the rejected
alternative → ROADMAP candidate row · editing intraclass's own candidate rows to comply,
which is that repo's file to change, not cairn's → nothing here.

## Acceptance criteria

- [ ] AC1: the rewritten thrash rule states all three of — returns counted per
      milestone with a re-cut incrementing and never resetting; the second trigger
      (one criterion, twice, new mechanism, same shape); and the no-recorded-alternative
      fallback offering `/milestone-brief`. Read out of the shipped file, not the draft.
- [ ] AC2: a new prose-guard file under `skills/tests/` fails when the rule block is
      blanked, carries one `Mutation(...)` entry per positive assert, and asserts the
      rule's phrases occur on exactly ONE surface repo-wide — so a later restatement
      reds rather than silently forking the rule (M112, M113).
- [ ] AC3: `tracking-rules.md` states the promotion-condition rule beside search-first
      candidate creation, guarded by an assert in `test_search_first_candidates.py`
      with its own `Mutation(...)` entry.
- [ ] AC4: `guard-doctrine.md` §3 states the matcher-rendering rule and §7 the sweep
      non-vacuity rule, each guarded in `test_lesson_graduation.py` with its own
      `Mutation(...)` entry — registration is per block, and the completeness meta-test
      catches only an unregistered FILE (M60/M85).
- [ ] AC5: a `DECISIONS.md` entry records the supersession, naming the per-cut reading
      it replaces and the M93/M92 evidence, and back-references the rule's prior form.
- [ ] AC6: all three `unittest` suites green from the repo root with exit codes checked
      individually, never through a pipe (M56/M65, M111); and an adjacency sweep shows
      every guard asserting a phrase near an edited block still matches on one physical
      line (M104), and no phrase this milestone adds gives an existing guard false
      coverage by occurring twice (M113).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T5

## Tasks

- [ ] T1: rewrite the thrash rule at `skills/milestone-review/SKILL.md:101-105` to the
      two-trigger, per-milestone-count form with the `/milestone-brief` fallback.
- [ ] T2: author `skills/tests/test_thrash_rule.py` — anchors copied from the shipped
      file's actual bytes, never the draft (M95); `\s+` matchers where a phrase wraps
      (M105); read the target via `Path.read_text` or the engine cannot see it (M100).
      Register each positive assert in `test_mutation_harness.py` and prove each reds.
- [ ] T3: add the promotion-condition rule to `tracking-rules.md` beside search-first;
      extend `test_search_first_candidates.py`; register and prove it reds.
- [ ] T4: add the §3 matcher-rendering rule and the §7 sweep non-vacuity rule to
      `guard-doctrine.md`; extend `test_lesson_graduation.py`'s `TestModuleExists`;
      register both and prove each reds.
- [ ] T5: write the D-entry; run the adjacency and double-occurrence sweeps over every
      edited file; run all three suites from the repo root, exit codes checked
      separately.

## Work log

- 2026-07-26: created by /milestone-plan from the /milestone audit's intraclass M93 post-mortem — 8 review passes and 3 plan re-cuts, of which passes 6-8 found no behaviour defect at all; M92 had 7 passes with the same signature ("1-6 each failed AC5 on prose authored about the work, never on the code").
- 2026-07-26: plan gate — three decisions. The thrash rule stays in `/milestone-review` (it has exactly one surface, and the rulebook is +83 lines / +7,401 chars over its M95 baseline with D-057 governing growth at the door). The promotion-condition rule goes in tracking-rules rather than the records-hygiene module, because candidate rows are created conversationally and a conditionally-read module would never fire on that path. The no-recorded-alternative case offers an RB escalation rather than collapsing into trigger (a); closing it upstream is a candidate row.
- 2026-07-26: verified at plan time rather than assumed — the thrash rule's phrases (`third trip`, `queue another retry`, `mis-planned`, `re-plan or split`) occur at exactly two lines repo-wide, both in `skills/milestone-review/SKILL.md`, and no file under `skills/tests/` asserts any of them, so the rule is unguarded prose today (M95: confirm an unpinned verdict against the guards, never against the prose).
- 2026-07-26: STATUS MIRROR, written on `main` at M115's plan gate. M114 ran seven review passes on branch `m114-review-loop-escape-hatches` (draft PR #114) and was parked `blocked` at the maintainer's call when its own AC7 terminus fired; the full record lives on that branch. Blocker: the recorded unblock condition is adoption of RR06 recs 4-5, which is M115. Written here because `main` carried `planned` for a milestone nobody could work on. The branch's work log is authoritative and supersedes this line at rebase.

## Decisions

## Review
