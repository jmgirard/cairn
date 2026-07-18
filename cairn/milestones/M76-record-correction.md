<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M76: Record correction — history vs. current knowledge, and the correct-in-place protocol

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP4, GP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m76-record-correction` · https://github.com/jmgirard/cairn/pull/74   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give cairn a stated rule for correcting a durable record later proven false,
by splitting the tracking files into history (supersede, never edit) and
current knowledge (correctable in place, marked).

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a `tracking-rules.md` rule naming which records are history — DECISIONS,
work-logs, IDs, entombed `legacy/` files — and which are current knowledge —
`LESSONS.md`, `references/` pages, `DESIGN.md` — with the correction mechanism
for the latter: fix in place, mark the correction (`(M71, corrected M75)`),
git keeps the original. The `LESSONS.md` file-map row and the three other live
"append-only" labels for that file are corrected to match. D-045 records the
mechanism, the split, and the reading of IP4 that both rest on. The stale M71
matcher rule still sitting in `hooks/tests/test_hooks.py:912` and echoed at
`references/claude-code-hooks.md:105` is swept — the first instance the new
rule governs.

**Out:** amending IP4's DESIGN.md wording — the gate chose to record the
reading instead (IP4's history set never named LESSONS), so no IP text changes
and there is no remainder to home. A `cairn_validate` CHECK for correction
markers is **declined, not deferred** (rationale in D-045): advisory doctrine
has never been a validate gate (M33/M42/M49), so no candidate row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1 — `tracking-rules.md` carries a named rule for correcting a durable
      record proven false: it names the history set and the current-knowledge
      set explicitly, and states correct-in-place-with-a-marker as the
      mechanism for the latter.
- [x] AC2 — the file map's `cairn/LESSONS.md` row no longer calls the file
      append-only and names its actual write-mode instead.
- [x] AC3 — a repo-wide `git grep` finds no live file calling `LESSONS.md`
      append-only. Exempt from the sweep: history files (`cairn/DECISIONS.md`,
      `cairn/milestones/archive/`, `cairn/reviews/archive/`, `cairn/legacy/`),
      the `cairn/ROADMAP.md` candidate row that quotes the defect, this
      milestone file itself (M62 — the sweep hits the text it must write), and
      the guards' own absence-asserts under `skills/tests/` (M59 — an
      `assertNotIn` is a hit for the token whose absence it locks).
- [x] AC4 — `cairn/DECISIONS.md` carries D-045 recording the mechanism, the
      history/current-knowledge split, and the IP4 reading; `cairn/DESIGN.md`'s
      IP4 line is byte-identical to its pre-milestone text (`git diff` on that
      line is empty). (ip-touching: settled at the 2026-07-18 plan gate —
      the reading is recorded, IP4's wording is not amended.)
- [x] AC5 — `hooks/tests/test_hooks.py`'s matcher comment and
      `references/claude-code-hooks.md:105` both state the verified rule (a
      literal matcher is split on `|`/`,` and each alternative exact-matched);
      no live file claims a literal matcher is compared as one whole exact
      string.
- [x] AC6 — new guards lock AC1's rule **label-inclusively** (M74: the assert
      names the rule label, not only its clause, so a label swap fails), each
      is registered in `skills/tests/test_mutation_harness.py`, and the three
      suites are green: `python3 -m unittest discover -s scripts/tests`,
      `-s skills/tests`, `-s hooks/tests` (generic profile `verify`).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T2
- AC2 → T2
- AC3 → T2, T3
- AC4 → T1
- AC5 → T4
- AC6 → T5, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

Task detail compressed 2026-07-18 as a cap remedy (implement-owned minor
edit); full wording in git history and the per-task commit messages.

- [x] T1 — author D-045 (mechanism, split, IP4 reading, declined CHECK).
- [x] T2 — rulebook correction rule + `cairn/LESSONS.md` file-map row.
- [x] T3 — sweep every live "append-only" label for LESSONS, repo-wide.
- [x] T4 — sweep the stale M71 matcher rule from test + reference page.
- [x] T5 — label-inclusive guards + `Mutation(...)` entry per positive assert.
- [x] T6 — full verify: three suites, `cairn_validate`, caps.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

Reflowed 2026-07-18 to the rulebook's one-physical-line-per-entry format (cap remedy; substance unchanged, no entry removed — see the final entry).

- 2026-07-18: created by /milestone-plan; promotes the durable-record-correction candidate (M75 review G4/91 + G2/78); gate chose correct-in-place-marked, general history/knowledge split, record the IP4 reading without amending IP4, fold in the matcher sweep.
- 2026-07-18: branch `m76-record-correction` cut from main; status -> in-progress.
- 2026-07-18: minor amendment — T1 ticked as already satisfied; /milestone-plan commits its own D-entries, so D-045 landed in 9ac2311 at plan time and AC4's evidence reads the committed entry.
- 2026-07-18: T2 — "Correcting a record proven false" added to Universal tracking rules; LESSONS file-map row no longer says append-only; both label->rule mappings on single physical lines for the guards.
- 2026-07-18: T3 — minor amendment: repo-wide sweep found FOUR live LESSONS "append-only" labels, not the three planned; `skills/milestone-review/SKILL.md:189` was the extra; all four corrected (vindicates M48).
- 2026-07-18: T3 — documenting the rule inside `cairn/LESSONS.md` blew its own <50 cap (49 -> 51); compressed the header rather than prune real lessons for boilerplate; file back to 49.
- 2026-07-18: T4 — matcher rule corrected at `hooks/tests/test_hooks.py:912` and `references/claude-code-hooks.md:105` (marked `(corrected M76)`, the rule's first dogfooded application); `:121` left alone as a verbatim quote of Claude Code's own shipped warning.
- 2026-07-18: T5 — `TestRecordCorrectionRule` (6 asserts) + 5 mutation entries; skills 289 -> 295; falsifiability claimed proven by blanking plus a by-hand label swap (see the superseding entry below).
- 2026-07-18: T6 — all six tasks done; skills 295 / scripts 96 / hooks 72 exit 0, cairn_validate exit 0; `cairn/DESIGN.md` absent from the branch diff, so AC4's IP4-untouched bar holds at its strongest; status -> review.
- 2026-07-18: review trip 1 — gate FAILED on AC3 (exemption list omitted the guard's own `assertNotIn`, the M59 trap); AC1/AC2/AC4/AC5 passed fresh; consistency gate clean; status -> in-progress; draft PR #74 opened.
- 2026-07-18: supersedes the T5 entry — its "falsifiability proven twice" held only for the mechanism sentence; fan-out F1 proved a swap of the SET ENUMERATIONS left all six guards green. Superseded, not edited: a work log is history under D-045.
- 2026-07-18: AC3 amended at the implement step-6 gate (user-approved) — exemption list gains the guards' absence-asserts under `skills/tests/` (M59) and widens the milestone-file exemption to the whole file; rejected narrowing the grep, and dropping AC3.
- 2026-07-18: cap remedy — plan-owned body hit 151/150 once trip-1 evidence landed; compressed Tasks (implement-owned) rather than the work log, which D-045 classifies as history.
- 2026-07-18: review trip 2 — gate PASSED 6/6; fan-out: blame no findings, prior-PR no evidence (clean no-op), diff-bug 4 findings scored 88/42/55/32; F1 fixed (enumeration guards + 3 mutation entries, swap now fails), F2/F3 fixed on operator judgment despite sub-80 scores (M73), F4 rejected with reason; skills 295 -> 298.
- 2026-07-18: cap remedy #2 — body hit 158/150 and the heaviest section was the work log (58 lines), which D-045 classifies as history. Reflowed every entry to the one-physical-line format the rulebook already mandates rather than cutting content: no entry removed, no substance changed. The structural tension (an append-only work log counts against a plan-owned cap and grows every review trip) is real and goes to a candidate row, not to this milestone.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->

### Trip 1 — 2026-07-18 — gate FAILED on AC3

PR #74 (draft): https://github.com/jmgirard/cairn/pull/74

**Evidence gathered (all fresh, by command):**

- AC1 — PASS. `tracking-rules.md:121-130` carries "Correcting a record proven
  false"; names the history set (DECISIONS, work-logs, IDs, `legacy/`) and the
  current-knowledge set (LESSONS, `references/`, DESIGN); states the mechanism
  ("current knowledge is corrected in place, history is superseded and never
  edited") and rules out leaving wrong text readable.
- AC2 — PASS. File-map row `:23` reads "current knowledge, so a lesson proven
  false is corrected in place and marked (D-045)"; `grep -c append-only` on
  that row returns 0.
- AC3 — **FAIL.** The criterion's grep returns one hit outside its stated
  exemption list: `skills/tests/test_lessons_loop.py:100`
  (`self.assertNotIn("append-only", row.lower())`). The hit is the guard's own
  absence-assert, not a file calling LESSONS append-only, so the criterion's
  *substance* holds — but its exemption list is incomplete, and dismissing the
  hit at review would be reinterpreting the criterion. This is the M59 trap
  (an AC evidence grep over a directory containing the guard tests trips on
  the absence-assert), which M59 resolved by gated amendment. Planning defect:
  M59 was harvested at plan time and the exemption list still omitted it.
- AC4 — PASS. `cairn/DECISIONS.md` carries exactly one `### D-045`.
  `git diff main..HEAD -- cairn/DESIGN.md` is empty — DESIGN.md never opened,
  so IP4 is byte-identical at the strongest available bar.
