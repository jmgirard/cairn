import { describe, expect, mock, test } from 'claude-code/testing'
import type { On } from 'claude-code'

import { BADGE_PAD, badgeSvg, badgeWidth } from './badge'
import { FIXTURES } from './fixtures.gen'
import { GRAY, flowOf, width } from './band'
import {
  CHECKED_MARK,
  cardCut,
  cardPlace,
  cardPlaces,
  cardRows,
  COMMAND_PHASE,
  INFO_LABEL,
  ITEM_OPEN_MARK,
  NO_FILE,
  NO_ROADMAP,
  OPEN_MARK,
  PRIORITY_MARK,
  goalBlocks,
  nextLabel,
  nextTitle,
  paneLines as layout,
  PR_VIEW_FIELDS,
  prViewRead,
  startedRows,
} from './pane'
import type { PaneLine, PrRead } from './pane'
import type { PaneState } from './reader'
import { archivedArgs, COMMON_DIR_ARGS, DESCRIBE_ARGS, REPO_QUERY, tagTimeArgs } from './repo'
import { candidateRows, listNames, parseRoadmapRows, takenRows } from './reader'

// The cairn pane (M205). Each case answers the shipped mod's file calls from
// an in-memory copy of a fixture, as band.test.tsx does, and answers the
// pane calls (`ui.open`, `ui.close`, `ui.panes`) beneath the mod from a list
// of the open panes that it keeps. The values each case expects come from
// the fixture's `expected.json`, which scripts/tests/test_status_fixtures.py
// holds to the Python helpers and scripts/cairn_next.py.

const SURFACES = ['terminal', 'desktop'] as const
const PANE = 'cairn'
const COMMAND = 'cairn-pane'
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
// The fixtures whose reader finds a ROADMAP.
const WITH_ROADMAP = Object.keys(FIXTURES).filter(name => FIXTURES[name].next !== null)
// The candidate rows a fixture's live started token hides, written out by
// hand from its ROADMAP (M273): `high-candidate`'s `— started M2` names the
// planned M002.
const HIDDEN: Record<string, string[]> = { 'high-candidate': ['Taken row'] }
// A fixture's drawn candidate rows, each with its index in `candidates`,
// high rows first, then normal, then low, then parked (M284), each level in
// ROADMAP order (M280). `candidates-order` and `candidates-parked` state
// their order by hand.
const LEVEL = { high: 0, normal: 1, low: 2, parked: 3 }
function drawnCandidates(name: string) {
  return FIXTURES[name].candidates
    .map((row, i) => ({ row, i }))
    .filter(({ row }) => !(HIDDEN[name] ?? []).includes(row.title))
    .sort((a, b) => LEVEL[a.row.priority] - LEVEL[b.row.priority] || a.i - b.i)
}

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
  // When set, an open answers that the pane waits undrawn, for this reason,
  // and the pane stays listed with `isPlaced` false, as the API keeps it.
  notPlaced?: string
  // The open ids that wait undrawn, and those behind another pane's tab.
  unplaced?: string[]
  hidden?: string[]
  // The toasts that reached beneath the mod.
  toasts?: string[]
  // The project root `$.session.root()` answers, when it differs from the
  // cwd (M222 review).
  root?: string
  // When set, every open is refused with this reason.
  refuse?: string
  // The command and args of each slash command run that reached beneath the
  // mod, and while set, a promise each run waits for before it answers
  // (M218).
  commands?: { command: string; args: string }[]
  runHold?: Promise<void>
  // While set, a slash command run beneath the mod throws this message
  // (M221 review).
  runThrows?: string
  // While set, the path of each `$.fs.read` call is pushed here (M236).
  reads?: string[]
  // While set, `$.ui.panes()` beneath the mod throws (M237).
  panesThrow?: boolean
  // While set, the next `$.ui.panes()` beneath the mod computes its answer,
  // clears this field, keeps that answer in `panesHeld`, and waits for this
  // promise before it answers (M256).
  panesHold?: Promise<void>
  panesHeld?: ReturnType<typeof panesOf>
  // While set, the session end beneath the mod throws, and while set, it
  // waits for this promise before it answers (M255).
  endThrows?: boolean
  endHold?: Promise<void>
  // The text and mode of each prompt box fill that reached beneath the mod
  // (M260).
  fills?: { text: string; mode: string }[]
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

// What `$.ui.panes()` answers the mod: the open panes, each shown unless it
// sits behind another pane's tab, and placed unless it waits undrawn.
function panesOf(copy: Copy) {
  return copy.open.map(id => ({
    id,
    title: id,
    isShown: !(copy.hidden ?? []).includes(id),
    isFocused: false,
    isPlaced: !(copy.unplaced ?? []).includes(id),
  }))
}

function seat(on: On, copy: Copy) {
  const has = (path: string) => Object.prototype.hasOwnProperty.call(copy.files, path)
  on('session.cwd', async () => ({ value: copy.cwd }))
  on('session.root', async () => ({ value: copy.root ?? copy.cwd }))
  on('fs.stat', async ($, e, next) =>
    has(e.path) ? { value: { kind: 'file', size: copy.files[e.path].length, mtimeMs: 0, isLink: false } } : next(e),
  )
  on('fs.read', async ($, e, next) => {
    copy.reads?.push(e.path)
    return has(e.path) && !copy.unreadable.includes(e.path) ? { value: copy.files[e.path] } : next(e)
  })
  on('fs.list', async ($, e, next) => {
    const names = listNames(Object.keys(copy.files), e.path)
    if (names === null) return next(e)
    return { value: names.map(name => ({ name, kind: 'other', size: 0, mtimeMs: 0, isLink: false })) }
  })
  on('session.start', async ($, e) => ({ cwd: e.cwd }))
  on('turn.complete', async () => ({ text: '' }))
  on('classic.Stop', async () => ({}))
  on('classic.SessionStart', async () => ({}))
  on('prompt.submit', async ($, e) => ({ text: e.text, origin: e.origin }))
  on('skill.prompt', async ($, e) => ({ text: e.text }))
  on('ui.render', { component: 'AbovePrompt' }, async () => ({ type: 'Text', props: {}, children: ['engine slot'] }))
  on('ui.open', async ($, e) => {
    if (copy.refuse !== undefined) return { deny: copy.refuse }
    copy.opens.push({ id: e.id, title: e.title })
    if (!copy.open.includes(e.id)) copy.open.push(e.id)
    copy.hidden = (copy.hidden ?? []).filter(id => id !== e.id)
    if (copy.notPlaced !== undefined) {
      copy.unplaced = [...(copy.unplaced ?? []).filter(id => id !== e.id), e.id]
      return { value: { isPlaced: false, reason: copy.notPlaced } }
    }
    copy.unplaced = (copy.unplaced ?? []).filter(id => id !== e.id)
    return { value: { isPlaced: true } }
  })
  on('ui.close', async ($, e) => {
    copy.closes.push(e.id)
    copy.open = copy.open.filter(id => id !== e.id)
    return { value: undefined }
  })
  on('ui.panes', async () => {
    if (copy.panesThrow === true) throw new Error('no panes')
    const value = panesOf(copy)
    const hold = copy.panesHold
    if (hold !== undefined) {
      copy.panesHold = undefined
      copy.panesHeld = value
      await hold
    }
    return { value }
  })
  on('ui.toast', async ($, e) => {
    copy.toasts = [...(copy.toasts ?? []), e.text]
    return { value: undefined }
  })
  on('prompt.fill', async ($, e) => {
    copy.fills = [...(copy.fills ?? []), { text: e.text, mode: e.mode }]
    return { isFilled: true }
  })
  on('command.run', async ($, e) => {
    copy.commands = [...(copy.commands ?? []), { command: e.command, args: e.args }]
    if (copy.runHold !== undefined) await copy.runHold
    if (copy.runThrows !== undefined) throw new Error(copy.runThrows)
    return { text: '' }
  })
  // The session end a `/clear` brings, which runs the command a Plan or
  // Implement press holds (M221).
  on('session.end', async ($, e) => {
    if (copy.endHold !== undefined) await copy.endHold
    if (copy.endThrows === true) throw new Error('the end failed')
    return { sessionId: e.sessionId }
  })
}

// A node's shown text. An `Svg` icon reads as its alt text, the glyph the
// terminal draws in its place, and a Box drawn `display: 'none'`, as the
// hover card is until the pointer is over its line (over its ⓘ on a
// candidate line, M290), reads as nothing (M286).
function textOf(node: unknown): string {
  if (typeof node === 'string') return node
  if (node === null || typeof node !== 'object') return ''
  if ((node as Element).type === 'Svg') return String((node as Element).props.alt ?? '')
  if ((node as Element).props?.display === 'none') return ''
  return ((node as Element).children ?? []).map(textOf).join('')
}

// The Box that holds the Button keyed `key` as its child, found anywhere
// under `node` (M290).
function holderOf(node: Element, key: string): Element | undefined {
  for (const child of kids(node)) {
    if (child.type === 'Button' && keyOf(child) === key) return node
    const found = holderOf(child, key)
    if (found !== undefined) return found
  }
  return undefined
}

// A hover card: a child placed `position: 'absolute'` that holds no
// Button, since the desktop's parked ✎ Box is placed too (M290). Most
// cards are a line's child; a candidate card that opens below is a child
// of the pane's root, after every line (M294).
function isCard(child: Element): boolean {
  return child.props.position === 'absolute' && !kids(child).some(node => node.type === 'Button')
}

function keyOf(node: Element): string | undefined {
  return node.key ?? (node.props?.key as string | undefined)
}

function kids(node: Element): Element[] {
  return (node.children ?? []).filter((c): c is Element => c !== null && typeof c === 'object')
}

// The pane root's lines in order, the card's lines first (M286), and after
// them any candidate card that opens below its row (M294), which is no line.
function flat(root: Element): Element[] {
  return kids(root).flatMap(line => (keyOf(line) === 'cairn-card' ? kids(line) : [line]))
}

// The Buttons under a node, in order (M219).
function buttonsIn(node: Element): Element[] {
  return kids(node).flatMap(child => (child.type === 'Button' ? [child] : buttonsIn(child)))
}

// A heading's text (M286): the bold label, and what follows it after a
// space where it has more: a tail, or since M302 a badge in the lead.
// The joined text is the same either way, so placement is checked by the
// M302 lead and tail tests, not by this helper.
const headText = (label: string, rest = '') => `${label}${rest === '' ? '' : ` ${rest}`}`
// A counted heading's text (M289): its badge reads as the number, the
// `Svg`'s alt text, on the desktop, and as the number with a space on each
// side in the terminal.
const countHead = (label: string, count: number | string, surface: (typeof SURFACES)[number]) =>
  headText(label, surface === 'terminal' ? ` ${count} ` : `${count}`)
// A heading's badge span as the layout gives it (M289), written out here
// from the plan's colors rather than read from badge.ts: since M302 every
// heading's badge takes the theme's gray.
const BADGE_KEY = 'inactive'
const badgeOf = (count: number) => ({
  text: ` ${count} `,
  color: 'inverseText',
  backgroundColor: BADGE_KEY,
  badge: { count },
})

// The pane's lines in order, each its key and its text, the card's lines
// first (M286).
async function paneLines($, surface: (typeof SURFACES)[number]): Promise<[string, string][]> {
  const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const out = kids(root)
    .flatMap(line => (keyOf(line) === 'cairn-card' ? kids(line) : [line]))
    .map(line => [keyOf(line) ?? '', textOf(line)] as [string, string])
  await ui.unmount()
  return out
}

const textAt = (lines: [string, string][], key: string) => lines.find(([k]) => k === key)?.[1]
const keysLike = (lines: [string, string][], pattern: RegExp) => lines.map(([k]) => k).filter(k => pattern.test(k))
const itemText = (item: { text: string; checked: boolean }) => `${item.checked ? CHECKED_MARK : ITEM_OPEN_MARK}  ${item.text}`

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
    // The unplaced pane stays listed. A second run opens it again rather
    // than closing a pane nobody saw (M205 review).
    copy.notPlaced = undefined
    const second = await $.command.run({ command: COMMAND })
    expect(copy.closes).toEqual([])
    expect(copy.opens.map(open => open.id)).toEqual([PANE, PANE])
    expect(second.text).toBe('cairn pane opened')
  })

  test('a pane behind another tab is opened again, not closed', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    await $.command.run({ command: COMMAND })
    copy.hidden = [PANE]
    const result = await $.command.run({ command: COMMAND })
    expect(copy.closes).toEqual([])
    expect(copy.opens.length).toBe(2)
    expect(result.text).toBe('cairn pane opened')
  })

  test('a refused open gives a line, not an error', async ($, on) => {
    const copy = copyOf('single-in-progress')
    copy.refuse = 'opens are refused here'
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true })
    const result = await $.command.run({ command: COMMAND })
    expect(result.text.startsWith('cairn pane: ')).toBe(true)
    expect(result.text).toContain('opens are refused here')
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
          // The head line ends with the band's percent for a row whose file
          // reads (M208 AC1).
          const band = FIXTURES[name].rows.find(b => b.id === row.id && b.status === row.status)
          const percent = row.file === null || band === undefined ? null : flowOf(band)?.percent
          const tail = percent === null || percent === undefined ? '' : `  ${percent}%`
          expect(textAt(lines, `${row.id}-head`)).toBe(`${row.id}  ${row.title}${tail}`)
          const file = row.file
          if (file === null) {
            expect(textAt(lines, `${row.id}-nofile`)).toBe(NO_FILE)
            expect(keysLike(lines, new RegExp(`^${row.id}-(task|criterion|log|goal)-`))).toEqual([])
            continue
          }
          const goal = keysLike(lines, new RegExp(`^${row.id}-goal-\\d+$`)).map(k => textAt(lines, k))
          expect(goal).toEqual(goalBlocks(file.goal).map(text => (text === '' ? ' ' : text)))
          const tasks = keysLike(lines, new RegExp(`^${row.id}-task-\\d+$`)).map(k => textAt(lines, k))
          // An in-progress milestone's first open task draws `⊙` (M286).
          const current = row.status === 'in-progress' ? file.tasks.findIndex(item => !item.checked) : -1
          expect(tasks).toEqual(file.tasks.map((item, i) => (i === current ? `⊙  ${item.text}` : itemText(item))))
          const criteria = keysLike(lines, new RegExp(`^${row.id}-criterion-\\d+$`)).map(k => textAt(lines, k))
          expect(criteria).toEqual(file.criteria.map(itemText))
          // No work-log section, though the file holds log lines (M286).
          expect(keysLike(lines, new RegExp(`^${row.id}-log`))).toEqual([])
        }
      })
    }
  }

  // The operator picked one line per item at the live look: each item, log
  // line, and title is cut with an ellipsis, and the goal's lines wrap.
  for (const surface of SURFACES) {
    test(`items cut to one line, the goal wraps (${surface})`, async ($, on) => {
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
      const wrapOf = async (key: string) => {
        const [box] = await ui.findAll({ key: `${key}-text` })
        return kids(box)[0].props.wrap
      }
      for (const key of ['M080-head', 'M080-task-0', 'M080-criterion-0', 'waiting-M083', 'workable-M085', 'next']) {
        expect([key, await wrapOf(key)]).toEqual([key, 'truncate-end'])
      }
      for (const key of ['M081-goal-0', 'M081-goal-1', 'M081-goal-2']) expect([key, await wrapOf(key)]).toEqual([key, 'wrap'])
      await ui.unmount()
    })
  }

  test('with no ROADMAP, an open pane says that none was found', async ($, on) => {
    seat(on, copyOf('no-roadmap'))
    await $.turn.complete(turn())
    for (const surface of SURFACES) expect(await paneLines($, surface)).toEqual([['no-roadmap', NO_ROADMAP]])
  })
})

describe('the goal wraps at the pane, one line per paragraph or list item (M286 AC1)', () => {
  // The goal's lines, as `paneLines` draws them for one active milestone,
  // each with its `wraps` flag. The expected texts are written out by hand.
  const goalOf = (goal: string) => {
    const state: PaneState = {
      found: true,
      milestones: [{ id: 'M1', title: 'x', status: 'in-progress', file: { goal, tasks: [], criteria: [], log: [] } }],
      next: null,
      workable: [],
      waiting: [],
      candidates: [],
      blocked: [],
      taken: [],
    }
    return layout(state)
      .filter(line => /^M1-goal-\d+$/.test(line.key))
      .map(line => [line.text?.text, line.wraps])
  }

  test('three lines broken by hand draw as one line', () => {
    expect(goalOf('The pane opens with a card\n  of the repo, and wraps\neach goal at its width.')).toEqual([
      ['The pane opens with a card of the repo, and wraps each goal at its width.', true],
    ])
  })

  test('two paragraphs with two blank lines between them draw two lines and one blank row', () => {
    expect(goalOf('First paragraph,\nbroken here.\n\n\nSecond paragraph.')).toEqual([
      ['First paragraph, broken here.', true],
      [' ', true],
      ['Second paragraph.', true],
    ])
  })

  test('a list mixing markers draws one line per item, a continuation line joining its item', () => {
    expect(goalOf('Three parts:\n- the card\n* the look,\n  with a new pill\n1. the rows\n12. the docs')).toEqual([
      ['Three parts:', true],
      ['- the card', true],
      ['* the look, with a new pill', true],
      ['1. the rows', true],
      ['12. the docs', true],
    ])
  })
})

describe("the pane shows the queue that cairn_next.py prints (M205 AC3)", () => {
  test('the domain reaches every recommended command', () => {
    const commands = new Set(WITH_ROADMAP.map(name => FIXTURES[name].next?.command))
    expect([...commands].sort()).toEqual(['/milestone-implement', '/milestone-plan', '/milestone-review'])
    // Each one has a phase for the Next line's color (M208 review).
    expect(Object.keys(COMMAND_PHASE).sort()).toEqual([...commands].sort())
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
        // The command follows `→ ` with no pill and no padding (M286).
        // Planning names the fixture's `[high]` row title, when it has one
        // (M272).
        const named = next.id ?? next.title
        expect(textAt(lines, 'next')).toBe(`→ ${named === null ? next.command : `${next.command} ${named}`}`)
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

// Each priority's mark, written out by hand rather than read from
// `PRIORITY_MARK` (M253).
// Each names the icon the desktop draws in its place (M286).
const MARKS = {
  high: { text: '↑', color: 'claude', bold: true, icon: 'high' },
  normal: { text: '○', icon: 'ring' },
  low: { text: '↓', color: 'inactive', icon: 'low' },
  // M284: a parked row's hourglass, gray.
  parked: { text: '⧗', color: 'inactive', icon: 'parked' },
} as const

// The candidates fixture's lines, written out by hand from its ROADMAP, in
// ROADMAP order: entry i is the line keyed `candidate-<i>`.
const CANDIDATE_LINES = [
  '↑ High row',
  '○ Normal row',
  '↓ Low row',
  '○ A row with no colon and space, cut at its dash',
  '○ [HIGH] Upper-case token, kept in the title',
  '○ [high]No space after the token, kept in the title',
  '○ Token in [low] mid-row, read as normal',
  '○ A long title that runs on well past the width of any docked pane, so the pane cuts it to one line with an ellipsis at its end',
  '○ `code',
  '○ ordinal',
  '○ loglog link for `binomial`. Needs a case',
  '○ Title — detail',
  '↓ Low row',
  '○ A `a',
  '○ A row with no colon and no dash',
]
// The order the pane draws them in, by index, written out by hand (M280):
// the high row, the normal rows in ROADMAP order, then the two low rows.
const CANDIDATE_ORDER = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 2, 12]

describe('the idle pane lists the candidate rows (M207 AC1, AC2)', () => {
  for (const surface of SURFACES) {
    test(`the candidates fixture's heading, count, marks, and titles (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'candidates-head')).toBe(countHead('Candidates', 15, surface))
      const rows = keysLike(lines, /^candidate-\d+$/)
      expect(rows).toEqual(CANDIDATE_ORDER.map(i => `candidate-${i}`))
      expect(rows.map(k => textAt(lines, k))).toEqual(CANDIDATE_ORDER.map(i => CANDIDATE_LINES[i]))
      // The section comes after the queue.
      const at = (key: string) => lines.findIndex(([k]) => k === key)
      expect(at('candidates-head')).toBeGreaterThan(at('next'))
      expect(at('candidates-head')).toBeGreaterThan(at('workable-M031'))
    })

    test(`each priority's mark (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
      const markOf = async (i: number) => {
        const [lead] = await ui.findAll({ key: `candidate-${i}-lead` })
        return kids(lead)[0]
      }
      // Each mark and its color are written out by hand (M253): ↑ high, ○
      // normal (the open circle, M253), and ↓ low. On the desktop each draws
      // as its icon, whose alt text is the mark (M286).
      expect(textOf(await markOf(0))).toBe('↑')
      expect(textOf(await markOf(1))).toBe('○')
      expect(textOf(await markOf(2))).toBe('↓')
      if (surface === 'desktop') {
        for (const i of [0, 1, 2]) expect((await markOf(i)).type).toBe('Svg')
      } else {
        // The high mark takes the implement phase's theme key, written out
        // by hand (M217), and is bold; the normal mark has no color.
        expect((await markOf(0)).props.color).toBe('claude')
        expect((await markOf(2)).props.color).toBe('inactive')
        expect((await markOf(0)).props.bold).toBe(true)
        expect((await markOf(1)).props.color).toBe(undefined)
        expect((await markOf(1)).props.bold).toBe(undefined)
      }
      const titleOf = async (i: number) => kids((await ui.findAll({ key: `candidate-${i}-text` }))[0])[0]
      expect((await titleOf(2)).props.color).toBe('inactive')
      expect((await titleOf(0)).props.color).toBe(undefined)
      expect((await titleOf(1)).props.color).toBe(undefined)
      // The constant holds exactly these marks, so no stray color or bold
      // rides on the normal mark.
      expect(PRIORITY_MARK).toEqual(MARKS)
      await ui.unmount()
    })

    test(`a long title is kept whole and cut by the truncate-end wrap (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
      const [box] = await ui.findAll({ key: 'candidate-7-text' })
      const text = kids(box)[0]
      expect(textOf(text)).toBe(CANDIDATE_LINES[7].slice(2))
      expect(textOf(text).length).toBeGreaterThan(PANE_VIEW.props.bodyColumns)
      expect(text.props.wrap).toBe('truncate-end')
      await ui.unmount()
    })

    test(`the skeleton's commented rows draw no section (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates-skeleton'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(keysLike(lines, /^candidate/)).toEqual([])
    })
  }

  // Every fixture: the section draws only with no active row and at least
  // one candidate row, and then holds every row (M207 AC2).
  test('the domain holds an active fixture with candidate rows and an idle one without', () => {
    expect(WITH_ROADMAP.some(name => FIXTURES[name].pane.length > 0 && FIXTURES[name].candidates.length > 0)).toBe(true)
    expect(WITH_ROADMAP.some(name => FIXTURES[name].pane.length === 0 && FIXTURES[name].candidates.length === 0)).toBe(true)
  })

  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name}: candidates only while idle (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const lines = await paneLines($, surface)
        const { pane } = FIXTURES[name]
        const candidates = drawnCandidates(name)
        if (pane.length > 0 || candidates.length === 0) {
          expect(keysLike(lines, /^candidate/)).toEqual([])
          return
        }
        expect(textAt(lines, 'candidates-head')).toBe(countHead('Candidates', candidates.length, surface))
        expect(keysLike(lines, /^candidate-\d+$/).map(k => textAt(lines, k))).toEqual(
          candidates.map(({ row }) => `${MARKS[row.priority].text} ${row.title}`),
        )
      })
    }
  }
})

// The candidates-order fixture's rows sit out of level order (M280): a high
// row below a low row, an untagged row below a low row, and each level's
// two rows split by rows of other levels. Its drawn order, by index and
// title, written out by hand.
const ORDER_LINES: [number, string][] = [
  [2, '↑ Late high'],
  [5, '↑ Last high'],
  [1, '○ Normal one'],
  [4, '○ Normal two'],
  [0, '↓ First low'],
  [3, '↓ Second low'],
]

describe('the pane draws candidate rows high, then normal, then low (M280 AC1, AC2)', () => {
  for (const surface of SURFACES) {
    test(`the candidates-order fixture draws in level order, ROADMAP order within a level (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates-order'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      const rows = keysLike(lines, /^candidate-\d+$/)
      expect(rows).toEqual(ORDER_LINES.map(([i]) => `candidate-${i}`))
      expect(rows.map(k => textAt(lines, k))).toEqual(ORDER_LINES.map(([, text]) => text))
    })
  }

  // The first drawn line is the ROADMAP's third row, and the last its
  // fourth; each ✎ plans its own row's title.
  for (const [i, title] of [[2, 'Late high'], [3, 'Second low']] as [number, string][]) {
    test(`✎ on the line drawn for row ${i} plans ${title}`, async ($, on) => {
      const copy = copyOf('candidates-order')
      seat(on, copy)
      await $.turn.complete(turn())
      await pressKey($, `cairn-pane-plan-${i}`)
      expect(copy.commands).toEqual([CLEAR_RUN])
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 2)
      expect(copy.commands).toEqual([CLEAR_RUN, { command: 'cairn:milestone-plan', args: title }])
    })
  }
})

// The blocked-prs fixture's lines, written out by hand from its milestone
// files (M223 AC1, AC2): one URL, the first of two URLs, a URL only after a
// `companion:` entry, a URL with a trailing path, no URL, a failed read, and
// a missing file.
const BLOCKED_LINES = [
  '○ M101  One pull request URL  #12',
  '○ M102  Two pull request URLs  #34',
  '○ M103  A URL only after a companion entry',
  '○ M104  A URL with a trailing path  #90',
  '○ M105  A branch with no URL',
  '○ M106  A file whose read fails',
  '○ M107  A missing file',
]
const blockedLine = (row: { id: string; title: string; pr: number | null; archived: boolean }) =>
  prText(row.id, row.title, row.pr, undefined, row.archived)

describe('the pane lists the blocked milestones and their PRs (M223 AC1, AC2)', () => {
  test('the domain holds blocked rows with and without an active milestone, and fixtures with none', () => {
    expect(FIXTURES['blocked-prs'].pane.length).toBe(0)
    expect(FIXTURES['blocked-prs'].unreadable).toEqual(['/cairn/milestones/M106-unreadable.md'])
    expect(Object.keys(FIXTURES['blocked-prs'].files)).not.toContain('/cairn/milestones/M107-missing.md')
    expect(FIXTURES['blocked-active'].pane.length).toBeGreaterThan(0)
    expect(FIXTURES['blocked-active'].blocked.length).toBeGreaterThan(0)
    expect(WITH_ROADMAP.some(name => FIXTURES[name].blocked.length === 0)).toBe(true)
  })

  for (const surface of SURFACES) {
    test(`blocked-prs: the heading, each row, and its number (${surface})`, async ($, on) => {
      seat(on, copyOf('blocked-prs'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'blocked-head')).toBe(countHead('Blocked', 7, surface))
      expect(keysLike(lines, /^blocked-M/).map(k => textAt(lines, k))).toEqual(BLOCKED_LINES)
      // After the queue's place and before the candidates.
      const at = (key: string) => lines.findIndex(([k]) => k === key)
      expect(at('blocked-head')).toBeGreaterThan(at('next'))
      expect(at('candidates-head')).toBeGreaterThan(at('blocked-M107'))
    })

    test(`blocked-active: the section beside an active milestone (${surface})`, async ($, on) => {
      seat(on, copyOf('blocked-active'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'M110-head')).toBeDefined()
      expect(keysLike(lines, /^blocked-M/).map(k => textAt(lines, k))).toEqual([line1250()])
      const at = (key: string) => lines.findIndex(([k]) => k === key)
      expect(at('blocked-head')).toBeGreaterThan(at('next'))
      // After the Workable rows (M223 review).
      expect(at('workable-M112')).toBeGreaterThan(at('next'))
      expect(at('blocked-head')).toBeGreaterThan(at('workable-M112'))
    })

    test(`all-waiting: the section follows the Waiting rows (${surface})`, async ($, on) => {
      seat(on, copyOf('all-waiting'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      const at = (key: string) => lines.findIndex(([k]) => k === key)
      expect(at('blocked-head')).toBeGreaterThan(at('waiting-M093'))
      expect(textAt(lines, 'blocked-M092')).toBe('○ M092  Blocked outside')
    })

    test(`the number sits in the line's tail (${surface})`, async ($, on) => {
      seat(on, copyOf('blocked-active'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
      const [tail] = await ui.findAll({ key: 'blocked-M111-tail' })
      expect(textOf(tail)).toBe('  #1250')
      // The state mark before a read is the ring: an `Svg` on the desktop,
      // and a gray `○` in the terminal (M286).
      const [lead] = await ui.findAll({ key: 'blocked-M111-lead' })
      expect(kids(lead).map(t => [t.type, textOf(t), t.props.color])).toEqual([
        surface === 'terminal' ? ['Text', '○', GRAY] : ['Svg', '○', undefined],
        ['Text', ' ', undefined],
        ['Text', 'M111', undefined],
        ['Text', '  ', undefined],
      ])
      await ui.unmount()
    })
  }

  // Every fixture: the section holds each blocked row in ROADMAP order, and
  // a fixture with none draws no section.
  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name}: blocked rows (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const lines = await paneLines($, surface)
        const { blocked } = FIXTURES[name]
        if (blocked.length === 0) {
          expect(keysLike(lines, /^blocked/)).toEqual([])
          return
        }
        expect(textAt(lines, 'blocked-head')).toBe(countHead('Blocked', blocked.length, surface))
        expect(keysLike(lines, /^blocked-M/).map(k => textAt(lines, k))).toEqual(blocked.map(blockedLine))
      })
    }
  }
})

// M208: the operator's picked look. The values below are written out by
// hand from the fixtures.
const view = (bodyColumns: number) => ({ ...PANE_VIEW, props: { ...PANE_VIEW.props, bodyColumns } })
// The theme keys for implement, review, and plan (M217).
const IMPLEMENT_KEY = 'claude'
const REVIEW_KEY = 'success'
const PLAN_KEY = 'planMode'

async function mountPane($, surface: (typeof SURFACES)[number], bodyColumns = 60) {
  return (await $.ui.mount({ plugin: 'cairn', surface, ...view(bodyColumns) })) as Ui
}
async function boxOf(ui: Ui, key: string): Promise<Element | undefined> {
  return (await ui.findAll({ key }))[0]
}
// The Text children of a line's lead, text, or tail Box.
async function partOf(ui: Ui, key: string): Promise<Element[]> {
  const box = await boxOf(ui, key)
  return box === undefined ? [] : kids(box)
}

describe('the head line ends with the band percent (M208 AC1)', () => {
  // M002 as a review row: one checked criterion, one open, and one open box
  // inside a comment, which the band counts and the pane's items do not.
  // Band: review 1/3, so floor(100 × (1 + 1 + 1/3) / 3) = 77. Over the
  // pane's items it would be 1/2, so 83.
  const REVIEW_FILE = [
    '# M002: Add the export command',
    '',
    '## Goal',
    '',
    'Export things.',
    '',
    '## Acceptance criteria',
    '',
    '- [x] AC1: done.',
    '<!--',
    '- [ ] AC9: hidden in a comment.',
    '-->',
    '- [ ] AC2: open.',
    '',
    '## Tasks',
    '',
    '- [x] T1: Write the parser.',
    '',
  ].join('\n')
  const reviewCopy = () => {
    const copy = copyOf('single-in-progress')
    copy.files['/cairn/ROADMAP.md'] = copy.files['/cairn/ROADMAP.md'].replace(
      '| M002 | Add the export command | in-progress |',
      '| M002 | Add the export command | review |',
    )
    copy.files[M002] = REVIEW_FILE
    return copy
  }

  for (const surface of SURFACES) {
    test(`an in-progress row, a review row, and a row with no file (${surface})`, async ($, on) => {
      // pane-full: M080 in-progress, tasks 1/3, so floor(100 × (1 + 1/3) / 3) = 44.
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      expect((await partOf(ui, 'M080-head-tail')).map(textOf).join('')).toBe('  44%')
      // M082's file cannot be read: no percent, and its warning line stays.
      expect(await boxOf(ui, 'M082-head-tail')).toBe(undefined)
      expect(textOf((await partOf(ui, 'M082-nofile-text'))[0])).toBe(NO_FILE)
      // No track on any head line: no desktop Svg and no terminal braille.
      // The marks' icons draw elsewhere (M286).
      for (const id of ['M080', 'M081', 'M082']) {
        expect(kids((await boxOf(ui, `${id}-head`)) as Element).flatMap(kids).filter(t => t.type === 'Svg')).toEqual([])
      }
      for (const id of ['M080', 'M081', 'M082']) {
        expect([id, /[⠀-⣿]/.test(textOf((await boxOf(ui, `${id}-head`)) as Element))]).toEqual([id, false])
      }
      await ui.unmount()
    })

    test(`a review row takes the band's count, not the pane's items (${surface})`, async ($, on) => {
      seat(on, reviewCopy())
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'M002-head')).toBe('M002  Add the export command  77%')
      // The head line's title is bold (M286).
      const ui = await mountPane($, surface)
      expect(kids((await boxOf(ui, 'M002-head-text')) as Element)[0].props.bold).toBe(true)
      await ui.unmount()
      // The pane's own items hold two criteria, one checked.
      expect(keysLike(lines, /^M002-criterion-\d+$/).length).toBe(2)
    })

    test(`at 44 columns a long title leaves the percent in its own unshrinking Box (${surface})`, async ($, on) => {
      seat(on, copyOf('long-title'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface, 44)
      const head = await boxOf(ui, 'M060-head')
      if (head === undefined) throw new Error('no M060 head line')
      // The ⌂ and ↻ Boxes sit on the card's first line since M286.
      // The hover card's Box has no key (M286).
      expect(kids(head).map(keyOf).filter(key => key !== undefined)).toEqual(['M060-head-lead', 'M060-head-text', 'M060-head-tail'])
      expect(kids(head)[2].props.flexShrink).toBe(0)
      const title = textOf(kids(await boxOf(ui, 'M060-head-text') as Element)[0])
      expect(title.length).toBeGreaterThan(44)
      expect((await partOf(ui, 'M060-head-tail')).map(textOf).join('')).toMatch(/^ {2}\d+%$/)
      await ui.unmount()
    })
  }
})

