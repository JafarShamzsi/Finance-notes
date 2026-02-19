# Value at Risk (VaR)

**VaR answers: "What is the maximum loss I can expect over a given time horizon at a given confidence level?" It's the single most widely used risk metric in finance — required by regulators and used by every trading desk.**

---

## Definition

```
VaR(α, t) = the loss level that is exceeded with probability (1-α) over horizon t

Example: 1-day 95% VaR of $1M means:
  "There is a 5% chance of losing more than $1M tomorrow"
```

## Three Methods

### 1. Historical VaR

Use actual historical returns. No distribution assumptions.

```python
import numpy as np
import pandas as pd

def historical_var(returns, confidence=0.95, horizon=1):
    """
    Non-parametric VaR from historical returns.
    """
    if horizon > 1:
        # Scale returns to horizon (rolling sum for overlapping)
        returns = returns.rolling(horizon).sum().dropna()

    var = np.percentile(returns, (1 - confidence) * 100)
    cvar = returns[returns <= var].mean()

    return {'VaR': var, 'CVaR': cvar, 'method': 'Historical'}
```

### 2. Parametric (Variance-Covariance) VaR

Assume normal distribution. Fast but underestimates tail risk.

```
VaR = μ - z_α × σ × √t

Where:
  μ = mean return (often assumed 0 for short horizons)
  z_α = z-score for confidence (1.645 for 95%, 2.326 for 99%)
  σ = standard deviation of returns
  t = time horizon in days
```

```python
from scipy.stats import norm

def parametric_var(returns, confidence=0.95, horizon=1):
    mu = returns.mean() * horizon
    sigma = returns.std() * np.sqrt(horizon)
    z = norm.ppf(1 - confidence)

    var = -(mu + z * sigma)
    cvar = -(mu - sigma * norm.pdf(z) / (1 - confidence))

    return {'VaR': var, 'CVaR': cvar, 'method': 'Parametric'}
```

### 3. Monte Carlo VaR

Simulate paths. Most flexible — can handle non-linear portfolios.

```python
def monte_carlo_var(returns_df, weights, confidence=0.95,
                    horizon=1, n_sims=10000):
    mu = returns_df.mean().values
    cov = returns_df.cov().values

    sim_returns = np.random.multivariate_normal(
        mu * horizon, cov * horizon, n_sims)
    port_returns = sim_returns @ weights

    var = np.percentile(port_returns, (1 - confidence) * 100)
    cvar = port_returns[port_returns <= var].mean()

    return {'VaR': -var, 'CVaR': -cvar, 'method': 'Monte Carlo'}
```

## Expected Shortfall (CVaR)

VaR only tells you the threshold — CVaR tells you the **average loss beyond VaR**.

```
CVaR = E[Loss | Loss > VaR]
```

CVaR is a **coherent risk measure** (VaR is not). Basel III requires banks to use Expected Shortfall.

## Method Comparison

| Method | Pros | Cons | Best For |
|---|---|---|---|
| **Historical** | No assumptions, captures fat tails | Needs long history, backward-looking | Linear portfolios |
| **Parametric** | Fast, analytical | Assumes normality, misses tails | Quick estimates |
| **Monte Carlo** | Flexible, handles non-linearity | Slow, model-dependent | Options, complex portfolios |

## Limitations of VaR

1. **Not coherent** — VaR of combined portfolio can exceed sum of individual VaRs
2. **Ignores tail shape** — Two portfolios with same VaR can have very different tail risks
3. **Assumes stationarity** — Past volatility may not predict future
4. **Confidence level arbitrary** — 95% vs 99% gives very different pictures
5. **Horizon dependent** — √t scaling assumes independent returns

## 4. Extreme Value Theory (EVT) (Peaks Over Threshold)

Standard historical VaR is limited by the sample size. EVT fits a distribution (Generalized Pareto Distribution - GPD) to the *tail* of the data only, allowing for more accurate estimation of extreme events (e.g., 99.9% VaR).

$$F_u(y) = P(X - u \le y | X > u) \approx G_{\xi, \beta}(y)$$

Where $\xi$ is the tail index (shape parameter). If $\xi > 0$, the distribution has fat tails (Frechet).

---

## 5. Cornish-Fisher Expansion (Modified VaR)

Adjusts the parametric Normal VaR for **Skewness ($S$)** and **Kurtosis ($K$)**.
- Assets with negative skew and high kurtosis have higher Modified VaR than Normal VaR.

$$z_{CF} = z_{\alpha} + \frac{1}{6}(z_{\alpha}^2 - 1)S + \frac{1}{24}(z_{\alpha}^3 - 3z_{\alpha})K - \frac{1}{36}(2z_{\alpha}^3 - 5z_{\alpha})S^2$$

Then: $\text{mVaR} = -(\mu + z_{CF} \cdot \sigma)$

---

## Component VaR (Risk Budgeting)

Decomposes the portfolio VaR into contributions from each asset.
- **Marginal VaR ($\Delta$VaR):** The change in VaR for a $1 increase in position size.
- **Component VaR (CVaR):** Position Size $\times$ Marginal VaR.
- **Property:** Sum of Component VaRs = Total Portfolio VaR (Euler's Theorem).

$$ \text{MVaR}_i = \frac{\partial \text{VaR}_p}{\partial w_i} = z_{\alpha} \frac{\text{Cov}(r_i, r_p)}{\sigma_p} $$

This tells a risk manager: "If we sell asset $i$, how much does our risk decrease?"

---

## Basel Requirements

| Framework | Risk Measure | Confidence | Horizon |
|---|---|---|---|
| Basel II | VaR | 99% | 10-day |
| Basel III / FRTB | Expected Shortfall | 97.5% | Varies by liquidity |

---

**Related:** [[Risk Management MOC]] | [[Monte Carlo Simulation]] | [[Probability and Statistics for Trading]] | [[Tail Risk and Black Swans]] | [[Performance Metrics]]
