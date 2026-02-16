# Copulas

Copulas separate the dependence structure of random variables from their marginal distributions. In finance, they model how assets move together — especially in the tails — going far beyond [[Correlation and Diversification|linear correlation]].

---

## Why Copulas?

**Correlation is not enough:**
- Correlation measures linear dependence only
- Two assets can have the same correlation but very different joint tail behavior
- In crashes, correlations spike to 1 — copulas model this **tail dependence**

The 2008 crisis was partly caused by misuse of Gaussian copulas for CDO pricing (David Li's formula), which assumed no tail dependence.

---

## Sklar's Theorem (Foundation)

For any joint distribution $F(x_1, ..., x_n)$ with marginals $F_1(x_1), ..., F_n(x_n)$:

$$F(x_1, ..., x_n) = C(F_1(x_1), ..., F_n(x_n))$$

Where $C: [0,1]^n \to [0,1]$ is the **copula** — it links marginals to the joint distribution.

**Key insight:** You can model marginals separately (e.g., each asset's return distribution) and then join them with a copula.

---

## Common Copula Families

### 1. Gaussian Copula

$$C_{\Sigma}^{\text{Gauss}}(u_1, ..., u_n) = \Phi_{\Sigma}(\Phi^{-1}(u_1), ..., \Phi^{-1}(u_n))$$

| Property | Value |
|----------|-------|
| Parameter | Correlation matrix $\Sigma$ |
| Tail dependence | **None** (zero in both tails) |
| Use case | Baseline, easy to implement |
| Weakness | Underestimates joint crashes |

### 2. Student-t Copula

Like Gaussian but with fatter joint tails:

$$C_{\Sigma,\nu}^{t}(u_1, ..., u_n) = t_{\Sigma,\nu}(t_\nu^{-1}(u_1), ..., t_\nu^{-1}(u_n))$$

| Property | Value |
|----------|-------|
| Parameters | Correlation matrix $\Sigma$, degrees of freedom $\nu$ |
| Tail dependence | **Symmetric** (both tails), increases as $\nu$ decreases |
| Use case | Default choice for financial returns |
| Advantage | Captures joint crashes AND joint rallies |

### 3. Clayton Copula

$$C_\theta(u_1, u_2) = (u_1^{-\theta} + u_2^{-\theta} - 1)^{-1/\theta}$$

| Property | Value |
|----------|-------|
| Parameter | $\theta > 0$ |
| Tail dependence | **Lower tail only** (joint crashes) |
| Use case | Equity crashes, credit risk |

### 4. Gumbel Copula

$$C_\theta(u_1, u_2) = \exp\left(-[(-\ln u_1)^\theta + (-\ln u_2)^\theta]^{1/\theta}\right)$$

| Property | Value |
|----------|-------|
| Parameter | $\theta \geq 1$ |
| Tail dependence | **Upper tail only** (joint rallies) |
| Use case | Insurance, extreme co-movements up |

### 5. Frank Copula

$$C_\theta(u_1, u_2) = -\frac{1}{\theta}\ln\left(1 + \frac{(e^{-\theta u_1}-1)(e^{-\theta u_2}-1)}{e^{-\theta}-1}\right)$$

| Property | Value |
|----------|-------|
| Parameter | $\theta \neq 0$ |
| Tail dependence | **None** (symmetric, no tail dependence) |
| Use case | When tail independence is appropriate |

---

## Tail Dependence

The probability that one variable is extreme given the other is extreme:

$$\lambda_L = \lim_{u \to 0^+} P(U_1 \leq u | U_2 \leq u) = \lim_{u \to 0^+} \frac{C(u,u)}{u}$$

$$\lambda_U = \lim_{u \to 1^-} P(U_1 > u | U_2 > u)$$

| Copula | $\lambda_L$ | $\lambda_U$ |
|--------|-------------|-------------|
| Gaussian | 0 | 0 |
| Student-t ($\nu$) | $2t_{\nu+1}\left(-\sqrt{(\nu+1)(1-\rho)/(1+\rho)}\right)$ | Same |
| Clayton ($\theta$) | $2^{-1/\theta}$ | 0 |
| Gumbel ($\theta$) | 0 | $2 - 2^{1/\theta}$ |

---

## Python Implementation

```python
import numpy as np
from scipy.stats import norm, t as t_dist
from scipy.optimize import minimize

class GaussianCopula:
    """Gaussian copula for bivariate case."""

    def __init__(self, rho):
        self.rho = rho

    def simulate(self, n=10000):
        """Generate samples from the copula."""
        mean = [0, 0]
        cov = [[1, self.rho], [self.rho, 1]]
        z = np.random.multivariate_normal(mean, cov, n)
        u = norm.cdf(z)  # Transform to uniform [0,1]
        return u

    def pdf(self, u1, u2):
        """Copula density."""
        x1 = norm.ppf(u1)
        x2 = norm.ppf(u2)
        rho = self.rho
        return (1 / np.sqrt(1 - rho**2)) * \
               np.exp(-(rho**2 * (x1**2 + x2**2) - 2 * rho * x1 * x2) /
                      (2 * (1 - rho**2)))


class StudentTCopula:
    """Student-t copula for bivariate case."""

    def __init__(self, rho, nu):
        self.rho = rho
        self.nu = nu

    def simulate(self, n=10000):
        """Generate samples from the t-copula."""
        mean = [0, 0]
        cov = [[1, self.rho], [self.rho, 1]]
        # Generate from multivariate normal
        z = np.random.multivariate_normal(mean, cov, n)
        # Scale by chi-squared for t distribution
        s = np.random.chisquare(self.nu, n) / self.nu
        t_samples = z / np.sqrt(s[:, np.newaxis])
        # Transform to uniform via t CDF
        u = t_dist.cdf(t_samples, self.nu)
        return u

    def tail_dependence(self):
        """Lower/upper tail dependence coefficient."""
        nu, rho = self.nu, self.rho
        td = 2 * t_dist.cdf(-np.sqrt((nu + 1) * (1 - rho) / (1 + rho)), nu + 1)
        return td  # Symmetric: lambda_L = lambda_U


class ClaytonCopula:
    """Clayton copula (lower tail dependence)."""

    def __init__(self, theta):
        assert theta > 0, "theta must be positive"
        self.theta = theta

    def simulate(self, n=10000):
        """Conditional sampling method."""
        u1 = np.random.uniform(0, 1, n)
        w = np.random.uniform(0, 1, n)
        u2 = u1 * (w**(-self.theta / (1 + self.theta)) - 1 + u1**self.theta) ** (-1 / self.theta)
        return np.column_stack([u1, u2])

    def tail_dependence(self):
        return 2**(-1 / self.theta)


def fit_copula(u1, u2, copula_type='gaussian'):
    """
    Fit a copula to uniform marginals.

    Parameters:
        u1, u2: Uniform [0,1] marginals (use empirical CDF to transform raw data)
        copula_type: 'gaussian', 'student_t', 'clayton'
    """
    if copula_type == 'gaussian':
        # MLE: maximize sum of log copula density
        def neg_ll(rho):
            rho = rho[0]
            x1 = norm.ppf(np.clip(u1, 1e-6, 1-1e-6))
            x2 = norm.ppf(np.clip(u2, 1e-6, 1-1e-6))
            ll = -0.5 * np.log(1 - rho**2) - \
                 (rho**2 * (x1**2 + x2**2) - 2 * rho * x1 * x2) / \
                 (2 * (1 - rho**2))
            return -np.sum(ll)

        result = minimize(neg_ll, x0=[0.5], bounds=[(-0.999, 0.999)])
        return {'type': 'gaussian', 'rho': result.x[0]}

    elif copula_type == 'clayton':
        # Kendall's tau relationship: tau = theta / (theta + 2)
        from scipy.stats import kendalltau
        tau, _ = kendalltau(u1, u2)
        theta = 2 * tau / (1 - tau) if tau > 0 else 0.1
        return {'type': 'clayton', 'theta': max(theta, 0.01)}

    return None


def empirical_cdf(x):
    """Transform data to uniform [0,1] via empirical CDF (rank transform)."""
    from scipy.stats import rankdata
    n = len(x)
    return rankdata(x) / (n + 1)  # Avoid 0 and 1
```

---

## Applications in Quant Finance

### 1. Portfolio Risk (VaR/CVaR)
- Use t-copula to model joint tail risk
- Gaussian copula underestimates portfolio VaR in crashes
- See [[Value at Risk (VaR)]] and [[Tail Risk and Black Swans]]

### 2. Pairs Trading / Stat Arb
- Model joint distribution of pair returns
- Copula-based signals detect changes in dependence structure
- See [[Pairs Trading]] and [[Statistical Arbitrage]]

### 3. Credit Risk / CDO Pricing
- Original use case (Li, 2000) — model default correlation
- Gaussian copula failed spectacularly in 2008
- Need t-copula or Clayton for realistic tail dependence

### 4. Multi-Asset Options
- Price basket options, best-of/worst-of options
- Copula determines payoff distribution
- See [[Derivatives Pricing]]

### 5. Correlation Trading
- Trade correlation as an asset (correlation swaps, dispersion trades)
- Copula choice directly impacts P&L estimation
- See [[Correlation and Diversification]]

---

## Related Notes
- [[Correlation and Diversification]] — Linear correlation limitations
- [[Probability and Statistics for Trading]] — Distribution theory
- [[Tail Risk and Black Swans]] — Extreme co-movements
- [[Value at Risk (VaR)]] — Copula-based VaR
- [[Monte Carlo Simulation]] — Simulating correlated assets
- [[Statistical Arbitrage]] — Copula-based pair selection
- [[Mathematics MOC]] — Parent section
