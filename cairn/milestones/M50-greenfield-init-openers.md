# M50: Greenfield init opener flow

- **Status:** review
- **Priority:** normal
- **Depends on:** —   <!-- M45–M47 (toolchain profiles) are all done; the greenfield-openers slot they defined empty is filled here -->
- **Principles touched:** IP3, GP3
- **Branch/PR:** m50-greenfield-init-openers · https://github.com/jmgirard/cairn/pull/48

## Goal

Give `cairn-init` a greenfield flow: in a new/empty repo it picks the toolchain
profile via a project-type chip, asks a universal + profile-specific opener set,
and lands each answer in a durable home — filling the three profiles'
`greenfield-openers` slots and staying tracking-only.

## Scope

**In:**
- Fill the `greenfield-openers` slot in all three shipped profiles
  (`skills/shared/profiles/{r-package,python,generic}.md`) with concrete,
  askable language-specific openers, replacing the "ships later" placeholders.
- Wire `cairn-init` SKILL §1 with a greenfield trigger (new/empty repo, profile
  not inferable from source), a project-type chip that selects the profile, a
  universal opener layer (distribution ambition, numeric-work-needs-oracles),
  execution of the selected profile's slot openers, answer-landing into durable
  homes, and an "undecided" path (reversible default + candidate row).
- Guard tests for the profile-slot content and the cairn-init wiring.

**Out:**
- Creating any package skeleton (DESCRIPTION / `pyproject.toml` / `R/` / `src/`)
  — cairn-init stays tracking-only; the skeleton is the *adopting repo's* obvious
  first milestone (surfaced on the routing chip), not a cairn milestone.
- Deep principle elicitation → stays `/design-interview` (D-013/D-014); openers
  are toolchain-config only.
- A bundled minor-conventions "defaults" opener (e.g. {cli}) → deferred to the
  adopting repo's first `/milestone-plan`, per the candidate.

## Acceptance criteria

- [x] AC1 — The three shipped profiles' `greenfield-openers` slots hold concrete
      askable language-specific openers, not "ships later" placeholders:
      r-package names compiled-code (Rcpp/RcppArmadillo); python names
      typing-strictness (`mypy --strict`) and `src/`-vs-flat layout; generic
      states the universal layer is its whole greenfield flow. Each
      language-specific opener names its options, a marked reversible default,
      each option's consequence, and the durable home its answer lands in.
- [x] AC2 — `cairn-init` SKILL §1 defines a greenfield trigger (a new/empty repo
      with no profile inferable from source) that runs a project-type chip
      selecting the toolchain profile before scaffolding; existing-code fresh
      scaffolds and migrations are unchanged (profile still inferred, no openers).
- [x] AC3 — In greenfield mode cairn-init asks a universal opener layer —
      distribution ambition (options rendered per selected profile:
      CRAN / PyPI / tagged-release) and numeric-work-needs-oracle-verification
      (universal, D-024/D-025) — then the selected profile's slot openers, in
      batched question-gate rounds, landing each answer in its named durable home
      (DESIGN Purpose & Scope / DESIGN Conventions / a PROFILE slot).
- [x] AC4 — An "undecided" answer to any opener takes that opener's marked
      reversible default and banks one ROADMAP candidate row recording the
      deferred choice; nothing is silently locked in (IP3 conservation).
- [x] AC5 — cairn-init stays tracking-only in greenfield mode — no package
      skeleton is created; the skeleton is surfaced as the adopting repo's first
      milestone on the closing routing chip. Openers stay bounded distinct from
      `/design-interview`: DESIGN principle elicitation still routes there.
- [x] AC6 — Guard tests lock the new surface: (a) each shipped profile's
      greenfield-openers slot names its intended opener(s), with the guard
      iterating all three shipped profiles (M48); (b) cairn-init's SKILL prose
      carries the greenfield trigger, project-type chip, universal opener layer,
      and reversible-default + candidate-row wording — each assertion anchored on
      phrasing the new work uniquely introduces (M39/M40 false-coverage guard).
      Existing `test_toolchain_profiles.py` slot-schema tests still pass (slots
      stay non-empty).
