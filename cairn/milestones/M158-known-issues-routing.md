# M158: DESIGN.md Known issues gains a lifecycle — review hygiene routes accepted limitations there

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** m158-known-issues-routing · https://github.com/jmgirard/cairn/pull/159

## Goal

Add one routing clause to `/milestone-review`'s post-merge hygiene step so an
accepted durable limitation lands in `cairn/DESIGN.md`'s Known issues section,
closing the gap that the plugin scaffolds and names that section but no
operational skill ever writes it.

## Scope

Surface tier: user-facing — the deliverable is shipped skill prose adopting
repos run. D-108's door is open on its retained trigger: a defect in shipped
behavior, surfaced by a downstream repo (quarto-index's scaffolded Known
issues section stays empty by construction — `cairn-init` creates it,
tracking-rules names it DESIGN-owned, no skill fills it), hosted here per
D-098.

**In:** one clause in step 9 of `skills/milestone-review/SKILL.md`, beside the
"Capture durable lessons" block, routing a durable limitation the milestone
surfaced and the user accepted — no candidate row, no fix planned — to an
entry in `cairn/DESIGN.md`'s Known issues section, written in the same hygiene
commit.

**Out:** a hygiene staleness check on Known issues entries → dropped at the
plan gate (DESIGN.md is current knowledge corrected in place under D-045; no
new instrument). A parallel clause in `/hotfix` → dropped at the plan gate
(rarely fires; second surface). Filling quarto-index's own DESIGN.md →
downstream repo's work, not cairn's. Deleting the section instead → rejected
at the plan gate; see work log.

## Acceptance criteria

- [x] AC1: Step 9 of `skills/milestone-review/SKILL.md` (the post-merge
      hygiene pass) contains a clause that routes an accepted durable
      limitation — one the milestone surfaced, the user chose to live with,
      and no candidate row or fix covers — to an entry in `cairn/DESIGN.md`'s
      Known issues section, and states that the entry is written in the same
      hygiene commit.
- [x] AC2: A fresh run of each of the two gating suites (`python3 -m
      unittest` over `scripts/tests` and `hooks/tests`) exits 0, and
      `skills/tests` is hand-run on the branch, any red classified per
      D-109 — traced to an intentional re-wording and noted as intentional,
      or else recorded as a candidate falsifier firing.

## Coverage

- AC1 → T1
- AC2 → T2

## Tasks

- [x] T1: Author the routing clause in step 9 of
      `skills/milestone-review/SKILL.md` (beside the lessons-capture block,
      ~line 345), keeping it short and echoing no pinned prose-guard marker
      phrase (the M148 lesson).
- [x] T2: Run both gating suites from the repo root, each exit code checked
      individually, and hand-run `skills/tests`; a red traced to the new
      sentence is fixed by rewording the new sentence only, never the pinned
      one.

## Work log

