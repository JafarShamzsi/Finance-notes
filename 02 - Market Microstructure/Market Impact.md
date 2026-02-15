# Market Impact

When you trade, you move the price against yourself. Understanding and minimizing market impact is critical for profitable execution.

---

## Types of Market Impact

### Temporary Impact
Price displacement that reverts after your trading stops.
- Caused by consuming [[Liquidity]] in the [[Order Book Dynamics|order book]]
- Reverts as market makers replenish quotes

### Permanent Impact
Price change that persists — the market learned from your trade.
- Your trade revealed information to the market
- This is the "cost of alpha"

```
Total Impact = Temporary + Permanent
```

## Square Root Model (Almgren-Chriss)

The most widely used impact model:

```
Impact = σ × η × (Q / ADV)^0.5

Where:
  σ = daily volatility
  η = impact coefficient (~0.1 - 0.5)
  Q = order quantity (shares)
  ADV = average daily volume
```

**Key insight:** Impact scales with the **square root** of order size, not linearly.

```python
def estimate_market_impact(price, quantity, adv, volatility,
                           eta=0.3, impact_exponent=0.5):
    """
    Estimate market impact in dollars.
    """
    participation_rate = quantity / adv
    impact_bps = eta * volatility * 10000 * (participation_rate ** impact_exponent)
    impact_dollars = price * (impact_bps / 10000) * quantity
    return impact_bps, impact_dollars
```

## Minimizing Market Impact

| Technique | How | Reference |
|---|---|---|
| **Break up orders** | Trade over time | [[TWAP Algorithm]], [[VWAP Algorithm]] |
| **Use limit orders** | Don't cross the spread | [[Order Types and Execution]] |
| **Dark pools** | Hide from the market | [[Smart Order Routing]] |
| **Iceberg orders** | Only show partial size | [[Iceberg Orders]] |
| **Trade at close** | Join the closing auction | High liquidity |
| **Reduce position size** | Smaller orders = less impact | [[Position Sizing]] |

## Almgren-Chriss Optimal Execution

Minimize the combined cost of market impact and timing risk:

```python
def almgren_chriss_trajectory(Q, T, n_intervals, sigma, eta, lambda_risk):
    """
    Optimal execution trajectory.

    Q: Total shares to trade
    T: Time horizon
    n_intervals: Number of trading intervals
    sigma: Volatility
    eta: Temporary impact parameter
    lambda_risk: Risk aversion
    """
    tau = T / n_intervals
    kappa = np.sqrt(lambda_risk * sigma**2 / eta)

    # Optimal trajectory
    times = np.linspace(0, T, n_intervals + 1)
    trajectory = Q * np.sinh(kappa * (T - times)) / np.sinh(kappa * T)

    # Trade list (how much to trade each interval)
    trades = -np.diff(trajectory)

    return trajectory, trades
```

---

**Related:** [[Market Microstructure MOC]] | [[TWAP Algorithm]] | [[VWAP Algorithm]] | [[Implementation Shortfall]] | [[Transaction Cost Analysis]]
