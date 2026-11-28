# M203: Record review findings in fixed formats

**Status:** done (2026-10-03, PR #210 https://github.com/jmgirard/cairn/pull/210)

**Goal:** Review records each finding and the reviewers each pass spawned in fixed line formats, and the up-front merge approval tried on this branch is removed, so the merge question stays the only gate for a milestone merge.

**Outcome:** The first cut let the plan question set approve a merge. Route-back cases kept that approval, and the merge guard read a `Merge approval:` header slot. After the review returns and two thrash stops, the user chose removal. The re-cut restored main's text in the hooks, the shared rulebook and templates, the plan skill, CLAUDE.md, README, and DESIGN, so IP1 is unchanged. Review step 5 now logs each finding as `<lens> #<rank>: <finding> — <disposition>`. The slugs are `diff-bug`, `blame-history`, and `prior-review`. A reject names its ground, and a fix-now line gains `, fixed <sha>`. Each pass that spawns reviewers writes one `spawned:` Review line, and a degraded pass writes none. Step 7 writes `step-7 decline:` on a decline. It counts amendments from lines that open with `substantive amendment:` or `amendment return:`. Implement step 6 writes the `substantive amendment:` prefix after the date. There is one CHANGELOG entry. RB15, RR15, RB16, and RR16 stay in the review archive.

**Decisions:** D-147 removes the up-front approval and supersedes D-145 and D-146, which stay as history.

**Review:** The first cut took four defect returns and an AC5 amendment return. The re-cut passed on its first review: three lenses with 21 findings. Ten were fixed on the branch, among them an amendment count that matched quoted prefixes and the D-147 lapse list. Ten were rejected with reasons. One, a double-written `amendment return:` line, went to the "Run edge cases" row. The M72 merge-guard lesson was corrected. No lesson was retired or graduated.
