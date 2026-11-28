# M141: README plain-language pass

**Status:** done (2026-08-14, PR #141 https://github.com/jmgirard/cairn/pull/141)

**Goal:** README.md reads as plain prose, the em-dash tic and machine-styled
constructions removed, with commands, guarded claims, and structure intact.

**Outcome:** em dashes 50 → 1 (the frozen tree block's), companion
double-hyphen and en-dash count 0, 265 lines; all four fenced blocks and ten
headings byte-identical to edb6942; zero guard changes — every pinned phrase
kept on its own physical line. A one-pass fresh reader reported 48
machine-styled constructions: 19 rewritten, 30 kept instances with recorded
reasons (R13 dual), the ledger arithmetic machine-checked after a returned
double-count.

**Decisions:** milestone-local only — the AC5 disposition ledger and its two
appended corrections (R3 kept; R13 dual; all 48 ids dispositioned).

**Review:** two passes, one defect return (F2/95, ledger arithmetic); F1/82
(meaning inversion) and F4/87 (deleted no-lock-in guarantees) fixed in the
same repair and verified by a fresh [O] verifier; 8 findings logged sub-80.
Nothing graduated or retired.
