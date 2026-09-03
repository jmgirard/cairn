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

2. **Assess.** For each item, gather the evidence below and choose exactly
   one disposition. The vocabulary is fixed — seven words, no sub-statuses
   (D-035 stands) and no scores:

   | Disposition | Meaning |
   |---|---|
   | `keep` | Unchanged. The default when no evidence class below fires. |
   | `compress` | Rewritten toward the soft aim of **~300 bytes** in the shape *what it is / promote when / provenance* — the trigger and the `added YYYY-MM-DD — <origin>` provenance always survive; only restated context goes. Advisory only, stated here and nowhere else. |
   | `merge` | Absorbed into a **named surviving row**, which gains one lineage clause (`absorbs <subject>, added <date> — <origin>`) and the absorbed row's trigger where it still applies. |
   | `split` | Replaced by **named rows**, each with one subject, one trigger, and the original provenance. |
   | `drop` | Removed. Its reason is one of three classes: *refuted premise* (a named archived milestone or record shows the premise false), *already shipped* (a named milestone or commit delivered it), or *rejected on principle* (the idea cuts against a stated stance). |
   | `promote` | Ready to plan — handed to `/milestone-plan` in the close block; **never planned in this pass**, and the row stays until that milestone's post-merge hygiene prunes it (records-hygiene §1). |
   | `route` | Misfiled — a candidate row that is really an accepted limitation moves to Known issues; a Known issues entry that is really deferred work moves to a candidate row with a stated trigger. |

   Evidence classes, checked in this order (the first that fires decides,
   later ones refine the wording):
   - **Staleness → `drop` or `compress`.** Grep `cairn/milestones/archive/`
     and the `### D-` headings for the item's subject: a premise an archived
     milestone refuted, a trigger that has already fired (the named
     condition is now in the repo) or can no longer fire (its subject is
     retired), or a cited path that no longer exists (`ls` it). A dead
     citation with a live trigger is `compress`, not `drop`.
   - **Overlap → `merge`.** Two items on one subject, or one whose trigger
     is a special case of another's. The survivor is the one with the
     stronger provenance; state whether the absorbed row's promotion
     trigger survives verbatim in the survivor (step 5 hangs on it).
   - **Overgrowth → `split` or `compress`.** Two promotion triggers or an
     "and" in the subject → `split`; over the ~300-byte aim with one
     trigger → `compress`.
   - **Misfiling → `route`.** A candidate with no promotion condition that
     describes a limitation the repo lives with; a Known issues entry with a
     fix condition that names future work.
   - **Readiness → `promote`.** The trigger has fired and the work is
     wanted now; the close block hands it on.
   A finding-absorbing row — one carrying deferred findings from two or
   more milestones — takes records-hygiene §7's options expressed in this
   vocabulary: `promote` (a bounded milestone for what guards shipped
   behaviour), `route` (accepted limitations to Known issues), `drop` (the
   rest), or `keep` as the explicit choice to extend no further; the
   proposal table names §7 as the reason.
   A row a `planned`/`in-progress`/`blocked`/`review` milestone absorbs is
   `keep` (records-hygiene §1), with that milestone named in the reason.
   Delegation: the session assesses inline. One `[S]` Explore fan-out is
   warranted only when several items cite code paths or symbols whose
   existence must be checked; give it the list of citations and take back
   one line per citation (exists / moved / gone). Never spawn to assess
   prose — that is the session's judgment, not a search.
