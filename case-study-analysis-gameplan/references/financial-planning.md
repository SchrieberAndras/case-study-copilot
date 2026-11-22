# Financial planning for cases

Single source for the financial baseline. `case-study-ppt` and `case-study-auditor` point here instead of repeating it.

Why this exists: a strategy is only credible if the company can pay for it. Judges ask "can they afford this?" before they ask about the details, and you cannot answer without knowing where the company starts. So establish the baseline first (Stage 1), and test every strategy against it (Stage 3), instead of discovering the numbers while building the financial slide.

## 1. The 3 basics (always establish, before any strategy)

| # | Basic | What to write down |
|---|---|---|
| 1 | **Revenue generated yearly** | Annual revenue, last 3 years if available, with the growth rate. State which revenue it is (company revenue vs systemwide or gross sales) |
| 2 | **Yearly profit** | Say which profit: operating profit (EBIT), EBITDA or net income. Margin next to it. Last 3 years if available |
| 3 | **Money they have, debt included** | Three numbers, not one: **cash** (and cash equivalents), **total debt**, **net debt** (debt minus cash; negative means net cash). Add equity or free cash flow only if the case makes it relevant |

Rules:
- Same year, same currency, same unit across all three (`$7.7M`, `€3.4B`). If the case mixes years or currencies, convert and state it.
- Case data comes first. Use outside filings only to fill gaps or to update to a newer year, and say which one you used.
- If a basic is not in the case and not findable, say so in one line and label the replacement an assumption with its basis. Never leave a blank and never invent a figure.
- Keep it proportionate: the baseline is 3 numbers plus a trend, a few lines in the rundown. It is not a full financial analysis.

## 2. Which statement answers which basic

| Statement | Gives you | Use it for |
|---|---|---|
| **Income statement** | Revenue, operating profit, net income, margins | Basics 1 and 2; is the business growing, and is it profitable? |
| **Balance sheet** | Cash, borrowings (short and long term), equity | Basic 3; how much room to invest or borrow? |
| **Statement of cash flows** | Operating cash flow, capex, financing flows | Whether profit turns into cash, and how the company paid for things so far |

Profit is not cash. A profitable company can still be short of cash, and a loss-making one can have plenty. Check both before saying the company "can afford" something.

## 3. Public company: find the three statements

1. Check the case exhibits first. Many cases include condensed statements; use them as the primary source and note the year.
2. If research is allowed, get the original statements from tier-1 sources (see `case-study-ppt/references/sources.md`):
   - the company's own annual report or Form 10-K on its investor relations page;
   - for US-listed companies, SEC EDGAR (search the company, open the latest 10-K or 20-F);
   - for other countries, the annual report on the investor relations page or the national filing register (for Hungarian companies the public financial-statement portal; check the link opens before citing it).
3. Pull revenue, profit, cash and debt for the same years from the three statements. Prefer the audited annual figures over press-release summaries.
4. Reconcile with the case: if the case says one number and the filing another, check the year, the definition (systemwide vs company revenue, adjusted vs reported profit) and the currency before calling it an error. Report the difference in one line.
5. Record each URL you actually opened. Never cite a statement from memory.

## 4. Private company or no statements available

- Use the case's numbers and exhibits only. Do not pretend to have filings.
- Fill gaps with the `guesstimation` skill (revenue from units x price, profit from a typical margin of the industry) and label every such number an assumption with its range.
- If cash and debt are unknown, say that the affordability test below can only be run in ranges, and list it under Open questions.

## 5. Affordability test (Stage 3, every candidate)

For each candidate strategy compare its cost with the baseline:
- **Investment needed** vs cash on hand and yearly operating cash flow: how many years of cash flow does it consume?
- **Funding route**: own cash, new debt or an external investor. Is that consistent with what the case says about the company (no-debt policy, family-owned, covenants)?
- **Debt headroom**: net debt after the investment relative to profit (net debt / EBITDA) where EBITDA is known. Say "stretched" if it looks risky; do not quote a threshold from memory as a rule.
- **Payback**: when does the cash come back, using the case's numbers?

A strategy that fails here fails test 4 (feasible: money) or test 5 (economics) in `stress-tests.md`.

## 6. Output: the Financial baseline table

Put this in the rundown (Stage 1), in the game plan Numbers section, and reuse it on the appendix slide.

| Item | Year -2 | Year -1 | Latest | Source |
|---|---|---|---|---|
| Revenue | | | | exhibit / URL |
| Profit (state which) | | | | |
| Cash | | | | |
| Total debt | | | | |
| Net debt | | | | |

Every cell is filled with a number, a stated assumption, or "not available" with the reason. The strategy's investment is then shown against this table on the Feasibility financial slide.
