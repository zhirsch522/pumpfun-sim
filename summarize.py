#!/usr/bin/env python3
"""Builds data/summary.json and data/summary.md from the v2 sim journal."""
import json, os, random, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim

D = sim.DATA_DIR
C = sim.CFG
def jl(name):
    try:
        with open(os.path.join(D, name)) as fh: return [json.loads(l) for l in fh if l.strip()]
    except FileNotFoundError: return []

def ret_pct(entry_px, exit_px):
    q = C["ticket_usd"] * (1 - C["fee"]) / sim.buy_px(entry_px)
    return 100 * (sim.sell_value(q, exit_px) - C["ticket_usd"]) / C["ticket_usd"]

def stats(xs):
    if not xs: return None
    return {"n": len(xs), "avg_pct": round(statistics.mean(xs), 2), "median_pct": round(statistics.median(xs), 2),
            "win_rate": round(100 * sum(x > 0 for x in xs) / len(xs), 1)}

def random_hold(rows, key_entry, key_path, rng, draws=50):
    out = []
    for r in rows:
        e = r.get(key_entry); path = [px for _, px in (r.get(key_path) or [])[1:] if px]
        if not e or not path: continue
        for _ in range(draws): out.append(ret_pct(e, rng.choice(path)))
    return out

def hold_for(rows, minutes):
    out = []
    for r in rows:
        e = r.get("entry_px"); path = r.get("path") or []
        if not e or len(path) < 2: continue
        t0 = path[0][0]; later = [px for t, px in path if t - t0 >= minutes * 60 and px]
        exit_px = later[0] if later else path[-1][1]
        if exit_px: out.append(ret_pct(e, exit_px))
    return out

WALLET_START = 20.0
WALLET_RISK = 0.25   # each paper trade stakes 25% of the wallet's current value (max 3 open = up to 75% in)

def wallet_replay(alltr, book):
    """Replays one book's logged trades as a $20 wallet that sizes each trade at 25% of its value.
    Each trade keeps its logged return (fees and slippage included); open stakes are marked at cost."""
    events = []
    entries = {}
    for t in alltr:
        if t.get("book") != book: continue
        if t.get("event") == "entry": entries.setdefault(t["pool"], []).append(t["ts"]); events.append((t["ts"], 0, t["pool"], None))
        elif t.get("event") == "exit": events.append((t["ts"], 1, t["pool"], t["proceeds"] / t["cost"] if t["cost"] else 0))
    events.sort()
    cash, open_, peak, max_dd, n = WALLET_START, {}, WALLET_START, 0.0, 0
    for ts, kind, pool, mult in events:
        if kind == 0:
            stake = min(cash, WALLET_RISK * (cash + sum(open_.values())))
            if stake <= 0.01: continue
            cash -= stake; open_[pool] = stake; n += 1
        elif pool in open_:
            cash += open_.pop(pool) * mult
        eq = cash + sum(open_.values())
        peak = max(peak, eq); max_dd = max(max_dd, 1 - eq / peak if peak else 0)
    end = cash + sum(open_.values())
    return {"start": WALLET_START, "end": round(end, 2), "return_pct": round(100 * (end / WALLET_START - 1), 1),
            "max_drawdown_pct": round(100 * max_dd, 1), "trades": n, "stake_pct": int(WALLET_RISK * 100)}