describe('the Tasks and Criteria headings draw a six-cell meter (M208 AC2, M286)', () => {
  for (const surface of SURFACES) {
    test(`partly checked and all checked (${surface})`, async ($, on) => {
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      // M080 tasks 1/3: two of six filled, in the implement color.
      expect(textAt(lines, 'M080-tasks-head')).toBe(headText('Tasks', '1/3 ━━────'))
      // M081 tasks 1/1: all six filled.
      expect(textAt(lines, 'M081-tasks-head')).toBe(headText('Tasks', '1/1 ━━━━━━'))
      const ui = await mountPane($, surface)
      const tail = await partOf(ui, 'M080-tasks-head-tail')
      expect(tail.find(t => textOf(t) === '━━')?.props.color).toBe(IMPLEMENT_KEY)
      expect(tail.find(t => textOf(t) === '────')?.props.color).toBe('subtle')
      const review = await partOf(ui, 'M081-tasks-head-tail')
      expect(review.find(t => textOf(t) === '━━━━━━')?.props.color).toBe(REVIEW_KEY)
      await ui.unmount()
    })

    test(`all open (${surface})`, async ($, on) => {
      // single-in-progress criteria 0/1: none filled.
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'M002-criteria-head')).toBe(headText('Criteria', '0/1 ──────'))
      const ui = await mountPane($, surface)
      const tail = await partOf(ui, 'M002-criteria-head-tail')
      expect(tail.find(t => textOf(t) === '──────')?.props.color).toBe('subtle')
      expect(tail.some(t => textOf(t).includes('━'))).toBe(false)
      await ui.unmount()
    })
  }
})

describe('section headings, the head line, Next, and the card in the picked look (M286 AC6)', () => {
  // The spans of look B, written out by hand from the operator's pick (the
  // milestone file's T1 work-log line), with the operator's changes at the
  // live look: no rule after a heading, and the app's task-list marks.
  const EMPTY_GROW = { text: { text: '' }, grow: true }
  const state: PaneState = {
    found: true,
    milestones: [
      {
        id: 'M7',
        title: 'Add the card',
        status: 'in-progress',
        file: {
          goal: 'Show a card.',
          tasks: [
            { text: 'T1: one', checked: true },
            { text: 'T2: two', checked: false },
            { text: 'T3: three', checked: false },
          ],
          criteria: [],
          log: [],
        },
      },
    ],
    next: { action: 'resume', command: '/milestone-implement', id: 'M7', title: null },
    workable: [],
    waiting: [],
    candidates: [],
    blocked: [{ id: 'M5', title: 'Handed off', pr: 9, url: 'https://github.com/o/r/pull/9', archived: false }],
    taken: [],
  }
  const lines = () =>
    layout(state, [], false, {}, [], [], { root: '/', counts: { prs: 3, issues: 12 }, done: { tag: 'v2.1.0', days: 12, count: 4 }, name: 'cairn' })
  const at = (key: string) => lines().find(line => line.key === key)

  test('a plain heading: the bold label and an empty text that grows', () => {
    expect(at('M7-goal-head')).toEqual({
      key: 'M7-goal-head',
      indent: 0,
      lead: [{ text: 'Goal', bold: true }],
      ...EMPTY_GROW,
    })
  })

  test('a count with a meter: the counts in gray and six cells in the phase color at the right end', () => {
    expect(at('M7-tasks-head')).toEqual({
      key: 'M7-tasks-head',
      indent: 0,
      lead: [{ text: 'Tasks', bold: true }],
      ...EMPTY_GROW,
      tail: [
        { text: ' ' },
        { text: '1/3 ', color: GRAY },
        { text: '━━', color: IMPLEMENT_KEY },
        { text: '────', color: 'subtle' },
      ],
    })
  })

  test('a section count: the badge right after the label and a space, and no tail (M289, M302)', () => {
    expect(at('blocked-head')).toEqual({
      key: 'blocked-head',
      indent: 0,
      lead: [{ text: 'Blocked', bold: true }, { text: ' ' }, badgeOf(1)],
      ...EMPTY_GROW,
    })
  })

  // M302 AC4: the Criteria heading, like Tasks above, keeps its counts and
  // meter in the tail at the right end.
  test('the Criteria count and meter stay in the tail (M302 AC4)', () => {
    const [milestone] = state.milestones
    const withCriteria: PaneState = {
      ...state,
      milestones: [{ ...milestone, file: { ...milestone.file!, criteria: [{ text: 'AC1: one', checked: true }, { text: 'AC2: two', checked: false }] } }],
    }
    const head = layout(withCriteria, [], false, {}, [], []).find(line => line.key === 'M7-criteria-head')
    expect(head).toEqual({
      key: 'M7-criteria-head',
      indent: 0,
      lead: [{ text: 'Criteria', bold: true }],
      ...EMPTY_GROW,
      tail: [
        { text: ' ' },
        { text: '1/2 ', color: GRAY },
        { text: '━━━', color: IMPLEMENT_KEY },
        { text: '───', color: 'subtle' },
      ],
    })
    expect(at('M7-tasks-head')?.tail?.slice(1, 2)).toEqual([{ text: '1/3 ', color: GRAY }])
  })

  // M302 AC1: with no active milestone, so that Candidates draws beside
  // Blocked and Hotfixes, each counted heading puts its badge in the lead
  // after the label and a space.
  test('Blocked, Hotfixes, and Candidates each lead with the label, a space, and the badge (M302 AC1)', () => {
    const idle: PaneState = {
      ...state,
      milestones: [],
      candidates: [
        { priority: 'normal', title: 'One', text: 'One' },
        { priority: 'low', title: 'Two', text: 'Two' },
      ],
    }
    const got = layout(idle, [], false, {}, [{ number: 12, title: 'Fix', url: 'https://github.com/o/r/pull/12' }], [])
    const heads = [
      ['blocked-head', 'Blocked', 1],
      ['hotfixes-head', 'Hotfixes', 1],
      ['candidates-head', 'Candidates', 2],
    ] as const
    for (const [key, label, count] of heads) {
      const head = got.find(line => line.key === key)
      expect([key, head?.lead]).toEqual([key, [{ text: label, bold: true }, { text: ' ' }, badgeOf(count)]])
      expect([key, head?.tail]).toEqual([key, undefined])
    }
  })

  test('the head line: the id bold in the phase color and the title bold', () => {
    const head = at('M7-head')
    expect(head?.lead).toEqual([{ text: 'M7', color: IMPLEMENT_KEY, bold: true }, { text: '  ' }])
    expect(head?.text).toEqual({ text: 'Add the card', bold: true })
  })

  // At the operator's direction after the pick: the app's task-list marks,
  // each naming its icon, gray, and two spaces after the mark.
  test('the items: a checked box the done icon with gray text, an open box the dashed icon', () => {
    expect(at('M7-task-0')?.lead).toEqual([{ text: '●', color: GRAY, icon: 'done' }, { text: '  ' }])
    expect(at('M7-task-0')?.text).toEqual({ text: 'T1: one', color: GRAY })
    expect(at('M7-task-2')?.lead).toEqual([{ text: '◌', color: GRAY, icon: 'open' }, { text: '  ' }])
    expect(at('M7-task-2')?.text).toEqual({ text: 'T3: three' })
  })

  // The first open task of an in-progress milestone draws the in-progress
  // icon. A review milestone's open task does not.
  test('the first open task of an in-progress milestone draws the in-progress icon', () => {
    expect(at('M7-task-1')?.lead).toEqual([{ text: '⊙', icon: 'current' }, { text: '  ' }])
    expect(at('M7-task-1')?.text).toEqual({ text: 'T2: two' })
    const review = layout({ ...state, milestones: [{ ...state.milestones[0], status: 'review' }] }, [], false)
    expect(review.find(line => line.key === 'M7-task-1')?.lead[0]).toEqual({ text: '◌', color: GRAY, icon: 'open' })
  })

  // On the desktop each icon draws as an `Svg` of one size, and in the
  // terminal as its glyph (M286).
  for (const surface of SURFACES) {
    test(`the marks draw as icons of one size on the desktop and as glyphs in the terminal (${surface})`, async ($, on) => {
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const svgs = await ui.findAll({ type: 'Svg' })
      if (surface === 'terminal') {
        expect(svgs).toEqual([])
        expect(textOf(kids((await boxOf(ui, 'M080-task-0-lead')) as Element)[0])).toMatch(/^[●⊙◌]$/)
      } else {
        expect(svgs.length).toBeGreaterThan(3)
        expect(new Set(svgs.map(svg => `${svg.props.width}x${svg.props.height}`))).toEqual(new Set(['14x14']))
        expect(svgs.every(svg => String(svg.props.source).startsWith('<svg') && /^[●⊙◌○↑↓⧗▲◐✕]$/.test(String(svg.props.alt)))).toBe(true)
        expect((await boxOf(ui, 'M080-task-0'))?.props.alignItems).toBe('center')
      }
      await ui.unmount()
    })
  }

  test('a blank row sits under the card', () => {
    expect(lines()[4]).toEqual({ key: 'card-gap', indent: 0, lead: [], text: { text: ' ' } })
  })

  test('the Next line: the arrow and the command bold in the phase color, with no pill', () => {
    expect(at('next')).toEqual({
      key: 'next',
      indent: 0,
      lead: [{ text: '→ ', color: IMPLEMENT_KEY, bold: true }],
      text: { text: '/milestone-implement M7', color: IMPLEMENT_KEY, bold: true },
    })
  })

  test('the card: four lines with a stored release read, the numbers bold and the labels gray', () => {
    expect(lines().slice(0, 4)).toEqual([
      {
        key: 'card-repo',
        indent: 0,
        lead: [],
        text: { text: 'cairn', bold: true },
        tail: [
          { text: '  ' },
          { text: '3', bold: true },
          { text: ' PRs', color: GRAY },
          { text: '   ' },
          { text: '12', bold: true },
          { text: ' issues', color: GRAY },
        ],
        tailGrows: true,
        card: true,
        buttons: ['refresh'],
      },
      {
        key: 'card-candidates',
        indent: 0,
        lead: [
          { text: 'candidates', color: GRAY },
          { text: ' ' },
          { text: '↑', color: IMPLEMENT_KEY, bold: true, icon: 'high' },
          { text: ' 0' },
          { text: '   ' },
          { text: '○', icon: 'ring' },
          { text: ' 0' },
          { text: '   ' },
          { text: '↓', color: GRAY, icon: 'low' },
          { text: ' 0' },
          { text: '   ' },
          { text: '⧗', color: GRAY, icon: 'parked' },
          { text: ' 0' },
        ],
        text: null,
        card: true,
      },
      {
        key: 'card-milestones',
        indent: 0,
        lead: [],
        text: { text: '0 planned · 1 blocked', color: GRAY },
        card: true,
      },
      {
        key: 'card-release',
        indent: 0,
        lead: [],
        text: { text: 'v2.1.0 · 12 days ago · 4 done since', color: GRAY },
        card: true,
      },
    ])
  })

  test('one day reads `1 day ago`, and with no release read for this root the card has three lines', () => {
    const one = layout(state, [], false, {}, [], [], { root: '/', counts: null, done: { tag: 'v1.0.0', days: 1, count: 0 }, name: null })
    expect(one.find(line => line.key === 'card-release')?.text?.text).toBe('v1.0.0 · 1 day ago · 0 done since')
    const none = layout(state, [], false, {}, [], [], null)
    expect(none.filter(line => line.card).map(line => line.key)).toEqual(['card-repo', 'card-candidates', 'card-milestones'])
  })

  for (const surface of SURFACES) {
    test(`the card draws in a round Box in subtle (${surface})`, async ($, on) => {
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const card = await boxOf(ui, 'cairn-card')
      expect(card?.props).toEqual(expect.objectContaining({ borderStyle: 'round', borderColor: 'subtle', flexDirection: 'column' }))
      expect(kids(card as Element).map(keyOf)).toEqual(['card-repo', 'card-candidates', 'card-milestones'])
      await ui.unmount()
    })
  }

  // The Next line takes the color of the phase its command runs.
  const NEXTS: [string, string, string][] = [
    ['pane-full', '/milestone-review M081', REVIEW_KEY],
    ['single-in-progress', '/milestone-implement M002', IMPLEMENT_KEY],
    ['all-waiting', '/milestone-plan', PLAN_KEY],
  ]
  for (const surface of SURFACES) {
    for (const [fixture, command, color] of NEXTS) {
      test(`the Next command takes its phase's color on ${fixture} (${surface})`, async ($, on) => {
        seat(on, copyOf(fixture))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        const [text] = await partOf(ui, 'next-text')
        expect(textOf(text)).toBe(command)
        expect(text.props).toEqual(expect.objectContaining({ color, bold: true }))
        expect(text.props.backgroundColor).toBe(undefined)
        await ui.unmount()
      })
    }
  }
})

// The test computes no layout, so it checks the widths the line keeps and
// the prop that lets the line shrink; the live look shows the drawing.
describe("each line's lead and tail fit a 44-column dock, and the line may shrink (M208 AC4)", () => {
  for (const surface of SURFACES) {
    for (const fixture of ['pane-full', 'candidates', 'blocked-prs', 'blocked-active', 'blocked-archived']) {
      test(`${fixture} (${surface})`, async ($, on) => {
        seat(on, copyOf(fixture))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface, 44)
        const [root] = await ui.findAll({ key: 'cairn-pane' })
        const lines = kids(root).flatMap(line => (keyOf(line) === 'cairn-card' ? kids(line) : [line]))
        expect(lines.length).toBeGreaterThan(10)
        for (const line of lines) {
          const key = keyOf(line) ?? ''
          const indent = (line.props.paddingLeft as number | undefined) ?? 0
          const sum = async (part: string) => (await partOf(ui, `${key}-${part}`)).map(t => width(textOf(t))).reduce((a, b) => a + b, 0)
          expect([key, indent + (await sum('lead')) + (await sum('tail')) <= 44]).toEqual([key, true])
          expect([key, line.props.minWidth]).toEqual([key, 0])
        }
        await ui.unmount()
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
      expect(copy.toasts ?? []).toEqual([])
      await ui.unmount()
    })

    test(`a press the surface does not place says why in a toast (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      copy.notPlaced = 'the attached surfaces place no panes'
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      await ui.press({ key: 'cairn-open' })
      expect(copy.toasts).toEqual(['cairn pane not placed: the attached surfaces place no panes'])
      await ui.unmount()
    })

    // With no ROADMAP, a running cairn skill draws no row, so the band yields
    // the slot and draws neither button (M206 removed the skill row, which
    // drew the close button alone here).
    test(`a running skill with no ROADMAP yields the slot (${surface})`, async ($, on) => {
      seat(on, copyOf('no-roadmap'))
      await $.turn.complete(turn())
      await $.skill.prompt({ skill: 'cairn:milestone-plan', text: 'the plan prompt' })
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...BAND })) as Ui
      expect(await ui.findAll({ key: 'cairn-stack' })).toEqual([])
      expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual([])
      expect(JSON.stringify(await ui.findAll({ type: 'Text' }))).toContain('engine slot')
      await ui.unmount()
    })
  }
})

// M218: the Next line's Button. Its label by the next step's action, and
// one fixture of each action, written out by hand.
const PANE_NEXT = 'cairn-pane-next'
const ACTION_LABELS: Record<string, string> = {
  implement: 'Implement',
  resume: 'Resume',
  review: 'Review',
  'plan the next milestone': 'Plan',
}
const BY_ACTION: [string, string][] = [
  ['single-in-progress', 'resume'],
  ['states-review', 'review'],
  ['idle-order', 'implement'],
  ['all-waiting', 'plan the next milestone'],
]
// What a press runs for a fixture: `cairn:` and the command less its slash,
// and the id, or no args for planning.
function runOf(name: string): { command: string; args: string } {
  const next = FIXTURES[name].next as { command: string; id: string | null; title: string | null }
  return { command: `cairn:${next.command.slice(1)}`, args: next.id ?? next.title ?? '' }
}

// The next actions whose Button runs `/clear` first, and its command only
// at the session end the clear brings (M221).
const CLEARS_FIRST = ['implement', 'plan the next milestone']
const CLEAR_END = { reason: 'clear', sessionId: 's1' } as const

// Waits until `n` slash command runs reached beneath the mod, for at most
// `tries` waits of 5 ms, and then once more, so the last run settles (M221).
async function untilRuns(copy: Copy, n: number, tries = 200) {
  for (let i = 0; i < tries && (copy.commands ?? []).length < n; i++) await new Promise(resolve => setTimeout(resolve, 5))
  await new Promise(resolve => setTimeout(resolve, 5))
}

describe("the Next line carries the next step's Button (M218 AC1)", () => {
  test('the fixtures reach every action', () => {
    expect([...new Set(WITH_ROADMAP.map(name => FIXTURES[name].next?.action))].sort()).toEqual(Object.keys(ACTION_LABELS).sort())
    expect(BY_ACTION.map(([name]) => FIXTURES[name].next?.action)).toEqual(BY_ACTION.map(([, action]) => action))
  })

  // An action named like an object property has no label, so its line
  // carries no action (M218 review).
  test('an action outside the map, an inherited property name among them, has no label', () => {
    for (const action of Object.keys(ACTION_LABELS)) expect([action, nextLabel(action)]).toEqual([action, ACTION_LABELS[action]])
    for (const action of ['toString', 'constructor', '__proto__', 'hasOwnProperty', 'blocked']) {
      expect([action, nextLabel(action)]).toEqual([action, undefined])
      const state: PaneState = {
        found: true,
        milestones: [],
        next: { action, command: '/milestone-plan', id: null, title: null, waiting: [] },
        workable: [],
        waiting: [],
        candidates: [],
        blocked: [],
        taken: [],
      }
      const next = layout(state, [], true).find(line => line.key === 'next')
      expect([action, next?.action]).toEqual([action, undefined])
      // Nor Status, which shows only with the next-step Button (M219
      // review).
      expect([action, next?.buttons]).toEqual([action, undefined])
    }
  })

  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        // The Next line's first Button: Status follows it (M219).
        const buttons = buttonsIn((await boxOf(ui, 'next')) as Element)
        expect(keyOf(buttons[0])).toBe(PANE_NEXT)
        expect(buttons.filter(button => keyOf(button) === PANE_NEXT).length).toBe(1)
        const want = ACTION_LABELS[FIXTURES[name].next?.action as string]
        expect([buttons[0].props.label, buttons[0].props.variant]).toEqual([want, 'secondary'])
        // The Button comes after the command, in the Box after the command's.
        const line = (await boxOf(ui, 'next')) as Element
        expect(kids(line).map(keyOf).slice(0, 3)).toEqual(['next-lead', 'next-text', 'next-action'])
        expect(kids(kids(line)[2]).map(keyOf)).toEqual([PANE_NEXT])
        await ui.unmount()
      })
    }
  }
})

describe("a running cairn skill hides the pane's Button (M218 AC2)", () => {
  for (const surface of SURFACES) {
    test(`the Button goes at a skill's prompt and comes back at its Stop (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const command = async () => textOf((await partOf(ui, 'next-text'))[0])
      expect((await ui.findAll({ key: PANE_NEXT })).length).toBe(1)
      await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
      expect(await ui.findAll({ key: PANE_NEXT })).toEqual([])
      expect(await command()).toBe('/milestone-implement M002')
      await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
      expect((await ui.findAll({ key: PANE_NEXT })).length).toBe(1)
      expect(await command()).toBe('/milestone-implement M002')
      await ui.unmount()
    })
  }
})

describe("a press of the pane's Button runs the next command (M218 AC3)", () => {
  for (const [name] of BY_ACTION) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        const copy = copyOf(name)
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        await ui.press({ key: PANE_NEXT })
        // Plan and Implement run `/clear`, and their command at the clear's
        // session end (M221).
        if (CLEARS_FIRST.includes(FIXTURES[name].next?.action as string)) {
          await $.session.end(CLEAR_END)
          await untilRuns(copy, 2)
          expect(copy.commands).toEqual([CLEAR_RUN, runOf(name)])
        } else {
          expect(copy.commands).toEqual([runOf(name)])
        }
        await ui.unmount()
      })
    }
  }

  // The runs written out by hand for two of them.
  test('the runs for planning and for a milestone', () => {
    expect(runOf('all-waiting')).toEqual({ command: 'cairn:milestone-plan', args: '' })
    expect(runOf('single-in-progress')).toEqual({ command: 'cairn:milestone-implement', args: 'M002' })
  })

  for (const surface of SURFACES) {
    test(`a second press during a held run reaches no second run (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      let release = () => {}
      copy.runHold = new Promise<void>(resolve => {
        release = resolve
      })
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const first = ui.press({ key: PANE_NEXT })
      try {
        for (let i = 0; i < 200 && (copy.commands ?? []).length === 0; i++) await new Promise(resolve => setTimeout(resolve, 5))
        expect(copy.commands).toEqual([runOf('single-in-progress')])
        await ui.press({ key: PANE_NEXT })
        expect(copy.commands).toEqual([runOf('single-in-progress')])
      } finally {
        release()
        await first
      }
      // The settled run frees the Button, so the next press runs again
      // (M218 review).
      copy.runHold = undefined
      await ui.press({ key: PANE_NEXT })
      expect(copy.commands).toEqual([runOf('single-in-progress'), runOf('single-in-progress')])
      await ui.unmount()
    })
  }
})

describe('the Next command gives way before the Button (M218 AC4)', () => {
  for (const surface of SURFACES) {
    test(`the Button's Box does not shrink, and the command's does (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const action = (await boxOf(ui, 'next-action')) as Element
      expect(action.props.flexShrink).toBe(0)
      const command = (await boxOf(ui, 'next-text')) as Element
      expect([command.props.flexShrink, command.props.minWidth]).toEqual([1, 0])
      await ui.unmount()
    })
  }
})

// M219: the Next line's Status Button, the Clear Button it carried until
// M241, and the first line's ⌂ (M241) and ↻ (M236), with their keys and
// labels written out by hand.
const PANE_STATUS = 'cairn-pane-status'
const PANE_CLEAR = 'cairn-pane-clear'
const PANE_HOME = 'cairn-pane-home'
const PANE_REFRESH = 'cairn-pane-refresh'
const STATUS_RUN = { command: 'cairn:milestone', args: '' }
const CLEAR_RUN = { command: 'clear', args: '' }

// The keys of the Next line's Buttons, in order, or null with no Next line.
async function nextKeys(ui: Ui): Promise<string[] | null> {
  const line = await boxOf(ui, 'next')
  return line === undefined ? null : buttonsIn(line).map(button => keyOf(button) as string)
}

// A cairn skill runs and its Stop ends the step, which leaves `ended` set.
async function endSkill($) {
  await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
  await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
}

describe('the Next line carries the Status Button after Next (M219 AC1)', () => {
  for (const name of WITH_ROADMAP) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
        expect(await ui.findAll({ key: PANE_CLEAR })).toEqual([])
        // No other line of the pane carries a Button (M219 review), but for
        // the ⌂ and ↻ on the first line (M236, M241) and the ✎ of each
        // candidate line with a short title (M242). Before any read, no
        // blocked line carries one.
        const candidates = FIXTURES[name].pane.length === 0 ? drawnCandidates(name) : []
        const plans = candidates.flatMap(({ row, i }) => (row.title === '' ? [] : [`cairn-pane-plan-${i}`]))
        expect((await ui.findAll({ type: 'Button' })).map(keyOf)).toEqual([PANE_HOME, PANE_REFRESH, PANE_NEXT, PANE_STATUS, ...plans])
        const [status] = await ui.findAll({ key: PANE_STATUS })
        expect([status.props.variant, status.props.label]).toEqual(['secondary', 'Status'])
        // The Buttons come after the command, each in its own Box.
        const line = (await boxOf(ui, 'next')) as Element
        expect(kids(line).map(keyOf)).toEqual(['next-lead', 'next-text', 'next-action', 'next-status'])
        await ui.unmount()
      })
    }
  }
})

// Until M241 a skill's end added Clear before Status. The pane now draws no
// Clear at any of these points, and the band's Clear is as its own tests
// assert (M241 AC4).
describe('a running skill hides Status, and its end adds no Clear (M219 AC2, M241 AC4)', () => {
  for (const surface of SURFACES) {
    test(`skill prompt, Stop, then an idle typed prompt (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
      await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
      expect(await ui.findAll({ key: PANE_STATUS })).toEqual([])
      expect(await ui.findAll({ key: PANE_CLEAR })).toEqual([])
      await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
      expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
      expect(await ui.findAll({ key: PANE_CLEAR })).toEqual([])
      await $.prompt.submit({ text: 'a typed prompt', wait: false, origin: { kind: 'composer' } })
      expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
      expect(await ui.findAll({ key: PANE_CLEAR })).toEqual([])
      await ui.unmount()
    })
  }

  test('paneLines gives the Next line Status alone while it acts', () => {
    const state: PaneState = {
      found: true,
      milestones: [],
      next: { action: 'plan the next milestone', command: '/milestone-plan', id: null, title: null, waiting: [] },
      workable: [],
      waiting: [],
      candidates: [],
      blocked: [],
      taken: [],
    }
    expect(layout(state, [], true).find(line => line.key === 'next')?.buttons).toEqual(['status'])
  })
})

describe('a press of Status runs its command (M219 AC3)', () => {
  for (const surface of SURFACES) {
    test(`Status runs the status skill (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      await ui.press({ key: PANE_STATUS })
      expect(copy.commands).toEqual([STATUS_RUN])
      await ui.unmount()
    })

    test(`a Status press while a Next run is held runs nothing (${surface})`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      let release = () => {}
      copy.runHold = new Promise<void>(resolve => {
        release = resolve
      })
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const first = ui.press({ key: PANE_NEXT })
      try {
        for (let i = 0; i < 200 && (copy.commands ?? []).length === 0; i++) await new Promise(resolve => setTimeout(resolve, 5))
        expect(copy.commands).toEqual([runOf('single-in-progress')])
        await ui.press({ key: PANE_STATUS })
        expect(copy.commands).toEqual([runOf('single-in-progress')])
      } finally {
        release()
        await first
      }
      await ui.unmount()
    })
  }
})

// The pane fixtures whose next action is planning or implement (M221 AC1,
// AC2).
const PANE_CLEAR_FIRST = WITH_ROADMAP.filter(name => CLEARS_FIRST.includes(FIXTURES[name].next?.action as string))

describe("the pane's Plan and Implement run /clear and then their command (M221 AC1, AC2)", () => {
  test('the cases reach both actions', () => {
    expect([...new Set(PANE_CLEAR_FIRST.map(name => FIXTURES[name].next?.action))].sort()).toEqual([...CLEARS_FIRST].sort())
  })

  for (const name of PANE_CLEAR_FIRST) {
    for (const surface of SURFACES) {
      test(`${name}: clear, no second press adds a run, then the command at the clear's end (${surface})`, async ($, on) => {
        const copy = copyOf(name)
        seat(on, copy)
        await $.turn.complete(turn())
        // Every action Button is pressed below, ⌂ among them (M241), after
        // a skill's Stop, as before M241 (M241 review).
        await endSkill($)
        const ui = await mountPane($, surface)
        expect(await nextKeys(ui)).toEqual([PANE_NEXT, PANE_STATUS])
        const [next] = await ui.findAll({ key: PANE_NEXT })
        expect(next.props.label).toBe(ACTION_LABELS[FIXTURES[name].next?.action as string])
        await ui.press({ key: PANE_NEXT })
        expect(copy.commands).toEqual([CLEAR_RUN])
        for (const key of [PANE_NEXT, PANE_HOME, PANE_STATUS]) await ui.press({ key })
        await untilRuns(copy, 2, 10)
        expect(copy.commands).toEqual([CLEAR_RUN])
        await $.session.end(CLEAR_END)
        await untilRuns(copy, 2)
        expect(copy.commands).toEqual([CLEAR_RUN, runOf(name)])
        await ui.unmount()
      })
    }
  }

  // M221 review: a refused clear in the pane runs nothing at the clear's
  // end, and the toast names /clear, as on the band.
  for (const surface of SURFACES) {
    test(`all-waiting: a refused clear runs nothing at the clear's end (${surface})`, async ($, on) => {
      const copy = copyOf('all-waiting')
      copy.runThrows = 'no such command here'
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      await ui.press({ key: PANE_NEXT })
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([CLEAR_RUN])
      expect(copy.toasts?.length).toBe(1)
      expect(copy.toasts?.[0]).toMatch(/^cairn: .* \(\/clear\)$/)
      await ui.unmount()
    })
  }
})

// M241: the first line's ⌂, written out by hand.
const HOME = '⌂'

// The first line's key for a fixture with a ROADMAP: the card's first line
// since M286, with or without an active milestone. Before M286 it was the
// first milestone's head line, or `no-active`.
function firstKey(_name: string): string {
  return 'card-repo'
}

// Waits up to `tries` waits of 5 ms for the opens beneath the mod to reach
// `n`, and then once more, so an unawaited open lands (M241).
async function untilOpens(copy: Copy, n: number, tries = 200) {
  for (let i = 0; i < tries && copy.opens.length < n; i++) await new Promise(resolve => setTimeout(resolve, 5))
  await new Promise(resolve => setTimeout(resolve, 5))
}

