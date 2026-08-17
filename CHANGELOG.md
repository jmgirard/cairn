# Changelog

## Unreleased

- **The core loop is a diagram now.** The README's "The core loop" section
  draws the four phases as a flowchart GitHub renders in place, with each
  gate labelled on the step it opens and an arrow back from review to
  implement for work a review sends back. The section showed a one-line
  arrow chain before, which had no way to show that return.

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
