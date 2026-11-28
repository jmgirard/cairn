# RB08: Is the milestone-local `## Decisions` section history or current knowledge? (M118)

- **Date:** 2026-07-27
- **Output required:** write findings to `cairn/reviews/RR08-decisions-section-record-class.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

cairn is a project-tracking plugin that dogfoods its own format under `cairn/`.
Each milestone gets one markdown file with fixed sections (Goal, Scope,
Acceptance criteria, Coverage, Tasks, Work log, Decisions, Review). A
`cairn_validate` check caps the "plan-owned body" of a live milestone file at
150 lines, failing on `n >= 150`.

Two sections are already exempt from that cap, for two different reasons:

- `## Review` (D-030) — it is review-owned and accumulates evidence at review
  time, so counting it let review evidence scramble plan-owned content.
- `## Work log` (D-046) — D-045 classifies it as **history**, which is never
  edited (IP4). Counting it meant the cap's sanctioned remedy ("compress the
  heaviest section") could land on a section IP4 forbids touching, i.e. the
  gate could demand a violation.

The milestone-local `## Decisions` section is **append-only** in the
section-ownership table but is **not** exempt. D-030 declined to exempt it, and
D-046 reaffirmed that as its choice (3), both on the premise that it "is meant
to stay brief, with cross-cutting entries promoted" to the repo-level
`cairn/DECISIONS.md`. D-066 later hit the collision live (milestone M114 at
149/150 with a 43-line Decisions section), deliberately declined to reopen it,
and recorded that "the entry to supersede is whichever of D-030/D-046 the fix
lands against."

Milestone M118 (planned 2026-07-27, not yet implemented) does exactly that. It
was planned on measurements taken over all 116 milestone files in this repo's
git history:

- The `## Decisions` section runs a **median of 4 lines**; the brevity premise
  holds for 79 of 116 files.
- But **every one of the 7 files that ever reached >=145 plan-owned lines**
  carries a Decisions section of **24-43 lines**.
- Only **1 of those 7** (M114) was driven by an external review report. The
  other six were ordinary milestones.
