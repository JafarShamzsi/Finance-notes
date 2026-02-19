# Transaction Cost Analysis (TCA)

**Transaction Cost Analysis (TCA)** is the rigorous quantitative process of auditing execution quality. In institutional trading, TCA is used to ensure "Best Execution" compliance and to refine the parameters of execution algorithms like [[VWAP Algorithm]] and [[Implementation Shortfall]].

---

## 1. The Four Components of Execution Cost

TCA decomposes the total cost of a trade into manageable pieces:

### A. Delay Cost (Slippage)
The price movement between the time the Portfolio Manager (PM) makes the decision and the time the order is received by the market.
$$\text{Delay Cost} = P_{\text{arrival}} - P_{\text{decision}}$$

### B. Execution Cost (Market Impact)
The movement in price caused by your own trading activity.
$$\text{Execution Cost} = P_{\text{average\_fill}} - P_{\text{arrival}}$$

### C. Opportunity Cost
The "missed profit" from shares that were never filled because the price moved away.
$$\text{Opportunity Cost} = (Q_{\text{total}} - Q_{\text{filled}}) \times (P_{\text{final}} - P_{\text{decision}})$$

### D. Explicit Costs
Fixed, transparent costs.
- Commissions, Exchange Fees, Taxes (STT).

---

## 2. Pre-Trade vs. Post-Trade TCA

### Pre-Trade Analysis (Predictive)
Before the trade, estimate the expected cost using historical volatility and liquidity.
- **Goal:** Set realistic expectations and choose the right algorithm (e.g., "This order will cost 15bps, use VWAP").

### Post-Trade Analysis (Descriptive)
After the trade, compare actual fills to benchmarks.
- **Goal:** Grade the broker or algorithm and identify "bad fills."

---

## 3. Key Benchmarks for Quants

| Benchmark | Definition | Use Case |
|-----------|------------|----------|
| **Arrival Price** | Mid-price at the start of trading. | Measuring urgent execution. |
| **VWAP** | Volume-weighted average of all trades. | Measuring passive, index-like execution. |
| **PWP** | Participation-Weighted Price. | Adjusting for your own participation rate. |
| **Reversion** | Price 30 mins after your trade. | Detecting if you had permanent market impact. |

---

## 4. Python Implementation: Basic Slippage Audit

```python
def calculate_slippage_bps(avg_fill, benchmark_price, side):
    """
    Calculates slippage in basis points.
    Positive value = bad slippage (cost).
    Negative value = price improvement.
    """
    sign = 1 if side == 'buy' else -1
    slippage = (avg_fill - benchmark_price) / benchmark_price
    return slippage * 10000 * sign

# Example
fill = 150.05
arrival = 150.00
print(f"Slippage: {calculate_slippage_bps(fill, arrival, 'buy'):.2f} bps")
# Output: 3.33 bps cost
```

---

## 5. The Feedback Loop

The ultimate goal of TCA is a **Continuous Feedback Loop**:
1.  **Analyze** previous trades to find patterns (e.g., "Broker X has high slippage at the market open").
2.  **Adjust** your [[Smart Order Routing]] logic to avoid those conditions.
3.  **Monitor** the next set of trades to verify improvement.

---

## Related Notes
- [[Execution MOC]] — Broader execution context
- [[Implementation Shortfall]] — The primary IS metric
- [[VWAP Algorithm]] — Typical target benchmark
- [[Market Impact Models]] — Modeling the "Execution Cost" piece
- [[Trading Sessions and Hours]] — Context for intraday cost variation
- [[Transaction Cost Models]] — Higher-level theoretical models
