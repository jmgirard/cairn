// The cairn plugin's `$.state` contract: the values its hooks module keeps
// for the session. `claude plugin validate` holds the module to it.

export type CairnBandRow = {
  id: string
  title: string
  status: string
  checked: number | null
  total: number | null
}

declare module 'claude-code' {
  interface PluginState {
    cairn: { band: CairnBandRow[] }
  }
}
