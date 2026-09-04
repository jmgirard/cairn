# Changelog

## Unreleased

- **Skills work under the symlink install.** Each skill now says how to
  find the plugin directory when the shell leaves `CLAUDE_PLUGIN_ROOT`
  unset (the symlink install in `~/.claude/skills` does): it falls back to
  the skill's own base directory, so the rulebook reads and the
  `scripts/` commands no longer resolve against `/scripts/…`.
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
- **A hotfix merged outside the session is still held to the hotfix bar.**
  Running `/hotfix` on an already-merged hotfix or adopted PR now verifies
  the merged diff after the fact: its regression test is proved to fail on
  the commit the PR was based on and pass on the default branch, the
  profile's checks run, and the changelog entry is checked. A missing test
  or entry lands through a follow-up PR with the usual approval chip; a
  clean result pauses at one acceptance chip before close-out, instead of
  jumping straight to it.
- **A whole-list triage pass, on demand.** `/cairn-triage` reads every
  ROADMAP candidate row and every DESIGN.md known issue, proposes one
  disposition per item (keep, compress, merge, split, drop, promote, or
  route) at a single gate, applies what you accept in one docs-only
  commit, and records drops made on principle as a decision so they are
  found by search rather than re-added. Nothing triggers it and nothing
  is written before you answer.
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
