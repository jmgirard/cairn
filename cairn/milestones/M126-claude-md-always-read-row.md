# M126: CLAUDE.md joins the always-read governance frame

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1
- **Branch/PR:** `m126-claude-md-always-read-row`

## Goal

The always-read governance frame's worked table covers every surface this repo
actually loads at session start, `CLAUDE.md` included, and states why cairn's
governance of it stops at the cairn section.

## Scope

**In:** a recorded sweep of what a session actually loads at start, classifying
each surface against the frame's table; a table row for each uncovered surface;
the statement of what makes the `CLAUDE.md` row unlike the five above it; guards
pinning both, mutation-registered and inversion-verified; a `DECISIONS.md` entry
recording the addition and its boundaries.

**Out:**
- Any change to what cairn governs in `CLAUDE.md` — D-018's section-only cap and
  D-009's routing-only rule both stand unchanged; nothing moves.
- Amending the frame's opening definition of an always-read file — settled at the
  plan gate as unnecessary; the reasoning lands in the D-entry (AC6), not in the
  rulebook.
- Reconciling the frame's membership rule with its contents — `tracking-rules.md`
  sits in the table though it is read when a skill fires, not at session start,
  while `PROFILE.md`'s slots are read that same conditional way and are absent →
  candidate row, added by this plan.
- Mechanizing the frame check → standing rejection (D-060, RR03 rec 10); the
  frame stays prose applied by audit judgment.

## Acceptance criteria

- [ ] AC1: A sweep enumerates every surface a session loads at start, derived by
      reading `hooks/hooks.json`'s SessionStart entry and `session_context.py`'s
      `build_context`, plus the harness-loaded project instructions — never a
      list carried from this plan. Each surface is classified covered by the
      frame's table, uncovered, or out of scope with its reason. Evidence: the
      classification, one row per surface, in the Review section.
- [ ] AC2: Each surface AC1 classifies uncovered gains a row in the
      "Always-read governance" worked table, appended after the existing fifth
      row so the guarded sentence "The fifth surface differs from the four above
      it" stays true. The `CLAUDE.md` row's three cells name: inflow — the
      routing-only rule (D-009); outflow — the weight-caps remedy trimming the
      section back to the template; signal — the <30-line cairn-section cap
      enforced by `cairn_validate`'s `weight caps` CHECK. Evidence: the shipped
      row plus the file:line of each of the three sources.
- [ ] AC3: The rulebook states beneath the table what makes the `CLAUDE.md` row
      unlike the five above it — cairn governs its `## Project tracking` section
      and the remainder of the file is governed by nothing cairn owns (D-018),
      as against the milestone file, whose cap-exempt sections are still
      governed, by read-bounding (D-063). The statement claims no uniqueness
      about differing always-read and governed units.
- [ ] AC4: `test_always_read_frame.py` pins each new row whole and the AC3
      statement, every anchor copied from the shipped bytes and sitting on one
      physical line of the target. Each new pinned block gets its own
      `test_mutation_harness.py` REGISTRY entry, and the harness runs green with
      them present. The new prose is grepped for every phrase an existing
      `test_always_read_frame.py` assert anchors on; any assert whose phrase the
      new prose duplicates is re-anchored into its own sentence (M113).
- [ ] AC5: Each rule this milestone ships in `tracking-rules.md` is inverted in
      place per `guard-doctrine.md` §1 — relabel, negate, or transpose **the
      rule**, never the assert; run; require red; restore and diff — with the
      per-rule result recorded. After restore, `python3 -m unittest discover`
      over `hooks/tests`, `scripts/tests` and `skills/tests` each exit 0, and
      `cairn_validate` exits 0.
- [ ] AC6: A `DECISIONS.md` entry records: that this applies D-060's own audit
      bullet as D-063 did, superseding nothing; the D-018/D-009 boundary making
      the section the governed unit; why the frame's opening definition is left
      unamended; and why `PROFILE.md` and the hook's preamble are out of scope.
      Evidence: the appended entry, `dangling id tokens` clean.

## Coverage

- AC1 → T1
- AC2 → T3
- AC3 → T3
- AC4 → T4
- AC5 → T5, T6
- AC6 → T2

## Tasks

- [x] T1: Run the AC1 sweep against `hooks/hooks.json` and
      `hooks/session_context.py:240-270` (`build_context`); classify each
      surface and record the table.
