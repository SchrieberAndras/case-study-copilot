# Sources: proof every link and its credibility (case-study-ppt section 8a)

Read this before delivering any deck, part or skeleton that cites sources, and in the fixer/merger when they touch sources.

Judges and graders click links and question numbers, so a dead, invented or weak source costs more credibility than having no source. Before delivering, proof every source the deck uses, including links already in an existing deck that the team added earlier.

**1. Collect every link.** Gather all URLs from the Sources slide, slide text, source lines, hyperlinks in the slide XML and the notes / Q&A files. Unzip the .pptx and grep the slide XML and `_rels` files so nothing is missed.

**2. Open each one.** Fetch every URL with WebFetch (the shell usually cannot reach outside sites). A link passes only if:
- the exact page loads (not a 404, not a redirect to a homepage, not a parked or AI-filler page);
- it is the specific page, not a site homepage (`ourworldindata.org/` is not a source; the chart page is);
- it actually supports what the deck uses it for: the number, date or claim on the slide appears on that page and matches.

If a fetch is blocked (robots, 429, paywall), confirm the document another way: a web search showing the title on the publisher's own site, the official landing page, or an open repository copy, and cite that verified page. If it still cannot be confirmed, drop the source and either find a replacement or remove or soften the claim it supported. Never cite a page that was not opened, and never write a URL from memory.

**3. Rate credibility and upgrade weak sources.**

| Tier | Examples | Use |
|---|---|---|
| 1. Primary / official | the case itself, company press releases and filings (FDD, annual reports, Form 10-K, the income statement, balance sheet and statement of cash flows in them), government and EU bodies, regulators, laws, peer-reviewed papers and official university repositories | preferred for every key number |
| 2. Reputable secondary | established trade and business press (QSR Magazine, Nation's Restaurant News, Restaurant Business, Reuters, WSJ, FT), recognised research and data firms (Statista, Euromonitor, FAO data via Our World in Data) | fine; market-research estimates labelled as estimates |
| 3. Weak | data aggregators, vendor and marketing blogs, SEO list articles, personal blogs | only when nothing better exists, labelled as an estimate, never the only support for a number on a main slide |
| Not acceptable | Wikipedia as the final citation, content farms, AI-generated sites, social media, forums, copies on ResearchGate / Scribd when the publisher or an official repository has it | replace or remove |

When a tier 3 source backs a key number, search for a tier 1-2 source with the same figure and swap it in. When two credible sources disagree, show the range or say "varies by source" in the appendix.

**4. Clean the links.** Strip tracking parameters and text fragments (`?utm_...`, `#:~:text=...`), prefer DOIs or official repository links for papers, and make every URL a working clickable hyperlink. After editing, remove leftover hyperlink relationships in the slide `_rels` files that no text references any more.

**5. Format the Sources slide.** One appendix slide titled `Sources used`, numbered list, alphabetical by author, one style for every entry: `Author or organisation. (Year, Month Day). Title. Publisher. URL` with the title set in italics on the slide, no asterisks (use `n.d.` when there is no date). Always include the case itself (author, year, title, case number, publisher). Fit everything on one slide; this is the one appendix slide allowed down to 10pt (never smaller). Frameworks, icons (Flaticon credit) and data sources all go here.

**6. Report it.** In the delivery message, list in a few bullets which links were replaced or removed and why, and which remaining sources are weaker (tier 3 or estimates), so the team knows what judges could challenge.
