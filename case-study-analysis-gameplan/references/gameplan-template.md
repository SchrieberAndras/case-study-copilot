# Game plan template

Write `COBE_<Case>_GamePlan.md` with exactly these sections, in this order. Keep it dense: bullets and tables, no prose padding. It is input for the case-study-ppt skill.

```markdown
# COBE <Case> – Game plan

## 0. Setup (answers for case-study-ppt section 0)
- Presentation length: <N> min → <M> main slides (or: fixed by brief)
- Presentation date: <date, for the title slide> | Time limit for the work: <none | deadline or hours>
- Timeline anchor: plan starts from <the case decision date | today> (no date in the deck may fall before it)
- Outside research: allowed / case only
- Team: solo | <n> presenters: <real names; never "Presenter 1">
- Council: <size used> | sub-agent models: standard | low-usage (all Haiku)
- Build mode (team cases): separate part files | one shared deck (<tool, e.g. Google Slides>)
- Sections: standard (Analysis | Strategy | Recommendation | Feasibility) | pillar names (Analysis | Strategy | <Pillar 1> | <Pillar 2> | Feasibility) | implementation/impact (Analysis | Strategy | Implementation | Impact)
- Frame slides owner: <name> (title, executive summary, Recommendation & next steps, Sources; default: the user)
- Style (every case, solo too): PRIMARY #<hex> (from <brand source: official brand colours and current marketing, checked on the web; else the case PDF>), PRIMARY_DARK #<hex>, OUTLINE #<hex>, MID #<hex>, NEUTRAL #<hex> (formulas in case-study-ppt section 4), ACCENT <none | #<hex> for key numbers, the chosen branch and KPI tiles>, font <name, chosen for the tool the deck is presented and edited in>, icons <line | glyph>
- Brief constraints: <fixed slide count, required topics, anything else>
- Case file: <file name>, case number, author, publisher, year
- Case title: <exact title, passed to the scripts as --case-title>
- Case source: `COBE_<Case>_CaseFacts.md` (every later step works from it, not the PDF)
- Extra deliverables (only what the user's first prompt or the brief lists; usually a one-page Word executive summary): <none | item, built by case-study-ppt at delivery with the docx or xlsx skill>

### Brief map (every requirement of the professor's brief)
| Brief requirement (as worded) | Slide # | Slide title | Covered by |

## 1. Case understanding (step 1)
- Case question:
- Decision maker:
- What a good answer must deliver:

## 2. Key findings (steps 2-4)
(each finding with its so-what, usable as the slide's conclusion bar)
### Macro environment
### Micro environment (market, competitors, customers / personas / journey)
### Internal abilities (company)
### Financial baseline (the 3 basics; table format in references/financial-planning.md)
| Item | Year -2 | Year -1 | Latest | Source |
|---|---|---|---|---|
| Revenue | | | | |
| Profit (state which) | | | | |
| Cash | | | | |
| Total debt | | | | |
| Net debt | | | | |
(every cell a number, a stated assumption or "not available" with the reason; one line on what it means for how much the company can invest)
### Root cause
### Precedents and reference points
| Company, year | Problem | What they did | Effect (number) | Parallel / where it breaks | Success or failure | URL |
(3-4 rows, at least one failure)
- Real outcome: <one line>
- Obvious answer: <one line>
### Main challenge or opportunity (one sentence; last Analysis slide and exec summary Challenge row)
### Frameworks used (appendix candidates)
| Framework | Key finding | Appendix slide |

## 3. Strategy (steps 5-6)
- **We recommend ...** <exact sentence, used word for word on exec summary and last slide>
- Why this option:
- Structure: single move / multi-pillar (and why, in one line)
- Pillars (multi-pillar only; order = sequencing):
| # | Pillar | Root-cause driver it fixes | Key action | KPI | Workstream |
### Best-practice use case per pillar
| Pillar | Company | What it did | Result (number) | Source URL (opened) |
- How the pillars reinforce each other (one line):
- Alternatives considered and rejected (one line each + reason):
| Option | Impact | Feasibility | Cost | Risk | Fit | Weighted | Verdict |
### Decision tree (Strategy main slide)
| Level | Branch | Kept / killed | One-line reason (test + case evidence) | Holds against a redesign of the option? |
### Partners (every outside party whose yes the strategy needs; "none" if none)
| Partner | Their gain (number) | Their cost or conflict | Their alternative | Evidence they do such deals (URL or case ref) | The ask | Fallback partner |
(the "what's in it for them" line goes on the pillar slide, the table on an appendix slide, "why would they agree?" in the Q&A)
### Where alternatives win (every metric on which another option or a variant beats the recommendation; "none" if none)
| Alternative | Metric | Theirs vs ours | Why the recommendation still wins (one line + reference) | Four checks passed? | Shown on a slide / Q&A only |
(an alternative that wins and has no reason that holds means the strategy changes; nothing in the deck may show an alternative ahead without this line)
### Wildcards used
| Name | Slot (signature / horizon) | Where in the deck | 30-day test |
(or "none survived: <reason>")

## 4. Workstreams (step 7)
(multi-pillar: one workstream per pillar, same names as in section 3)
1. <name> – <goal>
2. ...

## 5. Detailed actions (step 9)
| Workstream | Action | Who | When |

## 6. Creative element (step 10)
- Strategy name / slogan / memorable visual or number:
- Illustration per pillar (mock-up, annotated image, process):
### Images needed (AI images the user generates; "none" if none)
| Slide | What it must show | Plan facts it must match (names, colours, flavours, numbers) | Aspect ratio |

## 7. Timeline (step 11)
| Phase | Period | Key actions |
### Horizon option
- Move, trigger (`if <KPI> reaches <value> by <date>`), year-1 test, the slide that shows it

## 8. Risks and mitigation (step 12)
| # | Risk | Probability | Impact | Mitigation |
(include the failed precedent's cause as a risk row, naming the precedent)

## 9. Financial breakdown and KPIs (step 13)
### Numbers (single source of truth)
| Item | Value | Source / calculation |
### Financial breakdown
- Investment vs baseline (affordability): investment needed, share of cash and of yearly cash flow, funding route, net debt after:
- Approach: bottom-up | top-down (and why)
- Main assumptions (3-4 tiles on the slide):
- Bottom-up: cost drivers waterfall; cash inflow vs outflow per year; breakeven | Top-down: key assumptions (WACC, growth, share reinvested); results by segment over time
- NPV / payback (if the data supports it):
- Headline claims (breakeven year, payback, totals): each one an output of the model, with its calculation in Numbers; never typed
### With vs without the strategy (appendix slide)
- Baseline if nothing is done vs the plan, per year; for a launch: the cannibalisation assumption and the rate at which the case breaks
### Best / base / worst
### Hard KPIs (main slide)
| KPI | Value | Timeframe |
### Soft KPIs (main slide)
| Impact | Value | How measured |
### Balanced Scorecard strategy map (appendix)
| Perspective | Objective | KPI | Target | Initiative |
(Financial, Customer, Internal processes, Organisational capacity / learning & growth)

## 10. Storyline (step 8)
### McKinsey-12 grid (titles only; read alone they tell the story)
| Analysis | Pillar 1 | Pillar 2 | Feasibility |
|---|---|---|---|
| <title> | <title> | <title> | <title> |
### Slide table
| # | Section | Action title | Pattern | Key content | Backup |
(0 Title, 1 Executive summary, Analysis..., Strategy..., Recommendation (per pillar)..., Feasibility..., last = Recommendation & next steps)
Action titles: one line, about 60 characters, insight that passes the "So what?" test.
Analysis and Strategy never share a main slide; when the count is tight, financial impact and risks merge first.
No pattern on two neighbouring slides, none more than twice in the main deck; every pillar slide a different pattern.
Pattern: a pattern from case-study-ppt's `references/visuals.md` section 5 (or a custom pattern described precisely in Key content). Key content: the exact data and its source (e.g. "bar: market share 2019-23, Ex. 4"; "precedent strip: Ryanair 2014"). Design itself (layout, colours, chart styling, icons, maps) stays with case-study-ppt.
### Appendix plan
| A# | Title (framework name in title) | Content |

## 11. Next steps (for the recommendation slide)
| What | Who | When |

## 12. Sources (only URLs actually opened)
| Source | Tier | Supports |

## 13. Team split (team cases only)
| Member | Main slides built | Appendix slides built | Slides presented | Prep tasks | Brief file |

## 14. Likely Q&A
- Q: ... → A: ... (backup: A#) | lead: <name> | backup: <name> | persona: Feedback-giver / Skeptic / Curious expert / Forgetful juror / Impact-focused juror

## 15. Open questions

## 16. Change log (only user-approved changes after the plan was agreed)
| Date | What changed | Old → New | Approved by | Step |
|---|---|---|---|---|
| (no changes yet) | – | – | – | – |
```
