<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M20: Migration stress-test pilot — ackwards (Lineage B)

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Branch/PR:** m20-migration-pilot-ackwards (cairn side); ackwards PR #53

## Goal

Harden the `/cairn-init` §2 migration protocol by piloting it end-to-end for
real on the ackwards R package (Lineage B), folding surfaced gaps back into
the skill.

## Scope

**In:**
- Execute `/cairn-init` §2 migration on **ackwards** on a
  `cairn-init-migration` branch → real PR, CI exercised. (ackwards' own IDs
  are qualified "ackwards M<nn>"; this milestone is cairn M20.)
- Capture the run in `cairn/references/migration-pilot-notes.md` (committed
  **here**): the migration ledger summary, a per-§2-step friction log, and a
  gap list, each gap tagged `fix-here | candidate | out`.
- Land small-and-clear fixes to `/cairn-init` SKILL §2 and/or
  `tracking-rules.md` for surfaced gaps; lock any new mechanical invariant
  with a guard test in `skills/tests/`.

**Out:**
- circumplex migration → **M21** (depends on M20).
- Merging the ackwards PR / ackwards actually adopting cairn → ackwards' own
  review gate, decided there later; not required to close M20.
- Any design-heavy protocol redesign a gap implies → ROADMAP `candidate` row
  (or its own milestone), never forced into this PR.

## Acceptance criteria

- [ ] `/cairn-init` §2 executed on ackwards on a `cairn-init-migration`
      branch; PR opened; the PR description carries a complete **migration
      ledger** — every legacy file and every live item → new location /
      "entombed" / "dropped at user request" (§2 step 7b). Evidence: PR URL +
      ledger text.
- [ ] The `/milestone` health audit runs on the ackwards migration branch with
      **only the documented CLAUDE-cap exception outstanding** — 8/9 checks pass;
      the sole FAIL (CLAUDE.md 187 > `<80` cap) is a surfaced pilot finding filed
      as a cairn candidate, not a migration defect (amended 2026-07-12 at user
      gate; see Decisions). Evidence: audit output in pilot notes + ROADMAP G8 candidate.
- [ ] Migration performed correctly: ackwards' completed history moved
      **verbatim** to `cairn/legacy/` (no completed milestone rewritten), and
      the 3 repo-local skills (`implement-milestone`, `plan-milestone`,
      `post-milestone-review`) relocated out of `.claude/skills/`. Evidence:
      file listing / git diff in the pilot notes.
- [ ] `cairn/references/migration-pilot-notes.md` committed in this repo with
      the ledger summary, per-§2-step friction log, and the tagged gap list;
      one row added to `references/INDEX.md`. Evidence: file + INDEX row.
- [ ] Every gap tagged `fix-here` is resolved in this milestone (a `/cairn-init`
      and/or `tracking-rules.md` edit), each new mechanical invariant locked by
      a guard test; every `candidate` gap has a ROADMAP row. Evidence: diffs +
      passing tests + ROADMAP rows.
- [ ] Guard-test suite green: `python3 -m pytest` (or the repo's runner) over
      `skills/tests/` and `scripts/tests/`. Evidence: test run output.

## Coverage

- AC1 → T1, T2, T3, T4, T5, T6
- AC2 → T6
- AC3 → T3, T5
- AC4 → T7
- AC5 → T8
- AC6 → T9

## Tasks

- [x] **T1** — Preconditions + branch (§2 steps 1–2): confirm ackwards has a
      clean tree and nothing genuinely in-flight (carry at most one
      `in-progress`, explicitly); cut `cairn-init-migration` from up-to-date
      ackwards main.
- [x] **T2** — Inventory + disposition (§2 step 3): list every legacy tracking
      file and every live item; draft the status-mapping proposal. Note:
      ackwards' ROADMAP says "no scheduled milestones" — verify live state is
      mostly release-tail + unscheduled ideas (→ candidates), not planned work.
- [x] **T3** — Entomb history verbatim (§2 step 4): move legacy tracking files
      whole to ackwards `cairn/legacy/`; new ROADMAP header points at legacy +
      git log.
- [x] **T4** — Translate live state under the no-invention rule (§2 step 5):
      live items → milestone files / candidate rows; IDs continue from the
      legacy maximum; DECISIONS.md starts fresh at D-001 with a legacy pointer;
      re-record only still-governing decisions.
- [x] **T5** — Redistribute + deactivate (§2 step 6): CLAUDE.md content per the
      ownership table; relocate the 3 repo-local skills to `cairn/legacy/`;
      scaffold missing §1 pieces + ignore entries.
- [x] **T6** — Open the ackwards PR with the ledger in its description; run the
      `/milestone` health audit on the branch; observe CI. Record PR URL,
      ledger, and audit output (§2 step 7).
- [x] **T7** — Write `cairn/references/migration-pilot-notes.md` here: ledger
      summary + per-§2-step friction log + gap list (each tagged
      `fix-here | candidate | out`); add the `references/INDEX.md` row.
- [x] **T8** — Land `fix-here` gaps in `/cairn-init` SKILL and/or
      `tracking-rules.md`; add guard tests for any new mechanical invariant;
      file `candidate` gaps as ROADMAP rows.
- [x] **T9** — Run the guard-test suite green; commit cairn-side tracking +
      code together.

## Work log

- 2026-07-11: created by /milestone-plan (promotes the "stress-test migration
  on a Lineage B repo" candidate, DRAFT_2 §11; lineage M03 tidymedia pilot).
- 2026-07-11: in-progress; cut cairn branch m20-migration-pilot-ackwards.
- 2026-07-12: ran /cairn-init §2 live on ackwards; migration branch + PR #53
  (docs-only ledger); entombed M1–M53 history, kept DESIGN.md verbatim,
  15 still-governing decisions → DECISIONS.md (Sonnet-extracted, verified).
- 2026-07-12: health audit 8/9 — CLAUDE-cap FAIL accepted as documented
  exception (AC2 amended at user gate); pilot notes + INDEX row written (T7);
  10 gaps → 5 ROADMAP candidates (T8). No small isolable fix-here emerged.

## Decisions

- 2026-07-12 (Compromise A, user gate): a rich pre-existing DESIGN.md is kept
  verbatim as the canonical `cairn/DESIGN.md` with its §14 decision log embedded
  as frozen history; DECISIONS.md re-records only still-governing cross-cutting
  decisions citing §14. Full §14 extraction + inline-ref repoint (Compromise B)
  deferred as a ROADMAP candidate. Invariants stay as CLAUDE hard rules;
  IP/GP formalization routed to /design-interview (candidate).
- 2026-07-12 (cap exception, user gate): the `<80` CLAUDE.md cap is not met by a
  mature migrated repo even after full redistribution (ackwards 187 lines);
  accepted as a documented audit exception for this migration and filed as a
  cairn candidate (recalibrate the cap). The cap recalibration itself is a
  cross-cutting cairn design change → belongs to a follow-up cairn milestone,
  not a milestone-local D-entry here.

## Review
