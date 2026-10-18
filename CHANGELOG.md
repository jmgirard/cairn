# Changelog

## Unreleased

### Changes that affect existing repos

- **A feature split across milestones reaches users as one change.** When a
  plan splits one user-facing feature or fix into several milestones, it
  writes them as a feature series and puts a
  `feature series: M<a> -> M<b>` line in each milestone's work log. Each
  part before the last keeps its new behavior out of users' reach where it
  can, with no new export, user doc, or changelog entry. The last part adds
  them. When an earlier part must change visible behavior, its changelog
  entry is the feature's one entry, and later parts edit it. The changelog
  check in the `python`, `r-package`, `claude-plugin`, and `docker-image`
  profiles accepts that edit, and needs no entry for a hidden earlier part.
  Review reads the copy of that check in your `cairn/PROFILE.md`, so add the
  new sentences to its changelog line by hand. Copy them from
  `skills/shared/profiles/<profile>.md`.
  In guest mode, each series pull request says in one plain sentence
  whether it completes the series. The last one names the pull requests of
  the earlier parts and leaves out a dropped part. In owner
  mode, `/cairn-release` names each series that has a merged part and an
  unmerged part when it asks for the version. The `/milestone` status
  snapshot reports the same series. A part whose ROADMAP row was pruned
  takes its status from its archive summary, and new archive summaries
  copy the `feature series:` line. A `/hotfix` for behavior that the
  series' entry describes adds no second entry, and it edits that entry
  only where the fix changes what the entry says. A fix to behavior that
  an earlier release shipped still gets its own entry.
  A series also forms when an amendment at implement, or a descope at
  review, moves part of a user-facing milestone's promised work to later
  work. The amendment writes that work as a candidate row marked
  `split from M<NNN>`. The milestone that `/milestone-plan` makes from the
  row gets the `feature series:` line. Its changelog task edits the cut
  milestone's entry instead of adding a second one. Once the cut milestone
  is done, `/cairn-release` names a marked row as an unplanned part of the
  feature. It leaves the row out while a milestone planned from it is open.

- **Planning names the first high-priority candidate.** When no milestone
  is in review, in progress, or workable, `scripts/cairn_next.py`
  recommends planning. It now names a `[high]` candidate row by its short
  title: `Recommended: plan the next milestone → /milestone-plan <title>`.
  That row is the first `[high] ` row with a short title outside an HTML
  comment that no counted started token hides. A
  ` — started M<n>` token counts while milestone `M<n>` is `planned` or
  `blocked`, but not for a `blocked` row whose file was archived. A
  ` — started #<n>` token of up to 15 digits always counts here, because
  the script reads no PRs. A counted token hides every row
  with the same short title. The cairn pane's Next pill shows
  `/milestone-plan <title>` too. The `Plan` button on the pane and on the
  band runs `/clear` and then `/cairn:milestone-plan <title>`. In the
  pane, the title is the first `[high]` row that its Candidates list
  shows. That list also uses the pane's last read of your open PRs, so the
  pane can name a different row than the script. With no such row, the
  output, the pill, and `Plan` are as before. Before, planning never named
  a row.

- **A triage promote marks its row high priority.** When `/cairn-triage`
  promotes a candidate row (marks it ready to plan), it now also gives the
  row the `[high]` token. The token is added, or it replaces `[low]`, and
  the row moves to the high-priority rows at the top of the Candidates
  list. Before, a promote changed nothing of its own in the ROADMAP. A
  promoted row kept its old token, so a normal or low row showed no `↑` in
  the cairn pane. A row that already opens with `[high]` and a promoted
  Known issues entry take no change. A promote of a row without `[high]`
  always writes the mark, so to avoid it, amend the row to `keep`.

- **Explore searches run on Haiku.** The search subagents that
  `/milestone-plan`, `/milestone-implement`, `/design-interview`, and
  `/cairn-triage` fan out now run on Haiku 5.5 instead of Sonnet 5.5, so
  no cairn subagent role runs on Sonnet. Opus and Fable roles do not
  change. In the cairn repository's test
  (`cairn/references/haiku-search-clarified.md`), three search tasks ran
  three times on each model. Haiku scored at least as high as Sonnet on
  each task, at about 7% of Sonnet's cost. An earlier test had Haiku
  behind, but only because one task's prompt left unclear whether a file
  name includes its `.py` extension. The tasks have fixed answers, so the
  test does not cover an open investigation.

- **The two history reviewers run on Haiku.** In `/milestone-review`'s
  three-reviewer fan-out, the blame-history and prior-PR-comments
  reviewers now run on Haiku 5.5 instead of Sonnet 5.5. The diff-bug
  reviewer stays on Opus. In the cairn repository's test
  (`cairn/references/history-review-recall.md`), Haiku caught as many
  planted history conflicts as Sonnet on a first set, which both models
  caught in full. On a harder set, with each conflict placed away from
  what `git blame` on the changed lines shows and caught by no existing
  test, Haiku again caught at least as many as Sonnet under the test's
  rule, which also requires a finding to cite the right history. Counted
  by whether a finding reported the planted defect at all, Haiku reported
  every one and Sonnet missed one. In two of that set's three test
  commits the extra changed lines were a README rewrap in another file,
  not edits around the planted conflicts.

- **A guest milestone can build on one that waits for review.** In guest
  mode with `# Push remote: base`, a `planned` milestone can depend on one
  `blocked` milestone whose file names its PR. `cairn_next.py` and
  the cairn pane count it as workable. `/milestone-implement` cuts its
  branch from that PR's branch and records the base tip in a
  `stack base:` work-log line. Each resync rebases onto that branch with
  `git rebase --onto`, from the recorded tip. `/milestone-review` opens
  the PR with that branch as its base. Once the first PR merges,
  `/milestone` routes the milestone to `/milestone-implement`, which
  rebases it onto the default branch. A branch pushed before is
  force-pushed again. If GitHub did not retarget the PR, it retargets it
  to the default branch. `/milestone-implement` stops on these cases: two
  or more such dependencies, a base that is itself stacked, a base PR from
  a fork or another repo, and a closed base PR. Owner mode is unchanged.

- **Guest branches can go to the upstream repo.** In guest mode, add the
  line `# Push remote: base` near the top of `cairn/PROFILE.md`, and
  `/milestone-review` and `/hotfix` push the branch to the upstream repo
  instead of your fork. You can then set another open PR's branch as a
  PR's base. Before that push, they read your push permission on the upstream
  repo, and they stop with nothing pushed if it is not `true`. A branch
  whose PR is already open keeps pushing to the remote that holds that
  PR's head. A repo without the line still pushes to the fork. In both
  cases, `/milestone-implement` now fetches a pushed branch before it
  rebases. If the remote branch has commits your copy lacks, it stops and
  names them, and its force-push leases on the tip it read.

- **The routing section names the tier question.** The cairn section that
  `/cairn-init` adds to `CLAUDE.md` now names it. Where a hotfix or a
  direct edit fits, `/milestone-plan` offers it before its one question
  set. The section's Trivial line says that guest mode leaves the edit on
  disk, for `cairn/` files only. Its last line says that a trivial edit
  reaches the default branch on your request or at the tier question. In a
  repo set up earlier, `CLAUDE.md` keeps the old wording. To get
  the new wording, update that section by hand. In guest mode the session
  hook reads the plugin's own copy, so the new wording shows at once.

- **`/cairn-triage lessons` triages `cairn/LESSONS.md`.** It reads every
  lesson and proposes one disposition each at the triage gate: keep it,
  shorten it, correct it, merge it into another lesson, retire it, or hand
  a family of lessons to `/milestone-plan` to become a shared doctrine
  module. A retirement names one of five reasons: a test that fails on
  the mistake the lesson warns about, a tracking file that already holds
  the lesson, evidence read in the pass that shows the lesson false,
  evidence that the repo no longer has the path or tool it is about, or
  no loss to a planner without the line. A false lesson that is still
  partly useful is corrected in place instead, with its evidence, and the
  gate shows the new line. When the file is near its caps, each long
  lesson is proposed for shortening or kept with a reason for each
  clause. The gate warns if the proposed changes leave the file near its
  caps. A lesson that a
  test checks for stays as it is. Nothing changes until you accept at the
  gate, and the accepted edits land in one commit (in guest mode, on disk
  with no commit). Plain `/cairn-triage`
  still covers only candidate rows and known issues.

- **Candidate short titles hold no icons.** The cairn pane uses glyphs
  such as `⌂` and `✎` for its own marks and Buttons, so an icon anywhere in
  a short title can read as one of them. The rulebook now tells whoever writes
  a row to name things in words and to put no icon in the short title. An
  icon is a non-ASCII character whose Unicode general category is `So` or
  `Sm`, between backticks or not. Most emoji are icons, and so are `○`, `✓`,
  `⌂`, `✎`, `↑`, and `⋯`. `/cairn-triage` proposes a `retitle` for a row
  whose title holds an icon. When that title ends at a `: `, the new title
  replaces it in place. Any other such row takes the new title and `: `
  before its text, which stays with each icon removed. Existing
  rows keep their titles until a triage pass retitles them.

- **Candidate rows have one written short-title rule.** A row's short
  title is still its text up to the first `: `. A row with no `: ` is now
  cut at its first ` — `, so the cairn pane no longer shows the date and
  links that follow it. A row with neither still shows all its text. The
  rulebook now tells whoever writes a row to open it with a few
  words that name the row, then `: ` and the details, with an area word
  inside the title (`ordinal REML: …`, not `ordinal: REML. …`). The new
  ROADMAP skeleton shows that shape. `/cairn-triage` gains a `retitle`
  proposal for a row whose short title is empty, longer than 60
  characters, or the same as another row's. It puts a new short title
  before the row's text, which stays as it is (a row whose title is empty
  loses only its leading `: `), and rewrites each
  double-quoted mention of the old title in the other ROADMAP rows and in
  DESIGN.md's Known issues, except a mention of a title that several rows
  share, which it lists and leaves as it is. A quote of a row's whole
  text, written before this change for a row with no `: ` but a ` — `, no
  longer matches that row's title.

- **The plan checks that the work needs a milestone before it plans one.**
  Before `/milestone-plan` investigates, it puts the request in one work
  tier. If the request is a user-visible bug that a hotfix can fix, or an
  edit with no runtime effect such as a typo, the plan asks one question:
  take that route, plan a milestone anyway, or stop. The hotfix route
  starts `/hotfix` with your request text. In owner mode the direct-edit
  route makes the edit, shows it, commits only the files it touched, and
  pushes them to the default branch. The question names the file and the
  change. Before asking, the plan checks three things. The repo has a
  remote. The checkout is on the default branch and level with the
  remote. Nothing is staged, and those files hold no uncommitted changes.
  If a check fails, the question says so, and the route makes no edit. A
  failed or rejected push is never forced. In guest mode the direct edit
  applies only to `cairn/` files and stays on disk. A small change to
  running code that is not a bug still gets a milestone. A request that
  names a GitHub issue is not checked: `/milestone` with the issue is the
  way to judge an issue. An issue that `/milestone` judged a milestone and
  handed to the plan is not checked again. Neither is work that `/hotfix`
  found too large earlier in the same session. A plain `/milestone-plan`
  that names no work is not checked: the work you pick at the question
  set is planned as a milestone.
