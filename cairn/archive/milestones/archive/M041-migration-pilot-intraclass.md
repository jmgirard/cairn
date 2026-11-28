# M41: Migration stress-test pilot — intraclass (first Lineage A) — done 2026-07-12

**Goal:** harden `/cairn-init` §2 by piloting it live on intraclass — the first
**Lineage A** precursor (a full multi-file `project/` board) — folding small gaps
into the skill and deferring design-level ones as candidates.

**Outcome:** ran `/cairn-init` §2 migration live on intraclass → PR
jmgirard/intraclass#54 (docs-only, **0 package files**, 27×100% renames, audit
**12/12** clean — no exception, vs M20's 8/9). Entombed the status/history board +
6 repo-local skills to `cairn/legacy/`; kept `PRINCIPLES.md` (numbering intact),
`REFERENCES.md`→`references/`, `COVERAGE.md`/`estimand-specs/` repo-specific;
authored DESIGN seed + ROADMAP (IDs from M48) + **pointer-only** DECISIONS. cairn
PR #39. Independent 3-lens review 0 findings.

**Headline finding (G-I2):** the target cites principles **by number in 70 in-code
comments across 29 files** (`PRINCIPLES.md #N`) — folding them into DESIGN's IP/GP
strands all 70 or breaks the docs-only rule → **note-and-leave** forced. Like M20,
all 5 gaps (G-I1..G-I5) are design-level + interconnected: **no `fix-here`
emerged**, promoted to one grouped "Lineage A migration guidance" candidate for a
deliberate hardening milestone (M22/M23 pattern). Oracle-registry gap (G-I3) = the
existing `ORACLES.md` candidate, fed by M42.

**Key decisions (gate):** live branch + real PR; pointer-only DECISIONS for the
58-ADR log; concern-files integrated into cairn homes / kept repo-specific (no
DESIGN.md existed — Lineage A). Full record: `references/migration-pilot-notes.md` Pilot 3.
