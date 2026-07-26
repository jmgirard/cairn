# M113: Bounded session-start injection — cap-exempt sections read-bounded newest-first, and the active milestone file joins the always-read frame

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP1, IP4
- **Branch/PR:** m113-bounded-session-injection · https://github.com/jmgirard/cairn/pull/113

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

- [x] AC1: A cap-exempt section longer than the per-section budget is injected
      as its newest content only, preceded by a marker naming how much was
      elided and the file path to read for the rest. A section under budget is
      injected whole with no marker.
- [x] AC2: Against this repo's own worst historical case — M95's 23,147-char /
      65-entry work log — the injection contains M95's newest work-log entry
      and not its oldest, inverting today's behaviour. A fixture test pins both
      directions.
- [x] AC3: The per-section budget is ≥ the measured p90 of both cap-exempt
      section types (work log 3,740 chars, review 5,866 chars, over the 111
      milestone files this repo has had live), so ≥90% of each type injects
      whole; the measurement and its date are recorded in this file.
- [x] AC4: With more active milestones than the total budget holds, every one
      still appears with its `## cairn/milestones/…` header and path, and any
      truncation carries an explicit marker. No milestone and no content is
      dropped silently.
- [x] AC5: `tracking-rules.md`'s always-read table carries a fifth row for the
      active milestone file naming all three elements, and the surrounding
      prose states that this is the one always-read surface that leaves the set
      (archived at `done`) and the one split across two of GP1's mechanisms.
