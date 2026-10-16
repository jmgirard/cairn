# M259: Triage keeps started tokens current

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — `/cairn-triage` proposals and the ROADMAP rows it writes for the operator
- **Branch/PR:** m259-triage-started-tokens, https://github.com/jmgirard/cairn/pull/270

## Goal

`/cairn-triage` proposes, at its one gate, adding a missing ` — started M<NNN>` token to a candidate row that a live milestone file names and removing a started token whose work has ended, and it never rewrites away a live token.

## Scope

**In:** `skills/cairn-triage/SKILL.md`: the dead, missing, and live token rules, the reads they need (live milestone files; `gh pr view` for `#<n>` tokens, `--repo <base-repo>` in both modes), the token change as a row fact beside the disposition (the priority token's precedent), the keep rule for live-token rows, the chip, apply, and stamp. tracking-rules "Candidate started token" names triage as the step that does this. README, CHANGELOG, and a DECISIONS entry annotating D-165's "no step removes it" consequence. The rulebook-mass baseline re-seed that a tracking-rules edit owes.

**Out:**
- A `/milestone` health-audit check for missing or dead tokens → dropped at the user's choice (question set); no row.
- Proposing a missing `#<n>` token: owner mode marks a hotfix through PR-body `Candidate row:` lines and writes no `#<n>` token, guest `/hotfix` writes its token in the step that opens the PR, and a guest PR body carries no row text to match → not planned (decided at plan).
- `/milestone-plan` step 6 removing a dead token when it appends a new one → triage does it; no row.
- The other clauses of "Started mark edges (M252 review)" (body lines set at PR open, a cut `gh pr list`, fences, same-title rows, a later `: `, `/hotfix` matching a taken row) → stay in that row; its "a dead one stays" and "triage compress or merge can drop one" clauses leave it at M259's post-merge hygiene.

## Acceptance criteria

- [x] AC1: `skills/cairn-triage/SKILL.md` reads a started token as tracking-rules "Candidate started token" and the pane do (` — started ` and `M<digits>` or `#<digits>`, not followed by a letter or digit), compares ids at three-digit padding, and defines a dead token as an `M<NNN>` token whose id the ROADMAP milestone table holds as `done` or `dropped`, or does not hold, or whose milestone file sits in `cairn/milestones/archive/`, and as a `#<n>` token for which `gh pr view <n> --repo <base-repo> --json state` reports `MERGED` or `CLOSED`. Step 3's table proposes removing each dead token on a row proposed `keep`, `compress`, `retitle`, or `promote`. A `#<n>` read that fails proposes no token change for that token, and the table names the failed read.
- [x] AC2: The skill defines a missing token as ` — started M<NNN>` absent from a candidate row while the ROADMAP table holds `M<NNN>` as `planned`, `in-progress`, `blocked`, or `review` and that milestone's file directly under `cairn/milestones/` quotes the row's non-empty short title in double quotes outside its Scope `**Out:**` list. Step 3's table proposes appending that token to the end of each such row and names the file, and the user can decline it at the gate. The skill proposes adding no `#<n>` token.
- [x] AC3: The skill makes a token change a row fact beside the row's disposition, as a priority change is, never a ninth disposition, riding on a `keep`, `compress`, `retitle`, or `promote` row (a merge survivor is a `keep`, its lineage clause written before the row's tokens); a `drop`, `merge`, `split`, or `route` writes no dead token into any row it writes. The chip's question text names each proposed token change. Step 4 writes a token change only when the user's answer accepts it; the change adds or removes the token text (` — started <ref>`) and leaves the rest of the row as it is. Step 4's skip rule and cap count, step 3's untouched-items carve-outs, and step 6's stamp each count token changes.
- [x] AC4: The skill proposes `keep`, with the token named in the reason, for a row that carries a started token that is not dead under AC1, a `#<n>` token whose read failed included, as it does for a row a live milestone absorbs, and this rule comes before records-hygiene §7's options for a finding-absorbing row.
- [x] AC5: tracking-rules "Candidate started token" names `/cairn-triage` as the step that proposes a missing `M<NNN>` token and the removal of a dead token; README's started-token paragraph says so in place of its sentence that such a token "stays on the row and marks nothing"; `CHANGELOG.md`'s `## Unreleased` has an entry; a new `cairn/DECISIONS.md` entry annotates D-165's "no step removes it" consequence and records the ground on which it passes D-108's door. No sentence in README, `skills/`, or `cairn/DESIGN.md` says a dead token stays with no step to remove it, checked by `grep -rn -e "marks nothing" -e "no step removes" -e "stays on the row" README.md skills/ cairn/DESIGN.md`.
- [x] AC6: The `verify` slot of `cairn/PROFILE.md` is clean: both gating suites, `claude plugin validate` on the plugin and marketplace manifests, and `claude plugin test` for the status mod.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T2
- AC4 → T1, T2
- AC5 → T3
- AC6 → T4