describe('the first line carries ⌂ before ↻ while no cairn skill runs (M241 AC1)', () => {
  for (const name of ['single-in-progress', 'no-active']) {
    for (const surface of SURFACES) {
      test(`${name}: ⌂ then ↻, and ↻ alone while a skill runs (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        const key = firstKey(name)
        const first = (await boxOf(ui, key)) as Element
        expect(buttonsIn(first).map(keyOf)).toEqual([PANE_HOME, PANE_REFRESH])
        expect(kids(first).map(keyOf).slice(-2)).toEqual([`${key}-home`, `${key}-refresh`])
        expect((await boxOf(ui, `${key}-home`))?.props.flexShrink).toBe(0)
        const [home] = await ui.findAll({ key: PANE_HOME })
        expect([home.props.variant, home.props.label]).toEqual(['secondary', HOME])
        await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
        expect(buttonsIn((await boxOf(ui, key)) as Element).map(keyOf)).toEqual([PANE_REFRESH])
        expect(await ui.findAll({ key: PANE_HOME })).toEqual([])
        await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
        expect(buttonsIn((await boxOf(ui, key)) as Element).map(keyOf)).toEqual([PANE_HOME, PANE_REFRESH])
        await ui.unmount()
      })
    }
  }

  test('paneLines gives the first line home and refresh while it acts, and refresh alone otherwise', () => {
    const state: PaneState = {
      found: true,
      milestones: [],
      next: null,
      workable: [],
      waiting: [],
      candidates: [],
      blocked: [],
      taken: [],
    }
    expect(layout(state, [], true)[0]).toMatchObject({ key: 'card-repo', buttons: ['home', 'refresh'] })
    expect(layout(state, [], false)[0]).toMatchObject({ key: 'card-repo', buttons: ['refresh'] })
    // The no-active line follows the card and carries no Button (M286).
    expect(layout(state, [], true).find(line => line.key === 'no-active')?.buttons).toBe(undefined)
  })
})

describe('a press of ⌂ runs /clear once, and a guarded press runs nothing (M241 AC2)', () => {
  // On a milestone's head line and on the `no active milestone` line.
  for (const name of ['single-in-progress', 'no-active']) {
    test(`${name}: a free press runs clear with empty args`, async ($, on) => {
      const copy = copyOf(name)
      seat(on, copy)
      await $.turn.complete(turn())
      await pressKey($, PANE_HOME)
      expect(copy.commands).toEqual([CLEAR_RUN])
    })
  }

  // single-in-progress's Next is `Resume`, which runs its command with no
  // `/clear` first, so both presses hold a run in flight.
  for (const [label, key, want] of [
    ['Status', PANE_STATUS, STATUS_RUN],
    ['Resume', PANE_NEXT, runOf('single-in-progress')],
  ] as const) {
    test(`a press while a ${label} run is in flight runs nothing`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      let release = () => {}
      copy.runHold = new Promise<void>(resolve => {
        release = resolve
      })
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      const first = ui.press({ key })
      try {
        for (let i = 0; i < 200 && (copy.commands ?? []).length === 0; i++) await new Promise(resolve => setTimeout(resolve, 5))
        expect(copy.commands).toEqual([want])
        await ui.press({ key: PANE_HOME })
        expect(copy.commands).toEqual([want])
      } finally {
        release()
        await first
      }
      await ui.unmount()
    })
  }

  // One fixture for each held next step, `Plan` and `Implement`.
  const HELD = CLEARS_FIRST.map(action => PANE_CLEAR_FIRST.find(name => FIXTURES[name].next?.action === action) as string)
  test('the held cases reach both Plan and Implement', () => {
    expect(HELD.map(name => ACTION_LABELS[FIXTURES[name].next?.action as string]).sort()).toEqual(['Implement', 'Plan'])
  })

  for (const name of HELD) test(`${name}: a press while its command is held runs nothing`, async ($, on) => {
    const copy = copyOf(name)
    seat(on, copy)
    await $.turn.complete(turn())
    await pressKey($, PANE_NEXT)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await pressKey($, PANE_HOME)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    // The held command's end runs it, and opens no pane for a ⌂ press.
    const before = copy.opens.length
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2)
    expect(copy.commands).toEqual([CLEAR_RUN, runOf(name)])
    expect(copy.opens.length).toBe(before)
  })

  // Two presses in the same tick: the mark is set before the press's first
  // await, so only one passes (M241 review, PR #251).
  test('two presses at once run clear once', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await Promise.all([ui.press({ key: PANE_HOME }), ui.press({ key: PANE_HOME })])
    await ui.unmount()
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
  })

  test('a second press, or a Status press, before the first press ends runs nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.turn.complete(turn())
    await pressKey($, PANE_HOME)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await pressKey($, PANE_HOME)
    await pressKey($, PANE_STATUS)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    // The end frees the Buttons again.
    await $.session.end(CLEAR_END)
    await pressKey($, PANE_STATUS)
    expect(copy.commands).toEqual([CLEAR_RUN, STATUS_RUN])
  })
})

describe("a ⌂ press's /clear opens the pane at its end, and nothing else does (M241 AC3)", () => {
  // The pane is open and sits behind another pane's tab, so the open shows.
  async function homeReady($, on) {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    copy.hidden = [PANE]
    return copy
  }

  // The fake `ui.open` shows a hidden pane, so the check below holds the
  // mod to the open call, not to what the desktop app does with it.
  test('a clear end after a press opens the pane once', async ($, on) => {
    const copy = await homeReady($, on)
    const before = copy.opens.length
    await pressKey($, PANE_HOME)
    expect(copy.opens.length).toBe(before)
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 1)
    expect(copy.opens.slice(before)).toEqual([{ id: PANE, title: 'cairn' }])
    expect(panesOf(copy).find(each => each.id === PANE)?.isShown).toBe(true)
    // A later clear end opens nothing more.
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 2, 10)
    expect(copy.opens.length).toBe(before + 1)
  })

  // `other` also marks a reopen (M222), so `resume` is checked too (M241
  // review).
  for (const reason of ['other', 'resume'] as const) {
    test(`an end with reason ${reason} after a press opens nothing`, async ($, on) => {
      const copy = await homeReady($, on)
      const before = copy.opens.length
      await pressKey($, PANE_HOME)
      await $.session.end({ reason, sessionId: 's1' })
      await untilOpens(copy, before + 1, 10)
      expect(copy.opens.length).toBe(before)
    })
  }

  test('a refused clear leaves no open for a later clear end', async ($, on) => {
    const copy = await homeReady($, on)
    copy.runThrows = 'no such command here'
    const before = copy.opens.length
    await pressKey($, PANE_HOME)
    expect(copy.commands).toEqual([CLEAR_RUN])
    expect(copy.toasts?.[0]).toMatch(/^cairn: .* \(\/clear\)$/)
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 1, 10)
    expect(copy.opens.length).toBe(before)
  })

  test('a clear end with no press opens nothing', async ($, on) => {
    const copy = await homeReady($, on)
    const before = copy.opens.length
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 1, 10)
    expect(copy.opens.length).toBe(before)
  })
})

// A candidate line's ✎ (M242). The candidates fixture with three more rows
// at its end: one whose short title is empty, and two that share a title.
// The fixture's rows 2 and 12 also share the title `Low row` (M251).
const PANE_PLAN = 'cairn-pane-plan'
const PLAN_MARK = '✎'
const PLAN_COMMAND = 'cairn:milestone-plan'
const EMPTY_AT = 15
const SAME_AT = [16, 17]
function candidatesPlus(): Copy {
  const copy = copyOf('candidates')
  const path = Object.keys(copy.files).find(each => each.endsWith('cairn/ROADMAP.md')) as string
  copy.files[path] = copy.files[path].replace(
    '\n## Notes',
    '- : an empty short title — added 2026-01-10\n- Same title: one — added 2026-01-11\n- Same title: two — added 2026-01-12\n\n## Notes',
  )
  return copy
}
// The same copy with its one planned row done, so its Next is `Plan`.
function candidatesPlanNext(): Copy {
  const copy = candidatesPlus()
  const path = Object.keys(copy.files).find(each => each.endsWith('cairn/ROADMAP.md')) as string
  copy.files[path] = copy.files[path].replace('| M031 | Next up | planned |', '| M031 | Next up | done |')
  return copy
}
const TITLES = [...CANDIDATE_LINES.map(text => text.slice(2)), '', 'Same title', 'Same title']

describe('each candidate line with a short title carries ✎ while no cairn skill runs (M242 AC1)', () => {
  // The reader's lines for the copy, so the titles below are read, not
  // assumed (M242 review).
  test('the extra rows read as planned: an empty title and two equal ones', async ($, on) => {
    seat(on, candidatesPlus())
    await $.turn.complete(turn())
    const lines = await paneLines($, 'desktop')
    // The three extra rows are normal, so they draw after row 14 and before
    // the two low rows (M280).
    const order = [...CANDIDATE_ORDER.slice(0, -2), 15, 16, 17, ...CANDIDATE_ORDER.slice(-2)]
    const keys = keysLike(lines, /^candidate-\d+$/)
    expect(keys).toEqual(order.map(i => `candidate-${i}`))
    const rows = keys.map(k => textAt(lines, k))
    expect(rows).toEqual(order.map(i => [...CANDIDATE_LINES, '○ ', '○ Same title', '○ Same title'][i]))
    expect(rows.map(text => (text as string).slice(2))).toEqual(order.map(i => TITLES[i]))
  })

  for (const surface of SURFACES) {
    test(`✎ on each line with a title, none on the empty one, none while a skill runs (${surface})`, async ($, on) => {
      seat(on, candidatesPlus())
      await $.turn.complete(turn())
      const ui = await mountPane($, surface)
      const planKeys = async () => {
        const out: string[][] = []
        for (let i = 0; i < TITLES.length; i++) out.push(buttonsIn((await boxOf(ui, `candidate-${i}`)) as Element).map(keyOf) as string[])
        return out
      }
      const want = TITLES.map((title, i) => (title === '' ? [] : [`${PANE_PLAN}-${i}`]))
      expect(await planKeys()).toEqual(want)
      // The two rows with one title draw two keys.
      expect(new Set(SAME_AT.map(i => want[i][0])).size).toBe(2)
      for (const button of await ui.findAll({ type: 'Button' })) {
        if (!(keyOf(button) ?? '').startsWith(`${PANE_PLAN}-`)) continue
        expect([button.props.variant, button.props.label]).toEqual(['secondary', PLAN_MARK])
      }
      await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
      expect(await planKeys()).toEqual(TITLES.map(() => []))
      await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
      expect(await planKeys()).toEqual(want)
      await ui.unmount()
    })
  }

  test('paneLines gives plan, the index, and the title to each titled row while it acts, and nothing otherwise', () => {
    const state: PaneState = {
      found: true,
      milestones: [],
      next: null,
      workable: [],
      waiting: [],
      candidates: [
        { priority: 'high', title: 'High', text: 'High' },
        { priority: 'normal', title: 'Normal', text: 'Normal' },
        { priority: 'low', title: 'Low', text: 'Low' },
        { priority: 'normal', title: '', text: '' },
      ],
      blocked: [],
      taken: [],
    }
    const rows = (acts: boolean) => layout(state, [], acts).filter(line => /^candidate-\d+$/.test(line.key))
    // The untitled normal row draws before the low row (M280).
    expect(rows(true).map(line => [line.buttons, line.target, line.title])).toEqual([
      [['plan'], '0', 'High'],
      [['plan'], '1', 'Normal'],
      [undefined, undefined, undefined],
      [['plan'], '2', 'Low'],
    ])
    expect(rows(false).map(line => [line.key, line.buttons, line.target, line.title])).toEqual([
      ['candidate-0', undefined, undefined, undefined],
      ['candidate-1', undefined, undefined, undefined],
      ['candidate-3', undefined, undefined, undefined],
      ['candidate-2', undefined, undefined, undefined],
    ])
  })
})

describe("a press of ✎ runs /clear, and /cairn:milestone-plan with the row's title at its end (M242 AC2)", () => {
  // A high, a low, the backtick row, and the second of the two equal titles.
  for (const i of [0, 2, 8, SAME_AT[1]]) {
    test(`row ${i}: clear first, then the plan with the title`, async ($, on) => {
      const copy = candidatesPlus()
      seat(on, copy)
      await $.turn.complete(turn())
      await pressKey($, `${PANE_PLAN}-${i}`)
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([CLEAR_RUN])
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 2)
      expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args: TITLES[i] }])
    })
  }
})

// The copy's first row gains a counted started token, so it is hidden, and
// a press on the row after it plans that row's own title (M261 AC3).
describe('a ✎ press on a line drawn after a hidden row plans its own row (M261 AC3)', () => {
  test('the hidden row draws no line or ✎, and the next row plans its title', async ($, on) => {
    const copy = candidatesPlus()
    const path = Object.keys(copy.files).find(each => each.endsWith('cairn/ROADMAP.md')) as string
    copy.files[path] = copy.files[path].replace(
      '- [high] High row: the text after the first colon and space is not shown — added 2026-01-01',
      '- [high] High row: the text after the first colon and space is not shown — added 2026-01-01 — started M031',
    )
    expect(copy.files[path]).toContain('— started M031')
    seat(on, copy)
    await $.turn.complete(turn())
    const keys = await keysOf($)
    expect(keys.filter(key => /^candidate-\d+$/.test(key))[0]).toBe('candidate-1')
    expect(keys).not.toContain('candidate-0')
    await pressKey($, `${PANE_PLAN}-1`)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2)
    expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args: TITLES[1] }])
    expect(TITLES[1]).toBe('Normal row')
  })
})

describe('a guarded ✎ press runs nothing (M242 AC3)', () => {
  test('a press while a Status run is in flight runs nothing', async ($, on) => {
    const copy = candidatesPlus()
    let release = () => {}
    copy.runHold = new Promise<void>(resolve => {
      release = resolve
    })
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    const first = ui.press({ key: PANE_STATUS })
    try {
      for (let i = 0; i < 200 && (copy.commands ?? []).length === 0; i++) await new Promise(resolve => setTimeout(resolve, 5))
      expect(copy.commands).toEqual([STATUS_RUN])
      await ui.press({ key: `${PANE_PLAN}-0` })
      expect(copy.commands).toEqual([STATUS_RUN])
    } finally {
      release()
      await first
    }
    await ui.unmount()
  })

  test('a press while a Plan command is held runs nothing, and the held Plan runs at the end', async ($, on) => {
    const copy = candidatesPlanNext()
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    const [next] = await ui.findAll({ key: PANE_NEXT })
    expect(next.props.label).toBe('Plan')
    await ui.unmount()
    await pressKey($, PANE_NEXT)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await pressKey($, `${PANE_PLAN}-0`)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2)
    // The copy's first candidate row is `[high] High row`, which the held
    // Plan names (M272).
    expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args: 'High row' }])
  })

  test('a press while a ⌂ press is pending runs nothing, and the end opens the pane only', async ($, on) => {
    const copy = candidatesPlus()
    seat(on, copy)
    await $.turn.complete(turn())
    await pressKey($, PANE_HOME)
    expect(copy.commands).toEqual([CLEAR_RUN])
    await pressKey($, `${PANE_PLAN}-0`)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    const before = copy.opens.length
    await $.session.end(CLEAR_END)
    await untilOpens(copy, before + 1)
    expect(copy.opens.length).toBe(before + 1)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
  })

  test('two presses at once run clear once', async ($, on) => {
    const copy = candidatesPlus()
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await Promise.all([ui.press({ key: `${PANE_PLAN}-0` }), ui.press({ key: `${PANE_PLAN}-1` })])
    await ui.unmount()
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    // The first press's title runs, not the second's (M242 review).
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2)
    expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args: TITLES[0] }])
  })

  // A refused `/clear` drops the hold, so a later clear end runs no plan,
  // and the next press is free (M242 review).
  test('a refused clear drops the held plan', async ($, on) => {
    const copy = candidatesPlus()
    copy.runThrows = 'no such command here'
    seat(on, copy)
    await $.turn.complete(turn())
    await pressKey($, `${PANE_PLAN}-1`)
    expect(copy.commands).toEqual([CLEAR_RUN])
    expect(copy.toasts?.[0]).toMatch(/^cairn: .* \(\/clear\)$/)
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([CLEAR_RUN])
    copy.runThrows = undefined
    await pressKey($, `${PANE_PLAN}-2`)
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 3)
    expect(copy.commands).toEqual([CLEAR_RUN, CLEAR_RUN, { command: PLAN_COMMAND, args: TITLES[2] }])
  })
})

describe('✎ sits at the right end of a candidate line, and the title gives way (M242 AC4)', () => {
  for (const surface of SURFACES) {
    // Row 1's title is short, and row 7's is longer than 44 columns.
    for (const i of [1, 7]) {
      test(`row ${i} at 44 columns (${surface})`, async ($, on) => {
        seat(on, candidatesPlus())
        await $.turn.complete(turn())
        const ui = await mountPane($, surface, 44)
        const text = (await boxOf(ui, `candidate-${i}-text`)) as Element
        expect([text.props.flexGrow, text.props.minWidth]).toEqual([1, 0])
        expect(kids(text)[0].props.wrap).toBe('truncate-end')
        if (i === 7) expect(width(textOf(kids(text)[0]))).toBeGreaterThan(44)
        const line = (await boxOf(ui, `candidate-${i}`)) as Element
        // The hover card's Box, which has no key, sits last on the desktop
        // (M286), and there ✎ sits in an unkeyed Box just before it (M290).
        const keyed = kids(line).map(keyOf).filter(key => key !== undefined)
        if (surface === 'terminal') {
          expect(keyed.slice(-2)).toEqual([`candidate-${i}-text`, `candidate-${i}-plan`])
          expect((await boxOf(ui, `candidate-${i}-plan`))?.props.flexShrink).toBe(0)
        } else {
          expect(keyed.slice(-1)).toEqual([`candidate-${i}-text`])
          expect(holderOf(line, `${PANE_PLAN}-${i}`)?.props.flexShrink).toBe(0)
          expect(kids(line).at(-2)).toBe(holderOf(line, `${PANE_PLAN}-${i}`))
        }
        await ui.unmount()
      })
    }
  }
})

describe('the desktop shows a candidate line’s ✎ only under the pointer, and the terminal at rest (M290)', () => {
  // AC1, AC2: every candidate line that carries ✎ in these fixtures.
  for (const name of ['candidates', 'candidates-order']) {
    for (const surface of SURFACES) {
      test(`${name} (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        const rows = drawnCandidates(name).filter(({ row }) => row.title !== '')
        expect(rows.length).toBeGreaterThan(1)
        for (const { i } of rows) {
          const line = (await boxOf(ui, `candidate-${i}`)) as Element
          const holder = holderOf(line, `${PANE_PLAN}-${i}`) as Element
          expect(kids(line)).toContain(holder)
          if (surface === 'terminal') {
            expect(keyOf(holder)).toBe(`candidate-${i}-plan`)
            expect([holder.props.flexShrink, holder.props.display]).toEqual([0, undefined])
            // AC2: no hover and no icon under the line on the terminal.
            const all: Element[] = []
            const walk = (node: Element) => kids(node).forEach(child => (all.push(child), walk(child)))
            walk(line)
            expect(all.length).toBeGreaterThan(2)
            expect(all.filter(node => (node as Element & { hover?: unknown }).hover !== undefined)).toEqual([])
            expect(all.filter(node => node.type === 'Svg')).toEqual([])
          } else {
            // Parked past the edge, never `display: 'none'`, whose Button
            // takes no click in the desktop app (M290 live look).
            expect(keyOf(holder)).toBeUndefined()
            expect(holder.props.display).toBeUndefined()
            expect(holder.props.position).toBe('absolute')
            expect(holder.props.right as number).toBeLessThan(0)
            // It spans the row and centers ✎, as the row centers ⓘ.
            expect([holder.props.top, holder.props.bottom, holder.props.alignItems]).toEqual([0, 0, 'center'])
            // The drawn tree keeps `hover` beside `props` (M286).
            expect((holder as Element & { hover?: unknown }).hover).toEqual({ right: 0 })
          }
        }
        await ui.unmount()
      })
    }
  }

  // AC5: on the desktop the info glyph, hidden just before ✎, names the one
  // hover group that opens the line's card; other lines' cards keep theirs.
  const hoverOf = (node: Element | undefined) => (node as (Element & { hover?: unknown }) | undefined)?.hover
  for (const name of ['candidates', 'candidates-order']) {
    test(`${name}: the info glyph opens the card (desktop)`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      const ui = await mountPane($, 'desktop')
      const rows = drawnCandidates(name).filter(({ row }) => row.title !== '')
      expect(rows.length).toBeGreaterThan(1)
      const scopes: unknown[] = []
      for (const { i } of rows) {
        const line = (await boxOf(ui, `candidate-${i}`)) as Element
        const parts = kids(line)
        const info = parts[parts.indexOf(holderOf(line, `${PANE_PLAN}-${i}`) as Element) - 1]
        expect(keyOf(info)).toBeUndefined()
        expect(info.props.display).toBe('none')
        expect(hoverOf(info)).toEqual({ display: 'flex' })
        expect(kids(info).length).toBe(1)
        const group = kids(info)[0]
        const scope = (hoverOf(group) as { scope?: unknown } | undefined)?.scope
        expect(typeof scope).toBe('string')
        expect(group.type).toBe('Text')
        expect(hoverOf(group)).toEqual({ scope, bold: true })
        expect(textOf(group)).toBe(INFO_LABEL)
        // The glyph keeps room on its right for the parked ✎ to move into.
        expect(info.props.marginRight as number).toBeGreaterThan(0)
        const cards = parts.filter(isCard)
        expect(cards.length).toBe(1)
        expect(hoverOf(cards[0])).toEqual({ display: 'flex', scope })
        scopes.push(scope)
      }
      expect(new Set(scopes).size).toBe(scopes.length)
      await ui.unmount()
    })
  }
  // M290 review: while a cairn skill runs, a candidate line keeps its ⓘ, so
  // its card stays in reach, with no ✎ and no room kept for one.
  test('while a skill runs, ⓘ shows alone with no margin (desktop)', async ($, on) => {
    seat(on, copyOf('candidates'))
    await $.turn.complete(turn())
    await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
    const ui = await mountPane($, 'desktop')
    const rows = drawnCandidates('candidates').filter(({ row }) => row.title !== '')
    expect(rows.length).toBeGreaterThan(1)
    for (const { i } of rows) {
      const line = (await boxOf(ui, `candidate-${i}`)) as Element
      expect(holderOf(line, `${PANE_PLAN}-${i}`)).toBeUndefined()
      const infos = kids(line).filter(child => kids(child).some(node => node.type === 'Text' && textOf(node) === INFO_LABEL))
      expect(infos.length).toBe(1)
      expect([infos[0].props.display, infos[0].props.marginRight]).toEqual(['none', 0])
    }
    await ui.unmount()
  })

  for (const name of ['pane-full', 'candidates']) {
    test(`${name}: a card on a line that is not a candidate line opens from the whole line (desktop)`, async ($, on) => {
      seat(on, copyOf(name))
      await $.turn.complete(turn())
      const ui = await mountPane($, 'desktop')
      const [root] = await ui.findAll({ key: 'cairn-pane' })
      const cards = flat(root)
        .filter(line => !/^candidate-\d+$/.test(keyOf(line) ?? ''))
        .flatMap(line => kids(line).filter(isCard))
      expect(cards.length).toBeGreaterThan(0)
      for (const card of cards) expect(hoverOf(card)).toEqual({ display: 'flex' })
      await ui.unmount()
    })
  }

  // AC3: a press of a parked ✎ plans its row as on the terminal.
  for (const surface of SURFACES) {
    for (const [i, title] of [[2, 'Late high'], [3, 'Second low']] as [number, string][]) {
      test(`✎ on row ${i} plans ${title} (${surface})`, async ($, on) => {
        const copy = copyOf('candidates-order')
        seat(on, copy)
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        await ui.press({ key: `${PANE_PLAN}-${i}` })
        await ui.unmount()
        expect(copy.commands).toEqual([CLEAR_RUN])
        await $.session.end(CLEAR_END)
        await untilRuns(copy, 2)
        expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args: title }])
      })
    }
  }

  // AC4: no other Button's Box is drawn hidden.
  const others = (root: Element) =>
    flat(root).flatMap(line => {
      const out: Element[] = []
      const walk = (node: Element) => {
        for (const child of kids(node)) {
          const key = keyOf(child)
          if (child.type === 'Button' && !key?.startsWith(`${PANE_PLAN}-`)) out.push(holderOf(node, key as string) as Element)
          walk(child)
        }
      }
      walk(line)
      return out
    })
  for (const name of ['pane-full', 'candidates']) {
    for (const surface of SURFACES) {
      test(`${name}: no other Button is hidden (${surface})`, async ($, on) => {
        seat(on, copyOf(name))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        const [root] = await ui.findAll({ key: 'cairn-pane' })
        const boxes = others(root)
        expect(boxes.length).toBeGreaterThan(1)
        for (const box of boxes) expect(box.props.display).toBeUndefined()
        await ui.unmount()
      })
    }
  }
  test('blocked-prs: a merged line’s Finish is not hidden', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await ghSettled()
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    const [root] = await ui.findAll({ key: 'cairn-pane' })
    const finishes = others(root).filter(box => kids(box).some(b => keyOf(b)?.startsWith('cairn-pane-finish-')))
    expect(finishes.length).toBeGreaterThan(0)
    for (const box of finishes) expect(box.props.display).toBeUndefined()
    await ui.unmount()
  })
})

describe('the Next command gives way before Status (M219 AC4)', () => {
  for (const surface of SURFACES) {
    test(`the Button's Box does not shrink, and the command's does (${surface})`, async ($, on) => {
      seat(on, copyOf('single-in-progress'))
      await $.turn.complete(turn())
      await endSkill($)
      const ui = await mountPane($, surface)
      for (const key of ['next-status']) {
        const box = (await boxOf(ui, key)) as Element
        expect([key, box.props.flexShrink]).toEqual([key, 0])
      }
      const command = (await boxOf(ui, 'next-text')) as Element
      expect([command.props.flexShrink, command.props.minWidth]).toEqual([1, 0])
      await ui.unmount()
    })
  }
})

// M002's task T2 is open in the fixture, and each case ticks it before the
// event, so the drawing after the event shows it checked.
const M002 = '/cairn/milestones/M002-export.md'
// T2 is the in-progress M002's first open task, so it draws `⊙` (M286).
const T2_OPEN = `⊙  T2: Write the command.`
const T2_DONE = `${CHECKED_MARK}  T2: Write the command.`
const tick = (copy: Copy) => {
  copy.files[M002] = copy.files[M002].replace('- [ ] T2:', '- [x] T2:')
}

type Event = { name: string; before?: ($) => Promise<void>; act: ($) => Promise<void> }

const EVENTS: Event[] = [
  { name: 'session start', act: $ => $.session.start({ cwd: '/', surface: 'terminal', isInteractive: true }) },
  { name: 'turn end', act: $ => $.turn.complete(turn()) },
  // A press of a Clear Button raises no `session.start`, only this (M222).
  { name: 'session start after a clear', act: $ => $.classic.SessionStart({ source: 'clear' }) },
  { name: 'cairn skill prompt', act: $ => $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' }) },
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
    // One pane stays mounted across the event, so the case shows that the
    // drawing already open changes, not only a new one (M205 review).
    test(`the ${event.name} shows an edit made before it`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      if (event.before !== undefined) await event.before($)
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...PANE_VIEW })) as Ui
      const t2 = async () => textOf((await ui.findAll({ key: 'M002-task-1' }))[0])
      expect(await t2()).toBe(T2_OPEN)
      tick(copy)
      // The edit alone draws nothing new.
      expect(await t2()).toBe(T2_OPEN)
      await event.act($)
      expect(await t2()).toBe(T2_DONE)
      await ui.unmount()
    })
  }
})

// The pane across a `/clear` (M222). A press of a Clear Button ends the
// session with reason `clear` in the same process, and nothing closes the
// pane. A typed `/clear` in the desktop app ends the process with reason
// `other`, and the next process starts with no pane at the first message
// after the clear. Each case answers `$.store` from memory, which outlives
// the process as the engine's store does, and empties the open panes
// between an end and the next start, so it sees only what the mod opens.
// The panes a case reads are what `$.ui.panes()` answers the mod.
const NEW_START = { cwd: '/', surface: 'desktop', isInteractive: true } as const
const listed = (copy: Copy) => copy.open.includes(PANE)
const newProcess = (copy: Copy) => {
  copy.open = []
  copy.hidden = []
  copy.unplaced = []
}

async function openPane($, on, copy: Copy) {
  mock.store(on)
  seat(on, copy)
  await $.session.start(NEW_START)
  await $.command.run({ command: COMMAND })
  expect(listed(copy)).toBe(true)
}

describe('a clear end leaves the pane open (M222 AC1, AC2)', () => {
  const STATES = [
    { name: 'shown', set: (copy: Copy) => copy },
    { name: "behind another pane's tab", set: (copy: Copy) => { copy.hidden = [PANE] } },
    { name: 'waiting undrawn', set: (copy: Copy) => { copy.unplaced = [PANE] } },
  ]
  for (const state of STATES) {
    test(`a pane ${state.name} at a clear end is listed after it`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      await openPane($, on, copy)
      state.set(copy)
      await $.session.end(CLEAR_END)
      expect(copy.closes).toEqual([])
      const mine = panesOf(copy).find(open => open.id === PANE)
      expect(mine).toBeDefined()
      if (state.name === 'shown') {
        expect(mine?.isShown).toBe(true)
        expect(mine?.isPlaced).toBe(true)
      }
    })
  }

  test('a clear end with no pane open leaves none open', async ($, on) => {
    const copy = copyOf('single-in-progress')
    mock.store(on)
    seat(on, copy)
    await $.session.start(NEW_START)
    await $.session.end(CLEAR_END)
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })
})

describe('an end of another kind opens no pane at the next start (M222 AC3)', () => {
  for (const reason of ['resume', 'prompt_input_exit', 'logout'] as const) {
    test(`after a ${reason} end, the next start opens no pane`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      await openPane($, on, copy)
      await $.session.end({ reason, sessionId: 's1' })
      newProcess(copy)
      await $.session.start(NEW_START)
      expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
    })
  }
})

describe('an other end with the pane shown opens it at the next start in the same cwd (M222 AC7)', () => {
  const OTHER_END = { reason: 'other', sessionId: 's1' } as const

  test('the same cwd lists the pane at the next start', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).toContain(PANE)
  })

  test('a shell cd before the end still lists the pane at the next start in the root', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    copy.root = copy.cwd
    copy.cwd = '/sub'
    await $.session.end(OTHER_END)
    newProcess(copy)
    copy.cwd = copy.root
    copy.root = undefined
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).toContain(PANE)
  })

  for (const state of ['hidden', 'unplaced'] as const) {
    test(`a pane ${state} at the end lists none at the next start`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      await openPane($, on, copy)
      copy[state] = [PANE]
      await $.session.end(OTHER_END)
      newProcess(copy)
      await $.session.start(NEW_START)
      expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
    })
  }

  test('a clear end marks nothing for the next start', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(CLEAR_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })

  test('another cwd lists no pane at the next start', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    copy.cwd = '/sub'
    await $.session.start({ ...NEW_START, cwd: '/sub' })
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })

  test('no pane open at the end lists none at the next start', async ($, on) => {
    const copy = copyOf('single-in-progress')
    mock.store(on)
    seat(on, copy)
    await $.session.start(NEW_START)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })

  // A typed `/clear` closes the pane on screen, so a `/cairn-pane` that is
  // the first message after it is a request to open, though the start that
  // message brings has just reopened the pane. It keeps the pane open, and
  // the next one closes it.
  test('a /cairn-pane that is the first message after the reopen keeps the pane open', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(listed(copy)).toBe(true)
    const first = await $.command.run({ command: COMMAND })
    expect(first.text).toBe('cairn pane opened')
    expect(listed(copy)).toBe(true)
    const second = await $.command.run({ command: COMMAND })
    expect(second.text).toBe('cairn pane closed')
    expect(listed(copy)).toBe(false)
  })

  test('after a turn ends, a /cairn-pane closes the reopened pane', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    await $.turn.complete(turn())
    const got = await $.command.run({ command: COMMAND })
    expect(got.text).toBe('cairn pane closed')
    expect(listed(copy)).toBe(false)
  })

  test('a start with no reopen leaves the first /cairn-pane a close of a shown pane', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    const got = await $.command.run({ command: COMMAND })
    expect(got.text).toBe('cairn pane closed')
    expect(listed(copy)).toBe(false)
  })

  test('the reopen happens once: a close and a later exit end list no pane', async ($, on) => {
    const copy = copyOf('single-in-progress')
    await openPane($, on, copy)
    await $.session.end(OTHER_END)
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(listed(copy)).toBe(true)
    await $.turn.complete(turn())
    await $.command.run({ command: COMMAND })
    expect(listed(copy)).toBe(false)
    await $.session.end({ reason: 'prompt_input_exit', sessionId: 's2' })
    newProcess(copy)
    await $.session.start(NEW_START)
    expect(panesOf(copy).map(open => open.id)).not.toContain(PANE)
  })
})

// Each blocked line's pull request state (M224). A case answers the mod's
// `gh pr view` calls from `answer`, by the URL each call names, and records
// each call's argv and each `$.clock` wait the mod asks for. A `reject`
// answer throws, so the engine skips the hook and the mod's call rejects,
// as it does when `gh` cannot start. The words and Buttons each case expects
// are written out by hand.
// Since M237 a github.com URL takes one `gh api graphql` call for its word
// and its count, recorded apart in `graphql`, and only a URL of another
// form takes a `gh pr view` call, in `calls`. The fake answers the graphql
// call by the URL that its owner, repo, and number name, from both
// answers: `answer` gives the word's JSON as `gh pr view` prints it, and
// `graph` the threads, by default a reply with no unresolved thread. A
// rejecting, failing, or non-JSON `answer` is the call's answer as it is.
// A failing `graph` answer stands for threads that fail the shape check, so
// the reply carries the word and no threads. Either answer may be a
// promise, which holds the call until it settles. `reads` holds the URL of
// each pull request read, by either call, in order.
// The `git` calls and the `gh pr list` calls of M226 are recorded apart too,
// in `git` and `lists`. `git` answers from `remotes`, a remote's URL by its
// name, and by default the repo has no remote, so no list call runs.
// `list` answers each `gh pr list` call.
// An open does not wait for the read (M230), so a case waits with
// `settled` until no `process.run` call is in flight at four checks 5 ms
// apart, or until 400 checks (about 2 s) pass. The
// `answer` and `list` answers may be promises too, which hold their calls.
type GhAnswer = { exitCode: number; stdout: string } | 'reject'
type Gh = {
  calls: (readonly string[])[]
  graphql: (readonly string[])[]
  reads: string[]
  git: (readonly string[])[]
  lists: (readonly string[])[]
  clocks: string[]
  // The card's calls (M286): its `gh api graphql` repo query, and its
  // `git describe`, `git log`, and `git diff` calls, kept apart from the
  // lists above.
  card: (readonly string[])[]
  settled: () => Promise<void>
}
// `counts` answers the card's repo query, and `describe`, `log`, and `diff`
// its git calls (M286). By default the query gives 0 and 0, and the git
// calls fail.
type GhRepo = {
  remotes?: Record<string, string>
  list?: () => GhAnswer | Promise<GhAnswer>
  counts?: () => GhAnswer | Promise<GhAnswer>
  describe?: GhAnswer
  log?: GhAnswer
  diff?: GhAnswer
  // The `git rev-parse --git-common-dir` answer (M291).
  common?: GhAnswer
}
// A repo query reply in the shape GitHub returns (M286).
const repoReply = (prs: unknown, issues: unknown): GhAnswer => ({
  exitCode: 0,
  stdout: `${JSON.stringify({ data: { repository: { pullRequests: { totalCount: prs }, issues: { totalCount: issues } } } })}\n`,
})
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))
// The newest `gh` set-up's `settled`, which the drawing helpers below wait
// on before they mount the pane. It holds one set-up only, the newest.
let ghSettled: () => Promise<void> = async () => {}
const URL_1250 = 'https://github.com/upstream/repo/pull/1250'
// A blocked or hotfix line's text, written out by hand (M286): the state
// mark (`○` before a read), the identifier, the title, and after two spaces
// the number, the archived mark, and the word, one space apart.
const PR_MARKS: Record<string, string> = {
  merged: '●',
  approved: '●',
  'changes requested': '▲',
  'in review': '◐',
  closed: '✕',
  unknown: '◌',
}
const prText =(id: string, title: string, n: number | null, word?: string, archived = false) => {
  const tail = [n === null ? null : `#${n}`, archived ? 'archived' : null, word ?? null].filter(part => part !== null)
  return `${word === undefined ? '○' : PR_MARKS[word]} ${id}  ${title}${tail.length === 0 ? '' : `  ${tail.join(' ')}`}`
}
const line1250 = (word?: string) => prText('M111', 'Handed to the maintainers', 1250, word)

// The value of a `name=value` argument in a recorded argv.
const argOf = (argv: readonly string[], name: string) => argv.find(a => a.startsWith(`${name}=`))?.slice(name.length + 1)

function gh(
  on: On,
  answer: (url: string) => GhAnswer | Promise<GhAnswer>,
  graph: (url: string) => GhAnswer | Promise<GhAnswer> = () => countsReply(0),
  repo: GhRepo = {},
): Gh {
  let pending = 0
  const settled = async () => {
    for (let quiet = 0, i = 0; quiet < 4 && i < 400; i++) {
      await sleep(5)
      quiet = pending === 0 ? quiet + 1 : 0
    }
  }
  const out: Gh = { calls: [], graphql: [], reads: [], git: [], lists: [], clocks: [], card: [], settled }
  ghSettled = settled
  const remotes = repo.remotes ?? {}
  const value = (got: { exitCode: number; stdout: string }) => ({
    value: { exitCode: got.exitCode, stdout: got.stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false },
  })
  const failed = { exitCode: 128, stdout: '' }
  const reply = async (e: { argv: readonly string[] }) => {
    if (e.argv[0] === 'git' && ['describe', 'log', 'diff', 'rev-parse'].includes(e.argv[1])) {
      out.card.push(e.argv)
      const got =
        (e.argv[1] === 'describe' ? repo.describe : e.argv[1] === 'log' ? repo.log : e.argv[1] === 'diff' ? repo.diff : repo.common) ??
        failed
      if (got === 'reject') throw new Error('git cannot start')
      return value(got)
    }
    if (e.argv[1] === 'api' && argOf(e.argv, 'number') === undefined) {
      out.card.push(e.argv)
      const got = await (repo.counts ?? (() => repoReply(0, 0)))()
      if (got === 'reject') throw new Error('gh cannot start')
      return value(got)
    }
    if (e.argv[0] === 'git') {
      out.git.push(e.argv)
      if (e.argv[1] === 'remote' && e.argv.length === 2) return value({ exitCode: 0, stdout: Object.keys(remotes).map(n => `${n}\n`).join('') })
      const name = e.argv[3]
      const has = Object.prototype.hasOwnProperty.call(remotes, name)
      return value(has ? { exitCode: 0, stdout: `${remotes[name]}\n` } : { exitCode: 2, stdout: '' })
    }
    if (e.argv[1] === 'pr' && e.argv[2] === 'list') {
      out.lists.push(e.argv)
      const got = await (repo.list ?? (() => ({ exitCode: 0, stdout: '[]\n' })))()
      if (got === 'reject') throw new Error('gh cannot start')
      return value(got)
    }
    const isGraph = e.argv[1] === 'api'
    if (!isGraph) {
      out.calls.push(e.argv)
      out.reads.push(e.argv[3])
      const got = await answer(e.argv[3])
      if (got === 'reject') throw new Error('gh cannot start')
      return value(got)
    }
    out.graphql.push(e.argv)
    const url = `https://github.com/${argOf(e.argv, 'owner')}/${argOf(e.argv, 'repo')}/pull/${argOf(e.argv, 'number')}`
    out.reads.push(url)
    const [word, part] = await Promise.all([answer(url), graph(url)])
    if (word === 'reject') throw new Error('gh cannot start')
    return value(graphReply(word, part))
  }
  on('process.run', async ($, e) => {
    pending += 1
    try {
      return await reply(e)
    } finally {
      pending -= 1
    }
  })
  for (const name of ['clock.sleep', 'clock.after', 'clock.every'] as const) {
    on(name, async () => {
      out.clocks.push(name)
      return { value: undefined }
    })
  }
  return out
}

// One graphql reply from a word answer and a threads answer, as the fake's
// comment above says (M237).
function graphReply(word: { exitCode: number; stdout: string }, part: GhAnswer): { exitCode: number; stdout: string } {
  if (word.exitCode !== 0) return word
  let view: unknown
  try {
    view = JSON.parse(word.stdout)
  } catch {
    return word
  }
  if (view === null || typeof view !== 'object' || Array.isArray(view)) return word
  let threads: unknown
  if (part !== 'reject' && part.exitCode === 0) {
    try {
      threads = (JSON.parse(part.stdout) as { data?: { repository?: { pullRequest?: { reviewThreads?: unknown } } } })?.data?.repository
        ?.pullRequest?.reviewThreads
    } catch {
      threads = undefined
    }
  }
  const pr = threads === undefined ? { ...view } : { ...view, reviewThreads: threads }
  return { exitCode: 0, stdout: `${JSON.stringify({ data: { repository: { pullRequest: pr } } })}\n` }
}

