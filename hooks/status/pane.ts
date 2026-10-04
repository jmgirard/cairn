import type { Span } from './band'
import { GRAY, GREEN, ORANGE } from './band'
import type { PaneItem, PaneMilestone, PaneState } from './reader'

// The cairn pane's lines (M205), as a plain description that register.tsx
// draws. For each active milestone: its phase, id, and title, its goal,
// its tasks and criteria with their boxes, and its newest work-log lines.
// Below them: the command that scripts/cairn_next.py recommends, the
// workable planned milestones, and the planned ones that wait on
// dependencies. A line's `lead` keeps its width. Its `text` is cut to one
// line with an ellipsis, but for the goal's lines, which wrap: the operator
// picked one line per item at the M205 live look, so a long task list fits
// on one screen.

export type PaneLine = { key: string; indent: number; lead: Span[]; text: Span | null; wraps?: true }

export const NO_ROADMAP = 'no cairn ROADMAP found'
export const NO_FILE = 'no milestone file'
export const NO_ACTIVE = 'no active milestone'
export const CHECKED_MARK = '✓'
export const OPEN_MARK = '○'
// The warning text's theme key, as the band's warning labels use.
const WARNING = 'warning'

const PHASE: Record<string, { label: string; color: string }> = {
  'in-progress': { label: 'implement', color: ORANGE },
  review: { label: 'review', color: GREEN },
}

const line = (key: string, indent: number, lead: Span[], text: Span | null = null): PaneLine => ({
  key,
  indent,
  lead,
  text,
})

const heading = (key: string, text: string, count: string | null = null): PaneLine =>
  line(key, 0, [{ text, bold: true }], count === null ? null : { text: count, color: GRAY })

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

const count = (list: PaneItem[]) => `${list.filter(item => item.checked).length}/${list.length}`

function milestoneLines(row: PaneMilestone): PaneLine[] {
  const phase = PHASE[row.status] ?? { label: row.status, color: GRAY }
  const out: PaneLine[] = [
    line(
      `${row.id}-head`,
      0,
      [{ text: phase.label, color: phase.color, bold: true }, { text: ' ' }, { text: row.id, bold: true }, { text: '  ' }],
      { text: row.title },
    ),
  ]
  const file = row.file
  if (file === null) return [...out, line(`${row.id}-nofile`, 2, [], { text: NO_FILE, color: WARNING })]
  if (file.goal !== '') {
    out.push(heading(`${row.id}-goal-head`, 'Goal'))
    // A blank line between paragraphs draws as one space, so it keeps its row.
    file.goal.split('\n').forEach((text, i) =>
      out.push({ ...line(`${row.id}-goal-${i}`, 2, [], { text: text === '' ? ' ' : text }), wraps: true }),
    )
  }
  if (file.tasks.length > 0) {
    out.push(heading(`${row.id}-tasks-head`, 'Tasks ', count(file.tasks)))
    out.push(...items(`${row.id}-task`, file.tasks))
  }
  if (file.criteria.length > 0) {
    out.push(heading(`${row.id}-criteria-head`, 'Criteria ', count(file.criteria)))
    out.push(...items(`${row.id}-criterion`, file.criteria))
  }
  if (file.log.length > 0) {
    out.push(heading(`${row.id}-log-head`, 'Work log'))
    file.log.forEach((text, i) => out.push(line(`${row.id}-log-${i}`, 2, [], { text, color: GRAY })))
  }
  return out
}

// One blank row between groups.
const gap = (key: string) => line(key, 0, [], { text: ' ' })

export function paneLines(state: PaneState): PaneLine[] {
  if (!state.found) return [line('no-roadmap', 0, [], { text: NO_ROADMAP, color: GRAY })]
  const out: PaneLine[] = []
  if (state.milestones.length === 0) out.push(line('no-active', 0, [], { text: NO_ACTIVE, color: GRAY }))
  state.milestones.forEach((row, i) => {
    if (i > 0) out.push(gap(`${row.id}-gap`))
    out.push(...milestoneLines(row))
  })
  if (state.next !== null) {
    const target = state.next.id === null ? state.next.command : `${state.next.command} ${state.next.id}`
    out.push(gap('next-gap'))
    out.push(line('next', 0, [{ text: 'Next', bold: true }, { text: '  ' }], { text: target }))
  }
  if (state.workable.length > 0) {
    out.push(heading('workable-head', 'Workable'))
    for (const row of state.workable) {
      out.push(line(`workable-${row.id}`, 2, [{ text: row.id, bold: true }, { text: '  ' }], { text: row.title }))
    }
  }
  if (state.waiting.length > 0) {
    out.push(heading('waiting-head', 'Waiting'))
    for (const row of state.waiting) {
      out.push(
        line(`waiting-${row.id}`, 2, [{ text: row.id, bold: true }, { text: '  ' }], {
          text: `${row.title} · on ${row.unmet.join(', ')}`,
        }),
      )
    }
  }
  return out
}

// A line's text as one string, for tests and the alt text.
export function paneText(line: PaneLine): string {
  return [...line.lead, ...(line.text === null ? [] : [line.text])].map(span => span.text).join('')
}
