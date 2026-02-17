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

## Practical Workflow for Copula Modeling

Applying copulas involves a clear, multi-step process that separates the modeling of marginal distributions from the dependence structure.

### Step 1: Model the Marginal Distributions
For each asset or time series, you need to find its best-fitting marginal probability distribution.
1.  **Obtain the returns** (e.g., daily log returns for two stocks, MSFT and AAPL).
2.  **Fit a distribution to each series.** This is often a [[Time Series Analysis|GARCH model]] with a specified distribution for the innovations (residuals), like a standardized Student-t. This captures volatility clustering and fat tails in the individual series.
    - For `MSFT_returns`, fit `GARCH(1,1)` with a Student-t distribution.
    - For `AAPL_returns`, fit `GARCH(1,1)` with a Student-t distribution.
3.  **Extract the standardized residuals** from each fitted model. If the model is good, these residuals should be approximately IID (Independent and Identically Distributed).

### Step 2: Transform Residuals to Uniforms
The core input for a copula is a set of uniform variables, $u_i \in [0, 1]$. We transform the standardized residuals from Step 1 into uniforms using their own cumulative distribution function (CDF).
1.  For the `MSFT_residuals`, apply the CDF of the fitted Student-t distribution. This is often called the Probability Integral Transform (PIT).
    ```python
    # pseudo-code
    msft_u = t_dist.cdf(msft_residuals, df=msft_garch_fit.df)
    aapl_u = t_dist.cdf(aapl_residuals, df=aapl_garch_fit.df)
    ```
    Alternatively, and more simply, use the non-parametric empirical CDF (ECDF). This is less model-dependent.
    ```python
    msft_u = empirical_cdf(msft_residuals)
    aapl_u = empirical_cdf(aapl_residuals)
    ```
    Now you have two sets of uniform variables, `msft_u` and `aapl_u`, that retain the dependence structure of the original returns but have uniform marginals.

### Step 3: Fit a Copula to the Uniform Data
Now that you have the uniform marginals, you can fit different copula models to find the one that best describes their joint behavior.
1.  **Select candidate copulas** (e.g., Gaussian, Student-t, Clayton).
2.  **Fit each copula** to the pair of uniform data (`msft_u`, `aapl_u`) using Maximum Likelihood Estimation (MLE) or by calibrating to a rank correlation measure like Kendall's Tau.
3.  **Select the best-fitting copula** using information criteria like AIC or BIC, or by visual inspection of the resulting joint distribution.

### Step 4: Use the Fitted Copula for Simulation (Monte Carlo)
Once you have the full model (marginals + copula), you can simulate future scenarios.
1.  **Simulate from the copula:** Generate `N` pairs of dependent uniform variables from your chosen copula (e.g., a Student-t copula with fitted `rho` and `nu`).
    ```python
    # pseudo-code
    simulated_u = student_t_copula.simulate(n=N, rho=fitted_rho, nu=fitted_nu)
    ```
2.  **Transform uniforms back to residuals:** Use the inverse CDF (quantile function or PPF) of the marginal distributions to turn the simulated uniforms back into simulated standardized residuals.
    ```python
    # pseudo-code
    sim_residuals_msft = t_dist.ppf(simulated_u[:, 0], df=msft_garch_fit.df)
    sim_residuals_aapl = t_dist.ppf(simulated_u[:, 1], df=aapl_garch_fit.df)
    ```
3.  **Simulate returns:** Plug these simulated residuals into the GARCH models for each asset to generate simulated future returns. This generates a realistic, path-dependent forecast that respects the volatility clustering of the marginals and the tail dependence captured by the copula.

This complete process is essential for accurate risk modeling, portfolio optimization, and pricing complex multi-asset derivatives.

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

## More Copula Implementations

Here are the implementations for the Gumbel and Frank copulas, which are useful for modeling asymmetric upper-tail dependence and symmetric dependence without tail dependence, respectively.

