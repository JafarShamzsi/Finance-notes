# Factor Models

Factor models decompose asset returns into systematic risk factors, reducing the dimensionality of the covariance estimation problem and enabling better portfolio construction.

---

## Why Factor Models?

**The problem:** Estimating a full $n \times n$ covariance matrix for 500 stocks requires 125,750 parameters. Factor models reduce this to a manageable number.

**The insight:** Most of the co-movement between stocks is driven by a small number of common factors. Individual stock risk is mostly idiosyncratic.

---

## The General Factor Model

$$R_i = \alpha_i + \beta_{i1} F_1 + \beta_{i2} F_2 + ... + \beta_{ik} F_k + \epsilon_i$$

Where:
- $R_i$ = return of asset $i$
- $\alpha_i$ = asset-specific return (alpha)
- $\beta_{ij}$ = sensitivity of asset $i$ to factor $j$ (factor loading)
- $F_j$ = return of factor $j$
- $\epsilon_i$ = idiosyncratic return ($E[\epsilon_i \epsilon_j] = 0$ for $i \neq j$)

**Covariance structure:**
$$\Sigma = B \Sigma_F B^T + D$$

Where:
- $B$ = factor loading matrix $(n \times k)$
- $\Sigma_F$ = factor covariance matrix $(k \times k)$
- $D$ = diagonal idiosyncratic variance matrix $(n \times n)$

---

## Types of Factor Models

### 1. CAPM (Single Factor)
$$R_i - R_f = \alpha_i + \beta_i (R_m - R_f) + \epsilon_i$$

- One factor: the market
- $\beta_i$ = market beta

### 2. Fama-French Three-Factor Model (1993)
$$R_i - R_f = \alpha_i + \beta_1 MKT + \beta_2 SMB + \beta_3 HML + \epsilon_i$$

| Factor | Name | Long | Short |
|--------|------|------|-------|
| MKT | Market | Market portfolio | Risk-free rate |
| SMB | Size | Small caps | Large caps |
| HML | Value | High book/market | Low book/market |

### 3. Fama-French Five-Factor Model (2015)
Adds:
| Factor | Name | Long | Short |
|--------|------|------|-------|
| RMW | Profitability | Robust profitability | Weak profitability |
| CMA | Investment | Conservative investment | Aggressive investment |

### 4. Carhart Four-Factor Model (1997)
Fama-French 3 + Momentum:
| Factor | Name | Long | Short |
|--------|------|------|-------|
| UMD | Momentum | Past winners (12-1 month) | Past losers (12-1 month) |

### 5. Statistical Factors (PCA)
Extract factors directly from return data using Principal Component Analysis:
- No economic interpretation required
- First few PCs capture most variance
- Used by Barra, Axioma, Bloomberg risk models

### 6. Bloomberg/Barra Risk Model Factors
Production risk models used at JPM, Goldman, etc.:

**Style Factors:** Momentum, Value, Size, Volatility, Quality, Growth, Leverage, Liquidity, Beta, Earnings Yield, Dividend Yield

**Industry Factors:** 30-60 industry classifications (GICS sectors/industries)

**Country Factors:** For global portfolios

---

## Implementation