def main():
    st = sim.load_state(); rng = random.Random(42)
    alltr = jl("trades.jsonl")
    trades = [t for t in alltr if t.get("event") == "exit"]
    unknown = {}
    for t in alltr:
        if t.get("event") == "entry" and t.get("holders") == "unknown": unknown[t["book"]] = unknown.get(t["book"], 0) + 1
    shadows = list(st["shadows"].values()) + jl("shadows_done.jsonl")
    samples = list(st["samples"].values()) + jl("samples_done.jsonl")
    elapsed_h = ((st["last_poll"] or 0) - (st["started"] or 0)) / 3600 if st["started"] else 0
    out = {"generated": sim.iso(), "started": sim.iso(st["started"]) if st["started"] else None,
           "hours_covered": round(elapsed_h, 2), "gap_minutes": round(sum(g["minutes"] for g in st["gaps"]), 1),
           "gaps": st["gaps"], "done": st["done"], "counts": st["counts"], "api_calls": st["calls"],
           "rpc_fail": st.get("rpc_fail", {}), "books": {}}
    for b, bk in st["books"].items():
        equity = bk["cash"] + sum(sim.sell_value(p["qty"], p["last_px"]) for p in bk["open"].values())
        bt = sorted([t for t in trades if t.get("book") == b], key=lambda t: t["pnl"])
        mine = [s for s in shadows if b in (s.get("books") or [])]
        out["books"][b] = {
            "pnl_usd": round(equity - C["account_usd"], 2), "pnl_pct": round(100 * (equity / C["account_usd"] - 1), 2),
            "open": len(bk["open"]), "counts": bk["counts"], "entries_holder_check_unknown": unknown.get(b, 0),
            "closed_trades": stats([t["pnl_pct"] for t in bt]),
            "rules_on_all_its_survivors": stats([s["rule_exit"]["pnl_pct"] for s in mine if "rule_exit" in s]),
            "random_hold_on_its_survivors": stats(random_hold(mine, "entry_px", "samples", rng)),
            "wallet_20": wallet_replay(alltr, b),
            "exit_reasons": {r: sum(t["reason"] == r for t in bt) for r in {t["reason"] for t in bt}},
            "best": bt[-3:][::-1], "worst": bt[:3]}
    out["all_launch_sample"] = {
        "launches_sampled": len(samples), "with_entry_price": sum(1 for s in samples if s.get("entry_px")),
        "random_exit_within_3h": stats(random_hold(samples, "entry_px", "path", rng)),
        "hold_1h": stats(hold_for(samples, 60)), "hold_3h": stats(hold_for(samples, 180))}
    with open(os.path.join(D, "summary.json"), "w") as fh: json.dump(out, fh, indent=2)
    L = ["# pump.fun paper sim summary (v2)", "",
         f"- Window: {out['started']}, {out['hours_covered']}h covered, gaps {out['gap_minutes']} min, finished: {out['done']}",
         f"- Launches seen {st['counts'].get('launches_seen', 0)}, evaluated {st['counts'].get('evaluated', 0)}, missed (too old when first seen) {st['counts'].get('missed_too_old', 0)}",
         f"- All-launch baseline (1 in {C['sample_one_in']} launches, bought at 10 min old): random exit {out['all_launch_sample']['random_exit_within_3h']}, hold 1h {out['all_launch_sample']['hold_1h']}, hold 3h {out['all_launch_sample']['hold_3h']}", ""]
    for b, r in out["books"].items():
        kills = {k[5:]: v for k, v in r["counts"].items() if k.startswith("kill:")}
        L += [f"## {b}", f"- Paper P&L ${r['pnl_usd']} ({r['pnl_pct']}%), survivors {r['counts'].get('survivor', 0)}, trades {r['counts'].get('trade', 0)} (holder check unavailable on {r['entries_holder_check_unknown']}), open {r['open']}",
              "- Kills: " + ", ".join(f"{k} {v}" for k, v in sorted(kills.items(), key=lambda x: -x[1])),
              f"- $20 wallet, {r['wallet_20']['stake_pct']}% of wallet per trade: ends ${r['wallet_20']['end']} ({r['wallet_20']['return_pct']}%), worst drawdown {r['wallet_20']['max_drawdown_pct']}%",
              f"- Closed trades {r['closed_trades']}", f"- Rules on every survivor {r['rules_on_all_its_survivors']}",
              f"- Random hold on its survivors {r['random_hold_on_its_survivors']}", f"- Exits {r['exit_reasons']}",
              "- Best: " + "; ".join(f"{t['name']} {t['pnl_pct']}% ({t['reason']})" for t in r["best"]),
              "- Worst: " + "; ".join(f"{t['name']} {t['pnl_pct']}% ({t['reason']})" for t in r["worst"]), ""]
    with open(os.path.join(D, "summary.md"), "w") as fh: fh.write("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__": main()
