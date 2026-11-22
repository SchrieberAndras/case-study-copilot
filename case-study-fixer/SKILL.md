---
name: "case-study-fixer"
description: "Apply audit fixes or approved game plan changes to a COBE case deck, notes and Q&A on command, run a light re-check, and state READY or NOT READY TO SUBMIT. Use whenever the user says fix it, apply the fixes, fix 1-5, fix the criticals, or wants the audited deck repaired before submitting. Asks before running any audit or other pipeline step, unless the user asked for a no-interruption run."
---

# Case study fixer

Turns an audited case deck into a submission-ready one. It is the only case skill that edits a finished deck; `case-study-auditor` grades, this one repairs. Work like a careful teammate the night before the deadline: every fix complete, nothing half-done, nothing invented.

The user wants direct communication, short bullet points, no emojis.

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
- **Case source: `COBE_<Case>_CaseFacts.md`**, never the case PDF's text. Facts, numbers, quotes and page references come from it. The PDF file is carried forward only for scripts (`pdfimages` for a logo) and for the re-audit, where the auditor reads both. A fact missing from the facts file: tell the user; if it changes a number, a target or the recommendation, stop and offer case-study-analysis-gameplan Stage 5 (the fact is added there); otherwise use a labelled assumption. Never open the PDF to look unless the user says so.
- **The game plan stays current.** Only the user decides changes. A step applying an approved change to the recommendation, a number, a target or the storyline also updates the plan and adds a section 16 Change log row (what, old → new, who approved). Logged changes are approved, not drift. A step that finds an error without approval stops and tells the user.
- **Versions.** The first complete deck is v1 (`COBE_<Case>.pptx`), whichever step produced it, never `_v2`. If an input already has that name, copy it first (merge base → `COBE_<Case>_Skeleton.pptx`, shared-deck download → `COBE_<Case>_Download.pptx`) so the output takes the plain name. Only the fixer produces `_v2`, `_v3`, ...; an audit is numbered by the deck version it grades (`_Audit_v1` for v1).

## The completeness rule (most important)

**Never leave anything empty or unfinished.** No `[link to add]`, `[source]`, TBD, TODO, XX, `???`, empty table cells, empty boxes, or sources without a link. A placeholder looks like finished work at a glance and is exactly what a grader catches, so a fix that adds one has made the deck worse.

For every gap:
1. **Find it**: search, open the page with WebFetch, and confirm the page actually supports the claim (number, date, wording). Prefer primary sources (company, regulator, report) over news, news over blogs.
2. **If no verifiable source exists**: replace the claim with one you can verify, soften it to what the evidence supports, or remove the claim and its source. Say which you did.
3. **If only the user can supply it** (a private document, their own data, presenter names): ask before delivering.
4. **If anything is still unresolved at delivery**: the delivery message opens with a heavy banner, `## NOT READY TO SUBMIT`, listing each open item with slide number and exactly what is needed. Never present such a deck as finished.

The same applies to notes and Q&A files.

## 0. Inputs and scope

- **Deck** (required). **Audit file** `COBE_<Case>_Audit_vN.md` from case-study-auditor: if there is none, ask first: "No audit yet. Next: case-study-auditor grades the deck read-only, then I fix from its table. Run it now?" Only on a yes load it (follow it read-only, skip its next-step offer), then continue.
- **Case facts file** `COBE_<Case>_CaseFacts.md` (the source for fact checks), the case PDF (carried forward for scripts and the re-audit, not read), **game plan**, **notes / Q&A files** if they exist. Read the audit's **Context block** for setup answers (brief, slide count, length, team); don't re-ask them.
- **Facts-file rows:** audit rows with Where = `COBE_<Case>_CaseFacts.md` correct the facts file itself. Apply them first (with approval if they change a figure used on slides), then fix every slide, note, Q&A and game plan entry that used the wrong value, logging plan changes in its change log.
- **Other work orders:** the fix rows a game plan revision produces (Approval = Done) are applied the same way, without a new audit. One-slide files from case-slide-designer that the user wants in an audited deck are fix rows too (Type Design; replacing or adding a main slide needs approval): insert them with case-deck-merger's `merge_decks.py` as case-study-ppt section 4c describes, then the usual re-audit.
- **The fix table is the work order.** The audit ends with a fix table (`# | Sev | Type | Where | Problem | Exact change | Approval | Pts | Words | Done when`). Work from it row by row. An older audit with only a plain fix list: build the table yourself first from the issue list, using the same columns.
- **Scope = exactly what the user commanded.** "Fix it" / "fix everything" means every row. "Fix 1-5" means only those rows; "fix the criticals" means every Sev = Critical row. With a partial command, do the requested rows in Pts order (biggest gain first). Don't slip in unrequested changes; list extra problems you notice at the end instead.
- **Approvals in one round.** Collect every in-scope row with Approval = Yes, plus any other change to the recommendation, main idea, targets, financial assumptions or slide count, and ask about all of them in one question tool call (up to 4 questions; group related rows), each with 2-3 options, recommended option first. Don't edit those rows until answered; apply the rest meanwhile. Every approved change to the recommendation, a number, a target or the storyline is also written into the game plan (its section and a change-log row) and the updated plan is delivered with the deck; without a game plan, say that the deck now carries decisions no plan records. Don't ask about the re-check: after the fixes the light re-check runs by default (section 4), and "fix everything, don't re-audit" skips it. A subagent is spawned only when the user asked by name for a full independent re-audit; that request is the explicit yes this environment needs. Build the options with the `case-study-analysis-gameplan` stress tests (read `references/stress-tests.md` in that skill and apply tests 1-10, pillar tests 11-17 for a multi-pillar recommendation, and tests 18-20: partners, kill reasons, alternatives). If nobody can answer (an unattended run), apply every row that needs no approval, leave the Approval = Yes rows untouched, run the light re-check, and list the untouched rows under the NOT READY banner. In a no-interruption run take the recommended option on every Approval = Yes row instead, and list those choices at the end so the user can reverse them.

