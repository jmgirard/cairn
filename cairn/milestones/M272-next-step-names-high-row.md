<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M272: The next-step recommendation names the first unstarted high-priority candidate

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — adopters read `cairn_next.py`'s output and press the pane's and band's Plan Button   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m272-next-step-names-high-row   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

When nothing is in review, in progress, or workable, `cairn_next.py` and the cairn pane recommend planning the first unstarted `[high]` candidate row by its short title, and the Plan press plans that row.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A candidate-row reader in `scripts/` (priority, short title, started
token) and a `title` key on `recommend` in `scripts/cairn_next.py`; its
printed `Recommended:` line and docstrings. The TypeScript mirror in
`hooks/status/reader.ts`, a fixture that reaches the case, the pane's Next
line, and the shared `pressNext` in `hooks/status/register.tsx`. README and
CHANGELOG.

**Out:** The band's drawing: it shows no command (M220), so its only change is
the shared press. Skipping to a later `[high]` row when the pane hides the
first one for an open pull request's body (M252): the pane then shows no title,
as below; a later-row search stays out until that case is seen in a real
session. `/milestone` and `/milestone-plan` text: `/milestone` leads its
close with the Recommended line as printed, and `/milestone-plan` step 1 reads
only the active and workable picture. The triage change that writes `[high]` →
M271.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `recommend` in `scripts/cairn_next.py` returns a `title` key. In
      the planning case it holds the short title (tracking-rules "Candidate
      short title"), trimmed as JavaScript's `trim` trims, of the first row
      under `## Candidates`, in ROADMAP order and outside HTML comments, that
      opens with `[high] `, has a non-empty short title, and carries no
      started token (` — started M<n>` or ` — started #<n>`, followed by the
      row's end or a character that is not a letter or digit); with no such
      row, and in every other case, it is `None`. Tests in `scripts/tests`
      cover: a `[high]` row chosen over an earlier untagged row, a started
      `[high]` row passed over for a later `[high]` row, a `[high]` row inside
      an HTML comment passed over, no `[high]` row giving `None`, and a
      workable planned milestone giving `None` beside a `[high]` row.
- [ ] AC2: In the planning case with a title, `cairn_next.py`'s printed
      `Recommended:` line reads `Recommended: plan the next milestone →
      /milestone-plan <title>`; with no title the line is unchanged.
- [ ] AC3: `recommend` in `hooks/status/reader.ts` returns the same `title` as
      the Python on every fixture `scripts/tests/test_status_fixtures.py`
      compares, and at least one compared fixture gives a non-null title.
- [ ] AC4: In the planning case with a title, the pane's Next line shows
      `/milestone-plan <title>`, and the next-step Plan press, from the pane
      or the band, runs `/cairn:milestone-plan` with that title as its
      argument after `/clear`; with no title, or when an open pull request's
      body names that title (the pane's M252 hide rule), both behave as
      before. Tests in `hooks/status` cover the line and the press with and
      without a title.
- [ ] AC5: The README paragraph on the pane's Next line (~`README.md:290`),
      the paragraph naming `cairn_next.py`'s recommendation (~`README.md:187`),
      the `cairn_next.py` module and `recommend` docstrings, and a
      `CHANGELOG.md` `## Unreleased` entry each say that planning names the
      first unstarted `[high]` candidate.
- [ ] AC6: The `verify` slot of `cairn/PROFILE.md` passes on the branch head.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1
- AC2 → T1
- AC3 → T2
- AC4 → T3
- AC5 → T1, T4
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. -->

- [x] T1: Python: a candidate-row reader (Candidates sections, comments
      stripped, `[high] `/`[low] ` token, short title with JS-trim, started
      token) in `scripts/cairn_scripts.py` or `cairn_next.py`; `recommend`'s
      `title`; the `Recommended:` line; both docstrings; tests in
      `scripts/tests` for the AC1 cases and the AC2 line.
- [x] T2: TypeScript: `recommend` in `hooks/status/reader.ts` takes the
      candidate texts and returns `title`; `NextStep` gains `title`; add or
      edit a fixture with no workable row and a `[high]` row; regenerate the
      expected JSON with `hooks/status/fixtures.gen.ts`; run
      `test_status_fixtures.py`.
- [x] T3: Pane: the Next line's target text (`hooks/status/pane.ts` ~:465)
      and `pressNext`'s args (`hooks/status/register.tsx` ~:1111), both
      falling back to no title when an open pull request's body names it;
      tests in `hooks/status` for the line and the press.
- [ ] T4: README (~:187, ~:290) and CHANGELOG; run `verify`, including
      `claude plugin test`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-17: created by /milestone-plan.
- 2026-10-17: tier check: milestone — planned at the question set of M271's plan, which the user asked to include this work in; changes script output and pane behavior.
- 2026-10-17: collision check: D-134 (priority token), D-165 (started token), and D-167 (pane hides started rows) allow it; no candidate row or archived milestone covers naming a candidate in the recommendation.
- 2026-10-17: question set: name the first `[high]` row in the next-step recommendation — include it.
- 2026-10-17: plan gate chose the first unstarted `[high]` row in ROADMAP order over the first `[high]` row the pane draws because Python cannot read open pull request bodies and the parity test needs one rule; falsified by a session where the Next line names a row the Candidates list hides.
- 2026-10-17: criteria audit (full mode, fresh Opus reader): no criterion unreachable; fixed — the started token takes its real shape, the title trim is JavaScript's, AC4 falls back for a row an open PR names, AC5 narrowed to two named README paragraphs plus both docstrings; noted — a row with a dead started token is never recommended though the pane still lists it.
- 2026-10-17: implement started on branch m272-next-step-names-high-row, cut from main at b1d03358; untracked `cairn-probe.log` and `tsconfig.json` are unrelated and stay unstaged.
- 2026-10-17: T1 done: `candidate_texts`, `short_title`, and `high_title` in `scripts/cairn_next.py` (not `cairn_scripts.py`, since only `recommend` reads them); `recommend` takes an optional `roadmap` text and returns `title`; 6 tests in `TestNext`, each shown red on a planted defect. Choice: the started token takes any number of digits after `M` or `#` (AC1's `#<n>`), where the pane's `STARTED_TOKEN` caps `#` at 15 digits; a letter after the token is ASCII-only, as in that reader.
- 2026-10-17: T2 done: `highTitle` and `recommend(rows, workable, roadmap)` in `hooks/status/reader.ts`; new fixture `high-candidate` (title "Chosen row"); `"title": null` added to the other 29 fixtures' `next` by a Haiku subagent, diff checked as 29 one-line inserts; T1 and T2 commit together, since either alone fails the fixture parity tests.
- 2026-10-17: T3 done: `nextTitle` in `hooks/status/pane.ts` drops the title when an open PR body names it; the Next line and `pressNext` both read it; 6 old tests updated to the new planning shape and 6 new AC4 tests (line, pane press, band press, hide rule) added; plants of no hide rule and no title in the press turned 11 tests red, and a press plant without the hide rule turned 1 red.

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->
