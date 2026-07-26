# M114: Review-loop escape hatches — thrash counted per milestone, falsifying promotion conditions, detector-precision guard doctrine

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP4, IP2
- **Branch/PR:** `m114-review-loop-escape-hatches` · https://github.com/jmgirard/cairn/pull/114

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

- [x] AC1: the rewritten thrash rule states all three of — returns counted per
      milestone with a re-cut incrementing and never resetting; the second trigger
      (one criterion, twice, new mechanism, same shape); and the no-recorded-alternative
      fallback offering `/milestone-brief`. Read out of the shipped file, not the draft.
- [ ] AC2: a new prose-guard file under `skills/tests/` fails when the rule block is
      blanked, carries one `Mutation(...)` entry per positive assert, and asserts the
      rule's phrases occur on exactly ONE surface across the plugin's live doctrine
      prose — `skills/**/*.md`, `README.md` and `CLAUDE.md` — matched
      whitespace-tolerantly, so a restatement reds even when it re-wraps (M105).
      `cairn/` is out of scope and the guard says so: `DECISIONS.md` legitimately
      quotes the rule it records and IP4 makes that permanent, so a literally
      repo-wide assertion is unsatisfiable and grows less satisfiable over time
      (M112, M113).
- [x] AC3: `tracking-rules.md` states the promotion-condition rule beside search-first
      candidate creation, guarded by an assert in `test_search_first_candidates.py`
      with its own `Mutation(...)` entry.
- [x] AC4: `guard-doctrine.md` §3 states the matcher-rendering rule and §7 the sweep
      non-vacuity rule, each guarded in `test_lesson_graduation.py` with its own
      `Mutation(...)` entry — registration is per block, and the completeness meta-test
      catches only an unregistered FILE (M60/M85).
- [x] AC5: a `DECISIONS.md` entry records the supersession, naming the per-cut reading
      it replaces and the M93/M92 evidence, and back-references the rule's prior form.
- [x] AC6: all three `unittest` suites green from the repo root with exit codes checked
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

- [x] T1: rewrite the thrash rule at `skills/milestone-review/SKILL.md:101-105` to the
      two-trigger, per-milestone-count form with the `/milestone-brief` fallback.
- [x] T2: author `skills/tests/test_thrash_rule.py` — anchors copied from the shipped
      file's actual bytes, never the draft (M95); `\s+` matchers where a phrase wraps
      (M105); read the target via `Path.read_text` or the engine cannot see it (M100).
      Register each positive assert in `test_mutation_harness.py` and prove each reds.
- [x] T3: add the promotion-condition rule to `tracking-rules.md` beside search-first;
      extend `test_search_first_candidates.py`; register and prove it reds.
- [x] T4: add the §3 matcher-rendering rule and the §7 sweep non-vacuity rule to
      `guard-doctrine.md`; extend `test_lesson_graduation.py`'s `TestModuleExists`;
      register both and prove each reds.
- [x] T5: write the D-entry; run the adjacency and double-occurrence sweeps over every
      edited file; run all three suites from the repo root, exit codes checked
      separately.

## Work log

