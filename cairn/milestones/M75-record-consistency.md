<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M75: Record consistency — the `leave` disposition and MCP-matcher semantics

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** IP3   <!-- owner: plan · create/amend-via-gate -->
- **Branch/PR:** `m75-record-consistency` · https://github.com/jmgirard/cairn/pull/73   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Close two gaps where cairn's durable record fails to carry a fact its own
work already established.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** a `tracking-rules.md` Intake line legitimizing `leave` as a fourth
disposition, narrowed to noise, duplicates, and items already
cross-referenced in cairn; D-044 recording the IP3 reading that narrowing
rests on; an MCP-matcher bullet in `cairn/references/claude-code-hooks.md`;
a label-inclusive guard over the new rulebook line.

**Out:**

- Pruning `LESSONS.md:41` (the M71 matcher lesson) → ordinary post-merge
  hygiene, when the 50-line cap forces it. Decided at the M75 plan gate:
  the reference page becomes the durable home; the lesson prunes naturally.
- Guard coverage for the *rest* of the unguarded Intake paragraph → a
  candidate row if it ever matters; this milestone guards only the line it
  adds and the enumeration that line joins.
- Any change to `/milestone` §3's four dispositions → they stand as M74
  shipped them; the rulebook moves to meet the skill, not the reverse.
- A content guard over the hooks reference page → no reference page carries
  one (they record external facts, not cairn contracts); AC4's grep is the
  evidence.

**Settled at the plan gate, not open:** whether legitimizing `leave` weakens
IP3's conservation guarantee as D-042 extended it ("what the session
surfaced"). Settled in-session via D-044 rather than escalated — a
reason-stated, user-chosen `leave` on noise is not a *silent* drop, which is
what IP3 forbids. Implement inherits the answer, not the question.

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] AC1 — `tracking-rules.md`'s Intake paragraph names `leave` as a legal
      fourth disposition with its narrowing (noise, duplicates, already
      cross-referenced) stated on one physical line; the pre-M75 three-way
      sentence no longer stands as the whole enumeration.
- [x] AC2 — `cairn/DECISIONS.md` carries D-044 recording the IP3/D-042
      reading, the chosen narrowing, and the two rejected alternatives
      (drop `leave` from the skill; legitimize it unnarrowed).
- [x] AC3 — the rulebook line and `/milestone` §3's `leave` bullet agree:
      both texts quoted side by side in the Review section show no
      contradiction, and §3's four dispositions are unchanged by this
      milestone (`git diff` over `skills/milestone/SKILL.md` touches no
      disposition text).
- [ ] AC4 — `cairn/references/claude-code-hooks.md`'s "Matchers & execution"
      section states that a matcher of only word chars, `-`, space, `,` or
      `|` is compared as an exact string, so an MCP tool matcher must carry a
      metacharacter; its `INDEX.md` line still describes the page accurately.
- [x] AC5 — a guard asserts the new rulebook line *including its `leave`
      label* (M74/F3: a clause-only assert survives a label swap), with a
      mutation-harness entry whose anchor phrase is unique within
      `tracking-rules.md` (M58).
- [x] AC6 — verify clean: `python3 -m unittest discover` green for
      `scripts/tests`, `skills/tests`, and `hooks/tests`; `cairn_validate.py`
      exits 0.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T1
- AC4 → T3
- AC5 → T4
- AC6 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1 — Add the `leave` line to the Intake paragraph,
      `skills/shared/tracking-rules.md:199-205`. Keep the guarded phrase on
      one physical line (M23) and clear of `**bold**` splits (M26). Do not
      touch `skills/milestone/SKILL.md`.
- [x] T2 — Append D-044 to `cairn/DECISIONS.md` (text drafted at the plan
      gate; append-only, never renumber).
- [x] T3 — Add the MCP-matcher bullet to the "Matchers & execution" section,
      `cairn/references/claude-code-hooks.md:94-100`, alongside the existing
      exact-vs-regex bullet. Re-read the page's `INDEX.md` line and confirm
      it still describes the page.
