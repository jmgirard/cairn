<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M19: Memory-boundary write guard (GP4 enforcement)

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** M18   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Branch/PR:** m19-memory-boundary-guard   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

Give GP4 a runtime enforcement arm: a write-time guard that reminds Claude of
the memory→`cairn/`-files boundary when it saves to per-user memory in a cairn
repo — the way `merge_guard.py` enforces IP1.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:**
- New `hooks/memory_guard.py` (PreToolUse on `Write`): fires when a Write's
  `file_path` is under a per-user memory dir (`.claude/projects/*/memory/`)
  while cwd is a cairn repo; emits the softest non-blocking GP4 reminder the
  PreToolUse contract allows. Silent no-op otherwise (non-memory path,
  non-cairn cwd, malformed input) — fail-permissive like the other hooks.
- `hooks/hooks.json`: register the hook under PreToolUse with a `Write` matcher.
- `tracking-rules.md`: state the memory→`cairn/`-files **intake gate** — before
  writing to memory, apply the GP4 test (durable project knowledge → `cairn/`
  files; generalizable conduct/plugin defects → the plugin; memory only holds
  per-user meta-context).
- `hooks/tests/test_hooks.py`: memory-path write in a cairn repo fires;
  non-memory path, non-cairn cwd, and malformed input each no-op.
- D-entry recording the chosen emission mechanism + the nag-fatigue rationale.

**Out:**
- Content-gated firing (inspect memory text, fire only on durable-state
  signals) → candidate row; ship the unconditional soft nudge first, add
  content-gating only if it proves too noisy.
- Runnable-commands-in-code-blocks output-discipline tweak → stays in the
  "Rulebook wording tweaks" candidate (separate concern).
- CLAUDE.md router clause → not added; D-009 keeps the router routing-only, so
  the boundary prose lives in `tracking-rules.md`.
- On-main commit-guard hook (guards non-cairn code commits on main) → the
  distinct existing candidate, not this.

**Plan of record = build the hook** (softest non-blocking emission). If T1's
investigation confirms PreToolUse *cannot* emit a non-blocking nudge, prose-only
is the honest fallback: the D-entry records it and the hook criteria (AC1/AC2/
AC5) are amended via the implement gate (`/milestone-implement` step 6) — never
silently dropped or reinterpreted at review.

**Depends on M18:** both edit `tracking-rules.md`; M19 builds on M18's version
to avoid a merge conflict (the user chose this sequencing).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets -->

- [ ] `hooks/memory_guard.py` exists and, given a PreToolUse hook-input JSON
      for a `Write` whose `file_path` is under a `.claude/projects/*/memory/`
      directory with `cwd` a cairn repo, outputs the GP4 boundary reminder;
      given a non-memory path, a non-cairn cwd, or malformed input it produces
      no output (exit 0). Verified by unit test.
- [ ] `hooks/hooks.json` registers `memory_guard.py` under `PreToolUse` with a
      `Write` matcher.
- [ ] `tracking-rules.md` states the memory→`cairn/`-files intake gate
      (apply the GP4 test before writing memory) in its memory/state
      discipline, naming `cairn/` files for durable knowledge and the plugin
      for generalizable fixes.
- [ ] A D-entry records the chosen emission mechanism (non-blocking nudge, or
      the prose-only fallback if PreToolUse cannot emit one) with the
      nag-fatigue rationale.
- [ ] The new `hooks/tests/test_hooks.py` cases pass and the full `hooks/tests`
      suite is green.

## Coverage
<!-- owner: plan · create/amend-via-gate; each acceptance criterion → the
     task(s) satisfying it, by positional number (AC/Task counted
     top-to-bottom). Review reads to fence evidence — tracking-rules "AC fencing". -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T5
- AC5 → T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive
     change is amend-via-gate -->

- [x] T1: Confirm the PreToolUse emission contract (what non-blocking levers
      exist), then write `hooks/memory_guard.py` — detect a memory-dir `Write`
      in a cairn repo (reuse `cairn_common.find_cairn_root`), emit the softest
      reminder available, no-op otherwise. Pattern:
      ([merge_guard.py](../../hooks/merge_guard.py))
- [x] T2: Register the hook in `hooks/hooks.json` under PreToolUse with a
      `Write` matcher. ([hooks.json:25-36](../../hooks/hooks.json))
- [x] T3: Add the memory→`cairn/`-files intake gate to `tracking-rules.md`
      beside the "Tracking files outrank memory" rule.
      ([tracking-rules.md:99](../../skills/shared/tracking-rules.md))
- [x] T4: Add `memory_guard` cases to `hooks/tests/test_hooks.py` (memory-path
      fires; non-memory / non-cairn / malformed no-op); run the hooks suite
      green. ([test_hooks.py](../../hooks/tests/test_hooks.py))
- [ ] T5: Record the emission-mechanism D-entry (chosen mechanism +
      nag-fatigue rationale; prose-only fallback path).
      ([DECISIONS.md](../DECISIONS.md))

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates -->

- 2026-07-11: created by /milestone-plan. Reframed from a cairn-developer
  concern to GP4's general enforcement arm (durable knowledge → cairn/ files,
  not per-user memory) after the D-011 memory slip earlier this session.
  Gate: softest non-blocking nudge (prose-only fallback), Depends on M18.
- 2026-07-12: /milestone-implement start; branch m19-memory-boundary-guard,
  status in-progress. T1 investigation (official hooks docs): PreToolUse CAN
  emit a non-blocking nudge via hookSpecificOutput.additionalContext
  (permissionDecision optional) — plan of record holds, prose-only fallback
  not needed.
- 2026-07-12: T1 — wrote hooks/memory_guard.py. Gate: silent context nudge
  (additionalContext-only, no permissionDecision) per user "recommend me".
  Smoke-tested: memory write in cairn repo nudges; non-memory / non-cairn /
  non-Write / malformed input all silent no-op (exit 0).
- 2026-07-12: T2 — registered memory_guard.py in hooks.json under PreToolUse
  with a Write matcher (second PreToolUse entry alongside merge_guard/Bash).
  JSON validated.
- 2026-07-12: T3 — added the "Memory intake gate (GP4)" bullet to
  tracking-rules.md beside "Tracking files outrank memory"; states the GP4
  test (durable → cairn/, generalizable → plugin, meta-context → memory) and
  names the hook as prompting the test, not making the call.
- 2026-07-12: T4 — added TestMemoryGuard (nudge fires w/ additionalContext &
  no permissionDecision; non-memory, memory-lookalike-without-/memory/, and
  non-Write no-op) and wired memory_guard.py into the non-cairn + garbage-stdin
  shared tests. Full hooks suite green (22 tests).

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->
