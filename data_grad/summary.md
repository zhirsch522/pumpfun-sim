# pump.fun paper sim summary (grad)

- Window: 2026-11-04T13:02:09Z, 5.7h covered, gaps 5.9 min, finished: False
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 583, evaluated 546, missed (too old when first seen) 0
- All-launch baseline (1 in 2 launches, bought at 15 min old): random exit {'n': 14250, 'avg_pct': -10.87, 'median_pct': -5.83, 'win_rate': 22.1}, hold 1h {'n': 285, 'avg_pct': -12.46, 'median_pct': -5.83, 'win_rate': 18.9}, hold 3h {'n': 285, 'avg_pct': -16.7, 'median_pct': -5.83, 'win_rate': 18.6}

## momo
- Paper P&L $-68.84 (-6.88%), survivors 84, trades 24 (holder check unavailable on 0), open 3
- Kills: low_liquidity 268, low_volume 87, mcap_too_low 62, dumping_m5 19, mcap_too_high 9, sell_heavy_h1 6, no_momentum_h1 5, sell_heavy_m5 3, whale_wallet 2, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $6.61 (-66.9%), worst drawdown 73.7%
- Closed trades {'n': 21, 'avg_pct': -17.88, 'median_pct': -16.22, 'win_rate': 38.1}
- Rules on every survivor {'n': 69, 'avg_pct': -23.27, 'median_pct': -31.78, 'win_rate': 36.2}
- Random hold on its survivors {'n': 4100, 'avg_pct': -4.99, 'median_pct': -5.83, 'win_rate': 41.0}
- Exits {'dead_pool': 5, 'stop_loss': 7, 'trail_stop': 2, 'volume_fade': 3, 'no_volume': 4}
- Best: Chrome-Chan / SOL 121.99% (trail_stop); P C / SOL 114.23% (no_volume); 我画地为牢 / SOL 56.82% (volume_fade)
- Worst: NEX Ai / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool); Intel AI / SOL -100.0% (dead_pool)

## loose
- Paper P&L $-151.59 (-15.16%), survivors 159, trades 37 (holder check unavailable on 0), open 3
- Kills: low_liquidity 243, low_volume 66, mcap_too_low 42, dumping_m5 18, mcap_too_high 9, whale_wallet 4, sell_heavy_m5 2, sell_heavy_h1 2, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $1.43 (-92.9%), worst drawdown 92.9%
- Closed trades {'n': 34, 'avg_pct': -21.97, 'median_pct': -7.55, 'win_rate': 26.5}
- Rules on every survivor {'n': 134, 'avg_pct': -18.91, 'median_pct': -26.48, 'win_rate': 35.8}
- Random hold on its survivors {'n': 7750, 'avg_pct': -3.77, 'median_pct': -5.14, 'win_rate': 42.6}
- Exits {'dead_pool': 10, 'stop_loss': 12, 'trail_stop': 6, 'volume_fade': 3, 'no_volume': 3}
- Best: GTA 6 Coin / SOL 129.12% (volume_fade); Chrome-Chan / SOL 121.99% (trail_stop); Donkey / SOL 108.41% (trail_stop)
- Worst: RAM / SOL -100.0% (dead_pool); FOREVER / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool)

## any
- Paper P&L $-86.38 (-8.64%), survivors 29, trades 29 (holder check unavailable on 0), open 3
- Kills: whale_wallet 4, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $5.12 (-74.4%), worst drawdown 79.4%
- Closed trades {'n': 26, 'avg_pct': -18.53, 'median_pct': -5.83, 'win_rate': 19.2}
- Rules on every survivor {'n': 26, 'avg_pct': -18.53, 'median_pct': -5.83, 'win_rate': 19.2}
- Random hold on its survivors {'n': 1450, 'avg_pct': -13.05, 'median_pct': -5.83, 'win_rate': 18.2}
- Exits {'dead_pool': 3, 'stop_loss': 5, 'trail_stop': 1, 'volume_fade': 3, 'no_volume': 14}
- Best: P C / SOL 114.23% (no_volume); FOREVER / SOL 85.57% (volume_fade); PAIRITY / SOL 14.14% (volume_fade)
- Worst: NEX Ai / SOL -100.0% (dead_pool); MIGA / SOL -100.0% (dead_pool); UAV / SOL -99.99% (stop_loss)

