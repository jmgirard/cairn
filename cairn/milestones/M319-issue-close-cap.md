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
- **Branch/PR:** m319-issue-close-cap https://github.com/jmgirard/cairn/pull/332   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

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

- [x] AC1: Guest rule (3) in tracking-rules "Collaboration mode" keeps its conditions for a close, its one-line comment, and its ask-when-unsure clause. It says that the daily limit is 3 unless `cairn/PROFILE.md` carries a `# Issue close cap:` header line, read as "Toolchain profiles" states. A value that matches `[1-9][0-9]?` sets the limit. The value `off` removes the daily limit. Any other value leaves the limit at 3. When the count's read returns a full page of 100 events whose oldest event falls on the current UTC day, the count counts as reaching the limit. The PROFILE.md row of the tracking-rules file map names the line, says that the guest session and `hooks/session_context.py` read it, and says that no validator does.
- [x] AC2: `issue_close_cap(root)` in `hooks/cairn_common.py` returns `(limit, untaken)`, as `open_pr_caps` returns its untaken list. When the value matches `[1-9][0-9]?`, the limit is that number. When the value is `off` in any letter case, the limit is None. When the line is absent, the limit is 3. In these three cases `untaken` is empty. For any other value the limit is 3, and `untaken` is `[("Issue close cap", value)]` with the value as written.
- [x] AC3: The session-start text from `hooks/session_context.py` states the limit in force. With no `# Issue close cap:` line, the guest text is the same as before this milestone. With a number N, the clause from "at most 3" through "that day" says N, and it says "close" for N = 1. With `off`, that clause becomes a statement that such closes have no daily limit. With an untaken value, the text names the line and says the limit stays at 3. In owner mode, the text states no close limit and names no close-cap line, even when the line is present.
- [x] AC4: README's guest-rules passage states the default of 3, the `# Issue close cap:` line, and `off`. CHANGELOG.md Unreleased has an entry that names the line.
- [x] AC5: The verify slot of `cairn/PROFILE.md` runs clean.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T3, T6
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
- [x] T5: Run the verify slot.
- [x] T6: Carry the review return: amend rule (3)'s full-page clause per AC1 with D-216 superseding D-215's sentence, apply the fix-now items (DESIGN.md header list, "By default" in rule (3), README, and the older CHANGELOG entry, the untaken note wording), file the follow-up row, and rerun the verify slot.

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
- 2026-10-22: T5 done. Verify slot green: scripts 0, hooks 0, both `claude plugin validate` runs 0, `claude plugin test .` 2466 pass 0 fail. cairn_validate passes, skills/tests OK.
- 2026-10-22: claim audit: 23 claims read, 1 corrected — CHANGELOG.md, README.md. The CHANGELOG entry said guest sessions close at most 3 issues a day. It now says issues that someone else opened. Both texts now say "with no leading zero". The re-read found both true.
- 2026-10-22: status set to review.
- 2026-10-22: amendment routed: AC1 — the full-page clause counts any 100 events of any date, so it blocks every close on a busy repo; the intended clause is a full page whose oldest event falls on that UTC day. The return also carries the fix-now items in the Review section (DESIGN.md header list, "by default" in rule (3), README, and the older CHANGELOG entry, the untaken note wording) and a follow-up row for diff-bug #3.
- 2026-10-22: checkpoint (half-done): fix-now edits made to DESIGN.md (six header lines, D-215), README and the older CHANGELOG entry ("By default"), and the untaken note ("`off` removes the limit. The limit stays at 3."). The AC1 re-audit is running; the rule (3) rewrite, the superseding D-entry, and the follow-up row wait on it. Hooks suite OK.
- 2026-10-22: re-audit: AC1 (full) — one finding: "that UTC day" had no referent in the criterion; fixed to "the current UTC day". The reader confirmed the rule is sound for a newest-first read (a full page whose oldest event is today may miss same-day events on page 2; an older oldest event means the page holds the whole day) and named the superseding D-entry's content. No IP conflict, bounded, deliverable-bound.
- 2026-10-22: follow-up row "State the close count in guest text" filed for review diff-bug #3 (search-first: no candidate row or archive entry covers the guest text's count recipe).
- 2026-10-22: re-audit: AC1 (full) — two findings. A: `off` in another letter case would leave 3 under rule (3) — answered, false: the "Header lines" paragraph says value case does not count, so `OFF` reads as `off`. B: a new D-entry must supersede D-215's full-page sentence — taken as a record: D-216, cited by rule (3); AC1's wording unchanged.
- 2026-10-22: amendment return: AC1 — "When the count's read returns a full page of 100 events whose oldest event falls on the current UTC day, the count counts as reaching the limit."

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

