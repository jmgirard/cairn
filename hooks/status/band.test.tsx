import { describe, expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { bandLines, lineText } from './band'
import { FIXTURES } from './fixtures.gen'

// Each case answers the shipped mod's `$.session.cwd`, `$.fs.stat` and
// `$.fs.read` calls from an in-memory copy of a fixture, keyed by absolute
// path. A plain answer goes back as `{ value }`; a path the copy lacks goes
// on to the bottom of the chain, which rejects, as a missing file does in a
// session. The copy is mutable: an edit case edits a file between two turn
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

function at(bodyColumns: number) {
  return { ...BAND, props: { ...BAND.props, bodyColumns } }
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
  // The engine's own drawing of the band slot, which the mod draws its rows
  // above, or passes to when it has nothing to show.
  on('ui.render', { component: 'AbovePrompt' }, async () => ({ type: 'Text', props: {}, children: [ENGINE] }))
}

const ENGINE = 'engine slot'

// A plugin beneath the mod that draws its own band row and never calls
// `next`. Its register closes over nothing here, so its row text is
// written inside it and restated as BENEATH_ROW.
const BENEATH = {
  name: 'band-beneath',
  tier: 'append' as const,
  register: on => {
    on('ui.render', { component: 'AbovePrompt' }, async ($, e) => {
      const { Box, Text } = $.ui.resolve(e)
      return (
        <Box key="beneath-band">
          <Text>another plugin's band row</Text>
        </Box>
      )
    })
  },
}
const BENEATH_ROW = "another plugin's band row"

// An element as `findAll` returns it, or as it sits in a found element's
// `children`, where its key is in its props.
type Element = { type: string; key?: string; text?: string; props: Record<string, unknown>; children: unknown[] }
type Ui = {
  findAll: (q: { type?: string; key?: string }) => Promise<Element[]>
  press: (q: { key: string }) => Promise<unknown>
  unmount: () => Promise<void>
}

// The text an element shows, its nested Text children included. The close
// Button's label is left out, so a row reads the same on every surface.
function textOf(node: unknown): string {
  if (typeof node === 'string') return node
  if (node === null || typeof node !== 'object') return ''
  if ((node as Element).type === 'Button') return ''
  return ((node as Element).children ?? []).map(textOf).join('')
}

function keyOf(node: Element): string | undefined {
  return node.key ?? (node.props?.key as string | undefined)
}

// The element children of a node, strings left out.
function kids(node: Element): Element[] {
  return (node.children ?? []).filter((c): c is Element => c !== null && typeof c === 'object')
}

// Every element below `node` of the given type, at any depth.
function below(node: unknown, type: string): Element[] {
  if (node === null || typeof node !== 'object') return []
  const el = node as Element
  const rest = (el.children ?? []).flatMap(child => below(child, type))
  return el.type === type ? [el, ...rest] : rest
}

const ROW_KEY = /^M\d+-(header|item)$/

// A row's text with a header row's two groups joined by the right group's
// left margin, the least gap a row draws (a wide row spreads them further),
// with the close button's label and the spaces before it left out.
function rowText(row: Element): string {
  const groups = kids(row)
  if (row.props.justifyContent !== 'space-between' || groups.length !== 2) return textOf(row)
  const [left, right] = groups
  return `${textOf(left)}${' '.repeat(Number(right.props.marginLeft ?? 0))}${textOf(right)}`.trimEnd()
}

// The rows as drawn, top to bottom: each of cairn's header and item rows (a
// keyed Box), then the rows the hooks beneath drew (ENGINE, BENEATH_ROW).
async function lines(ui: Ui): Promise<string[]> {
  const all = await ui.findAll({})
  return all
    .filter(el => (el.type === 'Box' && ROW_KEY.test(el.key ?? '')) || (el.type === 'Text' && [ENGINE, BENEATH_ROW].includes(textOf(el))))
    .map(el => (el.type === 'Box' ? rowText(el) : textOf(el)))
}

// The `cairn-band` Box as found.
async function bandBox(ui: Ui): Promise<Element> {
  const [box] = await ui.findAll({ key: 'cairn-band' })
  expect(box?.type).toBe('Box')
  return box
}

// The Texts inside the `cairn-band` Box.
async function bandTexts(ui: Ui): Promise<Element[]> {
  return below(await bandBox(ui), 'Text')
}

// The keys of the row Boxes inside the `cairn-band` Box.
async function rowKeys(ui: Ui): Promise<string[]> {
  return below(await bandBox(ui), 'Box')
    .map(keyOf)
    .filter((k): k is string => ROW_KEY.test(k ?? ''))
}

// Whether the drawing holds any of cairn's elements.
async function hasCairn(ui: Ui): Promise<boolean> {
  const all = await ui.findAll({})
  return all.some(el => ROW_KEY.test(el.key ?? '') || /^cairn-/.test(el.key ?? ''))
}

async function mountEach(name: string, view: typeof BAND, check: (ui: Ui, surface: string) => Promise<void>, $) {
  for (const surface of SURFACES) {
    const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...view })) as Ui
    await check(ui, surface)
    await ui.unmount()
  }
}

