# M50: Greenfield init opener flow — done 2026-07-13

**Goal:** give `cairn-init` a greenfield flow for new/empty repos.
**PR:** #48 (squash-merged). **Principles:** IP3, GP3 (worked under, not changed).

**Outcome:** In a new/empty repo (no profile inferable from source), `cairn-init`
now presents a **project-type chip** to select the toolchain profile, then asks a
two-layer opener set — a **universal layer** (distribution ambition rendered per
profile; a universal numeric-work-needs-oracle-verification question, D-024/D-025)
plus the selected profile's **language-specific slot openers** — landing each
answer in a durable home (DESIGN Purpose & Scope / Conventions / a PROFILE slot).
An **undecided** answer takes a marked reversible default and banks one ROADMAP
`candidate` row (IP3 conservation). The flow stays **tracking-only** — no package
skeleton — surfacing the skeleton as the adopting repo's first milestone, and
stays bounded distinct from `/design-interview` (toolchain-config only). The three
shipped profiles' `greenfield-openers` slots (M45 placeholders) are filled:
r-package → compiled-code; python → typing-strictness + `src/`-vs-flat; generic →
"universal layer is the whole flow". +6 guards (`TestGreenfieldOpeners`,
`TestGreenfieldInitFlow`).

**Key decisions (plan gate):** trigger = empty/new repo only; universal opener
layer + profile openers (oracle-on universal); undecided ⇒ reversible default +
candidate row; evidence = prose-guards + dry-run (interactive rounds
non-automatable). **Review:** F2 (score 80) fixed — the legacy §1 DESIGN-fill
bullet is now greenfield-scoped (extend opener-seeded sections); F1 (20) logged.
