# pump.fun paper sim summary (v2)

- Window: 2026-11-03T18:29:49Z, 13.21h covered, gaps 519.2 min, finished: False
- Dead/rugged pools with garbage post-rug prices: 12 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 7746, evaluated 7460, missed (too old when first seen) 0
- All-launch baseline (1 in 5 launches, bought at 10 min old): random exit {'n': 72500, 'avg_pct': -6.5, 'median_pct': -5.83, 'win_rate': 3.1}, hold 1h {'n': 1450, 'avg_pct': -7.25, 'median_pct': -5.83, 'win_rate': 2.6}, hold 3h {'n': 1450, 'avg_pct': -7.86, 'median_pct': -5.83, 'win_rate': 2.5}

## strict
- Paper P&L $-174.17 (-17.42%), survivors 202, trades 53 (holder check unavailable on 0), open 3
- Kills: low_liquidity 6955, low_volume 241, few_buyers 18, dumping_m5 13, mcap_too_high 12, mcap_too_low 10, whale_wallet 6, sell_heavy_m5 2, sell_heavy_h1 1
- $20 wallet, 25% of wallet per trade: ends $0.54 (-97.3%), worst drawdown 97.6%
- Closed trades {'n': 50, 'avg_pct': -17.33, 'median_pct': -42.48, 'win_rate': 34.0}
- Rules on every survivor {'n': 154, 'avg_pct': -5.45, 'median_pct': -33.45, 'win_rate': 38.3}
- Random hold on its survivors {'n': 8350, 'avg_pct': 8.39, 'median_pct': -7.07, 'win_rate': 44.2}
- Exits {'stop_loss': 23, 'volume_fade': 20, 'dead_pool': 7}
- Best: Intel AI / SOL 281.74% (volume_fade); SASONA Ai / SOL 203.53% (volume_fade); STARMIND / SOL 128.29% (volume_fade)
- Worst: PEACE / SOL -100.0% (dead_pool); Plonk / SOL -100.0% (dead_pool); NEX Ai / SOL -100.0% (dead_pool)

## medium
- Paper P&L $-238.22 (-23.82%), survivors 242, trades 50 (holder check unavailable on 0), open 3
- Kills: low_liquidity 6453, low_volume 561, mcap_too_low 131, few_buyers 25, dumping_m5 15, mcap_too_high 12, sell_heavy_m5 11, whale_wallet 8, few_trades 1, sell_heavy_h1 1
- $20 wallet, 25% of wallet per trade: ends $2.44 (-87.8%), worst drawdown 88.8%
- Closed trades {'n': 47, 'avg_pct': -24.99, 'median_pct': -44.23, 'win_rate': 25.5}
- Rules on every survivor {'n': 185, 'avg_pct': -3.11, 'median_pct': -24.86, 'win_rate': 38.4}
- Random hold on its survivors {'n': 10000, 'avg_pct': 6.01, 'median_pct': -18.1, 'win_rate': 41.4}
- Exits {'stop_loss': 24, 'volume_fade': 19, 'dead_pool': 4}
- Best: Intel AI / SOL 281.74% (volume_fade); Other / SOL 141.36% (volume_fade); 2 / SOL 127.12% (volume_fade)
- Worst: PEACE / SOL -100.0% (dead_pool); Plonk / SOL -100.0% (dead_pool); STARMIND / SOL -100.0% (dead_pool)

## curve
- Paper P&L $-18.26 (-1.83%), survivors 480, trades 20 (holder check unavailable on 0), open 3
- Kills: mcap_too_low 2743, low_liquidity 2107, low_volume 1765, few_trades 117, sell_heavy_m5 88, few_buyers 85, sell_heavy_h1 29, dumping_m5 17, whale_wallet 15, mcap_too_high 12, concentrated_top10 1, chain_backlog 1
- $20 wallet, 25% of wallet per trade: ends $12.3 (-38.5%), worst drawdown 62.9%
- Closed trades {'n': 17, 'avg_pct': -4.57, 'median_pct': -16.33, 'win_rate': 29.4}
- Rules on every survivor {'n': 335, 'avg_pct': -7.09, 'median_pct': -7.03, 'win_rate': 23.9}
- Random hold on its survivors {'n': 19850, 'avg_pct': -1.79, 'median_pct': -6.62, 'win_rate': 22.2}
- Exits {'stop_loss': 3, 'volume_fade': 13, 'dead_pool': 1}
- Best: 2 / SOL 127.12% (volume_fade); STONKS / SOL 97.24% (volume_fade); Plonk / SOL 62.59% (volume_fade)
- Worst: Plonk / SOL -100.0% (dead_pool); Mag / SOL -98.88% (stop_loss); Pokémon / SOL -63.16% (stop_loss)

## rugonly
- Paper P&L $-6.64 (-0.66%), survivors 6, trades 6 (holder check unavailable on 0), open 3
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $19.23 (-3.9%), worst drawdown 3.9%
- Closed trades {'n': 3, 'avg_pct': -5.22, 'median_pct': -5.83, 'win_rate': 0.0}
- Rules on every survivor {'n': 3, 'avg_pct': -5.22, 'median_pct': -5.83, 'win_rate': 0.0}
- Random hold on its survivors {'n': 300, 'avg_pct': -7.3, 'median_pct': -5.83, 'win_rate': 0.0}
- Exits {'volume_fade': 3}
- Best: IQD / SOL -4.01% (volume_fade); casino / SPYx -5.83% (volume_fade); CRTMIND / SOL -5.83% (volume_fade)
- Worst: CRTMIND / SOL -5.83% (volume_fade); casino / SPYx -5.83% (volume_fade); IQD / SOL -4.01% (volume_fade)