// The rows at 120 columns, written out by hand, never derived from band.ts.
// A header row's two spaces before its bar or label are the right group's
// left margin.
const DRAWN: Record<string, string[]> = {
  'single-in-progress': ['implement M002 Add the export command  ███░░░░░░░  1/3 tasks', '  → T2: Write the command.'],
  mixed: [
    'review    M010 Nested tasks and a capital X  ██████░░░░  2/3 criteria',
    '  → AC3: Third criterion.',
    'implement M012 A Tasks section with no boxes  no tasks',
    'review    M013 Capitalized status, file gone  no milestone file',
    'implement M014 No Tasks section at all  no tasks',
  ],
  'nested-first': [
    'implement M030 The next task is nested  ███░░░░░░░  1/3 tasks',
    '  → T1a: Nested task, open, with extra spaces after the box.',
  ],
  'states-implement': [
    'implement M040 Its file was never written  no milestone file',
    'implement M041 No Tasks section  no tasks',
    'implement M042 A Tasks section with no boxes  no tasks',
    'implement M043 Every task checked  all 3 tasks checked',
  ],
  'states-review': [
    'review    M050 Its file was never written  no milestone file',
    'review    M051 No criteria section  no criteria',
    'review    M052 A criteria section with no boxes  no criteria',
    'review    M053 Every criterion checked  all 2 criteria checked',
  ],
  'missing-file': ['review    M004 Its file was never written  no milestone file'],
  subdirectory: ['implement M007 Started from a subdirectory  all 2 tasks checked'],
  'unlabeled-item': ['implement M062 The next task has no label  ███░░░░░░░  1/3 tasks', '  → Write the docs, with no label.'],
}

describe('a header row per active milestone, and an item row under each with an open box (M193 AC1)', () => {
  for (const name of ['single-in-progress', 'mixed', 'nested-first']) {
    test(`${name}: the rows in ROADMAP order, above the engine's drawing`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      await mountEach(
        name,
        BAND,
        async ui => {
          expect(await lines(ui)).toEqual([...DRAWN[name], ENGINE])
          expect((await bandTexts(ui)).filter(t => t.props.wrap !== 'truncate-end')).toEqual([])
        },
        $,
      )
    })
  }

  test('the hand-written rows match what band.ts builds', () => {
    for (const [name, drawn] of Object.entries(DRAWN)) {
      expect(FIXTURES[name].rows.flatMap(row => bandLines(row, 120)).map(lineText)).toEqual(drawn)
    }
  })

  test('the band yields to a survey', async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND, props: { ...BAND.props, hasSurvey: true } })) as Ui
    expect(await lines(ui)).toEqual([ENGINE])
    await ui.unmount()
  })
})

describe('three states draw the header row alone (M193 AC2)', () => {
  for (const name of ['states-implement', 'states-review', 'missing-file', 'subdirectory']) {
    test(`${name}: header rows only, with no bar and no item row`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      await mountEach(
        name,
        BAND,
        async ui => {
          expect(await lines(ui)).toEqual([...DRAWN[name], ENGINE])
          const keys = await rowKeys(ui)
          expect(keys).toEqual(FIXTURES[name].rows.map(row => `${row.id}-header`))
          expect((await bandTexts(ui)).filter(t => /[█░]/.test(textOf(t)))).toEqual([])
          expect((await bandTexts(ui)).filter(t => t.props.wrap !== 'truncate-end')).toEqual([])
        },
        $,
      )
    })
  }
})

