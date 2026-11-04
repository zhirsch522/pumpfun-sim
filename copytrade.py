#!/usr/bin/env python3
"""Paper-only copy-trading sim. No wallet, no keys, no orders.

Watches the busiest new pump.fun coins, reads their public trades (GeckoTerminal),
and keeps a running profit-and-loss ledger per trader wallet. A wallet becomes a
"leader" once it has closed several coins at a profit (built live from the trades
we read; free data has no long wallet history). When a leader makes a first buy in
a coin, the "leaders" book paper-buys it at the price we can get when we see it
(so the real reaction delay is baked in) and sells when the leader sells, or on
the usual stop / trailing stop / max hold.

Baseline: the "random_wallet" book copies first buys of random wallets of the same
size, with the same rules. If leaders don't beat random wallets, there's no edge.

Usage: SIM_MODE=copy SIM_DATA_DIR=data_copy python3 copytrade.py run --minutes 330
"""
import argparse, gzip, hashlib, json, os, sys, statistics
from datetime import datetime

os.environ.setdefault("SIM_MODE", "copy")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim
from sim import CFG, GT, now, iso, log, bump, f, http_json, fetch_new, fetch_pools, new_pos, close, manage, spike_check, buy_px, path

CC = {
    "hot_min_age_min": 10, "hot_recheck_min": 10, "hot_watch_max_age_min": 60,
    "hot_min_vol_h1": 5000, "hot_min_trades_h1": 50, "hot_hours": 3, "max_hot": 30,
    "trades_calls_per_step": 6, "trades_min_usd": 20,
    "min_copy_usd": 50, "max_signal_age_s": 600,
    "leader_min_mints": 3, "leader_max_mints": 60, "leader_min_pnl_usd": 100.0,
    "leader_min_winrate": 0.6, "leader_min_hold_s": 60,
    "leader_exit_frac": 0.5, "random_one_in": 25,
    "wallet_ttl_h": 30, "max_wallets": 80000, "wallets_save_min": 60,
}
WALLETS = {}   # wallet -> {mint: [tok_bought, usd_in, tok_sold, usd_out, first_buy_ts, first_sell_ts, last_ts]}
_last_wsave = [0.0]

def ts_of(s):
    try: return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
    except Exception: return None

def load_wallets():
    try:
        with gzip.open(path("wallets.json.gz"), "rt") as fh: WALLETS.update(json.load(fh))
    except (FileNotFoundError, OSError, ValueError): pass

def save_wallets(force=False):
    if not force and now() - _last_wsave[0] < CC["wallets_save_min"] * 60: return
    t = now(); cut = t - CC["wallet_ttl_h"] * 3600
    for w in [w for w, m in WALLETS.items() if max((v[6] for v in m.values()), default=0) < cut]: del WALLETS[w]
    if len(WALLETS) > CC["max_wallets"]:
        keep = sorted(WALLETS, key=lambda w: (len(WALLETS[w]), max(v[6] for v in WALLETS[w].values())), reverse=True)[:CC["max_wallets"]]
        keep = set(keep)
        for w in [w for w in WALLETS if w not in keep]: del WALLETS[w]
    tmp = path("wallets.json.gz.tmp")
    with gzip.open(tmp, "wt") as fh: json.dump(WALLETS, fh, separators=(",", ":"))
    os.replace(tmp, path("wallets.json.gz")); _last_wsave[0] = t

def score(w):
    """Track record from coins this wallet has mostly sold (>=50% of tokens bought)."""
    pnl, wins, n, holds = 0.0, 0, 0, []
    for v in WALLETS.get(w, {}).values():
        bt, bu, st_, su, fb, fs, _ = v
        if bt <= 0 or st_ < 0.5 * bt: continue
        r = su - bu * min(1.0, st_ / bt)
        n += 1; pnl += r; wins += r > 0
        if fb and fs: holds.append(fs - fb)
    hold = statistics.median(holds) if holds else 0
    return {"closed": n, "pnl_usd": round(pnl, 2), "winrate": round(wins / n, 2) if n else 0, "median_hold_s": round(hold)}

