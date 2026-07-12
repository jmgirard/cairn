# M21: Migration stress-test pilot — circumplex (Lineage B) — done (2026-07-12)

**Goal:** Second Lineage B migration pilot (after M20 ackwards), run against the
M22/M23-hardened `/cairn-init` §2, folding surfaced gaps back into the skill.

**Outcome:** Ran `/cairn-init` §2 live on circumplex (mature CRAN pkg, `master`
default) → PR https://github.com/jmgirard/circumplex/pull/31 (docs/tracking only,
100% renames, audit 9/9). The hardened protocol held — **5 M22/M23 fixes
validated** against real inputs (default-branch, §0 Lineage B widening,
Compromise A for a 315-line living DESIGN, §6 entombed-skill sweep,
`.Rbuildignore` prune). Only small mechanical residue remained (vs M20's
all-design-level gaps):
- **fix-here G-C1** — §1 scaffold omitted `LESSONS.md` (added; guard-tested).
- **fix-here G-C3** — a legacy "planned" item without criteria/tasks maps to
  `candidate`, not `planned` (§2 step-3 forward-ref + step-5 note; guard-tested).
- **candidates** G-C2 (date-scan false-positive on R CMD check notation),
  G-C4 (mature backlog vs the <60-line ROADMAP cap).

**Key decisions:** disposition (user gate) — circumplex release-prep → one
`blocked` milestone (CRAN cadence ~2026-08-02), M4 entombed done, M6+backlog →
candidates, zero `in-progress`. Full-run + real PR authorized by the user.

**Review:** 6/6 ACs verified fresh; two-lens review found 2 minor wording issues
(scored 80/90), both fixed on-branch. cairn PR #21.
