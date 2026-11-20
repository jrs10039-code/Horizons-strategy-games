from engine.simulator import load_config, run_set, summarize, backtest_config


def _settings(cfg, runs=300):
    s = dict(cfg["defaults"])
    s["runs"] = runs
    return s


def test_same_seed_same_futures():
    cfg = load_config()
    a = run_set(cfg, "A", _settings(cfg))
    b = run_set(cfg, "A", _settings(cfg))
    assert [r.totals for r in a] == [r.totals for r in b]


def test_starts_at_fy26_actuals():
    cfg = load_config()
    r = run_set(cfg, "A", _settings(cfg, runs=1))[0]
    assert abs(r.totals[0] - 19.72) < 1e-9


def test_triggers_protect_the_downside():
    cfg = load_config()
    s = _settings(cfg)
    on = summarize(cfg, run_set(cfg, "A", s, triggers=True))
    off = summarize(cfg, run_set(cfg, "A", s, triggers=False))
    assert on["p10"] > off["p10"]


def test_no_shocks_means_pure_compounding():
    cfg = load_config()
    s = _settings(cfg, runs=1)
    s["pestel_weights"] = {k: 0 for k in s["pestel_weights"]}
    s["player_aggression"] = {k: 0 for k in s["player_aggression"]}
    s["archetype_arrival_pct"] = {k: 0 for k in s["archetype_arrival_pct"]}
    cfg = dict(cfg, noise_sd=0.0)
    r = run_set(cfg, "A", s)[0]
    g = next(p for p in cfg["playbooks"] if p["id"] == "A")["g"]
    expected = sum(v * (1 + g[k]) ** cfg["years"] for k, v in cfg["start_segment_oi_busd"].items())
    assert abs(r.totals[-1] - expected) < 1e-9


def test_no_shocks_test_disables_tail():
    cfg = load_config()
    assert any(e["id"] == "pandemic" for e in cfg["pestel_events"])


def test_backtest_starts_at_fy19_and_excludes_ai():
    cfg = load_config()
    bt = backtest_config(cfg)
    s = _settings(cfg, runs=50)
    runs = run_set(bt, "P19", s)
    assert abs(runs[0].totals[0] - 14.85) < 1e-9
    assert len(runs[0].totals) == 8
    assert all("aiflood" not in r.first_seen and "openai" not in r.first_seen for r in runs)
