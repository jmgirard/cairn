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

3. **Propose and gate.** Present every proposal, then pose one chip. The
   order is fixed: **no file under `cairn/` is written before the chip's
   answer arrives** — steps 4–6 exist only for dispositions that answer
   accepts; the enumerate and assess steps read only.
   - **The table**, in the chat above the chip, one row per enumerated
     item: item (source + subject) → disposition → one-line reason. Every
     `drop` and `merge` reason names its evidence class (refuted premise /
     already shipped / rejected on principle for a drop; trigger survives /
     trigger lost for a merge) and the record or path the evidence sits in.
     A `merge` names its survivor; a `split` names its rows; a `route` names
     its destination; a `promote` names the milestone title it hands on.
     Items proposed `keep` sit last so the changes read first.
   - **The chip** (AskUserQuestion, one question) carries the substance the
     decision needs in its own text (tracking-rules Mandated-substance and
     Acceptance-chips rules): the question text says how many items were
     enumerated and names each item proposed for a disposition other than
     `keep` with its disposition in plain words; the table above is the
     verbatim evidence. Three options, in this order:
     1. **Accept as proposed** (recommended, first) — every disposition in
        the table is applied.
     2. **Amend** — the user names the items to change and what they become
        (the option description says so); everything unnamed keeps its
        proposed disposition; a named item with no replacement given
        becomes `keep`.
     3. **Apply nothing** — the stop option: no file changes, no commit, no
        D-entry; the pass ends at the close block with the table as its
        record in chat only.
     The chip is posed in the same turn as the table. Chip text is plain
     language: no decision-record ids, no principle numbers (the table
     above carries those).
   - **The amend loop.** On *Amend*, re-present the table once with the
     named items changed (only those rows change; a changed `drop` or
     `merge` re-states its evidence class or becomes `keep`), then pose the
     same three-option chip again. A second *Amend* is applied as named
     without a third table — the user has now spoken twice — and the pass
     proceeds; *Apply nothing* at any point ends the pass unchanged.
   - Whatever the answer, **every item not accepted for a change is left
     byte-for-byte untouched** — `keep` is a no-op, never a re-wording, and
     an item the user pulled out of a `merge` or `drop` stays as it was.

4. **Apply.** Edit `cairn/ROADMAP.md` and `cairn/DESIGN.md` per the accepted
   dispositions, nothing else. Each edit anchors on the item's own text
   (occurring once) and is re-read before the next step claims it landed
   (tracking-rules "verify a batched edit landed"). Per disposition:
   `compress` rewrites in place; `merge` rewrites the survivor and removes
   the absorbed line; `split` replaces one line with its named rows, each
   `added <original date> — <original origin>, split <today>`; `drop`
   removes the line; `route` writes the item in its destination's shape — a
   Known issues entry states the limitation as it **is** and how it was
   accepted (`routed from candidates <today>`), a candidate row states what
   it is, its promotion trigger as the class of evidence that would change
   the stance, and `added <today> — routed from Known issues`; `promote`
   and `keep` change nothing. Candidates stay one item per line, ordered
   higher-priority-first (advisory). After the edits, `wc -l -c
   cairn/ROADMAP.md` stays under the ROADMAP line cap and byte budget
   (tracking-rules "Weight caps"); a pass that would push it over is
   re-cut before it commits, never committed over.

5. **Record.** Two kinds of removal leave two kinds of record:
   - **A decision entry** — one per pass, appended to `cairn/DECISIONS.md`,
     only when at least one accepted `drop` is *rejected on principle* or at
     least one accepted `merge` loses the absorbed row's promotion trigger.
     Its shape is the triage-pass precedent's (`### D-027` in this repo's
     `DECISIONS.md` is the model — read it) minus its counts:
     **Context** (that a triage pass ran and what it weighed), **Decision**
     (each removed item by subject, its reason, and for a trigger-losing
     merge the trigger that no longer stands), **Consequences** (any prior
     decision entry the removal supersedes, named by id in the heading and
     the body; each removal re-openable by superseding this entry). No
     derived counts anywhere in it (the D-entry rule) — the stamp carries
     what the pass changed. Show the drafted entry verbatim in chat in the
     turn that commits it (durable-record preview: it rides in the close
     block's final rendered text).
   - **The commit message and the stamp** — a `drop` whose reason is a
     refuted premise or work already shipped is named there and nowhere
     else: deferrals and refuted premises are ROADMAP facts, not decisions.
   `keep`, `compress`, `split`, `route`, and a trigger-preserving `merge`
   write no decision entry; the stamp is their record.

6. **Stamp and commit.** Replace the ROADMAP `_Last hygiene check:` line —
   replace, never append (tracking-rules) — with one line dated today naming
   what the pass changed: each dropped, merged, split, routed, and
   compressed item by subject, the drops' reason classes, whether a decision
   entry was written, and `validate green`. Then run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_validate.py"` — it must
   pass — and make **one docs-only commit on the default branch**, subject
   prefixed `triage:`, body naming the refuted-premise and already-shipped
   drops with their evidence, and push it (the git model: docs-only
   tracking commits go straight to the pushed default branch; nothing here
   needs the merge gate because no code moves). Every `cairn/` change the
   gate accepted lands in that one commit, and nothing else does.

7. **Close block** (tracking-rules "Question gates and phase closes"), no
   chip. Lead with the outcome in plain words: what left the lists, what
   merged or moved, what stayed. Then a status line — items enumerated,
   dispositions applied by kind, the commit hash, or "nothing applied". The
   decision entry, if written, verbatim (step 5). Then, for **every**
   accepted `promote`, its own fenced block:

   ```
   /milestone-plan <the promoted item's title>
   ```

   labeled as the next command for that item (several promotes → several
   blocks, higher-priority-first). The safety line: the pass is committed
   and pushed (or wrote nothing), so `/clear` is safe here, and any item
   can be re-examined by running `/cairn-triage` again; an item dropped on
   principle returns only by superseding the pass's decision entry.