const prView = (state: string, decision?: string) =>
  ({ exitCode: 0, stdout: `${JSON.stringify(decision === undefined ? { state } : { state, reviewDecision: decision })}\n` }) as const

// A `gh api graphql` reply in the shape GitHub returns (M236), with `t`
// unresolved threads and one resolved.
function countsReply(t: number): GhAnswer {
  const pr = { reviewThreads: { nodes: [{ isResolved: true }, ...Array.from({ length: t }, () => ({ isResolved: false }))] } }
  return { exitCode: 0, stdout: `${JSON.stringify({ data: { repository: { pullRequest: pr } } })}\n` }
}

// The pane's line for a key, and the keys of the Buttons on it.
async function blockedView($, key: string): Promise<{ text: string; buttons: string[] }> {
  await ghSettled()
  const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const line = kids(root)
    .flatMap(child => (keyOf(child) === 'cairn-card' ? kids(child) : [child]))
    .find(child => keyOf(child) === key)
  await ui.unmount()
  return {
    text: line === undefined ? '' : textOf(line),
    buttons: line === undefined ? [] : buttonsIn(line).map(b => keyOf(b) ?? ''),
  }
}

describe('each blocked line shows its pull request state (M224 AC1)', () => {
  const SHAPES: { name: string; answer: GhAnswer; word: string }[] = [
    { name: 'MERGED', answer: prView('MERGED', 'APPROVED'), word: 'merged' },
    { name: 'CLOSED', answer: prView('CLOSED', ''), word: 'closed' },
    { name: 'OPEN with CHANGES_REQUESTED', answer: prView('OPEN', 'CHANGES_REQUESTED'), word: 'changes requested' },
    { name: 'OPEN with APPROVED', answer: prView('OPEN', 'APPROVED'), word: 'approved' },
    { name: 'OPEN with REVIEW_REQUIRED', answer: prView('OPEN', 'REVIEW_REQUIRED'), word: 'in review' },
    { name: 'OPEN with an empty decision', answer: prView('OPEN', ''), word: 'in review' },
    { name: 'OPEN with no decision', answer: prView('OPEN'), word: 'in review' },
  ]
  for (const shape of SHAPES) {
    test(`${shape.name} shows \`${shape.word}\``, async ($, on) => {
      const calls = gh(on, () => shape.answer)
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      const opened = await $.command.run({ command: COMMAND })
      expect(opened.text).toBe('cairn pane opened')
      await calls.settled()
      // One graphql call reads the github.com URL, and no `gh pr view` runs
      // (M237 AC4).
      expect(calls.reads).toEqual([URL_1250])
      expect(calls.graphql.length).toBe(1)
      expect(calls.calls).toEqual([])
      expect((await blockedView($, 'blocked-M111')).text).toBe(line1250(shape.word))
    })
  }

  test('a line not yet read shows no state word and no Button', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.reads).toEqual([])
    const line = await blockedView($, 'blocked-M111')
    expect(line.text).toBe(line1250())
    expect(line.buttons).toEqual([])
  })
})

describe('the merged, changes-requested, and closed lines carry a Button (M224 AC2)', () => {
  const BUTTONS = [
    { answer: prView('MERGED', ''), key: 'cairn-pane-finish-M111', command: { command: 'cairn:milestone-review', args: 'M111' } },
    {
      answer: prView('OPEN', 'CHANGES_REQUESTED'),
      key: 'cairn-pane-revise-M111',
      command: { command: 'cairn:milestone-implement', args: 'M111' },
    },
    { answer: prView('CLOSED', ''), key: 'cairn-pane-check-M111', command: { command: 'cairn:milestone', args: '' } },
  ]
  for (const each of BUTTONS) {
    test(`${each.key} runs /${each.command.command} with no /clear first`, async ($, on) => {
      gh(on, () => each.answer)
      const copy = copyOf('blocked-active')
      seat(on, copy)
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      expect((await blockedView($, 'blocked-M111')).buttons).toEqual([each.key])
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      await ui.press({ key: each.key })
      await ui.unmount()
      expect(copy.commands).toEqual([each.command])
    })
  }

  // M246 AC3: a blocked row whose milestone file was archived reads its PR
  // from the archive file. Its line carries `archived` after the number and
  // before the state word, or `archived` alone with no number. A merged one
  // carries the Finish Button for its id. A live row carries no `archived`.
  // The lines are written out by hand from the blocked-archived fixture.
  test('an archived row shows `archived`, its state word, and Finish', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-archived')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const archived = await blockedView($, 'blocked-M202')
    expect(archived.text).toBe(prText('M202', 'The URL on the Status line', 21, 'merged', true))
    expect(archived.buttons).toEqual(['cairn-pane-finish-M202'])
    const bare = await blockedView($, 'blocked-M204')
    expect(bare.text).toBe(prText('M204', 'A URL only in a later paragraph', null, undefined, true))
    expect(bare.buttons).toEqual([])
    const live = await blockedView($, 'blocked-M201')
    expect(live.text).toBe(prText('M201', 'A live file', 11, 'merged'))
    expect((await blockedView($, 'blocked-M206')).text).toBe('○ M206  A dropped archive')
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await ui.press({ key: 'cairn-pane-finish-M202' })
    await ui.unmount()
    expect(copy.commands).toEqual([{ command: 'cairn:milestone-review', args: 'M202' }])
  })

  // M246 review: an archived row carries no Revise or Check, since its
  // milestone file is gone. A live row keeps its Button.
  for (const each of [
    { answer: prView('OPEN', 'CHANGES_REQUESTED'), word: 'changes requested', live: 'cairn-pane-revise-M201' },
    { answer: prView('CLOSED', ''), word: 'closed', live: 'cairn-pane-check-M201' },
  ]) {
    test(`an archived row whose PR reads \`${each.word}\` carries no Button`, async ($, on) => {
      gh(on, () => each.answer)
      seat(on, copyOf('blocked-archived'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      const archived = await blockedView($, 'blocked-M202')
      expect(archived.text).toBe(prText('M202', 'The URL on the Status line', 21, each.word, true))
      expect(archived.buttons).toEqual([])
      expect((await blockedView($, 'blocked-M201')).buttons).toEqual([each.live])
    })
  }

  // A press while a cairn skill's step runs does nothing, as the Next,
  // Status, and Clear presses do (M224 review). The Button stays drawn.
  test('a press while a cairn skill runs runs nothing', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-finish-M111'])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await ui.press({ key: 'cairn-pane-finish-M111' })
    await ui.unmount()
    expect(copy.commands ?? []).toEqual([])
    // After the step ends, the same press runs its command.
    await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
    const after = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await after.press({ key: 'cairn-pane-finish-M111' })
    await after.unmount()
    expect(copy.commands).toEqual([{ command: 'cairn:milestone-review', args: 'M111' }])
  })

  const PLAIN = [
    { answer: prView('OPEN', 'APPROVED'), word: 'approved' },
    { answer: prView('OPEN', 'REVIEW_REQUIRED'), word: 'in review' },
  ]
  for (const each of PLAIN) {
    test(`an \`${each.word}\` line carries no Button`, async ($, on) => {
      gh(on, () => each.answer)
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      const line = await blockedView($, 'blocked-M111')
      expect(line.text).toBe(line1250(each.word))
      expect(line.buttons).toEqual([])
    })
  }
})

// `prWord` over shapes beyond the register cases (M224 review): a JSON
// value that is not an object, an object with no state, and a state in
// another case all read as `unknown`.
describe('prWord reads only the shapes it names', () => {
  // The word of a `gh pr view` read, which `prWord` gave until M301 and
  // `prViewRead` gives now.
  const prWord = (result: { exitCode: number; stdout: string } | null) => prViewRead(result).word
  test('a rejected call, a non-object, and an unknown state read as unknown', () => {
    const ok = (stdout: string) => ({ exitCode: 0, stdout })
    expect(prWord(null)).toBe('unknown')
    expect(prWord({ exitCode: 1, stdout: '{"state":"MERGED"}' })).toBe('unknown')
    expect(prWord(ok('null'))).toBe('unknown')
    expect(prWord(ok('[]'))).toBe('unknown')
    expect(prWord(ok('"MERGED"'))).toBe('unknown')
    expect(prWord(ok('{}'))).toBe('unknown')
    expect(prWord(ok('{"state":"open"}'))).toBe('unknown')
    expect(prWord(ok('{"state":"MERGED","reviewDecision":"CHANGES_REQUESTED"}'))).toBe('merged')
    expect(prWord(ok('{"state":"OPEN","reviewDecision":"SOMETHING_NEW"}'))).toBe('in review')
  })
})

// The `gh pr view` reply form gives the merge state as the graphql form
// does (M301 AC1).
describe('prViewRead gives an open pull request its merge state (M301 AC1)', () => {
  const ok = (value: unknown) => ({ exitCode: 0, stdout: `${JSON.stringify(value)}\n` })
  const INPUTS: [string, Record<string, unknown>, 'mergeable' | 'conflicts' | null][] = [
    ['MERGEABLE', { mergeable: 'MERGEABLE' }, 'mergeable'],
    ['CONFLICTING', { mergeable: 'CONFLICTING' }, 'conflicts'],
    ['UNKNOWN', { mergeable: 'UNKNOWN' }, null],
    ['another string', { mergeable: 'SOMETHING_NEW' }, null],
    ['the field absent', {}, null],
  ]
  for (const [name, part, mergeable] of INPUTS) {
    test(`an open reply with ${name} reads ${mergeable}`, () => {
      expect(prViewRead(ok({ state: 'OPEN', reviewDecision: 'APPROVED', ...part }))).toEqual({ word: 'approved', counts: null, mergeable })
    })
  }

  test('a MERGED or CLOSED reply with MERGEABLE carries no merge state', () => {
    expect(prViewRead(ok({ state: 'MERGED', reviewDecision: 'APPROVED', mergeable: 'MERGEABLE' }))).toEqual({
      word: 'merged',
      counts: null,
      mergeable: null,
    })
    expect(prViewRead(ok({ state: 'CLOSED', reviewDecision: '', mergeable: 'MERGEABLE' }))).toEqual({ word: 'closed', counts: null, mergeable: null })
  })

  test('a rejected call, a non-zero exit, and text that is not JSON read unknown', () => {
    const none = { word: 'unknown', counts: null, mergeable: null }
    expect(prViewRead(null)).toEqual(none)
    expect(prViewRead({ exitCode: 1, stdout: '{"state":"OPEN","mergeable":"MERGEABLE"}' })).toEqual(none)
    expect(prViewRead({ exitCode: 0, stdout: 'not json' })).toEqual(none)
  })
})

// Paths that run no `gh` call (M224 review): a close of a shown pane, and
// an open that a hook refuses. The pull request is open, so a read there
// would also run the `gh api graphql` call (M225 AC1).
describe('a close or a refused open reads no state (M224 AC3)', () => {
  test('/cairn-pane that closes a shown pane runs no gh call', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.graphql.length).toBe(1)
    calls.reads.length = 0
    calls.graphql.length = 0
    const closed = await $.command.run({ command: COMMAND })
    expect(closed.text).toBe('cairn pane closed')
    await calls.settled()
    expect(calls.reads).toEqual([])
    expect(calls.graphql).toEqual([])
  })

  test('a refused open runs no gh call, by the command or the band', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    copy.refuse = 'opens are refused here'
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
    await ui.press({ key: 'cairn-open' })
    await ui.unmount()
    await calls.settled()
    expect(calls.reads).toEqual([])
    expect(calls.graphql).toEqual([])
  })
})

// Each trigger reads the pull request with one `gh api graphql` call (M237),
// and a turn end runs none (M224 AC3, M225 AC1).
describe('the states are read at each pane open and at a Refresh press, and never on a timer (M224 AC3)', () => {
  const ONE_READ = [URL_1250]
  const graphOf = (calls: Gh) => calls.graphql.map(argv => [argOf(argv, 'owner'), argOf(argv, 'repo'), argOf(argv, 'number')])
  const ONE_QUERY = [['upstream', 'repo', '1250']]

  test('the /cairn-pane command reads once', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.reads).toEqual(ONE_READ)
    expect(graphOf(calls)).toEqual(ONE_QUERY)
    expect(calls.clocks).toEqual([])
  })

  test("the band's open button reads once", async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.graphql).toEqual([])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
    await ui.press({ key: 'cairn-open' })
    await ui.unmount()
    await calls.settled()
    expect(calls.reads).toEqual(ONE_READ)
    expect(graphOf(calls)).toEqual(ONE_QUERY)
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('in review'))
    expect(calls.clocks).toEqual([])
  })

  test('the session-start reopen reads once', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    await openPane($, on, copy)
    await calls.settled()
    await $.session.end({ reason: 'other', sessionId: 's1' })
    newProcess(copy)
    calls.reads.length = 0
    calls.graphql.length = 0
    await $.session.start(NEW_START)
    await calls.settled()
    expect(listed(copy)).toBe(true)
    expect(calls.reads).toEqual(ONE_READ)
    expect(graphOf(calls)).toEqual(ONE_QUERY)
    expect(calls.clocks).toEqual([])
  })

  test('a press of the ↻ Refresh Button reads once', async ($, on) => {
    let state = 'OPEN'
    const calls = gh(on, () => prView(state, ''))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('in review'))
    expect((await blockedView($, 'blocked-head')).buttons).toEqual([])
    expect((await blockedView($, 'card-repo')).buttons).toEqual(['cairn-pane-home', 'cairn-pane-refresh'])
    const press = async () => {
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      await ui.press({ key: 'cairn-pane-refresh' })
      await ui.unmount()
    }
    await press()
    expect(calls.reads).toEqual([...ONE_READ, ...ONE_READ])
    expect(graphOf(calls)).toEqual([...ONE_QUERY, ...ONE_QUERY])
    // A merged pull request takes the same one call, and no other (M237).
    state = 'MERGED'
    await press()
    expect(calls.reads).toEqual([...ONE_READ, ...ONE_READ, ...ONE_READ])
    expect(graphOf(calls)).toEqual([...ONE_QUERY, ...ONE_QUERY, ...ONE_QUERY])
    expect(calls.calls).toEqual([])
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('merged'))
    expect(calls.clocks).toEqual([])
  })

  test('a turn end runs no gh call', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.graphql.length).toBe(1)
    calls.reads.length = 0
    calls.graphql.length = 0
    await $.turn.complete(turn())
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.reads).toEqual([])
    expect(calls.graphql).toEqual([])
    expect(calls.clocks).toEqual([])
  })
})

describe('a failed read shows `unknown` and no Button (M224 AC4)', () => {
  // blocked-prs: M101's read fails, and M102 and M104 read as merged, so
  // the other lines are seen to draw as before.
  const URL_12 = 'https://github.com/upstream/repo/pull/12'
  const FAILS: { name: string; answer: GhAnswer }[] = [
    { name: 'a call that rejects', answer: 'reject' },
    { name: 'a non-zero exit', answer: { exitCode: 1, stdout: '' } },
    { name: 'text that is not JSON', answer: { exitCode: 0, stdout: 'no pull requests found\n' } },
    { name: 'JSON with an unknown state', answer: prView('DRAFT', '') },
  ]
  for (const fail of FAILS) {
    test(`${fail.name} shows \`unknown\``, async ($, on) => {
      gh(on, url => (url === URL_12 ? fail.answer : prView('MERGED')))
      seat(on, copyOf('blocked-prs'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      const opened = await $.command.run({ command: COMMAND })
      expect(opened.text).toBe('cairn pane opened')
      const failed = await blockedView($, 'blocked-M101')
      expect(failed.text).toBe(prText('M101', 'One pull request URL', 12, 'unknown'))
      expect(failed.buttons).toEqual([])
      expect((await blockedView($, 'blocked-M102')).text).toBe(prText('M102', 'Two pull request URLs', 34, 'merged'))
      expect((await blockedView($, 'blocked-M102')).buttons).toEqual(['cairn-pane-finish-M102'])
      expect((await blockedView($, 'blocked-M104')).text).toBe(prText('M104', 'A URL with a trailing path', 90, 'merged'))
      expect((await blockedView($, 'blocked-M103')).text).toBe('○ M103  A URL only after a companion entry')
      expect((await blockedView($, 'blocked-M105')).text).toBe('○ M105  A branch with no URL')
    })
  }
})

// The counts of an open handed-off pull request (M225). The texts each case
// expects are written out by hand.

// The keys, texts, and indents of the pane's lines, at a width.
async function linesAt(
  $,
  bodyColumns = 60,
  surface: (typeof SURFACES)[number] = 'desktop',
): Promise<{ key: string; text: string; indent: number }[]> {
  await ghSettled()
  const ui = await mountPane($, surface, bodyColumns)
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const out = flat(root).map(line => ({
    key: keyOf(line) ?? '',
    text: textOf(line),
    indent: (line.props.paddingLeft as number | undefined) ?? 0,
  }))
  await ui.unmount()
  return out
}
const countsOf = async ($, id = 'M111', surface: (typeof SURFACES)[number] = 'desktop') =>
  (await linesAt($, 60, surface)).find(line => line.key === `blocked-${id}-counts`)

describe('each open pull request is queried once, by its own owner, repo, and number (M225 AC1)', () => {
  // blocked-prs with M101 and M104 pointed at two other repos: both read
  // OPEN, and M102 reads MERGED. Each github.com URL takes one query (M237),
  // and the two open ones each draw their own count.
  test('two lines with different owners, repos, and numbers', async ($, on) => {
    const copy = copyOf('blocked-prs')
    copy.files['/cairn/milestones/M101-one.md'] = copy.files['/cairn/milestones/M101-one.md'].replace(
      'https://github.com/upstream/repo/pull/12',
      'https://github.com/alpha/one/pull/12',
    )
    copy.files['/cairn/milestones/M104-trailing.md'] = copy.files['/cairn/milestones/M104-trailing.md'].replace(
      'https://github.com/upstream/repo/pull/90',
      'https://github.com/beta/two/pull/90',
    )
    const calls = gh(
      on,
      url => (url.includes('/upstream/') ? prView('MERGED') : prView('OPEN', '')),
      url => (url.includes('/alpha/') ? countsReply(1) : countsReply(2)),
    )
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    const asked = calls.graphql.map(argv => [argv.slice(0, 3).join(' '), argOf(argv, 'owner'), argOf(argv, 'repo'), argOf(argv, 'number')])
    expect(asked.filter(each => each[1] !== 'upstream').sort()).toEqual([
      ['gh api graphql', 'alpha', 'one', '12'],
      ['gh api graphql', 'beta', 'two', '90'],
    ])
    expect(calls.calls).toEqual([])
    // Each query names the state, the decision, the merge state (M301), and
    // the threads (M237).
    for (const argv of calls.graphql) {
      const query = argOf(argv, 'query') ?? ''
      expect(query.includes('{ state reviewDecision mergeable reviewThreads(last: 100) { nodes { isResolved } } }')).toBe(true)
    }
    expect((await countsOf($, 'M101'))?.text).toBe('1 unresolved thread')
    expect((await countsOf($, 'M104'))?.text).toBe('2 unresolved threads')
    expect(await countsOf($, 'M102')).toBe(undefined)
  })

  const NOT_OPEN: { name: string; answer: GhAnswer }[] = [
    { name: 'merged', answer: prView('MERGED', '') },
    { name: 'closed', answer: prView('CLOSED', '') },
    { name: 'unknown, by a rejected call', answer: 'reject' },
    { name: 'unknown, by an unknown state', answer: prView('DRAFT', '') },
  ]
  // Since M237 the one query also gives the word, so a line that is not
  // open still takes it, and draws no count.
  for (const each of NOT_OPEN) {
    test(`a ${each.name} line takes one query and draws no count`, async ($, on) => {
      const calls = gh(on, () => each.answer, () => countsReply(3))
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.reads.length).toBe(1)
      expect(calls.graphql.length).toBe(1)
      expect(calls.calls).toEqual([])
      expect(await countsOf($)).toBe(undefined)
    })
  }

  // Each word `wordOf` gives an OPEN pull request gets the query (M225
  // review), so the open words and `wordOf` stay in step.
  const OPEN: { decision: string; word: string }[] = [
    { decision: 'CHANGES_REQUESTED', word: 'changes requested' },
    { decision: 'APPROVED', word: 'approved' },
    { decision: 'REVIEW_REQUIRED', word: 'in review' },
  ]
  for (const each of OPEN) {
    test(`an \`${each.word}\` line gets one query`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', each.decision), () => countsReply(1))
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.graphql.length).toBe(1)
      expect((await blockedView($, 'blocked-M111')).text).toBe(line1250(each.word))
      expect((await countsOf($))?.text).toBe('1 unresolved thread')
    })
  }
})

describe('the count line under a blocked line (M225 AC3)', () => {
  const LINES: { t: number; text: string | undefined }[] = [
    { t: 3, text: '3 unresolved threads' },
    { t: 2, text: '2 unresolved threads' },
    { t: 1, text: '1 unresolved thread' },
    { t: 0, text: undefined },
  ]
  for (const each of LINES) {
    test(`${each.t} threads draw ${each.text === undefined ? 'no line' : `\`${each.text}\``}`, async ($, on) => {
      gh(on, () => prView('OPEN', 'CHANGES_REQUESTED'), () => countsReply(each.t))
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      const lines = await linesAt($)
      const at = lines.findIndex(line => line.key === 'blocked-M111-counts')
      expect(lines.find(line => line.key === 'blocked-M111')?.text).toBe(line1250('changes requested'))
      if (each.text === undefined) {
        expect(at).toBe(-1)
        return
      }
      expect(lines[at]).toEqual({ key: 'blocked-M111-counts', text: each.text, indent: 4 })
      expect(lines[at - 1].key).toBe('blocked-M111')
    })
  }

  test('no line before the first read', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''), () => countsReply(3))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.graphql).toEqual([])
    expect(await countsOf($)).toBe(undefined)
  })

  // A Refresh whose query is held: the earlier counts stay drawn until it
  // returns, and then the new ones draw. A later Refresh whose query fails
  // takes the line away.
  test('a Refresh keeps the earlier counts until the new read returns', async ($, on) => {
    let hold: Promise<void> | null = null
    let reply = countsReply(2)
    const calls = gh(
      on,
      () => prView('OPEN', ''),
      async () => {
        if (hold !== null) await hold
        return reply
      },
    )
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await countsOf($))?.text).toBe('2 unresolved threads')
    let release = () => {}
    hold = new Promise<void>(resolve => {
      release = resolve
    })
    reply = countsReply(5)
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: 'cairn-pane-refresh' })
    try {
      for (let i = 0; i < 200 && calls.graphql.length < 2; i++) await new Promise(resolve => setTimeout(resolve, 5))
      expect(calls.graphql.length).toBe(2)
      // The desktop pane holds the press, so the terminal one is read.
      expect((await countsOf($, 'M111', 'terminal'))?.text).toBe('2 unresolved threads')
    } finally {
      release()
      await pressing
    }
    await ui.unmount()
    expect((await countsOf($))?.text).toBe('5 unresolved threads')
    hold = null
    reply = { exitCode: 1, stdout: '' }
    const again = await mountPane($, 'desktop')
    await again.press({ key: 'cairn-pane-refresh' })
    await again.unmount()
    expect(await countsOf($)).toBe(undefined)
  })

  // 3-digit counts fit a 44-column dock: the whole line, as well as each
  // line's lead and tail as the M208 check reads them.
  test('3-digit counts fit 44 columns', async ($, on) => {
    gh(on, () => prView('OPEN', ''), () => countsReply(100))
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const counts = (await linesAt($, 44)).find(line => line.key === 'blocked-M111-counts')
    expect(counts?.text).toBe('100 unresolved threads')
    expect((counts?.indent ?? 99) + width(counts?.text ?? '')).toBeLessThanOrEqual(44)
    const ui = await mountPane($, 'desktop', 44)
    const [root] = await ui.findAll({ key: 'cairn-pane' })
    for (const line of flat(root)) {
      const key = keyOf(line) ?? ''
      const indent = (line.props.paddingLeft as number | undefined) ?? 0
      const sum = async (part: string) => (await partOf(ui, `${key}-${part}`)).map(t => width(textOf(t))).reduce((a, b) => a + b, 0)
      expect([key, indent + (await sum('lead')) + (await sum('tail')) <= 44]).toEqual([key, true])
      expect([key, line.props.minWidth]).toEqual([key, 0])
    }
    await ui.unmount()
  })
})

// Since M237 the word and the threads come in one reply, so a failed call
// reads `unknown` (M224 AC4 above), and only threads that fail the shape
// check leave the word with no count (M237 AC4).
describe('threads that fail the shape check draw no count line and leave the state word (M225 AC4, M237 AC4)', () => {
  const reply = (pr: unknown): GhAnswer => ({ exitCode: 0, stdout: `${JSON.stringify({ data: { repository: { pullRequest: pr } } })}\n` })
  const good = JSON.parse((countsReply(2) as { stdout: string }).stdout).data.repository.pullRequest
  const FAILS: { name: string; answer: GhAnswer }[] = [
    { name: 'no reviewThreads', answer: reply({}) },
    { name: 'threads that are not a list', answer: reply({ ...good, reviewThreads: { nodes: null } }) },
    { name: 'a malformed node', answer: reply({ ...good, reviewThreads: { nodes: [{ isResolved: 'no' }] } }) },
  ]
  for (const fail of FAILS) {
    test(`${fail.name}`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', 'CHANGES_REQUESTED'), () => fail.answer)
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      const opened = await $.command.run({ command: COMMAND })
      expect(opened.text).toBe('cairn pane opened')
      await calls.settled()
      expect(calls.graphql.length).toBe(1)
      const line = await blockedView($, 'blocked-M111')
      expect(line.text).toBe(line1250('changes requested'))
      expect(line.buttons).toEqual(['cairn-pane-revise-M111'])
      expect(await countsOf($)).toBe(undefined)
    })
  }
})

// The open hotfix pull requests (M226). A case answers the mod's `git` calls
// from the remotes it names and its `gh pr list` calls from `list`, as `gh`
// above records them. The blocked-prs fixture holds blocked rows and a
// candidate row, and most cases answer its blocked pull requests as
// merged. The lines each case expects are written out by hand.
const ORIGIN = 'https://github.com/fork/repo.git'
const UPSTREAM = 'git@github.com:upstream/repo.git'
const GUEST_PROFILE = '# Toolchain profile: generic\n# Collaboration mode: guest\n\n## verify\n'
const listCall = (url: string) => [
  'gh', 'pr', 'list', '--repo', url, '--state', 'open', '--author', '@me', '--limit', '100', '--json', 'number,title,url,headRefName,body',
]
const prUrl = (n: number) => `https://github.com/upstream/repo/pull/${n}`
const pr = (n: number, branch: string, title = `Fix ${n}`) => ({ number: n, title, url: prUrl(n), headRefName: branch })
const listReply = (entries: unknown[]): GhAnswer => ({ exitCode: 0, stdout: `${JSON.stringify(entries)}\n` })
const HOTFIX_KEY = /^hotfix(es-head(-gap)?|-\d+(-counts)?)$/
const keysOf = async $ => (await linesAt($)).map(line => line.key)
const withoutHotfixes = (lines: { key: string }[]) => lines.filter(line => !HOTFIX_KEY.test(line.key))

async function pressKey($, key: string) {
  const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
  await ui.press({ key })
  await ui.unmount()
}

describe('each pane open and Refresh press lists the open pull requests on the base remote once (M226 AC1)', () => {
  const MODES = [
    { name: 'an owner-mode repo uses origin', profile: null, remotes: { origin: ORIGIN, upstream: UPSTREAM }, url: ORIGIN },
    { name: 'a guest-mode repo with upstream uses upstream', profile: GUEST_PROFILE, remotes: { origin: ORIGIN, upstream: UPSTREAM }, url: UPSTREAM },
    { name: 'a guest-mode repo without upstream uses origin', profile: GUEST_PROFILE, remotes: { origin: ORIGIN }, url: ORIGIN },
  ]
  for (const mode of MODES) {
    test(mode.name, async ($, on) => {
      const calls = gh(on, () => prView('MERGED'), undefined, { remotes: mode.remotes })
      const copy = copyOf('blocked-prs')
      if (mode.profile !== null) copy.files['/cairn/PROFILE.md'] = mode.profile
      seat(on, copy)
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.lists).toEqual([listCall(mode.url)])
    })
  }

  test("the band's open button lists once", async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN } })
    seat(on, copyOf('blocked-prs'))
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.lists).toEqual([])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
    await ui.press({ key: 'cairn-open' })
    await ui.unmount()
    await calls.settled()
    expect(calls.lists).toEqual([listCall(ORIGIN)])
  })

  test('the session-start reopen lists once, and a turn end lists nothing', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN } })
    const copy = copyOf('blocked-prs')
    await openPane($, on, copy)
    await calls.settled()
    await $.session.end({ reason: 'other', sessionId: 's1' })
    newProcess(copy)
    calls.lists.length = 0
    await $.session.start(NEW_START)
    await calls.settled()
    expect(listed(copy)).toBe(true)
    expect(calls.lists).toEqual([listCall(ORIGIN)])
    await $.turn.complete(turn())
    expect(calls.lists).toEqual([listCall(ORIGIN)])
  })
})

describe('the Hotfixes section lists the hotfix-* pull requests before the candidates (M226 AC2)', () => {
  test('only the hotfix-* entry draws, after Blocked and before Candidates', async ($, on) => {
    const list = () => listReply([pr(1265, 'hotfix-clmm', 'Return only fixed effects'), pr(1300, 'm226-pane'), pr(1301, 'feature-x')])
    gh(on, url => (url === prUrl(1265) ? prView('OPEN', '') : prView('MERGED')), () => countsReply(0), { remotes: { origin: ORIGIN }, list })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const keys = await keysOf($)
    expect(keys.filter(key => HOTFIX_KEY.test(key))).toEqual(['hotfixes-head-gap', 'hotfixes-head', 'hotfix-1265'])
    expect(keys.indexOf('blocked-head')).toBeLessThan(keys.indexOf('hotfixes-head'))
    expect(keys.indexOf('hotfixes-head')).toBeLessThan(keys.indexOf('candidates-head'))
    expect(keys.slice(keys.indexOf('hotfix-1265') + 1)[0]).toBe('candidates-head-gap')
    expect((await blockedView($, 'hotfixes-head')).text).toBe(headText('Hotfixes', '1'))
    expect((await blockedView($, 'hotfix-1265')).text).toBe(prText('fix', 'Return only fixed effects', 1265, 'in review'))
  })
})

// M289 AC1, AC2, M302 AC2, AC3: each section count draws as a badge, an
// `Svg` pill in the one gray fill on the desktop and the padded number on
// the theme's gray in the terminal, in the lead after the label and a
// space, and the row has no tail. On the desktop the line and its lead
// center the row.
describe('the Blocked, Hotfixes, and Candidates counts draw as gray badges after the label (M289 AC1, AC2, M302 AC2, AC3)', () => {
  // The plan's fill, written out here rather than read from badge.ts.
  const FILL = 'rgb(110,110,110)'
  const HEADS = [{ key: 'blocked-head' }, { key: 'hotfixes-head' }, { key: 'candidates-head' }] as const
  async function seatAll($, on, surface: (typeof SURFACES)[number]) {
    const list = () => listReply([pr(1265, 'hotfix-clmm', 'Return only fixed effects')])
    gh(on, url => (url === prUrl(1265) ? prView('OPEN', '') : prView('MERGED')), () => countsReply(0), { remotes: { origin: ORIGIN }, list })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface, isInteractive: true })
    await $.command.run({ command: COMMAND })
    await ghSettled()
    return mountPane($, surface)
  }

  test('desktop: each count is one Svg pill holding the number, in the one gray fill', async ($, on) => {
    const ui = await seatAll($, on, 'desktop')
    for (const { key } of HEADS) {
      expect([key, await boxOf(ui, `${key}-tail`)]).toEqual([key, undefined])
      const lead = kids((await boxOf(ui, `${key}-lead`)) as Element)
      // The label, the space, then the pill, and no count text beside it.
      expect(lead.map(child => child.type)).toEqual(['Text', 'Text', 'Svg'])
      expect(textOf(lead[1])).toBe(' ')
      const svg = lead[2]
      const count = String(svg.props.alt)
      expect(count).toMatch(/^\d+$/)
      const source = String(svg.props.source)
      expect(source).toMatch(new RegExp(`<rect class="badge" [^>]*fill="${FILL.replace(/[()]/g, '\\$&')}"`))
      expect(source).toMatch(new RegExp(`<rect class="badge" [^>]*rx="`))
      expect(source).toMatch(/<text class="badge-text"[^>]* fill="rgb\(255,255,255\)"/)
      expect(source).toContain(`>${count}</text>`)
      expect(svg.props.height).toBe(16)
      expect([key, (await boxOf(ui, key))?.props.alignItems]).toEqual([key, 'center'])
      expect([key, (await boxOf(ui, `${key}-lead`))?.props.alignItems]).toEqual([key, 'center'])
    }
    expect(textOf((await boxOf(ui, 'blocked-head-lead')) as Element)).toBe('Blocked 7')
    expect(textOf((await boxOf(ui, 'hotfixes-head-lead')) as Element)).toBe('Hotfixes 1')
    await ui.unmount()
  })

  test('terminal: each count is one span, the padded number in inverseText on the gray key', async ($, on) => {
    const ui = await seatAll($, on, 'terminal')
    expect(await ui.findAll({ type: 'Svg' })).toEqual([])
    for (const { key } of HEADS) {
      expect([key, await boxOf(ui, `${key}-tail`)]).toEqual([key, undefined])
      const lead = kids((await boxOf(ui, `${key}-lead`)) as Element)
      expect(lead.length).toBe(3)
      expect(textOf(lead[1])).toBe(' ')
      const span = lead[2]
      expect(textOf(span)).toMatch(/^ \d+ $/)
      expect(span.props.color).toBe('inverseText')
      expect(span.props.backgroundColor).toBe(BADGE_KEY)
    }
    expect(textOf(kids((await boxOf(ui, 'blocked-head-lead')) as Element)[2])).toBe(' 7 ')
    expect(textOf(kids((await boxOf(ui, 'hotfixes-head-lead')) as Element)[2])).toBe(' 1 ')
    await ui.unmount()
  })
})

