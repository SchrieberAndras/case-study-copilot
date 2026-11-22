"""Slide layouts. Each takes (deck, spec) and draws one slide. See references/layouts.md for the spec of each."""
import os, sys
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_MARK
from pptx.oxml.ns import qn
from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
import theme


def _frame(d, spec, **kw):
    s = d.new_slide(bg=spec.get("bg"))
    d.frame(s, spec["title"], kicker=spec.get("kicker"), subtitle=spec.get("subtitle"), source=spec.get("source"),
            tracker=spec.get("_tracker"), active=spec.get("phase"), **kw)
    return s


def _base(spec):
    """Bottom of the content area: case-study-ppt section 5 (y 6.95), less the source line when there is one."""
    return (SOURCE_Y - 0.05) if spec.get("source") else CY1


def _bottom(spec):
    return _base(spec) - 0.8 if spec.get("takeaway") else _base(spec) - 0.05


def _end(d, s, spec):
    if spec.get("takeaway"):
        d.takeaway(s, spec["takeaway"], y=_base(spec) - 0.67, icon=spec.get("takeaway_icon", "lightbulb"))
    return s


def _text_on(d, fill):
    return "ON_PRIMARY" if fill == "PRIMARY" else ("INK" if theme.contrast(d.pal.get(fill, fill), "FFFFFF") < 4.5 else "WHITE")


# ------------------------------------------------------------------ title
def title(d, spec):
    s = d.new_slide(bg="WHITE")
    d.rect(s, 8.55, 0, W - 8.55, H, fill="PRIMARY", name="cover-panel")
    d.rect(s, 8.55, 0, 0.12, H, fill="PRIMARY_DARK", name="cover-edge")
    ic = spec.get("icon")
    if ic:
        d.icon(s, ic, 8.55 + (W - 8.55 - 3.4) / 2 + 0.05, 2.05, 3.4, color=d.pal["ON_PRIMARY"], opacity=0.28, stroke=1.2)
    if d.logo:
        from PIL import Image
        iw, ih = Image.open(d.logo).size; sc = min(2.4 / iw, 0.8 / ih)
        d.picture(s, d.logo, MX, 0.6, iw * sc, ih * sc, name="logo")
    if spec.get("kicker"):
        d.text(s, MX + 0.35, 2.05, 7.4, 0.3, spec["kicker"], size=16, color="PRIMARY", bold=True, upper=True)
    size, ok = d.fit(spec["title"], 7.4, 2.2, 44, 30, head=True, spacing=1.2)
    nl = len(d.wrap(spec["title"], size, 7.2, head=True))
    th = nl * size * 1.2 / 72
    ty = 4.85 - th
    d.rect(s, MX, ty + 0.05, 0.1, th - 0.05, fill="PRIMARY", name="title-bar")
    d.text(s, MX + 0.35, ty, 7.2, th + 0.05, spec["title"], size=size, color="INK", head=True, valign="b", name="title")
    if spec.get("subtitle"):
        d.text(s, MX + 0.35, 5.05, 7.2, 0.9, spec["subtitle"], size=19, color="GREY", italic=True, min_size=16)
    meta = spec.get("meta") or []
    if meta:
        d.text(s, MX + 0.35, 6.3, 7.2, 0.8, meta, size=16, color="INK", name="meta")
    return s


# ------------------------------------------------------------------ section divider
def section(d, spec):
    s = d.new_slide(bg="PRIMARY_DARK")
    on = d.pal["ON_DARK"]
    cx = W / 2
    if spec.get("icon"):
        d.oval(s, cx - 1.45, 1.1, 2.9, 2.9, fill="PRIMARY")
        d.icon(s, spec["icon"], cx - 0.8, 1.75, 1.6, color=d.pal["ON_PRIMARY"], stroke=1.5)
    if spec.get("number"):
        d.text(s, 0, 4.15, W, 0.4, str(spec["number"]), size=16, color="MID", bold=True, align="c", upper=True)
    size, _ = d.fit(spec["title"], 11, 1.0, 46, 32, head=True)
    d.text(s, 1.1, 4.5, W - 2.2, 1.0, spec["title"], size=size, color=on, head=True, align="c", name="title")
    if spec.get("subtitle"):
        d.text(s, 1.6, 5.6, W - 3.2, 0.8, spec["subtitle"], size=20, color="TINT" if on == "FFFFFF" else "INK", italic=True, align="c", min_size=16)
    d.page_number(s, color="MID")
    return s


