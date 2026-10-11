<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M245: The audit reports new activity on the issues and pull requests that candidate rows link to

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP2, GP4
- **Resolves:** —
- **Surface tier:** user-facing — it changes what `/milestone`'s health audit reports in every adopting repo, guest mode included
- **Branch/PR:** m245-linked-item-activity, https://github.com/jmgirard/cairn/pull/255

## Goal

`/milestone`'s health audit reads each issue or pull request that a candidate row links to in one of three named forms, in owner and guest mode, and reports each close, merge, comment, and review that someone else made after the row's cut-off.

## Scope

**In:** A new "Linked items" bullet in `skills/milestone/SKILL.md` §2, run in
both modes. It finds links in the ROADMAP's Candidates section with one named
`grep -oE` command over three forms: a `https://github.com/<owner>/<repo>/issues/<N>`
or `/pull/<N>` URL, `<owner>/<repo>#<N>`, and a bare `#<N>`, read as
`<base-repo>` (the rulebook's slug recipe). The two short forms take a left
boundary, so a path tail such as `hooks/status#3` does not match. Links are
deduplicated on owner, repo, and number. Each item gets one
`gh api repos/<owner>/<repo>/issues/<N>` read. When its `updated_at` is at or
after the cut-off, the bullet reads its comments, and for a pull request also
its reviews and review-thread comments, each with `--paginate` and filtered on
creation or submission time in UTC. Activity by the operator's own login is
dropped. §3 gets four dispositions for these items, among them a new "update
the row" that writes a `checked <UTC time>` mark. README's contributions
bullet gets one sentence, and CHANGELOG gets an entry.

**Out:** The PRs of blocked handoff milestones stay with §2's existing
`blocked` bullet. `/milestone-plan`'s inbox sweep is unchanged. Nothing is
written to GitHub.

## Acceptance criteria

- [x] AC1: `skills/milestone/SKILL.md` §2 carries a bullet that runs in owner and guest mode. It finds the links in `cairn/ROADMAP.md`'s Candidates section with one named `grep -oE` command over three forms. Form 1 is `https://github.com/<owner>/<repo>/issues/<N>` or `/pull/<N>`. Form 2 is `<owner>/<repo>#<N>`. Form 3 is a bare `#<N>`, read as `<base-repo>`. Forms 2 and 3 match only at the start of the line or after a character outside `[A-Za-z0-9_./-]`. It reads each item, deduplicated on owner, repo, and number, with one `gh api repos/<owner>/<repo>/issues/<N>` call.
- [x] AC2: A row's cut-off is 00:00 UTC on the latest `YYYY-MM-DD` in the row's line, or the time in a `checked <YYYY-MM-DDTHH:MM[:SS]Z>` mark in the row when that is later. A row with no date takes the date on the ROADMAP's `Last hygiene check` line. If that line has no date either, the bullet names the row as undated and reads none of its links. An item linked from several rows takes the earliest cut-off, and its report names each row.
- [x] AC3: The bullet reports an item when it was closed or merged at or after its cut-off, unless the item read's `closed_by` login is the one `gh api user --jq .login` returns. It also reports each comment, review, and review-thread comment created or submitted at or after the cut-off by a login other than that one. It reads reviews and review-thread comments for pull requests only. Each list read uses `--paginate` and filters on the creation or submission time, never on the `since` parameter alone.
- [x] AC4: The bullet writes nothing to GitHub. If `gh` is missing or unauthenticated, or the repo has no remote, the bullet names which one and is skipped as a reported gap. If the read of one link fails, the bullet names that link and keeps the rest.
- [x] AC5: `skills/milestone/SKILL.md` §3 resolves each reported item with one of four dispositions: update the row (rewrite it to carry the news and a `checked` mark with the current UTC time, cut to the second, never rounded up), `/hotfix`, `/milestone-plan`, or leave. It states that the next audit reports a left item on a dated row again, and that in guest mode the row edit stays on disk, uncommitted.
- [x] AC6: A live run of the bullet's commands, with `<base-repo>` read as `easystats/performance`, over fixture A gives these results. Fixture A has a stamp dated 2026-10-11 and five rows. Row 1, dated 2026-10-10, links `easystats/insight#1262`: the run reports its merge and its Copilot review. Row 2, dated 2026-10-11, links `#428` and `easystats/insight#1263`: the run reports #1263's merge and the 2026-10-11 comments on performance#428 by mattansb and strengejacke, and none by the operator. Row 3, dated 2026-10-12, links `https://github.com/easystats/insight/issues/1261`: the run reports nothing for it. Row 4, dated 2026-10-10, links `easystats/see#465` and `https://github.com/easystats/see/pull/465`: the run reads it once and reports Copilot's reviews and review-thread comment and none by the operator. Row 5 links `easystats/insight#99999999`: the run names its failed read and keeps the other rows.
- [x] AC7: A live run over fixture B gives these results. Fixture B has a stamp dated 2026-10-11 and two rows. Row 1 reads `added 2026-10-10, checked 2026-10-11T15:44:30Z` and links `https://github.com/easystats/performance/issues/428` and `easystats/insight#1262`. Row 2 has no date and links `easystats/insight#1262`. The run reports strengejacke's comment on performance#428 and not mattansb's, which was created at 15:44:20 and edited later. It reports insight#1262's merge once, naming both rows, and not its 2026-10-10 Copilot review. A run over fixture C, whose stamp has no date and whose one row has no date, names that row as undated and reads none of its links. A run over fixture E, whose stamp is dated 2026-10-11, gives two results. Its row dated 2026-10-10 links `jmgirard/cairn#238`, merged on 2026-10-10 by the operator, and the run reports nothing for it. Its row dated 2009-12-10 links `tidyverse/ggplot2#1`, an issue closed on 2009-12-11 with no `closed_by` login, and the run reports that close and hadley's 2009-12-11 comment, and not his 2009-12-09 comment.
- [x] AC8: README's contributions bullet and a CHANGELOG `Unreleased` entry state the read. The profile's `verify` slot is green.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1, T5
- AC4 → T1
- AC5 → T2
- AC6 → T3
- AC7 → T3, T5
- AC8 → T4

## Tasks

- [x] T1: Write the "Linked items" bullet in `skills/milestone/SKILL.md` §2 after "Outside merges" (around line 261). It holds the `grep -oE` with its left boundaries, the dedupe, the cut-off rule, and the per-item `gh api` read with `--jq` for `state`, `closed_at`, `updated_at`, and `pull_request.merged_at`. It holds the list reads, run only when `updated_at` is at or after the cut-off less one minute (a review can land 2 to 3 seconds after the `updated_at` it sets): `issues/<N>/comments`, and for pull requests `pulls/<N>/reviews` and `pulls/<N>/comments`, each with `--paginate`. It holds the operator-login filter, the report shape (link, each row's opening words, what happened, each author and time), and the gap rules. Commands use no shell variable named `path` (the M133 lesson).
- [x] T2: Add the linked-item dispositions to §3: "update the row" with its `checked` mark, the other three, the re-report note, and the guest on-disk note. Name linked items in §3's triage-chip bullet.
- [x] T3: Build fixtures A, B, and C in the scratchpad and run the bullet's commands as written in a shell, over each fixture.
- [x] T4: Add the README sentence and the CHANGELOG entry. Run the five `verify` commands and hand-run `skills/tests` (the M148 lesson), and check each exit code.
- [x] T5: Step-7 decline: stop reporting a close or merge made by the operator. Amend AC3 (and AC7's fixture) through the gated amendment with its re-audit, filter on the item read's `closed_by` login in the block, update README and CHANGELOG, re-run the fixtures with fixture E (AC7) plus a row dated 2026-09-01 linking `jmgirard/cairn#168` (closed by the operator, must report nothing), and narrow the "Linked-item read edges (M245 review)" row.

## Work log

- 2026-10-11: created by /milestone-plan. Trigger: a performance guest-mode `/milestone` run after easystats/insight#1263 merged reported neither that merge nor new comments on easystats/performance#428, because no §2 bullet reads the items a candidate row links to (the operator confirmed the run came after the merge).
- 2026-10-11: collision check: no candidate row, planned milestone, or D-entry covers linked-item reads. Related, kept distinct: the "`/milestone` reads each bot thread on the operator's open PRs" row (the operator's own PRs) and M167's outside-merges bullet (merges into this repo). D-108's door is not reached: the deliverable is an audit read, not a conduct rule about records, and its trigger is a defect in shipped behavior.
- 2026-10-11: inbox sweep: jmgirard/cairn has 0 open issues and 0 open PRs.
- 2026-10-11: lessons harvested: M185 (every `gh` read names its repo; here `gh api repos/<owner>/<repo>/…` does), M133 (no shell variable named `path`), M148 (hand-run `skills/tests` after a skill edit), M65 family (probe against a known positive; fixtures A and B do).
- 2026-10-11: question set: read bare `#N` refs as the base repo's items? — yes (recommended). Read PR reviews and review-thread comments too? — yes (the operator chose this over the recommended comments-and-merge-only).
- 2026-10-11: criteria audit (full mode, fresh Opus reader), pass 1: 8 findings, all fixed by narrowing. A `checked` mark replaces the day-granular re-report trap. Undated rows fall back to the stamp, and the re-report note covers dated rows only. Items dedupe on owner, repo, and number with the earliest cut-off. List reads filter on creation time with `--paginate` in UTC. Fixtures gained a `/pull/` URL, an undated row, an edited comment, and a failed read. AC5's record-only clause was dropped. The short forms got a left boundary. Bare `#N` went to the question set.
- 2026-10-11: criteria audit, pass 2 over the criteria the answers changed: 3 findings. Fixed: the `checked` mark takes optional seconds and is cut, never rounded up; fixture B links insight#1262 from two rows, and fixture C has a dateless stamp. Answered, not narrowed: bare `#N` in row bodies reads about 13 old cairn items (finding numbers) per audit, and the operator chose all bare refs knowing finding numbers would be read; a false report needs new activity on an old item. T1 gates list reads at the cut-off less one minute, since `updated_at` can trail a review by 2 to 3 seconds.
- 2026-10-11: 8 criteria, over the 7 tripwire; kept as one milestone because the four tasks ship one bullet and its proof, and splitting the fixtures from the bullet would leave the bullet unverified.
- 2026-10-11: plan gate chose prose bullet over a `scripts/` reader because M167 kept GitHub reads out of scripts (D-043 context) and the reads are a handful of `gh api` calls; falsified by an audit run that misses or misreads a link the bullet's grep matches.
- 2026-10-11: plan gate chose a per-row cut-off (latest date in the row, or a `checked` UTC mark) over the hygiene-stamp date because every hygiene pass replaces the stamp and would hide news older than the last pass; falsified by rows whose dates stop tracking their last edit.
- 2026-10-11: branch m245-linked-item-activity cut from main at 3b6acc7. `cairn-probe.log` and `tsconfig.json` are untracked strangers, left unstaged.
- 2026-10-11: minor amendment (T1 wording): the list-read gate compares `updated_at`'s date with the cut-off's date, not the cut-off less one minute. The day gate reads more and never hides a review, and it needs no date arithmetic, which differs between BSD and GNU `date`.
- 2026-10-11: T1 done. The bullet's read is one fenced bash/zsh block (a here-string, not a heredoc, so a copy that keeps the list indent still runs). A dry run over the real performance ROADMAP took 20 s and reported 10 lines, among them the insight#1262 merge; the #428 row is gone there (promoted by the performance session). verify green (5/5), skills/tests 726 OK.
- 2026-10-11: T2 done. §3 names linked items in the triage-chip bullet, lists their four dispositions, adds "update the row" (the `checked` mark from `date -u +%Y-%m-%dT%H:%M:%SZ`, a docs-only commit in owner mode, on disk in guest mode), and notes that a left item on a dated row comes back. verify green (5/5), skills/tests OK.
- 2026-10-11: T3 done. Fixtures A, B, C built under the session scratchpad (`fa/`, `fb/`, `fc/`, each a `cairn/ROADMAP.md`). The bullet's block, cut from SKILL.md by awk and de-indented, with `base` set to easystats/performance, gave the same output in zsh and bash. A: insight#1262 merged + Copilot review, insight#1263 merged, performance#428 comments by mattansb (05:34, 15:44) and strengejacke and none by jmgirard, see#465 read once with Copilot's two reviews and thread comment, insight#1261 silent, insight#99999999 `read failed` with the rest read. B: performance#428 strengejacke only; insight#1262 merged once, lines 7 and 8, no Copilot review. C: `undated row at line 7: not read`.
- 2026-10-11: T4 done. README's contributions bullet and a CHANGELOG `Unreleased` entry state the read. verify green (5/5), skills/tests OK.
- 2026-10-11: claim audit: 31 claims read, 3 corrected — skills/milestone/SKILL.md (a standalone two-part `dir/name#N` is read as owner/repo, so the path-tail example is now `skills/hooks/status#3`; the `:00` pad for an HH:MM `checked` mark moved before `sort`, since two marks in one row picked the wrong one), README.md and CHANGELOG.md (close and merge are reported whoever made them; only comments and reviews drop the operator). The same reader re-read the three: all hold. Fixtures A, B, C re-run over the corrected block in zsh and bash: output unchanged.
- 2026-10-11: implement done; status review. verify green (5/5), skills/tests OK, cairn_validate green but for the 8-criteria advisory.
- 2026-10-11: step-7 decline: the operator chose "Fix own-merge noise first", so the read stops reporting a close or merge that the operator made (an AC3 amendment, from blame-history #1 and prior-review #1). Added as T5, with Coverage AC3 → T1, T5 and AC7 → T3, T5. Status back to in-progress.
- 2026-10-11: substantive amendment: AC3 now skips a close or merge whose `closed_by` login is the operator's, and AC7 adds fixture E (jmgirard/cairn#238, merged by the operator; tidyverse/ggplot2#1, closed with no `closed_by`). AC3 and AC7 unticked for re-review.
- re-audit: AC3 (full) — two probe gaps: no close-only case and no null `closed_by` case. Both disposed by AC7's fixture E ggplot2#1 row. The AC3 wording is unchanged.
- re-audit: AC7 (full) — first pass: the same two probe gaps, fixed by the ggplot2#1 row. AC8 would pass with stale README and CHANGELOG text.
- re-audit: AC7 (full) — second pass: no close-only item closed by the operator. Not amended again (the second-line bound): T5 runs `jmgirard/cairn#168` (closed by jmgirard 2026-09-02, no comments) in a row dated 2026-09-01 as a task-side check that must report nothing.
- re-audit: AC8 (full) — the proposed AC8 wording ("both say that a close or merge made by the operator is not reported") could pass beside contradicting old text. The AC8 amendment is withdrawn and AC8 keeps its plan wording. T5 corrects the README and CHANGELOG text, and the claim audit reads it.
- 2026-10-11: T5 done. The item read adds `(.closed_by.login // "-")`, and a close or merge whose `closed_by` is the operator prints nothing. The SKILL.md prose, README, and CHANGELOG say so, and the "Linked-item read edges (M245 review)" row drops the own-merge item. Fixtures A to D unchanged in zsh and bash. Fixture E: cairn#238 and the task-side cairn#168 row silent, ggplot2#1 reports `closed 2009-12-11T04:43:25Z` and hadley's 2009-12-11 comment. verify green (5/5), skills/tests OK.
- 2026-10-11: claim audit: 6 claims read, 1 corrected — CHANGELOG.md (the read reports an item's latest close or merge, not each one, since it reads `closed_at`/`merged_at` once). The same reader re-read the correction: it holds. Scope: the T5 diff, 2419528..HEAD outside `cairn/`.
- 2026-10-11: implement done after the step-7 decline; status review. verify green (5/5), skills/tests OK.

## Decisions

## Review

Pass 1, 2026-10-11, on `m245-linked-item-activity` at the PR #255 head. Copilot requested at step 2 (state query `none`, `gh pr edit --add-reviewer @copilot` exit 0).

- AC1 evidence: `skills/milestone/SKILL.md:262` opens the "Linked items" bullet, "in owner and guest mode". Line 302 holds the one `grep -oE` over the URL form, `<owner>/<repo>#<N>`, and bare `#<N>`, with the `(^|[^A-Za-z0-9_./-])` boundary; line 303's sed maps bare `#` to `$base`. Line 311 is the one `gh api "repos/$repo/issues/$num"` read per item after `sort -u` and the awk group on owner/repo#N (lowercased by `tr`). Fixture A row 4 (`easystats/see#465` plus `.../see/pull/465`) printed one item.
- AC2 evidence: SKILL.md:272-279 state the cut-off rule. Fresh runs, zsh and bash: fixture A cut-offs are 00:00 UTC on each row's date (`2026-10-10T00:00:00Z`, `2026-10-11T00:00:00Z`); fixture B row 1 takes its `checked 2026-10-11T15:44:30Z` mark; fixture B row 2 (no date) takes the stamp, and insight#1262 shows `lines 8,7, cut-off 2026-10-11T00:00:00Z`, the earlier of its two rows; fixture C (dateless stamp) printed `undated row at line 7: not read`.
- AC3 evidence: SKILL.md:313-321. Merge/close test is `[[ "$merged" < "$cut" ]] ||` (at or after). The three list reads use `--paginate` and `select(.created_at >= cut)` or `select(.submitted_at >= cut)` with `select(.user.login != me)`; no `since` parameter; reviews and review-thread comments sit inside `if [ "$kind" = pr ]`. Fresh run: fixture A reported performance#428 comments by mattansb and strengejacke and none by jmgirard (who has a 14:13 comment there); fixture B dropped mattansb's 15:44:20 comment (edited 15:44:58) against the 15:44:30 cut-off; issue #428 got no review reads.
- AC4 evidence: the block's only `gh` calls are `gh api user`, `gh api "repos/…/issues/<N>"`, and three `gh api --paginate` GETs (no `-X`, `-f`, or `-F`, so no write). SKILL.md:329-333 name the missing/unauthenticated/no-remote gap as a skip, never a `FAIL`. Fresh run: fixture A's insight#99999999 printed `read failed: … 404` and every other item was still read.
- AC5 evidence: SKILL.md:378-381 list the four dispositions for linked items. Line 394 defines "update the row" with a `checked` mark of the current UTC time, cut to the second (`date -u +%Y-%m-%dT%H:%M:%SZ`). Lines 391-393 say a left item on a dated row is reported again. Line 401 says the guest edit stays on disk, uncommitted. Line 356 names linked items in the triage-chip bullet.
- AC6 evidence: the block, cut from SKILL.md by awk and de-indented, with `base='easystats/performance'`, run over fixture A in zsh and in bash. Identical output: insight#1262 merged 2026-10-11T16:49:21Z and Copilot review 2026-10-10T17:57:07Z; insight#1263 merged 2026-10-11T16:51:04Z; performance#428 comments mattansb 05:34:13 and 15:44:20, strengejacke 16:41:40, none by jmgirard; see#465 one item, Copilot reviews 01:56:19 and 02:25:35 and one Copilot review-thread comment, none by jmgirard; nothing for insight#1261; `read failed` for insight#99999999.
- AC7 evidence: same block, both shells. Fixture B: performance#428 reported only strengejacke 16:41:40 (mattansb's 15:44:20 comment, edited later, falls before the `checked 2026-10-11T15:44:30Z` cut-off); insight#1262 reported once, `lines 8,7`, merged 16:49:21, with no line for its 2026-10-10 Copilot review. Fixture C: `undated row at line 7: not read`, and no `gh api` read of insight#1262.
- AC8 evidence: README.md:685-690 (contributions bullet) and CHANGELOG.md:7-16 (`Unreleased`, first entry) state the read. verify on the review head: `scripts/tests` exit 0, `hooks/tests` exit 0, plugin validate exit 0, marketplace validate exit 0, `claude plugin test .` exit 0.
- Consistency gate: `cairn_validate` exit 0 (one WARN, the 8-criteria split advisory logged at plan). Marketplace validate prints no `version` warning. The CHANGELOG entry exists, and the added README/CHANGELOG lines carry no milestone number (grep count 0). No DESIGN principle changed, so `cairn_impact --changed` is skipped. `skills/tests` (hand-run) exit 0.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1: `${item%#*}` and `${item##*#}` fail with `bad pattern` under zsh `extendedglob` — fix now, fixed 957bd36 (escaped `\#`; fixture D under `setopt extendedglob` reads both items)
- diff-bug #2: `[#8](…/pull/8)` also reads `<base-repo>#8` — fix now, fixed 957bd36 (`[` and `]` join the boundary set; fixture D silent on performance#1263)
- diff-bug #3: owner-mode "update the row" has no guard for an off-branch or dirty checkout — fix now, fixed 957bd36 (follows §4's add-a-row steps 1 to 4)
- diff-bug #4: the new reads carry no `--repo`, against §2's opening rule — fix now, fixed 957bd36 (the exception is stated: the repo is in the `repos/<owner>/<repo>` path)
- diff-bug #5: a future date in a row outranks a `checked` mark — follow-up, row "Linked-item read edges (M245 review)"
- diff-bug #6: undated rows follow the stamp, which `/milestone-review` and `/cairn-triage` also replace — reject, planned change (AC2's stamp fallback; CHANGELOG limits the re-report claim to dated rows)
- diff-bug #7: `/hotfix` is offered for another repo's PR, and there is no drop disposition — reject, false: the disposition takes up the row's own work here, now stated in §3 (957bd36); a drop goes through `/cairn-triage`
- diff-bug #8: the stamp grep keeps every match and needs one literal space — fix now, fixed 957bd36 (`head -n 1`, `[[:space:]]*`; fixture D's second stamp line is ignored)
- diff-bug #9: `&#8212;` read as `<base-repo>#8212`; README claims every link form — fix now, fixed 957bd36 (`&` joins the boundary set; README names the three forms)
- diff-bug #10: wrapped continuation lines and `* ` bullets are skipped — reject, false: the rulebook keeps each ROADMAP item on one line and rows open with `- `
- diff-bug #11: a failed `gh api user` leaves `me` empty and reports your own comments — fix now, fixed 957bd36 (the block prints `gh api user failed` and reads nothing; checked with a bad token)
- diff-bug #12: the date-level list gate can skip a review seconds after midnight — follow-up, row "Linked-item read edges (M245 review)"
- diff-bug #13: undated rows with no links print `undated row` noise — fix now, fixed 957bd36 (links are found first, and a row with none is skipped)
- diff-bug #14: zsh `echo` expands escapes, and fractional or lowercase `checked` marks fall back to 00:00 — reject, style: "update the row" writes neither form, and `$info` holds gh's JSON error text
- diff-bug #15: the `**Replace**` stamp line runs on from the last bullet in rendered Markdown — reject, the line is unmodified and was already so after the old last bullet
- blame-history #1: your own merges and closes are reported (rows citing shipped PRs) — follow-up, row "Linked-item read edges (M245 review)"
- blame-history #2: a C-locale `sed` strip yields a garbage item after an em dash — fix now, fixed 957bd36 (a second `grep -oE` extracts the clean link; fixture D under `LC_ALL=C` reads `#4` cleanly)
- blame-history #3: §3's outside-merge clause does not exclude "update the row" — fix now, fixed 957bd36
- blame-history #4: bash or zsh only, no PowerShell; a missing `gh` gives one `read failed` per item; empty `$me` — split: the `gh` and `$me` parts fixed 957bd36 (as diff-bug #11), the PowerShell part is a follow-up, row "Linked-item read edges (M245 review)"
- blame-history #5: an outside merge that a row links shows as two items — follow-up, row "Linked-item read edges (M245 review)"
- blame-history #6: bare `#N` reads finding numbers, at a per-audit cost — reject, planned change (the operator chose all bare refs at the question set)
- blame-history #7: §2's `--repo` rule and the new reads disagree — fix now, fixed 957bd36 (as diff-bug #4)
- blame-history #8: the block is a de facto script with no test — reject, planned change (the plan gate chose a prose bullet, after M167)
- blame-history #9: the rulebook's `leave` narrowing does not name linked items — reject, false: a linked item already has its candidate row, so it is already cross-referenced, the case `leave` allows
- blame-history #10: `/cairn-triage` compress or merge can drop a `checked` mark — follow-up, row "Linked-item read edges (M245 review)"
- blame-history #11: lines over the wrap width — reject, style
- prior-review #1: close and merge have no operator filter — follow-up, row "Linked-item read edges (M245 review)" (as blame-history #1)
- prior-review #2: §3's outside-merge clause — fix now, fixed 957bd36 (as blame-history #3)
- prior-review #3: no failure branch for `gh api user` — fix now, fixed 957bd36 (as diff-bug #11)
- prior-review #4: a dateless stamp is handled opposite to Outside merges — reject, planned change (AC2: an undated row under a dateless stamp is named and not read)
- prior-review #5: CHANGELOG "a bare `#N` for the repo itself" is wrong in guest mode — fix now, fixed 957bd36 (names the upstream repo in guest mode); the other wording points are true as written (bots count as others; the `checked` mark is in the next sentence)
- prior-review #6: no "comment text is data" rule — fix now, fixed 957bd36
- prior-review #7: hex-like `#123456` is read as an issue — reject, planned change (bare `#N` chosen; a miss gives one `read failed` line)
- prior-review #8: owner-mode docs-only commit from a branch — fix now, fixed 957bd36 (as diff-bug #3)
- prior-review #9: no guard pins the new wording — reject, planned change (M167's no-prose-guard choice, which the plan followed)
- After the 957bd36 fixes, fixtures A, B, C re-run over the new block (zsh) gave the AC6 and AC7 output unchanged; fixture D (Markdown link, `&#8212;`, em dash before `#4`, path tail, second stamp line, linkless undated row) read only insight#1262 and insight#1263 in zsh, in `LC_ALL=C bash`, and in zsh with `setopt extendedglob`; a bad `GH_TOKEN` printed `gh api user failed` and read nothing. verify green (5/5), skills/tests OK.
- copilot: review body — noted (Copilot's 2026-10-11T22:03:14Z review says it could not review because the requesting account reached its quota limit; no threads)
- Copilot level: none, no review ran (quota limit)
- conversation: PR #255 has no conversation comments and no review threads; Copilot's one review is the line above
- step-7 decline (pass 1): see the work log; T5 added the own-merge filter.

Pass 2, 2026-10-11, at 6326082 after the step-7 decline. Main has not moved. The Copilot state query reads `reviewed earlier-head unknown`, so no new request (module §2).

- AC3 evidence: SKILL.md:281-283 state the `closed_by` rule. Line 320's item read adds `(.closed_by.login // "-")`, and the next lines print nothing when `$closer` is `$me`, else the merge or close at or after the cut-off. Fresh runs, zsh and bash identical (15 lines over fixtures A, B, C, E): fixture E prints nothing for jmgirard/cairn#238 (merged by jmgirard) and nothing for jmgirard/cairn#168 (closed by jmgirard, the task-side check); ggplot2#1 (null `closed_by`) reports `closed 2009-12-11T04:43:25Z`; insight#1262 and #1263 (merged by strengejacke) are still reported in A and B. The comment, review, and list-read clauses are unchanged from pass 1 and the same A and B lines show them.
- AC7 evidence: same runs. Fixture B: performance#428 strengejacke only; insight#1262 merged once, `lines 8,7`, no Copilot review line. Fixture C: `undated row at line 7: not read`. Fixture E: nothing for cairn#238; ggplot2#1 reports its close and hadley's 2009-12-11T04:43:24Z comment, not the 2009-12-09 one.
- AC1, AC2, AC4, AC5, AC6, AC8 re-checked on 6326082: fixture A output matches pass 1's AC6 line exactly; AC1, AC2, AC4 and AC5's cited sites are unchanged apart from the 957bd36 fixes and the `closed_by` lines; README.md:686-691 and CHANGELOG.md:7-18 state the read; verify 5/5 exit 0.
- spawned: diff-bug, blame-history, prior-review
- diff-bug #1 (pass 2): the `checked` mark takes the edit time, so news between the read and the edit is lost — follow-up, row "Linked-item read edges (M245 review)" (an uncommitted read-time fix was reverted because AC5 names "the current UTC time")
- diff-bug #2 (pass 2): "update the row" for one item moves the cut-off for a left item on the same row — fix now, fixed 6c98018 (the leave note and CHANGELOG name the exception)
- diff-bug #3 (pass 2): any later date in a row moves its cut-off past unreported news — follow-up, row "Linked-item read edges (M245 review)"
- diff-bug #4 (pass 2): owner-mode "update the row" refuses over the stamp line §2 just rewrote — fix now, fixed 6c98018 (the stamp line rides in the row's commit)
- diff-bug #5 (pass 2): `[owner/repo#N]` is no longer read — fix now, fixed 6c98018 (`[` and `]` are excluded for bare `#N` only; fixture F reads `[easystats/insight#1263]`)
- diff-bug #6 (pass 2): undated rows follow the stamp — reject, planned change (as pass 1 diff-bug #6)
- diff-bug #7 (pass 2): the rulebook Intake list does not name "update the row" — reject, false: that list covers inbox issues and PRs, and a linked item is not an inbox item
- diff-bug #8 (pass 2): merge and close lines name no actor — fix now, fixed 6c98018 (`merged … by <login>`)
- diff-bug #9 (pass 2): AC1's boundary set differs from the block — reject, false: AC1 says the short forms match "only" after a character outside its set, a necessary condition the stricter block meets
- diff-bug #10 (pass 2): `state` is read and unused — reject, style
- diff-bug #11 (pass 2): `sort` and `[[ < ]]` follow the locale — reject, false: ISO times and slugs are ASCII, and fixture D passed under `LC_ALL=C`
- diff-bug #12 (pass 2): zsh `echo` expands escapes — reject, as pass 1 diff-bug #14
- diff-bug #13 (pass 2): CHANGELOG's "you made yourself" ignores a null `closed_by` — fix now, fixed 6c98018 ("that GitHub records as yours")
- blame-history #1 (pass 2): a linked PR merged by others also shows as an outside merge — follow-up, already in row "Linked-item read edges (M245 review)"
- blame-history #2 (pass 2): `leave` against the D-044 narrowing — reject, false (as pass 1 blame-history #9)
- blame-history #3 (pass 2): undated rows advance with the stamp — reject, planned change (AC2)
- blame-history #4 (pass 2): §4 refuses a foreign-repo issue while §2 reads other repos — reject, false: §4 is the one-issue look-in, and §2 reads linked items only
- blame-history #5 (pass 2): ROADMAP at 23,979 of 24,000 bytes — fix now, fixed 6c98018 (follow-up row compressed; 23,864 bytes), hygiene re-checks
- blame-history #6 (pass 2): a skipped §4-order write has no close block in §3 — reject, false: §3 ends with the close block
- blame-history #7 (pass 2): README line over the wrap width — fix now, fixed 6c98018
- blame-history #8 (pass 2): no prose guard — reject, planned change
- prior-review #1 (pass 2): the `checked` mark takes the edit time — follow-up (as pass 2 diff-bug #1)
- prior-review #2 (pass 2): §4's step 1 reports a skip in "the close block" — reject, false (as pass 2 blame-history #6)
- prior-review #3 (pass 2): `gh api user failed` does not name which of the three causes — reject, false: the prose assigns the naming to the agent, and gh's own error line (`Bad credentials (HTTP 401)`) prints beside it
- prior-review #4 (pass 2): `gh api user` carries no `--repo` — reject, false: it reads no repo
- prior-review #5 (pass 2): README and CHANGELOG omit the stamp fallback — reject, false: they summarize, and the skill states the full rule
- prior-review #6 (pass 2): locale-sensitive ranges and compares — reject, false (as pass 2 diff-bug #11)
- prior-review #7 (pass 2): bot reviews on your own linked PR re-report until updated — reject, planned change (bots count as others, the M177 choice)
- prior-review #8 (pass 2): no guard — reject, planned change
- prior-review #9 (pass 2): lines over the wrap width — fix now, fixed 6c98018 (README); CHANGELOG reject, style
- Post-fix runs at 6c98018: fixtures A to F, zsh and bash identical; A, B, C, E match the AC6 and AC7 lines above, with merge lines now ending `by <login>`.
- copilot: no new request on pass 2 (state `reviewed earlier-head unknown`, the quota-refused review). PR-conversation read below.
- conversation (pass 2): PR #255 still has only Copilot's quota-refused review, no conversation comments, and 0 review threads.
- Consistency gate, pass 2: `cairn_validate` exit 0 (the 8-criteria WARN only); marketplace validate has no `version` warning; the CHANGELOG entry exists and the added README/CHANGELOG lines carry no milestone number; `skills/tests` exit 0.
