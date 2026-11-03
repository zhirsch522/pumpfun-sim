#!/usr/bin/env python3
"""Builds data/summary.json and data/summary.md from the sim's journal."""
import json, os, random, statistics, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim

D = sim.DATA_DIR
def jl(name):
    try:
        with open(os.path.join(D, name)) as fh: return [json.loads(l) for l in fh if l.strip()]
    except FileNotFoundError: return []

def main():
    st = sim.load_state(); C = sim.CFG
    trades = [t for t in jl("trades.jsonl") if t.get("event") == "exit"]
    equity = st["cash"] + sum(sim.sell_value(p["qty"], p["last_px"]) for p in st["open"].values())
    pnl = equity - C["account_usd"]
    # rules applied to every survivor (no max-open limit)
    sh = list(st["shadows"].values()) + jl("shadows_done.jsonl")
    rule_all = [s["rule_exit"]["pnl_pct"] for s in sh if "rule_exit" in s]
    # random-hold baseline: buy every survivor at the same price, exit at a random later sample
    rng = random.Random(42); rand = []
    for s in sh:
        samp = [px for t, px in s["samples"][1:]]
        if not samp: continue
        for _ in range(200):
            px = rng.choice(samp)
            q = C["ticket_usd"] * (1 - C["fee"]) / sim.buy_px(s["entry_px"])
            rand.append(100 * (sim.sell_value(q, px) - C["ticket_usd"]) / C["ticket_usd"])
    def stats(xs):
        if not xs: return None
        return {"n": len(xs), "avg_pct": round(statistics.mean(xs), 2), "median_pct": round(statistics.median(xs), 2),
                "win_rate": round(100 * sum(x > 0 for x in xs) / len(xs), 1)}
    elapsed_h = ((st["last_poll"] or 0) - (st["started"] or 0)) / 3600 if st["started"] else 0
    gap_min = sum(g["minutes"] for g in st["gaps"])
    by = sorted(trades, key=lambda t: t["pnl"])
    out = {
        "generated": sim.iso(), "started": sim.iso(st["started"]) if st["started"] else None,
        "hours_covered": round(elapsed_h, 2), "gap_minutes": round(gap_min, 1), "gaps": st["gaps"], "done": st["done"],
        "equity": round(equity, 2), "pnl_usd": round(pnl, 2), "pnl_pct": round(100 * pnl / C["account_usd"], 2),
        "open_positions": len(st["open"]), "counts": st["counts"], "api_calls": st["calls"],
        "taken_trades": stats([t["pnl_pct"] for t in trades]),
        "rules_on_all_survivors": stats(rule_all),
        "random_hold_baseline": stats(rand),
        "best": by[-3:][::-1], "worst": by[:3],
        "exit_reasons": {r: sum(t["reason"] == r for t in trades) for r in {t["reason"] for t in trades}},
    }
    with open(os.path.join(D, "summary.json"), "w") as fh: json.dump(out, fh, indent=2)
    c = st["counts"]; kills = {k[5:]: v for k, v in c.items() if k.startswith("kill:")}
    lines = [f"# pump.fun paper sim summary", "",
             f"- Window: {out['started']} for {out['hours_covered']}h, gaps {out['gap_minutes']} min, finished: {out['done']}",
             f"- Paper P&L: ${out['pnl_usd']} ({out['pnl_pct']}%) on ${C['account_usd']:.0f}, equity ${out['equity']}",
             f"- Launches seen: {c.get('launches_seen', 0)}, survivors: {c.get('survivor', 0)}, trades: {c.get('trade', 0)}, skipped max-open: {c.get('skip:max_open', 0)}",
             "- Killed by filter: " + ", ".join(f"{k} {v}" for k, v in sorted(kills.items(), key=lambda x: -x[1])),
             f"- Taken trades: {out['taken_trades']}",
             f"- Rules on every survivor: {out['rules_on_all_survivors']}",
             f"- Random-hold baseline on survivors: {out['random_hold_baseline']}",
             f"- Exit reasons: {out['exit_reasons']}", "", "## Best", *[f"- {t['name']}: {t['pnl_pct']}% ({t['reason']}, {t['hold_min']} min)" for t in out['best']],
             "", "## Worst", *[f"- {t['name']}: {t['pnl_pct']}% ({t['reason']}, {t['hold_min']} min)" for t in out['worst']]]
    with open(os.path.join(D, "summary.md"), "w") as fh: fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__": main()
