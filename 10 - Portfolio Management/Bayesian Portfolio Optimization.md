# Bayesian Portfolio Optimization

Classical portfolio optimization (Markowitz) assumes we know the future returns and covariances perfectly. In reality, these are noisy estimates. **Bayesian Portfolio Optimization** treats these parameters as random variables with their own distributions, allowing quants to incorporate **Prior Beliefs** and **Uncertainty** into the allocation process.

---

## 1. The Core Idea: Prior + Evidence = Posterior

Instead of a single "best" weight, we look for weights that work across the range of likely scenarios.

1.  **Prior ($\pi$):** Our belief about returns before seeing recent data (e.g., "The market usually returns 8%").
2.  **Likelihood ($L$):** What the recent data suggests.
3.  **Posterior:** The updated belief used for optimization.

---

## 2. Black-Litterman Model (The Industry Standard)

The most famous Bayesian application in finance. It allows a Portfolio Manager to combine **Market Equilibrium** (prior) with their own **Subjective Views** (evidence).

- **Prior:** The market-cap-weighted portfolio is assumed to be optimal.
- **Views:** "I think Tech will outperform Utilities by 2%."
- **Benefit:** Prevents the "Extreme Weights" and "Instability" problems of standard mean-variance optimization.
- See [[Black-Litterman Model]] for full implementation.

---

## 3. Bayesian Shrinkage (Stein's Paradox)

Statistical estimates of returns for a large number of assets are prone to high error.
- **Shrinkage:** Moving individual asset return estimates toward a "Global Mean" or a "Factor Model" estimate.
- **Ledoit-Wolf Covariance:** A Bayesian-inspired shrinkage method for the covariance matrix that makes it more stable and invertible.

---

## 4. Full Bayesian Hierarchical Models

Using Markov Chain Monte Carlo (MCMC) to sample from the posterior distribution of optimal weights.
- **Why:** Allows for non-normal distributions (e.g., Student-t for fat tails) and non-linear constraints that classical quadratic programming cannot handle.

---

## 5. Advantages over Classical Markowitz

| Feature | Classical (MLE) | Bayesian |
|---------|-----------------|----------|
| **Parameter Uncertainty** | Ignored. | Explicitly modeled. |
| **Out-of-Sample Performance** | Often poor (Overfitting). | More robust and stable. |
| **Inclusion of Views** | No easy mechanism. | Core part of the framework (Priors). |
| **Sensitivity** | Extremely high. | Graceful degradation. |

---

## 6. Python: Shrinkage Concept

```python
import numpy as np

def bayesian_return_shrinkage(observed_returns, prior_mean, confidence=0.5):
    """
    Simple shrinkage estimator.
    Returns a weighted average of the observed data and the prior belief.
    """
    # confidence = 1.0 means we ignore data and trust the prior entirely
    shrunk_returns = (1 - confidence) * observed_returns + confidence * prior_mean
    return shrunk_returns
```

---

## Related Notes
- [[Modern Portfolio Theory]] — The baseline being improved.
- [[Black-Litterman Model]] — Detailed implementation.
- [[Linear Algebra in Finance]] — Covariance and Shrinkage.
- [[Factor Models]] — Providing the Bayesian priors.
- [[Portfolio Optimization]] — The broader context.