- **A hotfix removes the candidate row it fixes, once the fix merges.**
  `/hotfix` now looks for ROADMAP candidate rows that describe the bug: a
  row whose title the request quotes, or one that describes the same bug.
  It does this again on every run, including a rerun with a PR number. It
  names each matched row in chat and at the approval question. After the
  merge it deletes a row the fix covers in full, or narrows a row it covers
  in part, with a `narrowed YYYY-MM-DD by the PR #N hotfix` note. The edit
  lands in one tracking commit on the default branch. A declined or closed
  PR, or a fix too large for a hotfix, leaves the row. So does a row
  whose title an open milestone's file quotes: that milestone removes it
  when it finishes. In guest mode the
  row stays at the handoff. A later `/hotfix` run with the PR number edits
  it on disk after the maintainers merge, once you accept that run's check
  of the merged change.
- **The plan offers to assign you to an issue it resolves, in place of a
  comment.** When a plan absorbs a GitHub issue, the question set no
  longer offers a `Queued as M<NNN>: <title>` comment, or in guest mode a
  `Working on this: <issue title>` comment. It offers one option to assign
  your own account to each issue in the `Resolves:` slot, and posts no
  comment. The plan first reads your access to the repo. With less than
  triage access, or if the read fails, it offers nothing and says so in
  one line. The option
  description names each issue's current assignees. The assignment runs
  only if you select the option, after the milestone file is written. A
  failed assignment is named in chat and in the work log, and nothing else
  is written to GitHub for that issue.
- **In guest mode, text written for the host repo matches the host's own
  style.** The rule covers documentation (README, guides and vignettes,
  help pages and docstrings, code comments, changelog entries, and messages
  users see), commit messages, the PR title and body, and replies on the
  host's issues and PRs. That text now matches the host's existing text of
  the same kind in length, tone, and level of technical detail. The
  rulebook's "Collaboration mode" section states the rule, and the
  guest-mode line that the session hook injects carries it in short form,
  so it applies before any cairn skill loads. When another writing-style
  instruction in the session, from another plugin or your own, also covers
  that text, that instruction wins,
  and matching the host covers only what it leaves open.
- **The pane shows a blocked milestone whose file was archived before its
  row changed.** A cleanup after a merge can stop between moving the
  milestone file to the archive and setting its ROADMAP row to `done`. The
  pane then showed the row with no PR state and no button. Now, if exactly
  one archive file has the row's id and its `**Status:**` paragraph starts
  with `done`, the pane reads the PR from that paragraph and marks the
  line `archived`. A merged PR gets the Finish button, and the line gets no
  other button. In guest mode, `/milestone-review` accepts such a `blocked`
  milestone, sets its row to `done`, runs the checks, and names the
  archive, lesson, and review-brief work it skipped and the issue comments
  still owed. In owner mode it reports what
  it found and stops. `scripts/cairn_next.py` marks the line `archived`
  too.
