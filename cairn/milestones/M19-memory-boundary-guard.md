# M19: Memory-boundary write guard (GP4 enforcement)

- **Status:** review
- **Priority:** normal
- **Depends on:** M18
- **Branch/PR:** m19-memory-boundary-guard · [#17](https://github.com/jmgirard/cairn/pull/17)

## Goal

Give GP4 a runtime enforcement arm: a write-time guard that reminds Claude of
the memory→`cairn/`-files boundary when it saves to per-user memory in a cairn
repo — the way `merge_guard.py` enforces IP1.

## Scope

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

- [x] `hooks/memory_guard.py` exists and, given a PreToolUse hook-input JSON
      for a `Write` whose `file_path` is under a `.claude/projects/*/memory/`
      directory with `cwd` a cairn repo, outputs the GP4 boundary reminder;
      given a non-memory path, a non-cairn cwd, or malformed input it produces
      no output (exit 0). Verified by unit test.
- [x] `hooks/hooks.json` registers `memory_guard.py` under `PreToolUse` with a
      `Write` matcher.
- [x] `tracking-rules.md` states the memory→`cairn/`-files intake gate
      (apply the GP4 test before writing memory) in its memory/state
      discipline, naming `cairn/` files for durable knowledge and the plugin
      for generalizable fixes.
- [x] A D-entry records the chosen emission mechanism (non-blocking nudge, or
      the prose-only fallback if PreToolUse cannot emit one) with the
      nag-fatigue rationale.
- [x] The new `hooks/tests/test_hooks.py` cases pass and the full `hooks/tests`
      suite is green.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T5
- AC5 → T4

## Tasks

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
- [x] T5: Record the emission-mechanism D-entry (chosen mechanism +
      nag-fatigue rationale; prose-only fallback path).
      ([DECISIONS.md](../DECISIONS.md))

## Work log

- 2026-07-11: created by /milestone-plan. Reframed from a cairn-developer
  concern to GP4's general enforcement arm (durable knowledge → cairn/ files,
  not per-user memory) after the D-011 memory slip earlier this session.
  Gate: softest non-blocking nudge (prose-only fallback), Depends on M18.
- 2026-07-12: /milestone-implement start; branch m19-memory-boundary-guard,
  status in-progress. T1: PreToolUse CAN emit a non-blocking nudge via
  hookSpecificOutput.additionalContext (permissionDecision optional) — plan of
  record holds, prose-only fallback not needed.
- 2026-07-12: T1 — wrote hooks/memory_guard.py; gate = silent context nudge
  (additionalContext-only, no permissionDecision). Smoke-tested all branches.
- 2026-07-12: T2 — registered memory_guard.py in hooks.json under PreToolUse
  with a Write matcher. T3 — added "Memory intake gate (GP4)" bullet to
  tracking-rules.md. T4 — TestMemoryGuard + shared no-op/garbage cases; hooks
  suite green (22). T5 — recorded D-017.
- 2026-07-12: /milestone-review — trimmed redundant section-owner scaffolding
  comments to hold the 150-line cap (no tracking content changed). Review
  below.

## Decisions

- 2026-07-12: emission mechanism = non-blocking `additionalContext` nudge, no
  `permissionDecision` (softest lever; T1 confirmed PreToolUse supports it).
  Cross-cutting → promoted to D-017.

## Review

Same-session review 2026-07-12 — evidence by command; two fresh subagents + scorer.

**AC evidence (fresh):** AC1 ✓ direct invocation — memory-path `Write` in a
cairn cwd emits `PreToolUse / additionalContext(GP4) / no permissionDecision`;
non-memory, non-cairn, non-Write, malformed → no output, exit 0 (`TestMemoryGuard`
×4). AC2 ✓ hooks.json PreToolUse `Write`→memory_guard.py. AC3 ✓ tracking-rules
"Memory intake gate (GP4)" bullet. AC4 ✓ D-017. AC5 ✓ hooks suite green (22).

**Consistency gate:** cairn_validate.py exit 0 (9 checks); Coverage complete
(AC1→T1…AC5→T4, all tasks present); DESIGN untouched (GP4 pre-exists, no Sync
Impact needed); R gates (document/check, README, pkgdown, NEWS, .Rbuildignore)
waived — plugin repo per CLAUDE.md, no CI workflow.

**Independent review** ([O] diff-bug + [S] blame-history, then [S] scorer):
- [S] blame-history: no findings — extends M07's hook pattern, respects the M07
  testing lesson, D-011/GP4-consistent, appends D-017 without editing prior
  entries, leaves plan-owned Goal/Scope/AC untouched.
- [O] diff-bug: code clean (regex, fail-permissive, non-vacuous tests, envelope
  verified). 1 finding — contract reference omitted PreToolUse
  `additionalContext` — scorer 78, sub-threshold (<80): logged, not
  force-actioned (real but self-acknowledged/non-urgent).
- Triage: actioned its cheap slice anyway — recorded PreToolUse
  `additionalContext` (+ T1 source) in `references/claude-code-hooks.md`.
  Residual: the true live-fire needs a fresh post-merge session (hooks snapshot
  at process start); tracked in D-017.
