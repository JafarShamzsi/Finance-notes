# Data Engineering — Map of Content

> Garbage in, garbage out. Data quality is the foundation of every successful trading system.

---

## Topics
- [[Market Data Sources]] — Where to get data
- [[Alternative Data]] — Non-traditional data sources for alpha
- [[Data Cleaning and Preprocessing]] — Handling the mess
- [[Feature Engineering for Trading]] — Turning raw data into signals
- [[Database Design for Trading]] — Storage and retrieval
- [[Real-Time Data Pipelines]] — Live data infrastructure

## Data Pipeline Architecture

```
Sources → Ingestion → Cleaning → Storage → Feature Engineering → Model/Strategy
  ↓          ↓           ↓         ↓              ↓                    ↓
APIs      Websockets  Validation  TimescaleDB  Rolling calcs      Signals
Feeds     REST polls  Dedup       Arctic       Technical ind.     Orders
Files     FTP         Gap fill    Parquet      Normalization      Execution
```

---

**Related:** [[Trading Algorithms Master Index]] | [[Tick Data and Trade Data]] | [[Infrastructure MOC]]
