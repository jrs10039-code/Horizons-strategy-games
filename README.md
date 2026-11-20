# Strategy War Game

**A strategic early warning system built on war gaming.** It simulates Disney against 12 competitors and 4 startup archetypes over FY27–FY36, thousands of times, then surfaces the threats that keep showing up in the bad futures.

**[Open the live simulator →](https://USERNAME.github.io/strategy-war-game/)** Runs in your browser, no login.

> Prototype by Jake Schmidt. All assumptions are illustrative drafts built from public information, designed to be overwritten with a strategy team's own views and data. It is a risk-preparedness tool, not a forecast.

## What it answers

- **Which playbook holds up?** Six Disney playbooks run against the *same* simulated futures, so the comparison is fair. Robust playbooks keep the bad case (10th percentile) high, not just the median.
- **What should we watch?** Each event is ranked by what it costs when it hits. The costliest ones become **signposts**: observable signals worth monitoring.
- **Does early warning pay?** With triggers on, Disney responds after the first hit of a threat type, and later hits land softer. The simulator measures how much that protects the bad case.

## How the model works

1. **Starting point:** FY26 segment operating income from Disney's FY26 Q4 8-K: Experiences $11.19B, Entertainment $5.44B, Sports $3.09B.
2. **Each simulated year**, events fire with set annual probabilities:
   - **PESTEL shocks** (recession, AI content flood, hurricanes, copyright rulings, and so on), weighted by category
   - **Competitor moves** (Netflix wins a sports package, Universal opens a nearby park, and so on), scaled by each player's aggression
   - **Startup archetypes** (AI-native studio, personalized AI media, and so on), which arrive once and stay
3. Each event cuts or lifts segment OI by a set fraction for a set number of years.
4. **The playbook** sets each segment's base growth and its exposure to each threat type.
5. Repeat 1,000–5,000 times, with a seeded random generator so results can be reproduced.

Every number lives in [`config/assumptions.json`](config/assumptions.json). Disagree with one? Change it and rerun.

## Repo layout

| Path | What it is |
| --- | --- |
| `index.html` | The browser simulator. One self-contained file with sliders for every assumption. |
| `engine/simulator.py` | Python reference engine: same model, no UI, reads the assumptions file. |
| `run.py` | Command-line runner: playbook comparison plus the costliest events. |
| `config/assumptions.json` | Every assumption: players, events, impacts, probabilities, playbooks. |
| `tests/` | Checks for reproducibility, the starting point, trigger value, and pure compounding. |

```bash
python run.py                          # default assumptions, 1,000 futures per playbook
python run.py --runs 5000 --playbook D
python -m pytest tests
```

No dependencies beyond Python 3.9+ (pytest for the tests).

## How a strategy team would productionize it

| Layer | Prototype | Production |
| --- | --- | --- |
| Engine | One Python file | Same logic, versioned and tested; assumptions owned by the strategy team |
| Data | Public filings, draft judgment | Capital IQ / FactSet for competitors; internal FP&A for Disney's own numbers |
| Interface | One HTML page | The team's existing BI tool or a small internal app |
| Access | Public link | Company cloud and single sign-on; insider inputs for managers and up only |
| Monitoring (phase 2) | Not built | An approved AI model reads news, earnings calls and M&A, then *proposes* input changes. A manager approves each one, every change is logged, and the sim reruns on triggers (earnings, major deals). |

**Model-agnostic by design.** The engine contains no AI. AI only sits in the phase 2 monitoring layer, behind a thin adapter, so the model is a configuration choice.

**Pilot proposal.** 6–12 months. Before it starts, the team logs its own risk calls with timestamps. Keep the tool only if it flagged 3–5 risks earlier than the team did.

## Roadmap

- [ ] **2019 backtest:** start from FY2019 inputs only, and check whether the sim surfaces the risks that actually hit (streaming losses, linear decline, sports-rights inflation, Epic Universe, Asia weakness).
- [ ] Disney M&A moves and a balance sheet (cash and debt limits on moves)
- [ ] Phase 2 monitoring pilot
