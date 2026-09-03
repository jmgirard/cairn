---
name: cairn-triage
description: Triage every ROADMAP candidate row and every DESIGN.md Known issues entry in one pass - propose one disposition per item at a single gate, apply the accepted ones in one docs-only commit, and record principled drops as a decision. Use when the user wants to triage the candidates, prune the backlog, clean up the roadmap, or sweep the known issues.
argument-hint: ""
---

# /cairn-triage — whole-list triage of candidates and Known issues

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it (especially: search-first candidate creation, the bounded `DECISIONS.md`
read, the git model, the record-prose rule). Then read
`${CLAUDE_PLUGIN_ROOT}/skills/shared/records-hygiene.md` — this is a hygiene
gate. This skill is on demand: nothing triggers it, no threshold sizes it,
and it never runs unasked. It proposes, the user decides at one gate, and
it writes nothing before that answer.
Phase header: `# Triage` → `## Pass`.
Chapter markers: mark a chapter at each phase transition and at each numbered
step (session start implicit).

## Session start

Read, in order: `cairn/ROADMAP.md` (whole — the `## Candidates` section is
the subject), `cairn/DESIGN.md`'s `## Known issues` section (absent → note
that and continue), the `### D-` headings of `cairn/DECISIONS.md` per the
bounded read (open an entry whole only when an item cites it or its subject
matches one), and the file listing of `cairn/milestones/archive/`. Note
every milestone that is `planned`, `in-progress`, `blocked`, or `review`:
a row one of them absorbs is never dropped or merged away in this pass
(records-hygiene §1 — it graduates at that milestone's post-merge hygiene).

Preconditions: clean `git status`, on the default branch (detect it per the
tracking-rules git model — never assume `main`), synced with origin
(`git fetch`, ff-only pull). A dirty tree or a non-default branch stops the
pass with a close block naming what to fix; the pass never commits on a
milestone branch and never sweeps unrelated changes into its commit.

## Workflow

1. **Enumerate.** List every item in both sections, in file order, one line
   each: its source (`candidate` / `known issue`), its subject (the text up
   to the first colon, trimmed), its byte length, and its added date.
   - A candidate item is one `- ` line under `## Candidates` in
     `cairn/ROADMAP.md` (ROADMAP is one item per line, never split); its
     date is the `added YYYY-MM-DD` token, or `undated` when absent.
   - A Known issues item is one `- ` entry under `## Known issues` in
     `cairn/DESIGN.md` — the `- ` line and every indented continuation line
     up to the next `- ` line or the next heading; its date is `undated`
     (entries name their accepting milestone, `M<NNN>`, not a date — list
     that instead).
   - Read the counts from the files, never from memory or a prior stamp. An
     empty `## Candidates` section, or a missing `## Known issues` section,
     yields zero items from that source with no failure; both empty → the
     pass reaches the gate with an empty table and the close block says so.
   The enumeration is the pass's domain: every proposal in step 3 maps to
   exactly one enumerated item, and every enumerated item gets exactly one
   proposal.
