# M94: Cost instrumentation — measure what a milestone spends before governing it

**Status:** done · 2026-07-19 · PR #93 · branch `m94-cost-instrumentation`

**Goal.** Measure what a milestone costs — cache-read, fresh input, turns, by phase — so the next weight mechanism is aimed at a measured term. Sequenced FIRST per RR02 rec 4, ahead of M95 (slimming), M96 (ratchet), M97 (bounded read).

**Outcome.** `scripts/cairn_cost.py` reports per session, per phase and per milestone over the Claude Code session store, keyed by the runtime-written `attributionSkill` and `gitBranch` rather than by heuristic. `/milestone` §2 gained one always-read cost line, boundaried in prose as a reporting surface with no threshold or verdict. `cairn/references/session-cost-notes.md` records the schema, the A1–A6 attribution ledger, and a ten-milestone baseline.

**Headline measurement.** Cache-read per turn rose 166,451 (M63–M68) → 184,351 (M88–M93), **+10.8%**, while `tracking-rules.md` grew +56% and `DECISIONS.md` +103% over the same window — the always-read tracking files are a minority term in per-turn context. Cache-read exceeds fresh input 719:1 store-wide, which is why the four token classes are never summed.

**Key decisions.** Milestone attribution is branch-derived only; plan-phase work on the default branch is reported unkeyed (40.4% of turns) rather than imputed, since one plan session legitimately names four milestones. Subagent tokens are absent from every store on disk, so each phase reports its spawn count to label the figure partial rather than publishing it bare. Per-file apportionment of cache reads stays Out — no oracle exists for it.

**Review.** AC1 failed first pass (no per-session breakdown) and was sent back rather than read charitably. Three lenses + scorer: 8 findings, 5 scored ≥80 and fixed — F5/91 mutation-proven false coverage in a new guard; F8/90 a prose-guard docstring overclaiming its own registration, the trap M53's review caught; F3/88 a filtered report announcing its blind spot as 0.0%; F6/85 note overclaim; F2/82 session count decoupled from rendered rows. F4 (78) fixed at the user's instruction at the merge gate. Verify 447/236/72, `cairn_validate` exit 0.

**Graduated to LESSONS.md:** the multi-section false-coverage shape (appended to the M84 line) and the filter-vs-whole-population trap (new line).
