# pump.fun paper sim summary (copy)

- Window: 2026-11-04T13:02:11Z, 5.7h covered, gaps 165.3 min, finished: False
- Dead/rugged pools with garbage post-rug prices: 0 logged exits re-valued at 0 (live guard added Nov 4): a one-poll jump of 50x, or 10x that then freezes or collapses
- Launches seen 4710, evaluated 0, missed (too old when first seen) 0
- Copy: signals {'random_wallet': 174, 'leaders': 4}, median delay from their buy to our paper buy 242s, hot coins watched 801, trades read 99958, last wallet save {'ts': '2026-11-04T18:46:58Z', 'event': 'wallets_saved', 'wallets': 18023, 'leaders': 33}

## leaders
- Paper P&L $13.67 (1.37%), survivors 0, trades 3 (holder check unavailable on 0), open 3
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $20.0 (0.0%), worst drawdown 0.0%
- Closed trades None
- Rules on every survivor None
- Random hold on its survivors None
- Exits {}
- Best: 
- Worst: 

## random_wallet
- Paper P&L $-173.84 (-17.38%), survivors 0, trades 40 (holder check unavailable on 0), open 3
- Kills: 
- $20 wallet, 25% of wallet per trade: ends $1.66 (-91.7%), worst drawdown 91.9%
- Closed trades {'n': 37, 'avg_pct': -22.31, 'median_pct': -11.2, 'win_rate': 27.0}
- Rules on every survivor None
- Random hold on its survivors None
- Exits {'dead_pool': 4, 'volume_fade': 6, 'trail_stop': 4, 'stop_loss': 11, 'leader_exit': 4, 'no_volume': 8}
- Best: UAV / SOL 113.17% (leader_exit); 大A / SOL 106.11% (volume_fade); Donkey / SOL 69.09% (trail_stop)
- Worst: FOREVER / SOL -100.0% (dead_pool); AMD / SOL -100.0% (stop_loss); Reboot / SOL -100.0% (dead_pool)