# ------------------------------------------------------------------ one big number
def big_number(d, spec):
    s = d.new_slide(bg=spec.get("bg", "WHITE"))
    if spec.get("kicker"):
        d.text(s, 0, 1.2, W, 0.35, spec["kicker"], size=16, color="PRIMARY", bold=True, align="c", upper=True)
    size, _ = d.fit(spec["number"], 11, 2.2, 140, 60, head=True, bold=True)
    d.text(s, 0, 1.75, W, 2.4, spec["number"], size=size, color="PRIMARY", head=True, bold=True, align="c", valign="m", name="number")
    d.rect(s, W / 2 - 0.5, 4.35, 1.0, 0.05, fill="PRIMARY")
    d.text(s, 1.9, 4.65, W - 3.8, 1.5, spec["text"], size=26, color="INK", align="c", min_size=18, name="statement")
    if spec.get("source"):
        d.text(s, MX, SOURCE_Y, 11.0, 0.25, "Source: " + spec["source"], size=10, color="GREY", name="source")
    d.page_number(s)
    return s


# ------------------------------------------------------------------ KPI tiles
def kpis(d, spec):
    s = _frame(d, spec)
    tiles = spec["tiles"]; n = len(tiles)
    gap = 0.3; w = (CX1 - CX0 - gap * (n - 1)) / n
    top, bot = CY0 + 0.2, _bottom(spec) - 0.1
    for i, t in enumerate(tiles):
        x = CX0 + i * (w + gap)
        d.rect(s, x, top, w, bot - top, fill="TINT", radius=0.12, name=f"tile-{i+1}")
        if t.get("icon"):
            d.icon_badge(s, t["icon"], x + 0.62, top + 0.7, 0.8)
        vy = top + 1.35
        vs, _ = d.fit(t["value"], w - 0.5, 0.9, 44, 28, head=True, bold=True)
        d.text(s, x + 0.3, vy, w - 0.6, 0.95, t["value"], size=vs, color="PRIMARY", head=True, bold=True, valign="m", name=f"value-{i+1}")
        d.text(s, x + 0.3, vy + 1.0, w - 0.6, 0.7, t["label"], size=17, color="INK", bold=True, min_size=16, name=f"label-{i+1}")
        if t.get("note"):
            d.text(s, x + 0.3, vy + 1.75, w - 0.6, bot - (vy + 1.75) - 0.15, t["note"], size=16, color="GREY", min_size=16)
    return _end(d, s, spec)


# ------------------------------------------------------------------ executive summary (question -> answer rows)
EXEC_ICONS = {"challenge": "circle-help", "strategy": "compass", "solution": "puzzle", "impacts": "trending-up", "impact": "trending-up"}


def exec_summary(d, spec):
    s = _frame(d, spec)
    rows = spec["rows"]; n = len(rows)
    top, bot = CY0 + 0.1, _bottom(spec) - 0.05
    gap = 0.16
    # row heights: rows with `items` are taller
    weights = [1.25 if r.get("items") else 1.0 for r in rows]
    unit = (bot - top - gap * (n - 1)) / sum(weights)
    lx, lw_, cx = CX0, 2.7, CX0 + 3.0
    x0 = cx + 0.35; wcont = CX1 - x0
    y = top; centers = []
    for r, wt in zip(rows, weights):
        h = unit * wt
        centers.append(y + h / 2)
        ic = r.get("icon") or EXEC_ICONS.get(r["label"].strip().lower())
        if ic:   # case-study-ppt section 2: icon + label left (Challenge, Strategy, Solution, Impacts)
            d.icon(s, ic, lx, y + (h - 0.45) / 2, 0.45, color="PRIMARY")
            d.text(s, lx + 0.6, y, lw_ - 0.6, h, r["label"], size=18, color="PRIMARY", head=True, align="l", valign="m", min_size=16, name="row-label")
        else:
            d.text(s, lx, y, lw_, h, r["label"], size=18, color="PRIMARY", head=True, align="r", valign="m", min_size=16, name="row-label")
        if r.get("items"):
            k = len(r["items"]); g = 0.12; bw = (wcont - g * (k - 1)) / k
            for j, it in enumerate(r["items"]):
                cobe = r["label"].strip().lower() in EXEC_ICONS      # case-study-ppt: pillars in neutral boxes, dark text
                b = d.rect(s, x0 + j * (bw + g), y, bw, h, fill="NEUTRAL" if cobe else "PRIMARY", radius=0.06, name=f"item-{j+1}")
                d.box_text(s, b, it, size=19, color="INK" if cobe else "ON_PRIMARY", bold=True, min_size=16, head=True)
        else:
            fill = "TINT"
            b = d.rect(s, x0, y, wcont, h, fill=fill, radius=0.06, name="row-box")
            d.text(s, x0 + 0.25, y, wcont - 0.5, h, r["text"], size=18, color="INK", valign="m", min_size=16)
        y += h + gap
    d.line(s, cx, centers[0], cx, centers[-1], color="PRIMARY", lw=1.5)
    for c in centers:
        d.rect(s, cx - 0.07, c - 0.07, 0.14, 0.14, fill="PRIMARY")
    return _end(d, s, spec)


