import type { Span } from './band'
import type { FlowPhase } from './band'
import { FLOW_COLORS, flowOf, GRAY, width } from './band'
import type { BandRow, CandidateRow, PaneItem, PaneMilestone, PaneState } from './reader'
import { PILL_TEXT } from './track'

// The cairn pane's lines (M205), as a plain description that register.tsx
// draws. For each active milestone: its phase, id, and title, with the
// band's percent for the row at the end of the line when its file reads
// (M208), its goal, its tasks and criteria with their boxes, and its
// newest work-log lines.
// Below them: the command that scripts/cairn_next.py recommends, the
// workable planned milestones, and the planned ones that wait on
// dependencies. With no active milestone, the ROADMAP's candidate rows
// follow, each a priority mark and its short title (M207).
// A line's `lead` and `tail` keep their width. Its `text` is cut to one
// line with an ellipsis, but for the goal's lines, which wrap: the operator
// picked one line per item at the M205 live look, so a long task list fits
// on one screen.
// The operator picked the look at the M208 prototypes: a blank row, a
// `▎`, and a gray uppercase label for each section heading, eight squares
// beside the Tasks and Criteria counts, the Next command in a pill, and the
// percent alone on the head line, with no track. At the live look the
// operator asked for the phase colors: a milestone's marks and meters take
// its phase's color, the queue's take plan's, and the pill takes the color
// of the phase its command runs. The colors are theme keys (M217).
// While no cairn skill runs, the Next line also carries the band's
// next-step label after the pill, which register.tsx draws as a Button
// (M218).

// The Next line's `action`, when set, is the label of the next-step Button
// drawn after its tail. No other line carries one: register.tsx draws it
// with the one key `cairn-pane-next` and the next-step press.
// The `actions` line's `buttons` name the Buttons that register.tsx draws on
// it, in order (M219). No other line carries them.
export type PaneButton = 'clear' | 'status'
export type PaneLine = {
  key: string
  indent: number
  lead: Span[]
  text: Span | null
  tail?: Span[]
  wraps?: true
  action?: string
  buttons?: PaneButton[]
}

// The next-step Button's label by the action that scripts/cairn_next.py
// names (M212), planning among them (M213). The band and the pane read
// this one map (M218).
export const PLAN_LABEL = 'Plan'
export const NEXT_LABELS: Record<string, string> = {
  review: 'Review',
  resume: 'Resume',
  implement: 'Start',
  'plan the next milestone': PLAN_LABEL,
}

// An action's label, read from the map's own keys only, so an action named
// like an object property, such as `toString`, has none (M218 review).
export function nextLabel(action: string): string | undefined {
  return Object.prototype.hasOwnProperty.call(NEXT_LABELS, action) ? NEXT_LABELS[action] : undefined
}

// The Status and Clear Buttons' labels (M212, M216). The band and the
// pane's `actions` line read these (M219).
export const STATUS_LABEL = 'Status'
export const CLEAR_LABEL = 'Clear'

// The Next line's lead, a bold `Next` and two spaces. The `actions` line is
// indented by its width, so its Buttons sit under the pill (M219).
const NEXT_LEAD = 'Next'
const NEXT_GAP = '  '
const ACTIONS_INDENT = width(NEXT_LEAD) + width(NEXT_GAP)

export const NO_ROADMAP = 'no cairn ROADMAP found'
export const NO_FILE = 'no milestone file'
export const NO_ACTIVE = 'no active milestone'
export const CHECKED_MARK = '✓'
export const OPEN_MARK = '○'
// A candidate row's mark for each priority (M207).
export const PRIORITY_MARK: Record<CandidateRow['priority'], Span> = {
  high: { text: '↑', color: FLOW_COLORS.implement, bold: true },
  normal: { text: '·' },
  low: { text: '↓', color: GRAY },
}
// A section heading's accent mark, in the phase's color (M208).
export const ACCENT_MARK = '▎'
// The meter's squares, filled and empty, and how many it draws (M208).
export const METER_FULL = '■'
export const METER_EMPTY = '□'
export const METER_CELLS = 8
// The empty squares' theme key, as the band's terminal track marks use (M208 review).
export const METER_EMPTY_KEY = 'subtle'
// The warning text's theme key, as the band's warning labels use.
const WARNING = 'warning'