- [x] AC7 — The active profile's `verify` slot is clean:
      `python3 -m unittest discover -s skills/tests` and
      `python3 -m unittest discover -s scripts/tests` pass.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3, T5
- AC4 → T3, T5
- AC5 → T3
- AC6 → T4
- AC7 → T1, T2, T3, T4

## Tasks

- [x] T1 — Fill all three profiles' `greenfield-openers` slots with concrete
      language-specific openers (options + reversible default + consequence +
      home); remove the placeholders; keep slots non-empty. (evidence: AC1)
- [x] T2 — cairn-init SKILL §0: greenfield trigger → project-type chip → profile
      selection; existing-code/migration paths unchanged. (AC2)
- [x] T3 — cairn-init SKILL §1: universal opener layer + profile-slot openers +
      answer-homes + undecided⇒reversible-default+candidate-row; tracking-only;
      `/design-interview` boundary; chip surfaces the skeleton. (AC3–AC5)
- [x] T4 — Guard tests: profile-slot content (all 3 profiles) + SKILL prose
      (M39/M40-anchored); existing slot-schema tests still pass. (AC6)
- [x] T5 — Dry-run walkthrough on a scratch empty repo (interactive rounds
      non-automatable). (AC3/AC4 evidence)

## Work log

- 2026-07-13: T1–T5 implemented (details per task line above; +6 guards). Fresh
  suites at each checkpoint green (skills 129, scripts 65). During T4 caught and
  fixed one over-strict assertion (slots *reference* the universal oracle opener
  to defer it, not duplicate it).
- 2026-07-13: created by /milestone-plan. Gate decisions: trigger = empty/new
  repo (profile not inferable); architecture = universal opener layer + profile
  openers (oracle-on/distribution universal, D-024/D-025); undecided = reversible
  default + candidate row; evidence = prose-guards + dry-run. Absorbs the
  "Greenfield init flow" candidate (lineage M45–M47); row graduates at completion
  (M35 lesson).

## Decisions

## Review

Reviewed 2026-07-13, branch m50-greenfield-init-openers (PR #48), 7 files.
Profile generic → `verify` = `python3 -m unittest`.

**Acceptance criteria (fresh evidence)** — all ✓ via the M50 guard classes
`TestGreenfieldOpeners` + `TestGreenfieldInitFlow` (6 tests, each anchored on
M50-unique tokens): AC1 slots filled + placeholder gone (all 3 profiles); AC2
greenfield trigger + project-type chip in §0, other paths untouched; AC3
universal layer + profile-slot openers landing in named homes; AC4 undecided ⇒
reversible default + `candidate` row; AC5 tracking-only + `/design-interview`
boundary + skeleton on the chip; AC6 +6 guards, existing slot-schema +
`test_shipped_reference_profiles_are_valid` (real validator, all 3 profiles)
still pass; AC7 `skills/tests` 129 OK, `scripts/tests` 65 OK.

**Consistency gate:** `cairn_validate` exit 0; Coverage — AC1–AC7 all map to
existing T1–T5; no DESIGN principle text changed → `cairn_impact` skipped;
generic `consistency-gate` slot names no toolchain checks → clean no-op.

**Independent review (3 lenses + scorer):** [O] diff-bug: 2 findings (both
SKILL.md); [S] blame-history: none (M45–M49 intent intact; D-013/D-014/D-024/
D-025 not contradicted); [S] prior-PR: no prior-PR evidence (expected no-op).
- F1 (20, excluded/logged) — project-type chip prose doesn't restate the
  stop/pause chip invariant; it's a content-selection chip and the invariant is
  incorporated by reference, not a per-SKILL restatement.
- F2 (80, **fixed**) — the pre-existing §1 DESIGN-fill bullet ran unconditionally
  after the greenfield-openers step, unreconciled for greenfield (no DESCRIPTION/
  source; risked overwriting opener-seeded sections). Fixed: the bullet now scopes
  greenfield → extend the opener-seeded Purpose & Scope + Conventions, never
  overwrite. Re-ran suites after the fix: 129/65 OK, `cairn_validate` clean.