// M289 AC3: a badge widens with its number's digits, holds the number as its
// text, and fits the text to its width less its padding.
describe('a badge widens with its digits (M289 AC3)', () => {
  const parts = (svg: string) => ({
    width: Number(/^<svg [^>]*width="([\d.]+)"/.exec(svg)?.[1]),
    textLength: Number(/textLength="([\d.]+)"/.exec(svg)?.[1]),
    text: />([^<>]*)<\/text>/.exec(svg)?.[1],
  })
  test('widths strictly increase for 9, 10, and 100, and each text is its number', () => {
    const [nine, ten, hundred] = [9, 10, 100].map(count => parts(badgeSvg(count)))
    expect(nine.width).toBeLessThan(ten.width)
    expect(ten.width).toBeLessThan(hundred.width)
    expect([nine.text, ten.text, hundred.text]).toEqual(['9', '10', '100'])
  })
  // The number's color on each fill reaches the WCAG 2.2 text contrast of
  // 4.5:1, computed as band.test.tsx does for the band pill (M217).
  test('the badge number reads on its fill at 4.5:1 or more', () => {
    const rgb = (color: string) => (/^rgb\((\d+),(\d+),(\d+)\)$/.exec(color) ?? []).slice(1).map(Number)
    const lum = (c: number[]) =>
      c
        .map(v => (v / 255 <= 0.04045 ? v / 255 / 12.92 : Math.pow((v / 255 + 0.055) / 1.055, 2.4)))
        .reduce((sum, v, i) => sum + [0.2126, 0.7152, 0.0722][i] * v, 0)
    const ratio = (a: number[], b: number[]) => {
      const [hi, lo] = [lum(a), lum(b)].sort((x, y) => y - x)
      return (hi + 0.05) / (lo + 0.05)
    }
    expect(Math.abs(ratio([0, 0, 0], [255, 255, 255]) - 21)).toBeLessThan(1e-9)
    const svg = badgeSvg(7)
    const fill = rgb(/<rect class="badge"[^>]* fill="([^"]+)"/.exec(svg)?.[1] ?? '')
    const text = rgb(/<text class="badge-text"[^>]* fill="([^"]+)"/.exec(svg)?.[1] ?? '')
    expect([fill, text]).toEqual([
      [110, 110, 110],
      [255, 255, 255],
    ])
    expect(ratio(text, fill)).toBeGreaterThanOrEqual(4.5)
  })
  test('the text length is the width less the padding, and the Svg width matches', () => {
    for (const count of [9, 10, 100]) {
      const got = parts(badgeSvg(count))
      expect(got.textLength).toBe(got.width - BADGE_PAD)
      expect(got.width).toBe(badgeWidth(count))
    }
  })
})

describe('each hotfix line shows the word and counts a blocked line shows, and no Button (M226 AC3)', () => {
  // M237 AC4: a hotfix URL on a host other than github.com takes one
  // `gh pr view` call for its word and gets no count, while the github.com
  // blocked URL beside it takes one graphql call and draws its count.
  test('a hotfix on another host takes one gh pr view call and draws no count', async ($, on) => {
    const OTHER = 'https://ghe.example.com/upstream/repo/pull/7'
    const calls = gh(on, () => prView('OPEN', 'REVIEW_REQUIRED'), () => countsReply(2), {
      remotes: { origin: ORIGIN },
      list: () => listReply([{ number: 7, title: 'Fix 7', url: OTHER, headRefName: 'hotfix-other' }]),
    })
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    // The fields name `mergeable` since M301 (AC1), and the call uses the
    // exported constant.
    expect(calls.calls).toEqual([['gh', 'pr', 'view', OTHER, '--json', 'state,reviewDecision,mergeable']])
    expect(PR_VIEW_FIELDS).toBe('state,reviewDecision,mergeable')
    expect(calls.graphql.map(argv => [argOf(argv, 'owner'), argOf(argv, 'repo'), argOf(argv, 'number')])).toEqual([
      ['upstream', 'repo', '1250'],
    ])
    expect(calls.reads.sort()).toEqual([OTHER, URL_1250].sort())
    const lines = await linesAt($)
    const textOf_ = (key: string) => lines.find(line => line.key === key)?.text
    expect(textOf_('hotfix-7')).toBe(prText('fix', 'Fix 7', 7, 'in review'))
    expect(textOf_('hotfix-7-counts')).toBe(undefined)
    expect(textOf_('blocked-M111-counts')).toBe('2 unresolved threads')
  })

  test('an open PR with counts, a changes-requested PR, and a merged PR', async ($, on) => {
    const list = () => listReply([pr(1265, 'hotfix-a'), pr(1264, 'hotfix-b'), pr(1263, 'hotfix-c')])
    const views: Record<string, GhAnswer> = {
      [prUrl(1265)]: prView('OPEN', 'REVIEW_REQUIRED'),
      [prUrl(1264)]: prView('OPEN', 'CHANGES_REQUESTED'),
      [prUrl(1263)]: prView('MERGED', 'APPROVED'),
    }
    const calls = gh(on, url => views[url] ?? prView('MERGED'), url => (url === prUrl(1265) ? countsReply(2) : countsReply(0)), {
      remotes: { origin: ORIGIN },
      list,
    })
    // blocked-active's M111 is not in `views`, so it reads as merged here.
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const lines = await linesAt($)
    const textOf_ = (key: string) => lines.find(line => line.key === key)?.text
    expect(textOf_('hotfix-1265')).toBe(prText('fix', 'Fix 1265', 1265, 'in review'))
    expect(textOf_('hotfix-1264')).toBe(prText('fix', 'Fix 1264', 1264, 'changes requested'))
    expect(textOf_('hotfix-1263')).toBe(prText('fix', 'Fix 1263', 1263, 'merged'))
    expect(textOf_('hotfix-1265-counts')).toBe('2 unresolved threads')
    expect(textOf_('hotfix-1264-counts')).toBe(undefined)
    expect(textOf_('hotfix-1263-counts')).toBe(undefined)
    for (const key of ['hotfix-1265', 'hotfix-1264', 'hotfix-1263']) expect((await blockedView($, key)).buttons).toEqual([])
    // Each hotfix takes the one query (M237), and the merged one draws no
    // count, as a merged blocked line draws none.
    expect(calls.graphql.map(argv => argOf(argv, 'number')).sort()).toEqual(['1250', '1263', '1264', '1265'])
    expect(calls.calls).toEqual([])
  })

  test('a hotfix line shows the same word and counts as a blocked line with the same replies', async ($, on) => {
    const copy = copyOf('blocked-active')
    gh(on, () => prView('OPEN', 'CHANGES_REQUESTED'), () => countsReply(1), {
      remotes: { origin: ORIGIN },
      list: () => listReply([pr(1265, 'hotfix-a')]),
    })
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const lines = await linesAt($)
    const textOf_ = (key: string) => lines.find(line => line.key === key)?.text ?? ''
    expect(textOf_('blocked-M111')).toBe(line1250('changes requested'))
    expect(textOf_('hotfix-1265').endsWith(' changes requested')).toBe(true)
    expect(textOf_('hotfix-1265-counts')).toBe(textOf_('blocked-M111-counts'))
    expect(textOf_('hotfix-1265-counts')).toBe('1 unresolved thread')
  })
})

describe('a failed list keeps the last good read for the root, and an empty one draws none (M226 AC4)', () => {
  const GOOD = () => listReply([pr(1265, 'hotfix-a')])
  const FAILS: { name: string; answer: GhAnswer }[] = [
    { name: 'a call that rejects', answer: 'reject' },
    { name: 'a non-zero exit', answer: { exitCode: 1, stdout: '[]\n' } },
    { name: 'text that is not JSON', answer: { exitCode: 0, stdout: 'HTTP 502\n' } },
    { name: 'JSON that is not an array', answer: { exitCode: 0, stdout: '{"number":1265}\n' } },
  ]
  // Opens with no remote for the baseline lines, then lists once with a
  // good reply, and answers the next list with `next`.
  async function setUp($, on, next: () => GhAnswer) {
    const remotes: Record<string, string> = {}
    let answer = GOOD
    // The card's repo query fails, so its numbers stay `?` across the reads
    // and the lines compare with the baseline (M286). With no remote the
    // name comes from the common git dir, the same `repo` that the origin
    // URL names later (M291).
    const calls = gh(on, url => (url === prUrl(1265) ? prView('OPEN', '') : prView('MERGED')), undefined, {
      remotes,
      list: () => answer(),
      counts: () => ({ exitCode: 1, stdout: '' }),
      common: { exitCode: 0, stdout: '/work/repo/.git\n' },
    })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.lists).toEqual([])
    const baseline = await linesAt($)
    expect(baseline.filter(line => HOTFIX_KEY.test(line.key))).toEqual([])
    remotes.origin = ORIGIN
    await pressKey($, 'cairn-pane-refresh')
    expect((await keysOf($)).includes('hotfix-1265')).toBe(true)
    answer = next
    await pressKey($, 'cairn-pane-refresh')
    expect(calls.lists.length).toBe(2)
    return baseline
  }

  for (const fail of FAILS) {
    test(`${fail.name} keeps the hotfix line`, async ($, on) => {
      const baseline = await setUp($, on, () => fail.answer)
      const lines = await linesAt($)
      expect(lines.find(line => line.key === 'hotfix-1265')?.text).toBe(prText('fix', 'Fix 1265', 1265, 'in review'))
      expect(withoutHotfixes(lines)).toEqual(baseline)
    })
  }

  test('an entry with a missing field is skipped', async ($, on) => {
    const { url: _url, ...noUrl } = pr(1262, 'hotfix-b')
    const { headRefName: _head, ...noBranch } = pr(1261, 'hotfix-c')
    const baseline = await setUp($, on, () =>
      listReply([
        noUrl,
        noBranch,
        { ...pr(1260, 'hotfix-d'), number: '1260' },
        null,
        'hotfix-e',
        pr(1259, 'hotfix-f'),
        // A repeated entry draws once, so no two lines share a key (M226 review).
        pr(1259, 'hotfix-f'),
      ]),
    )
    const lines = await linesAt($)
    expect(lines.filter(line => HOTFIX_KEY.test(line.key)).map(line => line.key)).toEqual([
      'hotfixes-head-gap',
      'hotfixes-head',
      'hotfix-1259',
    ])
    expect(withoutHotfixes(lines)).toEqual(baseline)
  })

  test('an empty array replaces the kept lines and draws no section', async ($, on) => {
    const baseline = await setUp($, on, () => listReply([]))
    expect(await linesAt($)).toEqual(baseline)
  })

  test('a kept read from another root is not drawn', async ($, on) => {
    const remotes: Record<string, string> = { origin: ORIGIN }
    let answer = GOOD
    // The card's numbers are good in the first root and fail in the other
    // (M286), so the other root draws `?` before and after its read.
    let counts: GhAnswer = repoReply(3, 12)
    const calls = gh(on, () => prView('OPEN', ''), undefined, { remotes, list: () => answer(), counts: () => counts })
    const copy = copyOf('blocked-prs')
    for (const path of Object.keys(copy.files)) copy.files[`/other${path}`] = copy.files[path]
    copy.unreadable.push(...copy.unreadable.map(path => `/other${path}`))
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await keysOf($)).includes('hotfix-1265')).toBe(true)
    expect((await linesAt($)).find(line => line.key === 'card-repo')?.text).toBe('repo  3 PRs   12 issues')
    copy.cwd = '/other'
    await $.turn.complete(turn())
    const moved = await linesAt($)
    expect(moved.filter(line => HOTFIX_KEY.test(line.key))).toEqual([])
    // The other root's own segment, not the name read for the first (M291).
    expect(moved.find(line => line.key === 'card-repo')?.text).toBe('other  ? PRs   ? issues')
    counts = { exitCode: 1, stdout: '' }
    answer = () => 'reject'
    const viewsOf1265 = () => calls.reads.filter(url => url ===prUrl(1265)).length
    const before = viewsOf1265()
    await pressKey($, 'cairn-pane-refresh')
    // Its own read names the project from the URL though its numbers
    // failed (M291), and the rest of the lines stay.
    expect(await linesAt($)).toEqual(
      moved.map(line => (line.key === 'card-repo' ? { ...line, text: 'repo  ? PRs   ? issues' } : line)),
    )
    // The read itself drops the other root's list, so its URL is not read
    // again, apart from the drawing's root check (M226 review).
    expect(viewsOf1265()).toBe(before)
  })

  test('a repo with no remote runs no list call and draws no section', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { list: GOOD })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.git).toEqual([['git', 'remote', 'get-url', 'origin']])
    expect(calls.lists).toEqual([])
    expect((await keysOf($)).filter(key => HOTFIX_KEY.test(key))).toEqual([])
  })
})

// M236: the pane's first line, the Button keys the drawn pane holds, and
// the ↻ Button.
async function refreshOf($, surface: (typeof SURFACES)[number] = 'desktop') {
  const ui = await mountPane($, surface)
  const keys = (await ui.findAll({ type: 'Button' })).map(keyOf)
  const [root] = await ui.findAll({ key: 'cairn-pane' })
  const lines = root === undefined ? [] : flat(root)
  const [button] = await ui.findAll({ key: PANE_REFRESH })
  await ui.unmount()
  return { keys, lines, first: lines[0], button }
}
// The keys of a line Box's children, and the key and `flexGrow` of every
// line Box and child Box that sets one.
const childKeys = (line: Element | undefined) => (line === undefined ? [] : kids(line).map(keyOf))
const grows = (lines: Element[]) =>
  lines.flatMap(line => [line, ...kids(line)].filter(box => box.props.flexGrow !== undefined).map(box => [keyOf(box), box.props.flexGrow]))

describe('the pane has one ↻ Refresh Button, at the right end of its first line (M236 AC2)', () => {
  // The checks AC2 makes in every state with a ROADMAP. `firstKey` is the
  // first line's key, the head line of the first milestone or `no-active`.
  const one = async ($, firstKey: string) => {
    const got = await refreshOf($)
    expect(got.keys.filter(key => key === PANE_REFRESH)).toEqual([PANE_REFRESH])
    expect(got.keys.filter(key => (key ?? '').endsWith('-hotfixes'))).toEqual([])
    expect(keyOf(got.first as Element)).toBe(firstKey)
    const children = childKeys(got.first)
    expect(children[children.length - 1]).toBe(`${firstKey}-refresh`)
    // The first line's tail grows, so ↻ sits at its right end after the
    // project name and the counts (M291).
    // Besides the first line, each candidate line's text grows, so ✎ sits at
    // its right end (M242, M242 review; on the desktop while the pointer is
    // over the line, M290), and so does each blocked or hotfix
    // line with a tail, so its number and state word sit at the right end
    // whether or not its title is cut. Each section heading's text grows
    // too (M286), but a milestone's head line does not. No other line grows.
    const growing = got.lines
      .slice(1)
      .filter(line => {
        const key = keyOf(line) ?? ''
        if (/-head$/.test(key)) return !/^M\d+-head$/.test(key)
        if (/^candidate-\d+$/.test(key)) return true
        return /^(blocked-[^-]+|hotfix-\d+)$/.test(key) && childKeys(line).includes(`${key}-tail`)
      })
      .map(keyOf)
    expect(grows(got.lines)).toEqual([[`${firstKey}-tail`, 1], ...growing.map(key => [`${key}-text`, 1])])
    expect(got.lines.filter(line => line.props.justifyContent !== undefined).map(keyOf)).toEqual([])
    expect(got.button?.props.label).toBe('↻')
    return got
  }

  test('blocked PRs and hotfix PRs, no active milestone', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''), undefined, { remotes: { origin: ORIGIN }, list: () => listReply([pr(1265, 'hotfix-a')]) })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect((await keysOf($)).includes('hotfixes-head')).toBe(true)
    expect((await blockedView($, 'blocked-head')).buttons).toEqual([])
    expect((await blockedView($, 'hotfixes-head')).buttons).toEqual([])
    await one($, 'card-repo')
  })

  test('an in-progress and a review milestone: only the card carries ↻, no head line', async ($, on) => {
    gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('pane-full'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const got = await one($, 'card-repo')
    for (const id of ['M080-head', 'M081-head']) {
      const head = got.lines.find(line => keyOf(line) === id)
      expect(head).toBeDefined()
      expect(buttonsIn(head as Element)).toEqual([])
    }
  })

  test('the Next line with Status after a skill ends, and one active milestone', async ($, on) => {
    seat(on, copyOf('single-in-progress'))
    await endSkill($)
    const got = await one($, 'card-repo')
    expect(got.keys).toEqual([PANE_HOME, PANE_REFRESH, PANE_NEXT, PANE_STATUS])
  })

  test('one active milestone and no PRs', async ($, on) => {
    gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('single-in-progress'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await keysOf($)).filter(key => key.startsWith('blocked') || key.startsWith('hotfix'))).toEqual([])
    await one($, 'card-repo')
  })

  test('no ROADMAP draws no ↻ Button', async ($, on) => {
    seat(on, copyOf('no-roadmap'))
    await $.turn.complete(turn())
    const got = await refreshOf($)
    expect(got.keys.filter(key => key === PANE_REFRESH)).toEqual([])
  })

  test('a press of ↻ lists the hotfix PRs and reads each PR again', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, list: () => listReply([pr(1265, 'hotfix-a')]) })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.lists.length).toBe(1)
    await pressKey($, PANE_REFRESH)
    expect(calls.lists.length).toBe(2)
    expect(calls.reads.filter(url => url ===prUrl(1265)).length).toBe(2)
  })
})

describe('a head line starts with the id in its phase color, with no phase word (M236 AC3)', () => {
  // pane-full holds M080 in-progress and M081 review.
  for (const [id, color] of [
    ['M080', IMPLEMENT_KEY],
    ['M081', REVIEW_KEY],
  ] as const) {
    test(`${id}`, async ($, on) => {
      seat(on, copyOf('pane-full'))
      await $.turn.complete(turn())
      const ui = await mountPane($, 'desktop')
      const lead = await partOf(ui, `${id}-head-lead`)
      await ui.unmount()
      expect(lead.map(span => [textOf(span), span.props.color ?? null, span.props.bold ?? null])).toEqual([
        [id, color, true],
        ['  ', null, null],
      ])
    })
  }
})

describe('the ↻ Button reads ⋯ while a read runs, and a press during a press read does nothing (M236 AC4)', () => {
  // A gate: `wait` settles when `release` runs, so a `gh pr view` answer
  // that awaits it is held until then.
  function gate() {
    let release = () => {}
    const wait = new Promise<void>(resolve => {
      release = resolve
    })
    return { wait, release: () => release() }
  }
  const until = async (ok: () => boolean) => {
    for (let i = 0; i < 200 && !ok(); i++) await sleep(5)
    expect(ok()).toBe(true)
  }
  // The ↻ Button's label, read through a terminal mount, which no press
  // holds.
  const labelOf = async $ => (await refreshOf($, 'terminal')).button?.props.label
  const total = (calls: Gh, reads: string[]) => reads.length + calls.calls.length + calls.graphql.length + calls.lists.length + calls.git.length

  const ENDS: { name: string; answer: GhAnswer }[] = [
    { name: 'succeeds', answer: prView('OPEN', '') },
    { name: 'exits 1', answer: { exitCode: 1, stdout: '' } },
    { name: 'rejects', answer: 'reject' },
  ]
  for (const end of ENDS) {
    test(`a held read reads ⋯ on the first line, and ↻ after it ${end.name}`, async ($, on) => {
      const held_ = gate()
      const calls = gh(on, async () => {
        await held_.wait
        return end.answer
      })
      seat(on, copyOf('blocked-active'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      expect(await labelOf($)).toBe('↻')
      await $.command.run({ command: COMMAND })
      await until(() => calls.reads.length === 1)
      const during = await refreshOf($, 'terminal')
      expect(during.button?.props.label).toBe('⋯')
      const children = childKeys(during.first)
      expect(children[children.length - 1]).toBe(`${keyOf(during.first as Element)}-refresh`)
      held_.release()
      await calls.settled()
      expect(await labelOf($)).toBe('↻')
    })
  }

  test('an open and a press overlap: ↻ once the newer read settles', async ($, on) => {
    const older = gate()
    const newer = gate()
    let n = 0
    const calls = gh(on, async () => {
      n += 1
      await (n === 1 ? older.wait : newer.wait)
      return prView('OPEN', '')
    })
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await until(() => calls.reads.length === 1)
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: PANE_REFRESH })
    try {
      await until(() => calls.reads.length === 2)
      expect(await labelOf($)).toBe('⋯')
      newer.release()
      await pressing
      expect(await labelOf($)).toBe('↻')
    } finally {
      newer.release()
      older.release()
      await pressing
      await ui.unmount()
    }
    await calls.settled()
    expect(await labelOf($)).toBe('↻')
  })

  // The case the newest-read check exists for: the older read settles
  // first, and ⋯ stays while the newer one runs.
  test('an open and a press overlap: ⋯ stays when the older read settles first', async ($, on) => {
    const older = gate()
    const newer = gate()
    let n = 0
    const calls = gh(on, async () => {
      n += 1
      await (n === 1 ? older.wait : newer.wait)
      return prView('OPEN', '')
    })
    seat(on, copyOf('blocked-active'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await until(() => calls.reads.length === 1)
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: PANE_REFRESH })
    try {
      await until(() => calls.reads.length === 2)
      older.release()
      await sleep(50)
      expect(await labelOf($)).toBe('⋯')
      newer.release()
      await pressing
      expect(await labelOf($)).toBe('↻')
    } finally {
      older.release()
      newer.release()
      await pressing
      await ui.unmount()
    }
  })

  test('a second press during a held press read reads no file and runs no call', async ($, on) => {
    const held_ = gate()
    let holding = false
    const calls = gh(on, async () => {
      if (holding) await held_.wait
      return prView('OPEN', '')
    })
    const copy = copyOf('blocked-active')
    const reads: string[] = []
    copy.reads = reads
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    holding = true
    const ui = await mountPane($, 'desktop')
    const pressing = ui.press({ key: PANE_REFRESH })
    try {
      await until(() => calls.reads.length === 2)
      const second = await mountPane($, 'terminal')
      // The count starts after the second mount, so it holds only what the
      // press does.
      const before = total(calls, reads)
      await second.press({ key: PANE_REFRESH })
      await sleep(50)
      expect(total(calls, reads)).toBe(before)
      await second.unmount()
    } finally {
      held_.release()
      await pressing
      await ui.unmount()
    }
    await calls.settled()
    // Once the first press's read settles, a press reads again.
    holding = false
    await pressKey($, PANE_REFRESH)
    expect(calls.reads.length).toBe(3)
  })

  // The first assertion is M237 AC3's: a stored true with no read in flight
  // in this module draws ↻, not ⋯.
  test('a stored reading state with no read in this module draws ↻ and lets a press read', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    seat(on, copyOf('blocked-active'))
    // A read that a reloaded module ended leaves the stored state true: the
    // store answers true until the mod writes the key.
    let stale = true
    on('state.get', async ($, e, next) => {
      const got = await next(e)
      if (!stale || e.plugin !== 'cairn' || e.key !== 'reading') return got
      // The hook answers `{ value }`, a StateRead of `{ value, version }`.
      const read_ = (got as { value?: { version?: number } } | undefined)?.value
      return { value: { version: read_?.version ?? 0, value: { shape: 'reading-1', value: true } } }
    })
    on('state.set', async ($, e, next) => {
      if (e.plugin === 'cairn' && e.key === 'reading') stale = false
      return next(e)
    })
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    expect(await labelOf($)).toBe('↻')
    await pressKey($, PANE_REFRESH)
    await calls.settled()
    expect(calls.reads.length).toBe(1)
    expect(await labelOf($)).toBe('↻')
  })

  // M237 AC3: a read whose write of `reading` false fails leaves the stored
  // value true, and the next drawing after it settles still shows ↻. The
  // hook answers `{ deny }`, which rejects the mod's write, so the stored
  // value stays true. The redraw the mod asks for after that failure is not
  // tested here: with it removed, a pane mounted through the read still
  // read ↻ in this harness (M237 review).
  test('a failed write of the reading state false still draws ↻ once the read settles', async ($, on) => {
    const held_ = gate()
    const calls = gh(on, async () => {
      await held_.wait
      return prView('OPEN', '')
    })
    seat(on, copyOf('blocked-active'))
    const refused: unknown[] = []
    on('state.set', async ($, e, next) => {
      const value = (e as { value?: { value?: unknown } }).value?.value
      if (e.plugin === 'cairn' && e.key === 'reading' && value === false) {
        refused.push(value)
        return { deny: 'the store refused the write' }
      }
      return next(e)
    })
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await until(() => calls.reads.length === 1)
    expect(await labelOf($)).toBe('⋯')
    held_.release()
    await calls.settled()
    await until(() => refused.length > 0)
    expect(await labelOf($)).toBe('↻')
  })
})

// M230. `held` answers every `gh` call only after `release`, so an open
// that waited for the read could not finish first. `finishes` says whether
// a call finished within 300 ms. `until` waits for a condition, for at most
// 200 waits of 5 ms.
function held(on: On, list: () => GhAnswer = () => listReply([pr(1265, 'hotfix-a')])) {
  let release = () => {}
  const gate = new Promise<void>(resolve => {
    release = resolve
  })
  let listSettled = false
  const calls = gh(
    on,
    async () => {
      await gate
      return prView('OPEN', '')
    },
    async () => {
      await gate
      return countsReply(0)
    },
    {
      remotes: { origin: ORIGIN },
      list: async () => {
        await gate
        listSettled = true
        return list()
      },
    },
  )
  return { calls, release, listSettled: () => listSettled }
}
const finishes = (work: Promise<unknown>) => Promise.race([work.then(() => 'finished'), sleep(300).then(() => 'waiting')])
async function until(ok: () => boolean) {
  for (let i = 0; i < 200 && !ok(); i++) await sleep(5)
}

describe('an open finishes before the pull request reads settle (M230 AC1)', () => {
  test('/cairn-pane prints its line before any gh call settles', async ($, on) => {
    const { calls, release } = held(on)
    seat(on, copyOf('blocked-active'))
    await $.session.start(NEW_START)
    try {
      const run = $.command.run({ command: COMMAND })
      expect(await finishes(run)).toBe('finished')
      expect((await run).text).toBe('cairn pane opened')
      await until(() => calls.reads.length > 0)
      expect(calls.reads).toEqual([URL_1250])
    } finally {
      release()
    }
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('in review'))
  })

  test("the band's open Button's press returns before any gh call settles", async ($, on) => {
    const { calls, release } = held(on)
    seat(on, copyOf('blocked-active'))
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
    try {
      expect(await finishes(ui.press({ key: 'cairn-open' }))).toBe('finished')
      await until(() => calls.reads.length > 0)
      expect(calls.reads).toEqual([URL_1250])
    } finally {
      release()
      await ui.unmount()
    }
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('in review'))
  })

  test("the session-start reopen's handler returns before any gh call settles", async ($, on) => {
    const { calls, release } = held(on)
    const copy = copyOf('blocked-active')
    try {
      await openPane($, on, copy)
      await until(() => calls.reads.length > 0)
      await $.session.end({ reason: 'other', sessionId: 's1' })
      newProcess(copy)
      calls.reads.length = 0
      expect(await finishes($.session.start(NEW_START))).toBe('finished')
      expect(listed(copy)).toBe(true)
      await until(() => calls.reads.length > 0)
      expect(calls.reads).toEqual([URL_1250])
    } finally {
      release()
    }
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('in review'))
  })
})

describe('the blocked reads start before the hotfix list settles (M230 AC2)', () => {
  test("the blocked URL's read runs while gh pr list is held", async ($, on) => {
    const { calls, release, listSettled } = held(on)
    seat(on, copyOf('blocked-active'))
    await $.session.start(NEW_START)
    try {
      await $.command.run({ command: COMMAND })
      await until(() => calls.reads.length > 0 && calls.lists.length > 0)
      expect(calls.lists).toEqual([listCall(ORIGIN)])
      expect(listSettled()).toBe(false)
      expect(calls.reads).toEqual([URL_1250])
    } finally {
      release()
    }
    await calls.settled()
    // Once the list settles, its hotfix URL is read too.
    expect(calls.reads).toEqual([URL_1250, prUrl(1265)])
  })
})

describe('a /clear in the same process reads the states again while the pane shows (M230 AC3)', () => {
  // The pane is listed open with no read run, as after an in-process
  // `/clear`, whose host state starts empty (M222).
  async function setUp($, on, place: (copy: Copy) => void) {
    const got = held(on)
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start(NEW_START)
    place(copy)
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250())
    expect((await keysOf($)).filter(key => HOTFIX_KEY.test(key))).toEqual([])
    return got
  }

  test('a placed and shown pane reads the words and the hotfix list, and the hook does not wait', async ($, on) => {
    const { calls, release } = await setUp($, on, copy => {
      copy.open = [PANE]
    })
    try {
      expect(await finishes($.classic.SessionStart({ source: 'clear' }))).toBe('finished')
      await until(() => calls.reads.length > 0 && calls.lists.length > 0)
      expect(calls.lists).toEqual([listCall(ORIGIN)])
      expect(calls.reads).toEqual([URL_1250])
    } finally {
      release()
    }
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('in review'))
    expect((await blockedView($, 'hotfix-1265')).text).toBe(prText('fix', 'Fix 1265', 1265, 'in review'))
  })

  test('a closed pane runs no gh call', async ($, on) => {
    const { calls, release } = await setUp($, on, copy => {
      copy.open = []
    })
    try {
      await $.classic.SessionStart({ source: 'clear' })
      await calls.settled()
      expect(calls.reads).toEqual([])
      expect(calls.lists).toEqual([])
      expect(calls.graphql).toEqual([])
    } finally {
      release()
    }
  })
})

// A `/resume` empties the host's state as a `/clear` does, and either reads
// the files again (M237 AC1). Each case compares the drawing with the one a
// turn end, a read the band already trusts, gives right after.
describe('a resume start reads the files again, as a clear start does (M237 AC1)', () => {
  async function bandText($): Promise<string> {
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'terminal', ...BAND })) as Ui
    const [root] = await ui.findAll({ key: 'cairn-band' })
    const out = root === undefined ? '' : textOf(root)
    await ui.unmount()
    return out
  }
  for (const source of ['clear', 'resume'] as const) {
    test(`a ${source} start with empty state draws the fixture's rows and lines`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      expect(await bandText($)).toBe('')
      expect(textAt(await paneLines($, 'terminal'), 'M002-task-1')).toBeUndefined()
      await $.classic.SessionStart({ source })
      const band = await bandText($)
      const lines = await paneLines($, 'terminal')
      expect(band).toContain('M002')
      expect(textAt(lines, 'M002-task-1')).toBe(T2_OPEN)
      await $.turn.complete(turn())
      expect(await bandText($)).toBe(band)
      expect(await paneLines($, 'terminal')).toEqual(lines)
    })

    test(`a ${source} start replaces rows from the same root that differ from the files`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const before = await bandText($)
      expect(textAt(await paneLines($, 'terminal'), 'M002-task-1')).toBe(T2_OPEN)
      tick(copy)
      await $.classic.SessionStart({ source })
      const band = await bandText($)
      const lines = await paneLines($, 'terminal')
      expect(band).not.toBe(before)
      expect(textAt(lines, 'M002-task-1')).toBe(T2_DONE)
      await $.turn.complete(turn())
      expect(await bandText($)).toBe(band)
      expect(await paneLines($, 'terminal')).toEqual(lines)
    })
  }

  // A resumed process raises `session.start` first and then the resume
  // hook, which reads the files again (M237 review).
  test('a resumed process start draws the rows once both hooks have run', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    tick(copy)
    await $.classic.SessionStart({ source: 'resume' })
    const band = await bandText($)
    expect(band).toContain('M002')
    expect(textAt(await paneLines($, 'terminal'), 'M002-task-1')).toBe(T2_DONE)
    await $.turn.complete(turn())
    expect(await bandText($)).toBe(band)
  })

  for (const source of ['startup', 'compact'] as const) {
    test(`a ${source} start reads no file`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      copy.reads = []
      await $.classic.SessionStart({ source })
      expect(copy.reads).toEqual([])
    })
  }
})

// A clear or resume start reads the pull request states for a placed pane,
// shown or behind another tab, and for no other pane (M237 AC2). No
// `session.start` opens the pane first, so every `gh` call is the hook's.
describe('a clear or resume start reads the states for a placed pane (M237 AC2)', () => {
  const CASES: { name: string; place: (copy: Copy) => void; reads: boolean }[] = [
    { name: 'a placed and shown pane', place: copy => { copy.open = [PANE] }, reads: true },
    { name: 'a placed pane behind another tab', place: copy => { copy.open = [PANE]; copy.hidden = [PANE] }, reads: true },
    { name: 'a pane that is not listed', place: copy => { copy.open = [] }, reads: false },
    { name: 'a listed pane that is not placed', place: copy => { copy.open = [PANE]; copy.unplaced = [PANE] }, reads: false },
    { name: 'a pane list that throws', place: copy => { copy.open = [PANE]; copy.panesThrow = true }, reads: false },
  ]
  for (const source of ['clear', 'resume'] as const) {
    for (const { name, place, reads } of CASES) {
      test(`at a ${source} start, ${name} ${reads ? 'reads' : 'runs no gh call'}`, async ($, on) => {
        const calls = gh(on, () => prView('OPEN', ''), undefined, {
          remotes: { origin: ORIGIN },
          list: () => listReply([pr(1265, 'hotfix-a')]),
        })
        const copy = copyOf('blocked-active')
        seat(on, copy)
        place(copy)
        await $.classic.SessionStart({ source })
        await calls.settled()
        const all = [...calls.calls, ...calls.graphql, ...calls.lists]
        if (reads) {
          expect(calls.lists).toEqual([listCall(ORIGIN)])
          expect(calls.reads.sort()).toEqual([URL_1250, prUrl(1265)].sort())
          expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('in review'))
        } else {
          expect(all).toEqual([])
        }
      })
    }
  }
})

// One draw of the pane, as a surface that places it makes (M238).
async function draw($) {
  const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
  await ui.unmount()
}
const sorted = (list: string[]) => [...list].sort()

