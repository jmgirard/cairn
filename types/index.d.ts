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
// by priority and then id, and the repo root the rows came from, null when
// no ROADMAP was found (M210).
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
export type CairnPaneState = {
  found: boolean
  milestones: CairnPaneMilestone[]
  next: { action: string; command: string; id: string | null } | null
  workable: CairnWorkableRow[]
  waiting: { id: string; title: string; unmet: string[] }[]
  candidates: { priority: 'high' | 'normal' | 'low'; title: string }[]
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
      // What the cairn pane shows, written at each refresh (M205).
      pane: Shaped<CairnPaneState>
    }
  }
}
