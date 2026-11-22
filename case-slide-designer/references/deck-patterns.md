# Slide patterns from real COBE case decks

Patterns taken from two graded team decks: Deck A, a sustainability case (blue/green), and Deck B, a growth case (red/beige). Use them as building blocks. In deck-native mode, draw them with `deck_native.HostSlide` primitives in the host deck's colours. In house-style mode, use `core.Deck` primitives. Each pattern says when to use it, and the build notes give the geometry. The look should come from the host deck.

## Contents
1. Shared frame (every content slide)
2. Logic chain: the step-by-step build-up
3. Executive-summary rail
4. Numbered insight columns with a conclusion box
5. Input -> engine -> output
6. Hub and spoke
7. Gantt roadmap with decision gates
8. KPI wheel
9. Icon tile grid + context boxes
10. Map + KPI tiles
11. Flaws seen in the source decks (do not copy)
12. Decision tree (course)
13. Customer journey and personas (course)
14. Device mock-up and annotated image (course)
15. Build sequence: providing -> in order to (course)
16. Best-practice use case (course)
17. Financial waterfall + assumption tiles (course)
18. Hard and soft KPIs (course)
19. Analysis patterns: drivers + landscape, adoption curve, chart + takeaway, competitor benchmark, numbered cards + chart (course)
20. Profit / issue tree (course)
21. Pillar slide with use case box (course)
22. Three-phase timeline (course)
23. Risk matrix (course)
24. Recommendation & next steps, the closing slide (course)
25. Appendix-only patterns (course)

Patterns 12-25 come from the course's case-solving standard; case-study-ppt's `references/visuals.md` section 5 is the catalogue that points here. Text floors apply: 16pt body, 14pt chart and axis labels.

---

## 1. Shared frame
- A coloured vertical bar sits flush left beside the title block (about 0.18 in wide, about 1 in tall). It belongs to the layout, so it comes for free in deck-native mode.
- Line 1 is the title (topic or headline). Line 2 is the subtitle: one full sentence with the message, in a lighter weight, directly under it. (As found in the source decks; COBE decks built by case-study-ppt put the action title on line 1.)
- The logo sits top right.
- The section tracker sits bottom centre (labels Analysis, Strategy, Recommendation, Feasibility, or pillar names). It has a thin light base line across 4 equal segments, a thicker accent segment over the active section, and the active label in bold accent colour. The others are black or muted.
- The page number sits bottom right, as a field, not typed text.
- The body runs from about y 1.35 in to 6.85 in, and x from 0.36 in to 12.97 in (measured in the reference decks; new COBE slides use case-study-ppt section 5).

## 2. Logic chain (the user's preferred way to explain a plan)
Use it when a slide has to walk the audience through *why -> what -> how much -> what we get*.
- **Step header row** (y ~1.4): a numbered outline circle and a bold label per column ("Where we grow", "How many restaurants", "Yearly sales", "Our share"). Put a thin accent rule under each label and a filled accent chevron between columns.
- **Columns** of different widths, sized to their content. The widest one usually holds a map or picture.
- **Aligned rows**: when columns 2 and 3 describe the same items (region -> sales), give each item one row height in both columns. Link the pairs with a thin dashed connector in a soft accent. Bars in column 3 are proportional shapes: the lead item in full accent, the rest in the soft accent.
- **Result row** under the rows: one outlined rounded box per column with the total. Repeat the chevrons between them. Read aloud, the row tells the whole argument ("4 regions -> 550 restaurants -> $3.92B -> ~$1B").
- **Final column** is a tall filled accent tile with the payoff number (40 pt), its label, a thin white divider, and a 2-3 line explanation.
- **Bridge banner** at the bottom in a tinted rounded bar: how this links to the overall target ("550 + ~200 infill = 750 target").
- Keep the result boxes as bare totals, with no "=" signs. Keep each row to one primary number plus one short secondary line.

## 3. Executive-summary rail (Deck A slide 2)
- A left rail of 4 rows. Each row has a large line icon over an italic label: Challenge, Strategy, Solution, Impacts*. A thin vertical hairline separates the rail from the content.
- The right side changes per row:
  - Challenge: a dark filled banner with the case question in white, key words bold.
  - Strategy: a white answer box with a thin outline (no shadow) and an accent tab on top.
  - Solution: 3 tinted pillar cards side by side, each a bold heading plus 1-2 lines.
  - Impacts: 3 big signed numbers (-4%, -12%, -8%) over one-line metrics, aligned under the pillars.
- A footnote under the impacts carries the caveat: "*Proposed 24-month targets".

## 4. Numbered insight columns with a conclusion box (Deck A slide 3)
- 3 columns. Each has a large filled number circle that overlaps the left edge of an outlined rounded heading box with a 1-line insight.
- Under it go an illustration or icon cluster, then 2 icon bullets with **bold lead-ins**.
- A small accent down-chevron sits centred under the columns, pointing to the conclusion.
- The conclusion row has a dashed-outline box with a warning or "!" icon badge on its top-left corner holding the key takeaway. Beside it are 1-2 tinted fact boxes.

