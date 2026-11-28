# M246: The pane shows a blocked row whose milestone file was archived before its row was updated

**Status:** done (2026-10-12, PR #256 https://github.com/jmgirard/cairn/pull/256)

**Goal:** The cairn pane shows a `blocked` row as archived when its milestone file moved to the archive before the row changed, with its PR's state word and, for a merged PR, a Finish button that completes the row.

**Outcome:** `blocked` in `scripts/cairn_next.py` gained `archived_text` and
`status_paragraph`, mirrored in `hooks/status/reader.ts`. For a row whose
path is not a regular file, exactly one archive file with the row's
canonical id, read and starting `done` in its Status paragraph, gives
`archived: true` and the paragraph's first PR URL. The pane draws
`archived` after the number, keeps only Finish on such a line, and moved
its shape tag to `pane-5`. `cairn_next.py` prints `(PR #<n>, archived)`.
`/milestone-review` gained a guest-mode archived-file arm for a `blocked`
row: it sets the row to `done` with a named part of step 9, writes
nothing to the archive, and names skipped work and owed `partial`
comments. Owner mode reports and stops. Fixture `blocked-archived` holds
11 cases. Docs and `types/index.d.ts` describe it.

**Decisions:** D-159 (the arm, annotates D-130), D-160 (corrects D-159).

**Review:** two passes of three lenses, 51 findings: 21 fixed, AC5
amended once (narrowed to guest mode and `blocked` rows, accepted by the
user after two re-audits), 9 to "Archived blocked rows (M246 review)",
9 rejected, 4 noted. Copilot did not review (quota). Nothing retired.
