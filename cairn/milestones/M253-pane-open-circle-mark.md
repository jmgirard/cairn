<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M253: A normal candidate row's mark is an open circle

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the pane ships to plugin users   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m253-pane-open-circle-mark, https://github.com/jmgirard/cairn/pull/264   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

In the cairn pane, a normal-priority candidate row that no open pull request names leads with `○` in place of `·`, so the candidate marks read ↑ high, ↓ low, ○ normal, and ◐ started at any priority.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `PRIORITY_MARK.normal` in `hooks/status/pane.ts` becomes
`{ text: '○' }`, in the default text color. The tests in
`hooks/status/pane.test.tsx` that hold `·` or read the constant state the
marks as literals. README's mark list, DESIGN.md's ambiguous-width list,
and a CHANGELOG entry.

**Out:** the high, low, and started marks and the task list's `○`/`✓`
stay as they are (the request changes only the normal mark).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets.
     Every item opens with its positional label — `ACn:` — the item's
     position counted top-to-bottom, the number Coverage cites; an
     insertion, removal, or reorder renumbers the labels and the Coverage
     lines together. -->

- [x] AC1: `PRIORITY_MARK.normal` in `hooks/status/pane.ts` equals `{ text: '○' }`,
      the U+25CB character that `OPEN_MARK` holds, with no color or bold.
      `PRIORITY_MARK.high`, `PRIORITY_MARK.low`, and `STARTED_MARK` keep their
      M207 and M252 values. Shown by `hooks/status/pane.test.tsx` cases that
      state each mark as a literal, none reading it from the constant:
      `CANDIDATE_LINES` (every normal row of the candidates fixture, both
      surfaces), the ✎ test's empty-title and equal-title rows, and M252's
      `PLAIN` line draw `○`; the candidates fixture's high row draws `↑` in
      the implement color and bold and its low row `↓` in gray; and M252's
      cases for a row that an open PR's item names draw `◐` in the review
      color.
- [x] AC2: README's sentence that lists the candidate marks names `○` for a
      normal row, and `grep -n "·" README.md` finds no line that names `·` as
      a candidate mark. DESIGN.md's ambiguous-width list in Known issues names
      `↑ ○ ↓`. CHANGELOG.md's Unreleased "New" section has an entry for the
      change.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Tests first in `hooks/status/pane.test.tsx`: change `·` to `○` in
      `CANDIDATE_LINES` (`:375`), the ✎ rows (`:1442`), and M252's `PLAIN`
      (`:3987`); replace the constant-derived marks at `:416-432`, `:476`, and
      `:3977` with literals. See them red, then set `PRIORITY_MARK.normal`
      (`pane.ts:270`). Run `verify`.
- [x] T2: README (`:313`), DESIGN.md Known issues (`:707`), and a CHANGELOG
      entry. Run `verify`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates.
     EXEMPT from the 150-line cap (D-046): history under D-045, never edited,
     so the cap must never demand a trim here. Wrapped entries get a WARN.
     The rejected-alternative record (/milestone-plan step 4) takes this form:
     `- YYYY-MM-DD: plan gate chose <approach> over <alternative> because
     <reason>; falsified by <evidence class>.` — one per approach choice the
     gate actually weighed, none where it weighed none, and it is the record
     `/milestone-review`'s thrash trigger (b) reads. It lives here rather than
     below so an instantiated file inherits no placeholder to delete. -->

- 2026-10-15: created by /milestone-plan.
- 2026-10-15: tier check: milestone — a change to what the pane draws, a runtime surface, not a bug.
- 2026-10-15: collision check: M207 chose `·` for normal rows and M252 added `◐`; this extends both; no D-entry on the marks; inbox 0 open issues, 0 open PRs.
- 2026-10-15: criteria audit (full mode, Opus): 7 findings. Fixed 6 (AC1 names the literal-holding tests and M252's layout cases, constant-derived checks become literals; AC2 adds DESIGN's ambiguous-width list, a no-`·` grep, and the CHANGELOG section; goal says "○ normal"). Declined 1 (a README clause on the task list's `○`; tasks and candidates never draw together).
- 2026-10-15: question set: ○ color — default text; live look — the operator glances at the pane at the merge question, no extra stop.
- 2026-10-15: implement started on m253-pane-open-circle-mark; untracked `cairn-probe.log` and `tsconfig.json` stay unstaged; ROADMAP is 1 byte over its budget until this row drops at hygiene.
- 2026-10-15: T1: tests state the marks literally (a hand-written `MARKS` map, `PRIORITY_MARK` and `STARTED_MARK` asserted whole); 18 tests red with `·` received for `○` expected, then `PRIORITY_MARK.normal` set to `○`; mod tests 1729 green, verify green.
- 2026-10-15: T2: README mark list, DESIGN.md Known issues width list and hooks/status lineage, CHANGELOG Unreleased New entry; verify, `skills/tests`, cairn_validate green.
- 2026-10-15: claim audit: 12 claims read, 2 corrected — hooks/status/pane.ts, CHANGELOG.md (re-read once by the same reader: both TRUE); its note that DESIGN's ambiguous-width list lacked `◐` (an M252 gap) taken, `◐` added.
- 2026-10-15: implement done; verify green at head (mod tests 1729, scripts and hooks suites OK, both validates), `skills/tests` OK; status review.

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

- 2026-10-15 sync: `origin/main` has not moved since the branch was cut.
- 2026-10-15 Copilot arm: PR #264 opened at review start; state query `none`; `gh pr edit 264 --add-reviewer @copilot` exit 0.
- AC1: `pane.ts` holds `normal: { text: '○' }`; `claude plugin test .` at the review head, 1729 pass 0 fail. "each priority's mark" (both surfaces) asserts `'○'` with no color, `'↑'` in `'claude'` and bold, `'↓'` in `'inactive'`, and `PRIORITY_MARK` and `STARTED_MARK` whole by `toEqual` against literals; "the candidates fixture's heading, count, marks, and titles" (both surfaces) matches `CANDIDATE_LINES`, every normal row `○ …`; the M242 ✎ test's extra rows expect `○ `, `○ Same title` twice; M252's `PLAIN` is `○ An idea for later` (same-root, no-remote, and other-root tests pass); M252's matched-row tests expect `{ text: '◐', color: 'success' }`. `grep -n PRIORITY_MARK pane.test.tsx` shows only the import, a comment, and the whole-constant assertion. T1's work log records 18 tests red on `·` before the change.
- AC2: README.md:313 reads "`↑` for a `[high]` row, `○` for a normal one"; `grep -n "·" README.md` finds only line 600, the tracking-file map's separators, not a candidate mark. DESIGN.md:707 lists "`↑ ○ ◐ ↓` marks" as ambiguous width. CHANGELOG.md:155-158, under Unreleased "### New", has the `○` entry.
- AC2 (re-recorded; the line above misread DESIGN's list, which read `↑ ○ ◐ ↓` and so did not hold the span `↑ ○ ↓` the criterion names, prior-review #1): DESIGN.md:707 now reads "`↑ ○ ↓`, and `◐` marks are ambiguous width"; README and CHANGELOG evidence above unchanged.
