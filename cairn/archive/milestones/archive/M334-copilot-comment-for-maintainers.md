# M334: Say only what maintainers need in a Copilot comment

**Status:** done (2026-11-05, PR #349 https://github.com/jmgirard/cairn/pull/349)

**Goal:** A Copilot comment says only what the maintainers need to know, written to them, and goes out only when they need something.

**Outcome:** `skills/shared/copilot-review.md` §5 replaces the rules on naming notes, shas, and reasons with a reader's test: would a maintainer reading the PR act differently, or be misled, without the sentence? When no sentence passes, under the same conditions as a comment, the review gets no comment and its threads resolve. A guest round and `/copilot-review` show this and each note's disposition in the draft chip, and a draft chip also offers to resolve with no comment. A typed comment posts with or without a draft, and a typed instruction changes or writes the draft. §6 reports `copilot: <url> — no comment` and keeps the sha in its own record. A body finding with no anchor stays a note, and each later run decides it again. The skills, README, DESIGN, CHANGELOG, and guards follow. The guest limit on bot replies stays as a ceiling.

**Decisions:** D-239 (supersedes D-236's naming clauses, D-212's "one public record" and "its outcome lives in the review's comment", and D-187's summary comment where they require a comment; extends D-235's chip). The user chose no comment over one always-posted sentence at the plan question set.

**Review:** Full criteria audit at plan: 9 findings, fixed but for one answered. Claim audit: about 60 claims read, 8 corrected. Four fresh reviewers on one pass, no return: 30 findings, 12 fixed, 4 follow-up, 14 rejected (2 edge: a failed resolve call, a stale temp file). Copilot: 1 fixed, 2 rejected, no comment on the PR. New parked rows: "Keep Copilot body outcomes across runs", "Flag people's replies on Copilot threads". Lessons: no capture at the 25-lesson limit, marked 2026-11-02 (M332) and 2026-11-02 (M331) used.
