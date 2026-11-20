# Methodology

How Horizons works, how it is calibrated, how it scores against history, and what it cannot do yet.

## 1. What it is for

The model is an early warning system, not a forecast. It is built to answer three questions:

1. **Which Disney strategy holds up across many futures?** A strategy that holds up still does reasonably well in its worst futures. The tool judges strategies on their bad-decade result (the 10th percentile: 1 in 10 futures end lower), not only on their typical result.
2. **Which threats cost the most when they hit?** Those become signposts to monitor.
3. **Is early warning worth paying for?** This is measured as the lift in the bad case when Disney responds after the first hit of a threat type.

## 2. Mechanics

Each simulated year:

1. **Events fire.** Each event has an annual probability:
   - **PESTLE shocks:** 13 events across six categories: Political, Economic, Social, Technological, Legal and Environmental. Probability = base probability × category weight / 3.
   - **Competitor moves:** 109 companies. Tier probability × company aggression / 50 × arena aggression / 50.
   - **Startup archetypes:** 4. Each arrives once at most, then stays.
2. **Impacts apply.** Each event changes one or more segments' operating income by a set fraction for a set number of years. Impacts from different events add up. A segment cannot fall below 5% of its underlying level. A move cannot repeat while its last occurrence is still playing out (cooldown).
3. **Playbook exposure.** The chosen playbook multiplies impacts by threat type. For example, Sports fortress halves the impact of rights moves, and Experiences-heavy makes recessions 1.6× worse.
4. **Underlying growth.** Each segment compounds at the playbook's growth rate, plus random noise (2% standard deviation per year).
5. **Triggers.** With triggers on, after the first negative hit of a threat type, later hits of that type land 30% softer.

The run is repeated 200 to 5,000 times with a seeded random generator, so the same settings always give the same futures. All playbooks see the same random draws, which makes the comparison fair.

## 3. Competitor tiers

| Tier | Annual probability at default aggression | Impact on the segment it hits, per year active | Meaning |
| --- | --- | --- | --- |
| 1 | 9% | −2.5% × 1.5 severity scale | Can move a whole segment (Netflix, Universal, NFL) |
| 2 | 7% | −0.7% × 1.5 | Meaningful in its niche (MSC Cruises, Roku, F1) |
| 3 | 5% | −0.3% × 1.5 | Early or narrow (Meow Wolf, Overtime, Luma AI) |

Each competitor move lasts 4 years. The full roster is in [competitors.md](competitors.md).

## 4. Calibration

The global severity scale (1.5) and the tier impacts were set so that, under default assumptions and the Current course playbook:

- the median FY36 outcome (about $26.8B) implies about 3% a year compound growth. That is below Disney's FY27 guidance of about +8%, because shocks drag on the underlying 4–5% growth;
- roughly a fifth to a quarter of futures sit below FY26 profit in FY31, so the downside is real but not dominant;
- the 2019 backtest ends near Disney's actual FY26 result (see below).

These are judgment calls, chosen to make the tool useful for discussion. The model is not fitted statistically.

## 5. Backtest: FY19 to FY26

**Setup.** The sim starts from FY19 total segment OI of $14.85B (as recast in Disney's FY20 release), split into Experiences $6.76B (Parks, Experiences & Products, FY19 10-K), Sports about $3.0B (an assumption, since ESPN was not broken out) and Entertainment as the remainder. The playbook is a "2019 plan": Experiences +6%, Entertainment +3% (heavy Disney+ investment), Sports +2%. Threats nobody could have listed in 2019 are removed, such as generative AI, Sora-style tools, Netflix House, Qiddiya and Cosm.

**Result.** Default settings, 1,000 futures:

| Fiscal year | Sim 10th pct | Sim median | Sim 90th pct | Actual | Actual percentile |
| --- | --- | --- | --- | --- | --- |
| FY20 | 13.3 | 14.8 | 15.3 | 8.1 | 2nd |
| FY21 | 12.8 | 14.8 | 15.6 | 7.8 | 4th |
| FY22 | 13.2 | 15.0 | 16.0 | 12.1 | 4th |
| FY23 | 13.6 | 15.4 | 16.4 | 12.9 | 5th |
| FY24 | 14.4 | 16.3 | 17.4 | 15.6 | 29th |
| FY25 | 14.8 | 17.0 | 18.2 | 17.6 | 74th |
| FY26 | 15.7 | 17.6 | 19.0 | 19.7 | 98th |

All values are total segment operating income in $B. Actuals come from Disney's annual earnings releases. Segment definitions changed in FY20, FY21 and FY23, and FY20 and FY26 had 53 weeks.

**What it teaches**

1. **The threat deck was right.** 10 of the 11 threats a 2019 team could have listed happened by FY26: rivals moved into sports rights (Amazon, Netflix, YouTube, the NBA's 2024 deals), studios consolidated (Warner Bros. Discovery, Paramount Skydance), Universal opened Epic Universe, Asia parks weakened, and hurricanes hit. The one that did not happen was a non-pandemic US recession.
2. **Tail events matter.** With a 1.5%-a-year pandemic-class event, the COVID trough lands at the 2nd–4th percentile. Without it, the trough falls outside every simulated future. Lesson: always carry low-probability, high-severity shocks.
3. **The recovery outran the model.** Actual FY26 landed at the 98th percentile. The model has no rebound dynamics (pent-up demand, pricing power after reopening) and no streaming turnaround (Disney went from roughly $4B of DTC losses in FY22 to profit). Next fix: model streaming margin as its own variable.

Run it yourself with `python run.py --backtest`, or the Backtest switch on the site.

## 6. Risks and actions

For each future the tool records how much profit each threat took over the decade. A threat costing $0.5B+ in a future counts as serious; $1.5B+ counts as high-impact. A library of 10 low-cost actions maps each action to the threat types it softens, by a draft 20–35%. The tool greedily picks the three actions that cover the most serious-threat damage, then re-runs the same futures with them in place. Results and caveats are in [examples.md](examples.md) and [stress-test.md](stress-test.md).

## 7. Known limits

- No balance sheet: moves are not limited by cash or debt.
- No Disney M&A, and competitors do not react to Disney's moves (the interaction is one way).
- Events are independent. In reality a recession and an ad slump arrive together.
- No rebound or mean reversion after shocks.
- Probabilities and impacts are draft judgment from public information, not estimates from data.

## 8. How to change an assumption

- **On the site:** move the slider. Use "Save or load assumptions" to share settings as text.
- **In code:** edit `config/assumptions.json` and rerun `python run.py`. The site and the Python engine use the same model; the JSON is exported from the site's assumptions.