describe('the rows carry style props (M193 AC3)', () => {
  for (const columns of [59, 60, 120]) {
    test(`mixed at ${columns} columns`, async ($, on) => {
      seat(on, copyOf('mixed'))
      await $.turn.complete(turn())
      await mountEach(
        'mixed',
        at(columns),
        async ui => {
          const inBand = await bandTexts(ui)
          // A Text that holds only strings: one span of a row.
          const leaf = (text: string) => inBand.find(t => t.children.every(c => typeof c === 'string') && textOf(t) === text)
          expect(leaf('review   ')?.props.color).toBe('success')
          expect(leaf('implement')?.props.color).toBe('claude')
          expect(leaf('M010')?.props.bold).toBe(true)
          expect(leaf('no milestone file')?.props.color).toBe('warning')
          expect(inBand.length).toBeGreaterThan(10)
          expect(inBand.filter(t => t.props.wrap !== 'truncate-end')).toEqual([])

          const [header] = await ui.findAll({ key: 'M010-header' })
          expect(rowText(header).endsWith('  2/3 criteria')).toBe(true)
          const filled = leaf('██████')
          if (columns < 60) {
            expect(filled).toBeUndefined()
            expect(rowText(header)).toBe('review    M010 Nested tasks and a capital X  2/3 criteria')
          } else {
            expect(filled?.props.color).toBe('success')
            expect(leaf('░░░░')?.props.dimColor).toBe(true)
            expect(rowText(header)).toBe('review    M010 Nested tasks and a capital X  ██████░░░░  2/3 criteria')
          }
        },
        $,
      )
    })
  }
})

// One header row's layout: the row, its two groups, and the title's Text
// and the Box around it.
function layout(header: Element) {
  const groups = kids(header)
  const [left, right] = groups
  const titleBox = below(left, 'Box').find(b => b.props.flexShrink === 1 && kids(b).length === 1 && kids(b)[0].type === 'Text')
  return { groups, left, right, title: titleBox ? kids(titleBox)[0] : undefined }
}

const CLOSE = { terminal: '×', desktop: '×' } as const

describe('each header row is a left and a right group (AC1)', () => {
  for (const columns of [59, 60, 120]) {
    test(`mixed at ${columns} columns`, async ($, on) => {
      seat(on, copyOf('mixed'))
      await $.turn.complete(turn())
      await mountEach(
        'mixed',
        at(columns),
        async ui => {
          const rows = FIXTURES.mixed.rows
          for (const [i, row] of rows.entries()) {
            const [header] = await ui.findAll({ key: `${row.id}-header` })
            expect(header.props.justifyContent).toBe('space-between')
            const { groups, left, right, title } = layout(header)
            expect(groups.map(g => g.type)).toEqual(['Box', 'Box'])
            expect(header.children.length).toBe(2)
            expect(left.props.flexShrink).toBe(1)
            expect(right.props.flexShrink).toBe(0)
            expect(right.props.marginLeft).toBe(2)
            // The left group: the phase label, the id, and the whole title.
            expect(textOf(left)).toBe(`${row.status === 'review' ? 'review   ' : 'implement'} ${row.id} ${row.title}`)
            expect(textOf(title)).toBe(row.title)
            expect(title?.props.wrap).toBe('truncate-end')
            // The right group: the bar at 60 columns or more, and the counts
            // or the state label; the close button last on the first row.
            const hasBar = below(right, 'Text').some(t => /[█░]/.test(textOf(t)))
            expect(hasBar).toBe(row.id === 'M010' && columns >= 60)
            const last = kids(right)[kids(right).length - 1]
            expect(last.type === 'Button').toBe(i === 0)
            if (i === 0) expect(keyOf(last)).toBe('cairn-close')
          }
          const [m013] = await ui.findAll({ key: 'M013-header' })
          expect(textOf(layout(m013).right).trim()).toBe('no milestone file')
        },
        $,
      )
    })
  }

  for (const name of ['long-title', 'wide-title']) {
    test(`${name} at 40 columns: the title Text holds the whole title`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      const [row] = FIXTURES[name].rows
      await mountEach(
        name,
        at(40),
        async ui => {
          const [header] = await ui.findAll({ key: `${row.id}-header` })
          expect(header.props.justifyContent).toBe('space-between')
          const { left, right, title } = layout(header)
          expect(left.props.flexShrink).toBe(1)
          expect(right.props.flexShrink).toBe(0)
          expect(right.props.marginLeft).toBe(2)
          expect(title?.children).toEqual([row.title])
          expect(title?.props.wrap).toBe('truncate-end')
          expect(below(right, 'Text').some(t => /[█░]/.test(textOf(t)))).toBe(false)
          expect(textOf(right).trim()).toBe(name === 'long-title' ? '1/2 tasks' : '1/2 criteria')
          expect(keyOf(kids(right)[kids(right).length - 1])).toBe('cairn-close')
        },
        $,
      )
    })
  }

  test("the wide-title fixture's title holds wide characters and an emoji", () => {
    const [row] = FIXTURES['wide-title'].rows
    expect(row.title).toContain('🚀')
    expect(row.title).toContain('宽字符')
  })
})

