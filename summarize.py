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
        e = r.get(key_entry); path = [px for _, px in clean_path(r.get(key_path) or [])[1:] if px is not None]
        if not e or not path: continue
        for _ in range(draws): out.append(ret_pct(e, rng.choice(path)))
    return out

def hold_for(rows, minutes):
    out = []
    for r in rows:
        e = r.get("entry_px"); path = clean_path(r.get("path") or [])
        if not e or len(path) < 2: continue
        t0 = path[0][0]; later = [px for t, px in path if t - t0 >= minutes * 60 and px is not None]
        exit_px = later[0] if later else path[-1][1]
        if exit_px is not None: out.append(ret_pct(e, exit_px))
    return out

G = C.get("glitch_jump", 50.0)

J = C.get("suspect_jump", 10.0)

def spike_at(path):
    """Index of a garbage post-rug quote in a price path (same rule as the live guard), else None:
    a one-step jump of G x, or of J x that then freezes or collapses below 1% of the pre-jump price."""
    pxs = [px for _, px in path]
    for i in range(1, len(pxs)):
        prev, px = pxs[i - 1], pxs[i]
        if not prev or not px: continue
        if px >= G * prev: return i
        if px >= J * prev:
            nxt = [x for x in pxs[i + 1:i + 3] if x is not None]
            if len(nxt) == 2 and all(x == px or x < 0.01 * prev for x in nxt): return i
    return None

def clean_path(path):
    i = spike_at(path)
    return path if i is None else [list(p) for p in path[:i]] + [[path[i][0], 0.0]]

def correct_exits(rows):
    """Positions that saw a garbage post-rug price (peak or exit >= G x entry; quote then freezes or drops to ~0) are re-valued as a dead pool:
    keep only partial-exit proceeds taken at sane prices, the rest is worth 0. Returns corrected exit rows."""
    partials = {}
    for r in rows:
        if r.get("event") == "partial_exit": partials.setdefault((r["book"], r["pool"]), []).append(r)
    out = []
    for r in rows:
        if r.get("event") != "exit": continue
        r = dict(r)
        top = max(r.get("exit_px") or 0, r.get("peak_px") or 0)
        if r.get("entry_px") and top >= G * r["entry_px"]:
            keep = sum(p["value"] for p in partials.get((r["book"], r["pool"]), [])
                       if r["entry_t"] <= p["ts"] <= r["ts"] and p["px"] < G * r["entry_px"])
            r.update({"glitch_corrected": True, "orig_pnl_pct": r["pnl_pct"], "reason": "dead_pool",
                      "proceeds": round(keep, 4), "pnl": round(keep - r["cost"], 4),
                      "pnl_pct": round(100 * (keep - r["cost"]) / r["cost"], 2)})
        out.append(r)
    return out

WALLET_START = 20.0
WALLET_RISK = 0.25   # each paper trade stakes 25% of the wallet's current value (max 3 open = up to 75% in)

