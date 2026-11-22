# Visuals: icons, images, think-cell elements, charts and slide patterns (case-study-ppt sections 4c and 7)

Read this before building or redesigning any slide. Patterns follow the course's case-solving standard.

## 1. Icons

- One icon style for the whole deck: simple line (outline) icons or solid glyph icons, never mixed. Flaticon's "lineal" or "glyph" families are the reference look.
- Source: if the user provides Flaticon icons (PNG/SVG), use them and credit Flaticon on the Sources slide as its free licence requires. Otherwise use the line style from case-slide-designer's bundled Lucide library (1,544 icons; find with `python <designer-dir>/scripts/icons.py <keywords>`, render with `icons.render`, as SKILL.md 4c Tools describes). Glyph style: the user's glyph icons, else Font Awesome solid (`react-icons`, `fa6`); a line icon missing from Lucide can come from Feather (`react-icons`, `fi`); render `react-icons` to PNG at 256px+ as the pptx skill describes. The sandbox usually cannot download from flaticon.com.
- Recolour icons to PRIMARY; on PRIMARY boxes, white. Same size within a row (about 0.4-0.6 in), optionally inside a PRIMARY circle with a white icon for headers and KPI tiles.
- Every icon sits next to a label: executive summary row labels, column headers, KPI tiles, timeline phases, scorecard perspectives, next steps. No decorative icons, no clipart.

## 2. Images and mock-ups (allowed when they carry content)

The course's examples use real images to make the recommendation concrete, so these are allowed:
- **Device mock-ups**: a phone or laptop frame (drawn with rounded rectangles, or a frame image) holding a screen of the proposed app, page or feature. Build the screen from shapes and text in the palette so it stays editable, or use a screenshot the user provides.
- **Annotated mock-up**: one central image with 4-6 callout labels linked by thin elbow lines (bold key phrase + 2-4 words each), like the IKEA virtual-store example.
- **Product or company images** from the case PDF (`pdfimages -png`), the company's own site, or the user, when the slide is about that product. Credit the source on the source line.
- **Context photo** behind soft KPIs (a skyline, a store), only when it supports the message, with the numbers in clear circles on top.

- **Persona photos**: real-person photos for personas (STP, journey, adoption-curve slides), as in the course's own framework examples. Use photos the user provides or properly licensed stock (free licence such as Unsplash or Pexels, or a paid licence), credited on the Sources slide; one consistent style, circular crop, same size.

- **AI concept images** (product concepts, shelf or store scenes, a title hero): allowed when they carry content. The user generates them from your prompts (SKILL.md 4d); keep them small, add labels as real slide text, source line `Concept visual`.

Not allowed: decorative stock photos, clipart, images of people as decoration (outside personas), AI-generated people passed off as real, logos redrawn or stretched.

## 3. think-cell design elements (shapes in the palette)

- **Process chevrons**: phases or workstreams as a chevron row, PRIMARY / MID / NEUTRAL left to right.
- **Numbered circles with connectors** for steps, initiatives or risks.
- **Brackets** grouping items with a label box underneath.
- **Harvey balls** in PRIMARY for qualitative ratings.
- **Check / cross / warning marks** (PRIMARY check, near-black cross, MID warning triangle) instead of yes/no text.
- **Conclusion bar**: a full-width PRIMARY (or NEUTRAL) banner at the bottom carrying the slide's so-what in one line. Every Analysis slide ends with one; use it on Strategy and Recommendation slides when the title alone doesn't carry the conclusion. It must add the implication, not repeat the title.
- **Agenda / tracker**: the phase tracker is the deck's agenda; no separate agenda slide needed.

## 4. Charts (think-cell conventions, always native and editable)

