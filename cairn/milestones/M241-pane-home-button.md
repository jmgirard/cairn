# M241: A ⌂ Button in the cairn pane clears the conversation and brings the pane to the front

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing, because every adopter sees the Button in the cairn pane
- **Branch/PR:** m241-pane-home-button, https://github.com/jmgirard/cairn/pull/251

## Goal

The cairn pane's first line carries a ⌂ Button that clears the conversation and opens the pane, which brings a hidden pane forward.

## Scope

**In:** A `home` Button, labeled ⌂, on the pane's first line before ↻,
shown while no cairn skill's step is set. Its press runs the built-in
`clear`, guarded as the Clear press is but with no `ended` check. At the
session end of that `/clear`, the mod calls `$.ui.open` for the pane. The
pane's Next line loses its Clear Button. The band keeps its own Clear. The
press is the person's consent to drop the conversation, as a press of Clear
is (IP3, DESIGN.md's M221 note). README, DESIGN, and CHANGELOG describe the
change.

**Out:** A close and reopen of the pane, or a pane reset with no clear.
The user chose a clear with the pane brought to the front at the question
set. The two-click press on an unfocused pane stays with the candidate row
"Pane Button takes two clicks (upstream)". The older pane gaps stay with
the "Pane edges (M238 review)" row.

## Acceptance criteria

- [x] AC1: While no cairn skill's step is set, `paneLines` gives the pane's first line the Buttons `home` then `refresh`. The first line is the first milestone's head line, or the `no active milestone` line. register.tsx draws `home` as a `secondary` Button labeled `⌂` with key `cairn-pane-home`. While a step is set, the first line carries `refresh` alone. Mod tests cover both states on both kinds of first line.
- [x] AC2: A free press of ⌂ runs the built-in `clear` command once, with empty args. A press is free when no step is set, no Button's run is in flight or held, and no earlier ⌂ press is pending. A drawn ⌂ press runs no command in three guarded cases. They are a run in flight, a held `Plan` or `Implement` command, and a pending ⌂ press. While a step is set, ⌂ is not drawn (AC1). Mod tests assert the `$.command.run` calls in the free case and in each of the three guarded cases.
- [x] AC3: At the session end of a ⌂ press's `/clear` (reason `clear`), the mod calls `$.ui.open` for the pane exactly once. A session end with any other reason after a ⌂ press calls no open. A ⌂ press whose `/clear` run is refused leaves no pending open, so a later `clear` end from another Button calls no open. A session end with no ⌂ press pending calls no open. Mod tests assert the open calls in each of these four cases.
- [x] AC4: The pane's Next line carries no Clear Button, with `ended` true or false. It carries Status after the next-step Button as before. The band's Clear Button draws and presses as the existing band tests assert, and those tests pass.
- [x] AC5: A live look in the desktop app shows ⌂ just before ↻ on the pane's first line. A press of ⌂ there clears the conversation, and the cairn pane stays open. The operator accepts the look.
- [x] AC6: Three texts describe ⌂ and its press and say that the pane's Next line has no Clear. They are README.md's and DESIGN.md's text on the pane's current behavior, and a new CHANGELOG.md entry. Earlier CHANGELOG entries and the history in DESIGN.md do not change. A reader of the README and DESIGN lines that describe the pane's Next line finds no claim that it carries Clear.
- [x] AC7: The profile's five `verify` checks pass.

## Coverage

- AC1 → T1, T2
- AC2 → T2
- AC3 → T2
- AC4 → T1
- AC5 → T4
- AC6 → T3
- AC7 → T1, T2, T3

## Tasks

- [x] T1: pane.ts: add `home` to `PaneButton` and `HOME_LABEL = '⌂'`. Give the first line `['home', 'refresh']` while `acts` is true, and `['refresh']` otherwise. Drop `clear` from the Next line and update the `paneLines` comments. Update pane.test.tsx.
- [x] T2: register.tsx: add `PANE_BUTTONS.home` and route `home` in `pressPane` to a new `pressHome`. It returns at once while `busy()`, a step, or its own pending mark is set. Otherwise it sets the mark and runs `clear` through `run`, and a refused run clears the mark. `session.end` reads the mark and clears it at any end. On reason `clear`, it opens the pane unawaited, as the `heldRun` path runs its command. Write the AC2 and AC3 tests.
- [x] T3: README, DESIGN (current-behavior text and the `hooks/status/` entry), and a CHANGELOG entry.
- [x] T4: Live look in the desktop app (granted at the question set).

## Work log

- 2026-10-10: created by /milestone-plan.
- 2026-10-10: question set: what one ⌂ press does — clear the conversation, then open the pane so it comes to the front.
- 2026-10-10: question set: the pane's Clear Button — remove it from the pane. The band keeps its Clear.
- 2026-10-10: question set: ⌂ during a cairn skill's run — hidden, as Next and Status are.
- 2026-10-10: question set: a live look in the desktop app at implement — granted.
- 2026-10-10: plan gate chose a `/clear` and an open over closing and reopening the pane, because a Button's `/clear` keeps the pane open (M222). Falsified by a live look where the pane closes or moves after a Button's `/clear`.
- 2026-10-10: plan chose to open at the `clear` session end, not after `run` resolves. A Button's `/clear` run can fail to settle (M216, M221 T1). Falsified by a probe where the run always resolves before the session end.
- 2026-10-10: criteria audit (full mode, fresh Opus reader) returned 10 findings, all fixed in this file. AC2 split held and in-flight runs and added a second ⌂ press. AC3 added a refused run. AC4 named the band tests. AC5 dropped the refill claim, which holds without M241, and the recording clause. AC6 left CHANGELOG history alone and replaced a grep with a reader's check. The open's effect was narrowed to a pane behind another tab.
- 2026-10-10: inbox sweep: no open issues and no open PRs on jmgirard/cairn.
- 2026-10-10: collision check: M219 shipped the pane's Clear, which this milestone removes, as the user chose. M222 shipped the pane kept open across a Button's `/clear`. No candidate row or D-entry overlaps a ⌂ Button.

- 2026-10-10: substantive amendment: AC2 drops the set-step press from its tested guards. ⌂ is not drawn while a step is set (AC1), and `ui.press` presses only a drawn Button. `pressHome` keeps its step check, and no criterion promises it. The deliverable the user sees does not change.
- 2026-10-10: re-audit: AC2 (full) — the "free" definition contradicted the pending-⌂ guard, and the press-time step check had no promise. Fixed the definition, and kept no promise for the step check (narrower).
- 2026-10-10: re-audit: AC2 (full) — "pending" is not defined. The tests covered one in-flight run, one held label, and one kind of first line. Wording kept as audited. The tests now cover Status and Resume runs in flight, both held labels, and both kinds of first line.
- 2026-10-10: implement chose a module mark `homeRun` beside `heldRun` over an atom. A reload must drop a pending press, as it drops `heldRun`. `paneLines` lost its `ended` parameter, which only the pane's Clear read.
- 2026-10-10: T1, T2 done. ⌂ draws before ↻ while no step is set, a press runs `/clear`, and a `clear` end opens the pane. The pane's Clear is gone. 13 old pane tests changed to the new Button lists, and 17 M241 tests added. Mod tests 1625 pass, and all five verify checks pass.
- 2026-10-10: T3 done. README, DESIGN, and a CHANGELOG New entry describe ⌂ and the Next line with no Clear. DESIGN's Known issues line on the pane's Clear is corrected in place. Code comments no longer say the open brings a pane forward, since the API says only that an open id retitles. The live look checks it. The T1/T2 line's "13 old pane tests" was not counted.
- 2026-10-10: T4 stop for the live look. A desktop Code session keeps the mod it loaded at its start (LESSONS M195), so the operator opens a new Code session in this checkout on `m241-pane-home-button`.
- 2026-10-10: T4 done. Live look in a new desktop Code session: the operator saw ⌂ just before ↻, a press cleared the conversation with the pane still open, and the operator accepted the look. Whether the open brings a pane behind another tab forward was not reported.
- 2026-10-10: claim audit: 55 claims read, 3 corrected — register.tsx, CHANGELOG.md, pane.test.tsx
- 2026-10-10: The corrections: the `openHome` comment states what the API documents for an open of an open pane. The CHANGELOG adds the background-work wait. An old pane test's comment drops Clear, and its call drops the stray fourth argument. The reader re-read the three, and they hold. Verify passes: mod tests 1625, both Python suites, both validates.
- 2026-10-10: step-7 approval: m241-pane-home-button approved for merge

## Decisions

## Review

Evidence run 2026-10-10 on the code as of `3aa63d1`. Main has not moved since the branch was cut.

- AC1: `claude plugin test .` 1625 pass, 0 fail. The 5 "first line carries ⌂ before ↻" tests pass: single-in-progress and no-active, terminal and desktop, check ⌂ then ↻ with key `cairn-pane-home`, `secondary`, label ⌂, a `-home` Box that does not shrink, ↻ alone after a skill prompt, and ⌂ back after the Stop. The `paneLines` unit test checks `['home','refresh']` while acting and `['refresh']` otherwise.
- AC2: same run. The free case passes on both kinds of first line (`[{clear, ''}]`). The guarded cases pass: a Status run and a Resume run in flight, a held command for both `Plan` (all-waiting) and `Implement` (candidates), and a pending ⌂ press (a second ⌂ and a Status press add no run). Each asserts the exact `$.command.run` list.
- AC3: same run. The 4 open tests pass: a `clear` end after a press adds exactly one open of pane `cairn`, and a later `clear` end adds none. An `other` end after a press adds none. A refused `/clear` (toast names `/clear`) leaves no open at the next `clear` end. A `clear` end with no press adds none.
- AC4: same run. "a running skill hides Status, and its end adds no Clear" passes on both surfaces: after a Stop (`ended` true) and after a typed prompt (`ended` false) the Next line holds Next then Status, with no `cairn-pane-clear`. The `paneLines` test gives the Next line `['status']`. The 28 band tests named M216 (the band's Clear) pass.
- AC5: the T4 work-log line, 2026-10-10: in a new desktop Code session on this branch the operator saw ⌂ just before ↻, a press cleared the conversation with the pane still open, and the operator chose "Looks right, accept" at the live-look chip.
- AC6: read on 2026-10-10 after the review fixes. README.md lines 286-300 (the pane's Next line) say "The Next line has no `Clear` button" and point to ⌂. README lines 340-350 describe ⌂ and its press. DESIGN.md lines 419-440 describe the Next line with `status` alone, and ⌂ and `pressHome`. The `hooks/status/` entry names ⌂ (M241). The new CHANGELOG New entry describes ⌂ and says the Next line no longer carries Clear. `git diff main...HEAD -- CHANGELOG.md` shows that entry's added lines only, so earlier entries are unchanged. DESIGN's history (the entry's M219 list) is unchanged. No README or DESIGN line on the pane's Next line claims Clear.
- AC7: run on the tree of `58c4b7e`, each exit code read: `python3 -m unittest discover -s scripts/tests` 406 tests OK (21 skipped), `hooks/tests` 174 OK, both `claude plugin validate` checks pass, and `claude plugin test .` 1627 pass, 0 fail.

Consistency gate: `cairn_validate.py` all checks passed. Principles touched is IP3, which this milestone works under and does not change, so `cairn_impact` is skipped. Profile slot: verify passes (AC7). The marketplace validate prints no `version` warning. The CHANGELOG has the entry (AC6), with no milestone number in it.

spawned: diff-bug, blame-history, prior-review

- diff-bug #1: a ⌂ `/clear` with no session end leaves `homeRun` set and every action press dead with no toast — fix now (DESIGN Known issues line), fixed 58c4b7e
- diff-bug #2: two ⌂ presses in one tick both pass `busy` and both run `/clear` — fix now (mark set before the first await, new test seen red first), fixed 58c4b7e. The same pattern in the other presses goes to "⌂ edges (M241 review)".
- diff-bug #3: a typed `/clear` takes a queued ⌂ press's open — follow-up, "⌂ edges (M241 review)"
- diff-bug #4: the open can bring back a pane closed during the wait — follow-up, "⌂ edges (M241 review)"
- diff-bug #5: `openHome` uses the ended session's `$`, unchecked live — follow-up, "⌂ edges (M241 review)"
- diff-bug #6: title and Goal say the pane comes forward, which nobody saw — follow-up, "⌂ edges (M241 review)". The Goal is plan-owned and stays, and the archive summary says it was not seen.
- diff-bug #7: README "opened again" reads as a visible effect, and README omits the idle-wait for ⌂ — fix now (README says a shown pane stays as it is, that the tab case was not checked, and the idle wait), fixed 58c4b7e
- diff-bug #8: AC3 tests only reason `other`, which also marks a reopen — fix now (a `resume` case), fixed 58c4b7e
- diff-bug #9: in-flight tests use one fixture on desktop, and a work-log line claims both first lines — reject, false: that line's "both kinds of first line" names the free case, which covers both.
- diff-bug #10: the M221 pane test lost its `endSkill` — fix now (restored), fixed 58c4b7e
- diff-bug #11: the AC3 `isShown` check rests on the fake `ui.open` — reject, false as a defect: the test comment says it checks the call only.
- diff-bug #12: a rejecting `next(e)` at a `clear` end drops the open — follow-up, "⌂ edges (M241 review)"
- blame-history #1: ⌂ shows at every idle moment, where the pane's Clear showed only after a skill's end — reject, planned change: the question set chose ⌂ always shown outside a run and the pane's Clear removed.
- blame-history #2: a queued ⌂ `/clear` freezes every action press until its end — fix now, as diff-bug #1, fixed 58c4b7e
- blame-history #3: a non-`clear` end drops the ⌂ mark with no message — follow-up, "⌂ edges (M241 review)"
- blame-history #4: `openHome` has no `found` check or refresh, and its order against the start hook is untested — follow-up, "⌂ edges (M241 review)"
- blame-history #5: the "front" promise in the title and Goal is not shown — follow-up, as diff-bug #6
- blame-history #6: no test for a narrow first line with ⌂ and ↻ — reject, false: the M208 44-column test checks the `-home` and `-refresh` Boxes do not shrink.
- blame-history #7: stale text in register.tsx (Clear in the layout comment), DESIGN (`CLEAR_LABEL` read by the pane), and README ("each press runs the band's button of the same name") — fix now for the first two, fixed 58c4b7e. Reject the README part, false: Status is the band's Status.
- blame-history #8: no regression in `heldRun`, `runs`, or the M222 reopen — noted.
- prior-review #1: `openHome` opens before the new start's refresh, against M222's register-before-reopen order — follow-up, "⌂ edges (M241 review)"
- prior-review #2: an older Unreleased CHANGELOG bullet names "both Clear Buttons" — reject, false: each sentence there is still true (the live check covered both, and the band's Clear keeps the pane), and AC6 keeps earlier entries unchanged.
- copilot: hooks/status/register.tsx:1074 — fix now (the race of diff-bug #2), fixed 58c4b7e
- copilot: review body, "the milestone needs the PR URL" — noted: the header records PR #251 in the next push.
- Copilot level: Lite (set by GitHub's settings)
