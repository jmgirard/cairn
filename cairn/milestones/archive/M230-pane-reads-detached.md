# M230: The pane's PR reads stop holding up opens

**Status:** done (2026-10-10, PR #239 https://github.com/jmgirard/cairn/pull/239)

**Goal:** The cairn pane fills its pull request lines without holding up an open, fills them again after an in-process `/clear`, draws each pull request once, and keeps remote credentials out of its `gh` calls.

**Outcome:** `/cairn-pane`, `openPane`, and `reopen` in `register.tsx`
start `readPrs` with `void`. `readPrs` starts the blocked reads (`readPr`)
beside `readHotfixes`, and it reads hotfix-only URLs after the list. The
`classic.SessionStart` hook with source `clear` reads when `isShown`.
`paneLines` drops a hotfix whose URL is a blocked row's, and
`withoutUserinfo` strips http(s) userinfo. The test helper gained held
answers and `settled()`. Docs describe it. Mod tests went to 1777.

**Decisions:** none promoted. The plan merged the five pane edge rows into
"Pane edges (M222–M226 reviews)" at the user's request. The question set
declined the empty Hotfixes heading and a live look. A Refresh press
still waits for its read.

**Review:** claim audit, 38 claims, 8 corrected. Three lenses, 28
findings. 8 were fixed: no-call tests settle first, doc wording, the
DESIGN history list, and wrapping. 10 went to "Pane edges (M230
review)". 7 were rejected, among them detached `$` work, which the API
documents. 3 were noted. Nothing retired.
