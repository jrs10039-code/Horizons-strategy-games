# AI War Room: switching on live games for the public site

On the Claude-hosted copy of Horizons, the AI War Room runs on the viewer's own Claude account, so there is nothing to set up. These steps switch on live games for the **public GitHub site**, paid by your Claude API key. It takes about 15 minutes, done once.

## How it works

The page on GitHub never sees your API key. It sends each request to a small private server (`api/agent.js`, hosted free on Vercel). The server checks the passcode, picks the model for each role, calls Claude with your key, and sends the answer back.

| Role | Model | Calls per run (3 games) |
| --- | --- | --- |
| Rival players (several companies per call, plus 2 newcomers per game) | Claude Sonnet 5.5 | about 45 |
| Disney's player | Claude Sonnet 5.5 | 15 |
| Referee (scores moves, sizes the scenario) | Claude Sonnet 5.5 | about 35 |
| Analyst | Claude Opus 5.5 | 1 |

Cost per run: check your Anthropic Console usage page after the first test run, and set a spend limit before you share the link. "Play 2 more games" costs about two-thirds of a run.

## Step 1: Anthropic API account (about 5 minutes)

1. Go to **console.anthropic.com** and sign up. This is separate from your Claude.ai subscription.
2. Add prepaid credits: $10–20 is plenty for a handful of people.
3. Set a **monthly spend limit** in the Console's limits or billing settings, for example $20. This is your safety net.
4. Create an **API key** and copy it. It is shown only once.

## Step 2: Vercel (about 5 minutes)

1. Go to **vercel.com** and sign up with your GitHub account.
2. Click **Add New → Project** and import `Horizons-strategy-games`.
3. Leave the build settings as they are (Framework preset: Other).
4. Open **Environment Variables** and add two:
   - `ANTHROPIC_API_KEY`: the key from Step 1
   - `PASSCODE`: a word you will put in your email, for example `epcot1983`
5. Click **Deploy**.
6. Send Claude the project's address, for example `horizons-strategy-games.vercel.app`. If it differs from that, one line in `index.html` (`AGENT_API`) gets updated.

## Step 3: Test once

1. Open the public site in a private browser window and go to **AI War Room**.
2. Enter the passcode and click **Play 3 games**.
3. Check the Anthropic Console usage page afterwards to see what the click cost.

## Safety notes

- **The key** never appears in the page or the repo. It lives only in Vercel's settings.
- **The passcode** keeps strangers from spending your credits. Change it in Vercel at any time.
- **The spend limit** caps your worst case.
- **To switch it off**, delete the API key in the Console or pause the Vercel project.
