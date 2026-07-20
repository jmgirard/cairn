# What a cairn milestone costs, measured from the session store (M94)

**Provenance.** Ingested 2026-07-19 by M94 from the local Claude Code session
store for this repo — `~/.claude/projects/-Users-jmgirard-GitHub-cairn/*.jsonl`,
115 session files, 44,688 records — read with `scripts/cairn_cost.py`.
Pagination: —.
Extraction: a 2026-07-19 snapshot; the store is a live append log and has moved on independently since, so every figure below is a floor rather than a current value — observed 2026-07-19.

**Scope.** This page records the *method* by which cairn measures its own token
and turn cost, the limits of that method, and a baseline taken once so a later
measurement has something to compare against. It is not a source summary: there
is no external paper here, only this repo's own runtime record. It deliberately
builds no threshold, cap, ratchet, or verdict — M94 reports and never judges,
and the governing mechanism is M96's to define. Standard disclaimer: this is a
reference, not an authority — status lives in `ROADMAP.md`, decisions in
`DECISIONS.md`, architecture in `DESIGN.md`.

**Evidence snapshot.**

- The session store — `~/.claude/projects/-Users-jmgirard-GitHub-cairn/`, 115
  `*.jsonl` files, 189 MB, 44,688 records — observed 2026-07-19.
- A second store checked for subagent records — `-Users-jmgirard-GitHub-intraclass/`,
  65,389 records — observed 2026-07-19.
- Every project store under `~/.claude/projects/`, grepped for
  `"isSidechain":true` — zero matches — observed 2026-07-19.

## What the store is

Claude Code appends one JSON record per event to
`~/.claude/projects/<slug>/<session-uuid>.jsonl`, where `<slug>` is the repo's
absolute path with every non-alphanumeric character replaced by `-`. Records
carry a `type`; the observed set is `assistant`, `user`, `attachment`,
`last-prompt`, and `queue-operation`. Only `assistant` records bill tokens.

An `assistant` record carries `message.usage` with four separately-billed token
classes — `cache_read_input_tokens`, `cache_creation_input_tokens`,
`input_tokens`, `output_tokens` — plus two fields that make attribution
mechanical rather than heuristic: `attributionSkill` (the cairn skill active at
the time, e.g. `cairn:milestone-review`) and `gitBranch`. Both are written by
the runtime, so neither can drift from what actually happened.

**The four classes are never summed.** Over the whole store, cache-read
exceeds fresh input **719:1** (3,174,644,247 vs 4,413,685 — observed
2026-07-19). A collapsed "input" figure would misattribute the cost by roughly
three orders of magnitude, which is why `cairn_cost.py` keeps four columns and
`scripts/tests/test_cairn_cost.py` guards the separation.

## Attribution ledger — how a record is keyed

Tags: `mechanical` (read from a runtime-written field) · `absent` (the record
does not contain it) · `refused` (derivable only by guessing, so not derived).

| # | Quantity | How it is obtained | Tag |
|---|---|---|---|
| A1 | Phase (`plan`/`implement`/`review`, and the other cairn skills) | `attributionSkill` lookup | `mechanical` |
| A2 | Milestone id | `gitBranch` matching `^m(\d{2,})-` → `M<NN>` | `mechanical` |
| A3 | Token cost of a milestone's *plan* phase | plan work runs on the default branch, which names no milestone | `refused` |
| A4 | Subagent token cost | no store record anywhere carries `isSidechain: true` | `absent` |
| A5 | Subagent *count* per phase | `tool_use` blocks named `Agent`/`Task` | `mechanical` |
| A6 | Per-file share of context growth | a shared prompt cache cannot apportion cache reads between files | `refused` |

A3 is why the report states an unattributable share instead of hiding one:
40.7% of assistant turns and 33.9% of cache-read tokens carry no milestone id
(observed 2026-07-19). That share is default-branch work — planning, hygiene
commits, plain conversation — and imputing a milestone for it would mean
guessing, since a single plan session legitimately names four milestones (M94
through M97 were planned in one).

A4 is the method's real blind spot, and it bites hardest exactly where the cost
is highest: `/milestone-review`'s M17 fan-out spawns four subagents per
milestone, and none of their tokens are recorded. Rather than publish a partial
number unlabelled, every report carries A5's spawn count beside the tokens.
The count reads exactly `4` for every reviewed milestone in the baseline below,
which is independent corroboration that the counter is right.

