# Risk Parity

Risk parity allocates capital so that each asset (or asset class) contributes **equally to portfolio risk**, rather than equal capital allocation. Pioneered by Ray Dalio's Bridgewater Associates with the All Weather fund, risk parity has become one of the most important [[Portfolio Management MOC|portfolio construction]] frameworks.

---

## Core Idea

**Traditional 60/40 portfolio problem:**
- 60% equities, 40% bonds by capital
- But ~90% of risk comes from equities (vol ~16% vs bonds ~5%)
- Not truly diversified — it's an equity-risk portfolio with a bond garnish

**Risk parity solution:**
- Equalize **risk contribution** from each asset class
- Bonds get more capital (lower vol), equities less
- Use leverage to hit target return

---

## Mathematical Framework

### Risk Contribution

For a portfolio with weights $w$ and covariance matrix $\Sigma$:

**Portfolio variance:**
$$\sigma_p^2 = w^T \Sigma w$$

**Marginal risk contribution of asset $i$:**
$$MRC_i = \frac{\partial \sigma_p}{\partial w_i} = \frac{(\Sigma w)_i}{\sigma_p}$$

**Total risk contribution of asset $i$:**
$$RC_i = w_i \times MRC_i = \frac{w_i (\Sigma w)_i}{\sigma_p}$$

**Risk parity condition:**
$$RC_i = RC_j \quad \forall \, i, j$$

Or equivalently:
$$w_i (\Sigma w)_i = \frac{\sigma_p^2}{n} \quad \forall \, i$$

---

## Solving for Risk Parity Weights

### Method 1: Analytical (Equal Vol, No Correlation)
If assets are uncorrelated:
$$w_i \propto \frac{1}{\sigma_i}$$

Simple inverse-volatility weighting. A reasonable approximation.

### Method 2: Numerical Optimization (General Case)

```python
import numpy as np
from scipy.optimize import minimize

def risk_parity_weights(cov_matrix, risk_budget=None):
    """
    Compute risk parity portfolio weights.

    Parameters:
        cov_matrix: np.array (n × n) covariance matrix
        risk_budget: np.array of target risk contributions (default: equal)

    Returns:
        Optimal weights (sum to 1)
    """
    n = cov_matrix.shape[0]
    if risk_budget is None:
        risk_budget = np.ones(n) / n

    def objective(w):
        """Minimize sum of squared differences from target risk contributions."""
        port_vol = np.sqrt(w @ cov_matrix @ w)
        risk_contrib = w * (cov_matrix @ w) / port_vol
        # Difference from target
        target = risk_budget * port_vol
        return np.sum((risk_contrib - target)**2)

    # Constraints: weights sum to 1, all positive
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    bounds = [(0.01, None) for _ in range(n)]  # Min 1% per asset
    x0 = np.ones(n) / n

    result = minimize(objective, x0, method='SLSQP',
                      bounds=bounds, constraints=constraints)
    return result.x


def risk_contributions(weights, cov_matrix):
    """Compute risk contribution of each asset."""
    port_vol = np.sqrt(weights @ cov_matrix @ weights)
    marginal = cov_matrix @ weights / port_vol
    rc = weights * marginal
    rc_pct = rc / port_vol  # As percentage of total risk
    return {
        'risk_contribution': rc,
        'risk_contribution_pct': rc_pct,
        'portfolio_vol': port_vol
    }
```

### Method 3: Spinu's Analytical Solution (2013)
For the equal risk contribution case, solve:
$$w_i = \frac{(\Sigma^{-1} \mathbf{1})_i}{\mathbf{1}^T \Sigma^{-1} \mathbf{1}} \times \text{scaling}$$

Then iterate with Newton's method for exact risk parity.

---

## Bridgewater's All Weather Portfolio

### Philosophy
- Markets have 4 environments: **Growth Up/Down** × **Inflation Up/Down**
- Allocate 25% risk to each environment
- Each environment has assets that perform well in it

### Typical Allocation (Risk Budget)