- [ ] T2: Append the `DECISIONS.md` entry (AC6's four points).
- [x] T3: Add the row(s) after `tracking-rules.md:182` and the boundary
      statement beneath the table, near the existing fifth-surface paragraph at
      `tracking-rules.md:184-193`.
- [ ] T4: Add the asserts to `skills/tests/test_always_read_frame.py` (row shape
      at `:72-97`, standalone claims at `:99-117`) and the REGISTRY entries near
      `skills/tests/test_mutation_harness.py:2156-2173`; run the adjacent-phrase
      grep; run the harness.
- [ ] T5: Invert each shipped rule per guard-doctrine §1; record per-rule.
- [ ] T6: Full verify (three suites + `cairn_validate`); ROADMAP row; hygiene.

## Work log

- 2026-07-31: created by /milestone-plan.
- 2026-07-31: criteria audit ([O], fresh context) returned nine findings on the step-2 draft; eight fixed here, one taken to the gate. Wrong-unit inflow cell (the file-map row owns the whole file, which D-018 excludes) → repointed to D-009; AC1 unconstrained on row position, admitting an insert that falsifies the guarded "fifth surface" sentence → append-after-fifth required; AC2's uniqueness claim false against the milestone file's own unit split → narrowed to what cairn governs at all; AC5 inverted the assert rather than the rule (vacuously red) → repointed to guard-doctrine §1; AC4's per-entry reddening report does not exist (subTest aggregates) → green-harness evidence; AC1's "adds no new rule" judgment-as-measurement and its ~400-char work-log quote evidence → file:line pointers; adjacent-guard grep added to AC4; T1's D-entry mapped by no criterion → AC6 added.
- 2026-07-31: plan gate chose leaving the frame's opening definition unamended over amending it, because the shipped sentence excludes nothing and an amendment would ship unguarded against D-060's prose-guarded mandate, its target line wrapping besides; falsified by a reader taking the definition to exclude a section-scoped surface.
- 2026-07-31: plan gate chose sweeping every session-start surface over closing the named `CLAUDE.md` gap alone, because a criterion that lists its sites becomes the sweep and omits the rest (M118, M112); falsified by the sweep returning surfaces whose rows the frame cannot state.
- 2026-07-31: plan gate chose a candidate row over settling the frame's membership rule here, because the table already holds a conditionally-read file and fixing that is doctrine revision, not a table row; falsified by the AC1 sweep being unable to classify a surface without the rule settled.
- 2026-07-31: implement gate chose scoping the new row's first cell to `CLAUDE.md`'s `## Project tracking` section over naming the file bare, because all three of the row's cells state section-scoped governance (D-009 inflow, the trim-to-template outflow, the 30-line section cap) and a file-named cell makes all three overclaim against D-018; and chose a new paragraph for the AC3 boundary statement over reworking the guarded fifth-surface paragraph, avoiding the re-anchoring the M104 trap runs on.
- 2026-07-31: minor amendment — T3 worked before T2 (task reorder only; no criterion, scope or task text changed), so the D-entry records what shipped rather than what was intended.
- 2026-07-31: T1 — AC1 sweep run against `hooks/hooks.json:3-13` and `build_context` (`hooks/session_context.py:241-344`) plus the harness-loaded project instructions; six surfaces, `CLAUDE.md` the sole uncovered one, `PROFILE.md`'s name header / the hook `PREAMBLE` / per-user memory out of scope. Classification table in `## Decisions`.
- 2026-07-31: T3 — sixth frame row shipped at `tracking-rules.md:183`, scoped to `CLAUDE.md`'s `## Project tracking` section; the AC3 boundary statement added as its own paragraph at `:196-206`, leaving the guarded fifth-surface paragraph untouched. Cell sources: D-009 `cairn/DECISIONS.md:90`, the trim-to-template remedy `tracking-rules.md:141-143`, the 30-line cap `tracking-rules.md:86` with `scripts/cairn_scripts.py:89` and `scripts/cairn_validate.py:75-77`.

## Decisions

### 2026-07-31 — AC1 sweep: what a session actually loads at start

Derived by reading `hooks/hooks.json:3-13` (the sole `SessionStart` entry) and
`hooks/session_context.py:241-344` (`build_context`), plus the project
instructions the harness loads. Six surfaces; one uncovered.

| Surface | Loaded by | Classification |
|---|---|---|
| `CLAUDE.md` | the harness's project-instructions injection | **uncovered** — gains a frame row (AC2) |
| `cairn/ROADMAP.md` | `hooks/session_context.py:258` | covered — the frame's first row |
| each active `cairn/milestones/M<NN>-<slug>.md` | `hooks/session_context.py:294-296`, active statuses from `hooks/cairn_common.py:16` | covered — the frame's fifth row |
| `cairn/PROFILE.md`'s `# Toolchain profile:` header | `hooks/session_context.py:244-251` via `profile_name` (`:94-109`) | out of scope — only the profile NAME reaches the session; the seven slots the rulebook governs are read when a skill fires, so whether a conditionally-read file belongs in the frame is the membership question this milestone's Scope puts Out |
| the hook's `PREAMBLE` | `hooks/session_context.py:85-91`, emitted at `:243` | out of scope — plugin source rather than a repo record: a fixed string no repo writes to, so it has no inflow to test and cannot grow with use |
| per-user memory `MEMORY.md` | the harness's memory injection | out of scope — not a repo file, and it never holds project state ("Tracking files outrank memory", the GP4 intake gate); no repo's frame can bound a per-user surface |

Recorded, not resolved: the sweep runs one direction only. Three of the frame's
existing rows — `LESSONS.md`, `tracking-rules.md`, `DECISIONS.md` — are read
when a skill or a gate fires and not at session start, so the table's membership
already runs wider than its opening definition. That is the parked candidate
row, and nothing here settles it.

## Review
