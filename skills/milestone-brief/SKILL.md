---
name: milestone-brief
description: Escalate a hard technical question to a Fable-level review via a self-contained Review Brief (RB), and ingest the resulting Review Report (RR). Use when a question needs stronger review than the session can settle - statistical correctness, high-stakes design - or when the user says "fable review", "review brief", or an RR file needs ingesting.
argument-hint: "<id> <topic>"
---

# /milestone-brief <id> <topic> — Fable escalation (RB → RR)

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it.
Phase header: `# Review brief RB<NN>` → `## Draft` / `## Gate` / `## Ingest`.
Chapter markers: mark a chapter at each phase transition — each phase its
`Phase header:` directive names (session start implicit).
Fable is no longer pay-on-demand, but it typically uses more tokens than Opus:
spawning it requires **explicit user approval, every time** — a deliberate
per-instance choice, never a standing default — and only ever through this
protocol. The brief artifact comes first either way; it is what makes the
review reproducible and its findings ingestible. (D-062 updated this framing,
retaining D-004's per-instance gate on token-cost grounds.)

## Creating a brief

1. Determine the next RB number (max across `cairn/reviews/` and its
   archive, +1). Create `cairn/reviews/RB<NN>-<slug>.md` from
   `${CLAUDE_PLUGIN_ROOT}/skills/shared/templates/brief.md`. It must be
   fully self-contained (assume zero conversation context): background,
   exact files/lines to examine, numbered specific questions (never
   "thoughts?"), constraints with D-entry links, and the required output
   path `cairn/reviews/RR<NN>-<slug>.md`.
   **An RR is advisory by default:** the brief requests a
   `## Binding criteria` section only on the maintainer's explicit choice,
   recorded in the RB itself at authoring time — absent that request the RR
   emits recommendations only.
   **A mechanism's second escalation lists removal:** when the brief's
   subject mechanism is on its second or later escalation — counted by
   sweeping `cairn/reviews/` and `cairn/reviews/archive/` for briefs naming
   the same mechanism — the brief lists removal of that mechanism among the
   options it puts to the reviewer (RR13 B1: advisory conclusions delivered
   at Fable fluency acquire unearned momentum, and both RRs on §8's second
   escalation recommended amended keeps that a blunt retirement outperformed).

2. Set the milestone `blocked` (work-log line: "blocked on RB<NN>").
   Commit (docs-only, main): `brief RB<NN>: <topic>`.

3. **Approval gate** (AskUserQuestion): present the brief's scope, a rough
   size estimate (files/lines Fable must read), and a reminder that Fable
   typically uses more tokens than Opus. Acceptance chips (tracking-rules): show the drafted RB's
   question and scope text verbatim in the chat above, best-effort, with
   the compact form in the chip (Mandated-substance rule), never only a
   description. Options:
   - **Spawn Fable subagent** (recommended) — on approval, launch an Agent
     with `model: "fable"` ([F]-tagged description) whose entire prompt
     is: read
     `cairn/reviews/RB<NN>-<slug>.md` and follow its instructions exactly,
     writing findings to the RR path it specifies. When it returns, run
     ingestion (below) immediately in this session.
   - **I'll run it manually** — this is a **handoff**, so the prompt goes in a
     fenced block, never a blockquote or inline backticks (tracking-rules
     "Copy-run commands"): a blockquote renders no copy button and the user
     has to retype the path. Tell them to open a fresh Fable session in the
     repo root, and emit the prompt as its own copyable block:
     ```
     Read cairn/reviews/RB<NN>-<slug>.md and follow its instructions exactly.
     ```
     Then stop the turn; ingestion happens at the next session start.
   - **Cancel** — unblock the milestone; note the question as unresolved in
     the work-log.

4. Never spawn Fable without this gate, and never proceed past the blocking
   question while the RB is open.

## Ingesting an RR

Runs immediately after a spawned review returns, or automatically at session
start (any skill) when a manual RR appears:

1. Read the RR. Record its answers as dated entries in the milestone's
   Decisions section; promote cross-cutting ones to `cairn/DECISIONS.md`.
2. **If a recommendation contradicts a standing D-entry:** supersede, don't
   ignore — quote the prior rationale to the user and only proceed by
   appending a superseding D-entry. Never silently override the record, and
   never silently discard Fable's advice.
3. Apply or schedule recommendations as tasks (or candidate rows for
   out-of-scope ones), each triaged: apply / consider / reject-with-reason
   (logged). **Binding criteria travel verbatim:** when the RR carries a
   `## Binding criteria` section, the milestone it constrains sets its
   header's `Driving RR:` slot to `RR<NN>` and ingests each criterion
   verbatim into its `## Acceptance criteria` as a numbered acceptance
   criterion carrying its trace tag — `- [ ] ACn (BCm): <verbatim>` — and
   gives that criterion its own `## Coverage` line: `coverage-complete`
   counts every AC checkbox positionally, so a bare, unnumbered BC checkbox
   reds that check (M107). This runs through the `/milestone-implement`
   step-6 amendment gate when the AC block already exists. After ingesting,
   re-check the plan-owned body against the 150-line cap; if the added
   criteria push it over, compress the single heaviest plan-owned section in
   one pass (tracking-rules), never a nibble-and-recount loop.
   Any departure is a row in the "Deviations from RR<NN>" table at
   the end of that AC section, shown verbatim at this ingestion's preview,
   never slipped — IP3 applied to review findings. `cairn_validate`'s
   `binding criteria` check string-compares the AC block against the RR
   (whitespace-normalized): a softened criterion is a red check, not a
   reading. Copy the RR's numeric projections beside the criteria with
   their stated tolerances; an unstated tolerance is strict — any shortfall
   forces the accept-shortfall option at the merge gate.
   **A binding-criteria set is audited before it is ingested**, by the same
   fresh-context **[O]** reader `/milestone-plan` step 3 spawns (under a
   spawn-restricting harness instruction, tracking-rules' freshness-spawns
   clause governs) and the same
   three questions — *what state of the world satisfies this exactly as
   written*, *does any IP or D-entry make that state unreachable*, and
   *does it make a universal claim over a domain no procedure it names enumerates*
   — asked
   of the set as well as of each criterion, because criteria that are
   individually satisfiable can still be **jointly** unsatisfiable, and a
   frozen scope in one can forbid the work another mandates.
   The third question is asked of the
   domain the claim quantifies over, never of a proxy the named procedure
   happens to enumerate (M132).
   Where a criterion cites a mutation, inversion, or planted-defect
   verification, the audit asks whether the probes vary every axis the
   verified domain is free in — form as well as location — or stand one
   exemplar in for the family.
   A brief has
   already been convened over exactly that, with the collision surfacing at a
   review gate instead of here. What the audit returns is raised with the
   user, never softened away: `binding criteria` string-compares the AC block,
   so a quietly reworded criterion reds the check, and any departure agreed
   at the gate becomes a row in the Deviations table below. The ingest audit
   records one work-log line either way, on `/milestone-plan` step 3's terms
   (its line names the full mode — the ingest audit has no reduced form), in
   the fixed shape `ingest audit RR<NN> (full): cleared AC<list> — <what it
   returned, or "nothing">`: the cleared list names every criterion whose
   ingested wording the audit passed, and `/milestone-implement` step 6's
   re-audit exemption reads that list by name — a criterion the list omits
   is not exempt.
4. Relocate the RB/RR pair to `cairn/reviews/archive/` with plain `mv` then
   `git add`, never `git mv` — an in-session-generated or hand-dropped RR is
   untracked, and `git mv` fails on an untracked file; milestone status back
   to `in-progress`; durable-record preview (tracking-rules): show the
   Decisions entries, D-entries, and candidate rows the ingestion wrote
   verbatim in a guaranteed-rendered position (Mandated-substance rule);
   commit (docs-only): `ingest RR<NN>`.
5. **Close block** (tracking-rules "Question gates and phase closes"),
   composed from where the RR left the milestone — recap, status line,
   fenced next command(s) with plain labels (e.g. `/milestone-implement <id>`
   to resume), and the adjust-or-`/clear` safety line; no chip.
   The RR's conclusions/verdict section is shown verbatim in the close block's turn (its final rendered text, Mandated-substance rule).

Robustness:

- **Pasted RR content:** if the user pastes review output into chat instead
  of the file, normalize it — write the RR file from the paste verbatim,
  then ingest as usual. Never reject usable review output on formal grounds.
- **Non-responsive RR:** if the RR fails to answer the brief's questions,
  mark it unresolved and draft a fresh RB (new number) rather than
  re-ingesting a bad artifact.
