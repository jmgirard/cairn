# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

Append-only; one line per lesson: `- YYYY-MM-DD (M<NN>): <lesson>`. Capped at
50 lines (tracking-rules weight-caps) — when full, prune the stalest lessons
rather than letting it grow; git history keeps the full record.

<!-- lessons appended below by /milestone-review post-merge hygiene -->

- 2026-07-11 (M16): this repo has no CI — `gh pr checks --watch` returns "no checks reported" + exit 0; treat as no-CI and merge directly, never wait for green.
- 2026-07-11 (M16): a new top-level `cairn/` tracking file needs 4 wiring points — tracking-rules file-map + weight-caps, `cairn_scripts.LINE_CAPS`, and (if its lines carry dates) the `cairn_validate` date-scan tuple.
