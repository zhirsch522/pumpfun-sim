"""Download ~20 years of free daily prices (dividend/split adjusted) from Yahoo via yfinance.

Run:  pip install yfinance pandas && python fetch_data.py
Writes data/<TICKER>.csv with Date,Open,High,Low,Close,Volume (all prices adjusted).
"""
import os
import yfinance as yf

TICKERS = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "IEF", "GLD", "SHY", "BIL"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)

for t in TICKERS:
    df = yf.download(t, start="2002-01-01", auto_adjust=True, progress=False, multi_level_index=False)
    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    df.index.name = "Date"
    df.to_csv(os.path.join(OUT, f"{t}.csv"), float_format="%.6f")
    print(t, len(df), df.index[0].date(), df.index[-1].date())
