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
- **Branch/PR:** m245-linked-item-activity

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

- [ ] AC1: `skills/milestone/SKILL.md` §2 carries a bullet that runs in owner and guest mode. It finds the links in `cairn/ROADMAP.md`'s Candidates section with one named `grep -oE` command over three forms. Form 1 is `https://github.com/<owner>/<repo>/issues/<N>` or `/pull/<N>`. Form 2 is `<owner>/<repo>#<N>`. Form 3 is a bare `#<N>`, read as `<base-repo>`. Forms 2 and 3 match only at the start of the line or after a character outside `[A-Za-z0-9_./-]`. It reads each item, deduplicated on owner, repo, and number, with one `gh api repos/<owner>/<repo>/issues/<N>` call.
- [ ] AC2: A row's cut-off is 00:00 UTC on the latest `YYYY-MM-DD` in the row's line, or the time in a `checked <YYYY-MM-DDTHH:MM[:SS]Z>` mark in the row when that is later. A row with no date takes the date on the ROADMAP's `Last hygiene check` line. If that line has no date either, the bullet names the row as undated and reads none of its links. An item linked from several rows takes the earliest cut-off, and its report names each row.
- [ ] AC3: The bullet reports an item when it was closed or merged at or after its cut-off. It also reports each comment, review, and review-thread comment created or submitted at or after the cut-off by a login other than the one `gh api user --jq .login` returns. It reads reviews and review-thread comments for pull requests only. Each list read uses `--paginate` and filters on the creation or submission time, never on the `since` parameter alone.
- [ ] AC4: The bullet writes nothing to GitHub. If `gh` is missing or unauthenticated, or the repo has no remote, the bullet names which one and is skipped as a reported gap. If the read of one link fails, the bullet names that link and keeps the rest.
- [ ] AC5: `skills/milestone/SKILL.md` §3 resolves each reported item with one of four dispositions: update the row (rewrite it to carry the news and a `checked` mark with the current UTC time, cut to the second, never rounded up), `/hotfix`, `/milestone-plan`, or leave. It states that the next audit reports a left item on a dated row again, and that in guest mode the row edit stays on disk, uncommitted.
- [ ] AC6: A live run of the bullet's commands, with `<base-repo>` read as `easystats/performance`, over fixture A gives these results. Fixture A has a stamp dated 2026-10-11 and five rows. Row 1, dated 2026-10-10, links `easystats/insight#1262`: the run reports its merge and its Copilot review. Row 2, dated 2026-10-11, links `#428` and `easystats/insight#1263`: the run reports #1263's merge and the 2026-10-11 comments on performance#428 by mattansb and strengejacke, and none by the operator. Row 3, dated 2026-10-12, links `https://github.com/easystats/insight/issues/1261`: the run reports nothing for it. Row 4, dated 2026-10-10, links `easystats/see#465` and `https://github.com/easystats/see/pull/465`: the run reads it once and reports Copilot's reviews and review-thread comment and none by the operator. Row 5 links `easystats/insight#99999999`: the run names its failed read and keeps the other rows.
- [ ] AC7: A live run over fixture B gives these results. Fixture B has a stamp dated 2026-10-11 and two rows. Row 1 reads `added 2026-10-10, checked 2026-10-11T15:44:30Z` and links `https://github.com/easystats/performance/issues/428` and `easystats/insight#1262`. Row 2 has no date and links `easystats/insight#1262`. The run reports strengejacke's comment on performance#428 and not mattansb's, which was created at 15:44:20 and edited later. It reports insight#1262's merge once, naming both rows, and not its 2026-10-10 Copilot review. A run over fixture C, whose stamp has no date and whose one row has no date, names that row as undated and reads none of its links.
- [ ] AC8: README's contributions bullet and a CHANGELOG `Unreleased` entry state the read. The profile's `verify` slot is green.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1
- AC4 → T1
- AC5 → T2
- AC6 → T3
- AC7 → T3
- AC8 → T4

## Tasks

- [x] T1: Write the "Linked items" bullet in `skills/milestone/SKILL.md` §2 after "Outside merges" (around line 261). It holds the `grep -oE` with its left boundaries, the dedupe, the cut-off rule, and the per-item `gh api` read with `--jq` for `state`, `closed_at`, `updated_at`, and `pull_request.merged_at`. It holds the list reads, run only when `updated_at` is at or after the cut-off less one minute (a review can land 2 to 3 seconds after the `updated_at` it sets): `issues/<N>/comments`, and for pull requests `pulls/<N>/reviews` and `pulls/<N>/comments`, each with `--paginate`. It holds the operator-login filter, the report shape (link, each row's opening words, what happened, each author and time), and the gap rules. Commands use no shell variable named `path` (the M133 lesson).
- [x] T2: Add the linked-item dispositions to §3: "update the row" with its `checked` mark, the other three, the re-report note, and the guest on-disk note. Name linked items in §3's triage-chip bullet.
- [x] T3: Build fixtures A, B, and C in the scratchpad and run the bullet's commands as written in a shell, over each fixture.
- [x] T4: Add the README sentence and the CHANGELOG entry. Run the five `verify` commands and hand-run `skills/tests` (the M148 lesson), and check each exit code.

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

## Decisions

## Review
