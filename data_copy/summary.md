# pump.fun paper sim summary (copy)

- Window: 2026-11-04T13:02:11Z, 29.98h covered, gaps 219.9 min, finished: False
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 25429, evaluated 0, missed (too old when first seen) 0
- Copy: signals {'random_wallet': 833, 'leaders': 224}, median delay from their buy to our paper buy 317.0s, hot coins watched 3970, trades read 446982, last wallet save {'ts': '2026-11-05T19:04:16Z', 'event': 'wallets_saved', 'wallets': 54023, 'leaders': 201}
- random_wallet: closed 192, closed P&L $-16.75, best trade $193.21 (NEX Ai / SOL), P&L without it $-209.95; our price vs the copied wallet's: median 9.8% (paid more on 0.74 of trades); avg return faster half -4.8% vs slower half 3.9% (split at 274.0s)
- leaders: closed 68, closed P&L $-59.87, best trade $193.21 (NEX Ai / SOL), P&L without it $-253.07; our price vs the copied wallet's: median 15.2% (paid more on 0.84 of trades); avg return faster half -23.9% vs slower half 15.1% (split at 366.5s)

## leaders
- Paper P&L $-61.03 (-6.1%), survivors 0, trades 69 (holder check unavailable on 0), open 1
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $0.83 (-95.8%), worst drawdown 98.7%
- Closed trades {'n': 68, 'avg_pct': -4.4, 'median_pct': -5.83, 'win_rate': 39.7}
- Rules on every survivor None
- Random hold on its survivors None
- Exits {'trail_stop': 1, 'stop_loss': 12, 'no_volume': 27, 'volume_fade': 9, 'leader_exit': 7, 'dead_pool': 12}
- Best: NEX Ai / SOL 966.03% (no_volume); P C / SOL 130.37% (no_volume); PEACOCK / SOL 108.15% (no_volume)
- Worst: Buffett / SOL -100.0% (dead_pool); ZELDA / SOL -100.0% (stop_loss); ZELDA / SOL -100.0% (dead_pool)

## random_wallet
- Paper P&L $-16.74 (-1.67%), survivors 0, trades 195 (holder check unavailable on 0), open 3
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $0.07 (-99.7%), worst drawdown 99.7%
- Closed trades {'n': 192, 'avg_pct': -0.44, 'median_pct': -5.83, 'win_rate': 34.9}
- Rules on every survivor None
- Random hold on its survivors None
- Exits {'trail_stop': 13, 'stop_loss': 42, 'no_volume': 68, 'volume_fade': 32, 'leader_exit': 17, 'dead_pool': 20}
- Best: NEX Ai / SOL 966.03% (no_volume); Democat / SOL 514.68% (no_volume); Look / SOL 320.71% (volume_fade)
- Worst: FOREVER / SOL -100.0% (dead_pool); AMD / SOL -100.0% (stop_loss); Reboot / SOL -100.0% (dead_pool)

