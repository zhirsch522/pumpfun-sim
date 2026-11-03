#!/usr/bin/env python3
"""Paper-only pump.fun scanner + simulated trader.

No wallet, no keys, no orders. Reads free public data (GeckoTerminal + public
Solana RPC), applies plain-code rules, and journals fake fills.
State lives in DATA_DIR so any run resumes where the last one stopped.
Token names/symbols are untrusted text: stored truncated, never acted on.

Usage: python3 sim.py run --minutes 340
"""
import argparse, json, os, random, subprocess, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

DATA_DIR = os.environ.get("SIM_DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
GT = "https://api.geckoterminal.com/api/v2"
RPC = os.environ.get("SIM_RPC", "https://api.mainnet-beta.solana.com")
SYSTEM_PROGRAM = "11111111111111111111111111111111"

CFG = {
    "run_hours": 24,
    "account_usd": 1000.0,
    "ticket_usd": 20.0,
    "max_open": 3,
    "fee": 0.01,          # each way
    "slippage": 0.02,     # each way
    # when to judge a launch
    "eval_min_age_min": 10,
    "eval_max_age_min": 30,   # first seen older than this = missed, skipped
    # free kill rules (all from GeckoTerminal pool stats)
    "min_liq_usd": 5000,
    "min_mcap_usd": 8000,
    "max_mcap_usd": 500000,
    "min_vol_h1_usd": 10000,
    "min_trades_h1": 100,
    "min_buyers_h1": 40,
    "max_sell_buy_h1": 1.2,
    "max_sell_buy_m5": 1.5,
    "min_pc_m5": -30.0,
    # chain kill rules
    "max_top1_wallet_pct": 10.0,
    "max_top10_wallet_pct": 35.0,
    # exits
    "stop_pct": -35.0,
    "tp_mult": 2.0,
    "fade_after_min": 15,
    "fade_ratio": 0.25,       # m5 volume below 25% of entry m5 volume
    "max_hold_h": 24,
    "no_price_polls": 3,
    # shadow tracking of every survivor (for baseline)
    "shadow_hours": 6,
    "shadow_sample_min": 2,
    "max_active_shadows": 150,
    # loop
    "poll_s": 60,
    "pages": 2,
    "commit_every_min": 10,
}

def now(): return time.time()
def iso(t=None): return datetime.fromtimestamp(t or now(), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
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
def load_state():
    try:
        with open(path("state.json")) as fh: return json.load(fh)
    except FileNotFoundError:
        return {"started": None, "cash": CFG["account_usd"], "seen": {}, "watch": {}, "open": {},
                "shadows": {}, "counts": {}, "last_poll": None, "gaps": [], "calls": {"gt": 0, "rpc": 0, "err": 0},
                "done": False}
def save_state(st):
    tmp = path("state.json.tmp")
    with open(tmp, "w") as fh: json.dump(st, fh)
    os.replace(tmp, path("state.json"))
def bump(st, key): st["counts"][key] = st["counts"].get(key, 0) + 1

# ---------- http ----------
_last_gt = [0.0]
def http_json(url, body=None, st=None, kind="gt", tries=3):
    for i in range(tries):
        if kind == "gt":  # free tier ~30/min: keep >= 2.2s apart
            wait = 2.2 - (now() - _last_gt[0])
            if wait > 0: time.sleep(wait)
            _last_gt[0] = now()
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                         headers={"Accept": "application/json", "Content-Type": "application/json",
                                                  "User-Agent": "paper-sim/1.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if st: st["calls"][kind] += 1
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if st: st["calls"]["err"] += 1
            if e.code == 429:
                log("events.jsonl", {"event": "rate_limited", "source": kind, "url": url[:120]})
                time.sleep(15 * (i + 1)); continue
            if e.code == 404: return None
            time.sleep(3 * (i + 1))
        except Exception as e:
            if st: st["calls"]["err"] += 1
            time.sleep(3 * (i + 1))
    return None

def rpc(method, params, st):
    r = http_json(RPC, {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, st, kind="rpc")
    time.sleep(0.4)
    return (r or {}).get("result")

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
    out = []
    for page in range(1, CFG["pages"] + 1):
        d = http_json(f"{GT}/networks/solana/new_pools?page={page}&include=base_token,dex", st=st)
        if not d: continue
        out += [parse_pool(p) for p in d.get("data", [])]
    return out

def fetch_pools(addrs, st):
    res = {}
    addrs = list(dict.fromkeys(addrs))
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
def free_kill(p):
    c = CFG
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

def chain_check(p, st):
    """Returns (kill_reason or None, info). Excludes program-owned holders (curve/pool vaults)."""
    acc = rpc("getAccountInfo", [p["mint"], {"encoding": "jsonParsed"}], st)
    info = (((acc or {}).get("value") or {}).get("data") or {}).get("parsed", {}).get("info") if acc else None
    if not info: return "chain_unreadable", {}
    if info.get("mintAuthority"): return "mint_authority_set", {}
    if info.get("freezeAuthority"): return "freeze_authority_set", {}
    supply = f(info.get("supply")) / (10 ** int(info.get("decimals", 0)))
    largest = rpc("getTokenLargestAccounts", [p["mint"]], st)
    holders = (largest or {}).get("value") or []
    if not holders or supply <= 0: return "holders_unreadable", {}
    tas = [h["address"] for h in holders]
    ta_info = rpc("getMultipleAccounts", [tas, {"encoding": "jsonParsed"}], st)
    owners = []
    for h, a in zip(holders, (ta_info or {}).get("value") or []):
        own = ((((a or {}).get("data") or {}).get("parsed") or {}).get("info") or {}).get("owner")
        owners.append((own, f(h.get("uiAmount"))))
    uniq = list(dict.fromkeys(o for o, _ in owners if o))
    oi = rpc("getMultipleAccounts", [uniq, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 0}}], st) if uniq else None
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

def open_position(st, p, book):
    cost = CFG["ticket_usd"]
    qty = cost * (1 - CFG["fee"]) / buy_px(p["price"])
    pos = {"pool": p["pool"], "mint": p["mint"], "name": p["name"], "entry_t": now(), "entry_px": p["price"],
           "qty": qty, "cost": cost, "proceeds": 0.0, "half_taken": False, "entry_vol_m5": p["vol_m5"],
           "miss": 0, "last_px": p["price"], "peak_px": p["price"], "samples": [[round(now()), p["price"]]],
           "last_sample": now()}
    if book == "open": st["cash"] -= cost
    st[book][p["pool"]] = pos
    return pos

def close(st, book, key, px, reason, frac=1.0):
    pos = st[book][key]
    q = pos["qty"] * frac
    val = sell_value(q, px)
    pos["qty"] -= q; pos["proceeds"] += val
    if book == "open": st["cash"] += val
    if frac < 1.0:
        log("trades.jsonl" if book == "open" else "shadow.jsonl",
            {"event": "partial_exit", "pool": key, "name": pos["name"], "px": px, "reason": reason, "value": round(val, 4)})
        return
    pnl = pos["proceeds"] - pos["cost"]
    rec = {"event": "exit", "pool": key, "mint": pos["mint"], "name": pos["name"], "reason": reason,
           "entry_t": iso(pos["entry_t"]), "hold_min": round((now() - pos["entry_t"]) / 60, 1),
           "entry_px": pos["entry_px"], "exit_px": px, "peak_px": pos["peak_px"],
           "cost": pos["cost"], "proceeds": round(pos["proceeds"], 4), "pnl": round(pnl, 4),
           "pnl_pct": round(100 * pnl / pos["cost"], 2)}
    if book == "open":
        log("trades.jsonl", rec); del st[book][key]
    else:
        pos["rule_exit"] = rec  # shadow keeps sampling prices for the baseline
        log("shadow.jsonl", rec)

def manage(st, book, quotes):
    for key in list(st[book].keys()):
        pos = st[book][key]
        if book == "shadows":
            if now() - pos["entry_t"] > CFG["shadow_hours"] * 3600 or pos.get("ended"): pos["ended"] = True; continue
        q = quotes.get(pos["pool"])
        if not q or q["price"] <= 0:
            pos["miss"] += 1
            if pos["miss"] == 2 and pos.get("mint"):  # maybe graduated to a new pool
                alt = best_pool_for_mint(pos["mint"], st)
                if alt and alt["pool"] != pos["pool"]:
                    log("events.jsonl", {"event": "pool_switch", "book": book, "from": pos["pool"], "to": alt["pool"]})
                    pos["pool"] = alt["pool"]; pos["miss"] = 0; continue
            if pos["miss"] >= CFG["no_price_polls"]:
                if book == "shadows":
                    if "rule_exit" not in pos: close(st, book, key, pos["last_px"], "no_price")
                    pos["ended"] = True
                else:
                    close(st, book, key, pos["last_px"], "no_price")
            continue
        pos["miss"] = 0; px = q["price"]; pos["last_px"] = px; pos["peak_px"] = max(pos["peak_px"], px)
        if now() - pos["last_sample"] >= CFG["shadow_sample_min"] * 60:
            pos["samples"].append([round(now()), px]); pos["last_sample"] = now()
        if "rule_exit" in pos: continue
        held_min = (now() - pos["entry_t"]) / 60
        chg = 100 * (px / pos["entry_px"] - 1)
        if chg <= CFG["stop_pct"]: close(st, book, key, px, "stop_loss"); continue
        if not pos["half_taken"] and px >= CFG["tp_mult"] * pos["entry_px"]:
            close(st, book, key, px, "take_half_2x", frac=0.5); pos["half_taken"] = True
        if held_min >= CFG["fade_after_min"] and pos["entry_vol_m5"] > 0 and q["vol_m5"] < CFG["fade_ratio"] * pos["entry_vol_m5"]:
            close(st, book, key, px, "volume_fade"); continue
        if held_min >= CFG["max_hold_h"] * 60: close(st, book, key, px, "max_hold"); continue

def evaluate(st, p):
    """Run the filter stack on a watched pool that has reached eval age."""
    reason = free_kill(p)
    rec = {"pool": p["pool"], "mint": p["mint"], "name": p["name"], "dex": p["dex"],
           "age_min": round((now() - p["created"]) / 60, 1), "mcap": round(p["mcap"]), "liq": round(p["liq"]),
           "vol_h1": round(p["vol_h1"]), "trades_h1": p["buys_h1"] + p["sells_h1"], "buyers_h1": p["buyers_h1"],
           "price": p["price"]}
    if reason:
        bump(st, "kill:" + reason); log("decisions.jsonl", {**rec, "decision": "skip", "stage": "scanner", "reason": reason}); return
    reason, info = chain_check(p, st)
    rec.update(info)
    if reason:
        bump(st, "kill:" + reason); log("decisions.jsonl", {**rec, "decision": "skip", "stage": "chain", "reason": reason}); return
    bump(st, "survivor")
    if sum(1 for v in st["shadows"].values() if not v.get("ended")) < CFG["max_active_shadows"]:
        open_position(st, p, "shadows")
    else:
        bump(st, "shadow_cap")
    if len(st["open"]) >= CFG["max_open"]:
        bump(st, "skip:max_open"); log("decisions.jsonl", {**rec, "decision": "skip", "stage": "risk", "reason": "max_open"}); return
    if st["cash"] < CFG["ticket_usd"]:
        bump(st, "skip:no_cash"); log("decisions.jsonl", {**rec, "decision": "skip", "stage": "risk", "reason": "no_cash"}); return
    open_position(st, p, "open"); bump(st, "trade")
    log("decisions.jsonl", {**rec, "decision": "buy", "stage": "execution", "ticket": CFG["ticket_usd"]})
    log("trades.jsonl", {"event": "entry", **rec, "entry_px_with_slip": buy_px(p["price"]), "ticket": CFG["ticket_usd"]})

def archive_shadows(st):
    """Move finished shadows out of state so state.json stays small."""
    for k in [k for k, v in st["shadows"].items() if v.get("ended")]:
        with open(path("shadows_done.jsonl"), "a") as fh: fh.write(json.dumps({"pool_key": k, **st["shadows"][k]}) + "\n")
        del st["shadows"][k]

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
    # 1. scanner: register new pump launches
    for p in fetch_new(st):
        if not p["pool"] or p["pool"] in st["seen"] or not p["created"]: continue
        st["seen"][p["pool"]] = round(p["created"])
        if not is_pump(p["dex"]):
            bump(st, "ignored_non_pump"); continue
        bump(st, "launches_seen")
        age = (t - p["created"]) / 60
        if age > CFG["eval_max_age_min"]:
            bump(st, "kill:missed_too_old"); log("decisions.jsonl", {"pool": p["pool"], "name": p["name"], "decision": "skip", "stage": "scanner", "reason": "missed_too_old", "age_min": round(age, 1)}); continue
        st["watch"][p["pool"]] = round(p["created"])
    # 2. quotes for everything we care about
    due = [k for k, c in st["watch"].items() if t - c >= CFG["eval_min_age_min"] * 60]
    live = [v["pool"] for v in st["open"].values()] + [v["pool"] for v in st["shadows"].values() if not v.get("ended")]
    quotes = fetch_pools(due + live, st)
    for k in due:
        del st["watch"][k]
        q = quotes.get(k)
        if not q or not q["created"]:
            bump(st, "kill:no_data"); log("decisions.jsonl", {"pool": k, "decision": "skip", "stage": "scanner", "reason": "no_data"}); continue
        evaluate(st, q)
    # 3. exits
    manage(st, "open", quotes); manage(st, "shadows", quotes)
    archive_shadows(st)
    # trim memory of seen pools older than 2h
    if len(st["seen"]) > 20000:
        st["seen"] = {k: v for k, v in st["seen"].items() if t - v < 7200}

def run(minutes):
    os.makedirs(DATA_DIR, exist_ok=True)
    st = load_state()
    if st["started"] is None:
        st["started"] = now(); log("events.jsonl", {"event": "start", "cfg": CFG})
    if st.get("done"):
        print("run already finished"); return 0
    end_run = st["started"] + CFG["run_hours"] * 3600
    stop_at = min(now() + minutes * 60, end_run)
    log("events.jsonl", {"event": "session_start", "until": iso(stop_at)})
    last_commit = now()
    while now() < stop_at:
        t0 = now()
        try:
            step(st)
        except Exception as e:
            log("events.jsonl", {"event": "error", "err": repr(e)[:300]})
        save_state(st)
        if now() - last_commit > CFG["commit_every_min"] * 60:
            commit(f"sim data {iso()}"); last_commit = now()
        time.sleep(max(1, CFG["poll_s"] - (now() - t0)))
    if now() >= end_run:
        # close anything still open at the last price we have
        for k in list(st["open"]): close(st, "open", k, st["open"][k]["last_px"], "sim_end")
        for k, v in st["shadows"].items():
            if "rule_exit" not in v: close(st, "shadows", k, v["last_px"], "sim_end")
            v["ended"] = True
        archive_shadows(st)
        st["done"] = True; log("events.jsonl", {"event": "finished"})
    save_state(st)
    log("events.jsonl", {"event": "session_end"})
    commit(f"sim data {iso()}")
    return 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd")
    r = sub.add_parser("run"); r.add_argument("--minutes", type=float, default=340)
    a = ap.parse_args()
    if a.cmd == "run": sys.exit(run(a.minutes))
    ap.print_help()
