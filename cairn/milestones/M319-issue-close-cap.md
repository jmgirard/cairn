<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M319: Let PROFILE.md set the guest close limit

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the rulebook and the session-start hook ship to every cairn repo, and guest sessions act on host repos by them   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m319-issue-close-cap   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

A guest repo's `cairn/PROFILE.md` can set or remove the daily limit on issue closes with a `# Issue close cap:` line (D-215).

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** Guest rule (3) in tracking-rules and the file-map row state the line. `hooks/cairn_common.py` reads it. The guest session-start text states the limit in force. README and CHANGELOG describe it. Tests for each value shape.

**Out:** No guard blocks `gh issue close` by count, as D-213 rejected. Owner mode has no close limit and reads no such line. No validator checks the line, as for the PR cap lines.

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

- [ ] AC1: Guest rule (3) in tracking-rules "Collaboration mode" keeps its conditions for a close, its one-line comment, and its ask-when-unsure clause. It says that the daily limit is 3 unless `cairn/PROFILE.md` carries a `# Issue close cap:` header line, read as "Toolchain profiles" states. A value that matches `[1-9][0-9]?` sets the limit. The value `off` removes the daily limit. Any other value leaves the limit at 3. A full page of 100 events in the count's read counts as reaching the limit. The PROFILE.md row of the tracking-rules file map names the line, says that the guest session and `hooks/session_context.py` read it, and says that no validator does.
- [ ] AC2: `issue_close_cap(root)` in `hooks/cairn_common.py` returns `(limit, untaken)`, as `open_pr_caps` returns its untaken list. When the value matches `[1-9][0-9]?`, the limit is that number. When the value is `off` in any letter case, the limit is None. When the line is absent, the limit is 3. In these three cases `untaken` is empty. For any other value the limit is 3, and `untaken` is `[("Issue close cap", value)]` with the value as written.
- [ ] AC3: The session-start text from `hooks/session_context.py` states the limit in force. With no `# Issue close cap:` line, the guest text is the same as before this milestone. With a number N, the clause from "at most 3" through "that day" says N, and it says "close" for N = 1. With `off`, that clause becomes a statement that such closes have no daily limit. With an untaken value, the text names the line and says the limit stays at 3. In owner mode, the text states no close limit and names no close-cap line, even when the line is present.
- [ ] AC4: README's guest-rules passage states the default of 3, the `# Issue close cap:` line, and `off`. CHANGELOG.md Unreleased has an entry that names the line.
- [ ] AC5: The verify slot of `cairn/PROFILE.md` runs clean.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T3
- AC2 → T1
- AC3 → T2
- AC4 → T4
- AC5 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate. Every item opens with its positional label —
     `Tn:` — the item's position counted top-to-bottom, the number Coverage
     cites; an insertion, removal, or reorder renumbers the labels and the
     Coverage lines together. -->

- [x] T1: Add `ISSUE_CLOSE_CAP_LINE` and `issue_close_cap` to `hooks/cairn_common.py` beside `PR_CAP_LINES` (about line 420). Test 1, 99, `off`, `OFF`, an absent line, and the untaken values `0`, `100`, `03`, and `Many`.
- [x] T2: Turn `HOST_RULES` in `hooks/session_context.py` (about line 305, used at about line 431) into text built from `issue_close_cap`. Test no line (text equal to today's), 1, 5, `off`, an untaken value, and owner mode with the line present. Keep the existing guest-rules test passing.
- [x] T3: Edit guest rule (3) in tracking-rules (about line 447) and the PROFILE.md file-map row (line 15) as AC1 states.
- [x] T4: Edit README's guest-rules passage (about line 1114) and add a CHANGELOG Unreleased entry backed by the T1 and T2 tests.
- [ ] T5: Run the verify slot.

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

- 2026-10-22: created by /milestone-plan from the easystats session's request, made for the user, for a `# Issue close cap:` line.
- 2026-10-22: tier check: milestone — it changes a recorded guest rule (D-213), the hook's session text, and needs a superseding decision.
- 2026-10-22: idea vet: one concern. The request let `0` mean off, but `0` is an untaken value in the open-PR cap lines. Answer at the question set: only `off` removes the limit.
- 2026-10-22: collision check: D-213 set the 3-a-day limit at the user's decision (rule (4) there, rule (3) in the rulebook). The question set confirmed the line, and D-215 supersedes that clause. M315 (done) shipped the limit, and this extends it. No candidate row overlaps. Both GitHub inboxes have no open items.
- 2026-10-22: criteria audit (full mode, fresh Opus reader): 9 findings, all taken. The D-entry supersedes D-213's rule (4) by its own numbering and restates the falsifier. AC1 names the readers and adds the full-page clause. AC2 states the return shape. AC3 handles N = 1, says which clause `off` replaces, keeps the no-line text equal to today's, and covers owner mode. AC4 is new for README and CHANGELOG. T1 and T2 probe 1, 99, 100, `03`, and `Many`.
- 2026-10-22: plan gate chose a per-repo line with default 3 over dropping the limit in every guest repo, because only easystats asked; falsified by a second guest repo setting `off` for the same reason.
- 2026-10-22: plan gate chose `off` alone over `off` or `0`, because `0` is untaken in the PR cap lines; falsified by a user writing `0` and expecting no limit.
- 2026-10-22: plan gate chose the full-page clause over narrowing the value to 1 to 9, because a batch after a release can pass 9 and `off` reads no page; falsified by a repo whose own closes on one day pass 100 events.
- 2026-10-22: implement started on m319-issue-close-cap. The untracked `cairn-probe.log` and `tsconfig.json` stay unstaged.
- 2026-10-22: T1 done. `ISSUE_CLOSE_CAP_LINE` and `issue_close_cap` sit beside `PR_CAP_LINES` in `hooks/cairn_common.py`, reusing `PR_CAP_VALUE` for the 1-to-99 match. `TestIssueCloseCap` errored before the function existed and passes now (1, 99, `off`, `OFF`, no line, and the untaken `0`, `100`, `03`, `Many`).
- 2026-10-22: T2 done. `HOST_RULES` became two halves around the close clause, joined by `host_rules(root)`, which takes the limit from `issue_close_cap` and uses `_plural` for N = 1. With no line the text equals main's `HOST_RULES` (compared against `git show main:hooks/session_context.py`). Three new tests: the 1, 5, and `off` cases failed before the change and the no-line case passed; an untaken value names the line; owner mode states no limit. Hooks suite OK.
- 2026-10-22: T3 done. Guest rule (3) in tracking-rules gains the full-page clause and the `# Issue close cap:` line (a 1-to-99 value, `off`, else 3 with the line named, citing D-215). The file-map PROFILE.md row names the line, its two readers, and no validator. skills/tests OK.
- 2026-10-22: T4 done. README's guest-rules passage states the default of 3, the `# Issue close cap: N` line (1 to 99), and `off`. A CHANGELOG Unreleased entry heads "Changes that affect existing repos", backed by `TestIssueCloseCap` and the three session-text tests. The file-map row sentence from T3 was split to stay under the lint's sentence length.

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