- **`/milestone` reports news on the issues and PRs your candidate rows
  link to.** The health audit reads each link in a candidate row, whether a
  full GitHub URL, `owner/repo#N`, or a bare `#N` for the repo's own issues
  and PRs (the upstream repo's, in guest mode), and
  reports the item's latest close or merge, and each comment, review, or
  review-thread comment by someone else, since the row's latest date. A
  close or merge that GitHub records as yours is not reported. It runs in guest mode too,
  so a row that waits on another repo's merge or a maintainer's reply hears
  about it. At the triage chip you can update the row, which adds a
  `checked <UTC time>` mark so the same news is not reported again. If you
  leave it, the next audit reports it again, for a row that carries a date
  and that you did not update for another item.
  The read writes nothing to GitHub.
- **`/cairn-triage` runs in guest mode.** It used to stop at session
  start, because its pass ends in a commit to the default branch. In guest
  mode the pass now skips the clean-tree, default-branch, and sync checks,
  and its accepted edits are written to `cairn/` on disk and not committed
  or pushed. The hygiene stamp names the evidence for each item dropped as
  already shipped or as resting on a false premise, since no commit message
  holds it. `/cairn-release` still stops in guest mode.
- **In guest mode, pushes go to your fork, whatever its remote is
  named.** The rulebook finds the fork remote as the one remote whose
  GitHub parent is the base repo, and every guest push and the PR's
  `--head` owner use it. Before, guest pushes went to `origin`, which is
  the upstream repo in a checkout cloned from upstream with the fork added
  under another name. With no such remote, or more than one, a guest push
  stops and names the remotes it read.
- **`/milestone` names the repo in every `gh pr` and `gh issue`
  command.** The CI re-check, the merged-PR check, the inbox reads, the
  orphaned-issue read, the outside-merge reads, and the orphan close now
  pass `--repo` with the base repo, so a checkout with two remotes reads
  the right one.
- **The issue look-in's reply hand-off passes the reply as a file.** The
  draft goes to a file in the system temp directory, and the command to
  post it is `gh issue comment --body-file`, so no shell quoting touches
  the reply. You can edit the file before you post.
- **The audit's rulebook-size line counts bytes.** It used `wc -l -m`,
  whose character count changes with the shell locale. It now uses
  `wc -l -c`.
- **Edit-work subagents run on Haiku 5.5.** Mechanical migrations, test
  writing against a spec, and boilerplate now spawn Haiku 5.5, not
  Sonnet. Explore searches and the two history reviewers moved to Haiku
  later (see the entries above), and Opus and Fable roles do not change.
  The "Never Haiku" rule is gone. The session still reads each Haiku diff
  and runs the profile's `verify` checks before it commits. A
  side-by-side test measured migrations and test writing, and boilerplate
  follows that result untested. On three edit tasks both models scored the same, and
  Haiku cost $0.04 where Sonnet cost $0.49 (the cairn repository's
  `cairn/references/haiku-sonnet-roles.md`).
- **In guest mode, `/milestone-plan` reads the upstream repo's open issues
  and PRs.** Its inbox reads now pass `--repo` with the base repo, so a
  plan can find an upstream issue that the planned work resolves. An
  overlapping upstream PR becomes a candidate row that names the
  maintainers, since the rulebook does not support adopting a PR through
  `/hotfix` in guest mode.

### New

- **`/cairn-triage` keeps started tokens current.** A triage pass now
  reads each candidate row's ` — started M<NNN>` and ` — started #<n>`
  tokens. It proposes removing a dead token, which names a milestone that
  is `done`, `dropped`, gone from the table, or archived, or a PR that is
  merged or closed. It reads each PR's state with `gh pr view`. It also proposes
  adding a missing ` — started M<NNN>` token to a row whose short title a
  planned, in-progress, blocked, or review milestone file quotes in double
  quotes outside its Scope Out list. Each token change waits for your answer at the triage gate,
  beside the row's disposition. A row that carries a live token stays
  `keep`, so no triage disposition removes the token that hides the row
  in the pane. The row can still be re-rated, gain a merge survivor's lineage
  clause, or lose a dead token beside the live one.

- **A started token on a candidate row hides it in the cairn pane, guest
  mode included.** `/milestone-plan` now ends each candidate row that a
  plan absorbs with ` — started M<NNN>`, in owner and guest mode. In guest
  mode, `/hotfix` ends each row it matched with ` — started #<n>` on disk
  after it opens the PR for the maintainers. The pane leaves out of its
  Candidates list a row with an `M<NNN>` token while that milestone is
  `planned` or `blocked`, and a row with a `#<n>` token while PR #n is
  among your open hotfix PRs. A row that hygiene narrows loses its token.
  The token opens with ` — `, so the row's short title stays the same.

- **A normal-priority candidate row in the cairn pane shows `○`.** The
  open circle replaces the `·` mark, so the candidate marks read `↑` for
  high priority, `↓` for low, and `○` for normal.

- **The cairn pane hides a candidate row that an open PR already works
  on.** In owner mode, `/hotfix` and `/milestone-review` now put one
  `Candidate row: <short title>` line in the PR body for each candidate
  row that the merge removes or narrows. The pane's existing `gh pr list`
  call reads each of your open PRs' bodies, and the pane leaves out of its
  Candidates list each row whose short title a line names exactly. The
  Candidates heading counts only the rows it shows. A guest-mode PR
  carries no `Candidate row:` line. The PRs that hide rows change only
  when the pane reads its PRs, and the pane lists candidate rows only
  while no milestone is active. A PR opened before this change
  has no `Candidate row:` line. A `Candidate row:` line inside a fenced
  code block names no row. Such a block runs from a line that opens with
  three backticks or three tildes, after optional spaces, to the next
  such line or the end of the body.

- **A close names the Copilot opt-in line when Copilot reviews a PR with
  the round off.** In a repo whose `cairn/PROFILE.md` lacks
  `# Copilot review: on`, cairn does not handle Copilot's threads. When
  someone or something else already asked Copilot to review the PR, the
  close after a `/hotfix` or milestone merge made in that run, or after a
  guest handoff, says so in one line and names the line to set. This
  covers only PRs the round itself would review. It runs one read-only
  query at the close, so a Copilot request made after it goes unreported,
  and it requests, replies to, and resolves nothing.
- **`/milestone` looks into one GitHub issue.** Give it an issue number or
  URL, and it reads that issue and the code the issue names. It reports one
  verdict (`reply`, `hotfix`, or `milestone`), one maintainer-input level
  (`none`, `confirm`, or `decide`), file:line citations, and a reproduction
  or the reason none was run. One question then starts the work now, adds a
  candidate row, leaves the issue with a stated reason, or stops. A hotfix
  or a plan starts through `/hotfix` or `/milestone-plan`. A reply is
  drafted and shown with a `gh issue comment` command for you to run, and
  cairn never posts it. In guest mode the commands name the upstream repo,
  the draft uses no cairn terms, and a candidate row stays on disk.
  A reply declines a request only when the reason is on record. In owner
  mode the record is a decision entry, a `cairn/DESIGN.md` line, or a
  dropped milestone's archive summary. In guest mode it is the upstream
  repo's own docs or a maintainer's statement on GitHub. A decline with no
  such record gets the `milestone` verdict at the `decide` level, and the
  recommended option adds a candidate row, so the record lands in cairn.
  The rulebook's intake rule names the reply and `/milestone-plan` routes
  for issues.
  In guest mode, the optional issue comment that `/milestone-plan` offers
  now names the upstream repo and reads `Working on this: <issue title>`,
  with no milestone number.

- **An opt-in Copilot review round on hotfix and milestone PRs.** With
  `# Copilot review: on` in `cairn/PROFILE.md`, `/hotfix` and
  `/milestone-review` request a Copilot review on the PR, only when the PR
  has no Copilot request or review yet. In owner mode `/milestone-review`
  opens the PR at the start of review, so Copilot works during cairn's own
  checks, and the PR-conversation read before the merge question handles
  each unresolved Copilot thread: it is fixed, rejected with a reason, or
  sent to a candidate row, then gets a reply with no thanks and is
  resolved. A review still pending at the read gets a wait of up to 10
  minutes, once per pass, and then the run goes on and says it is pending.
  In owner mode a hotfix opens its PR before its approval chip, and a
  decline closes the PR and keeps the branch. In guest mode the round runs
  after the handoff. Adopted PRs, a review of an already-merged PR, and
  milestones with companion checkouts skip it.
  GitHub's settings choose the review level, because its API took none per
  request when this shipped; the report names the level from the review.
  The rules live in `skills/shared/copilot-review.md`.

- **The `/milestone` health audit lists your open hotfix PRs.** A new
  "Open hotfix PRs" item in its §2 runs one `gh pr list --state open
  --author @me --limit 100` call on the base repo, in owner and guest mode.
  It reports each PR from a `hotfix-` branch with its number, title, and
  review decision, and shows an empty decision as `none`. It says when the
  list can be cut at 100. It proposes no action and writes nothing to
  GitHub. When the call fails, it names the cause and lists no PR. Before
  this change, the inbox check dropped `hotfix-*` PRs and no other check
  reported them.

- **The cairn pane lists your open hotfix PRs.** A `/hotfix` run has no
  ROADMAP row, so the pane finds its PR on GitHub. Each time the pane
  opens, and at each ↻ press, it runs one `gh pr list --state open
  --author @me --limit 100` call on the base remote: `upstream` in guest
  mode when the repo has that remote, else `origin`. Each PR from a
  `hotfix-` branch takes a line under a `HOTFIXES` heading, after
  `BLOCKED` and before the candidates. The line shows `#<n>`, the title,
  and the same state word and count line that a blocked PR gets. A hotfix
  line has no Button. When the list call fails, the pane keeps the last
  list it read for the same repo.

- **The cairn pane counts each open PR's unresolved review threads.**
  Under a `BLOCKED` or `HOTFIXES` line whose PR is open, a line such as
  `3 unresolved threads` shows the review threads not marked resolved, a
  bot's threads included. A review or comment with no thread does not
  count, because GitHub does not link a reply to it. The count covers the
  newest 100 threads. Each time the pane opens, and at each ↻ press, it
  reads them in the same `gh api graphql` query that gives the PR's state.

- **The cairn pane has one ↻ Button.** It sits at the right end of the
  pane's first line, the first milestone's line or `no active milestone`,
  and shows whenever the pane has a ROADMAP, with or without PRs. A press
  reads the tracking files, the hotfix PRs, and each PR's state again. The
  ↻ reads `⋯` while a read runs, and a press while an earlier ↻ press's
  read runs does nothing. After a plugin reload, a stored reading state
  with no read running draws ↻, not `⋯`.

- **A ✎ Button on each candidate row in the cairn pane plans that row.**
  While no cairn skill runs or waits on its background work, each row in
  the pane's `CANDIDATES` list carries ✎ at its right end, but for a row
  whose short title is empty. The short title is the row's text after a
  leading `[high] ` or `[low] ` token with its space, up to its first
  `: `, with outer spaces removed. A press runs `/clear`, and then
  `/cairn:milestone-plan` with that short title in the cleared
  conversation. A press while Claude works outside a cairn skill runs when
  Claude is idle. While another button's command runs or waits for its
  `/clear`, or a ⌂ press waits for its `/clear`, a press does nothing.

- **The cairn pane has a ⌂ Button that clears the conversation.** It sits
  just before ↻ on the pane's first line while no cairn skill runs or
  waits on its background work. A press
  runs `/clear`, and when that `/clear` ends the session, the pane is
  opened again. A press does nothing while another button's command runs,
  while `Plan` or `Implement` waits for its `/clear`, or while an earlier
  ⌂ press waits for its `/clear`. The pane's Next line no longer carries a
  `Clear` button after a cairn skill ends. The band keeps its `Clear`.

- **The cairn pane fills again after `/resume` and after a `/clear` behind
  another tab.** A `/resume` reads the tracking files again, as a `/clear`
  that keeps the session's process does. After either one, a placed pane
  reads its PRs again, also when it sits behind another tab. A pane not
  yet shown, as in a narrow terminal, reads them when it is first drawn,
  unless an open read them first. A pane placed while a `/clear` start
  lists the panes reads them with no further draw. One start reads them once, also when a
  reopen at a new session start and the `/resume` both run in it. Before, a `/resume` left the band and the pane empty until
  the next prompt.

- **A pane head line shows the milestone id in its phase's color.** The
  phase word before the id is gone, and the id takes the implement or
  review color.

- **The cairn pane shows each blocked milestone's PR state.** After its
  `#<n>`, a `BLOCKED` line shows `merged`, `closed`, `changes requested`,
  `approved`, or `in review`, or `unknown` when the read fails. A PR on
  github.com takes one `gh api graphql` query for its state and its
  count. A hotfix PR on another host takes one `gh pr view <url> --json
  state,reviewDecision` call and gets no count. A `merged` line
  carries a `Finish` Button that runs `/cairn:milestone-review <id>`, a
  `changes requested` line a `Revise` Button that runs
  `/cairn:milestone-implement <id>`, and a `closed` line a `Check` Button
  that runs `/cairn:milestone`. None of them runs `/clear` first. The pane
  reads the states each time it opens and when you press ↻, never on a
  timer. The read needs `gh` on the
  session's `PATH`.

- **The cairn pane lists blocked milestones and their PRs.** A `BLOCKED`
  section after the queue shows each `blocked` milestone, with or without
  an active one. A line ends with `#<n>` when the milestone file's
  `Branch/PR` header names a GitHub pull request URL before any
  `companion:` entry. In guest mode, this lists
  the PRs you handed to the maintainers. `scripts/cairn_next.py` prints
  the same number after each "Externally blocked" line.

- **The cairn pane comes back after `/clear`.** A cairn pane that is shown
  at a `/clear` is open after it. A press of a Clear, `Plan`, or
  `Implement` Button keeps the pane. After a typed `/clear` in the desktop
  app, a pane that was shown opens again at your next message, in the same
  folder. An app quit or a closed terminal that ends the session with
  reason `other` (not checked) also brings the pane back at the next
  session in that folder. The desktop app is the surface checked live, for
  a typed `/clear` and both Clear Buttons. A `Plan` or `Implement` press
  clears through the same call.

### Fixes

- **A direct edit from `/milestone-plan` removes the candidate row it
  fixes.** When the plan finds a trivial edit and you take that route, it
  now finds each candidate row whose short title your request quotes, such
  as a row you pressed in the cairn pane, and that no started token claims.
  The edit deletes a row it fixes in
  full and narrows a row it fixes in part, in the same commit (in guest
  mode, on disk). The route's option names each row before you choose. A
  row that a planned or active milestone quotes is left for that milestone.

- **In guest mode, `/milestone-plan` no longer sends a pull request to
  `/hotfix`.** A request that names a pull request, such as a PR URL or
  "adopt PR 12", skips the tier check. If the PR is your own open or merged
  `hotfix-` handoff, the plan stops and points you at `/hotfix` with the
  PR. For any other PR, a closed one included, it stops and says that guest
  mode does not adopt someone else's PR. A bare `#N` is still read as an
  issue.

- **A plan picked at `/milestone`'s triage gate asks no tier question.**
  When you choose `/milestone-plan` for an item at `/milestone`'s triage
  gate, the plan treats the work as a milestone without asking again
  whether a hotfix or direct edit fits. This holds within the same session.

- **A `/hotfix` rerun on an open hotfix PR finishes the merge you
  approved.** When a hotfix stopped at its CI wait, its close block told you
  to rerun `/hotfix` with the PR number. While the PR was still open, that
  rerun started over as if it were adopting an outside PR: tier check,
  regression test, review, and a second merge question. Now `/hotfix` writes
  its merge approval, with the head commit you approved, before the CI
  wait, and merges only that commit. A rerun goes back to the CI wait and
  merges with no new question only when the PR's head is the same commit,
  no review requests changes, and the candidate rows it matches are the
  ones the PR body names. Otherwise, the rerun runs the full hotfix checks
  again and asks you again.
  In guest mode, a rerun on an open hotfix PR reports its state and
  review decision and stops, since the merge is the maintainers' to make.

- **A `/hotfix` rerun on a closed PR, on your own open hotfix PR, or on a
  guest PR with requested changes has a route forward.** Before,
  these reruns started the walk for adopting an outside PR, which cannot
  merge a closed PR and which guest mode does not allow, or stopped with
  no way forward.
  - A rerun on a PR that closed without a merge now stops. It says the PR
    closed, leaves reopening it to you on GitHub, and names a candidate
    row whose started token points at that PR. In owner mode it removes a
    hotfix merge approval that names the PR. Its next command is `/hotfix`
    with a description of the bug, which starts over on a new branch.
  - In owner mode, a rerun on your own open `hotfix-` PR that no recorded
    approval resumes runs the full hotfix checks on it as your own fix,
    not as an outside PR. With the Copilot round on, Copilot reviews it as
    it reviews any hotfix you wrote.
  - In guest mode, when the maintainers request changes on your open
    `hotfix-` PR after its newest commit, a rerun reads the PR's
    conversation and makes a change for each request, or says why it makes
    none. It runs the hotfix checks again and then asks you once before
    it pushes to your fork. It posts nothing on the PR, so the reply to
    the maintainers stays yours. A request older than the newest commit
    means the PR waits for a new review, so the rerun reports and stops.

- **The cairn pane right-aligns pull request numbers and states.** On a
  Blocked or Hotfixes row, the number and state word (for example `#786  in
  review`) now sit at the right edge of the pane. Before, they followed
  the title directly when the title was short enough to fit, and sat at
  the right edge only when the title was cut.

- **Three session-end races in the cairn pane are closed.** If the session
  end beneath the plugin fails, the pane Buttons now work again after it,
  even when the press's `/clear` never finishes. The next-step Button can
  hold a command for that end. That command now goes to the prompt box,
  and a toast reads `cairn: the session end failed (<command>)`. Before,
  the Buttons stayed dead and the command was dropped with no notice. A
  session end while a `⌂` press reads the stored state now cancels the
  press, so its `/clear` no longer clears the conversation that follows.
  A `/clear` end still opens the pane. At a `/clear` start, a second pane
  listing still waiting at a session end now reads nothing. A read that a
  later start owes is that start's own read.

- **A pane placed during a `/clear` start reads the pull request states
  with no further draw.** At a `/clear`, the plugin lists the panes. If the
  cairn pane is placed, the plugin reads the states of the pull requests
  that the pane shows. If it is listed but not placed, its first draw
  starts that read. Some
  panes were placed and drawn while that list was still waiting. That draw
  came before the read was owed, so the state words waited for a further
  draw. Now the plugin lists the panes a second time. If the pane is placed
  by then, the plugin reads the states.

- **A session end frees the pane Buttons from a press still reading.** A
  Status, Clear, next-step, blocked-line, or `✎` press reads the stored state
  before it runs its command. While that read waited, the other pane
  Buttons except `↻` did nothing, through a session end too. A read that
  never finished kept them dead until a reload. A read that finished after
  the end then ran its command late. Now the session end frees the
  Buttons, and a press cut off this way runs nothing. If the session end
  beneath the plugin fails, a `⌂` press still opens the pane at its
  `/clear` end.

- **The Copilot review wait lasts 25 minutes, not 10.** With
  `# Copilot review: on`, a hotfix or a guest handoff waits for a pending
  Copilot review before it reads the PR. Copilot's reviews often came
  after the 10-minute wait ended, so their threads went unhandled. The
  wait now lasts up to 25 minutes. It reports only a change in the
  review's state, so it no longer posts "pending" every 30 seconds.
- **A quick second press of a band or pane button runs no second
  command.** The `Plan`, `Implement`, `Resume`, `Review`, `Status`, and
  `Clear` buttons, and a blocked line's `Finish`, `Revise`, and `Check`,
  each read the step and the stored state before they run. Before, a
  second press of these buttons during those reads also passed the busy
  check, so both presses went on: both ran their command, or, for `Plan`
  and `Implement`, both ran `/clear`. Now a press
  marks the buttons busy before its reads start, so a second press during
  them does nothing. A press whose reads find nothing to run frees the
  buttons again.
- **`/cairn-pane` opens the pane after a typed `/clear`.** With the pane
  open, a typed `/clear` in the desktop app took it off the screen. When
  the next message was `/cairn-pane`, the session start reopened the pane,
  and the command then closed it and printed `cairn pane closed`. You had
  to run the command twice. Now that first `/cairn-pane` leaves the pane
  open and prints `cairn pane opened`.
- **The cairn pane opens without waiting for GitHub.** `/cairn-pane`, the
  band's open button, and the reopen at a session start now return without
  waiting for the reads from GitHub. Before, each one returned only after
  the `git` and `gh` reads of
  the pull request states and the hotfix list. The hotfix list's calls ran
  first, one after another, and then the PR state reads ran. Each call has
  a 15 s timeout. The blocked PRs' reads now start without waiting for the
  hotfix list call. The words and counts appear together when the last
  read settles.

- **The pane's PR words come back after an in-process `/clear`.** A
  `/clear` that keeps the session's process, as a `Clear`, `Plan`, or
  `Implement` press does, keeps the pane open. Before, the PR words,
  counts, Buttons, and hotfix list stayed empty until the next open or
  `Refresh`. Now a placed pane reads them again, also one behind another
  tab.

- **A hotfix PR that is also a blocked milestone's PR shows once.** It
  stays on the blocked line, which carries any Button its word calls for.
  The `HOTFIXES` count leaves it out, and when it is the only hotfix, the
  section is gone.

- **The pane's `gh pr list` call carries no remote credentials.** When the
  base remote is an `http` or `https` URL with a user name or token in it,
  such as `https://token@github.com/o/r.git`, the pane drops that part
  before it passes the URL to `gh`. Other URL forms pass unchanged.

- **`/hotfix` follows the repo's own conventions.** It reads the
  Conventions section of `cairn/DESIGN.md` and applies each per-change rule
  there, for example a development-version bump on every PR. The approval
  gate shows the bump. When the section states no such rule, `/hotfix`
  bumps no version.

- **`cairn_cost.py` counts each API call once and reads subagent
  transcripts.** The session store writes one call as several records that
  share a `message.id`, and a resumed session copies earlier calls into its
  own file. The script summed every record, so its turn and token figures
  ran high. It now merges the records of one call. It also reads each
  session's `subagents/agent-*.jsonl` files as part of that session, so the
  figures include the turns of spawned subagents. The store can keep a
  call's output count from the start of its stream, so the report and the
  `--audit-line` output label output tokens as a lower bound. Cost figures
  measured with the old script are not comparable with new ones.

## 2.0.0 (2026-10-06)

### Changes that affect existing repos

- **One question set, then the agent runs the milestone to the merge
  question.** `/milestone-plan` asks one question set, then invokes
  `/milestone-implement` itself. When its tasks pass, implement invokes
  `/milestone-review`. The set asks only what you alone can settle. That
  is what to work on, open choices about what you will get, and files,
  access, or looks that implement or review will need. It also asks
  permission for foreseen outward actions and dependency changes. The
  agent decides criteria wording,
  criteria-audit findings, splits, approach, test scope, and changelog
  entries, and logs each in the milestone's work log. Implement asks no
  question round of its own. It stops only at a listed stop, such as an
  action the question set did not cover or an amendment that changes what
  you get. Review settles each reviewer finding itself. It rejects a
  finding that is false, a style or linter item, or a complaint about a
  planned change, with the reason. It fixes a real finding inside the
  milestone's scope on the branch, and it sends the rest to candidate
  rows. The merge question lists each finding's outcome. A merge ends the
  run. The closing message gives `/clear` and the command that starts the
  next milestone of the same plan, so each milestone starts in a fresh
  context. Typing `/milestone-implement` or `/milestone-review` with the
  milestone id resumes a stopped run. The routing section that
  `/cairn-init` writes into a new `CLAUDE.md` describes the run. Repair
  never rewrites a section a repo already has, so an existing section keeps
  its old wording until you edit it by hand.
- **The pull request opens after you approve the merge, not before the
  review.** `/milestone-review` no longer pushes the branch or opens a
  draft PR at its start. After you approve at the merge question, it
  pushes the branch and opens a ready PR. The PR body carries the
  `Closes`/`Refs` lines. Then review waits on CI and merges. A
  `pull_request`-triggered CI suite so first runs on the head that merges,
  not on every push before your approval. The cost is that the CI wait
  comes after your approval. The merge question names the branch and the
  default branch. `/hotfix` does the same for a fix it authors: after your
  approval, it pushes and opens the PR. If an issue exists, the PR body
  carries `Fixes #N`. An adopted PR's path is unchanged.
- **Review records its findings in fixed line formats.**
  `/milestone-review` now logs each finding in the Review section as
  `<lens> #<rank>: <finding> — <disposition>`. The lens is `diff-bug`,
  `blame-history`, or `prior-review`. A reject names its reason and its
  ground: false, style, or planned change. A fix-now line gains
  `, fixed <sha>` once its fix is committed. Each review pass that spawns
  reviewers writes one `spawned: <lens>, …` line, and a degraded
  (author-inline) pass writes none. A declined merge question writes the
  work-log line `step-7 decline: <what was requested>`.
  `/milestone-implement` writes a substantive amendment's work-log line
  with `substantive amendment:` after its date. The merge question counts
  the milestone's amendments from those lines and the `amendment return:`
  lines.
- **A plugin repo with no `cairn/PROFILE.md` now infers `claude-plugin`.**
  If the repo has no R or Python marker, this rule applies. Before, it
  inferred `generic`, or `docker-image` if a `Dockerfile` was present. Its
  verify step now runs the `claude plugin` checks. If `/cairn-init` repair
  backfills the file, it writes the same profile.
- **Subagent titles no longer open with a model tag, and the session sets
  the model on every spawn.** The rulebook drops the rule that every Agent
  description starts with a one-letter tag for the model: S, O, or F in
  brackets. Each skill now names the model that a role calls for in words,
  for example "a fresh-context Opus reader". The session passes that model
  as the Agent tool's `model` setting. A spawn that sets no model gets the
  default of the agent type or the harness.
- **Inside a run, the session no longer ends its turn while work is still
  owed.** The rulebook names four unwanted turn endings while a task,
  check, or record is unfinished. They are a recap that names the next
  step and does not take it, an offer to carry on, a list of decisions
  that need no stop, and a stop to report because the turn was long. The
  run stops only where it needs you or a guard blocks it.
- **Closing messages say whether the next command waits on CI.** Where the
  work has a branch or an open PR, the closing message carries one plain
  sentence about CI. It says whether the next command waits on CI itself
  and what you do meanwhile.
- **User-facing prose is read against the code before review.** In a
  milestone whose `Surface tier:` is `user-facing`, `/milestone-implement`
  starts a fresh-context reader. The reader takes the lines that the
  branch adds outside `cairn/` and reads each claim about what the code
  does against the code. False claims get corrected. The work log gets
  `claim audit: <N> claims read, <K> corrected — <files>`, or
  `claim audit: not owed — <reason>`. Before the release commit,
  `/cairn-release` reads each behavior claim in the consolidated changelog
  section against what it describes.
- **File edits go through the Write and Edit tools.** While a cairn skill
  runs, the session edits repo files with those tools. It does not use
  shell redirection or scripts. The desktop app's per-turn "Edited N
  files" card so lists every file that a turn changed.

### New

- **A milestone band above the prompt.** The plugin now ships a Claude Code
  mod (`hooks/status/register.tsx`, named under a new `modules` key in
  `hooks/hooks.json`). In a cairn-tracked repo it draws one row above the
  prompt for the milestone in flight: the first `in-progress` row of the
  ROADMAP, else the first `review` row. While `/milestone-review` runs, it
  shows the first `review` row instead. The row shows the id in bold and
  the title at the left. At the right it shows a flow track of three equal
  parts, plan, implement, and review, and the percent of the whole flow.
  Implement fills by the checked boxes of `## Tasks`, and review by the
  checked boxes of `## Acceptance criteria`. A pill on the edge of the fill
  names the phase and its counts, such as `Implement 1/3`. In the desktop
  app the track is an image. In the terminal it is braille characters in
  your Claude Code theme's colors. The fill and the pill take the color of
  the current phase: `planMode` for plan, `claude` for implement, and
  `success` for review. With no active milestone, the row
  names the next milestone you can start, as `scripts/cairn_next.py` picks
  it. With none, it shows `No milestone ready`. While no cairn skill runs
  and Claude is not working, the row carries two buttons where it has room
  for them. The next-step
  button reads `Implement`, `Resume`, `Review`, or `Plan`, and `Status`
  runs `/cairn:milestone`. After a cairn skill ends, a `Clear` button shows
  before them. In a narrow row, `Clear` goes first. `Plan` and
  `Implement` run `/clear` first and then their
  command in the cleared conversation, and they do not ask first. As if
  you typed it, each other button runs its one command. If the run is
  refused, the command goes into the prompt box and a toast says why. A
  close button hides the band. The band comes back when the list of active
  milestones changes, when the next workable milestone changes, or when
  the session ends. A `≡` button opens the cairn pane. The band reads the
  files at session start, at the end of each turn, and at a cairn skill's
  start or end. It also reads them after Claude edits or writes a file
  under `cairn/`. It never shows another repo's milestones. It needs Claude Code 2.1.287 or
  later, where mods are on by default, or an earlier version with hooks
  modules turned on. See "The milestone band" in the README.
- **A cairn pane.** The new `/cairn-pane` command opens a pane that shows
  more than the band, and the same command closes it. The band's `≡`
  button also opens it. For each `in-progress` or `review` milestone, the
  pane shows the phase, id, title, percent, and goal. It lists every task
  and acceptance criterion with `✓` or `○`, and the five newest work-log
  lines. Below them it shows the next command in a pill and the workable
  planned milestones. It also shows the planned ones that wait on others,
  as `scripts/cairn_next.py` gives them. With no active milestone, it also
  lists the ROADMAP's candidate rows, marked `↑`, `·`, or `↓` by priority.
  The Next line carries the same next-step, `Status`, and `Clear` buttons
  as the band. A press acts as the band's button of the same name. The
  pane's buttons also show while Claude works outside a cairn skill, and a
  press then waits for the turn to end.
  Outside a cairn repo, with no pane open, the command prints
  `no cairn ROADMAP found`. `scripts/cairn_next.py` gains `recommend` and
  `waiting`, and its output is unchanged. See "The cairn pane" in the
  README.
- **A `claude-plugin` toolchain profile.** A repo that builds a Claude Code
  plugin, a marketplace, or a mod can now declare it. Its verify step runs
  `claude plugin validate` on each plugin's `.claude-plugin/plugin.json` and
  on the marketplace file. Where the repo has `*.test.ts` or `*.test.tsx`
  files, it also runs `claude plugin test`. It says where to find the
  `claude` binary when a desktop app shell has none on its PATH. The release
  walk bumps `version` in each plugin manifest and each marketplace entry
  that carries one. `/cairn-init` selects it when `.claude-plugin/plugin.json`
  or `.claude-plugin/marketplace.json` is at the repo root, after the R and
  Python markers and before a `Dockerfile`. A repo with markers for two
  kinds of deliverable gets a question about which one is primary. The
  project-type question for an empty repo lists the new profile.
- **Guest collaboration mode: run cairn in a repo you do not own, with
  `cairn/` kept local.** A second header line in `cairn/PROFILE.md`,
  `# Collaboration mode: guest`, switches the mode. With no such line, the
  repo is in owner mode and the earlier rules apply. `/cairn-init` asks
  which mode applies and recommends one from
  `gh repo view --json viewerPermission`. In guest mode it writes `cairn/`
  to git's exclude file and writes nothing else outside `cairn/`: no
  CLAUDE.md section, no ignore entries, no CI edit, and no scaffold commit.
  `cairn_validate` checks the mode. In guest mode it requires the exclude
  line and fails while any `cairn/` file is tracked. The session hook
  injects the routing section from the plugin's own template. The commit
  guard denies a `git commit` that it sees carrying a `cairn/` path.
  You get tracking on disk in the turn that changes the code, and it is
  never committed. Branches, commits, and PRs carry no cairn vocabulary,
  and the milestone branch is named `<slug>` alone. The base remote is
  `upstream` when it exists, else `origin`. Branches are cut from its
  default branch and pushed to your fork, and the PR targets the base
  repo. cairn never merges in guest mode. `/milestone-review` and `/hotfix`
  end with a handoff gate. You hand the branch to the maintainers, which
  pushes it and opens a ready PR against the base repo, or you decline. A
  handed-off milestone is set `blocked`, and `/milestone` routes it by its
  PR's state: a merged PR to the closing hygiene, a closed PR to a
  question, and a PR with changes requested to `/milestone-implement`.
  `/cairn-release` and `/cairn-triage` stop in guest mode, and `/hotfix`
  does not adopt a third party's PR. In guest mode, DESIGN.md principles
  are your working model of the maintainers' constraints. They come from
  the maintainers' public contributor docs, and their feedback corrects
  them. The r-package consistency gate explains the `check()` NOTE for the
  `cairn` directory by the mode.

### Fixes

- **Run edge cases in the skills.**
  - One amendment return counts once. Only `/milestone-implement` writes
    the counted `amendment return:` line, and `/milestone-review` writes
    an `amendment routed:` line that no count reads.
  - When the `release window` advisory fires, the review close block puts
    `/milestone` first only when the next command names the flagged
    release. Otherwise the next command stays first and `/milestone`
    follows it.
  - The `/milestone` audit counts a candidate row and the rows that quote
    its exact title as one group. A group with review findings from two or
    more milestones gets the disposition question. When review files a row
    that refers to an older row, it quotes the older row's title.

## 1.12.0 (2026-09-07)

### Changes that affect existing repos

- **The ROADMAP keeps 3 terminal rows, down from 5.** `cairn_validate`'s
  `terminal-row retention` check now fails a ROADMAP table holding more
  than 3 `done`/`dropped` rows combined; the rulebook's terminal-row
  retention bullet and the `/cairn-init` ROADMAP skeleton comment say 3.
  A repo whose ROADMAP carries 4 or 5 terminal rows reds on upgrade with
  `N terminal rows (retention 3): …`; the remedy is to prune the oldest
  done/dropped rows from the table — they survive in `milestones/archive/`
  and git.

### New

- **A whole-list triage pass, on demand.** `/cairn-triage` reads every
  ROADMAP candidate row and every DESIGN.md known issue, proposes one
  disposition per item (keep, compress, merge, split, drop, promote, or
  route) at a single gate, applies what you accept in one docs-only
  commit, and records drops made on principle as a decision so they are
  found by search rather than re-added. Nothing triggers it and nothing
  is written before you answer.
- **`/cairn-init` says that tracking-only pushes start CI, and offers to
  add the `cairn/**` ignore for you.** When a repo has
  `.github/workflows/`, init runs `scripts/cairn_ci_paths.py --report`
  and explains that cairn's tracking-only commits (checkpoints, review
  records) reach the remote on every branch push and start the
  push-triggered workflows whose `branches` filter admits the branch;
  that a `pull_request` trigger reads the whole PR diff, so ignoring
  `cairn/**` helps `push` triggers only; and that a required check under
  branch protection stays pending on a path-skipped run. It then poses
  one approve/decline chip for the workflow files it can edit: on
  approval `--apply` inserts `- 'cairn/**'` under each file's `push` →
  `paths-ignore` (created when absent), adding lines only, keeping the
  file's line endings, and checking the edit against PyYAML's own reading
  before writing. The edited file is left uncommitted for you. `--apply`
  needs PyYAML (optional, used by that mode alone; exit 3 naming it when
  absent, nothing written) and refuses, byte-identically with a reason,
  any file it cannot edit as a pure insertion — an unparseable or
  multi-document file, no block-mapping `on`, anchors or merge keys under
  `on`, no `push` trigger, a `push` carrying `paths` or a flow-style
  `paths-ignore`, one already ignoring `cairn/**`, or a failed post-edit
  check. A refused file, and every file when PyYAML is absent, gets the
  by-hand suggestion for each `push` trigger that could take it.
  `--report` stays stdlib and writes nothing. The rulebook's git model
  states the same fact, and the wait rule's no-checks clause names it as
  one source.
