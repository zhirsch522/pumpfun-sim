# pump.fun paper sim summary (fresh)

- Window: 2026-11-03T18:29:49Z, 18.49h covered, gaps 818.7 min, finished: True
- Dead/rugged pools with garbage post-rug prices: 14 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 11394, evaluated 11082, missed (too old when first seen) 0
- All-launch baseline (1 in 5 launches, bought at 10 min old): random exit {'n': 107900, 'avg_pct': -6.77, 'median_pct': -5.83, 'win_rate': 3.4}, hold 1h {'n': 2158, 'avg_pct': -7.33, 'median_pct': -5.83, 'win_rate': 3.0}, hold 3h {'n': 2158, 'avg_pct': -7.78, 'median_pct': -5.83, 'win_rate': 3.0}

## strict
- Paper P&L $-228.42 (-22.84%), survivors 318, trades 73 (holder check unavailable on 0), open 0
- Kills: low_liquidity 10266, low_volume 395, mcap_too_low 26, few_buyers 26, mcap_too_high 21, dumping_m5 18, whale_wallet 7, sell_heavy_m5 3, sell_heavy_h1 2
- $20 wallet, 25% of wallet per trade: ends $0.74 (-96.3%), worst drawdown 98.8%
- Closed trades {'n': 73, 'avg_pct': -15.65, 'median_pct': -40.0, 'win_rate': 37.0}
- Rules on every survivor {'n': 280, 'avg_pct': -4.05, 'median_pct': -19.09, 'win_rate': 41.4}
- Random hold on its survivors {'n': 14150, 'avg_pct': 3.49, 'median_pct': -19.14, 'win_rate': 41.5}
- Exits {'dead_pool': 10, 'sim_end': 3, 'no_volume': 5, 'volume_fade': 21, 'stop_loss': 34}
- Best: Intel AI / SOL 281.74% (volume_fade); SASONA Ai / SOL 203.53% (volume_fade); BLOOM / SOL 197.67% (no_volume)
- Worst: PEACE / SOL -100.0% (dead_pool); Plonk / SOL -100.0% (dead_pool); NEX Ai / SOL -100.0% (dead_pool)

## medium
- Paper P&L $-310.68 (-31.07%), survivors 379, trades 72 (holder check unavailable on 0), open 0
- Kills: low_liquidity 9552, low_volume 856, mcap_too_low 195, few_buyers 36, mcap_too_high 21, dumping_m5 19, sell_heavy_m5 13, whale_wallet 9, few_trades 1, sell_heavy_h1 1
- $20 wallet, 25% of wallet per trade: ends $2.41 (-88.0%), worst drawdown 95.3%
- Closed trades {'n': 72, 'avg_pct': -21.58, 'median_pct': -40.36, 'win_rate': 29.2}
- Rules on every survivor {'n': 334, 'avg_pct': -3.46, 'median_pct': -22.38, 'win_rate': 40.4}
- Random hold on its survivors {'n': 16800, 'avg_pct': 0.99, 'median_pct': -27.59, 'win_rate': 38.2}
- Exits {'dead_pool': 9, 'sim_end': 2, 'no_volume': 5, 'volume_fade': 23, 'stop_loss': 33}
- Best: Intel AI / SOL 281.74% (volume_fade); BLOOM / SOL 197.67% (no_volume); Other / SOL 141.36% (volume_fade)
- Worst: PEACE / SOL -100.0% (dead_pool); Plonk / SOL -100.0% (dead_pool); STARMIND / SOL -100.0% (dead_pool)

## curve
- Paper P&L $-32.75 (-3.28%), survivors 700, trades 32 (holder check unavailable on 0), open 0
- Kills: mcap_too_low 4262, low_liquidity 3229, low_volume 2438, few_trades 129, few_buyers 115, sell_heavy_m5 106, sell_heavy_h1 33, dumping_m5 24, whale_wallet 22, mcap_too_high 21, concentrated_top10 2, chain_backlog 1
- $20 wallet, 25% of wallet per trade: ends $9.84 (-50.8%), worst drawdown 72.1%
- Closed trades {'n': 32, 'avg_pct': -5.12, 'median_pct': -7.19, 'win_rate': 25.0}
- Rules on every survivor {'n': 577, 'avg_pct': -6.84, 'median_pct': -6.19, 'win_rate': 25.8}
- Random hold on its survivors {'n': 30800, 'avg_pct': -4.29, 'median_pct': -8.43, 'win_rate': 22.6}
- Exits {'dead_pool': 3, 'sim_end': 2, 'no_volume': 8, 'volume_fade': 14, 'stop_loss': 5}
- Best: BLOOM / SOL 197.67% (no_volume); 2 / SOL 127.12% (volume_fade); STONKS / SOL 97.24% (volume_fade)
- Worst: Plonk / SOL -100.0% (dead_pool); 特斯拉 / SOL -100.0% (dead_pool); Mag / SOL -98.88% (stop_loss)

## rugonly
- Paper P&L $-27.62 (-2.76%), survivors 24, trades 24 (holder check unavailable on 0), open 0
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $14.02 (-29.9%), worst drawdown 29.9%
- Closed trades {'n': 24, 'avg_pct': -5.75, 'median_pct': -5.83, 'win_rate': 0.0}
- Rules on every survivor {'n': 21, 'avg_pct': -5.74, 'median_pct': -5.83, 'win_rate': 0.0}
- Random hold on its survivors {'n': 1200, 'avg_pct': -6.85, 'median_pct': -5.83, 'win_rate': 0.0}
- Exits {'no_volume': 18, 'sim_end': 3, 'volume_fade': 3}
- Best: IQD / SOL -4.01% (volume_fade); pumpcat / SOL -5.57% (no_volume); NORTHKOREA / SOL -5.83% (sim_end)
- Worst: ROOTL / SOL -5.96% (sim_end); B277D / SOL -5.9% (no_volume); CRTMIND / SOL -5.83% (volume_fade)