- [x] AC6: `verify` slot clean — `python3 -m unittest discover` over all three
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
- 2026-07-25: review round 1 — 4 findings from the [O] diff-bug lens (other two lenses clean); scored 92/85/80/75. AC1 and AC4 fail as written (F1 unbounded+unmarked prose head; F2 milestone headers lost when the ROADMAP alone overflows). Un-ticked both, status -> in-progress. Correction to the 2026-07-25 T7 line above: the skills suite is 610 tests, not 613.
- 2026-07-25: review round 1 fixes — F1 prose rides with the oldest entry plus a line-level second pass; F2 the ROADMAP is truncated (announced) instead of tail-slicing the milestone parts away; F3 heading match now normalizes as scripts/cairn_scripts.py does (lowercased, fence-aware for ``` and ~~~). Six new hook tests, five red first. All three suites green.
- 2026-07-25: review round 2 — 4 findings on the round-1 fixes (incl. R2-F1, a regression I introduced); 3 fixed, 1 rejected with reason. AC1 and AC4 now hold; re-ticked, status -> review. 91 hook tests.
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

_Evidence gathered 2026-07-25 on branch `m113-bounded-session-injection`,
PR #113. Each criterion's box ticked as its line below was recorded._

- **AC1** — `TestSessionContextReadBound` (hooks suite): a 65-entry work log
  yields the marker `newest 11 of 65 entries shown — read cairn/… for the
  rest`; a 6-entry log injects all six with no marker
  (`test_bounded_section_names_what_it_elided_and_where_to_read_it`,
  `test_section_under_budget_is_injected_whole_with_no_marker`, both ok).
- **AC2** — run live against the real M95 file (23,147-char / 65-entry work
  log) in a scratch cairn repo: OLD hook 30,000 chars, newest entry ABSENT,
  oldest present, no marker, cut mid-sentence; NEW hook 24,118 chars, newest
  present, oldest absent, marker as above. Both directions also pinned by
  fixture (`test_long_work_log_keeps_the_newest_entries_and_drops_the_oldest`,
  ok).
- **AC3** — `SECTION_MAX_CHARS = 6000` (`hooks/session_context.py:41`) against
  the measured p90s: 6000 ≥ 3,740 (work log) and ≥ 5,866 (review). Method and
  full percentiles recorded in this file's Decisions section.
- **AC4** — four active milestones over budget: all four keep their
  `## cairn/milestones/…` header and path, the shed ones carrying
  `body elided for the injection budget`; an over-budget ROADMAP alone yields
  `injection truncated`
  (`test_no_active_milestone_vanishes_when_the_total_budget_binds`,
  `test_hard_truncation_is_marked_never_silent`, both ok). Confirmed the old
  behaviour was the defect: those same tests failed against `main`, with M09
  and M10 absent from the injection entirely.
- **AC5** — `skills/tests/test_always_read_frame.py` 9/9 ok, including the
  fifth row pinned whole and the two distinguishing claims each pinned
  separately; all three registered in the mutation harness.
- **AC6** — three suites from the repo root, exit codes checked separately
  (never piped): hooks 80 ok exit 0 · skills 610 ok exit 0 · scripts 280 ok
  exit 0.

**Review round 1 — returned to `in-progress` 2026-07-25.** The three-lens
fan-out (an [O] diff-bug lens, an [S] blame-history lens, an [S]
prior-PR-comments lens) plus an [S] scorer produced four findings; the
blame-history and prior-review lenses each returned zero. Three scored ≥80
and are actioned; one scored below and is logged. AC1 and AC4 do NOT hold as
written on the inputs F1 and F2 name, so their boxes were un-ticked and the
milestone went back rather than to a merge gate. Evidence for AC2, AC3, AC5
and AC6 above is unaffected and stands.

- **F1 (85) — a cap-exempt section whose prose precedes its first `- ` entry
  is neither bounded nor marked.** Every line before the first entry became an
  exempt `head`, uncharged against the budget and uncounted in the total, so
  `kept == total` and the marker never fired. Reproduced: a `## Review` of 40
  prose paragraphs closed by one bullet injected ~17,200 chars against a 6,000
  budget with no marker. Both halves of AC1 fail. Perversely, one bullet made
  it worse than none — a prose-only section falls to line-blocking and bounds
  correctly.
- **F2 (92) — AC4 held only while the ROADMAP itself fit.** The shed loop
  shrank milestone parts only; the ROADMAP was never bounded and the final
  hard truncation cut from the end of the joined context, which is exactly
  where the milestone parts live. Reproduced: a ~28k ROADMAP with four active
  milestones produced an injection with all four milestone headers absent and
  only a generic notice naming no milestone and no path. The ROADMAP's 60-line
  cap counts lines and D-052 deliberately leaves item-line length uncapped, so
  this is reachable without any gate reddening.
- **F3 (80) — the hook's heading match diverged from the cap's own.**
  `scripts/cairn_scripts.py` matches a cap-exempt heading case-insensitively
  (`line[3:].strip().lower()`) and fence-aware for both ``` and ~~~, and says
  it shares those rules with the advisory *on purpose* "or the exemption would
  open a hole the advisory never looks at". The hook compared raw strings and
  ignored fences, so `## Work Log` was cap-exempt to the scripts but injected
  WHOLE by the hook — the exact gap D-063 exists to close — and a `## Work log`
  quoted inside a fence counted as a real section, diluting the real one's
  budget. The code comment claiming "Exactly the sections the 150-line cap
  exempts" was false.
- **F4 (75, below threshold — logged, not actioned as a finding).** The
  equality-match invariant the code names by reference to M55 (`## Reviewers`
  must not match `## Review`) had no test: swapping equality for a prefix
  match left all eight new tests green. Fixed incidentally alongside F3, since
  that fix rewrites the same matcher.

**Review round 2 — the fixes re-reviewed by a fresh [O] diff-bug lens.** Four
more findings, each supplied with an executable reproduction, all verified
here by re-running them against the module rather than by a separate scorer.
Three actioned, one rejected with reason.

- **R2-F1 — a regression the round-1 fix introduced.** The line-level second
  pass had a floor of one line where the block pass has a floor of three
  entries, so a *tighter* budget could yield *less* than a zero budget:
  measured at budget 100-304 the work log showed ZERO entries and reported
  "newest 1 of 42 lines shown", the shown line being blank. Fixed by dropping
  the second pass entirely: the prose head is now charged against the budget
  and elided on its own when it does not fit, so entries are never traded away
  for a preamble. Re-measured across budgets 0/100/304/610/1000/6000: entry
  counts 3/3/3/3/3/19, monotonic, never below the floor.
- **R2-F2 — the ROADMAP truncation reserved its own marker at zero width.**
  `notice.format(0, 0)` reserved two characters for numbers that are three
  digits wide, so the rewritten part could overshoot by the digits it forgot
  and re-fire the whole-context slice that R1-F2 exists to prevent — measured
  at exactly 1 char over, cutting a milestone's path mid-marker. Fixed by
  reserving at full width; a sweep of filler widths 40-339 now overflows at
  none (previously 4).
- **R2-F3 — a negative `room` dropped the `## cairn/ROADMAP.md` heading.**
  The truncation could leave a marker naming no file. Fixed by always keeping
  the heading line.
- **R2-F4 — rejected with reason.** An unclosed fence swallows every following
  heading, silently disabling the read-bound for the rest of the file. That is
  exactly what `_plan_owned_scan` does with the same input, and matching it is
  the whole point of R1-F3; diverging here would reintroduce that finding. The
  same input also fails loud at `cairn_validate` (an over-cap milestone report)
  before the silent path matters, and no file in `cairn/` trips it today.

**AC4's honest bound.** Every active milestone keeps its header and path up to
roughly 50 of them; past ~240 the pointers alone exceed the 30,000-character
budget and headers are lost. That range is unreachable — `ROADMAP.md`'s 60-line
item cap is a `cairn_validate` CHECK, so a repo cannot hold 240 active rows
without failing the gate first. Measured clean at 10, 30, and 50 actives
(0 missing headers).

**Consistency gate.** `cairn_validate` exit 0, all checks passed (16 CHECK,
7 advisory OK). Coverage completeness green — every criterion maps to an
existing task. `cairn_impact --changed` skipped: no `DESIGN.md` principle
changed (the only DESIGN.md edit is the hooks-inventory clause). Toolchain
half of the gate is a clean no-op — the `generic` profile's
`consistency-gate` slot names no toolchain checks.