## 1. Load the standards

Read what the rows in scope need (the Type column decides; a Wording- or Number-only scope needs case-study-ppt sections 3, 3a, 4a and 4b, not the whole list). These define what "fixed" means:
- `case-study-ppt` SKILL.md and its `references/visuals.md` (pattern catalogue; for any pattern a fix builds, also the case-slide-designer `references/deck-patterns.md` section it points to) and `references/sources.md`: course structure (Analysis, Strategy, Recommendation, Feasibility), action titles that pass "So what?", conclusion bars, slide patterns, readability table (main 16pt, appendix 14pt, sources 10-12pt), about 40 body words per main slide as a guide for a clean look (60 on the executive summary and closing slide; not a rule), nothing that shows another option ahead of the recommendation (3b), number formatting (section 4b), sources proofing and format, file naming, "We recommend ..." on the executive summary and the closing slide.
- `case-study-analysis-gameplan` `references/stress-tests.md`: use it for any content or strategy fix.
- `pptx` skill SKILL.md: editing gotchas, `validate.py`, rendering.
- `docx` skill SKILL.md, when speaker-notes or Q&A .docx files must change: edit them as Word files in their own format, saved as the next version (`COBE_<Case>_SpeakerNotes_v<N+1>.docx`, `COBE_<Case>_QA_v<N+1>.docx`), never overwriting the originals.

Type → which standard applies: Design, Wording, Source, Structure → case-study-ppt; Strategy, Fact, Brief → case-study-analysis-gameplan stress tests plus the case facts file; Number → recompute in Python, then case-study-ppt number format.

**Visual identity**: keep the deck's own look (colours, fonts, layout) and apply the case-study-ppt rules within it. Do a full restyle into the house style only if the user asks. If the storyline itself is broken (wrong question answered, no coherent recommendation), say so and recommend a rebuild: case-study-analysis-gameplan → game plan → case-study-ppt. Let the user decide.

**Argument changes go everywhere.** A row that changes a kill reason, claim, precedent or number changes it on every slide, in the appendix, the notes, the Q&A and the game plan in the same pass; search for the old wording before finishing. Nothing a fix adds may show another option ahead of the recommendation: a contradiction-scan row is fixed by removing the comparison and adding its Q&A entry, or with the exact defending line the audit gives.

## 2. Plan the edits