- AC5 — PASS. `hooks/tests/test_hooks.py:911-918` and
  `references/claude-code-hooks.md:105` both state split-on-`|`/`,`-then-
  exact-match. `git grep "compared as an EXACT string\|plain string = exact"`
  returns nothing. `:121` retained deliberately — a verbatim quote of Claude
  Code's own shipped warning, accurate for the narrower `mcp__server` case.
- AC6 — PASS on substance, pending re-run after the amendment. skills 295 /
  scripts 96 / hooks 72, all exit 0; 5 `TestRecordCorrectionRule` mutation
  entries registered; `test_lessons_loop` 12 tests ok.

**Consistency gate:** `cairn_validate` exit 0, all 17 checks pass. Profile
`generic` names no toolchain checks — clean no-op. `cairn_impact` skipped
correctly: the header names IP4/GP2 as *touched*, but no principle *changed*.

**Disposition:** status -> in-progress for a gated AC3 amendment (implement
step 6). Fan-out not yet spawned — deferred to trip 2 so it reviews the final
diff.

### Trip 2 — 2026-07-18 — gate PASSED, 6/6

**Criterion evidence (fresh, by command, post-amendment):**

- AC1 — PASS. `tracking-rules.md:121-134`: rule named; history set
  (DECISIONS, work-logs, IDs, both archives, `legacy/`) and current-knowledge
  set (LESSONS, `references/`, DESIGN) each enumerated under its own label;
  mechanism + marker stated; IP/GP carve-out present.
