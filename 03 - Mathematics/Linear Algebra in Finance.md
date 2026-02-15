# Linear Algebra in Finance

Matrix operations are fundamental to portfolio optimization, factor models, risk management, and machine learning.

---

## Covariance Matrix

The foundation of portfolio risk:

```
Σ = Cov(R) where R is a vector of asset returns

Σᵢⱼ = Cov(Rᵢ, Rⱼ) = E[(Rᵢ - μᵢ)(Rⱼ - μⱼ)]

Portfolio variance: σ²_p = w'Σw
Where w = weight vector
```

```python
import numpy as np

def portfolio_risk(weights, cov_matrix):
    """Portfolio volatility from weights and covariance matrix."""
    return np.sqrt(weights @ cov_matrix @ weights)

# Shrinkage estimation (more stable)
from sklearn.covariance import LedoitWolf

def shrunk_covariance(returns_df):
    """Ledoit-Wolf shrinkage estimator for covariance."""
    lw = LedoitWolf().fit(returns_df.dropna())
    return pd.DataFrame(lw.covariance_,
                       index=returns_df.columns,
                       columns=returns_df.columns)
```

## Principal Component Analysis (PCA)

Decompose returns into orthogonal factors:

```python
from sklearn.decomposition import PCA

def returns_pca(returns_df, n_components=5):
    """
    Extract principal components from returns.
    PC1 ≈ Market factor (~40-50% of variance)
    PC2 ≈ Sector rotation (~10-15%)
    PC3+ ≈ More specific factors
    """
    pca = PCA(n_components=n_components)
    components = pca.fit_transform(returns_df.dropna())

    print("Explained variance ratios:")
    for i, ratio in enumerate(pca.explained_variance_ratio_):
        print(f"  PC{i+1}: {ratio:.1%}")

    return components, pca
```

**Applications:**
- Reduce dimensionality for [[Machine Learning Strategies]]
- Identify hidden risk factors
- Construct [[Factor Models]]
- [[Statistical Arbitrage]] — trade residuals after removing factors

## Eigenvalue Decomposition

```
Σ = QΛQ'

Where:
  Q = matrix of eigenvectors (principal directions)
  Λ = diagonal matrix of eigenvalues (variance in each direction)
```

**Random Matrix Theory (RMT):** Distinguish signal from noise in correlation matrices.

```python
def clean_correlation_matrix(returns_df):
    """Remove noise using Random Matrix Theory."""
    T, N = returns_df.shape
    corr = returns_df.corr().values
    eigenvalues, eigenvectors = np.linalg.eigh(corr)

    # Marchenko-Pastur bounds
    q = T / N
    lambda_plus = (1 + np.sqrt(1/q))**2

    # Zero out noise eigenvalues
    cleaned_eigenvalues = np.where(eigenvalues > lambda_plus, eigenvalues, 0)
    # Reconstruct
    cleaned_corr = eigenvectors @ np.diag(cleaned_eigenvalues) @ eigenvectors.T
    np.fill_diagonal(cleaned_corr, 1.0)

    return cleaned_corr
```

## Matrix Operations for Portfolio Optimization

See [[Portfolio Optimization]] for full treatment.

```python
def mean_variance_optimal(expected_returns, cov_matrix, target_return=None):
    """
    Markowitz mean-variance optimization.
    """
    from scipy.optimize import minimize

    n = len(expected_returns)

    def portfolio_vol(w):
        return np.sqrt(w @ cov_matrix @ w)

    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # Weights sum to 1
    ]
    if target_return:
        constraints.append(
            {'type': 'eq', 'fun': lambda w: w @ expected_returns - target_return}
        )

    bounds = [(0, 1)] * n  # Long only

    result = minimize(portfolio_vol, np.ones(n)/n,
                     method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x
```

---

**Related:** [[Mathematics MOC]] | [[Portfolio Optimization]] | [[Factor Models]] | [[Machine Learning Strategies]] | [[Probability and Statistics for Trading]]
