# Execution Map of Content

> *"Ideas are cheap. Execution is everything."* — Execution determines how much of your alpha you keep.

Trade execution bridges the gap between portfolio decisions and market reality. Poor execution can destroy a profitable strategy.

---

## The Execution Problem

You want to buy 100,000 shares of AAPL. If you send a single market order:
- You'll walk up the order book, paying worse and worse prices
- Other algos will detect your buying and front-run you
- Your own buying will push the price up (**market impact**)
- You might pay 50+ bps more than the current price

**Solution:** Execution algorithms that slice your order and spread it over time/venues.

---

## Core Concepts
- [[Execution Venues]] — Where orders get matched (exchanges, dark pools, internalizers)
- [[Order Routing]] — How orders flow from you to venues
- [[Smart Order Routing]] — Algorithmic routing across fragmented venues
- [[Transaction Cost Analysis]] — Measuring execution quality
- [[Market Impact Models]] — Predicting and minimizing price impact
- [[Implementation Shortfall]] — Gap between paper portfolio and real portfolio

---

## Execution Algorithms
- [[TWAP Algorithm]] — Time-Weighted Average Price
- [[VWAP Algorithm]] — Volume-Weighted Average Price
- [[Iceberg Orders]] — Hidden quantity orders
- [[Implementation Shortfall]] — Minimize total execution cost

### Algorithm Comparison

| Algorithm | Objective | Best For | Market Impact |
|-----------|-----------|----------|---------------|
| **TWAP** | Minimize time risk | Illiquid stocks, uniform urgency | Medium |
| **VWAP** | Match volume profile | Benchmark tracking | Low-Medium |
| **IS (Shortfall)** | Minimize total cost | Urgent trades, large alpha | Adaptive |
| **Iceberg** | Hide size | Very large orders | Low |
| **POV** | Match participation rate | Passive execution | Low |
| **Sniper** | Sweep dark pools | Hidden liquidity capture | Variable |

---

## Execution Cost Breakdown

```
Total Cost = Spread Cost + Market Impact + Timing Risk + Opportunity Cost

Spread:        ~1-5 bps (half the bid-ask spread)
Market Impact:  ~1-50 bps (depends on size and urgency)
Timing Risk:    ~1-10 bps (price moves while you trade slowly)
Opportunity:    Variable (cost of not getting filled at all)

Key insight: Impact and timing risk are inversely related.
            Trade fast → high impact, low timing risk
            Trade slow → low impact, high timing risk
```

---

## The Almgren-Chriss Framework

The foundational model for optimal execution (2000):

$$\min_{x_t} \quad E[\text{Cost}] + \lambda \cdot \text{Var}[\text{Cost}]$$

**Optimal trajectory** balances:
- **Temporary impact** — Immediate cost of trading (proportional to trading rate)
- **Permanent impact** — Lasting price change from information leakage
- **Timing risk** — Variance of cost from holding inventory

Result: Exponential decay trajectory. More urgent trades front-load execution.

---

## High-Frequency Trading
- [[High-Frequency Trading]] — HFT strategies and characteristics
- [[High-Frequency Trading Infrastructure]] — Technology stack for HFT

---

## Key Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Arrival Price Slippage** | Fill price - arrival price | < 5 bps |
| **VWAP Slippage** | Avg fill - VWAP | < 2 bps |
| **Implementation Shortfall** | Paper return - real return | Minimize |
| **Participation Rate** | My volume / total volume | 5-20% |
| **Fill Rate** | Filled qty / total qty | > 95% |

---

## Related Areas
- [[Market Microstructure MOC]] — Understanding the venues you trade on
- [[Regulation and Compliance MOC]] — Best execution requirements, Reg NMS
- [[Risk Management MOC]] — Execution risk management
- [[Infrastructure MOC]] — Systems that power execution
- [[Strategies MOC]] — Strategies that generate execution orders
- [[Portfolio Rebalancing]] — Generating rebalancing trade lists
