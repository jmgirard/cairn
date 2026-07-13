<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. -->
# M51: Oracle-registry doctrine (shape-free)

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Principles touched:** GP4
- **Branch/PR:** m51-oracle-registry-doctrine · https://github.com/jmgirard/cairn/pull/49

## Goal

Fold a shape-free oracle-registry requirement into the Validation doctrine —
catalogue each oracle so the ≥2-independent-types bar is auditable at scale —
without adopting any single registry file shape.

## Scope

**In:** Add one requirement to the `tracking-rules.md` "Validation doctrine"
section: every oracle is recorded (ID, type, its asserting `test:line`, source,
provenance) so the ≥2-independent-types bar is auditable at a glance, with the
asserting test as the single source of truth the record maps to. State the
record is **shape-free** — a central registry file, distributed generator
headers, or embedded fixture fields all satisfy it. Lock it with a
`test_oracle_doctrine.py` anchor. Record the content-not-shape disposition as a
superseding D-entry (annotating D-024/D-025, citing D-028's precedent).

**Out:**
- Adopting a central `ORACLES.md` as a new cairn tracking file → rejected in
  this milestone's D-entry (the shape-free choice supersedes it), re-openable
  by superseding that entry if a cairn-tracked statistical repo needs the
  central index.
- Any `cairn_validate` CHECK for oracle records → not in scope; the Validation
  doctrine is advisory prose enforced by review judgment, never a validate gate
  (matches M33/M42/M49).
- Naming exemplar repos (ackwards/intraclass) in the shared rulebook → the
  rulebook stays self-contained (D-024); exemplar grounding lives in the
  D-entry and the existing `references/oracle-*-notes.md`.
- Graduating the ROADMAP candidate row → happens at post-merge hygiene, not at
  plan time (M35 lesson); the row stays until M51 completes.

## Acceptance criteria

- [x] AC1 — The `tracking-rules.md` Validation doctrine names the oracle-registry
      requirement: each oracle recorded by **ID, type, asserting `test:line`,
      source, and provenance**, so the ≥2-independent-types bar is auditable, with
      the asserting test as the single source of truth. Evidence: the text plus a
      passing `test_oracle_doctrine.py` anchor asserting these field names on one
      physical line.
- [x] AC2 — The doctrine states the record is **shape-free** — a central registry
      file, distributed generator headers, or embedded fixture fields all satisfy
      it — and contains **no cross-repo citation** (no exemplar repo names) in the
      shared rulebook (D-024 self-contained rule). Evidence: a `test_oracle_doctrine.py`
      anchor on the three-shapes phrasing; the new assertions fail against the
      pre-M51 rulebook (M39/M40 false-coverage sanity check, recorded in the work log).
- [x] AC3 — A superseding D-entry (D-029) records the content-not-shape
      disposition: it annotates D-024/D-025 (their type list and deferral stand),
      cites D-028 as the precedent, and explicitly rejects the central-`ORACLES.md`
      tracking-file shape as this milestone's choice (re-openable by supersede).
      Evidence: the D-entry exists in `cairn/DECISIONS.md`.
- [x] AC4 — The generic profile's `verify` slot is clean: the full test suite
      passes (`python3 -m unittest discover -s skills/tests` and
      `-s scripts/tests`). Evidence: both runs report OK.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T3
- AC4 → T4

## Tasks

- [x] T1 — Add the registry-auditability paragraph to `tracking-rules.md` Validation doctrine (fields + rationale + shape-freedom; no repo names).
- [x] T2 — Add two `test_oracle_doctrine.py` anchors (field list, shape-free phrasing), RED-first per the M39/M40/M50 false-coverage discipline.
- [x] T3 — Append D-029 to `cairn/DECISIONS.md` (content-not-shape; annotates D-024/D-025, cites D-028, rejects the central-file shape).
- [x] T4 — Run both suites (`skills/tests`, `scripts/tests`); confirm green.

## Work log

- 2026-07-12: created by /milestone-plan (disposition B, shape-free registry
  doctrine + prose+guard enforcement; both chosen at the plan question gate).
- 2026-07-12: T2+T1 — wrote the two guard anchors first (`test:line` field list,
  `shape is the repo's choice`); confirmed both FAIL against the pre-T1 rulebook
  (RED, M39/M40 false-coverage check), then added the registry paragraph →
  7/7 green. Anchors are on new tokens absent from the pre-M51 file (grep: `registry`,
  `test:line`, `shape is the repo` all 0; avoided `auditable`, 2 pre-existing).
- 2026-07-12: T3 — D-029 appended (content-not-shape, annotates D-024/D-025,
  cites D-028, rejects the central-`ORACLES.md` file shape). T4 — full suites
  green: `skills/tests` 131 OK, `scripts/tests` 65 OK; `cairn_validate` 14/14
  PASS + sizing OK. Status → review.

## Decisions
<!-- owner: implement / review · append-only; milestone-local; promote
     cross-cutting ones to cairn/DECISIONS.md -->

## Review
<!-- owner: review · exclusive; evidence per criterion; consistency-gate
     results; independent-review findings and their triage -->

Reviewed 2026-07-12 · PR #49 · branch base == origin/main (not stale).

**Acceptance-criteria evidence (fresh):**
- AC1 ✓ — `tracking-rules.md` Validation doctrine carries the "Oracle registry
  (auditability)" paragraph naming the field list **ID, type, asserting
  `test:line`, source, and provenance** + the single-source-to-the-test
  rationale. `test_oracle_registry_records_the_audit_fields` passes.
- AC2 ✓ — the paragraph states the record's **shape is the repo's choice**
  (central file / distributed headers / embedded fixture fields);
  `grep -ciE "ackwards|intraclass"` over the new paragraph = **0** (self-contained,
  D-024). `test_oracle_registry_is_shape_free` passes.
- AC3 ✓ — D-029 present in `cairn/DECISIONS.md`: annotates D-024/D-025, cites
  D-028 as the content-not-shape precedent, rejects the central-`ORACLES.md`
  file shape and a `cairn_validate` CHECK.
- AC4 ✓ — `python3 -m unittest discover -s skills/tests` → 131 OK;
  `-s scripts/tests` → 65 OK.

**Consistency gate:** `cairn_validate` exit 0 — 14/14 PASS (incl. coverage
completeness, weight caps, sizing OK). `generic` profile `consistency-gate`
slot names no toolchain checks (clean no-op). DESIGN.md/GP4 unchanged on branch
→ `cairn_impact` correctly skipped (no principle changed).

**Independent review — three lenses, zero findings, no scorer needed:**
- [O] diff-bug (Opus): no surviving findings. Confirmed both guard anchors are
  absent from `origin/main`'s rulebook (genuine fail-on-removal, not false
  coverage) and D-029 is internally consistent with D-024/D-025/D-028.
- [S] blame-history (Sonnet): no findings. `git blame` confirms the ≥2-types
  bar / five types / reproducibility hard-stop are byte-for-byte unchanged (pure
  insertion); D-029's "annotates, not supersedes" framing verified against
  history; no stale-count trap (7 test defs match the work log).
- [S] prior-PR-comments (Sonnet): no prior-PR evidence — inline review-comment
  corpus on the touched files is empty (verified access; expected per M40).

**Sub-blocking note (not a finding, pre-existing):** the append-only D-log is
non-monotonic — D-028 is labelled 2026-07-13 though its commit landed 2026-07-12
(as did all M49/M50 work); D-029's 2026-07-12 is the correct date. D-028's label
(and the ROADMAP "Last hygiene check: 2026-07-13") are pre-existing mislabels,
out of M51's scope (append-only, already merged).
