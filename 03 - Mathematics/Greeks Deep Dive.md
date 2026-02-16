# Greeks Deep Dive

The Greeks measure the sensitivity of an option's price to various factors. They are the foundation of options risk management and the building blocks of every [[Volatility Trading|volatility strategy]] and [[Options Strategies for Algos|options algorithm]].

---

## Overview

| Greek | Measures | Formula (BS) | Typical Range |
|-------|----------|---------------|---------------|
| **Delta** ($\Delta$) | Price sensitivity to underlying | $\frac{\partial V}{\partial S}$ | Call: [0, 1], Put: [-1, 0] |
| **Gamma** ($\Gamma$) | Rate of change of Delta | $\frac{\partial^2 V}{\partial S^2}$ | Always positive (long options) |
| **Theta** ($\Theta$) | Time decay | $\frac{\partial V}{\partial t}$ | Usually negative (long options) |
| **Vega** ($\mathcal{V}$) | Volatility sensitivity | $\frac{\partial V}{\partial \sigma}$ | Always positive (long options) |
| **Rho** ($\rho$) | Interest rate sensitivity | $\frac{\partial V}{\partial r}$ | Small for short-dated options |

---

## Delta ($\Delta$)

### Definition
Delta measures how much the option price changes for a $1 move in the underlying.

### Black-Scholes Formulas

$$\Delta_{\text{call}} = N(d_1)$$
$$\Delta_{\text{put}} = N(d_1) - 1$$

Where:
$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$$

### Interpretations
1. **Hedge ratio:** Number of shares needed to delta-hedge one option contract
2. **Probability proxy:** Approximate probability of expiring in-the-money
3. **Equivalent position:** A 0.50 delta call behaves like owning 50 shares

### Delta Behavior
| Moneyness | Call Delta | Put Delta |
|-----------|-----------|-----------|
| Deep ITM | ~1.0 | ~-1.0 |
| ATM | ~0.5 | ~-0.5 |
| Deep OTM | ~0.0 | ~0.0 |

**Key insight:** Delta changes fastest for ATM options near expiry (high gamma).

---

## Gamma ($\Gamma$)

### Definition
Gamma is the rate of change of delta — the "delta of delta." It measures convexity.

### Black-Scholes Formula

$$\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T}} = \frac{\phi(d_1)}{S \sigma \sqrt{T}}$$

Where $\phi(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}$ is the standard normal PDF.

### Properties
- **Highest ATM:** Gamma peaks when the option is at-the-money
- **Increases near expiry:** Short-dated ATM options have explosive gamma
- **Long options = long gamma** (benefits from large moves)
- **Short options = short gamma** (hurts from large moves)

### Gamma Scalping
The core of [[Volatility Trading]]:
1. Buy options (long gamma)
2. Delta-hedge continuously
3. Profit if realized vol > implied vol
4. Loss comes from theta decay

**P&L from gamma:** $\Pi_{\gamma} \approx \frac{1}{2} \Gamma (\Delta S)^2$

---

## Theta ($\Theta$)

### Definition
Theta measures time decay — how much value the option loses per day (all else equal).

### Black-Scholes Formulas

$$\Theta_{\text{call}} = -\frac{S \phi(d_1) \sigma}{2\sqrt{T}} - rKe^{-rT}N(d_2)$$

$$\Theta_{\text{put}} = -\frac{S \phi(d_1) \sigma}{2\sqrt{T}} + rKe^{-rT}N(-d_2)$$

### Properties
- **Always negative for long options** (time works against you)
- **Accelerates near expiry** for ATM options
- **Theta-Gamma tradeoff:** Long gamma costs theta; short gamma earns theta

### The Theta-Gamma Identity (fundamental relationship)

$$\Theta + \frac{1}{2}\sigma^2 S^2 \Gamma + rS\Delta - rV = 0$$

This is just the [[Black-Scholes Model|Black-Scholes PDE]] rewritten in terms of Greeks.

**Trading implication:** If realized vol > implied vol, gamma P&L > theta decay (profitable to be long gamma).

---

## Vega ($\mathcal{V}$)

### Definition
Vega measures sensitivity to a 1% change in implied volatility.

### Black-Scholes Formula

$$\mathcal{V} = S\sqrt{T} \cdot \phi(d_1)$$

