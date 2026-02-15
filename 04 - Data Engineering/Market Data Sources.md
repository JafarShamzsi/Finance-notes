# Market Data Sources

Comprehensive guide to obtaining market data for algorithmic trading research and live systems.

---

## Free Data Sources

| Source | Data Type | Coverage | API | Limits |
|---|---|---|---|---|
| **Yahoo Finance** | EOD OHLCV, fundamentals | Global equities | `yfinance` | Unofficial, can break |
| **Alpha Vantage** | Intraday (1min+), FX, crypto | US equities, global FX | REST, free key | 5-25 calls/min |
| **FRED** | Economic data | US macro | `fredapi` | Generous |
| **Quandl (free tier)** | EOD, some alt data | US equities | `quandl` | Limited datasets |
| **IEX Cloud (free)** | EOD, basic intraday | US equities | REST | 50K credits/mo |
| **Binance/Exchange APIs** | Full tick, orderbook | Crypto | Websocket + REST | Rate limits |
| **SEC EDGAR** | Filings (10-K, 10-Q, 13-F) | US companies | REST | Generous |

## Paid Data Sources

| Source | Data Type | Cost | Best For |
|---|---|---|---|
| **Polygon.io** | Tick-level, real-time | $99-199/mo | Serious retail algo |
| **Nasdaq Data Link** | EOD, fundamentals, alt | $50-500/mo | Research |
| **Bloomberg Terminal** | Everything | ~$24K/year | Institutional |
| **Refinitiv/LSEG** | Everything | ~$22K/year | Institutional |
| **Norgate Data** | Clean EOD + survivorship-free | $50-150/mo | Backtesting |
| **QuantConnect** | Built-in data + compute | Free-$80/mo | Strategy platform |
| **Databento** | Tick data, futures | Pay per use | HFT research |

## Python Examples

```python
# Yahoo Finance (free, unreliable)
import yfinance as yf
data = yf.download('AAPL', start='2020-01-01', end='2024-01-01')

# Alpha Vantage
from alpha_vantage.timeseries import TimeSeries
ts = TimeSeries(key='YOUR_KEY')
data, meta = ts.get_intraday('AAPL', interval='5min', outputsize='full')

# Polygon.io
import requests
url = "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/minute/2024-01-15/2024-01-15"
resp = requests.get(url, params={'apiKey': 'YOUR_KEY'})

# FRED (economic data)
from fredapi import Fred
fred = Fred(api_key='YOUR_KEY')
gdp = fred.get_series('GDP')
unemployment = fred.get_series('UNRATE')
fed_funds = fred.get_series('FEDFUNDS')

# Crypto via CCXT
import ccxt
exchange = ccxt.binance()
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h', limit=1000)
```

## Data Quality Checklist

- [ ] Check for survivorship bias → [[Survivorship Bias]]
- [ ] Handle stock splits and dividends (use adjusted prices)
- [ ] Check for gaps and missing data → [[Data Cleaning and Preprocessing]]
- [ ] Verify timezone consistency
- [ ] Check for look-ahead bias in point-in-time data
- [ ] Validate against known prices (spot check)

---

**Related:** [[Data Engineering MOC]] | [[Alternative Data]] | [[Data Cleaning and Preprocessing]] | [[Tick Data and Trade Data]] | [[Survivorship Bias]]
