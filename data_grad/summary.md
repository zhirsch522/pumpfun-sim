# pump.fun paper sim summary (grad)

- Window: 2026-11-04T13:02:09Z, 23.98h covered, gaps 48.3 min, finished: True
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 2000, evaluated 1940, missed (too old when first seen) 0
- All-launch baseline (1 in 2 launches, bought at 15 min old): random exit {'n': 49650, 'avg_pct': -6.77, 'median_pct': -5.83, 'win_rate': 25.0}, hold 1h {'n': 993, 'avg_pct': -9.42, 'median_pct': -5.83, 'win_rate': 22.9}, hold 3h {'n': 993, 'avg_pct': -13.42, 'median_pct': -5.83, 'win_rate': 21.8}

## momo
- Paper P&L $-93.95 (-9.39%), survivors 270, trades 114 (holder check unavailable on 0), open 0
- Kills: low_liquidity 996, low_volume 317, mcap_too_low 200, dumping_m5 67, mcap_too_high 32, sell_heavy_h1 19, no_momentum_h1 16, sell_heavy_m5 13, whale_wallet 6, few_trades 3, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $2.19 (-89.0%), worst drawdown 90.1%
- Closed trades {'n': 114, 'avg_pct': -4.12, 'median_pct': 3.62, 'win_rate': 52.6}
- Rules on every survivor {'n': 269, 'avg_pct': -8.26, 'median_pct': -4.15, 'win_rate': 43.9}
- Random hold on its survivors {'n': 13450, 'avg_pct': 8.49, 'median_pct': 0.19, 'win_rate': 50.3}
- Exits {'volume_fade': 28, 'dead_pool': 19, 'sim_end': 1, 'stop_loss': 24, 'trail_stop': 6, 'no_volume': 36}
- Best: Green Cat / SOL 143.5% (no_volume); AMD / SOL 124.95% (no_volume); Chrome-Chan / SOL 121.99% (trail_stop)
- Worst: NEX Ai / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool); Intel AI / SOL -100.0% (dead_pool)

## loose
- Paper P&L $-72.85 (-7.29%), survivors 513, trades 149 (holder check unavailable on 0), open 0
- Kills: low_liquidity 926, low_volume 289, mcap_too_low 92, dumping_m5 58, mcap_too_high 32, whale_wallet 13, sell_heavy_h1 10, sell_heavy_m5 6, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $0.54 (-97.3%), worst drawdown 98.7%
- Closed trades {'n': 149, 'avg_pct': -2.44, 'median_pct': -4.15, 'win_rate': 40.9}
- Rules on every survivor {'n': 512, 'avg_pct': -4.45, 'median_pct': -4.13, 'win_rate': 44.5}
- Random hold on its survivors {'n': 25600, 'avg_pct': 13.57, 'median_pct': -2.96, 'win_rate': 47.7}
- Exits {'volume_fade': 24, 'dead_pool': 27, 'sim_end': 1, 'stop_loss': 41, 'trail_stop': 13, 'no_volume': 43}
- Best: CR / SOL 688.68% (no_volume); AI / SOL 373.65% (volume_fade); Democat / SOL 186.78% (volume_fade)
- Worst: RAM / SOL -100.0% (dead_pool); FOREVER / SOL -100.0% (dead_pool); Skateboard / SOL -100.0% (dead_pool)

## any
- Paper P&L $-277.01 (-27.7%), survivors 176, trades 176 (holder check unavailable on 0), open 0
- Kills: whale_wallet 24, concentrated_top10 2, mint_authority_set 2
- $20 wallet, 25% of wallet per trade: ends $0.2 (-99.0%), worst drawdown 99.1%
- Closed trades {'n': 176, 'avg_pct': -7.87, 'median_pct': -5.83, 'win_rate': 28.4}
- Rules on every survivor {'n': 176, 'avg_pct': -7.87, 'median_pct': -5.83, 'win_rate': 28.4}
- Random hold on its survivors {'n': 8800, 'avg_pct': -7.13, 'median_pct': -5.83, 'win_rate': 26.7}
- Exits {'volume_fade': 20, 'dead_pool': 14, 'sim_end': 3, 'stop_loss': 28, 'trail_stop': 8, 'no_volume': 103}
- Best: mspaint / SOL 232.96% (no_volume); PONS / SOL 186.04% (volume_fade); x / SOL 154.98% (trail_stop)
- Worst: NEX Ai / SOL -100.0% (dead_pool); MIGA / SOL -100.0% (dead_pool); Impeach / SOL -100.0% (dead_pool)