def wallet_replay(alltr, book, exits):
    """Replays one book's logged trades as a $20 wallet that sizes each trade at 25% of its value.
    Each trade keeps its logged return (fees and slippage included); open stakes are marked at cost."""
    events = []
    for t in alltr:
        if t.get("book") != book: continue
        if t.get("event") == "entry": events.append((t["ts"], 0, t["pool"], None))
    for t in exits:
        if t.get("book") == book: events.append((t["ts"], 1, t["pool"], t["proceeds"] / t["cost"] if t["cost"] else 0))
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
    trades = correct_exits(alltr)
    n_glitch = sum(1 for t in trades if t.get("glitch_corrected"))
    shadow_rows = correct_exits(jl("shadow.jsonl"))
    shadow_partials = {}
    for r in jl("shadow.jsonl"):
        if r.get("event") == "partial_exit": shadow_partials.setdefault(r["pool"], []).append(r)
    shadow_fix = {(r["pool"], r["entry_t"]): r for r in shadow_rows if r.get("glitch_corrected")}
    unknown = {}
    for t in alltr:
        if t.get("event") == "entry" and t.get("holders") == "unknown": unknown[t["book"]] = unknown.get(t["book"], 0) + 1
    shadows = list(st["shadows"].values()) + jl("shadows_done.jsonl")
    for sh in shadows:
        re_ = sh.get("rule_exit")
        if re_ and (re_["pool"], re_["entry_t"]) in shadow_fix: sh["rule_exit"] = re_ = shadow_fix[(re_["pool"], re_["entry_t"])]
        i = spike_at(sh.get("samples") or [])
        if re_ and not re_.get("glitch_corrected") and i is not None:
            spike = sh["samples"][i][1]
            if (re_.get("peak_px") or 0) >= 0.9 * spike:  # the rule exit traded on the garbage quote
                keep = sum(p["value"] for p in shadow_partials.get(re_["pool"], [])
                           if re_["entry_t"] <= p["ts"] <= re_.get("ts", "9999") and p["px"] < 0.9 * spike)
                sh["rule_exit"] = {**re_, "glitch_corrected": True, "reason": "dead_pool", "pnl_pct": round(100 * (keep - re_["cost"]) / re_["cost"], 2)}
    samples = list(st["samples"].values()) + jl("samples_done.jsonl")
    elapsed_h = ((st["last_poll"] or 0) - (st["started"] or 0)) / 3600 if st["started"] else 0
    out = {"generated": sim.iso(), "started": sim.iso(st["started"]) if st["started"] else None,
           "hours_covered": round(elapsed_h, 2), "gap_minutes": round(sum(g["minutes"] for g in st["gaps"]), 1),
           "gaps": st["gaps"], "done": st["done"], "counts": st["counts"], "api_calls": st["calls"],
           "rpc_fail": st.get("rpc_fail", {}), "glitch_exits_corrected": n_glitch, "books": {}}
    for b, bk in st["books"].items():
        bt = sorted([t for t in trades if t.get("book") == b], key=lambda t: t["pnl"])
        open_val = sum(p["proceeds"] - p["cost"] + (0 if p["last_px"] >= G * p["entry_px"] else sim.sell_value(p["qty"], p["last_px"]))
                       for p in bk["open"].values())
        equity = C["account_usd"] + sum(t["pnl"] for t in bt) + open_val  # rebuilt from the journal, not state cash (glitch-proof)
        mine = [s for s in shadows if b in (s.get("books") or [])]
        out["books"][b] = {
            "pnl_usd": round(equity - C["account_usd"], 2), "pnl_pct": round(100 * (equity / C["account_usd"] - 1), 2),
            "open": len(bk["open"]), "counts": bk["counts"], "entries_holder_check_unknown": unknown.get(b, 0),
            "closed_trades": stats([t["pnl_pct"] for t in bt]),
            "rules_on_all_its_survivors": stats([s["rule_exit"]["pnl_pct"] for s in mine if "rule_exit" in s]),
            "random_hold_on_its_survivors": stats(random_hold(mine, "entry_px", "samples", rng)),
            "wallet_20": wallet_replay(alltr, b, trades), "dead_pool_exits": sum(t["reason"] == "dead_pool" for t in bt),
            "exit_reasons": {r: sum(t["reason"] == r for t in bt) for r in {t["reason"] for t in bt}},
            "best": bt[-3:][::-1], "worst": bt[:3]}
    out["all_launch_sample"] = {
        "launches_sampled": len(samples), "with_entry_price": sum(1 for s in samples if s.get("entry_px")),
        "random_exit_within_3h": stats(random_hold(samples, "entry_px", "path", rng)),
        "hold_1h": stats(hold_for(samples, 60)), "hold_3h": stats(hold_for(samples, 180))}
    with open(os.path.join(D, "summary.json"), "w") as fh: json.dump(out, fh, indent=2)
    L = ["# pump.fun paper sim summary (v2)", "",
         f"- Window: {out['started']}, {out['hours_covered']}h covered, gaps {out['gap_minutes']} min, finished: {out['done']}",
         f"- Dead/rugged pools with garbage post-rug prices: {n_glitch} logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of {G:g}x, or {J:g}x that then freezes or collapses",
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
