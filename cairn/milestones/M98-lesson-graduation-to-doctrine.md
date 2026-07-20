<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M98: Lesson graduation to doctrine — a matured lesson family leaves LESSONS.md whole

- **Status:** review        <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** high   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP1, GP4   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m98-lesson-graduation` · https://github.com/jmgirard/cairn/pull/95   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give `LESSONS.md` a third outflow — graduation to doctrine — by distilling
its matured guard-craft family into a conditionally-read
`skills/shared/guard-doctrine.md` module and retiring the covered lessons.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** re-deriving which `LESSONS.md` items form a matured family (the
classification is the milestone's own evidence, never RR03's inherited 63%);
authoring `skills/shared/guard-doctrine.md` as distilled doctrine; a one-line
rulebook pointer beside the existing `validation-doctrine.md` pointer;
retiring the covered lessons whole from `cairn/LESSONS.md`; a D-entry
annotating D-051 with maturation as a third outflow beside enforcement and
ownership, and distinguishing it from D-051's rejected "separate
graduated-lessons file"; guards over the module and the new criterion, with
mutation registration.

**Out:**
- The anchor-choice discipline for the mutation harness (RR03 rec 8 — "anchor
  on rules, not on scaffolding") → candidate row; M98 builds the home, the
  content waits on rec 8's stated trigger (a pass where re-anchoring cost
  proves material).
- Re-deriving D-049's `LESSONS.md` weight threshold from a post-graduation
  mean → deferred to a later hygiene pass. RR03 rec 12 rejects re-derivation
  from the *pre*-graduation mean as ratifying accretion; a fresh measurement
  becomes legitimate only once the family has left, and it is not this
  milestone's job to bank it.
- Any change to `LESSONS.md`'s caps, one-line format, or capture/harvest
  wiring (D-015, standing) → not in scope; this milestone adds an exit, not a
  ceiling.
- The always-read audit frame (RR03 rec 7) → already banked in M95's work log.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1: The milestone file records a classification of **every** current
      `LESSONS.md` item as graduating or staying, each with its reason, derived
      in this milestone and not carried over from RR03. Items RR03 flagged as a
      possible second tier (`LESSONS.md:19` M51, `:44` M87) are classified
      explicitly either way.
- [ ] AC2: `skills/shared/guard-doctrine.md` exists, stating the graduated
      craft as doctrine rather than a paste of dated lesson lines, and is
      reachable from `skills/shared/tracking-rules.md` "What gets a test" by a
      pointer naming what it covers and when to read it.
- [ ] AC3: Every graduated lesson has a recorded inversion result — where its
      behavioral content landed in the module, and confirmation that deleting
      or inverting that text would change what a compliant agent does. A lesson
      whose content survives only in part is trimmed to its uncovered
      remainder, per D-051.
- [ ] AC4: Each graduated lesson is gone from `cairn/LESSONS.md` — no line, no
      breadcrumb — and the archive summary names what was graduated (D-051's
      tombstone form).
- [ ] AC5: A D-entry annotates D-051 naming maturation as a third outflow, and
      states why graduation is not the "separate graduated-lessons file"
      D-051 rejected as a divergence vector.
- [ ] AC6: New prose-guards pin the module's pointer and the maturation
      criterion, each on one physical line per the label→rule rule, registered
      in `skills/tests/test_mutation_harness.py`; the harness completeness
      meta-test is green.
- [ ] AC7: `cairn_validate` reports `record density` clean for
      `cairn/LESSONS.md` on both axes, and the `verify` slot (all three
      `python3 -m unittest` suites, run from the repo root with exit codes
      checked individually) is clean.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T2, T3
- AC3 → T2, T4
- AC4 → T4
- AC5 → T5
- AC6 → T6
- AC7 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1: Classify every item in `cairn/LESSONS.md` (32 items, 49 lines,
      21,085 chars at 2026-07-19) against the maturation bar; record the
      result here, deciding whether the records-hygiene items form a second
      family or join the guard-craft module.
- [x] T2: Author `skills/shared/guard-doctrine.md` from the classified family
      — distilled principles with their failure modes, never concatenated
      lesson lines. Shape precedent: `validation-doctrine.md`, 93 lines /
      6,036 chars. Record each lesson's inversion result as it is folded in.
- [x] T3: Wire the pointer into `tracking-rules.md` "What gets a test" beside
      the validation-doctrine reference (`:664-670` is the shape).
      Rulebook-reference only — no per-skill read directives (D-031).
- [x] T4: Retire the graduated lessons from `cairn/LESSONS.md` — delete
      whole, trim partial coverage to its remainder, no breadcrumb. Targeted
      Edit replacements, never an ad-hoc string script (M61). Re-measure both
      axes from command output.
- [x] T5: Author the D-entry annotating D-051 (maturation as the third
      outflow; the divergence-vector distinction; D-031 as module precedent).
- [x] T6: Author the guards and register them in the mutation harness —
      registration is per file, and a new `assertIn` in an already-registered
      file still needs its own entry (M53). After adding module prose, grep
      every word an existing guard anchors on (M85).
- [x] T7: Run `cairn_validate` and all three suites from the repo root,
      checking each exit code separately — never piped (M56/M65).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-19: created by /milestone-plan. Gate: module home over synthesis note; T1 re-derives the family boundary rather than inheriting RR03's 63%; fidelity proven by recorded inversion per lesson; the D-entry distinguishes rather than supersedes D-051's rejected graduated-lessons file.
- 2026-07-19: in-progress, branch `m98-lesson-graduation` cut from main at e684c39.
- 2026-07-20: T1's record blew the 150-line body cap (165, shed ≥16) and T1 was checked off against a red gate — corrected here. Two single-pass compressions: Decisions 42→33, Tasks 34→26. The Tasks pass also removed `LESSONS.md:NN` citations that T4 is about to invalidate by deleting those very lines. Further live evidence for the budget-first-drafting candidate row.
- 2026-07-20: T1 done — boundary re-derived independently (M98-D1); guard family is 18 items / 13,316 chars / 66% of item mass, differing from RR03 on six members. Records-hygiene items are a real second family, deferred to a candidate row rather than folded in: the guard family alone leaves 19 lines and 12,749 chars of headroom.
- 2026-07-20: T2 done — `skills/shared/guard-doctrine.md` authored, 7 sections, 191 lines / 9,972 chars against validation-doctrine's 93 / 6,036.
- 2026-07-20: T3 done — rulebook pointer wired in "What gets a test"; re-wrapped after drafting so the module→coverage mapping sits on one physical line, the defect §1 of the new module warns about.
- 2026-07-20: AC3 inversion ledger (source line → module home → inversion result; "restores the named failure" means deleting the module text puts a compliant agent back to committing the specific defect the lesson records).
- 2026-07-20: AC3 — L20 registration-per-file → §2; mutation-registered, blanking reddens (verified). L22 decoration + vary-every-axis → §5, §4; restores vacuous single-axis fixtures. L23 sweep/grep-AC scoping → §7; restores sweeps hitting the milestone's own artifacts. L24 fix-the-wrap → §1, §2, §6; restores loosening an assert to chase a reflow.
- 2026-07-20: AC3 — L26 substring anchor → §1; restores unfalsifiable bare `assertIn`. L27 setUpClass cache → §2; restores a guard reporting false coverage on itself. L31 containment guard both directions → §5; PARTIAL, the `git rebase main` sync remedy is uncovered and stays trimmed in LESSONS. L33 label→rule one line + inversion protocol → §1; mutation-registered, blanking reddens (verified).
- 2026-07-20: AC3 — L35 restatement-unverified → §6; restores shipping a restated rule unread. L36 real-checker-over-real-artifact → §4; restores template/checker pairs that never meet. L40 shared-parser safety claim → §5; PARTIAL, the synthesis-note aging rule is uncovered and stays trimmed. L41 negation-is-a-clause → §5; restores both-direction matcher breakage.
- 2026-07-20: AC3 — L42 vacuous absence-assert → §3; mutation-registered, blanking reddens (verified). L43 numbers derived-wrong/restated-stale → §6; restores inclusive derivation and uncounted encoding sites. L45 two-signal detector + helper defaults → §4; restores undiscriminating fixtures. L47 author-shaped fixture → §4; restores the overlap-collision pass. L48 whole-population under filter → §5; restores a report announcing its blind spot as absent. L49 interacting defects → §5; restores patching one finding in a shared matcher.
- 2026-07-20: T4 done — 16 lessons deleted, 2 trimmed to uncovered remainders (D-051). LESSONS.md 49→33 lines, 21,085→8,219 chars; `record density` WARN→OK. Script-driven deletion verified by `wc -l`, `git diff --stat`, and a full read-back (M61's escape clause).
- 2026-07-20: T5 done — D-055 appended; also updated the LESSONS.md header, the rulebook file-map row, and the retirement rule to name three criteria.
- 2026-07-20: T6 done — `test_lesson_graduation.py` (26 tests), 7 mutation entries registered. Two corrections en route: my own `assertRegex(..., re.M)` passed the flag as `msg` and was silently discarded; and the file-map edit broke M92's existing anchor plus its harness entry, both updated to the three-criterion wording (the rule changed, so this is re-anchoring, not loosening). Maturation line spot-checked by hand transposition → red, restored.
- 2026-07-20: T7 done — skills 487 / scripts 246 / hooks 72, exit 0 each, run separately from the repo root; `cairn_validate` exit 0, all checks passed, no advisories. Status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

### M98-D1 (2026-07-20): the maturation bar, and the family boundary re-derived

**Bar** (conjunctive): (a) **principle, not incident** — transferable craft
about authoring or verifying, not a fact about this repo's tools or runtime;
(b) **stabilized** — extended or consolidated ≥2×, later milestones adding
instances rather than changing the principle; (c) **no existing exit** —
fails D-051 enforcement (no test fails on the mistake) and ownership (no
tracking-file slot holds it).

**GRADUATE — guard-authoring craft** (18 items, 13,316 chars, 66% of item
mass): `LESSONS.md` lines 20, 22, 23, 24, 26, 27, 31, 33, 35, 36, 40, 41,
42, 43, 45, 47, 48, 49.

**STAY — tool/runtime quirk**, D-015's charter, fails (a) (6 items, 3,351
chars): 21, 25, 28, 30, 34, 46 — Bash cwd persistence, hook registration
snapshotting, `Edit --replace_all`, the `gh` quota, hook shipping surfaces.

**STAY — records/process-hygiene craft**, a real second family, deferred
(8 items, 3,493 chars): 18, 19, 29, 32, 37, 38, 39, 44. They pass (a) but
fire at a hygiene or plan gate, not at guard-authoring, so they need their
own read-trigger, not a seat here; 29 and 37 may instead be D-051 ownership
retirements scoped to the milestone shipping those surfaces. Candidate row.

**Not inherited:** RR03 named 20, 22, 24, 26-28, 33, 35, 36, 38, 40-43,
45-48; this differs on six (admits 23, 31, 49; excludes 28, 38, 46).

**Sufficiency:** the guard family alone leaves 31/50 lines and 7,751/20,500
chars — 19 lines and 12,749 of headroom, so deferring the second costs
nothing.

## Review

**PR:** https://github.com/jmgirard/cairn/pull/95 · reviewed 2026-07-20 ·
branch contained `origin/main` tip at review time (no sync needed). This repo
has no `.github/workflows`, so there is no CI to gate on; the three suites are
the whole verification surface.

### Acceptance-criteria evidence (fresh, by command)

- **AC1** — `M98-D1` records all 32 pre-change items in three disjoint sets
  (graduate 18 / quirk 6 / hygiene 8), summing to 32 with an assertion in the
  classification script that the partition is total. `LESSONS.md:19` (M51) and
  `:44` (M87) are both classified explicitly, into the deferred
  records-hygiene family. The entry states its own bar and records the six
  membership differences from RR03, so the derivation is demonstrably
  independent rather than inherited.
- **AC2** — `skills/shared/guard-doctrine.md` exists: **212 lines / 11,815
  chars, 7 `##` sections**. Content is distilled doctrine organised by
  failure mode, not dated lesson lines (zero `- 20YY-MM-DD (M` items in the
  file). Reachable from the rulebook at `tracking-rules.md:768`, in the "What
  gets a test" section, by a pointer naming both its coverage and when to read
  it.
