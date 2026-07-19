<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M91: Reference re-verification — the three partial extractions get read against their sources

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP4, GP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m91-reference-reverification`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Re-read every claim in the three partially-verified references pages against
its current source, correcting what has changed, so each page's extraction
status states what was actually checked.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `spec-kit.md`, `bmad-method.md`, `backlog-meridian.md` — the three
pages `cairn_validate`'s `references staleness` advisory flags as recording
only a partial verification. Four external repos across them (spec-kit,
BMAD-METHOD, Backlog.md, Meridian). Each page's factual claims are re-read
against a fresh clone at a pinned version; a claim that no longer holds is
corrected in place and marked, per D-045; the extraction status is rewritten
to name the version and date checked. Follows the M83 `task-master.md`
precedent verbatim. Also in: `competitive-landscape.md`, the synthesis note
derived from these pages, whose own status claims its eight inputs have had
"none re-read since 2026-07-11" — false since M83 re-read `task-master.md`
on 2026-07-18 and corrected three of its claims.

**Out:** re-evaluating the "What cairn should steal" sections as design
questions — a steal is touched only where a corrected fact undercuts it, and
anything genuinely new that surfaces becomes a `candidate` ROADMAP row, not
scope here. Out: the other twelve `references/` pages, which the advisory
does not flag. Out: any change to the advisory, its parser, or its
thresholds — this milestone is a consumer of M89's classifier, not a revision
of it; a parser defect found here is reported and routed, not fixed inline.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] Every factual claim in each of the three pages has been read against a
      fresh clone of its source; each page's extraction status names the
      pinned version (tag, release, or commit SHA) and the date checked.
- [ ] Every claim found false is corrected in place and marked in the M83
      style (`(M06, corrected M91)`), with git holding the original; no claim
      is deleted to avoid correcting it.
- [ ] `spec-kit.md`'s three citations are re-anchored from bare filenames to
      full repository paths, and each line anchor is re-checked against the
      current source; where an anchor no longer resolves, the claim resting
      on it is corrected.
- [ ] `competitive-landscape.md`'s false "none re-read since 2026-07-11"
      claim is corrected, and every conclusion resting on a fact corrected by
      T1–T3 is revisited — each either updated or explicitly recorded as
      unaffected.
- [ ] `cairn_validate` is run and its `references staleness` output recorded
      before and after; each rewritten status classifies as authored, proven
      by that command output naming the per-page state rather than by reading
      the status wording. Honest status is the bar: a page still WARNing
      ships with a stated reason its true status warrants the warning.
- [ ] The `verify` slot is clean — all three suites green
      (`skills/tests`, `scripts/tests`, `hooks/tests`), each exit code
      checked separately.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number. -->

- AC1 → T1, T2, T3
- AC2 → T1, T2, T3
- AC3 → T1
- AC4 → T4
- AC5 → T5
- AC6 → T5

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — `spec-kit.md`: clone github/spec-kit, pin the version, re-read all
      claims (the `specify`/`constitution`/`plan-template` citations, the
      ~10-command list, the `[NEEDS CLARIFICATION]` cap of 3, the
      Constitution Check gate, `/analyze` and `/converge` behavior). Correct
      and mark; rewrite the status. HEAD was 2026-07-18 at 0.13.1.dev0 with
      0.13.0 released 2026-07-17, so drift is expected, not hypothetical.
- [x] T2 — `bmad-method.md`: clone bmad-code-org/BMAD-METHOD, pin the
      version, re-read all claims (the four phases, `sprint-status.yaml` as
      state-machine ledger, section-level write permissions, the adversarial
      review agent, `bmad-help` routing). Correct and mark; rewrite the
      status. Note the page cites a V6 clone — confirm the current major.
- [x] T3 — `backlog-meridian.md`: two repos, MrLesk/Backlog.md and
      markmdev/meridian. Re-read both halves (Backlog.md's per-task files,
      `<!-- AC:BEGIN/END -->` fencing, three staged guides; Meridian's
      SessionStart/PreCompact re-injection, the blocking Stop hook at
      `scripts/stop-checklist.py:69`, the reviewer-score plan gate). Correct
      and mark; rewrite the status naming both pinned versions.
- [x] T4 — `competitive-landscape.md`: correct the false re-read claim, then
      walk each numbered differentiator against the corrections from T1–T3
      and record the disposition of each.
- [x] T5 — run `cairn_validate` and the three suites from the repo root,
      checking each exit code separately (never piped — M56/M78 lesson).
      Record the advisory's before/after output. If a rewritten status
      classifies differently than authored, fix the wording, not the
      classifier — a parser defect is reported and routed per Scope.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-07-19: created by /milestone-plan. Follows through on M89, whose archive records the three WARNs as true positives needing "a re-read of three external clones". Four gate answers: re-read against current source (M83 precedent), synthesis note in scope, steal lists frozen except where a corrected fact breaks one, honest status over zero-warnings.
- 2026-07-19: T1 done — spec-kit re-read at 0.13.1.dev0 (commit 57cc518). Every claim held; zero corrections. All three line anchors still exact (specify.md:128, constitution.md:87, plan-template.md:39,106); citations re-anchored to full paths and the command inventory completed (10 templates, `/speckit.*` namespace, `checklist`/`taskstoissues` added).
- 2026-07-19: `TestShippedPageStateLedger.EXPECTED` updated spec-kit.md `partial` → `ok` per the ledger's own deliberate-update protocol — the page was re-read in full against its source, so the classification change is the intended result, not parser drift. Suites green (skills/scripts/hooks all exit 0, checked separately).
- 2026-07-19: T2 done — bmad-method re-read at v6.10.0 (commit c23f234); still the V6 line, cited sprint-planning SKILL.md:8 still exact. Two claims wrong, corrected in place and marked: (a) "Quick Flow" was removed (removals.txt; CHANGELOG #2177/#2179/#2186 consolidated the personas into the Developer agent), its role now filled by `bmad-quick-dev`; (b) `bmad-help` is NOT auto-run at every workflow end — 1 of 26 non-agent skills invokes it at close, and it is otherwise user-invoked. Correction (b) undercut the "BMAD validates the pattern" steal, which is rewritten per the gate's break-a-steal rule. Ledger bmad-method.md `partial` → `ok`; suites green (each exit checked).
- 2026-07-19: T3 done — Backlog.md re-read at v1.48.0 (commit babd1d2), Meridian at commit d9b8775 (dormant since 2026-03-10). Meridian: all claims held, `scripts/stop-checklist.py:69` still the exact line returning `"decision": "block"`, plan-reviewer 9+ gate exact. Backlog.md: three lifecycle claims wrong and corrected — the three staged guides are now one `agent-guidelines.md` with Creation/Implementation/Wrap-up phases; the agent is instructed to check its own ACs and set Done (not forbidden); and follow-up tasks are an offered route, not gated on user approval. The evidence-before-checkbox steal rested on the corrected finalization rule and is rewritten as cairn's own extension.
- 2026-07-19: `TestUnlistedShippedFormsSatisfyTheShapeRule.FORMS` dropped its `partly verified at ingestion` entry — M91 retired that form from the corpus, and the class's own rule is that a form no page writes must fail rather than sit there as a phrase templates are measured against. `partial` keeps its dedicated parser coverage in scripts/tests. Advisory now OK (0); suites green (each exit checked).
- 2026-07-19: T4 done — competitive-landscape's false "none re-read since 2026-07-11" corrected (M83's task-master re-read had falsified it the same day it was dated). All five differentiators walked against the corrections and their dispositions recorded on the page: #2 corrected in wording, #3 corrected and strengthened (Backlog.md requires no evidence citation), #1/#4/#5 unaffected.
- 2026-07-19: T5 done — advisory `references staleness` WARN (3) → OK (0); per-page states proven by running TestShippedPageStateLedger against the live pages, not by reading status wording. All three suites exit 0, checked separately; cairn_validate exits 0 with every CHECK PASS.
- 2026-07-19: AC3 amended via the step-6 gate — its premise ("both moved under templates/commands/ since ingestion", "constitution.md now resolves to two candidate paths") was false: `git log --follow` puts templates/commands/specify.md at that path since the initial checkin 2025-08-22, and the second constitution.md hit is a different file (.specify/memory/). The M06 page cited bare filenames. Criterion reworded to the checkable requirement; required work unchanged.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. -->
