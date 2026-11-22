---
name: "case-slide-designer"
description: Turn rough text, data, notes or a semi-built .pptx into clean, professional consulting-style case study slides (action titles, native charts, line icons, KPI tiles, roadmaps, logic chains with arrows, decision trees, customer journeys, mock-ups, financial waterfalls, maps, comparison tables, 2x2s). Use whenever the user wants slides redesigned, restyled, rearranged, "made beautiful", polished or built from text and numbers for a case study, case competition, pitch or business-school deck, including "design slide 14" on an attached deck, even if they only say "make this look professional". Also use to redesign single slides of a finished case deck. For a whole COBE case deck built from a case or a game plan, use case-study-ppt instead.
---

# Case slide designer

Takes content that is already thought through (text, numbers, a rough deck) and returns slides that look like a top-tier consulting or case-competition deck. That means one message per slide, a clear visual structure and logical build-up, one accent colour, line icons, and native editable shapes and charts. This skill designs. It does not solve the case or change the facts.

There are two modes:
- **Deck-native mode** (the usual case): the user attaches a team deck and says "design slide N". Build the new slide *inside that deck's own master*, so it pastes back in without anything shifting. See "Deck-native mode" below.
- **House-style mode**: there is no host deck, or the user wants a fresh look. Build with the JSON spec and the house layouts (`build_deck.py`).

Output is always editable PowerPoint: real text boxes, real shapes and charts, never screenshots of slides.

**One house style with case-study-ppt.** This skill and case-study-ppt share one standard; where they used to differ, case-study-ppt's values win and the scripts now enforce them: font Avenir Next LT Pro (fallback Aptos), action title 24pt on one line (about 60 characters) passing the course's "So what?" test, optional 20pt subtitle, PRIMARY accent bar flush left, **16pt minimum for all body text on main slides** (appendix slides 14pt; only tracker, chart and axis labels 14pt; source line, page number and the Sources slide 10-12pt; legends and footnotes 14pt), about 40 body words per main slide (60 on the executive summary and closing slide) as a guide for a clean look, not a rule, tracker labels Analysis / Strategy / Recommendation / Feasibility, pillar names, or Analysis / Strategy / Implementation / Impact (as chosen in game plan section 0). Cut words or split the slide; never shrink below the floors. The course's case-solving standard defines the section structure and slide patterns (case-study-ppt `references/visuals.md`).

## Files

- `scripts/deck_native.py`: deck-native mode. Run `scan deck.pptx` to list colours, fonts, layouts and each slide's tracker, with the active label marked * (add `--labels "Pillar A,Pillar B"` when the tracker uses pillar names; pass the same list as `HostSlide(..., tracker_labels=[...])`). The `HostSlide` class builds a slide in the host master: titles, an exact tracker copy, the slide-number field, `copy_shape(from_slide, name)` for any other named shape of a sibling slide, primitives in the deck's style, and a one-slide export.
- `scripts/us_map.py`: an editable US map, with every state as a freeform you can recolour. It returns region centres for pins.
- `scripts/build_deck.py`: JSON spec -> .pptx using the house layouts (house-style mode). `--style "<game plan Style line>"` uses its PRIMARY, PRIMARY_DARK, OUTLINE, MID and NEUTRAL hex codes exactly.
- `scripts/extract_deck.py`: dumps a deck to JSON plus embedded images (logos).
- `scripts/render.py`: .pptx -> one PNG per slide (`--sheet` writes `_extra/sheet.png`).
- `scripts/check_deck.py`: mechanical QA (overflow, text below the floors in text boxes, groups and table cells, off-slide shapes, fonts; the word count is printed as a note only) with the same size floors and slide detection as the auditor's `audit_pptx.py`: main slides 16pt (word guide 40, 60 on a slide carrying "We recommend"), appendix 14pt, Sources slide and footer band 10pt, title and footer band not counted. Pass `--fonts "Head,Body"` or `--fonts safe` (Aptos) when not using Avenir Next LT Pro, or every run gets flagged.
- `scripts/icons.py`: search the 1,544 bundled line icons (`python scripts/icons.py growth money`).
- `scripts/core.py`, `layouts.py`, `theme.py`: the house toolkit (`core.Deck` primitives). The frame and grid in `core.py` are case-study-ppt section 5; the five COBE palette roles in `theme.py` come from case-study-ppt's `scripts/palette.py` (same formulas as a fallback).
- `references/layouts.md`: spec keys and limits for the 13 house layouts.
- `references/design-rules.md`: palette, type scale, title formulas, chart and icon rules, anti-patterns.
- `references/deck-patterns.md`: slide patterns from real COBE decks (logic chain, exec-summary rail, input -> engine -> output, hub and spoke, gantt with gates, KPI wheel, map + tiles) plus the course's patterns (decision tree, customer journey, device mock-up, build sequence, use case, financial waterfall, hard and soft KPIs). Read it when choosing a structure.
- `assets/us-states-albers.json`: the map data (us-atlas, ISC licence: `assets/US-ATLAS-LICENSE.txt`).
- `assets/icons.json`, `assets/icon-tags.json`: the Lucide icon library and its search tags (`assets/ICONS-LICENSE.txt` must ship with them).
- `assets/example-spec.json`: a full house-style spec using every layout; copy it as a starting point (its `section` slide is for non-COBE decks).

