# Banff

EscapeWith.Ady Banff + Rockies Offline Guide is a clean static website for a reusable Banff/Rockies route planner. Visitors can download the full website as a PDF using the browser print dialog.

## Files

- `guide-content/banff-guide.md` - editable human-readable guide copy.
- `guide-content/itinerary.json` - structured itinerary source data.
- `guide-content/sources.md` - verify-before-trip links for parking, shuttles, passes, roads, and operators.
- `site/index.html` - static website version of the guide.
- `site/styles.css` - minimal offline website styling.
- `site/design-system.md` - design tokens, components, icon rules, and print/PDF guidance.
- `assets/banff-rockies-map-points.geojson` - approximate map points for compatible map apps.
- `assets/banff-rockies-map-points.kml` - approximate map points for Google Earth and compatible map apps.
- `assets/thumb-*.svg` - local illustrated thumbnails used by the website timeline.
- `vercel.json` - Vercel rewrites that serve the static site from the repo root.

## Edit the guide

Update `guide-content/itinerary.json` for day labels, routes, activities, drive notes, stays, parking notes, and offline reminders.

Update `guide-content/banff-guide.md` when you want to revise the readable master copy or reuse the content in captions, posts, or another format.

Update `guide-content/sources.md` before sharing the guide publicly. Parking, shuttle pickup rules, fees, seasonal schedules, road conditions, and opening times can change.

## Open the website locally

```text
site/index.html
```

For a local server that matches deployed asset paths, run from the repo root:

```sh
python3 -m http.server 4173
```

Then open `http://127.0.0.1:4173/site/`.

## Download the website as a PDF

Open `site/index.html` in a browser and click **Download as PDF**.

In the print dialog:

- Destination: Save as PDF
- Layout: Portrait
- Paper size: Letter or A4
- Margins: Default
- Background graphics: On, if your browser offers the option

The website includes print-specific CSS so the full guide exports cleanly.

Map downloads are saved in `assets/`. Import the GeoJSON or KML file into a compatible maps app, then verify exact trailheads, shuttle lots, parking rules, and road access before driving.

## Offline design notes

The website uses system fonts, inline SVG icons, local CSS, and local map files. It does not require external font downloads, web images, or internet assets to render.

Before final sharing, verify the links in `guide-content/sources.md`, especially Parks Canada Lake Louise/Moraine Lake shuttle rules, Town of Banff parking, Kananaskis pass requirements, Icefields Parkway road conditions, Columbia Icefield activity details, and community tips from Reddit.