1. Copy the deck; never edit the original. Output name: next version, `COBE_<Case>_v<N+1>.pptx` (an unversioned `COBE_<Case>.pptx` is v1, so its fix is v2).
2. Map every shape: `python <skill-dir>/scripts/pptx_edit_helpers.py map deck.pptx`.
3. For each row, add the shape ids for every place in its Where column, and check its Words effect. Every place listed in Where must change, or the deck contradicts itself. Fixes must not make a main slide look crowded (the word count is a guide, not a rule; the playbook's "within 40" lines mean the same): when a fix adds content, move detail to the appendix or notes to compensate. If the brief forces density (e.g. a fixed 5-slide limit with many required topics), keep slides as lean as possible and report the trade-off.
4. Read `references/fix-playbook.md` for the standard way to handle common fixes.

## 3. Apply

Write one fix script in the working directory and import the helpers:
```python
import sys; sys.path.insert(0, "<skill-dir>/scripts")
from pptx_edit_helpers import *
```
Helpers keep the original formatting: `set_paras`, `set_text`, `set_cell`, `table_font` (one size for a whole table, e.g. appendix 14pt), `font_size`, `add_table_row`, `add_table_column`, `add_text` (pass `font=` with the deck's font, or it inherits the theme font), `move`, `link_urls` (https, http and www; splits the URL into its own clickable run, trailing punctuation stays outside), `disable_shrink`, `copy_background`, `remove_notes` (strips speaker notes from every slide; copy their text into the notes .docx first), `shape` / `iter_shapes` (also find shapes inside groups; `map` lists group members indented). `replace_in_notes` only matters for a deck whose notes the user chose to keep inside the .pptx. Rerun the script from the original copy each time you adjust, so edits never stack up.

Then:
- `python <pptx-skill-dir>/scripts/office/validate.py out.pptx --original deck.pptx`
- Render (`soffice.py` → PDF → `pdftoppm`) and **look at every changed slide**: overlaps, overflow, titles on one line, empty bands, consistent style. Fix and re-render until clean.
- Update speaker notes and Q&A so they match the new slides (numbers, removed ideas, new risks).
- Logos: use a logo from the case PDF (`pdfimages`) or one the user provides. Never draw or recreate a logo.
- **A new slide** (a missing decision tree, a pillar slide, a Partners or with-vs-without appendix slide): build it in the deck's own master with case-slide-designer's deck-native mode (`deck_native.py scan`, then `HostSlide` and `save_single`), insert it with case-deck-merger's `merge_decks.py` as case-study-ppt section 4c describes, then renumber the appendix titles (A1, A2, ...) and every `Backup: A#` pointer in the notes and Q&A.
- Notes stay in the briefing format (case-study-ppt section 9): the point, why it's true, must mention, numbers to know, likely pushback, handover. An AI image the user sends later replaces its shape mock-up as a Design row.

## 4. Re-audit and deliver

1. Run the auditor's script on the new version: `python <auditor-skill-dir>/scripts/audit_pptx.py out.pptx (--minutes N | --main-slides N) --case-title "<case title>" --extra <notes/Q&A files>` (take the length or fixed count from the audit's Context block) and `overlap_check.py out.pptx case.pdf`, plus `overlap_check.py <file> case.pdf` for each notes and Q&A file. Any `submission_blockers` means you are not done: go back to the completeness rule.
2. **Tick off every row's "Done when"** with evidence (script output, render, text search). A row that fails its check is not fixed.
3. **Light re-check** (the default; skip it only when the user said not to re-audit): follow case-study-auditor section 5a yourself: numbers tie everywhere, every changed slide rendered and looked at, the investment still fits the baseline, each row's "Done when" ticked. It writes `COBE_<Case>_Audit_v<N+1>.md` headed `Type: light re-check`. No read of the case PDF and no re-scoring of every category. **Full independent re-audit** only when the user asked for it by name and the Agent tool is available: spawn one subagent to run the full `case-study-auditor` on the new deck, giving it the new .pptx, the case PDF and the case facts file, the brief, the notes/Q&A files, the game plan with its change log, the merge log if any, `COBE_Calibration.md` and the previous audit file. Tell it the fixer started it (take setup from the Context block, ask nothing, write the file, make no next-step offer), but not what you changed or what score you expect.
4. **One more pass at most.** If the re-check finds a blocker or a Critical, fix it (same approval rules) as `COBE_<Case>_v<N+2>.pptx`, re-run step 1 on it, add the result to the same audit file under `Second pass (v<N+2>)`, and deliver that version. No third pass: anything still open goes under the NOT READY banner.
5. **Export the PDF** of the deck as `COBE_<Case>_v<N+1>.pdf` from the new .pptx.
6. Send the .pptx, the PDF, the updated notes/Q&A files (if changed), the updated game plan (if changed) and the new audit file.
7. Delivery message, in this order:
   - **Readiness banner first**: `## READY TO SUBMIT` or `## NOT READY TO SUBMIT` + every open item, bold, with slide number.
   - Score before → after.
   - Rows done (by number) and rows not done with the reason; what changed (grouped, short), including any claim softened or removed for lack of a verifiable source and any change written into the game plan.
   - Anything the user still has to decide or provide.
   - Next-step offer: still NOT READY → "Next: another fixer pass on the open rows. Run it now?"; READY → say it can be submitted, no further step.

## Notes

- Never invent numbers, quotes, sources or URLs. Every URL in the deck must have been opened in this session.
- Recompute any number you touch in Python, and update every place it appears (main slides, appendix, notes, Q&A).
- If a fix conflicts with the professor's brief, the brief wins; say so.