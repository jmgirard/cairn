# M108: Always-read audit frame

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, GP2
- **Branch/PR:** —

## Goal

Add the always-read audit frame — a rulebook doctrine paragraph naming the
three governance elements every always-read file must have (inflow test,
outflow or read-bound, attention signal) plus a `/milestone` audit bullet that
flags any always-read file missing one — so an ungoverned always-read surface
is visible before it accretes unchecked (RR03 rec 7).

## Scope

**In:**
- A doctrine paragraph in `skills/shared/tracking-rules.md` stating the frame:
  every always-read file names its three elements, D-045's
  history/current-knowledge split decides which outflows are legal, and a file
  missing an element is the gap the frame exists to surface.
- The worked enumeration of GP1's four always-read files (ROADMAP.md,
  LESSONS.md, tracking-rules.md, DECISIONS.md) with each file's three elements
  filled — the frame derived from a worked case, not projected.
- A judgment bullet in `/milestone` §2 audit applying the frame, alongside the
  existing staleness / references-staleness advisories.
- Prose-guards (mutation-registered) over the frame's three-element wording and
  the audit bullet.
- A D-entry (annotates D-045; cites D-053/D-056/D-057); the candidate row's
  lineage recorded (it graduates at review post-merge hygiene, not at plan — M35).

**Out:**
- Any `cairn_validate` check or other automated mechanism → stays prose-only
  (RR03 rec 7 "no new mechanism"; rec 10 rejects a shared machine). A mechanical
  check, if ever wanted → a future candidate superseding rec 7.
- Any per-file mass/growth measure or size gate → excluded; D-057's closed
  stock-side size program stays closed (the frame is completeness-only).
- Enumerating always-read files beyond GP1's four (DESIGN.md, the CLAUDE.md
  cairn section, PROFILE.md, active milestone files) → the general rule covers
  new surfaces; a broader table → a future candidate if it earns one.
- Unifying the three files' governance into one mechanism → rejected by RR03
  rec 10; not in scope.

## Acceptance criteria

- [ ] AC1: `tracking-rules.md` states the frame — every always-read file names
      its three elements (inflow test / outflow-or-read-bound / attention
      signal), with D-045's history/current-knowledge split deciding which
      outflows are legal, and a file missing an element named as the gap the
      frame surfaces (RR03 §5).
- [ ] AC2: The rulebook enumerates GP1's four always-read files (ROADMAP.md,
      LESSONS.md, tracking-rules.md, DECISIONS.md) with each file's three
      elements filled — the worked case.
- [ ] AC3: `/milestone` §2 audit includes a bullet applying the frame: it
      checks each always-read file has all three elements and that any
      newly-added always-read surface is covered, reporting a gap as a judgment
      (never auto-fixed, never a `FAIL`) — the form of the existing
      staleness / references-staleness advisories.
- [ ] AC4: The frame is completeness-only — it states no per-file mass/growth
      measure and adds no `cairn_validate` check or other mechanism (evidence:
      no new check in `cairn_validate.py`; the audit bullet measures
      element-presence, never size).
- [ ] AC5: A D-entry records the frame (annotating D-045; citing D-053, D-056,
      D-057), and the "Always-read audit frame" candidate row is set to
      graduate (executed at review post-merge hygiene — M35).
- [ ] AC6: Prose-guards pin the frame's three-element wording (rulebook) and the
      audit bullet (`/milestone` SKILL.md), each mutation-registered so blanking
      the block reddens its guard.
- [ ] AC7: The generic profile's `verify` (the three `python3 -m unittest`
      suites) and `cairn_validate` are clean.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T1, T2, T4
- AC5 → T4
- AC6 → T3
- AC7 → T3, T4

## Tasks

- [ ] T1: Author the doctrine paragraph + the four-file worked enumeration in
      `skills/shared/tracking-rules.md` (near the Weight caps / GP1-governance
      material). Completeness-only wording; no mass/growth clause.
- [ ] T2: Add the judgment bullet to `/milestone` SKILL.md §2 audit applying the
      frame (element-completeness per always-read file + new-surface coverage;
      report-not-fix, never `FAIL`).
- [ ] T3: Author prose-guards over the frame wording (T1) and the audit bullet
      (T2); register each in `test_mutation_harness.py`; verify by mutation that
      blanking each block reddens its guard. After the skill-prose edit, grep
      that every nearby guard's asserted substring is still contiguous on one
      physical line (M104).
- [ ] T4: Author D-060; record the candidate-row graduation lineage; run the
      three unittest suites from the repo root (each exit code checked, M56) and
      `cairn_validate` — both green.

## Work log

- 2026-07-23: created by /milestone-plan.

## Decisions

## Review
