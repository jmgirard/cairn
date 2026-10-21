<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M311: Link the pane card to the repo on GitHub

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the cairn pane ships with the plugin   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m311-pane-repo-link, https://github.com/jmgirard/cairn/pull/325   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In the desktop app, the name and counts on the cairn pane's summary card open the project's GitHub pages.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** The read of a github.com base remote stores its owner and repo.
On surfaces other than the terminal, the card's first line links the
project name to the repo page, the PR count to its pull requests list, and
the issue count to its issues list. The links use the platform's `Link`
element inside the spans' existing `Text`, so bold, color, and the name's
cut stay as they are. README, `cairn/DESIGN.md`, and `CHANGELOG.md` follow.

**Out:** Links in the terminal pane: a terminal without OSC 8 draws the
URL after the text and would push ⌂ and ↻ off the row (not planned; no
row, as the operator chose desktop-only links at the plan). Links on a
blocked or hotfix line's `#N` (not chosen at the plan; no row). Cut and odd
card names stay with the parked row "Fix cut and odd names on the pane card".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together.
     Driving RR set → its Binding criteria appear VERBATIM here (binding-
     criteria check), each ingested as a numbered criterion carrying its tag
     — `- [ ] ACn (BCm): <verbatim>` — with its own Coverage line, since
     coverage-complete counts AC checkboxes positionally (M107); departures:
     a "Deviations from RR<NN>" table ends this section. -->

- [ ] AC1: When the stored read for the root holds the owner and repo of a
      github.com base remote, the card's first line gives three link
      targets. The project name links to `https://github.com/<owner>/<repo>`.
      The PR count and its ` PRs` word link to `…/pulls`. The issue count and
      its ` issues` word link to `…/issues`. A test in
      `hooks/status/pane.test.tsx` asserts the three targets for one
      scp-like, one `ssh://`, and one `https://` remote URL.
- [ ] AC2: In each of these cases the card's first line carries no link
      target and draws the same spans as on main. Case 1: no read is stored
      for the root yet. Case 2: the base remote is on another host. Case 3:
      there is no base remote. Case 4: a github.com remote whose owner or
      repo holds a character outside `A-Z a-z 0-9 . _ -`, or is `.` or `..`.
      Each case is a fixture in `hooks/status/pane.test.tsx`. Cases 2 to 4
      set the base remote URL and run the read.
- [ ] AC3: When the stored read holds an AC1 repo page and a project
      name, on the desktop `register.tsx` draws the card's first line with
      three `Link`s, one for the name span and one for each count with its
      word, each with its `href` and inside a `Text` with
      `wrap: 'truncate-end'`. Inside each `Link` every span is a `Text` with
      the span's style, the theme's `text` color where the span names none,
      and `underline: false`. On the terminal the card's first line draws
      main's text and no `Link`. A test renders the pane for an AC1 fixture
      on both surfaces and checks these.
- [ ] AC4: In the desktop app's docked pane, in a Code session started
      after the change is installed, a press on the project name opens the
      repo's GitHub page. The name and counts draw in the card's colors with
      no link blue or underline, and each count with its word lights as one
      link.
- [ ] AC5: The README's summary-card paragraph and the pane section of
      `cairn/DESIGN.md` state what the name and counts open, that the links
      draw only off the terminal, and the four AC2 cases with no link.
      `CHANGELOG.md` states what the name and counts open in the desktop app
      and that a remote not on github.com draws no link.
- [ ] AC6: The `verify` slot is green: `python3 -m unittest` in
      `scripts/tests` and `hooks/tests`, `claude plugin validate` on the
      plugin and marketplace manifests, and `claude plugin test`.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T3
- AC4 → T5
- AC5 → T4
- AC6 → T1, T2, T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: In `hooks/status/repo.ts` and the read in `register.tsx`
      (`readRepo`, near register.tsx:1180), store the owner and repo of a
      github.com base remote in `CairnRepoRead`, only when both match
      `[A-Za-z0-9._-]+` and neither is `.` or `..`. Bump the stored value's
      `shape` tag (LESSONS mod facts) and update `types/index.d.ts`.
- [x] T2: Give `Span` (band.ts) an optional link target. In `cardLines`
      (pane.ts:728) set it on the name span and the count spans from the
      read. Write the AC1 and AC2 tests, using the harness's `remotes` for
      cases 2 to 4 (pane.test.tsx:3771).
- [x] T3: In `register.tsx`, gate `Link` off the terminal as `Svg` is
      (register.tsx:424), and draw a linked span's text as a `Link` child
      inside its `Text`, on both paths: `drawSpan` (register.tsx:429) and the
      line's `text` (register.tsx:498). Pass the text as the Link's children,
      so `textOf` (pane.test.tsx:241) keeps reading it. Write the AC3 test.
- [x] T4: Update the README summary-card paragraph (README.md:295), the
      pane section of `cairn/DESIGN.md`, and `CHANGELOG.md` under Unreleased.
- [x] T5: Live look (AC4). The app refuses to start a session inside a
      run, so stop and ask the operator to open a new Code session in this
      repo, press the name, and report what opened and how the row fits.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete.
     A milestone of a feature series also carries the plan's
     `feature series: M<a> -> M<b>[ -> …]` line (tracking-rules "Feature series"). -->

