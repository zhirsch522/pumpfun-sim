#!/usr/bin/env python3
"""Paper-only pump.fun scanner + simulated trader, v2 (several filter sets side by side).

No wallet, no keys, no orders. Reads free public data (GeckoTerminal + public
Solana RPC), applies plain-code rules, and journals fake fills.
State lives in DATA_DIR so any run resumes where the last one stopped.
Token names/symbols are untrusted text: stored truncated, never acted on.

Books (each its own $1000 paper account, same fees, slippage and exits):
  strict  - original filters
  medium  - looser market filters
  curve   - market filters sized for bonding-curve coins
  rugonly - no market filters, only the chain (rug) checks
Baselines:
  shadows - every survivor of any book, rule exits + price samples for 6h
  sample  - 1 in N of ALL launches, price sampled every few minutes for 3h

Usage: python3 sim.py run --minutes 330
"""
import argparse, hashlib, json, os, subprocess, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

DATA_DIR = os.environ.get("SIM_DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
GT = "https://api.geckoterminal.com/api/v2"
RPCS = [u for u in os.environ.get("SIM_RPCS", "https://solana-rpc.publicnode.com,https://solana.drpc.org,https://api.mainnet-beta.solana.com").split(",") if u]
SYSTEM_PROGRAM = "11111111111111111111111111111111"

BOOKS = {
    "strict":  {"min_liq_usd": 5000, "min_mcap_usd": 8000, "max_mcap_usd": 500000, "min_vol_h1_usd": 10000,
                "min_trades_h1": 100, "min_buyers_h1": 40, "max_sell_buy_h1": 1.2, "max_sell_buy_m5": 1.5, "min_pc_m5": -30.0},
    "medium":  {"min_liq_usd": 3000, "min_mcap_usd": 5000, "max_mcap_usd": 500000, "min_vol_h1_usd": 5000,
                "min_trades_h1": 60, "min_buyers_h1": 25, "max_sell_buy_h1": 1.3, "max_sell_buy_m5": 1.7, "min_pc_m5": -40.0},
    "curve":   {"min_liq_usd": 1500, "min_mcap_usd": 3000, "max_mcap_usd": 500000, "min_vol_h1_usd": 2000,
                "min_trades_h1": 30, "min_buyers_h1": 15, "max_sell_buy_h1": 1.5, "max_sell_buy_m5": 2.0, "min_pc_m5": -50.0},
    "rugonly": None,
}

CFG = {
    "version": 2,
    "run_hours": 24,
    "account_usd": 1000.0,
    "ticket_usd": 20.0,
    "max_open": 3,
    "fee": 0.01,          # each way
    "slippage": 0.02,     # each way
    "eval_min_age_min": 10,
    "eval_max_age_min": 30,
    "max_top1_wallet_pct": 10.0,
    "max_top10_wallet_pct": 35.0,
    "chain_checks_per_step": 12,
    "chain_retry_steps": 2,
    "rpc_holders": False,   # free RPCs refuse getTokenLargestAccounts; use pool trades instead
    # exits (all books)
    "stop_pct": -35.0,
    "tp_mult": 2.0,
    "fade_after_min": 15,
    "fade_ratio": 0.25,
    "max_hold_h": 24,
    "no_price_polls": 3,
    "glitch_jump": 50.0,   # one-poll jump this big = dead/rugged pool with a garbage quote; valued at 0
    "suspect_jump": 10.0,  # one-poll jump this big is held as suspect; dead if the quote then freezes or collapses
    # survivor shadows
    "shadow_hours": 6,
    "shadow_sample_min": 2,
    "max_active_shadows": 300,
    # all-launch sample
    "sample_one_in": 5,
    "sample_hours": 3,
    "sample_every_min": 5,
    "max_active_samples": 1500,
    # loop
    "poll_s": 60,
    "max_pages": 4,
    "gt_min_gap_s": 2.2,
    "commit_every_min": 10,
}

def now(): return time.time()
def iso(t=None): return datetime.fromtimestamp(now() if t is None else t, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def f(x, d=0.0):
    try: return float(x) if x is not None else d
    except (TypeError, ValueError): return d
def clean(s, n=40):
    s = "" if s is None else str(s)
    return "".join(c for c in s if c.isprintable())[:n]

# ---------- io ----------
def path(name): return os.path.join(DATA_DIR, name)
def log(name, rec):
    rec = {"ts": iso(), **rec}
    with open(path(name), "a") as fh: fh.write(json.dumps(rec) + "\n")
def new_state():
    return {"version": 2, "started": None, "seen": {}, "watch": {}, "chainq": {}, "chain_cache": {},
            "books": {b: {"cash": CFG["account_usd"], "open": {}, "counts": {}} for b in BOOKS},
            "shadows": {}, "samples": {}, "counts": {}, "last_poll": None, "gaps": [],
            "calls": {"gt": 0, "rpc": 0, "err": 0}, "rpc_fail": {}, "done": False}
def load_state():
    try:
        with open(path("state.json")) as fh: st = json.load(fh)
        return st if st.get("version") == 2 else new_state()
    except FileNotFoundError:
        return new_state()
def save_state(st):
    tmp = path("state.json.tmp")
    with open(tmp, "w") as fh: json.dump(st, fh)
    os.replace(tmp, path("state.json"))
def bump(d, key, n=1): d[key] = d.get(key, 0) + n

# ---------- http ----------
_last_gt = [0.0]
def http_json(url, body=None, st=None, kind="gt", tries=2):
    for i in range(tries):
        if kind == "gt":
            wait = CFG["gt_min_gap_s"] - (now() - _last_gt[0])
            if wait > 0: time.sleep(wait)
            _last_gt[0] = now()
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                         headers={"Accept": "application/json", "Content-Type": "application/json",
                                                  "User-Agent": "paper-sim/2.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if st: st["calls"][kind] += 1
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if st: st["calls"]["err"] += 1
            if e.code == 429:
                log("events.jsonl", {"event": "rate_limited", "source": kind, "host": url.split("/")[2]})
                if kind == "rpc": return None
                time.sleep(10 * (i + 1)); continue
            if kind == "rpc":
                log("events.jsonl", {"event": "rpc_http_error", "host": url.split("/")[2], "code": e.code}); return None
            if e.code == 404: return None
            time.sleep(2)
        except Exception as e:
            if st: st["calls"]["err"] += 1
            if kind == "rpc":
                log("events.jsonl", {"event": "rpc_exception", "host": url.split("/")[2], "err": repr(e)[:120]}); return None
            time.sleep(2)
    return None

def rpc(method, params, st):
    """Try each free RPC once, healthiest first; no long sleeps so the main loop never stalls."""
    health = st.setdefault("rpc_ok", {})
    order = sorted(RPCS, key=lambda ep: -health.get(ep.split("/")[2] + ":" + method, 0))
    for ep in order:
        key = ep.split("/")[2] + ":" + method
        r = http_json(ep, {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, st, kind="rpc", tries=1)
        time.sleep(0.25)
        if r and "result" in r:
            health[key] = min(health.get(key, 0) + 1, 20); return r["result"]
        health[key] = health.get(key, 0) - 1
        bump(st["rpc_fail"], key)
        if r and "error" in r and st["rpc_fail"][key] <= 5:
            log("events.jsonl", {"event": "rpc_error", "host": ep.split("/")[2], "method": method, "error": str(r["error"])[:200]})
    return None

# ---------- data parsing ----------
def parse_pool(p):
    a = p.get("attributes", {}); rel = p.get("relationships", {})
    tx = a.get("transactions", {}) or {}; vol = a.get("volume_usd", {}) or {}; pc = a.get("price_change_percentage", {}) or {}
    h1 = tx.get("h1", {}) or {}; m5 = tx.get("m5", {}) or {}
    dex = ((rel.get("dex") or {}).get("data") or {}).get("id", "")
    base = ((rel.get("base_token") or {}).get("data") or {}).get("id", "")
    created = a.get("pool_created_at")
    try: ct = datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp() if created else None
    except Exception: ct = None
    return {
        "pool": a.get("address") or p.get("id", "").split("_", 1)[-1],
        "mint": base.split("_", 1)[-1] if base else None,
        "name": clean(a.get("name")), "dex": dex, "created": ct,
        "price": f(a.get("base_token_price_usd")),
        "mcap": f(a.get("market_cap_usd")) or f(a.get("fdv_usd")),
        "liq": f(a.get("reserve_in_usd")),
        "vol_m5": f(vol.get("m5")), "vol_h1": f(vol.get("h1")),
        "buys_h1": int(f(h1.get("buys"))), "sells_h1": int(f(h1.get("sells"))), "buyers_h1": int(f(h1.get("buyers"))),
        "buys_m5": int(f(m5.get("buys"))), "sells_m5": int(f(m5.get("sells"))),
        "pc_m5": f(pc.get("m5")),
    }

def is_pump(dex): return "pump" in (dex or "").lower()

def fetch_new(st):
    """Page through new pools until we reach ones we've already seen (max_pages)."""
    out = []
    for page in range(1, CFG["max_pages"] + 1):
        d = http_json(f"{GT}/networks/solana/new_pools?page={page}&include=base_token,dex", st=st)
        pools = [parse_pool(p) for p in (d or {}).get("data", [])]
        out += pools
        if not pools or any(p["pool"] in st["seen"] for p in pools): break
        if page == CFG["max_pages"]: bump(st["counts"], "scan_pages_maxed")
    return out

def fetch_pools(addrs, st):
    res = {}
    addrs = list(dict.fromkeys(a for a in addrs if a))
    for i in range(0, len(addrs), 30):
        chunk = addrs[i:i + 30]
        d = http_json(f"{GT}/networks/solana/pools/multi/{','.join(chunk)}?include=base_token,dex", st=st)
        for p in (d or {}).get("data", []):
            q = parse_pool(p); res[q["pool"]] = q
    return res

def best_pool_for_mint(mint, st):
    d = http_json(f"{GT}/networks/solana/tokens/{mint}/pools?page=1&include=base_token,dex", st=st)
    pools = [parse_pool(p) for p in (d or {}).get("data", [])]
    pools = [p for p in pools if p["price"] > 0 and p["mint"] == mint]
    return max(pools, key=lambda p: p["liq"]) if pools else None

# ---------- rules ----------
def free_kill(p, c):
    if c is None: return None if p["price"] > 0 else "no_price"
    if p["liq"] < c["min_liq_usd"]: return "low_liquidity"
    if p["mcap"] < c["min_mcap_usd"]: return "mcap_too_low"
    if p["mcap"] > c["max_mcap_usd"]: return "mcap_too_high"
    if p["vol_h1"] < c["min_vol_h1_usd"]: return "low_volume"
    if p["buys_h1"] + p["sells_h1"] < c["min_trades_h1"]: return "few_trades"
    if p["buyers_h1"] < c["min_buyers_h1"]: return "few_buyers"
    if p["sells_h1"] > c["max_sell_buy_h1"] * max(p["buys_h1"], 1): return "sell_heavy_h1"
    if p["sells_m5"] > c["max_sell_buy_m5"] * max(p["buys_m5"], 1): return "sell_heavy_m5"
    if p["pc_m5"] < c["min_pc_m5"]: return "dumping_m5"
    return None

def holders_from_trades(p, supply, st):
    """Fallback holder check: net tokens bought per wallet from the pool's recent trades
    (GeckoTerminal, up to 300). Pool/curve accounts never appear as traders, so they are
    excluded by construction. Returns (top1_pct, top10_pct, n_trades) or None."""
    d = http_json(f"{GT}/networks/solana/pools/{p['pool']}/trades", st=st)
    rows = (d or {}).get("data")
    if rows is None or supply <= 0: return None
    net = {}; matched = 0
    for r in rows:
        a = r.get("attributes", {}); w = a.get("tx_from_address")
        if not w: continue
        if a.get("to_token_address") == p["mint"]: net[w] = net.get(w, 0) + f(a.get("to_token_amount")); matched += 1
        elif a.get("from_token_address") == p["mint"]: net[w] = net.get(w, 0) - f(a.get("from_token_amount")); matched += 1
    if rows and not matched:
        if st["counts"].get("trades_unmatched", 0) < 5:
            a = rows[0].get("attributes", {})
            log("events.jsonl", {"event": "trades_unmatched", "pool": p["pool"], "mint": p["mint"],
                                 "keys": sorted(a.keys())[:40], "from_token": a.get("from_token_address"), "to_token": a.get("to_token_address")})
        bump(st["counts"], "trades_unmatched")
        return None
    bal = sorted((v for v in net.values() if v > 0), reverse=True)
    return 100 * (bal[0] if bal else 0) / supply, 100 * sum(bal[:10]) / supply, len(rows)

def chain_check(p, st):
    """Returns (kill_reason or None, info). None reason with info {} never happens; 'retry' means RPC failed."""
    acc = rpc("getAccountInfo", [p["mint"], {"encoding": "jsonParsed"}], st)
    info = ((((acc or {}).get("value") or {}).get("data") or {}).get("parsed") or {}).get("info") if acc else None
    if not info: return "retry", {}
    if info.get("mintAuthority"): return "mint_authority_set", {}
    if info.get("freezeAuthority"): return "freeze_authority_set", {}
    ok = {"authorities_ok": True}
    supply = f(info.get("supply")) / (10 ** int(info.get("decimals", 0)))
    ok["supply"] = supply
    largest = rpc("getTokenLargestAccounts", [p["mint"]], st) if CFG["rpc_holders"] else None
    holders = (largest or {}).get("value") or []
    if not holders or supply <= 0:
        h = holders_from_trades(p, supply, st)
        if h is None: return "retry", ok
        top1, top10, n = h
        info = {"top1_pct": round(top1, 2), "top10_pct": round(top10, 2), "holders_source": "trades", "trades_seen": n}
        if top1 > CFG["max_top1_wallet_pct"]: return "whale_wallet", info
        if top10 > CFG["max_top10_wallet_pct"]: return "concentrated_top10", info
        return None, info
    tas = [h["address"] for h in holders]
    ta_info = rpc("getMultipleAccounts", [tas, {"encoding": "jsonParsed"}], st)
    if not ta_info: return "retry", ok
    owners = []
    for h, a in zip(holders, ta_info.get("value") or []):
        own = ((((a or {}).get("data") or {}).get("parsed") or {}).get("info") or {}).get("owner")
        owners.append((own, f(h.get("uiAmount"))))
    uniq = list(dict.fromkeys(o for o, _ in owners if o))
    oi = rpc("getMultipleAccounts", [uniq, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 0}}], st) if uniq else None
    if uniq and not oi: return "retry", ok
    prog_owned = set()
    for o, a in zip(uniq, (oi or {}).get("value") or []):
        if o == p["pool"] or (a and a.get("owner") != SYSTEM_PROGRAM): prog_owned.add(o)
    real = sorted((amt for o, amt in owners if o and o not in prog_owned), reverse=True)
    top1 = 100 * (real[0] if real else 0) / supply
    top10 = 100 * sum(real[:10]) / supply
    info = {"top1_pct": round(top1, 2), "top10_pct": round(top10, 2), "excluded_program_accts": len(prog_owned)}
    if top1 > CFG["max_top1_wallet_pct"]: return "whale_wallet", info
    if top10 > CFG["max_top10_wallet_pct"]: return "concentrated_top10", info
    return None, info

# ---------- paper trading ----------
def buy_px(px): return px * (1 + CFG["slippage"])
def sell_value(qty, px): return qty * px * (1 - CFG["slippage"]) * (1 - CFG["fee"])

def new_pos(p, books=None):
    cost = CFG["ticket_usd"]
    return {"pool": p["pool"], "mint": p["mint"], "name": p["name"], "entry_t": now(), "entry_px": p["price"],
            "qty": cost * (1 - CFG["fee"]) / buy_px(p["price"]), "cost": cost, "proceeds": 0.0, "half_taken": False,
            "entry_vol_m5": p["vol_m5"], "miss": 0, "last_px": p["price"], "peak_px": p["price"],
            "samples": [[round(now()), p["price"]]], "last_sample": now(), **({"books": books} if books else {})}

def close(st, holder, key, px, reason, book, frac=1.0):
    """holder is a dict of positions (a book's open dict, or st['shadows'])."""
    pos = holder[key]
    q = pos["qty"] * frac
    val = sell_value(q, px)
    pos["qty"] -= q; pos["proceeds"] += val
    shadow = book == "shadow"
    if not shadow: st["books"][book]["cash"] += val
    fname = "shadow.jsonl" if shadow else "trades.jsonl"
    if frac < 1.0:
        log(fname, {"event": "partial_exit", "book": book, "pool": key, "name": pos["name"], "px": px, "reason": reason, "value": round(val, 4)})
        return
    pnl = pos["proceeds"] - pos["cost"]
    rec = {"event": "exit", "book": book, "pool": key, "mint": pos["mint"], "name": pos["name"], "reason": reason,
           "entry_t": iso(pos["entry_t"]), "hold_min": round((now() - pos["entry_t"]) / 60, 1),
           "entry_px": pos["entry_px"], "exit_px": px, "peak_px": pos["peak_px"],
           "cost": pos["cost"], "proceeds": round(pos["proceeds"], 4), "pnl": round(pnl, 4),
           "pnl_pct": round(100 * pnl / pos["cost"], 2)}
    log(fname, rec)
    if shadow: pos["rule_exit"] = rec  # keep sampling prices for the baseline
    else: del holder[key]

def spike_check(obj, px):
    """Rugged pools often report a garbage quote: a sudden huge jump that then freezes or drops to ~0.
    Returns 'ok' (use px), 'hold' (suspect, skip this quote) or 'dead' (value the position at 0)."""
    sus = obj.get("suspect")
    if sus:
        if px == sus["px"] or px < 0.01 * sus["prev"]:
            sus["n"] += 1
            return "dead" if sus["n"] >= 2 else "hold"
        obj.pop("suspect"); return "ok"
    last = obj.get("last_px")
    if last and px >= CFG["glitch_jump"] * last: return "dead"
    if last and px >= CFG["suspect_jump"] * last:
        obj["suspect"] = {"px": px, "prev": last, "n": 0}; return "hold"
    return "ok"

def manage(st, holder, book, quotes):
    shadow = book == "shadow"
    for key in list(holder.keys()):
        pos = holder[key]
        if shadow and (pos.get("ended") or now() - pos["entry_t"] > CFG["shadow_hours"] * 3600):
            pos["ended"] = True; continue
        q = quotes.get(pos["pool"])
        if not q or q["price"] <= 0:
            pos["miss"] += 1
            if pos["miss"] == 2 and pos.get("mint") and not pos.get("switched"):  # maybe graduated to a new pool
                pos["switched"] = True
                alt = best_pool_for_mint(pos["mint"], st)
                if alt and alt["pool"] != pos["pool"]:
                    log("events.jsonl", {"event": "pool_switch", "book": book, "from": pos["pool"], "to": alt["pool"]})
                    pos["pool"] = alt["pool"]; pos["miss"] = 0; continue
            if pos["miss"] >= CFG["no_price_polls"]:
                if "rule_exit" not in pos: close(st, holder, key, pos["last_px"], "no_price", book)
                if shadow: pos["ended"] = True
            continue
        verdict = spike_check(pos, q["price"])
        if verdict == "hold": pos["miss"] = 0; continue
        if verdict == "dead":
            bump(st["counts"], "dead_pool_glitch")
            if st["counts"]["dead_pool_glitch"] <= 30:
                log("events.jsonl", {"event": "price_glitch", "book": book, "pool": pos["pool"], "last_px": pos["last_px"],
                                     "px": q["price"], "liq": q["liq"], "mcap": q["mcap"], "vol_m5": q["vol_m5"]})
            if shadow: pos["samples"].append([round(now()), 0.0]); pos["ended"] = True
            if "rule_exit" not in pos: close(st, holder, key, 0.0, "dead_pool", book)
            continue
        pos["miss"] = 0; px = q["price"]; pos["last_px"] = px; pos["peak_px"] = max(pos["peak_px"], px)
        if shadow and now() - pos["last_sample"] >= CFG["shadow_sample_min"] * 60:
            pos["samples"].append([round(now()), px]); pos["last_sample"] = now()
        if "rule_exit" in pos: continue
        held_min = (now() - pos["entry_t"]) / 60
        if 100 * (px / pos["entry_px"] - 1) <= CFG["stop_pct"]: close(st, holder, key, px, "stop_loss", book); continue
        if not pos["half_taken"] and px >= CFG["tp_mult"] * pos["entry_px"]:
            close(st, holder, key, px, "take_half_2x", book, frac=0.5); pos["half_taken"] = True
        if held_min >= CFG["fade_after_min"] and pos["entry_vol_m5"] > 0 and q["vol_m5"] < CFG["fade_ratio"] * pos["entry_vol_m5"]:
            close(st, holder, key, px, "volume_fade", book); continue
        if held_min >= CFG["max_hold_h"] * 60: close(st, holder, key, px, "max_hold", book); continue

def sampled(pool):
    return int(hashlib.sha256(pool.encode()).hexdigest(), 16) % CFG["sample_one_in"] == 0

def market_rec(p):
    return {"pool": p["pool"], "mint": p["mint"], "name": p["name"], "dex": p["dex"],
            "age_min": round((now() - p["created"]) / 60, 1), "mcap": round(p["mcap"]), "liq": round(p["liq"]),
            "vol_h1": round(p["vol_h1"]), "trades_h1": p["buys_h1"] + p["sells_h1"], "buyers_h1": p["buyers_h1"],
            "price": p["price"]}

def free_stage(st, p):
    """Market filters for every book. Queues a chain check when any book still wants the coin."""
    verdict = {b: free_kill(p, c) for b, c in BOOKS.items()}
    rec = {**market_rec(p), "market": verdict}
    for b, r in verdict.items():
        if r: bump(st["books"][b]["counts"], "kill:" + r)
    market_pass = [b for b, r in verdict.items() if not r and BOOKS[b] is not None]
    rug_queued = sum(1 for it in st["chainq"].values() if "rugonly" in it["want"])
    rug_wants = verdict["rugonly"] is None and len(st["books"]["rugonly"]["open"]) + rug_queued < CFG["max_open"]
    if verdict["rugonly"] is None and not rug_wants: bump(st["books"]["rugonly"]["counts"], "not_checked_book_full")
    want = market_pass + (["rugonly"] if rug_wants else [])
    log("decisions.jsonl", {**rec, "stage": "market", "passed": want})
    if want: st["chainq"][p["pool"]] = {"p": p, "want": want, "tries": 0}

def chain_stage(st):
    done = 0
    for pool in list(st["chainq"].keys()):
        if done >= CFG["chain_checks_per_step"]: bump(st["counts"], "chain_deferred"); break
        item = st["chainq"][pool]; p = item["p"]
        if now() - p["created"] > (CFG["eval_max_age_min"] + 15) * 60:
            del st["chainq"][pool]
            for b in item["want"]: bump(st["books"][b]["counts"], "kill:chain_backlog")
            continue
        cached = st["chain_cache"].get(p["mint"])
        if cached: reason, info = cached
        else:
            reason, info = chain_check(p, st); done += 1
        if reason == "retry":
            item["tries"] += 1
            if item["tries"] <= CFG["chain_retry_steps"]: continue
            # Authorities are read first; if even those failed we can't vouch for the coin.
            if not info.get("authorities_ok"):
                reason = "chain_unreadable"
            else:
                reason, info = None, {**info, "holders": "unknown"}
                bump(st["counts"], "holders_unknown_pass")
        st["chain_cache"][p["mint"]] = [reason, info]
        del st["chainq"][pool]
        rec = {**market_rec(p), **info, "stage": "chain", "books": item["want"]}
        if reason:
            for b in item["want"]: bump(st["books"][b]["counts"], "kill:" + reason)
            log("decisions.jsonl", {**rec, "decision": "skip", "reason": reason}); continue
        # survivor: track as shadow once, then try each book
        if not st["shadows"].get(pool):
            if sum(1 for v in st["shadows"].values() if not v.get("ended")) < CFG["max_active_shadows"]:
                st["shadows"][pool] = new_pos(p, books=item["want"])
            else: bump(st["counts"], "shadow_cap")
        taken = []
        for b in item["want"]:
            bk = st["books"][b]; bump(bk["counts"], "survivor")
            if len(bk["open"]) >= CFG["max_open"]: bump(bk["counts"], "skip:max_open"); continue
            if bk["cash"] < CFG["ticket_usd"]: bump(bk["counts"], "skip:no_cash"); continue
            bk["open"][pool] = new_pos(p); bk["cash"] -= CFG["ticket_usd"]; bump(bk["counts"], "trade"); taken.append(b)
            log("trades.jsonl", {"event": "entry", "book": b, **market_rec(p), **info,
                                 "entry_px_with_slip": buy_px(p["price"]), "ticket": CFG["ticket_usd"]})
        log("decisions.jsonl", {**rec, "decision": "survivor", "bought_in": taken})

def sample_tick(st, due, quotes):
    """All-launch baseline: price path for a 1-in-N sample of every launch."""
    t = now()
    for pool in due:
        s = st["samples"].get(pool)
        if s is None: continue
        q = quotes.get(pool)
        v = spike_check(s, q["price"]) if (q and q["price"] > 0 and s.get("entry_px") and not s.get("dead")) else "ok"
        if s.get("dead") or v == "hold": pass
        elif v == "dead":
            s["path"].append([round(t), 0.0]); s["dead"] = True; s["created"] = 0  # dead pool: record 0 and archive
        elif q and q["price"] > 0:
            if s["entry_px"] is None:
                s["entry_px"] = q["price"]; s["entry_t"] = t; s["entry_liq"] = q["liq"]
            s["path"].append([round(t), q["price"]]); s["last_px"] = q["price"]
        elif s["entry_px"] is not None:
            s["misses"] = s.get("misses", 0) + 1
        s["next"] = t + CFG["sample_every_min"] * 60
        if t - s["created"] > CFG["sample_hours"] * 3600 + CFG["eval_min_age_min"] * 60:
            with open(path("samples_done.jsonl"), "a") as fh: fh.write(json.dumps({"pool": pool, **s}) + "\n")
            del st["samples"][pool]

def archive_shadows(st):
    for k in [k for k, v in st["shadows"].items() if v.get("ended")]:
        with open(path("shadows_done.jsonl"), "a") as fh: fh.write(json.dumps({"pool_key": k, **st["shadows"][k]}) + "\n")
        del st["shadows"][k]

def run_hours():
    """Run length in hours; a number in data/run_hours.txt overrides the default (git pull'd each commit)."""
    try:
        with open(path("run_hours.txt")) as fh: return max(1.0, min(120.0, float(fh.read().strip())))
    except (FileNotFoundError, ValueError): return CFG["run_hours"]

def commit(msg):
    if not os.environ.get("SIM_GIT_COMMIT"): return
    try:
        subprocess.run(["git", "add", "-A", DATA_DIR], check=False, timeout=60)
        subprocess.run(["git", "commit", "-q", "-m", msg], check=False, timeout=60)
        for _ in range(3):
            if subprocess.run(["git", "push", "-q"], timeout=120).returncode == 0: break
            subprocess.run(["git", "pull", "-q", "--rebase"], timeout=120)
    except Exception as e:
        print("commit failed", e, file=sys.stderr)

def step(st):
    t = now()
    if st["last_poll"] and t - st["last_poll"] > 3 * CFG["poll_s"]:
        gap = {"from": iso(st["last_poll"]), "to": iso(t), "minutes": round((t - st["last_poll"]) / 60, 1)}
        st["gaps"].append(gap); log("events.jsonl", {"event": "gap", **gap})
    st["last_poll"] = t
    # 1. scanner
    for p in fetch_new(st):
        if not p["pool"] or p["pool"] in st["seen"] or not p["created"]: continue
        st["seen"][p["pool"]] = round(p["created"])
        if not is_pump(p["dex"]): bump(st["counts"], "ignored_non_pump"); continue
        bump(st["counts"], "launches_seen")
        age = (t - p["created"]) / 60
        if age > CFG["eval_max_age_min"]:
            bump(st["counts"], "missed_too_old"); continue
        st["watch"][p["pool"]] = round(p["created"])
        if sampled(p["pool"]) and len(st["samples"]) < CFG["max_active_samples"]:
            st["samples"][p["pool"]] = {"created": p["created"], "mint": p["mint"], "entry_px": None, "path": [],
                                        "next": p["created"] + CFG["eval_min_age_min"] * 60, "last_px": None}
            bump(st["counts"], "sampled")
    # 2. quotes
    due = [k for k, c in st["watch"].items() if t - c >= CFG["eval_min_age_min"] * 60]
    live = [v["pool"] for bk in st["books"].values() for v in bk["open"].values()]
    live += [v["pool"] for v in st["shadows"].values() if not v.get("ended")]
    samp_due = [k for k, s in st["samples"].items() if t >= s["next"]]
    quotes = fetch_pools(due + live + samp_due, st)
    for k in due:
        del st["watch"][k]
        q = quotes.get(k)
        if not q or not q["created"]:
            bump(st["counts"], "no_data"); continue
        bump(st["counts"], "evaluated")
        free_stage(st, q)
    chain_stage(st)
    # 3. exits and baselines
    for b, bk in st["books"].items(): manage(st, bk["open"], b, quotes)
    manage(st, st["shadows"], "shadow", quotes)
    sample_tick(st, samp_due, quotes)
    archive_shadows(st)
    if len(st["seen"]) > 30000:
        st["seen"] = {k: v for k, v in st["seen"].items() if t - v < 7200}
    if len(st["chain_cache"]) > 5000: st["chain_cache"] = {}

def run(minutes):
    os.makedirs(DATA_DIR, exist_ok=True)
    st = load_state()
    if st["started"] is None:
        st["started"] = now(); log("events.jsonl", {"event": "start", "cfg": CFG, "books": BOOKS, "rpcs": RPCS})
    if st.get("done"):
        print("run already finished"); return 0
    session_end = now() + minutes * 60
    end_run = st["started"] + run_hours() * 3600
    stop_at = min(session_end, end_run)
    log("events.jsonl", {"event": "session_start", "until": iso(stop_at), "run_hours": run_hours()})
    last_commit = now()
    while now() < stop_at:
        t0 = now()
        end_run = st["started"] + run_hours() * 3600   # data/run_hours.txt can extend a live run
        stop_at = min(session_end, end_run)
        try: step(st)
        except Exception as e: log("events.jsonl", {"event": "error", "err": repr(e)[:300]})
        save_state(st)
        if now() - last_commit > CFG["commit_every_min"] * 60:
            commit(f"sim data {iso()}"); last_commit = now()
        time.sleep(max(1, CFG["poll_s"] - (now() - t0)))
    if now() >= end_run:
        for b, bk in st["books"].items():
            for k in list(bk["open"]): close(st, bk["open"], k, bk["open"][k]["last_px"], "sim_end", b)
        for k, v in st["shadows"].items():
            if "rule_exit" not in v: close(st, st["shadows"], k, v["last_px"], "sim_end", "shadow")
            v["ended"] = True
        archive_shadows(st)
        for pool, s in list(st["samples"].items()):
            with open(path("samples_done.jsonl"), "a") as fh: fh.write(json.dumps({"pool": pool, **s, "cut_at_end": True}) + "\n")
        st["samples"] = {}
        st["done"] = True; log("events.jsonl", {"event": "finished"})
    save_state(st)
    log("events.jsonl", {"event": "session_end"})
    commit(f"sim data {iso()}")
    return 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("run"); r.add_argument("--minutes", type=float, default=330)
    a = ap.parse_args()
    if a.cmd == "run": sys.exit(run(a.minutes))
    ap.print_help()
