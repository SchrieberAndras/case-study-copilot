---
name: "guesstimation"
description: Solve guesstimates, market-sizing and Fermi estimation questions with a clear structure, explicit assumptions, checked arithmetic, a sanity check and a final range. Use whenever the user asks "how many...", "how much...", "estimate the size of...", "what is the market for...", needs a number for a case study or case deck slide (market size, revenue potential, customers, volume) that isn't in the case, or poses a brain teaser, Fermi problem or absurd hypothetical (piano tuners, golf balls in a plane, "how many toddlers could I beat"), even if they never say "guesstimate" or "market sizing".
---

# Guesstimation

A guesstimate is judged on the logic, not on hitting the exact number. A reader (professor, interviewer, teammate) must be able to follow every step, challenge any single assumption, and see how the answer moves. So the deliverable is a transparent model that lands on a defensible number, plus a check that the number is not absurd.

## Workflow

### 1. Define the question precisely
Before any math, pin down what is being counted. Most bad estimates come from a fuzzy target.
- **Unit**: people, units sold, transactions, money (revenue vs. spend vs. profit), volume.
- **Scope**: geography, segment (B2C/B2B), what counts and what does not (e.g. "coffee" = cups bought out of home, or also home-brewed?).
- **Time**: per day / per year; stock (how many exist now) vs. flow (how many sold per year).
- **Count the way the source counts**: when the question asks for an organisation's reported figure ("items the library acquired", "passengers the airport handled", "titles in the database"), ask what that organisation actually puts in that statistic. A library reports catalogued items, not archived web pages; an airport counts arriving + departing + transfer passengers. Estimating the wrong definition well still gives a wrong answer, often by 5x or more. Include everyone and everything the statistic counts, not just the headline group: Everest summit counts include the guides and Sherpas (often as many as the paying clients), a fleet count includes reserve vehicles, a store count includes all brands in the group.
- **When is a stock counted?** A count taken on a specific date holds whatever is there at that point in the cycle: a June livestock census includes the spring's newborns, a summer visitor count includes tourists, a December inventory is pre-holiday. Ask what is seasonally in or out on the count date before modelling the "normal" level.

**Write a one-line definition check in every answer, even short ones**, before any number: *Counts: [who/what is included, incl. non-headline members] | As of: [date or period, and what is seasonally in or out then] | Memory: [none / recalled ~X from ~year]*. In testing, models that skipped this line repeated the same misses even when they knew the rule (a June sheep census without the spring lambs, Everest summits without the Sherpas, a remembered store count from two years earlier). The line only helps if it changes the math: **every group or seasonal effect you name in it must appear as its own factor or segment in the equation** (sheep = breeding ewes + lambs born this spring; summits = paying clients + Sherpas and guides, who often match them one-for-one). Writing "lambs are included" and then using a single remembered flock figure changes nothing. And **check that a remembered figure measures the same thing**: the number you recall may be the December count, the breeding flock, the clients only, or the group's main brand only. If it might be a narrower definition, treat it as one segment of the answer, not the answer.

Do not stall by asking the user. State the definition you chose in one line and move on. Ask only if two readings would give answers more than 10x apart and the context does not settle it.

**Absurd or joke premises** ("how many toddlers could you beat", "how many ducks to carry a car"): play along and give them the same rigour, because the fun is in taking a silly question seriously. These questions usually hide the real model in the rules, so write the rules down: who the contestants are (size, fitness), the arena, the win and lose conditions, and what counts as "beating" one. If the literal premise would mean modelling serious harm to children or to real, named people (a fight "to the death" against toddlers), do not model that version: redefine the win condition so nobody is hurt (ejecting, pinning, tagging) or offer a different opponent (animals, robots), and say so in one line.

### 2. Pick the approach
- **Top-down (demand side)**: population -> relevant segment -> penetration/usage -> frequency -> price. Best for consumer markets.
- **Bottom-up (supply side)**: number of suppliers/outlets/machines -> capacity per unit -> utilisation. Best when supply is countable (shops, airports, tuners, seats).
- **Analogy / benchmark**: scale a known number from a comparable market (per-capita, % of GDP).

