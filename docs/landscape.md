# Where Horizons sits in the market

Notes as of November 2026. This is about tools like Horizons, not Disney's competitors (those are in [competitors.md](competitors.md)).

## What to call it

"Competitive intelligence" usually means *monitoring*: tracking what rivals are doing now. Horizons looks forward and plays out moves and countermoves. The established names for that are **business war gaming** and **strategic simulation**. Newer AI vendors use **strategic foresight**. Horizons is described here as a *strategic early warning simulator built on war gaming*.

## Who sells this

| Type | Examples | How it works | Notes |
| --- | --- | --- | --- |
| Human-run war games | Fuld & Company (since 1979), pharma-focused CI firms | One- or two-day workshops with briefing books and role-playing teams | Proven, but expensive and occasional. Pharma is the heaviest buyer. |
| Strategy consultancies | BCG (AI-enhanced war gaming; Henderson Institute multi-agent platform) | Hybrid games with human and AI players, run as engagements | No public self-serve product. |
| AI strategic foresight startups | **Principle** (futureprinciple.com) | Builds digital models of companies, competitors, regulators and markets, then runs hundreds of futures per decision | Pre-seed (about $2.5M, 2026). Has a media and entertainment page aimed at studios, streamers, sports and parks: slate bets, park capex, rights, M&A, franchise funding. Says it has done proof-of-value work with an unnamed major entertainment company. No public example simulations or pricing. |
| Small self-serve tools | GameTheory (Product Hunt), IDEO's competitor-battle tool | Adversarial AI agents stress-test one plan | Lightweight; not calibrated to a company's financials. |
| Synthetic customer simulation (adjacent) | Simile ($2B valuation, Jul 2026), Aaru ($1B headline, Dec 2025) | Simulate how customers or the public respond | Where most of the venture money is. They simulate customers, not competitors. |
| Defense and government | RAND, GenWar Sim, Anadyr Horizon | AI players in geopolitical or military games | A separate market; the source of most published research. |

## What the evidence says

No one has published hard return-on-investment numbers for AI business war games; what exists is vendor case studies. The research on AI players is mixed:

- In a Stanford study with 107 national-security experts, AI players matched human choices on about half of the actions and differed systematically on the rest, and results depended on which model was used.
- The same work found AI players got more aggressive depending on how the game was prompted.
- A 2026 study found AI players start out close to human behavior but drift apart over later rounds.

## How Horizons answers those weaknesses

| Known weakness | What Horizons does |
| --- | --- |
| AI invents numbers | The app computes each move's dollar value itself from the referee's percent effects, and the referee must show its arithmetic. Each ruling and each analyst finding is labeled **Fact / Stated / Assumption / Hypothesis / Contradicted** by what it rests on (idea borrowed from Principle's evidence labels). |
| AI players drift or over-escalate over many rounds | Calibration bands per move, a cap on total rival pressure per segment, a background drag for ~100 smaller rivals, and a referee that remembers past rulings so nothing is counted twice. |
| Results are a black box | Every game is logged move by move; the analyst must cite specific moves; each finding says what would have to be true for it to pay off. |
| No sense of the normal range | A rules-based Monte Carlo of 1,000 decades sits alongside the AI games, and the model is backtested from FY19. |
| Can't tell an effect from luck | Scenario games are played in matched pairs with the same outside shocks and newcomers, so the scenario's effect is isolated. |

## Where Horizons is different

- Built on Disney's actual segment operating income and checked against FY19-FY26 results.
- A rules-based simulator and the AI game side by side, rather than AI alone.
- Open: every assumption is a slider or a line in `config/assumptions.json`.
- What it is not: a vendor product with proprietary data. It's a prototype a strategy team could own and extend in-house.