```python
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression

class FactorModel:
    def __init__(self, returns, factor_returns=None, n_factors=5):
        """
        Parameters:
            returns: Asset returns (T x n)
            factor_returns: Known factor returns (T x k). If None, use PCA.
            n_factors: Number of PCA factors if factor_returns is None.
        """
        self.returns = np.array(returns)
        self.T, self.n = self.returns.shape

        if factor_returns is not None:
            self.factors = np.array(factor_returns)
            self.k = self.factors.shape[1]
            self._fit_regression()
        else:
            self.k = n_factors
            self._fit_pca()

    def _fit_pca(self):
        """Extract statistical factors using PCA."""
        pca = PCA(n_components=self.k)
        self.factors = pca.fit_transform(self.returns)
        self.loadings = pca.components_.T  # (n x k)
        self.explained_variance = pca.explained_variance_ratio_

        # Compute idiosyncratic variance
        predicted = self.returns @ self.loadings @ np.linalg.pinv(self.loadings)
        residuals = self.returns - predicted
        self.idio_var = np.var(residuals, axis=0)

    def _fit_regression(self):
        """Fit factor loadings via cross-sectional regression."""
        self.loadings = np.zeros((self.n, self.k))
        self.alphas = np.zeros(self.n)
        residuals = np.zeros_like(self.returns)

        for i in range(self.n):
            reg = LinearRegression().fit(self.factors, self.returns[:, i])
            self.loadings[i] = reg.coef_
            self.alphas[i] = reg.intercept_
            residuals[:, i] = self.returns[:, i] - reg.predict(self.factors)

        self.idio_var = np.var(residuals, axis=0)

    def covariance_matrix(self):
        """Compute factor-model covariance matrix: B * Sigma_F * B' + D"""
        factor_cov = np.cov(self.factors.T)
        if factor_cov.ndim == 0:
            factor_cov = np.array([[factor_cov]])

        systematic = self.loadings @ factor_cov @ self.loadings.T
        idiosyncratic = np.diag(self.idio_var)

        return systematic + idiosyncratic

    def risk_decomposition(self, weights):
        """
        Decompose portfolio risk into factor and specific risk.

        Returns:
            total_var, factor_var, specific_var, factor_contributions
        """
        w = np.array(weights)
        factor_cov = np.cov(self.factors.T)
        if factor_cov.ndim == 0:
            factor_cov = np.array([[factor_cov]])

        # Factor risk
        factor_exposure = self.loadings.T @ w  # (k,)
        factor_var = factor_exposure @ factor_cov @ factor_exposure

        # Specific risk
        specific_var = w @ np.diag(self.idio_var) @ w

        # Total risk
        total_var = factor_var + specific_var

        # Factor contributions
        factor_marginal = factor_cov @ factor_exposure
        factor_contributions = factor_exposure * factor_marginal / factor_var

        return {
            'total_risk': np.sqrt(total_var),
            'factor_risk': np.sqrt(factor_var),
            'specific_risk': np.sqrt(specific_var),
            'pct_factor': factor_var / total_var,
            'pct_specific': specific_var / total_var,
            'factor_contributions': factor_contributions
        }
```

---

## Factor Investing: Smart Beta

Factor investing = systematically harvesting factor risk premia.

| Factor | Annual Premium | Sharpe | Capacity | Crash Risk |
|--------|---------------|--------|----------|------------|
| **Value** | 3-5% | 0.3-0.5 | Very high | Value traps |
| **Momentum** | 5-8% | 0.4-0.7 | Medium | Momentum crashes |
| **Size** | 2-3% | 0.2-0.3 | Low | Liquidity crises |
| **Quality** | 3-5% | 0.4-0.6 | Very high | Low |
| **Low Volatility** | 2-4% | 0.3-0.5 | High | Rising rates |
| **Carry** | 3-5% | 0.4-0.6 | High | Risk-off events |

---

## Practical Considerations at Institutional Level

1. **Barra/Axioma models** are the industry standard — Bloomberg PORT, MSCI Barra
2. **Factor exposures change** — Reestimate regularly (monthly or quarterly)
3. **Factor crowding** — When everyone owns the same factors, the premium shrinks
4. **Factor timing** — Controversial, but some evidence for value/momentum timing
5. **Multi-factor portfolios** — Combine factors for smoother returns (diversification of alpha)

---

## Related Notes
- [[Modern Portfolio Theory]] — Factor models improve MPT estimation
- [[Black-Litterman Model]] — Use factor views in BL
- [[Portfolio Optimization]] — Factor-based optimization
- [[Linear Algebra in Finance]] — PCA and matrix decomposition
- [[Statistical Arbitrage]] — Factor-neutral strategies
- [[Performance Attribution]] — Factor-based attribution