- Exempting the section drops all 7 into the 106-125 range (measuring each
  file's final state before archiving).

M118's plan makes two moves, and **the second is what this brief exists to
test**:

1. Exempt `## Decisions` from the cap.
2. Classify it as **history under D-045** — never edited, IP4 applies — which
   is what makes move 1 rest on D-046's accepted un-editability argument rather
   than on mere convenience.

The reasoning recorded for move 2 was: the ownership table already makes the
section append-only; its entries are dated dispositions recording what was
decided at a time; and the alternative classification is self-defeating,
because current knowledge is corrected in place, hence trimmable, and a
trimmable section has no claim to an exemption grounded in un-editability.

This question was flagged at the plan gate as hitting the `ip-touching`
escalation tripwire, because classifying a new section as history extends IP4's
reach. The maintainer initially returned the call to the session, then elected
to escalate it before any code is written. **The decision is currently recorded
as D-074 and the whole M118 plan is built on it.** Nothing has been
implemented; reversing it now costs one D-entry and one milestone re-plan.

## Materials

Read these, in this order:

- `cairn/DESIGN.md` — the IP block (IP4 is at line 96); the surrounding
  principles for context on what IP status means here.
- `skills/shared/tracking-rules.md` — in particular: the "File map and
  ownership boundaries" table and the "Milestone-file section ownership" table
  (write-modes, including `append-only`); the "Weight caps" section; the
  "Always-read governance" section; and under "Universal tracking rules" the
  bullet **"Correcting a record proven false"**, which states the
  history-vs-current-knowledge split and enumerates the members of each class.
- `cairn/DECISIONS.md`, these entries read whole:
  - D-030 (line 597) — the original cap scoping and the first refusal.
  - D-045 — the history / current-knowledge split itself. **This is the entry
    whose class boundary M118 extends; read its reasoning closely.**
  - D-046 (line 1100) — the work-log exemption, its choice (3) refusal, and its
    stated distinguishing ground ("that release valve is real and absent from
    the work log").
  - D-063 (line 1877) — the newest-first read-bound applied to cap-exempt
    sections at session start; it is scoped to the cap-exempt set, so the set's
    membership determines its reach.
  - D-066 (line 2028) — the live collision, its choice (4), and its
    "entry to supersede" pointer.
  - D-074 (last entry in the file) — the decision under review.
- `cairn/milestones/M118-decisions-section-cap-exempt.md` — the plan built on it.
- `skills/shared/templates/milestone.md` — the `## Decisions` section comment
  (owner, write-mode, the "promote cross-cutting ones" instruction) and the
  drafting-budget preamble that reserves >=21 lines for the section.
- For worked examples of what the section actually contains at size, read the
  `## Decisions` section of the largest instances from git history (ref-based
  git only — see Constraints):
  - `git show a25e6dd^:cairn/milestones/M114-review-loop-escape-hatches.md`
    (43 lines, the largest)
  - the same section in M83, M84, M94, M98 (33-35 lines each), found via
    `git log --all --diff-filter=A --name-only -- 'cairn/milestones/M*.md'`

## Questions

1. **Is the classification correct?** Is a milestone-local `## Decisions`
   section **history** in D-045's sense, or **current knowledge**? Answer from
   D-045's own stated criteria and from what the section's entries actually
   contain at size, not from the convenience of the outcome.

2. **Is the supporting argument sound, or is it circular?** M118 argues that
   classifying the section as current knowledge is "self-defeating," because
   correctable implies trimmable implies no claim to an un-editability
   exemption. That argument reaches its conclusion partly from the desirability
   of the exemption. Does it survive being run in the other direction — i.e. if
   one first asks what the section *is*, independent of the cap, does the same
   answer follow?

3. **Is there a third option the plan missed?** Specifically: could the section
   be exempted from the cap **without** classifying it as history — on
   `## Review`'s D-030 grounds (differently-owned: the section is
   implement/review-owned while the cap governs plan discipline), or on some
   other ground? If so, compare that route against M118's on robustness and on
   what each commits the repo to later.

4. **What does the classification cost if it is wrong?** If `## Decisions` is
   really current knowledge, IP4 would forbid correcting a milestone-local
   decision found false, leaving only supersede-by-later-entry. Is that an
   acceptable cost, an acceptable outcome, or a genuine loss? Note that
   `cairn/DECISIONS.md` itself operates exactly that way, and that the rulebook
   elsewhere warns that a false record left readable gets harvested into later
   plans (D-045's own rationale for correcting current knowledge in place).

5. **Does extending IP4's reach here create any second-order problem?** In
   particular consider: D-063's read-bound is scoped to the cap-exempt set and
   would silently gain a third member; `cairn_validate` has no check that
   enforces IP4 on any section; and the section is written by two different
   skills (implement and review) rather than one.

## Constraints

Fixed; flag disagreement explicitly rather than working around it.

- **IP4 itself is not up for revision** — "History is never fabricated,
  rewritten, or renumbered — append-only" (`cairn/DESIGN.md:96`). What is in
  scope is whether this section falls under it.
- **The 150-line cap value is not up for revision** (D-030); M118 does not
  propose changing it and neither should you.
- **Do not relitigate whether the squeeze is real.** The measurements above are
  taken and reproducible; if you believe they are wrong, say so with your own
  measurement rather than by assertion.
- **The two rejected alternatives stay rejected unless you show cause**:
  exempting a review-report-bound acceptance-criteria block (measured to
  relieve 1 of 7 files), and a separate Decisions sub-cap (rejected by both
  D-030 and D-046 as second-number complexity).
- **Ref-based git only.** You share the primary working checkout with an active
  session. Use `git show`/`log`/`diff`/`blame` against refs. Never run
  `git checkout`, `git switch`, `git reset`, or `git worktree add`.
- **Write no code and edit no tracking file.** Your entire output is the RR
  file at the path above.

## Output format

In `RR08-decisions-section-record-class.md`: answer each question by number
with your reasoning and evidence; list any additional findings separately under
"Beyond the brief"; end with concrete recommendations, each marked apply /
consider / reject-with-reason.

Where findings bind implementation, also emit a `## Binding criteria` section:
numbered `BC1…`, each a measurable assertion checkable against evidence, with
any numeric projection stating its tolerance. These are ingested VERBATIM into
M118's acceptance criteria and mechanically diffed against this file;
departures are legal only through M118's shown "Deviations from RR08" table.

**A note on binding criteria, from this repo's own experience:** a prior brief
emitted a criteria set that was individually satisfiable but **jointly**
unsatisfiable — one criterion froze a file list that another criterion's
mandated work had to write to — and the collision surfaced at a review gate
rather than at ingestion (D-066). If you emit binding criteria, check the set
against itself for that shape before you write it, and keep the set small
enough to fit alongside M118's existing seven acceptance criteria: the file
currently sits at 115 of 149 permitted plan-owned lines.
