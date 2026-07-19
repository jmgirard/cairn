# Changelog

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