## 5. Input -> engine -> output (Deck A slide 5)
- One large rounded outline container holds 3 columns separated by dashed vertical lines. Triangle arrows on the separators show the direction.
- Each column has a filled header tab overlapping the container's top edge. The middle "engine" column uses the second brand colour.
- Rows are an icon in a filled circle plus one line of text, 3-4 per column, aligned across columns.
- Optional: a "core pillars" strip under it, with 3 outlined circles on a soft wave line, each a heading plus 3 lines.

## 6. Hub and spoke (Deck A slide 4)
- A question header goes top-left: a filled "?" circle plus a bold question.
- A central picture (globe or product) sits in a thin coloured ring. 4 icon nodes sit on the ring (filled circles, white icons).
- Each node connects with an elbow connector to a rounded outline callout box at the slide edge, with **bold key phrases** inside.
- A dashed takeaway bar runs along the bottom.

## 7. Gantt roadmap with decision gates (Deck A slide 6)
- The grid has workstream labels on the left, quarter and month headers on top, and light alternating row bands.
- Bars are rounded, coloured by phase (light -> mid -> dark as the work matures).
- Decision gates are dashed vertical lines with an up-arrow and a label above ("Gate 2: Pilot evaluation").
- Under the grid sit 3 phase cards, each outlined in its phase colour with an icon circle, a bold "Phase n: Name" and one sentence.

## 8. KPI wheel (Deck A slide 7)
- A centre donut of 4 segments labelled "01. MOVE" to "04. VERIFY", with an image in the hole.
- Metric groups sit left and right: a bold heading, a hairline, then 2 icon-bullet metrics each.
- A footnote in grey italics says how the KPIs are measured.

## 9. Icon tile grid + context boxes (Deck A slide 13)
- Left: a 2x4 grid of tinted tiles, each with a line icon and a 1-2 word label.
- Right: 3 outlined boxes, each with an icon on the left and 1-2 sentences.
- A down-chevron leads to a dashed conclusion box with a "!" badge.

## 10. Map + KPI tiles (Deck B slide 50, v2)
- An editable US map (`us_map.draw_us_map`) with the target states in accent and the rest in the beige or neutral tint. Numbered outline pins sit at region centres.
- Region cards under the map carry the number, the name, and one primary and one secondary line.
- On the right, 3 stacked KPI tiles: an icon in an outline circle, a big value, a bold label and a short note. The last tile is filled accent as the payoff.

## 11. Flaws seen in the source decks (do not copy)
- Text spilling out of boxes and header tabs ("Reuse what already exists" running past its tab, wrapped words under number bubbles). Size boxes to the text and check the render.
- Truncated or duplicated tracker labels ("Strateg", "Appendi", "Implementation" twice). Copy the tracker from a slide whose labels are right, or rewrite the labels.
- Number circles overlapping the first word of the next line.
- A slide from a different case left in the deck (a Deck A executive summary inside the Deck B deck). Flag it.

---

## 12. Decision tree (Strategy section)
- A full-width PRIMARY header bar with the strategic question ("<Client>'s strategic options").
- 2-3 levels of rounded boxes joined by thin straight arrows from the parent's bottom centre. Kept branches: white with a dark outline and a filled check badge on the lower-right corner. Killed branches: near-black fill, white text, a cross badge and a small PRIMARY tag with the one-line reason (from the game plan's kills: failed test + case evidence).
- A fading wedge under the tree leads into a conclusion bar: the direction chosen. Keep each box to 1-3 words.
- The scored alternatives table stays in the appendix.

