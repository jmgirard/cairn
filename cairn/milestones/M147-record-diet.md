# M147: The records shrink to their jobs

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** M146
- **Driving RR:** —
- **Principles touched:** GP1, IP4
- **Branch/PR:** m147-record-diet

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

- [ ] AC1: Every lesson entry of `cairn/LESSONS.md` at the pre-milestone
      default-branch commit is dispositioned in the ledger — kept, trimmed
      to its uncovered remainder, or retired under a named D-051/D-055
      ground or the RR13-reduction ground — and the shipped file contains
      exactly the kept and trimmed entries, each a single
      `- YYYY-MM-DD (M<NN>):` line stating one lesson or one consolidated
      family with its members named.
- [ ] AC2: Every candidate row of `cairn/ROADMAP.md` at the pre-milestone
      default-branch commit is dispositioned in the same ledger — rewritten,
      merged, or dropped — and each surviving row states the idea, why it is
      parked, its promotion condition, and its added-date/source, plus any
      search-first cross-reference, and nothing else; no surviving row names
      a retired artifact, verified by re-running M146's AC2/AC4 greps
      without their ROADMAP/LESSONS exclusions.
- [ ] AC3: `cairn_validate` exits 0 (item caps hold after the rewrite).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3

## Tasks

- [x] T1: Ledger and rewrite `cairn/LESSONS.md` (32 lesson entries at
      today's tree; grounds named per entry).
- [x] T2: Ledger and rewrite the ROADMAP candidate rows; execute the five
      gate-approved drops; re-run M146's greps over ROADMAP/LESSONS.
- [ ] T3: Run `cairn_validate`; confirm exit 0; commit ledger + rewrites
      together.

## Ledger

Baseline: default-branch commit `f767109` (branch point). LESSONS.md lesson
lines 18–49 keyed L01–L32 in file order; ROADMAP.md candidate rows keyed
R01–R27 in file order. Grounds: D-051 (enforcement/ownership), D-055
(maturation), RR13-reduction (rec 8: guard-craft families retire into the
git-archived doctrine — guard-doctrine.md deleted at M146, the prose-guard
suite gating nothing per D-109).

**Lessons:**

- L01 (M56+M65 verification width): trimmed — consolidated family line; the suite-command specifics owned by PROFILE `verify`; M111's `;`-chain half (L12) and M124's finally-restore (L27) folded in as members.
- L02 (M71 hook matching/shipping): trimmed — dispatch detail cross-referenced to `references/claude-code-hooks.md`; the four shipping surfaces kept.
- L03 (M72 merge-guard direction): kept.
- L04 (M73 gh GraphQL/REST): kept.
- L05 (M81/M91 derived-page aging): kept.
- L06 (M90 replace_all indentation): trimmed — the prove-guard-reddens-per-input half retired, RR13-reduction (prose-guard craft).
- L07 (M99 fixed-point figures): retired — ownership: the tracking-rules derived-figures rule owns the remedy (the line itself records the graduation); case history in archive + git.
- L08 (M99 rewrite drops disposal): kept.
- L09 (M95 anchor-authoring craft): retired — RR13-reduction/maturation (guard-craft family).
- L10 (M95 inversion-sweep craft): retired — RR13-reduction/maturation (guard-craft family).
- L11 (M100 fail loud, never open): trimmed — checker craft kept to one line.
- L12 (M104 adjacent-guard reflow): retired — RR13-reduction: the hazard is the gating prose-guard suite, which gates nothing (D-109).
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
- L24 (M118 definitional line elsewhere): retired — RR13-reduction: certification-sweep craft; its bounded-promise half already graduated (M130).
- L25 (M117 mutation-registry family): retired — RR13-reduction/maturation: the flagship guard-craft family.
- L26 (M119 near-miss controls): retired — RR13-reduction: detector-control craft for a retired instrument class.
- L27 (M124 finally-restore): trimmed — absorbed into L01's family line (member named there).
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
- R08 (frame membership rule): dropped — moot: the always-read governance frame was deleted at M146 (`always-read` has zero hits in the reduced rulebook), so the membership question has no subject.
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

## Decisions

## Review
