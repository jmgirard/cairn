# M312: Link the band's milestone id to its PR

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — the status band is part of the plugin's UI
- **Branch/PR:** m312-band-pr-link, https://github.com/jmgirard/cairn/pull/327

## Goal

In the desktop app, the milestone id on the status band's row opens the milestone's pull request when its file names one.

## Scope

**In:** `BandRow` gains the pull request URL that the milestone file's `Branch/PR` header names, and the Python fixture helper and every fixture's expected rows follow it. The band's shape tag and the published `CairnBandRow` type change with it. On the desktop surface the band draws the id of a row with a URL as a `Link` in the id's current style, gray and bold with no underline, using the form M311 proved for the pane card. README, DESIGN.md, and CHANGELOG describe the link.

**Out:** a link for a row whose header names no pull request, such as an in-progress row before review opens its PR. Such an id draws as it does today, and no candidate row is made, since the request names the PR. A link in the terminal: no `Link` draws there, because a terminal without OSC 8 prints the URL, as M311 found. Links on the idle row and the empty row: the idle row's milestone has no PR, and the empty row has no id.

## Acceptance criteria

- [x] AC1: In `hooks/status/reader.ts`, each `BandRow` gains `url`. It holds the first pull request URL that the milestone file's `Branch/PR` header names before any `companion:` entry, which is what `prUrl` returns. It is `null` when the file is missing, is not a regular file, or fails to read, or when its header names no pull request. `CairnBandRow` in `types/index.d.ts` gains `url: string | null`, and the band atom's shape tag in `hooks/status/register.tsx` moves from `band-4` to `band-5`. `hooks/status/reader.test.ts` asserts a header that names a URL, a header that names none, a missing file, and an unreadable file. Every fixture's expected `rows` give each row's `url`, among them the M301 URL in `stack-in-progress`. `claude plugin test` and `scripts/tests/test_status_fixtures.py` both check those rows, and its `python_rows` computes `url` with `cairn_next.pr_url`.
- [x] AC2: On the desktop surface, the band draws a milestone row's id as a `Link` whose `href` is the row's `url`, with the id's text in the band's gray (`inactive`), bold, and not underlined. The title, track, tail, and Buttons draw as before, and the existing `hooks/status/band.test.tsx` suites pass unchanged. `hooks/status/band.test.tsx` asserts the `Link`, its `href`, and the id's style for a desktop row with a `url`.
- [x] AC3: The band draws no `Link` for a milestone row with a null `url`, both for a row with no readable file and for a row whose header names no pull request. It also draws none for the idle row, for the empty row, or on the terminal surface for a row whose `url` is set. `hooks/status/band.test.tsx` asserts each of the five cases.
- [x] AC4: README's "The milestone band" section, the `hooks/status/` entry in `cairn/DESIGN.md`, and `CHANGELOG.md` say two things. In the desktop app, and on any other surface that draws links, the band's id opens the first pull request that the milestone file's `Branch/PR` header names. A milestone whose header names none draws its id as before.
- [ ] AC5: In the desktop app, a band row for a milestone whose `Branch/PR` header names a pull request draws its id in the band's gray, bold, with no underline, and a click on the id opens that pull request.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T2
- AC4 → T3
- AC5 → T4

## Tasks

- [x] T1: In `hooks/status/reader.ts`, add `url` to `BandRow` and `NO_FILE` (null) and set it from `prUrl(text)` in `loadAt`. Add `url` to `CairnBandRow` in `types/index.d.ts`, and in `scripts/tests/test_status_fixtures.py` `python_rows` from `cairn_next.pr_url`. Add `url` to every fixture's `expected.json` rows, regenerate `hooks/status/fixtures.gen.ts` with `python3 hooks/status/gen_fixtures.py`, and add the four reader cases to `hooks/status/reader.test.ts`.
- [x] T2: In `hooks/status/band.ts`, give `BandLine` an optional `href` and set it in `bandLines` from `row.url`, and update the `Span.href` comment, which says the band links none. In `hooks/status/register.tsx`, move `BAND_SHAPE` to `band-5`. Off the terminal, draw the id of a line with an `href` as a `Link` around a `Text` with `color={GRAY}`, `bold`, and `underline: false`, as the pane card does (`register.tsx` near line 427). Add the AC2 and AC3 cases to `hooks/status/band.test.tsx`.
- [x] T3: Update README's "The milestone band" section, the `hooks/status/` entry in `cairn/DESIGN.md`, and `CHANGELOG.md`. Grep README and DESIGN.md for "links none" and other band wording that the change makes stale (LESSONS M112).
- [ ] T4: At review, once the PR is open and its URL is in this file's `Branch/PR` header, stop for the user's live look. The user opens a new Code session in this repo, checks that the band's id is gray, bold, and not underlined, and clicks it to see that the PR opens.

