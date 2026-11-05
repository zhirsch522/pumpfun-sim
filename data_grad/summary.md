# pump.fun paper sim summary (grad)

- Window: 2026-11-04T13:02:09Z, 11.21h covered, gaps 16.4 min, finished: False
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 1013, evaluated 966, missed (too old when first seen) 0
- All-launch baseline (1 in 2 launches, bought at 15 min old): random exit {'n': 25150, 'avg_pct': -13.15, 'median_pct': -5.83, 'win_rate': 23.5}, hold 1h {'n': 503, 'avg_pct': -15.11, 'median_pct': -5.83, 'win_rate': 20.9}, hold 3h {'n': 503, 'avg_pct': -21.37, 'median_pct': -5.83, 'win_rate': 19.5}

## momo
- Paper P&L $-12.54 (-1.25%), survivors 131, trades 44 (holder check unavailable on 0), open 0
- Kills: low_liquidity 489, low_volume 166, mcap_too_low 94, dumping_m5 37, mcap_too_high 14, sell_heavy_h1 11, no_momentum_h1 10, sell_heavy_m5 9, whale_wallet 3, concentrated_top10 1, few_trades 1
- $20 wallet, 25% of wallet per trade: ends $12.28 (-38.6%), worst drawdown 73.7%
- Closed trades {'n': 44, 'avg_pct': -1.42, 'median_pct': -3.54, 'win_rate': 47.7}
- Rules on every survivor {'n': 130, 'avg_pct': -15.16, 'median_pct': -5.83, 'win_rate': 37.7}
- Random hold on its survivors {'n': 6500, 'avg_pct': 4.26, 'median_pct': -3.62, 'win_rate': 44.3}
- Exits {'dead_pool': 6, 'stop_loss': 12, 'trail_stop': 4, 'no_volume': 14, 'volume_fade': 8}
- Best: Green Cat / SOL 143.5% (no_volume); AMD / SOL 124.95% (no_volume); Chrome-Chan / SOL 121.99% (trail_stop)
- Worst: NEX Ai / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool); Intel AI / SOL -100.0% (dead_pool)

## loose
- Paper P&L $-105.1 (-10.51%), survivors 257, trades 64 (holder check unavailable on 0), open 0
- Kills: low_liquidity 446, low_volume 142, mcap_too_low 60, dumping_m5 33, mcap_too_high 14, whale_wallet 6, sell_heavy_h1 4, sell_heavy_m5 3, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $1.65 (-91.7%), worst drawdown 94.7%
- Closed trades {'n': 64, 'avg_pct': -8.21, 'median_pct': -5.7, 'win_rate': 35.9}
- Rules on every survivor {'n': 255, 'avg_pct': -10.99, 'median_pct': -5.83, 'win_rate': 40.0}
- Random hold on its survivors {'n': 12800, 'avg_pct': 4.1, 'median_pct': -5.83, 'win_rate': 43.5}
- Exits {'dead_pool': 14, 'stop_loss': 20, 'trail_stop': 9, 'no_volume': 15, 'volume_fade': 6}
- Best: AI / SOL 373.65% (volume_fade); Green Cat / SOL 143.5% (no_volume); GTA 6 Coin / SOL 129.12% (volume_fade)
- Worst: RAM / SOL -100.0% (dead_pool); FOREVER / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool)

## any
- Paper P&L $-104.54 (-10.45%), survivors 61, trades 61 (holder check unavailable on 0), open 0
- Kills: whale_wallet 8, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $3.63 (-81.9%), worst drawdown 84.0%
- Closed trades {'n': 61, 'avg_pct': -8.57, 'median_pct': -5.83, 'win_rate': 27.9}
- Rules on every survivor {'n': 61, 'avg_pct': -8.57, 'median_pct': -5.83, 'win_rate': 27.9}
- Random hold on its survivors {'n': 3050, 'avg_pct': -10.22, 'median_pct': -5.83, 'win_rate': 26.2}
- Exits {'dead_pool': 4, 'stop_loss': 10, 'no_volume': 38, 'trail_stop': 3, 'volume_fade': 6}
- Best: P C / SOL 114.23% (no_volume); Aren / SOL 110.82% (trail_stop); FOREVER / SOL 85.57% (volume_fade)
- Worst: NEX Ai / SOL -100.0% (dead_pool); MIGA / SOL -100.0% (dead_pool); Impeach / SOL -100.0% (dead_pool)