- 2026-08-23: created by /milestone-plan; criteria passed the full-mode audit (fresh [O] reader, two rounds: round 1 five findings — an instrument-bound evidence-quotation tail, an ambiguous commit clause, a skills/tests-green demand that would re-arm the gate D-109 removed, harness-bound AC2 wording, a missing door citation — all repaired; round 2 passed AC1 and repaired AC2's undecidable no-regression form to per-suite exit-0 with a two-sided red classification).
- 2026-08-23: plan gate chose the routing clause over deleting the Known issues section from the scaffold and ownership table because the section earns its keep in cairn's own DESIGN.md and the fix costs one sentence; falsified by adopting repos' Known issues sections staying empty with the routing clause live.
- 2026-08-23: plan gate chose review-hygiene-only placement over also adding a hotfix-close clause because milestones are where accepted limitations surface and a second shipped surface would rarely fire; falsified by a hotfix session surfacing an accepted durable limitation with nowhere to record it.
- 2026-08-23: T1 — routing clause added to step 9 under its own header ("Route accepted limitations:"), between the lessons-capture and retirement blocks; echoes neither pinned marker phrase; both gating suites exit 0 (324 + 103 tests, OK).
- 2026-08-23: T2 — gating suites re-run individually on the branch (scripts/tests 324, hooks/tests 103, each exit 0); skills/tests hand-run: 528 tests, exit 0, zero reds, nothing to classify. Status → review.
- 2026-08-23: review — PR #159 (draft); AC1–AC2 verified with fresh evidence (Review section); cairn_validate all checks pass; generic profile → toolchain gate no-op; three-lens fan-out spawned (user-facing tier).

## Decisions

## Review

- 2026-08-23 AC1: verified by reading `git diff main...HEAD -- skills/milestone-review/SKILL.md` — step 9 gains a "Route accepted limitations:" block between the lessons-capture and retirement blocks, routing a durable limitation the milestone surfaced, the user chose to live with, and no candidate row or fix covers, to an entry in `cairn/DESIGN.md`'s Known issues section, "written in this same hygiene commit"; "None accepted → skip." Pass.
- 2026-08-23 AC2: fresh runs at review — `python3 -m unittest discover` per suite, exit codes checked individually: scripts/tests 324 tests exit 0; hooks/tests 103 tests exit 0; skills/tests hand-run, 528 tests exit 0, zero reds, nothing to classify under D-109. Pass.

Fan-out findings and triage (2026-08-23; [O] diff-bug 9 findings, [S] blame-history 1 flag, [S] prior-PR-comments no prior-review evidence, zero findings):

- F1 [O]: a Known issues entry is the only newly authored durable record in the hygiene commit without durable-record preview coverage — both enumerations (skill step 9, tracking-rules) omit it. **Fixed now:** added to both enumerations; pinned guard phrases untouched; all three suites re-run green (324/103/528).
- F2 [O]: the clause's "no candidate row, no fix planned" condition contradicts an existing Known issues entry that carries a candidate row. **Rejected:** the condition is a routing trigger for otherwise-unrecorded limitations, not a membership test for the section; entries that also carry candidate rows stay legal.
- F3 [O]: inflow with no outflow — no rule for when an entry leaves. **Rejected:** plan gate deliberately dropped the staleness check (Out); DESIGN.md is current knowledge corrected in place (D-045), which is the outflow.
- F4 [O]: no entry grammar (date/attribution/length unspecified). **Rejected:** DESIGN.md prose is not line-formatted; existing entries set the precedent; adding a grammar is hardening beyond the milestone's one-sentence scope.
- F5 [O]: ambiguity against the adjacent "a choice is a D-entry" sentence. **Rejected:** DECISIONS.md explicitly does not own deferrals ("not now" is not a decision); an accepted limitation is a state fact, and a genuinely cross-cutting choice still takes its D-entry independently.
- F6 [O]: missing-section case unhandled for adopting/migrated repos. **Rejected:** writing an entry to a named section implies creating the heading when absent; scaffold repair is `/cairn-init`'s job and out of this milestone's scope.
- F7 [O]: "the user chose to live with" is applied post-merge with no recorded artifact. **Rejected:** same epistemics as the adjacent lessons-capture block, which also draws on session memory; the acceptance it names happens at recorded surfaces (gate triage, plan-gate Out lines).
- F8 [O]: placement splits the LESSONS inflow/outflow pair. **Rejected:** reviewer's own reading finds the retirement block unambiguous; plan placed the clause beside lessons-capture deliberately.
- F9 [O]: stray blank work-log line; review-phase edits uncommitted at snapshot time. **Fixed now** (blank line removed) / already resolved (evidence commit cc7e872 pushed before triage).
- F10 [S blame]: the D-108 door justification is the milestone's self-assessment and this class of argument has been miscalled before; reviewer's own scrutiny finds the door genuinely open (shipped scaffold names a section no skill writes, surfaced by a downstream repo). **Rejected (noted):** the plan gate recorded the door basis; no new evidence against it.

Return floor: no finding demonstrates an acceptance criterion failing or a load-bearing defect in shipped behavior — no status return.
