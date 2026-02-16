# Modern Portfolio Theory (MPT)

> Harry Markowitz (1952) — Nobel Prize 1990

Modern Portfolio Theory is the foundation of quantitative portfolio management. It formalizes the tradeoff between risk and return using mean-variance optimization.

---

## Core Idea

**Investors are rational and risk-averse.** Given two portfolios with the same expected return, they prefer the one with lower risk. MPT finds the set of portfolios that maximize return for each level of risk.

---

## Mathematical Framework

### Single Asset
- Expected return: $E[R_i] = \mu_i$
- Risk: $\sigma_i = \sqrt{Var(R_i)}$

### Two-Asset Portfolio
For weights $w_1, w_2$ where $w_1 + w_2 = 1$:

$$E[R_p] = w_1 \mu_1 + w_2 \mu_2$$

$$\sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \rho_{12} \sigma_1 \sigma_2$$

**Key insight:** When $\rho_{12} < 1$, the portfolio risk is **less than** the weighted average of individual risks. This is the mathematical basis of diversification.

### N-Asset Portfolio
$$E[R_p] = \mathbf{w}^T \boldsymbol{\mu}$$
$$\sigma_p^2 = \mathbf{w}^T \Sigma \mathbf{w}$$

Where:
- $\mathbf{w}$ = weight vector $(n \times 1)$
- $\boldsymbol{\mu}$ = expected return vector $(n \times 1)$
- $\Sigma$ = covariance matrix $(n \times n)$

---

## The Efficient Frontier

The efficient frontier is the set of portfolios that offer the highest expected return for each level of risk.

```python
import numpy as np
from scipy.optimize import minimize

def efficient_frontier(mu, cov, n_points=100):
    """
    Compute the efficient frontier.

    Parameters:
        mu: Expected returns (n,)
        cov: Covariance matrix (n, n)
        n_points: Number of points on the frontier
    """
    n = len(mu)

    def portfolio_vol(w):
        return np.sqrt(w @ cov @ w)

    def portfolio_ret(w):
        return w @ mu

    # Find min and max return portfolios
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(0, 1)] * n  # Long-only

    # Minimum variance portfolio
    res_min = minimize(portfolio_vol, np.ones(n)/n,
                       bounds=bounds, constraints=constraints)
    min_ret = portfolio_ret(res_min.x)
    max_ret = max(mu)

    target_returns = np.linspace(min_ret, max_ret, n_points)
    efficient_vols = []
    efficient_weights = []

    for target in target_returns:
        cons = [
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - target}
        ]
        res = minimize(portfolio_vol, np.ones(n)/n,
                       bounds=bounds, constraints=cons)
        efficient_vols.append(portfolio_vol(res.x))
        efficient_weights.append(res.x)

    return target_returns, efficient_vols, efficient_weights
```

---

## The Tangency Portfolio (Maximum Sharpe)

The tangency portfolio is the point on the efficient frontier with the highest Sharpe ratio:

$$\max_{\mathbf{w}} \frac{\mathbf{w}^T \boldsymbol{\mu} - r_f}{\sqrt{\mathbf{w}^T \Sigma \mathbf{w}}}$$

**Analytical solution (unconstrained):**
$$\mathbf{w}^* = \frac{\Sigma^{-1}(\boldsymbol{\mu} - r_f \mathbf{1})}{\mathbf{1}^T \Sigma^{-1}(\boldsymbol{\mu} - r_f \mathbf{1})}$$

```python
def tangency_portfolio(mu, cov, rf=0.0):
    """Compute the maximum Sharpe ratio portfolio."""
    n = len(mu)
    excess_mu = mu - rf
    cov_inv = np.linalg.inv(cov)
    w = cov_inv @ excess_mu
    w = w / np.sum(w)  # Normalize to sum to 1
    return w
```

---

## Problems with MPT in Practice

| Problem | Description | Solution |
|---------|-------------|----------|
| **Estimation error** | Small changes in $\mu$ → huge weight changes | [[Black-Litterman Model]], shrinkage estimators |
| **Concentrated portfolios** | Optimizer exploits estimation errors | Position constraints, regularization |
| **Unstable covariance** | Covariance changes over time | Factor models, exponential weighting |
| **Single period** | Ignores multi-period dynamics | Dynamic programming, rebalancing rules |
| **Normal assumption** | Returns have fat tails | CVaR optimization, robust methods |
| **Transaction costs** | Ignores trading friction | Turnover constraints, [[Transaction Cost Analysis]] |

### The "Markowitz Curse"
> The more assets you have, the more estimation errors compound. With $n$ assets, you need to estimate $n$ returns, $n$ variances, and $\frac{n(n-1)}{2}$ covariances. For 500 stocks, that's **125,750** parameters.

**Practical solutions:**
1. **Shrinkage estimators** — Ledoit-Wolf shrinkage toward structured target
2. **Factor models** — Reduce dimensionality (see [[Factor Models]])
3. **Bayesian methods** — Incorporate prior beliefs (see [[Black-Litterman Model]])
4. **Robust optimization** — Optimize for the worst case within uncertainty set

---

## Implementation: Full Mean-Variance Optimizer

```python
import numpy as np
from scipy.optimize import minimize

class MeanVarianceOptimizer:
    def __init__(self, mu, cov, rf=0.0):
        self.mu = np.array(mu)
        self.cov = np.array(cov)
        self.rf = rf
        self.n = len(mu)

    def min_variance(self, long_only=True):
        """Minimum variance portfolio."""
        bounds = [(0, 1)] * self.n if long_only else [(-1, 1)] * self.n
        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]

        res = minimize(
            lambda w: w @ self.cov @ w,
            np.ones(self.n) / self.n,
            bounds=bounds,
            constraints=constraints
        )
        return res.x

    def max_sharpe(self, long_only=True):
        """Maximum Sharpe ratio portfolio."""
        bounds = [(0, 1)] * self.n if long_only else [(-1, 1)] * self.n
        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]

        def neg_sharpe(w):
            ret = w @ self.mu - self.rf
            vol = np.sqrt(w @ self.cov @ w)
            return -ret / vol if vol > 1e-10 else 0

        res = minimize(neg_sharpe, np.ones(self.n) / self.n,
                       bounds=bounds, constraints=constraints)
        return res.x

    def risk_parity(self):
        """Risk parity portfolio — equal risk contribution."""
        def risk_budget_obj(w):
            vol = np.sqrt(w @ self.cov @ w)
            marginal_risk = self.cov @ w
            risk_contrib = w * marginal_risk / vol
            target = vol / self.n
            return np.sum((risk_contrib - target) ** 2)

        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
        bounds = [(0.01, 1)] * self.n

        res = minimize(risk_budget_obj, np.ones(self.n) / self.n,
                       bounds=bounds, constraints=constraints)
        return res.x
```

---

## Key Takeaways for Quants

1. **MPT is the starting point, not the endpoint** — Every portfolio optimizer builds on Markowitz
2. **Garbage in, garbage out** — The optimizer is only as good as your return/risk estimates
3. **Constraints matter** — Real portfolios need position limits, sector limits, turnover limits
4. **Factor models reduce estimation error** — Don't estimate a full covariance matrix
5. **Rebalancing is part of the strategy** — Static optimization is not enough

---

## Related Notes
- [[Black-Litterman Model]] — Bayesian improvement on MPT
- [[Factor Models]] — Dimensionality reduction for covariance
- [[Portfolio Optimization]] — Beyond mean-variance
- [[Risk Management MOC]] — Risk constraints in optimization
- [[Linear Algebra in Finance]] — Matrix operations underlying MPT
- [[Optimization Methods]] — Solvers and algorithms
