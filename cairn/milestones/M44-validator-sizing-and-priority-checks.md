# M44: Validator-hardening — sizing advisory + Priority-field schema

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Principles touched:** —   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Branch/PR:** m44-validator-checks · https://github.com/jmgirard/cairn/pull/42   <!-- owner: implement (branch) / review (PR URL) · create -->

## Goal

Give `cairn_validate` the two judgment-call checks it still lacks — a
non-failing sizing **advisory** and a hard **Priority-field** vocabulary
check — turning two prose-only rules into deterministic script output.

## Scope

**In:**
- A new non-failing **advisory (WARN)** output tier in `cairn_validate`,
  rendered distinctly from `PASS`/`FAIL` and never affecting the exit code.
- A **sizing advisory** check: per live milestone file, count acceptance
  criteria and tasks and emit a `WARN` when a file exceeds the split
  tripwires (>7 criteria, >10 tasks — `tracking-rules.md` "Sizing").
  Advisory, because the tripwires are advisory (a milestone may exceed them
  with stated justification).
- A **Priority-field vocabulary** check (hard `FAIL`): every ROADMAP row's
  Priority value is one of `{high, normal, low}` (`PRIORITY_ORDER` keys),
  parallel to the existing `check_vocab` for status.
- `/milestone` Audit-section text documenting the advisory output
  (report-but-don't-fail; advisories are not gate failures).
- Dropping the two low-fit M06 steals (parallel-task metadata, tiered tool
  exposure) with a `DECISIONS.md` entry, and updating the M06 candidate row.

**Out:**
- Scored-rubric hygiene audit for `/milestone` → stays a candidate sub-item
  of the M06 row (not built: it cuts against cairn's binary-gate audit).
- Extra header-field schemas beyond Priority (Depends-on format, Branch/PR
  format) → not now; `check_coverage_complete`/`check_principles_slot`
  already cover the fragments that mattered, so the "strict schemas" steal is
  effectively shipped bar this Priority residual.
- Turning the sizing advisory into a hard failure → out by design (advisory,
  not a gate).
- Gated candidates (content-gated memory guard, scripts `--json`,
  scaffold-spec version stamp, session-opening TOC label) → unchanged
  candidate rows; each awaits its own recorded trigger.

## Acceptance criteria

- [x] AC1 — `cairn_validate` renders a distinct advisory section; a milestone
      file that exceeds a sizing tripwire yields a `WARN` line **and the exit
      code stays 0** (advisories never fail the gate). Test: a fixture with 8
      criteria / 11 tasks → WARN + exit 0.
- [x] AC2 — The sizing advisory fires at **>7 acceptance criteria** and
      **>10 tasks** per live milestone file, and no-ops for files within both
      tripwires and for archived files. Test: within-tripwire fixture → no
      WARN; each threshold exercised at boundary.
- [x] AC3 — A ROADMAP row whose Priority is outside `{high, normal, low}`
      makes the Priority-vocab check `FAIL` (exit 1); valid priorities pass.
      Test: bad-priority fixture fails, valid-priority fixture passes.
- [x] AC4 — The pre-existing 12 checks and the clean-tree suite still pass
      unchanged — no regression to exit codes or output assertions from the
      new advisory section. Test: full `scripts/tests` suite green.
- [x] AC5 — Tracking updated: `/milestone` Audit documents the advisory
      output; the two low-fit steals are removed from the ROADMAP with a
      `DECISIONS.md` entry recording the rationale; the M06 candidate row
      reflects the drops and this milestone. Evidence: grep of the skill,
      ROADMAP, and DECISIONS.

## Coverage

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T4
- AC5 → T5, T6

## Tasks

- [x] T1 — Tests-first, then add the advisory tier to `cairn_validate.run()`:
      an `ADVISORIES` list rendered as `WARN`/`OK` lines, tallied separately
      from `failures` so the exit code is unaffected
      (`scripts/cairn_validate.py:340` `run`).
- [x] T2 — Implement `check_sizing_advisory`: count criteria via the existing
      `_AC_ITEM`/`_section_body` helpers and count tasks via a task-checkbox
      matcher over the Tasks section; WARN over >7 / >10; skip archived files.
      Register in `ADVISORIES`. Add a dedicated `live_sized(status, n_crit,
      n_tasks)` builder rather than mutating `Tree.build` (M34/M38 lesson).
- [x] T3 — Implement `check_priority_vocab` (ROADMAP Priority ∈
      `PRIORITY_ORDER` keys), parallel to `check_vocab`; register in `CHECKS`.
      Tests: bad priority fails, valid passes (base fixture priorities are
      already valid, so `Tree.build` is untouched).
- [x] T4 — Run `python3 -m unittest discover -s scripts/tests` (M32: this
      repo has no pytest); confirm the existing checks + clean-tree assertions
      stay green, fixing any output-assertion breakage caused by the new
      advisory section.
- [x] T5 — Update the `/milestone` SKILL Audit section to document the
      advisory output (report-but-don't-fail), anchoring any new guard
      assertion on phrasing the feature uniquely introduces (M39/M40 lesson).
- [x] T6 — Append the `DECISIONS.md` entry dropping parallel-task metadata +
      tiered tool exposure (don't-fit-cairn rationale); update the M06
      candidate row (remove those two sub-items; note sizing advisory shipped
      here and Priority check fulfills the strict-schemas residual); update
      ROADMAP status/rows. (D-026 + M06 row landed at the plan gate where the
      drop was decided; branch inherits them — see work log.)

## Work log

- 2026-07-12: created by /milestone-plan (validator-hardening pair; folds the
  split-advisory + Priority-schema M06 steals, drops two low-fit steals).
- 2026-07-12: T1–T4 — added the ADVISORIES WARN tier + `check_sizing_advisory`
  + `check_priority_vocab` to cairn_validate; 58/58 script tests green, live
  repo validates clean (13 PASS + OK sizing).
- 2026-07-12: T5 — documented the advisory output in the /milestone SKILL
  Audit section (report-but-don't-fix; WARN never blocks the gate).
- 2026-07-12: T6 — D-026 (drop parallel-task-metadata + tiered-tool-exposure)
  and the M06 row rewrite were committed at the plan gate where the drop was
  decided; the m44 branch was cut afterward and inherits them, so the drop is
  in repo state (grep-verified) though not in the PR diff. Status → review.

## Decisions

## Review

**Evidence (2026-07-12, fresh):**
- AC1/AC2 — `TestSizingAdvisory` (4 tests) green; live over-tripwire fixture
  (9 crit / 12 tasks) → `WARN sizing (2)` + `all checks passed` + exit 0; the
  criteria (>7) and tasks (>10) thresholds each fired independently, 7/10
  boundary produced `OK`, and archived files were skipped (function-level).
- AC3 — `test_unknown_priority` fails on `urgent` with exit 1; clean tree
  (valid priorities) passes `priority vocabulary`.
- AC4 — full suite 58/58 green; live repo `cairn_validate` exit 0 (13 PASS +
  `OK sizing`), no regression to the pre-existing checks.
- AC5 — skill Audit documents advisories (SKILL.md:52+, "non-failing
  advisories"; status+priority vocab at :48); `D-026` present; ROADMAP M06 row
  records the two drops and M44/M38/M39 dispositions.

**Consistency gate:** `cairn_validate` exit 0; Coverage complete (AC1→T1 …
AC5→T5,T6, all mapped); no DESIGN principle changed (slot `—`) → cairn_impact
skipped; R gates waived (plugin repo, per CLAUDE.md).

**Independent review (3 lenses, fresh-context):** zero findings.
[O] diff-bug (Opus) — verified thresholds (strict `>`, 7/10 boundary), section
parsing, exit-code neutrality, priority-field/set, CHECKS/ADVISORIES wiring, and
that no consumer parses `run()` text (all assertions are `assertIn`/returncode);
tests are not false-coverage (each fails if its feature is removed).
[S] blame-history (Sonnet) — `run()` contract preserved, registration follows
the `check_vocab` pattern, `live_sized` honors the M34/M38 don't-mutate-Tree.build
lesson; no D-entry/lesson contradicted. [S] prior-PR-comments (Sonnet) — no
prior-PR evidence, lens no-ops (expected, M40). Nothing to score/triage.
