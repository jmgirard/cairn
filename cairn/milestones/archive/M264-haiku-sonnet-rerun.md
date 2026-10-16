# M264: Re-test Haiku 5.5 against Sonnet 5.5 on search and history review, three runs each

**Status:** done (2026-10-16, PR #276 https://github.com/jmgirard/cairn/pull/276)

**Goal:** A committed note gives the search and history-review role groups a Haiku-or-Sonnet verdict from three runs per task and model, in place of M228's single runs.

**Outcome:** `cairn/references/haiku-sonnet-rerun.md` replays M228's S1 to S3 and H1 to H3 three times on each model (36 foreground runs, `effort` unset, search in `git archive c023018` copies), with one Opus judge per history task and run index under random labels. Costs use M228's method and are lower bounds. Verdicts: search `stay` (Haiku 2.00 against 2.89; every Haiku S2 run dropped `.py`, which the S2 prompt's wording can explain), history review `move` (12 judged-valid findings against 13, ratio 0.92, a one-finding margin; Haiku at 32% of the cost, which the output undercount can reverse). It does not test missed findings. No rule changed. INDEX line, shipped-page ledger pin (`ok`), and a pointer from `haiku-sonnet-roles.md`.

**Decisions:** none. Question set: the Haiku re-test, three runs per task and model. Plan gate chose fresh Sonnet runs, M228's prompts verbatim, and a new note.

**Review:** No returns. Criteria audit (reduced): 0 findings. Three lenses: 16 fixed (a 64-row per-finding table, score ranges, a flip column, the S2 prompt and undercount caveats, M228's judge-disagreement caveat, a misread S3 miss, dates), 2 rejected. Copilot (Lite): 1 fixed. The candidate row "Haiku for the remaining Sonnet roles" narrowed to the open rule choice. No lesson captured; nothing retired.