def is_leader(sc):
    return (CC["leader_min_mints"] <= sc["closed"] <= CC["leader_max_mints"] and sc["pnl_usd"] >= CC["leader_min_pnl_usd"]
            and sc["winrate"] >= CC["leader_min_winrate"] and sc["median_hold_s"] >= CC["leader_min_hold_s"])

def poll_trades(st, pool, h, signals):
    d = http_json(f"{GT}/networks/solana/pools/{pool}/trades?trade_volume_in_usd_greater_than={CC['trades_min_usd']}", st=st)
    rows = (d or {}).get("data")
    h["polled"] = now()
    if rows is None: bump(st["counts"], "trades_fail"); return
    mint = h["mint"]; last_ts = h.get("last_ts", 0); last_tx = set(h.get("last_tx", []))
    new = []
    for r in reversed(rows):   # oldest first
        a = r.get("attributes", {}); t = ts_of(a.get("block_timestamp") or "")
        if t is None or t < last_ts or (t == last_ts and a.get("tx_hash") in last_tx): continue
        new.append((t, a))
    if not new: return
    top = max(t for t, _ in new)
    h["last_tx"] = [a.get("tx_hash") for t, a in new if t == top] + (h.get("last_tx", []) if top == last_ts else [])
    h["last_ts"] = top
    first_poll = last_ts == 0
    for t, a in new:
        w = a.get("tx_from_address"); usd = f(a.get("volume_in_usd"))
        if not w: continue
        if a.get("to_token_address") == mint: side, tok = "buy", f(a.get("to_token_amount"))
        elif a.get("from_token_address") == mint: side, tok = "sell", f(a.get("from_token_amount"))
        else: bump(st["counts"], "trade_unmatched"); continue
        L = WALLETS.setdefault(w, {}).setdefault(mint, [0.0, 0.0, 0.0, 0.0, None, None, 0])
        if side == "buy":
            if L[0] == 0 and usd >= CC["min_copy_usd"] and now() - t <= CC["max_signal_age_s"]:
                sc = score(w)
                book = "leaders" if is_leader(sc) else ("random_wallet" if int(hashlib.sha256((w + mint).encode()).hexdigest(), 16) % CC["random_one_in"] == 0 else None)
                if book:
                    bump(st["counts"], f"signal:{book}")
                    signals.append({"book": book, "pool": pool, "mint": mint, "wallet": w, "lead_usd": round(usd, 2),
                                    "lead_px": usd / tok if tok else None, "trade_ts": t, "score": sc, "first_poll": first_poll})
            L[0] += tok; L[1] += usd; L[4] = L[4] or t
        else:
            L[2] += tok; L[3] += usd; L[5] = L[5] or t
        L[6] = t
        bump(st["counts"], "trades_read")
        if side == "sell":   # does a position follow this wallet on this coin?
            for b, bk in st["books"].items():
                pos = bk["open"].get(pool)
                if pos and pos.get("lead") == w and L[2] >= CC["leader_exit_frac"] * L[0]: pos["lead_exit"] = True