const PHASE: Record<string, { label: string; color: string }> = {
  'in-progress': { label: 'implement', color: FLOW_COLORS.implement },
  review: { label: 'review', color: FLOW_COLORS.review },
}
// The phase each recommended command runs, for the Next pill's color.
export const COMMAND_PHASE: Record<string, FlowPhase> = {
  '/milestone-plan': 'plan',
  '/milestone-implement': 'implement',
  '/milestone-review': 'review',
}
// The queue's headings are about planned work and candidates.
const QUEUE_COLOR = FLOW_COLORS.plan

const line = (key: string, indent: number, lead: Span[], text: Span | null = null): PaneLine => ({
  key,
  indent,
  lead,
  text,
})

// One blank row, before each section heading, each milestone after the
// first, and Next.
const gap = (key: string) => line(key, 0, [], { text: ' ' })

// The filled share of the meter: none only with no box checked, and all
// only with every box checked.
export function meterFill(checked: number, total: number): number {
  if (total === 0 || checked === 0) return 0
  if (checked >= total) return METER_CELLS
  return Math.min(METER_CELLS - 1, Math.max(1, Math.round((METER_CELLS * checked) / total)))
}

export function meter(checked: number, total: number, color: string): Span[] {
  const fill = meterFill(checked, total)
  return [
    { text: METER_FULL.repeat(fill), color },
    { text: METER_EMPTY.repeat(METER_CELLS - fill), color: METER_EMPTY_KEY },
  ].filter(span => span.text !== '')
}

// A section heading and the blank row before it: the accent in `color`,
// the label in gray uppercase, and its count and meter where it has them.
function heading(key: string, label: string, color: string, after: Span[] = []): PaneLine[] {
  return [
    gap(`${key}-gap`),
    line(key, 0, [
      { text: ACCENT_MARK, color },
      { text: ' ' },
      { text: label.toUpperCase(), color: GRAY, bold: true },
      ...after,
    ]),
  ]
}

function counted(key: string, label: string, list: PaneItem[], color: string): PaneLine[] {
  const checked = list.filter(item => item.checked).length
  return heading(key, label, color, [
    { text: ' ' },
    { text: `${checked}/${list.length}`, color: GRAY },
    { text: ' ' },
    ...meter(checked, list.length, color),
  ])
}

function items(prefix: string, list: PaneItem[]): PaneLine[] {
  return list.map((item, i) =>
    line(
      `${prefix}-${i}`,
      2,
      [item.checked ? { text: CHECKED_MARK, color: GRAY } : { text: OPEN_MARK }, { text: ' ' }],
      item.checked ? { text: item.text, color: GRAY } : { text: item.text },
    ),
  )
}

function milestoneLines(row: PaneMilestone, band: BandRow | undefined): PaneLine[] {
  const phase = PHASE[row.status] ?? { label: row.status, color: GRAY }
  const head = line(
    `${row.id}-head`,
    0,
    [{ text: phase.label, color: phase.color, bold: true }, { text: ' ' }, { text: row.id, bold: true }, { text: '  ' }],
    { text: row.title },
  )
  const file = row.file
  // The band's percent for the row, from its own counts, which count a box
  // inside an HTML comment where the pane's items do not.
  const flow = file === null || band === undefined ? null : flowOf(band)
  if (flow !== null && flow.percent !== null) head.tail = [{ text: '  ' }, { text: `${flow.percent}%`, color: GRAY }]
  const out: PaneLine[] = [head]
  if (file === null) return [...out, line(`${row.id}-nofile`, 2, [], { text: NO_FILE, color: WARNING })]
  if (file.goal !== '') {
    out.push(...heading(`${row.id}-goal-head`, 'Goal', phase.color))
    // A blank line between paragraphs draws as one space, so it keeps its row.
    file.goal.split('\n').forEach((text, i) =>
      out.push({ ...line(`${row.id}-goal-${i}`, 2, [], { text: text === '' ? ' ' : text }), wraps: true }),
    )
  }
  if (file.tasks.length > 0) {
    out.push(...counted(`${row.id}-tasks-head`, 'Tasks', file.tasks, phase.color))
    out.push(...items(`${row.id}-task`, file.tasks))
  }
  if (file.criteria.length > 0) {
    out.push(...counted(`${row.id}-criteria-head`, 'Criteria', file.criteria, phase.color))
    out.push(...items(`${row.id}-criterion`, file.criteria))
  }
  if (file.log.length > 0) {
    out.push(...heading(`${row.id}-log-head`, 'Work log', phase.color))
    file.log.forEach((text, i) => out.push(line(`${row.id}-log-${i}`, 2, [], { text, color: GRAY })))
  }
  return out
}