Setup: if `import cairosvg` fails (icons), run `pip install --break-system-packages cairosvg` first.

## Workflow

1. **Intake.**
   - If the user says "ask before making" or the slide could take several very different shapes, offer 2-3 layout options with ASCII previews in one AskUserQuestion round. Batch in the other open decisions: what the numbering means, which tracker phase, appendix or main deck. Otherwise build straight away.
   - In house-style mode, also settle the accent colour, the logo (take it from the deck's media, never redraw it) and the fonts.
2. **Read the input.**
   - Run `extract_deck.py` and `render.py` on the deck, then look at the target slide *and* 3-4 sibling slides to learn the deck's look.
   - In deck-native mode, also run `deck_native.py scan deck.pptx`.
   - Never edit the user's file. Always write a new one.
3. **Check the content before designing.**
   - Re-add every total and sub-total: units, sums, before -> after counts, shares.
   - Look for the same metric with two values, and for ranking numbers that disagree with the data.
   - If the slide is an empty template (blank boxes, no risks or mitigations written), ask for the content. Never invent it.
   - Note things to flag: typos, a slide from another case, truncated tracker labels.
4. **Plan the story.** Decide the structure (see "Choosing a structure"), where each fact goes, and what to cut. Show the plan only when you restructured something.
5. **Build.** In deck-native mode use the recipe below. In house-style mode write the spec (`references/layouts.md`) and run `build_deck.py spec.json out.pptx --primary HEX --logo logo.png`.
6. **Look at it.** Render, open the PNG and inspect it as a viewer would: wrapped single words, labels touching edges, inconsistent sizes between sibling boxes, icons that do not read, empty zones. Expect 2-4 passes.
7. **Run `check_deck.py`** with the right `--fonts` and clear everything it reports. Word-count lines are notes: judge the rendered slide and cut only when it looks crowded.
8. **Deliver** the .pptx with SendUserFile and a short note covering:
   - what the slide became
   - what you cut or reworded
   - number checks and inconsistencies you found
   - font substitution, if the deck font was missing when rendering
   - how to paste it in (deck-native: Reuse Slides, or paste with "Use Destination Theme")

## Deck-native mode

The user's deck already has a visual system: an accent bar left of the title, title and subtitle placeholders, a logo, a section tracker, a page-number field, brand colours, a body font and an icon style. A redesigned slide must look like it was always part of that deck. So build it on the deck's own master and copy, rather than imitate, the deck's frame elements. Users notice immediately when the accent bar is missing, when the tracker differs by a few pixels, or when a red is slightly off.

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from deck_native import HostSlide
from us_map import draw_us_map            # only if a map helps

h = HostSlide("deck.pptx", layout_from=14)      # a sibling slide whose layout has the accent bar + logo
h.set_titles("<original title, verbatim>", "<original subtitle, verbatim>")
h.copy_tracker(from_slide=12, labels=["Analysis", "Strategy", "Recommendation", "Feasibility"], active="Recommendation")
h.copy_slide_number(from_slide=12)
# ... draw content with h.box / h.text / h.num_badge / h.line_icon / h.chevron / h.connector, h.s for raw access
h.save_single("out/SlideNN_<topic>.pptx")
```

Rules, each learned from user corrections:
- **Keep both title lines exactly as the user wrote them**, in the layout's title and subtitle placeholders. Do not demote the title to a kicker or move the subtitle into a caption. If you think a sharper action title would help, suggest it in the delivery note instead.
- **Keep the accent bar, logo and title styles** by using a layout that has them. Pick it from a content slide, not from an appendix layout with a baked-in "Appendix" tracker.
- **Copy the tracker exactly** from a sibling slide with `copy_tracker`. Pass `labels=` to fix typos (one deck had "Implementation" twice), and pick the active phase with `active=`, which moves the highlight segment and swaps the bold/colour styles. Prefer a source slide whose labels `scan` shows as correct.
- **Use the deck's hex codes, never approximations.** Read them from `scan` and from the target slide's XML: brand accent, card tint, soft secondary colour, text colour. Use the target slide's own fill colours first.
- **Use the deck's body font** (from `scan`) on every run. If it is missing on the render machine, say so once and leave a little slack in text boxes.
- **Match the icon style** by looking at the rendered slides. Case decks usually use thin line icons in the accent colour, either bare or inside a thin accent outline circle, and numbers inside accent outline circles. Use `h.line_icon(..., ring=True)` and `h.num_badge(...)` to match. Use a filled circle only if the deck does.
- **Deliver a one-slide file** that shares the master (`save_single`). The slide-number field shows 1 in that file and becomes correct after pasting.
- Remove leftover empty or off-slide placeholders (`set_titles` does this).

## Choosing a structure

| The content is... | Structure |
|---|---|
| a plan or argument that builds step by step (where -> what -> how much -> payoff) | **logic chain** (deck-patterns.md section 2): numbered step headers with chevrons, aligned rows, a result row with arrows, a payoff tile, a bridge banner |
| a location strategy (regions, states, markets) | map + region cards, or a map as step 1 of a logic chain |
| goal / problem / solution / impact in one view | exec-summary rail (deck-patterns section 3) or `exec_summary` |
| 2-4 parallel ideas, pillars, insights | numbered insight columns (section 4) or `columns` |
| inputs processed into outputs | input -> engine -> output (section 5) |
| one theme with 4 surrounding drivers or barriers | hub and spoke (section 6) |
| phases with dates and decision points | gantt with gates (section 7) or `roadmap` |
| KPIs grouped by objective | KPI wheel (section 8) or `kpis` |
| one striking statistic | `big_number` |
| numbers (comparison, trend, mix, bridge, relationship, share) | `chart` + `callouts`; pick the chart type with case-study-ppt section 4c "Choosing a chart" |
| options kept or killed, setting the direction | **decision tree** (deck-patterns section 12) |
| a process with pain points, or personas across a journey | **customer journey** (section 13) |
| a pillar that needs to be seen (app, feature, store concept) | **device mock-up** or annotated image (section 14) |
| a pillar explained as "we provide X in order to Y" | **build sequence** (section 15) |
| proof that a pillar works elsewhere | **use case** panel (section 16) |
| cost drivers, cash flow, financial assumptions | **financial waterfall + assumption tiles** (section 17) |
| financial and non-financial results | **hard KPIs** / **soft KPIs** (section 18) |
| options scored against criteria | `comparison` |
| two dimensions, prioritising | `matrix` |
| sequential steps | `process` |
| risk -> mitigation, problem -> solution | `pairs` |

When the user asks for "a better path of thought", "arrows", "logical build-up" or "easier to explain", use the logic chain. A presenter should be able to read the bottom row aloud as the whole argument, with the columns above as evidence.

## Content rules that matter

- **Facts are fixed.** Never change a number, name, date or claim. Rewrite wording to fit, and list in the delivery note anything you cut or any inconsistency you found. If something is ambiguous, keep the user's version and flag it.
- **Less is more.** This user consistently cut the following, so don't add them in the first place:
  - Secondary metrics next to the primary one (for example "~12 per 1M people" beside a store count).
  - Bullets that restate the subtitle (for example "Under-represented today / Heavy commuter traffic" under a subtitle that already says that).
  - Symbol clutter in totals ("= 550"). Write bare results ("550 new restaurants") and let the arrows carry the logic.
  - Empty boxes from the original ("Financials" with nothing in it). Drop them and say so.
- **Titles.** In house-style mode, every slide gets an action title (one line, about 60 characters, an insight that passes "So what?") with an optional 20pt subtitle; the spec's `kicker` key is shown as that subtitle. In deck-native mode, keep the deck's title/subtitle convention: the subtitle is usually the action sentence.
- **One message per slide.** Walls of bullets become columns, a chain, a process or a chart. Keep at most 3 short bullets per box.
- **Numbers.** Use one format everywhere (`$3.9B`, `$869M`, `+245`, `223 → 468`; COBE decks follow case-study-ppt 4b: 1 decimal for M/B on main slides, `$3.92B` only in appendix tables). Compute totals rather than retyping them, and label units once.
- **Chart type: message first.** Before picking a chart, ask what the number must prove, then consider case-study-ppt section 4c "Choosing a chart" (comparison → column or sorted bar, bridge → waterfall, trend → line, relationship → scatter or bubble, share → donut or 100% stacked, target → bullet or KPI tile). It's a guide to weigh first, not a rule: keep the user's chart when it reads well, and suggest a better one in the delivery note instead of silently swapping it. The builder's `chart` covers column, stacked, stacked100, bar, line and donut; build other types from shapes. Add the one emphasis that carries the title (highlight, labelled target line, or difference arrow).
- **Charts and bars** carry one highlight: the item that makes the point in the accent colour, the rest in the soft accent. Use data labels, not axes or gridlines. Use native charts in house-style mode. Proportional shape bars are fine when they must line up with rows on the same slide.
- **Icons carry meaning.** Use one per concept, never decorative. Check every icon in the render.
- **Source line** goes on any slide with outside data. Never invent a source.
- Cut words that sound written by a machine ("leverage", "robust", "seamless", "not just X but Y").

## House-style mode notes

The house layouts follow `references/design-rules.md` (one accent, Avenir Next LT Pro or `--fonts safe`, accent bar + action title + optional subtitle, the case-study-ppt section 5 frame, tracker via the spec's `tracker` + `phase`). Fonts must be installed on the presenting machine. Offer `--fonts safe` (Aptos) if the user will present from another computer. The builder numbers pages from 1: when delivering a single slide for a known position, set the `page-number` text box to that number before saving.

## Working with the COBE case skills

Place in the pipeline (full table in case-study-analysis-gameplan, "Case pipeline"): an optional step for redesigning single slides of a case deck with finished content (action titles, numbers, storyline). case-study-ppt does not call it afterwards: its section 4c uses this skill's rules and tools while building. When working on a COBE deck:
- Keep every title, number and the storyline exactly. Facts come from the game plan and `COBE_<Case>_CaseFacts.md`, never from the case PDF; a fact missing there: tell the user; if it changes a number, a target or the recommendation, stop and offer case-study-analysis-gameplan Stage 5; otherwise use a labelled assumption. Never invent it.
- Use the Style line's palette and fonts (`--style "<Style line>"`, `--fonts "Head,Body"`; deck-native mode reads the deck's own colours).
- Pass `tracker` (`Analysis, Strategy, Recommendation, Feasibility`, the pillar labels, or `Analysis, Strategy, Implementation, Impact`, as in game plan section 0) and each slide's `phase`.
- Run `check_deck.py` with its defaults (16pt main / 14pt appendix floors; the word count is a guide); fix by splitting content rather than shrinking.
- Never add speaker notes.
- **Never change an argument on one slide.** A kill reason, claim, precedent or number that should change is a plan change: say so and offer case-study-analysis-gameplan Stage 5, which lists every place it appears (other slides, appendix, notes, Q&A). Redesigning the look is this skill's job; changing what the deck argues is not.
- Nothing on the slide may show another option ahead of the recommendation (case-study-ppt 3b). Don't reuse the pattern of a neighbouring slide. The accent colour only as the Style line allows. AI images only from files the user sends (prompts as in case-study-ppt 4d).
- No section-divider slides (the tracker is the agenda) and no `big_number` slide unless it is a planned main slide; build the title slide per case-study-ppt section 2a, not the house `title` layout.
- Deliver one-slide files; never edit the deck or name a version. Before the deck's first audit, case-study-ppt inserts them (its section 4c, `merge_decks.py`); after it, inserting or replacing slides is a case-study-fixer job (new version, then re-audit), so versions and the audit trail stay right.
- End with: "Next: <case-study-ppt inserts these slides | case-study-fixer puts them into the deck and re-audits>. Run it now?" and wait for the user's yes.

If the team deck already exists, prefer deck-native mode so the slides match it.