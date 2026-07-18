# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-07-18 (M73 done + archived; M68 pruned under terminal-row retention; M40 and M45 lessons pruned at the LESSONS cap)_

Note: this repo dogfoods the tracking file formats by hand; it is a plugin,
not an R package, so R-specific gates don't apply.

## Milestones

_Released 1.0.0 2026-07-16 (tag v1.0.0)._

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
| M72 | Collaboration boundary — what survives a merge outside cairn, plus PR-bound approval (D-043) | done | — | high | milestones/archive/M72-collaboration-boundary.md |
| M73 | External-PR intake — /hotfix adopts a PR it did not author | done | M72 | high | milestones/archive/M73-external-pr-intake.md |
| M74 | Issue triage — /milestone enumerates untriaged inboxes into candidate rows | review | M73 | normal | milestones/M74-issue-triage.md |
| M71 | Idea-capture intake gate — out-of-band ideas also land as candidates (D-042) | done | — | high | milestones/archive/M71-idea-capture-intake-gate.md |
| M70 | Docker-image toolchain profile — fourth profile for pure-image repos | done | — | normal | milestones/archive/M70-docker-image-profile.md |
| M69 | Cap-overrun diagnostic — per-section breakdown + single-pass compression discipline | done | — | normal | milestones/archive/M69-cap-overrun-diagnostic.md |

## Candidates

_Ordered higher-priority-first (advisory only — candidates carry no Priority field). Triage: D-027._

- `leave` as a fourth issue disposition is skill-only doctrine: M74's `/milestone` §3 offers candidate row / `/hotfix` / `/milestone-plan` / **leave**, but the rulebook's Intake enumeration (`tracking-rules.md:200`) says only "Issues → `candidate` rows or the hotfix path", so an acknowledged-but-left item persists with the GitHub issue as its only record — which sits awkwardly beside D-042's "an inbox feeds the ROADMAP, it never substitutes for it"; needs a rulebook line legitimizing `leave` (probably narrowed to noise/duplicates/already-cross-referenced) or a narrowing of the skill — swept: no existing row or D-entry covers it — added 2026-07-18 — M74 review F5 (40, sub-threshold; AC3 named `leave`, so review declined to reinterpret the criterion)
- Concurrent-cairn-operator hardening: if two people ever run cairn in the same repo at once the tracking files race — milestone IDs and D-numbers are model-picked with no allocator, duplicate D-numbers auto-merge and validate GREEN (`cairn_validate.py:500-506` uses a `set`), `/milestone-plan` commits to the default branch with no fetch/pull at any step, and `check_single_in_progress` (`cairn_validate.py:61-64`) is a hard FAIL two operators trip by construction; cheapest standalone piece is a `check_d_uniqueness`; swept: no existing row or D-entry covers it — promote if a second cairn operator actually appears — added 2026-07-18 — M72 Out (D-043)
- Doc surfaces still describe the pre-M73 `/hotfix` trigger: `DESIGN.md:68-70` Conventions says `/hotfix` "auto-triggers on bug reports" and README's `/hotfix` row (`:118`) plus the "Contributions come in through you" bullet (`:194`) predate the PR door, so a reader consulting DESIGN as the architecture authority still concludes an incoming PR has no entry point — swept: no existing row or D-entry covers it; both files were out of M73's Scope In (scored 35, sub-threshold) — added 2026-07-18 — M73 review F5 — ABSORBED into M74 (plan amendment 2026-07-18, AC6/T4); graduates at M74 completion, not now (M35)
- MCP-matcher semantics in `references/claude-code-hooks.md`: the reference's Matchers section never mentions MCP tool names, so the M71 T1 finding (a word-chars-only matcher is an EXACT-string compare, hence the regex form) survives only in a work log that compresses at archive — swept: no existing row or D-entry covers it; the M19/D-017 precedent put its T1 finding in this same file — added 2026-07-18 — M71 review F3 (63)
- Budget-first drafting (cap prevention): up-front per-section line budgets in the milestone template/rulebook so first drafts land under the 150-line cap by construction, rather than compressing after — reassess once M69's diagnostic + single-pass discipline is in use and we can see whether the cure suffices — added 2026-07-17 — M69 Out
- Content-gated memory guard: make M19's memory-boundary hook inspect the write and fire only on durable-state signals (decisions, conventions, project facts), staying silent on pure per-user prefs; promote only if the unconditional soft nudge proves too noisy — added 2026-07-11 — M19 Out
- Contributor-facing scaffold: cairn ships nothing a repo can hand an outsider — no CONTRIBUTING, PR template, or issue template (`git ls-files` matches zero; there is no `.github/` in this repo), so a contributor learns the branch/commit/tracking conventions only by being told; would be a `/cairn-init` opt-in, not a core scaffold addition — promote once M72's README subsection is in use and proves insufficient — added 2026-07-18 — M72 Out
- Branch-protection compatibility: cairn structurally requires direct pushes to the default branch (`tracking-rules.md:248-252` docs-only commits; `/milestone-review`'s post-merge hygiene pass), which a repo protecting its default branch behind required PRs cannot do — needs a decision on whether hygiene commits get their own PR or the rule gains a protected-branch mode — promote if an adopting repo turns on branch protection — added 2026-07-18 — M72 Out
- Scaffold-spec version stamp / content-drift detection (Direction 2, deferred from M24): M24 detects *missing* §1 pieces but not a piece whose template *body* changed while the file still exists; stamp a scaffold-spec version into the adopted CLAUDE.md and compare against the plugin's current spec to catch content drift — needs a maintained spec version + changelog + a definition of "what counts as a bump"; promote only if content drift (as opposed to missing files) actually bites — added 2026-07-12 — M24 Out