### Properties
- **Highest ATM:** Like gamma, vega peaks at-the-money
- **Increases with time:** Longer-dated options have more vega
- **Same for calls and puts** (at same strike/expiry)

### Vega in Practice
- **Long vega:** Profit when IV rises (buy options before events)
- **Short vega:** Profit when IV falls (sell options after events)
- **Vega-neutral:** Balanced long/short options to isolate other Greeks

### Implied Volatility and Vega

$$\Delta\text{Option Price} \approx \mathcal{V} \times \Delta\sigma_{\text{impl}}$$

A 25-delta put with vega = 0.15 gains $0.15 for each 1% rise in IV.

---

## Rho ($\rho$)

### Definition
Rho measures sensitivity to a 1% change in the risk-free rate.

### Black-Scholes Formulas

$$\rho_{\text{call}} = KTe^{-rT}N(d_2)$$
$$\rho_{\text{put}} = -KTe^{-rT}N(-d_2)$$

### Properties
- **Usually small** for short-dated options
- **Matters for LEAPS** and long-dated options
- **Higher rates** increase call values, decrease put values
- **More relevant in rising/falling rate environments**

---

## Second and Third Order Greeks

| Greek | Measures | Formula | Use Case |
|-------|----------|---------|----------|
| **Vanna** | $\frac{\partial \Delta}{\partial \sigma}$ = $\frac{\partial \mathcal{V}}{\partial S}$ | Cross-sensitivity | Skew trading, dealer hedging |
| **Volga (Vomma)** | $\frac{\partial \mathcal{V}}{\partial \sigma}$ | Vega convexity | Vol-of-vol exposure |
| **Charm** | $\frac{\partial \Delta}{\partial t}$ | Delta decay | Overnight hedging |
| **Speed** | $\frac{\partial \Gamma}{\partial S}$ | Gamma sensitivity | Large move risk |
| **Color** | $\frac{\partial \Gamma}{\partial t}$ | Gamma decay | Expiry management |

### Vanna — The Dealer Hedging Greek
Vanna drives market flows as dealers hedge their skew exposure:
- When spot drops, put delta increases (negative vanna) → dealers sell more stock → amplifies selloff
- **"Vanna flows"** are a major driver of intraday market moves around OPEX

### Charm — Delta Bleed
Charm tells you how much your delta hedge drifts overnight:
- ATM options: charm is small (delta stays ~0.5)
- OTM options near expiry: charm is large (delta moves fast)

---

## Python Implementation

