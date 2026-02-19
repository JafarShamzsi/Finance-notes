# Derivatives Pricing

Derivatives pricing is the mathematical process of determining the "fair value" of a contract that derives its value from an underlying asset. The fundamental principle is **no-arbitrage pricing**.

---

## 1. No-Arbitrage Principle

A fair price is one where no risk-free profit can be made by simultaneously buying and selling related assets. In a risk-neutral world, the price of a derivative is the expected discounted value of its future payoffs.

$$f_0 = e^{-rT} \mathbb{E}^{\mathbb{Q}}[f_T]$$

---

## 2. Binomial Options Pricing Model (BOPM)

The binomial model assumes the underlying price can move to only two possible states (Up or Down) in each time step.

### Single-Period Model
- $u$: Up factor
- $d$: Down factor
- $p$: Risk-neutral probability $= \frac{e^{r\Delta t} - d}{u - d}$

$$f = e^{-r\Delta t} [p f_u + (1-p) f_d]$$

### Multi-Period Binomial Tree
```python
import numpy as np

def binomial_tree_pricing(S, K, T, r, sigma, N, option_type='call'):
    """
    Price a European option using a multi-period binomial tree.
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # Initialize asset prices at maturity
    prices = np.zeros(N + 1)
    for i in range(N + 1):
        prices[i] = S * (u ** (N - i)) * (d ** i)

    # Payoffs at maturity
    if option_type == 'call':
        payoffs = np.maximum(prices - K, 0)
    else:
        payoffs = np.maximum(K - prices, 0)

    # Backward induction
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            payoffs[i] = np.exp(-r * dt) * (p * payoffs[i] + (1 - p) * payoffs[i+1])

    return payoffs[0]

# Example
price = binomial_tree_pricing(100, 100, 1, 0.05, 0.2, 100)
# Output: ~10.45 (close to Black-Scholes)
```

---

## 3. Monte Carlo Pricing

Monte Carlo simulation is essential for path-dependent options (like Asian or Barrier options) where no analytical solution exists.

### Algorithm
1.  Simulate $N$ price paths using Geometric Brownian Motion (GBM).
2.  Calculate the option payoff for each path.
3.  Average the payoffs and discount back to the present.

$$S_{t+\Delta t} = S_t e^{(r - \frac{1}{2}\sigma^2)\Delta t + \sigma\sqrt{\Delta t} Z}$$

```python
def monte_carlo_pricing(S, K, T, r, sigma, n_paths=100000):
    """
    Price a European call option using Monte Carlo simulation.
    """
    # Simulate final prices
    Z = np.random.standard_normal(n_paths)
    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    # Calculate payoffs
    payoffs = np.maximum(S_T - K, 0)

    # Discount and average
    price = np.exp(-r * T) * np.mean(payoffs)
    std_error = np.exp(-r * T) * np.std(payoffs) / np.sqrt(n_paths)

    return price, std_error

# Example
mc_price, error = monte_carlo_pricing(100, 100, 1, 0.05, 0.2)
# Output: (10.45, 0.05)
```

---

## 4. Black-Scholes Model (Analytical)

The continuous-time limit of the binomial model. See [[Black-Scholes Model]] for a deep dive.

---

## 5. Greeks

Sensitivity of the option price to its parameters. See [[Greeks Deep Dive]] for more.

---

## Related Notes
- [[Mathematics MOC]] — Master navigation
- [[Black-Scholes Model]] — Deep dive into the analytical model
- [[Greeks Deep Dive]] — Sensitivities (Delta, Gamma, etc.)
- [[Volatility Surface Modeling]] — IV modeling
- [[Stochastic Calculus]] — The math behind GBM
- [[Monte Carlo Simulation]] — General MC techniques