| Environment | Assets | Risk Allocation |
|-------------|--------|----------------|
| Growth Up | Equities, Corporate Bonds, Commodities | 25% |
| Growth Down | Nominal Bonds, TIPS | 25% |
| Inflation Up | TIPS, Commodities, EM Bonds | 25% |
| Inflation Down | Nominal Bonds, Equities | 25% |

### Simplified All Weather Weights (Capital)

| Asset Class | Approximate Weight | Risk Contribution |
|------------|-------------------|-------------------|
| Long-Term Treasuries | 40% | ~25% |
| Intermediate Treasuries | 15% | ~10% |
| Equities (S&P 500) | 30% | ~40% (over-contributes) |
| Commodities (diversified) | 7.5% | ~12.5% |
| Gold | 7.5% | ~12.5% |

**Note:** True risk parity with leverage targets 10-12% vol by leveraging the bond allocation.

---

## Leverage in Risk Parity

### Why Leverage?
Risk parity naturally underweights high-return/high-vol assets (equities) and overweights low-return/low-vol assets (bonds). Without leverage, the portfolio return is low.

**Solution:** Leverage the entire portfolio to hit a target return/vol:

$$w_{\text{leveraged}} = \frac{\sigma_{\text{target}}}{\sigma_{\text{RP}}} \times w_{\text{RP}}$$

### Leverage Implementation
```python
def leveraged_risk_parity(cov_matrix, target_vol=0.10, risk_budget=None):
    """
    Risk parity with leverage to hit target volatility.

    Parameters:
        cov_matrix: Covariance matrix
        target_vol: Target annualized volatility
        risk_budget: Risk allocation per asset

    Returns:
        Leveraged weights (may sum > 1)
    """
    base_weights = risk_parity_weights(cov_matrix, risk_budget)
    base_vol = np.sqrt(base_weights @ cov_matrix @ base_weights)

    leverage = target_vol / base_vol
    leveraged_weights = base_weights * leverage

    return {
        'weights': leveraged_weights,
        'leverage': leverage,
        'gross_exposure': np.sum(leveraged_weights),
        'portfolio_vol': target_vol
    }
```

### Leverage Risks
- **Borrowing costs** eat into returns
- **Margin calls** during crises (2020 March, 2022 rates)
- **Correlation spikes** — all assets fall together, leverage amplifies losses
- **Liquidity risk** — forced deleveraging at worst time

---

## Risk Parity vs Alternatives

| Approach | Equities Weight | Bond Weight | Vol | Sharpe | Tail Risk |
|----------|----------------|-------------|-----|--------|-----------|
| **60/40** | 60% | 40% | ~10% | ~0.4 | High (equity-driven) |
| **Risk Parity (unlev)** | ~20% | ~55% | ~5% | ~0.5 | Low |
| **Risk Parity (lev)** | ~30% | ~80% | ~10% | ~0.6 | Medium |
| **Max Sharpe** | Variable | Variable | ~10% | ~0.5 | Medium-High |
| **Min Variance** | Low | High | ~6% | ~0.4 | Low |

---

## Criticisms and Limitations

1. **Interest rate sensitivity:** Heavy bond allocation means rates rising destroys the portfolio (2022 was brutal)
2. **Leverage dependency:** Returns depend on cheap borrowing
3. **Assumes stable correlations:** Stock-bond correlation flipped positive in 2022
4. **Crowding:** Massive AUM in risk parity creates crowded trades
5. **Backward-looking vol estimates:** Past vol may not predict future vol

### The 2022 Problem
- Stocks AND bonds fell simultaneously
- Stock-bond correlation turned positive
- Risk parity funds drew down 15-25%
- Key lesson: diversification across **economic regimes** matters more than across asset classes

---

## Related Notes
- [[Portfolio Optimization]] — Mean-variance, HRP, and other methods
- [[Modern Portfolio Theory]] — MPT foundation
- [[Portfolio Rebalancing]] — Maintaining risk parity over time
- [[Correlation and Diversification]] — Why diversification fails in crises
- [[Position Sizing]] — Risk-based sizing at strategy level
- [[Value at Risk (VaR)]] — Measuring portfolio risk
- [[Factor Models]] — Factor-based risk decomposition
- [[Portfolio Management MOC]] — Parent section