```python
import numpy as np
from scipy.stats import norm

class BSGreeks:
    """
    Complete Black-Scholes Greeks calculator.

    Parameters:
        S: Spot price
        K: Strike price
        T: Time to expiry (years)
        r: Risk-free rate
        sigma: Implied volatility
        q: Dividend yield (default 0)
    """

    def __init__(self, S, K, T, r, sigma, q=0):
        self.S = S
        self.K = K
        self.T = max(T, 1e-10)  # Avoid division by zero
        self.r = r
        self.sigma = sigma
        self.q = q
        self._compute_d()

    def _compute_d(self):
        self.d1 = (np.log(self.S / self.K) +
                    (self.r - self.q + 0.5 * self.sigma**2) * self.T) / \
                   (self.sigma * np.sqrt(self.T))
        self.d2 = self.d1 - self.sigma * np.sqrt(self.T)

    # --- First Order Greeks ---

    def delta(self, option_type='call'):
        if option_type == 'call':
            return np.exp(-self.q * self.T) * norm.cdf(self.d1)
        return np.exp(-self.q * self.T) * (norm.cdf(self.d1) - 1)

    def gamma(self):
        return (np.exp(-self.q * self.T) * norm.pdf(self.d1)) / \
               (self.S * self.sigma * np.sqrt(self.T))

    def theta(self, option_type='call'):
        """Returns daily theta (divide annual by 365)."""
        term1 = -(self.S * np.exp(-self.q * self.T) * norm.pdf(self.d1) * self.sigma) / \
                 (2 * np.sqrt(self.T))
        if option_type == 'call':
            term2 = -self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
            term3 = self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(self.d1)
        else:
            term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
            term3 = -self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(-self.d1)
        return (term1 + term2 + term3) / 365  # Daily theta

    def vega(self):
        """Returns vega per 1% move in vol."""
        return self.S * np.exp(-self.q * self.T) * norm.pdf(self.d1) * \
               np.sqrt(self.T) / 100

    def rho(self, option_type='call'):
        """Returns rho per 1% move in rate."""
        if option_type == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * \
                   norm.cdf(self.d2) / 100
        return -self.K * self.T * np.exp(-self.r * self.T) * \
               norm.cdf(-self.d2) / 100

    # --- Second Order Greeks ---

    def vanna(self):
        """dDelta/dVol = dVega/dSpot."""
        return -np.exp(-self.q * self.T) * norm.pdf(self.d1) * \
               self.d2 / self.sigma

    def volga(self):
        """dVega/dVol (vega convexity)."""
        return self.vega() * 100 * self.d1 * self.d2 / self.sigma

    def charm(self, option_type='call'):
        """dDelta/dTime."""
        term1 = -self.q * np.exp(-self.q * self.T) * norm.cdf(self.d1) if option_type == 'call' \
                else self.q * np.exp(-self.q * self.T) * norm.cdf(-self.d1)
        term2 = np.exp(-self.q * self.T) * norm.pdf(self.d1) * \
                (2 * (self.r - self.q) * self.T - self.d2 * self.sigma * np.sqrt(self.T)) / \
                (2 * self.T * self.sigma * np.sqrt(self.T))
        return term1 - term2

    # --- Option Price ---

    def price(self, option_type='call'):
        if option_type == 'call':
            return self.S * np.exp(-self.q * self.T) * norm.cdf(self.d1) - \
                   self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - \
               self.S * np.exp(-self.q * self.T) * norm.cdf(-self.d1)

    def summary(self, option_type='call'):
        """Print all Greeks for quick reference."""
        return {
            'Price': self.price(option_type),
            'Delta': self.delta(option_type),
            'Gamma': self.gamma(),
            'Theta (daily)': self.theta(option_type),
            'Vega (per 1%)': self.vega(),
            'Rho (per 1%)': self.rho(option_type),
            'Vanna': self.vanna(),
            'Volga': self.volga(),
            'Charm': self.charm(option_type),
        }


# --- Example Usage ---
if __name__ == '__main__':
    # AAPL Call: S=150, K=155, 30 days to expiry, 5% rate, 25% IV
    greeks = BSGreeks(S=150, K=155, T=30/365, r=0.05, sigma=0.25)

    print("=== Call Option Greeks ===")
    for name, val in greeks.summary('call').items():
        print(f"  {name:20s}: {val:+.6f}")

    print("\n=== Put Option Greeks ===")
    for name, val in greeks.summary('put').items():
        print(f"  {name:20s}: {val:+.6f}")
```

---

## Greeks for Portfolio Risk

### Portfolio Greeks
For a portfolio of $n$ options:

$$\Delta_P = \sum_{i=1}^{n} w_i \Delta_i, \quad \Gamma_P = \sum_{i=1}^{n} w_i \Gamma_i, \quad \text{etc.}$$

### Delta-Neutral Portfolio
Set $\Delta_P = 0$ by trading the underlying:
$$\text{Shares to hedge} = -\Delta_P \times \text{contract multiplier}$$

### Gamma-Neutral Portfolio
Requires trading another option (can't gamma-hedge with stock alone):
1. Choose a hedging option with known $\Gamma_H$
2. Trade $n = -\Gamma_P / \Gamma_H$ contracts of the hedging option
3. Re-delta-hedge with stock

---

## Greeks Across Market Regimes

| Regime | Key Risk | Hedge Priority |
|--------|----------|----------------|
| **Low Vol / Trending** | Gamma risk on shorts | Monitor short gamma exposure |
| **High Vol / Choppy** | Vega risk, theta bleed | Vega-neutral structures |
| **Pre-Event (Earnings)** | Vol crush risk | Vega exposure sizing |
| **Crisis / Crash** | Vanna flows, correlation spike | Tail hedges, reduce gross |
| **OPEX / Expiry** | Pin risk, charm | Close or roll near-expiry |

---

## Related Notes
- [[Black-Scholes Model]] — The pricing model behind these formulas
- [[Volatility Trading]] — Using Greeks for vol strategies
- [[Options Strategies for Algos]] — Algorithmic options strategies
- [[Volatility Surface Modeling]] — Beyond flat vol assumptions
- [[Stochastic Calculus]] — Mathematical foundation (Ito's lemma)
- [[Risk Management MOC]] — Greeks as risk measures
- [[Mathematics MOC]] — Parent section
