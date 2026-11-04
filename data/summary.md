# pump.fun paper sim summary (v2)

- Window: 2026-11-03T18:29:49Z, 5.65h covered, gaps 150.4 min, finished: False
- Launches seen 5750, evaluated 5447, missed (too old when first seen) 0
- All-launch baseline (1 in 5 launches, bought at 10 min old): random exit {'n': 53800, 'avg_pct': 5017.86, 'median_pct': -5.83, 'win_rate': 3.3}, hold 1h {'n': 1076, 'avg_pct': 6275.4, 'median_pct': -5.83, 'win_rate': 3.2}, hold 3h {'n': 1076, 'avg_pct': 6274.75, 'median_pct': -5.83, 'win_rate': 3.2}

## strict
- Paper P&L $1126464.24 (112646.42%), survivors 148, trades 39 (holder check unavailable on 0), open 3
- Kills: low_liquidity 5107, low_volume 152, few_buyers 12, dumping_m5 9, mcap_too_low 7, mcap_too_high 7, whale_wallet 3, sell_heavy_m5 1, sell_heavy_h1 1
- $20 wallet, 25% of wallet per trade: ends $1.682771994561232e+18 (8.41385997280616e+18%), worst drawdown 52.1%
- Closed trades {'n': 36, 'avg_pct': 156452.77, 'median_pct': 12.88, 'win_rate': 55.6}
- Rules on every survivor {'n': 111, 'avg_pct': 467889.9, 'median_pct': 14.48, 'win_rate': 55.9}
- Random hold on its survivors {'n': 5650, 'avg_pct': 476390.54, 'median_pct': -5.83, 'win_rate': 47.4}
- Exits {'stop_loss': 14, 'volume_fade': 22}
- Best: AMD / SOL 1339292.95% (volume_fade); PEACE / SOL 1214375.96% (volume_fade); FOREVER / SOL 967988.92% (volume_fade)
- Worst: Green Cat / SOL -99.98% (stop_loss); GTA 6 Coin / SOL -98.9% (stop_loss); Mag / SOL -98.88% (stop_loss)

## medium
- Paper P&L $530868.76 (53086.88%), survivors 178, trades 36 (holder check unavailable on 0), open 3
- Kills: low_liquidity 4744, low_volume 381, mcap_too_low 96, few_buyers 16, dumping_m5 10, sell_heavy_m5 9, mcap_too_high 7, whale_wallet 4, few_trades 1, sell_heavy_h1 1
- $20 wallet, 25% of wallet per trade: ends $36473639.49 (182368097.5%), worst drawdown 76.3%
- Closed trades {'n': 33, 'avg_pct': 80433.71, 'median_pct': -6.37, 'win_rate': 42.4}
- Rules on every survivor {'n': 134, 'avg_pct': 387583.76, 'median_pct': 6.68, 'win_rate': 53.7}
- Random hold on its survivors {'n': 6800, 'avg_pct': 408352.63, 'median_pct': -15.96, 'win_rate': 44.8}
- Exits {'stop_loss': 14, 'volume_fade': 19}
- Best: PEACE / SOL 1214375.96% (volume_fade); Plonk / SOL 733581.63% (volume_fade); FOREVER / SOL 706661.27% (volume_fade)
- Worst: GTA 6 Coin / SOL -98.9% (stop_loss); Mag / SOL -98.88% (stop_loss); X / SOL -97.58% (stop_loss)

## curve
- Paper P&L $146718.06 (14671.81%), survivors 377, trades 20 (holder check unavailable on 0), open 3
- Kills: mcap_too_low 2043, low_liquidity 1495, low_volume 1244, few_trades 102, sell_heavy_m5 67, few_buyers 60, sell_heavy_h1 28, dumping_m5 13, whale_wallet 9, mcap_too_high 7, concentrated_top10 1
- $20 wallet, 25% of wallet per trade: ends $24933.68 (124568.4%), worst drawdown 49.9%
- Closed trades {'n': 17, 'avg_pct': 43153.17, 'median_pct': -5.83, 'win_rate': 35.3}
- Rules on every survivor {'n': 255, 'avg_pct': 203665.43, 'median_pct': -5.83, 'win_rate': 31.0}
- Random hold on its survivors {'n': 14750, 'avg_pct': 198858.38, 'median_pct': -6.29, 'win_rate': 21.6}
- Exits {'stop_loss': 3, 'volume_fade': 14}
- Best: Plonk / SOL 733581.63% (volume_fade); 2 / SOL 127.12% (volume_fade); STONKS / SOL 97.24% (volume_fade)
- Worst: Mag / SOL -98.88% (stop_loss); Pokémon / SOL -63.16% (stop_loss); RabBIT / Satoshi -44.23% (stop_loss)

## rugonly
- Paper P&L $-6.64 (-0.66%), survivors 6, trades 6 (holder check unavailable on 0), open 3
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $19.23 (-3.9%), worst drawdown 3.9%
- Closed trades {'n': 3, 'avg_pct': -5.22, 'median_pct': -5.83, 'win_rate': 0.0}
- Rules on every survivor {'n': 3, 'avg_pct': -5.22, 'median_pct': -5.83, 'win_rate': 0.0}
- Random hold on its survivors {'n': 300, 'avg_pct': -9.23, 'median_pct': -5.83, 'win_rate': 0.0}
- Exits {'volume_fade': 3}
- Best: IQD / SOL -4.01% (volume_fade); casino / SPYx -5.83% (volume_fade); CRTMIND / SOL -5.83% (volume_fade)
- Worst: CRTMIND / SOL -5.83% (volume_fade); casino / SPYx -5.83% (volume_fade); IQD / SOL -4.01% (volume_fade)