## Baseline — the ten milestones before M94

Per-milestone totals, branch-derived (so `plan`-phase cost is excluded per A3):

| Milestone | turns | cache-read | fresh-in | output | agents |
|---|---|---|---|---|---|
| M93 | 236 | 40,348,807 | 439 | 190,730 | 4 |
| M92 | 208 | 37,082,554 | 381 | 196,418 | 4 |
| M91 | 227 | 48,033,722 | 419 | 200,559 | 4 |
| M90 | 152 | 26,780,610 | 2,874 | 97,486 | 4 |
| M89 | 200 | 36,457,414 | 377 | 150,553 | 4 |
| M88 | 203 | 37,311,561 | 378 | 169,131 | 4 |
| M87 | 151 | 29,981,268 | 917 | 162,267 | 4 |
| M86 | 128 | 20,207,953 | 237 | 109,871 | 4 |
| M85 | 178 | 34,016,600 | 332 | 131,786 | 4 |
| M84 | 203 | 34,209,640 | 384 | 232,447 | 4 |
| **mean** | 188 | 34,443,012 | 673 | 164,124 | 4.0 |

Phase split over those ten: `implement` 1,154 turns / 182,843,790 cache-read;
`review` 482 turns / 103,059,639 cache-read / 34 agents; `unattributed` 250
turns / 58,526,700 cache-read / 6 agents.

**Cache-read per turn** is the derived quantity that tracks always-read weight,
because it is the average context re-read on every single turn:

| Band | turns | cache-read/turn | output/turn |
|---|---|---|---|
| M63–M68 | 589 | 166,451 | 1,034 |
| M69–M80 | 2,112 | 170,250 | 882 |
| M81–M87 | 1,446 | 170,131 | 890 |
| M88–M93 | 1,226 | 184,351 | 819 |

Per-turn context rose **+10.8%** from M63–M68 to M88–M93. Over that same
window `tracking-rules.md` grew +56% and `DECISIONS.md` +103%, so the
always-read tracking files are a minority term in the context a turn actually
carries. Stated as a measurement, not a conclusion: M94 does not judge whether
+10.8% warrants a mechanism, and nothing here licenses a threshold.

## Disposition

- A1, A2, A5 → implemented in `scripts/cairn_cost.py`, guarded behaviourally
  by `scripts/tests/test_cairn_cost.py` (assertions against the classifier
  functions, never the rendered report).
- The four-class separation → guarded in the same file; it is the one property
  whose violation would silently invalidate every figure on this page.
- The reporting-only boundary on the `/milestone` cost line → prose-guarded by
  `skills/tests/test_cost_audit_line.py`, whose three protected blocks are
  registered in the mutation harness and mutation-verified.
- A3 and A4 → stated as limits here and in the script docstring, and surfaced
  in the report output itself (the unattributable share on the attribution
  line; the `agents` column and its "unrecorded" note).
- A6 → stated as a limit here and in the milestone's Scope, and **not**
  surfaced in the report output: there is no figure to caveat, because the
  per-file share is never computed. It was scoped Out at plan time for the
  reason restated above; nothing in this milestone revisits it.
- The baseline table → M96's input. M96 owns any ratchet, threshold, or
  verdict over these numbers; M94 deliberately ships none.
- The `/milestone` audit line → `skills/milestone/SKILL.md` §2, reported
  verbatim, explicitly boundaried as a reporting surface.

## Open questions

- Whether subagent tokens are recorded anywhere on disk at all — checked
  `~/.claude/projects/`, `~/.claude/tasks/` (a todo store, not transcripts),
  and `~/.claude/sessions/`; none carried subagent turns — observed
  2026-07-19. If a surface is found later, A4 stops being `absent` and the
  review-phase figures should be re-measured.
- Whether `attributionSkill` is populated on every Claude Code version an
  adopting repo might run; this repo's store has it throughout, but that is one
  repo on one version — observed 2026-07-19.
- Whether the +10.8% per-turn figure holds once M95's slimming lands; the band
  comparison should be re-run after it merges — observed 2026-07-19.
