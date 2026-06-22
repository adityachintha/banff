#!/usr/bin/env python3
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Circle, Drawing, Line, Path as ShapePath, Rect
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "guide-content"
OUTPUT = ROOT / "output" / "escape-with-ady-banff-rockies-guide.pdf"

PAGE_W, PAGE_H = letter
MARGIN = 0.58 * inch
FOOTER_H = 0.35 * inch

DEEP_GREEN = colors.HexColor("#1F2933")
SLATE = colors.HexColor("#4B5563")
GLACIER = colors.HexColor("#F3F4F6")
GLACIER_DARK = colors.HexColor("#374151")
WARM_BEIGE = colors.HexColor("#FAFAF8")
BEIGE_DARK = colors.HexColor("#9CA3AF")
MIST = colors.HexColor("#FFFFFF")
LINE = colors.HexColor("#D1D5DB")
WARNING_BG = colors.HexColor("#FFF3D8")
WARNING = colors.HexColor("#8A4E12")
TEXT = colors.HexColor("#111827")


def load_data():
    with (CONTENT / "itinerary.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def styles():
    base = getSampleStyleSheet()
    return {
        "coverTitle": ParagraphStyle(
            "coverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=33,
            textColor=TEXT,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "coverSubtitle": ParagraphStyle(
            "coverSubtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=12.5,
            leading=17,
            textColor=SLATE,
            alignment=TA_CENTER,
            spaceAfter=18,
        ),
        "coverBrand": ParagraphStyle(
            "coverBrand",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=TEXT,
            alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            textColor=DEEP_GREEN,
            spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=DEEP_GREEN,
            spaceBefore=4,
            spaceAfter=7,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=15,
            textColor=GLACIER_DARK,
            spaceBefore=3,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.2,
            textColor=TEXT,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.1,
            leading=10.6,
            textColor=SLATE,
        ),
        "micro": ParagraphStyle(
            "micro",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=9,
            textColor=SLATE,
        ),
        "label": ParagraphStyle(
            "label",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10,
            textColor=DEEP_GREEN,
            spaceAfter=2,
        ),
        "cardTitle": ParagraphStyle(
            "cardTitle",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=17,
            textColor=colors.white,
            spaceAfter=5,
        ),
        "cardText": ParagraphStyle(
            "cardText",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.7,
            leading=11.4,
            textColor=TEXT,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.1,
            leading=12.3,
            textColor=TEXT,
            leftIndent=9,
            bulletIndent=0,
            spaceAfter=3,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.2,
            leading=9,
            textColor=SLATE,
            alignment=TA_CENTER,
        ),
    }


S = styles()


def p(text, style="body"):
    text = str(text).replace("&", "&amp;")
    return Paragraph(text, S[style])


def icon_drawing(name):
    d = Drawing(18, 18)
    c = GLACIER_DARK
    sw = 1.4

    if name == "info":
        d.add(Circle(9, 9, 7, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Line(9, 7, 9, 12, strokeColor=c, strokeWidth=sw))
        d.add(Circle(9, 14, 0.7, strokeColor=c, fillColor=c))
    elif name == "check":
        d.add(Rect(3, 3, 12, 12, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Line(6, 9, 8, 6, strokeColor=c, strokeWidth=sw))
        d.add(Line(8, 6, 13, 12, strokeColor=c, strokeWidth=sw))
    elif name == "route":
        d.add(Circle(4, 4, 2, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Circle(14, 14, 2, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Line(5.5, 5.5, 12.5, 12.5, strokeColor=c, strokeWidth=sw))
    elif name == "days":
        d.add(Rect(3, 4, 12, 10, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Line(3, 11, 15, 11, strokeColor=c, strokeWidth=sw))
        d.add(Line(6, 15, 6, 13, strokeColor=c, strokeWidth=sw))
        d.add(Line(12, 15, 12, 13, strokeColor=c, strokeWidth=sw))
    elif name == "book":
        d.add(Rect(3, 4, 12, 10, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Line(6, 4, 6, 14, strokeColor=c, strokeWidth=sw))
        d.add(Line(8, 11, 13, 11, strokeColor=c, strokeWidth=sw))
    elif name == "rain":
        d.add(Line(4, 8, 14, 8, strokeColor=c, strokeWidth=sw))
        d.add(Line(9, 8, 9, 3, strokeColor=c, strokeWidth=sw))
        d.add(Line(9, 3, 12, 3, strokeColor=c, strokeWidth=sw))
        pth = ShapePath(strokeColor=c, fillColor=None, strokeWidth=sw)
        pth.moveTo(4, 8)
        pth.curveTo(5, 13, 13, 13, 14, 8)
        d.add(pth)
    elif name == "apps":
        d.add(Rect(5, 2.5, 8, 13, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Line(7, 13, 11, 13, strokeColor=c, strokeWidth=sw))
        d.add(Circle(9, 4.5, 0.6, strokeColor=c, fillColor=c))
    elif name == "map":
        d.add(Rect(3, 4, 12, 10, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Line(7, 4, 7, 14, strokeColor=c, strokeWidth=sw))
        d.add(Line(11, 4, 11, 14, strokeColor=c, strokeWidth=sw))
        d.add(Circle(9, 9, 1.5, strokeColor=c, fillColor=None, strokeWidth=sw))
    elif name == "pack":
        d.add(Rect(4, 3, 10, 10, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Line(7, 13, 7, 15, strokeColor=c, strokeWidth=sw))
        d.add(Line(11, 13, 11, 15, strokeColor=c, strokeWidth=sw))
        d.add(Line(7, 15, 11, 15, strokeColor=c, strokeWidth=sw))
        d.add(Line(5.5, 8, 12.5, 8, strokeColor=c, strokeWidth=sw))
        d.add(Line(6, 5, 12, 5, strokeColor=c, strokeWidth=sw))
        d.add(Line(4, 9, 2.5, 9, strokeColor=c, strokeWidth=sw))
        d.add(Line(2.5, 9, 2.5, 6, strokeColor=c, strokeWidth=sw))
        d.add(Line(2.5, 6, 4, 6, strokeColor=c, strokeWidth=sw))
        d.add(Line(14, 9, 15.5, 9, strokeColor=c, strokeWidth=sw))
        d.add(Line(15.5, 9, 15.5, 6, strokeColor=c, strokeWidth=sw))
        d.add(Line(15.5, 6, 14, 6, strokeColor=c, strokeWidth=sw))
    elif name == "trail":
        d.add(Line(3, 4, 8, 14, strokeColor=c, strokeWidth=sw))
        d.add(Line(8, 14, 15, 4, strokeColor=c, strokeWidth=sw))
        d.add(Line(6, 8, 10, 8, strokeColor=c, strokeWidth=sw))
    elif name == "firstaid":
        d.add(Rect(4, 4, 10, 10, strokeColor=c, fillColor=None, strokeWidth=sw))
        d.add(Line(9, 6, 9, 12, strokeColor=c, strokeWidth=sw))
        d.add(Line(6, 9, 12, 9, strokeColor=c, strokeWidth=sw))
    elif name == "food":
        d.add(Line(5, 15, 5, 3, strokeColor=c, strokeWidth=sw))
        d.add(Line(3, 15, 3, 10, strokeColor=c, strokeWidth=sw))
        d.add(Line(7, 15, 7, 10, strokeColor=c, strokeWidth=sw))
        d.add(Line(3, 10, 7, 10, strokeColor=c, strokeWidth=sw))
        d.add(Line(12, 15, 12, 3, strokeColor=c, strokeWidth=sw))
        pth = ShapePath(strokeColor=c, fillColor=None, strokeWidth=sw)
        pth.moveTo(12, 15)
        pth.curveTo(16, 13, 16, 8, 12, 8)
        d.add(pth)
    else:
        d.add(Circle(9, 9, 6, strokeColor=c, fillColor=None, strokeWidth=sw))
    return d


def section_heading(title, icon_name, style="h1"):
    t = Table([[icon_drawing(icon_name), p(title, style)]], colWidths=[0.28 * inch, PAGE_W - 2 * MARGIN - 0.28 * inch])
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def bullets(items, style="bullet"):
    return ListFlowable(
        [ListItem(p(item, style), leftIndent=9) for item in items],
        bulletType="bullet",
        bulletFontName="Helvetica",
        bulletFontSize=7,
        bulletColor=DEEP_GREEN,
        start="circle",
        leftIndent=14,
        bulletIndent=2,
        spaceAfter=6,
    )


def activity_lookup(data):
    return {item["name"]: item for item in data.get("activities", [])}


def compact_table(rows, col_widths=None):
    if col_widths is None:
        col_widths = [2.0 * inch, PAGE_W - 2 * MARGIN - 2.0 * inch]
    t = Table(rows, colWidths=col_widths)
    t.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def tag(text, bg=GLACIER, fg=DEEP_GREEN):
    t = Table([[p(text, "small")]], colWidths=[None])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("TEXTCOLOR", (0, 0), (-1, -1), fg),
                ("BOX", (0, 0), (-1, -1), 0.25, bg),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def callout(title, body, kind="tip"):
    bg = WARNING_BG if kind == "warning" else GLACIER
    border = WARNING if kind == "warning" else GLACIER_DARK
    rows = [[p(title, "label")], [p(body, "small")]]
    t = Table(rows, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.8, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return KeepTogether([t, Spacer(1, 8)])


def nowaitsy_card(short=False):
    body = (
        "Banff gets crowded fast. Use NoWaitsy before you leave so you do not waste time "
        "walking into long waits."
        if short
        else "Mountain towns get crowded fast, especially around lunch, dinner, cafes, and popular downtown areas. "
        "Before heading out, use NoWaitsy to check nearby places, avoid long waits, and make faster decisions."
    )
    rows = [[p("Before you go: check if it is worth going right now", "label")], [p(body, "small")]]
    if not short:
        rows.append(
            [
                bullets(
                    [
                        "Check before leaving your hotel",
                        "Compare nearby restaurants/cafes",
                        "Avoid wasting time in long queues",
                        "Useful for Banff, Canmore, Calgary, and busy stops",
                    ],
                    "small",
                )
            ]
        )
        rows.append([p("Download/use NoWaitsy before heading to crowded places.", "label")])
    t = Table(rows, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), MIST),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return KeepTogether([t, Spacer(1, 8)])


def food_stops_table(data):
    rows = [[p("Area", "label"), p("Coffee / hangouts", "label"), p("Food / bars", "label"), p("Best use", "label")]]
    for item in data.get("foodStops", []):
        coffee_hangouts = (
            f"<b>Coffee:</b> {'; '.join(item.get('coffee', []))}<br/>"
            f"<b>Hangouts:</b> {'; '.join(item.get('hangouts', []))}"
        )
        food_bars = (
            f"<b>Food:</b> {'; '.join(item.get('food', []))}<br/>"
            f"<b>Bars:</b> {'; '.join(item.get('bars', []))}"
        )
        rows.append([p(item["area"], "small"), p(coffee_hangouts, "micro"), p(food_bars, "micro"), p(item["note"], "micro")])
    t = Table(
        rows,
        colWidths=[1.0 * inch, 1.8 * inch, 2.05 * inch, PAGE_W - 2 * MARGIN - 4.85 * inch],
        repeatRows=1,
    )
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), DEEP_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DEEP_GREEN)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.drawString(MARGIN, 0.37 * inch, "EscapeWith.Ady | @escapewith.ady")
    canvas.setFont("Helvetica", 7.3)
    canvas.setFillColor(SLATE)
    canvas.drawCentredString(PAGE_W / 2, 0.37 * inch, "Offline Banff + Rockies Guide")
    canvas.drawRightString(PAGE_W - MARGIN, 0.37 * inch, f"{doc.page}")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 0.55 * inch, PAGE_W - MARGIN, 0.55 * inch)
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(1)
    canvas.line(MARGIN, PAGE_H - 1.25 * inch, PAGE_W - MARGIN, PAGE_H - 1.25 * inch)
    canvas.line(MARGIN, 1.25 * inch, PAGE_W - MARGIN, 1.25 * inch)
    canvas.setFillColor(SLATE)
    canvas.setFont("Helvetica", 9)
    canvas.drawCentredString(PAGE_W / 2, PAGE_H - 0.95 * inch, "ESCAPEWITH.ADY")
    canvas.restoreState()


def cover_story(data):
    return [
        Spacer(1, 2.45 * inch),
        p(data["guideTitle"], "coverTitle"),
        p(data["subtitle"], "coverSubtitle"),
        p("Pick the days that fit your trip", "coverSubtitle"),
        Spacer(1, 8),
        p(f"By {data['brand']} | {data['handle']}", "coverBrand"),
        Spacer(1, 2.45 * inch),
        p("Use NoWaitsy before heading to crowded restaurants, cafes, and popular spots.", "coverSubtitle"),
        NextPageTemplate("normal"),
        PageBreak(),
    ]


def intro_story(data):
    checklist = [
        "Download Google Maps offline: Calgary, Canmore, Banff, Lake Louise, Icefields Parkway, Jasper.",
        "Save hotel addresses offline.",
        "Screenshot activity bookings.",
        "Screenshot shuttle reservations.",
        "Screenshot parking confirmations.",
        "Fill fuel before Icefields Parkway.",
        "Carry snacks and water.",
        "Keep a power bank.",
        "Save emergency numbers.",
        "Keep warm layers even in early summer.",
        "Keep printed or offline copy of park pass/reservations.",
    ]
    return [
        section_heading("How to use this guide", "info"),
        p(
            "This is a route-based offline guide. Pick the days that match your schedule, save it to your phone before the trip, download offline maps, "
            "screenshot bookings, and use the plan as a flexible planner instead of a strict checklist.",
        ),
        callout(
            "Verify before final use",
            "Parking, shuttle pickup rules, fees, seasonal schedules, road conditions, and opening times can change. "
            "Check official Parks Canada, Town of Banff, Alberta, operator, and activity pages before the trip.",
            "warning",
        ),
        section_heading("Offline prep checklist", "check"),
        bullets(checklist),
        callout(
            "Creator note",
            "Follow @escapewith.ady for real travel routes, parking tips, and Banff guides.",
        ),
        PageBreak(),
    ]


def route_story(data):
    flow_rows = []
    for idx, leg in enumerate(data["route"], 1):
        flow_rows.append([p(str(idx), "label"), p(leg, "body")])
    t = Table(flow_rows, colWidths=[0.38 * inch, PAGE_W - 2 * MARGIN - 0.38 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), GLACIER),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return [
        section_heading("Route overview", "route"),
        p("A simple route flow for planning, driving days, and offline map downloads."),
        t,
        Spacer(1, 11),
        p("Best base logic", "h2"),
        bullets(data["stays"]),
        callout(
            "Offline map logic",
            "Download the whole corridor, not only pins. Include Calgary, Canmore, Banff, Lake Louise, Icefields Parkway, and Jasper.",
        ),
        PageBreak(),
    ]


def planning_sections_story(data):
    activity_rows = [[p("Activity", "label"), p("Book / verify", "label")]]
    for item in data.get("activities", []):
        activity_rows.append(
            [
                p(f"{item['name']}<br/><font size='6'>{item['area']}</font>", "small"),
                p(f"{item['bookUrl']}<br/>{item['note']}", "micro"),
            ]
        )

    rainy = [
        "Banff Upper Hot Springs",
        "Cave and Basin, Whyte Museum, or Banff Park Museum",
        "Bow Falls or Bow River walk if rain is light",
        "Johnston Canyon only if conditions and crowd levels make sense",
        "Canmore cafes, Elevation Place, or a slow food/reset window",
        "Banff Gondola only if visibility is still good",
    ]
    apps = [
        "Google Maps or Apple Maps: download offline areas before leaving Calgary/Canmore",
        "Parks Canada app/site: closures, trail conditions, shuttle rules, park info",
        "Alberta 511: road conditions before Icefields Parkway",
        "Roam Transit: Banff/Canmore transit routes and schedules",
        "AllTrails: route-finding and recent trail feedback; verify closures with official sources",
        "NoWaitsy: check restaurants, cafes, bars, hangouts, and crowded areas before you leave",
        "Download NoWaitsy on the App Store: https://apps.apple.com/ca/app/nowaitsy-live-wait-times/id6763641743",
    ]
    viewpoints = [
        "Lake Minnewanka",
        "Banff Gondola / Sulphur Mountain",
        "Moraine Lake",
        "Lake Louise Lakeshore",
        "Peyto Lake Viewpoint",
        "Bow Lake",
        "Mistaya Canyon",
        "Columbia Icefield",
        "Tangle Falls",
        "Sunwapta Falls and Athabasca Falls if going farther toward Jasper",
    ]
    essentials = [
        "Warm layer, rain shell, comfortable walking shoes",
        "Water bottle, snacks, electrolytes",
        "Power bank and charging cable",
        "Sunglasses, sunscreen, lip balm",
        "Offline maps, screenshots, park pass/reservations",
        "Small trash bag and tissues",
        "Bear spray for appropriate trails; do not fly with it",
    ]
    trails = [
        "Lake Louise Lakeshore: easy, classic, crowd-friendly",
        "Moraine Lake Rockpile: short iconic viewpoint when access is available",
        "Tunnel Mountain: approachable Banff town hike",
        "Bow River / Bow Falls: low-commitment walk",
        "Johnston Canyon: popular rainy-day-friendly option, verify crowds/closures",
        "Lake Agnes: classic Lake Louise trail, more effort",
        "Sulphur Mountain: hike option instead of gondola if conditions and fitness fit",
    ]
    first_aid = [
        "Bandages, blister pads, gauze, medical tape",
        "Antiseptic wipes and small antibiotic ointment",
        "Pain reliever, antihistamine, personal medication",
        "Tweezers, safety pins, small scissors",
        "Elastic wrap, instant cold pack",
        "Emergency blanket and whistle",
        "Hand sanitizer and gloves",
    ]

    return [
        section_heading("Activities to book or verify", "book"),
        p("Use these as activity references, not fixed personal timings. Book with the confirmed provider and screenshot every reservation."),
        compact_table(activity_rows, [1.75 * inch, PAGE_W - 2 * MARGIN - 1.75 * inch]),
        Spacer(1, 10),
        section_heading("Rainy day activities", "rain", "h2"),
        bullets(rainy),
        section_heading("Apps to use", "apps", "h2"),
        bullets(apps),
        PageBreak(),
        section_heading("Food, coffee, hangouts, and bars by location", "food"),
        p("Use this as a shortlist, not a fixed reservation plan. Check current hours, seasonal openings, reservations, and live waits before going."),
        food_stops_table(data),
        Spacer(1, 8),
        callout(
            "Check before going",
            "Open NoWaitsy before choosing a spot, check wait times, then decide if it is worth going right now. App Store: https://apps.apple.com/ca/app/nowaitsy-live-wait-times/id6763641743",
        ),
        PageBreak(),
        section_heading("Viewpoints and downloadable map points", "map"),
        bullets(viewpoints),
        callout(
            "Map download",
            "Approximate map pins are saved in assets/banff-rockies-map-points.geojson and assets/banff-rockies-map-points.kml. Import them into a compatible maps app, then verify exact trailheads, parking, and shuttle locations before driving.",
            "warning",
        ),
        section_heading("Essentials to pack", "pack", "h2"),
        bullets(essentials),
        section_heading("Best trails to consider", "trail", "h2"),
        bullets(trails),
        section_heading("First aid kit", "firstaid", "h2"),
        bullets(first_aid),
        PageBreak(),
    ]


def field_block(label, content):
    if isinstance(content, list):
        flow = [p(label, "label"), bullets(content, "small")]
    else:
        flow = [p(label, "label"), p(content, "small")]
    return flow


def day_card(day):
    title = f"{day['day']} | {day['route']}"
    left = []
    left.extend(field_block("Main plan", day["mainPlan"]))
    left.extend(field_block("Drive notes", day["driveNotes"]))
    left.extend(field_block("Parking/shuttle notes", day["parkingShuttleNotes"]))
    right = []
    right.extend(field_block("What to see", day["whatToSee"]))
    right.extend(field_block("Food/washroom note", day["foodWashroomNote"]))
    right.extend(field_block("Backup option", day["backupOption"]))
    right.extend(field_block("Offline reminder", day["offlineReminder"]))
    if day.get("bookingDisplay"):
        right.extend(field_block("Book / verify", day["bookingDisplay"]))
    right.append(p(f"Stay: {day['stay']}", "label"))
    if day.get("sleepNote"):
        right.append(p(f"Sleep note: {day['sleepNote']}", "small"))

    header = Table([[p(title, "cardTitle")]], colWidths=[PAGE_W - 2 * MARGIN])
    body = Table([[left, right]], colWidths=[(PAGE_W - 2 * MARGIN) * 0.49, (PAGE_W - 2 * MARGIN) * 0.49])
    header.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), GLACIER_DARK),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    body.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return KeepTogether([header, body, Spacer(1, 11)])


def days_story(data):
    activities = activity_lookup(data)
    story = [p("Day-by-day itinerary", "h1")]
    for day in data["days"]:
        day["bookingDisplay"] = [
            f"{name}: {activities[name]['bookUrl']}" if name in activities else name
            for name in day.get("bookingLinks", [])
        ]
        story.append(day_card(day))
        if day["day"] in {"Banff Activity Day", "Lake Louise + Moraine Lake Day"}:
            story.append(nowaitsy_card(short=True))
    story.append(PageBreak())
    return story


def cheat_sheet_story():
    sections = [
        ("Banff town parking strategy", "Arrive early, choose a parking target before entering town, and verify Town of Banff rules before final use."),
        ("Lake Minnewanka parking/transit note", "Verify cruise check-in, parking, and transit conditions before final use."),
        ("Banff Gondola/Sulphur Mountain parking note", "Verify parking and shuttle options before final use."),
        ("Lake Louise parking/shuttle note", "Verify the correct lot, ticket type, check-in location, and return window before final use."),
        ("Moraine Lake shuttle note", "Do not assume personal vehicle access. Verify shuttle pickup, return window, and backup plan before final use."),
        ("Canmore parking/stay strategy", "Use Canmore as the calmer base and confirm hotel parking."),
        ("Kananaskis pass note", "Verify whether your exact Kananaskis stops require a Conservation Pass."),
    ]
    rows = [[p(title, "label"), p(body, "small")] for title, body in sections]
    t = Table(rows, colWidths=[2.12 * inch, PAGE_W - 2 * MARGIN - 2.12 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), WARM_BEIGE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return [
        p("Parking and shuttle cheat sheet", "h1"),
        callout(
            "Important warning",
            "Do not assume parking and park entry are the same thing. Parking, shuttles, reservations, and activities may be separate.",
            "warning",
        ),
        t,
        Spacer(1, 9),
        callout(
            "Rule of thumb",
            "Use cautious language when sharing this guide: verify before trip, rules and fees can change, and check official Parks Canada / Town of Banff pages before final use.",
        ),
        nowaitsy_card(short=True),
        PageBreak(),
    ]


def stop_guide_story():
    stops = [
        ("Must-stop", "Peyto Lake", "lake/viewpoint", "20-45 min", "Iconic aerial-style lake view.", "Compressed wide shot from the viewpoint."),
        ("Must-stop", "Bow Lake", "lake/viewpoint", "quick stop / 20 min", "Easy roadside mountain-lake pause.", "Shoreline foreground with peaks behind."),
        ("Must-stop", "Columbia Icefield", "glacier/activity hub", "2.5+ hrs", "Main Icefields Parkway booked experience.", "Scale shots with glacier and tour vehicles."),
        ("Must-stop", "Mistaya Canyon", "canyon", "30-45 min", "Good texture, water movement, and canyon drama.", "Vertical canyon framing."),
        ("Great if time", "Herbert Lake", "lake", "quick stop", "Calm reflection if light is good.", "Still water reflection clip."),
        ("Great if time", "Waterfowl Lakes", "lake/viewpoint", "20 min", "Scenic pause without overcommitting.", "Wide lake pan."),
        ("Great if time", "Saskatchewan Crossing", "rest stop", "quick stop", "Useful logistics stop for food/fuel check.", "Route reset clip."),
        ("Great if time", "Big Bend", "viewpoint", "quick stop", "Road-scale scene.", "Cinematic road curve."),
        ("Great if time", "Weeping Wall", "waterfall", "quick stop", "Roadside waterfall texture.", "Short drive-by or pullout clip."),
        ("Great if time", "Tangle Falls", "waterfall", "quick stop", "Easy waterfall stop if traffic and parking feel safe.", "Tight waterfall detail."),
        ("Only if going farther toward Jasper", "Sunwapta Falls", "waterfall", "30-45 min", "Worth it if already pushing farther north.", "Bridge/water movement shot."),
        ("Only if going farther toward Jasper", "Athabasca Falls", "waterfall/canyon", "45 min", "Powerful waterfall and canyon stop.", "Mist and canyon detail."),
    ]
    rows = [[p("Priority", "label"), p("Stop", "label"), p("Type/time", "label"), p("Why + photo idea", "label")]]
    for priority, name, typ, time, why, photo in stops:
        rows.append([p(priority, "micro"), p(name, "small"), p(f"{typ}<br/>{time}", "micro"), p(f"{why}<br/><b>Photo/video:</b> {photo}<br/><b>Offline:</b> save map pin before driving.", "micro")])
    t = Table(rows, colWidths=[1.05 * inch, 1.22 * inch, 1.28 * inch, PAGE_W - 2 * MARGIN - 3.55 * inch], repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), DEEP_GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return [
        p("Canmore -> Jasper / Icefields Parkway stop guide", "h1"),
        p("Ranked stops for the scenic drive. Keep the day realistic and cut stops when weather, fatigue, or bookings demand it."),
        t,
        Spacer(1, 7),
        callout("Offline note", "Download the full Parkway area. Signal and services are limited, and fuel/food options are spaced out.", "warning"),
        PageBreak(),
    ]


def mix_match_story():
    plans = [
        ("Classic first-timer route", "Lake Minnewanka, Banff Gondola, Moraine Lake, Lake Louise, Peyto Lake, Columbia Icefield."),
        ("Calm Banff route", "Canmore base, Lake Minnewanka, early food breaks, gondola, fewer downtown stops."),
        ("Parking-safe route", "Shuttle days for Lake Louise/Moraine Lake, preselected Banff town parking, avoid last-minute downtown loops."),
        ("Icefields Parkway scenic route", "Bow Lake, Peyto Lake, Mistaya Canyon, Columbia Icefield, Big Bend, Tangle Falls if time works."),
        ("Bad-weather backup route", "Protect booked activities, reduce roadside stops, use Canmore/Banff cafes and short viewpoints."),
        ("Content creator route for reels", "Lake Minnewanka for calm Banff clips; Banff Gondola for scale and wide shots; Moraine Lake/Lake Louise for iconic views; Peyto Lake for aerial-style lake view; Icefields Parkway for cinematic driving clips."),
    ]
    flow = [p("Mix-and-match plans", "h1")]
    for title, body in plans:
        bg = GLACIER if "Content creator" not in title else WARM_BEIGE
        t = Table([[p(title, "label")], [p(body, "small")]], colWidths=[PAGE_W - 2 * MARGIN])
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), bg),
                    ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 9),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        flow.extend([t, Spacer(1, 6)])
    flow.extend([nowaitsy_card(short=False), PageBreak()])
    return flow


def mistakes_story(data):
    mistakes = [
        "Do not rely on cell signal on Icefields Parkway.",
        "Do not assume Moraine Lake allows personal vehicle access.",
        "Do not confuse shuttle pickup locations.",
        "Do not overpack Icefields Parkway day.",
        "Do not wait until you are hungry to search for food.",
        "Do not assume Banff downtown parking will be easy.",
        "Do not treat The Crossing as Jasper town.",
        "Do not forget fuel before long scenic drives.",
        "Do not plan flight-day mountain driving unless absolutely necessary.",
    ]
    sources = [
        "Parks Canada - Visiting Lake Louise and Moraine Lake",
        "Town of Banff - Parking",
        "Alberta - Kananaskis Conservation Pass",
        "Banff Jasper Collection - Columbia Icefield Adventure",
        "Alberta 511 road conditions",
        "Reddit community reference - r/Banff Summer FAQ",
    ]
    return [
        p("Mistakes to avoid", "h1"),
        bullets(mistakes),
        callout(
            "NoWaitsy reminder",
            "Before heading to restaurants, cafes, or crowded spots, check NoWaitsy to see if it is worth going right now.",
        ),
        p("Verify-before-trip source list", "h2"),
        bullets(sources, "small"),
        p("Full URLs are saved in guide-content/sources.md for editing and final checks.", "small"),
        PageBreak(),
        p("Save this before your Banff trip", "h1"),
        p("Follow @escapewith.ady on Instagram for more guides, routes, parking notes, and real trip breakdowns."),
        p("Use NoWaitsy before heading to crowded restaurants and cafes."),
        Spacer(1, 30),
        final_cta_box(data),
    ]


def final_cta_box(data):
    w = PAGE_W - 2 * MARGIN
    rows = [
        [p("EscapeWith.Ady", "h2")],
        [p("@escapewith.ady", "label")],
        [p("Real travel routes, parking tips, and Banff guides.", "body")],
        [p("NoWaitsy: check crowded restaurants, cafes, and popular spots before you leave.", "small")],
    ]
    t = Table(rows, colWidths=[w])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WARM_BEIGE),
                ("BOX", (0, 0), (-1, -1), 1.0, BEIGE_DARK),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
            ]
        )
    )
    return t


def build_pdf():
    data = load_data()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frame = Frame(MARGIN, MARGIN + FOOTER_H, PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN - FOOTER_H, id="normal")
    cover_frame = Frame(MARGIN, MARGIN, PAGE_W - 2 * MARGIN, PAGE_H - 2 * MARGIN, id="cover")
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
        title=data["guideTitle"],
        author=data["brand"],
    )
    doc.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[cover_frame], onPage=cover_page),
            PageTemplate(id="normal", frames=[frame], onPage=on_page),
        ]
    )
    story = []
    story.extend(cover_story(data))
    story.extend(intro_story(data))
    story.extend(route_story(data))
    story.extend(planning_sections_story(data))
    story.extend(days_story(data))
    story.extend(cheat_sheet_story())
    story.extend(stop_guide_story())
    story.extend(mix_match_story())
    story.extend(mistakes_story(data))
    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    out = build_pdf()
    print(out)