- [x] T4 — Guard T1 in `skills/tests/test_external_pr_intake.py` (it already
      reads `tracking-rules.md` and owns the intake paragraph's PR half):
      a label-inclusive assert plus a `Mutation(...)` entry in
      `test_mutation_harness.py`. Run all three suites and `cairn_validate.py`;
      check exit codes explicitly, never through a pipe (M56/M65).

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-18: created by /milestone-plan; absorbs the M74-F5 and M71-F3 candidate rows.
- 2026-07-18: T1 — rulebook Intake paragraph names `leave`, narrowed per D-044; phrase unique in file; 96/287/72 suites green.
- 2026-07-18: T2 — no branch work needed: D-044 landed in the plan commit a00653d, before the branch was cut. Ticked as satisfied, not re-authored.
- 2026-07-18: T3 — MCP-matcher bullet added to the hooks reference; exemplar verified live against hooks.json:67 + idea_guard.py:28 (same suffix shape); INDEX line amended to record the non-official-docs provenance.
- 2026-07-18: T4 — two label-inclusive guards + two mutation entries; label swap (`leave`→`ignore`) proven to fail the suite, not just blanking. Verify clean: scripts 96 / skills 289 / hooks 72, cairn_validate 0, exit codes checked unpiped (M56/M65).
- 2026-07-18: all tasks done; status → review.
- 2026-07-18: review GATE FAILED → in-progress. F1: the hooks-reference matcher rule is factually wrong (literal path splits on `|`/`,` and compares each part; verified in binary 2.1.207) and AC4's own wording mandates the error — needs a gated AC4 amendment. F2: `tracking-rules.md:202` dropped D-044's "in cairn" locus. F4: a guard comment overclaims coverage `assertIn` does not give. AC1/AC4 unticked.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion, consistency-gate
     results, review findings + triage. EXEMPT from the 150-line cap (M55):
     only the plan-owned body above counts; evidence never scrambles it. -->

**PR:** https://github.com/jmgirard/cairn/pull/73 · reviewed 2026-07-18 ·
no CI on this repo (`gh pr checks 73` → "no checks reported", exit 0; M16).

### Criterion evidence (fresh, by command)

- **AC1** — `tracking-rules.md:202` carries the narrowing on one physical
  line; the surrounding paragraph (`:199-207`) shows the pre-M75 three-way
  sentence now continues into the fourth disposition rather than standing
  alone.
- **AC2** — `DECISIONS.md:1014` opens D-044; the entry states the IP3
  reading (silent-drop vs. reason-stated), the narrowing, and both rejected
  alternatives (drop `leave` from the skill; legitimize it unnarrowed).
- **AC3** — `git diff --stat main..HEAD -- skills/milestone/SKILL.md` is
  empty: no disposition text touched. The two texts read together —
  rulebook: "`leave` is legal only for noise, duplicates, or already-covered
  items — no row, no action, reason stated, never anything genuinely new";
  skill `SKILL.md:129`: "**leave** — no row, no action, with the reason
  stated." The skill states the mechanics, the rulebook adds the eligibility
  bar; no contradiction.
- **AC4** — `claude-code-hooks.md:101-108` states the exact-vs-regex rule for
  MCP names, that `_` is a word char, and the metacharacter remedy. Exemplar
  verified live: `hooks.json:67` = `"mcp__.*__spawn_task"`,
  `idea_guard.py:28` = `^mcp__.+__spawn_task$` — same suffix shape as
  claimed. `INDEX.md:13` amended to record the non-official-docs provenance.
- **AC5** — two asserts at `test_external_pr_intake.py:144,152`, both
  label-inclusive; both anchors occur exactly once in `tracking-rules.md`
  (M58). Falsifiability proven beyond blanking: swapping the label
  `leave`→`ignore` turned the suite red (1 failure + 1 harness hard-error),
  which is the M74/F3 mode blanking alone cannot reach.
- **AC6** — scripts 96 / skills 289 / hooks 72 all `OK`; `cairn_validate`
  exit 0, 17 checks. Exit codes captured directly, never through a pipe
  (M56/M65).

### Fan-out findings (2026-07-18) — GATE FAILED, returned to implement

Three lenses. Blame-history: 0 findings. Prior-PR-comments: 0 findings
(no inline PR comments exist on #69–#72; it read the archive files instead).
Diff-bug [O]: 4 findings. Scorer [S] gave 35 / 82 / 40 / 78.

**Actioned:**

- **F1 (scored 35 — score overridden, operator judgment; M73 lesson).**
  `claude-code-hooks.md:101-105` states the matcher rule wrongly. Verified
  against the installed binary (2.1.207): the literal path is
  `/^[a-zA-Z0-9_|, -]+$/` followed by `e.split(/[|,]/)`, so it splits on `|`
  and `,` and exact-compares each alternative — not a whole-string exact
  compare. `Edit|Write` matches both. The bullet names `,` and `|` in its own
  character list and then calls the result "an EXACT string". The scorer
  agreed the mechanism splits, objecting only that the single-name worked
  example is accurate; for a page being promoted to oracle here, a general
  rule wrong for two of five named characters is load-bearing. The error is
  inherited verbatim from `LESSONS.md:41`, so **M71's lesson is also wrong**.
- **F2 (82).** `tracking-rules.md:202` dropped the "in cairn" locus: D-044
  narrows `leave` to items "already cross-referenced **in cairn**" and AC1
  says "already cross-referenced", but the delivered line reads
  "already-covered items". An issue tracked only on an upstream board reads
  as covered, gets `leave`, and its sole record is the GitHub issue — the
  D-042 substitution the narrowing exists to forbid.
- **F4 (78).** `test_external_pr_intake.py:141` comment claims "widening the
  narrowing has to fail this too". `assertIn` is a substring match, so an
  appended fourth category leaves both guards green — verified directly by
  the scorer. The label-swap and blanking claims in the same comment hold.

**Logged, sub-threshold, not actioned:**

- **F3 (40).** "the fourth disposition" counts §3's list, not the rulebook's,
  and the rulebook never names `/milestone-plan` as an *issue* route. The
  phrasing explicitly scopes the numbering to §3, so this is largely
  readability — but the missing issue-route remains true.

**Gate disposition.** AC4 is worded to require the page state the *wrong*
rule ("compared as an exact string"). Correcting the prose makes AC4 fail as
written, and review never reinterprets a criterion — so M75 returns to
`in-progress` for a gated AC4 amendment plus the F1/F2/F4 fixes, then
re-review. First trip back (thrash rule: not triggered).

### Consistency gate

`cairn_validate` exit 0 (all checks pass, incl. `coverage complete`).
Profile is `generic`, whose `consistency-gate` slot names no toolchain
checks — that half is a clean no-op. `cairn_impact --changed`: "no changed
principles" — M75 reasons about IP3 but changes no principle text, so no
reconciliation was owed.
