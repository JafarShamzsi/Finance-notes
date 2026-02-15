# Market Microstructure — Map of Content

> How markets actually work at the mechanical level. Understanding microstructure separates profitable algos from money-losing ones.

---

## Core Topics
- [[Order Book Dynamics]] — How buy/sell orders are organized and matched
- [[Bid-Ask Spread]] — The cost of immediacy
- [[Price Discovery]] — How markets find the "right" price
- [[Market Impact]] — How your orders move prices
- [[Liquidity]] — How easily you can trade without moving prices
- [[Tick Data and Trade Data]] — The finest granularity of market data

## Key Concepts

### Information Asymmetry
Some traders know more than others. The spread exists partly to compensate market makers for trading against informed traders.

### Price Formation
```
Trade → Information incorporated → New price → New quotes
         ↑                                        ↓
         └────────── Feedback loop ───────────────┘
```

### Market Quality Metrics
| Metric | Measures | Good Value |
|---|---|---|
| Spread | Cost of trading | Tight |
| Depth | Size available at best prices | Deep |
| Resilience | Recovery speed after large trade | Fast |
| Volatility | Price uncertainty | Moderate |

## Theoretical Models

| Model | Key Insight |
|---|---|
| **Kyle (1985)** | Informed trader's profit = f(market depth) |
| **Glosten-Milgrom (1985)** | Spread = f(adverse selection probability) |
| **Avellaneda-Stoikov (2008)** | Optimal market making quotes |
| **Almgren-Chriss (2000)** | Optimal execution with market impact |

---

**Related:** [[Trading Algorithms Master Index]] | [[Market Making Strategies]] | [[High-Frequency Trading]] | [[Execution MOC]]
