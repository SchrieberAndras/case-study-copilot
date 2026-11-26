---
name: "case-deck-merger"
description: "Merge a team's case slide files into one consistent COBE deck (one style, one storyline, one set of numbers, one Sources slide, merged notes and Q&A), or check and restyle one shared team deck. Use whenever the user has several members' .pptx parts to combine, or a downloaded shared Google Slides / PowerPoint Online team deck to clean up. Asks before handing over to the auditor, unless the user asked for a no-interruption run."
---

# Case deck merger

Team cases arrive as several files: each member built their part in their own style. Graders see one presentation, so it has to read as one: one look, one storyline, one set of numbers, one sources slide. This skill does the merge and only the merge. Grading and content fixes belong to the auditor and the fixer.

## Case pipeline

Chain: case-study-analysis-gameplan (1) → case-study-ppt (2) → case-deck-merger (2b, team decks only) → case-study-auditor (3) → case-study-fixer (4); steps 3-4 repeat until READY TO SUBMIT. The full table of who owns and hands over what is in `case-study-analysis-gameplan` ("Case pipeline"). Rules (a copy of case-study-analysis-gameplan's "Handoff rules"; change them there first, then here):
- Each step does only its own job; for anything another step owns, hand over.
- Finish with one line: "Next: <skill> – <what it will do>. Run it now?" On yes, load it with the Skill tool and pass every file so far; in a new chat, list the files to attach.
- **Always confirm before moving on**, including calls inside a skill's own flow (compressed mode, pre-audit, re-check). Unattended runs stop at the offer. The one exception is a no-interruption run (next rule).
- **No-interruption run** (the user says "just build it", "just run it" or "run with no interruptions"): the chain runs to the end without a stop. It starts from the user's game plan, or from case-study-analysis-gameplan when there is none (full analysis, council at graded size, your recommended strategy, named at the top of the delivery). No sample-slide stop, no "Run it now?", no approval questions: take the recommended option each time and list every such choice at the end so the user can reverse it. Then build → one full audit → one fix pass → one light re-check → deliver once. Image prompts go out with the delivery (shape mock-ups in the deck until then). Only what the user alone can supply (a case fact that changes the recommendation, a private file, real presenter names) stays open: finish everything else and deliver NOT READY TO SUBMIT with it on top.
- **The audit loop is capped.** One full audit, one fix pass, one light re-check (numbers, look, feasibility; case-study-auditor section 5a), at most one more fix pass, then deliver with anything still open on top. "Fix everything, don't re-audit" skips the re-check. A full independent re-audit runs only when the user asks for it by name.
- **Conflicts get asked.** When something the user supplies (an image, a file, a number, a team decision) differs from the game plan, ask which is right and write the answer into the plan; never work around it silently. In a no-interruption run follow the user's newest input and list the conflict at the end.
- Nothing is re-asked downstream: setup answers (length, presentation date, time limit, timeline anchor, research, team and presenter names, build mode, section labels, brief constraints, case file and title, frame-slide owner, Style line with accent and font) live in game plan section 0, the merge log and the audit's Context block.
- Nothing is lost: every file carries forward (case PDF, facts file, brief, game plan with change log, deck, notes, Q&A, merge log, latest audit, calibration record). If one is missing, say which and continue.
- **Case source: `COBE_<Case>_CaseFacts.md`**, never the case PDF's text. The PDF is carried forward for the auditor, not read. A fact missing from the facts file: tell the user; if it changes a number, a target or the recommendation, stop and offer case-study-analysis-gameplan Stage 5 (the fact is added there); otherwise use a labelled assumption. Never open the PDF to look unless the user says so.
- **The game plan stays current.** Only the user decides changes. A step applying an approved change to the recommendation, a number, a target or the storyline also updates the plan and adds a section 16 Change log row (what, old → new, who approved). Logged changes are approved, not drift. A step that finds an error without approval stops and tells the user.
- **Versions.** The first complete deck is v1 (`COBE_<Case>.pptx`), whichever step produced it, never `_v2`. If an input already has that name, copy it first (merge base → `COBE_<Case>_Skeleton.pptx`, shared-deck download → `COBE_<Case>_Download.pptx`) so the output takes the plain name. Only the fixer produces `_v2`, `_v3`, ...; an audit is numbered by the deck version it grades (`_Audit_v1` for v1).

## 0. Mode and inputs (ask in one round only for what's missing)

**Mode first.** Read it from the game plan's "Build mode" line. Without one: several .pptx files → **merge mode**; a single deck, or the user says the team works in one shared deck → **shared-deck mode** (section 0a). Ask only if still unclear.

Merge mode inputs:
- **Every member's .pptx** and who made each one (owner names). Part files from case-study-ppt's part mode are named `COBE_<Case>_Part_<Name>.pptx`: take the owner from the name and also use their `_Sources_<Name>.md`, `_SpeakerNotes_<Name>.docx` and `_QA_<Name>.docx`.
- **Base deck**: whose style wins. Default: the whole deck or skeleton built by case-study-ppt, else the deck with the title slide, else the part covering the most main slides. Say which you picked. When the game plan has a Style line, it beats the base deck on palette, font and icon style. If the base deck (or any member file) is already named `COBE_<Case>.pptx`, copy it to `COBE_<Case>_Skeleton.pptx` (a member file: `COBE_<Case>_Part_<Name>.pptx`) and use the copy: the merged output must take the plain name as v1, or the audit and fix numbering is off by one. The script refuses to write over any input.
- **Frame slides** (title, executive summary, Recommendation & next steps, Sources): their owner is named in game plan section 0 and the team split. Take them from that member's file; without an owner, from the base deck.
- **Game plan** (`COBE_<Case>_GamePlan.md`): its storyline gives the slide order, its Numbers section is the truth for conflicts, its team split says who owns which slide. Without one, ask the user to confirm the slide order you propose.
- Case facts file `COBE_<Case>_CaseFacts.md` (it carries the brief word for word, for the fixed main-slide count, and the case numbers for conflicts the game plan doesn't settle). Without it, the brief file; never read the case PDF.

## 0a. Shared-deck mode (team built in one live deck)

The scripts work on local .pptx files; they cannot edit Google Slides or PowerPoint Online live. So:

1. **Freeze, then download.** Save the download as `COBE_<Case>_Download.pptx` and leave it untouched, then make the working copy `COBE_<Case>.pptx` from it, so the output takes the plain name. Tell the user, in short bullets: ask the team to stop editing, then download a copy (Google Slides: File > Download > Microsoft PowerPoint; PowerPoint Online: File > Save As > Download a copy) and attach it. Edits made in the live deck after the download are not included; record the download time in the merge log.
2. **Owners**: take who built which slides from the game plan's team split; if missing, ask once. If nobody knows, leave owners blank.
3. **No merge, only form.** Treat the working copy `COBE_<Case>.pptx` as both base and input (no `merge_decks.py` run is needed): run the inventory on it, then fix consistency across members' slides (section 3 steps 3-5: restyle to a reference content slide, align body layout, apply agreed numbers, merge duplicate Sources slides into one). Drop duplicate slides only with approval.
4. **Deliver** `COBE_<Case>.pptx` (= v1; the download stays untouched as `_Download`), the merge log with `Mode: shared deck` and the download time, and the next-step offer to the auditor.
5. **Getting it back to the team**: tell the user to upload the final file to the shared folder as a new file (or import its slides into the live deck), and that teammates should work from the new version from now on. Don't use the browser or connectors to overwrite the live deck.

## 1. Inventory

```bash
python <skill-dir>/scripts/inventory_decks.py base.pptx anna.pptx bence.pptx --json inventory.json
```
It lists, per deck: slide size, fonts and colours used, titles, word counts, numbers, links, notes. Across decks: likely duplicate slides and the same label with different numbers. Then render every deck (`soffice.py` → PDF → `pdftoppm`) and look at them.

## 2. Decide (show the user one short plan before merging)

- **Order**: one entry per final slide, following the game plan storyline (title, executive summary/answer, Analysis, Strategy, Recommendation, Feasibility, Recommendation & next steps, appendix, one Sources slide last). Every member slide carries the tracker labels from game plan section 0 (standard, pillar names, or Implementation/Impact); fix mismatches. Same-title build sequences stay together in order. Members' own title slides, agenda slides and sources slides are dropped (sources get consolidated).
- **Duplicates**: two members built the same slide → keep the stronger one (clearer action title, better evidence, fewer words) and say which; move unique content from the other into it or the appendix.
- **Number conflicts**: the game plan's Numbers section wins. Without a game plan, or if both differ from it, ask (one question, all conflicts together). Every occurrence gets the agreed value, including notes. A value the user chooses that differs from the game plan is also written into the game plan (Numbers section plus a change-log row); deliver the updated plan with the merge.
- **Missing slides**: storyline or brief items no member covered. Don't invent content; list them as open and offer case-study-ppt to build them. Part files have no title slide, executive summary, recommendation slide or Sources slide unless one member was assigned them: take them from the base deck; if none exists, list them as missing and offer case-study-ppt in skeleton mode (its section 0b), which builds exactly these frame slides. The Sources slide is the exception: build it here from the members' sources (step 5).
- **Appendix numbering**: renumber all appendix slides A1, A2, ... in final order (part files may use initials like `A-AS1`), and update every `Backup: A#` pointer in the notes and Q&A to match.
- **Colour map**: member brand colours → base palette (from the inventory's colour lists), and the base font. The Style line's accent colour stays as it is; a member's own extra colours map to the palette.
- **Clashing arguments**: two slides that give different reasons for the same decision, or a member's table or chart that shows another option ahead of the recommendation (case-study-ppt 3b). Don't pick silently: name them in the plan you show the user and list them in the merge log as open items for the auditor.

Ask for approval only where a choice changes content (duplicates with different content, conflicting numbers, missing slides); apply the rest.

## 3. Merge

1. Write `order.json`: `[{"deck": "anna.pptx", "slide": 3, "owner": "Anna"}, ...]` and `colors.json`: `{"E5163A": "1F2A44"}`.
2. Merge (output is always `COBE_<Case>.pptx`; if an input has that name, copy it away first as in section 0):
```bash
python <skill-dir>/scripts/merge_decks.py --base base.pptx --order order.json --out COBE_<Case>.pptx --font "<base font>" --colormap colors.json
```
   It keeps the base deck's masters and theme, copies each slide's shapes with images, charts (and their data), tables and hyperlinks, refuses to overwrite any input file, and, because the house rule is no notes inside the deck, leaves every slide's speaker notes out of the .pptx and writes them to `COBE_<Case>_member_notes.md`, scales slides of a different size to fit, gives member slides the base background, applies the font and the colour map to slide shapes and tables (not inside charts: `restyle_like_base.py` recolours charts), renumbers slide-number boxes, and prints the origin table plus warnings (SmartArt, video, OLE, slide-to-slide links need a manual check).
3. Restyle the member slides to match a base content slide:
```bash
python <skill-dir>/scripts/restyle_like_base.py COBE_<Case>.pptx --ref <base content slide #> --slides <member slide #s> [--table-ref <base slide with a table>] [--highlight <series #>] [--primary <game plan PRIMARY hex>] --out COBE_<Case>.pptx
```
   Title position/size/colour, accent bars and logo, slide numbers, table header style, chart colours (no gridlines, data labels; in multi-series charts the highlight series, default the first, gets PRIMARY and the others a light NEUTRAL tint; pass `--neutral <hex>` to use the game plan's exact NEUTRAL). When the game plan has a Style line, always pass its PRIMARY with `--primary`; otherwise the script detects the most used saturated colour. Body layout is not touched.
4. Body clean-up with the fixer's helpers (`case-study-fixer/scripts/pptx_edit_helpers.py`: `map`, `move`, `set_paras`, `set_cell`, `font_size`): align member content to the base content area and margins, fix overlaps, apply the agreed numbers, apply the base's text sizes (case-study-ppt minimums: main 16pt, appendix 14pt). Follow case-study-ppt's style rules; keep the base deck's look.
5. **One Sources slide**: merge every member's sources (their Sources slides and any `_Sources_<Name>.md` files) into the base Sources slide, or a new one if the base has none, dedupe by URL, one format (case-study-ppt `references/sources.md`), clickable links (`link_urls`). A member source without a verifiable link: find it (search, open, confirm) or drop the claim it supports. Never leave a placeholder.
6. **Speaker notes and Q&A**: one `COBE_<Case>_SpeakerNotes.docx` in case-study-ppt's briefing format (presentation plan first: team introduction line, minutes per section as a guide, who presents what; then per slide the point, why it's true, must mention, numbers to know, likely pushback, handover), presenter name per slide from the origin table; one `COBE_<Case>_QA.docx` merging members' Q&A (dedupe), with the Q&A protocol and a lead answerer and backup per question from the team split. Use the members' `_SpeakerNotes_<Name>.docx` and `_QA_<Name>.docx` files where they exist instead of writing those parts again, and fold in any text from the `_member_notes.md` sidecar for slides whose notes only existed inside a member's .pptx. Build them with the docx skill. Notes never stay inside the .pptx.
7. Validate (`pptx` skill `validate.py`), render and look at every slide. Run `python <auditor-skill-dir>/scripts/audit_pptx.py COBE_<Case>.pptx [--minutes N | --main-slides N] --case-title "<case title>"` (it also prints the "We recommend" word-for-word check); fix every merge-caused blocker (placeholders, empty cells, unlinked sources). Then run `python <designer-dir>/scripts/check_deck.py COBE_<Case>.pptx --fonts <Style line font pair> --primary <PRIMARY> --accent <ACCENT | none>` (case-slide-designer's script, ending with the slop check): fix what the merge caused (an extra colour family from one member's part, the same layout twice in a row at a seam, mixed icon styles); list the rest for the auditor. Content blockers that existed in a member's slides are left for the auditor, but name them.

## 4. Deliver

- First export the PDF from the merged deck.

- Files: merged .pptx, PDF, speaker notes, Q&A, and `COBE_<Case>_MergeLog.md`: the mode (merge or shared deck, with the download time for shared), the origin table (slide → owner → source deck/slide), every decision (duplicates, number conflicts, colour map, dropped slides), game plan changes made, warnings, and open items. The auditor and fixer read it, so nothing decided here is lost.
- Message: readiness of the merge (open items first, bold), slide count vs the brief, what was dropped or changed, then the next-step offer: "Next: case-study-auditor grades the merged deck. Run it now?"

## Notes

- The merge changes form, not substance: no new analysis, no rewritten arguments. Weak content is the auditor's to flag and the fixer's to repair.
- Never overwrite members' files; they may still be editing.
- If a member's slides use a different language, translate to the deck's language and say so.