# pump.fun paper sim summary (copy)

- Window: 2026-11-04T13:02:11Z, 31.76h covered, gaps 219.9 min, finished: True
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 26958, evaluated 0, missed (too old when first seen) 0
- Copy: signals {'random_wallet': 850, 'leaders': 241}, median delay from their buy to our paper buy 321.5s, hot coins watched 4199, trades read 470503, last wallet save {'ts': '2026-11-05T20:51:35Z', 'event': 'wallets_saved', 'wallets': 52661, 'leaders': 205}
- random_wallet: closed 200, closed P&L $-55.29, best trade $193.21 (NEX Ai / SOL), P&L without it $-248.49; our price vs the copied wallet's: median 9.9% (paid more on 0.74 of trades); avg return faster half -5.3% vs slower half 2.6% (split at 274.0s)
- leaders: closed 74, closed P&L $-91.69, best trade $193.21 (NEX Ai / SOL), P&L without it $-284.9; our price vs the copied wallet's: median 16.5% (paid more on 0.84 of trades); avg return faster half -19.7% vs slower half 7.3% (split at 376.0s)

## leaders
- Paper P&L $-91.69 (-9.17%), survivors 0, trades 74 (holder check unavailable on 0), open 0
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $0.53 (-97.3%), worst drawdown 99.1%
- Closed trades {'n': 74, 'avg_pct': -6.19, 'median_pct': -5.83, 'win_rate': 37.8}
- Rules on every survivor None
- Random hold on its survivors None
- Exits {'leader_exit': 7, 'stop_loss': 13, 'trail_stop': 1, 'sim_end': 1, 'dead_pool': 13, 'volume_fade': 9, 'no_volume': 30}
- Best: NEX Ai / SOL 966.03% (no_volume); P C / SOL 130.37% (no_volume); PEACOCK / SOL 108.15% (no_volume)
- Worst: Buffett / SOL -100.0% (dead_pool); ZELDA / SOL -100.0% (stop_loss); ZELDA / SOL -100.0% (dead_pool)

## random_wallet
- Paper P&L $-55.29 (-5.53%), survivors 0, trades 200 (holder check unavailable on 0), open 0
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $0.04 (-99.8%), worst drawdown 99.8%
- Closed trades {'n': 200, 'avg_pct': -1.38, 'median_pct': -5.83, 'win_rate': 34.5}
- Rules on every survivor None
- Random hold on its survivors None
- Exits {'leader_exit': 17, 'stop_loss': 45, 'trail_stop': 14, 'dead_pool': 20, 'volume_fade': 34, 'no_volume': 70}
- Best: NEX Ai / SOL 966.03% (no_volume); Democat / SOL 514.68% (no_volume); Look / SOL 320.71% (volume_fade)
- Worst: FOREVER / SOL -100.0% (dead_pool); AMD / SOL -100.0% (stop_loss); Reboot / SOL -100.0% (dead_pool)

