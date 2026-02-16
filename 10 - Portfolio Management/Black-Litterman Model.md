# Black-Litterman Model

> Fischer Black & Robert Litterman (1992) — Developed at Goldman Sachs

The Black-Litterman model solves Markowitz's biggest problem: **extreme sensitivity to expected return estimates**. It combines market equilibrium returns with investor views using Bayesian inference.

---

## Why Black-Litterman?

**The Markowitz problem:** If you estimate expected returns from historical data, the optimizer produces insane portfolios — 300% long one stock, 200% short another. Small changes in inputs cause wild swings in weights.

**The BL solution:** Start from a neutral "equilibrium" portfolio (the market), then tilt toward your views proportional to your confidence.

---

## The Model in Three Steps

### Step 1: Implied Equilibrium Returns (Prior)

Reverse-engineer the expected returns that make the market portfolio optimal:

$$\boldsymbol{\Pi} = \delta \Sigma \mathbf{w}_{mkt}$$

Where:
- $\boldsymbol{\Pi}$ = implied equilibrium excess returns
- $\delta$ = risk aversion coefficient (typically $\delta = \frac{E[R_m] - r_f}{\sigma_m^2}$, around 2.5)
- $\Sigma$ = covariance matrix
- $\mathbf{w}_{mkt}$ = market capitalization weights

### Step 2: Express Your Views

Views are expressed as: **"I believe [portfolio P] will return [Q] with confidence [Omega]"**

$$P \cdot \boldsymbol{\mu} = Q + \epsilon, \quad \epsilon \sim N(0, \Omega)$$

Where:
- $P$ = pick matrix (which assets the view is about)
- $Q$ = expected returns of the view
- $\Omega$ = uncertainty of the view (diagonal matrix)

**Example views:**
| View | P row | Q |
|------|-------|---|
| "AAPL will return 10%" | [0, 0, 1, 0, 0] | 0.10 |
| "GOOGL will outperform MSFT by 3%" | [0, -1, 0, 1, 0] | 0.03 |
| "Tech sector returns 8%" | [0.33, 0.33, 0.33, 0, 0] | 0.08 |

### Step 3: Combine (Posterior)

$$\boldsymbol{\mu}_{BL} = [(\tau \Sigma)^{-1} + P^T \Omega^{-1} P]^{-1} [(\tau \Sigma)^{-1} \boldsymbol{\Pi} + P^T \Omega^{-1} Q]$$

Where $\tau$ is a scalar (typically 0.025–0.05) representing uncertainty in the equilibrium.

---

## Full Implementation

