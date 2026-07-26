# M114: Review-loop escape hatches — thrash counted per milestone, falsifying promotion conditions, detector-precision guard doctrine

- **Status:** in-progress
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

**In:** the thrash rule at `skills/milestone-review/SKILL.md` — returns counted per
milestone (a `/milestone-plan` re-cut increments, never resets, and the rule names the
work log as the record that survives a re-cut), two triggers, the second remedied by
reconsidering the plan gate's recorded alternative or an offered `/milestone-brief`
escalation, and **trigger (a) taking precedence when both fire** · one rule in
`skills/shared/tracking-rules.md` beside search-first candidate creation: a promotion
condition names the class of evidence that would falsify the chosen approach, never a
count of failures · two additions to `skills/shared/guard-doctrine.md` — §3 on exercising
a detector's matcher at every rendering its target can take, §7 on sweep non-vacuity ·
a prose-guard over the thrash rule, one `Mutation(...)` entry per doctrine-pinning
assert · D-064.

**Out:** **the one-surface pin** — asserting the rule's phrase occurs on exactly one file.
Re-cut out at the third return (2026-07-26): it consumed all three returns across six
findings of one shape, while the five other criteria never failed. Detecting a forked
rule by searching for its phrase requires enumerating every rendering the phrase can take,
and three attempts each missed one the next review found → ROADMAP candidate row, which
records the renderings already known so a later attempt does not restart · any
`cairn_validate` check for the three rules — the counting half is inert and the
shape-recurrence half is a judgment (D-059 precedent) · changes to the
`/milestone-review` fan-out, which caught every failure here → it is working · size or
cost governance, closed by D-057 · an obligation on `/milestone-plan` to record the
rejected alternative → candidate row.

## Acceptance criteria

<!-- Re-cut 2026-07-26 at the third return. AC2's one-surface clause is deleted with the
     pin; AC1 gains the precedence and work-log-pointer elements (review F4, F3). Every
     box unticked — the tree changes, so each criterion re-verifies from scratch. -->

- [ ] AC1: the thrash rule states all five of — returns counted per milestone with a
      re-cut incrementing and never resetting; the work log named as the record that
      survives a re-cut; the second trigger (one criterion, twice, new mechanism, same
      shape); the no-recorded-alternative fallback offering `/milestone-brief`; and that
      trigger (a) takes precedence where both fire. Read out of the shipped file.
- [ ] AC2: a prose-guard file under `skills/tests/` fails when the rule block is blanked,
      and carries one `Mutation(...)` entry per positive assert that pins doctrine prose.
      No claim about how many files state the rule — that is the pin, now Out.
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
      individually, never through a pipe (M56/M65, M111); an adjacency sweep shows every
      guard asserting a phrase near an edited block still matches on one physical line
      (M104); and no phrase this milestone adds gives an existing guard false coverage
      by occurring twice (M113).

## Coverage

- AC1 → T7
- AC2 → T6
- AC3 → T3
- AC4 → T4
- AC5 → T5
- AC6 → T8

## Tasks

<!-- T1-T5 shipped before the re-cut and stay on the branch; T6 reverts the part of T2
     that built the one-surface pin. T6-T8 are the re-cut's work. -->

- [x] T1: rewrite the thrash rule to the two-trigger, per-milestone-count form.
- [x] T2: author `skills/tests/test_thrash_rule.py` and register each doctrine-pinning
      assert in `test_mutation_harness.py`.
- [x] T3: add the promotion-condition rule to `tracking-rules.md`; extend
      `test_search_first_candidates.py`; register and prove it reds.
- [x] T4: add the §3 and §7 rules to `guard-doctrine.md`; extend
      `test_lesson_graduation.py`; register both and prove each reds.
- [x] T5: write D-064.
- [x] T6: delete the one-surface pin — `TestThrashRuleHasOneSurface`,
      `TestDetectorSeesEveryRendering`, `normalize()`, `states_the_rule()`, `RENDERINGS`,
      `NON_FORKS`, `PHRASE`, `surfaces()` — and its registry entry; verify the count goes
      9 → 8 rather than assuming it.
- [ ] T7: add the precedence clause and the work-log pointer to the thrash rule; extend
      the guard to pin both; register each and prove it reds.