# ------------------------------------------------------------------ 2-4 columns (icon + heading + bullets or value)
def columns(d, spec):
    s = _frame(d, spec)
    cols = spec["columns"]; n = len(cols)
    top = CY0 + 0.1
    if spec.get("question"):
        b = d.rect(s, CX0, top, CX1 - CX0, 0.7, fill="PRIMARY", radius=0.08, name="question")
        d.box_text(s, b, spec["question"], size=19, color="ON_PRIMARY", bold=True, min_size=16, head=False, margin=0.25)
        top += 0.9
    bot = _bottom(spec) - 0.1
    gap = 0.28; w = (CX1 - CX0 - gap * (n - 1)) / n
    # size cards to their content (centred in the free area) so few bullets do not leave empty boxes
    need = 0
    for c in cols:
        h_ = 1.0 + (1.0 if c.get("value") else 0) + (0.75 if c.get("label") else 0)
        if c.get("bullets"):
            h_ += sum(len(d.wrap(b, 20, w - 0.9 - 0.22)) for b in c["bullets"]) * 20 * 1.2 / 72 + 10 * len(c["bullets"]) / 72
        need = max(need, h_ + 0.35)
    avail = bot - top
    if need < avail - 0.3:
        ch_ = max(need, 3.0)
        top += (avail - ch_) / 2 if not spec.get("question") else 0
        bot = top + ch_
    for i, c in enumerate(cols):
        x = CX0 + i * (w + gap)
        d.rect(s, x, top, w, bot - top, fill="TINT", radius=0.1, name=f"card-{i+1}")
        hy = top + 0.25
        if c.get("icon"):
            d.icon_badge(s, c["icon"], x + 0.25 + 0.3, hy + 0.3, 0.6)
            tx = x + 1.05
        else:
            tx = x + 0.3
        d.text(s, tx, hy, x + w - tx - 0.2, 0.6, c["heading"], size=18, color="INK", head=True, valign="m", min_size=16, name=f"heading-{i+1}")
        d.line(s, x + 0.3, hy + 0.85, x + w - 0.3, hy + 0.85, color="LINE", lw=1)
        by = hy + 1.0
        if c.get("value"):
            vs, _ = d.fit(c["value"], w - 0.6, 0.9, 44, 28, head=True, bold=True)
            d.text(s, x + 0.3, by, w - 0.6, 0.95, c["value"], size=vs, color="PRIMARY", head=True, bold=True, valign="m")
            by += 1.0
        if c.get("label"):
            d.text(s, x + 0.3, by, w - 0.6, 0.7, c["label"], size=18, color="INK", bold=True, min_size=16)
            by += 0.75
        if c.get("bullets"):
            d.text(s, x + 0.3, by, w - 0.6, bot - by - 0.2, c["bullets"], size=20, color="INK", bullets=True,
                   min_size=16, space_after=10, name=f"bullets-{i+1}")
    return _end(d, s, spec)


# ------------------------------------------------------------------ native chart + callouts
def _style_axis(d, chart, labels_pt=14):
    ca = chart.category_axis
    ca.has_major_gridlines = False
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.format.line.color.rgb = rgb(d.pal["GREY"])
    ca.tick_labels.font.size = Pt(labels_pt); ca.tick_labels.font.name = d.fonts["body"]
    ca.tick_labels.font.color.rgb = rgb(d.pal["INK"])
    va = chart.value_axis
    va.visible = False; va.has_major_gridlines = False; va.has_minor_gridlines = False


