---
name: "case-study-analysis-gameplan"
description: "Analyse a business-school case before any deck is built: case facts file, rundown, frameworks, precedents and the real outcome, strategy options (with a low-cost strategy council and wildcard ideas), debate, the agreed strategy and the game plan file; also revises the plan when the strategy changes. Use whenever the user shares a case PDF or brief, asks how to solve a case, what to recommend, which strategy is best, or wants to start a COBE case, even if they only say 'help me with this case'. Never moves to the next pipeline step without the user's yes."
---

# Case study analysis and game plan

This skill does the thinking; `case-study-ppt` does the building. Output: an **agreed strategy** and, on request, a **game plan file** case-study-ppt builds from without asking again. It also owns later revisions of the plan (Stage 5). Strategy is argued over here, while it is cheap to change, so the deck never defends an unchallenged answer.

- Default context: university coursework (Corvinus, COBE). Depth over speed, outside research allowed.
- Course standard: the course's case-solving standard. Deck: Executive summary, Analysis (situation, environment, company → main challenge or opportunity), Strategy (direction, alternatives, analysis of alternatives), Recommendation (pillars, illustrated), Feasibility (timeline, risks and mitigation, soft and hard impacts, financial breakdown). It beats any older rule.
- Style with the user: short, bullets, no emojis, honest ratings /10, "You're wrong" when they are.
- **The case PDF is read once by a model** (1.0) and turned into `COBE_<Case>_CaseFacts.md`. After that no model reads the PDF: not you, no sub-agent, not the arena. Scripts may still use the file (the 1.0 check, the auditor's copied-text check, `pdfimages` for the logo): they cost no usage. **A fact missing from the facts file** (any later step): tell the user. If it changes a number, a target or the recommendation, stop and offer Stage 5 (the fact is added to the facts file there); otherwise use it as a labelled assumption. Reopen the PDF only if the user says so.
- **Web research is done once, by you.** Sub-agents never search the web (cost multiplies, results diverge, memory invents precedents). What they need from outside is verified by you and written into the facts file.

## Case pipeline (the one full copy; the other case skills point here)

| Step | Skill | Owns | Hands over |
|---|---|---|---|
| 1 | case-study-analysis-gameplan | Facts file, analysis, precedents, options, debate, agreed strategy, plan revisions | `COBE_<Case>_CaseFacts.md`, `COBE_<Case>_GamePlan.md` (setup, strategy, numbers, storyline, brief map, sources, Q&A, change log) |
| 2 | case-study-ppt | Building: whole deck, one member's part, or the team skeleton | Whole: `COBE_<Case>.pptx` (= v1), `.pdf`, `_SpeakerNotes.docx`, `_QA.docx`. Part: `_Part_<Name>.pptx`, `_Sources_<Name>.md`, `_SpeakerNotes_<Name>.docx`, `_QA_<Name>.docx`. Skeleton: `_Skeleton.pptx` |
| 2b | case-deck-merger (team only) | Merging part files, or checking one shared team deck | `COBE_<Case>.pptx` (= v1) + merged notes/Q&A + `_MergeLog.md` |
| 3 | case-study-auditor | Grading only, never edits; also verifies the facts file against the PDF | `COBE_<Case>_Audit_vN.md` (Context block + fix table) |
| 4 | case-study-fixer | Repairs on command; light re-check (full independent re-audit only on request) | `COBE_<Case>_v(N+1).pptx` + updated files + re-check file |
| – | case-slide-designer (optional) | Redesigning single slides; its rules and tools are also used inside step 2 | One-slide files; before the first audit case-study-ppt inserts them, after it only case-study-fixer does (new version, re-audit) |

Steps 3-4 repeat until READY TO SUBMIT. 2b merges separate part files, or only checks and restyles a downloaded shared deck.

**Handoff rules** (every other case skill carries a copy of this block; change it here first, then in each copy)
- Each step does only its own job; for anything another step owns, hand over.
- Finish with one line: "Next: <skill> – <what it will do>. Run it now?" On yes, load it with the Skill tool and pass every file so far; in a new chat, list the files to attach.
- **Always confirm before moving on**, including calls inside a skill's own flow (compressed mode, pre-audit, re-check). Unattended runs stop at the offer. The one exception is a no-interruption run (next rule).
- **No-interruption run** (the user says "just build it", "just run it" or "run with no interruptions"): the chain runs to the end without a stop. It starts from the user's game plan, or from case-study-analysis-gameplan when there is none (full analysis, council at graded size, your recommended strategy, named at the top of the delivery). No sample-slide stop, no "Run it now?", no approval questions: take the recommended option each time and list every such choice at the end so the user can reverse it. Then build → one full audit → one fix pass → one light re-check → deliver once. Image prompts go out with the delivery (shape mock-ups in the deck until then). Only what the user alone can supply (a case fact that changes the recommendation, a private file, real presenter names) stays open: finish everything else and deliver NOT READY TO SUBMIT with it on top.
- **The audit loop is capped.** One full audit, one fix pass, one light re-check (numbers, look, feasibility; case-study-auditor section 5a), at most one more fix pass, then deliver with anything still open on top. "Fix everything, don't re-audit" skips the re-check. A full independent re-audit runs only when the user asks for it by name.
- **Conflicts get asked.** When something the user supplies (an image, a file, a number, a team decision) differs from the game plan, ask which is right and write the answer into the plan; never work around it silently. In a no-interruption run follow the user's newest input and list the conflict at the end.
- Nothing is re-asked downstream: setup answers (length, presentation date, time limit, timeline anchor, research, team and presenter names, build mode, section labels, brief constraints, case file and title, frame-slide owner, Style line with accent and font) live in game plan section 0, the merge log and the audit's Context block.
- Nothing is lost: every file carries forward (case PDF, facts file, brief, game plan with change log, deck, notes, Q&A, merge log, latest audit, calibration record). If one is missing, say which and continue.
- **Case source for every later step is `COBE_<Case>_CaseFacts.md`**, not the PDF (the auditor reads both to check them against each other). A fact missing from it: tell the user; if it changes a number, a target or the recommendation, stop and offer case-study-analysis-gameplan Stage 5; otherwise use a labelled assumption. Reopen the PDF only if the user says so.
- **The game plan stays current.** Only the user decides changes. A step applying an approved change to the recommendation, a number, a target or the storyline also updates the plan and adds a section 16 Change log row (what, old → new, who approved). Logged changes are approved, not drift. A step that finds an error without approval stops and tells the user.
- **Versions.** The first complete deck is v1 (`COBE_<Case>.pptx`), whichever step produced it, never `_v2`. If an input already has that name, copy it first (merge base → `COBE_<Case>_Skeleton.pptx`, shared-deck download → `COBE_<Case>_Download.pptx`) so the output takes the plain name. Only the fixer produces `_v2`, `_v3`, ...; an audit is numbered by the deck version it grades (`_Audit_v1` for v1).

## Stage 0 – Setup (ask before anything else)

Two short rounds at most (the question tool takes 4 per call). Skip anything the user's prompt already answers; in a no-interruption run ask nothing and use the defaults. Whatever the user's prompt sets (council size or no council, slide count, research, labels, colours) always wins over a default, in a no-interruption run too.

1. **Solo or team?** Team: presenters with their **real names** (placeholder names become a submission blocker), **how slides are built** (separate files merged later, or one shared live deck), **who builds the frame slides** (title, executive summary, Recommendation & next steps, Sources; default the user).
2. **Presentation length** (minutes).
3. **Outside research**: "Allowed / encouraged (Recommended)" first; default allowed.
4. **Stakes** (council size, 3.0):
   - **Graded coursework (Recommended)**: 5 drafters, 2 wildcard, 1 red team = 8 calls.
   - **Practice**: 3 + 1 + 1 = 5 calls.
   - **High stakes**: 7 + 2 + 2 red teams + 2 revisions = 13 calls.
   - **No council**: you alone, 0 calls.
   A size the user gives (for example 2+1+1) is used as given. **Low-usage** (only when the user asks for it): every council agent runs on Haiku; say once that the drafts get thinner.
   Default graded. The full arena (3.5) is never offered here; it runs only if the user asks for it by name.
5. **Section labels** (ask every time): **Standard (Recommended)** `Analysis`, `Strategy`, `Recommendation`, `Feasibility`; **Pillar names** (one label per pillar; multi-pillar only, else standard; each label must fit its tracker segment at 14pt, about 14 characters, so shorten longer pillar names here); **Implementation/Impact** (Recommendation content under Implementation, Feasibility under Impact). Recorded as `Sections:` in game plan section 0.

Second round, only what is still open (defaults in brackets):
6. **Presentation date and time limit** [date: ask; limit: none]. With a time limit (a 5-hour case) say the time plan in one line (analysis until X, slides until Y) and scale to it: practice-size council under 6 hours, no council under 3.
7. **Timeline anchor**: does the plan start from the case's decision date or from today? [the case date; today when the brief asks for a current plan]. No date in the plan or the deck may fall before it.
8. **Accent colour**: one secondary colour for key numbers, the chosen branch and KPI tiles? [none].
9. **Presenting tool**: PowerPoint desktop, PowerPoint Online or Google Slides? It decides the font [PowerPoint desktop: Avenir Next LT Pro; otherwise a font that tool has, named in the Style line].

These are case-study-ppt's section 0 answers too; they go into the game plan.

From the case, also extract the **brief's hard constraints** (fixed slide count, required topics or framework, backup rules, word limit); they override default sizing and appear in the rundown. **Extra deliverables** are only what the user's first prompt or the brief lists (usually a one-page Word executive summary): record each in the brief map and section 0; case-study-ppt builds it at delivery with the docx or xlsx skill. Don't ask about extras.

**AI-use notice**: if the PDF forbids AI input (Ivey cases do), say so in one line before analysing so the user can check the course policy; then follow their call.

## Stage 1 – Case facts file, rundown, hypothesis

### 1.0 Case facts file (the only model read of the PDF)
Read the whole case once, with exhibits, endnotes (often the key calculation) and any brief files. Write `COBE_<Case>_CaseFacts.md` (short name, no spaces). A **complete record, not a summary**: the PDF won't be read again.

Section 1 – Case record:
- Header: title, publisher, year, pages, AI-use notice if any.
- Case question as stated, decision maker, decision time frame. The professor's brief word for word.
- Company: history, business model, products, segments, channels, organisation, culture, values and non-negotiables (short verbatim quotes with page for every constraint).
- Market, each competitor with its numbers, customers, macro factors: every fact with its page.
- **Every exhibit in full** as a markdown table (all rows, columns, units, footnotes), titled `Exhibit N – <title> (p. X)`; chart values marked "read from chart".
- Every endnote with content. Key quotes (short, with page). "Not in the case": missing data and conflicting figures.
- **An exhibit too small or blurred to read as text**: render its page (`pdftoppm -r 200 -f N -l N -png case.pdf page`) and read the image, as part of this one read, before calling it unreadable. Still unreadable: ask the user for a clearer copy and list it under "Not in the case".

**Mandatory completeness check (a script, not a re-read).** Run `python3 <skill-dir>/scripts/facts_check.py <case.pdf> COBE_<Case>_CaseFacts.md` (needs `pdftotext`).

It compares page by page, so give every fact its page (`p. 4`): a number counts as covered when the facts file carries it next to that page reference. `MISSING` lines: add the fact from the printed context. `CHECK` lines (a short number found only under another page): confirm it is the same fact. Irrelevant hits (page numbers, years in references, footnote markers) go under a `## Ignored numbers` heading at the end of the facts file. Re-run until it prints 0 missing. Exit code 2 means the PDF has no text layer (scanned): the check did not run and is not a pass; read the rendered pages instead and say so. Then report in one line: "Case facts file written: <N> exhibits, <M> endnotes, check: 0 unexplained numbers. The PDF won't be read again."

Sections 2-3 are appended in Stage 2 and 3.0.

### 1.1 Rundown (from the facts file, about two minutes to read)
- **Case question** (one sentence), **decision maker**, **what a good answer must deliver**.
- **Brief constraints**.
- **Key facts and numbers** (5-10, with exhibit refs), grouped macro / micro (market, competitors, customers) / internal; compute derived numbers (CAGR, ratios, gaps).
- **Financial baseline** (always, before any strategy): yearly revenue, yearly profit, cash, total debt, net debt, in the table in `references/financial-planning.md`; public companies also their statements when research is allowed. Missing basics: one line, replacement marked an assumption. Every strategy is tested against it.
- **Tensions**: the 2-4 trade-offs built into the case.
- **Missing or ambiguous** data.
- **Initial hypothesis**: "Our best guess is that X should do Y because Z", plus what would prove it wrong. Stage 2 tries to break it.

## Stage 2 – Analysis (case-study-ppt steps 1-4)

Analyse to **test the hypothesis**, from the facts file. Menu in `references/frameworks.md`.
- Run every framework that plausibly applies, internally. **Show only those with an insight**: framework → 1-3 findings → "so what". The rest in one line ("Checked, nothing decisive: PESTEL, BCG"); graders punish framework dumps.
- Cover, in order: **macro** (PESTEL drivers, trends), **micro** (market, competitors, customers: segments, personas, journey), **internal** (business model, unit economics, what the baseline says about growth, profitability and room to invest, strengths/weaknesses), **root cause** (cause vs symptoms) with its named drivers.
- Conclude in **one main challenge or opportunity** sentence (last Analysis slide, executive summary Challenge row). Write each finding so it can be a conclusion bar.
- Numbers in a small Python script; note every assumption.
- Research (if allowed): web search, primary or reputable sources, record every URL opened, never cite from memory; public companies' statements, private-company fallbacks in `references/financial-planning.md`.
- End with **Hypothesis: confirmed / revised / rejected** and why.

### 2.1 Precedents, real outcome, obvious answer (you, once, 5-10 searches)
Only if research is allowed; else one line and "Precedents: none (research not allowed)" in Section 2. Open every page you cite; record URLs.
1. **3-4 precedents**: real companies with the same root-cause driver or a similar position (any industry): company, year, problem, what they did, measured effect, how close the parallel is and where it breaks, URL. **Different solutions, at least one failure** (with why); one success story makes every drafter copy it. Nothing verifiable for a driver: say so. For each precedent note **which option it supports**: one about the product, channel or model of an option you may reject is evidence for that option, not for yours.
2. **Real outcome**: what the case company actually did after the case date and how it went, with URL (or "too recent / not public"). A reference point, not the answer.
3. **Obvious answer**: 1-2 searches for public solutions of this or a similar case (student decks, competition write-ups). Never hunt for teaching notes or leaked copies. Use them only to state, in one line, the answer most teams will give; copy nothing else into any file. Tell the user once to check the course rules on published solutions; skip this step if not allowed.

Append **Section 2 – Diagnosis** to the facts file: baseline table, computed key numbers (with calculation), verified research facts (with URL), root cause and named drivers, tensions, main challenge sentence, and **Precedents and reference points** labelled "precedents are inspiration and evidence, not templates; the real outcome and the obvious answer are reference points to beat, not to copy". No hypothesis, verdict or favoured option.

### 2.2 Checkpoint (before any council call)
Show the user in at most 8 lines: root cause and drivers, main challenge sentence, precedents (one line each), real outcome, obvious answer. Then one question (question tool): **"Diagnosis right? Starting the council (<n> calls)."** Options: "Correct, start (Recommended)", "Change something first", "Skip the council". On a change, update Section 2 and ask again. A wrong root cause wastes every council call. Unattended: proceed and say so at the top.

## Stage 3 – Strategy options, stress test, debate (steps 5-6)

### 3.0 Strategy council
Cheap, deliberately different drafts plus longshot wildcards, attacked at once by one strong red team. It replaces the arena's knockout rounds (they repeat 3b and the debate at ten times the cost). Output is **input to 3a-3d, never the answer**. Size from Stage 0. Skip only for "No council", the user saying so, no Agent tool (one line, go to 3a), or Stage 5.

1. **Announce, don't ask**: "Running the strategy council: 5 drafters, 2 wildcard agents, 1 red team, 8 calls." The 2.2 answer was the yes; don't ask again.
2. **Append Section 3 – Council brief** to the facts file, so the file stands alone (sub-agents see nothing else):
   - Case question, decision maker, what a good answer must deliver; length; solo/team; the brief's hard constraints word for word.
   - The full text of `references/stress-tests.md`: "Your strategy must pass every knock-out test; if multi-pillar, every pillar test too; tests 18-20 apply to every draft."
   - **Drafter output** (max 900 words, English): umbrella name; one "We recommend ..." sentence; single move or 2-4 pillars (each: root-cause driver it fixes, actions what/who/when, 1 KPI with target, supporting precedent from Section 2 if any, other examples labelled unverified); **precedent use** (which inspired it, what was adapted, how it avoids the failed precedent's mistake); **versus the obvious answer** (one line); one **only-this-company move** (rests on an asset, fact or constraint unique to this case, with reference); key numbers with calculation; affordability vs the baseline in one line; **partners** (every outside party whose yes the strategy needs: their gain as a number, their cost or conflict, their alternative, evidence they do such deals, an ask they would grant; test 18); **where another option beats this one** (any metric, with both numbers, and why this one still wins); top 3 risks with mitigations; rejected options, one line each.
   - **Rules for every sub-agent**: "This file is the complete case record and your only source. Never look for, open or ask for the case PDF; no web search. Never invent case facts or precedents; cite section, exhibit or page; label anything else an assumption."
3. **Drafters and wildcard agents in one message** (high stakes: two waves, 5 + 4). Every call: `subagent_type` general-purpose, `description` "council <id>", absolute paths, only `.md` files.
   - **Drafters** (`model` sonnet; low-usage: haiku), D1-D3 practice, D1-D5 graded, D1-D7 high. Stances: D1 **Focus / defend** (narrow to core customers and products, protect the moat); D2 **Attack / growth** (new segments, markets, products, channels); D3 **Business model change** (who pays, what is sold, how delivered); D4 **Partner / ecosystem** (alliances, acquisitions, platforms, a rival as partner); D5 **Operations / cost** (efficiency, capacity, pricing power, supply chain); D6 **Customer-led** (most valuable or underserved segment and its journey); D7 **Contrarian** (start from Section 2's obvious answer, or the one most teams would give, and build the strongest strategy that rejects it).
     Prompt: "Read `<abs>/COBE_<Case>_CaseFacts.md`; it is your whole brief and only source. Stance: <stance>. Build the best strategy inside it that meets Section 3. Stay in the stance; drifting to the obvious answer makes the draft useless. If the stance can't pass a knock-out, say which and give the closest version. Write `<abs>/.council/D<n>.md`. Reply: DONE D<n> <words>."
   - **Wildcard agents** (`model` haiku: volume and variance matter here, not polish). W1: **far analogy** (a model from an unrelated industry, from Section 2's precedents where they fit, else labelled unverified) + **flip the weakness** (the biggest weakness, constraint or odd fact becomes the asset). W2: **attention stunt** (bold, cheap, newsworthy, moves a case KPI) + **model pivot** (who pays, what is sold, how delivered, inside the constraints). Practice: W1 gets all four.
     Prompt: "Read `<abs>/COBE_<Case>_CaseFacts.md`; it is your only source (ignore the drafter output spec). Lenses: <lenses>. 4 ideas per lens, each: name; one sentence; the case fact it exploits with reference (test: only this company could do this); type (stunt / pivot / partnership / product / business model); the hard constraint it touches and why it stays inside; cost vs yearly profit (<1% / 1-5% / >5%); cheapest 30-day test; what it could grow into in 2-3 years. Banned unless reinvented for this case: generic app, social media campaign, influencers, loyalty programme, 'go digital', 'sustainability', 'new markets', 'premiumise', the obvious answer. At least 2 must make a sceptical professor raise an eyebrow, at least 2 must cost almost nothing. Write `<abs>/.council/W<n>.md`. Reply: DONE W<n> <ideas>."
4. **Red team** (default model), only after every drafter and wildcard agent has replied DONE (they run in the background: wait for all of them). R1 does a-d (high stakes: R1 a-c, R2 d).
   Prompt: "Read `<abs>/COBE_<Case>_CaseFacts.md` and every D and W file in `<abs>/.council/`; only these `.md` files, no PDF, no web. You are a hostile COBE professor. Write `<abs>/.council/R<n>.md`, max 2,200 words:
   (a) Per draft: each knock-out pass/fail with reference; top 3 attacks FATAL/MAJOR/MINOR, specific and checkable; numbers that disagree with the facts file; precedent check (which precedent supports it, which warns, does it repeat the failure, does any cited precedent really support a rejected option instead); partner test 18 per partner (pass, repairable and how, or fail); kill-reason test 19 on the draft's rejected options (would the kill survive the strongest redesign of that option?); versus the real outcome and the obvious answer; rating /10.
   (b) Best pillars across drafts: pillar, source draft, driver fixed, supporting precedent, why strong.
   (c) 2 best combinations: umbrella, pillars from different drafts, drivers covered, backing precedent, main conflict.
   (d) Wildcards: kill for breaking a constraint, unfundable, failing only-this-company, duplicate, or just the obvious answer (one line each). Score the rest 1-5 on novelty, case fit, upside, feasibility, cheap-to-test (/25). Keep the top 5 with a slot: signature move, horizon option or challenger. Make shaky ideas feasible without losing the twist; never sand one into a generic idea. For each kept wildcard restate: name, one line, the case fact it exploits with reference, cost band, cheapest 30-day test.
   (e) Where alternatives win: for the two best drafts, every metric (margin, market size, growth, payback, cost) on which another draft, or a variant of the same idea, beats it, with both numbers.
   Don't rewrite strategies. Reply: REVIEWED <killed> of <drafts>, <kept> wildcards."
5. **Revisions (high stakes, 2 calls, `model` sonnet)** for the two best unkilled drafts: "Read the facts file, `<abs>/.council/D<n>.md` and its part of `R1.md` (only `.md`). Fix every valid attack, rebut the rest in one line each at the end, keep your stance and the output spec. Write `D<n>_v2.md`. Reply: REVISED D<n>." Read the `_v2` versions.
6. **Read**: R files first, then only unkilled drafts and drafts named as a best-pillar source. Never the W files (the R file restates the kept wildcards). **Check every kill before trusting it**: look up the FATAL's cited evidence in the facts file; if it doesn't hold, read that draft and put it back in the pool.

### 3a. Generate wide
Pool: surviving drafts, the red team's 2 combinations, challenger wildcards built into full candidates. Add your own only for gaps in the range. No head start for council candidates: all go through 3b. Aim for 5-8 deliberately different candidates (focus vs diversify, organic vs partner, defend vs attack, invest vs harvest), at least one bold option and the status quo baseline.

**Multi-pillar check.** Most winning answers are one umbrella strategy with 2-4 pillars. If the root cause has 2+ drivers, a single move probably fixes only part: build 1-2 multi-pillar candidates (umbrella name, "We recommend ...", each pillar names its driver), using the red team's best pillars. For strong single moves, test whether 1-2 enabling pillars (capability, funding, channel, organisation) make them feasible or stronger. Single driver: one line, "Checked multi-pillar: single driver, one move suffices".

**Graft the wildcards** in their slot:
- **Signature move**: executes an existing pillar (e.g. a stunt that launches the DTC pillar); serves that pillar's driver, so test 11 passes through the host; doesn't count toward the pillar limit; becomes the pillar's creative element.
- **Horizon option**: a bigger move for year 2-3 with a trigger ("if KPI X reaches Y by <date>, launch Z") and a cheap year-1 test; lives in Feasibility, not the pillars.
- **Challenger**: a full candidate, tested like the rest.
Every graft passes knock-outs 3-4 and pillar test 15. Aim for at least one surviving wildcard in the final answer; if none survives, say why in one line; never force one.

### 3b. Stress-test and kill
Run every candidate through `references/stress-tests.md` (all ten, knock-outs first; the brief is part of test 3). The red team's verdicts are a head start, not a ruling: check them against the facts file. Precedents are evidence for economics, competitor response and the pre-mortem (a failed precedent with the same plan is a pre-mortem); the obvious answer feeds test 9. Kill knock-out failures; keep 2-4.

Multi-pillar candidates also run the **pillar tests** (section B): each pillar, then the set. A weak pillar is cut or replaced and the candidate re-tested; kill it only if no coherent 2+ pillar set remains.

Kills and cut pillars: one line each with the failed test and case evidence ("Killed: franchising – conflicts with one-operator-one-store, p.5"), so the user can revive one. They become the Strategy section's decision tree.

**Tests 18-20 on every survivor** (`references/stress-tests.md` section C):
- **Partners (18)**: prove the other side's gain. A failing deal is repaired (resize the ask → swap the partner → another route to the same goal); the pillar is cut only if all three fail.
- **Kill reasons (19)**: each kill must hold against the strongest redesign of the killed option, or the option stays alive.
- **Alternatives (20)**: list every metric where another option, or a variant of the recommendation (dose, price, size), beats it. Change the recommendation, or write the one-line reason and run its four checks. A reason that fails stays off every slide and goes to the Q&A.
Results go into the game plan tables "Partners" and "Where alternatives win".

### 3c. Present the survivors
- Top line: "Council: <n> drafts, <k> killed, <w> wildcards kept" and the folder.
- Per survivor: one-line description, "We recommend ..." sentence, source (D<n>, combination, challenger, or yours); weighted scoring table on impact, feasibility, cost, risk, fit (weights stated, 1-5), with feasibility and cost resting on the affordability test in `references/financial-planning.md` (one-line result); steelman and biggest weakness (pre-mortem); precedent line (backing precedent, warning precedent, vs real outcome and obvious answer); rating /10.
- Multi-pillar: `Pillar | Driver | Key action | KPI | Use case (verified precedent first, else "none found") | Rating /10`, plus sequencing and how the pillars reinforce each other.
- **Wildcards** block, up to 3: `Name | One line | Slot | Case fact | Cost | 30-day test | Rating /10 | Include? + why`.
- **Partners and alternatives**: per survivor, each partner's gain in one line (or the repair made), and every metric where an alternative wins, with the reason and whether it passed the four checks.
- Keep the red team's attacks on survivors for the Stage 4 Q&A.
- **Your recommendation** and why it beats the runner-up; single-move or multi-pillar and why. If the pillars could be three separate recommendations, it's a list, not a strategy.

### 3d. Debate
- **Push back on the user's pick by default**, as a sceptical professor; "You're wrong" if it's weaker. Use the failed precedent and the real outcome where they apply. Stop only when they've answered the objections, ask you to stop, or say to go with it.
- New ideas, added pillars and pulled-in wildcards get the same tests (pillar tests on the new set, graft tests for wildcards) and an honest rating.
- Single move with several drivers: which driver stays unfixed?
- Close with an explicit confirmation: strategy, "We recommend ...", pillars in order, signature move and horizon option if any, main open risks.

**Then stop.** One question: **Write the game plan and build the deck** (recommended; Stage 4 then case-study-ppt) / **Game plan only** / **Just save the analysis** (`COBE_<Case>_Analysis.md`: rundown, findings, precedents, options with scores and kills, agreed strategy, open risks) / **Stop here**.

### 3.5 Full arena (only on explicit request)
Only when the user asks for it by name. Give the size first (`ARENA plan`; 16 agents = 91 calls) and get a yes. `.arena/task.md` points every agent to `<abs>/COBE_<Case>_CaseFacts.md` as the complete record, with "The case PDF is not available; do not look for it. No web search." and "Judges: use Section 2's precedents and reference points as evidence for robustness and specificity"; no PDF path. Init with `--rubric "<this skill's folder>/references/case-rubric.md"`. Champion and semi-finalists join the 3a pool.

## Stage 4 – Game plan file (only on request)

1. Work out case-study-ppt steps 7-13 for the agreed strategy, from the facts file:
   - **Recommendation**: pillars (one workstream each unless one needs two), actions what/who/when, creative element (strategy name, illustration per pillar; agreed signature moves here), one **best-practice use case per pillar** (company, action, measured result, verified URL; verified precedents first; none verifiable → Open questions, never invented); for every partner the **"what's in it for them" line** for the pillar slide and the Partners table for an appendix slide.
   - **Feasibility**: timeline (from the section 0 timeline anchor, no earlier date anywhere; with any horizon option, its trigger KPI and year-1 test); risks and mitigations (a failed precedent's cause is a ready-made risk); **financial breakdown** opening with the investment vs the baseline (cash, funding route, net debt after), then bottom-up (cost drivers, assumptions, cash in/out per year, breakeven) or top-down (WACC, growth, results by segment), NPV when data supports it, best/base/worst; **hard KPIs**; **soft KPIs**; Balanced Scorecard map (objective, KPI, target, initiative per perspective) for the appendix; **headline claims** (breakeven year, payback, totals) taken from the model's output, never typed; an appendix **with vs without the strategy** slide of its own, never a row on another slide (the baseline if nothing is done against the plan; for a launch, the cannibalisation assumption and the rate at which the case breaks).
   - **Q&A**: the red team's attacks; "Why not something bolder?" (the horizon option); "Hasn't someone tried this?" (the precedents); "What did the company actually do?" (the real outcome, and why the recommendation still holds); "Why would <partner> agree?" (the Partners table); "Isn't <alternative> better on <metric>?" for every row of "Where alternatives win", above all those kept off the slides.
   - **Storyline**: the **McKinsey-12 grid** first (columns Analysis | Pillar 1 | Pillar 2 (| Pillar 3) | Feasibility, about 3 action titles each; titles alone tell the story), then the slide table sized to the length or the brief's slide count. Analysis and Strategy never share a main slide; when the count is tight, merge financial impact and risks first.
   - **Action titles**: one line (~60 characters), a declarative insight passing "So what?", never a topic, bare fact, instruction or long if-then.
   - **Slide patterns (the user chooses, before the file is written)**: read only the pattern catalogues: section 5 of case-study-ppt's `references/visuals.md` (course patterns) and the "Choosing a structure" list in case-study-ppt section 4c (patterns from real COBE decks: logic chain, exec-summary rail, insight columns, input → engine → output, hub and spoke, gantt with gates, KPI wheel, icon tiles, map + KPI tiles), plus, for slides that show numbers, the "Choosing a chart" guide right after it. For those slides, name the chart type in the recommended pattern (e.g. "chart + takeaway: waterfall") and the one emphasis it needs (target line, highlighted bar); treat the guide as the first thing to consider, not a rule. Show one table for the main slides: `# | Action title | Recommended pattern | 1-2 alternatives | Why the recommendation (what it proves best)`, plus the creative element per pillar (illustration idea, signature move visual) and the **images needed** (any AI image the user will generate: slide, what it must show, the plan facts it must match). Vary patterns: none on two neighbouring slides, none more than twice in the main deck, every pillar slide a different one; every slide needs a visual element. Then one question (question tool): **"Slide patterns?"** with "Use the recommended ones (Recommended)", "Change some or add my own ideas" and "Show me more options for the pillar slides". On a change or idea, take it in: rate it honestly /10 against what the slide must prove and the course standard, say "You're wrong" if it hides the message (e.g. a pie chart for a trend), suggest the closest catalogue pattern or keep it as a custom pattern described precisely in Key content, and confirm the final table in one line. The chosen pattern goes into the slide table's Pattern column; the deck builder still owns the design. Unattended: use the recommended patterns and say so.
2. Write `COBE_<Case>_GamePlan.md` in the exact structure of `references/gameplan-template.md` (mirrors case-study-ppt), with the `Frame slides owner:` line and the section 16 Change log starting `(no changes yet)`, even solo. Section 0 names the facts file as the case source and always carries the **Style line** (solo cases too): PRIMARY from a quick web check of the company's official brand colours and current marketing (site, campaigns, social; the case PDF only as fallback), the other four roles from case-study-ppt's `scripts/palette.py`, the accent if one was chosen, the font for the presenting tool, the icon style. Precedent and real-outcome URLs go in Sources; nothing from published solutions.
3. **Team kit (team cases only)**:
   - The **Style line** (step 2) is binding for every member. Nobody derives colours alone.
   - **Team split** (section 13): who builds and presents which main and appendix slides; confirm with the user if not discussed. Name the **frame-slide owner** there and in section 0.
   - One `COBE_<Case>_Brief_<Name>.md` per member (first name, no spaces), one page, for teammates without Claude: their slides (number, phase, exact action title, pattern, content, backup slide); their numbers from the Numbers section ("use exactly these; new numbers go to <user> before the merge"); verified sources; style essentials (palette, font, 24pt one-line action title, section labels, conclusion bars on analysis slides, main 16pt / appendix 14pt, about 40 body words as a guide, `$7.7M` `12%` `1,500`); what not to build (frame slides unless assigned); what to hand in (`_Part_<Name>.pptx` + `_Sources_<Name>.md` + `_SpeakerNotes_<Name>.docx` + `_QA_<Name>.docx` (3-5 questions); shared-deck mode: edit only own slides, sources on the shared Sources slide); the handover line to the next presenter.
4. Offer the McKinsey-12 grid as a Whiteboard artifact in one line (if listed); build only on a yes.
5. Send the game plan, facts file (and briefs), then: "Next: case-study-ppt builds the deck, PDF, speaker notes and Q&A from this game plan. Run it now?" On yes, load it and pass the game plan, the facts file and the case PDF (carried forward for scripts and the auditor only). New chat: the user attaches all three.

Rules: every number once in "Numbers" with source or calculation; one full-sentence action title per main slide; only agreed content (the rest under "Open questions"); a **brief map** row for every required item (an unmapped item means the storyline is incomplete); **no placeholders** (TBD, `[add]`, empty cells: research it, state an assumption, or list it as open); precise enough that case-study-ppt never re-solves anything; Sources only URLs actually opened.

**Shareable doc (on request)**: a Claude Docs document with the same content written for humans (case, strategy and why, who does what), via the docs skill.

## Stage 5 – Revise the game plan

Runs when the user changes the strategy, a number or a target, or a later step found an error and stopped. From the facts file, never the PDF.
1. Read the plan and change log; one line on what changes and why. **A case fact missing from the facts file** (a later step stopped on it): ask the user for it, or read only that page of the PDF if the user says so; add it to `COBE_<Case>_CaseFacts.md` with its page, then continue.
2. Strategy change: stress tests (precedents as evidence) and a 3d debate until confirmed. Number or wording change: recompute in Python and list every place it appears (Numbers, storyline, brief map, KPIs, Q&A, briefs). An argument, kill reason or precedent that changes is a plan change like a number: list every place it appears (slides, appendix, notes, Q&A, briefs) so nothing keeps the old one.
3. Update the plan, keep the rest, add the change-log row.
4. If a deck exists, list the disagreements as fix rows (`# | Sev | Type | Where | Problem | Exact change | Approval | Pts | Words | Done when`, Approval = Done); the fixer applies them without a new audit.
5. Offer: deck exists → "Next: case-study-fixer applies these rows. Run it now?"; else → "Next: case-study-ppt builds from the updated plan. Run it now?"

## Compressed mode (case-study-ppt has no game plan, or "just give me the strategy")

Same stages, shorter; stress-testing never skipped:
- Reuse setup answers; ask only what's missing.
- Facts file (1.0) in full, with the check.
- Rundown and hypothesis in 10 lines; only frameworks with an insight.
- Precedents trimmed: 2-3 (one failed), real outcome, obvious answer, at most 6 searches. Checkpoint (2.2) still asked.
- Council at the Stage 0 size unless skipped; top 2 wildcards only.
- 3-4 stress-tested options, at least one multi-pillar unless single driver; kills in one line; your recommendation.
- Slide patterns: the same table and one question as in Stage 4, shown with the strategy confirmation if possible.
- One confirmation (the user picks, or pushes back once and you answer). Write the game plan (no team kit unless team), then: "Game plan ready. Next: case-study-ppt builds the deck from it. Run it now?" Hand back only on a yes.

## Behaviour notes
- A fixed brief: every required item covered explicitly and mapped to a slide.
- Never invent case facts or precedents; anything not in the facts file or verified research is a labelled assumption.
- Chat in English; game plan, facts file and slides in English unless asked otherwise.