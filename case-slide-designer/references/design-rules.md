# Design rules (the house style, and why)

This is the same house style as case-study-ppt; where the two ever differ, case-study-ppt wins. Key values: Avenir Next LT Pro (Aptos fallback), title 24pt one line, 16pt body minimum on main slides (14pt on appendix slides), about 40 body words per main slide (60 on the executive summary and closing slide).

The look is a blend of the three reference decks: the Auckland deck's calm framing and flat, friendly icons-in-circles; the Ivey deck's kicker + action title + thin rule, one strong accent, and big-number slide; the consulting layout of the user's pptx (phase chevrons, flags and number rows, native donut, section tracker). Sizing in the user's pptx was inspiration only; this system sets its own grid.

## Grid and frame (13.333 x 7.5 in)
- Grid and frame = case-study-ppt section 5 (`core.py` uses its values): content area x 0.182-13.15, y 1.30-6.95; a source line, when present, sits at y 6.70 (the content ends above it); a takeaway banner sits at the bottom of the content area.
- Frame: PRIMARY accent bar flush left beside the title (x 0, y 0.214, w 0.182, h 0.981); action title 24pt on one line at x 0.182, y 0.214 (about 60 characters; shorten rather than shrink, two lines only as a flagged fallback); optional subtitle 20pt at y 0.757; no rule under the title; logo top right (x ~11.32, h ~0.84, aspect kept); source line 10pt grey; page number bottom right (y 7.08); optional phase tracker bottom centre (3pt NEUTRAL_DARK line x 2.667-10.667 at y 7.108, active segment 4.5pt PRIMARY_DARK with a bold PRIMARY_DARK label).
- Generous white space: gaps of 0.2-0.3 between cards, 0.15+ padding inside. A slide that looks full is a slide to split.

## Colour: one accent, derived roles
`theme.make_palette(hex)` gives the five COBE roles exactly as case-study-ppt section 4 (from its `scripts/palette.py`): PRIMARY (accent), PRIMARY_DARK (active states, dark backgrounds), OUTLINE (2.25pt box outlines), MID (55% tint: secondary series, dashed outlines), NEUTRAL (light boxes, non-highlighted series), plus NEUTRAL_DARK (tracker base line). House-style extras: SOFT (25% tint: de-emphasised bars, comparison pills), TINT (card background), LINE (hairlines), INK (text `1B1F27`), GREY (secondary text `6B7280`). In COBE decks use only the five roles plus white and near-black text (case-study-ppt section 4); `build_deck.py --style` takes the game plan's Style line. Text on PRIMARY switches to dark automatically when white would fall below 4.5:1 contrast (yellow and light-green brands).
Use the accent for: key numbers, highlighted bars, icons, filled banners. Never add a second accent hue. Body text is INK on white or TINT; grey only for notes and sources.

## Type
- Headings, big numbers and body: Avenir Next LT Pro (premium) / Aptos (safe). Rendering uses Poppins/Inter as width proxies, so leave about 10% slack.
- Scale: title 24, subtitle 20, card heading 18-20 bold, body 16-18 (**16 minimum on main slides, 14 on appendix slides**, as case-study-ppt 4a; the scripts enforce it), table cells 16, chart, axis and tracker labels, legends and footnotes 14, source line and page number 10-12. KPI values 24-44, big number 80-140.
- Bold only the key phrase, never whole paragraphs. Sentence case everywhere except the kicker and row tags.
- Never rely on PowerPoint autofit; the builder measures text and sets explicit sizes.

## Titles (the most valuable thing you write)
Insightful, relevant, short, punchy (the course's standard). Formula: subject + verb + so-what, one line, about 60 characters. Run the "So what?" test: "Analysis" (topic) → "Most long-haul flyers also fly domestic" (fact) → "Converting long-haul flyers to domestic is the key to sustainable growth" (insight). Prefer the insight over an instruction ("Convert ... to grow"). Good: "Empowering patients is the key to success", "Two markets carry 42% of the international plan". Topic labels ("Market overview") go nowhere on the slide; the tracker already shows the section.

## Icons
Lucide line icons, 1.75 stroke, recoloured to the accent (white on filled shapes). Always paired with a label, in a filled circle ("badge") for headers and tiles, bare for list rows. One style per deck; do not mix in other icon sets. Pick concrete metaphors (store, users, trending-up, shield-check, timer) over abstract ones (star, sparkles). Faded large icons are allowed only on the cover.

## Charts
Native PowerPoint charts so the user can edit numbers. No border, gridlines, value axis or chart title inside the chart; data labels on every bar; category labels under the bars; legend only when the series cannot be labelled at the right end (the house builder then puts it at the bottom). One highlight colour (PRIMARY), the rest NEUTRAL, MID for a second level (case-study-ppt `references/visuals.md` section 4). Donuts: at most 4 slices, label the centre. Put the unit in `chart_title`. Do not use pie, 3-D, or more than 6 categories on a column chart (switch to `bar`).

## Layout variety
In a deck, do not repeat the same layout back to back; alternate card slides with charts, process, comparison. Use a `section` or `big_number` slide to break rhythm every 4-6 slides, except in COBE decks (case-study-ppt): there the phase tracker is the agenda, so no section dividers; vary layouts instead, and use a `big_number` slide only if it is a planned main slide.

## Anti-patterns (fix on sight)
- Paragraphs inside boxes; more than 3 bullets in a box.
- A takeaway banner that restates the title.
- Icons with no label, or an icon that does not match (check the render).
- Two charts on one slide unless they answer one question.
- Tiny text to make things fit: cut words or split the slide.
- Shadows, gradients, clip art, decorative stock photos, WordArt-style effects. (Device mock-ups, product images, screenshots and licensed persona photos that carry content are fine.)
- Logos stretched or recreated; use the supplied file at its native aspect ratio.
- Changing the user's numbers while "tidying".

## Restyle checklist (before delivering)
1. Every slide has an action title that passes "So what?"; titles tell the story read alone in order; Analysis slides end in a conclusion bar.
2. Every number matches the input; formats are consistent; units are labelled once.
3. No orphaned words, no text touching box edges, nothing outside the margins.
4. One highlight per chart; legend only when needed.
5. Icons recognisable; same stroke and size within a row.
6. `check_deck.py` (16pt floor; word counts are notes, not problems) reports OK; all PNGs inspected.
7. Delivery note lists cuts, reorderings, flagged inconsistencies, and the font reminder.
