<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". -->
# M58: Rulebook doctrine placement — governance up, validation doctrine out, registry pointer

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** GP1, GP3
- **Branch/PR:** m58-rulebook-doctrine-placement

## Goal

Put each doctrine where it governs: universal change-governance moves up from
two profile slots to the core rulebook, the conditionally-relevant validation
doctrine moves out to a `skills/shared/validation-doctrine.md` module, and the
oracle registry gains a declared pointer (RR01 recs 4/6/9).

## Scope

**In:**
- Dependency-change gating + deprecation-cycle policy stated once in the core
  rulebook's Universal tracking rules; r-package/python `test-doctrine` slots
  keep only the mechanical renderings (`Imports/Suggests` vs `pyproject.toml`
  dependencies; `DeprecationWarning` vs R deprecation mechanics). Generic
  adopters inherit both rules via core (gate-decided 2026-07-16).
- Extract "Validation doctrine" through "Source ingestion"
  (tracking-rules.md:462-524-ish) to `skills/shared/validation-doctrine.md`;
  the rulebook keeps a ~3-line reference (what it covers, who must read it:
  repos with numeric/scoring work). Wiring is rulebook-reference-only — no
  per-skill directives (gate-decided).
- The M57 references/ page-type rules (Synthesis notes paragraph: two page
  types, page⇒INDEX-line) stay in core, reworded to stand alone — they are
  universal, not numeric-conditional (gate-decided; supersedes RR01 rec 9's
  literal "through Source ingestion" boundary, which predates M57).
- Registry-pointer line in the module's oracle-registry paragraph: a repo with
  numeric work declares *where* its oracle records live (DESIGN.md
  Conventions); absence in a numeric repo is itself the audit finding. Shape
  stays free; no validate CHECK (D-029 stands).
- D-entry recording the placement norm — "new domain doctrine gets a module,
  not a rulebook section" — annotating D-024/D-029.
- Guard re-anchors + mutation-registry updates for every moved/reworded block;
  repo-wide cross-reference sweep (M48 lesson).

**Out:**
- Oracle-record micro-syntax (greppable `oracle O-<id> type=<type>` key,
  RR01 §4 second hardening) → dropped at the user's explicit request
  (gate 2026-07-16); RR01 §4 records it, search-first re-finds it if a
  mechanical-tally consumer ever appears.
- Skill/hook single-source-of-truth batch (RR01 recs 7/8/12/13) → existing
  ROADMAP candidate row, untouched here.
- Changelog profile slot, IP4 naming → their existing candidate rows.

## Acceptance criteria

- [ ] AC1: Dependency-change gating ("never unilateral — question-gate +
      D-entry") and deprecation-cycle policy ("breaking changes follow a
      deprecation cycle unless pre-1.0 and explicitly waived") are stated in
      the core rulebook's Universal tracking rules; the r-package and python
      `test-doctrine` slots carry only mechanical renderings (still passing
      `test_relocated_guardrail_specifics_survive`'s `deprecation` +
      `Imports/Suggests` token asserts); a new mutation-registered guard locks
      the core statement (RR01 §3).
- [ ] AC2: `skills/shared/validation-doctrine.md` exists and owns the
      validation doctrine (priority list, five oracle types, ≥2-types bar,
      registry fields + shape freedom, reproducibility hard stop,
      primary-sources hard stop, source ingestion); the rulebook retains only
      a ~3-line reference to it; the references/ page-type rules remain in the
      core rulebook and read stand-alone (no dangling "second page type"
      back-reference into the module).
- [ ] AC3: The module's registry paragraph requires the registry pointer —
      declared location in the adopting repo's DESIGN.md Conventions, absence
      in a numeric repo = audit finding (RR01 §4) — locked by a
      mutation-registered guard.
- [ ] AC4: All three unittest suites green (`python3 -m unittest discover -s
      skills/tests`, `-s scripts/tests`, `-s hooks/tests` from the repo root —
      M56 lesson); `test_oracle_doctrine.py` reads the module,
      `test_references_pages.py` matches the reworded core text, and every
      affected `Mutation(...)` registry entry targets the file its guard now
      reads.
- [ ] AC5: A DECISIONS.md entry records the module-placement norm annotating
      D-024/D-029, and `git grep` finds no remaining prose locating the
      validation doctrine inside tracking-rules (profile header comments,
      generic.md test-doctrine, "What gets a test" tail, DESIGN.md swept).

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T1, T2, T3, T6
- AC5 → T4, T5

## Tasks

- [x] T1: Move governance up. Add the two rules as bullets in Universal
      tracking rules; trim [r-package.md:53-54](../../skills/shared/profiles/r-package.md)
      and [python.md:49-52](../../skills/shared/profiles/python.md) to
      mechanical renderings keeping the guarded tokens; add the core guard +
      `Mutation(...)` entry. Guard edits ship in this commit (M46 lesson:
      source-of-truth flip lands in the first relocating commit).
- [ ] T2: Extract the module. Create `skills/shared/validation-doctrine.md`
      (doctrine through Source ingestion, minus the Synthesis-notes
      paragraph); leave the ~3-line rulebook reference; reword the
      Synthesis-notes paragraph to define both references/ page types
      stand-alone; re-anchor `test_oracle_doctrine.py` to the module and
      `test_references_pages.py` to the reworded text; update their
      `Mutation(...)` targets — all in this commit.
- [ ] T3: Add the registry-pointer requirement to the module's registry
      paragraph + its guard assert + `Mutation(...)` entry.
- [ ] T4: Cross-reference sweep — `git grep -i` for `Validation doctrine`,
      `stated once in tracking-rules`, `oracle doctrine` repo-wide; update
      profile header comments (r-package/python/generic), generic.md
      test-doctrine line, tracking-rules "What gets a test" tail + profiles
      preamble, DESIGN.md:11 to name the module.
- [ ] T5: Append the D-entry (module-placement norm; annotates D-024/D-029).
- [ ] T6: Run all three suites from the repo root; fix any missed anchor
      (M23/M26 single-line/inside-bold matchability applies to moved text).

## Work log

- 2026-07-16: created by /milestone-plan (gate: boundary = oracle+ingestion,
  core home = Universal tracking rules, pointer-only, rulebook-only wiring).
- 2026-07-16: T1 done — governance bullets in Universal tracking rules;
  r-package/python trimmed to renderings; TestUniversalChangeGovernance +
  2 Mutation entries; "What gets a test" tail corrected; 3 suites green.

## Decisions

## Review
