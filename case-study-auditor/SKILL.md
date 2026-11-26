---
name: "case-study-auditor"
description: "Audit and grade a business-school case deck like the COBE professor: score /100, every issue with an exact fix, READY / NOT READY TO SUBMIT, and a live jury Q&A drill on request. Use whenever the user asks to check, review, grade, rate or proofread case slides before submitting, wants to know what the professor will criticise, or says 'grill me' or 'practice the Q&A'. Also use for a design-only critique of a deck or named slides ('critique slide 5', 'does this look AI-made', 'design review'). Never edits the deck and never starts the fixer without the user's yes."
---

# Case study auditor

Grades a case deliverable the way a coursework professor would, against the course's case-solving standard (Executive summary, Analysis, Strategy, Recommendation, Feasibility), finds every problem, and tells the user exactly how to fix each one. Its value is finding what costs points **before** the professor does, so be honest: a flattering audit is worthless.

**This skill never edits the deck.** It recommends every fix with the exact change. When the user gives a command ("fix it", "fix the criticals", "apply 1, 4 and 7"), hand over to the `case-study-fixer` skill with the audit file; keeping auditing and fixing separate keeps the grade honest.

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
- **Case sources: the auditor is the one step that reads both** the case PDF and `COBE_<Case>_CaseFacts.md`. Every other step works only from the facts file, so checking it against the PDF is part of every audit. A fact missing from or wrong in the facts file is a fix row (section 2, Facts-file check).
- **The game plan stays current.** Only the user decides changes. A step applying an approved change to the recommendation, a number, a target or the storyline also updates the plan and adds a section 16 Change log row (what, old → new, who approved). Logged changes are approved, not drift. A step that finds an error without approval stops and tells the user.
- **Versions.** The first complete deck is v1 (`COBE_<Case>.pptx`), whichever step produced it, never `_v2`. If an input already has that name, copy it first (merge base → `COBE_<Case>_Skeleton.pptx`, shared-deck download → `COBE_<Case>_Download.pptx`) so the output takes the plain name. Only the fixer produces `_v2`, `_v3`, ...; an audit is numbered by the deck version it grades (`_Audit_v1` for v1).

## 0. Setup

Collect inputs. Ask in one round only for what is missing and matters:

1. **The deliverable** (required): .pptx preferred; a PDF of the deck also works (design checks become visual only).
2. **The case PDF and the case facts file** `COBE_<Case>_CaseFacts.md` (both strongly recommended): the PDF for fact checks and the copied-text check, the facts file because the deck was built from it. Say which is missing.
3. **Presentation length** in minutes, and the **brief or rubric** if the professor gave one (fixed slide count, required topics, criteria).
4. **Previous audit** (`COBE_<Case>_Audit_vN.md`) if this is a re-check, for progress tracking.
5. **`COBE_Calibration.md`** (the record of graded decks): if it isn't attached, ask for it once at the start of every audit; without it, say the grade is uncalibrated.

Also use, if present: the game plan (`COBE_<Case>_GamePlan.md`) with its change log, the merge log (`COBE_<Case>_MergeLog.md`), speaker notes and Q&A files. Changes in the game plan's change log and decisions in the merge log (dropped duplicates, chosen numbers, missing slides listed as open) are approved choices: don't report them as drift or defects, though open items in the merge log still count.

Extra deliverables listed in game plan section 0 or the brief (usually a one-page Word executive summary): check each exists and matches the deck's numbers and "We recommend ..." sentence; a missing one is a brief item (Critical).