// A press hides the band until the active list changes, and that state
// lasts the session, so each surface gets a session of its own.
describe('the close button (AC2)', () => {
  for (const name of ['mixed', 'single-in-progress']) {
    for (const surface of SURFACES) {
      test(`${name}: one dismiss Button, and a press passes to the engine (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await lines(ui)).toEqual([...DRAWN[name], ENGINE])
        const buttons = await ui.findAll({ type: 'Button' })
        expect(buttons.map(keyOf)).toEqual(['cairn-close'])
        const [button] = buttons
        expect(button.props.role).toBe('dismiss')
        expect(button.props.plain).toBe(true)
        expect(button.props.label).toBe(CLOSE[surface])
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        expect(await hasCairn(ui)).toBe(false)
        expect(await ui.findAll({ type: 'Button' })).toEqual([])
        await ui.unmount()
      })
    }
  }

  for (const surface of SURFACES) {
    test(`mixed over a plugin beneath: a press leaves the row the plugin beneath draws (${surface})`, { plugins: [BENEATH] }, async ($, on) => {
      seat(on, copyOf('mixed'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await lines(ui)).toEqual([...DRAWN.mixed, BENEATH_ROW])
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([BENEATH_ROW])
      expect(await hasCairn(ui)).toBe(false)
      await ui.unmount()
    })
  }
})

// The item row's Texts, each with the Texts that enclose it.
function textsIn(node: unknown, outer: Element[] = []): { text: Element; outer: Element[] }[] {
  if (node === null || typeof node !== 'object') return []
  const el = node as Element
  const inner = el.type === 'Text' ? [...outer, el] : outer
  const rest = (el.children ?? []).flatMap(child => textsIn(child, inner))
  return el.type === 'Text' ? [{ text: el, outer }, ...rest] : rest
}

const LABELED: [string, string, string][] = [
  ['mixed', 'M010-item', 'AC3:'],
  ['single-in-progress', 'M002-item', 'T2:'],
  ['nested-first', 'M030-item', 'T1a:'],
]

describe("the item row's label draws bold (AC4)", () => {
  for (const [name, key, label] of LABELED) {
    test(`${name}: ${label} is bold and undimmed, the rest dim`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      await mountEach(
        name,
        BAND,
        async ui => {
          const [item] = await ui.findAll({ key })
          const texts = textsIn(item)
          const found = texts.filter(t => t.text.children.length === 1 && t.text.children[0] === label)
          expect(found.length).toBe(1)
          const [{ text, outer }] = found
          expect(text.props.bold).toBe(true)
          expect([text, ...outer].filter(t => t.props.dimColor)).toEqual([])
          const others = texts.filter(t => t.text !== text && !outer.includes(t.text))
          expect(others.length).toBeGreaterThan(0)
          expect(others.filter(t => t.text.props.dimColor !== true)).toEqual([])
        },
        $,
      )
    })
  }

  test('unlabeled-item: every Text of the item row is dim', async ($, on) => {
    seat(on, copyOf('unlabeled-item'))
    await $.turn.complete(turn())
    await mountEach(
      'unlabeled-item',
      BAND,
      async ui => {
        expect(await lines(ui)).toEqual([...DRAWN['unlabeled-item'], ENGINE])
        const [item] = await ui.findAll({ key: 'M062-item' })
        const texts = textsIn(item)
        expect(texts.length).toBeGreaterThan(0)
        expect(texts.filter(t => t.text.props.dimColor !== true)).toEqual([])
        expect(texts.filter(t => t.text.props.bold)).toEqual([])
      },
      $,
    )
  })
})

// Each edit case asserts the band at a first turn end, edits the copy, ends
// a second turn, and asserts again.
type Edit = { name: string; fixture: string; edit: (files: Record<string, string>) => void; before: string[]; after: string[] }

const ROADMAP = '/cairn/ROADMAP.md'
const M002 = '/cairn/milestones/M002-export.md'
const M030 = '/cairn/milestones/M030-nested.md'
const EXPORT = 'M002 Add the export command'
const EDITS: Edit[] = [
  {
    name: 'a task gets checked',
    fixture: 'single-in-progress',
    edit: files => {
      files[M002] = files[M002].replace('- [ ] T2:', '- [x] T2:')
    },
    before: [`implement ${EXPORT}  ███░░░░░░░  1/3 tasks`, '  → T2: Write the command.', ENGINE],
    after: [`implement ${EXPORT}  ██████░░░░  2/3 tasks`, '  → T3: Write the docs.', ENGINE],
  },
  {
    name: 'a row moves from planned to in-progress',
    fixture: 'no-active',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Waiting to start | planned |', '| Waiting to start | in-progress |')
    },
    before: [ENGINE],
    after: ['implement M021 Waiting to start  ░░░░░░░░░░  0/1 tasks', '  → T1: Not started.', ENGINE],
  },
  {
    name: 'a row moves from in-progress to review, and both rows switch to criteria',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | review |')
    },
    before: [`implement ${EXPORT}  ███░░░░░░░  1/3 tasks`, '  → T2: Write the command.', ENGINE],
    after: [`review    ${EXPORT}  ░░░░░░░░░░  0/1 criteria`, '  → AC1: The export command writes one file per table.', ENGINE],
  },
  {
    name: 'a row leaves both statuses from review',
    fixture: 'missing-file',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Its file was never written | review |', '| Its file was never written | done |')
    },
    before: ['review    M004 Its file was never written  no milestone file', ENGINE],
    after: [ENGINE],
  },
  {
    name: 'a row leaves both statuses',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | done |')
    },
    before: [`implement ${EXPORT}  ███░░░░░░░  1/3 tasks`, '  → T2: Write the command.', ENGINE],
    after: [ENGINE],
  },
  {
    name: "a check on the item row's nested task grows the bar and names the next task",
    fixture: 'nested-first',
    edit: files => {
      files[M030] = files[M030].replace('- [ ]   T1a:', '- [x]   T1a:')
    },
    before: ['implement M030 The next task is nested  ███░░░░░░░  1/3 tasks', '  → T1a: Nested task, open, with extra spaces after the box.', ENGINE],
    after: ['implement M030 The next task is nested  ██████░░░░  2/3 tasks', '  → T2: Second top-level task.', ENGINE],
  },
]

describe('the band follows edits at the next turn end (M193 AC4)', () => {
  for (const { name, fixture, edit, before, after } of EDITS) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        const copy = copyOf(fixture)
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        expect(await lines(ui)).toEqual(before)
        edit(copy.files)
        await $.turn.complete(turn())
        expect(await lines(ui)).toEqual(after)
        await ui.unmount()
      })
    }
  }
})

// Each close case presses the close button, ends a turn with nothing
// changed, edits the copy, ends another turn, and asserts whether the band
// shows, by the keys of the rows it draws.
type Close = { name: string; fixture: string; edit: (files: Record<string, string>) => void; shown: string[] | null }

const ADDED = (status: string) => `| M005 | Added later | ${status} | — | normal | milestones/M005-added.md |\n`
const CLOSES: Close[] = [
  {
    name: 'a checked task box keeps it hidden',
    fixture: 'single-in-progress',
    edit: files => {
      files[M002] = files[M002].replace('- [ ] T2:', '- [x] T2:')
    },
    shown: null,
  },
  {
    name: 'an added planned row keeps it hidden',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| M001 | First release |', `${ADDED('planned')}| M001 | First release |`)
    },
    shown: null,
  },
  {
    name: 'an edited title keeps it hidden',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command |', '| Add the export commands |')
    },
    shown: null,
  },
  {
    name: 'a row moved from in-progress to review shows it',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| Add the export command | in-progress |', '| Add the export command | review |')
    },
    shown: ['M002-header', 'M002-item'],
  },
  {
    name: 'an added active row shows it',
    fixture: 'single-in-progress',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| M001 | First release |', `${ADDED('in-progress')}| M001 | First release |`)
    },
    shown: ['M002-header', 'M002-item', 'M005-header'],
  },
  {
    name: 'a removed active row shows it',
    fixture: 'mixed',
    edit: files => {
      files[ROADMAP] = files[ROADMAP].replace('| A Tasks section with no boxes | in-progress |', '| A Tasks section with no boxes | done |')
    },
    shown: ['M010-header', 'M010-item', 'M013-header', 'M014-header'],
  },
  {
    name: 'two active rows that swap ROADMAP order show it',
    fixture: 'mixed',
    edit: files => {
      const lines = files[ROADMAP].split('\n')
      const a = lines.findIndex(l => l.startsWith('| M010 |'))
      const b = lines.findIndex(l => l.startsWith('| M012 |'))
      ;[lines[a], lines[b]] = [lines[b], lines[a]]
      files[ROADMAP] = lines.join('\n')
    },
    shown: ['M012-header', 'M010-header', 'M010-item', 'M013-header', 'M014-header'],
  },
]

describe('a press hides the band until the active ids, statuses, or order change (AC3)', () => {
  for (const { name, fixture, edit, shown } of CLOSES) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        const copy = copyOf(fixture)
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        await ui.press({ key: 'cairn-close' })
        expect(await lines(ui)).toEqual([ENGINE])
        // A turn end with nothing changed keeps it hidden.
        await $.turn.complete(turn())
        expect(await lines(ui)).toEqual([ENGINE])
        const unedited = JSON.stringify(copy.files)
        edit(copy.files)
        expect(JSON.stringify(copy.files)).not.toBe(unedited)
        await $.turn.complete(turn())
        if (shown === null) {
          expect(await lines(ui)).toEqual([ENGINE])
          expect(await hasCairn(ui)).toBe(false)
        } else {
          expect(await rowKeys(ui)).toEqual(shown)
        }
        await ui.unmount()
      })
    }
  }

  for (const surface of SURFACES) {
    test(`a move to review shows it, and a move back keeps it shown (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      const original = copy.files[ROADMAP]
      copy.files[ROADMAP] = original.replace('| Add the export command | in-progress |', '| Add the export command | review |')
      await $.turn.complete(turn())
      expect(await rowKeys(ui)).toEqual(['M002-header', 'M002-item'])
      copy.files[ROADMAP] = original
      await $.turn.complete(turn())
      expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], ENGINE])
      // The band stays shown until the next press.
      await ui.press({ key: 'cairn-close' })
      expect(await lines(ui)).toEqual([ENGINE])
      await ui.unmount()
    })
  }
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

