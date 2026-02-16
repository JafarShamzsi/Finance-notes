# Portfolio Optimization

Beyond Markowitz mean-variance, modern portfolio optimization uses robust methods, alternative risk measures, and practical constraints to build real-world portfolios.

---

## The Optimization Problem

$$\max_{\mathbf{w}} \quad U(\mathbf{w}) = f(\text{return}) - g(\text{risk}) - h(\text{cost})$$

Subject to:
- $\sum w_i = 1$ (full investment)
- $w_i \geq 0$ (long-only, if applicable)
- Sector/position/turnover constraints

---

## Optimization Methods

### 1. Mean-Variance (Markowitz)
$$\max_{\mathbf{w}} \quad \mathbf{w}^T \boldsymbol{\mu} - \frac{\delta}{2} \mathbf{w}^T \Sigma \mathbf{w}$$

See [[Modern Portfolio Theory]] for details.

### 2. Minimum Variance
$$\min_{\mathbf{w}} \quad \mathbf{w}^T \Sigma \mathbf{w}$$

- No return estimates needed (only covariance)
- Surprisingly good out-of-sample performance
- Tends to overweight low-volatility assets

### 3. Risk Parity
Each asset contributes equally to portfolio risk:

$$RC_i = w_i \cdot \frac{(\Sigma \mathbf{w})_i}{\sqrt{\mathbf{w}^T \Sigma \mathbf{w}}} = \frac{\sigma_p}{n} \quad \forall i$$

- Used by Bridgewater's All Weather fund
- Naturally diversified
- Often requires leverage to meet return targets

### 4. Maximum Diversification
$$\max_{\mathbf{w}} \quad DR = \frac{\mathbf{w}^T \boldsymbol{\sigma}}{\sqrt{\mathbf{w}^T \Sigma \mathbf{w}}}$$

Where $\boldsymbol{\sigma}$ = vector of individual asset volatilities.
- Diversification ratio > 1 means diversification benefits exist
- Maximizes the gap between weighted-average vol and portfolio vol

### 5. CVaR Optimization (Conditional Value at Risk)
$$\min_{\mathbf{w}} \quad CVaR_\alpha(\mathbf{w}) = E[L | L > VaR_\alpha]$$

- Coherent risk measure (unlike VaR)
- Captures tail risk
- Linear programming formulation (Rockafellar & Uryasev, 2000)

### 6. Hierarchical Risk Parity (HRP)
ML-based method by Marcos López de Prado (2016):

1. Compute distance matrix from correlations
2. Hierarchical clustering (dendrogram)
3. Quasi-diagonalize covariance matrix
4. Recursive bisection to allocate weights

```python
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import squareform

def hierarchical_risk_parity(cov, corr):
    """
    Hierarchical Risk Parity (López de Prado, 2016).

    Parameters:
        cov: Covariance matrix
        corr: Correlation matrix
    """
    n = cov.shape[0]

    # Step 1: Distance matrix
    dist = np.sqrt(0.5 * (1 - corr))
    condensed_dist = squareform(dist)

    # Step 2: Hierarchical clustering
    link = linkage(condensed_dist, method='single')
    sort_order = leaves_list(link)

    # Step 3: Quasi-diagonalize
    cov_sorted = cov[np.ix_(sort_order, sort_order)]

    # Step 4: Recursive bisection
    weights = np.ones(n)

    def recursive_bisect(items, cov_matrix):
        if len(items) <= 1:
            return
        mid = len(items) // 2
        left = items[:mid]
        right = items[mid:]

        # Variance of each cluster (inverse-variance allocation)
        left_var = _cluster_var(left, cov_matrix)
        right_var = _cluster_var(right, cov_matrix)

        alpha = 1 - left_var / (left_var + right_var)

        for i in left:
            weights[i] *= alpha
        for i in right:
            weights[i] *= (1 - alpha)

        recursive_bisect(left, cov_matrix)
        recursive_bisect(right, cov_matrix)

    def _cluster_var(items, cov_matrix):
        sub_cov = cov_matrix[np.ix_(items, items)]
        w = 1 / np.diag(sub_cov)  # Inverse variance
        w /= w.sum()
        return w @ sub_cov @ w

    recursive_bisect(list(range(n)), cov_sorted)

    # Unsort
    final_weights = np.zeros(n)
    for i, orig_idx in enumerate(sort_order):
        final_weights[orig_idx] = weights[i]

    return final_weights / final_weights.sum()
```

**Advantages:**
- No matrix inversion (numerically stable)
- Works well with noisy covariance estimates
- No need for expected returns
- Naturally diversified

---

## Practical Constraints

Real portfolio optimization includes:

```python
# Position limits
w_min <= w_i <= w_max  # e.g., 0% to 5%

# Sector limits
sum(w_i for i in sector) <= sector_max  # e.g., 25%

# Turnover constraint
sum(|w_i - w_i_old|) <= max_turnover  # e.g., 20% monthly

# Factor exposure limits
factor_min <= B.T @ w <= factor_max  # e.g., beta between 0.9 and 1.1

# Number of holdings
count(w_i > 0) <= max_holdings  # e.g., 100 stocks

# Tracking error
sqrt((w - w_bench).T @ cov @ (w - w_bench)) <= max_TE  # e.g., 3%
```

---

## Comparison of Methods

| Method | Needs Returns? | Needs Cov? | Robust? | Diversified? | Complexity |
|--------|---------------|-----------|---------|-------------|------------|
| Mean-Variance | Yes | Yes | Low | Variable | Low |
| Min Variance | No | Yes | Medium | Low-vol bias | Low |
| Risk Parity | No | Yes | High | High | Medium |
| Max Diversification | No | Yes | Medium | Very high | Medium |
| CVaR | Yes | Simulated | Medium | Variable | High |
| HRP | No | Yes | Very high | High | Medium |
| Black-Litterman | Views | Yes | High | Variable | High |

---

## Related Notes
- [[Modern Portfolio Theory]] — Classical mean-variance framework
- [[Black-Litterman Model]] — Bayesian return estimation
- [[Factor Models]] — Structured covariance estimation
- [[Optimization Methods]] — Numerical solvers
- [[Risk Management MOC]] — Risk constraints
- [[Portfolio Management MOC]] — Parent note
