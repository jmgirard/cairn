# M210: The status band keeps the right state

**Status:** done (2026-10-04, PR #217 `https://github.com/jmgirard/cairn/pull/217`).

**Goal:** The status band and pane show rows, steps, and the close state that match the session's real state in seven cases where they do not today.

**Outcome:** `dirname` treats a `\\host\share` or `//host/share` head as a root, so the ROADMAP walk stops at a UNC share. `readCairn` in `reader.ts` returns the state with the root it found, and an empty or whitespace-only ROADMAP is a failed read. The `band` value stores `root` (shape `band-4`, and `CairnBandState` gained it). A failed read keeps rows only when the stored root equals the found one, and that decision and its write stand at one version. Another root, a `$.session.cwd()` throw, or rows with no root empty the band and pane. `reconcile` clears `dismissed` through `$.state.get` and an `ifVersion` set, so a refresh with nothing hidden writes nothing. The close-button press takes the version before its reads and writes with `ifVersion`, so a `session.end` between them wins. A `classic.Stop` keeps the step while `session_crons` holds a one-shot entry. An idle typed prompt still ends the step before `next`, and on a `drop` puts back the step and the close state. Mod tests went from 998 to 1024. README, DESIGN, CHANGELOG, and the `register.tsx` and `reader.ts` comments describe it.

**Decisions:** The question set kept the bare-skill-name and foreign-task items out, and chose tests only with no live look. An empty ROADMAP is treated as a failed read, not re-read after a delay. The press uses a version check, not a session-generation atom.

**Review:** Three lenses gave 26 findings. 10 were fixed on the branch, and 9 went to the "Band state follow-ons (M210 review)" row. 7 were rejected as planned, chosen, false, or style. The fixes were the dropped prompt showing a band hidden during `/milestone-review`, the read-then-write races in the failed-read path and `reconcile`, and five doc corrections. A claim audit read 64 claims and corrected 5. The promoted items were trimmed from "Status mod follow-ons", and the fixed move item from "Pane follow-ons (M205 review)".