## Work log

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — a change to running code (the status mod) that is not a bug.
- 2026-10-21: idea vet: none found. A row whose header names no PR draws its id as before, so in an owner repo without the Copilot round the link shows only between the PR's opening and its merge. In this repo the round opens the PR when review starts.
- 2026-10-21: collision check: M311 (done) linked the pane card to the repo and shipped the `Link` drawing form reused here. No D-entry covers band links, and no open issue or PR overlaps (0 issues, 0 PRs).
- 2026-10-21: criteria audit (full mode, fresh Opus reader): 10 findings. Taken: the shape tag and public type added to AC1, the Python helper and all fixtures named and no new fixture needed (`stack-in-progress` holds a PR URL), the unread-file cases named, AC2 narrowed to the desktop surface, "as before" bound to the existing suites, AC3's null case split into its two drawing branches with a terminal row that has a URL, AC4 matched to README's "any other surface that draws links" wording and to the first URL before `companion:`, and AC5's recording clause dropped. Noted with no change: the idle and empty cases are guards, since neither row can carry a URL. Proportionality: no finding.
- 2026-10-21: plan gate chose a `url` field on `BandRow`, read by the same `prUrl` that the pane's blocked rows use, over looking the URL up from the pane state at draw time, because the band and the pane load separately and the band's own row is where its id is drawn; falsified by a band row whose URL differs from the one `prUrl` reads for the same file.
- 2026-10-21: question set: stop at review for the user's live look at the band's link in the desktop app — yes, at review, once the PR is open (T4).
- 2026-10-21: implement started on `m312-band-pr-link`; the untracked `cairn-probe.log` and `tsconfig.json` predate the branch and stay unstaged.
- 2026-10-21: T1 done: `BandRow.url` from `prUrl` (null in `NO_FILE`), `CairnBandRow.url`, `python_rows` from `cn.pr_url`, `url` on all 34 fixture rows (only `stack-in-progress` M301 non-null), fixtures regenerated, one reader test over a URL, a branch-only header (`blocked-active` M110, since `single-in-progress` has no `Branch/PR` line), a missing file, and an unreadable file. Verify: both unittest suites, both validates, and `claude plugin test` (2467 pass) green.
- 2026-10-21: checkpoint, T2 not yet checked off: `BandLine.href` from `row.url`, `BAND_SHAPE` `band-5`, and the desktop id drawn as `Link` > `Text` (gray, bold, `underline={false}`) directly in the head Box, with no wrapping `Text` so the existing `idAndTitle` sweep passes unchanged (the live look checks the drawing). Six new band tests pass. The first full run had 2 unrelated fails in the M221 AC4 refused-clear tests (a doubled `/clear` fill), and a rerun is checking whether they are flaky. T3 done: README band section, DESIGN `hooks/status/` entry, CHANGELOG New entry. My added sentences pass the simple-english lint; the rest of its README and CHANGELOG hits predate this branch.
- 2026-10-21: T2 done: the full `claude plugin test` rerun is green (2472 pass, 0 fail), so the two M221 AC4 fails of the first run were flaky.
- 2026-10-21: blocked: paused at the user's request so that the test-guidance milestone the easystats audit asked for can be planned and implemented first, at high priority. T1 to T3 are done. Resume with `/milestone-implement M312`, which runs the claim audit (step 7) and then hands off to review, where T4's live look waits.
- 2026-10-21: resumed (M313 done, the blocker gone): merged main (M313) into the branch, the only conflict the ROADMAP's M313 row, resolved to main's file with M312 `in-progress`. Verify green: scripts/tests 445 OK, hooks/tests 193 OK, both validates, `claude plugin test` 2472 pass, 0 fail. The untracked `cairn-probe.log` and `tsconfig.json` stay unstaged.
- 2026-10-21: claim audit: 23 claims read, 0 corrected — CHANGELOG.md, README.md, hooks/status/band.ts, reader.ts, register.tsx, band.test.tsx, reader.test.ts, types/index.d.ts, scripts/tests/test_status_fixtures.py, cairn/DESIGN.md. The reader also found one stale line outside the diff, DESIGN.md's `band` value root sentence still naming shape `band-4`; fixed to `band-5` since M312.
- 2026-10-21: review checkpoint (verify on this head still running): review fix-now work from the four lenses and Copilot. `pullOf` in repo.ts passes a header's PR URL to the band's `Link` only when its owner and repo pass `webOf`'s checks (a planted `href = row.url` failed the new band test alone, 2481 pass, 1 fail); M082's unreadable fixture names a PR so its reader case can fail; `built()` gains `url: null`; two restating test comments, a repeated `idAndTitle` check, and a terminal `underline` check dropped; the register comment reworded; DESIGN names `pullOf`.
- 2026-10-21: review return 1: AC5 failed at the live look. In the desktop app the band's M312 id sits higher than the title and too close to it, because the bare `Link` in the head Box (the form chosen to keep `idAndTitle` unchanged) does not line up with the title's `Text`. The fix is the pane card's form, the `Link` inside a `Text` with `wrap: 'truncate-end'`, which needs a narrowing amendment to AC2's "existing suites pass unchanged" clause, since `idAndTitle` counts the left group's Texts.

## Review

