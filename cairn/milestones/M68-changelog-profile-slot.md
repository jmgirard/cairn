<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M68: Changelog profile slot — required seventh slot, "none" legal

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** m68-changelog-profile-slot · https://github.com/jmgirard/cairn/pull/66   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Add `changelog` as a required seventh toolchain-profile slot — the repo's
changelog file name or "none" — so `/hotfix`, `/cairn-release`, and the
consistency-gate read one declaration instead of each improvising the name.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `_REQUIRED_SLOTS` + docstring in `scripts/cairn_validate.py`; the
tracking-rules "Toolchain profiles" slot list (six→seven) incl. the "none"
semantics; `## changelog` in all three reference profiles (r-package
`NEWS.md`, python `CHANGELOG.md`, generic declare-or-none) with their
release-walk and consistency-gate changelog bullets repointed at the declared
file; `/hotfix` step 5 and `/cairn-release` wording reading the slot
(today's inference demoted to the absent-PROFILE fallback); this repo's
`cairn/PROFILE.md` declaring `CHANGELOG.md`; `DESIGN.md` six→seven; guard +
fixture updates (`SLOTS` tuple, `Tree.build()`, mutation registrations).

**Out:** cairn-init repair machinery for the new FAIL — a missing-slot FAIL
in an adopting repo is an ordinary one-line `/milestone` audit fix (stated in
D-040), no scaffolder change; validating that the declared file exists on
disk — "none" is legal, files may be created later, and a wrong declaration
surfaces at hotfix/release time; the repair passes themselves — they happen
in each adopting repo at its next `/milestone`.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [x] AC1: `cairn_validate` FAILs a PROFILE.md whose `## changelog` slot is
      missing or empty and passes one declaring a file name or "none" —
      scripts-suite fixture tests for present/missing/empty.
- [x] AC2: all three shipped reference profiles and this repo's
      `cairn/PROFILE.md` define a non-empty `## changelog` (`NEWS.md` /
      `CHANGELOG.md` / declare-or-none instructions / `CHANGELOG.md`), each
      under the <120 cap — `test_shipped_reference_profiles_are_valid` green
      + full `cairn_validate` green on this repo.
- [x] AC3: the three consumers read the declaration — `/hotfix` step 5 names
      the changelog slot with the NEWS/CHANGELOG inference as the
      absent-PROFILE fallback only; the r-package and python release-walk and
      consistency-gate bullets reference the declared changelog rather than
      hardcoding the file name again — guard asserts in the skills suite.
- [x] AC4: the tracking-rules slot list names seven slots and states the
      "none" semantics (hotfix skips the entry; the release-walk skips
      consolidation and derives the bump from commit history) — guard
      assert, mutation-registered.
- [x] AC5: no live "six slots" claim survives repo-wide (case-insensitive
      grep) outside history files (DECISIONS, archives, legacy, reviews) and
      this milestone's own tracking record.
- [x] AC6: both suites green from the repo root —
      `python3 -m unittest discover -s scripts/tests` and
      `python3 -m unittest discover -s skills/tests` (this repo's verify),
      incl. the mutation harness covering the new prose guards.

## Coverage
<!-- owner: plan · create/amend-via-gate; review reads to fence evidence -->

- AC1 → T1
- AC2 → T3
- AC3 → T4, T5
- AC4 → T2, T5
- AC5 → T6
- AC6 → T1, T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: `cairn_validate.py` — add `changelog` to `_REQUIRED_SLOTS`; update
      the docstring six→seven; extend the shared `Tree.build()` PROFILE.md
      fixture (M24 lesson) and add present/missing/empty fixture tests in
      `scripts/tests/`.
- [x] T2: tracking-rules "Toolchain profiles" — "Six slots:" → seven, add the
      changelog slot bullet with the "none" semantics kept on one physical
      line (M64 reflow lesson); `DESIGN.md` Purpose six→seven.
- [x] T3: the three reference profiles gain `## changelog` (r-package:
      `NEWS.md`; python: `CHANGELOG.md`; generic: declare-here-or-"none");
      repoint their release-walk + consistency-gate changelog bullets at the
      declared file; add the slot to this repo's `cairn/PROFILE.md`
      (`CHANGELOG.md`).
- [x] T4: consumers — `/hotfix` step 5 reads the slot (inference becomes the
      absent-PROFILE fallback per tracking-rules "Toolchain profiles");
      `/cairn-release` wording reads the declared changelog.
- [x] T5: guards — extend `SLOTS` in `skills/tests/test_toolchain_profiles.py`
      + new slot/consumer/doctrine asserts; mutation-register the new prose
      guards (M53/M54: per-file `Mutation(...)` entries, run via discover).
- [x] T6: sweep — `git grep -i` the whole repo for surviving six-slot claims
      (M48 whole-repo rule), exempting history files and this milestone's own
      record (M62 lesson).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-16: created by /milestone-plan — promoted early from the RR01 rec 11/Q2 candidate row (pre-v1.0 schema argument), user-approved at the scope chip; shape decisions in D-040.
- 2026-07-16: minor amendment — T1+T3 folded into one checkpoint with T5's SLOTS-tuple edit (schema/profiles/guard-tuple are atomically coupled: each alone reds a suite — M46 fold-don't-defer).
- 2026-07-16: T1+T3 done; mutation harness caught "commit history" wording giving the generic release-walk guard false coverage — reworded to "git history"; all suites green.
- 2026-07-16: T2 done — seven-slot list + changelog bullet (none-semantics, one physical line) in tracking-rules; DESIGN six→seven.
- 2026-07-16: T4 done — /hotfix step 5 reads the slot (none → skip; absent PROFILE → infer), /cairn-release steps 1–2 read the declared changelog (none → git history / skip consolidation).
- 2026-07-16: T5 done — TestChangelogSlot (5 guards over profiles/rulebook/consumers) + 6 Mutation entries; skills suite 219 OK.
- 2026-07-16: T6 done — sweep caught one straggler (tracking-rules file-map row "six slots", the M48-class miss); remaining hits are this milestone's own record (exempt per AC5).
- 2026-07-16: all tasks done; three suites + cairn_validate clean; status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55). -->

Evidence (2026-07-16, all fresh-run this review):

- AC1: scripts suite 86 OK incl. `test_changelog_slot_missing_fails` +
  `test_changelog_declares_file_passes` (verbose run shows both ok).
- AC2: `test_all_profiles_define_all_seven_slots` +
  `test_shipped_reference_profiles_are_valid` ok; `wc -l`: generic 63,
  python 108, r-package 101, cairn/PROFILE.md 63 — all < 120 (D-034);
  `cairn_validate` on this repo: all checks passed.
- AC3: `TestChangelogSlot` hotfix/release/consistency-gate guards all ok
  (verbose run).
- AC4: `test_rulebook_states_the_none_semantics` ok; mutation-registered
  (harness green inside the 219-test skills suite).
- AC5: exemption-scoped `git grep -inE "six (known|slots)|all six|the six
  slots"` → no hits outside this milestone's record (exit 1).
- AC6: scripts 86 OK · skills 219 OK · hooks 55 OK, from the repo root.

Consistency gate: `cairn_validate` exit 0 (all pass). No IPn/GPn text
changed (GP3 worked-under only) → `cairn_impact --changed` skipped. Generic
profile's consistency-gate slot names no toolchain checks → no-op.

Note: AC4's parenthetical says "derives the bump from commit history"; the
shipped bullet says "git history" (work-log 2026-07-16 mutation fix). The
criterion mandates the semantics, not that literal token — identical meaning,
recorded here rather than silently passed.
