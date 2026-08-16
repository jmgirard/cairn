# RB<NN>: <Topic> (M<NN>)

- **Date:** YYYY-MM-DD
- **Output required:** write findings to `cairn/reviews/RR<NN>-<slug>.md`

You are performing an independent expert review. This brief is fully
self-contained — do not assume any conversation context. Read only what this
brief directs you to read, answer the numbered questions, and write your
findings to the output path above using the same numbering.

## Background

Self-contained context: what the package does, what this milestone is doing,
and why this question needs independent review.

## Materials

Exact files (and lines where relevant) to examine. How to run relevant code
or tests. Cite `cairn/references/<citekey>.md` summaries where sources
matter.

## Questions

1. Numbered, specific, answerable. Never "any thoughts?"
2. …

## Constraints

What is fixed and must not be relitigated (link D-entries by ID). Flag
disagreement with a constraint explicitly rather than silently working
around it.

## Output format

In `RR<NN>-<slug>.md`: answer each question by number with your reasoning
and evidence; list any additional findings separately under "Beyond the
brief"; end with concrete recommendations, each marked apply / consider /
reject-with-reason. Your report is advisory: emit a `## Binding criteria`
section ONLY if this brief explicitly requests one. Where requested:
numbered `BC1…`, each a measurable assertion checkable against evidence,
with any numeric projection stating its tolerance. These are ingested
VERBATIM into the constrained milestone's acceptance criteria and
mechanically diffed against this file; departures are legal only through
that milestone's shown "Deviations from RR<NN>" table.
<!-- Brief author: state here, explicitly, whether a Binding-criteria
     section is requested (maintainer's choice, recorded at authoring) and,
     when the subject mechanism is on its second or later escalation, list
     removal of the mechanism among the options put to the reviewer. -->