- AC1: `reader.ts:58-61` gives `BandRow.url`, `NO_FILE.url` is null (:275), and `fileFields` sets `url: prUrl(text)` (:288). `types/index.d.ts:18` reads `url: string | null`, and `register.tsx:110` is `band-5`. `reader.test.ts:138-152` asserts M301's URL, M110's branch-only header, M004's missing file, and M082's failed read, whose file now names `/pull/82`. All 34 fixture rows carry `url` (a script over every `expected.json`), and `test_status_fixtures.py:221` sets it from `cn.pr_url`. Verify on 42e5360a: scripts/tests 445 OK, `claude plugin test` 2482 pass, 0 fail. Pass.
- AC2: `register.tsx:892-902` draws `Link href={line.href}` around `Text color={GRAY} bold underline={false}` off the terminal. `band.test.tsx` "stack-in-progress: the desktop draws M301 in a Link" asserts one Link in the head Box, its `href`, and the id Text's gray, bold, and `underline` false. The diff to band.test.tsx before line 3970 is one added `url: null` in `built()`, with no assertion changed. Suites green on 42e5360a. Pass.
- AC3: the same describe asserts no Link for `missing-file` M004, `single-in-progress` M002 (no `Branch/PR` line), `no-active`'s idle row, the first empty fixture's row, and, in the terminal branch, M301 whose `url` is set. Green on 42e5360a. Pass.
- AC4: README "The milestone band" (:102-108), DESIGN's `hooks/status/` entry (:95-104), and CHANGELOG Unreleased (:242-247) each say that in the desktop app, and on any other surface that draws links, the id opens the first PR URL on the `Branch/PR` header before any `companion:` entry, and that a header with none draws the id as before. Pass.
- gate: `cairn_validate` passed, coverage complete. Verify on 42e5360a: scripts/tests 445 OK, hooks/tests 193 OK, both validates passed (marketplace with no `plugins[N].version` warning), `claude plugin test` 2482 pass, 0 fail. CHANGELOG Unreleased has the entry. No principle changed, so `cairn_impact` was skipped.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the band passed `prUrl`'s raw match to a `Link`, so a header URL with `..`, `<`, a non-ASCII letter, or an over-long name could make the desktop refuse the band — fix now (`pullOf` in repo.ts with `webOf`'s checks, a band test and `pullOf` cases), fixed 42e5360a
- diff-bug #2: the id's `Link` sits bare in the head Box, not in a wrapping `Text` as the pane card's do — reject (false): AC2 and T2 name a `Link` around a styled `Text`, which the code draws, and AC5's live look checks the drawing
- diff-bug #3: no test shows a link on a surface other than the desktop, while README and CHANGELOG say "any other surface that draws links" — follow-up ("Test the band link on other surfaces")
- diff-bug #4: the unreadable-file reader case could not fail, since M082's file named no PR — fix now (M082's fixture names `/pull/82`, with a precondition), fixed 42e5360a
- diff-bug #5: the missing-file and no-PR band cases run one drawing path — reject (planned change): AC3 names both
- diff-bug #6: the idle and empty cases guard code the change does not touch — reject (planned change): AC3 names both
- diff-bug #7: the terminal `underline` check tests how the code is written — fix now (dropped), fixed 42e5360a
- diff-bug #8: two comments restate the next lines and an `idAndTitle` call repeats the fixture sweep; the `every(url === null)` precondition is vacuous for the idle and empty fixtures — fix now for the comments and the call, fixed 42e5360a; reject the precondition (false): it holds for the two milestone-row fixtures it guards and is true for the others
- blame-history #1: the band's href has no canonical-URL guard — fix now (diff-bug #1), fixed 42e5360a
- blame-history #2: the id Link departs from M311's wrapping-Text form — reject (false), as diff-bug #2
- blame-history #3: the desktop drawing is unverified — reject (false): no defect shown, AC5's live look covers it
- blame-history #4: a stored `band-4` value reads as absent after the upgrade, so one failed read empties the band — reject (planned change): AC1 moves the tag, and the tag rule says so
- blame-history #5: DESIGN.md:144 runs longer than its neighbours — reject (style)
- prior-review #1: the band href is not canonicalized as M311's `webOf` is — fix now (diff-bug #1), fixed 42e5360a
- prior-review #2: the Link sits outside a Text — reject (false), as diff-bug #2
- prior-review #3: `built()` in band.test.tsx builds a `BandRow` with no `url` — fix now (`url: null`), fixed 42e5360a
- prior-review #4: the new register comment reads as if the terminal links — fix now (reworded "except in the terminal"), fixed 42e5360a
- ripple #1: DESIGN.md's M311 rule on canonical hrefs disagrees with the unchecked band href — fix now (diff-bug #1; DESIGN names `pullOf`), fixed 42e5360a
- ripple #2: the `BandRow` comment at reader.ts:44-45 does not name `url` — reject (false): the field's own comment at :58-60 says when it is null
- copilot: hooks/status/reader.ts:61 — fix now (`built()` gains `url: null`), fixed 42e5360a
- copilot: review body (the terminal-rendering comment) — fix now (reworded), fixed 42e5360a
- Copilot level: Lite (set by GitHub's settings)
- AC5: not ticked. At the live look (T4) on 96d14bbf, the operator's screenshot showed the M312 id drawn higher than the title, with too little space before it. Review return 1 (work log).
