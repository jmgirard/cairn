# M176: The amendment-time re-audit records a work-log line

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2
- **Resolves:** —
- **Surface tier:** user-facing — skill conduct prose the plugin ships to every adopting repo (`/milestone-implement` step 6, `/milestone-brief` step 3)
- **Branch/PR:** m176-reaudit-record · https://github.com/jmgirard/cairn/pull/182

## Goal

The criteria audit's third surface — the amendment-time re-audit in `/milestone-implement` step 6 — records a work-log line in a fixed shape, and the ingest audit's line names the criteria it cleared, so a resumed session reads the once-per-criterion re-entry bound and the ingest-clearance exemption from the work log alone.

## Scope

**In:** `/milestone-implement` step 6's re-audit clause gains a mandatory work-log line in a fixed shape — `re-audit: AC<N> (<full|reduced>) — <what it returned, or "nothing">` — one line per criterion re-entered, with the once-per-criterion bound, its further-churn stop, and the ingest-clearance exemption restated as readings of work-log lines; `/milestone-brief` step 3's ingest-audit line gains a fixed shape naming the criteria it cleared — `ingest audit RR<NN> (full): cleared AC<list> — <what it returned, or "nothing">`; a hand-run of the existing `skills/tests` locators (no new pins — the profile's test-doctrine, D-109); a CHANGELOG Unreleased entry. The D-entry recording this milestone's passage through the D-108 door is written in the plan commit, before the file (records-hygiene §2).

**Out:** a `cairn_validate` or `cairn_next` check that parses or counts the new lines — rejected at the plan gate (work log below), no follow-up home. The `/milestone-plan` step 3 audit line's own shape — unchanged, it already names the mode and no count reads it (D-079 clause 2, D-111). Review-side reclassification of record-binding criterion failures — the existing ROADMAP candidate row. A resume route that re-runs a re-audit whose line is absent — `/milestone-implement`'s resume already re-derives state from the file; an absent line reads as "did not run" and the amendment is re-entered as any other.

## Acceptance criteria

- [x] AC1: `/milestone-implement` step 6 states that the amendment-time re-audit records one work-log line either way, one line per criterion re-entered, in the fixed shape `re-audit: AC<N> (<full|reduced>) — <what it returned, or "nothing">`, and that an absent line means the reader did not run, never that it ran and was silent.
- [x] AC2: `/milestone-implement` step 6 states the once-per-criterion re-entry bound and its stop as read from those lines — a second `re-audit: AC<N>` line naming the same criterion on one milestone is the stop, and further churn on that criterion goes to the user — with no appeal to session memory.
- [x] AC3: `/milestone-brief` step 3 states that the ingest audit's work-log line takes the fixed shape `ingest audit RR<NN> (full): cleared AC<list> — <what it returned, or "nothing">`, and `/milestone-implement` step 6's exemption reads that line by name: amended wording is exempt from the re-audit only when the ingest line names the criterion and the amended text equals the ingested text whitespace-normalized (the `binding criteria` check's comparison).
- [x] AC4: The profile's `verify` slot (`python3 -m unittest discover -s scripts/tests` and `python3 -m unittest discover -s hooks/tests`, each exit code checked) exits 0 at the reviewed commit.

## Coverage

- AC1 → T1
- AC2 → T1
- AC3 → T1, T2
- AC4 → T4

## Tasks

- [x] T1: Rewrite the re-audit clause of `/milestone-implement` step 6 (`skills/milestone-implement/SKILL.md:111-124`): add the record sentence and fixed shape (AC1); restate the once-per-criterion bound and further-churn stop as a reading of `re-audit: AC<N>` lines (AC2); restate the exemption as reading the ingest line by name with the whitespace-normalized equality condition (AC3, implement side). Keep every sentence the existing `TestAmendmentReaudit` pins match, or reword the new sentence rather than a pinned one (LESSONS M148).
- [x] T2: Give `/milestone-brief` step 3's ingest-audit record sentence (`skills/milestone-brief/SKILL.md:128-130`) the fixed shape naming the cleared criteria (AC3, brief side), keeping the sentence `TestRRIngestionCriteriaAudit.test_ingest_audit_records_its_own_line_on_the_plan_gate_terms` pins.
- [x] T3: Hand-run `python3 -m unittest discover -s skills/tests` after T1 and T2 to confirm the existing `TestAmendmentReaudit` and `TestRRIngestionCriteriaAudit` locators still match (a new sentence echoing a pinned phrase breaks uniqueness — LESSONS M148); no new pins or mutation entries — the profile's test-doctrine says a new skill rule owes none (M144, D-109).
- [x] T4: CHANGELOG Unreleased entry; run both gating suites from the repo root with exit codes checked; `cairn_validate` green; checkpoint commit.

## Work log

- 2026-09-03: created by /milestone-plan, promoted from the ROADMAP candidate row "The amendment-time audit surface records nothing" (added 2026-08-09, M138 review F1/F8); the row stays until post-merge hygiene (records-hygiene §1).
- 2026-09-03: plan gate chose a fixed line shape (`re-audit: AC<N> (<mode>) — …`) over a freeform "re-audit ran" sentence because the once-per-criterion bound needs a token a resumed session can count; falsified by a resume that finds the shape present and the count still ambiguous.
- 2026-09-03: plan gate chose naming the cleared criteria in the ingest line, with whitespace-normalized equality as the exemption test, over leaving the exemption's referent as the line's existence because an existence test exempts every later amendment on an ingested milestone; falsified by an RR whose criteria list cannot be named on one work-log line.
- 2026-09-03: criteria audit ran in full mode ([O] fresh reader, user-facing tier): 5 findings — evidence-quotation clauses cut from AC1–AC3 (record-instrument binding); AC4 narrowed to the gating `verify` slot and its probe clause dropped (instrument-bound; the profile's test-doctrine owes no prose guard); the D-108 door posed at the gate; joint satisfiability and Coverage clean.
- 2026-09-03: plan gate chose a by-name exception to D-108's door (D-132) over restating the trigger as a shipped-behavior defect (none observed) and over leaving the row parked for the next step-6 milestone because the user mandated promotion with the trigger unfired; falsified by a resume that never reads the line.
- 2026-09-03: plan gate chose no new prose guards over pins and mutation entries per the profile's test-doctrine (a new skill rule owes none, D-109); falsified by the new sentences drifting unnoticed past a PR diff review.
- 2026-09-03: plan gate chose prose-only record lines over a `cairn_validate` count of them because the row parked exactly the mechanized form and D-108's door bars new apparatus; falsified by a resume that miscounts re-entries with the shape present.
- 2026-09-03: T1 — step 6 re-audit clause rewritten: record sentence with the `re-audit: AC<N> (<full|reduced>) — …` shape and the absent-line reading (AC1); bound and stop restated as readings of `re-audit: AC<N>` lines (AC2); exemption restated as reading the ingest line by name with whitespace-normalized equality (AC3). The three `TestAmendmentReaudit` pinned sentences kept verbatim; verify slot 334+126 green, hand-run skills/tests 604 green.
- 2026-09-03: T2 — `/milestone-brief` step 3's ingest-audit sentence gains the `ingest audit RR<NN> (full): cleared AC<list> — …` shape and states that step 6's exemption reads the cleared list by name; the `test_ingest_audit_records_its_own_line_on_the_plan_gate_terms` sentence and its line wrap kept verbatim. Verify slot 334+126 green.
- 2026-09-03: T3 — hand-run `python3 -m unittest discover -s skills/tests` after T1+T2: 604 tests OK, exit 0; `-k TestAmendmentReaudit -k TestRRIngestionCriteriaAudit` 13 tests OK. No pins or mutation entries added (D-109).
- 2026-09-03: T4 — CHANGELOG Unreleased entry added; gating suites 334+126 OK with exit 0 each; `cairn_validate` all checks passed. Status → review.

## Decisions

## Review

Reviewed 2026-09-03 at 9be5731 (PR #182), main at 050c45f, branch up to date with origin/main.

- AC1 — `skills/milestone-implement/SKILL.md:120-124` states the re-audit "records one work-log line either way, one line per criterion re-entered, in the fixed shape `re-audit: AC<N> (<full|reduced>) — <what it returned, or "nothing">`" and that "an absent line means the reader did not run, never that it ran and was silent" (grep, same-session read). PASS.
- AC2 — `skills/milestone-implement/SKILL.md:133-138` states the bound and stop "both read from the `re-audit: AC<N>` lines, never from session memory: a second `re-audit: AC<N>` line naming the same criterion on one milestone is the stop", with further churn going to the user (the kept pinned sentence). PASS.
- AC3 — `skills/milestone-brief/SKILL.md:130-135` states the shape `ingest audit RR<NN> (full): cleared AC<list> — <what it returned, or "nothing">` and that step 6's exemption reads the cleared list by name; `skills/milestone-implement/SKILL.md:125-131` reads the ingest line by name and requires the amended text to equal the ingested text whitespace-normalized, citing the `binding criteria` check (its `_norm` at `scripts/cairn_validate.py:584-587` is `" ".join(s.split())`). PASS.
- AC4 — at 9be5731: `python3 -m unittest discover -s scripts/tests` 334 tests OK exit 0; `python3 -m unittest discover -s hooks/tests` 126 tests OK exit 0. PASS.

Consistency gate: `cairn_validate` all checks passed (exit 0); no principle changed, `cairn_impact` skipped; profile `consistency-gate` slot names no toolchain checks (generic), no CI in this repo.

Independent review (user-facing tier → three lenses, fresh context):

- [O] diff-bug: 9 findings.
  - O1 (stop stated one re-entry late — a second line never written if re-entry is once): rejected. The first line records the reader's audit of the amended wording; the once re-entry after a mini-gate fix writes the second, which is the stop — AC2's reading. Fix-now clarifying sentence added at step 6 naming which line is which.
  - O2 (ingested text not on the work log, so equality is not decidable from the log alone): fix-now — step 6 now names the ingested text as the criterion the milestone file carried at the ingest commit.
  - O3 (`binding criteria` check compares BC-to-AC substrings, not amended-to-ingested equality): fix-now — the citation now names the normalization only (`" ".join(s.split())`).
  - O4 (`AC<list>` spelling undefined, defeating a by-name read): fix-now — brief step 3 requires each criterion spelled with its own `AC<N>` token, never a range or shared prefix.
  - O5 (no form for an empty cleared list): fix-now — `cleared none`.
  - O6 (an exempt criterion writes no line, so absence is overloaded): fix-now — step 6 states an exempt criterion writes no re-audit line and spends no re-entry; absence beside a naming ingest line with equal text reads as exempt.
  - O7 ("cleared" ambiguous for wording fixed at the gate): fix-now — the conservative reading: passed unchanged; a criterion reworded at the gate is not cleared.
  - O8 (CHANGELOG drops "whitespace-normalized"): fix-now.
  - O9 (three audit surfaces record in three spellings; informational): rejected — the plan line's shape is out of scope by the plan, no count reads across surfaces.
- [S] blame-history: 1 candidate, self-assessed compliant — per-surface shape strings alongside kept cross-references vs D-071 single-home; rejected: D-132 authorizes the third surface, and the wiring matches the M130/M132 precedent.
- [S] prior-PR-comments: no regressions; `gh api …/pulls/comments?per_page=1` returned `[]`, archive `## Review` findings on these files (M121, M130, M132, M134, M138, M148, M151) checked; pinned sentences verified verbatim.

Fix-now set applied on the branch after the pre-gate checkpoint; suites re-run: scripts 334 OK, hooks 126 OK, skills/tests 604 OK (hand-run), `cairn_validate` exit 0.