```python
class GumbelCopula:
    """Gumbel copula (upper tail dependence)."""

    def __init__(self, theta):
        assert theta >= 1, "theta must be >= 1"
        self.theta = theta

    def simulate(self, n=10000):
        """Simulation using the Marshall-Olkin method."""
        # Generate stable distribution variable, not trivial in Python
        # A common approach is to use known algorithms e.g., from Chambers, Mallows, Stuck
        # For simplicity, we can use a library like `copulas` or `pycop` for this
        # The conceptual formula is:
        # u1 = exp(-(x1/A1)**theta)
        # u2 = exp(-(x2/A2)**theta)
        # where x are independent exponentials and A are from a stable distribution
        # As this is complex, we will show the tail dependence calculation here
        # and recommend using a library for simulation.
        print("Gumbel simulation is non-trivial; use a dedicated library.")
        return None

    def tail_dependence(self):
        return 2 - 2**(1 / self.theta)

class FrankCopula:
    """Frank copula (no tail dependence)."""

    def __init__(self, theta):
        assert theta != 0, "theta cannot be zero"
        self.theta = theta

    def simulate(self, n=10000):
        """Simulation via conditional distribution method."""
        u1 = np.random.uniform(0, 1, n)
        w = np.random.uniform(0, 1, n)
        
        # Numerically solve for u2, as the inverse is not closed-form
        # C(u2|u1) = w  => dC/du1 / dC = w
        # This is complex. A simpler method involves a log series distribution.
        # Again, a library is the practical choice here.
        print("Frank simulation is non-trivial; use a dedicated library.")
        return None

    def tail_dependence(self):
        return 0, 0 # Lower and Upper
```

---

## Copula Selection

Choosing the right copula is as important as fitting it correctly. The goal is to select the model that best represents the true underlying dependence structure.

### 1. Visual Inspection
- **Scatter plots:** Plot the uniform-transformed data (`u1` vs `u2`).
    - **Clustering in the bottom-left corner** suggests lower tail dependence (use Clayton).
    - **Clustering in the top-right corner** suggests upper tail dependence (use Gumbel).
    - **Clustering in both corners** suggests symmetric tail dependence (use Student-t).
    - **No obvious clustering in corners** suggests no tail dependence (use Gaussian or Frank).
- **Contour plots:** Plot the PDF of the fitted copula over the scatter plot of the data. The contours of a good model should align with the density of the data points.

### 2. Information Criteria (AIC/BIC)
The most common quantitative method is to compare goodness-of-fit using information criteria, which penalize models for having more parameters.
1.  Fit several candidate copulas (Gaussian, Student-t, Clayton, Gumbel) to the data using Maximum Likelihood Estimation (MLE).
2.  Calculate the log-likelihood (`LL`) for each fitted model.
3.  Calculate the Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC):
    $$ \text{AIC} = 2k - 2 \cdot LL $$
    $$ \text{BIC} = k \ln(n) - 2 \cdot LL $$
    Where `k` is the number of parameters in the copula (e.g., `k=1` for Gaussian/Clayton/Gumbel, `k=2` for Student-t) and `n` is the number of data points.

**The model with the lowest AIC or BIC is considered the best.** BIC penalizes model complexity more heavily than AIC.

### 3. Goodness-of-Fit Tests
More formal statistical tests can be used, such as the Cramer-von Mises test, tailored for copulas. These tests compare the empirical copula (derived from the data) to the parametric copula being tested. A high p-value suggests the copula is a good fit. These are more complex to implement and are often found in specialized R packages like `VineCopula`.

### Practical Recommendation
For most financial applications:
1.  Start by fitting a **Student-t copula** as it is flexible and captures the common case of symmetric tail dependence.
2.  Fit a **Clayton copula** if you specifically suspect asymmetric downside risk (e.g., equity portfolio).
3.  Compare the BIC of the Student-t and Clayton models. If the Student-t BIC is significantly lower, its added parameter ($\nu$) is justified. If not, the simpler model may be preferred.
4.  Use visual inspection to confirm your choice.

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
