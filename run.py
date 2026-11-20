"""Command-line runner: compare playbooks and list the themes in bad futures.

    python run.py                      # default assumptions, 1,000 futures
    python run.py --runs 5000 --seed 7
    python run.py --playbook D --no-triggers
    python run.py --config my_assumptions.json
"""

import argparse

from engine.simulator import load_config, run_set, summarize, themes, DEFAULT_CONFIG


def main() -> None:
    ap = argparse.ArgumentParser(description="Strategy war game: Monte Carlo of Disney vs. competitors")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--playbook", default=None, help="Playbook id for the themes table (A-F)")
    ap.add_argument("--runs", type=int, default=None)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--no-triggers", action="store_true")
    args = ap.parse_args()

    cfg = load_config(args.config)
    settings = dict(cfg["defaults"])
    if args.runs:
        settings["runs"] = args.runs
    if args.seed:
        settings["seed"] = args.seed
    if args.playbook:
        settings["playbook"] = args.playbook
    settings["triggers"] = not args.no_triggers

    end_fy = cfg["start_fy"] + cfg["years"]
    mid_fy = cfg["start_fy"] + cfg["years"] // 2
    print(f"\n{settings['runs']:,} futures per playbook, seed {settings['seed']}, "
          f"triggers {'on' if settings['triggers'] else 'off'}\n")
    print(f"FY{end_fy % 100} total segment OI ($B)")
    print(f"{'Playbook':<24}{'P10':>8}{'Median':>8}{'P90':>8}   Below FY{cfg['start_fy'] % 100} in FY{mid_fy % 100}")
    for pb in cfg["playbooks"]:
        s = summarize(cfg, run_set(cfg, pb["id"], settings))
        print(f"{pb['name']:<24}{s['p10']:>8.1f}{s['p50']:>8.1f}{s['p90']:>8.1f}"
              f"   {s['share_below_start_at_midpoint']:>6.0%}")

    pb = next(p for p in cfg["playbooks"] if p["id"] == settings["playbook"])
    runs = run_set(cfg, pb["id"], settings)
    print(f"\nCostliest events under {pb['name']} (median FY{end_fy % 100} OI, hit vs not hit)")
    for r in themes(cfg, runs, settings)[:10]:
        print(f"  {r['cost_when_hits_busd']:+6.1f}B  {r['event']}  ({r['source']})")
    print()


if __name__ == "__main__":
    main()