- 2026-07-26: created by /milestone-plan from the /milestone audit's intraclass M93 post-mortem — 8 review passes and 3 plan re-cuts, of which passes 6-8 found no behaviour defect at all; M92 had 7 passes with the same signature ("1-6 each failed AC5 on prose authored about the work, never on the code").
- 2026-07-26: plan gate — three decisions. The thrash rule stays in `/milestone-review` (it has exactly one surface, and the rulebook is +83 lines / +7,401 chars over its M95 baseline with D-057 governing growth at the door). The promotion-condition rule goes in tracking-rules rather than the records-hygiene module, because candidate rows are created conversationally and a conditionally-read module would never fire on that path. The no-recorded-alternative case offers an RB escalation rather than collapsing into trigger (a); closing it upstream is a candidate row.
- 2026-07-26: verified at plan time rather than assumed — the thrash rule's phrases (`third trip`, `queue another retry`, `mis-planned`, `re-plan or split`) occur at exactly two lines repo-wide, both in `skills/milestone-review/SKILL.md`, and no file under `skills/tests/` asserts any of them, so the rule is unguarded prose today (M95: confirm an unpinned verdict against the guards, never against the prose).
- 2026-07-26: branch `m114-review-loop-escape-hatches` cut from main (0/0 with origin); status -> in-progress.
- 2026-07-26: T1 — the thrash rule is rewritten to count returns per milestone with a re-cut incrementing and never resetting, and split into two triggers: a third return (mis-planned, re-plan or split) and the same criterion failing twice by a new mechanism of the same shape (wrong approach — reconsider the alternative the plan gate recorded against, or offer `/milestone-brief` where none was recorded). All three suites exit 0 after the edit, which is also the M104 adjacency evidence: no neighbouring guard's anchor reflowed.
- 2026-07-26: T2 — `skills/tests/test_thrash_rule.py` adds 7 asserts over the rule's four properties plus a one-surface pin, each with its own `Mutation(...)` entry (7 registered; every block resolves 1x in the shipped file, including the one spanning the line break, matched with `\s+` per M105). Confirmed the mechanism first: the completeness meta-test redded on the unregistered file before I registered it. The one-surface pin sweeps `skills/**/*.md` plus `README.md` — the README is in scope because M112 found doctrine going stale exactly there — and was inversion-proved by hand: a forked copy appended to README reds it, restoring goes green, README byte-identical after.
- 2026-07-26: T3 — `tracking-rules.md` gains **Falsifying promotion conditions** directly after search-first candidate creation: a promotion condition names the class of evidence that would falsify the chosen approach, never a count of failures. Guarded in `test_search_first_candidates.py` with three registered entries, because the heading, the positive form and the prohibition fail independently — dropping only the prohibition leaves a rule a count still satisfies. The wrap is matched with `\s+`, not a literal newline. M113 sweep clean: every repeated phrase sits inside the new paragraph and no existing guard asserts one. Rulebook 862 -> 870 lines, 61,152 -> 61,631 chars (+8 / +479).
- 2026-07-26: T4 — `guard-doctrine.md` §3 gains the matcher-rendering rule (the positive signal proves the detector RAN, never that it would SEE its target; carry the renderings in as positive controls, which beats external mutation-verification because a detector's author is exactly who cannot enumerate what it misses) and §7 the silent-cell rule (assert a positive check count per cell, assert the positive case fired somewhere, and prefer the converse `named == usable`; a bare `assertGreaterEqual(checked, 0)` is named as the tautology). Four registered entries — diagnosis and remedy pinned separately, since a diagnosis with no remedy is what let the same sweep defect recur across three intraclass M93 passes. M113 sweep clean: `positive signal` now occurs 3x in the module but no guard asserts it.
- 2026-07-26: T5 — D-064 appended, recording all six plan-gate choices and naming the per-cut reading it supersedes; every intraclass ID qualified by repo, since a bare M<NN> in cairn's records is repo-local. AC6's two sweeps run as a baseline DIFF rather than an absolute count, which is what made them readable: M104 — 11 guard literals were already wrap-broken at main, 10 at HEAD, so 0 newly broken and the delta is my own new anchor matching for the first time; M113 — 12 guard-literal counts rose, 11 of them my own new asserts going 0->1, and the 12th (`universal`, 1->2, from the §7 rule's "universal silence") belongs to a guard reading cairn-init's SKILL.md, not guard-doctrine, which no guard-doctrine reader asserts. My first cut of the M104 sweep was itself mis-scoped — it swept README and LESSONS literals it never meant to — which is the §7 rule this milestone just wrote, hit while writing it.
- 2026-07-26: review pass 1 (in progress) — PR #114 opened as a draft; per-criterion evidence gathered and AC1, AC3, AC4, AC5, AC6 verified and ticked. AC2's tick withheld: the guard is sound (14/14 new blocks red on deletion, 0 survived) but the criterion's word `repo-wide` is unsatisfiable — the pinned phrase occurs in the skill AND in `cairn/DECISIONS.md`, because D-064 legitimately quotes the rule it records, and IP4 makes that history permanent. Consistency gate clean. Three review lenses still running; their findings join this pass before the verdict.
- 2026-07-26: review pass 1 FAILED the gate — AC2 alone, three ways: `repo-wide` is unsatisfiable as written (D-064 legitimately quotes the rule and IP4 makes that permanent), F1 (85) the one-surface pin is a rigid literal so a re-wrapped fork passes green, and F5 (85) the registry holds 7 entries against 9 positive asserts. AC2's tick withdrawn; AC1, AC3, AC4, AC5, AC6 verified this phase and stand. Two lenses clean; the shipped doctrine text is unimplicated and all 14 registered blocks red on deletion. First return — neither thrash trigger fires. Status -> in-progress.
- 2026-07-26: gated amendment — AC2's `repo-wide` clause is replaced by the three live-prose surfaces it can actually bound (`skills/**/*.md`, `README.md`, `CLAUDE.md`), plus an explicit whitespace-tolerance requirement and the stated reason `cairn/` is out (D-064 quotes the rule it records; IP4 makes that permanent). `CHANGELOG.md` stays out as a history file, the one thing guard-doctrine §7 lets an exclusion list name. AC1, AC3-AC6 wording untouched.
- 2026-07-26: F1/F2 fixed — the one-surface pin is now a `re.compile(r"per\s+milestone,\s+never\s+per\s+cut")` search instead of a literal `in`, and `surfaces()` yields `CLAUDE.md` beside `README.md`. Positive-controlled at every surface rather than argued: a fork appended in BOTH wrapped and one-line form reds `skills/milestone/SKILL.md`, `README.md` and `CLAUDE.md` (6/6) and correctly leaves `CHANGELOG.md`, `cairn/DESIGN.md` and `cairn/LESSONS.md` green (6/6) — 12/12, 0 mismatches, baseline green, every probe file byte-restored.
- 2026-07-26: F5 fixed — the two unregistered asserts now carry `Mutation(...)` entries; 9 positive asserts against 9 registered entries, and both new blocks proved to red on deletion. Gate on the final tree: three suites exit 0 separately (skills 620 / scripts 280 / hooks 91), `cairn_validate` exit 0, plan-owned body 98/149. Status -> review.

## Decisions

## Review

**Branch state.** `main` 0/0 with `origin/main`; branch 6 ahead / 0 behind. Draft PR
#114, head `6546db0`. This repo has no CI (PROFILE.md `consistency-gate`), so local
green is the gate.

**Fresh per-criterion evidence.** All commands run this phase.

- AC1 — **verified.** Read out of the shipped file, not the draft: per-milestone
  counting at `skills/milestone-review/SKILL.md:104`, the re-cut clause at `:105`,
  the second trigger at `:110-111`, its recorded-alternative remedy at `:113`, and the
  `/milestone-brief` fallback at `:114`. All three elements the criterion names are
  present.
- AC2 — **GATE FAILURE, and the criterion is what fails.** The guard is sound: the file
  exists with 7 asserts, carries 7 `Mutation(...)` entries, and I blanked each of the 14
  new blocks independently this phase and confirmed the named test reds — 14/14 red,
  0 survived. What fails is the criterion's word **repo-wide**. A literally repo-wide
  "exactly one surface" assertion FAILS right now: the phrase occurs in
  `skills/milestone-review/SKILL.md` and in `cairn/DECISIONS.md`, because D-064
  legitimately quotes the rule it records. `DECISIONS.md` is append-only history (IP4),
  so it will keep accumulating quotations of rules it decides on and the criterion can
  never be satisfied. The implementation (sweep `skills/**/*.md` + `README.md`, exclude
  `cairn/`) is the right behaviour; AC2 as written is unsatisfiable. Not reinterpreted
  charitably — returned for a gated amendment.
- AC3 — **verified.** Rule at `skills/shared/tracking-rules.md:352-358`, immediately
  after search-first candidate creation at `:343`. Guarded in
  `test_search_first_candidates.py`; 3 registered entries (heading, positive form,
  prohibition), each redding on deletion.
- AC4 — **verified.** §3 matcher-rendering rule at `skills/shared/guard-doctrine.md:96`
  (§3 opens `:76`); §7 silent-cell rule at `:221` (§7 opens `:214`). 4 registered
  entries, diagnosis and remedy pinned separately, each redding on deletion.
- AC5 — **verified.** D-064 present, 59 lines. Six content checks pass: names the
  per-cut reading it supersedes, cites intraclass M93 and intraclass M92, back-references
  the prior form's own phrases (`third trip`, `queue another retry`), names the
  supersession, and qualifies every cross-repo milestone id by repo.
- AC6 — **verified.** Three suites run from the repo root with exit codes captured
  separately, never piped: skills 620 / scripts 280 / hooks 91, exit 0 each. Both sweeps
  re-run this phase as a diff against `origin/main`, which is what makes them readable:
  M104 **0 newly wrap-broken**; M113 **12 guard-literal counts rose, 11 my own new
  asserts (0->1)**, and the 12th (`universal`, 1->2) belongs to
  `test_toolchain_profiles.TestGreenfieldInitFlow`, whose `setUp` reads
  `cairn-init/SKILL.md` — resolved by reading the class this phase, not from recall — so
  guard-doctrine's new "universal silence" cannot give it coverage.

**Consistency gate.** `cairn_validate` exit 0 — 16 PASS including `coverage complete`,
`weight caps`, `mirror agreement` and `binding criteria`; advisories only. `cairn_impact`
does not apply: no `DESIGN.md` principle changed (`git diff --name-only` on it is empty),
and the header's GP4/IP2 are principles the milestone works under, not ones it edits.
Profile `consistency-gate` slot is `generic` — none — a clean no-op.

**Thrash rule, applied to this milestone.** First return. Trigger (a) needs a third;
trigger (b) needs one criterion failing twice by a new mechanism of the same shape.
Neither fires, so this is an ordinary send-back and not a re-plan signal.

**Independent review — three lenses, then a scorer.** [O] diff-bug, [S] blame-history,
[S] prior-review, each with a distinct evidence base; findings scored by a fresh [S] that
did not generate them. Prior-review: zero findings (archive sweep found no regression;
the PR-comments probe returned empty, so no thread walk). Blame-history: no regression —
it re-derived the rulebook arithmetic (862 = 779 + 83 against M95's archive), confirmed no
prior D-entry mentions thrash, and confirmed `guard-doctrine.md` was untouched between its
M98 creation and this diff. Diff-bug: five findings.

- **F1 (85) — actioned.** `skills/tests/test_thrash_rule.py:92,101`. The one-surface pin
  matches `PHRASE` as a rigid literal substring, while every other assert in the file uses
  `\s+` across the shipped wrap and the docstring cites M105 for exactly that. A fork
  re-wrapped as `per milestone, never per\ncut` passes green; the same text on one line
  reds. These files wrap at ~75 cols and the phrase is 28 chars, so a genuine copy has a
  real chance of landing on the break — the guard misses the fork it exists to catch. This
  is the M105 lesson recurring inside the guard written to apply it.
- **F5 (85) — actioned.** `skills/tests/test_mutation_harness.py`. AC2 requires one
  `Mutation(...)` entry per positive assert; verified this phase — 9 positive asserts, 7
  entries. Unregistered: `recommend re-plan or split via ` + "`/milestone-plan`" + ` and
  `instance, never automatically`. Each occurs once in the target today so there is no
  false coverage yet, but neither is proven by the harness, so either gaining a second
  occurrence later turns its assert into false coverage with the suite silent. The T2
  work-log line ("7 asserts ... each with its own entry") miscounted asserts as methods.

**Logged, below the 80 threshold (5).** F2 (68) the sweep also omits `CLAUDE.md` and
`CHANGELOG.md`, not just `cairn/` as the docstring claims — the scorer judged `CHANGELOG`
defensible as history but `CLAUDE.md` a real live-file gap; carried into the AC2 amendment
below rather than dropped. F4 (60) the two triggers can co-fire on the motivating case
with no stated precedence, and "the same acceptance criterion" is undefined across a
re-cut that may renumber criteria. F7 (50) D-064's D-059 precedent is arguable — D-059
retired a built-and-measured mechanism, D-064 declines to build one. F6 (45) two comments
use a bare `M93` where the antecedent is `intraclass M93` lines above. F3 (30) the rewrite
drops the old `(count the work-log)` pointer; the scorer judged the surviving context
sufficient.

**Review incident, recorded.** The [O] lens appended a scratch copy of the thrash rule to
`CLAUDE.md` to test the sweep's scope, and my `git add -A` swept it into the pushed commit
`9f9f876`. The lens self-reported it. Fixed forward in `4f7e0dc` (no history rewrite on a
pushed branch); `CLAUDE.md` is now identical to `origin/main` and absent from the branch
diff. The rule I broke is tracking-rules' own: never sweep strangers into a checkpoint
commit. `git add -A` is unsafe while subagents are live in a shared checkout.

**GATE FAILURE — returned to `in-progress` (review pass 1).** AC2 alone, failing three
ways: its `repo-wide` wording is unsatisfiable (D-064 legitimately quotes the rule, and
IP4 makes that permanent), F1's rigid literal misses a re-wrapped fork, and F5's registry
is two entries short of what the criterion requires. **AC2's tick withheld**; AC1, AC3,
AC4, AC5 and AC6 were verified this phase with fresh evidence and stand. The shipped rules
themselves are unimplicated — all 14 registered blocks red on deletion, and no lens found
a defect in the doctrine text.

**Thrash rule, applied to itself.** First return for M114. Trigger (a) needs a third;
trigger (b) needs one criterion failing twice by a new mechanism of the same shape. Neither
fires — an ordinary send-back, not a re-plan signal.
