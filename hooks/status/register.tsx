import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import { bandLine } from './band'
import type { BandRow, FileSource } from './reader'
import { loadBand } from './reader'

// The milestone band above the prompt (M191): one line per `in-progress` or
// `review` ROADMAP row, refreshed when the session starts and at the end of
// each turn.

const band = atom({ plugin: 'cairn', key: 'band' } as const, [] as BandRow[])

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const result = await next(e)
    await refresh($)
    return result
  })

  on('turn.complete', async ($, e, next) => {
    const result = await next(e)
    // A subagent's turn ending is not the session's turn ending.
    if (e.agentId === undefined) await refresh($)
    return result
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const rows = await read($, band)
    if (rows.length === 0) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box key="cairn-band" flexDirection="column">
        {rows.map(row => (
          <Text key={row.id} dimColor wrap="truncate-end">
            {bandLine(row)}
          </Text>
        ))}
      </Box>
    )
  })
}

async function refresh($) {
  let rows: BandRow[] = []
  try {
    rows = await loadBand(fsSource($))
  } catch {
    // No readable working directory or ROADMAP: the band is cleared.
    rows = []
  }
  await update($, band, () => rows)
}

function fsSource($): FileSource {
  return {
    cwd: () => $.session.cwd(),
    isFile: path => isFile($, path),
    read: path => readText($, path),
  }
}

async function isFile($, path: string): Promise<boolean> {
  try {
    return (await $.fs.stat(path)).kind === 'file'
  } catch {
    return false
  }
}

async function readText($, path: string): Promise<string | null> {
  try {
    return await $.fs.read(path)
  } catch {
    return null
  }
}