describe('the band draws nothing', () => {
  for (const name of ['no-roadmap', 'no-active']) {
    test(`${name}: the mod draws nothing, passes to the engine, and does not throw`, { plugins: [PROBE] }, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      for (const surface of SURFACES) {
        const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
        const shown = (await ui.findAll({ type: 'Text' })).map(textOf)
        expect(shown).toEqual(['cairn hook: returned', ENGINE])
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
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND })) as Ui
    expect(await lines(ui)).toEqual([ENGINE])
    await ui.unmount()
  })
})

describe("cairn's rows sit above the band beneath (M193 AC6)", () => {
  test('single-in-progress over a plugin beneath', { plugins: [BENEATH] }, async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await $.turn.complete(turn())
    await mountEach(
      'single-in-progress',
      BAND,
      async ui => {
        expect(await lines(ui)).toEqual([...DRAWN['single-in-progress'], BENEATH_ROW])
        expect((await bandTexts(ui)).map(textOf)).not.toContain(BENEATH_ROW)
      },
      $,
    )
  })

  test('with nothing active, the band beneath shows alone', { plugins: [BENEATH] }, async ($, on) => {
    seat(on, copyOf('no-active'))
    await $.turn.complete(turn())
    await mountEach('no-active', BAND, async ui => expect(await lines(ui)).toEqual([BENEATH_ROW]), $)
  })
})
