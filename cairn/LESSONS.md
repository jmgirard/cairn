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
- 2026-07-11 (M17): `cairn_impact.py` traces principle citations by whole word, so an inaccurate `(IPn)`/`(GPn)` parenthetical is not cosmetic — it misattributes the line in the Sync Impact Report; cite the exact principle (M17 shipped an IP2→IP3 fix the review caught).
- 2026-07-12 (M18): `test_section_allow_lists.py` requires every phase skill to contain the literal phrase "section-ownership table" — rewording that sentence in a SKILL silently fails the guard; keep the phrase when editing.
- 2026-07-12 (M18): the owner-parity test reads an H2's `owner:` tag only in the 3 lines after the heading (`lines[i+1:i+4]`) — a template section's owner comment must close `-->` within that window or it parses as "no owner tag".
- 2026-07-12 (M19): hooks snapshot at process start, so a hook added/registered this session can't be live-fired now — a fixture test proves only what it PRINTS; verifying the client actually honors the envelope needs a brand-new conversation after merge.
- 2026-07-12 (M19): a milestone file near the 150-line cap can't absorb review evidence — reclaim room by trimming the redundant `<!-- owner: … -->` section-scaffolding comments (they duplicate tracking-rules' ownership table), never by cutting tracking content.
- 2026-07-12 (M20): `cairn_validate.py` audits whatever repo is the CWD — to audit a migration target you must `cd` into that repo; running it from the cairn checkout silently validates cairn instead (bit me mid-review, gave a false 9/9).
- 2026-07-12 (M20): entombment-is-verbatim is provable by `git diff -M --summary <base>..<branch>` showing `rename … (100%)` — the clean evidence for the "no completed milestone rewritten" criterion.
- 2026-07-12 (M20): the M16 "no CI here" lesson is cairn-specific — migration target repos (real R packages) DO have CI, and pushing a review-fix commit re-triggers the full matrix; the target-repo PR is its own merge gate, not the cairn milestone's.
