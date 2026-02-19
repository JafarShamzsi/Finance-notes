# Database Design for Trading

In quantitative finance, the database is more than just storage; it is a critical infrastructure component for low-latency retrieval, backtesting at scale, and real-time signal generation.

---

## 1. Key Database Paradigms

| Type | Best For | Popular Technologies |
|------|----------|----------------------|
| **Relational (SQL)** | Metadata, configuration, trade history. | PostgreSQL, MySQL. |
| **Time-Series (TSDB)** | Tick data, OHLCV, market indicators. | TimescaleDB, InfluxDB. |
| **Columnar** | Large-scale backtesting, aggregation. | kdb+/q, ClickHouse, Apache Parquet. |
| **Binary Storage** | Compressed tick-level archives. | Arctic (Man Group), HDF5. |

---

## 2. Industry Standard: kdb+/q

The gold standard in Tier-1 banks and high-frequency shops.
- **In-memory speed:** Processes millions of rows per second.
- **q Language:** Vector-based language optimized for time-series arithmetic.
- **Disk Format:** Stores data in columnar format, allowing for high compression and fast reads on specific columns (e.g., just the 'Price').

```q
/ q example: calculate VWAP for a specific ticker
select vwap:size wavg price by sym from trade where sym=`AAPL
```

---

## 3. TimescaleDB (PostgreSQL Extension)

Ideal for shops that want the power of SQL with time-series optimizations.
- **Hypertables:** Automatically partitions data by time.
- **Continuous Aggregates:** Pre-calculates OHLCV bars from tick data in the background.
- **Compression:** Can achieve 90%+ compression on older data using columnar storage.

---

## 4. Arctic (Man Group / Open Source)

A high-performance data store for financial data, built on top of MongoDB.
- **Pandas Native:** Designed specifically for storing and retrieving DataFrames.
- **Versioning:** Allows you to see exactly what the data looked like at a specific point in time (crucial for reproducible backtesting).

---

## 5. Design Considerations for Quants

### Partitioning & Sharding
- **Time-based:** Partition data by Day or Month (PostgreSQL `PARTITION BY RANGE`).
- **Ticker-based:** Sharding data by asset class or ticker to parallelize reads.

### Compression
- Use **Delta Encoding** or **Double-Delta Encoding** (like Gorilla/TSX) for prices and timestamps.
- Columnar storage (Parquet) is superior for analytical queries (e.g., "What was the mean vol across all 500 stocks?").

### Data Integrity & Gap Filling
- **As-of Joins:** Joining a trade table with a quote table to find the *last known* quote at the time of the trade.
- **Forward Filling:** Handling missing ticks during illiquid periods.

---

## Related Notes
- [[Data Engineering MOC]] — Parent section
- [[Tick Data and Trade Data]] — Nature of the data stored
- [[Infrastructure MOC]] — Broader system design
- [[Real-Time Data Pipelines]] — Ingestion into the database
- [[Backtesting Framework Design]] — Retrieving data for testing
