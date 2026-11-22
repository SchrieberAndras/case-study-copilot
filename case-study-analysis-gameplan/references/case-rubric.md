# The case strategy rubric

Every match is a fight between two strategies for the same business-school case. Score both against
this page. The arena skill's `bracket.py` does the arithmetic and the higher weighted total goes through.

The task you were given points to `COBE_<Case>_CaseFacts.md`, the complete case record. The task and that file carry the case question,
the brief's hard constraints, the root cause and its drivers, the precedents and reference points, and the full stress tests
(knock-out tests and pillar tests). The case PDF is not available; do not look for it, and do not search the web. This rubric
tells you how those turn into scores. Check the facts file whenever a fact or a number decides a score: a strategy that
sounds right but misreads the case loses.

## The five criteria

Each criterion is scored 0 to 10. The weight is how much of the 100-point total it is worth.

| criterion | weight | the question |
| --- | --- | --- |
| Correctness | 30 | Are the case facts, numbers and calculations right, and is every assumption labelled? |
| Completeness | 25 | Does it answer the case question, fix every root-cause driver, and meet every brief constraint and required output element? |
| Specificity | 15 | Is it concrete and specific to this company: actions with who and when, KPIs with targets, numbers from the case? |
| Robustness | 20 | Does it survive this match's attacks and the soft stress tests: economics, competitor response, pre-mortem, second-order effects? |
| Clarity | 10 | Can it be presented: one "We recommend ..." sentence, coherent pillars, 3-4 KPIs, within the word limit? |

Weighted total = (correctness x 30 + completeness x 25 + specificity x 15 + robustness x 20 + clarity x 10) / 10.
That gives a number from 0 to 100.

## Anchors

Use the whole scale. A 7 is not a polite default.

**Correctness**
- 10: every fact and number matches the case or a named source; calculations check out when you redo them; assumptions are labelled as assumptions.
- 7: a minor slip (a rounding error, a wrong exhibit reference) that does not change the recommendation.
- 4: a wrong number or a misread fact that a key argument rests on, or an unlabelled assumption presented as a case fact.
- 0 to 2: it misreads what the case is about, or the economics are wrong at the core.

**Completeness**
- 10: answers the exact case question for the decision maker; every root-cause driver named in the task is fixed by the strategy or a pillar; every brief constraint and every required output element (umbrella name, "We recommend ..." sentence, pillars with drivers, actions, KPI, numbers, risks, rejected options) is there.
- 7: everything is there, one element is thin (for example a KPI with no target).
- 4: a root-cause driver is left unfixed, or a required output element or brief item is missing.
- 0 to 2: it answers a different question from the case question.

**Specificity**
- 10: the decision maker could start Monday: who does what by when, KPIs with numeric targets and time frames, figures taken from the case.
- 7: mostly concrete, one or two actions without an owner or a date.
- 4: generic moves ("invest in digital", "improve marketing") that would fit any company in the industry; few numbers.
- 0 to 2: textbook advice with nothing from this case in it.

**Robustness**
- 10: every attack in this match is fixed or correctly rebutted, and the strategy holds up on economics (impact versus cost with case numbers, plausible payback), competitor response (the advantage survives what the 2-3 main rivals do next), the pre-mortem (the most likely failure story has a mitigation) and second-order effects (no damage to another strength of the company).
- 7: one MINOR attack still standing, or one soft test answered only thinly.
- 4: a MAJOR attack still standing, or a soft test it clearly fails (for example rivals can copy it in a month, or the payback is implausible).
- 0 to 2: a FATAL attack still standing.

A missing attack file means the opponent raised nothing. Score robustness on the flaws you found yourself, against the soft stress tests.

**Clarity**
- 10: one "We recommend ..." sentence carries the whole strategy; pillars (if any) are 2-4, follow one umbrella logic, do not overlap, and have a clear order; 3-4 KPIs measure it; within the word limit.
- 7: presentable, with one padded pillar or one confusing section.
- 4: more than 4 pillars, overlapping pillars, or no single sentence that states the recommendation.
- 0 to 2: a list of unrelated ideas.

## The fatal rule

Mark a strategy `fatal` only when you have verified, against the case, that it fails a knock-out test:

- It does not answer the case question (knock-out test 1).
- It treats a symptom and leaves the root cause untouched (knock-out test 2).
- It breaks a hard constraint: a value or non-negotiable stated in the case, a legal limit, or the professor's brief (knock-out test 3).
- The company cannot do it with the capabilities, money and time the case gives it, or can realistically get (knock-out test 4).
- A pillar breaks a hard constraint or is infeasible on its own (pillar test 12).
- The pillars are unrelated recommendations with no umbrella logic (pillar test 14).
- A central number or fact is invented and the recommendation rests on it.

A fatal strategy cannot beat one that is not fatal, whatever the totals say. If both are fatal, the totals decide.

## Ties

There are no draws. On an exact tie, the strategy with fewer attacks still standing wins. If that is
also level, the higher correctness score wins. If that is also level, pick the one you would rather
defend in front of a sceptical professor, and say why in the reason.

## What the judge does not reward

- **Length.** A tight strategy that meets every requirement beats a long one that meets the same requirements.
- **Boldness or caution for its own sake.** A bold move scores well only if it passes the knock-outs and the economics; a safe one scores well only if it actually fixes the root cause.
- **Framework names.** Naming SWOT or Porter earns nothing; the finding it produces for this case does.
- **Confidence.** A defense that says "fixed" is not proof. Check the revised strategy.
- **The approach.** You never see the strategy cards and do not guess at them. Score the strategy, not the method that produced it.
- **Agreement with your own pick** where the case does not decide it.
