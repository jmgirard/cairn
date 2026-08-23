# M80: References-page authoring — the ingestion trigger and the synthesis-note template

**Status:** done · **PR:** https://github.com/jmgirard/cairn/pull/78 · **Depends on:** —

**Goal.** Make authoring a `cairn/references/` page a triggered act with a template for either page type, instead of a recipe only numeric sessions ever meet.

**Outcome.** `tracking-rules.md` "References pages" gains a **When a page is owed** rule — a page is owed once the repo *relies* on a source, and an analysis that will outlive its milestone is a synthesis note — and names both shipped template paths for the first time. Ships `skills/shared/templates/synthesis-note.md`, drawn from the six synthesis pages already here; cairn had named that page type at M57 and enforced it since, with no way to author one. The trigger went into core, not the numeric-gated module: D-031 was upheld, not superseded, so no per-skill read directive was added.

**Origin.** Gaps 1+2 of the M78/M79 grouped candidate, promoted ahead of its "once M78's template is in use" gate — the gate was self-blocking, since nothing triggered the template's use and that was gap 1. Gap 3 → M81.

**Amendments (both gated).** AC3 reworded at implement: it required the shipped template *itself* to pass the checkers, which `YYYY-MM-DD` placeholders make impossible — it now instantiates, as an author would. AC4 amended at review: it named `README.md` a template inventory, but README lists no templates; corrected rather than reinterpreted.

**Scope grew once, deliberately.** AC7 folded in at the implement gate after the new pairing test proved M78's `source-note.md` template emits a page that fails the dated-extraction guard M78 shipped in the same milestone — this repo's 16 pages comply only because M78's review fixed the *pages* by hand (F3/90) and never the generator. Every adopter authoring a source note produced a page their own validator rejects.

**Review.** All 7 criteria evidenced, two differentially against `main` (the three rulebook anchors absent there; `main`'s source-note template proven to fail). Blame-history and prior-PR lenses: no findings. Diff-bug lens: four, all fixed — F2/83 (guard-mechanics note left in body prose, so every authored page would commit a sentence about a test guard), F4/80 (the AC4 defect above), and two sub-threshold actioned under the M73 read-every-sub-80 rule: F1/76 (source-note's header still routed synthesis notes into itself, in a file this milestone edited) and F3/65 (the `extraction:` field anchor was false coverage — the phrase also occurs in the file's own comment header, so deleting the real field left the guard green; closure proven by mutation). Nothing logged-and-dropped. skills 337, scripts 128, hooks 72, each exit 0; `cairn_validate` exit 0.
