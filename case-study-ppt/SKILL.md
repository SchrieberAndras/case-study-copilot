---
name: "case-study-ppt"
description: "Build the COBE case deck as a PowerPoint .pptx file (plus PDF, speaker notes, Q&A) from an agreed game plan, or one team member's part, or the team skeleton. Use whenever the user wants case study slides, a case presentation, a COBE deck or 'make the slides for the case', even without saying PowerPoint; the output is always a .pptx file, so this wins over generic slide skills and Slides artifacts for case decks. Never solves the case itself, and never moves to the next pipeline step without the user's yes, unless the user asked for a no-interruption run."
---

# Case study PPT

**The deliverable is always a PowerPoint .pptx file** (with a PDF export, and Word files for the notes and Q&A), never a Slides artifact or another format, whatever the session's default for decks is.

Builds the case deck with a fixed process, storyline and visual system. Copy the **process, style and structure** below; take **colours, logo and content from the case at hand**, never from a previous case. Course standard (case-solving guidance): Executive summary, Analysis, Strategy, Recommendation, Feasibility; it beats any older rule.

Read the `pptx` skill's SKILL.md first (pptxgenjs gotchas, validation, rendering). Build with pptxgenjs, `pres.layout = "LAYOUT_WIDE"` (13.333 x 7.5 in). Geometry below is in inches.

## Case pipeline

