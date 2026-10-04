import { describe, expect, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { FIXTURES } from './fixtures.gen'
import { CHECKED_MARK, NO_FILE, NO_ROADMAP, OPEN_MARK } from './pane'
import { listNames } from './reader'

// The cairn pane (M205). Each case answers the shipped mod's file calls from
// an in-memory copy of a fixture, as band.test.tsx does, and answers the
// pane calls (`ui.open`, `ui.close`, `ui.panes`) beneath the mod from a list
// of the open panes that it keeps. The values each case expects come from
// the fixture's `expected.json`, which scripts/tests/test_status_fixtures.py
// holds to the Python helpers and scripts/cairn_next.py.

const SURFACES = ['terminal', 'desktop'] as const
const PANE = 'cairn'
const COMMAND = 'cairn-pane'
const CHAPTER_TOOL = 'mcp__ccd_session__mark_chapter'
const PANE_VIEW = {
  component: 'Pane',
  requestId: PANE,
  props: {
    title: 'cairn',
    isFocused: false,
    bodyColumns: 60,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 200 },
    view: {},
  },
} as const
const BAND = {
  component: 'AbovePrompt',
  props: { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 120 },
} as const
// The phase label of each status, written out by hand.
const PHASE_LABEL: Record<string, string> = { 'in-progress': 'implement', review: 'review' }
// The fixtures whose reader finds a ROADMAP.
const WITH_ROADMAP = Object.keys(FIXTURES).filter(name => FIXTURES[name].next !== null)

type Element = { type: string; key?: string; props: Record<string, unknown>; children: unknown[] }
type Ui = {
  findAll: (q: { type?: string; key?: string }) => Promise<Element[]>
  press: (q: { key: string }) => Promise<unknown>
  unmount: () => Promise<void>
}

type Copy = {
  cwd: string
  files: Record<string, string>
  unreadable: string[]
  // The ids of the open panes, and each open and close that reached beneath
  // the mod.
  open: string[]
  opens: { id: string; title?: string }[]
  closes: string[]
  // When set, an open answers that the pane waits undrawn, for this reason.
  notPlaced?: string
}

function copyOf(name: string): Copy {
  const fixture = FIXTURES[name]
  return { cwd: fixture.cwd, files: { ...fixture.files }, unreadable: [...fixture.unreadable], open: [], opens: [], closes: [] }
}

let turnCount = 0
function turn() {
  turnCount += 1
  return { answer: '', durationMs: 1, isAborted: false, turnId: `t${turnCount}`, reason: 'answer' as const }
}

function seat(on: On, copy: Copy) {
  const has = (path: string) => Object.prototype.hasOwnProperty.call(copy.files, path)
  on('session.cwd', async () => ({ value: copy.cwd }))
  on('fs.stat', async ($, e, next) =>
    has(e.path) ? { value: { kind: 'file', size: copy.files[e.path].length, mtimeMs: 0, isLink: false } } : next(e),
  )
  on('fs.read', async ($, e, next) =>
    has(e.path) && !copy.unreadable.includes(e.path) ? { value: copy.files[e.path] } : next(e),
  )
  on('fs.list', async ($, e, next) => {
    const names = listNames(Object.keys(copy.files), e.path)
    if (names === null) return next(e)
    return { value: names.map(name => ({ name, kind: 'other', size: 0, mtimeMs: 0, isLink: false })) }
  })
  on('session.start', async ($, e) => ({ cwd: e.cwd }))
  on('turn.complete', async () => ({ text: '' }))
  on('classic.Stop', async () => ({}))
  on('prompt.submit', async ($, e) => ({ text: e.text, origin: e.origin }))
  on('skill.prompt', async ($, e) => ({ text: e.text }))
  on('tool.call', { tool: CHAPTER_TOOL }, async () => ({ result: 'Chapter marked' }))
  on('ui.render', { component: 'AbovePrompt' }, async () => ({ type: 'Text', props: {}, children: ['engine slot'] }))
  on('ui.open', async ($, e) => {
    copy.opens.push({ id: e.id, title: e.title })
    if (copy.notPlaced !== undefined) return { value: { isPlaced: false, reason: copy.notPlaced } }
    if (!copy.open.includes(e.id)) copy.open.push(e.id)
    return { value: { isPlaced: true } }
  })
  on('ui.close', async ($, e) => {
    copy.closes.push(e.id)
    copy.open = copy.open.filter(id => id !== e.id)
    return { value: undefined }
  })
  on('ui.panes', async () => ({
    value: copy.open.map(id => ({ id, title: id, isShown: true, isFocused: false, isPlaced: true })),
  }))
}