- copilot: no review. The request on PR #332 exited 0, but the state query still reads `none`, so GitHub may not have recorded it.
- AC1: tracking-rules lines 446-455 (read 2026-10-22). Guest rule (3) keeps its close conditions, one-line comment, and ask-when-unsure clause. It adds the full-page clause and the `# Issue close cap:` line, read as "Toolchain profiles" states: `[1-9][0-9]?` sets the limit, `off` removes it, and any other value leaves 3 with the line named. The file-map row (line 15) names the line, the guest session and `hooks/session_context.py` as readers, and no validator.
- AC2: `TestIssueCloseCap` (3 tests) ok: 1 and 99 give `(N, [])`, `off` and `OFF` give `(None, [])`, no line gives `(3, [])`, and `0`, `100`, `03`, `Many` give `(3, [("Issue close cap", value)])`.
- AC3: `test_the_close_limit_follows_the_issue_close_cap_line` ok (no line, 1 with "such close", 5, `off`), `test_an_untaken_close_cap_keeps_three_and_is_named` ok, `test_owner_mode_states_no_close_limit` ok, and the existing guest-rules test ok. `host_rules` with no line equals main's `HOST_RULES` (loaded from `git show main:`). The untaken note for `0` ends "so the limit stays at 3".
- AC4: README lines 1114-1118 state the default of 3, the `# Issue close cap: N` line, and `off`. CHANGELOG.md Unreleased opens with the entry that names the line.
- AC5: verify slot: scripts 0, hooks 0, both plugin validates 0, `claude plugin test .` 2466 pass 0 fail.
- gate: `cairn_validate.py` all checks passed. The marketplace validate output has no `version` warning. CHANGELOG has the entry (AC4). No DESIGN.md principle changed, so `cairn_impact` is skipped.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: `issues/events?per_page=100` returns the newest 100 events of every kind and date, so "a full page of 100 events counts as reaching the limit" blocks every close on a busy repo at any number — amendment return (AC1 and D-215 mandate the clause; the repair is "a full page whose oldest event falls on that UTC day")
- diff-bug #2: DESIGN.md lines 17-20 still list five header lines — fix now
- diff-bug #3: the session-start text never states how to count a day's closes — follow-up: the gap predates this milestone, and AC3 keeps the no-line text equal to main
- diff-bug #4: the untaken note calls `off` a limit — fix now; its place after rule (4) — reject (style)
- diff-bug #5: the `off` text's "which holds over host style matching, and such closes" can blur what "which" refers to — reject (style): the clause reads as before, and each case was read in full
- diff-bug #6: `off please` reads as `off`, and an empty value is silent — reject (false): both follow the "Header lines" paragraph
- diff-bug #7: `Many` and the 5 case repeat a code path, and a test comment cites a milestone id — reject (false): `Many` checks the value kept as written and 5 checks a number other than the default, and milestone-id comments are the file's pattern
- diff-bug #8: the rulebook does not say `off` skips the count — reject (false): with no limit there is nothing to count, and the fix-now rewording of rule (3) puts the limit first
- blame-history #1: rule (3) still opens "Make at most 3" before the `off` clause — fix now (the same fix as ripple #2)
- blame-history #2: the full-page clause blocks a guest whose page holds no close of its own — the same defect as diff-bug #1, taken by its amendment return
- blame-history #3: a guest session can write `off` into its own PROFILE.md — reject (planned change): the user asked for this line, and D-213 and D-215 keep the limit an instruction, not a guard
- blame-history #4: DESIGN.md's header-line list — fix now (the same fix as diff-bug #2)
- blame-history #5: README keeps "at most 3" unconditional — fix now (the same fix as ripple #3)
- blame-history #6: the rulebook-mass baseline in `skills/milestone/SKILL.md` is not re-seeded — reject (false): the audit reports growth against the M317 figure on purpose, as at M318
- prior-review #1: the baseline growth is not logged — reject (false): the archive summary will name it, as at M318
- prior-review #2: the full-page clause might reverse M315's close-count fix — reject (false): it adds a stopping rule to the same read and removes nothing
- prior-review #3: `issue_close_cap` reads the value as written — reject (false): it compares `off` lowercased, as the rule says
- ripple #1: DESIGN.md's "five optional lines" — fix now (with diff-bug #2)
- ripple #2: tracking-rules rule (3) opens with a fixed "at most 3" — fix now
- ripple #3: README's "at most 3" is unconditional — fix now
- ripple #4: the older Unreleased CHANGELOG entry says "at most 3" — fix now ("by default")
- ripple #5: DESIGN.md lines 77-80 describe the four guest rules without the line — reject (false): the description stays true
