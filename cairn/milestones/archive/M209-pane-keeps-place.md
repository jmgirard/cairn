# M209: The cairn pane stays where it is put

**Status:** dropped (2026-10-04, at the goal-wrong stop, by the operator's choice). The work log stays on the unmerged local branch `m209-pane-keeps-place`.

**Goal:** The operator moves or resizes the cairn pane in the desktop app. After a switch to another session and back, the pane keeps that column and that width.

**Outcome:** No code changed. T1 put a logging copy of the mod, named `cairn-probe`, in the session's hot-reload folder. It logged each `ui.*` and `session.*` event and each Pane render. It also logged each open and close call and each band and pane write. A switch to another session and back raises `session.detach` and then `session.attach`. The operator resized the pane to 43 body columns. After each of three switches, the pane went back to the rightmost column and drew at its first width of 42. Between the resize and the put-back, the mod made no `$.ui.open` call, no `$.ui.close` call, and no band or pane write. Its only part was its `ui.render` answer to the engine's redraw. The desktop app therefore re-seats the pane by itself, and no change to the mod can stop it.

**Decisions:** The plan's Scope Out set this case as the goal-wrong stop. A search found no report of the bug for mod panes. The nearest is anthropics/claude-code#83002 (closed), where the app's file viewer lost its state on a session switch. The operator chose to drop M209 and to file a new upstream report from a draft. The candidate row "Mod pane placement (upstream)" holds the follow-up.
