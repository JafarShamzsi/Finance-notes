# Transaction Cost Analysis (TCA)

**Transaction Cost Analysis (TCA)** is the systematic process of measuring and evaluating the efficiency of trade executions. In quantitative trading, where margins are often thin, TCA is the difference between a profitable strategy and a failing one.

---

## 1. Explicit vs. Implicit Costs

| Category | Cost Type | Definition |
|----------|-----------|------------|
| **Explicit** | Commissions | Fees paid to the broker. |
| **Explicit** | Exchange Fees | Fees for accessing the matching engine. |
| **Explicit** | Taxes/STT | Regulatory levies (e.g., Stamp Duty). |
| **Implicit** | Spread | The difference between Best Bid and Best Ask. |
| **Implicit** | Market Impact | The price movement caused by your own order. |
| **Implicit** | Opportunity Cost | The cost of unexecuted orders if the price moves away. |
| **Implicit** | Delay (Slippage) | Price movement between decision and arrival. |

---

## 2. Key Benchmarks for TCA

To measure if an execution was "good," we compare it to a benchmark price.

- **Arrival Price:** The mid-price at the moment the order was sent to the execution desk. (Best for [[Implementation Shortfall]]).
- **VWAP (Volume-Weighted Average Price):** The average price of all trades in the market during the execution window.
- **TWAP (Time-Weighted Average Price):** The average price of the asset over time.
- **Interval VWAP:** VWAP only during the specific time the order was active.
- **Close Price:** Comparing execution to the final price of the day (important for mutual funds).

---

## 3. Pre-Trade vs. Post-Trade Analysis

### Pre-Trade (The Prediction)
Estimating the expected cost *before* trading.
- **Input:** Order size, volatility, ADV (Average Daily Volume).
- **Model:** Square Root Law (see [[Market Impact Models]]).
- **Output:** "This 50k share order should cost roughly 12 basis points."

### Post-Trade (The Audit)
Measuring the actual cost *after* the trade is done.
- **Metric:** `Slippage (bps) = (Execution_Price - Benchmark_Price) / Benchmark_Price * 10000`.
- **Goal:** Compare `Actual Cost` vs. `Predicted Cost` to refine the pre-trade model.

---

## 4. Measuring Slippage Decay

A critical part of TCA is understanding the **Temporary vs. Permanent Impact** (see [[Market Impact Models]]).
- **T+0:** The price at execution.
- **T+30 min:** Does the price revert? (If yes, your impact was mostly temporary/liquidity-driven).
- **T+1 day:** Has the price stayed at the new level? (If yes, you had permanent impact/information leakage).

---

## 5. Broker & Venue Analysis

TCA allows a quant to rank different execution routes:
- **Broker A vs. Broker B:** Who provides better fills for small vs. large orders?
- **Dark Pools vs. Lit Exchanges:** Where is the adverse selection higher?
- **Algo A (VWAP) vs. Algo B (IS):** Which algorithm is better at capturing liquidity?

---

## 6. Python Implementation: Basic TCA Metric

```python
import pandas as pd

def calculate_tca_performance(executions, market_data):
    """
    Calculate slippage vs. Arrival and VWAP.
    
    Parameters:
        executions: DataFrame of your trades (Price, Quantity, Arrival_Time)
        market_data: Tick data or OHLCV for benchmarking
    """
    # 1. Arrival Price Slippage
    executions['arrival_price'] = market_data.asof(executions['arrival_time'])['mid']
    executions['is_bps'] = (executions['price'] - executions['arrival_price']) / \
                            executions['arrival_price'] * 10000 * executions['side_sign']
    
    # 2. Market VWAP (simplified)
    market_vwap = (market_data['price'] * market_data['volume']).sum() / \
                   market_data['volume'].sum()
    executions['vwap_slippage_bps'] = (executions['price'] - market_vwap) / \
                                       market_vwap * 10000 * executions['side_sign']
    
    return executions[['is_bps', 'vwap_slippage_bps']].mean()
```

---

## Related Notes
- [[Execution MOC]] — Parent section
- [[Implementation Shortfall]] — The "gold standard" benchmark
- [[Market Impact Models]] — Modeling the "why" behind TCA
- [[VWAP Algorithm]] — A common target benchmark
- [[TWAP Algorithm]] — A common target benchmark
- [[Order Book Dynamics]] — Microstructure level TCA
- [[High-Frequency Trading]] — TCA at the microsecond level
