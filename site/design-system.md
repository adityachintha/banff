# EscapeWith.Ady Internal Guide Design System

This is the internal style guide for the Banff + Rockies guide website. It should not be exposed as a public page. The public guide should feel like a polished SaaS planning product: clear hero value, high-contrast cards, labels, tags, CTA hierarchy, compact sections, and reusable decision components.

## Design Principles

- SaaS travel utility: every section should look like a useful product surface, not a plain article.
- Decision first: sections should help someone plan, verify, save, book, compare, or decide.
- Clear hierarchy: use eyebrow labels, section kickers, cards, metrics, badges, and CTAs to make the guide scannable.
- Offline safe: system fonts, inline SVG icons, local CSS, local map files.
- Accessible by default: semantic headings, visible focus rings, high contrast, icons marked decorative.
- Print friendly: website content should export cleanly through browser "Save as PDF".

## Color System

Use this palette for the public UI. Keep contrast high and avoid publishing a visible style-guide page.

| Role | Token | Hex | Use |
| --- | --- | --- | --- |
| Ink | `--color-ink` | `#0f2522` | Primary body text |
| Strong ink | `--color-accent-strong` | `#0f2f2b` | Headings, primary CTA base, high-emphasis labels |
| Primary | `--color-accent` | `#166f61` | Buttons, active states, success/route accents |
| Signal | `--color-link` | `#0b7b94` | Links, secondary action accents, informational badges |
| Warm action | `--color-trail` / `--color-warning-line` | `#b65f22` | Warnings, long-drive labels, verification emphasis |
| Canvas | `--color-page` | `#f6faf8` | Page background |
| Surface | `--color-surface` | `#ffffff` | Cards and panels |
| Soft primary | `--color-accent-soft` | `#dff1eb` | Selected chips, low-emphasis badges |
| Soft signal | `--color-signal-soft` | `#e4f5f8` | Informational panels |
| Warning | `--color-warning` | `#fff4dc` | Verify-before-trip warnings |

Contrast rules:

- Primary text should use `--color-ink` on white, canvas, soft green, or soft signal surfaces.
- Primary CTAs should use white text on the evergreen gradient from `--color-accent-strong` to `--color-accent`.
- Warning panels should use dark text, warm background, and `--color-warning-line` borders.
- Links should keep visible underlines or strong context, and use `--color-link`.
- Badges should never rely on color alone; the label text must carry the meaning.

## Tokens

Tokens live in `site/styles.css` under `:root`.

Colors:

- `--color-ink`: primary text.
- `--color-muted`: secondary text.
- `--color-line`: borders and dividers.
- `--color-surface`: white content surface.
- `--color-page`: light SaaS canvas background.
- `--color-surface-soft`: subtle cards and callouts.
- `--color-surface-cool`: informational blue-green section surfaces.
- `--color-surface-green`: soft primary section surfaces.
- `--color-warning`: cautious verification notes.
- `--color-warning-line`: warning borders.
- `--color-accent`: icons, brand rule, hover accents.
- `--color-accent-strong`: primary action and tab text.
- `--color-accent-soft`: icon backgrounds, card accents, and selected surfaces.
- `--color-link`: external links and map actions.
- `--color-trail`: route and earth accent.
- `--color-snow`: warm white card surface.
- `--color-ridge`: muted mountain/ridge surface.
- `--color-signal-soft`: informational panel surface.
- `--shadow-card` and `--shadow-subtle`: restrained depth for screen only.

Typography:

- `--font-sans`: system sans stack.
- `--step--1`: helper text.
- `--step-0`: body text.
- `--step-1`: subtitle text.
- `--step-2`: section headings.
- `--step-3`: page title.

Spacing:

- `--space-1` to `--space-7` provide consistent increments from 4px to 48px.

Shape and borders:

- `--radius-card`: 8px.
- `--border-thin`: one-pixel divider.
- `--focus-ring`: high-contrast focus outline.

## Components

Header:

- Use `.site-header` for the guide cover area.
- Use `.hero-layout`, `.hero-copy`, and `.hero-panel` for the SaaS-style hero.
- Keep one brand line, one eyebrow, one `h1`, one summary, one route chip list, one primary action, and one secondary action.
- The hero panel should show useful proof/summary metrics, not decorative filler.

Buttons:

- Use `.button` for actions.
- Use `.button-secondary` for secondary public CTAs.
- Avoid more than two hero CTAs unless the extra action is essential.
- Add `.no-print` when the control should not appear in exported PDFs.

Sections:

- Use semantic `section` elements.
- Each section should start with an `h2` containing an inline SVG icon.
- Add `.section-kicker` above major headings to make sections feel productized and scannable.
- Icons are decorative and should use `aria-hidden="true"`.
- Add `.page-section` to guide sections.
- Add `.page-section-cool`, `.page-section-green`, or `.page-section-warm` when a section needs a subtle colored page band.
- Keep standalone paragraphs constrained to a readable line length so the guide does not feel text-heavy on wide screens.

Tabs:

- Use `.tabs` for the top guide navigation.
- Tabs should link to section IDs on the same page.
- Keep tab labels clear and short: one or two words, but not vague.
- Use large tap targets, visible focus states, opaque backgrounds, and enough scroll offset that sticky tabs do not cover headings.
- Add `.no-print` so tabs do not appear in downloaded PDFs.

Cards:

- Use `.day-grid` for two-column card layouts.
- Use `.day-card` for route/day modules.
- Add a `.badge` at the top of day cards when the card has a clear status such as `Buffer`, `Booked stack`, `Shuttle first`, or `Long drive`.
- Use `.food-guide-grid` and `.food-guide-card` for location-based food, coffee, hangout, and bar recommendations.
- Keep card headings short and details scannable.

Badges:

- Use `.badge-must` for important/required planning items.
- Use `.badge-time` for flexible or timing-related items.
- Use `.badge-farther` for long-drive, conditional, or extra-distance items.
- Badge text must be specific enough to make sense without color.

Links:

- Use `.link-list` for important actions such as booking links and map downloads.
- External links print with their URLs automatically.
- External web links use `target="_blank"` and `rel="noopener noreferrer"`.
- External links receive a small arrow marker on screen.
- Local downloads, such as map files, should not use the external-link arrow.

Lists:

- Use `.list-check` for packing and checklist content.
- Use `.list-compact` for short warning or mistake lists.
- Use `.list-ruled` for scannable reference lists.
- Use `.chip-list` for route flow or tab-like list items.

Callouts:

- Use `.callout` for helpful notes.
- Use `.warning` for verify-before-trip warnings.

Columns:

- Use `.columns` for compact grouped lists that do not need sequence or map context.

Timeline:

- Use `.timeline` for ordered route sections.
- Use `.timeline-item` for each stop.
- Each timeline item should include an image, badge, heading, short note, and map link.
- Badge options are `.badge-must`, `.badge-time`, and `.badge-farther`.
- Use local image assets so print/PDF export remains reliable.

## Icons

The icon system is inline SVG in `site/index.html`.

Rules:

- Keep icons 24x24 with 1.8px strokes.
- Use line icons only.
- Do not introduce emoji as section icons.
- Reuse existing symbols before adding new ones.
- Add new symbols inside `.icon-defs`, then reference with:

```html
<svg class="icon" aria-hidden="true"><use href="#icon-name"></use></svg>
```

## Print Rules

Print rules live in the `@media print` block in `site/styles.css`.

- The **Download as PDF** button is hidden in print via `.no-print`.
- Cards and callouts avoid page breaks where possible.
- Link URLs print after external links.
- Use Letter or A4, portrait, default margins.

## Editing Checklist

Before sharing:

- Check that every section has a clear heading and icon.
- Check that booking links and map downloads still work.
- Check that verify-before-trip warnings remain near rules, parking, shuttles, and passes.
- Use the browser **Download as PDF** button and scan the saved PDF for awkward breaks.
- Confirm the page works on mobile width.