- 2026-10-21: created by /milestone-plan.
- 2026-10-21: tier check: milestone — a new feature in the shipped status mod.
- 2026-10-21: idea vet: no concern; the request is a link to the repo page, and the question set widened it to the PR and issue counts.
- 2026-10-21: collision check: no ROADMAP row, archived milestone, or D-entry covers a link from the pane; the parked row "Fix cut and odd names on the pane card" touches the same name span and stays separate. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-21: lessons harvested: mod facts (shape tag on a stored value change, `claude plugin test` checks layout props only, drawing needs a live look in a new session, the app refuses a session inside a run).
- 2026-10-21: question set: which card items link — the name and both counts; link form — the name itself is the link; live look — yes, the run stops at T5 for the operator to open a new Code session and press the name.
- 2026-10-21: plan gate chose the platform's `Link` over a pane Button because a Button's press has no way to open a web page; falsified by a platform call that opens a URL from a press.
- 2026-10-21: plan gate chose the name as the link over a separate ↗ link because it adds no width to the 44-column row; falsified by a live look where the operator cannot tell the name is clickable.
- 2026-10-21: criteria audit (full, Opus): 7 findings, all fixed. (1) terminal fallback would push ⌂ ↻ off the row: links gated off the terminal, AC2/AC3 say so. (2) a bare `Link` drops bold and the cut: the Link goes inside the span's `Text`. (3) AC1 claimed every remote form: narrowed to one URL per form. (4) `.` and `..` pass the character check and refuse the tree: case 4 includes them. (5) AC4 dropped "in the browser", the recording clause, and gained the no-skill-running condition; T5 says the operator opens the session. (6) AC5 dropped the provenance clause and trimmed the CHANGELOG claim. (7) AC2 cases 2-4 run the read with a set remote.
- 2026-10-21: implement started on m311-pane-repo-link; the untracked `cairn-probe.log` and `tsconfig.json` stay unstaged, not this milestone's.
- 2026-10-21: T1 done: `webOf` in repo.ts gives the repo page of a github.com remote, or null for another host, no URL, a name outside `[A-Za-z0-9._-]+`, or `.`/`..`; `readRepo` stores it as `web`, shape `repo-4`. Nine `webOf` cases in repo.test.ts. verify green (scripts 445 OK, hooks 193 OK, both validates, plugin test 2453 pass).
- 2026-10-21: T2 and T3 done in one commit, since the AC2 read-flow cases can only fail once Links draw: `Span.href` (band.ts); `cardLines` links the name, each count, and its word from `repo.web`; register.tsx draws a linked span's text as a `Link` inside its `Text` off the terminal, on both the span and line-text paths. 10 tests in pane.test.tsx (M311 block). plugin test 2463 pass.
- 2026-10-21: T4 done: README summary-card paragraph, DESIGN.md card paragraph (`webOf`, `repo-4`, the Link inside the Text, no terminal link), CHANGELOG Unreleased/New entry. The simple-english lint hook's README and CHANGELOG counts are older text; the README count did not move with the added lines.
- 2026-10-21: claim audit: 44 claims read, 3 corrected — README.md (ASCII letters; "outside the terminal"), CHANGELOG.md (no-link cases; "outside the terminal"); the reader's re-read found all three hold.
- 2026-10-21: planted defects, each restored after: Link on the terminal reds the AC3 terminal test; dropping the owner check in `webOf` reds the AC2 bad-owner read test and its repo.test case; drawing the line text without `spanText` reds the AC3 desktop test. Tree restored clean.
- 2026-10-21: T5 live look 1 (operator, verbatim): "the links work but i dont like the blue and underlined formatting and i dont like how 0 and PRs seem to be separate links and 0 and issues seem to be separate links". Fix: a count and its word draw as one Link; inside each Link every span is a `Text` in its own style, the theme's `text` color where it names none, `underline: false`. AC3 test updated (3 Links). plugin test 2463 pass. Look 2 next; AC3/AC4 wording waits on it.
- 2026-10-21: T5 live look 2: the operator opened a new Code session in the repo and picked "Looks right now", whose description read "Card colors with no blue or underline, "3 PRs" and "12 issues" each light as one link, and clicks open the pages."
- 2026-10-21: re-audit: AC3 (full) — 3 findings: "each run of spans" over all parts though only the tail groups (narrowed to the card's first line); "a surface other than the terminal" untested beyond the desktop (narrowed to the desktop); "draws as on main" beyond the test (narrowed to main's text and no Link). The test satisfies the wording.
- 2026-10-21: re-audit: AC4 (full) — 2 findings: look 2 unrecorded (recorded above); the 44-column row-fit clause unevidenced and not checkable by eye (dropped; the M291 test "a long name is the part that is cut" still checks the tail and Buttons keep their width at 44 columns), and the named URL narrowed to "the repo's GitHub page".
- 2026-10-21: re-audit: AC3 (full) — 1 finding: no precondition, so AC2's no-link cases and a missing name falsified it; fixed with "When the stored read holds an AC1 repo page and a project name". A second line for AC3, so no further reader runs.
- 2026-10-21: re-audit: AC4 (full) — nothing; the two looks satisfy it as written.
- 2026-10-21: substantive amendment: AC3 and AC4 rewritten to the drawing the operator asked for at live look 1 and approved at look 2 (one Link per count with its word, the card's colors, no underline); the 44-column row-fit clause dropped as unevidenced. User direction, logged.
- 2026-10-21: T5 done; all tasks checked. verify ran green at 012d3653 (plugin test 2463 pass); the commits after it touch only DESIGN.md and the milestone file.
- 2026-10-21: implement complete, status review: scripts 445 OK, hooks 193 OK, both manifest validates, cairn_validate green.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md.
     EXEMPT from the 150-line cap (D-074) because D-045 makes it history like the work log — dated dispositions, never edited — so the cap must never demand a trim here either.
     Entries carry their rationale; the counterweight `decisions format`
     advisory watches for pasted output, not for entry length (D-075). -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55),
     as are the work log (D-046) and the decisions section (D-074); evidence
     never scrambles plan-owned content. -->