Build charts with pptxgenjs `addChart`; draw with shapes only when PowerPoint has no native form.
- No border, background, gridlines or value axis line; label the data instead.
- Data labels on every bar or segment; category labels under the bars; thin near-black baseline.
- Legends only when unavoidable; label series at the right end instead.
- One highlight: the series or bar carrying the message in PRIMARY, the rest NEUTRAL (MID for a second level). Never a rainbow.
- Wide bars, gap width ~50-80%.
- Bar and column charts start at zero; a line chart whose axis doesn't says so on the axis.
- Annotations on top where they carry the message: CAGR arrow with a rounded label (`+8% CAGR`), difference arrow (`+$1.2B`), total label on stacked columns.
- Typical types: column / stacked column, horizontal bar (rankings), waterfall (cost drivers, EBITDA allocation), 100% stacked (shares), clustered inflow vs outflow columns (cash flow), stacked column + line on a secondary axis (segment mix + margin), Gantt-style timeline.

## 5. Slide patterns by section (catalogue)

The word guide from SKILL.md section 3 applies on main slides. Vary patterns: none on neighbouring slides, none more than twice in the main deck, a different one for each pillar slide. This is the catalogue (name, when to use it, what it proves); the build notes for each pattern are in case-slide-designer's `references/deck-patterns.md` (`DP §N`), read only for the patterns the deck uses.

### Analysis (macro environment → micro environment → internal abilities → main challenge or opportunity)
- **Drivers + landscape**: industry drivers and a competitive 2x2 with the target dimension; proves where the client must move (DP §19).
- **STP / personas**: Segmenting → Targeting → Positioning with 3-4 persona columns; proves who to target and how to reach them (DP §13).
- **Customer journey (pain points)**: stages with check / cross / warning marks; proves which stages to fix (DP §13).
- **Personas + journey vs competitor**: satisfaction per stage, client vs competitor; proves the competitor's biggest edge (DP §13).
- **Adoption curve + personas** (new product or tech adoption cases only): proves which adopter group to win first (DP §19).
- **Chart + takeaway**, **competitor benchmark** (5-6 rows, Harvey balls), **numbered cards + chart** (DP §19).
- The last Analysis slide states the **main challenge or opportunity** in one sentence.

### Strategy (determine the direction, create alternatives, analyse them)
- **Decision tree** (main slide): kept and killed branches with the game plan's kill reasons; proves the direction chosen (DP §12).
- **Profit / issue tree**: one metric split into levers; proves which levers were chosen (DP §20).
- The scored alternatives table stays in the appendix.

### Recommendation (one section per pillar, or one section with a slide per pillar)
- **Pillar slide with use case box**: what the pillar does + illustration + sourced use case (DP §21).
- **Build sequence** ("Providing → In order to"): same-title slides adding one row each, no animations; the auditor's script counts the run as one slide (DP §15).
- **Device mock-up / annotated image / mock-up with feature list**: makes the pillar concrete (DP §14).
- **Best-practice use case**: 3-step timeline of how the benchmark works + framed result panel; proves it works elsewhere (DP §16).

### Feasibility (implementation and timeline, risks and mitigation, soft and hard impacts, financial breakdown)
- **Timeline**: 3 phases (DP §22) or a Gantt with decision gates (DP §7).
- **Risk matrix**: probability x impact, one-line mitigations; full table in the appendix (DP §23).
- **Financial breakdown, bottom-up** (waterfall of cost drivers + 3-4 assumption tiles, optional cash in vs out per year with breakeven) or **top-down** (assumption tiles + results by segment, or EBITDA → free cash flow waterfall) (DP §17).
- **Hard KPIs**: 3-5 big numbers, title states what they enable; **soft KPIs**: 2-4 non-financial impacts as large circles (DP §18).
- **Balanced Scorecard strategy map** (appendix; the main deck shows the hard and soft KPI slides instead) (DP §18).
- **Recommendation & next steps** (closing slide): "We recommend ..." banner, 3 impact numbers, 3 next steps (DP §24).

### Appendix-only patterns
Formula chain, alternatives comparison table, full financial model with best / base / worst, native tables (DP §25).

Every slide needs a visual element. Plain bullet slides do not fit this style.
