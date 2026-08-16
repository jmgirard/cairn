# M147: The records shrink to their jobs

- **Status:** review
- **Priority:** normal
- **Depends on:** M146
- **Driving RR:** —
- **Principles touched:** GP1, IP4
- **Branch/PR:** m147-record-diet · https://github.com/jmgirard/cairn/pull/148

## Goal

cairn's own always-read records shrink to their jobs — one lesson (or one
named family) per LESSONS line, idea/parking/promotion per candidate row —
against a committed per-entry disposition ledger (RR13 rec 8). Internal
tier: no external consumer of the repo relies on cairn's own LESSONS and
ROADMAP rows.

## Scope

**In:**
- A per-entry disposition ledger in this file over every LESSONS entry and
  every ROADMAP candidate row at the pre-milestone default-branch commit;
  the rewrite ships against it.
- The five machinery rows whose drop the 2026-08-16 plan gate approved —
  write-time stamp check, budget redistribution, re-pin Substantive bullet,
  partial-pin asserts, one-surface pin — dropped via the ledger with a
  one-line reason each; the archive summary points at the ledger.
- The retired-artifact name cleanup M146 deferred (guard-doctrine,
  DENSITY_FILES, cairn_budget mentions inside rows).

**Out:** no new caps, formats, or checking machinery of any kind — the
reduction just removed that class (D-108); ROADMAP milestone rows and
statuses untouched beyond normal hygiene; RR13 rec 9's post-reduction
re-measurement stays with the existing re-measurement candidate row.

## Acceptance criteria

- [x] AC1: Every lesson entry of `cairn/LESSONS.md` at the pre-milestone
      default-branch commit is dispositioned in the ledger — kept, trimmed
      to its uncovered remainder, or retired under a named D-051/D-055
      ground or the RR13-reduction ground — and the shipped file contains
      exactly the kept and trimmed entries, each a single
      `- YYYY-MM-DD (M<NN>):` line stating one lesson or one consolidated
      family with its members named.
- [x] AC2: Every candidate row of `cairn/ROADMAP.md` at the pre-milestone
      default-branch commit is dispositioned in the same ledger — rewritten,
      merged, or dropped — and each surviving row states the idea, why it is
      parked, its promotion condition, and its added-date/source, plus any
      search-first cross-reference, and nothing else; no surviving row names
      a retired artifact, verified by re-running M146's AC2/AC4 greps
      without their ROADMAP/LESSONS exclusions.
- [x] AC3: `cairn_validate` exits 0 (item caps hold after the rewrite).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3

## Tasks

