# Position Sizing

**How much you bet matters more than what you bet on. Position sizing is the bridge between a good signal and a good P&L. Get it wrong and even a winning strategy will blow up.**

---

## Why Position Sizing Matters

```
Same Strategy, Different Sizing:
  Too small: 5% annual return (opportunity cost)
  Optimal:   25% annual return (Sharpe 2.0)
  Too large:  Ruin (account blown despite positive edge)
```

## Methods

### 1. Fixed Fractional (Percent Risk)

Risk a fixed percentage of capital per trade.

```python
def fixed_fractional_size(capital, risk_pct, entry, stop_loss):
    """
    risk_pct: e.g., 0.01 for 1% risk per trade
    """
    risk_per_share = abs(entry - stop_loss)
    dollar_risk = capital * risk_pct
    shares = int(dollar_risk / risk_per_share)
    return shares

# Example: $100K capital, 1% risk, buy at $50, stop at $48
# Risk per share = $2, Dollar risk = $1,000, Shares = 500
```

**Rule of thumb:** Risk 0.5%-2% of capital per trade.

### 2. Volatility-Based (ATR Method)

Size inversely proportional to volatility. Each position contributes equal risk.

```python
def volatility_position_size(capital, target_risk, price, atr, atr_multiplier=2):
    """
    Turtle Trading style: size by ATR.
    target_risk: fraction of capital (e.g., 0.01)
    """
    dollar_risk = capital * target_risk
    risk_per_unit = atr * atr_multiplier
    units = int(dollar_risk / (risk_per_unit * price / price))
    return units

def equal_risk_sizing(capital, target_vol, volatilities, prices):
    """
    Allocate so each position contributes equal volatility.
    """
    n = len(volatilities)
    per_position_vol = target_vol / n

    sizes = []
    for vol, price in zip(volatilities, prices):
        notional = capital * per_position_vol / vol
        shares = int(notional / price)
        sizes.append(shares)
    return sizes
```

### 3. Equal Risk Contribution

Each position contributes equally to portfolio variance.

```python
def equal_risk_contribution(cov_matrix, capital):
    from scipy.optimize import minimize

    n = cov_matrix.shape[0]

    def objective(w):
        port_vol = np.sqrt(w @ cov_matrix @ w)
        marginal = cov_matrix @ w
        risk_contrib = w * marginal / port_vol
        target = port_vol / n
        return np.sum((risk_contrib - target)**2)

    result = minimize(objective, np.ones(n)/n,
                     constraints={'type': 'eq', 'fun': lambda w: sum(w) - 1},
                     bounds=[(0.01, 1)] * n)

    return result.x * capital
```

### 4. Kelly Criterion

See [[Kelly Criterion]] for full treatment. Optimal for maximizing long-term growth.

### 5. Fixed Dollar

Simplest: same dollar amount per position. Ignores volatility.

## Comparison

| Method | Complexity | Risk Control | Best For |
|---|---|---|---|
| Fixed Fractional | Low | Good | Single-asset strategies |
| Volatility-Based | Medium | Excellent | Multi-asset, trend following |
| Equal Risk | Medium | Excellent | Balanced portfolios |
| Kelly | High | Theoretically optimal | When edge is well-estimated |
| Fixed Dollar | Lowest | Poor | Quick prototyping |

## Position Sizing Constraints

| Constraint | Rationale |
|---|---|
| Max 5% of capital per position | Prevent concentration risk |
| Max 25% per sector | Sector diversification |
| Max 2x leverage total | Limit gross exposure |
| Reduce size in drawdown | Protect surviving capital |
| Scale with strategy confidence | Higher conviction = larger size |

---

**Related:** [[Risk Management MOC]] | [[Kelly Criterion]] | [[Drawdown Management]] | [[Stop Loss Strategies]] | [[Trend Following]]
