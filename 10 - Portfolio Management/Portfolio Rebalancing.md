# Portfolio Rebalancing

Rebalancing is the process of bringing portfolio weights back to target allocations. Without rebalancing, winner assets dominate and the portfolio drifts from its intended risk profile.

---

## Why Rebalance?

1. **Risk control** — Drift increases concentration risk
2. **Contrarian alpha** — Sell winners, buy losers (mean reversion at portfolio level)
3. **Factor exposure maintenance** — Keep factor tilts on target
4. **Mandate compliance** — Institutional mandates require staying within bands

---

## Rebalancing Approaches

### 1. Calendar Rebalancing
Rebalance on a fixed schedule (daily, weekly, monthly, quarterly).

| Frequency | Turnover | Cost | Tracking Error |
|-----------|----------|------|----------------|
| Daily | High | High | Very low |
| Weekly | Medium | Medium | Low |
| Monthly | Low-Medium | Low-Medium | Medium |
| Quarterly | Low | Low | Higher |

**Best for:** Index funds, pension funds, low-frequency strategies.

### 2. Threshold Rebalancing
Rebalance when any weight drifts beyond a band (e.g., +/- 5% of target).

```python
def threshold_rebalance(current_weights, target_weights, threshold=0.05):
    """
    Check if rebalancing is needed based on drift threshold.

    Parameters:
        current_weights: Current portfolio weights
        target_weights: Target portfolio weights
        threshold: Maximum allowed drift (e.g., 0.05 = 5%)

    Returns:
        trades: Required weight changes, or None if no rebalance needed
    """
    drift = current_weights - target_weights
    max_drift = np.max(np.abs(drift))

    if max_drift > threshold:
        return target_weights - current_weights  # Trades needed
    return None  # No rebalance needed
```

**Best for:** Tax-efficient portfolios, cost-sensitive strategies.

### 3. Optimal Rebalancing (Cost-Aware)
Minimize a utility function that trades off tracking error against transaction costs:

$$\min_{\mathbf{w}} \quad \lambda (\mathbf{w} - \mathbf{w}^*)^T \Sigma (\mathbf{w} - \mathbf{w}^*) + \sum_i c_i |w_i - w_i^{current}|$$

Where:
- First term = tracking error vs. target
- Second term = transaction costs of rebalancing
- $\lambda$ = tradeoff parameter

```python
from scipy.optimize import minimize

def optimal_rebalance(current_w, target_w, cov, costs, lam=1.0):
    """
    Cost-aware rebalancing optimizer.

    Parameters:
        current_w: Current weights
        target_w: Target weights
        cov: Covariance matrix
        costs: Per-asset transaction cost (proportional)
        lam: Tracking error penalty
    """
    n = len(current_w)

    def objective(w):
        # Tracking error vs. target
        diff = w - target_w
        te = lam * diff @ cov @ diff
        # Transaction costs
        tc = np.sum(costs * np.abs(w - current_w))
        return te + tc

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1)] * n

    res = minimize(objective, current_w, bounds=bounds, constraints=constraints)
    return res.x
```

**Best for:** Institutional portfolios, high-cost environments.

---

## Rebalancing and Transaction Costs

The **rebalancing premium** is the excess return from systematically selling high and buying low. But it must overcome:

| Cost Type | Typical Size | Mitigation |
|-----------|-------------|------------|
| Commissions | 0.1-1 bps | Negotiate, use dark pools |
| Spread | 1-10 bps | Limit orders, patient execution |
| Market impact | 1-50 bps | TWAP/VWAP, slice orders |
| Tax | 15-37% of gains | Tax-loss harvesting, long-term holding |

**Rule of thumb:** Rebalancing is worth it when expected tracking error cost > expected transaction cost.

---

## Tax-Loss Harvesting

For taxable accounts, rebalancing creates an opportunity:

1. Sell losing positions to realize losses (tax deduction)
2. Replace with correlated substitute (maintain exposure)
3. Wait 30 days before buying back original (wash sale rule)

```
If AAPL is down → Sell AAPL, buy QQQ or MSFT temporarily
After 30 days → Sell substitute, buy AAPL back
Tax benefit: Realized loss offsets capital gains
```

---

## Institutional Rebalancing Framework

At JPM/Bloomberg scale:

```
Daily:
  ├── Check drift vs. target
  ├── Flag breached thresholds
  └── Generate trade list

Weekly:
  ├── Review factor exposures
  ├── Check risk limits
  └── Rebalance if needed

Monthly:
  ├── Full portfolio review
  ├── Reoptimize weights
  └── Factor exposure rebalancing

Quarterly:
  ├── Strategic review
  ├── Universe changes
  └── Benchmark reconstitution
```

---

## Related Notes
- [[Modern Portfolio Theory]] — Target weights from optimization
- [[Transaction Cost Analysis]] — Measuring rebalancing costs
- [[Execution MOC]] — How to execute rebalancing trades
- [[VWAP Algorithm]] — Execution algorithm for rebalancing
- [[Risk Management MOC]] — Risk limits that trigger rebalancing
- [[Portfolio Management MOC]] — Parent note
