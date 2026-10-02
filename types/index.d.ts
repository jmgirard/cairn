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

// The active milestones in ROADMAP order, and the workable planned
// milestones by priority and then id.
export type CairnBandState = { rows: CairnBandRow[]; workable: CairnWorkableRow[] }

// One active milestone's id and status, as the close button stores them.
export type CairnBandMark = { id: string; status: string }

// What the close button stores at a press: the active ids and statuses in
// ROADMAP order, and the running cairn skill's bare name, or null.
export type CairnBandHidden = { marks: CairnBandMark[]; skill: string | null }

// The running cairn skill's bare name (`milestone-plan`), and the title of
// the last chapter the main loop marked since its prompt was expanded.
export type CairnStep = { skill: string; chapter: string | null }

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
    }
  }
}
