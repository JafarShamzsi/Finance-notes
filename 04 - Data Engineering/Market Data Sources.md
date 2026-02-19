# Market Data Sources

Selecting the right data source is a tradeoff between **latency**, **accuracy**, **history depth**, and **cost**. A quant needs different sources for backtesting (long history) vs. live trading (low latency).

---

## 1. Professional Data Terminals

Used by J.P. Morgan, Bloomberg, and top-tier hedge funds.
- **Bloomberg Terminal:** The industry standard. Unmatched for fundamentals, news, and fixed-income data.
- **Refinitiv (Eikon/LSEG):** Bloomberg's main competitor. Strong in FX and macro data.
- **FactSet:** Excellent for equity research and portfolio attribution.

---

## 2. API-First Data Vendors (Quant Favorites)

| Vendor | Best For | Data Resolution |
|--------|----------|-----------------|
| **Polygon.io** | US Equities & Options. | Tick-level, Real-time & Historical. |
| **Nasdaq Data Link** | Institutional Alternative Data. | EOD, Fundamental, and specialized. |
| **IEX Cloud** | US Equities (Low cost). | Intraday & EOD. |
| **Alpha Vantage** | Multi-asset (Retail/Hobbyist). | 1-min intervals. |
| **Databento** | HFT-grade Futures & Equities. | Nanosecond tick-by-tick. |

---

## 3. Backtesting Data (Survivorship-Bias Free)

For serious backtesting, you cannot use "Current S&P 500" lists.
- **Norgate Data:** The "Gold Standard" for retail/pro quants. Provides clean, adjusted, survivorship-bias-free data for US/AU/CA markets.
- **CRSP (Chicago):** The academic standard for US historical equity data.

---

## 4. Crypto Data Sources

- **CCXT Library:** A Python library that connects to 100+ exchanges (Binance, Coinbase, Kraken) with a unified API.
- **CoinMetrics / Glassnode:** Institutional-grade on-chain data (Wallet flows, Hash rates).
- **Kaiko:** High-quality tick data for centralized and decentralized exchanges.

---

## 5. Economic & Macro Data

- **FRED (St. Louis Fed):** 800,000+ free economic time series (GDP, CPI, Unemployment).
- **EDGAR (SEC):** Raw corporate filings (10-K, 10-Q) for [[Natural Language Processing (NLP)|NLP analysis]].

---

## 6. Data Quality Checklist

Before using a new source, verify:
- [ ] **Adjustments:** Are prices adjusted for stock splits and dividends?
- [ ] **Point-in-Time:** Does the database reflect what was known *at that moment*?
- [ ] **Gaps:** Are there missing minutes or days in the middle of the history?
- [ ] **Timestamps:** Are timestamps in UTC or local exchange time?

---

## Related Notes
- [[Data Engineering MOC]] — Managing the ingested data
- [[Alternative Data]] — Beyond price/volume
- [[Tick Data and Trade Data]] — Nature of the data resolved
- [[Survivorship Bias]] — Why the source matters
- [[Database Design for Trading]] — Storing the data
- [[Python Code MOC]] — Using `yfinance` and `ccxt`
