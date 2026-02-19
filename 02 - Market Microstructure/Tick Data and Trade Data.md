# Tick Data and Trade Data

**Tick Data** is the highest possible resolution of market information. It records every individual event that occurs on an exchange, including price changes, trade executions, and order book updates.

---

## 1. The Data Hierarchy

| Level | Name | Description | Size |
|-------|------|-------------|------|
| **L1** | **Top of Book** | Best Bid, Best Ask, and the Last Trade. | Moderate |
| **L2** | **Market Depth** | Aggregated size at each price level (usually top 10-50 levels). | Large |
| **L3** | **Order Detail** | Individual order IDs, sizes, and timestamps. Essential for "Iceberg Sniffing." | Massive |

---

## 2. TAQ Data (Trades and Quotes)

The standard for US Equities research.
- **Quote Record:** Timestamp, Bid Price, Bid Size, Ask Price, Ask Size, Exchange.
- **Trade Record:** Timestamp, Execution Price, Execution Size, Sale Condition (e.g., "Regular" or "Intermarket Sweep").

---

## 3. Sampling: Moving Beyond Time-Bars

Traditional "Time Bars" (e.g., 1-minute candles) are suboptimal for quants because financial markets don't tick at regular time intervals. **Marcos Lopez de Prado** advocates for information-based sampling:

- **Tick Bars:** Sample every $N$ transactions. (Captures activity speed).
- **Volume Bars:** Sample every $N$ shares/contracts traded. (Synchronizes with market depth).
- **Dollar Bars:** Sample every $N$ dollars of value exchanged. (Normalizes for price changes).

**Benefit:** Information-based bars exhibit better statistical properties (closer to normal distribution, less heteroscedasticity).

---

## 4. Handling the Volume

Tick data for a single day of the S&P 500 can exceed 10GB of raw text.
- **Storage:** Use columnar formats like **Apache Parquet** or high-performance databases like **kdb+/q** (see [[Database Design for Trading]]).
- **Cleaning:** Must filter out "Outliers" (bad prints) and "Sale Conditions" that don't represent the true market price (e.g., late-reported trades).

---

## 5. Python: Simple Tick-to-Bar Aggregator

```python
import pandas as pd

def aggregate_volume_bars(ticks, volume_threshold):
    """
    ticks: DataFrame with ['price', 'volume']
    """
    ticks['cum_vol'] = ticks['volume'].cumsum()
    ticks['bar_id'] = (ticks['cum_vol'] / volume_threshold).astype(int)
    
    bars = ticks.groupby('bar_id').agg({
        'price': ['first', 'max', 'min', 'last'],
        'volume': 'sum',
        'timestamp': 'first'
    })
    return bars
```

---

## Related Notes
- [[Data Engineering MOC]] — Broader data context
- [[Market Data Sources]] — Where to get tick data
- [[Order Book Dynamics]] — The structure tick data describes
- [[Order Flow Analysis]] — Analyzing trade data
- [[High-Frequency Trading]] — The primary user of tick data
- [[Database Design for Trading]] — How to store this data