- [ ] T8: candidate row for the pin, promotion condition naming a class of evidence and
      never a count (the rule this milestone ships); adjacency + false-coverage sweeps;
      three suites from the repo root, exit codes checked separately.

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
- 2026-07-26: review pass 2 FAILED the gate — AC2 again, and THRASH TRIGGER (b) FIRES on this milestone by its own rule. AC2 has failed twice, each by a new mechanism of one shape (the one-surface detector cannot see a rendering its target can take): pass 1 a line wrap (F1), pass 2 a blockquote continuation marker (G2, 83) and mid-phrase emphasis (G3, 80). Five findings scored >=80: G4 (90) the Review section cited a commit hash that does not exist — written from memory, corrected in place and marked; G7 (87) the registry comment says 'Six entries' against 9, wrong on arrival at 7; G1 (85) the matcher carries zero in-test positive controls, which is exactly what this milestone's own guard-doctrine §3 forbids; plus G2 and G3. G6 (68) and G5 (40) logged. AC1, AC3-AC6 re-verified this pass and stand; shipped doctrine untouched. Remedy per trigger (b): adopt the recorded alternative — §3's in-test positive controls — rather than widen the regex a third time. No brief escalation owed, since an alternative is on record. Status -> in-progress.
- 2026-07-26: gated amendment (pass 2) — AC2's mutation-entry clause is scoped to asserts that PIN DOCTRINE, because the §3 controls assert over the test's own synthetic strings and a mutation entry blanks a block in a target doctrine file, which is meaningless for a literal defined in the test; and "matched whitespace-tolerantly" becomes the §3 requirement that the matcher be exercised in-test against every rendering — pass 2 showed the whitespace framing was the too-narrow axis. AC1, AC3-AC6 untouched.
- 2026-07-26: G1/G2/G3 fixed STRUCTURALLY, per trigger (b)'s remedy — not a third regex guess. `normalize()` flattens the three axes a doctrine phrase renders along (wrap, blockquote continuation marker, emphasis) and `states_the_rule()` matches over it; the durable part is the in-test corpus, 11 RENDERINGS the detector must see and 8 NON_FORKS it must not, both routed through the same predicate the pin uses so a control cannot check something the pin does not.
- 2026-07-26: the negative controls immediately earned their keep by finding a defect the positives structurally could not — `states_the_rule` was a bare substring test, so `per milestone, never per cutover` read as a copy of the rule. Fixed with word boundaries. First mutation run had proved the NEGATIVES inert (normalization only deletes characters, so it can only turn a match into a non-match); re-run after the boundary fix, each control set now reds on a distinct defect class: dropping `\b` reds the negatives, dropping any normalization axis reds the positives.
- 2026-07-26: G4 fixed — the Review section's `4f7e0dc` corrected in place to `4c260fc` and marked (D-045: current knowledge corrected where it sits). G7 fixed — the registry comment no longer states an entry count at all, per §6's own remedy of letting the list be the count; it said "six" at seven entries and was staler at nine. G6 (logged) rode along: the docstring no longer claims a single `\s+` exception.
- 2026-07-26: gate on the final tree — three suites exit 0 separately (skills 622 / scripts 280 / hooks 91), all 9 registered blocks red on deletion, 9 doctrine-pinning asserts against 9 entries, `cairn_validate` exit 0, body 100/149. End-to-end in a scratch copy: the pass-1 wrap and both pass-2 renderings now red on every in-scope surface and stay green on every out-of-scope one, 30/30. Status -> review.
- 2026-07-26: review pass 3 FAILED the gate — AC2 a third time. H1 (95): the §3 controls have no non-vacuity assert, so emptying either corpus, or both plus gutting `normalize()`, leaves the suite green at 622 — the fix deletes silently. That is guard-doctrine §7, shipped by THIS milestone, unapplied to the §3 controls shipped beside it. H2 (85): the `.lower()` axis has no control and the pass-2 work-log claim that every axis reds the positives is false for it. H4 (82): the comment's 'normalization only deletes characters' invariant is contradicted by normalize()'s own purpose. H3 (75) and H5 (62) logged. AC1, AC3-AC6 re-verified and stand; doctrine untouched and unimplicated across all three passes. BOTH triggers now fire — (a) third return, (b) same shape a third time — the precedence collision pass-1 F4 predicted at 60 and nobody actioned. Following (a): re-plan or split, not another implement pass. Status -> in-progress.
- 2026-07-26: RE-CUT by /milestone-plan after the third return, following thrash trigger (a). Split at the line the evidence drew: the doctrine (thrash rule, promotion conditions, guard-doctrine §3/§7, D-064) has been byte-identical and unimplicated since pass 1 and stays; the ONE-SURFACE PIN goes Out to a candidate row, having consumed all three returns across six findings of one shape. Gate decision: fix F4 and F3 now rather than ship a rule whose own review documented a contradiction in it — trigger (a) takes precedence where both fire, and the rule names the work log as the record surviving a re-cut. That edits the one file three reviews cleared unchanged, so AC1 re-verifies from scratch; every AC box is unticked for the same reason. Candidate row records the renderings already known (wrap, blockquote, `>>` vs `> >`, partial emphasis, case, word boundaries, corpus vacuity) so a later attempt does not restart, and its promotion condition names a class of evidence rather than a count — the falsifying-promotion-condition rule this milestone ships, applied to its own leftovers.
- 2026-07-26: T6 — the one-surface pin and all its machinery are gone: `TestThrashRuleHasOneSurface`, `TestDetectorSeesEveryRendering`, `normalize()`, `states_the_rule()`, `RENDERINGS`, `NON_FORKS`, `PHRASE`, `surfaces()`, the now-dead `import re`, and the registry entry that pinned the assert. The docstring records what was removed and why, so the file does not read as though the pin was never considered. Count MEASURED rather than assumed, as the task required: 8 asserts against 8 registered entries. Suites 619/280/91, exit 0 each — skills is down 3 tests, exactly the three deleted.

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
`9f9f876`. The lens self-reported it. Fixed forward in `4c260fc` (hash corrected pass 2 — `4f7e0dc` never existed, G4) (no history rewrite on a
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

## Review pass 2 (2026-07-26)

**Scope of this pass.** `git diff 9f9f876..HEAD` on the shipped doctrine
(`milestone-review/SKILL.md`, `tracking-rules.md`, `guard-doctrine.md`,
`DECISIONS.md`) is EMPTY — byte-identical to what pass 1's three lenses cleared. The
delta is the two test files, the milestone file, and the `CLAUDE.md` revert. All six
criteria were still re-run from scratch rather than inherited, because the ticks on
AC1/AC3-AC6 were earned against the pre-fix tree.

**Fresh per-criterion evidence.** All commands run this phase.

- AC1 — re-verified. Per-milestone counting at `SKILL.md:104` (exactly 1 occurrence),
  re-cut clause `:105`, second trigger `:110-111`, recorded-alternative remedy `:113`,
  brief fallback `:114`.
- AC2 — **verified against the amended wording**, all four clauses.
  (a) All 9 registered blocks red on deletion — 9 redded, 0 survived.
  (b) 9 positive asserts : 9 `Mutation(...)` entries, pass-1 F5's shortfall closed.
  (c) Whitespace tolerance positive-controlled in a scratch copy of the repo, never by
  mutating it: 6 wrap positions (one-line, after `per`, after the comma, after `never`,
  before `cut`, indented continuation) x 8 files = **48 cases, 0 mismatches**. Every
  in-scope surface (`skills/**/*.md`, `README.md`, `CLAUDE.md`) reds at every wrap
  position; every out-of-scope file (`CHANGELOG.md`, `cairn/DESIGN.md`,
  `cairn/LESSONS.md`, `cairn/DECISIONS.md`) stays green. The pass-1 defect was exactly
  the wrapped case, so the controls are aimed where the guard was blind.
  (d) The guard states the `cairn/` exclusion and its IP4 reason in `surfaces()`.
- AC3 — re-verified. Rule at `tracking-rules.md:352-358`, prohibition clause at `:354`.
- AC4 — re-verified. §3 matcher-rendering rule at `guard-doctrine.md:96`; §7 silent-cell
  rule at `:221`.
- AC5 — re-verified. D-064 present, single heading.
- AC6 — re-verified. Three suites from the repo root, exit codes captured separately,
  never piped: skills 620 / scripts 280 / hooks 91, exit 0 each. Sweeps as a diff against
  `origin/main`: M104 **0 newly wrap-broken**; M113 **12 counts rose, 11 mine**, the
  12th (`universal`) again belonging to `test_toolchain_profiles`, which reads
  `cairn-init/SKILL.md` — same non-finding as pass 1, re-derived not recalled.

**Consistency gate.** `cairn_validate` exit 0, 16 PASS, advisories only. `cairn_impact`
N/A — `git diff --name-only origin/main..HEAD -- cairn/DESIGN.md` is empty, so no
principle changed. Profile `consistency-gate` is `generic` — none.

**Independent review — three lenses, then a scorer.** Prior-review: zero findings; it
verified each pass-1 fix discharged its finding and that F3/F4/F6/F7 are still recorded
(IP3). Blame-history: no regression; it confirmed the M103 identity property survives the
matcher swap, and raised the stale entry-count comment below. Diff-bug: six findings. All
three lenses left the tree clean this pass — the pass-1 contamination did not recur.

- **G4 (90) — actioned, fixed this pass.** The Review section cited commit `4f7e0dc` for
  the contamination revert; no such object exists (`git cat-file -t` fails). The real
  commit is `4c260fc`. I wrote the hash from memory instead of from command output —
  the exact failure guard-doctrine §6 names ("write evidence counts from command output,
  never memory"). Corrected in place and marked, per D-045.
- **G7 (87) — actioned.** `test_mutation_harness.py:2280` introduces the thrash block as
  "Six entries because the rule fails in six independent ways"; there are 9. It said
  "Six" when written against 7, so it was wrong on arrival and is wronger now — §6's
  "derived wrong, and restated stale", both halves, in this milestone's own comment.
- **G1 (85) — actioned.** `test_thrash_rule.py:97`. The matcher carries ZERO in-test
  positive controls. §3, added by THIS milestone, says to carry the renderings into the
  test because "the author of a detector is exactly who cannot enumerate the renderings
  it misses". The rendering coverage was done externally in a scratch copy and discarded,
  so nothing committed exercises `PATTERN` against any rendering; the registered mutation
  proves only that the guard reds on DELETION, never that it sees a copy APPEARING.
- **G2 (83) — actioned.** `\s+` does not cross a blockquote continuation marker: a fork
  rendered `> count returns per milestone,\n> never per cut` does not match, because the
  inter-token text is `,\n> ` and `>` is not whitespace. Blockquotes are how
  `milestone-review/SKILL.md` already hands doctrine to subagents (7 such lines there,
  1 in `tracking-rules.md`).
- **G3 (80) — actioned.** The matcher widened along the whitespace axis only, against §5's
  standing requirement to accept emphasis around a token it reads. A fork writing
  `**per milestone**, never **per cut**` passes green; the surface being swept carries 39
  bold runs and the shipped rule bolds this very phrase.

**Logged, below the 80 threshold (2).** G6 (68) the module docstring still says one assert
is `\s+`-tolerant "except the second trigger" when there are now two. G5 (40) the
`surfaces()` comment presents excluding `cairn/` as §7-sanctioned when §7 says an exclusion
list may name only history files and never a live directory — the scorer judged the
exclusion itself plan-approved by the AC2 amendment and already scrutinized at pass 1.

**GATE FAILURE — returned to `in-progress` (review pass 2).** AC2 again. AC1, AC3, AC4,
AC5 and AC6 were re-verified from scratch this pass and stand; the shipped doctrine prose
is untouched and unimplicated.

**THRASH TRIGGER (b) FIRES — on this milestone, by its own rule.** AC2 has now failed
twice, each time by a new mechanism of one shape: *the one-surface detector cannot see a
rendering its target can legitimately take* — pass 1 a line wrap (F1), pass 2 a blockquote
marker (G2) and mid-phrase emphasis (G3). The rule's own words apply verbatim: "Re-cutting
around the same predicate buys the next mechanism, not a fix." Widening the regex a third
time would buy the third. The remedy trigger (b) prescribes is to reconsider the
alternative recorded against the chosen approach — and G1 names it, in this milestone's
own shipped §3: carry the renderings INTO the test as positive controls, which is
"strictly stronger than external mutation-verification". No `/milestone-brief` escalation
is owed, because an alternative IS on record; the fallback exists only for when none is.
Second return, so trigger (a) has not fired.

## Review pass 3 (2026-07-26)

**Scope.** Shipped doctrine still byte-identical to pass 1 (`git diff 9f9f876..HEAD` on
the four doctrine files is empty). Delta since pass 2 is the reworked guard, its harness
comment, and tracking. All six criteria re-run from scratch again.

**Fresh per-criterion evidence.** All commands run this phase.

- AC1 — re-verified, all three elements present once each in the shipped file. (First
  evidence command returned 0 on element 1 because it was case-sensitive against a
  capitalised "Count"; re-run case-insensitively, as the guard itself matches, it is 1.
  Recorded because a miscounted evidence command is how a false negative enters a record.)
- AC2 — **verified against the twice-amended wording**, all three clauses.
  (1) All 9 registered blocks red on deletion — 9 redded, 0 survived.
  (2) 11 asserts, of which 2 assert over the test's own synthetic renderings and have no
  doctrine block to blank; 9 doctrine-pinning asserts against 9 entries.
  (3) The matcher is exercised in-test: 11 RENDERINGS it must see, 8 NON_FORKS it must
  not, both routed through `states_the_rule()` — the same predicate the pin uses, so a
  control cannot check something the pin does not. The three renderings review actually
  found (pass-1 wrap, pass-2 blockquote, pass-2 partial emphasis) are all seen; the
  boundary false positive the negative controls found (`per milestone, never per cutover`)
  is correctly not seen.
- AC3, AC4, AC5 — re-verified, each rule present once in its shipped file; D-064 single
  heading.
- AC6 — re-verified. Three suites from the repo root, exit codes separately: skills 622 /
  scripts 280 / hooks 91, exit 0 each. Sweeps against `origin/main`: M104 0 newly
  wrap-broken; M113 12 counts risen, 11 mine, the 12th `universal` again belonging to
  `test_toolchain_profiles`, which reads `cairn-init/SKILL.md`.

**Consistency gate.** `cairn_validate` exit 0, 16 PASS, advisories only. `cairn_impact`
N/A — no `DESIGN.md` principle changed. Profile `consistency-gate` `generic` — none.

**Thrash count.** Two returns so far. A failure this pass would be the third and would
fire trigger (a).

**Independent review — three lenses, then a scorer.** Prior-review and blame-history:
zero findings each; both independently confirmed the pass-2 rework did not regress the
pass-1 fix, and blame-history spot-checked this file's own historical claims against git.
Diff-bug: five findings, three scored >=80. All three lenses left the tree clean.

- **H1 (95) — the fix can be deleted with nothing redding.** `test_thrash_rule.py:184-200`.
  Both control tests are bare `for ... in DICT.items()` loops with no non-vacuity assert,
  so an empty corpus passes. Verified here against a `git archive` baseline (a partial
  scratch copy gives a RED baseline and makes every mutation look caught — my first
  attempt did exactly that and had to be redone): emptying `RENDERINGS` leaves the suite
  green at 622; emptying `NON_FORKS` leaves it green; emptying BOTH and gutting
  `normalize()` to `return text.lower()` still leaves it green. `subTest` does not change
  the test count, so a reviewer watching counts sees nothing either. This is precisely
  the shape **guard-doctrine §7, added by this milestone**, exists to prevent — the §3
  controls were written without applying the §7 rule shipped beside them, and the house
  pattern already exists in `test_mutation_harness.py` and `test_source_note_template.py`.
- **H2 (85) — a false claim in a durable record.** The `.lower()` axis of `normalize()`
  has no positive control: all 11 renderings spell the phrase lowercase, so dropping
  `.lower()` leaves the suite green. The pass-2 work-log line claiming "dropping any
  normalization axis reds the positives" is therefore false for that axis. A fork opening
  a sentence or heading with the phrase is caught today only by `.lower()`.
- **H4 (82) — a false invariant stated as evidence.** The comment at `:61-64`, repeated in
  the work log, claims normalization "only deletes characters and so can only ever turn a
  match INTO a non-match". Turning a non-match into a match is `normalize()`'s entire
  purpose: `states_the_rule` is False on a raw wrapped string and True after
  normalization. The real reason the positives could not find the boundary defect is that
  they only ever `assertTrue`.

**Logged, below threshold (2).** H3 (75) the nested-blockquote control covers `>>` but not
`> >`, the CommonMark spelling most editors emit — narrowed because no repo file uses
either form today. H5 (62) `PHRASE` is dead code introduced by this diff, an
un-synchronised fourth copy of the literal inside the guard whose thesis is one surface.

**GATE FAILURE — third return.** AC2 again; AC1, AC3, AC4, AC5, AC6 re-verified this pass
and stand, and the shipped doctrine prose remains byte-identical to what pass 1 cleared
and unimplicated in all three passes.

**BOTH THRASH TRIGGERS NOW FIRE, WITH DIFFERENT REMEDIES.** Trigger (a): third return, so
"do not queue another retry — recommend re-plan or split via `/milestone-plan`". Trigger
(b): AC2 has failed three times, each by a new mechanism of one shape (the detector or its
controls do not cover a case the target can take) — pass 1 a wrap, pass 2 a blockquote and
emphasis, pass 3 vacuity and case-folding. **This is exactly the collision pass-1 finding
F4 (60, logged, not actioned) predicted**, and the rule states no precedence between the
two. F4 was right and was under-scored. Following trigger (a), which is the stricter of
the two, this does NOT go back to `/milestone-implement`.