def add_chart(d, s, ch, x, y, w, h):
    t = ch.get("type", "column")
    cd = CategoryChartData()
    cd.categories = ch["categories"]
    for ser in ch["series"]:
        cd.add_series(ser["name"], ser["values"])
    kind = {"column": XL_CHART_TYPE.COLUMN_CLUSTERED, "stacked": XL_CHART_TYPE.COLUMN_STACKED,
            "bar": XL_CHART_TYPE.BAR_CLUSTERED, "line": XL_CHART_TYPE.LINE_MARKERS,
            "donut": XL_CHART_TYPE.DOUGHNUT, "stacked100": XL_CHART_TYPE.COLUMN_STACKED_100}[t]
    gf = s.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    gf.name = "chart"
    chart = gf.chart
    chart.has_title = False
    chart.font.name = d.fonts["body"]; chart.font.size = Pt(14)
    fmt = ch.get("number_format", "General")
    multi = len(ch["series"]) > 1
    palette = [d.pal["PRIMARY"], d.pal["NEUTRAL"], d.pal["MID"], d.pal["NEUTRAL_DARK"], d.pal["PRIMARY_DARK"]]   # case-study-ppt visuals.md 4: one highlight, rest NEUTRAL, MID for a second level
    plot = chart.plots[0]
    if t == "donut":
        chart.has_legend = True; chart.legend.position = XL_LEGEND_POSITION.BOTTOM; chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(14)
        hole = plot._element.find(qn("c:holeSize"))
        if hole is None:
            hole = etree.SubElement(plot._element, qn("c:holeSize"))
        hole.set("val", "62")
        ser = plot.series[0]
        for i in range(len(ch["categories"])):
            pt = ser.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(palette[i % len(palette)])
            pt.format.line.color.rgb = rgb("FFFFFF")
        plot.has_data_labels = True
        dl = plot.data_labels; dl.number_format = fmt; dl.number_format_is_linked = False
        dl.font.size = Pt(14); dl.font.bold = True
        dl.font.color.rgb = rgb(d.pal["ON_PRIMARY"]); dl.show_value = True
        return gf
    _style_axis(d, chart)
    if t == "bar":
        chart.category_axis.reverse_order = True          # first category on top, as written
    if t in ("column", "bar", "stacked", "stacked100"):
        plot.gap_width = ch.get("gap", 60)
        if t.startswith("stacked"):
            plot.overlap = 100
    chart.has_legend = multi and ch.get("legend", True)
    if chart.has_legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM; chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(14)
    hl = ch.get("highlight")
    for si, ser in enumerate(plot.series):
        col = palette[si % len(palette)]
        if t == "line":
            ser.format.line.color.rgb = rgb(col); ser.format.line.width = Pt(3); ser.smooth = False
            ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = rgb(col)
            ser.marker.format.line.color.rgb = rgb(col); ser.marker.size = 8
        else:
            ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(col)
            ser.invert_if_negative = False
            if not multi and hl is not None:
                vals = ch["series"][0]["values"]
                idx = {"last": [len(vals) - 1], "max": [vals.index(max(vals))], "first": [0]}.get(hl, hl) if not isinstance(hl, list) else hl
                for pi in range(len(vals)):
                    pt = ser.points[pi]; pt.format.fill.solid()
                    pt.format.fill.fore_color.rgb = rgb(d.pal["PRIMARY"] if pi in idx else d.pal["NEUTRAL"])
        dl = ser.data_labels
        dl.show_value = True; dl.number_format = fmt; dl.number_format_is_linked = False
        dl.font.size = Pt(14); dl.font.bold = True; dl.font.name = d.fonts["body"]
        if t.startswith("stacked"):
            dl.position = XL_LABEL_POSITION.CENTER
            dl.font.color.rgb = rgb("FFFFFF" if si == 0 and d.pal["ON_PRIMARY"] == "FFFFFF" else d.pal["INK"])
        elif t == "line":
            dl.position = XL_LABEL_POSITION.ABOVE; dl.font.color.rgb = rgb(d.pal["INK"])
        else:
            dl.position = XL_LABEL_POSITION.OUTSIDE_END; dl.font.color.rgb = rgb(d.pal["INK"])
    return gf


