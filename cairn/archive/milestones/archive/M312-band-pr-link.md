# M312: Link the band's milestone id to its PR

**Status:** dropped (2026-10-22, PR #327 https://github.com/jmgirard/cairn/pull/327, not merged; branch `m312-band-pr-link` kept)

**Goal:** In the desktop app, the milestone id on the status band's row opens the milestone's pull request when its file names one.

**Outcome:** Not shipped. The branch adds `url` to `BandRow` (from `prUrl`, shape tag `band-5`), draws a desktop row's id as a `Link`, and passes `claude plugin test`. AC5's live look failed three times: the desktop drew the linked id above the title's line, unchanged across a bare `Link`, a `Link` inside a `Text`, and centered row parts, so the cause stayed unknown. The operator parked it at the thrash stop, then demoted it at the user's decision: dropped, with the idea kept as the parked candidate row "Link the band's milestone id to its PR".

**Decisions:** none promoted. The plan gate chose a `url` field on `BandRow` over a draw-time lookup in the pane state.

**Review:** Three review returns, each an AC5 live-look failure (work log on the branch). Next try, per the blocker line: check that a new Code session runs the changed mod (LESSONS M201), then try two or three link forms in one live look, one per row (LESSONS M290).
