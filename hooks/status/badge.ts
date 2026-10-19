import type { Span } from './band'

// The count badge on the Blocked, Hotfixes, and Candidates headings
// (M289), in place of the bare gray count that M286 drew. On the desktop
// it draws as an `Svg` pill, a rounded rectangle in the heading's fill
// with the number in white. In the terminal it draws as the number with a
// space on each side, in `inverseText` on the heading's theme key, the
// colors of the band's terminal pill (track.ts `PILL_TEXT`), though not
// bold as that pill is.
// An image has no theme signal (ROADMAP "Gaps only the app or mod API can
// close"), so each fill is a fixed color near its key, dark enough that
// white reads on it at about 5:1 or more: the band pill's own plan blue
// and implement orange (track.ts `PHASE_FILLS`), and a dark amber near
// `warning`.

export type BadgeName = 'blocked' | 'hotfixes' | 'candidates'

// The theme key each heading's terminal badge takes as its ground.
export const BADGE_KEY: Record<BadgeName, string> = {
  blocked: 'warning',
  hotfixes: 'claude',
  candidates: 'planMode',
}

// Each heading's desktop pill: its fill and the number's color.
export const BADGE_FILL: Record<BadgeName, { fill: string; text: string }> = {
  blocked: { fill: 'rgb(146,103,22)', text: 'rgb(255,255,255)' },
  hotfixes: { fill: 'rgb(152,85,57)', text: 'rgb(255,255,255)' },
  candidates: { fill: 'rgb(71,103,158)', text: 'rgb(255,255,255)' },
}

// The terminal badge's text color.
export const BADGE_TEXT_KEY = 'inverseText'

// The pill's height in CSS pixels, the estimated width of one digit, and
// the room left and right of the number together.
export const BADGE_H = 16
export const BADGE_DIGIT = 7
export const BADGE_PAD = 12

// The pill's width: the number's estimated width and the padding, 19 for
// one digit, so even a one-digit count draws as a short pill.
export function badgeWidth(count: number): number {
  return `${count}`.length * BADGE_DIGIT + BADGE_PAD
}

// The pill's SVG document. As in the band's pill (track.ts), `textLength`
// holds the number to the width less the padding, so a wider fallback font
// squeezes the digits rather than running past the pill's ends.
export function badgeSvg(count: number, name: BadgeName): string {
  const width = badgeWidth(count)
  const { fill, text } = BADGE_FILL[name]
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${BADGE_H}" viewBox="0 0 ${width} ${BADGE_H}">` +
    `<rect class="badge" width="${width}" height="${BADGE_H}" rx="${BADGE_H / 2}" fill="${fill}"/>` +
    `<text class="badge-text" x="${width / 2}" y="${BADGE_H / 2}" textLength="${width - BADGE_PAD}" lengthAdjust="spacingAndGlyphs" text-anchor="middle" dominant-baseline="central" font-family="-apple-system,system-ui,sans-serif" font-size="10.5" font-weight="650" fill="${text}">${count}</text>` +
    `</svg>`
  )
}

// The badge as a span: the terminal's text and colors, and the badge's
// name and count, which the desktop draws as `badgeSvg`.
export function badgeSpan(count: number, name: BadgeName): Span {
  return { text: ` ${count} `, color: BADGE_TEXT_KEY, backgroundColor: BADGE_KEY[name], badge: { name, count } }
}
