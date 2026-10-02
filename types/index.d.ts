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

// One active milestone's id and status, as the close button stores them.
export type CairnBandMark = { id: string; status: string }

declare module 'claude-code' {
  interface PluginState {
    // `band` is kept under a shape tag (register.tsx), so rows an older
    // layout wrote read as absent after a reload. `dismissed` holds the
    // active ids and statuses, in ROADMAP order, at the last press of the
    // close button, and is null while the band shows.
    cairn: { band: Shaped<CairnBandRow[]>; dismissed: CairnBandMark[] | null }
  }
}
