# Stochastic Calculus

Stochastic calculus is the mathematical foundation of continuous-time finance. It allows us to model assets that evolve randomly over time, providing the tools for derivatives pricing, risk management, and optimal execution.

---

## 1. Brownian Motion (Wiener Process)

A stochastic process $W_t$ is a standard Brownian motion if:
1.  $W_0 = 0$.
2.  It has continuous paths.
3.  It has independent increments: $W_t - W_s \sim N(0, t-s)$ for $t > s$.

**Properties for Quants:**
- **Martingale:** $E[W_t | \mathcal{F}_s] = W_s$. The best guess for the future is the current value.
- **Quadratic Variation:** $[W, W]_t = t$. Unlike smooth functions, the sum of squared increments of BM is non-zero. This is why we need Itô's Lemma.

---

## 2. Geometric Brownian Motion (GBM)

The "Standard Model" for stock prices (Black-Scholes-Merton).

$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

**Solution (via Itô's Lemma):**
$$S_t = S_0 \exp\left( (\mu - \frac{1}{2}\sigma^2)t + \sigma W_t \right)$$

- **Log-normal Distribution:** Prices $S_t$ are log-normal; log-returns $\ln(S_t/S_0)$ are normal.
- **Drift ($\mu$):** The expected return.
- **Volatility ($\sigma$):** The standard deviation of returns.

---

## 3. Itô's Lemma (The Chain Rule)

If $X_t$ is an Itô process $dX_t = \mu_t dt + \sigma_t dW_t$, and $f(t, x)$ is a twice-differentiable function, then:

$$df(t, X_t) = \left( \frac{\partial f}{\partial t} + \mu_t \frac{\partial f}{\partial x} + \frac{1}{2} \sigma_t^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma_t \frac{\partial f}{\partial x} dW_t$$

**Why it matters:** In normal calculus, $df = f_t dt + f_x dx$. In stochastic calculus, the $(\frac{1}{2} \sigma^2 f_{xx}) dt$ term appears because $(dW_t)^2 = dt$. This is the "Convexity Adjustment."

---

## 4. Change of Measure (Girsanov Theorem)

In derivatives pricing, we move from the **Physical Measure ($\mathbb{P}$)** to the **Risk-Neutral Measure ($\mathbb{Q}$)**.

- **$\mathbb{P}$ (Real World):** Assets have an expected return $\mu$.
- **$\mathbb{Q}$ (Risk-Neutral):** Assets have an expected return $r$ (the risk-free rate).

Girsanov's Theorem allows us to "shift" the drift of a Brownian motion while keeping the same volatility, which is the core of the **Fundamental Theorem of Asset Pricing**.

---

## 5. Feynman-Kac Formula

Provides a link between SDEs and Partial Differential Equations (PDEs).
- The solution to a PDE (like Black-Scholes) can be represented as an expectation of an SDE (Monte Carlo pricing).

---

## 6. Stochastic Volatility & Jumps

Standard GBM is often "too simple" for real markets.
- **Heston Model:** Volatility is itself a mean-reverting stochastic process.
- **Merton Jump-Diffusion:** Adds a Poisson process to account for sudden price crashes.
  $$dS_t = \mu S_t dt + \sigma S_t dW_t + S_t dJ_t$$

---

## Related Notes
- [[Mathematics MOC]] — Parent section
- [[Black-Scholes Model]] — Direct application of GBM
- [[Derivatives Pricing]] — No-arbitrage and measures
- [[Monte Carlo Simulation]] — Numerical solution of SDEs
- [[Interest Rate Models]] — SDEs for rates (Vasicek, CIR)
- [[Volatility Surface Modeling]] — Beyond constant volatility
