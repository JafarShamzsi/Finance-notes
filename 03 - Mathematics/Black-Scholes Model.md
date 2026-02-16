# Black-Scholes Model

The Black-Scholes-Merton (BSM) model is the cornerstone of modern options pricing. Published in 1973, it provides a closed-form solution for European option prices and defines the framework for [[Greeks Deep Dive|the Greeks]], [[Volatility Trading|volatility trading]], and [[Derivatives Pricing|derivatives pricing]].

---

## The Black-Scholes Formula

### Call Option
$$C = S_0 e^{-qT} N(d_1) - K e^{-rT} N(d_2)$$

### Put Option
$$P = K e^{-rT} N(-d_2) - S_0 e^{-qT} N(-d_1)$$

Where:
$$d_1 = \frac{\ln(S_0/K) + (r - q + \sigma^2/2)T}{\sigma\sqrt{T}}$$
$$d_2 = d_1 - \sigma\sqrt{T}$$

| Symbol | Meaning |
|--------|---------|
| $S_0$ | Current spot price |
| $K$ | Strike price |
| $T$ | Time to expiration (years) |
| $r$ | Risk-free interest rate |
| $\sigma$ | Volatility of the underlying |
| $q$ | Continuous dividend yield |
| $N(\cdot)$ | Standard normal CDF |

---

## Derivation Sketch

### Step 1: Assume GBM for the Underlying
$$dS = \mu S \, dt + \sigma S \, dW$$

Where $W$ is a Wiener process (see [[Stochastic Calculus]]).

### Step 2: Construct a Riskless Portfolio
Hold $\Delta$ shares and short 1 option (or vice versa):
$$\Pi = \Delta S - V$$

Choose $\Delta = \frac{\partial V}{\partial S}$ to eliminate the stochastic term.

