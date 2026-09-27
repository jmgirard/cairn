# prompting-opus-5-5 — Anthropic's model-specific prompting guide for Claude Opus 5.5

**Provenance.** Ingested 2026-09-27 by M189 from
https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
— retrieved by the implementing session as raw Markdown (`curl -L` of the
page's `.md` sibling, HTTP 200, 28,306 bytes), saved on the gitignored shelf as
`cairn/references/sources/prompting-opus-5-5.md`, not through a summarizing
fetch.
Pagination: — (a single unpaginated web page; values below anchor on its `##`
section headings).
Extraction: verified 2026-09-27 — full page read directly from the shelf copy; every quotation below found in it by a whitespace-collapsed fixed-string match run by M189's T1 — observed 2026-09-27.

**Citation.** Anthropic. *Prompting Claude Opus 5.5*. Claude Platform Docs,
`build-with-claude/prompt-engineering/prompting-claude-opus-5-5`. Subtitle as
printed: "Behavioral differences from Claude Opus 5 and the prompting and
harness patterns that address them: effort calibration, thinking behavior in
API integrations and chat, progress updates, unattended and multiagent tasks,
safeguard refusals, frontend design, complex visual inputs, multi-app
workflows, and pasted text in user messages." No author, date, or version is
printed on the page.

**Role.** cairn's skills and rulebook are prompts executed by the Opus tier
(`tracking-rules.md` "Model and agent strategy"), so this guide is first-party
evidence about how the successor to the model `prompting-opus-5.md` describes
reads them. It is here to settle one conduct question cairn had no rule for —
which turn endings between gates stop work that is still owed — and to
re-scale the effort notes against a model whose `medium` is a different amount
of thinking. It is a guidance source, not a numeric one: nothing here is an
oracle.

Disposition of the shelf copy's twelve `##` sections (M189 plan gate,
2026-09-27; the domain is `grep '^## '` over the shelf copy):

1. § Capabilities relevant to prompting — not adopted: capability claims with
   no cairn rule surface; its `medium`-versus-`high` comparison is the
   § Calibrate effort claim quoted below.
2. § Calibrate effort — adopted as a dated observation in
   `cairn/references/effort-experiment-notes.md` (Open questions), no rule:
   effort is a user session setting, not a plugin surface.
3. § Prompts written for thinking disabled — not adopted: cairn's sessions run
   under the Claude Code harness with thinking on; no cairn surface.
4. § Unattended agentic runs — adopted as the early-stop bullet in
   `skills/shared/tracking-rules.md` "Question gates and phase closes"; the
   sample paragraph's same-message status-note clause is not imported (it
   conflicts with the Mandated-substance rule), and its harness-side
   continuation loop is the harness's, not the plugin's.
5. § Safeguard refusals — not adopted: API-level classifier behavior with no
   cairn surface.
6. § User-facing progress updates — already covered: lever three (a statement
   of intent before the first tool call, a recap at the end) is the
   narration-cadence guidance `prompting-opus-5.md` traces to the "Deltas, not
   dumps" and "Plain style" bullets (M152); levers one, two, and four are
   harness-side, and the Claude Code harness applies the progress reminder
   itself.
7. § Explore context in multi-app workflows — not adopted: every cairn skill
   states its own session-start reading list; there is no multi-app surface.
8. § Time signals for multiagent harnesses — not adopted (plan gate): cairn's
   fan-outs are small and its reviewers exist to verify, which the guide's own
   caveat says the sentence trades away.
9. § Thinking instructions in chat system prompts — not adopted: cairn carries
   no thinking instruction, and the guide itself excludes the "treat earlier
   answers as settled" instruction from agentic tasks.
10. § Mark pasted text in user messages — already covered by the Claude Code
    harness, whose system prompt carries the guide's `<pasted_content>` note.
11. § Tools for complex visual inputs — not adopted: no cairn surface.
12. § Frontend design defaults — not adopted: no cairn surface.

## Extracted values

Every value carries its `##` section anchor. Values that must be exact are
quoted verbatim, in quotation marks, rather than paraphrased:

- The Opus 5 patterns still apply — "Existing Claude Opus 5 prompts should
  perform well without changes, and the patterns in" the Opus 5 guide (a link
  in the page text, its title the link's label) "remain a reasonable starting
  point." — page introduction, the paragraph before the section list.
- The new effort default — "Start at `medium`, the default on Claude Opus 5.5
  (Claude Opus 5 defaults to `high`), set it explicitly, and test several
  levels against your own evals rather than carrying over the setting you used
  on Claude Opus 5." — § Calibrate effort.