// The pane's lines from its state and the band's rows, whose counts give
// each head line its percent. `acts` is true while no cairn skill's step is
// set, and then the Next line carries its action label (M218) and the
// `actions` line follows it with the Status Button. `ended` is true after a
// cairn skill ends, and then the Clear Button comes before Status (M219).
export function paneLines(state: PaneState, band: BandRow[] = [], acts = false, ended = false): PaneLine[] {
  if (!state.found) return [line('no-roadmap', 0, [], { text: NO_ROADMAP, color: GRAY })]
  const out: PaneLine[] = []
  if (state.milestones.length === 0) out.push(line('no-active', 0, [], { text: NO_ACTIVE, color: GRAY }))
  state.milestones.forEach((row, i) => {
    if (i > 0) out.push(gap(`${row.id}-gap`))
    out.push(...milestoneLines(row, band.find(b => b.id === row.id && b.status === row.status)))
  })
  if (state.next !== null) {
    const target = state.next.id === null ? state.next.command : `${state.next.command} ${state.next.id}`
    out.push(gap('next-gap'))
    const next = line('next', 0, [{ text: NEXT_LEAD, bold: true }, { text: NEXT_GAP }], {
      text: ` ${target} `,
      color: PILL_TEXT,
      backgroundColor: FLOW_COLORS[COMMAND_PHASE[state.next.command] ?? 'implement'],
      // Bold, as the band's pill is. The text and fill are the theme's own
      // keys (M217), so their contrast is the theme's.
      bold: true,
    })
    const label = nextLabel(state.next.action)
    if (acts && label !== undefined) next.action = label
    out.push(next)
    if (acts) out.push({ ...line('actions', ACTIONS_INDENT, []), buttons: ended ? ['clear', 'status'] : ['status'] })
  }
  if (state.workable.length > 0) {
    out.push(...heading('workable-head', 'Workable', QUEUE_COLOR))
    for (const row of state.workable) {
      out.push(line(`workable-${row.id}`, 2, [{ text: row.id, bold: true }, { text: '  ' }], { text: row.title }))
    }
  }
  if (state.waiting.length > 0) {
    out.push(...heading('waiting-head', 'Waiting', QUEUE_COLOR))
    for (const row of state.waiting) {
      out.push(
        line(`waiting-${row.id}`, 2, [{ text: row.id, bold: true }, { text: '  ' }], {
          text: `${row.title} · on ${row.unmet.join(', ')}`,
        }),
      )
    }
  }
  // With no active milestone, the ROADMAP's candidate rows (M207).
  if (state.milestones.length === 0 && state.candidates.length > 0) {
    out.push(
      ...heading('candidates-head', 'Candidates', QUEUE_COLOR, [{ text: ' ' }, { text: `${state.candidates.length}`, color: GRAY }]),
    )
    state.candidates.forEach((row, i) =>
      out.push(
        line(
          `candidate-${i}`,
          2,
          [PRIORITY_MARK[row.priority], { text: ' ' }],
          row.priority === 'low' ? { text: row.title, color: GRAY } : { text: row.title },
        ),
      ),
    )
  }
  return out
}
