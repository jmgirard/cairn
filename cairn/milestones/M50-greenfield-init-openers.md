# M50: Greenfield init opener flow

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —   <!-- M45–M47 (toolchain profiles) are all done; the greenfield-openers slot they defined empty is filled here -->
- **Principles touched:** IP3, GP3
- **Branch/PR:** m50-greenfield-init-openers

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

- [ ] AC1 — The three shipped profiles' `greenfield-openers` slots hold concrete
      askable language-specific openers, not "ships later" placeholders:
      r-package names compiled-code (Rcpp/RcppArmadillo); python names
      typing-strictness (`mypy --strict`) and `src/`-vs-flat layout; generic
      states the universal layer is its whole greenfield flow. Each
      language-specific opener names its options, a marked reversible default,
      each option's consequence, and the durable home its answer lands in.
- [ ] AC2 — `cairn-init` SKILL §1 defines a greenfield trigger (a new/empty repo
      with no profile inferable from source) that runs a project-type chip
      selecting the toolchain profile before scaffolding; existing-code fresh
      scaffolds and migrations are unchanged (profile still inferred, no openers).
- [ ] AC3 — In greenfield mode cairn-init asks a universal opener layer —
      distribution ambition (options rendered per selected profile:
      CRAN / PyPI / tagged-release) and numeric-work-needs-oracle-verification
      (universal, D-024/D-025) — then the selected profile's slot openers, in
      batched question-gate rounds, landing each answer in its named durable home
      (DESIGN Purpose & Scope / DESIGN Conventions / a PROFILE slot).
- [ ] AC4 — An "undecided" answer to any opener takes that opener's marked
      reversible default and banks one ROADMAP candidate row recording the
      deferred choice; nothing is silently locked in (IP3 conservation).
- [ ] AC5 — cairn-init stays tracking-only in greenfield mode — no package
      skeleton is created; the skeleton is surfaced as the adopting repo's first
      milestone on the closing routing chip. Openers stay bounded distinct from
      `/design-interview`: DESIGN principle elicitation still routes there.
- [ ] AC6 — Guard tests lock the new surface: (a) each shipped profile's
      greenfield-openers slot names its intended opener(s), with the guard
      iterating all three shipped profiles (M48); (b) cairn-init's SKILL prose
      carries the greenfield trigger, project-type chip, universal opener layer,
      and reversible-default + candidate-row wording — each assertion anchored on
      phrasing the new work uniquely introduces (M39/M40 false-coverage guard).
      Existing `test_toolchain_profiles.py` slot-schema tests still pass (slots
      stay non-empty).
- [ ] AC7 — The active profile's `verify` slot is clean:
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
      language-specific openers (r-package: compiled code; python: typing
      strictness + layout; generic: "the universal layer is the whole greenfield
      flow"); each language-specific opener names options + marked reversible
      default + consequence + durable home; remove the "ships later" placeholder
      prose. Keep every slot non-empty (schema).
- [x] T2 — Wire `cairn-init` SKILL §1: greenfield trigger (new/empty repo, no
      inferable profile) → project-type chip → profile selection + PROFILE.md
      instantiation. Leave the existing-code fresh-scaffold and migration paths
      unchanged (profile still inferred, openers skipped).
- [x] T3 — Wire the opener flow in cairn-init: the universal opener layer
      (distribution ambition rendered per profile; oracle-on) → the selected
      profile's slot openers → answer-landing into the named durable homes →
      undecided ⇒ reversible default + one candidate row. Add the tracking-only
      guard (no skeleton), the `/design-interview` boundary note, and update the
      closing routing chip to surface "plan the package skeleton" as the first
      milestone.
- [ ] T4 — Guard tests: profile-slot content (iterate all three shipped
      profiles; extend any hardcoded profile list per M48) + cairn-init SKILL
      prose (anchored on phrasing the new work uniquely introduces, M39/M40);
      confirm `test_toolchain_profiles.py` slot-schema tests still pass.
- [ ] T5 — Dry-run walkthrough against a scratch empty repo (project-type chip →
      universal + profile openers → answer homes → undecided path), recorded in
      the work log as review evidence (the interactive flow can't be unit-tested).

## Work log

- 2026-07-13: T3 — cairn-init §1 gains the greenfield opener flow (universal layer: distribution ambition per profile + oracle-on; profile layer: slot openers; undecided ⇒ reversible default + one candidate row); tracking-only guard, /design-interview boundary, chip surfaces the package skeleton as the first milestone. Full skills suite (123 tests) green.
- 2026-07-13: T2 — cairn-init §0 gains a greenfield-detection bullet (new/empty + no marker) → project-type chip selects the profile explicitly instead of defaulting to generic; non-greenfield/migration paths unchanged.
- 2026-07-13: T1 — filled the three profiles' greenfield-openers slots with concrete openers (r-package: compiled code; python: typing strictness + `src/`-vs-flat; generic: universal layer is the whole flow); universal openers left to cairn-init, not duplicated. Existing test_toolchain_profiles.py (24 tests) still green.
- 2026-07-13: created by /milestone-plan. Gate decisions: trigger = empty/new
  repo only (profile not inferable); architecture = universal opener layer +
  profile openers (oracle-on/distribution universal per D-024/D-025); undecided =
  reversible default + candidate row; evidence = prose-guards + dry-run
  walkthrough. Absorbs the "Greenfield init flow" candidate (lineage: M45–M47
  toolchain profiles, references/design-interview-notes.md); the candidate row
  graduates at completion (M35 lesson).

## Decisions

## Review
