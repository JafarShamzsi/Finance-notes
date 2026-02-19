# Linear Algebra in Finance

Linear algebra is the "workhorse" of quantitative finance. It is the language of risk, diversification, and machine learning.

---

## 1. Covariance Matrix ($\Sigma$)

The cornerstone of modern portfolio theory. For a vector of returns $\mathbf{r} \in \mathbb{R}^n$:

$$\Sigma = E[(\mathbf{r} - \boldsymbol{\mu})(\mathbf{r} - \boldsymbol{\mu})^T]$$

- **Properties:** Symmetric, positive semi-definite (PSD).
- **Portfolio Variance:** $\sigma_p^2 = \mathbf{w}^T \Sigma \mathbf{w}$.
- **Positive Definiteness:** If $\Sigma$ is not positive definite, it implies one or more assets are perfectly correlated or the sample size is too small ($n > T$).

---

## 2. Eigenvalue Decomposition

Every symmetric matrix $\Sigma$ can be decomposed:

$$\Sigma = Q \Lambda Q^T$$

- **Eigenvectors ($Q$):** The "Principal Components" (see below).
- **Eigenvalues ($\Lambda$):** The variance explained by each principal component.

### Random Matrix Theory (RMT)
Financial correlation matrices are often "noisy."
- **Marchenko-Pastur Law:** Defines the distribution of eigenvalues for a random matrix.
- **Cleaning:** Eigenvalues that fall within the Marchenko-Pastur "bulk" are likely noise and should be filtered or "shrunk."

---

## 3. Principal Component Analysis (PCA)

PCA is the primary way to decompose the drivers of an asset universe.
- **PC1 (The Market):** Typically captures 40-50% of the variance (the "Beta" factor).
- **PC2 (Sector/Style):** Often captures industry-wide moves.
- **PC3+ (The Residuals):** Asset-specific idiosyncratic noise.

**Application in Fixed Income:**
PCA on the yield curve consistently identifies three components:
1.  **Level:** Parallel shift (all rates move together).
2.  **Slope:** Flattening or steepening.
3.  **Curvature:** Changes in the hump of the curve.

---

## 4. Singular Value Decomposition (SVD)

The generalization of eigenvalue decomposition for any matrix $A \in \mathbb{R}^{m \times n}$:

$$A = U \Sigma V^T$$

- **Usage:** Factor models, noise reduction, and latent semantic analysis in [[Natural Language Processing (NLP)]].

---

## 5. Cholesky Decomposition

Factorizes a symmetric, PSD matrix $\Sigma$ into a lower triangular matrix $L$:

$$\Sigma = L L^T$$

**Critical for Monte Carlo Simulation:**
To generate correlated random returns $\mathbf{r}$:
1.  Generate uncorrelated normal variables $\mathbf{z} \sim N(0, I)$.
2.  Transform them: $\mathbf{r} = \boldsymbol{\mu} + L \mathbf{z}$.
3.  The resulting $\mathbf{r}$ will have the desired covariance $\Sigma$.

```python
import numpy as np

# Generate correlated returns
mu = np.array([0.05, 0.08])
cov = np.array([[0.04, 0.02], [0.02, 0.09]])

L = np.linalg.cholesky(cov)
z = np.random.standard_normal(2)
r = mu + L @ z
```

---

## 6. Matrix Operations for Factor Models

$$R = F B + \epsilon$$

- $R$: Asset returns ($T \times n$).
- $F$: Factor returns ($T \times k$).
- $B$: Factor loadings ($k \times n$).
- $\epsilon$: Idiosyncratic returns ($T \times n$).

Finding $B$ via OLS: $B = (F^T F)^{-1} F^T R$.

---

## Related Notes
- [[Mathematics MOC]] — Parent section
- [[Modern Portfolio Theory]] — Application of covariance
- [[Factor Models]] — Core linear algebra application
- [[Portfolio Optimization]] — Matrix inversion and quadratic programming
- [[Monte Carlo Simulation]] — Using Cholesky decomposition
- [[Stochastic Calculus]] — Connection to multi-variate GBM