def chart(d, spec):
    s = _frame(d, spec)
    top, bot = CY0 + 0.1, _bottom(spec) - 0.1
    callouts = spec.get("callouts") or []
    cw = (CX1 - CX0) * (0.62 if callouts else 1.0)
    if spec.get("chart_title"):
        d.text(s, CX0, top, cw, 0.4, spec["chart_title"], size=16, color="GREY", bold=True, name="chart-title")
        top += 0.42
    c = spec["chart"]
    gf = add_chart(d, s, c, CX0, top, cw, bot - top - (0.3 if (spec.get("footnote") or c.get("footnote")) else 0))
    if c.get("type") == "donut" and spec.get("center_label"):
        cl = spec["center_label"]
        cxm = CX0 + cw / 2; cym = top + (bot - top - 0.5) / 2
        d.text(s, cxm - 1.2, cym - 0.6, 2.4, 0.7, cl["value"], size=34, color="PRIMARY", head=True, bold=True, align="c", valign="m")
        d.text(s, cxm - 1.2, cym + 0.05, 2.4, 0.5, cl["label"], size=14, color="GREY", align="c", name="chart-label")
    fn = spec.get("footnote") or c.get("footnote")
    if fn:
        d.text(s, CX0, bot - 0.05, cw, 0.3, fn, size=14, color="GREY", italic=True, name="footnote")
    if callouts:
        px = CX0 + cw + 0.4; pw = CX1 - px
        d.rect(s, px, top, pw, bot - top, fill="TINT", radius=0.12, name="callout-panel")
        k = len(callouts); h = (bot - top - 0.3) / k
        for i, co in enumerate(callouts):
            y = top + 0.15 + i * h
            vs, _ = d.fit(co["value"], pw - 0.6, 0.8, 38, 24, head=True, bold=True)
            d.text(s, px + 0.3, y, pw - 0.6, h * 0.5, co["value"], size=vs, color="PRIMARY", head=True, bold=True, valign="b", name=f"callout-value-{i+1}")
            d.text(s, px + 0.3, y + h * 0.5 + 0.03, pw - 0.6, h * 0.5 - 0.1, co["label"], size=16, color="INK", min_size=16, name=f"callout-label-{i+1}")
            if i < k - 1:
                d.line(s, px + 0.3, y + h - 0.02, px + pw - 0.3, y + h - 0.02, color="LINE", lw=0.75)
    return _end(d, s, spec)


# ------------------------------------------------------------------ roadmap (phases with chevrons)
def roadmap(d, spec):
    s = _frame(d, spec)
    ph = spec["phases"]; n = len(ph)
    gap = 0.0; w = (CX1 - CX0) / n
    top = CY0 + 0.15; ch_h = 0.85
    shades = ["PRIMARY_DARK", "PRIMARY", "PRIMARY", "PRIMARY"]
    for i, p in enumerate(ph):
        fill = shades[min(i, 3)] if n <= 4 else shades[min(i, 3)]
        x = CX0 + i * w
        kind = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        shp = d.shape(s, kind, x, top, w + (0.25 if i < n - 1 else 0), ch_h, fill=fill, name=f"phase-chevron-{i+1}")
        shp.adjustments[0] = 0.28
        shp.line.color.rgb = rgb("FFFFFF"); shp.line.width = Pt(3)
        col = _text_on(d, fill)
        d.oval(s, x + (0.25 if i else 0.2), top + 0.2, 0.45, 0.45, fill="WHITE")
        d.text(s, x + (0.25 if i else 0.2), top + 0.2, 0.45, 0.45, str(i + 1), size=16, color="PRIMARY_DARK", head=True, bold=True, align="c", valign="m")
        d.text(s, x + (0.85 if i else 0.8), top, w - 1.1, ch_h, p["name"], size=17, color=col, head=True, valign="m", min_size=16, name=f"phase-name-{i+1}")
        if p.get("dates"):
            d.text(s, x + 0.2, top + ch_h + 0.1, w - 0.4, 0.35, p["dates"], size=16, color="PRIMARY", bold=True, name=f"phase-dates-{i+1}")
        iy = top + ch_h + (0.6 if p.get("dates") else 0.25)
        items = p.get("items", [])
        avail = _bottom(spec) - 0.1 - iy - (0.95 if p.get("milestone") else 0)
        rh = min(0.78, avail / max(1, len(items)))
        for j, it in enumerate(items):
            txt = it if isinstance(it, str) else it["text"]
            ic = None if isinstance(it, str) else it.get("icon")
            ry = iy + j * rh
            if ic:
                d.icon(s, ic, x + 0.2, ry + (rh - 0.38) / 2, 0.38)
            d.text(s, x + (0.75 if ic else 0.2), ry, w - (1.0 if ic else 0.45), rh, txt, size=16, color="INK", valign="m", min_size=16, name=f"phase-item-{i+1}-{j+1}")
        if p.get("milestone"):
            my = _bottom(spec) - 0.1 - 0.8
            b = d.rect(s, x + 0.2, my, w - 0.45, 0.8, fill="TINT", radius=0.08, name=f"milestone-{i+1}")
            d.icon(s, "flag", x + 0.35, my + 0.25, 0.3)
            d.text(s, x + 0.75, my, w - 1.15, 0.8, p["milestone"], size=16, color="INK", bold=True, valign="m", min_size=16)
        if i < n - 1:
            d.line(s, x + w + 0.05, iy - 0.05, x + w + 0.05, _bottom(spec) - 0.1, color="LINE", lw=1, dash=True)
    return _end(d, s, spec)