- **A hotfix merged outside the session is still held to the hotfix bar.**
  Running `/hotfix` on an already-merged hotfix or adopted PR now verifies
  the merged diff after the fact: its regression test is proved to fail on
  the commit the PR was based on and pass on the default branch, the
  profile's checks run, and the changelog entry is checked. A missing test
  or entry lands through a follow-up PR with the usual approval chip; a
  clean result pauses at one acceptance chip before close-out, instead of
  jumping straight to it.
- **The amendment-time re-audit leaves a line a resumed session can read.**
  When `/milestone-implement` re-audits amended acceptance-criterion
  wording, it now writes one work-log line per criterion in a fixed shape
  (`re-audit: AC<N> (<full|reduced>) — …`); an absent line means the
  reader did not run. The once-per-criterion re-entry bound and its stop
  are read from those lines, not remembered. `/milestone-brief`'s ingest
  audit line now names the criteria it cleared
  (`ingest audit RR<NN> (full): cleared AC<list> — …`), and the re-audit
  exemption applies only to a criterion that list names whose amended
  text still equals the ingested text whitespace-normalized.

### Fixes

- **Skills work under the symlink install.** Each skill now says how to
  find the plugin directory when the shell leaves `CLAUDE_PLUGIN_ROOT`
  unset (the symlink install in `~/.claude/skills` does): it falls back to
  the skill's own base directory, so the rulebook reads and the
  `scripts/` commands no longer resolve against `/scripts/…`.
