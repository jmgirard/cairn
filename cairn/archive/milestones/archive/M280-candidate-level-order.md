# M280: The pane shows candidates by priority, and validate warns on file order

**Status:** done (2026-10-18, PR #292 https://github.com/jmgirard/cairn/pull/292)

**Goal:** The cairn pane lists candidate rows high → normal → low whatever their file order, and `cairn_validate` warns on a Candidates section whose file order breaks that rule.

**Outcome:** `paneLines` (hooks/status/pane.ts) sorts the drawn candidate rows by `LEVEL_RANK` (high, normal, low), then ROADMAP index; `state.candidates`, each line's key, and its ✎ target stay in ROADMAP order, so `pressCandidate` is unchanged. `scripts/cairn_validate.py` gains the `candidate order` advisory (`check_candidate_order`), one finding per row whose level ranks above the lowest level read before it, reading rows with `cairn_next.candidate_texts` and `short_title` (`cairn_next` added to `TestStdlibOnly.ALLOWED`); exit code unchanged. New status fixture `candidates-order`; pane, band, and validate tests; DESIGN.md, README, and CHANGELOG text. Triggered by ackwards, whose pane showed a `[high]` row below ten `[low]` rows.

**Decisions:** D-182 (pane level order and the order advisory; annotates D-134, whose rejected token check stands). Plan gate: sort in `paneLines`, not in the reader's state. Question set: one WARN line per row, no live look, ackwards' ROADMAP left to that repo. Criteria audit (full): 3 findings fixed.

**Review:** user-facing, three-lens fan-out, one pass, defect-return count 0, amendment-return count 0. Claim audit: 29 claims, 2 corrected (validate output format in CHANGELOG and README). 19 findings: 6 fixed (a DESIGN.md sentence split, four stale test names or comments, a pane.ts comment), 5 to the new row "Candidate order advisory edges (M280 review)" (hidden rows counted, empty titles, misspelled tokens, D-182's first-`[high]` sentence), 8 rejected. Copilot: request exited 0 twice but never registered, as in M279; new row "Copilot request not registered". No lesson captured or retired.