# ------------------------------------------------------------------ comparison matrix (Harvey balls / ticks / text)
def comparison(d, spec):
    s = _frame(d, spec)
    cols = spec["columns"]; rows = spec["rows"]
    n = len(cols)
    top = CY0 + 0.15; bot = _bottom(spec) - (0.35 if spec.get("legend_harvey") else 0.05)
    lw_ = spec.get("label_width", 2.9)
    cw = (CX1 - CX0 - lw_) / n
    hh = 0.7
    rh = (bot - top - hh) / len(rows)
    hc = spec.get("highlight")
    for hci in ([] if hc is None else (hc if isinstance(hc, list) else [hc])):
        d.rect(s, CX0 + lw_ + hci * cw + 0.04, top, cw - 0.08, bot - top + 0.02, fill="TINT", line="PRIMARY", lw=1.5, dash=True, radius=0.06, name="highlight")
    hr_ = spec.get("highlight_row")
    if hr_ is not None:
        d.rect(s, CX0 - 0.05, top + hh + hr_ * rh + 0.03, CX1 - CX0 + 0.1, rh - 0.06, fill="TINT", line="PRIMARY", lw=1.5, dash=True, radius=0.06, name="highlight-row")
    for j, c in enumerate(cols):
        d.text(s, CX0 + lw_ + j * cw, top, cw, hh, c, size=16, color="PRIMARY", head=True, align="c", valign="m", min_size=16, name=f"col-head-{j+1}")
    for i, r in enumerate(rows):
        y = top + hh + i * rh
        d.line(s, CX0, y, CX1, y, color="LINE", lw=0.75)
        d.text(s, CX0 + 0.05, y, lw_ - 0.1, rh, r["label"], size=16, color="INK", bold=True, valign="m", min_size=16, name=f"row-label-{i+1}")
        for j, v in enumerate(r["cells"]):
            cx = CX0 + lw_ + j * cw + cw / 2; cy = y + rh / 2
            if isinstance(v, dict):                       # {"text": "High", "tone": "good|mid|bad"}
                tone = v.get("tone", "mid"); txt = v["text"]
                pw_ = min(cw - 0.3, d.text_width(txt, 14, bold=True) + 0.45); ph_ = 0.4
                fill, line, tcol = {"good": ("PRIMARY", None, "ON_PRIMARY"), "mid": ("SOFT", None, "INK"), "bad": ("WHITE", "GREY", "GREY")}[tone]
                d.rect(s, cx - pw_ / 2, cy - ph_ / 2, pw_, ph_, fill=fill, line=line, lw=1.25, radius=ph_ / 2, name="pill")
                d.text(s, cx - pw_ / 2, cy - ph_ / 2, pw_, ph_, txt, size=16, color=tcol, bold=True, align="c", valign="m")
            elif isinstance(v, (int, float)) and not isinstance(v, bool):
                d.harvey(s, cx, cy, min(0.42, rh * 0.6), int(v))
            elif str(v).lower() in ("yes", "check", "true"):
                d.icon(s, "check", cx - 0.2, cy - 0.2, 0.4, color="PRIMARY", stroke=2.4)
            elif str(v).lower() in ("no", "cross", "false"):
                d.icon(s, "x", cx - 0.2, cy - 0.2, 0.4, color="GREY", stroke=2.4)
            elif str(v).lower() == "partial":
                d.icon(s, "minus", cx - 0.2, cy - 0.2, 0.4, color="MID", stroke=2.4)
            else:
                d.text(s, cx - cw / 2 + 0.08, y, cw - 0.16, rh, str(v), size=16, color="INK", align="c", valign="m", min_size=16)
    d.line(s, CX0, top + hh + len(rows) * rh, CX1, top + hh + len(rows) * rh, color="LINE", lw=0.75)
    if spec.get("legend_harvey"):
        d.text(s, CX0, bot + 0.07, 8, 0.25, spec["legend_harvey"], size=14, color="GREY", name="legend")
    return _end(d, s, spec)


