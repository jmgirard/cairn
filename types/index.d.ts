// The cairn plugin's `$.state` contract: the values its hooks module keeps
// for the session. `claude plugin validate` holds the module to it.

// One active milestone. The counts and next items are null when its
// milestone path is not a readable regular file; a next item is also null
// when its section holds no open box.
export type CairnBandRow = {
  id: string
  title: string
  status: string
  tasksChecked: number | null
  tasksTotal: number | null
  criteriaChecked: number | null
  criteriaTotal: number | null
  nextTask: string | null
  nextCriterion: string | null
}

// A planned milestone whose dependencies are all done.
export type CairnWorkableRow = { id: string; title: string }

// The active milestones in ROADMAP order, the workable planned milestones
// by priority and then id, and the repo root of the last read, null when no
// ROADMAP was found or the working directory could not be read (M210).
export type CairnBandState = { rows: CairnBandRow[]; workable: CairnWorkableRow[]; root: string | null }

// One active milestone's id and status, as the close button stores them.
export type CairnBandMark = { id: string; status: string }

// What the close button stores at a press: the active ids and statuses in
// ROADMAP order, `milestone-review` while that skill runs and moves the band
// to another row, else null, and the idle row's id while no row is active
// (M206). A step stored before a reload that names a skill the cairn list
// has since dropped reads as no step (M200).
export type CairnBandHidden = { marks: CairnBandMark[]; skill: string | null; idle: string | null }

// The running cairn skill's bare name (`milestone-plan`). A main-loop Stop
// with no background work in flight, or a prompt the operator types while
// the session is idle, ends it (M201).
export type CairnStep = { skill: string }

// One checkbox item of a milestone file's Tasks or Acceptance criteria,
// less its box, with a wrapped item's lines joined (M205).
export type CairnPaneItem = { text: string; checked: boolean }

// One active milestone as the cairn pane shows it. `file` is null when the
// milestone file is missing or its read fails; `log` holds the newest five
// work-log lines, less their `- `, which the pane has not drawn since M286.
export type CairnPaneMilestone = {
  id: string
  title: string
  status: string
  file: { goal: string; tasks: CairnPaneItem[]; criteria: CairnPaneItem[]; log: string[] } | null
}

// What the cairn pane shows (M205): `found` is false when no ROADMAP is
// found. `next` is `recommend` in scripts/cairn_next.py, its `id` null for
// planning and its `title` the short title `highTitle` names while
// planning (the first `[high]` candidate row no counted started token
// names, every `#` token counted), else null (M272, M273); the band's Plan
// press picks its own row (`nextTitle`), and since M305 the pane's Next
// line names none. `waiting` is its `waiting`, each row's undone dependencies
// as written with their status. `candidates` holds the ROADMAP's candidate
// rows, each its priority, its short title (the text before its first
// `: `, else before its first ` — `, else all of it; M207, M251), and its
// whole text after the priority token, trimmed (M293).
// `blocked` holds the `blocked` rows in ROADMAP order, each with the number
// of the pull request its milestone file's `Branch/PR` header names, or
// null (M223), and that pull request's URL up to its number, or null (M224).
// `archived` is true when the row's file is gone and its one archive file
// reads done, the number and URL then read from its Status paragraph (M246).
// `taken` holds each candidate row's ` — started <ref>` token with the row's
// short title: an `M<NNN>` token only while the table holds that id as
// `planned` or `blocked`, and every `#<n>` token (M258).
export type CairnPaneState = {
  found: boolean
  milestones: CairnPaneMilestone[]
  next: { action: string; command: string; id: string | null; title: string | null } | null
  workable: CairnWorkableRow[]
  waiting: { id: string; title: string; unmet: string[] }[]
  // `parked`: a row whose promotion condition has not held (M284).
  candidates: { priority: 'high' | 'normal' | 'low' | 'parked'; title: string; text: string }[]
  blocked: { id: string; title: string; pr: number | null; url: string | null; archived: boolean }[]
  taken: { title: string; ref: string }[]
}

