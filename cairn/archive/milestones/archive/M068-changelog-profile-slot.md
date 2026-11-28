# M68: Changelog profile slot — required seventh slot, "none" legal (archived)

- **Status:** done (merged 2026-07-16, PR https://github.com/jmgirard/cairn/pull/66)
- **Goal:** add `changelog` as a required seventh toolchain-profile slot —
  the repo's changelog file name or "none" — so `/hotfix`, `/cairn-release`,
  and the consistency-gate read one declaration instead of improvising.

**Outcome:** `_REQUIRED_SLOTS`/`SLOTS` grew to seven; all three reference
profiles + this repo's PROFILE.md declare the slot (NEWS.md / CHANGELOG.md /
declare-or-none / CHANGELOG.md); release-walk + consistency-gate bullets
repoint at the declaration; /hotfix step 5 and /cairn-release steps 1–2 read
it ("none" → skip entry / bump from git history; absent PROFILE → infer);
seven-slot sweep across rulebook/DESIGN/file-map. TestChangelogSlot ×5 +
empty-fixture test + 6 mutation registrations. Suites 87/219/55 OK.

**Decisions:** D-040 (required slot, "none" legal, all three consumers;
early promotion past the candidate row's wait-for-next-profile trigger on
the pre-v1.0 schema-freeze argument). Promoted from the RR01 rec 11/Q2 row.

**Review:** 6/6 ACs on fresh evidence; three lenses + scorer — blame-history
and prior-PR clean; diff-bug F1/80 (empty-leg fixture) and F2/87 (hotfix
step-6 "none" carve-out) fixed in-review; F3/75 logged unactioned (generic
slot text names the consistency-gate, which is "none" for generic — doc nit,
candidate-worthy if it misleads).
