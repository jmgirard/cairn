# M242: A ✎ Button on each candidate row in the cairn pane plans that candidate

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP3
- **Resolves:** —
- **Surface tier:** user-facing, because every adopter sees the Button in the cairn pane
- **Branch/PR:** m242-pane-candidate-plan

## Goal

Each candidate row in the cairn pane carries a ✎ Button whose press starts `/milestone-plan` with the row's short title.

## Scope

**In:** A `plan` pane Button, labeled ✎, at the right end of each candidate
line whose short title is not empty. It shows while no cairn skill's step
is set, as ⌂ does. Its press runs `/clear` first. In the cleared
conversation it then runs `/cairn:milestone-plan <title>`, through the
held-run path of the `Plan` Button (M221). `<title>` is the row's short
title as `candidateRows` reads it: the text before its first `: `, with no
priority token. The press is the person's consent to drop the
conversation, as a press of Plan or ⌂ is (IP3, DESIGN.md's M221 note). The
press also checks the stored candidate rows and a set step, as the other
pane presses do. README, DESIGN, and CHANGELOG describe it.

**Out:** Buttons on the Workable, Waiting, Blocked, or Hotfixes lines. A
press that reads the ROADMAP file again before it runs. The two-click press
on an unfocused pane stays with "Pane Button takes two clicks (upstream)".
The held-run edges stay with "⌂ edges (M241 review)".

## Acceptance criteria

- [ ] AC1: While no cairn skill's step is set, `paneLines` gives the Button `plan` to each candidate line whose short title is not empty. While a step is set, no candidate line carries it. A candidate line with an empty short title never carries it. register.tsx draws `plan` as a `secondary` Button labeled `✎`. Its key carries the line's index, so two rows with one title draw two keys. Mod tests cover both states. Their rows are a high, a normal, a low, and an empty-title row, and two rows that share a title.
- [ ] AC2: A free press of a candidate's ✎ runs the built-in `clear` command once, with empty args. The press holds `cairn:milestone-plan` with that row's short title as its args. At the session end of that `/clear` (reason `clear`), the mod runs the held command once. When no other Button's run is in flight or held, and no ⌂ press is pending, a press is free. Mod tests assert the `$.command.run` calls of a free press and of its `clear` end.
- [ ] AC3: A press runs no command in each of three guarded cases. They are a run in flight, a held `Plan` command, and a pending ⌂ press. A second ✎ press in the same tick as a free press runs no second `clear`. Mod tests plant each case and assert the `$.command.run` calls.
- [ ] AC4: On a candidate line, the title's Box has `flexGrow` 1 and `minWidth` 0, and its Text keeps `truncate-end`. The ✎ Button sits after it in its own Box with `flexShrink` 0. Mod tests assert these props on a short-title line and on a line whose title is longer than 44 columns.
- [ ] AC5: The live look runs in circumplex, a cairn repo with no `in-progress` or `review` milestone. There the idle pane shows ✎ at the right end of each candidate row. A press clears the conversation and starts `/cairn:milestone-plan` with that row's short title. The operator stops that plan at its question set and accepts the look.
- [ ] AC6: Three texts describe ✎ and what its press runs. They are README.md's and DESIGN.md's text on the pane's current behavior, and a new CHANGELOG.md entry. Earlier CHANGELOG entries and the history in DESIGN.md do not change.
- [ ] AC7: The profile's five `verify` checks pass.

## Coverage

- AC1 → T1, T2
- AC2 → T2
- AC3 → T2
- AC4 → T1
- AC5 → T4
- AC6 → T3
- AC7 → T1, T2, T3

## Tasks

- [x] T1: pane.ts: add `plan` to `PaneButton` and a ✎ label. Give each candidate line with a non-empty title `['plan']` while `acts` is true, and `grow` so its title Box takes the free width. Carry the line's index and short title for the press, and say in the `PaneLine` comment which field holds which. Update the `paneLines` comments and pane.test.tsx.
- [x] T2: register.tsx: add `PANE_BUTTONS.plan`, keyed by the line's index. Route `plan` in `pressPane` to a new press. It sets `heldRun` before its first await, as `pressHome` sets its mark (M241 review). Two cases take the hold back: a set step, and stored candidate rows with no row of the drawn title at that index. Otherwise it runs `clear` through `run`, and a refused run drops the hold. Write the AC1–AC3 tests.
- [x] T3: README, DESIGN (current-behavior text and the `hooks/status/` entry), and a CHANGELOG entry. ✎ has no band twin, so the README's sentence on presses that run the band button's command does not cover it.
- [x] T4: Live look in circumplex (granted at the question set).

## Work log

- 2026-10-11: created by /milestone-plan.
- 2026-10-11: question set: what a ✎ press does with the conversation — clear it, then plan, as the Plan Button does.
- 2026-10-11: question set: the Button's label — ✎.
- 2026-10-11: question set: a live look in circumplex at implement — granted, and the operator stops the started plan at its question set.
- 2026-10-11: plan chose the row's short title as the press's args over the full row text. The full text needs a new pane state field and shape tag, and the plan's collision check finds the row from its title. Falsified by a live plan that does not find its candidate row from the title.
- 2026-10-11: plan chose the stored candidate rows for the press's check over a new read of the ROADMAP file. A refresh redraws the Button, so no test reaches a stale press, and the other pane presses read stored state. Falsified by a press in a real session that plans a row the ROADMAP no longer holds.
- 2026-10-11: criteria audit (full mode, fresh Opus reader) returned 7 findings, all fixed in this file. AC5 moved to circumplex, since this repo's pane hides candidates while M242 is active. AC3 dropped the set-step and row-gone cases, which no drawn Button reaches, and split held `Plan` from pending ⌂. AC1 keyed the Button by index and drew no ✎ for an empty title. AC4 added `flexGrow` and a short-title line. The Goal and AC2 name the short title as `candidateRows` reads it. T3 keeps the README's band-twin sentence off ✎.
- 2026-10-11: inbox sweep: no open issues and no open PRs on jmgirard/cairn.
- 2026-10-11: collision check: M207 shipped the candidate lines, M218 and M221 the Plan Button and its held run, M241 ⌂. No candidate row or D-entry overlaps a per-row Button. "⌂ edges (M241 review)" holds held-run edges that this press shares.
- 2026-10-11: branch m242-pane-candidate-plan cut from main at 2e6f86a. Untracked `cairn-probe.log` and `tsconfig.json` are not this milestone's and stay unstaged.
- 2026-10-11: T1 and T2 done in one checkpoint. `PaneLine` gained `title`. A candidate line carries `target` (its index) and `title` while it shows ✎, and every candidate line grows. `pressCandidate` holds `cairn:milestone-plan` in `heldRun`. 14 new mod tests, and two older Button-list and grow checks now allow candidate lines. Mod tests 1643, all five verify checks green.
- 2026-10-11: planted an empty-title ✎ and a hold set after the first await. The AC1 tests and the same-tick test failed, and the files were restored.
- 2026-10-11: paused at the user's request after T2. T3 (docs) and T4 (live look in circumplex) remain.
- 2026-10-11: resumed. T3 done: README's candidate paragraph, DESIGN's candidate-row text and `hooks/status/` entry, and a CHANGELOG "New" entry describe ✎. Five verify checks green, mod tests 1643.
- 2026-10-11: T4 live look in circumplex, a session the operator opened there on this branch's mod. The operator reported ✎ at the right end of each candidate row. A press cleared the conversation and started the plan with that row's title, and the operator stopped it at its question set. The operator accepted the look.

## Decisions

## Review
