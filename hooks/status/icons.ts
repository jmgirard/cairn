// The cairn pane's marks as small SVG icons on the desktop (M286), drawn
// like the desktop app's own task list: a filled circle with a check, a
// circle with three dots, and a dashed circle, all one size. A span that
// names an icon draws it on a surface with the `Svg` element and its text
// glyph in the terminal. An image has no theme signal (ROADMAP "Gaps only
// the app or mod API can close"), so each icon takes a fixed color chosen
// to read on both the dark and the light theme.

export type IconName =
  | 'done'
  | 'current'
  | 'open'
  | 'ring'
  | 'merged'
  | 'review'
  | 'attention'
  | 'closed'
  | 'high'
  | 'low'
  | 'parked'
  | 'mergeable'
  | 'conflicts'

// The icon's drawn size in CSS pixels.
export const ICON_PX = 14

// The fixed colors: a neutral gray, and the implement, review, warning, and
// error colors near the theme's own (red since M301), and a muted blue for
// a parked row, so it differs from a gray low row (M305).
export const ICON_COLORS = {
  gray: '#8f8f8f',
  ink: '#1f1f1e',
  orange: '#d77757',
  green: '#4eba65',
  amber: '#d9a21b',
  red: '#e5534b',
  blue: '#7f93c4',
} as const

const RING = (color: string, dash = '') =>
  `<circle cx="8" cy="8" r="6.5" fill="none" stroke="${color}" stroke-width="1.4"${dash === '' ? '' : ` stroke-dasharray="${dash}"`}/>`
const DISC = (color: string) => `<circle cx="8" cy="8" r="7" fill="${color}"/>`
const CHECK = (color: string) =>
  `<path d="M4.9 8.2 7.1 10.3 11.1 5.9" fill="none" stroke="${color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>`
const DOTS = (color: string) => [5, 8, 11].map(x => `<circle cx="${x}" cy="8" r="0.95" fill="${color}"/>`).join('')
const LINE = (d: string, color: string) =>
  `<path d="${d}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>`

// A merge symbol (M301): a branch from the top node runs down to the bottom
// node and curves out to the right node.
const MERGE = (color: string) =>
  LINE('M5 5V11M5 5.2C5 8 7.6 8 10.1 8', color) +
  [
    [5, 3.4],
    [5, 12.6],
    [11.7, 8],
  ]
    .map(([x, y]) => `<circle cx="${x}" cy="${y}" r="1.6" fill="none" stroke="${color}" stroke-width="1.4"/>`)
    .join('')

const { gray, ink, orange, green, amber, red, blue } = ICON_COLORS
const BODIES: Record<IconName, string> = {
  done: DISC(gray) + CHECK(ink),
  current: RING(gray) + DOTS(gray),
  open: RING(gray, '2.2 1.9'),
  ring: RING(gray),
  merged: DISC(green) + CHECK(ink),
  review: RING(gray) + DOTS(gray),
  attention: DISC(amber) + LINE('M8 4.6V8.7', ink) + `<circle cx="8" cy="11.1" r="0.9" fill="${ink}"/>`,
  closed: RING(gray) + LINE('M5.8 5.8 10.2 10.2M10.2 5.8 5.8 10.2', gray),
  high: RING(orange) + LINE('M8 11V5M5.6 7.4 8 5 10.4 7.4', orange),
  low: RING(gray) + LINE('M8 5V11M5.6 8.6 8 11 10.4 8.6', gray),
  parked: RING(blue, '2.2 1.9') + LINE('M8 5.2V8.2L9.9 9.4', blue),
  mergeable: MERGE(green),
  conflicts: DISC(red) + LINE('M5.8 5.8 10.2 10.2M10.2 5.8 5.8 10.2', ink),
}

// The icon's SVG document.
export function iconSvg(name: IconName): string {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${ICON_PX}" height="${ICON_PX}" viewBox="0 0 16 16">${BODIES[name]}</svg>`
}
