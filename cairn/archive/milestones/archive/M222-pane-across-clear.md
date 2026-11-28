# M222: The cairn pane stays open across /clear

**Status:** done (2026-10-06, PR #229 https://github.com/jmgirard/cairn/pull/229)

**Goal:** A cairn pane that is open when the conversation is cleared is open after the clear: left open by the mod where the clear stays in the same process, and opened again when the next session starts in the same folder, which in the desktop app is at the first message after a typed `/clear`.

**Outcome:** A T1 probe found that a Button's `/clear` ends with reason
`clear` in the same process and closes no pane. A typed `/clear` in the
desktop app ends the process with reason `other`, and the next process
starts at the next message. At an `other` end with the pane shown and
placed, `markReopen` adds `$.session.root()` to the store key `reopen`,
and `reopen` at the next `session.start` clears the mark and opens the
pane after the refresh and the `/cairn-pane` registration. A
`classic.SessionStart` hook refreshes at source `clear`, because the
host's state starts empty under the new session id (T6). README, DESIGN,
and CHANGELOG describe it. Mod tests went to 1307.

**Decisions:** none promoted. The operator chose to treat `other` as a
typed `/clear`, accepting that an app quit also brings the pane back, and
narrowed AC4 to three clears, since `Plan` and `Implement` cannot show
while a milestone is active. AC5 was amended to a shown pane.

**Review:** claim audit, 33 claims, 7 corrected. Three lenses, 36
findings: 7 fixed (root key, register before reopening, 3 tests, docs), 14
to "Pane reopen edges", 13 rejected, 2 noted. Nothing retired.
