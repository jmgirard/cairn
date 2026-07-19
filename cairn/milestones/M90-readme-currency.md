<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M90: README currency — the front door catches up with what shipped

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** GP2, GP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m90-readme-currency`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Make the README describe the system that actually shipped in 1.1.0, and make
the profile enumeration a guarded surface so it cannot silently go stale again.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** three documentation gaps (the references-page system in its own
section; cairn never proposing a release; the advisory hook nudges), two stale
claims (README ¶1's three-profile list, the CRAN-only `/cairn-release` row),
the pre-existing `LESSONS.md` omission from the file map, and a
derived positioning guard that requires every shipped profile to appear in
README ¶1 and both `.claude-plugin` manifests.

**Out:**
- Deriving the hook inventory from `hooks/` the way this milestone derives
  profiles → stays the live candidate the `HOOKS` tuple comment already names
  (`skills/tests/test_positioning_guard.py:27-33`); this milestone touches
  only the profile axis.
- `DESIGN.md` edits → already current (four profiles, eight hooks, both note
  templates); no gap found.
- A worked provenance-block example in README → declined at the plan gate as
  reference-manual material; the shipped templates carry it.
- A CONTRIBUTING/PR-template scaffold → the standing "Contributor-facing
  scaffold" candidate row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — README carries a dedicated section on reference pages covering, in
      plain words with no milestone numbers or internal jargon: what a page
      records, when one is owed (the repo relies on a source), that a page
      states where it came from and whether it has been re-checked, and that
      the health check warns about pages never checked or long unchecked.
- [ ] AC2 — README's "What this system deliberately does NOT do" list states
      that cairn never proposes, plans, or nominates a release — release
      timing is the maintainer's declaration.
- [ ] AC3 — README's install section describes the advisory nudges (out-of-band
      idea capture, memory boundary) alongside the blocking guards, so the
      described hook behavior matches what an adopter will actually see fire.
- [ ] AC4 — A guard reads the shipped profile filenames from
      `skills/shared/profiles/` and fails if any shipped profile is absent from
      README ¶1, `.claude-plugin/plugin.json`, or
      `.claude-plugin/marketplace.json`; README ¶1 names all four. Proven by
      running the new guard against `main`'s README (three profiles) and
      requiring red.
- [ ] AC5 — The `/cairn-release` row in the "Which skill, when" table is
      profile-neutral: no CRAN-only framing on a walk that has been
      profile-driven since 1.0.0.
- [ ] AC6 — `LESSONS.md` appears in both the directory tree and the boundary
      rule in "What lives where".
- [ ] AC7 — No existing README guard anchor is degraded by the new prose:
      each phrase asserted by `test_positioning_guard.py` and
      `test_collaboration_boundary.py` against README is verified still
      uniquely matchable, by inversion (relabel/negate in place, require red,
      restore) — not by eye. Every new prose-guard is mutation-registered.
- [ ] AC8 — The `generic` profile's `verify` slot is clean: all three
      `unittest` suites green, and `cairn_validate` exit 0.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T3
- AC2 → T4
- AC3 → T5
- AC4 → T1, T2
- AC5 → T6
- AC6 → T6
- AC7 → T7
- AC8 → T7

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits) -->

- [x] T1 — Write the derived profile guard in
      `skills/tests/test_positioning_guard.py`: read the `*.md` basenames of
      `skills/shared/profiles/`, map each to its human label, assert every one
      appears in README ¶1 and both manifests. Run it before touching README
      and record the red output as AC4's differential evidence.
- [x] T2 — Fix README.md:12's enumeration to name all four profiles; T1 goes
      green. Keep ¶1's existing anchors (`language-agnostic`,
      `toolchain profile`) intact and singular.
- [x] T3 — Author the reference-pages section. Plain words; no page may reuse
      an existing guard anchor phrase (see T7). Add its prose-guard.
- [x] T4 — Add the release-timing promise to the "deliberately does NOT do"
      list, beside the existing auto-release line; add its prose-guard.
- [x] T5 — Extend the install section's hook description to cover the advisory
      nudges; add its prose-guard.
- [x] T6 — Two small currency fixes in one pass: the `/cairn-release` table row
      goes profile-neutral, and `LESSONS.md` joins the directory tree and the
      boundary rule. Guard the boundary rule as a label→member pairing on one
      physical line (`LESSONS.md:34` — pin the label with its members).
- [x] T7 — Anchor-collision sweep and verification: grep every phrase the two
      existing README guards assert, confirm each still occurs exactly once,
      verify by inversion. Register every new prose-guard in
      `test_mutation_harness.py` (per file, ≥1 exemplar block, each anchor on
      one physical line). Run all three suites plus `cairn_validate` from the
      repo root, checking each exit code explicitly.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-19: created by /milestone-plan. Scope drawn from a README audit run during the 1.1.0 release walk; extends M62 (README authoring) and M54 (outward positioning as a guarded surface). Targets the user-declared 1.1.1 release window.
- 2026-07-19: T1+T2 landed in one commit — T1's deliverable is a RED run and committing it alone would leave the branch failing at checkoff, which the verify rule forbids. AC4 differential evidence captured before the fix: `AssertionError: 'Docker image' not found in ...` on README ¶1, both manifests already passing.
- 2026-07-19: T1 hit LESSONS.md:23's wrap trap in the milestone whose own AC7 is anchor hygiene — "Docker image" straddled a line break. Resolved by normalizing whitespace within the read paragraph (label still matched exactly), NOT by loosening the assertion; M64's one-physical-line rule binds mutation blocks and M74's binds label→rule pairings, neither of which this presence check is. README reflowed too.
- 2026-07-19: verified the guard is fail-closed by adding an unmapped profile file — one clean failure (`Lists differ: ['zz-fake-profile'] != []`); tightened the two surface tests to skip unmapped profiles so the dedicated label test owns that signal alone.
- 2026-07-19: T3–T6 authored the four prose changes; new guard file `skills/tests/test_readme_currency.py` (12 tests across 5 classes), 12 mutation registrations added. The profile-enumeration guard is deliberately NOT mutation-registered — its block is a derived list, so blanking one label leaves three passing; its falsifiability rests on the differential red run and the fail-closed unmapped check instead, recorded in the registry comment.
- 2026-07-19: T7 anchor sweep — all 7 pre-existing README anchors still occur exactly once (4 raw, 3 against the lowercased read `test_collaboration_boundary.py:36` uses). Verified by inversion, not by eye: relabelling "The guards only watch this session" → "watch every session" reddened its guard, restored green. The mutation suite passing is a second mechanical proof, since `blank_block` raises on any block matching twice.
- 2026-07-19: verify slot clean at completion — skills 419 / scripts 196 / hooks 72, each exit 0 checked separately (not piped); `cairn_validate` exit 0. Status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

- M90-D1 (plan gate): the profile enumeration becomes a *derived* guard rather than a hand-maintained tuple. README ¶1 went stale at M70 because `test_positioning_guard.py:62-66` pins the framing (`language-agnostic`, `toolchain profile`) but never the list, so shipping a fourth profile left three positioning surfaces green and wrong — the M87 lesson that a number restated in a file's own prose is itself an encoding. A hand-maintained tuple was rejected as the same pattern that just failed. Deriving from `hooks/` on the hook axis stays Out, as its comment already names it a live candidate.

## Review
<!-- owner: review · exclusive -->
