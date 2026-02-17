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

## Detailed Derivation of the Black-Scholes PDE

The derivation of the Black-Scholes Partial Differential Equation (PDE) is a cornerstone of quantitative finance. It elegantly combines stochastic calculus with the economic argument of no-arbitrage.

### Step 1: Model the Underlying Asset Price
We start by assuming the underlying asset's price, $S_t$, follows a Geometric Brownian Motion (GBM). This is a stochastic process defined by the following Stochastic Differential Equation (SDE):
$$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$$
Here, $\mu$ is the expected return (drift) of the asset, $\sigma$ is its volatility, and $dW_t$ is a Wiener process, representing the source of randomness.

### Step 2: Form a Risk-Free Portfolio
The core insight is to construct a portfolio, $\Pi$, that is instantaneously risk-free. We do this by holding a long position in $\Delta$ units of the underlying asset and a short position in one unit of a derivative (e.g., a call option), whose price is $V(S, t)$.
$$\Pi_t = \Delta_t S_t - V(S_t, t)$$
The change in the value of this portfolio over a small time step $dt$ is:
$$d\Pi_t = \Delta_t \, dS_t - dV_t$$

### Step 3: Apply Itô's Lemma to the Derivative's Price
Since $V$ is a function of the random variable $S_t$ and time $t$, we must use [[Stochastic Calculus|Itô's lemma]] to find its differential, $dV_t$. Itô's lemma gives us:
$$dV_t = \left( \frac{\partial V}{\partial t} + \mu S_t \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} \right) dt + \sigma S_t \frac{\partial V}{\partial S} dW_t$$
The terms can be identified with the Greeks: $\frac{\partial V}{\partial S} = \Delta$, $\frac{\partial^2 V}{\partial S^2} = \Gamma$, and $\frac{\partial V}{\partial t} = \Theta$.

### Step 4: Substitute and Eliminate Risk
Now, substitute the expressions for $dS_t$ and $dV_t$ back into the portfolio change equation, $d\Pi_t$:
$$d\Pi_t = \Delta_t (\mu S_t dt + \sigma S_t dW_t) - \left[ \left( \frac{\partial V}{\partial t} + \mu S_t \Delta_t + \frac{1}{2} \sigma^2 S_t^2 \Gamma_t \right) dt + \sigma S_t \Delta_t dW_t \right]$$
Notice that we have set the portfolio's delta, $\Delta_t$, to be equal to the option's delta, $\frac{\partial V}{\partial S}$. This is the crucial hedging step. The terms with the random component $dW_t$ are:
$$\Delta_t \sigma S_t dW_t - \sigma S_t \Delta_t dW_t = 0$$
They cancel out perfectly! This is the essence of delta hedging. The portfolio is now instantaneously risk-free. The change in its value is purely deterministic:
$$d\Pi_t = - \left( \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S_t^2 \Gamma_t \right) dt$$

### Step 5: The No-Arbitrage Argument
A fundamental economic principle states that a risk-free portfolio must earn the risk-free interest rate, $r$. Any other return would present an arbitrage opportunity.
$$d\Pi_t = r \Pi_t \, dt = r (\Delta_t S_t - V) \, dt$$
We now have two expressions for $d\Pi_t$. Setting them equal gives:
$$- \left( \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S_t^2 \Gamma_t \right) dt = r (\Delta_t S_t - V) \, dt$$
Dividing by $dt$ and rearranging gives the celebrated Black-Scholes PDE:
$$\frac{\partial V}{\partial t} + rS\frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - rV = 0$$
This equation must be satisfied by the price of any derivative on the asset $S$. The specific derivative (call, put, etc.) is determined by the boundary conditions applied when solving the PDE.

### Key Insight: Risk-Neutral Pricing
The drift of the stock, $\mu$, has vanished from the final equation. This is a profound result. It means the option's price does not depend on the expected return of the underlying asset. We can, therefore, price the option in a "risk-neutral" world where we assume the asset grows at the risk-free rate, $r$, and then discount the expected payoff. This is the principle of risk-neutral valuation.

$$C = e^{-rT} \mathbb{E}^{\mathbb{Q}}[\max(S_T - K, 0)]$$

---

## Assumptions and Limitations

The BSM model's elegance comes from its strong, often unrealistic, assumptions. Understanding these is key to knowing when and why the model fails.

| # | Assumption | Reality & Limitation | Practical Impact |
|---|---|---|---|
| 1 | **Log-normal Returns** | Financial returns exhibit "fat tails" (kurtosis) and skewness. Extreme events are far more common than a normal distribution predicts. | The model systematically underprices out-of-the-money options, especially puts, which are sensitive to crashes. This gives rise to the [[Volatility Surface Modeling|volatility smile/skew]]. |
| 2 | **Constant Volatility ($\sigma$)** | Volatility is stochastic; it changes over time and is not constant. It clusters in periods of high and low activity. | The model cannot price options on volatility itself (like VIX options) and fails to capture the term structure of volatility. [[GARCH Models]] and stochastic volatility models (Heston) are needed. |
| 3 | **No Transaction Costs or Frictions** | Trading incurs costs (commissions, bid-ask spreads, slippage). Delta hedging is not frictionless. | Continuous rebalancing is impossible and costly. In practice, hedging is done discretely, leading to hedging error and tracking risk. |
| 4 | **Continuous Trading** | Trading occurs at discrete intervals, not continuously. | The perfect hedge is a mathematical ideal. Jumps or gaps in the underlying price between rebalancing periods can cause large hedging losses. |
| 5 | **Constant Risk-Free Rate ($r$)** | Interest rates are not constant; they are stochastic and have their own term structure. | This is a minor issue for short-dated options but becomes a significant source of error for long-dated options (LEAPS) and interest rate derivatives. |
| 6 | **No Arbitrage Opportunities** | The model's derivation relies on the ability to execute risk-free arbitrage. | In reality, market frictions, capital constraints, and risk limits can prevent arbitrageurs from forcing prices to their theoretical values. |
| 7 | **European-Style Exercise** | The formula only applies to options that can be exercised at expiration. | It cannot be directly used for American options, which can be exercised early. This requires numerical methods like binomial trees or finite difference methods. |
| 8 | **No Dividends (Basic Model)** | Many stocks pay dividends, which affects the stock price on the ex-dividend date. | The Merton (1973) extension for a continuous dividend yield ($q$) is a standard fix, but it does not handle discrete dividend payments accurately. |

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
