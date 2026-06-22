# EscapeWith.Ady Guide Design System

This is a Rockies field-guide design system for the Banff + Rockies guide website. The goal is to keep the guide readable on mobile, printable as a PDF, and easy to maintain while giving it a stronger mountain-route identity.

## Design Principles

- Field-guide first: practical layouts, map-like accents, calm alpine colors, and no heavy decoration.
- Travel utility over marketing: every section should help someone plan, verify, save, or decide.
- Offline safe: system fonts, inline SVG icons, local CSS, local map files.
- Accessible by default: semantic headings, visible focus rings, high contrast, icons marked decorative.
- Print friendly: website content should export cleanly through browser "Save as PDF".

## Tokens

Tokens live in `site/styles.css` under `:root`.

Colors:

- `--color-ink`: primary text.
- `--color-muted`: secondary text.
- `--color-line`: borders and dividers.
- `--color-surface`: white content surface.
- `--color-page`: alpine page background.
- `--color-surface-soft`: subtle cards and callouts.
- `--color-surface-cool`: glacier-blue section surfaces.
- `--color-surface-green`: soft evergreen section surfaces.
- `--color-warning`: cautious verification notes.
- `--color-warning-line`: warning borders.
- `--color-accent`: icons, brand rule, hover accents.
- `--color-accent-strong`: primary action and tab text.
- `--color-accent-soft`: icon backgrounds, card accents, and selected surfaces.
- `--color-link`: external links and map actions.
- `--color-trail`: route and earth accent.
- `--color-snow`: warm white card surface.
- `--color-ridge`: muted mountain/ridge surface.
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
- Keep one brand line, one `h1`, one subtitle, one short note, and one primary action.
- Header styling should feel like a quiet map cover: strong title, route subtitle, and subtle ridge accents.

Buttons:

- Use `.button` for actions.
- Add `.no-print` when the control should not appear in exported PDFs.

Sections:

- Use semantic `section` elements.
- Each section should start with an `h2` containing an inline SVG icon.
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
- Use `.food-guide-grid` and `.food-guide-card` for location-based food, coffee, hangout, and bar recommendations.
- Keep card headings short and details scannable.

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
