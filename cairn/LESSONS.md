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
- 2026-07-12 (M22): when a lean hand-authored milestone file blows the 150-line cap at review (no `<!-- owner -->` scaffolding comments left to trim per the M19 lesson), reclaim room by compressing the verbose task-completion annotations — the Review section already holds the evidence, so `- [x] Tn — one line` is enough.
- 2026-07-12 (M23): skill-prose guard tests read the file as one string and `assertIn` fails across a newline — anchor every asserted phrase on a single line of the SKILL, or the lock silently can't match wrapped text.
- 2026-07-12 (M21): `cairn_validate`'s ISO-date scan false-positives on R CMD check result notation (three slash-separated counts like all-zeros) — write check results as "0 errors / 0 warnings / 0 notes" in tracking files, never the slash form, until the scanner is fixed (candidate G-C2).
- 2026-07-12 (M24): adding a new check to `cairn_validate.CHECKS` that requires files also means extending the shared `Tree.build()` fixture in `scripts/tests/test_scripts.py` — every existing validate test reuses it, so a stricter check silently fails the whole suite until the fixture represents a valid repo for the new invariant.
- 2026-07-12 (M24): scaffold/presence checks over git-tracked files can't assert empty scaffold dirs (`milestones/archive/`, `references/pdf/`) — git doesn't preserve empty dirs, so their absence isn't drift; check only always-tracked files + ignore-file entries.
- 2026-07-12 (M25): to audit for a hardcoded branch name, grep `\bmain\b` (word boundary), not bare `main` — the bare form matches substrings like "remaining"/"domain" and buries the real hits; the guard test uses the same regex.
- 2026-07-12 (M25): runtime default-branch detection must resolve via the remote (`refs/remotes/origin/HEAD`, else `git ls-remote --symref origin HEAD`), never the local current branch — the operational skills run on a feature branch, so `git symbolic-ref --short HEAD` returns the wrong name.
- 2026-07-12 (M26): a prose-guard sentinel token inside a bolded step (`**Routing chip**`) is split by the `**`, so `assertIn` misses it — put the token *inside* the bold (`**Routing chip (AskUserQuestion)**`) and match case-insensitively; extends the M23 single-line rule.
- 2026-07-12 (M26): a routing-chip audit can't assume one chip per skill — `cairn-init` ends both its scaffold and migration flows with a routing chip, and `milestone-brief` ends its RR-ingest phase with one too (the latter uncaught by M26, banked as a candidate).
- 2026-07-12 (M27): in cairn's Claude Code runtime the navigable TOC is built from chapter markers (`mark_chapter`), NOT markdown headers — `#`/`##`/`###` render as visual hierarchy but populate no outline (verified live: many headers → zero TOC, one marker → an entry). Use chapter markers when navigability matters; client UIs like the TOC aren't observable agent-side, so characterizing them needs live probing in the user's own session (D-020).
- 2026-07-12 (M28): a D-entry that cites a count/size of something the same milestone changes is a stale-count trap — D-021 said `NON_REVIEW_CHIP_SKILLS` was six while an earlier task in the same branch made it seven; both review lenses caught it. Write such counts from the post-change state (or omit the number); the guard suite doesn't cross-check D-entry prose against list lengths.
- 2026-07-12 (M30): `cairn_validate`'s slash-date scan now requires a 4-digit year, so R CMD check counts in slash form (e.g. 0/0/0) pass — the M21 "write check results as spaced '0 errors / 0 warnings / 0 notes'" workaround is retired (D-023); slash-form check results may go in tracking files again.
- 2026-07-12 (M30): a milestone that edits the date scanner has its own tracking files scanned by the rule it's changing — write illustrative *real* slash-dates spaced (`2026 / 07 / 11`) in tracking prose, since after this fix a 4-digit-year slash date still trips (only count-triples were freed); the test file lives outside `cairn/` and can use unspaced literals. Bit me in the plan file, D-023, and the review note.