```python
import numpy as np

class BlackLitterman:
    def __init__(self, cov, market_weights, risk_aversion=2.5, tau=0.05):
        """
        Parameters:
            cov: Covariance matrix (n x n)
            market_weights: Market cap weights (n,)
            risk_aversion: Risk aversion coefficient (scalar)
            tau: Uncertainty in equilibrium (scalar, 0.025-0.05)
        """
        self.cov = np.array(cov)
        self.w_mkt = np.array(market_weights)
        self.delta = risk_aversion
        self.tau = tau
        self.n = len(market_weights)

        # Step 1: Implied equilibrium returns
        self.pi = self.delta * self.cov @ self.w_mkt

    def posterior(self, P, Q, omega=None, confidence=None):
        """
        Compute Black-Litterman posterior returns.

        Parameters:
            P: Pick matrix (k x n) — k views on n assets
            Q: View returns (k,)
            omega: View uncertainty (k x k). If None, use proportional method.
            confidence: Confidence levels (k,) — higher = more confident in view
        """
        P = np.array(P)
        Q = np.array(Q)
        k = len(Q)

        # Default omega: proportional to uncertainty of the view portfolio
        if omega is None:
            if confidence is None:
                confidence = np.ones(k) * 0.5
            # Idzorek's method: scale omega inversely with confidence
            omega = np.diag([
                (1 / conf - 1) * (p @ (self.tau * self.cov) @ p)
                for p, conf in zip(P, confidence)
            ])

        # Posterior expected returns
        tau_cov_inv = np.linalg.inv(self.tau * self.cov)
        omega_inv = np.linalg.inv(omega)

        posterior_cov = np.linalg.inv(tau_cov_inv + P.T @ omega_inv @ P)
        posterior_mu = posterior_cov @ (tau_cov_inv @ self.pi + P.T @ omega_inv @ Q)

        # Posterior covariance of returns
        posterior_sigma = self.cov + posterior_cov

        return posterior_mu, posterior_sigma

    def optimal_weights(self, P, Q, omega=None, confidence=None):
        """Compute optimal portfolio weights given views."""
        mu_bl, sigma_bl = self.posterior(P, Q, omega, confidence)
        # Mean-variance optimal weights
        w = np.linalg.inv(self.delta * sigma_bl) @ mu_bl
        w = w / np.sum(w)  # Normalize
        return w


# --- Example Usage ---
if __name__ == "__main__":
    # 5 assets: SPY, QQQ, TLT, GLD, VWO
    cov = np.array([
        [0.0225, 0.0180, -0.0030, 0.0010, 0.0150],
        [0.0180, 0.0324, -0.0045, 0.0005, 0.0160],
        [-0.0030, -0.0045, 0.0100, 0.0020, -0.0020],
        [0.0010, 0.0005, 0.0020, 0.0144, 0.0030],
        [0.0150, 0.0160, -0.0020, 0.0030, 0.0400]
    ])

    market_weights = np.array([0.40, 0.25, 0.15, 0.10, 0.10])

    bl = BlackLitterman(cov, market_weights)
    print("Equilibrium returns:", bl.pi)

    # Views:
    # 1. QQQ will return 15% (high confidence)
    # 2. GLD will outperform VWO by 5% (medium confidence)
    P = np.array([
        [0, 1, 0, 0, 0],       # View 1: QQQ
        [0, 0, 0, 1, -1],      # View 2: GLD vs VWO
    ])
    Q = np.array([0.15, 0.05])
    confidence = np.array([0.8, 0.5])

    mu_bl, _ = bl.posterior(P, Q, confidence=confidence)
    print("BL returns:", mu_bl)

    w_bl = bl.optimal_weights(P, Q, confidence=confidence)
    print("BL weights:", w_bl)
```

---

## Why It Works at JPM / Goldman

1. **Stable outputs** — Weights don't flip when you change one estimate slightly
2. **Intuitive** — Start from market, tilt toward your views
3. **Flexible confidence** — Express strong or weak views, model reacts proportionally
4. **No views = market portfolio** — Sensible default when you have no alpha
5. **Combines multiple PMs** — Each PM expresses views, BL combines them

---

## Key Parameters

| Parameter | Typical Range | Effect |
|-----------|--------------|--------|
| $\tau$ | 0.025–0.05 | Lower = trust equilibrium more |
| $\delta$ | 2.0–4.0 | Risk aversion, higher = less risky portfolio |
| Confidence | 0–1 | Higher = tilt more toward view |
| $\Omega$ scaling | Varies | Controls how much views override equilibrium |

---

## Limitations

- **Garbage views in = garbage out** — BL doesn't validate your views
- **Single period** — No multi-period dynamics
- **Normal assumption** — Fat tails not captured
- **Covariance estimation** — Still need a good covariance matrix
- **Parameter sensitivity** — $\tau$ and $\Omega$ require calibration

---

## Related Notes
- [[Modern Portfolio Theory]] — The foundation BL improves upon
- [[Factor Models]] — Alternative approach to return estimation
- [[Portfolio Optimization]] — Other optimization methods
- [[Optimization Methods]] — Numerical methods for BL
- [[Probability and Statistics for Trading]] — Bayesian inference foundations
