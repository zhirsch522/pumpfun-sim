# pump.fun paper sim summary (grad)

- Window: 2026-11-04T13:02:09Z, 16.74h covered, gaps 35.9 min, finished: False
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 1464, evaluated 1396, missed (too old when first seen) 0
- All-launch baseline (1 in 2 launches, bought at 15 min old): random exit {'n': 36600, 'avg_pct': -12.2, 'median_pct': -5.83, 'win_rate': 24.1}, hold 1h {'n': 732, 'avg_pct': -14.27, 'median_pct': -5.83, 'win_rate': 21.9}, hold 3h {'n': 732, 'avg_pct': -19.13, 'median_pct': -5.83, 'win_rate': 20.6}

## momo
- Paper P&L $-8.38 (-0.84%), survivors 194, trades 74 (holder check unavailable on 0), open 2
- Kills: low_liquidity 707, low_volume 233, mcap_too_low 135, dumping_m5 57, mcap_too_high 24, no_momentum_h1 14, sell_heavy_h1 13, sell_heavy_m5 12, whale_wallet 4, few_trades 2, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $11.31 (-43.4%), worst drawdown 73.7%
- Closed trades {'n': 72, 'avg_pct': -0.84, 'median_pct': 1.95, 'win_rate': 51.4}
- Rules on every survivor {'n': 191, 'avg_pct': -12.27, 'median_pct': -5.78, 'win_rate': 41.4}
- Random hold on its survivors {'n': 9650, 'avg_pct': 4.7, 'median_pct': -0.23, 'win_rate': 48.6}
- Exits {'trail_stop': 5, 'stop_loss': 15, 'no_volume': 24, 'volume_fade': 17, 'dead_pool': 11}
- Best: Green Cat / SOL 143.5% (no_volume); AMD / SOL 124.95% (no_volume); Chrome-Chan / SOL 121.99% (trail_stop)
- Worst: NEX Ai / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool); Intel AI / SOL -100.0% (dead_pool)

## loose
- Paper P&L $-43.34 (-4.33%), survivors 372, trades 101 (holder check unavailable on 0), open 3
- Kills: low_liquidity 654, low_volume 206, mcap_too_low 72, dumping_m5 48, mcap_too_high 24, whale_wallet 8, sell_heavy_h1 7, sell_heavy_m5 4, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $2.11 (-89.5%), worst drawdown 94.7%
- Closed trades {'n': 98, 'avg_pct': -2.45, 'median_pct': -4.47, 'win_rate': 41.8}
- Rules on every survivor {'n': 364, 'avg_pct': -8.84, 'median_pct': -5.83, 'win_rate': 41.8}
- Random hold on its survivors {'n': 18550, 'avg_pct': 3.42, 'median_pct': -4.22, 'win_rate': 45.2}
- Exits {'trail_stop': 10, 'stop_loss': 26, 'no_volume': 31, 'volume_fade': 13, 'dead_pool': 18}
- Best: AI / SOL 373.65% (volume_fade); PONS / SOL 186.04% (volume_fade); Green Cat / SOL 143.5% (no_volume)
- Worst: RAM / SOL -100.0% (dead_pool); FOREVER / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool)

## any
- Paper P&L $-160.34 (-16.03%), survivors 115, trades 115 (holder check unavailable on 0), open 3
- Kills: whale_wallet 13, concentrated_top10 2, mint_authority_set 2
- $20 wallet, 25% of wallet per trade: ends $1.01 (-95.0%), worst drawdown 95.0%
- Closed trades {'n': 112, 'avg_pct': -7.13, 'median_pct': -5.83, 'win_rate': 27.7}
- Rules on every survivor {'n': 112, 'avg_pct': -7.13, 'median_pct': -5.83, 'win_rate': 27.7}
- Random hold on its survivors {'n': 5750, 'avg_pct': -12.25, 'median_pct': -5.83, 'win_rate': 24.9}
- Exits {'trail_stop': 5, 'stop_loss': 21, 'no_volume': 67, 'volume_fade': 13, 'dead_pool': 6}
- Best: mspaint / SOL 232.96% (no_volume); PONS / SOL 186.04% (volume_fade); P C / SOL 114.23% (no_volume)
- Worst: NEX Ai / SOL -100.0% (dead_pool); MIGA / SOL -100.0% (dead_pool); Impeach / SOL -100.0% (dead_pool)

