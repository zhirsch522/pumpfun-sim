# pump.fun paper sim summary (copy)

- Window: 2026-11-04T13:02:11Z, 13.37h covered, gaps 219.9 min, finished: False
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 11182, evaluated 0, missed (too old when first seen) 0
- Copy: signals {'random_wallet': 346, 'leaders': 26}, median delay from their buy to our paper buy 229s, hot coins watched 1818, trades read 207006, last wallet save {'ts': '2026-11-05T02:28:08Z', 'event': 'wallets_saved', 'wallets': 31512, 'leaders': 64}

## leaders
- Paper P&L $34.37 (3.44%), survivors 0, trades 10 (holder check unavailable on 0), open 1
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $29.04 (45.2%), worst drawdown 12.1%
- Closed trades {'n': 9, 'avg_pct': 19.75, 'median_pct': 1.21, 'win_rate': 55.6}
- Rules on every survivor None
- Random hold on its survivors None
- Exits {'no_volume': 4, 'stop_loss': 3, 'volume_fade': 2}
- Best: XDG / SOL 91.38% (no_volume); FOREVER / SOL 71.56% (no_volume); FOREVER / SOL 64.75% (no_volume)
- Worst: tinfoilcat / SOL -50.9% (stop_loss); Aren / SOL -45.17% (stop_loss); thesis / SOL -5.83% (no_volume)

## random_wallet
- Paper P&L $-93.1 (-9.31%), survivors 0, trades 79 (holder check unavailable on 0), open 2
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $1.48 (-92.6%), worst drawdown 93.6%
- Closed trades {'n': 77, 'avg_pct': -5.99, 'median_pct': -5.83, 'win_rate': 36.4}
- Rules on every survivor None
- Random hold on its survivors None
- Exits {'volume_fade': 11, 'dead_pool': 8, 'stop_loss': 15, 'leader_exit': 8, 'trail_stop': 7, 'no_volume': 28}
- Best: UAV / SOL 242.37% (no_volume); B/C Cow / SOL 210.24% (no_volume); UAV / SOL 113.17% (leader_exit)
- Worst: FOREVER / SOL -100.0% (dead_pool); AMD / SOL -100.0% (stop_loss); Reboot / SOL -100.0% (dead_pool)

