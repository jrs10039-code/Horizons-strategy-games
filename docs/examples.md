# Example results

Default assumptions, 1,000 futures, seed 2026, Current course strategy unless noted. "Profit" means total segment operating income. Every number comes from draft assumptions. These are examples of what the tool produces, not forecasts.

## The headline

> Under Current course, Disney's profit most likely grows from $19.7B to **$26.8B** by fiscal 2036. In a bad decade (10th percentile) it reaches only **$23.3B**. Three low-cost actions address **50% of the serious threats** and lift the bad decade to **$24.7B**.

## The thesis: three low-cost actions

Across 1,000 futures Disney faced about 17 serious threats per future. A serious threat costs $0.5B+ of profit over the decade; 41% of them were high-impact, costing $1.5B+. The tool searched its library of 10 actions for the three that cover the most serious-threat damage:

| # | Action | Cost | Threats it addresses |
| --- | --- | --- | --- |
| 1 | Pre-build a downturn playbook for the parks: pricing, staffing and cost triggers, plus phase-gates on the $60B plan | Near zero | Recession and rates; pandemic-class shutdown |
| 2 | Set up an AI rights and tools desk: license the library on Disney's terms, adopt AI production tools, track copyright | Low | AI disruption of content; legal and copyright |
| 3 | Put Disney IP where Gen Alpha already spends time: Roblox, Fortnite, YouTube creators | Low | Competition for kids' and young adults' time |

The three actions:

- **Cover** 50% of serious threats and 68% of their damage.
- **Re-simulated** on the same 1,000 futures with the actions in place, they avoid 18% of all threat damage.
- **Lift** the bad decade from $23.3B to $24.7B, and the most likely outcome from $26.8B to $27.7B.

**It holds up.** The same three actions come out on top under all six strategies and across five different random seeds. Coverage is 50–53% in every case.

**Caveat:** each action's effect (a 25–35% cut to the threats it addresses) is a draft assumption. The tool shows where the leverage is, not exactly how much each action delivers.

## Where the serious damage comes from

Recession and rates 21% · AI disruption of content 16% · Competition for young audiences' time 14% · Pandemic-class shutdown 13% · Rival parks and venues 8% · Weather and climate 6% · Asia 5% · Rival mergers 5% · Rival cruise lines 4% · Legal and copyright 4% · Brand 2% · Sports-rights bidding 1% · Carriage fights 1%

Sports-rights threats rank low in dollar terms, because Sports is the smallest segment ($3.1B of operating income). They still show up often.

## Threats that keep coming back

Share of futures where the threat is among that future's five costliest:

| Threat | Top 5 in |
| --- | --- |
| US recession cuts park visits and ad spend | 73% |
| AI-generated content floods supply | 52% |
| An AI-native studio makes film-quality content cheaply | 50% |
| Asia parks slump deepens | 37% |
| Immersive venues near cities take day-trip share | 36% |
| Personalized AI stories cut demand for fixed films and shows | 34% |
| Gen Alpha leaves long-form TV and film | 29% |
| AI copyright ruling weakens IP protection | 29% |

## Three individual futures

| Future | FY36 profit | Five costliest threats ($B of profit lost over the decade) |
| --- | --- | --- |
| Bad decade (10th pct) | $23.3B | Recession (7.7) · Personalized AI media (4.7) · AI content flood (3.5) · Gen Alpha leaves long-form (3.3) · Immersive venues (3.3) |
| Typical (median) | $26.8B | Recession (5.5) · Florida hurricane season (4.3) · AI content flood (2.4) · Personalized AI media (2.3) · AI copyright ruling (2.3) |
| Good decade (90th pct) | $29.4B | Recession (4.0) · Gen Alpha leaves long-form (3.1) · Extreme heat (2.5) · Universal park opening (1.8) · Creator-led franchise (1.7) |

## Strategy comparison

| Strategy | Bad decade | Most likely | Good decade |
| --- | --- | --- | --- |
| AI-forward | $23.6B | $26.8B | $29.5B |
| Streaming-first | $23.6B | $26.9B | $29.8B |
| Sports fortress | $23.5B | $26.8B | $29.3B |
| Current course | $23.4B | $26.7B | $29.3B |
| Experiences-heavy | $22.8B | $28.1B | $31.2B |
| Asset-light pivot | $22.4B | $24.7B | $26.8B |

These figures come from the Python engine. The site uses a different random-number generator, so its numbers differ by about $0.1B (for example $23.3B vs $23.4B for Current course).

Differences under about $0.5B are within simulation noise (see [stress-test.md](stress-test.md)). The robust findings:

- Experiences-heavy has the highest median and a weaker bad decade.
- Asset-light has the lowest upside.

## Backtest (FY19 to FY26)

- 10 of 11 listed threats happened.
- COVID lands at the 2nd–4th percentile with the pandemic-class event in the deck, and outside every simulated future without it.
- Actual FY26 ($19.7B) beat 98% of simulated futures: the model misses the rebound and the streaming turnaround.
