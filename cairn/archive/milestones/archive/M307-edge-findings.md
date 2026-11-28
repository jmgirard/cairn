# M307: Reject review findings that only unusual inputs reach

**Status:** done (2026-10-21, PR #321 https://github.com/jmgirard/cairn/pull/321)

**Goal:** `/milestone-review` rejects a real finding that only an unusual input reaches and that gives no wrong result.

**Outcome:** `/milestone-review` step 5 gains a fourth reject ground, `edge`, in owner and guest mode. It covers a real defect the diff adds that only input outside both documented and common use reaches, whose effect is an error, a warning, or slow running. The reason names the input and the use. A finding is never `edge` when it gives a wrong result with no error or warning, shows an acceptance criterion failing or wrong, authorizes an outward-facing irreversible action, or is a human's request in the PR conversation. An `edge` defect is not load-bearing for the return floor. The Review-line format names the ground, and step 7 shows each `edge` reject verbatim. At the user's request at review, step 8's guest arm lists the reviewer `edge` rejects in plain words before any `Closes`/`Refs` lines of a new PR body and asks the maintainers whether they want those inputs handled. On an open PR, one PR comment carries the list for that review pass and the close block names it. README's "Ship it" paragraph and CHANGELOG follow. The trigger was maintainer review on easystats datawizard #730 and #726 and bayestestR #794.

**Decisions:** D-205 records the ground. D-206 corrects four of its clauses, annotates D-144, and records the guest PR-body list. Question set: both modes.

**Review:** Criteria audit at plan (full). Claim audit 7 claims, 2 corrected. One review return for a missing CHANGELOG entry. One substantive amendment (AC4, the user's guest PR-body request), re-audited twice. Two passes of fresh reviewers plus Copilot (Lite, 3 threads): 23 fixed, 10 rejected (one as `edge`), 3 noted, none to a candidate row. Hygiene: M304 row pruned to the terminal cap; no lesson added (LESSONS at its cap); no row graduated or unparked.
