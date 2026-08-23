# M158: DESIGN.md Known issues gains a lifecycle — review hygiene routes accepted limitations there

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Branch/PR:** —

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

- [ ] AC1: Step 9 of `skills/milestone-review/SKILL.md` (the post-merge
      hygiene pass) contains a clause that routes an accepted durable
      limitation — one the milestone surfaced, the user chose to live with,
      and no candidate row or fix covers — to an entry in `cairn/DESIGN.md`'s
      Known issues section, and states that the entry is written in the same
      hygiene commit.
- [ ] AC2: A fresh run of each of the two gating suites (`python3 -m
      unittest` over `scripts/tests` and `hooks/tests`) exits 0, and
      `skills/tests` is hand-run on the branch, any red classified per
      D-109 — traced to an intentional re-wording and noted as intentional,
      or else recorded as a candidate falsifier firing.

## Coverage

- AC1 → T1
- AC2 → T2

## Tasks

- [ ] T1: Author the routing clause in step 9 of
      `skills/milestone-review/SKILL.md` (beside the lessons-capture block,
      ~line 345), keeping it short and echoing no pinned prose-guard marker
      phrase (the M148 lesson).
- [ ] T2: Run both gating suites from the repo root, each exit code checked
      individually, and hand-run `skills/tests`; a red traced to the new
      sentence is fixed by rewording the new sentence only, never the pinned
      one.

## Work log

- 2026-08-23: created by /milestone-plan; criteria passed the full-mode audit (fresh [O] reader, two rounds: round 1 five findings — an instrument-bound evidence-quotation tail, an ambiguous commit clause, a skills/tests-green demand that would re-arm the gate D-109 removed, harness-bound AC2 wording, a missing door citation — all repaired; round 2 passed AC1 and repaired AC2's undecidable no-regression form to per-suite exit-0 with a two-sided red classification).
- 2026-08-23: plan gate chose the routing clause over deleting the Known issues section from the scaffold and ownership table because the section earns its keep in cairn's own DESIGN.md and the fix costs one sentence; falsified by adopting repos' Known issues sections staying empty with the routing clause live.
- 2026-08-23: plan gate chose review-hygiene-only placement over also adding a hotfix-close clause because milestones are where accepted limitations surface and a second shipped surface would rarely fire; falsified by a hotfix session surfacing an accepted durable limitation with nowhere to record it.

## Decisions

## Review