## Tasks

- [x] T1: Triage session start and step 2: read the files directly under `cairn/milestones/` of each live milestone, read each `#<n>` token's PR state with `gh pr view <n> --repo <base-repo> --json state` (guest mode reads the base repo too), and state the dead, missing, and live rules; extend the keep rule (`skills/cairn-triage/SKILL.md:56-58`, `:171-172`) to live-token rows.
- [x] T2: Steps 3, 4, and 6: the token change in the table's reason cell and the chip's question text, the untouched-items carve-out (`:228-234`), the apply edit (`:264-267`, a token appended at the row's end, removal of the token text alone), the skip rule (`:236-240`), the cap count, the merge survivor's lineage clause before its tokens, and the stamp (`:311-315`). A row a `drop`, `merge`, `split`, or `route` takes out writes no dead token into the rows it writes. Place the live-token keep before §7's options (`:162-172`).
- [x] T3: tracking-rules "Candidate started token" (`:215-220`), README's started-token paragraph (`README.md:476-495`), a CHANGELOG `## Unreleased` entry, the DECISIONS entry, and the rulebook-mass baseline in `skills/milestone/SKILL.md:116` plus its two hand-run pins (LESSONS M149). Sweep README and `cairn/DESIGN.md` for other triage or token sentences the change makes stale (LESSONS M112).
- [x] T4: Apply AC1 and AC2's rules by hand to this repo's ROADMAP and milestone files and log which tokens are dead, live, and missing. Hand-run `skills/tests` for the triage guards and fix a pinned phrase the edit moved. Run the `verify` slot.

## Work log

- 2026-10-15: created by /milestone-plan.
- 2026-10-15: tier check: milestone — changes `/cairn-triage`'s shipped behavior and settles a design choice (where token upkeep lives); routed by a request relayed from another session.
- 2026-10-15: collision check: absorbs in part the candidate row "Started mark edges (M252 review)" (its "a dead one stays" and "triage compress or merge can drop one" clauses), so it gets ` — started M259`; annotates D-165 (its consequence that no step removes a dead token); a token change rides beside a disposition as D-134's priority token does, so D-027's eight words stand and D-035's no-sub-status rule holds (D-165: a token holds no status). Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-15: D-108's door judged passed on its retained trigger: a triage `compress` or `retitle` can rewrite away a live `#<n>` token, which drops the pane's mark for an open PR, and M258's own hygiene left a dead ` — started M258` on that row in this repo; the D-entry records it. Checker-regress shape judged not hit: triage is an on-demand editing pass, not a checker; the `/milestone` audit check, the checker-shaped part, was posed as not recommended.
- 2026-10-15: lessons harvested: M112 (sweep README and DESIGN for stale wording, CHANGELOG task), M149 (rulebook-mass pins re-seed in three places), M185 (`gh` reads carry `--repo <base-repo>`), LESSONS line 1 (a SKILL.md edit runs both gating suites).
- 2026-10-15: criteria audit (full, fresh Opus reader): 10 findings, all fixed: AC1 and AC3 disagreed on dead tokens under other dispositions (now ride on keep, compress, retitle, promote; leaving rows write none); ids compared at three-digit padding; token shape tied to tracking-rules and the pane; AC2's substring match narrowed to a double-quoted title outside Scope Out, declinable at the gate; skip rule and cap count token changes; merge survivor's lineage clause goes before its tokens; live-token keep comes before §7's options and a failed read proposes no token change; AC5's grep widened and made the check for a stated property; D-108's door ground goes in the D-entry; Out names the row clauses that leave at hygiene.
- 2026-10-15: plan gate chose a token change beside the disposition over a ninth disposition because D-027 fixes the vocabulary and D-134 set the precedent; falsified by a pass where a token change must happen on a row that leaves the list.
- 2026-10-15: plan gate chose a double-quoted short-title match outside Scope Out over any literal substring because generic titles and Out lists over-match; falsified by a live milestone that absorbs a row without quoting its title, which triage then misses.
- 2026-10-15: plan gate chose not to propose missing `#<n>` tokens: owner mode marks hotfixes through PR-body lines and guest `/hotfix` writes its token as it opens the PR; falsified by a guest hotfix PR open with no token on its row.
- 2026-10-15: question set: a `/milestone` health-audit check for tokens — dropped, triage only, idea not recorded.
- 2026-10-15: question set: the stale ` — started M258` on "Started mark edges (M252 review)" — left in place; T4's hand run must report it dead, and M259's hygiene removes it.
- 2026-10-15: ROADMAP: M258's done row pruned to keep the table under the 60-line cap (terminal-row retention).
- 2026-10-15: implement started on branch m259-triage-started-tokens; untracked `cairn-probe.log` and `tsconfig.json` left unstaged (not this milestone's).
- 2026-10-15: T1 done: triage session start reads tokens, `gh pr view` for `#<n>`, and live milestone files, and defines dead, live, and missing; live-token rows held at session start and `keep` before §7's options. The simple-english lint hook counts the whole file (181 hits on main); the new text was reworded until the count returned to 181. verify green (scripts 408 OK, hooks 175 OK, both validates, mod test 1759 pass).
- 2026-10-15: T2 done: a "Started tokens → a token change" paragraph in step 2; the table's reason cell, the chip's question text, the untouched-items carve-out (a third edit), the skip rule, the apply edit (append at the row's end, remove the token text alone, a survivor's lineage clause before its first token), the cap count, step 5's no-decision list, the stamp, and the close block's status line all count token changes. Lint 184 against 181 on main: three long sentences that already existed grew by a clause each. verify green (408, 175, both validates, 1759).
- 2026-10-15: T3 done: tracking-rules "Candidate started token" names triage's proposals and what a dead token is; README's sentence that a dead token "stays on the row and marks nothing" replaced; CHANGELOG `### New` entry; D-166 annotates D-165 and records D-108's door ground; DESIGN's reader paragraph names triage as a token writer. Rulebook-mass baseline re-seeded to 677 lines / 65,153 bytes in `skills/milestone/SKILL.md` and its two hand-run pins; main stood at 675 / 64,890 against the old 668 / 64,222 seed, so M258 had not re-seeded it. AC5 sweep (`grep -rn -e "marks nothing" -e "no step removes" -e "stays on the row" README.md skills/ cairn/DESIGN.md`) returns nothing. verify green (408, 175, both validates, 1759); `test_cost_audit_line` OK.
- 2026-10-15: T4 done: AC1 and AC2's rules applied by a scratch script to the live ROADMAP: "Started mark edges (M252 review)" carries ` — started M258` (dead: absent from the table and archived) and ` — started M259` (live: in-progress); no row is missing a token. Control: the same row without its M259 token reads as missing, since M259's file quotes its title in the work log outside Out. `skills/tests` hand-run: 752 OK. No code changed after T3's verify run.
- 2026-10-15: claim audit: 23 claims read, 4 corrected — CHANGELOG.md, README.md, skills/shared/tracking-rules.md (a live-token row "kept as it is" → stays `keep` and can still be re-rated, take a lineage clause, or lose a dead token; README and tracking-rules name the four live statuses; the dead-token summaries add the archived case); also SK "the other" → "the second" in the carve-out list. The same reader re-read the corrections: all hold. Rulebook baseline re-seeded again to 678 lines / 65,222 bytes after the tracking-rules fix (three sites). verify green (408, 175, both validates, 1759); `skills/tests` 752 OK; validate green.
- 2026-10-15: implement complete; status → review.
- 2026-10-15: review started; Copilot arm opened PR #270 and requested Copilot (state query `none` before the request).

## Review

- AC1: `skills/cairn-triage/SKILL.md` at 321e3cc7: token shape and the pane's reading at :62-64, three-digit padding at :64-65, `gh pr view <n> --repo <base-repo> --json state` at :66, dead `M<NNN>` (done/dropped, absent, archived) at :71-73, dead `#<n>` (`MERGED`/`CLOSED`) at :73-74, removal proposed on a `keep`/`compress`/`retitle`/`promote` row at :203-205, a failed read proposes no token change and is named in the table at :208-209. Pass.
- AC2: same file: missing defined at :77-80 (the four statuses, the milestone file's double-quoted non-empty short title outside Scope `**Out:**`, the row lacking ` — started M<NNN>`), no `#<n>` token ever missing at :80-82, append at the row's end naming the file at :205-206, user can decline (proposal at the gate; nothing written before the chip's answer, step 3). T4's hand run found the live row correctly not missing and the control row missing. Pass.
- AC3: same file: row fact beside the disposition, never a ninth, riding keep/compress/retitle/promote, survivor a `keep` at :201-204; leaving dispositions write no dead token at :206-208; reason cell example at :236-239; chip names each token change at :246-247; written only when accepted (step 3's no-write-before-answer rule, "An accepted token change" at :310); adds or removes the token text and leaves the rest at :310-312; lineage clause before the first token at :312-313; carve-out at :276-277; skip rule at :280-281; cap count at :316; stamp at :362-363. Pass.
- AC4: same file: live includes a failed `#<n>` read at :75; a live-token row is `keep` before anything else, §7's options included, its reason naming the token at :134-135; held at session start at :59; restated with the live-milestone keep at :197-200. Pass.
- AC5: tracking-rules :220-223 names `/cairn-triage`'s missing-token and dead-token proposals; README :493-498 replaces "stays on the row and marks nothing" (the removed line is in `git diff main -- README.md`); CHANGELOG :167 under `## Unreleased`, no milestone ids; D-166 at DECISIONS :5977 annotates D-165's "no step removes it" and records D-108's door ground. Sweep `grep -rn -e "marks nothing" -e "no step removes" -e "stays on the row" README.md skills/ cairn/DESIGN.md` exit 1, no match; README's remaining "marks\nnothing" wraps a line and says only that a dead token marks nothing, which holds (LESSONS M156: a line grep misses a wrapped phrase; read by eye). Pass.
- AC6: on 321e3cc7: scripts suite 408 OK (21 skipped), hooks suite 175 OK, `claude plugin validate` plugin exit 0 and marketplace exit 0 with no version warning, `claude plugin test .` 1759 pass 0 fail. Pass.
- Gate: `cairn_validate.py` exit 0, all checks passed; no principle changed, so `cairn_impact` skipped; consistency-gate: verify green, no `plugins[N].version` warning, CHANGELOG entry present with no milestone ids. `skills/tests` hand-run 752 OK.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: a row a live milestone quotes can be dropped or merged and its missing token lost — fix now: a row missing a token is `keep`, like a live-token row, fixed 9e1c29c1
- diff-bug #2: a `MERGED` `#<n>` or `done` M dead token is removed with no note that its work shipped — follow-up: "Triage token edges (M259 review)"
- diff-bug #3: the chip's Accept and Amend options did not cover a token change — fix now: Accept applies priority and token changes, Amend can decline a token change alone, fixed 9e1c29c1
- diff-bug #4: the close block's `nothing applied` called any all-`keep` accept a no-op — fix now, fixed 9e1c29c1
- diff-bug #5: `compress` did not say it keeps tokens — fix now: it keeps each token not accepted for removal at the row's end, fixed 9e1c29c1
- diff-bug #6: session start held a live-token row more weakly than step 2 — fix now: it says `keep` (step 2), fixed 9e1c29c1
- diff-bug #7: a note after a removed token had no stated place — fix now: it stays where it was, fixed 9e1c29c1
- diff-bug #8: "the pane reads it the same way" missed the pane's 15-digit `#` cap; an empty-title row with a live token cannot be retitled — fix now for the shape (`#` with one to fifteen digits), fixed 9e1c29c1; the empty-title case follow-up: "Triage token edges (M259 review)"
- diff-bug #9: an M token on a `candidate`-status table row counts as live — follow-up: "Triage token edges (M259 review)" (AC1 fixes the dead set)
- diff-bug #10: removal anchored on padded ids could miss a row's literal `M58` — fix now: removed as the row spells it, fixed 9e1c29c1
- diff-bug #11: README listed fewer dead kinds than the skill; CHANGELOG omitted "outside its Scope Out list" — fix now, fixed 9e1c29c1
- diff-bug #12: the §1 absorbed-row keep still follows §7's options while the live-token keep precedes them — follow-up: "Triage token edges (M259 review)" (an ordering choice on main before M259)
- diff-bug #13: rows sharing a quoted title all get a missing-token proposal — fix now: a shared title is listed as ambiguous with no proposal, fixed 9e1c29c1
- diff-bug #14: a merge survivor's added trigger had no place relative to tokens — fix now: lineage clause and taken trigger go before the first token, fixed 9e1c29c1
- blame-history #1: the missing rule matches any double-quoted mention, so a plan's ledger or log line can draw a token onto a row it did not absorb — fix now: the reason cell quotes the line that holds the title so the user judges at the gate, fixed 9e1c29c1 (the match stays AC2's)
- blame-history #2: shared titles — same as diff-bug #13, fixed 9e1c29c1
- blame-history #3: a note after a removed token is stranded — same as diff-bug #7, fixed 9e1c29c1
- blame-history #4: the live-token keep overrides §7 and the icon `retitle` exception without saying so — fix now: §7's clause now reads "any other finding-absorbing row" and §7 applies again once the token is dead, fixed 9e1c29c1; the icon exception already yields to a live milestone's quote (`retitle` exclusion), so no change there
- blame-history #5: "rides on keep/compress/retitle/promote" overstates reachable pairings — reject, false after diff-bug #1's fix: a dead-token removal does ride on all four, and missing-token rows are `keep`
- blame-history #6: README's "dead" sits beside "marks nothing" while in-progress and review tokens are live but unmarked — fix now: README says such a token is not dead, fixed 9e1c29c1
- blame-history #7: D-166's door ground covers only the keep rule — reject, false: a missing token is a taken row the pane fails to mark, a shipped-behavior defect, and D-166's Context names it ("no step added a token that a plan missed or that predates M258")
- blame-history #8: removing a `MERGED` guest `#<n>` token loses the cue that the row is owed a narrowing — follow-up: "Triage token edges (M259 review)" (with diff-bug #2)
- blame-history #9: the rulebook-mass gloss implied only M259's delta moved — fix now: it names the whole file, fixed 9e1c29c1
- blame-history #10: a long DESIGN line and README wrapping — reject, style
- prior-review #1: §7 precedence clash — same as blame-history #4, fixed 9e1c29c1
- prior-review #2: the missing rule matches mentions, not absorption — same as blame-history #1, fixed 9e1c29c1
- prior-review #3: shared titles — same as diff-bug #13, fixed 9e1c29c1
- prior-review #4: removal leaves a trailing period; 16+ digit `#` tokens — fix now for the digit cap (diff-bug #8), fixed 9e1c29c1; the period stays with the text before the token, which reads correctly, so no change
- prior-review #5: the stamp-length clause did not list token changes — fix now, fixed 9e1c29c1
- prior-review #6: the amend loop is silent on token changes — same as diff-bug #3, fixed 9e1c29c1
- prior-review #7: README wording; the ROADMAP row still names the absorbed clauses; D-165's body unchanged — README part same as diff-bug #11, fixed 9e1c29c1; the row narrows at post-merge hygiene (records-hygiene §1); D-165 is history (IP4), annotated by D-166
- After fixes on 9e1c29c1: verify green (408, 175, both validates, 1759), `skills/tests` 752 OK, validate green, AC5 sweep exit 1 (no match). AC1–AC6 evidence re-read on 9e1c29c1: the fixes add rules and change no criterion's promise.
- Return floor: no finding shows a criterion failing inside its named procedure's domain or a load-bearing defect needing implement; every real finding was fixed on the branch or sent to the follow-up row, so no return. The follow-up row is written at post-merge hygiene as a new row naming "Started mark edges (M252 review)", which is finding-absorbing (§7).
- copilot: cairn/milestones/M259-triage-started-tokens.md:10 (record the PR URL in Branch/PR) — fix now, fixed 321e3cc7
- copilot: skills/cairn-triage/SKILL.md:63 (`#` token to the pane's 1–15 digits) — fix now, fixed 9e1c29c1
- copilot: review body ("live-token exception handling", no thread anchor) — noted; the live-token precedence over §7 was fixed under blame-history #4, 9e1c29c1
- Copilot level: Lite (set by GitHub's settings); its review covered an earlier head.
- conversation: PR #270 — no human reviews or comments; the one review is Copilot's (`COMMENTED`, Bot), so the blocking rule does not apply.