- **Simulation (dynamic problems)**: when the answer depends on rates racing each other over time, a single multiplication is wrong because the outcome has a tipping point. Signs: something accumulates while something else clears it (a swarm piling on vs. being shaken off, a queue building vs. being served, stock running down vs. being restocked), fatigue or learning changes rates over time, or the question asks "how many before X fails / wins". Use `scripts/race_sim.py` (edit its `step` function) to run the process second by second many times, sweep the input count, and report the break point where the win chance crosses 50%. Then rerun with each key assumption moved to show which one drives the result.

Use one as the main route and a second one as the cross-check whenever the question allows it. Triangulation is what makes an estimate credible. For a simulation, the cross-check is a back-of-envelope static version (e.g. clearing rate x time): if the two differ, explain why (the dynamic one captures the pile-up).

### 3. Build the equation as a tree
Write the decomposition as a single equation first, then as a tree, before plugging numbers:

```
Daily coffees sold = Adults x share who buy out-of-home coffee x cups per buyer per day
                   + tourists/commuters x cups per day
```

Rules that keep trees sound:
- **Segment where behaviour really differs** (age bands, B2B vs B2C, locals vs tourists, urban vs rural). Do not segment for show; 2-4 segments is usually enough.
- **Keep factors independent and MECE**, so nothing is counted twice and nothing is missing.
- **Watch stock vs. flow**: to get annual sales of a durable good, use stock / replacement cycle (e.g. 4M households x 1 TV / 8-year life = 0.5M TVs/yr).
- **Units must cancel**. Write units next to every factor when it is not obvious.

### 4. Assumptions table
Every number gets a row: value, short rationale, and its type, because a reader needs to know what is fact and what is judgement:
- **Fact** - a known or looked-up figure (population, airport passengers). Cite the source if looked up.
- **Anchor** - derived from a fact with simple logic ("~2,000 working hours/year").
- **Estimate** - your judgement; say why it is reasonable.

**Model first, memory second.** If you think you remember the answer, set it aside and build the model from inputs that do not come from that memory. Never back-solve a factor from a remembered total ("172 goals / 64 matches = 2.69 per match"): that is recall dressed up as a model, and it hides whether the reasoning works. Then bring the memory in as a separate check, label it ("recall: ~X, as of ~year"), and reconcile openly. Remembered figures are often years old: for anything that grows (databases, companies, user counts, traffic), roll the memory forward to the asked date at the recent growth rate, and when growth is accelerating (user-generated content, platforms), skew the range upward. In testing, the most frequent miss was exactly this: a remembered figure from a year or two earlier for something growing (an expanding retail chain, a recovering transit network, a conservation population, a festival), landing 10-30% low with a range that stopped just short of the truth. When the memory may predate the asked year, move the point toward the trend and extend the range further on the growth side.

**Do not import averages into specific cases.** A regional or global rate (marriages per 1,000, goals per match, spend per head) can be off by 30%+ for one country, year or company because of policy, culture or a one-off event. Use it, but widen that factor's range instead of treating the average as known.

Round aggressively (1-2 significant figures). False precision ("3,847,215") signals that you don't understand the uncertainty. Common anchors are in `references/anchors.md`; read it when you need population, household, time or economic anchors, and treat them as approximate.

### 5. Calculate - and get it right
Arithmetic slips are the most embarrassing failure because they are entirely avoidable. Show each step's intermediate result. For anything beyond a two-step multiplication, run the numbers with `scripts/estimate.py` (or plain Python) instead of doing it in your head. The script also gives a realistic low/high range from per-factor ranges:

```bash
python scripts/estimate.py "adults=1.2M,1.4M,1.5M" "buyer_share=0.3,0.45,0.6" "cups=1,1.5,2"
# sum of segments: a lone "+" starts a new segment
python scripts/estimate.py "locals=1.4M" "share=0.2,0.3,0.4" + "tourists=30k,40k,60k" "cups=1,1.5,2"
# divide by a factor with a leading "/"
python scripts/estimate.py "annual_items=150k,250k,400k" "/days=365"
```