- [x] T1: Ledger and rewrite `cairn/LESSONS.md` (32 lesson entries at
      today's tree; grounds named per entry).
- [x] T2: Ledger and rewrite the ROADMAP candidate rows; execute the five
      gate-approved drops; re-run M146's greps over ROADMAP/LESSONS.
- [x] T3: Run `cairn_validate`; confirm exit 0; commit ledger + rewrites
      together.

## Ledger

Baseline: default-branch commit `f767109` (branch point). LESSONS.md lesson
lines 18–49 keyed L01–L32 in file order; ROADMAP.md candidate rows keyed
R01–R27 in file order. Grounds: D-051 (enforcement/ownership), D-055
(maturation), RR13-reduction (rec 8: guard-craft families retire into the
git-archived doctrine — guard-doctrine.md deleted at M146, the prose-guard
suite gating nothing per D-109).

**Lessons:**

- L01 (M56+M65 verification width): trimmed — consolidated family line; the suite-command specifics owned by PROFILE `verify`; M111's `;`-chain half (L16) and M124's finally-restore (L27) folded in as members; the validate≠suites clause restored at review triage (F1: PROFILE never named the trigger surfaces, so it was unowned).
- L02 (M71 hook matching/shipping): trimmed — dispatch detail cross-referenced to `references/claude-code-hooks.md`; the four shipping surfaces kept.
- L03 (M72 merge-guard direction): kept.
- L04 (M73 gh GraphQL/REST): kept.
- L05 (M81/M91 derived-page aging): kept.
- L06 (M90 replace_all indentation): trimmed — the per-input redness clause restored at review triage (F6: it came from a gating behavior guard, not prose-guard craft; RR13-reduction did not reach it).
- L07 (M99 fixed-point figures): trimmed — restored as a one-liner at review triage (F2: the initially claimed ownership fails post-D-116 — the derived-figures rule binds code-adjacent artifacts and exempts tracking records, which L07's instances are).
- L08 (M99 rewrite drops disposal): kept.
- L09 (M95 anchor-authoring craft): retired — RR13-reduction/maturation (guard-craft family).
- L10 (M95 inversion-sweep craft): retired — RR13-reduction/maturation (guard-craft family).
- L11 (M100 fail loud, never open): trimmed — checker craft kept to one line.
- L12 (M104 adjacent-guard reflow): retired — RR13-reduction: the hazard's home suite gates nothing (D-109); noted at review triage (F7) that gating `scripts/tests` still hold prose-shaped asserts against shipped templates — that remainder is carried by L01's restored trigger-surface clause.
- L13 (M104 scope-word broadening): kept.
- L14 (M105 remote squash): kept.
- L15 (M109 SkipTest/fixture spy): kept.
- L16 (M111 retention prune): trimmed — its `;`-chain half folded into L01.
- L17 (M112 doctrine-wording surfaces): kept.
- L18 (M113 double floor): kept.
- L19 (M113 prose gives false coverage): retired — RR13-reduction: mutation-harness craft, non-gating family.
- L20 (M113/M122 layer agreement): kept (already its remainder).
- L21 (M115 dangling-id skip window): kept.
- L22 (M115 unmerged citation): kept.
- L23 (M114 facts not characterizations): kept.
- L24 (M118 definitional line elsewhere): retired — ownership: the kept M112 line (L17) owns doctrine-wording-surface craft; its bounded-promise half already graduated (M130); ground corrected at review triage (F8 — not certification-sweep craft).
- L25 (M117 mutation-registry family): retired — RR13-reduction/maturation: the flagship guard-craft family.
- L26 (M119 near-miss controls): retired — RR13-reduction: detector-control craft for a retired instrument class.
- L27 (M124 finally-restore): retired — RR13-reduction consolidation: absorbed into L01's family line, its content surviving as a named member; label corrected from "trimmed" at review triage (F4 — the separate entry leaves, so it is not among the shipped kept+trimmed lines).
- L28 (M127 whole-file deletion): kept.
- L29 (M131/M132 partial anchors): retired — RR13-reduction: prose-guard probe craft.
- L30 (M133 zsh `path`): kept.
- L31 (M134 test-coverage claims): retired — ownership: the derived-claims rule owns the docstring remedy (the line records the graduation); the work-log half is de-escalated (D-116).
- L32 (M146 AST recount): kept.

**Candidate rows** (dispositions: rewritten to the AC2 shape / merged / dropped):

- R01 (external adoption pass): rewritten.
- R02 (write-time stamp check): dropped — gate-approved 2026-08-16; D-115's fallback redirected by D-117.
- R03 (README flow diagram): rewritten.
- R04 (re-pin Substantive bullet): dropped — gate-approved: step-6 pin coverage was the retired prose-guard program's concern (D-108/D-109); analysis in git.
- R05 (amendment-time audit record): rewritten.
- R06 (record-defect re-measurement): rewritten; RR13 rec 9 added as source per this milestone's Out clause.
- R07 (standing-instrument adoption discipline): rewritten.
- R08 (frame membership rule): dropped — moot: the always-read governance frame was deleted at M146 (`always-read` has zero hits in the reduced rulebook), so the membership question has no subject; noted at review triage (F10) that DESIGN.md GP1 retains the phrase "always-read surface" — the row's specific subject (the rulebook's membership table and the audit sweep) is what no longer exists.
- R09 (rulebook "is never one line" overclaim): dropped — moot: M146's rewrite removed the sentence (`is never one line` has zero hits).
- R10 (reasoning-effort dial): rewritten.
- R11 (numeric spawn cap): rewritten.
- R12 (template drafting budgets): dropped — gate-approved; also moot: M146 deleted the budget preamble, so there is no block to redistribute.
- R13 (partial-pin asserts): dropped — gate-approved: prose-guard pin quality gates nothing (D-109); analysis in git.
- R14 (one-surface pin): dropped — gate-approved: doctrine-fork detection was the retired program's concern (D-108); analysis in git.
- R15 (/explore-sources skill): rewritten.
- R16 (citekey resolution): rewritten.
- R17 (concurrent-operator hardening): rewritten.
- R18 (BC-aware coverage message): rewritten.
- R19 (content-gated memory guard): rewritten.
- R20 (contributor-facing scaffold): rewritten.
- R21 (branch-protection compatibility): rewritten.
- R22 (scaffold-spec version stamp): rewritten.
- R23 (phase-gated doctrine loading): rewritten.
- R24 (action-graded finding vocabulary): rewritten.
- R25 (streamlining pass): rewritten.
- R26 (deferred hook-nudge tier): rewritten.
- R27 (stakes-tier follow-through): rewritten.

## Work log

- 2026-08-16: created by /milestone-plan (RR13 step 2, gate round 1).
- 2026-08-16: criteria audit ran ([O] fresh reader): AC1 gained the consolidated-family form and the RR13-reduction retirement ground (a strict one-lesson-per-line split would breach the 50-line cap); AC2 gained the search-first cross-reference allowance; the completeness-claiming drop criterion was demoted to ledger dispositions with the reasons in this file, not the capped archive summary; AC3 tightened to exit 0.
- 2026-08-16: plan gate approved the five machinery-row drops via the ledger rather than a completeness-claiming criterion; falsified by a dropped row's subject resurfacing as needed work.
- 2026-08-16: M146 review note — the In-scope row-drop list intersects D-115's Consequences: the write-time-stamp-check row is D-115's named remedy path, so dropping it requires a superseding clause in the same milestone or sparing (and correcting) the row; that row's premise and blocker analysis also name machinery M146 retired, and LESSONS.md line 18 cites the deleted test_cairn_budget — both are this milestone's cleanup ground (M146 review findings O2/O5/O8).
- 2026-08-16: pre-implementation gate — user approved dropping the write-time-stamp-check row WITH a superseding D-entry redirecting D-115's fallback (over sparing the row).
- 2026-08-16: T1 — LESSONS ledgered at f767109 (32 entries: 16 kept, 5 trimmed, 11 retired — 9 RR13-reduction/maturation, 2 ownership) and rewritten 49→38 lines; suites 308+103 green, validate exit 0.
- 2026-08-16: T2 — 27 candidate rows ledgered (20 rewritten to the AC2 shape, 7 dropped: the 5 gate-approved plus R08/R09 moot, their subjects deleted at M146); D-117 appended redirecting D-115's fallback; M146's AC2/AC4 greps re-run without ROADMAP/LESSONS exclusions — zero hits, positive control 30 hits on DECISIONS.md; ROADMAP 54→45 lines; suites 308+103 green, validate exit 0.
- 2026-08-16: T3 — final run at tip: validate exit 0, suites 308+103 green; status → review.
- 2026-08-16: correction — the T2 line's "ROADMAP 54→45" baseline figure is wrong: the baseline at f767109 is 53 lines (F13).
- 2026-08-16: review triage — 14 findings from the [O] lens: 12 fixed at the gate, 1 rejected with reason (F10), 1 noted deliberate (F14); LESSONS regains L07 and two clauses (22 entries, 39 lines); five ROADMAP rows gain explicit parked-clauses; six ledger grounds corrected in place.

## Decisions

## Review

- 2026-08-16 AC1: baseline `git show f767109:cairn/LESSONS.md` counts 32 lesson entries; ledger dispositions 32 (L01–L32); shipped file has 21 entries = 16 kept + 5 trimmed, zero lines failing the `- YYYY-MM-DD (M<NN>):` shape, zero continuation lines after the preamble. PASS.
- 2026-08-16 AC2: baseline candidate rows 27; ledger dispositions 27 (R01–R27); shipped rows 20, each with an added-date/source and a promotion condition (20/20 on both greps); M146's AC2/AC4 greps re-run without ROADMAP/LESSONS exclusions — zero hits each, positive control 30 hits on DECISIONS.md. PASS.
- 2026-08-16 AC3: `cairn_validate` (plugin copy) exit 0, all checks OK. PASS.
- Projection-vs-outcome: Driving RR is `—` — no numeric projections; clean no-op.
- 2026-08-16 fresh-context review, single [O] diff-bug lens (internal tier, markdown-only diff per D-112): 14 ranked findings. Dispositions — F1 fixed (L01's validate≠suites clause restored; PROFILE never owned the trigger surfaces); F2 fixed (L07 restored as a trimmed one-liner; claimed ownership fails post-D-116); F3 fixed (R06 regains the 08bbb07 baseline locator; the D-099/D-116 claim narrowed to the supersede exits); F4 fixed (L27 ledger label trimmed→retired-by-consolidation; shipped file already correct under AC1's consolidated-family clause); F5 fixed (R06 "never on felt cost" and R07 "never on a count of milestones" restored); F6 fixed (L06's per-input redness clause restored); F7 fixed (L12 ground annotated; remainder carried by L01's restored clause); F8 fixed (L24 ground corrected to ownership via L17); F9 fixed (explicit parked-clauses added to R05/R06/R19/R24/R27; AC2 evidence re-recorded over all four elements); F10 rejected — the drop stands, ledger annotated (GP1 retains the phrase; the row's subject — the rulebook's membership table and audit sweep — is gone); F11 fixed (L02 count-words, R21 two-way decision, R22 changelog, R16 archive pointer restored); F12 fixed (R11 "pinned" → "held … hand-run since D-109"); F13 fixed (work-log correction line: ROADMAP baseline 53, not 54); F14 noted, deliberate — per-row sweep clauses live in git, AC2 permits.
- 2026-08-16 AC1 re-run post-triage: ledger 32 dispositions (16 kept, 6 trimmed, 10 retired); shipped file 22 entries = 16 kept + 6 trimmed, zero format violations, zero continuation lines. PASS.
- 2026-08-16 AC2 re-run post-triage: 27 dispositions (20 rewritten, 7 dropped); 20 shipped rows, all four elements verified per row — idea and promotion condition present 20/20 by grep, parking reason present 20/20 (a stated blocker, a "parked" clause, or the unfired trigger named in the row), source/date 20/20; both retired-artifact greps zero hits, positive control 30 hits. PASS.
- 2026-08-16 AC3 re-run post-triage: `cairn_validate` exit 0; suites 308+103 green. PASS.