def step(st):
    t = now()
    if st["last_poll"] and t - st["last_poll"] > 3 * CFG["poll_s"]:
        gap = {"from": iso(st["last_poll"]), "to": iso(t), "minutes": round((t - st["last_poll"]) / 60, 1)}
        st["gaps"].append(gap); log("events.jsonl", {"event": "gap", **gap})
    st["last_poll"] = t
    st.setdefault("hot", {}); st.setdefault("cwatch", {})
    # 1. scan new pump.fun pools
    for p in fetch_new(st):
        if not p["pool"] or p["pool"] in st["seen"] or not p["created"]: continue
        st["seen"][p["pool"]] = round(p["created"])
        if not sim.is_pump(p["dex"]): bump(st["counts"], "ignored_non_pump"); continue
        bump(st["counts"], "launches_seen")
        if (t - p["created"]) / 60 > CC["hot_watch_max_age_min"]: bump(st["counts"], "missed_too_old"); continue
        st["cwatch"][p["pool"]] = {"created": p["created"], "next": p["created"] + CC["hot_min_age_min"] * 60}
    # 2. trades: open positions first, then hot pools least recently polled
    held = {pool for bk in st["books"].values() for pool in bk["open"]}
    order = sorted(st["hot"], key=lambda k: (k not in held, st["hot"][k].get("polled", 0)))
    signals = []
    for pool in order[:CC["trades_calls_per_step"]]:
        poll_trades(st, pool, st["hot"][pool], signals)
    # 3. quotes: watchlist due, open positions, signal pools
    due = [k for k, c in st["cwatch"].items() if t >= c["next"]]
    quotes = fetch_pools(due + list(held) + [s["pool"] for s in signals], st)
    for k in due:
        c = st["cwatch"][k]; q = quotes.get(k)
        if q and q["vol_h1"] >= CC["hot_min_vol_h1"] and q["buys_h1"] + q["sells_h1"] >= CC["hot_min_trades_h1"] and q["mint"]:
            st["hot"][k] = {"mint": q["mint"], "name": q["name"], "until": t + CC["hot_hours"] * 3600}
            del st["cwatch"][k]; bump(st["counts"], "hot_added")
        elif (t - c["created"]) / 60 >= CC["hot_watch_max_age_min"]: del st["cwatch"][k]
        else: c["next"] = t + CC["hot_recheck_min"] * 60
    # 4. leader exits, then the usual exits
    for b, bk in st["books"].items():
        for pool in [k for k, p in bk["open"].items() if p.get("lead_exit")]:
            q = quotes.get(pool); pos = bk["open"][pool]
            if q and q["price"] > 0 and spike_check(pos, q["price"]) == "ok":
                close(st, bk["open"], pool, q["price"], "leader_exit", b)
        manage(st, bk["open"], b, quotes)
    # 5. entries
    for s in signals:
        bk = st["books"][s["book"]]; q = quotes.get(s["pool"])
        if not q or q["price"] <= 0: bump(bk["counts"], "skip:no_quote"); continue
        if s["pool"] in bk["open"]: bump(bk["counts"], "skip:already_in"); continue
        if len(bk["open"]) >= CFG["max_open"]: bump(bk["counts"], "skip:max_open"); continue
        if bk["cash"] < CFG["ticket_usd"]: bump(bk["counts"], "skip:no_cash"); continue
        pos = new_pos(q); pos.update({"lead": s["wallet"], "lead_exit": False})
        bk["open"][s["pool"]] = pos; bk["cash"] -= CFG["ticket_usd"]; bump(bk["counts"], "trade")
        lag = round(t - s["trade_ts"])
        log("trades.jsonl", {"event": "entry", "book": s["book"], **sim.market_rec(q), "lead_wallet": s["wallet"],
                             "lead_usd": s["lead_usd"], "lead_px": s["lead_px"], "lag_s": lag, "lead_score": s["score"],
                             "entry_px_with_slip": buy_px(q["price"]), "ticket": CFG["ticket_usd"]})
    # 6. housekeeping
    for k in [k for k, h in st["hot"].items() if h["until"] < t and k not in held]: del st["hot"][k]
    if len(st["hot"]) > CC["max_hot"]:   # keep the newest
        for k in sorted(st["hot"], key=lambda k: st["hot"][k]["until"])[:len(st["hot"]) - CC["max_hot"]]:
            if k not in held: del st["hot"][k]
    if len(st["seen"]) > 30000: st["seen"] = {k: v for k, v in st["seen"].items() if t - v < 7200}
    st["counts"]["wallets_tracked"] = len(WALLETS)
    save_wallets()

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("run"); r.add_argument("--minutes", type=float, default=330)
    a = ap.parse_args()
    if a.cmd != "run": ap.print_help(); return 0
    os.makedirs(sim.DATA_DIR, exist_ok=True)
    load_wallets()
    try: return sim.run(a.minutes, step_fn=step)
    finally:
        save_wallets(force=True)
        leaders = sum(1 for w in WALLETS if is_leader(score(w)))
        log("events.jsonl", {"event": "wallets_saved", "wallets": len(WALLETS), "leaders": leaders})
        sim.commit(f"wallets {iso()}")

if __name__ == "__main__": sys.exit(main())