// The state word of a blocked milestone's pull request, as the pane last
// read it from `gh api graphql`, or from `gh pr view` for a URL on another
// host (M224, M237).
export type CairnPrWord = 'merged' | 'closed' | 'changes requested' | 'approved' | 'in review' | 'unknown'

// An open pull request's merge state, from GitHub's `mergeable` field
// (M301): MERGEABLE reads `mergeable` and CONFLICTING reads `conflicts`.
export type CairnPrMerge = 'mergeable' | 'conflicts'

// One read of a blocked milestone's pull request: its state word (M224),
// and for an open one, its review threads not marked resolved (M225, M236).
// `counts` is null for a pull request that is not open, or whose threads
// failed the shape check (M237). `mergeable` is null for a pull request
// that is not open, or whose `mergeable` is UNKNOWN, another value, or
// absent (M301).
export type CairnPrRead = { word: CairnPrWord; counts: { unresolved: number } | null; mergeable: CairnPrMerge | null }

// One open pull request that the operator opened from a `hotfix-*` branch,
// as `gh pr list` gave it (M226).
export type CairnHotfixPr = { number: number; title: string; url: string }

// One `Candidate row: <short title>` line of an open pull request's body,
// with that pull request's number, from any head branch (M252).
export type CairnStartedRow = { title: string; number: number }

// The hotfix list that the last read wrote, and the repo root it is for
// (M226): a good `gh pr list` read's result, the list kept after a failed
// call in the same root, or empty when no call ran or the kept list was
// for another root. `root` is null before any read and when no ROADMAP
// root was known. `started` holds the same read's candidate rows that the
// listed bodies name, kept and emptied with `prs` (M252).
export type CairnHotfixRead = { root: string | null; prs: CairnHotfixPr[]; started: CairnStartedRow[] }

// The summary card's numbers (M286): the base remote repo's open pull
// requests and open issues, and the milestones done since the latest
// release tag, with the whole days since that tag's commit. `counts` is null
// until a read for `root` gives numbers, and a read that gives none keeps
// the last good ones for the same root. `done` is the last read's, null
// when that read could not count. `name` is the project name the last read
// for `root` found (M291), null only with no root, and '' for a root with
// no folder name, such as `/`. The shape moved to
// `repo-2` with `days`, and to `repo-3` with `name`.
export type CairnRepoCounts = { prs: number; issues: number }
export type CairnRepoDone = { tag: string; days: number; count: number }
export type CairnRepoRead = {
  root: string | null
  counts: CairnRepoCounts | null
  done: CairnRepoDone | null
  name: string | null
}

declare module 'claude-code' {
  interface PluginState {
    // Each value is kept under a shape tag (register.tsx), so a value an
    // older layout wrote reads as absent after a reload. `dismissed` is
    // null while the band shows, and `step` is null while no cairn skill
    // runs.
    cairn: {
      band: Shaped<CairnBandState>
      dismissed: Shaped<CairnBandHidden | null>
      step: Shaped<CairnStep | null>
      // True from a cairn skill's prompt until the next prompt, Stop, turn
      // end, or session end (M201).
      expanded: Shaped<boolean>
      // True from a Stop that ends a cairn skill's step until the next idle
      // typed prompt that enters, cairn skill, or session end. A row that
      // draws the action Buttons then carries the Clear Button too, when it
      // has room (M216).
      ended: Shaped<boolean>
      // What the cairn pane shows, written at each refresh (M205).
      pane: Shaped<CairnPaneState>
      // Each blocked milestone's pull request state word, its counts, and
      // its merge state, by its URL, as the last read at a pane open or a
      // Refresh press found them (M224, M225, M301). A URL with no entry has
      // not been read.
      prs: Shaped<Record<string, CairnPrRead>>
      // The open hotfix pull requests and the repo root they are for, as
      // the last read at a pane open or a Refresh press wrote them (M226).
      // Their words and counts sit in `prs` by URL.
      hotfixes: Shaped<CairnHotfixRead>
      // The summary card's numbers, written by the same read (M286).
      repo: Shaped<CairnRepoRead>
      // True from the start of a read of the pull request states until the
      // newest read started has settled, while the pane's ↻ Button reads ⋯
      // (M236).
      reading: Shaped<boolean>
    }
  }
}
