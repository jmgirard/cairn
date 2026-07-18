# What good DESIGN-elicitation questions look like

**Provenance.** Citekey `design-interview-notes` · ingested 2026-07-11 by M02 from repo-specific findings note — the openac pilot session (same session, same AskUserQuestion format; model switched Opus 4.8 → Fable 5 partway through).
Pagination: —.
Extraction: first-hand session record, not an extraction from an external source; nothing to re-verify against.

**Scope:** repo-specific findings note (not a source summary). Raw material
for a future design-interview skill or an elicitation upgrade to
`/cairn-init`. Provenance: openac pilot session, 2026-07-11 — same session,
same AskUserQuestion format, same repo context; model switched from Opus 4.8
to Fable 5 partway through. Question quality judged markedly better by Jeff
after the switch; transcript comparison confirmed a difference in *kind*.

## The failure mode (observed on Opus)

Ungrounded classification: the model drafts candidate principles itself,
then asks the user to file each one into fixed buckets ("Inviolable /
Guiding / Drop") — three questions in a row with identical option sets, no
recommendations, no evidence in the options, and *before* the design facts
were elicited. (Correction from a later pass: classification per se is
fine — the good pass-2 interview also used IP/GP/skip buckets. The failure
is classifying before eliciting, with no grounding or recommendation.)

## What the better interview did (observed on Fable)

1. **Elicit, don't classify.** Ask for what cannot be inferred from the
   repo: who the package is *for*; where its job *ends* (contract
   boundary); which platforms are commitments vs. best-effort; what bar a
   new tool must clear to earn a wrapper family; distribution ambition;
   API-stability posture; dependency posture.
2. **Chain rounds on prior answers.** Each round consumes the last:
   "You said the roster grows opportunistically — what should the bar be?"
   / "You chose run-plus-tidy-outputs; readers don't exist yet — add
   candidates now?"
3. **Ground every option in repo evidence.** Cite real files, functions,
   Imports, installer coverage, and recent-commit history in the option
   text (e.g. "`os_fix_csv` is the seed of this").
4. **Options are hypotheses that do work.** Each option carries an
   implication or consequence ("this sets the API-stability bar"), not a
   generic label.
5. **Ask the wart question.** "What warts/fragilities do YOU know about
   that code-reading wouldn't reveal?" — with options that are evidence-based
   guesses (recent fixes, unmaintained upstreams, platform-biased testing).

## Pass 2: the principle interview (observed on Fable, 2026-07-11)

A second interview run after the overall design interview settled. Jeff
judged it equally strong. It did categorically different work than pass 1 —
possible only *because* pass 1's answers existed:

6. **Stress-test adopted principles against later decisions.** Find
   collisions between commitments the user endorsed separately (GP1 "thin
   wrappers" vs. the pass-1 "tidy outputs" choice → "where's the line?").
7. **Separate essence from accident.** Ask whether a principle is the
   capability or the current idiom (GP2: batch *parity* vs. the `_dir`
   API shape), citing recorded decisions (D-002 free-breakage) as leverage.
8. **Probe the scope of each IP.** Offer extend / keep / downgrade for
   every inviolable (IP1: extend to write locations?).
9. **Mine git history for implicit principles.** Generalize ad-hoc fixes
   into candidates (the "skip files without audio" fix → "resilient
   batches").
10. **Derive candidates from the domain, not just the code.** Irreplaceable
    participant recordings → inputs-sacrosanct; IRB/consent → local-only
    processing (with forward consequences stated: constrains future
    HF wrappers to local inference); methods reporting → transparent calls.
11. **Every candidate arrives classified.** Proposed strength (IP/GP/skip)
    with a marked recommendation, and adjacent-but-separate matters fenced
    off explicitly ("output-overwrite defaults are a separate, tradeable
    matter") so each question stays decidable.

## Proposed structure: one interview, two phases (refined 2026-07-11)

Originally framed as two passes (Jeff); refined after discussion to a
single continuous interview with two phases and an explicit seam:

- **Phase 1 — overall design interview:** elicit what can't be inferred
  (items 1–5). Never asks for principle commitments; instead **banks**
  proto-principles in a running ledger as they surface in answers
  ("sounds like a principle — banking it for the principles round").
- **Phase 2 — principle interview:** formalize and test (items 6–11):
  propose the banked material plus domain-derived and git-mined
  candidates, each with a strength recommendation; stress-test the full
  set for collisions with phase-1 decisions.
- **The seam:** at the phase boundary, summarize what was heard, write
  the DESIGN draft + banked-candidates ledger to disk, checkpoint-commit
  ("stop points are commit points"), and offer a routing chip: continue
  into principles now (recommended) / pause here. Continuous by default,
  pausable without loss; a later session resumes statelessly.

Why principles wait for phase 2 (empirical): all three principles adopted
in openac's early classification round (GP1/GP2/IP1) had to be reopened in
the pass-2 stress-test — boundary redrawn, essence-vs-idiom split, scope
extended. Commitments made before the fact base existed all got reworked
after it existed; facts → principles is a one-way dependency.

Why the seam stays explicit: (a) checkpoint + stateless resume; (b) exit
ramp for interview fatigue (~25 decisions in openac's run); (c) it makes
model elevation targetable — phase 2 is the judgment-heavy half, so a
future variant could run phase 1 on Opus and elevate only phase 2 to Fable
behind the standard approval gate.

## Levers to experiment with

- **Cheap:** encode 1–5 as instructions in a skill (design-interview skill,
  or the DESIGN-filling step of `/cairn-init`) and test whether Opus's
  interview quality rises. Pricing favors this if it works.
- **Expensive:** elevate DESIGN elicitation to Fable behind a per-instance
  approval gate, mirroring the `/milestone-brief` pattern.
- Confound to control in any test: the better interview also had more
  warm-up context (later in session). Compare cold-start runs.