- **The commit and force-push guards see through environment prefixes.**
  A `git commit` or `git push` spelled with leading `VAR=value` words
  (`GH_TOKEN=x git push -f origin main`, `GIT_AUTHOR_NAME=x git commit`)
  is now guarded exactly like the plain spelling, as the merge guard
  already was; the three guards share one command-position pattern.
- **`cairn_cost` finds a milestone however its id is spelled.** The
  `--milestone` filter and the audit line now resolve ids by number, so
  `--milestone M057` and `--milestone M57` report the same milestone, a
  branch named `m57-…` is reported as `M057`, and branches of different
  zero-pad widths for one milestone land in one row instead of two.
- **The review close block hands you the slash command, as typed.** After a
  merge the copyable next-step lines are now `/clear` and the recommended
  skill command (for example `/milestone-plan`), never the path of the
  helper script that produced the recommendation and never a `claude `
  shell prefix, which is wrong when pasting into Claude Desktop.

## 1.11.0 (2026-09-02)

Six milestones since 1.10.1, on two themes: cairn now reads the repo's
GitHub issues and pull requests at the moments where they matter, and the
session-conduct rules that were untested (waiting on background work,
where chapters go) are now grounded in evidence. Backward-compatible:
existing tracked repos keep working unchanged.

- **A milestone can name the issue it resolves, and GitHub closes it at
  merge.** The milestone template gains a plan-owned `Resolves:` slot
  (`#N closes` or `#N partial`). Planning fills it, review ends the PR body
  with the matching `Closes` or `Refs` line and reads the issue back after
  the merge to confirm it closed, and a hotfix does the same for a
  `Fixes #N` issue. A partial fix rows the remainder as a candidate and can
  leave a "queued as" comment on the issue at the gate.