// A clear or resume start that finds the pane listed but not placed owes a
// read, and the pane's first draw starts it (M238 AC1). The repo has no
// remote, so no hotfix list runs and `reads` holds the blocked URLs alone.
describe('a pane placed after a clear or resume start reads at its first draw (M238 AC1)', () => {
  const CASES = [
    { source: 'clear', fixture: 'blocked-active', urls: [URL_1250] },
    { source: 'resume', fixture: 'blocked-prs', urls: [prUrl(12), prUrl(34), prUrl(90)] },
  ] as const
  for (const { source, fixture, urls } of CASES) {
    test(`a ${source} start reads nothing, and the first draw reads each URL once (${fixture})`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', ''))
      const copy = copyOf(fixture)
      seat(on, copy)
      copy.open = [PANE]
      copy.unplaced = [PANE]
      await $.classic.SessionStart({ source })
      await calls.settled()
      expect(calls.reads).toEqual([])
      copy.unplaced = []
      await draw($)
      await calls.settled()
      expect(sorted(calls.reads)).toEqual(sorted([...urls]))
      await draw($)
      await calls.settled()
      expect(sorted(calls.reads)).toEqual(sorted([...urls]))
      // The read's words reach the pane (M238 review).
      const key = fixture === 'blocked-active' ? 'blocked-M111' : 'blocked-M101'
      expect((await blockedView($, key)).text).toMatch(/ in review$/)
    })
  }

  const OPENS: { name: string; open: ($, copy: Copy) => Promise<void> }[] = [
    { name: 'a /cairn-pane open', open: async $ => void (await $.command.run({ command: COMMAND })) },
    {
      name: "a press of the band's open button",
      open: async $ => {
        const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
        await ui.press({ key: 'cairn-open' })
        await ui.unmount()
      },
    },
  ]
  for (const { name, open } of OPENS) {
    test(`${name} between the start and the first draw leaves that draw reading nothing`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', ''))
      const copy = copyOf('blocked-active')
      seat(on, copy)
      copy.open = [PANE]
      copy.unplaced = [PANE]
      await $.classic.SessionStart({ source: 'clear' })
      await open($, copy)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
    })
  }

  const NONE: { name: string; before: ($, copy: Copy) => Promise<void> }[] = [
    { name: 'with no clear or resume start before it', before: async $ => void (await $.turn.complete(turn())) },
    {
      name: 'after a start that found no pane listed',
      before: async ($, copy) => {
        copy.open = []
        await $.classic.SessionStart({ source: 'clear' })
        copy.open = [PANE]
      },
    },
    {
      name: 'after a start whose pane list threw',
      before: async ($, copy) => {
        copy.open = [PANE]
        copy.unplaced = [PANE]
        copy.panesThrow = true
        await $.classic.SessionStart({ source: 'resume' })
        copy.panesThrow = false
        copy.unplaced = []
      },
    },
  ]
  for (const { name, before } of NONE) {
    test(`a first draw ${name} reads nothing`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', ''))
      const copy = copyOf('blocked-active')
      seat(on, copy)
      await before($, copy)
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([])
    })
  }
})

// A clear start's pane list answers not placed, and the pane is placed and
// drawn before that answer reaches the hook. The draw comes before the hook
// owes a read, so it reads nothing, and the hook's second list reads (M256
// AC1).
describe('a pane placed while a clear start lists the panes reads with no further draw (M256 AC1)', () => {
  const CASES = [
    { fixture: 'blocked-active', urls: [URL_1250] },
    { fixture: 'blocked-prs', urls: [prUrl(12), prUrl(34), prUrl(90)] },
  ] as const
  for (const { fixture, urls } of CASES) {
    test(`the hook reads each URL once after its held list (${fixture})`, async ($, on) => {
      const calls = gh(on, () => prView('OPEN', ''))
      const copy = copyOf(fixture)
      seat(on, copy)
      copy.open = [PANE]
      copy.unplaced = [PANE]
      let release = () => {}
      copy.panesHold = new Promise<void>(resolve => {
        release = resolve
      })
      const start = $.classic.SessionStart({ source: 'clear' })
      try {
        await until(() => copy.panesHold === undefined)
        // The hook's list is held, its answer computed as not placed.
        expect(copy.panesHold).toBeUndefined()
        expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(false)
        copy.unplaced = []
        await draw($)
        await calls.settled()
        expect(calls.reads).toEqual([])
      } finally {
        release()
      }
      await start
      await calls.settled()
      expect(sorted(calls.reads)).toEqual(sorted([...urls]))
    })
  }

  // The second list is held too, its answer computed as placed. A draw
  // while it waits takes the owed read, so the list reads nothing more.
  test('a draw while the second list waits takes the read, and the list reads nothing more', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    copy.open = [PANE]
    copy.unplaced = [PANE]
    let releaseFirst = () => {}
    let releaseSecond = () => {}
    copy.panesHold = new Promise<void>(resolve => {
      releaseFirst = resolve
    })
    const second = new Promise<void>(resolve => {
      releaseSecond = resolve
    })
    const start = $.classic.SessionStart({ source: 'clear' })
    try {
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(false)
      copy.unplaced = []
      copy.panesHold = second
      releaseFirst()
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHold).toBeUndefined()
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(true)
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
    } finally {
      releaseFirst()
      releaseSecond()
    }
    await start
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })
})

// A session end clears the read a clear start owed, so the pane's first
// draw after the end reads nothing (M256 AC2).
describe('a session end clears an owed read (M256 AC2)', () => {
  test('a pane owed a read at a session end reads nothing at its first draw after it', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    copy.open = [PANE]
    copy.unplaced = [PANE]
    await $.classic.SessionStart({ source: 'clear' })
    await calls.settled()
    expect(calls.reads).toEqual([])
    await $.session.end(CLEAR_END)
    copy.unplaced = []
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([])
  })
})

// A process start can raise both the reopen's `session.start` and a resume
// or clear `classic.SessionStart`. Between them they read each URL once
// (M238 AC2). Source `clear` is a guard, since no record shows a reopened
// start raising it.
describe('one process start reads each URL once (M238 AC2)', () => {
  const OTHER_END = { reason: 'other', sessionId: 's1' } as const
  // An open pane at an `other` end, so the next start in the folder reopens
  // it, with the open's own read settled and cleared from `reads`.
  async function marked($, on): Promise<{ calls: Gh; copy: Copy }> {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    await openPane($, on, copy)
    await calls.settled()
    await $.session.end(OTHER_END)
    newProcess(copy)
    calls.reads.length = 0
    return { calls, copy }
  }
  for (const source of ['resume', 'clear'] as const) {
    test(`the reopen, then a ${source} start, read each URL once`, async ($, on) => {
      const { calls } = await marked($, on)
      await $.session.start(NEW_START)
      await $.classic.SessionStart({ source })
      await calls.settled()
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
    })

    test(`a ${source} start, then the reopen, read each URL once`, async ($, on) => {
      const { calls } = await marked($, on)
      await $.classic.SessionStart({ source })
      await $.session.start(NEW_START)
      await calls.settled()
      await draw($)
      await calls.settled()
      expect(calls.reads).toEqual([URL_1250])
    })
  }

  test('an unplaced reopen, a resume start, and the first draw read each URL once', async ($, on) => {
    const { calls, copy } = await marked($, on)
    copy.notPlaced = 'the terminal is too narrow'
    await $.session.start(NEW_START)
    await $.classic.SessionStart({ source: 'resume' })
    await calls.settled()
    copy.notPlaced = undefined
    copy.unplaced = []
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // The read at the first draw is the start's read, so a reopen after it
  // reads nothing (M238 review). In a new process the pane is not listed
  // before the reopen, so this order is a guard, not one seen on a host.
  test('a resume start that owes, the first draw, then the reopen read each URL once', async ($, on) => {
    const { calls, copy } = await marked($, on)
    copy.open = [PANE]
    copy.unplaced = [PANE]
    await $.classic.SessionStart({ source: 'resume' })
    await calls.settled()
    expect(calls.reads).toEqual([])
    copy.unplaced = []
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
    await $.session.start(NEW_START)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // A pane placed before both hooks: the resume hook reads, and the reopen
  // after it reads nothing (M238 review).
  test('a resume start that reads, then the reopen, read each URL once', async ($, on) => {
    const { calls, copy } = await marked($, on)
    copy.open = [PANE]
    await $.classic.SessionStart({ source: 'resume' })
    await $.session.start(NEW_START)
    await calls.settled()
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // Both hooks of one start begun together, for a placed pane (M238
  // review). The harness runs the two in turn, so this test passed before
  // the classic hook's second `startRead` check, and it does not test that
  // check.
  test('the reopen and a resume start begun together read each URL once', async ($, on) => {
    const { calls, copy } = await marked($, on)
    copy.open = [PANE]
    await Promise.all([$.session.start(NEW_START), $.classic.SessionStart({ source: 'resume' })])
    await calls.settled()
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // A clear start reads again after a session end, also while an open's
  // read is still in flight.
  test('a clear start reads again while an open read is held', async ($, on) => {
    const { calls, release } = held(on)
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start(NEW_START)
    try {
      await $.command.run({ command: COMMAND })
      await until(() => calls.reads.length > 0)
      await $.session.end(CLEAR_END)
      await $.classic.SessionStart({ source: 'clear' })
      await until(() => calls.reads.filter(url => url === URL_1250).length > 1)
      expect(calls.reads.filter(url => url === URL_1250)).toEqual([URL_1250, URL_1250])
    } finally {
      release()
    }
  })

  // A session end ends the start, so after a reopen's read, a clear start in
  // the same process reads again.
  test("a clear start after a session end reads again after the reopen's read", async ($, on) => {
    const { calls } = await marked($, on)
    await $.session.start(NEW_START)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
    await $.session.end(CLEAR_END)
    await $.classic.SessionStart({ source: 'clear' })
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250, URL_1250])
  })
})

describe("a hotfix whose URL is a blocked row's draws on the blocked line only (M230 AC4)", () => {
  const SHARED = { number: 1250, title: 'Fix 1250', url: URL_1250, headRefName: 'hotfix-shared' }

  test('beside another hotfix, the shared one draws once and the count leaves it out', async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''), undefined, {
      remotes: { origin: ORIGIN },
      list: () => listReply([SHARED, pr(1265, 'hotfix-a')]),
    })
    seat(on, copyOf('blocked-active'))
    await $.session.start(NEW_START)
    await $.command.run({ command: COMMAND })
    const keys = await keysOf($)
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('in review'))
    expect(keys.filter(key => HOTFIX_KEY.test(key))).toEqual(['hotfixes-head-gap', 'hotfixes-head', 'hotfix-1265'])
    expect((await blockedView($, 'hotfixes-head')).text).toBe(headText('Hotfixes', '1'))
    expect(calls.reads.filter(url => url ===URL_1250).length).toBe(1)
  })

  test('when the shared one is the only hotfix, no Hotfixes heading draws', async ($, on) => {
    gh(on, () => prView('OPEN', ''), undefined, { remotes: { origin: ORIGIN }, list: () => listReply([SHARED]) })
    seat(on, copyOf('blocked-active'))
    await $.session.start(NEW_START)
    await $.command.run({ command: COMMAND })
    expect((await blockedView($, 'blocked-M111')).text).toBe(line1250('in review'))
    expect((await keysOf($)).filter(key => HOTFIX_KEY.test(key))).toEqual([])
  })
})

describe('the gh pr list call names an http(s) remote without its userinfo (M230 AC5)', () => {
  const FORMS: { name: string; remote: string; repo: string }[] = [
    { name: 'a user and token', remote: 'https://user:token@github.com/o/r.git', repo: 'https://github.com/o/r.git' },
    { name: 'a token alone', remote: 'https://token@github.com/o/r.git', repo: 'https://github.com/o/r.git' },
    { name: 'an scp-form ssh URL, kept as it is', remote: 'git@github.com:o/r.git', repo: 'git@github.com:o/r.git' },
  ]
  for (const form of FORMS) {
    test(form.name, async ($, on) => {
      const calls = gh(on, () => prView('MERGED'), undefined, {
        remotes: { origin: form.remote },
        list: () => listReply([pr(1265, 'hotfix-a')]),
      })
      seat(on, copyOf('blocked-active'))
      await $.session.start(NEW_START)
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.lists).toEqual([listCall(form.repo)])
      const recorded = [...calls.calls, ...calls.graphql, ...calls.git, ...calls.lists].flat()
      expect(recorded.filter(arg => arg.includes('token'))).toEqual([])
    })
  }
})

// Two presses in the same tick of a blocked line's `Finish`: the press marks
// itself busy before its first await, so the second runs nothing (M243 AC1).
describe('two presses at once of a blocked line Button run its command once (M243 AC1)', () => {
  test('cairn-pane-finish-M111', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-finish-M111'])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    await Promise.all([ui.press({ key: 'cairn-pane-finish-M111' }), ui.press({ key: 'cairn-pane-finish-M111' })])
    await ui.unmount()
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([{ command: 'cairn:milestone-review', args: 'M111' }])
  })
})

// A Status press and a ⌂ press in the same tick each mark `busy` before
// their first await, so only the press listed first runs (M243 AC2). ⌂
// marks itself since M241, so the ⌂-first order held before M243 too.
describe('a Status press and a ⌂ press at once run only the first one (M243 AC2)', () => {
  const ORDERS = [
    { keys: [PANE_STATUS, PANE_HOME], run: STATUS_RUN },
    { keys: [PANE_HOME, PANE_STATUS], run: CLEAR_RUN },
  ]
  for (const { keys, run } of ORDERS) {
    test(keys.join(' then '), async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      // Both Buttons are drawn, so each press reaches its handler.
      for (const key of keys) expect((await ui.findAll({ key })).length).toBe(1)
      await Promise.all(keys.map(key => ui.press({ key })))
      await ui.unmount()
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([run])
    })
  }
})

// A press whose checks fail takes its mark back, so the next free press
// runs (M243 AC4).
describe('a press whose checks fail leaves the next press free (M243 AC4)', () => {
  test('a Finish press during a step, then a Status press after the step ends', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await $.skill.prompt({ skill: 'cairn:milestone-implement', text: 'the prompt' })
    // Finish stays drawn while the step runs (M224 review).
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-finish-M111'])
    await pressKey($, 'cairn-pane-finish-M111')
    expect(copy.commands ?? []).toEqual([])
    await $.classic.Stop({ stop_hook_active: false, background_tasks: [] })
    await pressKey($, PANE_STATUS)
    expect(copy.commands).toEqual([STATUS_RUN])
  })

  test('a Finish press that reads a changed PR word, then a Status press', async ($, on) => {
    gh(on, () => prView('MERGED', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    // Once `changed` is set, every stored PR reads `closed`, which carries
    // the Check Button, not Finish, so the Finish press's check fails.
    let changed = false
    on('state.get', async ($, e, next) => {
      const got = await next(e)
      if (!changed || e.plugin !== 'cairn' || e.key !== 'prs') return got
      const read_ = (got as { value?: { version?: number; value?: { shape?: string; value?: Record<string, object> } } } | undefined)?.value
      const words = read_?.value?.value ?? {}
      const closed = Object.fromEntries(Object.entries(words).map(([url, each]) => [url, { ...each, word: 'closed' }]))
      return { value: { version: read_?.version ?? 0, value: { shape: read_?.value?.shape ?? 'prs-4', value: closed } } }
    })
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-finish-M111'])
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    changed = true
    await ui.press({ key: 'cairn-pane-finish-M111' })
    await ui.unmount()
    expect(copy.commands ?? []).toEqual([])
    // The press read `closed`, not an empty store: a drawing now carries
    // the Check Button.
    expect((await blockedView($, 'blocked-M111')).buttons).toEqual(['cairn-pane-check-M111'])
    await pressKey($, PANE_STATUS)
    expect(copy.commands).toEqual([STATUS_RUN])
  })
})

// M252: a candidate row that an open pull request's body names in a
// `Candidate row: <short title>` line counts as started, and since M261 the
// pane does not draw it. The items each case
// expects are written out by hand.
const bodied = (n: number, branch: string, body: unknown) => ({ ...pr(n, branch), body })

describe('startedRows reads the Candidate row lines of each listed body (M252 AC1)', () => {
  const read = (entries: unknown[]) => startedRows(listReply(entries) as { exitCode: number; stdout: string })

  test('every head branch counts, and each line gives one item', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', 'Fixes the parse.\n\nCandidate row: Pane edges (M238 review)\n'),
        bodied(2, 'm252-pane', 'Candidate row: Retitle edges\nCandidate row: Band in the app\'s code font'),
        bodied(3, 'feature-x', 'Candidate row: An idea for later'),
      ]),
    ).toEqual([
      { title: 'Pane edges (M238 review)', number: 1 },
      { title: 'Retitle edges', number: 2 },
      { title: "Band in the app's code font", number: 2 },
      { title: 'An idea for later', number: 3 },
    ])
  })

  test('the prefix must open the line, exactly', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', 'See Candidate row: Not this one\n  Candidate row: Nor this one\ncandidate row: Nor lower case\nCandidate row:No space'),
      ]),
    ).toEqual([])
  })

  test('the rest is trimmed, and an empty or blank rest gives no item', () => {
    expect(read([bodied(1, 'hotfix-a', 'Candidate row: \nCandidate row:    \nCandidate row:  Spaced title \t')])).toEqual([
      { title: 'Spaced title', number: 1 },
    ])
  })

  test('a CRLF body loses each line end', () => {
    expect(read([bodied(1, 'hotfix-a', 'Intro\r\nCandidate row: One\r\nCandidate row: Two\r\n')])).toEqual([
      { title: 'One', number: 1 },
      { title: 'Two', number: 1 },
    ])
  })

  test('an entry with a non-string body or a non-integer number gives none', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', null),
        pr(2, 'hotfix-b'),
        { ...bodied(3, 'hotfix-c', 'Candidate row: Three'), number: '3' },
        { ...bodied(4, 'hotfix-d', 'Candidate row: Four'), number: 4.5 },
        null,
        'Candidate row: Five',
        bodied(6, 'hotfix-f', 'Candidate row: Six'),
      ]),
    ).toEqual([{ title: 'Six', number: 6 }])
  })

  // M257: a line between a fence line and the next fence line names no row.
  test('a line inside a backtick, tilde, or indented fence gives no item', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', '```\nCandidate row: Inside backticks\n```\nCandidate row: After backticks'),
        bodied(2, 'hotfix-b', '~~~markdown\nCandidate row: Inside tildes\n~~~\nCandidate row: After tildes'),
        bodied(3, 'hotfix-c', 'Intro\n   ```\nCandidate row: Inside spaced\n  ```\nCandidate row: After spaced'),
      ]),
    ).toEqual([
      { title: 'After backticks', number: 1 },
      { title: 'After tildes', number: 2 },
      { title: 'After spaced', number: 3 },
    ])
  })

  test('any fence line closes an open fence, whatever its character', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', '```\nCandidate row: Inside mixed\n~~~\nCandidate row: After mixed'),
        bodied(2, 'hotfix-b', '~~~\nCandidate row: Inside mixed\n```\nCandidate row: After mixed'),
      ]),
    ).toEqual([
      { title: 'After mixed', number: 1 },
      { title: 'After mixed', number: 2 },
    ])
  })

  test('a fence that never closes hides the rest of its body only', () => {
    expect(
      read([
        bodied(1, 'hotfix-a', 'Candidate row: Before\n```\nCandidate row: Unclosed one\nCandidate row: Unclosed two'),
        bodied(2, 'hotfix-b', 'Candidate row: Next body'),
      ]),
    ).toEqual([
      { title: 'Before', number: 1 },
      { title: 'Next body', number: 2 },
    ])
  })

  test('a call that rejected, failed, or printed no JSON array gives null', () => {
    expect(startedRows(null)).toBe(null)
    expect(startedRows({ exitCode: 1, stdout: '[]\n' })).toBe(null)
    expect(startedRows({ exitCode: 0, stdout: 'HTTP 502\n' })).toBe(null)
    expect(startedRows({ exitCode: 0, stdout: '{"number":1}\n' })).toBe(null)
  })
})

describe('a candidate row that an item names is not drawn (M261 AC1, AC2)', () => {
  const state: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: [
      { priority: 'high', title: 'High row', text: 'High row' },
      { priority: 'normal', title: 'Normal row', text: 'Normal row' },
      { priority: 'low', title: 'Low row', text: 'Low row' },
      { priority: 'normal', title: 'Unmatched row', text: 'Unmatched row' },
      { priority: 'normal', title: 'Shared title', text: 'Shared title' },
      { priority: 'low', title: 'Shared title', text: 'Shared title' },
      { priority: 'normal', title: 'case row', text: 'case row' },
      { priority: 'normal', title: '', text: '' },
    ],
    blocked: [],
    taken: [],
  }
  const items = [
    { title: 'High row', number: 11 },
    { title: 'Normal row', number: 14 },
    { title: 'Normal row', number: 12 },
    { title: 'Low row', number: 13 },
    { title: 'Shared title', number: 15 },
    { title: 'Case row', number: 16 },
    { title: '', number: 17 },
  ]
  // A hidden row moves the rows after it up, so `rowsAbove` (M294) is left
  // out of the comparison.
  const withoutRow = ({ rowsAbove: _, ...rest }: PaneLine) => rest
  const rows = (acts: boolean, started = items) =>
    layout(state, [], acts, {}, [], started)
      .filter(line => /^candidate-\d+$/.test(line.key))
      .map(withoutRow)
  const heads = (started = items) => layout(state, [], true, {}, [], started).filter(line => line.key.startsWith('candidates-head'))

  for (const acts of [true, false]) {
    test(`matched rows draw no line, and each other line matches its line drawn with no items, by key (acts ${acts})`, () => {
      const got = rows(acts)
      const before = rows(acts, [])
      // Unmatched, a title that differs only by case, and an empty title.
      const kept = [3, 6, 7]
      expect(got.map(line => line.key)).toEqual(kept.map(i => `candidate-${i}`))
      // `before` draws in level order (M280), so each line is matched by key.
      got.forEach(line => expect([line.key, line]).toEqual([line.key, before.find(each => each.key === line.key)]))
    })

    // A hidden row between a high and a low row, the low one with an empty
    // short title, so neither a priority mark nor the ✎ rule shifts.
    test(`a hidden row between a high and an untitled low row leaves both as before (acts ${acts})`, () => {
      const three: PaneState = {
        ...state,
        candidates: [
          { priority: 'high', title: 'Up', text: 'Up' },
          { priority: 'normal', title: 'Taken', text: 'Taken' },
          { priority: 'low', title: '', text: '' },
        ],
      }
      const draw = (started: { title: string; number: number }[]) =>
        layout(three, [], acts, {}, [], started)
          .filter(line => /^candidate-\d+$/.test(line.key))
          .map(withoutRow)
      const before = draw([])
      const got = draw([{ title: 'Taken', number: 5 }])
      expect(got.map(line => line.key)).toEqual(['candidate-0', 'candidate-2'])
      expect(got).toEqual([before[0], before[2]])
      expect([got[0].lead[0], got[1].lead[0]]).toEqual([MARKS.high, MARKS.low])
      expect([got[0].buttons, got[1].buttons]).toEqual(acts ? [['plan'], undefined] : [undefined, undefined])
    })
  }

  test('the heading counts the drawn rows only (AC2)', () => {
    const [gap, head] = heads()
    expect([gap.key, head.key]).toEqual(['candidates-head-gap', 'candidates-head'])
    expect(head.lead.slice(-1)).toEqual([badgeOf(3)])
    // The control: with no items every row draws and counts.
    expect(heads([])[1].lead.slice(-1)).toEqual([badgeOf(state.candidates.length)])
  })

  test('with every row hidden there is no heading and no gap (AC2)', () => {
    // Every titled row, each named by one item. An empty title is never
    // hidden, so it is left out.
    const one: PaneState = { ...state, candidates: state.candidates.filter(row => row.title !== '') }
    const all = one.candidates.map((row, i) => ({ title: row.title, number: 100 + i }))
    const lines = layout(one, [], true, {}, [], all)
    expect(lines.filter(line => line.key.startsWith('candidate'))).toEqual([])
    // The control: with the first row's item gone, that row draws, with the
    // heading and its gap.
    expect(one.candidates[0].title).toBe('High row')
    const left = layout(one, [], true, {}, [], all.slice(1))
    expect(left.filter(line => /^candidate-\d+$/.test(line.key)).map(line => line.key)).toEqual(['candidate-0'])
    expect(left.filter(line => line.key.startsWith('candidates-head')).map(line => line.key)).toEqual([
      'candidates-head-gap',
      'candidates-head',
    ])
  })

  // The lines drawn with no items, written out by hand: each row once, in
  // level order (M280), with its priority mark, no tail, and ✎ on each
  // titled row while `acts` is true.
  test('with no items every candidate line draws, in level order', () => {
    const lines = rows(true, [])
    expect(lines.length).toBe(state.candidates.length)
    // Level order (M280): the high row, the five normal rows, then the two
    // low rows, written out by hand.
    expect(lines.map(line => line.key)).toEqual([0, 1, 3, 4, 6, 7, 2, 5].map(i => `candidate-${i}`))
    lines.forEach(line => {
      const i = Number(line.key.slice('candidate-'.length))
      const row = state.candidates[i]
      expect([i, line.lead, line.tail]).toEqual([i, [MARKS[row.priority], { text: ' ' }], undefined])
      expect([i, line.text]).toEqual([i, row.priority === 'low' ? { text: row.title, color: GRAY } : { text: row.title }])
      expect([i, line.buttons, line.target]).toEqual(row.title === '' ? [i, undefined, undefined] : [i, ['plan'], `${i}`])
    })
  })
})

// M258: a counted ` — started <ref>` token on the row marks it too. The
// reader keeps an `M<NNN>` token only while its milestone is `planned` or
// `blocked` (reader.test.ts), so `taken` here holds counted M tokens.
describe('a candidate row that a started token marks is not drawn (M258 AC1-AC3, M261 AC1)', () => {
  const titles = ['Planned', 'Blocked', 'Two ids', 'Listed', 'Unlisted', 'Two numbers', 'Body and id', 'Number and id', 'Body and number', 'Plain']
  const state: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: titles.map(title => ({ priority: 'normal', title, text: title })),
    blocked: [],
    taken: [],
  }
  const hotfix = (number: number) => ({ number, title: `Fix ${number}`, url: `https://github.com/o/r/pull/${number}` })
  const draw = (taken: PaneState['taken'], hotfixes = [hotfix(301), hotfix(302), hotfix(305)], started: { title: string; number: number }[] = []) =>
    layout({ ...state, taken }, [], true, {}, hotfixes, started).filter(line => /^candidate-\d+$/.test(line.key))
  // A hidden row draws no line under its key. A drawn row keeps its index
  // in `state.candidates` as its key and its ✎ target (M261).
  const hidden = (lines, i: number) => expect([i, lines.find(line => line.key === `candidate-${i}`)]).toEqual([i, undefined])
  const plain = (lines, i: number) => {
    const line = lines.find(each => each.key === `candidate-${i}`)
    expect([i, line?.lead[0], line?.tail, line?.text]).toEqual([i, MARKS.normal, undefined, { text: titles[i] }])
    expect([i, line?.buttons, line?.target]).toEqual([i, ['plan'], `${i}`])
  }

  test('a counted milestone id hides its row (AC1)', () => {
    const lines = draw([
      { title: 'Planned', ref: 'M258' },
      { title: 'Blocked', ref: 'M240' },
      { title: 'Two ids', ref: 'M300' },
      { title: 'Two ids', ref: 'M259' },
    ])
    hidden(lines, 0)
    hidden(lines, 1)
    hidden(lines, 2)
    for (let i = 3; i < titles.length; i++) plain(lines, i)
  })

  // The milestone row and its neighbours in table order, as M261 AC1 asks.
  test('a hidden row between two plain rows leaves them drawn in order', () => {
    const lines = draw([{ title: 'Unlisted', ref: 'M258' }])
    expect(lines.map(line => line.key)).toEqual(titles.map((_, i) => `candidate-${i}`).filter(key => key !== 'candidate-4'))
    plain(lines, 3)
    plain(lines, 5)
  })

  test('a #n token hides its row only while the open hotfix list holds n (AC2)', () => {
    const taken = [
      { title: 'Listed', ref: '#301' },
      { title: 'Unlisted', ref: '#999' },
      { title: 'Two numbers', ref: '#998' },
      { title: 'Two numbers', ref: '#305' },
    ]
    const lines = draw(taken)
    plain(lines, 2)
    hidden(lines, 3)
    plain(lines, 4)
    hidden(lines, 5)
    plain(lines, 6)
    // With no hotfix list, as before any read or for another root, no #n
    // token counts.
    const none = draw(taken, [])
    titles.forEach((_, i) => plain(none, i))
  })

  test('a body line, a #n token, and a milestone id in any mix hide the row (AC3)', () => {
    const lines = draw(
      [
        { title: 'Body and id', ref: 'M258' },
        { title: 'Number and id', ref: 'M258' },
        { title: 'Number and id', ref: '#302' },
        { title: 'Body and number', ref: '#301' },
      ],
      undefined,
      [
        { title: 'Body and id', number: 400 },
        { title: 'Body and number', number: 350 },
      ],
    )
    hidden(lines, 6)
    hidden(lines, 7)
    hidden(lines, 8)
    plain(lines, 9)
  })

  // The reader's filter and the drawing together (M258 review return 1):
  // an id counts only while its table row is `planned` or `blocked`.
  test('a done, dropped, or absent id leaves the row drawn, planned and blocked hide it (AC1)', () => {
    const roadmap = [
      '| ID | Title | Status | Depends on | Priority | File/Archive |',
      '|---|---|---|---|---|---|',
      '| M258 | P | planned | — | normal | m |',
      '| M240 | B | blocked | — | normal | m |',
      '| M230 | D | done | — | normal | m |',
      '| M231 | X | dropped | — | normal | m |',
      '',
      '## Candidates',
      '',
      '- Planned: x — started M258',
      '- Blocked: x — started M240',
      '- Done: x — started M230',
      '- Dropped: x — started M231',
      '- Absent: x — started M999',
      '- Two ids: x — started M230 — started M240',
    ].join('\n')
    const candidates = candidateRows(roadmap)
    const lines = layout(
      { ...state, candidates, taken: takenRows(roadmap, parseRoadmapRows(roadmap)) },
      [],
      true,
      {},
      [],
      [],
    ).filter(line => /^candidate-\d+$/.test(line.key))
    expect(candidates.map(row => row.title)).toEqual(['Planned', 'Blocked', 'Done', 'Dropped', 'Absent', 'Two ids'])
    expect(lines.map(line => [line.key, line.text?.text, line.target])).toEqual([
      ['candidate-2', 'Done', '2'],
      ['candidate-3', 'Dropped', '3'],
      ['candidate-4', 'Absent', '4'],
    ])
  })

  test('a token on a row with an empty short title hides nothing', () => {
    const lines = layout(
      { ...state, candidates: [{ priority: 'normal', title: '', text: '' }], taken: [{ title: '', ref: 'M258' }] },
      [],
      true,
      {},
      [],
      [],
    ).filter(line => /^candidate-\d+$/.test(line.key))
    expect([lines[0].lead[0], lines[0].tail, lines[0].buttons]).toEqual([MARKS.normal, undefined, undefined])
  })
})

// The candidates-parked fixture (M284): parked rows above and among other
// levels, three misspelled or misplaced tokens read as normal, and a parked
// row with an empty short title. Its drawn order, by index and text,
// written out by hand.
const PARKED_LINES: [number, string][] = [
  [1, '○ Normal row'],
  [2, '○ [PARKED] Upper-case parked, read as normal'],
  [3, '○ [parked]No space after the parked token, kept in the title'],
  [4, '○ Token [parked] mid-row, read as normal'],
  [5, '↓ Low row'],
  [0, '⧗ Parked first'],
  [6, '⧗ '],
  [7, '⧗ Parked last'],
]

describe('a parked candidate row draws last, with a gray hourglass (M284 AC3)', () => {
  for (const surface of SURFACES) {
    test(`the candidates-parked fixture draws parked rows after the low row (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates-parked'))
      await $.turn.complete(turn())
      const lines = await paneLines($, surface)
      expect(textAt(lines, 'candidates-head')).toBe(countHead('Candidates', 8, surface))
      const rows = keysLike(lines, /^candidate-\d+$/)
      expect(rows).toEqual(PARKED_LINES.map(([i]) => `candidate-${i}`))
      expect(rows.map(k => textAt(lines, k))).toEqual(PARKED_LINES.map(([, text]) => text))
    })

    test(`a parked row's mark and title are gray (${surface})`, async ($, on) => {
      seat(on, copyOf('candidates-parked'))
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface, ...PANE_VIEW })) as Ui
      const [lead] = await ui.findAll({ key: 'candidate-0-lead' })
      expect(textOf(kids(lead)[0])).toBe('⧗')
      // On the desktop the mark draws as its icon (M286).
      if (surface === 'terminal') expect(kids(lead)[0].props.color).toBe('inactive')
      else expect(kids(lead)[0].type).toBe('Svg')
      const titleOf = async (i: number) => kids((await ui.findAll({ key: `candidate-${i}-text` }))[0])[0]
      expect((await titleOf(0)).props.color).toBe('inactive')
      // The control: an untagged row's title has no color.
      expect((await titleOf(1)).props.color).toBe(undefined)
      await ui.unmount()
    })

    test(`✎ on the first parked row plans it (${surface})`, async ($, on) => {
      const copy = copyOf('candidates-parked')
      seat(on, copy)
      await $.turn.complete(turn())
      await pressKey($, 'cairn-pane-plan-0')
      expect(copy.commands).toEqual([CLEAR_RUN])
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 2)
      expect(copy.commands).toEqual([CLEAR_RUN, { command: 'cairn:milestone-plan', args: 'Parked first' }])
    })
  }

  const state: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: [
      { priority: 'parked', title: 'Waits', text: 'Waits' },
      { priority: 'parked', title: '', text: '' },
      { priority: 'high', title: 'Up', text: 'Up' },
      { priority: 'parked', title: 'Taken', text: 'Taken' },
    ],
    blocked: [],
    taken: [],
  }
  const draw = (acts: boolean, started: { title: string; number: number }[] = []) =>
    layout(state, [], acts, {}, [], started).filter(line => /^candidate-\d+$/.test(line.key))

  for (const acts of [true, false]) {
    test(`a parked row's ✎, key, and target follow the rules of any row (acts ${acts})`, () => {
      const lines = draw(acts)
      expect(lines.map(line => line.key)).toEqual(['candidate-2', 'candidate-0', 'candidate-1', 'candidate-3'])
      const waits = lines[1]
      expect([waits.lead, waits.tail, waits.text]).toEqual([[MARKS.parked, { text: ' ' }], undefined, { text: 'Waits', color: GRAY }])
      expect([waits.buttons, waits.target, waits.title]).toEqual(acts ? [['plan'], '0', 'Waits'] : [undefined, undefined, undefined])
      // A parked row with an empty short title has no ✎, as any such row.
      expect([lines[2].buttons, lines[2].target]).toEqual([undefined, undefined])
    })
  }

  test('a started parked row is hidden, and the heading counts the drawn rows', () => {
    const lines = layout(state, [], true, {}, [], [{ title: 'Taken', number: 7 }])
    expect(lines.filter(line => /^candidate-\d+$/.test(line.key)).map(line => line.key)).toEqual([
      'candidate-2',
      'candidate-0',
      'candidate-1',
    ])
    expect(lines.find(line => line.key === 'candidates-head')?.lead.slice(-1)).toEqual([badgeOf(3)])
  })
})