## 13. Customer journey and personas (Analysis section)
- **Pain-point journey**: a header bar naming the process; 5-7 outlined stage boxes in one row; an arrow line under them with a marker per stage (check = well executed, cross = wrong or missing, warning triangle = depends on earlier steps) and a 3-line legend on the left; under the failing stages, filled boxes (PRIMARY for cross, MID for warning) naming the problem in 3-6 words; conclusion bar at the bottom: which stages to fix.
- **Personas across a journey**: stage labels on top (and the competitor's stages at the bottom), one line chart band per persona with a neutral midline (thumbs up / down icons at the left), client series in PRIMARY and competitor in MID, the decisive stages framed in a dashed box; persona photo circles from user-supplied or licensed stock photos (credited on the Sources slide), else an icon in a circle. Conclusion bar: the competitor's biggest edge.
- **STP / personas**: three headers Segmenting → Targeting → Positioning (PRIMARY / MID / NEUTRAL with arrows), then 3-4 persona columns crossed by three tinted bands: key attributes, pain points, how to reach them. Persona photos from the user or licensed stock (credited), one style, circular crop, same size; else an icon per persona.

## 14. Device mock-up and annotated image (Recommendation section)
- Phone (rounded rectangle about 2.2 x 4.4 in, 0.12 in dark bezel, small notch) or laptop frame drawn with shapes; the screen built from shapes and text in the palette (header bar, cards, buttons) so it stays editable, or a screenshot the user provides.
- Annotated version: the mock-up centred, 4-6 callouts around it, each a bold key phrase + 2-4 words, linked to the screen element by thin elbow connectors ending in a small dot.
- Pair it with 3-4 feature rows (icon + bold label) or a quoted tagline header. **Mock-up with feature list**: the device mock-up on one side, 3-4 features with icons on the other, a short tagline in quotes as a header.

## 15. Build sequence: providing -> in order to (Recommendation section)
- Left column header "Providing:", middle header "In order to:", illustration (mock-up) on the right.
- Rows: `<what we provide>` with the key word in PRIMARY → a light chevron → an outlined box with 2 short outcomes.
- Build it as consecutive slides with the identical title; each adds one row and greys the earlier rows (GREY text or 55% transparency, faded chevrons and box outlines) while the right-hand illustration changes to match the new row. No animations. The auditor counts the run as one slide; the last slide holds all rows and must meet the word limit.

## 16. Best-practice use case (Recommendation section)
- A 3-step numbered timeline across the top (circle numbers on one arrow line, a bold step name and one short sentence each).
- Under each step an image, screenshot or mock-up of how the benchmark company does it.
- A framed panel over the lower half labelled **Use case** with the company name (no logo unless supplied) and its measured result in large PRIMARY numbers ("reduced toxicity by 40%"), with the source on the source line.

## 17. Financial waterfall + assumption tiles (Feasibility section)
- **Bottom-up**: native waterfall (or stacked column with an invisible base series) from the starting total in PRIMARY down through the cost drivers in PRIMARY_DARK or NEUTRAL, values labelled above each bar; title above as a small chart title with the unit. Under it a header bar "Main assumptions" and 3-4 tiles (in two rows when 4): icon, label in a NEUTRAL box, value in a PRIMARY box (average price, volume, unit cost, breakeven).
- **Cash flow**: clustered columns, inflow in NEUTRAL and outflow in PRIMARY per year, labels on top; a PRIMARY bar underneath with the milestone ("Breakeven in 2025").
- **Top-down**: left, 3-4 key assumptions stacked as big PRIMARY numbers (WACC, share reinvested, growth rate, the strategy executed) with a label each; right, stacked columns by segment with a margin line on a secondary axis, optional start and end donuts linked by wedges. Or a waterfall from EBITDA to free cash flow with the strategic spend split in a donut.

## 18. Hard and soft KPIs (Feasibility section)
- **Hard KPIs**: 3-5 tiles (or diamonds) with a big PRIMARY number and a 2-4 word label: NPV, additional revenue, units, price change. Title states what they enable.
- **Soft KPIs**: 2-4 large outlined circles with the number and a one-line label (CO2 saved, satisfaction, brand, air quality), optionally over a relevant context image with thin dashed leader lines.
- **KPI strategy map / Balanced Scorecard** (appendix): vision and purpose rows, 3 strategic priorities and results, then four perspective rows (Financial, Customer, Internal processes, Organisational capacity / learning & growth) of linked objective ovals with KPI, target and initiative columns on the right. The main deck shows the hard and soft KPI slides instead.

## 19. Analysis patterns (Analysis section: macro environment -> micro environment -> internal abilities -> main challenge or opportunity)
- **Drivers + landscape**: left, 3-4 key industry drivers (icon + one bold phrase each); right, a competitive landscape 2x2 (two decisive dimensions) with competitors placed, the client's current position, an arrow to the highlighted **target dimension** box. Conclusion bar: what reaching the target dimension gives the client.
- **Adoption curve + personas** (new product or tech adoption cases only): bell curve with the five groups (innovators 2.5%, early adopters 13.5%, early majority 34%, late majority 34%, laggards 16%) and one persona card per group or per target group.
- **Chart + takeaway**, **competitor benchmark** (5-6 rows, Harvey balls) and **numbered cards + chart** also fit the Analysis section.
- The last Analysis slide states the **main challenge or opportunity** in one sentence.

## 20. Profit / issue tree (Strategy section)
- When the case is about one metric: revenue vs cost branches down to levers, ending in a "brainstorming ideas" bar that names the levers chosen.

## 21. Pillar slide with use case box (Recommendation section)
- What the pillar does (2-3 short boxes or icon rows) + an illustration (mock-up, annotated image, process) + a **use case box**: "Use case: <company>" with its logo-free name, what it did and its result number, sourced.

## 22. Three-phase timeline (Feasibility section)
- 3 phases: numbered circles, name, dates, 2-3 keywords each. With decision points, use the gantt with gates (section 7).

## 23. Risk matrix (Feasibility section)
- Probability x impact square, numbered risks, one-line mitigations; the full table in the appendix.

## 24. Recommendation & next steps (closing slide)
- "We recommend ..." in a PRIMARY banner, 3 headline impact numbers, 3 numbered next steps (what / who / when).

## 25. Appendix-only patterns
- Formula chain (`Traffic x Capture x Check x Days = AUV`) with an assumptions box and the full calculation table.
- Alternatives comparison table: options as rows, criteria as columns, Harvey balls, chosen option in MID.
- Full financial model with best / base / worst.
- Native tables with a PRIMARY header row, NEUTRAL bottom borders and a totals row.
