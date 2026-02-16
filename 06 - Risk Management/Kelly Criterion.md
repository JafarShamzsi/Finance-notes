# Kelly Criterion

**The Kelly Criterion tells you the mathematically optimal fraction of your bankroll to bet on each opportunity to maximize long-term geometric growth. It comes from information theory (John Kelly, Bell Labs, 1956) and is one of the most powerful — and dangerous — tools in a quant's arsenal.**

---

## The Formula

### Binary Outcome (Simple)

```
f* = (p × b - q) / b

Where:
  f* = optimal fraction of capital to bet
  p = probability of winning
  q = 1 - p (probability of losing)
  b = ratio of win to loss (e.g., 2:1 means b=2)
```

**Example:** Strategy wins 55% of the time with 1:1 payoff.
```
f* = (0.55 × 1 - 0.45) / 1 = 0.10 → bet 10% of capital
```

### Continuous Case (Trading)

For normally distributed returns:

```
f* = μ / σ² = Sharpe² / (excess return)

Where:
  μ = expected excess return
  σ² = variance of returns
```

```python
def kelly_fraction(win_rate, win_loss_ratio):
    """Binary Kelly fraction."""
    p = win_rate
    q = 1 - p
    b = win_loss_ratio
    f = (p * b - q) / b
    return max(f, 0)

def kelly_continuous(expected_return, variance):
    """Continuous Kelly for normally distributed returns."""
    return expected_return / variance

def kelly_from_sharpe(sharpe_ratio, volatility):
    """Kelly leverage from Sharpe ratio."""
    return sharpe_ratio / volatility
```

### Multi-Asset Kelly

```python
def multi_asset_kelly(expected_returns, cov_matrix):
    """
    Optimal Kelly weights for multiple assets.
    f* = Σ^(-1) × μ
    """
    return np.linalg.solve(cov_matrix, expected_returns)
```

## Fractional Kelly

**Full Kelly is too aggressive for real trading.** Estimation errors in μ and σ make full Kelly dangerous.

| Fraction | Properties |
|---|---|
| Full Kelly (1.0) | Max growth, but extreme drawdowns (50%+) |
| **Half Kelly (0.5)** | **75% of max growth, much smaller drawdowns** |
| Quarter Kelly (0.25) | 50% of max growth, conservative |
| >1.0 Kelly | GUARANTEED RUIN in the long run |

```python
def fractional_kelly(full_kelly, fraction=0.5):
    """
    Half Kelly is the standard institutional practice.
    """
    return full_kelly * fraction
```

> **Practical wisdom:** Half Kelly gives you 75% of the growth rate with far less risk of ruin. Most institutional quants use quarter to half Kelly.

## Connection to Information Theory

Kelly maximizes the **expected log utility** of wealth:

```
E[log(W)] = p × log(1 + f×b) + q × log(1 - f)
```

This is equivalent to maximizing the **Shannon entropy** of the growth rate.

## Practical Limitations

1. **Edge estimation error** — You never know your true win rate or Sharpe precisely
2. **Non-stationarity** — Edge changes over time (alpha decay)
3. **Fat tails** — Kelly assumes known distributions; real markets have fatter tails
4. **Correlation** — Multi-asset Kelly requires accurate covariance estimation
5. **Drawdown tolerance** — Full Kelly produces drawdowns most humans can't stomach
6. **Leverage constraints** — Full Kelly may require leverage beyond what's available

## Bankroll Management

```python
def kelly_bankroll_simulation(win_rate, win_loss_ratio, kelly_fraction,
                               initial_capital=10000, n_trades=1000, n_sims=100):
    """Simulate bankroll evolution under Kelly sizing."""
    results = []
    for _ in range(n_sims):
        capital = initial_capital
        path = [capital]
        for _ in range(n_trades):
            bet = capital * kelly_fraction
            if np.random.random() < win_rate:
                capital += bet * win_loss_ratio
            else:
                capital -= bet
            path.append(max(capital, 0))
            if capital <= 0:
                break
        results.append(path)
    return results
```

---

**Related:** [[Risk Management MOC]] | [[Position Sizing]] | [[Drawdown Management]] | [[Probability and Statistics for Trading]] | [[Performance Metrics]]
