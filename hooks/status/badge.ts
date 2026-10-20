import type { Span } from './band'

// The count badge on the Blocked, Hotfixes, and Candidates headings
// (M289), in place of the bare gray count that M286 drew. On the desktop
// it draws as an `Svg` pill, a rounded rectangle in one gray fill with
// the number in white. In the terminal it draws as the number with a
// space on each side, in `inverseText` on `inactive`, the theme's gray:
// the band terminal pill's text key (track.ts `PILL_TEXT`), but not bold,
// where that pill is bold. Since M302 the three headings share the one gray, where
// M289 gave each its own color.
// An image has no theme signal (ROADMAP "Gaps only the app or mod API can
// close"), so the fill is a fixed mid gray, dark enough that white reads
// on it at about 5:1, and light enough to show on a dark ground.

// The terminal badge's ground: the theme's gray.
export const BADGE_KEY = 'inactive'

// The desktop pill's fill and the number's color.
export const BADGE_FILL = { fill: 'rgb(110,110,110)', text: 'rgb(255,255,255)' }

// The terminal badge's text color.
export const BADGE_TEXT_KEY = 'inverseText'

// The pill's height in CSS pixels, the estimated width of one digit, and
// the room left and right of the number together. A system-font digit at
// 10.5 px is about 6 px wide, so `textLength` stretches it little.
export const BADGE_H = 16
export const BADGE_DIGIT = 6
export const BADGE_PAD = 12

// The pill's width: the number's estimated width and the padding, 18 for
// one digit, so even a one-digit count draws as a short pill.
export function badgeWidth(count: number): number {
  return `${count}`.length * BADGE_DIGIT + BADGE_PAD
}

// The pill's SVG document. As in the band's pill (track.ts), `textLength`
// holds the number to the width less the padding, so a wider fallback font
// squeezes the digits rather than running past the pill's ends.
export function badgeSvg(count: number): string {
  const width = badgeWidth(count)
  const { fill, text } = BADGE_FILL
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${BADGE_H}" viewBox="0 0 ${width} ${BADGE_H}">` +
    `<rect class="badge" width="${width}" height="${BADGE_H}" rx="${BADGE_H / 2}" fill="${fill}"/>` +
    `<text class="badge-text" x="${width / 2}" y="${BADGE_H / 2}" textLength="${width - BADGE_PAD}" lengthAdjust="spacingAndGlyphs" text-anchor="middle" dominant-baseline="central" font-family="-apple-system,system-ui,sans-serif" font-size="10.5" font-weight="650" fill="${text}">${count}</text>` +
    `</svg>`
  )
}

// The badge as a span: the terminal's text and colors, and the badge's
// count, which the desktop draws as `badgeSvg`.
export function badgeSpan(count: number): Span {
  return { text: ` ${count} `, color: BADGE_TEXT_KEY, backgroundColor: BADGE_KEY, badge: { count } }
}
