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

declare module 'claude-code' {
  interface PluginState {
    cairn: { band: CairnBandRow[] }
  }
}