- **Open issues and pull requests are swept when you plan.** The planning
  collision check now lists the repo's open issues and open PRs from other
  authors. One that overlaps the goal being planned is posed at the question
  gate as a `Resolves:` entry or a candidate row; the rest are counted and
  left to the status audit. Nothing is written to GitHub, and an unreachable
  `gh` skips the sweep with a note rather than blocking planning.
- **Pull requests merged by someone else reach the health audit.** The
  `/milestone` audit lists PRs merged since the last hygiene stamp by anyone
  but the operator, shows which archived milestone summaries mention the
  files each one touched, and carries each to the triage chip: a candidate
  row, a hotfix, a planned milestone, or leave it.
- **Waiting on CI or background work follows one tested rule.** The old
  "one blocking wait" rule was replaced after an experiment over the
  harness's actual wait mechanisms (foreground timeout ceiling, background
  tasks, monitors, subagent notifications). Sessions now arm one watcher per
  wait, use a foreground `gh pr checks --watch --fail-fast` with a timeout
  under the ceiling for CI, report fresh state and stop the watcher on a
  timeout, and never leave a watcher armed at a commit, turn end, or
  `/clear` point. The experiment's findings ship as a reference note.
- **Chapter markers follow the stretches inside a phase.** A session that
  holds one phase now gets a chapter per task, per criterion, or per gate
  step rather than one chapter per phase, so the navigable table of contents
  is useful mid-milestone. Titles open with the item's label (`T3:`,
  `AC2:`), and the phase header is re-emitted at every session start,
  including after `/clear`.
- **Criteria and tasks carry their positional labels.** The milestone
  template's example items read `AC1:` and `T1:`, and the plan and implement
  skills state the rule: the label is the item's position from the top, the
  number Coverage cites, and inserting, removing, or reordering renumbers
  labels and Coverage lines together. The binding-criterion ingest form is
  unified to `ACn (BCm):` everywhere.

## 1.10.1 (2026-09-01)

- **CRAN comments stay short.** For R packages, the release walk now writes
  `cran-comments.md` in its conventional few-line form (check results, one
  line per NOTE, test environments, revdep summary) instead of restating
  NEWS, which produced a long file reviewers had to wade through.

## 1.10.0 (2026-08-30)

Four milestones since 1.9.0: the merge guard learns about multi-repo
sessions, cairn survives its first adoption by an outside repo, the shipped
scripts get a simplification pass, and mandated reviewers keep spawning under
a new Claude Code restriction. Backward-compatible: existing tracked repos
keep working unchanged.

- **Independent review survives the "no unrequested subagents" instruction.**
  Some Claude Code surfaces now tell sessions not to spawn subagents unless
  the user requested them, and sessions were reading that as forbidding
  cairn's fresh-context reviewers and criteria audits — silently checking
  work only with the session that produced it. The rules now state that
  invoking a cairn skill *is* the request for the spawns that skill requires;
  a session that still can't spawn must say so at the next decision gate,
  with the review declared degraded, and an author-only run is allowed only
  as a deviation you explicitly accept — never silently.
- **The merge guard understands multi-repo sessions.** An approval marker
  binds the repo it lives in: merges that target another repo (`--repo`,
  `-R`, a `GH_REPO=` prefix, or a `cd`-into-another-directory compound) are
  denied with guidance, instead of being waved through against the wrong
  repo's approval. A secondary repo's merge runs from a session working
  directory inside that repo, through that repo's own gate.
- **First outside adoption, and the fixes it forced.** A second repository
  was migrated onto cairn and ran a full milestone loop end to end. The
  friction found is fixed: `/cairn-init` now ships LESSONS and DECISIONS
  file templates instead of describing them, and the merge guard's messages
  cover the spellings that confused the pass.
- **Simpler internals, same behavior.** An advisory audit of the shipped
  scripts and hooks was applied: one shared test-module loader replaces
  three ad-hoc mechanisms, duplicate tests were merged, and several scripts
  lost needless indirection. No commands, checks, or outputs changed.

Five milestones since 1.8.0, on two themes: what a phase end routes you to,
and when a deferred item has to be decided rather than carried. Milestone IDs
also sort correctly now, and the README documents for the first time how
cairn checks a numeric result. Backward-compatible: existing tracked repos
keep working unchanged.

- **Phase closes route you to the right next command.** A close block's next
  command now comes from `cairn_next`, so a milestone that is already planned
  and workable sends you to `/milestone-implement` instead of back to
  planning. Review's hygiene step validates its own edits before committing
  them, and when that check flags a release window, the release offer takes
  the lead — it keeps its chip, the one place a close block still asks
  something. The status skill gained a matching entry so both surfaces give
  the same answer.
- **A candidate that keeps absorbing findings gets decided.** A backlog row
  that has collected deferred review findings from two or more milestones is
  no longer silently extended. The pass that would extend it stops and asks
  what to do instead: promote a bounded milestone, route what you have
  accepted to Known issues, prune the row, or extend it once on purpose.
  Rewriting the row shorter does not count as deciding it.
- **An accepted limitation lands somewhere durable.** When a milestone
  surfaces a limitation you choose to live with and no backlog row or fix
  covers it, review hygiene now writes it into `DESIGN.md`'s Known issues in
  the same commit, rather than leaving it in a closed milestone file.
- **Milestone IDs sort numerically.** IDs are written padded to three digits
  (`M007`, not `M7`), archive filenames carry the padded prefix, and the
  scripts resolve either spelling to the same milestone — so a directory
  listing is in id order and an unpadded reference still resolves. This
  repo's 99 legacy archive files were renamed once; adopting repos need
  change nothing.
- **The test floor says what makes a check discriminating.** The universal
  "what gets a test" rules gained a short passage distilling five principles:
  prove the check fails on a planted defect, give it a non-empty domain, have
  it state one fact independently, keep fixtures it must stay silent on, and
  assert identity or kind rather than mere presence.
- **The README says how numeric results are checked.** A new section states
  the rule for a repo that computes results — a statistic, a score, a fitted
  value: each one is backed by at least two independent kinds of check, a
  confidence interval's check is coverage, and what backs each number is
  recorded. Previously the doctrine shipped in the rulebook with no mention in
  the README, so it was invisible to anyone deciding whether to adopt cairn.

## 1.8.0 (2026-08-22)

Two milestones since 1.7.0, both about what the user actually sees at
decision points and phase ends. Backward-compatible: existing tracked repos
keep working unchanged.

- **What a decision needs to see now always renders.** Text a session emits
  before a tool call in the same turn is not reliably displayed, so substance
  the rules require the user to see — the evidence behind a decision chip, a
  drafted durable record, a handoff command — no longer relies on it. Such
  text now rides in one of the two positions guaranteed to render: the chip's
  own question and option text, or the turn's final rendered text; where the
  full text lives in a file on disk, the chip cites its path. (The 1.7.0
  release session itself lost its handoff checklist to this gap.)
- **Every phase ends with the same close block.** A skill or phase that hands
  the user a next step now ends with a fixed shape: a short recap of the
  outcome, a status line or table, the next command in a copyable fenced
  block with a plain-language label, and a note that adjusting course or
  `/clear` are both safe there. Routing chips at phase ends are retired —
  chips remain only where a real choice is made (approvals, acceptances,
  continue/stop), each posed in the same turn as its presentation and
  readable on its own, in plain language with no internal record identifiers.

## 1.7.0 (2026-08-22)

Four milestones since 1.6.0, on one theme: what a session says and records.
Chat and tracking prose now follow a stated plain-style rule, the lighter
planning audit asks the same instrument question the full one does, and
doctrine modules carry declared size budgets. Backward-compatible: existing
tracked repos keep working unchanged.

- **Sessions write plainer.** Two new rules govern prose. In chat, response
  length matches what the turn needs, plain words win over jargon (a term of
  art is glossed at first use or dropped), and stock filler, hype adjectives,
  and padding are out. In the durable records under `cairn/`, the same
  standard applies to what is written down: a work-log line, decision entry,
  or roadmap row states decision-relevant facts without characterizations the
  facts don't need. Text mandated to appear verbatim — a durable-record
  preview, the substance above an acceptance chip — is never compressed under
  either rule.
- **The lighter planning audit still catches a promise about the checker.**
  The audit question asking whether a criterion promises something about the
  deliverable or about the thing that verifies it now runs in the shorter
  internal-tier audit too, not just the full one, and its wording now reaches
  recording acts — a criterion that binds a work-log quotation or a mandated
  evidence line is flagged at planning time in every tier, and a
  mid-implementation rewording re-enters the question in either mode.
- **Doctrine modules carry their own size budgets.** When a family of lessons
  graduates whole into a doctrine module, the graduating work now writes a
  line and byte budget into the module's own header, sized from the graduated
  content plus stated headroom. Hygiene passes read each module against its
  stated budget by hand (`wc -l -c`, no validator), and going over means
  compressing or retiring content, never letting the module grow. The three
  shipped modules each carry a budget now.
- **The record rules were re-measured and kept.** The baselines behind last
  release's record-discipline rules were re-measured over the sixteen
  milestones since: record-caused review returns have fallen to zero,
  corrections batch to one superseding entry per milestone, and neither
  rule's retirement condition has fired. The full classification ledger is
  on file under `cairn/references/`.

## 1.6.0 (2026-08-17)

Ten milestones and a hotfix since 1.5.0, around one idea: how hard cairn
checks something now depends on what is at stake. A plan classifies whether
its deliverable is user-facing or internal, and the criteria audit, the review
fan-out, and the escalated-review path each scale to that answer. The other
half of the release is subtraction — the shipped rulebook, the lessons file,
and the roadmap backlog were each cut down, and one reporting tool retired.
Backward-compatible: existing tracked repos keep working unchanged.

- **Removed: `cairn_budget`**, along with the record-density advisory it
  reported and the budget-check step four skills ran before writing a record.
  The size caps it measured are unchanged and still enforced by
  `cairn_validate`; what went away is the separate while-you-write reporter
  and the four skill steps that called it.
- **Rigor scales to what's at stake.** Every plan now classifies its
  deliverable as user-facing or internal — anything unclear, or spanning
  both, counts as user-facing — and records the tier with its reason. Three
  things follow from that answer: the planning-time criteria audit runs in
  full for user-facing or escalation-flagged work and in a shorter
  two-question form otherwise; a review whose milestone is internal and whose
  diff is documentation only gets a single reviewer instead of the three-lens
  fan-out; and an internal-tier criterion has to quantify over a domain its
  named procedure enumerates directly.
- **Reviewers rank, the maintainer decides.** The numeric confidence score
  attached to each review finding is gone. Reviewers order their own findings
  by severity and you triage the ranked list at the merge gate, with every
  finding logged either way.
