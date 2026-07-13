<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M54: Release positioning + DESIGN refresh

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Principles touched:** IP1
- **Branch/PR:** m54-release-positioning-design-refresh · https://github.com/jmgirard/cairn/pull/52

## Goal

Bring cairn's outward positioning and DESIGN.md into line with the
language-agnostic architecture M45–M48 shipped, so the first files an external
adopter reads no longer say R-only and DESIGN audits clean (RR01 recs 1 + 5).

## Scope

**In:**
- Reframe the two externally-first-read surfaces — `.claude-plugin/plugin.json`
  description and `README.md` ¶1 — from R-exclusive to the profile-based
  framing already stated in DESIGN Purpose & Scope.
- Remove `cairn-init` §0's redundant "not an R package — adapt or abort"
  bullet; genericize `/hotfix` step 5's hardcoded `NEWS.md` (prose only).
- Refresh `cairn/DESIGN.md`: all 5 hooks listed, IP1 "main" → "the default
  branch", Known-issues rewritten to the honest single-author/single-OS list
  including the honor-system limitation.
- Fold in the same-family template drift: `claude-md-section.md` boundary rule
  gains `Lessons → LESSONS`.
- Lock the positioning framing + DESIGN 5-hook fact with a mutation-harness-
  registered guard test.

**Out:**
- LICENSE (MIT), README worked example, human-facing "what cairn does without
  asking" section, external de-risking (env check, migration dry-run mode),
  DRAFT file removal, v1.0 tag → stay in the "Public release prep" candidate
  (RR01 rec 14 / §10).
- `cairn-init` §0 default-branch fallback recipe alignment → RR01 rec 7
  candidate ("Skill/hook single-source-of-truth").
- Adding a changelog declaration to the profile schema → RR01 rec 11 candidate
  ("Changelog profile slot"); this milestone genericizes `/hotfix` wording
  only, no slot.

## Acceptance criteria

- [x] AC1 — `plugin.json` description and README ¶1 both reframed from
      R-exclusive to the language-agnostic-core + toolchain-profile framing
      (naming r-package / python / generic), consistent with DESIGN Purpose &
      Scope; a whole-repo `git grep` for other R-exclusive positioning mentions
      (M48 lesson) turns up none unaddressed.
- [x] AC2 — `cairn-init` §0's "No DESCRIPTION file → not an R package" bullet
      is gone and the adjacent "Toolchain profile" bullet still handles the
      DESCRIPTION-absent case (profile-selection behavior unchanged).
- [x] AC3 — `/hotfix` step 5 no longer hardcodes `NEWS.md`; it names the
      profile's changelog generically, with no profile-schema slot added.
- [x] AC4 — `cairn/DESIGN.md` hooks bullet lists all 5 hooks (adds
      `commit_guard.py`, `memory_guard.py`) and IP1 reads "the default branch",
      not "main". (RB tripwire: ip-touching — IP1 wording; M25 already decided
      the semantics, so review confirms no new D-entry is owed, only alignment.)
- [x] AC5 — DESIGN Known-issues no longer says "Unpiloted (M02/M03)"; it states
      the honest list — single-author, single-OS, hooks unverified on Windows,
      and conduct enforced as prose/guard-tests (only spot-verified at runtime).
- [x] AC6 — `skills/shared/templates/claude-md-section.md` boundary rule
      includes `Lessons → LESSONS`.
- [x] AC7 — a guard test positively asserts the profile framing (plugin.json +
      README) and DESIGN's 5-hook list, registered in the mutation harness
      (blanking a protected block fails the guard; the completeness meta-test
      passes); the `verify` slot — `python3 -m unittest discover` over the
      script + skill suites — is clean.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T4
- AC6 → T5
- AC7 → T6

## Tasks

