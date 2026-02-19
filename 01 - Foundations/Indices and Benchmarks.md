# Indices and Benchmarks

Indices are statistical measures of the performance of a specific segment of the financial market. For a quant, indices serve two primary purposes: they are **tradable instruments** (via ETFs and Futures) and they are **performance benchmarks** for evaluating alpha.

---

## 1. Major Equity Indices

| Index | Type | Methodology | Description |
|-------|------|-------------|-------------|
| **S&P 500** | Large-Cap | Market-Cap Weighted | 500 largest US public companies. The "Market" baseline. |
| **NASDAQ 100** | Tech/Growth | Market-Cap Weighted | 100 largest non-financial stocks on NASDAQ. |
| **Russell 2000** | Small-Cap | Market-Cap Weighted | Bottom 2,000 stocks of the Russell 3000. |
| **MSCI World** | Global | Market-Cap Weighted | Developed market stocks across 23 countries. |
| **DJIA** | Blue-Chip | **Price Weighted** | 30 major US companies (archaic weighting method). |

---

## 2. Weighting Methodologies

The way an index is calculated significantly affects its risk/return profile and how it should be used as a benchmark.

- **Market-Cap Weighted:** Weights are proportional to the total value of outstanding shares ($Price 	imes Shares$). Dominates by winners. (e.g., S&P 500).
- **Equal Weighted:** Every stock gets the same weight ($1/N$). Provides more exposure to small-cap and value factors.
- **Price Weighted:** Weights are proportional to the price per share. Arbitrary and rarely used in modern quant finance (except for Dow Jones).
- **Fundamental Weighted:** Weights based on earnings, dividends, or book value (Smart Beta).

---

## 3. Index Rebalancing (The "Index Effect")

Indices are reconstituted periodically (quarterly or semi-annually).
- **Additions:** Stocks being added to an index see massive buying pressure from passive funds (ETFs).
- **Deletions:** Stocks being removed see massive selling pressure.
- **Quant Opportunity:** Anticipating rebalancing events to profit from the temporary supply/demand imbalance (see [[Event-Driven Strategies]]).

---

## 4. Benchmarking Performance

To determine if a strategy has **Alpha**, its return must be compared to a relevant benchmark.

- **Beta ($\beta$):** The sensitivity of the strategy to the benchmark.
- **Tracking Error:** The standard deviation of the difference between strategy and benchmark returns.
- **Information Ratio:** Alpha divided by Tracking Error.

**Example:** A technology-focused strategy should be benchmarked against the NASDAQ 100 (QQQ), not the S&P 500 (SPY), to isolate the true managerial skill from sector exposure.

---

## 5. Tradability: ETFs and Futures

Quants rarely trade the index "cash" directly. They use:
- **ETFs (Exchange Traded Funds):** e.g., SPY, IVV, VOO.
- **Index Futures:** e.g., E-mini S&P 500 (ES), Micro E-mini (MES).
- **Index Options:** e.g., SPX options.

Futures are often preferred by quants due to **leverage** and **capital efficiency**.

---

## Related Notes
- [[Asset Classes]] — Equities context
- [[Survivorship Bias]] — How index constituents change over time
- [[Alpha Research]] — Benchmarking alpha
- [[Event-Driven Strategies]] — Rebalancing arbitrage
- [[Factor Models]] — Indices as factor proxies