- **An escalated review comes back as advice, not orders.** A returning
  review report is advisory by default; its findings become binding criteria
  only when the brief asked for that in its request slot. A second escalation
  on the same question puts removal on the table as one of the options.
- **A review return narrows the promise.** When a finding defeats a criterion
  and the amendment surface opens, narrowing or holding the criteria set is
  the one recommended option; widening it stays available as an explicitly
  non-recommended alternative, taken at your selection and logged per
  criterion. The full criteria audit also now asks whether a criterion
  promises something about the deliverable or about the thing that verifies
  it — a promise about the instrument moves to the tasks or the gate
  procedure, or the criterion narrows.
- **A milestone that keeps coming back gets smaller, not re-cut.** At the
  thrash threshold the review now recommends descoping the milestone — narrow
  it to its already-verified criteria, send the remainder to candidates or a
  split, re-review what's left — or parking it as blocked. Re-cutting the same
  objective is still available but is never the recommendation, since it is
  the move that just failed.
- **The rulebook says less.** The shared tracking rules were rewritten to
  state operative rules only, leaving the reasoning behind each one to the
  decisions file and git history; the guard-craft doctrine module was removed
  whole and every site referencing it rewritten. Every rule the skills
  actually cite survived the cut.
- **The always-read records shrank.** The lessons file now carries one lesson
  (or one named family) per line, and a roadmap candidate row states the idea,
  why it is parked, what would promote it, and where it came from — nothing
  else. Both files were passed entry by entry against a committed disposition
  ledger rather than trimmed by feel.
- **Byte budgets beside the line caps.** The roadmap and lessons files now
  carry byte budgets as well as line caps — under 24,000 and 20,000 bytes
  respectively — so a file cannot defeat its line cap by growing wider lines
  instead of more of them. Judged by eye at hygiene passes with `wc -c`: no
  validator check and no new machinery.
- **The core loop is a diagram now.** The README's "The core loop" section
  draws the milestone cycle as a flowchart GitHub renders in place: the three
  phases with each gate named on the phase where you're asked, and an arrow
  back from review to implement when a criterion is unmet. The section showed
  a one-line arrow chain before, which had no way to show that return.
- **A plainer README.** The rest of the README was rewritten to read as
  ordinary prose, with its commands, its guarded claims, and its structure
  intact.

Fixes:

- **The hygiene stamp is checked while it can still be fixed.** Both places
  that rewrite the "Last hygiene check" line — the status audit and the
  post-merge pass — now tell you to re-run the validator after writing the
  stamp and before committing, and to fix an over-length stamp by rewriting
  it shorter rather than appending or splitting it. The length advisory
  already existed; nothing ran it while the stamp was still editable, so an
  over-length stamp could reach a commit and only surface afterwards. The
  post-merge pass previously said only to check weight caps, which measures
  a different thing and read as covering this.

## 1.5.0 (2026-08-14)

Six milestones since 1.4.0, most of them one arc: a review return that
defeats a recalled list is now repaired by narrowing the promise at the
return itself, and the guards locking that doctrine were rebuilt around
whole-text comparison after three review passes showed fragment matching
could not hold it. Backward-compatible: existing tracked repos keep working
unchanged.

- **A defeated enumeration is repaired at the return, not by a re-plan.**
  When a review finding defeats a criterion whose membership was fixed by
  the author's recall rather than decided by a procedure, and the only
  repair available widens the list, the return is now classified as a
  criterion-wording matter: it routes to the amendment track with its
  tighter two-attempt stop and never increments the defect count that
  escalates to a re-plan. The amendment takes the narrowing repair the
  planning rule states; a wider enumeration is not an admissible amendment.
- **Doctrine guards compare whole rules, not fragments.** A test locking a
  rule now holds a verbatim copy of the rule's entire text and compares the
  whole marker-bounded block, so an edit anywhere in the rule — a changed
  word, an inserted clause, a reordered or relocated sentence — fails the
  suite until the copy is deliberately updated in the same commit. Fragment
  anchors always left an unpinned remainder, and three consecutive review
  passes each inverted a rule through one. The guard-craft doctrine now
  states the two invariants this rests on (the pinned extent equals the
  block; the block equals one rule) and the instrument's declared blind
  spots (whitespace-only and insertion-related edge cases).
- **An observed failure backs a claim only as the failure it is verified to
  be.** An error, refusal, or red test reads the same whether it is the
  behavior under test or an artifact of malformed inputs, so a claim
  resting on one now verifies the failure's identity — its condition class,
  message, or signaling site — before the claim is written, and a test
  asserting a failure asserts which failure, with its passing control shown
  to pass for the claim's reason.
- **A derived figure is pinned or procedural, never free-standing.** A
  count or figure derived from the repo's artifacts either stands beside
  the procedure that produced it and the commit it was measured at, or is
  replaced by its derivation. The free-standing hand-written number — 
  stranded by the next edit and read as current until a review catches it —
  is the defect the rule deletes.
- **The criteria audit reaches everything a criterion promises.** Criterion
  wording amended mid-implementation now goes back through the planning
  audit's three questions with a fresh reader (once per criterion; further
  churn goes to the user), and a criterion citing a mutation or
  planted-defect check is asked whether its probes vary every axis the
  verified domain is free in, or stand one exemplar in for the family.

Fixes:

- The dangling-id check no longer warns on a migrated repo's references to
  its pre-migration milestone ids (322 spurious warnings measured in one
  adopting repo, now zero), so a real dangler is visible again; behavior in
  repos without a legacy directory is byte-identical to before.

## 1.4.0 (2026-08-05)

Five milestones since 1.3.0, aimed at one failure shared by all of them: a
record that says something the artifact does not. Plans now have to say how a
promise will be checked, reviews reopen only for a real breach, and prose about
what something does has to be read off the thing itself. Backward-compatible:
existing tracked repos keep working unchanged.

- **A criterion has to name what will check it.** An acceptance criterion that
  quantifies over a whole domain — every skill, all guards — now names the
  procedure that enumerates that domain, and a list the author typed from
  memory is not one. The procedure also has to cover the domain the criterion
  actually promises over rather than a proxy for it; the tell is membership
  fixed by recall instead of decided by a procedure. When a criterion fails the
  test, the repair is to narrow the promise until a stated procedure settles
  it, never to widen the list. Asked as the third question of the planning-time
  criteria audit, and again when a review report is ingested.
- **Review returns need a real breach.** Reopening a finished milestone now
  requires a criterion breach scored 80 or better, or a functional defect in
  shipped behavior scored 90 or better; findings below the floor are triaged
  and recorded without changing the milestone's status. A criterion that turns
  out to promise the wrong thing is reworded on its own separate track, which
  stops at the second attempt on the same criterion — so a review converges
  instead of circling.
- **A scripted edit is verified before the record that claims it landed.** A
  batched or scripted edit can match the wrong place or fail while its siblings
  succeed, and the record written next then asserts a change that is not there.
  Such an edit is now re-read at its target before anything claims it landed,
  an edit aimed at a document section anchors on text occurring exactly once in
  that file, and ticking a box is sequenced strictly after the write of the
  evidence it depends on.
- **Claims about behavior are derived, never composed.** Prose a branch adds
  about what an artifact does or contains — in tracking records, code comments,
  docstrings, changelog entries, or docs — is written against the artifact or
  an execution's output at the time of writing, not from recollection. Prose
  that only restates what its cited artifact already shows is replaced by a
  cross-reference, and a claim that would list an artifact's members points at
  the artifact instead.

Fixes:

- The marketplace listing's version number, left at 1.2.0 through the 1.3.0
  release, now tracks the plugin's own version.

Also on file: a first-hand read of another Claude Code skill's architecture,
under `cairn/references/`, with every finding dispositioned and three follow-up
ideas parked as candidates.

## 1.3.0 (2026-07-31)

Seventeen milestones since 1.2.0, dominated by one correction: a pre-review
verification step adopted earlier this month grew into the repo's largest
session cost and repeatedly failed to converge, and after a rebuild and two
rounds of stopping rules it was retired outright. The rest of the release
tightens how plans are audited, how gates read, and how a session resumes.
Backward-compatible: existing tracked repos keep working unchanged.

- **The pre-review certification step is gone.** Having a fresh reader
  re-check every guard description before review was measured as the dominant
  cost of a milestone and kept looping without converging; it was rebuilt,
  given stopping rules, and finally removed whole. What survives is the
  cheaper instrument that worked: a fresh-context audit of acceptance
  criteria at planning time, which asks of each criterion what state of the
  world satisfies it as written and whether any standing rule makes that
  state unreachable.
- **New verification machinery now needs a defect to point at.** Proposing a
  new checking apparatus requires a shipped-behavior defect as its trigger —
  closing the door the retired step originally came through.
- **Review loops end by rule, not by override.** Repeated review returns are
  counted per milestone and fire on a repeated failure *shape*, converting
  the obligation into a structural remedy that closes the class rather than
  another round of the same fix.
- **Plans record the road not taken.** Wherever a plan settles which approach
  a criterion will be met by, it logs the alternative that lost, why, and
  what evidence would falsify the choice. Promotion conditions for parked
  ideas are likewise written as falsifiers ("promote when X is observed"),
  never as failure counts.
- **Gate questions lead in plain words.** The first sentence of a question
  says what is being decided, the second what happens on each choice, both
  before any term of art; internal record identifiers stay out of question
  text and option labels.
- **Resuming a session starts from the truth.** Session start now injects
  the newest content of a live milestone's unbounded history sections within
  a stated budget — saying what it left out — and the active milestone file
  and the repo's own instruction file joined the set of governed always-read
  surfaces.
- **A milestone's local decisions are history.** The milestone file's
  decisions section is exempt from the size cap on the same never-edit
  grounds as the work log, with a format advisory watching for pasted
  output in place of summaries.
- **An interrupted repair resumes.** A superseded source-shelf directory
  left on disk after a declined migration stays visible — the validator
  reports it, and re-running repair picks the migration back up.
- **Sturdier guard tests.** Guard doctrine now covers *where* a detector
  looks, not just what it matches; a differential test holds the two
  independent implementations of heading classification to one contract; and
  quantified claims in records must name a verbatim-reproducible procedure.

## 1.2.0 (2026-07-23)

Nineteen milestones since the last feature release, aimed mostly inward — at
what cairn's own records cost to carry, how its rulebook is kept from bloating,
and how sharply its gates and audits read. Backward-compatible: existing repos
keep working unchanged; everything here adds a tool, a rule, or a check rather
than altering the tracking file format.