- Effort names do not carry across models — "Effort level names don't
  correspond to the same amount of thinking across models: in Anthropic's
  testing, Claude Opus 5.5 at `medium` matches or exceeds Claude Opus 5 at
  `high` on coding and knowledge-work evaluations, and on several coding
  evaluations `low` comes close to it at much lower cost." — § Calibrate
  effort.
- The behavior the early-stop instruction answers — "On long tasks with
  several parts, Claude Opus 5.5 keeps the user updated as it works, and some
  of those updates end the turn with text rather than a tool call" —
  § Unattended agentic runs.
- What the model responds to — "Claude Opus 5.5 is responsive to
  instructions that name the specific kinds of early stop you want it to
  avoid, such as ending the turn with a summary that announces the next step
  instead of taking it. It also helps to name the stops you do want, for
  example when no work can advance without the user's input." — § Unattended
  agentic runs.
- The four unwanted turn endings, from the sample paragraph — "One: a long
  summary of what was done that closes by announcing the next step and has no
  tool call, so the next thing never starts. Two: an offer to carry on with
  something unless the user would prefer otherwise, which stops to wait for
  an answer the user was not going to give. Three: a list of decisions for the
  user when, by your own account, none of them blocks the rest of the work.
  Four: deciding that this is a good place to report, because the turn has
  been long or a milestone is done." — § Unattended agentic runs.
- The push, from the sample paragraph — "If you notice yourself inviting the
  user to redirect you or offering to wait, delete it and do the next thing."
  — § Unattended agentic runs.
- The wanted-stop sentence, from the sample paragraph — "The stops the user
  does want are the ones where nothing can move without them, or where the
  thing blocking you is deliberately protected from you. This does not
  override the need for confirmation on risky or destructive actions." —
  § Unattended agentic runs.
- The same-message status-note clause, not imported — "Status notes are
  welcome, and so are your recommendations on open decisions, but put them in
  the same message as your next tool call and carry on with whatever does not
  depend on the user's answer." — § Unattended agentic runs.
- The human-in-the-loop caution — "With this addition the model carries on
  where it would otherwise have stopped to check in, so keep your own
  confirmation step for risky or irreversible actions, and leave the addition
  out of human-in-the-loop applications, where someone is there to answer.
  Expect somewhat more tool calls and output tokens per task." — § Unattended
  agentic runs.
- The time-signal claim — "In Anthropic's evaluations of small agent teams on
  research tasks, both signals made teams finish sooner than a single agent
  working without them." — § Time signals for multiagent harnesses.
- The time-signal verification caveat — "Also check answer quality on your
  own tasks, because under time pressure the model might search and verify a
  little less." — § Time signals for multiagent harnesses.
- The settled-answers exclusion — "Leave it out where you want the model to
  keep re-examining its earlier work, for example in long analyses, or in
  agentic tasks where a later step can reveal a mistake in an earlier one." —
  § Thinking instructions in chat system prompts.

## Traces to

What in the repo reads this page. Anchors are bullet titles and section
headings, not line numbers (`prompting-opus-5.md`'s M152 re-verification found
line anchors stale).

- `skills/shared/tracking-rules.md` — the "Between gates, the turn does not
  end while work is still owed" bullet, in Question gates and phase closes
  (M189). Takes the § Unattended agentic runs sample paragraph's four unwanted
  endings, its push, and its wanted-stop test, re-worded to cairn's stops; the
  same-message status-note clause is not taken.
- `cairn/references/prompting-opus-5.md` — the Open questions observation
  (M189) quoting the introduction's "remain a reasonable starting point"
  statement.
- `cairn/references/effort-experiment-notes.md` — the Open questions
  observation (M189) attributing the `medium` default and the
  `medium`-matches-`high` claim to § Calibrate effort.
- `cairn/ROADMAP.md` — the "Reasoning-effort dial per spawned agent" candidate
  row's M189 re-check note cites this page's § Calibrate effort as the reason
  the row's effort vocabulary is read against the new scale.

## Open questions

Claims about the *repo's own state* — what is on the shelf, what has not been
read, what a later task must still check — are dated observations, not
standing facts. Each carries `— observed YYYY-MM-DD` inline.

- The page prints no version or last-updated date, so a later re-verification
  can detect drift only by re-reading the whole page — observed 2026-09-27.
- The guide's linked companion pages (`What's new in Claude Opus 5.5`, the
  migration guide, `Effort` and its "Recommended effort levels for Claude Opus
  5.5" section) are not ingested; the effort values quoted above are this
  page's own statements — observed 2026-09-27.
- The four unwanted endings are quoted from a sample paragraph the guide
  offers as "a starting point" for fully unattended agents; whether cairn's
  between-gate stretches match that setting closely enough for the bullet to
  change turn endings is the plan gate's falsifier (a session skipping a stop
  the rulebook wanted), not yet observed either way — observed 2026-09-27.
