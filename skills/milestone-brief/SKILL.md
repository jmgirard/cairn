---
name: milestone-brief
description: Escalate a hard technical question to a Fable-level review via a self-contained Review Brief (RB), and ingest the resulting Review Report (RR). Use when a question needs stronger review than the session can settle - statistical correctness, high-stakes design - or when the user says "fable review", "review brief", or an RR file needs ingesting.
argument-hint: "<id> <topic>"
---

# /milestone-brief <id> <topic> — Fable escalation (RB → RR)

Read `${CLAUDE_PLUGIN_ROOT}/skills/shared/tracking-rules.md` first and obey
it. Stage banner: `[cairn · brief · RB<NN> · <draft|gate|ingest>]`.
Fable is token-billed pay-per-use: spawning it requires **explicit user
approval, every time, with no standing authorization** — and only ever
through this protocol. The brief artifact comes first either way; it is what
makes the review reproducible and its findings ingestible.

## Creating a brief

1. Determine the next RB number (max across `cairn/reviews/` and its
   archive, +1). Create `cairn/reviews/RB<NN>-<slug>.md` from
   `${CLAUDE_PLUGIN_ROOT}/skills/shared/templates/brief.md`. It must be
   fully self-contained (assume zero conversation context): background,
   exact files/lines to examine, numbered specific questions (never
   "thoughts?"), constraints with D-entry links, and the required output
   path `cairn/reviews/RR<NN>-<slug>.md`.

2. Set the milestone `blocked` (work-log line: "blocked on RB<NN>").
   Commit (docs-only, main): `brief RB<NN>: <topic>`.

3. **Approval gate** (AskUserQuestion): present the brief's scope, a rough
   size estimate (files/lines Fable must read), and a reminder that Fable is
   token-billed. Options:
   - **Spawn Fable subagent** (recommended) — on approval, launch an Agent
     with `model: "fable"` ([F]-tagged description) whose entire prompt is: read
     `cairn/reviews/RB<NN>-<slug>.md` and follow its instructions exactly,
     writing findings to the RR path it specifies. When it returns, run
     ingestion (below) immediately in this session.
   - **I'll run it manually** — tell the user verbatim:
     > Open a fresh Fable session in the repo root and prompt:
     > `Read cairn/reviews/RB<NN>-<slug>.md and follow its instructions exactly.`
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
   (logged).
4. Move the RB/RR pair to `cairn/reviews/archive/`; milestone status back
   to `in-progress`; commit (docs-only): `ingest RR<NN>`.
5. Routing chip, composed from where the RR left the milestone — e.g.
   **Resume implementation** → `/milestone-implement <id>` (recommended) /
   Stop here.

Robustness:

- **Pasted RR content:** if the user pastes review output into chat instead
  of the file, normalize it — write the RR file from the paste verbatim,
  then ingest as usual. Never reject usable review output on formal grounds.
- **Non-responsive RR:** if the RR fails to answer the brief's questions,
  mark it unresolved and draft a fresh RB (new number) rather than
  re-ingesting a bad artifact.