- **AC3** — inversion ledger recorded across five work-log entries covering
  all 18 graduated items, each naming its module destination and the failure
  restored by deletion. Four are additionally proven mechanically (three
  module blocks are mutation-registered and redden when blanked; the rulebook
  maturation line was hand-transposed to a wrong rule and went red, then
  restored).
- **AC4** — `cairn/LESSONS.md` 49 → 34 lines and 21,085 → 8,284 chars, 32 →
  16 items. No `guard-doctrine` breadcrumb anywhere in the file (checked by
  string search). Archive summary naming the graduated family is authored in
  the post-merge hygiene pass, per D-051's tombstone form.
- **AC5** — `D-055` at `DECISIONS.md:1509`, heading annotates D-051. Carries a
  dedicated paragraph distinguishing maturation from D-051's rejected
  "separate graduated-lessons file" on the ground that the source line is
  deleted in the same pass, so the record count never rises.
- **AC6** — `test_lesson_graduation.py`: 26 tests, all pass. 7 entries
  registered in `test_mutation_harness.py`; the registry-wide
  `test_each_registered_guard_fails_when_its_block_is_blanked` and the
  `test_every_prose_guard_is_registered_or_exempt` completeness meta-test both
  pass (9/9 in the harness suite).
- **AC7** — `cairn_validate` exit 0, every check PASS, **`record density` OK**
  (it WARNed `shed ≥586` before this milestone). Suites run separately from
  the repo root with exit codes read individually: skills 487 exit 0, scripts
  246 exit 0, hooks 72 exit 0 — 805 tests.

### Consistency gate

`cairn_validate` exit 0, all checks PASS including `coverage complete` and
`weight caps`. `cairn_impact --changed` reports no changed principles — M98
works under GP1/GP4 but alters neither, so the header slot is accurate and no
reconciliation is owed. Profile is `generic`, whose `consistency-gate` slot
names no toolchain checks, so that half is a clean no-op.

### Self-caught record defect

The T2 work-log line states the module is "191 lines / 9,972 chars"; it is
**212 lines / 11,815 chars**. The figure was measured mid-task and not
re-derived after later edits — a stale restatement, and precisely the defect
§6 of the module this milestone ships warns about ("an amendment fixing a
stale number is itself a restatement; re-derive from a fresh measurement").
The work log is append-only history (D-045/IP4), so the wrong figure stays
where it sits and this line is the correction of record.

<!-- owner: review · exclusive -->
