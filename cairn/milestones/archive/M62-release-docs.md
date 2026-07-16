# M62: Release docs — LICENSE, README worked example + framing, DRAFT removal — done 2026-07-16

**Goal:** Make the repo publicly presentable for v1.0: MIT LICENSE, a README
with a worked example and the governed-LLM-Wiki framing, DRAFT_2.md removed.

**Outcome:** MIT LICENSE (Jeffrey Girard, 2026). README: LLM-Wiki framing in
¶1 (M56 verdict, references/llm-wiki.md), a fictional-CLI worked example
walking one milestone through the three gates, chips-are-stops +
guard-backed merge-approval wording, a no-lock-in bail-out bullet
(pause/drop/uninstall), and the status ¶ off piloting/DRAFT framing (no
version claims — CHANGELOG pointer). DRAFT_2.md (1,146 lines) deleted after
a skim found one true gap, ported to DESIGN Conventions (repos never pin
plugin versions; breaking state-format changes ship with /cairn-init
migration handling); DESIGN's "content moves here" promise sentence
reworded. Guard: test_readme_carries_the_llm_wiki_framing + two mutation
entries.

**Decisions (gate):** AC5 amended to exempt tracking lines recording the
removal (the grep otherwise hits its own record); worked example = fictional
generic repo; DRAFT_2 disposition = skim + port true gaps only.

**Review:** 6/6 criteria with fresh evidence; cairn_validate exit 0; three
lenses (diff-bug, blame-history, prior-PR) — zero findings; scorer no-op.
PR: https://github.com/jmgirard/cairn/pull/60
