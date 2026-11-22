# Grading rubric (default, out of 100)

If the user supplies the course's own rubric or the professor's brief, use that instead and map these checks onto it. The professor's brief always overrides: missing a required item is Critical regardless of category.

Score each category 0-10, multiply by its weight. **Calibrated to university coursework** (Corvinus, 2nd-year BSc), not competitions:

| Score /10 | Meaning |
|---|---|
| 9-10 | Top of the class: clear answer, rigorous numbers, distinctive idea, clean design |
| 8 | Solid, well-executed coursework with minor flaws (a typical good team lands here, ~80/100 total) |
| 6-7 | Acceptable but with clear gaps (weak root cause, generic idea, cluttered slides) |
| 4-5 | Significant problems that a professor will mark down |
| 0-3 | Missing or wrong |

Be honest, not harsh for its own sake: don't mark coursework down for lacking competition-level polish, but never inflate a score to be encouraging. Until graded decks are recorded in the user's `COBE_Calibration.md` (format in `calibration.md`), the score is an estimate.

| # | Category | Weight |
|---|---|---|
| 1 | Answer and storyline | 20 |
| 2 | Analysis and evidence | 20 |
| 3 | Strategy and idea quality | 20 |
| 4 | Feasibility and impact | 15 |
| 5 | Design and readability | 15 |
| 6 | Sources, brief compliance and deliverables | 10 |

## 1. Answer and storyline (20)
- The case question is answered directly; one clear "We recommend ..." sentence.
- Executive summary and last main slide carry the same sentence word for word.
- Action titles: insightful, relevant, short, punchy; every main slide title passes the "So what?" test (an insight, not a topic like "Market analysis", a bare fact or an instruction). Reading only the titles tells the full story.
- Logical flow Analysis → Strategy → Recommendation → Feasibility (the course agenda); each slide leads to the next; no orphan slides.
- MECE: no overlaps or gaps between workstreams / arguments.
- "So what" is explicit on every analysis slide (a conclusion bar), and the Analysis section ends in one main challenge or opportunity.
- Creative element (strategy name, slogan, memorable number) present and reused at the close.

## 2. Analysis and evidence (20)
- Analysis covers macro environment, micro environment and internal abilities; root cause identified, not just symptoms.
- Uses case data and exhibits correctly (check against the case PDF if provided): right metric (systemwide sales vs revenue), right year, right units.
- The financial baseline is established and sourced: yearly revenue, yearly profit (which profit is stated) and cash, debt and net debt, with years and units. Public company: figures match its income statement, balance sheet and cash flow statement (or the case exhibits). Private or missing data: clearly labelled assumptions. A missing basic is Major; a wrong one (profit mistaken for cash, systemwide sales for revenue) is Major, Critical if the recommendation rests on it.
- Numbers tie across slides, appendix and notes; totals add up; growth rates recomputed correctly.
- Assumptions stated and reasonable; no single outlier assumption driving the result.
- Frameworks applied with insight, named in appendix titles, not dumped.
- Outside research used where allowed, and it strengthens the argument.

## 3. Strategy and idea quality (20)
- Fits the company's values and constraints stated in the case.
- Feasible with the company's resources; addresses competitor response.
- Direction set and alternatives analysed: a decision tree (kept and killed branches with reasons) on a main slide, scored comparison in the appendix.
- Recommendation broken into coherent pillars, each illustrated (mock-up, image or process) and backed by a best-practice use case with a sourced result.
- Distinctive: not the obvious generic answer, or the generic answer defended unusually well.
- Run every recommendation through the stress tests (tests 1-10 in `case-study-analysis-gameplan`'s `references/stress-tests.md`, plus pillar tests 11-17 for a multi-pillar recommendation, and tests 18-20 for every recommendation).
- Partners have a proven gain (test 18); kill reasons hold against a redesign of the rejected option (test 19); nothing in the deck shows another option, or a variant, ahead of the recommendation (test 20).

## 4. Feasibility and impact (15)
- Concrete actions (what, who, when), not slogans.
- Timeline realistic and phased; quick wins visible.
- Risks with probability, impact and a specific mitigation each.
- Affordability: the investment is shown against the company's baseline (cash, yearly cash flow, net debt) with a funding route that fits the case's constraints; a strategy the company visibly cannot pay for is Critical.
- Financial breakdown, bottom-up or top-down, with the main assumptions visible on the slide (waterfall of cost drivers, cash flow and breakeven, NPV where the data supports it); best/base/worst in appendix; numbers plausible.
- Hard KPIs (financial, volume) and soft KPIs (non-financial impacts), each with a measurable target and timeframe; Balanced Scorecard strategy map in the appendix.
- Next steps concrete on the last slide.

## 5. Design and readability (15)
Default standard = the case-study-ppt house style. Read the installed case-study-ppt SKILL.md for the current values; the list below is a fallback summary:
- Title slide first; tracker (Analysis, Strategy, Recommendation, Feasibility; pillar names; or Analysis, Strategy, Implementation, Impact) on main-body slides; appendix footer on backups.
- Main slides look clean and read at a glance (about 40 body words, 60 on the executive summary and closing slide, is a guide and not a rule: judge the rendered slide and never deduct for the count alone), text ≥ 16pt (chart and tracker labels 14pt; appendix ≥ 14pt; sources ≥ 10pt), titles on one line, no shrink-to-fit.
- One visual element per slide; no plain bullet slides; no pattern repeated on neighbouring slides or one template for every pillar; no half-empty tall boxes, no overflow, aligned elements, consistent spacing.
- Palette from the case company's brand, used consistently; contrast readable.
- Charts think-cell style: no gridlines/borders, data labels, one highlight color, no rainbow, no 3D.
- One icon style; no clipart or decorative stock images (mock-ups, product images, screenshots and licensed persona photos that carry content are fine).
- Number format consistent ($7.7M, 1,500, 10–15, 12%).
- Main-slide count fits the presentation length (about 1.25–1.5 min per slide) or the brief's fixed count.

## 6. Sources, brief compliance and deliverables (10)
- Every required item from the brief is covered and easy to find.
- Sources slide present, consistent format, tier 1-2 sources for key numbers, links work and support the claim.
- No speaker notes inside the .pptx (house rule), files named `COBE_<Case>...`, PDF export, speaker notes and Q&A files present if expected.
- **Originality**: no passages copied from the case or sources (7+ identical words) without quotes and a citation.
- **AI-sounding text**: wording reads as the team's own (see `ai-tells.md`). High AI-risk is a Major issue.

## Severity
- **Critical**: would cost a grade band or invite a killer question (no clear answer, wrong core number, missing brief item, strategy that violates the company's values, dead/invented source for a key number, a slide that shows another option ahead of the recommendation, a headline claim the deck's own model contradicts).
- **Major**: clearly costs points (weak root cause, untied numbers, cluttered slides, missing risks or KPIs, small text).
- **Minor**: polish (alignment, wording, inconsistent format).
