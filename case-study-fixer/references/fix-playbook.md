# Fix playbook

Standard ways to handle the fixes audits ask for most.

## Titles
- Topic title → action title that passes the course's "So what?" test: an insight, not a topic, a bare fact, an instruction or a long if-then sentence ("Convert long-haul flyers to domestic to grow" → "Converting long-haul flyers to domestic is the key to sustainable growth"). State the finding or decision, with a number when there is one. "Key factors and barriers" → "Flights are 72% of the footprint, yet barely reported".
- One line: about 60 characters at 24pt on a 13.33 in slide (shorter at larger sizes). Shorten the wording rather than shrinking the font below 24pt.
- If a logo sits top right, narrow the title box so they don't collide.

## Answer up front
- No executive summary allowed by the brief (fixed slide count)? Put the "We recommend ..." sentence as the title-slide subtitle.
- Otherwise the executive summary and the closing slide carry the identical sentence.

## Density (too many words / text too small)
In this order:
1. Cut words: phrases instead of sentences, drop adjectives and restatements of the title.
2. Move evidence to the appendix (keep the conclusion on the main slide) and point to it in the notes, not on the slide.
3. Move narration to the speaker notes.
4. Only then reduce font size, never below the minimums (main 16pt, appendix 14pt, sources 10pt).
Tables on main slides: cut columns or rows before shrinking text.

## Numbers that don't tie
- Recompute in Python from the deck's own stated assumptions.
- Pick the version the model supports, and change the target, not the model, unless the user decides otherwise (strategy change → ask).
- Update every occurrence: main slide, appendix, notes, Q&A.

## Unsupported or wrong facts
- Open the source; quote nothing longer than needed; restate the claim exactly as the source supports it.
- No source found → soften ("far above typical festivals") or remove. Never keep an unsupported "x times" comparison.

## Sources slide
- Format (case-study-ppt `references/sources.md`): `Author or organisation. (Year, Month Day). Title. Publisher. URL`, alphabetical, one style.
- Every entry clickable (`link_urls`), every URL opened this session, specific page not homepage.
- The case itself is cited without URL (author, year, title, case number, publisher).
- A source you can't find: replace with a verified source for the same fact, or remove the fact and the source. Never a placeholder.

## Structure fixes (course agenda)
- Missing conclusion bar on an Analysis slide: add a one-line bottom banner with the implication (not the title restated); take words out of the body to stay within 40.
- Missing decision tree: build it from the game plan's kills (Strategy section); the scored table stays in the appendix.
- Pillar without illustration or use case: add a mock-up, annotated image or process, and a use case from the game plan's use-case table; if none is verified, research one (open the source) or soften to "similar approaches elsewhere" with no number. Never invent a company or result.
- Financials without visible assumptions: add 3-4 assumption tiles from the game plan's Numbers section; move the model to the appendix.
- Wrong tracker labels: use the labels from game plan section 0 (standard, pillar names, or Implementation/Impact) on every main slide.
- Section changes that add or remove a main slide need approval.

## Strategy fixes (always confirm first)
- Use gameplan stress tests to propose 2-3 options; recommended first.
- Common upgrades: replace restrictive measures that clash with the company's values with incentives; add a funding source for costs; split savings into a safe base case and an ambition case when one assumption drives most of the result; add the weakest assumption as a risk with mitigation.

## Layout clean-up after edits
- Re-render after every batch; look for overlaps (tables growing into text below), empty bands, misaligned boxes.
- Tables grow when text wraps: widen the long-text column, shorten cell text, then move the element below.
- Appendix slides should share the main slides' background, accent elements and slide numbers.

## Notes and Q&A
- Search notes for every changed number, removed idea or renamed item and update them.
- New open risk from a fix → add a Q&A entry with a one-line answer.

## Speaker notes found inside the .pptx
- House rule: no notes in the deck. Copy each slide's notes into `COBE_<Case>_SpeakerNotes_v<N+1>.docx` (right slide, right presenter), then strip them with `remove_notes(prs)`.
- Done when: `audit_pptx.py` prints no "Speaker notes inside the .pptx" line.

## URLs typed as text
- `link_urls(tf)` on every text frame of the Sources slide and any slide with a source line; it handles https, http and www and keeps trailing punctuation out of the link.
- Done when: `audit_pptx.py` reports no "URL(s) typed as text".