Values take k / M / bn suffixes, which avoids the most common slip in testing (a missing or extra 1e6). It prints every running result (so each step can be shown), the base case, and a P10-P90 range from a simulation, which is more honest than multiplying all the lows and all the highs together. The simulated range only covers the factor ranges you entered; if the structure of the model itself is uncertain (a missing segment, a different definition), widen the final range and say why.

### 6. Sanity check
Before stating the answer, test it against at least one independent reality check:
- Per-capita or per-household value: does it sound like normal behaviour?
- Share of a known total (GDP, total retail spend, total passengers).
- The second approach from step 2.
- A physical limit (opening hours, seats, shelf space).

If the check fails by more than ~3x, find the broken assumption and fix it openly ("first pass gave X; that implies Y per person, which is too high, so...").

### 7. Verify anchors when tools allow
When web search is available, look up the 1-3 load-bearing facts (population, a reported market size, operator statistics) rather than trusting memory, because these change and memory is often stale. Then, if a published figure exists for the final answer itself, compare: "Estimate 17M vs. reported 17.6M (2025) - within 5%" or explain the gap.
Keep the reasoning as the main deliverable: the looked-up number checks the model, it does not replace it. For pure brain teasers (balls in a bus), skip searching; the point is reasoning.

### 8. Set an honest range
The range should contain the truth about 80% of the time. In testing, the most common failure was a good point estimate with a range so narrow it missed (point 10-20% off, range +/-5%). Ranges built only from the script's simulation tend to be too tight, because people enter tight factor ranges. Use these as minimum widths and go wider when the situation calls for it:

| Basis of the answer | Minimum range |
|---|---|
| Precise fact you clearly remember, with its year, no growth since | +/-15% |
| Remembered figure, but unsure of its year or it may have grown since | +/-25%, extended on the growth side |
| Model built on solid anchors (population, known capacities) | +/-30% |
| Model with one or more judgement factors (shares, frequencies, behaviour) | x/÷2 (e.g. 50-200) |
| Unclear definition, fast-changing quantity, or no reliable anchor | x/÷3 or wider |

When the script's P10-P90 and this table disagree, report the wider of the two; the script only knows the factor ranges you typed in. If the range feels embarrassingly wide, that is usually the honest one. Skew it toward the side where the model is most likely to be wrong (missing segments push the answer up; overcounting definitions push it down).

### 9. Answer
End with:
- **Answer**: point estimate, rounded, with unit and scope, and a range (low-high).
- **Key drivers**: the 1-2 assumptions the answer is most sensitive to, and what the answer becomes if they move.
- **Confidence**: one line (e.g. "right order of magnitude; +/-40%").

## Output formats

Match the format to the use case:

**Fermi / brain teaser** - short and elegant: definition line, equation, assumptions table, math, sanity check, answer. No padding.

**Absurd / joke premise** - same as Fermi, but open with the rules (contestants, arena, win/lose condition). If you simulated, show a small table of N vs. win chance so the break point is visible.

**Case study / case deck** - the number will go on a slide and be questioned by a professor, so also give:
- An **action title** stating the so-what, not the topic ("The Budapest specialty coffee market is worth ~HUF 40bn a year, enough room for a new chain" not "Market size").
- A **slide-ready calculation**: the tree or a compact table (Factor | Value | Source/rationale).
- A **sources line** separating looked-up facts (with source and year) from team assumptions, because graders penalise numbers with no visible origin.
- 1-2 likely **challenge questions** with a prepared answer (e.g. "Why 30% penetration?").

**Real-world / business decision** - same as case format, but emphasise the range and which assumption to validate first with real data.

## Common mistakes to avoid
- Counting the same people twice across segments.
- Confusing frequency and penetration (share who ever buy vs. how often buyers buy).
- Annual vs. daily, or stock vs. flow mismatches.
- Using total population when only adults / households / businesses are relevant.
- Mixing currencies or gross/net prices without saying so.
- Presenting a single number with no range.
- Letting a web-found figure silently replace the estimate instead of being used as a check.
- Multiplying average rates when the outcome depends on a pile-up or tipping point; simulate instead.
- Leaving the win condition of a joke question undefined, so the number means nothing.
- Back-solving the model from a remembered answer, or trusting an old remembered figure for a growing quantity.
- Ranges narrower than the evidence supports (see step 8).
