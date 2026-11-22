# Stress tests for strategy candidates

## A. Tests for every candidate

Run every candidate through these before showing it to the user. **K** = knock-out: failing it kills the option. The rest lower the score.

1. **(K) Answers the case question.** Does it directly resolve the decision the case asks about, or does it solve a different problem?
2. **(K) Fits the root cause.** Does it fix the cause found in Stage 2, or only a symptom?
3. **(K) Respects hard constraints.** Company values and non-negotiables stated in the case (e.g. closed on Sundays, no debt, privately held, one operator per store), legal limits, and the professor's brief.
4. **(K) Feasible for this company.** Capabilities, money and time it actually has, or can realistically get. Money means the affordability test against the financial baseline (`financial-planning.md` section 5): investment vs cash and yearly cash flow, a funding route that fits the company's stated policies, debt headroom. An option the company cannot fund and has no realistic way to finance fails here.
5. **Economics.** Rough impact vs cost with numbers from the case; payback plausible. Compare the yearly impact with the baseline revenue and profit: a gain that is a rounding error against revenue, or a cost larger than a year of profit, needs a stated reason.
6. **Competitor response.** What do the 2-3 main rivals do next, and does the advantage survive it?
7. **Pre-mortem.** "It is two years later and this failed. Why?" If the most likely failure story is very likely and has no mitigation, kill it.
8. **Second-order effects.** Does it damage another strength (brand, culture, a channel, a customer segment)?
9. **Distinctiveness.** Would graders see it as obvious/generic? Generic is acceptable only if very well supported.
10. **Presentability.** Can it be explained in one "We recommend ..." sentence and measured with 3-4 KPIs?

When killing an option, give one line with the failed test and the case evidence (page or exhibit).

## B. Pillar tests (multi-pillar candidates only)

Run after section A. Tests 11-13 apply to each pillar; 14-17 to the set. **K** here means the pillar is cut (or the candidate killed, if fewer than 2 coherent pillars remain).

11. **(K) Root-cause link.** Does the pillar fix a named root-cause driver from Stage 2? A pillar that fixes nothing in the diagnosis is padding.
12. **(K) Passes the knock-outs on its own.** Each pillar must respect the case's hard constraints and be feasible (tests 3-4). One infeasible pillar sinks the whole recommendation in Q&A.
13. **Earns its place.** Remove the pillar: does the strategy get clearly weaker? If not, cut it. An enabler pillar (funding, capability, organisation) earns its place if another pillar fails without it.
14. **(K) Coherence.** One umbrella logic connects the pillars and fits one "We recommend ..." sentence. If the pillars could be three unrelated recommendations, it is a list, not a strategy.
15. **No conflicts.** The pillars don't pull against each other (e.g. premium pricing + discount-led volume push; cost cutting + service expansion) or compete for the same scarce budget, people or management attention without a plan.
16. **Coverage without overlap.** Together the pillars cover every root-cause driver; no two pillars fix the same driver.
17. **Sequencing and capacity.** There is a clear order (quick win / foundation first), and the company can run all pillars at once with the resources in the case. 2-4 pillars; more than 4 is almost always a "do everything" answer, and 3 is the easiest to present.

When cutting a pillar, give one line with the failed test and the case evidence.

## C. Partner, kill-reason and alternatives tests (every surviving candidate)

Run after sections A and B. They keep their own numbers (18-20) so tests 1-17 stay as they were.

18. **Partner test (repair, not knock-out).** Applies to any outside party whose yes the strategy depends on: retailer, distributor, supplier, co-brand, acquisition target, investor, ambassador. A deal that only helps the case company is not a deal. Prove, per partner:
    - **Gain**: what they earn, as a number (revenue, margin per unit, traffic, a gap in their range filled).
    - **Cost or conflict**: what they give up or what it clashes with (their own brand in the category, an existing exclusive, shelf space, their positioning).
    - **Their alternative** if they say no.
    - **Evidence** that this partner, or one like it, does this kind of deal (a verified precedent or a case fact).
    - **A plausible ask**: sized to what they would grant (a trial listing, not exclusive space next to their own competing product).
    Unproven items are labelled assumptions and a fallback partner is named. **If the test fails, repair in this order**: (1) resize the ask; (2) swap in another partner with a real gain and no conflict, tested the same way; (3) replace the partnership with another route to the same goal (own channel, another deal structure). Cut the pillar only if all three fail; the strategy survives if the remaining pillars still cover every root-cause driver. A repaired partnership scores fully; an unproven one that stays in lowers feasibility and is listed as an open risk.
19. **Kill reasons survive a redesign.** Test every kill reason against the strongest version of the option it kills: reformulated, resized, repriced, repositioned. A reason the option can dodge by changing its design ("just make a low-caffeine version") is not a kill reason. Find one that holds whatever the design (who buys, market structure, economics, a hard constraint), or the option stays alive.
20. **No better alternative left standing.** Compare the recommendation with every alternative, including variants of itself (another dose, price, size or scope), on every metric the analysis uses (margin, market size, growth, payback, cost, risk). For each metric where an alternative wins, either the recommendation changes, or a written reason says why it still wins overall. That reason must pass four checks: (a) it rests on a case fact, a verified source or a computed number, with the reference; (b) it changes the verdict in numbers, on the same metric or a bigger one; (c) it survives a red-team attack (attack it yourself as the hostile professor; any attack left standing fails it); (d) it fits one line. A reason that passes may go on a slide with that line; one that fails stays off every slide and goes into the Q&A with the best available answer. If no reason holds, the alternative is the better strategy: go back to 3a.

Also check each precedent for **which side it supports**: a precedent about the product, channel or model of a rejected option is evidence for that option, not for the recommendation. Label it so or drop it.