- **Two measurement tools.** `cairn_cost` reports what a milestone actually
  spent — turns, cache reads, fresh input, output — read from the session
  store, so a weight decision aims at a measured number instead of a guess.
  `cairn_budget` shows an artifact's size against whichever cap applies *while
  it is being written*, so a first draft lands under cap by construction
  instead of by trimming afterward. The `/milestone` audit now also reports the
  rulebook's line and character mass and its growth since the last editorial
  pass. All three are reporting surfaces only — no threshold, no pass/fail
  attached to any number.
- **Specialist doctrine now loads only when it applies.** Two bodies of
  guidance — the craft of writing guard tests, and the discipline of keeping
  records clean at each gate — moved out of the always-read files into their
  own modules, read only when that work is actually happening. A session that
  never writes a guard or touches a record stops paying to carry the guidance
  for it.
- **Lessons now leave, not just accumulate.** The lessons file gained two
  exits: a lesson retires once a guard test actually fails on the mistake it
  warns about (the warning is enforced in code, not just written down), and a
  matured family of related lessons graduates whole into a doctrine module.
  Previously the only way out was pruning by age.
- **Escalated-review findings are binding through to the merge gate.** When a
  hard question is sent for outside review, the returning report's findings now
  travel verbatim into the milestone as numbered criteria, and a new hard check
  refuses to pass a milestone that dropped or softened one. What the review
  concluded is what the merge gate sees.
- **Sharper audits.** The staleness clock that flags a stalled milestone now
  measures genuine work, so a milestone kept alive only by bookkeeping entries
  is correctly read as stale rather than active. A new check confirms every
  always-read file still names how content enters it, how it leaves, and what
  keeps it honest.
- **Review ticks each criterion as its evidence lands** — not in one batch pass
  at the end — mirroring how implementation checks off tasks at each checkpoint.
  The "no evidence, no tick" rule is unchanged.
- **The decision surface leads in plain words.** A question and its options
  gloss a technical term at first use rather than assuming it, and the
  plain-language meaning comes before any technical justification.
- **Exploring sources you haven't cited yet is legitimate.** Reading a corpus
  of prospective sources to discover a method or oracle — before any claim
  depends on them — is now a recognized activity that gets triaged into roadmap
  candidates, rather than dismissed for lack of a citation.
- **Ingesting an outside review carries the planning path's discipline.** The
  brief-ingest and mid-milestone amendment paths now follow the same form, size
  budget, and file-hygiene rules the planning path already had.
- **Faster planning reads.** The step that consults past decisions now scans
  their headings and reads only what it needs — about 90% less text on what had
  been over half the planning-time read.
- **Smaller housekeeping fixes.** The hygiene stamp is replaced rather than
  appended, so it stays one line instead of growing into a chain; the
  record-density advisory was reworked to watch per-line mass.

### Fixed

- Binding criteria written in prose — `- **BC1 (Layer A).** …`, with the
  label bolded and the delimiter inside the bold — are now recognized by the
  validator. Previously only the plain `- BC1:` form parsed, so a review whose
  criteria used the bolded style validated as if it bound nothing and failed
  the check. A criterion whose bold closes before any delimiter (`- **BC1**:`)
  still parses as nothing and fails loud, unchanged.

## 1.1.1 (2026-07-19)

A documentation release. The README now describes what 1.1.0 actually
shipped, and a new test keeps one part of it from drifting again.

- **The README caught up.** A new section explains how a cairn repo records
  the sources its claims rest on. The list of what cairn deliberately does
  *not* do now says plainly that it never proposes a release or nominates one
  as your next action. Each non-failing nudge is named by what triggers it,
  and the release command is described without assuming an R package.
- **The list of shipped toolchain profiles is now guarded.** It is derived
  from the profiles themselves and checked against the README and both plugin
  manifests, so adding a profile without advertising it fails the tests. The
  fourth profile had shipped in 1.1.0 with three surfaces still claiming three.

## 1.1.0 (2026-07-19)

Twenty-one milestones of hardening on top of the first stable release. The
headline is a full documentation-of-sources system — cairn repos can now
record what a claim rests on, and be told when that record has gone
unchecked — alongside real intake paths for outside contributors and a
release path that waits for the maintainer instead of nagging.

- **Reference pages, end to end.** A repo can now record the sources its
  claims rest on. Two page types ship with templates — a source note (one
  primary source) and a synthesis note (a cross-source analysis) — and a
  stated rule for when a page is owed: once the repo *relies* on a source,
  authored in the work that takes the dependency. Every page carries a
  provenance block saying where it came from, when it was ingested, and
  whether its extracted values have actually been re-read against the
  source. Claims about a source and claims about the repo's own state are
  held apart, the latter stamped with the date they were observed, so a
  note written this morning can't quietly read as a standing fact.
- **Staleness reporting for those pages.** A non-failing advisory reads each
  page's provenance and flags one never checked against its source, or last
  checked over 180 days ago. A page whose verification claim is
  self-contradictory, undatable, or dated in the future is reported as such
  rather than resolved by guesswork — an unreadable status stays on the
  backlog instead of passing as verified.
- **Release timing is the maintainer's call.** cairn no longer proposes a
  release, plans release work unprompted, or nominates one as the next
  action. A release whose window the maintainer hasn't opened parks as
  blocked, where no routing surface recommends it, and stays there until
  the maintainer says otherwise. (The release command itself already never
  self-submitted; this extends the same authority to whether a release is
  even queued.)
- **Working with outside contributors.** `/hotfix` now runs in both
  directions: given an incoming pull request it checks that branch out,
  holds the change to the hotfix bar, adds the missing regression test, and
  merges on your approval — the contributor's branch and PR number are left
  alone. `/milestone` sweeps open issues and pull requests into the audit and
  resolves each into an explicit disposition. And the README and rulebook now
  state plainly which guarantees survive a merge made outside a cairn session
  and which degrade to honor-system, rather than implying the guards are
  everywhere.
- **Merge approval is bound to its pull request.** The approval marker names
  the PR it authorizes, and a merge of any other PR — or of none — is
  refused, including the second and later merges in a chained command.
- **A fourth toolchain profile**: `docker-image`, for repos whose deliverable
  is a container image (lint plus build, optional vulnerability scan, a
  registry release walk that pushes nothing on its own). A repo carrying both
  a Dockerfile and a language marker is asked rather than guessed at.
- **Ideas can't hide outside the tracking files.** An idea captured through a
  side channel — a task chip, a scratch note — now also lands as a roadmap
  candidate in the same turn, with a non-blocking nudge at the moment of
  capture. The side channel stays usable; it just stops being the only place
  an idea exists.
- **Correcting a record that turns out to be wrong** now has a stated
  protocol, split by what the file is for: what's true *now* (lessons, design,
  reference pages) is fixed where it sits and marked; what happened (decisions,
  work logs, archives) is superseded and never edited.
- **Size limits got more useful.** An over-cap milestone now reports its
  heaviest sections and exactly how many lines to shed, so trimming is one
  targeted rewrite instead of a nibble-and-recount loop. The work log no
  longer counts against that limit — it's history, and the limit could
  otherwise demand an edit the rules forbid. And a second, non-failing
  measure watches total character mass, catching prose that bloats inside
  lines where a line count can't see it.

### Deprecated

- The gitignored source shelf moved from `cairn/references/pdf/` to
  `cairn/references/sources/` — the shelf holds any source, not only PDFs.
  The old entry still validates and is reported by a non-failing advisory;
  `/cairn-init` repair performs the move for you, on an explicit ask.

### Fixed

- A references page with no provenance block could be reported as having an
  incomplete one — or pass the check outright — when ordinary prose happened
  to wrap so that a line began with the word "provenance". The block heading
  is now recognized as a label rather than as any line starting with that
  word.

## 1.0.0 (2026-07-16)

First stable release. cairn is a milestone-driven development workflow and
tracking system for Claude Code: a language-agnostic core with per-repo
toolchain profiles, human-gated skills for planning, implementing, and
reviewing work, and a self-auditing `cairn/` file system that keeps all
project state in plain markdown. Everything below has been piloted on real
repositories since 0.1.0.

- **Nine skills** (was eight): `/design-interview` joins the set — a
  standalone two-phase interview (facts → principles) that fills or deepens
  a repo's `DESIGN.md`; `/cairn-init` hands off to it, and it can be re-run
  to deepen a thin design doc.
- **Toolchain profiles**: the R-only assumptions of 0.1.0 are gone. Each
  repo declares its toolchain in `cairn/PROFILE.md` with seven slots
  (verify, consistency-gate, test-doctrine, release-walk, init-detection,
  greenfield-openers, changelog); three reference profiles ship — r-package
  (CRAN walk), python (pyproject/pytest/PyPI), and generic. A repo without
  a profile is inferred from its markers, so pre-profile adopters keep
  working unchanged.
- **Validation doctrine** for statistical/numeric work, in its own module:
  five named oracle types (frozen, live, invariant, closed-form,
  simulation-coverage), a two-independent-types bar per numeric result,
  reproducibility and primary-sources hard stops, and an auditable oracle
  registry whose shape is the repo's choice.
- **Guardrail hooks** (seven): session-start tracking injection, an
  uncommitted-tracking stop guard, marker-based merge-approval enforcement
  (approval survives failed merge retries, never a successful merge), a
  default-branch force-push guard, a commit guard, and a memory-boundary
  nudge. Fail-safe by construction; best-effort Windows fallback.
- **Self-audit scripts**: `cairn_validate` (hard checks plus non-failing
  advisories), `cairn_next` (what's workable, mechanically), `cairn_status`,
  and `cairn_impact` (principle-impact tracing).
- **Interaction discipline**: decisions happen at explicit gates with
  selectable chips (including merge approval — no free-text yes/no);
  produced conclusions and durable-record text appear verbatim in chat
  before being accepted or committed; phase transitions are navigable
  chapters.
- **Migration**: `/cairn-init` migrates precursor tracking systems via an
  interactive, PR-based protocol with a read-only dry-run mode and an
  opening environment check; history is entombed verbatim, never rewritten.
- **Docs**: MIT license; README with a worked example, install paths
  (symlink dev install or marketplace), and an explicit no-lock-in bail-out.

## 0.1.0 (2026-07-11)

Initial build from the DRAFT_2.md spec.

- Eight skills: `/milestone` (status + health audit + routing),
  `/milestone-plan`, `/milestone-implement`, `/milestone-review`,
  `/milestone-brief` (Fable RB/RR protocol), `/hotfix`, `/cairn-release`,
  `/cairn-init` (scaffold / repair / migration).
- Shared rulebook (`skills/shared/tracking-rules.md`) read by every skill:
  ownership boundaries, weight caps, status vocabulary, work tiers, git and
  approval model, CI waiting rules, model strategy, oracle doctrine, source
  ingestion, test-scope guidance, R guardrails.
- Templates: milestone, review brief, decision entry, CLAUDE.md section.
- Unpiloted — see DRAFT_2.md §11 for the pilot plan.
