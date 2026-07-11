# What good DESIGN-elicitation questions look like

**Scope:** repo-specific findings note (not a source summary). Raw material
for a future design-interview skill or an elicitation upgrade to
`/cairn-init`. Provenance: openac pilot session, 2026-07-11 — same session,
same AskUserQuestion format, same repo context; model switched from Opus 4.8
to Fable 5 partway through. Question quality judged markedly better by Jeff
after the switch; transcript comparison confirmed a difference in *kind*.

## The failure mode (observed on Opus)

Classification questions: the model drafts candidate principles itself,
then asks the user to file each one into fixed buckets ("Inviolable /
Guiding / Drop") — three questions in a row with identical option sets.
The model never asks anything it doesn't already have a candidate answer
for. Useful, but it only confirms drafts; it doesn't discover.

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

## Levers to experiment with

- **Cheap:** encode 1–5 as instructions in a skill (design-interview skill,
  or the DESIGN-filling step of `/cairn-init`) and test whether Opus's
  interview quality rises. Pricing favors this if it works.
- **Expensive:** elevate DESIGN elicitation to Fable behind a per-instance
  approval gate, mirroring the `/milestone-brief` pattern.
- Confound to control in any test: the better interview also had more
  warm-up context (later in session). Compare cold-start runs.