If the user attached `COBE_Calibration.md` (section 6) with graded decks or a profile for this professor, apply it. Always apply the COBE course profile in `references/calibration.md` (the course's case-solving standard). Without graded decks, note in the report that the grade is an estimate.

## 1. Mechanical checks (run first)

For .pptx:
```bash
python <skill-dir>/scripts/audit_pptx.py deck.pptx [--minutes <N> | --main-slides <N from the brief>] [--case-title "<case title>"] [--extra notes.docx qa.docx gameplan.md] --json audit.json
python <skill-dir>/scripts/overlap_check.py deck.pptx case.pdf [other_source.pdf ...]
python <skill-dir>/scripts/overlap_check.py notes.docx case.pdf     # likewise for the Q&A file
python <designer-dir>/scripts/slop_check.py deck.pptx --primary <PRIMARY> --accent <ACCENT | none> --json slop.json
```
- `audit_pptx.py`: finds titles even when the deck uses plain text boxes instead of title placeholders (a shape named `title`, else the largest text starting in the top inch, so a big KPI number below it is never taken for the title), splits main vs appendix (titles starting `A1`, `Appendix`, or an `Appendix` / `Backup` label in the bottom band of the slide or its layout, including the typo `Appendi`), excludes footers/source lines from word counts, and prints **submission blockers** first. A title that *is* "Sources"/"Sources used"/"References"/"Bibliography" (optionally numbered, e.g. `A9 – Sources used`), in any top text box whatever its font size, marks the Sources slide, not any title containing the word; the Sources slide always counts as appendix. Part-file appendix numbering like `A-AN1` counts as appendix. The case itself needs no URL: it is recognised by a case number (`9B24M001`, `9-321-045`, `UV1234`), by a case publisher (Ivey, Harvard Business School/Publishing, The Case Centre, Darden Business Publishing, INSEAD, Kellogg School, WDI Publishing, McGraw Hill; or a `(Case MH0084)`-style number) together with the word "case", or by `--case-title` (always pass it). The bare word "case" or a company name such as Kellogg or Darden does not exempt a source line from needing a link. Add `--part` when checking one member's part file (skips the Sources, We recommend and slide-count checks). It compares the "We recommend" sentence on the first and last main slide that carries it (appendix slides are ignored) and prints `match`, `MISMATCH` (report as Major, Critical if the recommendation itself differs) or that only one slide carries it. Per slide: word count as a note (guide 40, 60 on a slide carrying "We recommend"; information only, never a blocker or an issue by itself), text below 16/14/10pt, shrink-to-fit, speaker notes left in the file, hyperlinks, number-format problems, "We recommend" locations, main vs appendix slide count vs length (consecutive main slides with the same title are one build sequence and count once; `--minutes`: minutes ÷ 1.5 to ÷ 1.25, the same range as case-study-ppt section 0; `--main-slides` for a fixed count in the brief). Empty-cell checks skip tables whose body is 75%+ empty (layout grids or backgrounds with text boxes on top). It also flags URLs typed as plain text (not clickable) and scans `--extra` files (speaker notes, Q&A, game plan) for placeholders. Citations like `[Source: AGF 2024]` or `[1]` are not placeholders. Treat output as leads, not verdicts (fonts inherited from the master show as unknown; check them visually).

For a **PDF deliverable**, run the same script on the .pdf: it switches to text-only checks (placeholders, sources without URLs, unclickable links, "We recommend"); judge fonts, word counts and layout from the rendered pages.
- `slop_check.py` (case-slide-designer's script; `<designer-dir>` = that skill's folder): the slide slop detector, P0-P3 per finding, with the design move that fixes it. Take PRIMARY and ACCENT from the Style line (game plan section 0 or the Context block). Its findings feed the design critique (section 2a).
- `overlap_check.py`: every passage of 7+ words identical to the case (or other sources passed in). Run it again with each speaker-notes and Q&A file as the first argument; never pass them as sources, that compares the deck with its own notes. Ignore hits on the Sources slide's own case citation line.

Then render every slide and **look at each one** (scripts cannot see design):
```bash
python <pptx-skill-dir>/scripts/office/soffice.py --headless --convert-to pdf deck.pptx
pdftoppm -r 80 -png deck.pdf slide
```
For a PDF deliverable, render it the same way. Extract all text (`markitdown deck.pptx`) for the content review.

## 2. Content, logic and idea review

Read `references/rubric.md` and go through every category. For design and formatting standards (font minimums, the word guide, number format, sources format, slide patterns), read the whole current `case-study-ppt` SKILL.md and its `references/visuals.md` and `references/sources.md`, and use their values over the rubric's, so the two skills can't drift apart.

- **Answer**: write down the deck's "We recommend ..." sentence. If there is no clear one in the first two slides, that is Critical.
- **Title test**: list all main-slide titles in order. Do they tell the full story alone (the McKinsey-12 test)? Apply the course's "So what?" ladder to each: flag topic titles ("Market analysis"), bare facts with no implication, instructions ("Convert X to grow") where an insight is expected, long if-then sentences, titles over one line, and titles that don't follow from the previous one. Give the rewritten insight title.
- **Structure test** (course agenda): sections in order Analysis → Strategy → Recommendation → Feasibility with matching tracker labels (standard, pillar names, or Implementation/Impact, as chosen in game plan section 0); Analysis ordered macro → micro → internal and ending in one main challenge or opportunity; a conclusion bar on every Analysis slide; a decision tree (or equivalent) showing the direction and the rejected alternatives in Strategy; every pillar with an illustration (mock-up, image, process) and a best-practice use case with a sourced number; Feasibility with timeline, risks and mitigation, a bottom-up or top-down financial breakdown with visible assumptions, hard and soft KPIs; Analysis and Strategy on separate main slides. Each missing element is Major (Critical if the brief requires it). One pattern on neighbouring slides, or one template for every pillar slide, is a Design issue (Minor; Major when three in a row).
- **MECE**: Analysis areas and pillars don't overlap and together cover the case question and every root-cause driver.
- **Team introduction**: presenters named on the title slide and an opening intro line in the speaker notes; missing is Minor (a named course pitfall).
- **Fact check against the case**: check every number on main slides against the case PDF and exhibits (right metric, year, unit, calculation). Recompute CAGRs, totals, ratios in Python. Give the correct value for each mismatch.
- **Facts-file check** (when the facts file exists): run `python3 <gameplan-skill-dir>/scripts/facts_check.py case.pdf COBE_<Case>_CaseFacts.md` (case-study-analysis-gameplan's script) and review every hit. Then spot-check against the PDF: every exhibit used on a main slide cell by cell, every hard-constraint quote, the case question and the brief. A main-slide number that matches the facts file but not the PDF means the facts file is wrong. Each wrong or missing fact is a fix row with Where = `COBE_<Case>_CaseFacts.md`, Type Fact; Critical if the strategy or a main-slide number rests on it, else Major.
- **Financial baseline**: check the deck (or the game plan's baseline table) has revenue, profit, cash and debt, each with year, unit and source. For a public company, compare against the statements (case exhibits first, then filings opened with WebFetch); for a private one, check that gaps are labelled assumptions. Then test affordability: does the investment on the Feasibility slide fit the cash, yearly cash flow and funding route the baseline shows? Standard in `case-study-analysis-gameplan/references/financial-planning.md`. Fix-table type: Fact (or Strategy if the plan is unaffordable).
- **Number ties**: same figure identical on main slides, appendix, notes and Q&A.
- **Strategy stress test**: use `case-study-analysis-gameplan`'s `references/stress-tests.md`. Rate the idea out of 10; if weak, say plainly what would be stronger.
- **Contradiction scan (always)**: go through every slide, main and appendix, for anything that shows another option, or a variant of the recommended one, ahead of the recommendation: a margin or price table, a scorecard, a chart, two numbers side by side. Each hit is **Critical** unless the slide carries a one-line reason that passes the four checks of stress test 20 (evidence with a reference; changes the verdict in numbers; survives your own hostile attack; fits one line). The fix row gives one of: remove it from the slides and add the Q&A entry; the exact line that defends it; or, when nothing defends it, that the strategy needs case-study-analysis-gameplan Stage 5.
- **Partner test**: for every outside party the strategy depends on (retailer, distributor, supplier, co-brand, investor): is their gain proven with a number, their conflict addressed, the ask plausible (stress test 18)? A one-sided or unproven deal is Major, Critical if the recommendation rests on it; the fix proposes the repair (a smaller ask, another partner, another route).
- **Kill reasons and precedents**: would each rejected option's kill reason survive a redesign of that option (test 19)? Does every cited precedent support the recommendation and not a rejected option? A dodgeable kill or a precedent for the wrong side is Major.
- **One argument everywhere**: the same kill reason, claim and precedent on every slide, in the appendix, notes and Q&A. A slide that still carries a replaced argument is Major.
- **Headline claims**: recompute breakeven year, payback and totals from the deck's own model; a claim the model doesn't give is Critical.
- **Dates**: nothing in the timeline earlier than the game plan's timeline anchor.
- **Red threads** (only when the game plan's `Threads:` line names them): the persona journey is revisited after each pillar and resolved before Feasibility; every scoreboard task is ticked on the last main slide with a number. An unticked task is Major (Critical if it is a brief item); a broken persona thread is Minor. Without a Threads line never deduct for their absence; if the case would clearly have suited one, say so in one line.
- **Breaking point** (Feasibility): the appendix shows where the target or budget breaks on the least certain driver; missing is Minor, Major when the recommendation rests on one shaky assumption.
- **Appendix index**: present as the first appendix slide, every link opening the right slide; missing or broken links are Minor.
- **Brief compliance**: tick off every item the professor required (use the game plan's brief map if there is one). A missing item is Critical.
- **Drift from the game plan** (if one exists): the deck's recommendation, numbers, targets and storyline must match the agreed game plan, including the rows of its change log. Unlogged drift is Major (Critical if the recommendation changed); list each difference.
- **Sources**: open every link with WebFetch; flag dead links, homepages, links that don't support the claim, weak sources behind key numbers.
- **Copied text**: every passage from `overlap_check.py`, with a paraphrase to replace it.
- **AI-sounding text (always)**: read `references/ai-tells.md` and check every slide, the notes and Q&A. Flag each phrase with a plainer rewrite, and give a Low / Medium / High AI-risk verdict for the deck.
- **Density is judged by eye**: the script's word count is a hint for where to look. A slide over the guide that reads cleanly is not an issue; a slide that looks crowded is a Design issue (Minor; Major when the message is lost), whatever its count.

## 2a. Design critique (scored, ranked P0-P3)

Scores the Design and readability category from six checks instead of one overall impression, and ranks every design finding by how much it hurts. Idea taken from Impeccable's `critique` (web design), rewritten for case decks. Judge the rendered slides; the house style (case-study-ppt) is the standard, or the professor's template when the deck follows one.

| Check | Question | 10 looks like |
|---|---|---|
| Hierarchy | Does the eye land on the title, then the one key number or visual, then the support? | One clear focal point per slide; action title, then the big number or chart |
| Focus | One message per slide, and is the so-what visible? | Nothing on the slide that the title doesn't need; conclusion bar on Analysis slides |
| Consistency | Same palette roles, icon style, element sizes and grid across the deck? | Sibling boxes identical, edges aligned, one icon style, palette roles only |
| Legibility | Sizes, contrast, line length? | ≥16pt body (14pt appendix), contrast ≥4.5:1 (3:1 large), no shrink-to-fit |
| Breathing room | Does each slide read at a glance? | Gaps 0.2-0.3 in, 0.15+ in padding, no crowded or half-empty zones |
| Data clarity | Is the right chart used, and read at once? | Native chart, one highlight, data labels, no gridlines, axis from zero |

- **Score**: each check 0-10; the Design and readability category = their average (rounded to 0.5). Write the six scores in the report.
- **Findings**: every slop-check P0, P1 and P2 finding is confirmed on the render and becomes a fix row, unless the render shows the slide is better as it is (say why in one line). P3 findings go in one combined polish row per type. Add what you see by eye with a P level too:
  - **P0** unreadable or misleading (text you can't read, a chart that shows the wrong thing)
  - **P1** clearly against the house style or hurting the message
  - **P2** looks like AI slop or template work
  - **P3** polish
- **Severity in the fix table**: P0 and P1 = Major (Critical when the slide is the executive summary or the recommendation and the message is lost); P2 and P3 = Minor. The Problem cell starts with the level (`[P1] gradient on pillar cards`). The Exact change names the design move from case-study-fixer's playbook (`quieter: flat NEUTRAL fill on the three cards`), so the fixer applies it without guessing.
- **Order**: design rows are numbered P0 first, then P1, P2, P3; the fixer works them in that order.

**Design-only mode** (the user asks for a design critique, not an audit): run `slop_check.py` and `audit_pptx.py` for sizes, render the named slides (or the whole deck), do 2a only. Output: the six scores, the P0-P3 list with design moves, at most 3 "what's good" bullets. No grade, no content review and no audit file unless asked; write the findings as fix-table rows so the user can say "fix 1-4". End with: "Next: case-study-fixer applies these as design moves. Run it now?"

## 3. Judge simulation

Write the **5 hardest questions** the jury would ask, aimed at the weakest points, each with whether the deck currently survives it and what to add so it does. Cover the course's jury types (academic member, case-company member, industry expert) and tag each question with the Q&A persona that would ask it and the response rule from the course:
- **the Feedback-giver** gives feedback instead of asking: confirm the question first, then reflect on the feedback.
- **the Skeptic** is hard to convince: answer patiently, lean on facts and evidence.
- **the Curious expert** wants the team's view on broader topics: answer on the spot, show interest and a human side.
- **the Forgetful juror** asks about what was already presented: softly repeat it, professionally, and point to the slide.
- **the Impact-focused juror** wants numbers and logic: confirm the impact, then answer from the logical assumptions.

## 3a. Team breakdown (team decks only)

So each member knows exactly what to fix on their own slides:
- **Owners**: from the merge log's origin table, else the game plan's team split. If neither exists, ask once who built which slides; if the user doesn't know, skip this section and say so.
- Per member, one row: slides owned, Critical / Major / Minor counts, points at stake (sum of Pts from the fix table), fix numbers to apply (e.g. `3, 7, 12`), and their single biggest issue.
- **Cross-member issues** go in a separate line (style differences between parts, the same number shown differently, handover gaps in the storyline). They belong to whoever does the merge or the fixes, not to one person.
- **Tone**: about slides, not people. Factual counts only: no ranking of members, no "weakest member", no judgements about effort. The user may forward this section to the team.
- Solo decks: skip this section entirely.

## 3b. Submission readiness

A deck is **NOT READY TO SUBMIT** if any of these is true, whatever its score:
- Placeholder or unfinished text anywhere, including notes: `[link to add]`, `[add ...]`, TBD, TODO, XX, `???`, lorem ipsum.
- Empty table cells or empty boxes meant for content.
- Any source without a working link (except the case itself), or a link that failed when opened.
- A required brief item missing, or the main-slide count not matching a fixed count in the brief.
- Any Critical issue still open.
- No "We recommend ..." answer anywhere.

The script's `submission_blockers` covers the first three mechanically; add the rest from your review. A high score never overrides this: a 90/100 deck with one `[link to add]` is still not ready.

## 4. Report

Big problems must be impossible to miss. Give it in chat, in this order:

0. **Readiness banner, first line of the report**, impossible to miss:
   - Not ready: a block starting with `## NOT READY TO SUBMIT`, then every blocker as a bold bullet with slide number and what exactly must be done.
   - Ready: `## READY TO SUBMIT (no blockers found)`.
1. **Grade**: total /100 with a one-line verdict (e.g. "74/100 – solid analysis, but the answer is buried"), state that it's an uncalibrated estimate if there is no `COBE_Calibration.md`. Then a table: category, score /10, weight, one-line reason.
2. **CRITICAL ISSUES** block at the top, before anything else in the issue list, each as a bold line: **`CRITICAL – Slide N – problem`**, then why it costs points and the exact fix. If there are none, say "No critical issues."
3. **Top 3 point-losers**: what fixing them would gain in points.
4. **All other issues**, by severity (Major, then Minor), each: `Slide N – problem – why it costs points – recommended fix`. Fixes must be concrete and ready to apply: the replacement title text, which bullets move to which appendix slide, the correct number, the new font size. Never vague ("improve design").
4b. **Team breakdown** (team decks only, section 3a): the per-member table and the cross-member line.
5. **Idea verdict**: the strategy rated /10, and the stronger alternative or upgrade if there is one.
5b. **Design critique** (section 2a): the six check scores and the top 3 design fixes by P level.
6. **AI-risk and originality**: verdict plus the worst examples (full list in the file).
7. **Judge questions** from section 3.
8. **Progress** (re-checks only): previous score → new score per category, issues fixed, issues still open, and any issue that has come back across versions (flag recurring ones in bold, they point to a habit).
9. **What's good** (max 3 bullets).
10. **Fix table**: every recommended fix, numbered, in the format below, so the user can reply "fix 1-5, 9" and the `case-study-fixer` can apply them without re-reading the report. Same numbers as in the issue list.

| # | Sev | Type | Where (every place) | Problem | Exact change | Approval | Pts | Words | Done when |
|---|---|---|---|---|---|---|---|---|---|
| 4 | Major | Number | S6, A5, notes S6 | Rail target 35% vs model 28% | Target 28% (2027: 25%); notes "21 to 28 percent" | Yes | +1.5 | 0 | All 3 places show 28% |

- **Type**: Wording, Number, Fact, Source, Design, Structure, Brief, Strategy. Tells the fixer which rules apply (case-study-ppt for Design/Wording/Source; case-study-analysis-gameplan stress tests for Strategy).
- **Where**: every slide, appendix slide, notes page and Q&A entry the fix touches. A changed number usually lives in 3-4 places.
- **Exact change**: ready to apply (replacement text, correct value, what moves where). If the right change depends on the user's choice, give the options and set Approval = Yes.
- **Approval**: Yes for anything that changes the recommendation, targets, financial assumptions, the main idea or adds/removes a slide; No for wording, numbers proven wrong, sources, design; Done for rows written by a game plan revision (already approved).
- **Pts**: estimated points gained (rough, from the category weights). Lets a partial fix start with the biggest gains.
- **Words**: effect on that slide's body word count (+12, -20, 0). Fixes that add words must say where words come out.
- **Done when**: an objective check, ideally one the script or a render can confirm ("no placeholder on slide 13", "title fits one line").

The file starts with a **Context** block so the fixer never re-asks: case file and case title (for `--case-title`), case facts file and its check result, brief and its constraints (fixed main-slide count, required topics), presentation length, presentation date, timeline anchor, time limit, research allowed, solo/team and presenters, build mode, section labels, frame-slide owner, Style line (with accent and font), game plan file, merge log (if any), deck file and version, notes/Q&A files, previous audit. Then the report.

Always also write the full report to `COBE_<Case>_Audit_vN.md` (N = deck version audited; an unversioned `COBE_<Case>.pptx` counts as v1) and send it, so the next audit can track progress against it. Remind the user in one line to keep it for the next check.

Rating discipline: don't inflate. If the deck is strong, say so, and list what a 95 would need.

## 5. Next step

Fixing is not done here. End the report with the next-step offer:
- NOT READY or open issues: "Next: case-study-fixer applies the fix table. Fix everything, only Critical + Major, or pick numbers?" On an answer, load case-study-fixer and pass the audit file, deck, case PDF, case facts file, game plan and notes/Q&A files.
- READY with only Minor issues: say it can be submitted; offer the fixer for the Minor rows as optional.
When case-study-fixer started this audit (its pre-audit because no audit file existed, or a re-check), skip the offer and return to the fixer; it reports back. In a no-interruption run skip the offer too: hand the fix table to case-study-fixer with the recommended option on every Approval = Yes row.

## 5a. Light re-check (after a fix pass; the default instead of a second full audit)

Its job is to catch obvious errors the fixes left or caused, not to grade again.
- **Numbers**: run `audit_pptx.py` and `overlap_check.py` on the new version; every changed figure is identical on main slides, appendix, notes and Q&A; headline claims still match the model.
- **Look**: render every changed slide and look at it: overflow, overlaps, one-line titles, text sizes, a slide that became crowded. Run `slop_check.py` again: no new P0 or P1, and every design row's P level is gone or explained.
- **Feasibility**: the investment still fits the financial baseline; timeline and risks still match the plan.
- **Fix rows**: tick each row's "Done when" with evidence.
- **Not done here**: no read of the case PDF, no re-opening of unchanged links, no re-scoring of all six categories, no hunt for new Minor issues.
- **Output**: `COBE_<Case>_Audit_v<N+1>.md` headed `Type: light re-check`, with the Context block, the readiness banner, rows confirmed and rows failed, anything new that is a blocker or Critical, and the score as the previous score plus the Pts of the rows confirmed (marked as an estimate).
- A **full independent re-audit** (sections 0-4 again, by a separate subagent that gets the calibration file and the Context block, and is told the fixer started it) runs only when the user asks for it by name.

## 6. Calibration (when graded decks arrive)

If the user uploads a deck together with its real grade or professor feedback:
1. Audit it blind first (without looking at the grade), then compare your score to the real one.
2. Note which categories were over- or under-scored and what the professor actually commented on.
3. If a pattern repeats across 2+ decks, record adjusted category weights or descriptors in `COBE_Calibration.md` and apply them on top of `references/rubric.md` for this run (never edit the skill's own files: they are replaced on update).
4. After every graded deck (no pattern needed), add its entry to `COBE_Calibration.md` and build or update a profile for that professor/course there (format rules, length, recurring comments, pet peeves).

The skill folder is reinstalled with updates, so the running record lives in `COBE_Calibration.md`: tables of graded decks (case, course/professor, real grade, auditor score, gap, what the professor focused on), professor profiles and adjusted weights. Create or update it after each calibration run, send it to the user, and ask them to attach it to future audits. Tell the user what changed.

## 7. Judge drill (on request: "grill me", "rehearse the Q&A", "practice questions")

A practice mode, not an audit: it produces no grade for the audit file and edits nothing. Needs the deck; use the Q&A file and speaker notes if they exist.
1. Take the 5 hardest judge questions (section 3) plus the Q&A file's questions. Ask one at a time, weakest point first, each in the voice of its persona (the Feedback-giver, the Skeptic, the Curious expert, the Forgetful juror, the Impact-focused juror). Follow up when an answer is vague ("which number supports that?").
2. After each answer: a rating out of 10, what a stronger answer adds, and the backup slide (A#) to point to. Say "You're wrong" when the answer contradicts the deck or the case. Also flag the course's Q&A pitfalls: too long (over ~30 seconds), not answering the question, praising the question ("great question"), phlegmatic or impatient tone, "may I add" chains, and in team drills a one-man show, no Q&A protocol (who answers what) or teammates contradicting each other.
3. Timing: only the spoken answers are timed (over ~30 seconds is too long). The speaker notes are a briefing, not a script, so they are not timed.
4. End with the 3 weakest answers. If the drill exposed a deck defect, write it as a fix-table row and offer case-study-fixer; don't change the deck here.

## Notes

- Team decks: check that slides by different members look like one deck (fonts, colors, box styles, number formats, tone), and that the game plan's Style line was followed if it has one. Report the per-member view in the team breakdown (section 3a).
- If the deck follows the professor's own template or style guide, grade design against that instead of the house style, and say which standard was used.
- Never invent problems to look thorough; every issue needs a slide reference or evidence.