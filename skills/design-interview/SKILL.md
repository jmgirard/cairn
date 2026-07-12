---
name: design-interview
description: Run a two-phase design-elicitation interview to fill or deepen a repo's DESIGN.md — Phase 1 elicits facts that can't be inferred from code and banks proto-principles; Phase 2 formalizes and stress-tests principles (IP/GP). Use when the user wants to articulate a repo's design, purpose, contract boundary, conventions, or guiding/inviolable principles, run a design interview, or enrich a thin DESIGN.md.
argument-hint: ""
---

# /design-interview — elicit design, then principles

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: question gates, contextual chip construction, the DESIGN.md
ownership boundary, and IP/GP numbering).
Phase header: `# Design interview` → `## Facts` / `## Principles`.
Chapter markers: mark a chapter at each phase transition (session start implicit).

This skill does what code-reading cannot: it interviews the human for the
intent behind the repo and writes it into `cairn/DESIGN.md`. It runs in two
phases with an explicit seam. **Facts before principles is a one-way
dependency** — commitments made before the fact base exists get reworked
once it does — so Phase 1 never asks the user to commit a principle; it only
**banks** proto-principles for Phase 2.

**Run this on Fable.** The interview is markedly better on Fable than on
Opus — its questions land in plain language and its Phase-2 judgment is
stronger (openac pilot, 2026-07-11; D-014). If the session is not already on
Fable, recommend switching before starting; then proceed. This is the user's
per-instance model choice (no cairn-spawned Fable subagent, so D-004 is
unaffected), not a standing elevation.

## Session start

Require `cairn/DESIGN.md` to exist; if there is no `cairn/`, stop and route
to `/cairn-init` (scaffold first, interview second). Read the current
DESIGN.md, `cairn/DECISIONS.md`, and — so every option can be grounded in
evidence — the repo itself: DESCRIPTION/manifest, the exported surface,
Imports/dependencies, installer/platform coverage, and recent `git log`.
For a repo spanning many files, fan out `[S]`-tagged Explore subagents with
specific focuses and require file:line citations. Draft your grounded
option sets internally before asking anything.

## Phase 1 — Facts

Elicit what cannot be inferred from the repo; **do not classify anything**.
Run a series of batched AskUserQuestion rounds (2–5 questions each, every
option carrying a marked recommendation). Five disciplines, all mandatory:

1. **Elicit, don't classify.** Ask for intent the code can't show: who the
   package is *for*; where its job *ends* (the contract boundary); which
   platforms are commitments vs. best-effort; what bar a new capability must
   clear to earn a place; distribution ambition; API-stability posture;
   dependency posture.
2. **Chain rounds on prior answers.** Each round consumes the last — e.g.
   "You said the roster grows opportunistically; what should the bar be?"
   Batch only what is mutually independent within a round.
3. **Ground every option in repo evidence.** Cite real files, functions,
   Imports, installer coverage, recent commits in the option text
   (e.g. "`os_fix_csv` is the seed of this family").
4. **Options are hypotheses that do work.** Each option states an
   implication or consequence ("this sets the API-stability bar"), never a
   generic label.
5. **Ask the wart question.** "What warts or fragilities do *you* know about
   that code-reading wouldn't reveal?" — with options that are
   evidence-based guesses (recent fixes, unmaintained upstreams,
   platform-biased testing).

**Bank, don't decide.** When an answer implies a principle, name it and add
it to a running **banked-candidates ledger** ("sounds like a principle —
banking it for the principles round"); never ask for the commitment now.

## The seam

At the phase boundary: summarize what was heard; write the DESIGN draft
(Purpose & Scope, contract boundary, conventions) plus the banked-candidates
ledger to disk; **checkpoint-commit** (stop points are commit points, so a
later session resumes statelessly); then a routing chip —

- **Continue into principles** → Phase 2 (recommended)
- **Pause here** — stop; resume statelessly later

Continuous by default, pausable without loss. Both phases run in one
session — best on Fable (see the note at the top).

## Phase 2 — Principles

Formalize and pressure-test. Sources for candidates: the banked ledger,
plus two the interview must add itself —

- **Mine git history for implicit principles.** Generalize ad-hoc fixes
  into candidates (a "skip files without audio" fix → "resilient batches").
- **Derive candidates from the domain, not just the code.** State forward
  consequences (irreplaceable recordings → inputs-sacrosanct; IRB/consent
  → local-only processing, which constrains future remote-inference
  wrappers).

Then propose and test:

- **Every candidate arrives classified.** Proposed strength — **IP**
  (inviolable) / **GP** (guiding) / **skip** — with a *marked
  recommendation*, and adjacent-but-separate matters fenced off explicitly
  ("output-overwrite defaults are a separate, tradeable matter") so each
  question stays decidable.
- **Stress-test the adopted set against phase-1 decisions.** Surface
  collisions between separately-endorsed commitments ("thin wrappers" vs.
  a "tidy outputs" choice → where's the line?).
- **Separate essence from accident.** Ask whether a principle is the
  capability or the current idiom, citing recorded decisions as leverage.
- **Probe the scope of each IP.** Offer extend / keep / downgrade for every
  inviolable.

**Write-out.** Record the settled principles in `cairn/DESIGN.md` under
Design Principles: the **IP block first, then GPs**; numbers run within each
type and are **never reused or renumbered** (retiring one takes a D-entry).
A genuine cross-cutting choice with rationale (not a deferral) becomes a
`cairn/DECISIONS.md` D-entry. Deferred candidates become ROADMAP
`candidate` rows — nothing the user surfaced is silently dropped.

## Routing

Close with a routing chip (AskUserQuestion) composed from what was produced — e.g.
**Plan the first milestone** → `/milestone-plan` (recommended) /
Run `/milestone` / Stop. A chip is a user stop; never auto-proceed.
