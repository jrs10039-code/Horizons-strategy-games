# Stress test: findings, fixes and suggestions

I ran the model through extreme settings, different random seeds and different run counts, and checked its accounting. Run date: November 20, 2026.

## Checks that passed

| Check | Result |
| --- | --- |
| All shocks and competitors off | No damage recorded; profit simply compounds to $31.7B by FY36 (the no-threat ceiling) |
| Everything at maximum | No errors or blanks. Worst year bottoms at $2.3B (the 5% floor works); median FY36 $22.0B |
| Highest single-event probability at maximum | 36% a year, so no probability exceeds 100% |
| Monotonic: industry aggression 0 → 25 → 50 → 75 → 100 | Median FY36 falls steadily: $28.4B → $27.6B → $26.8B → $26.1B → $25.5B |
| Same seed, same settings | Identical futures (also covered by a unit test) |
| Thesis stability across 5 seeds | The same three actions every time; coverage 50% each time |
| Thesis stability across 6 strategies | The same three actions under all 6; coverage 50–53% |
| Damage accounting | Tracked threat damage ($43.4B per future) vs. the gap to a no-threat run ($41.2B): within 6% (overlap and the floor cause the gap) |
| Python vs. browser | Same model, same conclusions; tiny differences come from different random generators |

## Bug found and fixed

**Competitor moves could repeat while still playing out.** Before the fix, a single company could "open a park near a Disney market" several times a decade: up to 6 times in one future, 3.4 on average for the most frequent event. That is unrealistic.

- **Fix:** a cooldown. A move cannot fire again until its last one has run its course (usually 4 years). The random draw is still taken, so every strategy keeps seeing the same futures.
- **Effect:** events per future fell from 79 to 69. One-year events, such as a hurricane season, can still happen in back-to-back years. The Current course bad decade moved from $22.4B to $23.3B. The backtest conclusions are unchanged.

## Findings to know before presenting

1. **Strategy rankings in the middle are noise.** Across seeds the bad-decade value moves by about $0.7B (from $23.3B to $24.0B for Current course), while AI-forward, Sports fortress, Current course and Streaming-first sit within about $0.3B of each other, and their order changes from seed to seed. Only two findings are robust: Experiences-heavy has the widest range, and Asset-light has the lowest upside. The site now says so on the Compare strategies tab.
2. **200 futures is too few for the bad-decade number.** It shifts by about $0.5B; 1,000 is the right default.
3. **The "learning as it goes" effect is generous.** A 30% softer second hit adds about $2.8B to the bad decade. That is a draft assumption, and it is worth stress-testing with the team.
4. **Sports looks small in dollar terms** because it is the smallest segment. Rights threats recur often but rank low on damage. A team might weight strategic importance, not only operating income.
5. **Action effects are assumptions.** The tool identifies where the leverage is (which threat types drive the damage). The 25–35% cut per action is judgment.

## Suggestions, in priority order

1. **Streaming margin as its own variable, plus rebound after shocks.** This fixes the main backtest miss (FY26 actual beat 98% of futures).
2. **Correlated shocks.** A recession should raise the odds of ad-market and travel shocks in the same year. Today every event is independent.
3. **Competitors react to Disney.** Today rivals move on fixed odds whatever Disney does.
4. **Real financial data.** SEC EDGAR (free, US-listed companies only) for competitor size and growth; Capital IQ or FactSet for the rest. This needs a small backend, because a static site cannot hold API keys.
5. **Port the risk-and-actions analysis to the Python engine.** It currently runs only in the browser.
6. **A cost-and-benefit view per action:** dollars avoided per dollar spent, once the team prices each action.