- AC2 — PASS. File-map row `:23` names the write-mode; `grep -c append-only`
  on that row = 0.
- AC3 — PASS. Repo-wide sweep under the amended exemption list returns zero
  hits. The `skills/tests/` exemption verified to cover exactly one line
  (the guard's own `assertNotIn`), so it masks nothing real.
- AC4 — PASS. Exactly one `### D-045` in `cairn/DECISIONS.md`;
  `git diff main..HEAD -- cairn/DESIGN.md` empty — DESIGN.md never opened.
- AC5 — PASS. `test_hooks.py:911-918` + `claude-code-hooks.md:105` state
  split-then-exact-match; `git grep` for the whole-string claim returns
  nothing. Diff-bug lens independently confirmed fidelity to the
  authoritative dispatch bullet at `claude-code-hooks.md:102-113`.
- AC6 — PASS. skills 298 / scripts 96 / hooks 72, all exit 0; 8
  `TestRecordCorrectionRule` mutation entries. Falsifiability proven by
  mutation: the enumeration swap that previously left all guards green now
  exits 1 (2 failures + 2 errors).

**Consistency gate:** `cairn_validate` exit 0, 17/17. Profile `generic`
names no toolchain checks (clean no-op). `cairn_impact` skipped — IP4/GP2
are *touched*, no principle *changed*.

**Fan-out — 3 lenses + Sonnet scorer.** Blame-history: no findings; it
independently verified against D-032's text that IP4 names only work-logs and
DECISIONS, never LESSONS, so D-045's reading holds. Prior-PR-comments:
"no prior-PR evidence" (repo has zero inline PR comments) — clean no-op.
Diff-bug: 4 findings.

Actioned (>=80):
- **F1 (88) — FIXED.** Guards locked the rule's mechanism but not its
  enumerations; reviewer proved a set-swap and an outright deletion both left
  all 6 asserts green, leaving half of AC1 unguarded. Added 3 asserts pinning
  each label to its members on one physical line, + 3 mutation entries.
  Re-proved: the swap now fails.

Below threshold — logged, and two fixed anyway on operator judgment per the
M73 lesson (a sub-80 score gates the actioned list, not the operator):
- **F2 (42) — FIXED.** `DESIGN.md` classed as current knowledge with no
  carve-out would authorise editing an IP/GP line in place, bypassing the
  user-decision + D-entry gate at `:73-78`. Added the exception clause. Fixed
  despite the score because it authorises a governance bypass.
- **F3 (55) — FIXED.** History enumeration omitted `milestones/archive/` and
  `reviews/archive/`, which AC3's own exemption list treats as history — the
  rule was narrower than the criterion enforcing it. Both added.
- **F4 (32) — REJECTED, reason recorded.** The marker reads `(corrected M76)`
  rather than the prescribed `(M71, corrected M75)` shape. Blame shows the
  reference page's wrong line originated in **M07**, not M71, so naming an
  origin would have been wrong; omission is the defensible choice. No change.
