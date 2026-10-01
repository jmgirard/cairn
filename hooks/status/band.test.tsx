import { describe, expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { bandLine } from './band'
import { FIXTURES } from './fixtures.gen'

// Each case answers the shipped mod's `$.session.cwd`, `$.fs.stat` and
// `$.fs.read` calls from an in-memory copy of a fixture, keyed by absolute
// path. A plain answer goes back as `{ value }`; a path the copy lacks goes
// on to the bottom of the chain, which rejects, as a missing file does in a
// session. The copy is mutable: an AC3 case edits a file between two turn
// ends, and the second turn end reads the edit.

const SURFACES = ['terminal', 'desktop'] as const
const BAND = {
  component: 'AbovePrompt',
  props: { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 120 },
} as const
let turnCount = 0
function turn() {
  turnCount += 1
  return { answer: '', durationMs: 1, isAborted: false, turnId: `t${turnCount}`, reason: 'answer' as const }
}

type Copy = { cwd: string; files: Record<string, string> }

function copyOf(name: string): Copy {
  const fixture = FIXTURES[name]
  return { cwd: fixture.cwd, files: { ...fixture.files } }
}

// The world beneath the mod: the fixture copy as the session's directory and
// files, and a turn end that answers nothing.
function seat(on: On, copy: Copy) {
  const has = (path: string) => Object.prototype.hasOwnProperty.call(copy.files, path)
  on('session.cwd', async () => ({ value: copy.cwd }))
  on('fs.stat', async ($, e, next) =>
    has(e.path) ? { value: { kind: 'file', size: copy.files[e.path].length, mtimeMs: 0, isLink: false } } : next(e),
  )
  on('fs.read', async ($, e, next) => (has(e.path) ? { value: copy.files[e.path] } : next(e)))
  on('turn.complete', async () => ({ text: '' }))
  // The engine's own drawing of the band slot, which the mod passes to when
  // it has nothing to show.
  on('ui.render', { component: 'AbovePrompt' }, async () => ({ type: 'Text', props: {}, children: [ENGINE] }))
}

const ENGINE = 'engine slot'

// The band's lines as drawn: [ENGINE] when the mod passed to the engine.
async function lines(ui: { findAll: (q: { type: string }) => Promise<{ text: string }[]> }) {
  return (await ui.findAll({ type: 'Text' })).map(t => t.text)
}

describe('band lines for active milestones (AC1)', () => {
  for (const name of ['single-in-progress', 'mixed', 'missing-file', 'subdirectory']) {
    test(`${name}: one line per active row, in ROADMAP order`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      for (const surface of SURFACES) {
        const ui = await $.ui.mount({ plugin: 'cairn', surface, ...BAND })
        expect(await lines(ui)).toEqual(FIXTURES[name].rows.map(bandLine))
        await ui.unmount()
      }
    })
  }

  test('line text names id, title, phase and counts', () => {
    const [m010, m012, m013] = FIXTURES['mixed'].rows
    expect(bandLine(m010)).toBe('M010 Nested tasks and a capital X · review · 3/5 tasks')
    expect(bandLine(m012)).toBe('M012 A Tasks section with no boxes · implement · 0/0 tasks')
    expect(bandLine(m013)).toBe('M013 Capitalized status, file gone · review · no milestone file')
  })

  test('the band yields to a survey', async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await $.turn.complete(turn())
    const ui = await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND, props: { ...BAND.props, hasSurvey: true } })
    expect(await lines(ui)).toEqual([ENGINE])
    await ui.unmount()
  })
})

// A plugin above the mod that draws how the mod's render hook settled, read
// from `next.trace`: `returned` when it settled on a result, here the
// engine's drawing it handed on to, and `skipped` when it threw. A thrown
// hook is skipped and the engine draws, so the drawing alone cannot tell
// the two apart.
const PROBE = {
  name: 'band-probe',
  tier: 'prepend' as const,
  register: on => {
    on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
      const drawn = await next(e)
      const link = next.trace.find(t => t.plugin === 'cairn')
      const { Box, Text } = $.ui.resolve(e)
      return (
        <Box key="band-probe" flexDirection="column">
          <Text>{`cairn hook: ${link ? link.outcome : 'absent'}`}</Text>
          {drawn}
        </Box>
      )
    })
  },
}

describe('the band draws nothing (AC2)', () => {
  for (const name of ['no-roadmap', 'no-active']) {
    test(`${name}: the mod draws nothing, passes to the engine, and does not throw`, { plugins: [PROBE] }, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      for (const surface of SURFACES) {
        const ui = await $.ui.mount({ plugin: 'cairn', surface, ...BAND })
        expect(await lines(ui)).toEqual(['cairn hook: returned', ENGINE])
        await ui.unmount()
      }
    })
  }

  test('a cairn repo with a ROADMAP below the working directory only draws nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    // The ROADMAP sits one level below the working directory, where the
    // upward walk never looks.
    seat(on, { cwd: '/', files: Object.fromEntries(Object.entries(copy.files).map(([k, v]) => [`/below${k}`, v])) })
    await $.turn.complete(turn())
    const ui = await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND })
    expect(await lines(ui)).toEqual([ENGINE])
    await ui.unmount()
  })
})

// Each AC3 case asserts the band at a first turn end, edits the copy, ends
// a second turn, and asserts again.
type Edit = { name: string; fixture: string; edit: (files: Record<string, string>) => void; before: string[]; after: string[] }

const ROADMAP = '/cairn/ROADMAP.md'
const M002 = '/cairn/milestones/M002-export.md'
const EXPORT = 'M002 Add the export command'
const EDITS: Edit[] = [
  {
    name: 'a task gets checked',
    fixture: 'single-in-progress',
    edit: files => {
      files[M002] = files[M002].replace('- [ ] T2:', '- [x] T2:')
    },
    before: [`${EXPORT} · implement · 1/3 tasks`],
    after: [`${EXPORT} · implement · 2/3 tasks`],
  },
  {
    name: 'a row moves from planned to in-progress',
    fixture: 'no-active',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Waiting to start | planned |', '| Waiting to start | in-progress |')
    },
    before: [ENGINE],
    after: ['M021 Waiting to start · implement · 0/1 tasks'],
  },
  {
    name: 'a row moves from in-progress to review',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | review |')
    },
    before: [`${EXPORT} · implement · 1/3 tasks`],
    after: [`${EXPORT} · review · 1/3 tasks`],
  },
  {
    name: 'a row leaves both statuses from review',
    fixture: 'missing-file',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Its file was never written | review |', '| Its file was never written | done |')
    },
    before: ['M004 Its file was never written · review · no milestone file'],
    after: [ENGINE],
  },
  {
    name: 'a row leaves both statuses',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | done |')
    },
    before: [`${EXPORT} · implement · 1/3 tasks`],
    after: [ENGINE],
  },
]

describe('the band follows edits at the next turn end (AC3)', () => {
  for (const { name, fixture, edit, before, after } of EDITS) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        const copy = copyOf(fixture)
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = await $.ui.mount({ plugin: 'cairn', surface, ...BAND })
        expect(await lines(ui)).toEqual(before)
        edit(copy.files)
        await $.turn.complete(turn())
        expect(await lines(ui)).toEqual(after)
        await ui.unmount()
      })
    }
  }
})
