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
// work-log lines, less their `- `.
export type CairnPaneMilestone = {
  id: string
  title: string
  status: string
  file: { goal: string; tasks: CairnPaneItem[]; criteria: CairnPaneItem[]; log: string[] } | null
}

// What the cairn pane shows (M205): `found` is false when no ROADMAP is
// found. `next` is `recommend` in scripts/cairn_next.py, its `id` null for
// planning, and `waiting` is its `waiting`, each row's undone dependencies
// as written with their status. `candidates` holds the ROADMAP's candidate
// rows, each its priority and the text before its first `: ` (M207).
// `blocked` holds the `blocked` rows in ROADMAP order, each with the number
// of the pull request its milestone file's `Branch/PR` header names, or
// null (M223), and that pull request's URL up to its number, or null (M224).
export type CairnPaneState = {
  found: boolean
  milestones: CairnPaneMilestone[]
  next: { action: string; command: string; id: string | null } | null
  workable: CairnWorkableRow[]
  waiting: { id: string; title: string; unmet: string[] }[]
  candidates: { priority: 'high' | 'normal' | 'low'; title: string }[]
  blocked: { id: string; title: string; pr: number | null; url: string | null }[]
}

// The state word of a blocked milestone's pull request, as the pane last
// read it from `gh pr view` (M224).
export type CairnPrWord = 'merged' | 'closed' | 'changes requested' | 'approved' | 'in review' | 'unknown'

// One read of a blocked milestone's pull request: its state word (M224),
// and for an open one, its review threads not marked resolved (M225, M236).
// `counts` is null for a pull request that is not open, or whose count read
// failed.
export type CairnPrRead = { word: CairnPrWord; counts: { unresolved: number } | null }

// One open pull request that the operator opened from a `hotfix-*` branch,
// as `gh pr list` gave it (M226).
export type CairnHotfixPr = { number: number; title: string; url: string }

// The hotfix list that the last read wrote, and the repo root it is for
// (M226): a good `gh pr list` read's result, the list kept after a failed
// call in the same root, or empty when no call ran or the kept list was
// for another root. `root` is null before any read and when no ROADMAP
// root was known.
export type CairnHotfixRead = { root: string | null; prs: CairnHotfixPr[] }

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
      // Each blocked milestone's pull request state word, and its counts,
      // by its URL, as the last read at a pane open or a Refresh press found
      // them (M224, M225). A URL with no entry has not been read.
      prs: Shaped<Record<string, CairnPrRead>>
      // The open hotfix pull requests and the repo root they are for, as
      // the last read at a pane open or a Refresh press wrote them (M226).
      // Their words and counts sit in `prs` by URL.
      hotfixes: Shaped<CairnHotfixRead>
    }
  }
}
