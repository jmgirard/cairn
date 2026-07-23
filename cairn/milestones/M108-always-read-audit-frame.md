# M108: Always-read audit frame

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, GP2
- **Branch/PR:** m108-always-read-audit-frame · https://github.com/jmgirard/cairn/pull/106

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

- [x] AC1: `tracking-rules.md` states the frame — every always-read file names
      its three elements (inflow test / outflow-or-read-bound / attention
      signal), with D-045's history/current-knowledge split deciding which
      outflows are legal, and a file missing an element named as the gap the
      frame surfaces (RR03 §5).
- [x] AC2: The rulebook enumerates GP1's four always-read files (ROADMAP.md,
      LESSONS.md, tracking-rules.md, DECISIONS.md) with each file's three
      elements filled — the worked case.
- [x] AC3: `/milestone` §2 audit includes a bullet applying the frame: it
      checks each always-read file has all three elements and that any
      newly-added always-read surface is covered, reporting a gap as a judgment
      (never auto-fixed, never a `FAIL`) — the form of the existing
      staleness / references-staleness advisories.
- [x] AC4: The frame is completeness-only — it states no per-file mass/growth
      measure and adds no `cairn_validate` check or other mechanism (evidence:
      no new check in `cairn_validate.py`; the audit bullet measures
      element-presence, never size).
- [x] AC5: A D-entry records the frame (annotating D-045; citing D-053, D-056,
      D-057), and the "Always-read audit frame" candidate row is set to
      graduate (executed at review post-merge hygiene — M35).
- [x] AC6: Prose-guards pin the frame's three-element wording (rulebook) and the
      audit bullet (`/milestone` SKILL.md), each mutation-registered so blanking
      the block reddens its guard.
- [x] AC7: The generic profile's `verify` (the three `python3 -m unittest`
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

- [x] T1: Author the doctrine paragraph + the four-file worked enumeration in
      `skills/shared/tracking-rules.md` (near the Weight caps / GP1-governance
      material). Completeness-only wording; no mass/growth clause.
- [x] T2: Add the judgment bullet to `/milestone` SKILL.md §2 audit applying the
      frame (element-completeness per always-read file + new-surface coverage;
      report-not-fix, never `FAIL`).
- [x] T3: Author prose-guards over the frame wording (T1) and the audit bullet
      (T2); register each in `test_mutation_harness.py`; verify by mutation that
      blanking each block reddens its guard. After the skill-prose edit, grep
      that every nearby guard's asserted substring is still contiguous on one
      physical line (M104).
- [x] T4: Author D-060; record the candidate-row graduation lineage; run the
      three unittest suites from the repo root (each exit code checked, M56) and
      `cairn_validate` — both green.

## Work log

- 2026-07-23: created by /milestone-plan.
- 2026-07-23: branched m108-always-read-audit-frame.
- 2026-07-23: T1 — added `## Always-read governance` frame + four-file worked table to tracking-rules.md; density/validate green.
- 2026-07-23: T2 — added the frame-completeness judgment bullet to /milestone §2 audit; skills/tests 569 green.
- 2026-07-23: T3 — added test_always_read_frame.py (7 asserts) + 10 mutation-harness registrations; harness + all three suites + validate green.
- 2026-07-23: T4 — verified D-060 present (authored at plan), cairn_impact reports no changed principles, no stale DESIGN inventory; all three suites + validate green. Status → review. Candidate-row graduation deferred to review post-merge hygiene (M35).

## Decisions

## Review

**Reviewed 2026-07-23 · PR #106 · no Driving RR (projection-vs-outcome no-ops).**

Acceptance evidence (fresh, by command):
- AC1: `test_always_read_frame.py::TestAlwaysReadFrameRulebook` — the three
  element labels (inflow test / outflow-or-read-bound / attention signal) and
  the D-045-split-decides-legal-outflows clause pinned in `tracking-rules.md`;
  7-assert guard green.
- AC2: same guard, `test_enumerates_the_four_files_with_their_elements` — all
  four worked-table rows (ROADMAP/LESSONS/tracking-rules/DECISIONS, each bound
  to its three elements) pinned; green.
- AC3: `TestAlwaysReadFrameAudit` — the `/milestone` §2 bullet applying the
  frame and its report-never-`FAIL` clause pinned; green.
- AC4: `git diff main..HEAD -- scripts/cairn_validate.py` = 0 lines (no check
  added); `test_frame_is_completeness_only` pins "never measures or gates a
  file's mass"; `cairn_validate` exit 0.
- AC5: `grep ^### D-060 DECISIONS.md` = 1 (authored at plan); candidate row
  still parked (graduates at post-merge hygiene, M35).
- AC6: mutation harness `discover -p test_mutation_harness.py` — 9 tests OK,
  the 10 new M108 blocks each reddening-proven when blanked.
- AC7: skills/scripts/hooks unittest suites + `cairn_validate` all exit 0.

Consistency gate: `cairn_validate` exit 0 (one pre-existing, unrelated
`references staleness` advisory on the rulebook-classification-ledger — not
introduced here). No principle wording changed (`cairn_impact --changed`: none)
→ impact reconciliation skipped. Profile `generic` → no toolchain checks.

Fan-out (three fresh-context lenses, ref-based git): **zero actionable
findings.** [O] diff-bug (Opus) — worked-table claims, guard anchors, and 10
mutation registrations all check out; completeness-only consistent with D-057.
[S] blame-history (Sonnet) — the new rulebook section and audit bullet disturb
no adjacent guard anchor (M104); no D-045/D-053/D-056 contradiction; D-057 not
reopened. [S] prior-review (Sonnet) — GitHub inline-comment probe empty; no
archived `## Review` finding (M74/M76/M95/M100/M103/M104) regressed. Scorer
no-ops (no surviving finding to score). One observation dropped pre-report
(diff-bug, taxonomy): frame prose "~30-milestone weight saga (M84–M98)" pairs
RR03 rec 7's "30 milestones" framing with a 15-ID span — loose but verbatim
from the plan-approved D-060 (already on main, IP4-frozen); left as-is for
record consistency, not diff-introduced.
