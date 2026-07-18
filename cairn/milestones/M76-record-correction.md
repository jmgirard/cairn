<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M76: Record correction — history vs. current knowledge, and the correct-in-place protocol

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP4, GP2   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m76-record-correction`   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give cairn a stated rule for correcting a durable record later proven false,
by splitting the tracking files into history (supersede, never edit) and
current knowledge (correctable in place, marked).

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a `tracking-rules.md` rule naming which records are history — DECISIONS,
work-logs, IDs, entombed `legacy/` files — and which are current knowledge —
`LESSONS.md`, `references/` pages, `DESIGN.md` — with the correction mechanism
for the latter: fix in place, mark the correction (`(M71, corrected M75)`),
git keeps the original. The `LESSONS.md` file-map row and the three other live
"append-only" labels for that file are corrected to match. D-045 records the
mechanism, the split, and the reading of IP4 that both rest on. The stale M71
matcher rule still sitting in `hooks/tests/test_hooks.py:912` and echoed at
`references/claude-code-hooks.md:105` is swept — the first instance the new
rule governs.

**Out:** amending IP4's DESIGN.md wording — the gate chose to record the
reading instead (IP4's history set never named LESSONS), so no IP text changes
and there is no remainder to home. A `cairn_validate` CHECK for correction
markers is **declined, not deferred** (rationale in D-045): advisory doctrine
has never been a validate gate (M33/M42/M49), so no candidate row.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `tracking-rules.md` carries a named rule for correcting a durable
      record proven false: it names the history set and the current-knowledge
      set explicitly, and states correct-in-place-with-a-marker as the
      mechanism for the latter.
- [ ] AC2 — the file map's `cairn/LESSONS.md` row no longer calls the file
      append-only and names its actual write-mode instead.
- [ ] AC3 — a repo-wide `git grep` finds no live file calling `LESSONS.md`
      append-only. Exempt from the sweep: history files (`cairn/DECISIONS.md`,
      `cairn/milestones/archive/`, `cairn/reviews/archive/`, `cairn/legacy/`),
      the `cairn/ROADMAP.md` candidate row that quotes the defect, and this
      milestone file's own Scope (M62 — the sweep hits the text it must write).
- [ ] AC4 — `cairn/DECISIONS.md` carries D-045 recording the mechanism, the
      history/current-knowledge split, and the IP4 reading; `cairn/DESIGN.md`'s
      IP4 line is byte-identical to its pre-milestone text (`git diff` on that
      line is empty). (ip-touching: settled at the 2026-07-18 plan gate —
      the reading is recorded, IP4's wording is not amended.)
- [ ] AC5 — `hooks/tests/test_hooks.py`'s matcher comment and
      `references/claude-code-hooks.md:105` both state the verified rule (a
      literal matcher is split on `|`/`,` and each alternative exact-matched);
      no live file claims a literal matcher is compared as one whole exact
      string.
- [ ] AC6 — new guards lock AC1's rule **label-inclusively** (M74: the assert
      names the rule label, not only its clause, so a label swap fails), each
      is registered in `skills/tests/test_mutation_harness.py`, and the three
      suites are green: `python3 -m unittest discover -s scripts/tests`,
      `-s skills/tests`, `-s hooks/tests` (generic profile `verify`).

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T2
- AC2 → T2
- AC3 → T2, T3
- AC4 → T1
- AC5 → T4
- AC6 → T5, T6

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — author D-045 in `cairn/DECISIONS.md`: the correct-in-place
      mechanism, the history/current-knowledge split, the IP4 reading, and the
      declined validate CHECK. Annotates D-015; leaves IP4 untouched.
- [x] T2 — `skills/shared/tracking-rules.md`: add the correction rule to
      "Universal tracking rules" adjacent to "Append, don't rewrite" (:118),
      and fix the `cairn/LESSONS.md` file-map row (:23). Author the rule's
      label on ONE physical line (M59/M64 reflow trap — AC6's guard greps it).
- [x] T3 — sweep the three remaining live "append-only" labels for LESSONS:
      `skills/cairn-init/SKILL.md:103`, `cairn/LESSONS.md:8` (the file's own
      header), `skills/tests/test_lessons_loop.py:3` (docstring). Verify with a
      repo-wide `git grep` per AC3's exemption list, not a per-file read (M48).
- [x] T4 — sweep the stale matcher rule: rewrite the comment at
      `hooks/tests/test_hooks.py:912` and the loose echo at
      `references/claude-code-hooks.md:105` to the split-then-exact-match rule.
      Read the corrected rule out of `references/claude-code-hooks.md`'s
      verified dispatch section, never restated from a work-log (M75).
- [x] T5 — guards for AC1/AC2 in `skills/tests/test_lessons_loop.py` (its
      subject is the LESSONS contract) + `Mutation(...)` entries per positive
      assert, not per file (M53).
- [x] T6 — full verify: the three suites green, `cairn_validate.py` green,
      caps clean. Run from the repo root, exit codes gating the chain, never
      piped through `tail` (M56/M65).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan; promotes the durable-record-correction
  candidate row (M75 review G4/91 + G2/78). Four gate decisions: correct in
  place marked; general history/knowledge split; record the IP4 reading without
  amending IP4; fold the matcher sweep in.
- 2026-07-18: branch `m76-record-correction` cut from main; status -> in-progress.
- 2026-07-18: minor amendment — T1 ticked as already satisfied: /milestone-plan
  authors D-entries in its own commit, so D-045 landed in 9ac2311 at plan time.
  No re-authoring; AC4's evidence reads the committed entry.
- 2026-07-18: T2 — "Correcting a record proven false" added to Universal
  tracking rules (:121-130); LESSONS file-map row no longer says append-only.
  Both label->rule mappings authored on single physical lines for the guards.
- 2026-07-18: T3 — minor amendment: the repo-wide sweep found FOUR live LESSONS
  "append-only" labels, not the three T3 named; `skills/milestone-review/
  SKILL.md:189` (the capture step) was the extra. All four corrected. Vindicates
  M48 (sweep repo-wide, never per-file).
- 2026-07-18: T3 — documenting the rule inside `cairn/LESSONS.md` blew its own
  <50 cap (49 -> 51). Compressed the header back to 3 lines rather than prune
  real lessons for boilerplate; file now 49. The cap remedy landed on the file
  whose mis-labelling started the milestone.
- 2026-07-18: T4 — matcher rule corrected at `hooks/tests/test_hooks.py:912`
  and `references/claude-code-hooks.md:105`, the latter marked
  `(corrected M76)` — the new rule's first application, dogfooded. Left
  `:121` alone: it verbatim-quotes Claude Code's own shipped warning, which is
  accurate for the narrower `mcp__server` case it describes.
- 2026-07-18: T5 — `TestRecordCorrectionRule` (6 asserts) + 5 mutation entries;
  skills suite 289 -> 295. Falsifiability proven twice: mutation harness green
  on blanking, and a by-hand LABEL SWAP (history <-> current knowledge) went
  red as required — the check the harness structurally cannot make (M74/F3).
- 2026-07-18: T6 — all six tasks done; skills 295 / scripts 96 / hooks 72 all
  exit 0, cairn_validate exit 0, caps and sizing clean. `cairn/DESIGN.md` is
  absent from the branch diff entirely, so AC4's IP4-untouched bar holds at its
  strongest. Status -> review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->