// The copy's one candidate row: a read whose items name it hides the row,
// and with it the Candidates heading (M261 AC1, AC2).
describe('the pane read stores the items with the hotfix list and hides the rows they name (M252 AC3, M261)', () => {
  const STARTED_BODY = 'Fixes it.\nCandidate row: An idea for later\n'
  const HIDDEN = undefined
  const PLAIN = '○ An idea for later'
  const GOOD = () => listReply([bodied(1265, 'm252-pane', STARTED_BODY)])
  const candidateLine = async $ => (await linesAt($)).find(line => line.key === 'candidate-0')?.text

  test('the call asks for body, a read hides the line, and the Hotfixes section skips an m-branch', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, list: GOOD })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.lists).toEqual([listCall(ORIGIN)])
    expect(await candidateLine($)).toBe(HIDDEN)
    expect((await keysOf($)).filter(key => key.startsWith('candidate'))).toEqual([])
    // The control: the pane drew, with its blocked rows (M261 review).
    expect(await keysOf($)).toContain('blocked-M101')
    expect((await keysOf($)).filter(key => HOTFIX_KEY.test(key))).toEqual([])
  })

  test('a failed call in the same root keeps the row hidden', async ($, on) => {
    let answer: () => GhAnswer = GOOD
    gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, list: () => answer() })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect(await candidateLine($)).toBe(HIDDEN)
    answer = () => 'reject'
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(HIDDEN)
    answer = () => listReply([])
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(PLAIN)
    // The drawn line carries ✎ again (M252 review).
    expect((await blockedView($, 'candidate-0')).buttons).toEqual([`${PANE_PLAN}-0`])
  })

  test('a root with no base-remote URL draws the row again', async ($, on) => {
    const remotes: Record<string, string> = { origin: ORIGIN }
    gh(on, () => prView('MERGED'), undefined, { remotes, list: GOOD })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect(await candidateLine($)).toBe(HIDDEN)
    delete remotes.origin
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(PLAIN)
  })

  test('a failed call in another root draws the row the first root hid', async ($, on) => {
    let answer: () => GhAnswer = GOOD
    gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, list: () => answer() })
    const copy = copyOf('blocked-prs')
    for (const path of Object.keys(copy.files)) copy.files[`/other${path}`] = copy.files[path]
    copy.unreadable.push(...copy.unreadable.map(path => `/other${path}`))
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    expect(await candidateLine($)).toBe(HIDDEN)
    answer = () => 'reject'
    copy.cwd = '/other'
    await $.turn.complete(turn())
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(PLAIN)
    // Back in the first root, a failed call finds the other root's empty
    // value, not the first root's items.
    copy.cwd = '/'
    await $.turn.complete(turn())
    await pressKey($, 'cairn-pane-refresh')
    expect(await candidateLine($)).toBe(PLAIN)
  })
})

// A one-shot hold on the mod's `step` read. It is armed after mount, since
// the draw reads the key too, and it fires once, so the session end's
// update of the key passes (M255).
function holdStep(on: On) {
  let open = () => {}
  const gate = new Promise<void>(resolve => (open = resolve))
  const hold = { armed: false, held: false, release: () => open() }
  on('state.get', async ($, e, next) => {
    if (hold.armed && e.plugin === 'cairn' && e.key === 'step') {
      hold.armed = false
      hold.held = true
      await gate
    }
    return next(e)
  })
  return hold
}

describe('a press check cut off by a session end frees the Buttons and runs nothing late (M255 AC1, AC2)', () => {
  test('a Status press after the end runs once, and the cut-off press runs nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    const hold = holdStep(on)
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    hold.armed = true
    const first = ui.press({ key: PANE_STATUS })
    await until(() => hold.held)
    expect(hold.held).toBe(true)
    expect(copy.commands ?? []).toEqual([])
    await $.session.end(CLEAR_END)
    await ui.press({ key: PANE_STATUS })
    expect(copy.commands).toEqual([STATUS_RUN])
    hold.release()
    await first
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([STATUS_RUN])
    await ui.unmount()
  })

  // While the end beneath is still running, the cut-off press's mark keeps
  // a new press from reading the state of the session that is ending.
  test('a press during the end, while a cut-off press reads, runs nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    const hold = holdStep(on)
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    hold.armed = true
    const first = ui.press({ key: PANE_STATUS })
    await until(() => hold.held)
    let finish = () => {}
    copy.endHold = new Promise<void>(resolve => (finish = resolve))
    const end = $.session.end(CLEAR_END)
    await sleep(20)
    await ui.press({ key: PANE_STATUS })
    expect(copy.commands ?? []).toEqual([])
    copy.endHold = undefined
    finish()
    await end
    hold.release()
    await first
    await ui.press({ key: PANE_STATUS })
    expect(copy.commands).toEqual([STATUS_RUN])
    await ui.unmount()
  })

  // A next-step press whose checks would hold its command for a `/clear`.
  const name = PANE_CLEAR_FIRST[0]
  test(`${name}: a cut-off next-step press holds nothing for a later clear end`, async ($, on) => {
    const copy = copyOf(name)
    const hold = holdStep(on)
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    hold.armed = true
    const first = ui.press({ key: PANE_NEXT })
    await until(() => hold.held)
    expect(hold.held).toBe(true)
    expect(copy.commands ?? []).toEqual([])
    await $.session.end(CLEAR_END)
    hold.release()
    await first
    await untilRuns(copy, 1, 10)
    expect(copy.commands ?? []).toEqual([])
    await $.session.end(CLEAR_END)
    await untilRuns(copy, 1, 10)
    expect(copy.commands ?? []).toEqual([])
    await ui.unmount()
  })
})

describe("a ⌂ press's open still runs when the session end beneath rejects (M255 AC3)", () => {
  test('a clear end whose next(e) rejects opens the pane once', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const before = copy.opens.length
    await pressKey($, PANE_HOME)
    copy.endThrows = true
    let rejected = false
    try {
      await $.session.end(CLEAR_END)
    } catch {
      rejected = true
    }
    expect(rejected).toBe(true)
    await untilOpens(copy, before + 1)
    await untilOpens(copy, before + 2, 10)
    expect(copy.opens.slice(before)).toEqual([{ id: PANE, title: 'cairn' }])
  })

  test('a clear end whose next(e) rejects, with no press, opens nothing', async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    const before = copy.opens.length
    copy.endThrows = true
    let rejected = false
    try {
      await $.session.end(CLEAR_END)
    } catch {
      rejected = true
    }
    expect(rejected).toBe(true)
    await untilOpens(copy, before + 1, 10)
    expect(copy.opens.length).toBe(before)
  })
})

// A session end that rejects frees the action Buttons, so a press whose
// `/clear` run never settles leaves none dead (M260 AC1).
describe('a rejected session end frees the action Buttons (M260 AC1)', () => {
  test("a Status press after a rejected end runs, while the ⌂ press's /clear never settles", async ($, on) => {
    const copy = copyOf('single-in-progress')
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    let settle = () => {}
    copy.runHold = new Promise<void>(resolve => (settle = resolve))
    void ui.press({ key: PANE_HOME })
    await untilRuns(copy, 1)
    expect(copy.commands).toEqual([CLEAR_RUN])
    copy.endThrows = true
    let rejected = false
    try {
      await $.session.end(CLEAR_END)
    } catch {
      rejected = true
    }
    expect(rejected).toBe(true)
    copy.endThrows = undefined
    void ui.press({ key: PANE_STATUS })
    await untilRuns(copy, 2)
    expect(copy.commands).toEqual([CLEAR_RUN, STATUS_RUN])
    copy.runHold = undefined
    settle()
    await ui.unmount()
  })

  // A press made while the end beneath is pending keeps its run when the
  // end settles, resolved or rejected, so a second press does not run
  // beside it (M260 review, PR #271).
  for (const rejects of [false, true]) {
    test(`a press made during a ${rejects ? 'rejecting' : 'resolving'} end keeps its run past the end`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      let finish = () => {}
      copy.endHold = new Promise<void>(resolve => (finish = resolve))
      copy.endThrows = rejects ? true : undefined
      const end = $.session.end(CLEAR_END).then(
        () => false,
        () => true,
      )
      await sleep(20)
      let settle = () => {}
      copy.runHold = new Promise<void>(resolve => (settle = resolve))
      void ui.press({ key: PANE_STATUS })
      await untilRuns(copy, 1)
      expect(copy.commands).toEqual([STATUS_RUN])
      copy.endHold = undefined
      finish()
      expect(await end).toBe(rejects)
      copy.endThrows = undefined
      void ui.press({ key: PANE_STATUS })
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([STATUS_RUN])
      copy.runHold = undefined
      settle()
      await ui.unmount()
    })
  }

  // A press whose checks are still reading at the rejected end leaves the
  // shared press mark free too, so a later press runs (M260 review).
  test('a Status press after a rejected end that cut off a press still reading runs once', async ($, on) => {
    const copy = copyOf('single-in-progress')
    const hold = holdStep(on)
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    hold.armed = true
    const first = ui.press({ key: PANE_STATUS })
    await until(() => hold.held)
    expect(hold.held).toBe(true)
    copy.endThrows = true
    let rejected = false
    try {
      await $.session.end(CLEAR_END)
    } catch {
      rejected = true
    }
    expect(rejected).toBe(true)
    copy.endThrows = undefined
    await ui.press({ key: PANE_STATUS })
    expect(copy.commands).toEqual([STATUS_RUN])
    hold.release()
    await first
    await untilRuns(copy, 2, 10)
    expect(copy.commands).toEqual([STATUS_RUN])
    await ui.unmount()
  })
})

// A held command that a rejected session end drops goes to the prompt box,
// and a toast says why, for an end of either reason (M260 AC2).
describe('a rejected session end hands its held command to the prompt box (M260 AC2)', () => {
  const name = PANE_CLEAR_FIRST[0]
  for (const reason of ['clear', 'other'] as const) {
    test(`${name}: a rejected ${reason} end fills the held command and toasts`, async ($, on) => {
      const copy = copyOf(name)
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      await ui.press({ key: PANE_NEXT })
      expect(copy.commands).toEqual([CLEAR_RUN])
      copy.endThrows = true
      let rejected = false
      try {
        await $.session.end({ reason, sessionId: 's1' })
      } catch {
        rejected = true
      }
      expect(rejected).toBe(true)
      const run = runOf(name)
      const line = run.args === '' ? `/${run.command}` : `/${run.command} ${run.args}`
      for (let i = 0; i < 200 && ((copy.toasts ?? []).length < 1 || (copy.fills ?? []).length < 1); i++) await sleep(5)
      expect(copy.fills).toEqual([{ text: line, mode: 'append' }])
      expect(copy.toasts).toEqual([`cairn: the session end failed (${line})`])
      await untilRuns(copy, 2, 10)
      expect(copy.commands).toEqual([CLEAR_RUN])
      await ui.unmount()
    })
  }
})

// A session end that lands while a ⌂ press reads its step cancels the
// press, so its `/clear` never reaches the conversation that follows. A
// `clear` end still gives the pane the open it gives any ⌂ mark, and an
// `other` end none (M260 AC3).
describe("a session end during a ⌂ press's step read cancels its /clear (M260 AC3)", () => {
  const ENDS = [
    { name: 'a resolving clear end', reason: 'clear', rejects: false, opens: 1 },
    { name: 'a rejecting clear end', reason: 'clear', rejects: true, opens: 1 },
    { name: 'a resolving other end', reason: 'other', rejects: false, opens: 0 },
    { name: 'a rejecting other end', reason: 'other', rejects: true, opens: 0 },
  ] as const
  for (const { name, reason, rejects, opens } of ENDS) {
    test(`${name} runs no /clear and opens the pane ${opens} time(s)`, async ($, on) => {
      const copy = copyOf('single-in-progress')
      const hold = holdStep(on)
      seat(on, copy)
      await $.turn.complete(turn())
      const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
      hold.armed = true
      const first = ui.press({ key: PANE_HOME })
      await until(() => hold.held)
      expect(hold.held).toBe(true)
      expect(copy.commands ?? []).toEqual([])
      const before = copy.opens.length
      copy.endThrows = rejects ? true : undefined
      let rejected = false
      try {
        await $.session.end({ reason, sessionId: 's1' })
      } catch {
        rejected = true
      }
      expect(rejected).toBe(rejects)
      copy.endThrows = undefined
      hold.release()
      await first
      await untilRuns(copy, 1, 10)
      expect(copy.commands ?? []).toEqual([])
      await untilOpens(copy, before + opens)
      await untilOpens(copy, before + opens + 1, 10)
      expect(copy.opens.slice(before)).toEqual(opens === 1 ? [{ id: PANE, title: 'cairn' }] : [])
      await ui.unmount()
    })
  }
})

// A ⌂ press whose read of the stored step rejects takes its mark back, so
// it runs no `/clear` and a later press runs (M278 AC1). The hook answers
// `{ deny }` for the one read, since a hook that throws is skipped.
describe("a ⌂ press whose step read rejects leaves the Buttons free (M278 AC1)", () => {
  test('the ⌂ press runs no /clear, and a Status press after it runs', async ($, on) => {
    const copy = copyOf('single-in-progress')
    const deny = { armed: false, denied: 0 }
    on('state.get', async ($, e, next) => {
      if (deny.armed && e.plugin === 'cairn' && e.key === 'step') {
        deny.armed = false
        deny.denied += 1
        return { deny: 'the store refused the read' }
      }
      return next(e)
    })
    seat(on, copy)
    await $.turn.complete(turn())
    const ui = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...PANE_VIEW })) as Ui
    deny.armed = true
    let message: string | undefined
    try {
      await ui.press({ key: PANE_HOME })
    } catch (error) {
      message = error instanceof Error ? error.message : String(error)
    }
    // The press rejects with the denied read's reason, so the one denial
    // was the ⌂ press's own read (M278 review).
    expect(message).toContain('the store refused the read')
    expect(deny.denied).toBe(1)
    await untilRuns(copy, 1, 10)
    expect(copy.commands ?? []).toEqual([])
    await ui.press({ key: PANE_STATUS })
    await untilRuns(copy, 1)
    expect(copy.commands).toEqual([STATUS_RUN])
    await ui.unmount()
  })
})

// A start's second pane listing that is still pending at a session end
// reads nothing when it answers, even placed and with a later start's read
// owed, so the read a later start owes is that start's; here the pane's next
// draw makes it (M260 AC4).
describe('a second listing pending at a session end reads nothing (M260 AC4)', () => {
  test("the old start's placed second listing adds no read, and the next draw reads once", async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    copy.open = [PANE]
    copy.unplaced = [PANE]
    let releaseFirst = () => {}
    let releaseSecond = () => {}
    copy.panesHold = new Promise<void>(resolve => {
      releaseFirst = resolve
    })
    const second = new Promise<void>(resolve => {
      releaseSecond = resolve
    })
    const old = $.classic.SessionStart({ source: 'clear' })
    try {
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(false)
      // The second listing's answer is computed placed when it is held.
      copy.unplaced = []
      copy.panesHold = second
      releaseFirst()
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHold).toBeUndefined()
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(true)
      await $.session.end(CLEAR_END)
      // The new start lists the pane unplaced twice, so it owes a read and
      // makes none.
      copy.unplaced = [PANE]
      await $.classic.SessionStart({ source: 'clear' })
      await calls.settled()
      expect(calls.reads).toEqual([])
    } finally {
      releaseFirst()
      releaseSecond()
    }
    await old
    await calls.settled()
    expect(calls.reads).toEqual([])
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })

  // The same holds one list earlier: a first listing pending at a session
  // end reads nothing when it answers placed, and leaves the later start's
  // owed read in place (M260 review).
  test("the old start's placed first listing adds no read, and the next draw reads once", async ($, on) => {
    const calls = gh(on, () => prView('OPEN', ''))
    const copy = copyOf('blocked-active')
    seat(on, copy)
    copy.open = [PANE]
    copy.unplaced = []
    let release = () => {}
    copy.panesHold = new Promise<void>(resolve => {
      release = resolve
    })
    const old = $.classic.SessionStart({ source: 'clear' })
    try {
      await until(() => copy.panesHold === undefined)
      expect(copy.panesHeld?.find(open => open.id === PANE)?.isPlaced).toBe(true)
      await $.session.end(CLEAR_END)
      copy.unplaced = [PANE]
      await $.classic.SessionStart({ source: 'clear' })
      await calls.settled()
      expect(calls.reads).toEqual([])
    } finally {
      release()
    }
    await old
    await calls.settled()
    expect(calls.reads).toEqual([])
    await draw($)
    await calls.settled()
    expect(calls.reads).toEqual([URL_1250])
  })
})

// While planning, the Next line names the first `[high]` row that the
// Candidates list draws and the next-step press plans it; with no such row
// both name no title (M272 AC4, M273 AC3). The titles are written out by
// hand from the fixtures' ROADMAPs.
describe("planning's Next line and press name the first drawn [high] row (M272 AC4, M273 AC3)", () => {
  const PLAN = { action: 'plan the next milestone', command: '/milestone-plan', id: null, title: null }
  const ROWS: PaneState['candidates'] = [
    { priority: 'normal', title: 'Plain row', text: 'Plain row' },
    { priority: 'high', title: 'First high', text: 'First high' },
    { priority: 'high', title: 'Second high', text: 'Second high' },
  ]
  const plan = (candidates = ROWS, taken: PaneState['taken'] = []): PaneState => ({
    found: true,
    milestones: [],
    next: PLAN,
    workable: [],
    waiting: [],
    candidates,
    blocked: [],
    taken,
  })
  const nextText = (state: PaneState, started: { title: string; number: number }[] = []) =>
    layout(state, [], true, {}, [], started).find(line => line.key === 'next')?.text?.text
  const hotfix = (number: number) => ({ number, title: 'Fix', url: `https://github.com/o/r/pull/${number}` })

  test('the pick passes over each row the list hides and names the first it draws', () => {
    expect(nextTitle(PLAN, ROWS, [], [], [])).toBe('First high')
    // An open PR body naming the first `[high]` row: the second is named.
    expect(nextTitle(PLAN, ROWS, [], [], [{ title: 'First high', number: 5 }])).toBe('Second high')
    // A `#` token whose PR is in the open hotfix list hides the row, and
    // the same token with the PR not in the list hides nothing.
    const hashed = [{ title: 'First high', ref: '#41' }]
    expect(nextTitle(PLAN, ROWS, hashed, [hotfix(41)], [])).toBe('Second high')
    expect(nextTitle(PLAN, ROWS, hashed, [hotfix(42)], [])).toBe('First high')
    // A counted `M` token hides every row with its short title (the
    // readers' `takenRows` gives tokens by title, so a same-titled sibling's
    // token arrives here as this entry), and the pick moves on.
    expect(nextTitle(PLAN, ROWS, [{ title: 'First high', ref: 'M005' }], [], [])).toBe('Second high')
    // Every `[high]` row hidden: no title.
    const both = [
      { title: 'First high', ref: 'M005' },
      { title: 'Second high', ref: '#41' },
    ]
    expect(nextTitle(PLAN, ROWS, both, [hotfix(41)], [])).toBe(null)
    // Outside planning, no title.
    expect(nextTitle({ ...PLAN, action: 'implement', command: '/milestone-implement', id: 'M003' }, ROWS, [], [], [])).toBe(null)
  })

  test('the line names the pick, and with no drawn [high] row shows the command alone', () => {
    expect(nextText(plan())).toBe('/milestone-plan First high')
    expect(nextText(plan(), [{ title: 'First high', number: 5 }])).toBe('/milestone-plan Second high')
    expect(nextText(plan([ROWS[0]]))).toBe('/milestone-plan')
  })

  const CASES = [
    { name: 'high-candidate', args: 'Chosen row' },
    { name: 'candidates-skeleton', args: '' },
  ]
  for (const { name, args } of CASES) {
    test(`${name}: the press runs /clear, then planning with ${args === '' ? 'no arguments' : 'the title'}`, async ($, on) => {
      const copy = copyOf(name)
      seat(on, copy)
      await $.turn.complete(turn())
      expect(textAt(await paneLines($, 'desktop'), 'next')).toBe(`→ /milestone-plan${args === '' ? '' : ` ${args}`}`)
      await pressKey($, PANE_NEXT)
      expect(copy.commands).toEqual([CLEAR_RUN])
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 2)
      expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args }])
    })
  }

  for (const [body, args] of [
    ['Candidate row: Chosen row\n', 'Later high'],
    ['Candidate row: Later high\n', 'Chosen row'],
  ] as const) {
    test(`a body naming ${args === 'Later high' ? 'the row moves planning to the next drawn row' : 'another row keeps the title'} on the line and the press`, async ($, on) => {
      const calls = gh(on, () => prView('MERGED'), undefined, {
        remotes: { origin: ORIGIN },
        list: () => listReply([bodied(1265, 'm272-x', body)]),
      })
      const copy = copyOf('high-candidate')
      seat(on, copy)
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.lists).toEqual([listCall(ORIGIN)])
      const next = (await linesAt($)).find(line => line.key === 'next')?.text ?? ''
      expect(next).toBe(`→ /milestone-plan ${args}`)
      await pressKey($, PANE_NEXT)
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 2)
      expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args }])
      // The band's Plan shares the press, and reads the same stored list.
      const band = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
      await band.press({ key: 'cairn-next' })
      await band.unmount()
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 4)
      expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args }, CLEAR_RUN, { command: PLAN_COMMAND, args }])
    })
  }

  // The callers pass the open hotfix list to the pick (M273 review): a
  // `#41` token on "Chosen row" hides it while hotfix PR 41 is open, and
  // the line and both presses then plan "Later high"; with another hotfix
  // PR open, the token hides nothing.
  for (const [open, args] of [
    [41, 'Later high'],
    [42, 'Chosen row'],
  ] as const) {
    test(`a #41 token with hotfix PR ${open} open names ${args} on the line and the press`, async ($, on) => {
      const calls = gh(on, () => prView('MERGED'), undefined, {
        remotes: { origin: ORIGIN },
        list: () => listReply([pr(open, 'hotfix-x')]),
      })
      const copy = copyOf('high-candidate')
      const path = Object.keys(copy.files).find(key => key.endsWith('/cairn/ROADMAP.md')) as string
      copy.files[path] = copy.files[path].replace(' — started M001\n', ' — started M001 — started #41\n')
      seat(on, copy)
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      const next = (await linesAt($)).find(line => line.key === 'next')?.text ?? ''
      expect(next).toBe(`→ /milestone-plan ${args}`)
      await pressKey($, PANE_NEXT)
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 2)
      expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args }])
      const band = (await $.ui.mount({ plugin: 'cairn', surface: 'desktop', ...BAND })) as Ui
      await band.press({ key: 'cairn-next' })
      await band.unmount()
      await $.session.end(CLEAR_END)
      await untilRuns(copy, 4)
      expect(copy.commands).toEqual([CLEAR_RUN, { command: PLAN_COMMAND, args }, CLEAR_RUN, { command: PLAN_COMMAND, args }])
    })
  }
})

describe('the card counts the drawn candidate rows by level and the planned and blocked milestones (M286 AC2)', () => {
  // Rows at all four levels and one started row, which the list hides and
  // the card leaves out; two planned milestones and one blocked one. The
  // counts are written out by hand.
  const idle: PaneState = {
    found: true,
    milestones: [],
    next: { action: 'plan the next milestone', command: '/milestone-plan', id: null, title: null },
    workable: [{ id: 'M3', title: 'Ready' }],
    waiting: [{ id: 'M4', title: 'Later', unmet: ['M3'] }],
    candidates: [
      { priority: 'low', title: 'Low one', text: 'Low one' },
      { priority: 'high', title: 'High one', text: 'High one' },
      { priority: 'normal', title: 'Normal one', text: 'Normal one' },
      { priority: 'normal', title: 'Started one', text: 'Started one' },
      { priority: 'parked', title: 'Parked one', text: 'Parked one' },
      { priority: 'normal', title: 'Normal two', text: 'Normal two' },
    ],
    blocked: [{ id: 'M5', title: 'Handed off', pr: null, url: null, archived: false }],
    taken: [{ title: 'Started one', ref: 'M3' }],
  }
  const active: PaneState = {
    ...idle,
    milestones: [{ id: 'M2', title: 'Now', status: 'in-progress', file: null }],
    next: { action: 'resume', command: '/milestone-implement', id: 'M2', title: null },
  }
  const CARD = [
    ['card-repo', '? PRs   ? issues'],
    ['card-candidates', 'candidates ↑ 1   ○ 2   ↓ 1   ⧗ 1'],
    ['card-milestones', '2 planned · 1 blocked'],
  ]
  const cardOf = (state: PaneState) =>
    layout(state, [], true)
      .filter(line => line.card)
      .map(line => [line.key, [...line.lead, ...(line.text === null ? [] : [line.text]), ...(line.tail ?? [])].map(span => span.text).join('')])

  test('with no active milestone, the card matches the drawn list', () => {
    expect(cardOf(idle)).toEqual(CARD)
    const drawn = layout(idle, [], true).filter(line => /^candidate-\d+$/.test(line.key))
    expect(drawn.length).toBe(5)
    expect(drawn.map(line => line.title)).not.toContain('Started one')
  })

  test('with an active milestone, the list is gone and the card counts the same rows', () => {
    expect(cardOf(active)).toEqual(CARD)
    expect(layout(active, [], true).filter(line => /^candidate-\d+$/.test(line.key))).toEqual([])
  })

  test('the card leads the pane, and the no-active line and the milestones follow it', () => {
    expect(layout(idle, [], true).map(line => line.key).slice(0, 5)).toEqual([
      'card-repo',
      'card-candidates',
      'card-milestones',
      'card-gap',
      'no-active',
    ])
    expect(layout(active, [], true).map(line => line.key).slice(0, 5)).toEqual([
      'card-repo',
      'card-candidates',
      'card-milestones',
      'card-gap',
      'M2-head',
    ])
  })

  test('with no ROADMAP there is no card', () => {
    expect(layout({ ...idle, found: false }).map(line => line.key)).toEqual(['no-roadmap'])
  })
})

describe("the card's GitHub numbers come from one query, at the pull request reads only (M286 AC3)", () => {
  const cardText = async $ => (await linesAt($)).find(line => line.key === 'card-repo')?.text
  const ORIGIN_QUERY = ['gh', 'api', 'graphql', '--hostname', 'github.com', '-f', `query=${REPO_QUERY}`, '-f', 'owner=fork', '-f', 'repo=repo']

  test('a pane open runs the query on the base remote and draws its numbers', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, counts: () => repoReply(3, 12) })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    expect(await cardText($)).toBe('? PRs   ? issues')
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.card.filter(argv => argv[0] === 'gh')).toEqual([ORIGIN_QUERY])
    expect(await cardText($)).toBe('repo  3 PRs   12 issues')
  })

  // M286 review: the blocked words and the hotfix list do not wait for the
  // card's read, as M230 keeps the blocked reads apart.
  test('a held card query does not hold the blocked words or the hotfix list', async ($, on) => {
    let release: () => void = () => {}
    const held = new Promise<void>(resolve => {
      release = resolve
    })
    const calls = gh(on, () => prView('MERGED'), undefined, {
      remotes: { origin: ORIGIN },
      list: () => listReply([pr(1265, 'hotfix-a')]),
      counts: async () => {
        await held
        return repoReply(3, 12)
      },
    })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    // The held query keeps the fake busy, so these reads mount the pane
    // directly rather than wait for it to go quiet.
    let lines = await paneLines($, 'desktop')
    for (let i = 0; i < 200 && textAt(lines, 'hotfix-1265') === undefined; i++) {
      await sleep(5)
      lines = await paneLines($, 'desktop')
    }
    expect(textAt(lines, 'blocked-M102')).toBe(prText('M102', 'Two pull request URLs', 34, 'merged'))
    expect(textAt(lines, 'hotfix-1265')).toBeDefined()
    expect(textAt(lines, 'card-repo')).toBe('? PRs   ? issues')
    release()
    await calls.settled()
    expect(await cardText($)).toBe('repo  3 PRs   12 issues')
  })

  test('a turn end runs no query', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, counts: () => repoReply(3, 12) })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    const before = calls.card.length
    await $.turn.complete(turn())
    await $.turn.complete(turn())
    await calls.settled()
    expect(calls.card.length).toBe(before)
  })

  test('a failed read keeps the last good numbers for the same root', async ($, on) => {
    let answer: GhAnswer = repoReply(3, 12)
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, counts: () => answer })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    for (const fail of ['reject', { exitCode: 1, stdout: '' }, { exitCode: 0, stdout: 'HTTP 502\n' }] as GhAnswer[]) {
      answer = fail
      await pressKey($, 'cairn-pane-refresh')
      await calls.settled()
      expect(await cardText($)).toBe('repo  3 PRs   12 issues')
    }
  })

  test('a failed first read draws `?`', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ORIGIN }, counts: () => ({ exitCode: 1, stdout: '' }) })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(calls.card.filter(argv => argv[0] === 'gh').length).toBe(1)
    expect(await cardText($)).toBe('repo  ? PRs   ? issues')
  })

  for (const [name, remotes] of [
    ['a remote on another host', { origin: 'https://gitlab.com/o/r.git' }],
    ['a repo with no remote', {}],
  ] as [string, Record<string, string>][]) {
    test(`${name} runs no query`, async ($, on) => {
      const calls = gh(on, () => prView('MERGED'), undefined, { remotes, counts: () => repoReply(3, 12) })
      seat(on, copyOf('blocked-prs'))
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(calls.card.filter(argv => argv[0] === 'gh')).toEqual([])
      expect(await cardText($)).toBe('? PRs   ? issues')
    })
  }
})

describe('the card draws a release line when the read can read the latest release (M286 AC4)', () => {
  const releaseText = async $ => (await linesAt($)).find(line => line.key === 'card-release')?.text
  const DIFF = { exitCode: 0, stdout: 'cairn/milestones/archive/M1-a.md\ncairn/milestones/archive/M2-b.md\n' }
  // A commit time three days and a minute before now, in whole seconds.
  const threeDaysAgo = () => ({ exitCode: 0, stdout: `${Math.floor(Date.now() / 1000) - 3 * 86_400 - 60}\n` })

  test('a tag, its commit time, and a diff draw the line after the read', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, {
      remotes: { origin: ORIGIN },
      describe: { exitCode: 0, stdout: 'v2.1.0\n' },
      log: threeDaysAgo(),
      diff: DIFF,
    })
    seat(on, copyOf('blocked-prs'))
    await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
    expect(await releaseText($)).toBe(undefined)
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(await releaseText($)).toBe('v2.1.0 · 3 days ago · 2 done since')
    expect(calls.card.filter(argv => argv[0] === 'git')).toEqual([
      ['git', ...DESCRIBE_ARGS],
      ['git', ...tagTimeArgs('v2.1.0')],
      ['git', ...archivedArgs('v2.1.0')],
    ])
  })

  const CASES: { name: string; describe: GhAnswer; log: GhAnswer | null; diff: GhAnswer; guest: boolean }[] = [
    { name: 'describe fails', describe: { exitCode: 128, stdout: '' }, log: null, diff: DIFF, guest: false },
    { name: 'describe prints nothing', describe: { exitCode: 0, stdout: '\n' }, log: null, diff: DIFF, guest: false },
    { name: 'git log fails', describe: { exitCode: 0, stdout: 'v2.1.0\n' }, log: { exitCode: 128, stdout: '' }, diff: DIFF, guest: false },
    { name: 'the diff fails', describe: { exitCode: 0, stdout: 'v2.1.0\n' }, log: null, diff: { exitCode: 128, stdout: '' }, guest: false },
    { name: 'guest mode', describe: { exitCode: 0, stdout: 'v2.1.0\n' }, log: null, diff: DIFF, guest: true },
  ]
  for (const each of CASES) {
    test(`${each.name}: no release line`, async ($, on) => {
      const calls = gh(on, () => prView('MERGED'), undefined, {
        remotes: { origin: ORIGIN },
        describe: each.describe,
        log: each.log ?? threeDaysAgo(),
        diff: each.diff,
      })
      const copy = copyOf('blocked-prs')
      if (each.guest) copy.files['/cairn/PROFILE.md'] = GUEST_PROFILE
      seat(on, copy)
      await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect(await releaseText($)).toBe(undefined)
      if (each.guest) expect(calls.card.filter(argv => argv[0] === 'git')).toEqual([])
    })
  }
})

describe('a blocked line and a hotfix line share one layout (M286 AC5)', () => {
  const BLOCKED_URL = 'https://github.com/o/r/pull/9'
  const HOTFIX_URL = 'https://github.com/o/other/pull/9'
  const state: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: [],
    blocked: [{ id: 'M5', title: 'Same title', pr: 9, url: BLOCKED_URL, archived: false }],
    taken: [],
  }
  const hotfix = { number: 9, title: 'Same title', url: HOTFIX_URL }
  const WORDS = ['merged', 'closed', 'changes requested', 'approved', 'in review', 'unknown'] as const
  const READS: [string, PrRead | undefined][] = [
    ['no read', undefined],
    ...WORDS.map(word => [word, { word, counts: ['changes requested', 'approved', 'in review'].includes(word) ? { unresolved: 2 } : null, mergeable: null }] as [string, PrRead]),
  ]
  for (const [name, got] of READS) {
    test(name, () => {
      const prs = got === undefined ? {} : { [BLOCKED_URL]: got, [HOTFIX_URL]: got }
      const lines = layout(state, [], false, prs, [hotfix])
      const blocked = lines.find(line => line.key === 'blocked-M5')
      const fix = lines.find(line => line.key === 'hotfix-9')
      // Each line differs only in its key, its identifier, and the Button
      // that the blocked line's word carries.
      const plain = (line: PaneLine | undefined) => ({
        ...line,
        key: '',
        lead: line?.lead.map((span, i) => (i === 2 ? { ...span, text: 'ID' } : span)),
        buttons: undefined,
        target: undefined,
      })
      expect(plain(fix)).toEqual(plain(blocked))
      expect(blocked?.lead[2]).toEqual({ text: 'M5', bold: true })
      expect(fix?.lead[2]).toEqual({ text: 'fix', bold: true })
      const counts = (key: string) => {
        const line = lines.find(each => each.key === key)
        return line === undefined ? undefined : { ...line, key: '' }
      }
      expect(counts('hotfix-9-counts')).toEqual(counts('blocked-M5-counts'))
      expect(blocked?.buttons).toEqual(got === undefined ? undefined : PR_BUTTONS_OF[got.word])
    })
  }
  const PR_BUTTONS_OF: Record<string, string[] | undefined> = {
    merged: ['finish'],
    'changes requested': ['revise'],
    closed: ['check'],
    approved: undefined,
    'in review': undefined,
    unknown: undefined,
  }
})

