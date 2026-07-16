# M61: External de-risking (done)

**Goal:** Close RR01 rec 14's pre-1.0 external-adopter risks: environment
assumptions, first-contact migration safety, cross-profile symmetry.
PR #59 (squash, 2026-07-16).

**Outcome:**
- `/cairn-init` §0 opens with an environment check — git/python3/gh/remote
  probes, a named degradation path per gap, only missing git fatal.
- All 8 hooks.json commands chain `|| py -3 <same script>` (Windows launcher
  fallback; user-gated). Safe on macOS/Linux: every hook exits 0, denies via
  JSON stdout. Best-effort, Windows-unverified (DESIGN Known issues).
- Migration protocol gains a read-only dry-run mode: step-3 inventory +
  proposed ledger, nothing written, offered at migration entry (RR01 §10.3).
- python profile test-doctrine mirrors the r-package Codecov CI pair
  (pytest-cov → Codecov, diagnostic-only) — graduates the M52 candidate.
- Amendment (gated, D-034): shipped profiles (97 lines) had outgrown the
  90-line PROFILE.md instantiation cap → cap raised to <120; shipped
  references now cap-coupled in test_scripts.py.

**Review:** all 6 ACs on fresh evidence; suites 184+84+55 + validate green;
fan-out: diff-bug 2 findings (85/88 — dangling comment pointer, 2 missing
mutation entries), both fixed; blame-history + prior-PR lenses clean.