function textOf(node: unknown): string {
  if (typeof node === 'string') return node
  if (node === null || typeof node !== 'object') return ''
  return ((node as Element).children ?? []).map(textOf).join('')
}

function keyOf(node: Element): string | undefined {
  return node.key ?? (node.props?.key as string | undefined)
}

function kids(node: Element): Element[] {
  return (node.children ?? []).filter((c): c is Element => c !== null && typeof c === 'object')
}

// The pane's lines in order, each its key and its text.
async function paneLines($, surface: (typeof SURFACES)[number]): Promise<[string, string][]> {
  const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const out = kids(root).map(line => [keyOf(line) ?? '', textOf(line)] as [string, string])
  await ui.unmount()
  return out
}

const textAt = (lines: [string, string][], key: string) => lines.find(([k]) => k === key)?.[1]
const keysLike = (lines: [string, string][], pattern: RegExp) => lines.map(([k]) => k).filter(k => pattern.test(k))
const itemText = (item: { text: string; checked: boolean }) => `${item.checked ? CHECKED_MARK : OPEN_MARK} ${item.text}`

describe('/cairn-pane opens and closes the pane (M205 AC1)', () => {
  test('with a ROADMAP, the command opens pane cairn, and run again closes it', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    const first = await $.command.run({ command: COMMAND })
    expect(copy.opens.map(open => open.id)).toEqual([PANE])
    expect(copy.open).toEqual([PANE])
    expect(first.text).toBe('cairn pane opened')
    const second = await $.command.run({ command: COMMAND })
    expect(copy.closes).toEqual([PANE])
    expect(copy.open).toEqual([])
    expect(second.text).toBe('cairn pane closed')
    // A third run opens it again.
    await $.command.run({ command: COMMAND })
    expect(copy.open).toEqual([PANE])
  })

  test('with no ROADMAP, the command opens no pane and says so', async ($, on) => {
    const copy = copyOf('no-roadmap')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    const result = await $.command.run({ command: COMMAND })
    expect(copy.opens).toEqual([])
    expect(result.text).toBe(NO_ROADMAP)
  })

  test("an open the surface does not place prints the engine's reason", async ($, on) => {
    const copy = copyOf('single-in-progress')
    copy.notPlaced = 'the attached surfaces place no panes'
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    const result = await $.command.run({ command: COMMAND })
    expect(copy.opens.map(open => open.id)).toEqual([PANE])
    expect(result.text).toContain('the attached surfaces place no panes')
  })
})

describe('the pane shows each active milestone in full (M205 AC2)', () => {
  test('the domain holds the shapes AC2 names', () => {
    expect(WITH_ROADMAP.length).toBeGreaterThan(10)
    expect(WITH_ROADMAP).toContain('pane-full')
    expect(FIXTURES['pane-full'].unreadable.length).toBe(1)
  })

  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const lines = await paneLines($, surface)
        const want = FIXTURES[name].pane
        // The milestones in ROADMAP order, and no others.
        expect(keysLike(lines, /-head$/).filter(k => /^M\d+-head$/.test(k))).toEqual(want.map(row => `${row.id}-head`))
        for (const row of want) {
          expect(textAt(lines, `${row.id}-head`)).toBe(`${PHASE_LABEL[row.status]} ${row.id}  ${row.title}`)
          const file = row.file
          if (file === null) {
            expect(textAt(lines, `${row.id}-nofile`)).toBe(NO_FILE)
            expect(keysLike(lines, new RegExp(`^${row.id}-(task|criterion|log|goal)-`))).toEqual([])
            continue
          }
          const goal = keysLike(lines, new RegExp(`^${row.id}-goal-\\d+$`)).map(k => textAt(lines, k))
          expect(goal).toEqual(file.goal === '' ? [] : file.goal.split('\n').map(text => (text === '' ? ' ' : text)))
          const tasks = keysLike(lines, new RegExp(`^${row.id}-task-\\d+$`)).map(k => textAt(lines, k))
          expect(tasks).toEqual(file.tasks.map(itemText))
          const criteria = keysLike(lines, new RegExp(`^${row.id}-criterion-\\d+$`)).map(k => textAt(lines, k))
          expect(criteria).toEqual(file.criteria.map(itemText))
          const log = keysLike(lines, new RegExp(`^${row.id}-log-\\d+$`)).map(k => textAt(lines, k))
          expect(log).toEqual(file.log)
          expect(log.length).toBeLessThanOrEqual(5)
        }
      })
    }
  }

  test('with no ROADMAP, an open pane says that none was found', async ($, on) => {
    seat(on, copyOf('no-roadmap'))
    await $.turn.complete(turn())
    for (const surface of SURFACES) expect(await paneLines($, surface)).toEqual([['no-roadmap', NO_ROADMAP]])
  })
})

