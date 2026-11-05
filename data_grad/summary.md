# pump.fun paper sim summary (grad)

- Window: 2026-11-04T13:02:09Z, 22.27h covered, gaps 48.3 min, finished: False
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 1883, evaluated 1828, missed (too old when first seen) 0
- All-launch baseline (1 in 2 launches, bought at 15 min old): random exit {'n': 46800, 'avg_pct': -8.74, 'median_pct': -5.83, 'win_rate': 24.5}, hold 1h {'n': 936, 'avg_pct': -11.51, 'median_pct': -5.83, 'win_rate': 22.2}, hold 3h {'n': 936, 'avg_pct': -15.27, 'median_pct': -5.83, 'win_rate': 21.3}

## momo
- Paper P&L $-75.73 (-7.57%), survivors 259, trades 107 (holder check unavailable on 0), open 1
- Kills: low_liquidity 932, low_volume 298, mcap_too_low 190, dumping_m5 63, mcap_too_high 30, sell_heavy_h1 18, no_momentum_h1 16, sell_heavy_m5 13, whale_wallet 5, few_trades 3, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $3.0 (-85.0%), worst drawdown 85.0%
- Closed trades {'n': 106, 'avg_pct': -3.74, 'median_pct': 1.97, 'win_rate': 51.9}
- Rules on every survivor {'n': 255, 'avg_pct': -8.33, 'median_pct': -4.57, 'win_rate': 43.1}
- Random hold on its survivors {'n': 12900, 'avg_pct': 10.02, 'median_pct': 0.08, 'win_rate': 50.3}
- Exits {'volume_fade': 25, 'no_volume': 36, 'trail_stop': 5, 'stop_loss': 22, 'dead_pool': 18}
- Best: Green Cat / SOL 143.5% (no_volume); AMD / SOL 124.95% (no_volume); Chrome-Chan / SOL 121.99% (trail_stop)
- Worst: NEX Ai / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool); Intel AI / SOL -100.0% (dead_pool)

## loose
- Paper P&L $-184.93 (-18.49%), survivors 494, trades 139 (holder check unavailable on 0), open 2
- Kills: low_liquidity 866, low_volume 271, mcap_too_low 86, dumping_m5 55, mcap_too_high 30, whale_wallet 11, sell_heavy_h1 8, sell_heavy_m5 6, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $0.27 (-98.7%), worst drawdown 98.7%
- Closed trades {'n': 137, 'avg_pct': -6.74, 'median_pct': -5.04, 'win_rate': 40.1}
- Rules on every survivor {'n': 484, 'avg_pct': -7.1, 'median_pct': -5.3, 'win_rate': 43.6}
- Random hold on its survivors {'n': 24600, 'avg_pct': 12.3, 'median_pct': -3.03, 'win_rate': 47.3}
- Exits {'volume_fade': 21, 'no_volume': 41, 'trail_stop': 12, 'stop_loss': 36, 'dead_pool': 27}
- Best: AI / SOL 373.65% (volume_fade); Democat / SOL 186.78% (volume_fade); PONS / SOL 186.04% (volume_fade)
- Worst: RAM / SOL -100.0% (dead_pool); FOREVER / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool)

## any
- Paper P&L $-248.48 (-24.85%), survivors 161, trades 161 (holder check unavailable on 0), open 3
- Kills: whale_wallet 23, concentrated_top10 2, mint_authority_set 2
- $20 wallet, 25% of wallet per trade: ends $0.25 (-98.8%), worst drawdown 99.1%
- Closed trades {'n': 158, 'avg_pct': -8.25, 'median_pct': -5.83, 'win_rate': 28.5}
- Rules on every survivor {'n': 158, 'avg_pct': -8.25, 'median_pct': -5.83, 'win_rate': 28.5}
- Random hold on its survivors {'n': 8050, 'avg_pct': -8.64, 'median_pct': -5.83, 'win_rate': 26.6}
- Exits {'volume_fade': 17, 'no_volume': 95, 'trail_stop': 7, 'stop_loss': 26, 'dead_pool': 13}
- Best: mspaint / SOL 232.96% (no_volume); PONS / SOL 186.04% (volume_fade); x / SOL 154.98% (trail_stop)
- Worst: NEX Ai / SOL -100.0% (dead_pool); MIGA / SOL -100.0% (dead_pool); Impeach / SOL -100.0% (dead_pool)

