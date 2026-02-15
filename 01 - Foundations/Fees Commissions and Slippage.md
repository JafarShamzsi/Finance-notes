# Fees, Commissions, and Slippage

The difference between a profitable and unprofitable strategy is often **transaction costs**. Many backtested strategies that look great fail live because costs weren't modeled correctly.

---

## Types of Trading Costs

### 1. Explicit Costs

| Cost | Description | Typical Range |
|---|---|---|
| **Commission** | Broker fee per trade | $0-$0.005/share (equities), $0.50-$2.50/contract (futures) |
| **Exchange fees** | Per-share/contract to exchange | $0.001-$0.003/share |
| **Regulatory fees** | SEC, TAF fees | ~$0.00008/share |
| **Data fees** | Real-time market data subscriptions | $10-$500+/month |
| **Platform fees** | Software/API access | Varies |

### 2. Implicit Costs

| Cost | Description | Impact |
|---|---|---|
| **Spread** | [[Bid-Ask Spread]] cost of crossing | Half-spread per side = full spread round-trip |
| **Slippage** | Difference between expected and fill price | 0.01%-0.10% per trade |
| **Market Impact** | Price movement caused by your order (see [[Market Impact]]) | Scales with order size |
| **Opportunity Cost** | Missed fills on limit orders | Hard to measure |
| **Delay Cost** | Price moves while waiting to execute | Scales with latency |

## Modeling Total Cost

```
Total Cost = Commission + Spread + Slippage + Market Impact

Per-trade cost = C + S/2 + α·σ·√(Q/ADV)

Where:
  C = commission per share
  S = bid-ask spread
  α = market impact coefficient
  σ = volatility
  Q = order quantity
  ADV = average daily volume
```

### Round-Trip Example (100 shares of $50 stock)

| Component | Cost |
|---|---|
| Commission | $0 (commission-free broker) |
| Spread ($0.02) | $2.00 (half-spread × 2 sides × 100 shares) |
| Slippage (~1 cent) | $2.00 |
| **Total Round-Trip** | **$4.00 = 0.04% of $10,000** |

For a strategy making 0.10% per trade, costs eat 40% of gross profit.

## Cost Impact by Strategy Type

| Strategy | Trades/Day | Cost Sensitivity | Break-Even Alpha |
|---|---|---|---|
| [[High-Frequency Trading]] | 10,000+ | EXTREME | 0.001% per trade |
| [[Market Making Strategies]] | 1,000+ | Very High | Spread - costs > 0 |
| Intraday [[Momentum Strategies]] | 10-50 | High | ~0.05% per trade |
| Daily [[Mean Reversion Strategies]] | 1-10 | Medium | ~0.10% per trade |
| Weekly [[Trend Following]] | 0.5-2 | Low | ~0.50% per trade |

## Reducing Costs

1. **Use limit orders** instead of market orders → avoid spread
2. **Trade liquid instruments** → tighter spreads (see [[Liquidity]])
3. **Break up large orders** → reduce [[Market Impact]] (see [[TWAP Algorithm]], [[VWAP Algorithm]])
4. **Negotiate broker rates** → volume discounts
5. **Choose maker fee structures** → get rebates
6. **Optimize execution timing** → trade during high-volume periods
7. **Use [[Smart Order Routing]]** → find best prices across venues

## Backtesting Transaction Costs

**CRITICAL:** Always include realistic costs in backtests (see [[Backtesting Framework Design]])

```python
# Realistic cost model for backtesting
def estimate_trade_cost(price, quantity, adv, spread_bps=5):
    """
    Estimate total one-way trade cost.

    Args:
        price: Current price
        quantity: Shares to trade
        adv: Average daily volume
        spread_bps: Bid-ask spread in basis points

    Returns:
        Total estimated cost in dollars
    """
    commission = 0.001 * quantity  # $0.001/share
    half_spread = price * (spread_bps / 10000) / 2 * quantity

    # Market impact (square root model)
    participation = quantity / adv
    impact = 0.1 * price * (participation ** 0.5) * quantity

    return commission + half_spread + impact
```

---

**Related:** [[Bid-Ask Spread]] | [[Market Impact]] | [[Transaction Cost Analysis]] | [[Performance Metrics]] | [[Backtesting Framework Design]]
