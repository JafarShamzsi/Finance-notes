# Tick Data and Trade Data

The most granular level of market data. Every quote change, every trade — the raw material for microstructure research and HFT.

---

## Data Types

| Type | Content | Size | Use |
|---|---|---|---|
| **Trade (TAQ)** | Price, size, timestamp, exchange | ~1-5 GB/day (US equities) | Signal research, backtesting |
| **Quote** | Bid/ask price, bid/ask size, timestamp | ~10-50 GB/day | Spread analysis, market making |
| **Order Book (L2/L3)** | Full book snapshots or deltas | ~100+ GB/day | HFT, microstructure |
| **OHLCV Bars** | Aggregated open/high/low/close/volume | Small | Most algo strategies |

## Bar Types for Algo Trading

### Time Bars (Standard)
```python
# 1-minute, 5-minute, daily bars
bars = df.resample('1min').agg({
    'price': ['first', 'max', 'min', 'last'],
    'volume': 'sum'
})
```

### Volume Bars (Better for Algos)
Sample every N shares traded instead of every N seconds:
```python
def volume_bars(trades, volume_per_bar=10000):
    """Create bars based on volume, not time."""
    bars = []
    current_bar = {'volume': 0, 'prices': [], 'start': None}

    for _, trade in trades.iterrows():
        if current_bar['start'] is None:
            current_bar['start'] = trade['timestamp']
        current_bar['prices'].append(trade['price'])
        current_bar['volume'] += trade['volume']

        if current_bar['volume'] >= volume_per_bar:
            bars.append({
                'timestamp': current_bar['start'],
                'open': current_bar['prices'][0],
                'high': max(current_bar['prices']),
                'low': min(current_bar['prices']),
                'close': current_bar['prices'][-1],
                'volume': current_bar['volume']
            })
            current_bar = {'volume': 0, 'prices': [], 'start': None}

    return pd.DataFrame(bars)
```

### Dollar Bars
Sample every $N traded. Normalizes for price changes over time.

### Tick Bars
Sample every N trades.

**Marcos Lopez de Prado** recommends dollar/volume bars over time bars — they produce more uniform statistical properties (closer to IID).

## Data Sources

| Source | Coverage | Cost |
|---|---|---|
| **Yahoo Finance** | EOD, free | Free |
| **Alpha Vantage** | Intraday, limited | Free tier |
| **Polygon.io** | Tick-level US equities | $99-$199/mo |
| **Quandl/Nasdaq Data Link** | EOD + alternative data | Varies |
| **IEX Cloud** | US equities | $9-$499/mo |
| **LOBSTER** | Order book reconstructions | Academic |
| **Binance/Exchange APIs** | Crypto | Free |

---

**Related:** [[Market Microstructure MOC]] | [[Market Data Sources]] | [[Data Cleaning and Preprocessing]] | [[Feature Engineering for Trading]]
