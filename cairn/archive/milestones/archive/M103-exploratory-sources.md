# M103: Exploratory sources — supply-push ingestion

**Status:** done (2026-07-20, PR #101 https://github.com/jmgirard/cairn/pull/101)

**Goal:** Legitimize reading a corpus of uncited sources to discover new oracles
or methods, so cairn triages them into candidates rather than dismissing them.

**Outcome:** A new "Exploring prospective sources" paragraph in the rulebook's
"References pages" section names **supply-push exploration** as legitimate and
distinct from the demand-pull "owed" trigger — a `sources/`-shelf corpus is
triaged, not dismissed for want of a citation (the circumplex incident). Three
outputs: ROADMAP candidate rows always (D-042), a committed survey synthesis
note only when the triage outlives its exploration, per-source `<citekey>.md`
pages staying demand-pull; the M56 guardrail restated. `/milestone-plan` step 2
recognizes a corpus. Guarded by `TestExploratorySources` + 6 mutations.

**Decisions:** none (all choices recorded in the doctrine + the deferred
`/explore-sources` candidate row).

**Review:** three lenses + scorer. F1 (92, fixed): survey-note/per-source
guards anchored on bare clauses not naming their record (M74/M76 label→SET
false-coverage) — re-anchored to bind record→disposition. F2 (30, logged).
Lesson captured on mutation-reddening not defending a SET swap; none retired.