- [x] T1 — Reframe outward positioning (plugin.json + README ¶1) to profile framing; M48 sweep the repo for other R-exclusive strings.
- [x] T2 — Delete cairn-init §0's "not an R package" bullet; confirm the Toolchain-profile bullet still covers the DESCRIPTION-absent path.
- [x] T3 — Genericize /hotfix step 5 (NEWS.md → the profile's changelog; no slot).
- [x] T4 — Refresh DESIGN.md: 5-hook list, IP1 "main" → "the default branch" (RB tripwire: ip-touching), honest Known-issues + honor-system line.
- [x] T5 — Add `Lessons → LESSONS` to the claude-md-section template boundary rule.
- [x] T6 — Add the positioning/DESIGN-hooks guard test (single-line, unbolded asserts per M23/M26) + Mutation-harness entries; full suite green.

## Work log

- 2026-07-13: created by /milestone-plan (RR01 recs 1 + 5; carved from the "Public release prep" candidate).
- 2026-07-13: IP1 disposition gate → wording alignment, no D-entry (M25 owns the semantics).
- 2026-07-13: T1–T3 — positioning reframed; M48 sweep caught 2 more R-only strings in `marketplace.json`; cairn-init R-centric bullet removed; /hotfix genericized (no slot).
- 2026-07-13: T4–T5 — DESIGN 5-hook list + IP1 default-branch + honest Known-issues; template gains `Lessons → LESSONS` (its guard was folded into T6 — minor amendment).
- 2026-07-13: T6 — `test_positioning_guard.py` (7 methods) + 8 mutation-harness entries; full suite green, guard proven non-false-coverage → status review.

## Decisions

## Review

PR: https://github.com/jmgirard/cairn/pull/52 · reviewed 2026-07-13.

**Acceptance evidence (fresh, by command):**
- AC1 — plugin.json + marketplace.json (×2) + README ¶1 carry the profile
  framing; "for R packages" / "milestone-driven R package development" absent;
  whole-repo `git grep` for R-exclusive positioning → only the guard's own
  `assertNotIn` strings.
- AC2 — `grep "not an R package"` → 0 in cairn-init; "Toolchain profile" bullet
  present and confirm-before-write intact.
- AC3 — /hotfix names "the profile's changelog file"; old "NEWS.md entry" / "the
  NEWS line" wording → 0; no profile slot added.
- AC4 — DESIGN names all 5 hooks (session_context, stop_guard, merge_guard,
  commit_guard, memory_guard); IP1 "Nothing reaches the default branch",
  "reaches main" gone. `cairn_impact --changed`: IP1's 11 citations all remain
  valid (meaning unchanged); GP4's new DESIGN:42 citation accurate — reconciled.
- AC5 — "Unpiloted" gone; Single-author + unverified-on-Windows + enforced-as-
  prose present.
- AC6 — template boundary rule contains `Lessons → LESSONS`.
- AC7 — verify slot clean: 150 skills tests + 65 scripts tests OK; mutation
  harness blanks each of the 8 registered blocks and the guard fails
  (non-false-coverage); completeness meta-test passes. `cairn_validate` 14/14
  CHECKS + sizing OK (exit 0). Generic profile consistency-gate: no extra
  toolchain checks (clean no-op).

**Independent fresh-context review (3 lenses):** zero findings — no scorer/
triage needed.
- [O] diff-bug (Opus): no defects. Verified all 8 mutation blocks occur once
  and their blanking breaks a live assert (genuine coverage); both JSON files
  parse; cairn-init "confirm before writing" survives; R_COMMAND_TOKENS guard
  untouched (reads r-package.md, not /hotfix); 5 hooks ship and the two nudges
  emit no `permissionDecision` (advisory claim true).
- [S] blame-history (Sonnet): consistent with history. IP1 "main" was a gap M25
  left (it scoped itself to operational skills; M22 set the doctrine) — wording
  alignment, no D-entry owed; hooks/Known-issues rewrite drops no live content.
- [S] prior-PR-comments (Sonnet): no-op — all 26 prior PRs touching these files
  have 0 inline review comments (expected, M40 lesson).
