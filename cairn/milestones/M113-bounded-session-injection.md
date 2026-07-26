# M113: Bounded session-start injection — cap-exempt sections read-bounded newest-first, and the active milestone file joins the always-read frame

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, IP4
- **Branch/PR:** m113-bounded-session-injection

## Goal

Make the SessionStart injection tell a resuming session the truth about
current state, and give the surface it injects the three governance elements
the always-read frame requires.

## Scope

**In:** `hooks/session_context.py` — the cap-exempt sections of an active
milestone file (`## Work log`, `## Review`) are injected newest-first up to a
measured per-section budget, each carrying a marker naming what was elided and
where to read it; every active milestone appears with its header and path
regardless of total budget; any remaining truncation is marked, never silent.
`skills/shared/tracking-rules.md` — the active milestone file becomes the
frame's fifth row, with the cap-exempt/capped split named as its read-bound.
`cairn/DECISIONS.md` — D-063. Guards: hook tests and the extended frame guard,
mutation-registered.

**Out:** a `cairn_validate` advisory measuring injection size — declined at the
gate on D-057 grounds, recorded in D-063's Rejected, not deferred. Re-injection
on compaction (PreCompact is block-only) → unchanged, no work here. Any change
to what a milestone file *stores* → forbidden by IP4/D-045/D-046; this
milestone reads less, never trims history. Raising `MAX_CHARS` → out; the
allocation below makes the cap degrade gracefully instead.

## Acceptance criteria

- [ ] AC1: A cap-exempt section longer than the per-section budget is injected
      as its newest content only, preceded by a marker naming how much was
      elided and the file path to read for the rest. A section under budget is
      injected whole with no marker.
- [ ] AC2: Against this repo's own worst historical case — M95's 23,147-char /
      65-entry work log — the injection contains M95's newest work-log entry
      and not its oldest, inverting today's behaviour. A fixture test pins both
      directions.
- [ ] AC3: The per-section budget is ≥ the measured p90 of both cap-exempt
      section types (work log 3,740 chars, review 5,866 chars, over the 111
      milestone files this repo has had live), so ≥90% of each type injects
      whole; the measurement and its date are recorded in this file.
- [ ] AC4: With more active milestones than the total budget holds, every one
      still appears with its `## cairn/milestones/…` header and path, and any
      truncation carries an explicit marker. No milestone and no content is
      dropped silently.
- [ ] AC5: `tracking-rules.md`'s always-read table carries a fifth row for the
      active milestone file naming all three elements, and the surrounding
      prose states that this is the one always-read surface that leaves the set
      (archived at `done`) and the one split across two of GP1's mechanisms.
- [ ] AC6: `verify` slot clean — `python3 -m unittest discover` over all three
      suites, each exit code checked separately (M56/M111).

## Coverage

- AC1 → T2, T5
- AC2 → T2, T5
- AC3 → T1, T2
- AC4 → T3, T5
- AC5 → T4, T6
- AC6 → T7

## Tasks

- [x] T1: Record the measured percentiles and the chosen per-section budget in
      this file's Decisions section, with the method (final live revision of
      every `cairn/milestones/M*.md` in git history) and the date.
- [x] T2: In `hooks/session_context.py`, add a `bounded_tail` helper: split a
      section body into blocks (`- ` entries where present, else lines), take
      blocks from the tail until the budget is spent, floor of the newest 3,
      and return the text plus the elided/total counts for the marker.
- [x] T3: Rework `build_context` allocation (`hooks/session_context.py:53`):
      reserve the ROADMAP and every active milestone's capped sections plus its
      floor entries first, distribute the remainder across cap-exempt sections,
      and replace the silent `[:MAX_CHARS]` tail chop (`hooks/session_context.py:80`)
      with a marked truncation.
- [x] T4: Add the fifth row and its framing sentence to `tracking-rules.md`'s
      "Always-read governance" (D-063, landed with this plan, is the record).
- [x] T5: Extend `TestSessionContext` in `hooks/tests/test_hooks.py` — the M95
      fixture (newest present, oldest absent, marker text), an under-budget
      section injected whole, and the multi-active-milestone case.
- [x] T6: Extend `test_always_read_frame.py` with the fifth row, rename
      `test_enumerates_the_four_files_with_their_elements`, and update its
      mutation registration (`skills/tests/test_mutation_harness.py:2059`).
- [x] T7: Run the three suites from the repo root, checking each exit code
      separately; `cairn_validate` as its own `&&`-gated step (M111).

## Work log

- 2026-07-25: created by /milestone-plan.
- 2026-07-25: T1 — budget set at 6,000 chars from the measured p90 of both cap-exempt section types (111 files); recorded in Decisions with the method.
- 2026-07-25: T5 then T2+T3 — 8 hook tests written first (7 red, incl. M09/M10 vanishing from the injection under the old chop), then bounded_tail + the reallocated build_context turned them green; all three suites clean.
- 2026-07-25: T4/T6 — fifth frame row + its two distinguishing claims in tracking-rules.md; guard extended (row, both claims, renamed four-files test) and re-registered.
- 2026-07-25: the new row's `work-log format` mention created false coverage in test_milestone_cap_exemption (bare-label anchor would survive deleting the advisory rule); mutation harness caught it — re-anchored that assert in the rule's own sentence. M104's pattern, second occurrence.
- 2026-07-25: live before/after on the real M95 file (65 entries): old hook 30,000 chars, newest entry ABSENT, oldest present, no marker, cut mid-sentence; new hook 24,118 chars, newest present, oldest absent, marker 'newest 11 of 65 entries shown'.
- 2026-07-25: T7 — hooks 80 / skills 613 / scripts suites all green (exit codes checked separately), cairn_validate green; DESIGN.md hook-inventory clause updated. Status → review.
- 2026-07-25: minor amendment — T5's hook tests are written before T2/T3 (tests-first), not after; task order in the file unchanged, execution order noted here.

## Decisions

- 2026-07-25 — **Per-section budget: 6,000 characters, shared by both
  cap-exempt section types.** Measured over the final live revision of every
  `cairn/milestones/M*.md` in git history (111 files, measured 2026-07-25):
  `## Work log` p50 1,211 · p75 2,476 · p90 3,740 · max 23,147 chars (M95,
  65 entries); `## Review` p50 2,283 · p75 3,611 · p90 5,866 · max 8,560
  chars. 6,000 clears both p90s, so ≥90% of each section type injects whole
  and only genuine outliers meet the bound. Neither distribution is censored
  — both sections are cap-exempt, so nothing jams against a limit and the
  percentiles are a legitimate budget basis (M99). A single shared figure
  rather than one per section type: the rule is derived from the cap
  ("cap-exempt sections are read-bounded"), and two numbers would invite the
  reader to look for a distinction the doctrine does not make.
- 2026-07-25 — **Degradation order: `in-progress`, then `review`, then
  `blocked`.** AC4 requires that no active milestone disappear when the total
  budget binds, which means something must give first. Injecting in that
  status order and shrinking from the end drops the least-current milestone's
  detail first. Discovered at T3; not a plan change — AC4 demands graceful
  degradation and this is what it degrades by.

## Review