Chain: case-study-analysis-gameplan (1) → case-study-ppt (2) → case-deck-merger (2b, team only) → case-study-auditor (3) → case-study-fixer (4); 3-4 repeat until READY TO SUBMIT. Full table in `case-study-analysis-gameplan` ("Case pipeline"). Rules (a copy of case-study-analysis-gameplan's "Handoff rules"; change them there first, then here):
- Each step does only its own job; for anything another step owns, hand over.
- Finish with one line: "Next: <skill> – <what it will do>. Run it now?" On yes, load it with the Skill tool and pass every file so far; in a new chat, list the files to attach.
- **Always confirm before moving on**, including calls inside a skill's own flow (compressed mode, pre-audit, re-check). Unattended runs stop at the offer. The one exception is a no-interruption run (next rule).
- **No-interruption run** (the user says "just build it", "just run it" or "run with no interruptions"): the chain runs to the end without a stop. It starts from the user's game plan, or from case-study-analysis-gameplan when there is none (full analysis, council at graded size, your recommended strategy, named at the top of the delivery). No sample-slide stop, no "Run it now?", no approval questions: take the recommended option each time and list every such choice at the end so the user can reverse it. Then build → one full audit → one fix pass → one light re-check → deliver once. Image prompts go out with the delivery (shape mock-ups in the deck until then). Only what the user alone can supply (a case fact that changes the recommendation, a private file, real presenter names) stays open: finish everything else and deliver NOT READY TO SUBMIT with it on top.
- **The audit loop is capped.** One full audit, one fix pass, one light re-check (numbers, look, feasibility; case-study-auditor section 5a), at most one more fix pass, then deliver with anything still open on top. "Fix everything, don't re-audit" skips the re-check. A full independent re-audit runs only when the user asks for it by name.
- **Conflicts get asked.** When something the user supplies (an image, a file, a number, a team decision) differs from the game plan, ask which is right and write the answer into the plan; never work around it silently. In a no-interruption run follow the user's newest input and list the conflict at the end.
- Nothing is re-asked downstream: setup answers (length, presentation date, time limit, timeline anchor, research, team and presenter names, build mode, section labels, brief constraints, case file and title, frame-slide owner, Style line with accent and font) live in game plan section 0, the merge log and the audit's Context block.
- Nothing is lost: every file carries forward (case PDF, facts file, brief, game plan with change log, deck, notes, Q&A, merge log, latest audit, calibration record). If one is missing, say which and continue.
- **Case source: `COBE_<Case>_CaseFacts.md`**, never the case PDF's text. Facts, numbers, quotes and page references come from it and the game plan. The PDF is used only by scripts (`pdfimages` for the logo, `overlap_check.py`). A fact missing from the facts file: tell the user; if it changes a number, a target or the recommendation, stop and offer case-study-analysis-gameplan Stage 5 (the fact is added there); otherwise use a labelled assumption. Never open the PDF to look unless the user says so.
- **The game plan stays current.** Only the user decides changes. A step applying an approved change to the recommendation, a number, a target or the storyline also updates the plan and adds a section 16 Change log row (what, old → new, who approved). Logged changes are approved, not drift. A step that finds an error without approval stops and tells the user.
- **Versions.** The first complete deck is v1 (`COBE_<Case>.pptx`), whichever step produced it, never `_v2`. If an input already has that name, copy it first (merge base → `COBE_<Case>_Skeleton.pptx`, shared-deck download → `COBE_<Case>_Download.pptx`) so the output takes the plain name. Only the fixer produces `_v2`, `_v3`, ...; an audit is numbered by the deck version it grades (`_Audit_v1` for v1).

## Building from a game plan (the normal path)

`COBE_<Case>_GamePlan.md` **is the answer to the 13 steps and to section 0**. Build from it; don't re-solve or re-ask.
- **Never change** the agreed strategy, the "We recommend ..." sentence, targets or numbers. An error or real gap: stop, tell the user, offer case-study-analysis-gameplan Stage 5, build on the updated plan.
- Use: the storyline table for order, action titles and the **Pattern column (the user chose these; build them)**; Key content for the exact data per slide; Numbers as the single source of truth (copied into the build script's asserts); the brief map to place every required item; Sources for links (re-proofed per 8a); the team split for the notes; Creative element, Wildcards used and Horizon option for pillar visuals and the timeline; Precedents for use-case slides; Likely Q&A for the Q&A file (expand to 8-10, keep its answers); Partners for the "what's in it for them" line on the pillar slide, its appendix slide and the Q&A; "Where alternatives win" for what may be shown (only rows marked for a slide, with their one-line reason) and what stays in the Q&A (3b); Images needed for the prompts (4d); the timeline anchor for every date.
- Fill in only what the plan leaves to the deck: layout, visuals, icons. The Style line: use its palette, accent, font and icon style exactly (a plan without one: derive it per section 4 and write it into section 0).

**Without a game plan**: ask once, "The analysis skill (case-study-analysis-gameplan) works out and stress-tests the strategy with you before any slides. Run it first (full or compressed)?" Load it only on a yes; compressed mode asks before handing back. This skill never solves the case. If the user refuses, stop: a deck needs an agreed strategy.

## 0. Questions before starting

One round (the question tool takes 4 per call; use a second call only if more are open). **Skip everything game plan section 0 or the conversation answers**; without a game plan, ask them all.
0. **What to build?** Solo → whole deck. Team, one shared deck → whole deck. Team, separate files → ask: "Only my part" (recommended), "Team skeleton", "Whole deck", confirming name and slides from the team split. No plan → "Whole deck" (recommended) or "Only my part". Part → 0a, skeleton → 0b.
1. **Presentation length** (minutes): it sizes the deck, the hardest thing to fix later.
2. **Outside research**: "Allowed / encouraged" first (recommended); default allowed.
3. **Presenters**: number and real names (never "Presenter 1": placeholder names block submission), for the title slide, team intro and notes split.
4. **Section labels** (unless section 0 has `Sections:`): **Standard (Recommended)** `Analysis`, `Strategy`, `Recommendation`, `Feasibility`; **Pillar names** (`Analysis`, `Strategy`, one per pillar, `Feasibility`; multi-pillar only; each label fits its segment at 14pt, ~14 characters); **Implementation/Impact** (Recommendation slides under `Implementation`, Feasibility under `Impact`, same order). Write the answer into section 0.
Add any other real fork (placement in an existing deck, conflicting figures, scope) to the same round; default the rest.

**The brief beats sizing.** A fixed main-slide count or required topics: build exactly that, map every topic, the rest to the appendix. If the executive summary doesn't fit, the "We recommend ..." sentence becomes the title-slide subtitle, word for word on the closing slide.

Otherwise size by length: minutes ÷ 1.5 to ÷ 1.25 main slides, rounded (10 min → 7-8, 15 → 10-12, 20 → 13-16; the auditor checks the same range). Executive summary and recommendation slide count; title and appendix don't. Tight on slides: merge financial impact and risks into one Feasibility slide first, then move Analysis detail to the appendix. Analysis and Strategy never share a main slide, and the recommendation is never cut. With four main slides or fewer, Recommendation and Feasibility may share the closing slide: it carries the "We recommend ..." banner first, then the headline numbers, the partner line, risks and next steps in compact tiles with their detail in the appendix, and its tracker shows Feasibility (the closing slide's section). Nobody to ask: 15 minutes, research allowed, standard labels; say so at delivery.

## 0a. Part mode (one member's slides)

- **Questions (same round)**: which slides and your name (default from the team split and member brief; confirm only); a base deck to match (optional: read palette, font, title frame, tracker from it).
- **Without a game plan**: say once that parts without a shared storyline and numbers clash at the merge and offer case-study-analysis-gameplan. If the user goes ahead, ask for the exact action titles and key numbers, build only those, list the risk at delivery.
- **Builds**: the assigned main slides with their exact titles, plus their backing appendix slides. **Not** the frame slides (title, executive summary, Recommendation & next steps, Sources) unless this member owns them. Main slides carry the tracker with the right phase active.
- **Style**: the plan's Style line, else the base deck's, else the house style from the case brand (section 4). Never a different palette.
- **Numbers** only from the plan's Numbers; a missing one: compute with source, use it, list it under "New numbers" at delivery.
- **Appendix numbering**: the plan's A#, else member initials (`A-AS1`); the merger renumbers.
- **Sources**: proof per 8a; `Source:` lines on slides, full entries in `COBE_<Case>_Sources_<Name>.md` (8a format + slide supported), no Sources slide.
- **Notes and Q&A for own slides**: `COBE_<Case>_SpeakerNotes_<Name>.docx` (the section 9 briefing format for this member's slides, ending with the handover line) and `COBE_<Case>_QA_<Name>.docx` (3-5 questions).
- **Checks**: skip title-first, all-13-steps, slide count and the first/last "We recommend" match; everything else in section 8 applies. Run `python <auditor-skill-dir>/scripts/audit_pptx.py COBE_<Case>_Part_<Name>.pptx --part` and clear its blockers.
- **File**: `COBE_<Case>_Part_<Name>.pptx` (first name, no spaces; the one name exception). No PDF unless asked.
- **Delivery**: slides and appendix built (number + title), new numbers, dependencies on others' slides, weak sources. End: "Next: case-deck-merger combines everyone's parts into one deck. Run it when the other parts are ready?"

## 0b. Skeleton mode (team base deck)

- **Builds**: title slide, executive summary, Recommendation & next steps, Sources (the plan's verified sources), plus one example content slide per section and one appendix slide, each with its real action title and the full frame (accent bar, logo, tracker, appendix footer, palette, font, icons). The examples show members the box and chart look; they're replaced at the merge.
- **Style**: the plan's Style line exactly. **File**: `COBE_<Case>_Skeleton.pptx` only (no PDF, notes or Q&A).
- **Checks**: section 8 on the slides built; skip slide count and all-13-steps.
- **Delivery**: say who should match it, then "Next: build your own part (case-study-ppt, part mode) or wait for the parts; then case-deck-merger merges them on this skeleton."



## 0c. Sample slides first (default for every whole deck)

Palette, density and visual style are the expensive things to change late, so the user sees them on three real slides before the rest is built.
- **Build**: the title slide, one Analysis slide with a native chart and one pillar slide, with their real titles, numbers and the full frame (accent bar, logo, tracker, palette, accent, font, icons). Render them.
- **Send** `COBE_<Case>_Sample.pptx` and the three PNGs, with any image prompts (4d) in the same message, then one question (question tool): **"Does this look right?"** with "Yes, build the rest (Recommended)", "Change something" (colours, density, style, chart look) and "Different direction". Apply every correction to the whole deck, not just the samples; a change to the Style line is written into game plan section 0.
- **Team cases with separate files**: the approved sample grows into the skeleton (0b), so the look is built once.
- **Skip it** in a no-interruption run, when the user says to build straight through, in part mode (the base deck or Style line already sets the look), and when adding slides to an existing deck.

## 1. The 13 steps and where they show up

The game plan has worked out all 13 steps; the deck must cover every one (checked in section 8).

| Section | Steps | In the deck |
|---|---|---|
| **Analysis** (→ one main challenge or opportunity) | 1 Understanding the case; 2 Company (internal abilities, financial baseline: revenue, profit, cash, debt); 3 Environment (macro, then micro: market, competitors, customers, personas, journey); 4 Problem (root cause) | Main slides ordered macro → micro → internal, each with a conclusion bar; frameworks and detail in the appendix |
| **Strategy** | 5 Alternatives; 6 Chosen strategy, "We recommend ..."; 7 Pillars (2-4); 8 Storyline (the slide plan, not a slide) | Decision-tree main slide (chosen and rejected branches, one-line kill reasons), then the recommendation and its pillars; scored comparison in the appendix |
| **Recommendation** | 9 Detailed actions per pillar; 10 Creative elements (strategy name, mock-ups, a use case per pillar) | At least one main slide per pillar, each illustrated (mock-up, annotated image, process) with a **best-practice use case** (company, result number, verified source); the strategy name early and again at the close |
| **Feasibility** | 11 Timeline (3-phase or Gantt); 12 Risks (matrix + mitigation each); 13 Financial breakdown and impacts | Timeline, risks, financials, hard and soft KPIs, ending with Recommendation & next steps; full model and Balanced Scorecard map in the appendix |

With pillar-name labels the Recommendation section splits into one segment per pillar; with Implementation/Impact, Recommendation shows `Implementation` and Feasibility `Impact`.

## 2. Storyline and deck order

0 **Title slide** (2a) · 1 **Executive summary** (no tracker) · 2 **Analysis** · 3 **Strategy** · 4 **Recommendation** · 5 **Feasibility**, ending with **Recommendation & next steps** · 6 **Appendix** (detail, calculations, frameworks, sources).

- **Storyline first**: lay the action titles out as the plan's McKinsey-12 grid (Analysis | Pillar 1 | Pillar 2 (| Pillar 3) | Feasibility, ~3 each); read alone, they must tell the whole story. 12 is the method, not a slide count.
- **Phase tracker** (section 5) on every main-body slide, current section highlighted, with the section 0 labels. Appendix slides get the Appendix footer instead; title and executive summary get neither.
- **Answer up front, close with it**: the executive summary states the answer as one bold "We recommend ..." sentence; the last main slide (**Recommendation & next steps**) repeats it word for word in a PRIMARY-filled banner, with the 3 headline impact numbers and 3 next steps (what, who, when).
- **Show the decision, not the debate**: the decision tree uses the plan's kills (check for chosen, cross plus one-line reason for rejected).
- **Financial breakdown**: open with the investment against the plan's baseline (investment vs cash and yearly cash flow, funding route, net debt after), the judges' first question. Then say which approach: **bottom-up** (waterfall of the main cost drivers + 3-4 assumption tiles: price, volume, unit cost, breakeven; optionally cash in vs out per year with the breakeven year) or **top-down** (3-4 tiles such as WACC, growth, share reinvested + results by segment over time, or a waterfall from EBITDA to cash flow). Multi-year cash flow, breakeven and NPV when the data supports them; full model with best/base/worst in the appendix. Then a **hard KPI** slide and a **soft KPI** slide (or one slide when tight). Appendix: a **With vs without the strategy** slide of its own (the baseline if nothing is done against the plan, per year; for a launch the cannibalisation assumption and the rate at which the case breaks; never just a row on another slide), the Balanced Scorecard map and a **Financial baseline** slide (revenue, profit, cash, debt, net debt over recent years, with the statement behind each).
- **Executive summary layout**: four stacked rows, icon + label left (`Challenge`, `Strategy`, `Solution`, `Impacts`): the challenge as a one-line question in a light box, the bold "We recommend ..." sentence, 2-4 side-by-side neutral boxes of a few words (the pillars), 3 big numbers (24-28pt bold) with short labels.

## 2a. Title slide (always first)

PRIMARY accent bar on the left, about the height of the title block, vertically centred with it. Case company logo large, top right or centred above the title. Title: case name or question, 36-40pt bold, left-aligned, near-black. Subtitle: one line, 20-24pt (e.g. "Case study presentation" or the strategy's creative name). Bottom left, 16pt: `COBE`, the date, presenter names with their part ("Anna – Analysis") if given: the team introduction the notes open with. No tracker, slide number or other content. Add one when an existing deck lacks it.

## 3. Clean main slides, detail in the appendix, notes in separate files

**The .pptx contains no notes of any kind**: no `slide.addNotes()`, presenter cues, "see appendix" pointers, comments or hidden text. Existing notes: copy them into the notes file, then strip them from your copy with `remove_notes` from `case-study-fixer/scripts/pptx_edit_helpers.py`.

**Main slides** (projected; the presenter talks, the slide shows the point):
- One message per slide, carried by the action title: insightful, relevant, short, punchy; passes "So what?"; a declarative insight ("Converting long-haul flyers to domestic is the key to sustainable growth"), not a topic, a bare fact, an instruction or a long if-then. One line, ~60 characters.
- **Analysis slides end in a conclusion bar**: one line with the implication for the decision, not a repeat of the title.
- About 40 body words (title and tracker excluded; 60 on the executive summary and the Recommendation & next steps slide) is a **guide for a clean look, not a rule**. Judge the rendered slide: if it reads at a glance and nothing is crowded, the count doesn't matter; if it looks dense, cut or move detail. The scripts print the count as a note and never block on it.
- Boxes: a heading and 1-2 bullets of ~8 words; with 3-4 boxes, one phrase or one number + label each. No paragraphs.
- Show results, not workings (headline number, chart, ranking). Leave white space.

**Appendix has no slide limit, ever.** Never cap, merge or drop appendix slides to keep the deck short; only main slides are counted (section 1 sizing). **Every claim, number, chart, framework, precedent, risk and KPI on a main slide must have backup in the appendix**: before finishing, list each main slide's facts and check each has an A# slide with the calculation, source, full table or detail behind it; add as many appendix slides as that takes (one topic per slide, split rather than shrink). Appendix slides need the same design care as main slides (tables or charts, no walls of text), 14pt minimum.

**Appendix**: calculations and models (formula chains, full tables, best/base/worst), where each driver comes from, the alternatives comparison, extra facts, competitor detail, sources. Number titles `A1`, `A2`, ... in story order. **Name frameworks in the title** (`A2 – Porter's Five Forces: low switching costs, high rivalry`). 14pt minimum: split a slide rather than shrink. End with one Sources slide (8a). Keep the conclusion on the main slide, the evidence in the appendix (main: "550 new restaurants, +$3.9B sales/yr" with a bar per region; appendix: the traffic x capture x check x days table and the capture-rate source).

## 3a. Own words, no AI tone

The auditor blocks copied and AI-sounding text. **Never copy 7+ consecutive words** from the case or a source (quote only when wording matters, in quotation marks with the source). Every claim gets a number, a case fact or a concrete action; at most one em dash per slide; avoid the tells in `case-study-auditor`'s `references/ai-tells.md` ("not just X, but Y", "..., ensuring ...", inflated vocabulary, rule-of-three everywhere). Same for notes and Q&A.

## 3b. Nothing in the deck argues against the recommendation

- **No slide, main or appendix, shows another option ahead of the recommendation**: no margin table, scorecard, chart or price breakdown where an alternative, or a variant of the recommended option, comes out better. That includes numbers that merely sit side by side (a rejected option's higher margin in the next column).
- **Default: leave an unfavourable comparison off the slides** and keep it in the Q&A file with its prepared answer and backup slide.
- **It may be shown only when the game plan's "Where alternatives win" row is marked for a slide**: its one-line reason passed the four checks (evidence with a reference; changes the verdict in numbers; survived a red-team attack; fits one line). The slide's title or conclusion bar then carries that line.
- **Found while building** (a model output, a new table): don't hide it and don't build around it. Stop and offer case-study-analysis-gameplan Stage 5; in a no-interruption run apply stress test 20 yourself, take the stronger option if the reason fails, and say so at the top of the delivery.
- **One argument everywhere**: a kill reason, precedent or claim reads the same on every slide, in the appendix, the notes and the Q&A. A scored comparison shown anywhere ranks the recommendation first with the plan's own weights.
- **Partners**: every pillar that needs another company's yes carries the plan's "what's in it for them" line; the Partners table is an appendix slide.

## 4. Palette and font

Take it from the game plan's Style line. Without one, derive it: a quick web check of the company's official brand colours and current marketing (site, campaigns, social) decides PRIMARY; the logo in the case PDF is the fallback. Only these five roles plus white and near-black text, and the optional accent below:

| Role | How to derive | Used for |
|---|---|---|
| `PRIMARY` | brand's main colour | title accent bar, key boxes (white text), table headers, highlighted chart series, icons |
| `PRIMARY_DARK` | PRIMARY, HSL lightness −12 points (same hue/saturation); if PRIMARY's lightness < 25%, = PRIMARY | active tracker segment and label |
| `OUTLINE` | PRIMARY, HSL lightness +5 points | 2.25pt solid box outlines |
| `MID` | RGB 55% PRIMARY + 45% white (c x 0.55 + 255 x 0.45) | dashed outlines, secondary series, highlighted cells |
| `NEUTRAL` | PRIMARY's hue, lightness 86.5%, saturation = min(PRIMARY's, 22%) (tracker base line variant: lightness 78%) | light boxes with dark text, totals rows, non-highlighted series, tracker base line |

White on PRIMARY must reach 4.5:1; if not (yellow, light green), near-black text on PRIMARY boxes. Compute all five with `python <skill-dir>/scripts/palette.py <PRIMARY hex>` (prints the contrast too) and write them into the plan's Style line. Reference only, never reuse: Deck B used E51636 / C00000 / E5354F / E47482 / E3D3CF and D5C6C1 (hand-picked; the formulas give MID F17F90, NEUTRAL E4D5D7).

**ACCENT (optional, only when section 0 names one)**: one secondary colour for key numbers, the chosen branch of the decision tree, KPI tiles and the one thing a slide must make pop. Never for body text, outlines or decoration, and never a second accent. If the accent on white is under 4.5:1, use a darker shade of it for text and a light tint (about 10%) for boxes; record all three in the Style line.

Font: the Style line's font for all text (default Avenir Next LT Pro for PowerPoint desktop, fallback Aptos; a deck presented or edited in Google Slides or PowerPoint Online uses the font chosen for that tool in setup); the sandbox render substitutes it, so leave ~10% spare width when judging one-line titles. Title 24pt, subtitle 20pt, main box text 16-18pt, box headings 18-20pt bold, appendix 14-16pt.

## 4a. Readability

| Text | Main | Appendix |
|---|---|---|
| Body, bullets, box text, table cells | 16pt | 14pt |
| Box / column headings | 18pt bold | 16pt bold |
| Chart, axis, value labels; tracker labels | 14pt | 14pt |
| Key numbers / KPIs | 24-40pt bold | 20pt+ bold |
| Source line, Sources slide (only exceptions) | 10-12pt | 10-12pt |

Near-black on white or NEUTRAL, white bold on PRIMARY; no grey-on-grey, MID-coloured text or light weights. Never autofit: set sizes, turn shrink-on-overflow off, cut words or move detail instead. Bullets wrap to 2 lines max; ~0.15 in padding inside boxes.

## 4b. Number format (everywhere: slides, charts, tables, notes)

- Currency symbol first, no space: `$7.7M`, `$1.2B`, `$850K`, `€3.4M`; one currency per deck (convert, rate in the appendix).
- `K`, `M`, `B`, capital, no space; one scale per figure and per chart or table (never `$0.9B` and `$900M`).
- 1 decimal for M/B on main slides, 2 allowed in appendix tables; whole percentages on main slides (`12%`), 1 decimal only to show a difference.
- Comma thousands, dot decimals, no spaces inside numbers (`1,500`, `$29,400`).
- Ranges with an en dash, no spaces (`10–15 min`); `~` for estimates.
- Units in the chart title or column header (`Sales ($B)`).
- Totals from unrounded values; if rounded parts don't add up, keep the computed total and note it in the appendix.
- One format helper in the build script (`fmtMoney`, `fmtPct`, `fmtInt`) for every number.

## 4c. Visuals (this skill's rules + the slide designer's toolkit)

The deck must come out designer-grade, so case-slide-designer never has to run afterwards. Its rules and tools are used here directly; `<designer-dir>` = that skill's folder. Where the two disagree, this skill's values win (the designer's own rule).

**Before building, read**: `references/visuals.md` (below); `<designer-dir>/references/design-rules.md` sections Icons, Charts, Layout variety, Anti-patterns and Restyle checklist; and in `<designer-dir>/references/deck-patterns.md` only the sections for the patterns this deck uses plus section 11 (flaws seen in real decks).

**Choosing a structure** (when the plan's Pattern column leaves room, or for appendix slides): plan or argument that builds step by step → **logic chain** (deck-patterns 2; read aloud, the bottom row is the whole argument); goal / problem / solution / impact → exec-summary rail (3); 2-4 parallel ideas → numbered insight columns with a conclusion box (4); inputs processed into outputs → input → engine → output (5); one theme with 4 drivers or barriers → hub and spoke (6); phases with dates and decisions → gantt with gates (7); KPIs by objective → KPI wheel (8); concepts as tiles → icon tile grid (9); locations → map + KPI tiles (10); plus the course patterns in visuals.md section 5 (decision tree, customer journey, device mock-up, build sequence, use case, financial waterfall, hard and soft KPIs).

**Choosing a chart (a guide to weigh first, not a rule)**: on any slide that shows numbers, first ask what the number must prove for the action title, then start from the chart below that proves it fastest. The plan's Pattern column, the house chart rules and the user's choice still win, and another chart is fine when it reads better; say why in one line. Adapted from SAP's "Selecting the right chart" series (People Analytics Report Stories, 2020).

| The message is... | Consider first | Watch out for |
|---|---|---|
| Comparison, few categories or periods | column; time left to right, ordered groups (age, size bands) in natural order | more than 6 categories: switch to bar |
| Comparison, many items, ranking, long labels | horizontal bar, sorted | unsorted bars hide the ranking |
| Totals plus their mix | stacked column; 100% stacked when only shares matter | at most ~4 segments, clearly different tints (PRIMARY / MID / NEUTRAL) |
| How a start becomes an end (bridge) | waterfall: start + drivers - drains = end (DP §17) | every step labelled; the total computed, not typed |
| Trend over separate points | line | an axis that doesn't start at zero says so |
| Trend in continuous data with a mix | stacked area | more than 3 series gets hard to compare |
| Two measures over time | column + line on a secondary axis | use sparingly; with a stacked column it is three messages at once: split it or move it to the appendix |
| Spread or distribution | histogram; box plot only in the appendix | box plots need statistics knowledge the jury may not have |
| A pattern across two dimensions | heat map in PRIMARY tints (light = low, dark = high) | never a rainbow scale |
| Relationship between two variables | scatter; bubble when a third measure (size) matters, e.g. market size vs growth vs share | label the dots that make the point, not all of them |
| Share of a whole | donut (max 4 slices, centre label) or 100% stacked bar; treemap for shares inside a hierarchy; Marimekko for a market map (segment size x share) | no pie (house rule) |
| One number against a target | big number or KPI tile; bullet chart (actual vs target band) | |
| A low-high range or estimate (e.g. 6-12 months, $350-700K) | one range bar (solid to the low end, lighter to the high end) or a shaded band | two separate bars for low and high read as two different things |
| Many attributes per option | Harvey-ball benchmark table on main slides; radar only in the appendix | radar skews towards outliers |

- **Is the chart enough?** A bare chart often doesn't carry the so-what. Add the one emphasis that does: the highlight bar (house rule), a dashed MID reference line for a target or benchmark (labelled), a min-max target band, the one bar or dot the title is about in PRIMARY, or a CAGR / difference arrow. One emphasis per chart, not all at once.
- **Audience check**: box plots, radar, dual axes and bubbles slow a jury of classmates. Show the takeaway on the main slide and keep the complex chart as appendix backup.
- **Tools**: pptxgenjs `addChart` covers column and bar (clustered, stacked, 100%), line, area, doughnut, scatter, bubble and radar, and combos. Waterfall, heat map, treemap, Marimekko and bullet charts are built from shapes (or a stacked bar with an invisible base), with the numbers in an appendix table so they stay editable.
- **For the auditor and fixer**: a chart that fits the message worse than the table's suggestion is a **Minor** issue with the better chart named; **Major** only when it hides or misstates the message (a pie for a trend, a truncated bar axis, a combo nobody can read). Never deduct just for not following this table.

**Content rules learned from the user's corrections**: no secondary metric next to the primary one; no bullets that restate the title or subtitle; bare results ("550 new restaurants"), not symbol clutter ("= 550"), and let arrows carry the logic; drop empty boxes; at most 3 short bullets per box; one icon per concept, never decorative; never two charts on one slide unless they answer one question; no shadows, gradients, clip art, WordArt or decorative stock.

**Tools**: icons from the designer's Lucide library (1,544 line icons): find with `python <designer-dir>/scripts/icons.py <keywords>`, render a recoloured PNG with `from icons import render; render("<name>", "<PRIMARY hex>")` and place it with `addImage`; one library per deck (needs `pip install --break-system-packages cairosvg` if the import fails). A US map: build that slide with the designer's deck-native mode (`HostSlide` on the built deck, `layout_from` a sibling content slide, `draw_us_map`, `copy_tracker`), then put it in its position and re-render. Same for any slide added to an existing deck (section 8). **Inserting a one-slide file** (`save_single` output): copy the deck, then run case-deck-merger's `python <merger-dir>/scripts/merge_decks.py --base <copy> --order order.json --out <deck name>`, with `order.json` listing every slide of the copy in order and the one-slide file at its position (`{"deck": "<file>", "slide": 1}`); it keeps masters, charts and images. Re-render after. Once the deck has been audited, adding or replacing slides is a case-study-fixer job (new version, re-audit).

Also from `references/visuals.md`: one icon style (line or glyph, Flaticon look), icons always labelled; real images and device mock-ups only when they carry content (no decorative stock, no clipart); think-cell elements (chevrons, numbered circles, Harvey balls, check/cross/warning marks, conclusion bars); native editable charts with one highlight colour, data labels, no gridlines; waterfalls for financial breakdowns. Pattern catalogue: its section 5 (Analysis: drivers + competitive landscape, STP/personas, customer journey with pain points, personas + journey vs competitor, adoption curve; Strategy: decision tree, profit/issue tree; Recommendation: pillar slide with use case, build sequence, device mock-up, best-practice use case; Feasibility: timeline, risk matrix, bottom-up/top-down breakdown, hard and soft KPIs, Recommendation & next steps; appendix: formula chain, alternatives table, model, Balanced Scorecard). Use the game plan's chosen pattern per slide; without a plan, vary patterns. No pattern on two neighbouring slides and none more than twice in the main deck; pillar slides each get a different pattern (never one template three times). If the plan's Pattern column breaks this, change the later slide and say so. Bar and column charts start at zero. Every slide needs a visual element. A custom pattern in the plan: build it as described in Key content, inside these design rules.

## 4d. AI images (the user generates them)

When a slide needs a generated image (product concept, shelf or store scene, title hero), you write the prompts and the user makes the images in Nano Banana. Never generate them yourself, fake them or skip them silently.
- **When**: with the sample slides (0c), before the full build. One message, one prompt per image, each in its own code block.
- **Each prompt**: the slide it is for and what the image must show; the aspect ratio of its box (16:9, 4:3, 1:1); the style (product photography, photoreal scene, clean illustration); the palette hex codes; **the plan's specifics word for word** (names, flavours, colours, counts: an image that contradicts the plan is a defect); "no other text" (generated small text comes out garbled, labels are added as real slide text); 2K or higher; the file name to send back (`img_<slide>_<topic>.png`).
- **Placing**: small and purposeful, never full-bleed except a title-slide hero; small enough that generation flaws don't show; real slide text for every label; source line `Concept visual`.
- **An image that differs from the plan** (other flavours, another name): ask which is right (the conflict rule) and update the plan; don't quietly remove the clashing detail.
- **No image yet** (not sent, or a no-interruption run): build the slide with an editable shape mock-up in the palette, and put every prompt in full, each in its own code block, in the delivery message itself under "Images to generate" (naming them in the game plan is not enough); the image is swapped in later as a fixer row. Never a placeholder box.

## 5. Slide frame (all slides except the title slide)

- **Title accent bar**: PRIMARY rectangle x 0, y 0.214, w 0.182, h 0.981.
- **Title**: x 0.182, y 0.214, w 11.0, h 0.51, 24pt, left, sentence case, one line (~60 characters; the auditor flags longer).
- **Subtitle** (optional): x 0.182, y 0.757, w 11.0, h 0.41, 20pt.
- **Logo**: top right, x ~11.32, y 0.214, h ~0.84, aspect kept.
- **Content area**: y 1.30-6.95, x 0.182-13.15 (with a source line, content ends at y 6.65).
- **Slide number**: bottom right, x 12.76, y 7.08, small.
- **Source line** (optional): x 0.182, y 6.70, w 11.0, h 0.25, 10-12pt, one line starting `Source:`; it sits above the tracker and the appendix footer (lower, it collides with their lines).
- **Phase tracker**: base line x 2.667, y 7.108, w 8.0, 3pt, NEUTRAL-dark; four labels w 2.0, h 0.34, y 7.128 at x 2.667 / 4.667 / 6.667 / 8.667, 14pt, centred (pillar labels: same 8.0 in line split into equal segments from x 2.667); active phase: 4.5pt PRIMARY_DARK segment over its 2.0 in and its label bold PRIMARY_DARK; others regular, dark.
- **Appendix footer**: full-width 3pt line at y 7.08 (x 0.74-12.6), centred bold 18pt `Appendix` in PRIMARY_DARK with a 4.5pt PRIMARY segment above it.
- **Name the frame shapes** so the scripts read the slide right: pptxgenjs `objectName` = `title`, `subtitle`, `source`, `page-number`, `tracker` (line and labels), and `chart-label` / `axis-label` for hand-drawn chart text. Big KPI numbers never start above y 1.30.

## 6. Box vocabulary

Rounded rectangles (default radius), four styles by meaning: (1) **Primary filled**: PRIMARY fill and line, white text: question banner, column headers, key takeaway, recommendation banner. (2) **Neutral filled**: NEUTRAL, dark text: context, facts, bottom summary. (3) **Solid outline**: 2.25pt OUTLINE, dark text: main content columns. (4) **Dashed outline**: 2.25pt MID dashed, dark text: alternatives, risks, secondary content, assumptions. Inner margin ~0.1-0.15 in; PRIMARY bullet character, ~6-8pt space before; bold lead-in phrase per bullet; size boxes to content (no tall half-empty boxes).

## 7. Slide patterns

In 4c (catalogue: `references/visuals.md` section 5).

## 8. Quality bar

- **Compute, don't type, numbers**: the model in the build script with `assert`s for totals and consistency, so slides, appendix and notes show the same figure; headline claims (breakeven year, payback period, totals) are written from the model's output, never typed. One benchmark everywhere, totals that tie, no outlier assumption silently driving the result; every driver explained in the appendix. Name metrics right (systemwide sales vs revenue vs profit; annual vs daily).
- **Research** (if allowed): verify current facts and add outside data; tiny `Source:` line on main slides, full references on the Sources slide; case data only → only the facts file. Every source through 8a.
- Slides in the deck's language (default English); translate, don't copy.
- **Never overwrite the user's file**; work on a copy (section 9 names). Adding to an existing deck: build new slides in its own master with the designer's deck-native mode (`python <designer-dir>/scripts/deck_native.py scan deck.pptx`, then `HostSlide`: its exact colours, font, tracker copy, slide-number field), insert main slides in the right phase and detail in the appendix (inserting one-slide files: see 4c Tools), leave other slides untouched.
- **Render and look** at every new slide (PDF/PNG): no crowded or dense-looking slide (the word count is only a hint), no body text under 16pt (chart and tracker 14pt, source 10-12pt), one-line titles, no overflow or half-empty tall boxes, charts without gridlines or stray legends, one icon style; appendix ≥14pt. Scan the XML for `sz` below minimums and `normAutofit fontScale`. Also check: every link passed 8a; Sources fits one slide; **no speaker-notes text in the file** (pptxgenjs writes empty notes parts by itself: after the build run `remove_notes` from `case-study-fixer/scripts/pptx_edit_helpers.py` on the deck and confirm `audit_pptx.py` prints no speaker-notes line); title slide first; all 13 steps covered (main or appendix); conclusion bar on every Analysis slide; decision tree in Strategy; illustration and use case per pillar; slide count fits; numbers per 4b; the same "We recommend ..." on the executive summary and the last main slide; nothing that shows an alternative ahead of the recommendation (3b); no date before the timeline anchor; bar and column charts starting at zero; no pattern on neighbouring slides. Fix before delivering.

## 8a. Sources

Judges click links. Proof every source (Sources slide, slide text, XML hyperlinks, notes, Q&A): open each, keep only specific pages that support the claim, rate the tier and upgrade weak ones, clean links, one alphabetical Sources slide. Procedure, tiers and format: `references/sources.md`; read it before any Sources slide or source line.

## 9. Deliverables and names

Every file starts `COBE_<Case>` (short, no spaces); no team names or numbers (exceptions: part files, `_Skeleton.pptx`).
1. `COBE_<Case>.pptx`: the deck, no notes.
2. `COBE_<Case>.pdf`: export via the pptx skill's `soffice.py`.
3. `COBE_<Case>_SpeakerNotes.docx`: **a briefing, not a script**. The presenters speak freely; the notes exist so every teammate understands the strategy and knows what to cover. Opens with a **presentation plan** (purpose: convince the client to act; likely jury: academics, case-company members, industry experts, and what each cares about; the team intro line; minutes per section as a guide; who presents what). Then one section per slide (number + title, presenter name): **The point** (what this slide proves, one line); **Why it's true** (the reasoning in plain language, so someone who didn't build the slide could explain it); **Must mention** (2-4 topics); **Numbers to know** (each key figure, what it means, its unit and where it comes from, with terms such as fiscal years explained); **Likely pushback** (the question this slide invites, with its `Backup: A3` slide); **Handover** (one line to the next presenter). No word-for-word script and no words-per-minute target.
4. `COBE_<Case>_QA.docx`: opens with the **Q&A protocol** (who takes which topic, one answer per question, no "may I add" chains, confirm feedback-style questions first, no "great question", patient and factual, never contradict a teammate). Then 8-10 likely questions (weakest assumption, "why not Y?", risks, financials, feasibility), each with a 20-30 second answer, the backing appendix slide, lead and backup answerer (team), and the jury persona (the Feedback-giver, the Skeptic, the Curious expert, the Forgetful juror, the Impact-focused juror).
5. **Extra deliverables** listed in game plan section 0 (usually a one-page Word executive summary): build each from the game plan with the docx or xlsx skill, with the same numbers and "We recommend ..." sentence, named `COBE_<Case>_<Item>.<ext>`. Nothing listed: build none and don't offer any.

.docx files via the docx skill, plain. Adding to an existing deck still yields v1: save as `COBE_<Case>.pptx`, never touch the upload; if it already has that name, copy it to `COBE_<Case>_Original.pptx` first and say so. Nothing unfinished: no placeholders (`[link to add]`, TBD, XX), empty cells or sources without a working clickable link (the case excepted). Anything open: **NOT READY TO SUBMIT** at the top of the delivery message with the items.

## 9a. Final export (last step)

Export the PDF from the final .pptx and check every delivered file opens.

## 10. Workflow

0. Settle what to build (section 0, question 0); part → 0a, skeleton → 0b; the steps below apply to those slides only.
1. Read the game plan (else "Without a game plan"); ask only the section 0 questions it leaves open, in one round. Note any fixed slide count or required topics. Copy its Numbers into the build script's asserts.
2. Palette, accent and font from the Style line (else per section 4), logo (`pdfimages -png` on the case PDF, or the user's file; never drawn; none → build without, say so), icon style; read the design sources in 4c (visuals.md, the designer's design rules and the deck-patterns sections this deck uses).
3. Sample slides first (0c) together with the image prompts (4d); after the user's yes, work on a copy: title slide, then lean main slides (native charts, design elements, icons, format helpers, chosen patterns, no notes), then the appendix. Proof sources (`references/sources.md`), build the Sources slide. Validate (`validate.py`), render, and inspect every slide as a viewer would, 2-4 passes: wrapped single words, labels touching edges, sibling boxes of different sizes, icons that don't read, empty zones, the same layout twice in a row. Run `python <designer-dir>/scripts/check_deck.py COBE_<Case>.pptx --fonts "Avenir Next LT Pro,Avenir Next LT Pro"` (or `--fonts safe` for Aptos) and clear what it reports (word-count lines are notes, not problems; it uses the same slide detection as the auditor's script). Run `python <auditor-skill-dir>/scripts/audit_pptx.py COBE_<Case>.pptx --minutes <N> | --main-slides <N> --case-title "<case title>"` and clear every blocker and any "We recommend" mismatch.
4. Export the PDF; write the notes and Q&A files. Re-run the script with `--extra <notes> <QA>`, and `python <auditor-skill-dir>/scripts/overlap_check.py <file> case.pdf` on the deck, notes and Q&A; fix everything.
5. Final export (9a), build any extra deliverable from section 0, deliver the files (with the image prompts in the message when any image is still a mock-up), offer the next step (a no-interruption run goes straight on to case-study-auditor and delivers once at the end; otherwise: "Next: case-study-auditor grades the deck like the professor and lists every fix. Run it now?"; teammates building separate files → "Next: case-deck-merger combines everyone's slides into this deck's style. Run it when their files are ready?"), and list briefly: main-slide count vs length, what the deck covers, the assumptions that matter most, sources replaced or flagged, figures to double-check.