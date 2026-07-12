# M20: Migration stress-test pilot — ackwards (Lineage B) — done 2026-07-12

**Goal:** harden `/cairn-init` §2 by piloting it for real on a mature Lineage B
R package (ackwards), folding surfaced gaps back into the skill.

**Outcome:** ran `/cairn-init` migration live on ackwards → PR jmgirard/ackwards#53
(docs-only): M1–M53 entombed to `cairn/legacy/`, DESIGN.md kept verbatim as
canonical (§14 embedded), 15 still-governing decisions re-recorded to a fresh
DECISIONS.md (Sonnet-extracted, no-invention verified), CLAUDE.md redistributed,
live state → candidates. Audit 8/9 (only the documented CLAUDE-cap FAIL).
Cairn-side (cairn PR #18, merged): `references/migration-pilot-notes.md` (10
tagged gaps) + 5 ROADMAP hardening candidates.

**Headline findings:** the `<80` CLAUDE cap doesn't survive a mature repo (187
lines post-redistribution); cairn is `main`-hardcoded (no `master` adaptation);
mature repos cite tracking files by name in source (~17 refs); a rich
pre-existing DESIGN.md with an embedded decision log breaks the thin-DESIGN
assumption. All → candidates (gaps are design-level; no `fix-here` emerged).

**Key decisions:** Compromise A (keep DESIGN verbatim; full §14 extraction
deferred as candidate); CLAUDE-cap over-run accepted as a documented exception
(AC2 amended at user gate). Review: 2 lenses + scorer; H1 (dropped owner
CI/branch-protection decision) + O1 (§14 citation summary) fixed; O2 logged.
