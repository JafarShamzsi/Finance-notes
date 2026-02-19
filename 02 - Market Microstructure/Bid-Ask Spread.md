# Bid-Ask Spread

The **Bid-Ask Spread** is the difference between the highest price a buyer is willing to pay (Bid) and the lowest price a seller is willing to accept (Ask). It is the most fundamental cost of trading and serves as the primary revenue source for [[Market Making Strategies]].

---

## 1. Components of the Spread

In microstructure theory, the spread is not just "profit"; it is compensation for three distinct risks:

### A. Adverse Selection (The Information Risk)
Compensation for the risk of trading against someone with superior information (e.g., an insider or a faster quant). If a buyer is aggressive, they likely know the price is going up.
- See [[Order Flow Analysis]] for more on toxicity.

### B. Inventory Risk
The cost of holding an unwanted position. If a market maker buys 1,000 shares to provide liquidity, they are now "long" and exposed to market price drops.

### C. Order Processing Costs
The fixed costs of technology, exchange connectivity, and regulatory capital required to maintain a presence in the market.

---

## 2. Types of Spreads

- **Quoted Spread:** $Ask - Bid$ (The spread visible in the order book).
- **Effective Spread:** $2 \times |Price_{trade} - Midpoint|$. This accounts for trades that happen *inside* the spread (e.g., in a dark pool).
- **Realized Spread:** The profit a market maker actually keeps after the price moves (e.g., if they buy at the bid and the price immediately drops, their realized spread is negative).

---

## 3. Relative Spread (BPS)

For quants, comparing spreads across assets requires normalization.
$$\text{Relative Spread (bps)} = \frac{Ask - Bid}{Midpoint} \times 10,000$$

- **High Liquidity (SPY):** < 1 bps.
- **Moderate Liquidity (AAPL):** 1-2 bps.
- **Low Liquidity (Small Cap):** 20-100+ bps.

---

## 4. Python Implementation: Spread Analysis

```python
import pandas as pd

def calculate_spread_metrics(bids, asks, trades):
    """
    bids, asks: Series of best prices
    trades: Series of actual execution prices
    """
    midpoint = (asks + bids) / 2
    quoted_spread = asks - bids
    relative_spread_bps = (quoted_spread / midpoint) * 10000
    
    # Effective spread for a specific trade
    effective_spread = 2 * abs(trades - midpoint)
    
    return {
        'avg_quoted': quoted_spread.mean(),
        'avg_rel_bps': relative_spread_bps.mean(),
        'avg_effective': effective_spread.mean()
    }
```

---

## 5. Factors that Widen Spreads

1.  **High Volatility:** Uncertainty increases inventory risk.
2.  **Low Volume:** Fewer participants to compete on price.
3.  **Earnings/News Events:** High risk of adverse selection from informed traders.
4.  **Market Close:** Liquidity providers often "pull their quotes" to avoid overnight risk.

---

## Related Notes
- [[Market Microstructure MOC]] — Broader plumbing context
- [[Order Book Dynamics]] — Where the spread lives
- [[Liquidity]] — The relationship between depth and spread
- [[Market Making Strategies]] — Trading the spread
- [[Fees Commissions and Slippage]] — Spread as a cost
- [[Order Flow Analysis]] — Information content of the spread
