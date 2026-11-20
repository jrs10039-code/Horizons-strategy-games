"""Monte Carlo war-game engine.

Python reference implementation of the model behind the browser prototype
(index.html). Same assumptions file, same logic. It is the piece a strategy
team would own and extend: pure functions, no UI, every assumption read from
config/assumptions.json.

Model, in one paragraph: each simulated year, PESTEL shocks, moves by 109 competitors
and startup archetypes fire with set probabilities. Each one cuts (or lifts)
segment operating income by a set fraction for a set number of years. The
chosen Disney playbook sets each segment's base growth and how exposed it is
to each kind of threat. With early-warning triggers on, the first hit of a
threat type makes later hits of the same type land softer.
"""

from __future__ import annotations

import json
import random
import statistics
from dataclasses import dataclass, field
from pathlib import Path

SEGMENTS = ("exp", "ent", "spt")
SEGMENT_NAMES = {"exp": "Experiences", "ent": "Entertainment", "spt": "Sports"}
DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "assumptions.json"


def load_config(path: str | Path = DEFAULT_CONFIG) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@dataclass
class Event:
    id: str
    label: str
    source: str
    prob: float          # annual probability
    impact: dict         # segment -> fraction of OI while active
    duration: int        # years active
    tag: str             # threat type, used for playbook exposure and triggers
    once: bool = False   # archetypes arrive once and stay


@dataclass
class Run:
    totals: list[float]                              # total segment OI, FY0..FYn
    first_seen: dict[str, int] = field(default_factory=dict)
    log: list[tuple[int, Event]] = field(default_factory=list)


def backtest_config(cfg: dict) -> dict:
    """Return a copy of cfg set up for the FY19-FY26 backtest."""
    bt = cfg["backtest"]
    out = dict(cfg)
    out.update(start_fy=bt["start_fy"], start_segment_oi_busd=bt["start_segment_oi_busd"],
               years=bt["years"], playbooks=[bt["playbook"]], _excluded=set(bt["excluded_events"]))
    return out


def build_events(cfg: dict, settings: dict) -> list[Event]:
    """Turn the assumptions plus slider settings into annual probabilities."""
    names = {c["id"]: c["name"] for c in cfg["pestel_categories"]}
    events = []
    for e in cfg["pestel_events"]:
        w = settings["pestel_weights"][e["src"]]
        events.append(Event(e["id"], e["label"], names[e["src"]], e["p"] * w / 3,
                            e["imp"], e["dur"], e["tag"]))
    for p in cfg["players"]:
        a = settings["player_aggression"][p["id"]]
        arena = settings["arena_aggression"][p["arena"]]
        events.append(Event(p["id"], p["label"], p["name"], p["p"] * a / 50 * arena / 50,
                            p["imp"], p["dur"], p["tag"]))
    for a in cfg["archetypes"]:
        r = settings["archetype_arrival_pct"][a["id"]]
        events.append(Event(a["id"], a["label"], "Startup: " + a["name"], r / 100,
                            a["imp"], cfg["years"], a["tag"], once=True))
    excluded = set(cfg.get("_excluded", ()))
    if not settings.get("tail", True):
        excluded.add("pandemic")
    return [e for e in events if e.id not in excluded]


def simulate_one(cfg: dict, playbook: dict, events: list[Event],
                 rng: random.Random, triggers: bool) -> Run:
    years = cfg["years"]
    base = dict(cfg["start_segment_oi_busd"])
    run = Run(totals=[sum(base.values())])
    active: list[tuple[int, dict]] = []     # (last active year, scaled impact)
    mitigation: dict[str, float] = {}

    for y in range(1, years + 1):
        for e in events:
            if e.once and e.id in run.first_seen:
                continue
            if rng.random() < e.prob:
                run.first_seen.setdefault(e.id, y)
                run.log.append((y, e))
                exposure = playbook["sens"].get(e.tag, 1.0)
                damp = mitigation.get(e.tag, 1.0)
                scaled = {k: v * cfg["impact_scale"] * exposure * (damp if v < 0 else 1.0)
                          for k, v in e.impact.items()}
                active.append((y + e.duration - 1, scaled))
                if triggers and any(v < 0 for v in e.impact.values()):
                    mitigation[e.tag] = cfg["trigger_mitigation"]

        factor = {k: 1.0 for k in SEGMENTS}
        for until, imp in active:
            if y <= until:
                for k, v in imp.items():
                    factor[k] += v

        total = 0.0
        for k in SEGMENTS:
            base[k] *= 1 + playbook["g"][k] + cfg["noise_sd"] * rng.gauss(0, 1)
            total += base[k] * max(cfg.get("segment_floor", 0.05), factor[k])
        run.totals.append(total)
    return run


def run_set(cfg: dict, playbook_id: str, settings: dict, triggers: bool | None = None) -> list[Run]:
    """Run N futures for one playbook. Same seed = same futures across playbooks."""
    playbook = next(p for p in cfg["playbooks"] if p["id"] == playbook_id)
    trig = settings["triggers"] if triggers is None else triggers
    rng = random.Random(settings["seed"])
    events = build_events(cfg, settings)
    return [simulate_one(cfg, playbook, events, rng, trig) for _ in range(settings["runs"])]


def percentile(values: list[float], q: float) -> float:
    s = sorted(values)
    i = (len(s) - 1) * q
    lo, hi = int(i), min(int(i) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (i - lo)


def summarize(cfg: dict, runs: list[Run]) -> dict:
    years = cfg["years"]
    start = runs[0].totals[0]
    final = [r.totals[years] for r in runs]
    mid = years // 2
    return {
        "p10": percentile(final, 0.1),
        "p50": percentile(final, 0.5),
        "p90": percentile(final, 0.9),
        "share_below_start_at_midpoint": sum(r.totals[mid] < start for r in runs) / len(runs),
    }


def themes(cfg: dict, runs: list[Run], settings: dict, bad_share: float = 0.2) -> list[dict]:
    """Rank events by what they cost when they hit (median final OI, hit vs not hit)."""
    years = cfg["years"]
    n = len(runs)
    order = sorted(range(n), key=lambda i: runs[i].totals[years])
    bad = set(order[: max(1, int(n * bad_share))])
    rows = []
    for e in build_events(cfg, settings):
        hit = [runs[i].totals[years] for i in range(n) if e.id in runs[i].first_seen]
        miss = [runs[i].totals[years] for i in range(n) if e.id not in runs[i].first_seen]
        if not hit or not miss:
            continue
        rows.append({
            "event": e.label,
            "source": e.source,
            "share_all": len(hit) / n,
            "share_bad": sum(1 for i in bad if e.id in runs[i].first_seen) / len(bad),
            "cost_when_hits_busd": statistics.median(hit) - statistics.median(miss),
            "upside": any(v > 0 for v in e.impact.values()),
        })
    return sorted(rows, key=lambda r: r["cost_when_hits_busd"])