describe("the pane shows the queue that cairn_next.py prints (M205 AC3)", () => {
  test('the domain reaches every recommended command', () => {
    const commands = new Set(WITH_ROADMAP.map(name => FIXTURES[name].next?.command))
    expect([...commands].sort()).toEqual(['/milestone-implement', '/milestone-plan', '/milestone-review'])
    expect(WITH_ROADMAP.some(name => (FIXTURES[name].next?.waiting.length ?? 0) > 0)).toBe(true)
  })

  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const lines = await paneLines($, surface)
        const next = FIXTURES[name].next
        if (next === null) throw new Error('a fixture with a ROADMAP has a next step')
        expect(textAt(lines, 'next')).toBe(`Next  ${next.id === null ? next.command : `${next.command} ${next.id}`}`)
        // Every id opens with `M`, and the heading lines' keys end in `head`.
        expect(keysLike(lines, /^workable-M/)).toEqual(FIXTURES[name].workable.map(id => `workable-${id}`))
        expect(keysLike(lines, /^waiting-M/)).toEqual(next.waiting.map(row => `waiting-${row.id}`))
        for (const row of next.waiting) {
          expect(textAt(lines, `waiting-${row.id}`)).toBe(`${row.id}  ${row.title} · on ${row.unmet.join(', ')}`)
        }
      })
    }
  }
})

describe("the band's open button opens the pane (M205 AC4)", () => {
  for (const surface of SURFACES) {
    test(`a press opens pane cairn (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await ui.press({ key: 'cairn-open' })
      expect(copy.opens.map(open => open.id)).toEqual([PANE])
      expect(copy.open).toEqual([PANE])
      await ui.unmount()
    })

    test(`a skill row with no ROADMAP has no open button (${surface})`, async ($, on) => {
      seat(on, copyOf('no-roadmap'))
      await $.turn.complete(turn())
      await $.skill.prompt({ skill: 'cairn:milestone-plan', text: 'the plan prompt' })
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect((await ui.findAll({ key: 'skill-row' })).length).toBe(1)
      expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual(['cairn-close'])
      await ui.unmount()
    })
  }
})

// M002's task T2 is open in the fixture, and each case ticks it before the
// event, so the drawing after the event shows it checked.
const M002 = '/cairn/milestones/M002-export.md'
const T2_OPEN = `${OPEN_MARK} T2: Write the command.`
const T2_DONE = `${CHECKED_MARK} T2: Write the command.`
const tick = (copy: Copy) => {
  copy.files[M002] = copy.files[M002].replace('- [ ] T2:', '- [x] T2:')
}

type Event = { name: string; before?: ($) => Promise<void>; act: ($) => Promise<void> }

const EVENTS: Event[] = [
  { name: 'session start', act: $ => $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true }) },
  { name: 'turn end', act: $ => $.turn.complete(turn()) },
  { name: 'cairn skill prompt', act: $ => $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' }) },
  { name: 'marked chapter', act: $ => $.tool.call({ tool: CHAPTER_TOOL, title: 'T2: Write the command' }) },
  {
    name: 'Stop that ends a step',
    before: $ => $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' }),
    act: $ => $.classic.Stop({ stop_hook_active: false, background_tasks: [] }),
  },
  {
    name: 'idle typed prompt that ends a step',
    before: async $ => {
      await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
      // A Stop with work in flight keeps the step and reads no files.
      await $.classic.Stop({
        stop_hook_active: false,
        background_tasks: [{ id: 'b1', type: 'subagent', status: 'running', description: 'a reviewer', agent_type: 'general-purpose' }],
      })
    },
    act: $ => $.prompt.submit({ text: 'a typed prompt', wait: false, origin: { kind: 'composer' } }),
  },
]

describe('an open pane draws again at each refresh the band takes (M205 AC5)', () => {
  for (const event of EVENTS) {
    test(`the ${event.name} shows an edit made before it`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      if (event.before !== undefined) await event.before($)
      expect(textAt(await paneLines($, 'terminal'), 'M002-task-1')).toBe(T2_OPEN)
      tick(copy)
      // The edit alone draws nothing new.
      expect(textAt(await paneLines($, 'terminal'), 'M002-task-1')).toBe(T2_OPEN)
      await event.act($)
      expect(textAt(await paneLines($, 'terminal'), 'M002-task-1')).toBe(T2_DONE)
    })
  }
})