describe('an open pull request line ends with its merge state mark (M301 AC2)', () => {
  const BLOCKED_URL = 'https://github.com/o/r/pull/9'
  const HOTFIX_URL = 'https://github.com/o/other/pull/4'
  const state: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: [],
    blocked: [{ id: 'M5', title: 'Handed off', pr: 9, url: BLOCKED_URL, archived: false }],
    taken: [],
  }
  const hotfix = { number: 4, title: 'Fix a crash', url: HOTFIX_URL }
  const read = (mergeable: 'mergeable' | 'conflicts' | null): PrRead => ({ word: 'in review', counts: null, mergeable })
  // The icon names and glyphs are written out by hand, apart from the
  // MERGE_MARK table in pane.ts.
  const CASES: [string, Record<string, PrRead>, { icon: string; text: string } | null][] = [
    ['mergeable', { [BLOCKED_URL]: read('mergeable'), [HOTFIX_URL]: read('mergeable') }, { icon: 'mergeable', text: '✓' }],
    ['conflicts', { [BLOCKED_URL]: read('conflicts'), [HOTFIX_URL]: read('conflicts') }, { icon: 'conflicts', text: '✗' }],
    ['a null merge state', { [BLOCKED_URL]: read(null), [HOTFIX_URL]: read(null) }, null],
    ['no read yet', {}, null],
  ]
  for (const [name, prs, want] of CASES) {
    for (const key of ['blocked-M5', 'hotfix-4']) {
      test(`${name} on ${key}`, () => {
        const line = layout(state, [], false, prs, [hotfix]).find(each => each.key === key)
        expect(line).not.toBe(undefined)
        const tail = line?.tail ?? []
        const icons = tail.filter(span => span.icon !== undefined)
        if (want === null) {
          expect(icons).toEqual([])
          return
        }
        expect(icons.length).toBe(1)
        const last = tail[tail.length - 1]
        expect(last.icon).toBe(want.icon)
        expect(last.text).toBe(want.text)
        // The mark comes after the state word.
        const wordAt = tail.findIndex(span => span.text === 'in review')
        expect(wordAt).toBeGreaterThan(-1)
        expect(tail.length - 1).toBeGreaterThan(wordAt)
      })
    }
  }

  // A read that is not open draws no mark even when it holds a merge
  // state, as a stored read rewritten to `closed` can (M301 review).
  for (const word of ['merged', 'closed', 'unknown'] as const) {
    test(`a ${word} read holding a merge state draws no mark`, () => {
      const got: PrRead = { word, counts: null, mergeable: 'conflicts' }
      const line = layout(state, [], false, { [BLOCKED_URL]: got, [HOTFIX_URL]: got }, [hotfix]).find(each => each.key === 'hotfix-4')
      expect(line?.tail?.some(span => span.text === word)).toBe(true)
      expect(line?.tail?.filter(span => span.icon !== undefined)).toEqual([])
    })
  }
})

describe('hovering a line on the desktop shows a card with its full text (M286 AC9)', () => {
  // One state with an active milestone, the queue, a blocked row, and a
  // hotfix; one with no active milestone, for the candidate lines. Each
  // line's full text is written out by hand.
  const active: PaneState = {
    found: true,
    milestones: [
      {
        id: 'M7',
        title: 'A long milestone title',
        status: 'in-progress',
        file: {
          goal: 'Goal.',
          tasks: [{ text: 'T1: a task', checked: false }],
          criteria: [{ text: 'AC1: a criterion', checked: true }],
          log: ['a log line'],
        },
      },
    ],
    next: { action: 'resume', command: '/milestone-implement', id: 'M7', title: null },
    workable: [{ id: 'M8', title: 'Ready next' }],
    waiting: [{ id: 'M9', title: 'Later', unmet: ['M8'] }],
    candidates: [{ priority: 'high', title: 'Hidden while active', text: 'Hidden while active' }],
    blocked: [{ id: 'M5', title: 'Handed off', pr: 9, url: 'https://github.com/o/r/pull/9', archived: false }],
    taken: [],
  }
  const idle: PaneState = {
    ...active,
    milestones: [],
    candidates: [
      { priority: 'high', title: 'First row', text: 'First row: its detail — added 2026-10-19' },
      { priority: 'low', title: '', text: '' },
    ],
  }
  const hotfix = { number: 4, title: 'Fix a crash', url: 'https://github.com/o/r/pull/4' }
  // The blocked row's PR reads open with threads, so a counts line draws
  // too, and it has no card.
  const read: Record<string, PrRead> = { 'https://github.com/o/r/pull/9': { word: 'in review', counts: { unresolved: 2 }, mergeable: null } }
  const fulls = (state: PaneState) =>
    layout(state, [], true, read, [hotfix])
      .filter(line => line.full !== undefined)
      .map(line => [line.key, line.full])

  test('with an active milestone: head, task, criterion, workable, waiting, blocked, and hotfix lines, and no other', () => {
    expect(fulls(active)).toEqual([
      ['M7-head', 'A long milestone title'],
      ['M7-task-0', 'T1: a task'],
      ['M7-criterion-0', 'AC1: a criterion'],
      ['workable-M8', 'Ready next'],
      ['waiting-M9', 'Later · on M8'],
      ['blocked-M5', 'Handed off'],
      ['hotfix-4', 'Fix a crash'],
    ])
  })

  test('the active state draws a counts line, which has no card', () => {
    expect(layout(active, [], true, read, [hotfix]).some(line => line.key === 'blocked-M5-counts')).toBe(true)
  })

  test('with no active milestone: each candidate line with its whole text (M293), but none for an empty text, and no card on the no-active line', () => {
    expect(fulls(idle)).toEqual([
      ['workable-M8', 'Ready next'],
      ['waiting-M9', 'Later · on M8'],
      ['blocked-M5', 'Handed off'],
      ['hotfix-4', 'Fix a crash'],
      ['candidate-0', 'First row: its detail — added 2026-10-19'],
    ])
    expect(layout(idle, [], true).some(line => line.key === 'no-active')).toBe(true)
  })

  for (const surface of SURFACES) {
    for (const fixture of ['pane-full', 'blocked-prs']) {
      test(`${fixture}: the card's Box on the desktop, none in the terminal (${surface})`, async ($, on) => {
        seat(on, copyOf(fixture))
        await $.turn.complete(turn())
        const ui = await mountPane($, surface)
        const [root] = await ui.findAll({ key: 'cairn-pane' })
        const cards = flat(root).flatMap(line =>
          kids(line)
            .filter(isCard)
            .map(card => ({ card, candidate: /^candidate-\d+$/.test(keyOf(line) ?? '') })),
        )
        if (surface === 'terminal') {
          expect(cards).toEqual([])
        } else {
          expect(cards.length).toBeGreaterThan(2)
          for (const { card, candidate } of cards) {
            expect(card.props).toEqual(
              expect.objectContaining({
                position: 'absolute',
                bottom: 1,
                left: 0,
                right: 0,
                display: 'none',
                borderStyle: 'round',
                borderColor: 'subtle',
                backgroundColor: 'userMessageBackground',
              }),
            )
            // The drawn tree keeps `hover` beside `props`. A candidate line's
            // card opens from its info icon's hover group (M290).
            expect((card as Element & { hover?: unknown }).hover).toEqual(
              candidate ? { display: 'flex', scope: expect.any(String) } : { display: 'flex' },
            )
            expect(keyOf(card)).toBe(undefined)
            expect(kids(card)[0].props.wrap).toBe('wrap')
          }
        }
        await ui.unmount()
      })
    }
  }
})

// M293 AC1, AC2: a candidate line's card holds its row's whole text after
// the priority token, trimmed as the short title is, and the line still
// draws the short title. The rows go through `candidateRows`, so the text
// is read as `candidateTexts` reads it. Each value is written out by hand.
// BOM and US are built from code points (LESSONS M272).
describe("a candidate line's card holds the row's whole text (M293)", () => {
  const BOM = String.fromCharCode(0xfeff)
  const US = String.fromCharCode(0x1f)
  const roadmap = [
    '## Candidates',
    '',
    '- Detail row: the detail after the title — added 2026-10-19',
    '- [high] Dash row — added 2026-10-19 — M290 review',
    '- [low] A row with neither',
    '- [parked] Parked row: waits on a trigger <!-- a note --> — added 2026-10-19',
    '- [High] Inexact token: kept in the text',
    `- ${BOM} Padded row: x \t${BOM}`,
    `- Unit separator row: x${US}`,
    '- : an empty short title — added 2026-10-19',
    '- ',
    '- [parked] ',
    '',
  ].join('\n')
  const state: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: candidateRows(roadmap),
    blocked: [],
    taken: [],
  }
  const lines = new Map(
    layout(state, [], true)
      .filter(line => /^candidate-\d+$/.test(line.key))
      .map(line => [line.key, { text: line.text?.text, full: line.full, info: line.info }]),
  )

  test('each line keeps its short title and holds its whole text', () => {
    expect(lines.get('candidate-0')).toEqual({ text: 'Detail row', full: 'Detail row: the detail after the title — added 2026-10-19', info: true })
    expect(lines.get('candidate-1')).toEqual({ text: 'Dash row', full: 'Dash row — added 2026-10-19 — M290 review', info: true })
    expect(lines.get('candidate-2')).toEqual({ text: 'A row with neither', full: 'A row with neither', info: true })
    expect(lines.get('candidate-3')).toEqual({ text: 'Parked row', full: 'Parked row: waits on a trigger  — added 2026-10-19', info: true })
    expect(lines.get('candidate-4')).toEqual({ text: '[High] Inexact token', full: '[High] Inexact token: kept in the text', info: true })
    expect(lines.get('candidate-5')).toEqual({ text: 'Padded row', full: 'Padded row: x', info: true })
    expect(lines.get('candidate-6')).toEqual({ text: 'Unit separator row', full: `Unit separator row: x${US}`, info: true })
  })

  test('a row with an empty short title opens its card from ⓘ', () => {
    expect(lines.get('candidate-7')).toEqual({ text: '', full: ': an empty short title — added 2026-10-19', info: true })
  })

  test('a row with no text has no card', () => {
    expect(lines.get('candidate-8')).toEqual({ text: '', full: undefined, info: undefined })
    expect(lines.get('candidate-9')).toEqual({ text: '', full: undefined, info: undefined })
  })
})

// M291: the project name, bold, at the left of the card's first line. The
// names each case expects are written out by hand.
describe('the card names the project at the left of its first line (M291)', () => {
  // A copy of a fixture with its files under `root`, opened there.
  const rootedAt = (name: string, root: string) => {
    const copy = copyOf(name)
    const files: Record<string, string> = {}
    for (const [path, text] of Object.entries(copy.files)) files[`${root}${path}`] = text
    copy.files = files
    copy.unreadable = copy.unreadable.map(path => `${root}${path}`)
    copy.cwd = root
    return copy
  }
  const firstText = async $ => (await linesAt($)).find(line => line.key === 'card-repo')?.text
  const ok = (stdout: string): GhAnswer => ({ exitCode: 0, stdout: `${stdout}\n` })
  const ALPHA = 'https://github.com/o/alpha.git'

  for (const surface of SURFACES) {
    test(`the name bold, then the counts, then ⌂ and ↻, with the other card lines unchanged (AC1, ${surface})`, async ($, on) => {
      const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ALPHA }, counts: () => repoReply(3, 12) })
      seat(on, rootedAt('pane-full', '/work/zeta'))
      await $.session.start({ cwd: '/work/zeta', surface, isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      const ui = await mountPane($, surface)
      const card = await boxOf(ui, 'cairn-card')
      expect(kids(card as Element).map(keyOf)).toEqual(['card-repo', 'card-candidates', 'card-milestones'])
      const first = kids(card as Element)[0]
      expect(kids(first).map(keyOf)).toEqual(['card-repo-text', 'card-repo-tail', 'card-repo-home', 'card-repo-refresh'])
      const [name] = kids((await boxOf(ui, 'card-repo-text')) as Element)
      expect(name.props.bold).toBe(true)
      expect(textOf(name)).toBe('alpha')
      expect(textOf(await boxOf(ui, 'card-repo-tail'))).toBe('  3 PRs   12 issues')
      expect((await boxOf(ui, 'card-repo-tail'))?.props.flexGrow).toBe(1)
      expect((await boxOf(ui, 'card-repo-text'))?.props.flexGrow).toBe(undefined)
      expect(textOf(first)).toBe('alpha  3 PRs   12 issues')
      await ui.unmount()
    })

    test(`a long name is the part that is cut, and the counts and Buttons keep their width (AC4, ${surface})`, async ($, on) => {
      const long = 'a-project-name-far-longer-than-the-docked-pane-is-wide'
      const calls = gh(on, () => prView('MERGED'), undefined, {
        remotes: { origin: `https://github.com/o/${long}.git` },
        counts: () => repoReply(3, 12),
      })
      seat(on, rootedAt('pane-full', '/work/zeta'))
      await $.session.start({ cwd: '/work/zeta', surface, isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      const ui = await mountPane($, surface, 44)
      const first = (await boxOf(ui, 'card-repo')) as Element
      expect(first.props.minWidth).toBe(0)
      const text = (await boxOf(ui, 'card-repo-text')) as Element
      expect(text.props).toEqual(expect.objectContaining({ flexShrink: 1, minWidth: 0 }))
      expect(kids(text)[0].props.wrap).toBe('truncate-end')
      expect(textOf(kids(text)[0])).toBe(long)
      for (const key of ['card-repo-tail', 'card-repo-home', 'card-repo-refresh']) {
        expect((await boxOf(ui, key))?.props.flexShrink).toBe(0)
      }
      await ui.unmount()
    })
  }

  const NAMES: { name: string; profile: string | null; remotes: Record<string, string>; root?: string; common?: GhAnswer; want: string }[] = [
    { name: 'an origin github.com remote', profile: null, remotes: { origin: ALPHA }, want: 'alpha' },
    {
      name: 'guest mode with an upstream github.com remote',
      profile: GUEST_PROFILE,
      remotes: { origin: 'https://github.com/me/fork-name.git', upstream: 'git@github.com:up/beta.git' },
      want: 'beta',
    },
    { name: 'guest mode with only origin', profile: GUEST_PROFILE, remotes: { origin: 'https://github.com/me/fork-name.git' }, want: 'fork-name' },
    { name: 'a remote not on github.com', profile: null, remotes: { origin: 'https://gitlab.com/o/r.git' }, common: ok('/work/gamma/.git'), want: 'gamma' },
    { name: 'no remote', profile: null, remotes: {}, common: ok('/work/delta/.git'), want: 'delta' },
    { name: 'a root inside a linked worktree', profile: null, remotes: {}, root: '/work/main/.claude/worktrees/w1', common: ok('/work/main/.git'), want: 'main' },
    { name: 'a common dir not named .git', profile: null, remotes: {}, root: '/work/super/subdir', common: ok('/work/super/.git/modules/sub'), want: 'subdir' },
    { name: 'a failed git call', profile: null, remotes: {}, root: '/work/epsilon', common: { exitCode: 128, stdout: '' }, want: 'epsilon' },
  ]
  for (const each of NAMES) {
    test(`${each.name} names ${each.want} (AC2)`, async ($, on) => {
      const root = each.root ?? '/work/zeta'
      const calls = gh(on, () => prView('MERGED'), undefined, { remotes: each.remotes, counts: () => repoReply(3, 12), common: each.common })
      const copy = rootedAt('blocked-prs', root)
      if (each.profile !== null) copy.files[`${root}/cairn/PROFILE.md`] = each.profile
      seat(on, copy)
      await $.session.start({ cwd: root, surface: 'desktop', isInteractive: true })
      await $.command.run({ command: COMMAND })
      await calls.settled()
      expect((await firstText($))?.split('  ')[0]).toBe(each.want)
      // Only a URL that is not a github.com one, or none, asks git for the
      // common dir.
      const asked = calls.card.filter(argv => argv[1] === 'rev-parse')
      expect(asked).toEqual(each.common === undefined ? [] : [['git', ...COMMON_DIR_ARGS]])
    })
  }

  test('a failed GitHub read still names the project from the URL (AC2)', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ALPHA }, counts: () => ({ exitCode: 1, stdout: '' }) })
    seat(on, rootedAt('blocked-prs', '/work/zeta'))
    await $.session.start({ cwd: '/work/zeta', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(await firstText($)).toBe('alpha  ? PRs   ? issues')
  })

  test('a linked worktree draws its own folder name until the read is written (AC3)', async ($, on) => {
    gh(on, () => prView('MERGED'), undefined, { remotes: {}, common: ok('/work/main/.git') })
    seat(on, rootedAt('blocked-prs', '/work/main/.claude/worktrees/w1'))
    await $.session.start({ cwd: '/work/main/.claude/worktrees/w1', surface: 'desktop', isInteractive: true })
    expect(await firstText($)).toBe('w1  ? PRs   ? issues')
  })

  test('a held read draws the root folder name, then the name it reads (AC3)', async ($, on) => {
    let release: () => void = () => {}
    const held = new Promise<void>(resolve => {
      release = resolve
    })
    const calls = gh(on, () => prView('MERGED'), undefined, {
      remotes: { origin: ALPHA },
      counts: async () => {
        await held
        return repoReply(3, 12)
      },
    })
    seat(on, rootedAt('blocked-prs', '/work/proj'))
    await $.session.start({ cwd: '/work/proj', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    // The held query keeps the fake busy, so this mounts the pane directly.
    expect(textAt(await paneLines($, 'desktop'), 'card-repo')).toBe('proj  ? PRs   ? issues')
    release()
    await calls.settled()
    expect(await firstText($)).toBe('alpha  3 PRs   12 issues')
  })

  test('a name stored for another root is not drawn (AC3)', async ($, on) => {
    const calls = gh(on, () => prView('MERGED'), undefined, { remotes: { origin: ALPHA }, counts: () => repoReply(3, 12) })
    const copy = rootedAt('blocked-prs', '/work/one')
    for (const path of Object.keys(copy.files)) copy.files[path.replace('/work/one', '/work/two')] = copy.files[path]
    copy.unreadable.push(...copy.unreadable.map(path => path.replace('/work/one', '/work/two')))
    seat(on, copy)
    await $.session.start({ cwd: '/work/one', surface: 'desktop', isInteractive: true })
    await $.command.run({ command: COMMAND })
    await calls.settled()
    expect(await firstText($)).toBe('alpha  3 PRs   12 issues')
    copy.cwd = '/work/two'
    await $.turn.complete(turn())
    expect(await firstText($)).toBe('two  ? PRs   ? issues')
  })
})

// M294 AC1: a card opens above its row when it fits there, else below,
// else on the side with more rows (above on a tie), cut to that side's
// rows, and with no card when that side has fewer than 3 rows. Each value
// is written out by hand.
describe('cardPlace picks the side a candidate card opens on (M294 AC1)', () => {
  const table: [string, number, number, number, ReturnType<typeof cardPlace>][] = [
    ['fits above', 5, 10, 2, { side: 'up', rows: null }],
    ['exactly fits above', 10, 10, 0, { side: 'up', rows: null }],
    ['fits only below', 8, 4, 20, { side: 'down', rows: null }],
    ['exactly fits below', 20, 4, 20, { side: 'down', rows: null }],
    ['fits neither, more room above', 30, 12, 9, { side: 'up', rows: 12 }],
    ['fits neither, more room below', 30, 6, 15, { side: 'down', rows: 15 }],
    ['fits neither, a tie', 30, 8, 8, { side: 'up', rows: 8 }],
    ['fits neither, larger side under 3 rows', 30, 2, 1, null],
    ['fits neither, larger side of exactly 3 rows', 30, 1, 3, { side: 'down', rows: 3 }],
  ]
  for (const [name, need, above, below, place] of table) {
    test(name, () => {
      expect(cardPlace(need, above, below)).toEqual(place)
    })
  }
})

// M294 AC2: the rows a card's text takes, an estimate: a greedy wrap at
// spaces at four columns less than the pane's (the card's border and
// padding), a word longer than a row split across rows, plus the two
// border rows. Columns are code points, as `width` in band.ts counts them.
// With 14 columns a row holds 10. Each value is written out by hand.
describe('cardRows estimates the rows a candidate card takes (M294 AC2)', () => {
  const table: [string, string, number][] = [
    ['an empty text', '', 2],
    ['one short word', 'ab', 3],
    ['a text that fills a row exactly', 'abcd efghi', 3],
    ['a row plus one word', 'abcd efghi jk', 4],
    ['a word longer than a row', 'abcdefghijklm', 4],
    ['repeated spaces', 'ab     cd', 3],
    ['a word that exactly fills the last row', 'ab cdefghijklmnopqrstuv', 5],
  ]
  for (const [name, text, rows] of table) {
    test(name, () => {
      expect(cardRows(text, 14)).toBe(rows)
    })
  }
})

// M294 AC3: each candidate line carries the rows the pane draws before it,
// each line one row, plus the summary card's two border rows. With no
// milestone active, no goal line wraps. Each case counts its rows by hand:
// the card's top border, its three lines (four with the release line), its
// bottom border, the card's gap row, `no active milestone`, then each
// section's gap and heading and its lines, then the Candidates gap and
// heading. The bare state puts its first candidate on row 9.
describe('each candidate line carries the rows drawn before it (M294 AC3)', () => {
  const base: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: [
      { priority: 'high', title: 'Up row', text: 'Up row: x' },
      { priority: 'normal', title: 'Mid row', text: 'Mid row: y' },
      { priority: 'low', title: 'Low row', text: 'Low row: z' },
    ],
    blocked: [],
    taken: [],
  }
  const blocked = { id: 'M5', title: 'Handed off', pr: 9, url: 'https://github.com/o/r/pull/9', archived: false }
  const rows = (lines: PaneLine[]) =>
    lines.filter(line => line.key.startsWith('candidate-') && line.key !== 'candidates-head').map(line => [line.key, line.rowsAbove])
  const expectRows = (lines: PaneLine[], first: number) =>
    expect(rows(lines)).toEqual([
      ['candidate-0', first],
      ['candidate-1', first + 1],
      ['candidate-2', first + 2],
    ])

  test('no release line, no Next line, no other section', () => {
    expectRows(layout(base), 9)
  })

  test('the Next line adds its gap and itself', () => {
    expectRows(layout({ ...base, next: { action: 'plan the next milestone', command: '/milestone-plan', id: null, title: null } }), 11)
  })

  test('the release line adds one card row', () => {
    const repo = { root: '/r', counts: { prs: 1, issues: 2 }, done: { tag: 'v1.0.0', days: 3, count: 2 }, name: 'r' }
    expectRows(layout(base, [], false, {}, [], [], repo, '/r'), 10)
  })

  test('a blocked row with its counts line adds four rows', () => {
    const read = { 'https://github.com/o/r/pull/9': { word: 'in review' as const, counts: { unresolved: 2 }, mergeable: null } }
    expectRows(layout({ ...base, blocked: [blocked] }, [], false, read), 13)
  })

  test('a blocked row with no counts line adds three rows', () => {
    expectRows(layout({ ...base, blocked: [blocked] }), 12)
  })

  test('a hotfix line adds three rows', () => {
    expectRows(layout(base, [], false, {}, [{ number: 4, title: 'Fix a crash', url: 'https://github.com/o/r/pull/4' }]), 12)
  })

  test('a workable row and two waiting rows add seven rows', () => {
    const state = {
      ...base,
      workable: [{ id: 'M8', title: 'Ready' }],
      waiting: [
        { id: 'M9', title: 'Later', unmet: ['M8'] },
        { id: 'M10', title: 'Later two', unmet: ['M8'] },
      ],
    }
    expectRows(layout(state), 16)
  })

  test('a row an open pull request names is hidden, and the row after it moves up (review pass 1)', () => {
    const lines = layout(base, [], false, {}, [], [{ title: 'Mid row', number: 5 }])
    expect(rows(lines)).toEqual([
      ['candidate-0', 9],
      ['candidate-2', 10],
    ])
  })

  test('no other line carries a row', () => {
    expect(layout(base).filter(line => line.rowsAbove !== undefined).every(line => /^candidate-\d+$/.test(line.key))).toBe(true)
  })
})

// M294 AC4: each candidate card is placed from the Pane props. One row
// whose text, `Long row: aaaa bbbb cccc dddd eeee ffff gggg hhhh`, wraps to
// 5 rows at 14 columns (10 for text), so its card needs 7, and to 1 row at
// 60 columns, a card of 3. In the bare idle state its line is on row 9
// (M294 AC3), and the tree has 8 lines, so 10 rows. Each value is written
// out by hand.
describe('each candidate card is placed from the Pane props (M294 AC4)', () => {
  const long: PaneState = {
    found: true,
    milestones: [],
    next: null,
    workable: [],
    waiting: [],
    candidates: [{ priority: 'high', title: 'Long row', text: 'Long row: aaaa bbbb cccc dddd eeee ffff gggg hhhh' }],
    blocked: [],
    taken: [],
  }
  const table: [string, number, number, number, 'dock' | 'inline', ReturnType<typeof cardPlace>][] = [
    ['room above at the top of the window', 14, 0, 40, 'dock', { side: 'up', rows: null }],
    ['scrolled so 4 rows show above: below', 14, 5, 40, 'dock', { side: 'down', rows: null }],
    ['4 rows each side: cut above on the tie', 14, 5, 9, 'dock', { side: 'up', rows: 4 }],
    ['2 above and 5 below: cut below', 14, 7, 8, 'dock', { side: 'down', rows: 5 }],
    ['1 row each side: no card', 14, 8, 3, 'dock', null],
    ['inline, the frame fits the tree: cut below', 14, 5, 200, 'inline', { side: 'down', rows: 5 }],
    ['a wider pane makes the card fit above', 60, 5, 40, 'dock', { side: 'up', rows: null }],
  ]
  for (const [name, bodyColumns, offset, bodyRows, placement, place] of table) {
    test(name, () => {
      expect(cardPlaces(layout(long), { bodyColumns, offset, bodyRows, placement })).toEqual({ 'candidate-0': place })
    })
  }

  test('only candidate lines are placed', () => {
    const state = { ...long, workable: [{ id: 'M8', title: 'Ready' }] }
    expect(Object.keys(cardPlaces(layout(state), { bodyColumns: 14, offset: 0, bodyRows: 40, placement: 'dock' }))).toEqual(['candidate-0'])
  })
})

// M294 AC5: an upward card is drawn in its line at `bottom: 1`; a card that
// opens below is drawn after every line in the pane's root Box at its
// line's row plus 1, hidden until the line's ⓘ group lights; a cut card
// holds its text cut by whole words to fit its rows, ending in `…`, and
// sets no height; the terminal draws none. The line's row is
// read off the drawn tree: its place in the pane's lines, plus the summary
// card's two border rows, each line one row.
describe('a candidate card is drawn on the side it opens on (M294 AC5)', () => {
  const ROADMAP = [
    '# Roadmap',
    '',
    '## Milestones',
    '',
    '| ID | Title | Status | Depends on | Priority | File/Archive |',
    '|---|---|---|---|---|---|',
    '',
    '## Candidates',
    '',
    '- [high] Long row: aaaa bbbb cccc dddd eeee ffff gggg hhhh',
    '',
  ].join('\n')
  const longCopy = () => {
    const copy = copyOf('candidates')
    copy.files[Object.keys(copy.files).find(path => path.endsWith('cairn/ROADMAP.md')) as string] = ROADMAP
    return copy
  }
  const mountAt = async (
    $,
    surface: (typeof SURFACES)[number],
    offset: number,
    bodyRows: number,
    bodyColumns = 14,
    placement: 'dock' | 'inline' = 'dock',
  ) =>
    (await $.ui.mount({
      plugin: 'cairn',
      surface,
      ...PANE_VIEW,
      props: { ...PANE_VIEW.props, bodyColumns, placement, scroll: { offset, bodyRows } },
    })) as Ui
  // The candidate line's row and the pane's root.
  const drawn = async (
    $,
    surface: (typeof SURFACES)[number],
    offset: number,
    bodyRows: number,
    bodyColumns = 14,
    placement: 'dock' | 'inline' = 'dock',
  ) => {
    const ui = await mountAt($, surface, offset, bodyRows, bodyColumns, placement)
    const [root] = await ui.findAll({ key: 'cairn-pane' })
    // A pane mounts once per surface, so each read unmounts it.
    await ui.unmount()
    const lines = flat(root)
    const line = lines.find(each => keyOf(each) === 'candidate-0') as Element
    return { root, line, row: lines.indexOf(line) + 2 }
  }
  const scope = 'cairn-info-candidate-0'
  // The test kit keeps `hover` beside `props` (LESSONS M284).
  const hoverOf = (node: Element) => (node as Element & { hover?: unknown }).hover

  for (const surface of SURFACES) {
    test(`a card with room above is in its line at bottom 1 (${surface})`, async ($, on) => {
      seat(on, longCopy())
      await $.turn.complete(turn())
      const { root, line } = await drawn($, surface, 0, 200)
      const cards = kids(line).filter(isCard)
      const overlays = kids(root).filter(isCard)
      expect(overlays).toEqual([])
      if (surface === 'terminal') {
        expect(cards).toEqual([])
      } else {
        expect(cards.length).toBe(1)
        expect(cards[0].props).toEqual(expect.objectContaining({ position: 'absolute', bottom: 1, display: 'none' }))
        expect(hoverOf(cards[0])).toEqual({ display: 'flex', scope })
        expect(cards[0].props.height).toBeUndefined()
      }
    })

    test(`a card with no room above is drawn last in the pane at its row plus 1 (${surface})`, async ($, on) => {
      seat(on, longCopy())
      await $.turn.complete(turn())
      const { row } = await drawn($, surface, 0, 200)
      const { root, line } = await drawn($, surface, row, 200)
      expect(kids(line).filter(isCard)).toEqual([])
      const last = kids(root).at(-1) as Element
      if (surface === 'terminal') {
        expect(kids(root).filter(isCard)).toEqual([])
      } else {
        expect(isCard(last)).toBe(true)
        expect(keyOf(last)).toBeUndefined()
        expect(last.props).toEqual(expect.objectContaining({ position: 'absolute', top: row + 1, display: 'none' }))
        expect(hoverOf(last)).toEqual({ display: 'flex', scope })
        expect(last.props.height).toBeUndefined()
      }
    })

    test(`a card that fits neither side is cut to the larger one (${surface})`, async ($, on) => {
      seat(on, longCopy())
      await $.turn.complete(turn())
      const { row } = await drawn($, surface, 0, 200)
      // One row above the line in the window and 5 below: the card needs 7.
      const { root } = await drawn($, surface, row - 1, 7)
      const last = kids(root).at(-1) as Element
      if (surface === 'terminal') {
        expect(kids(root).filter(isCard)).toEqual([])
      } else {
        // A cap of 5 holds 3 text rows of 10 columns: `Long row:`,
        // `aaaa bbbb`, `cccc …`. The card sets no height (amended AC5).
        expect(last.props).toEqual(expect.objectContaining({ position: 'absolute', top: row + 1, display: 'none' }))
        expect(last.props.height).toBeUndefined()
        expect(last.props.overflow).toBeUndefined()
        expect(textOf(kids(last)[0])).toBe('Long row: aaaa bbbb cccc …')
      }
    })

    // M294 AC4 (review return 1): redraws that vary `bodyColumns` and
    // `placement`. The line is on row 11, counted by hand: the card's top
    // border, its three lines, its bottom border, the card's gap row,
    // `no active milestone`, the Next line's gap and the Next line, and the
    // Candidates gap and heading.
    test(`the line sits on row 11 (${surface})`, async ($, on) => {
      seat(on, longCopy())
      await $.turn.complete(turn())
      expect((await drawn($, surface, 0, 200)).row).toBe(11)
    })

    test(`with 4 rows showing above, a 60-column pane opens the card above and a 14-column one below, none in the terminal (${surface})`, async ($, on) => {
      seat(on, longCopy())
      await $.turn.complete(turn())
      // At 60 columns the card needs 3 rows; at 14 it needs 7.
      const wide = await drawn($, surface, 7, 200, 60)
      const narrow = await drawn($, surface, 7, 200, 14)
      if (surface === 'terminal') {
        expect([...kids(wide.root), ...kids(wide.line)].filter(isCard)).toEqual([])
        expect([...kids(narrow.root), ...kids(narrow.line)].filter(isCard)).toEqual([])
      } else {
        expect(kids(wide.line).filter(isCard).map(card => card.props.bottom)).toEqual([1])
        expect(kids(wide.root).filter(isCard)).toEqual([])
        expect(kids(narrow.line).filter(isCard)).toEqual([])
        expect(kids(narrow.root).filter(isCard).map(card => card.props.top)).toEqual([12])
      }
    })

    test(`inline, the frame fits the tree, so the card is cut where a dock opens it whole, none in the terminal (${surface})`, async ($, on) => {
      seat(on, longCopy())
      await $.turn.complete(turn())
      // With the window at offset 6 the line shows on its row 5. Inline the
      // room is the tree's 12 rows, so 6 rows lie below: the card's 7 fit
      // neither side, and it is cut to the 6 below. In a dock of 200 rows it
      // opens below whole.
      const inline = await drawn($, surface, 6, 200, 14, 'inline')
      const dock = await drawn($, surface, 6, 200, 14, 'dock')
      if (surface === 'terminal') {
        for (const draw of [inline, dock]) expect([...kids(draw.root), ...kids(draw.line)].filter(isCard)).toEqual([])
      } else {
        const [cut] = kids(inline.root).filter(isCard)
        const [whole] = kids(dock.root).filter(isCard)
        expect(cut.props.top).toBe(12)
        expect(textOf(kids(cut)[0])).toBe('Long row: aaaa bbbb cccc dddd eeee …')
        expect(whole.props.top).toBe(12)
        expect(textOf(kids(whole)[0])).toBe('Long row: aaaa bbbb cccc dddd eeee ffff gggg hhhh')
      }
    })

    test(`a window too short on both sides draws no card (${surface})`, async ($, on) => {
      seat(on, longCopy())
      await $.turn.complete(turn())
      // At offset 10 the line shows on its row 1 of a 3-row window: 1 row
      // above and 1 below, under the 3 a card needs at the least.
      const short = await drawn($, surface, 10, 3)
      expect([...kids(short.root), ...kids(short.line)].filter(isCard)).toEqual([])
      // The same line with room draws its card, so the empty result above
      // is the placement's and not a missing line.
      if (surface !== 'terminal') {
        const roomy = await drawn($, surface, 10, 200)
        expect([...kids(roomy.root), ...kids(roomy.line)].filter(isCard).length).toBe(1)
      }
    })
  }
})

// M294 AC5 (amended after the live look): a cut card's text is its longest
// run of whole words from the start that fits in its rows with ` …` after
// it. With 14 columns a row holds 10. Each value is written out by hand.
describe('cardCut cuts the text of a card by whole words (M294 AC5)', () => {
  const table: [string, string, number, string][] = [
    ['a cut mid-text', 'aaaa bbbb cccc dddd eeee ffff gggg', 5, 'aaaa bbbb cccc dddd eeee …'],
    ['a run whose … would wrap past the rows', 'aaaa bbbb cccc dddd eeee ffff', 4, 'aaaa bbbb cccc …'],
    ['a first word that does not fit alone', 'abcdefghij klm', 3, '…'],
    ['a text that fits whole', 'aaaa bbbb', 3, 'aaaa bbbb'],
    ['repeated and leading spaces', '  aaaa   bbbb cccc dddd', 3, 'aaaa …'],
    ['a word longer than a row that fits once split', 'abcdefghijklmno uvw xyz', 4, 'abcdefghijklmno …'],
  ]
  for (const [name, text, rows, cut] of table) {
    test(name, () => {
      expect(cardCut(text, rows, 14)).toBe(cut)
    })
  }
})