# ------------------------------------------------------------------ 2x2 matrix
def matrix(d, spec):
    s = _frame(d, spec)
    top, bot = CY0 + 0.1, _bottom(spec) - 0.6
    left = CX0 + 0.9; right = CX1
    q = spec["quadrants"]            # order: top-left, top-right, bottom-left, bottom-right
    gap = 0.14
    qw = (right - left - gap) / 2; qh = (bot - top - gap) / 2
    hi = spec.get("highlight")
    for i, qd in enumerate(q):
        x = left + (i % 2) * (qw + gap); y = top + (i // 2) * (qh + gap)
        on = (hi == i)
        d.rect(s, x, y, qw, qh, fill="PRIMARY" if on else "TINT", radius=0.08, name=f"quadrant-{i+1}")
        c1 = "ON_PRIMARY" if on else "PRIMARY"; c2 = "ON_PRIMARY" if on else "INK"
        d.text(s, x + 0.25, y + 0.15, qw - 0.5, 0.45, qd["title"], size=17, color=c1, head=True, min_size=16, name=f"quadrant-title-{i+1}")
        if qd.get("text") and not spec.get("dots"):
            d.text(s, x + 0.25, y + 0.62, qw - 0.5, qh - 0.75, qd["text"], size=16, color=c2, min_size=16, name=f"quadrant-text-{i+1}")
    for dot in spec.get("dots", []):
        px = left + dot["x"] * (right - left); py = bot - dot["y"] * (bot - top)
        on = dot.get("highlight")
        d.oval(s, px - 0.17, py - 0.17, 0.34, 0.34, fill="PRIMARY_DARK" if on else "MID", line="WHITE", lw=2)
        lw2 = d.text_width(dot["label"], 13, bold=True) + 0.24
        d.rect(s, px + 0.24, py - 0.17, lw2, 0.34, fill="WHITE", line="LINE", lw=0.75, radius=0.17, name="dot-label-bg")
        d.text(s, px + 0.24, py - 0.17, lw2, 0.34, dot["label"], size=14, color="INK", bold=True, align="c", valign="m", name="chart-label")
    ya, xa = spec.get("y_axis", {}), spec.get("x_axis", {})
    d.line(s, left - 0.25, bot, left - 0.25, top, color="GREY", lw=1.5, arrow=True)
    d.line(s, left, bot + 0.2, right, bot + 0.2, color="GREY", lw=1.5, arrow=True)
    if xa.get("label"):
        d.text(s, left, bot + 0.24, right - left, 0.3, xa["label"], size=14, color="GREY", bold=True, align="c", name="axis-label")
    if ya.get("label"):
        tb = d.text(s, CX0 - 1.55, (top + bot) / 2 - 0.15, 3.6, 0.3, ya["label"], size=14, color="GREY", bold=True, align="c", name="axis-label")
        tb.rotation = -90
    return _end(d, s, spec)


# ------------------------------------------------------------------ cascade (question -> focus -> strategy -> impact)
def cascade(d, spec):
    s = _frame(d, spec)
    levels = spec["levels"]; n = len(levels)
    top, bot = CY0 + 0.1, _bottom(spec) - 0.05
    gap = 0.42
    lab_w = 0.55
    hs = [lv.get("height", 1.0) for lv in levels]
    unit = (bot - top - gap * (n - 1)) / sum(hs)
    x0 = CX0 + lab_w + 0.15; wt = CX1 - x0
    y = top; geom = []
    styles = {"PRIMARY": ("PRIMARY", None), "TINT": ("TINT", None), "OUTLINE": (None, "PRIMARY")}
    for li, lv in enumerate(levels):
        h = unit * hs[li]
        tag = lv["label"].upper()
        tsz = max(8, min(11, 11 * (h - 0.1) / max(0.01, d.text_width(tag, 11, bold=True))))
        tw_ = max(h, d.text_width(tag, tsz, bold=True) + 0.1)
        d_lab = d.text(s, CX0 + lab_w / 2 - tw_ / 2, y + h / 2 - 0.2, tw_, 0.4, tag, size=round(tsz, 1), color="GREY", bold=True, align="c", valign="m", name="row-tag")
        d_lab.rotation = -90
        k = len(lv["boxes"]); g = 0.2; bw = (wt - g * (k - 1)) / k
        row = []
        for j, bx in enumerate(lv["boxes"]):
            span = bx.get("span", 1)
            x = x0 + j * (bw + g)
            style = lv.get("style", "TINT")
            fill, line = styles[style]
            b = d.rect(s, x, y, bw, h, fill=fill, line=line, lw=1.5, radius=0.08, name=f"cascade-{li+1}-{j+1}")
            col = "ON_PRIMARY" if style == "PRIMARY" else "INK"
            ix = x + 0.2
            if bx.get("icon"):
                d.icon(s, bx["icon"], x + 0.2, y + (h - 0.5) / 2, 0.5, color="ON_PRIMARY" if style == "PRIMARY" else "PRIMARY")
                ix = x + 0.85
            has_text = bx.get("text")
            if has_text:
                d.text(s, ix, y + 0.05, bw - (ix - x) - 0.15, h * 0.42, bx["title"], size=16, color=col, head=True, valign="b", min_size=16)
                d.text(s, ix, y + h * 0.47, bw - (ix - x) - 0.15, h * 0.5, bx["text"], size=16, color=col, min_size=16)
            else:
                d.text(s, ix, y, bw - (ix - x) - 0.15, h, bx["title"], size=16, color=col, head=True, valign="m", align="c" if not bx.get("icon") else "l", min_size=16)
            row.append((x + bw / 2, y, h))
        geom.append(row)
        y += h + gap
    for li in range(n - 1):
        for (cx, yy, hh) in geom[li]:
            d.shape(s, MSO_SHAPE.DOWN_ARROW, cx - 0.14, yy + hh + 0.06, 0.28, gap - 0.12, fill="PRIMARY")
    return _end(d, s, spec)


# ------------------------------------------------------------------ process (numbered steps with icons)
def process(d, spec):
    s = _frame(d, spec)
    steps = spec["steps"]; n = len(steps)
    top, bot = CY0 + 0.25, _bottom(spec) - 0.1
    w = (CX1 - CX0) / n
    ly = top + max(0.55, ((bot - top) - 3.2) / 2 + 0.55)
    d.line(s, CX0 + w / 2, ly, CX1 - w / 2, ly, color="PRIMARY", lw=2, arrow=False)
    for i, st in enumerate(steps):
        cx = CX0 + i * w + w / 2
        if st.get("icon"):
            d.icon_badge(s, st["icon"], cx, ly, 1.05, fill="PRIMARY")
        else:
            d.oval(s, cx - 0.5, ly - 0.5, 1.0, 1.0, fill="PRIMARY")
        d.oval(s, cx + 0.3, ly - 0.72, 0.4, 0.4, fill="WHITE", line="PRIMARY", lw=1.5)
        d.text(s, cx + 0.3, ly - 0.72, 0.4, 0.4, str(i + 1), size=16, color="PRIMARY", head=True, bold=True, align="c", valign="m")
        d.text(s, cx - w / 2 + 0.15, ly + 0.75, w - 0.3, 0.7, st["title"], size=18, color="INK", head=True, align="c", valign="t", min_size=16, name=f"step-title-{i+1}")
        if st.get("text"):
            d.text(s, cx - w / 2 + 0.2, ly + 1.5, w - 0.4, bot - (ly + 1.5), st["text"], size=16, color="INK", align="c", min_size=16, name=f"step-text-{i+1}")
    return _end(d, s, spec)


def pairs(d, spec):
    """Rows of left item -> right item (risk -> mitigation, problem -> solution, today -> target)."""
    s = _frame(d, spec)
    rows = spec["rows"]; n = len(rows)
    top, bot = CY0 + 0.35 if spec.get("headers") else CY0 + 0.1, _bottom(spec) - 0.1
    gap = 0.2; arrow_w = 0.55
    lw_ = (CX1 - CX0 - arrow_w) * 0.42; rw = (CX1 - CX0 - arrow_w) - lw_
    if spec.get("headers"):
        hl, hr = spec["headers"]
        d.text(s, CX0, CY0, lw_, 0.32, hl, size=16, color="GREY", bold=True, upper=True)
        d.text(s, CX0 + lw_ + arrow_w, CY0, rw, 0.32, hr, size=16, color="GREY", bold=True, upper=True)
    rh = min(1.25, (bot - top - gap * (n - 1)) / n)
    y0 = top + (bot - top - (rh * n + gap * (n - 1))) / 2 if n <= 3 else top
    for i, r in enumerate(rows):
        y = y0 + i * (rh + gap)
        left = d.rect(s, CX0, y, lw_, rh, fill="TINT", radius=0.1, name=f"left-{i+1}")
        tx = CX0 + 0.25
        if r.get("icon"):
            d.icon_badge(s, r["icon"], CX0 + 0.25 + 0.3, y + rh / 2, 0.6); tx = CX0 + 1.05
        d.text(s, tx, y, CX0 + lw_ - tx - 0.15, rh, r["left"], size=19, color="INK", head=True, valign="m", min_size=16)
        d.shape(s, MSO_SHAPE.RIGHT_ARROW, CX0 + lw_ + 0.08, y + rh / 2 - 0.17, arrow_w - 0.16, 0.34, fill="PRIMARY")
        b = d.rect(s, CX0 + lw_ + arrow_w, y, rw, rh, fill="PRIMARY", radius=0.1, name=f"right-{i+1}")
        d.text(s, CX0 + lw_ + arrow_w + 0.25, y, rw - 0.5, rh, r["right"], size=19, color="ON_PRIMARY", valign="m", min_size=16)
    return _end(d, s, spec)


LAYOUTS = {k: v for k, v in dict(title=title, section=section, big_number=big_number, kpis=kpis,
                                 exec_summary=exec_summary, columns=columns, chart=chart, roadmap=roadmap,
                                 comparison=comparison, matrix=matrix, cascade=cascade, process=process, pairs=pairs).items()}
