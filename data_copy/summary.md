# pump.fun paper sim summary (copy)

- Window: 2026-11-04T13:02:11Z, 24.45h covered, gaps 219.9 min, finished: False
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 20346, evaluated 0, missed (too old when first seen) 0
- Copy: signals {'random_wallet': 682, 'leaders': 179}, median delay from their buy to our paper buy 322s, hot coins watched 3150, trades read 372111, last wallet save {'ts': '2026-11-05T13:31:35Z', 'event': 'wallets_saved', 'wallets': 43770, 'leaders': 205}
- random_wallet: closed 154, closed P&L $215.72, best trade $193.21 (NEX Ai / SOL), P&L without it $22.51; our price vs the copied wallet's: median 9.6% (paid more on 0.72 of trades); avg return faster half -0.2% vs slower half 14.2% (split at 278.0s)
- leaders: closed 57, closed P&L $59.17, best trade $193.21 (NEX Ai / SOL), P&L without it $-134.04; our price vs the copied wallet's: median 14.8% (paid more on 0.81 of trades); avg return faster half -12.8% vs slower half 23.8% (split at 369s)

## leaders
- Paper P&L $56.4 (5.64%), survivors 0, trades 58 (holder check unavailable on 0), open 1
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $5.01 (-75.0%), worst drawdown 92.5%
- Closed trades {'n': 57, 'avg_pct': 5.19, 'median_pct': -5.83, 'win_rate': 43.9}
- Rules on every survivor None
- Random hold on its survivors None
- Exits {'no_volume': 25, 'trail_stop': 1, 'stop_loss': 9, 'volume_fade': 8, 'dead_pool': 7, 'leader_exit': 7}
- Best: NEX Ai / SOL 966.03% (no_volume); PEACOCK / SOL 108.15% (no_volume); Look / SOL 99.47% (trail_stop)
- Worst: Buffett / SOL -100.0% (dead_pool); ZELDA / SOL -100.0% (stop_loss); ZELDA / SOL -100.0% (dead_pool)

## random_wallet
- Paper P&L $214.55 (21.46%), survivors 0, trades 155 (holder check unavailable on 0), open 1
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $2.74 (-86.3%), worst drawdown 97.6%
- Closed trades {'n': 154, 'avg_pct': 7.0, 'median_pct': -5.83, 'win_rate': 39.0}
- Rules on every survivor None
- Random hold on its survivors None
- Exits {'no_volume': 58, 'trail_stop': 11, 'stop_loss': 29, 'volume_fade': 26, 'dead_pool': 14, 'leader_exit': 16}
- Best: NEX Ai / SOL 966.03% (no_volume); Democat / SOL 514.68% (no_volume); Look / SOL 320.71% (volume_fade)
- Worst: FOREVER / SOL -100.0% (dead_pool); AMD / SOL -100.0% (stop_loss); Reboot / SOL -100.0% (dead_pool)

