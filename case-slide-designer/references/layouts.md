# Layout reference

Spec file shape:

```json
{"primary": "E51636", "logo": "media/logo.png", "fonts": "premium",
 "tracker": ["Analysis", "Strategy", "Recommendation", "Feasibility"],
 "slides": [ {"layout": "kpis", "title": "...", "kicker": "...", ...}, ... ]}
```

Keys every content layout accepts (all but `title`, `section`, `big_number`):
`subtitle` (optional 20pt line under the title; `kicker` is accepted as an alias), `title` (action title, required), `source` (bottom-left line, "Source: " is added),
`takeaway` (one-line banner at the bottom; shrinks the content area), `takeaway_icon` (icon name, default `lightbulb`),
`phase` (0-based index into `tracker`; draws the progress tracker with that phase active).

Text supports `**bold**` anywhere. Icon values are icon names (`rocket`) or free text (`growth chart`); look names up with `python scripts/icons.py <words>` and confirm in the render.

Word budget: aim for 25-40 words on a content slide (60 on the executive summary and closing slide); check_deck prints the count as a note; it is a guide, not a rule. Body text never goes below 16pt: if a box overflows at 16pt the builder warns, so cut words or split the slide. Boxes hold a heading plus one short phrase or 2-3 bullets of about 8 words.

---

## title
`title`, `subtitle`, `kicker`, `meta` (list of lines: team, date), `icon` (large faint icon on the colour panel). Logo from the deck logo goes top-left. House style only: COBE title slides follow case-study-ppt section 2a.

## section
Dark full-bleed divider. `title`, `subtitle`, `number` (e.g. "Part 2"), `icon` (white icon in a circle).

## big_number
One statistic. `number` ("97%"), `text` (the sentence under it; `**bold**` the key phrase), `kicker`, `source`.

## kpis
2-4 tiles. `tiles`: `[{"icon", "value", "label", "note"}]`. Keep `value` short (`$4.2M`, `137%`, `1,500`). 

## exec_summary
Question-and-answer rows joined by a vertical line. `rows`: `[{"label": "What is the goal?", "text": "..."}]` or `{"label", "items": ["Unlocked","Evolved","Connected"]}` for a row of filled tiles. 3-5 rows; at most one `items` row per slide to keep it readable. COBE decks use the case-study-ppt section 2 layout: four rows labelled `Challenge`, `Strategy`, `Solution`, `Impacts`; those labels get their icon automatically (left of the label), or pass `"icon"` per row. Content per case-study-ppt: the challenge as a one-line question, the bold "We recommend ..." sentence, 2-4 pillars as `items` (neutral boxes with dark text under these labels), and the 3 big impact numbers (24-28pt bold) with short labels; this layout writes the Impacts row as text, so for the big-number row build that slide in deck-native mode or let case-study-ppt build it.

## columns
2-4 cards. Optional `question` (filled banner above the cards). `columns`: `[{"icon", "heading", "bullets": [..]}]`, or with a number: `{"icon", "heading", "value": "75%", "label": "of growth"}`. Bullets and value can combine.

## chart
`chart`: `{"type": "column|stacked|stacked100|bar|line|donut", "categories": [...], "series": [{"name", "values": [...]}], "number_format": "0\"%\"", "highlight": "last|max|first|[indices]", "legend": true}`.
Single series: use `highlight` to colour the bars that carry the message. Multi series: first series is the accent colour.
Optional `chart_title` (small grey label above, put the unit here), `callouts`: `[{"value": "~105", "label": "restaurants in Canada and the UK"}]` (1-3, in a tinted panel on the right; omit for a full-width chart), `center_label` (`{"value","label"}` inside a donut).
Number formats: `0`, `0.0`, `#,##0`, `0"%"` (values already in percent), `0%` (values as fractions), `"$"#,##0.0"M"`.

## roadmap
3-4 phases as chevrons. `phases`: `[{"name", "dates", "items": [{"icon", "text"} or "text"], "milestone"}]`. 2-4 items per phase, short phrases. `milestone` renders a flag box at the bottom of the column.

## comparison
`columns` (option names), `rows`: `[{"label", "cells": [...]}]`, one cell per column. Cell values: integer 0-4 (Harvey ball, 4 = full), `"yes"`, `"no"`, `"partial"` (tick, cross, dash), or any short text. `highlight` (column index, or a list of indices, to outline as the recommended option(s)), `highlight_row` (row index, when the options are the rows), `legend_harvey` (a one-line key under the table), `label_width`. 3-6 rows, 2-4 columns.

## matrix
2x2. `quadrants`: 4 items in order top-left, top-right, bottom-left, bottom-right, each `{"title", "text"}`; `highlight` (quadrant index to fill with the accent); `x_axis` / `y_axis`: `{"label"}`. Optional `dots`: `[{"label", "x": 0-1, "y": 0-1, "highlight": true}]` placed on the grid; when dots are used the quadrant `text` is hidden (titles only) so labels stay readable.

## cascade
Top-down logic: question -> focus areas -> strategy -> impact. `levels`: `[{"label": "Strategy", "style": "TINT|OUTLINE|PRIMARY", "height": 1.0, "boxes": [{"title", "text", "icon"}]}]`. Arrows run from each box to the next level. 3-5 levels, 1-4 boxes each; keep `label` short (it is rotated). `height` is a relative weight.

## process
3-6 numbered steps joined by a line. `steps`: `[{"icon", "title", "text"}]`.

## pairs
Left item -> right item rows: risk -> mitigation, problem -> solution, today -> target. `rows`: `[{"icon", "left", "right"}]`, optional `headers`: `["Risk", "Mitigation"]`. 2-5 rows. Use this instead of `columns` when each column would hold one short line.

## Extra keys
- `comparison` cells may be `{"text": "High", "tone": "good|mid|bad"}` (pill: filled accent / soft / outlined grey). Pill colours: filled accent = favourable, soft = middling, outlined grey = unfavourable. Choose the tone by whether the value is *favourable*, not whether it is high: for risk or cost, "Low" is `good`. State the scoring direction in `legend_harvey` ("4 = best; for effort, 4 = least effort"). 
- `footnote` (slide level; `chart.footnote` also works): one small italic line under the chart (use for caveats like "Export growth is from a small base").
- `--primary` on the command line overrides `primary` in the spec; setting only one is enough.
- Look at per-slide PNGs, not the contact sheet, to judge text size and balance.
- `bar` charts plot the first category on top, in the order you write them (sort descending yourself).
- Pill/Harvey scores are hard to compare by eye; for 1-4 scores, prefer Harvey balls plus the scoring direction in `legend_harvey` (it is a general scoring-key line, not only for Harvey balls).