### Step 3: Apply Ito's Lemma
By [[Stochastic Calculus|Ito's lemma]], the option price $V(S, t)$ satisfies:
$$dV = \frac{\partial V}{\partial t} dt + \frac{\partial V}{\partial S} dS + \frac{1}{2} \frac{\partial^2 V}{\partial S^2} \sigma^2 S^2 dt$$

### Step 4: The Black-Scholes PDE
Since the portfolio is riskless, it must earn the risk-free rate:

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0$$

This is **the** fundamental PDE of options pricing.

### Step 5: Solve with Boundary Conditions
- **Call:** $V(S, T) = \max(S - K, 0)$
- **Put:** $V(S, T) = \max(K - S, 0)$

The solution gives the closed-form formulas above.

### Key Insight: Risk-Neutral Pricing
The drift $\mu$ disappears from the PDE — only the risk-free rate $r$ matters. This is **risk-neutral pricing**: we can price options as if the underlying grows at $r$, not $\mu$.

$$C = e^{-rT} \mathbb{E}^{\mathbb{Q}}[\max(S_T - K, 0)]$$

---

## Assumptions

| # | Assumption | Reality | Impact |
|---|-----------|---------|--------|
| 1 | Log-normal returns (GBM) | Fat tails, skewness | Underprices OTM puts (vol smile) |
| 2 | Constant volatility | Vol changes over time | Need [[GARCH Models]] or stoch vol |
| 3 | No transaction costs | Spreads, commissions, slippage | Delta hedging costs money |
| 4 | Continuous trading | Discrete rebalancing | Hedging error, gamma risk |
| 5 | No dividends (basic) | Stocks pay dividends | Use Merton's extension ($q$ term) |
| 6 | Constant risk-free rate | Rates change | Matters for long-dated options |
| 7 | No arbitrage | Market friction | Foundation of risk-neutral pricing |
| 8 | European exercise only | American options exist | Need binomial/FD for Americans |

---

## Put-Call Parity

A fundamental no-arbitrage relationship:

$$C - P = S_0 e^{-qT} - K e^{-rT}$$

If this is violated, there's an arbitrage opportunity.

**Uses:**
- Verify your pricing model
- Compute implied vol for one from the other
- Identify mispricings

---

## Implied Volatility

The market doesn't quote option prices — it quotes implied volatility. IV is the $\sigma$ that makes BSM match the market price.

### Newton-Raphson IV Solver
```python
def implied_vol(market_price, S, K, T, r, q=0, option_type='call',
                tol=1e-8, max_iter=100):
    """
    Solve for implied volatility using Newton-Raphson.
    Uses vega as the derivative.
    """
    sigma = 0.20  # Initial guess
    for _ in range(max_iter):
        greeks = BSGreeks(S, K, T, r, sigma, q)
        price = greeks.price(option_type)
        vega = greeks.vega() * 100  # Convert from per-1% to per-1

        diff = price - market_price
        if abs(diff) < tol:
            return sigma

        if abs(vega) < 1e-12:
            break  # Vega too small, can't converge

        sigma -= diff / vega

    return sigma  # Best estimate
```

### The Volatility Smile/Skew
BSM assumes constant $\sigma$ across all strikes. In reality:
- **Equity skew:** OTM puts have higher IV than OTM calls (crash protection demand)
- **FX smile:** Both wings have higher IV (symmetric jumps)
- **Commodity smile:** Varies by market structure

This is why we need [[Volatility Surface Modeling]].

---

## Extensions and Alternatives

| Model | Extension | Use Case |
|-------|-----------|----------|
| **Merton (1973)** | Dividend yield | Equity options |
| **Black (1976)** | Futures/forwards | Commodity options, caps/floors |
| **Garman-Kohlhagen** | Two interest rates | FX options |
| **Merton Jump-Diffusion** | Adds Poisson jumps | Fat tails, earnings events |
| **Heston (1993)** | Stochastic volatility | Vol smile, term structure |
| **SABR** | Stoch vol + CEV | Swaptions, FX |
| **Local Volatility** | Strike/time dependent $\sigma(S,t)$ | Exotic pricing |

---

## Python Implementation

```python
import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, q=0, option_type='call'):
    """
    Black-Scholes-Merton option pricing.

    Parameters:
        S: Spot price
        K: Strike price
        T: Time to expiration (years)
        r: Risk-free rate (continuous)
        sigma: Volatility
        q: Continuous dividend yield
        option_type: 'call' or 'put'

    Returns:
        Option price
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)


def bs_greeks_all(S, K, T, r, sigma, q=0, option_type='call'):
    """Return all Greeks as a dict. See [[Greeks Deep Dive]] for details."""
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    price = black_scholes(S, K, T, r, sigma, q, option_type)
    gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T) / 100

    if option_type == 'call':
        delta = np.exp(-q * T) * norm.cdf(d1)
        theta = (-(S * np.exp(-q * T) * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2)
                 + q * S * np.exp(-q * T) * norm.cdf(d1)) / 365
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:
        delta = np.exp(-q * T) * (norm.cdf(d1) - 1)
        theta = (-(S * np.exp(-q * T) * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)
                 - q * S * np.exp(-q * T) * norm.cdf(-d1)) / 365
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

    return {
        'price': price, 'delta': delta, 'gamma': gamma,
        'theta': theta, 'vega': vega, 'rho': rho
    }
```

---

## Historical Significance

- **1973:** Fischer Black, Myron Scholes publish the model; Robert Merton extends it
- **1997:** Scholes and Merton receive Nobel Prize (Black had died in 1995)
- **Impact:** Enabled the explosion of derivatives markets, standardized options pricing
- **LTCM (1998):** Showed the limits of BSM assumptions in crisis conditions

---

## Related Notes
- [[Greeks Deep Dive]] — Detailed Greeks derivations and implementation
- [[Stochastic Calculus]] — Mathematical foundation (GBM, Ito)
- [[Volatility Surface Modeling]] — Beyond constant vol
- [[Derivatives Pricing]] — Alternative pricing methods
- [[Options Strategies for Algos]] — Trading strategies using BSM
- [[Volatility Trading]] — Vol as an asset class
- [[Monte Carlo Simulation]] — MC pricing as BSM alternative
- [[Mathematics MOC]] — Parent section
