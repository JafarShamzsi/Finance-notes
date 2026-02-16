# Derivatives Pricing

Beyond the [[Black-Scholes Model|Black-Scholes]] closed-form, most real-world derivatives require numerical methods. This note covers the three main numerical pricing approaches: **binomial trees**, **finite difference methods**, and **Monte Carlo simulation** — the tools every quant needs.

---

## Pricing Methods Overview

| Method | Best For | Complexity | Accuracy |
|--------|----------|-----------|----------|
| **Closed-form (BS)** | European vanilla | O(1) | Exact (within model) |
| **Binomial/Trinomial Trees** | American options, barriers | O(N²) | Good (N>200) |
| **Finite Difference (PDE)** | American, barriers, complex payoffs | O(N×M) | Very good |
| **Monte Carlo** | Path-dependent, multi-asset | O(N_paths × N_steps) | Flexible but slow |
| **FFT/Characteristic Function** | European (Heston, jumps) | O(N log N) | Excellent |

---

## Binomial Tree (Cox-Ross-Rubinstein, 1979)

### Model
At each step, the stock can go **up** by factor $u$ or **down** by factor $d$:

$$u = e^{\sigma\sqrt{\Delta t}}, \quad d = e^{-\sigma\sqrt{\Delta t}} = 1/u$$

Risk-neutral probability:
$$p = \frac{e^{(r-q)\Delta t} - d}{u - d}$$

### Algorithm
1. Build the tree forward (stock prices at each node)
2. Compute payoff at terminal nodes
3. Walk backward, discounting at each node

**For American options:** At each node, check if early exercise is optimal:
$$V_{\text{node}} = \max(\text{intrinsic value}, \text{continuation value})$$

```python
import numpy as np

def binomial_tree(S, K, T, r, sigma, q=0, N=500, option_type='call', american=False):
    """
    Binomial tree option pricer.

    Parameters:
        S: Spot price
        K: Strike
        T: Time to expiry (years)
        r: Risk-free rate
        sigma: Volatility
        q: Dividend yield
        N: Number of time steps
        option_type: 'call' or 'put'
        american: True for American-style exercise
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp((r - q) * dt) - d) / (u - d)
    disc = np.exp(-r * dt)

    # Terminal stock prices
    stock = S * u**(np.arange(N, -1, -1)) * d**(np.arange(0, N+1, 1))

    # Terminal payoffs
    if option_type == 'call':
        values = np.maximum(stock - K, 0)
    else:
        values = np.maximum(K - stock, 0)

    # Backward induction
    for i in range(N - 1, -1, -1):
        stock_i = S * u**(np.arange(i, -1, -1)) * d**(np.arange(0, i+1, 1))
        values = disc * (p * values[:-1] + (1 - p) * values[1:])

        if american:
            if option_type == 'call':
                intrinsic = np.maximum(stock_i - K, 0)
            else:
                intrinsic = np.maximum(K - stock_i, 0)
            values = np.maximum(values, intrinsic)

    return values[0]


# Early exercise premium
def early_exercise_premium(S, K, T, r, sigma, q=0, option_type='put'):
    """Compute the value of early exercise for American options."""
    european = binomial_tree(S, K, T, r, sigma, q, american=False, option_type=option_type)
    american = binomial_tree(S, K, T, r, sigma, q, american=True, option_type=option_type)
    return american - european
```

---

## Finite Difference Methods

Solve the [[Black-Scholes Model|Black-Scholes PDE]] directly on a grid:

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0$$

### Three Schemes

| Scheme | Stability | Accuracy | Speed |
|--------|-----------|----------|-------|
| **Explicit** | Conditional ($\Delta t < \Delta S^2 / \sigma^2 S^2$) | $O(\Delta t + \Delta S^2)$ | Fast |
| **Implicit** | Unconditional | $O(\Delta t + \Delta S^2)$ | Moderate |
| **Crank-Nicolson** | Unconditional | $O(\Delta t^2 + \Delta S^2)$ | Moderate |

### Crank-Nicolson Implementation
```python
def finite_difference_cn(S, K, T, r, sigma, q=0, N_time=500, N_space=200,
                          option_type='put', american=False, S_max=None):
    """
    Crank-Nicolson finite difference option pricer.

    Parameters:
        N_time: Number of time steps
        N_space: Number of stock price steps
    """
    if S_max is None:
        S_max = 4 * K  # Upper boundary

    dt = T / N_time
    dS = S_max / N_space
    S_grid = np.linspace(0, S_max, N_space + 1)

    # Terminal condition
    if option_type == 'call':
        V = np.maximum(S_grid - K, 0)
    else:
        V = np.maximum(K - S_grid, 0)

    # Tridiagonal matrix coefficients
    j = np.arange(1, N_space)
    alpha = 0.25 * dt * (sigma**2 * j**2 - (r - q) * j)
    beta = -0.5 * dt * (sigma**2 * j**2 + r)
    gamma_coef = 0.25 * dt * (sigma**2 * j**2 + (r - q) * j)

    # Build tridiagonal matrices
    # M1 * V_new = M2 * V_old (Crank-Nicolson)
    M1 = np.diag(1 - beta) + np.diag(-gamma_coef[:-1], 1) + np.diag(-alpha[1:], -1)
    M2 = np.diag(1 + beta) + np.diag(gamma_coef[:-1], 1) + np.diag(alpha[1:], -1)

    for i in range(N_time):
        # Boundary conditions
        if option_type == 'call':
            V[0] = 0
            V[-1] = S_max - K * np.exp(-r * (T - (i + 1) * dt))
        else:
            V[0] = K * np.exp(-r * (T - (i + 1) * dt))
            V[-1] = 0

        # Solve system
        rhs = M2 @ V[1:-1]
        rhs[0] += alpha[0] * (V[0])   # Boundary correction
        rhs[-1] += gamma_coef[-1] * (V[-1])
        V[1:-1] = np.linalg.solve(M1, rhs)

        # American exercise constraint
        if american:
            if option_type == 'call':
                V = np.maximum(V, S_grid - K)
            else:
                V = np.maximum(V, K - S_grid)

    # Interpolate to get price at S
    return np.interp(S, S_grid, V)
```

---

## Monte Carlo Pricing

Most flexible method — handles path-dependent and multi-asset options.

### Basic Framework
1. Simulate $N$ price paths under risk-neutral measure
2. Compute payoff for each path
3. Average and discount: $V_0 = e^{-rT} \frac{1}{N} \sum_{i=1}^{N} \text{payoff}_i$

```python
def monte_carlo_price(S, K, T, r, sigma, q=0, n_paths=100000, n_steps=252,
                       option_type='call', payoff_func=None):
    """
    Monte Carlo option pricer with variance reduction.

    Parameters:
        payoff_func: Custom payoff function(paths) for exotic options
                     Default: vanilla call/put
    """
    dt = T / n_steps
    # Antithetic variates for variance reduction
    Z = np.random.standard_normal((n_paths // 2, n_steps))
    Z = np.vstack([Z, -Z])  # Antithetic

    # Simulate paths (GBM)
    drift = (r - q - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt)
    log_returns = drift + diffusion * Z
    log_paths = np.log(S) + np.cumsum(log_returns, axis=1)
    paths = np.exp(log_paths)

    # Add initial price
    full_paths = np.column_stack([np.full(n_paths, S), paths])

    if payoff_func is not None:
        payoffs = payoff_func(full_paths)
    else:
        # Vanilla payoff
        S_T = paths[:, -1]
        if option_type == 'call':
            payoffs = np.maximum(S_T - K, 0)
        else:
            payoffs = np.maximum(K - S_T, 0)

    price = np.exp(-r * T) * np.mean(payoffs)
    std_err = np.exp(-r * T) * np.std(payoffs) / np.sqrt(n_paths)

    return {'price': price, 'std_error': std_err,
            '95_ci': (price - 1.96 * std_err, price + 1.96 * std_err)}


# --- Exotic Payoff Examples ---

def asian_call_payoff(K):
    """Arithmetic Asian call: payoff based on average price."""
    def payoff(paths):
        avg_price = np.mean(paths, axis=1)
        return np.maximum(avg_price - K, 0)
    return payoff

def barrier_call_payoff(K, barrier, barrier_type='down_and_out'):
    """Barrier option payoff."""
    def payoff(paths):
        S_T = paths[:, -1]
        if barrier_type == 'down_and_out':
            knocked = np.min(paths, axis=1) <= barrier
            pay = np.maximum(S_T - K, 0)
            pay[knocked] = 0
        elif barrier_type == 'up_and_out':
            knocked = np.max(paths, axis=1) >= barrier
            pay = np.maximum(S_T - K, 0)
            pay[knocked] = 0
        return pay
    return payoff

def lookback_call_payoff():
    """Lookback call: payoff based on max price."""
    def payoff(paths):
        S_max = np.max(paths, axis=1)
        S_T = paths[:, -1]
        return S_max - S_T  # Floating strike lookback
    return payoff
```

### Variance Reduction Techniques
| Technique | Speedup | Implementation |
|-----------|---------|----------------|
| **Antithetic variates** | ~2x | Use $Z$ and $-Z$ |
| **Control variates** | ~5-10x | Use BS price as control |
| **Importance sampling** | ~10x+ | Shift distribution toward payoff region |
| **Quasi-random (Sobol)** | ~3-5x | Replace pseudo-random with low-discrepancy |

---

## Method Selection Guide

| Option Type | Recommended Method |
|------------|-------------------|
| European vanilla | Black-Scholes (closed-form) |
| American vanilla | Binomial tree or FD |
| American with dividends | FD (Crank-Nicolson) |
| Asian (arithmetic) | Monte Carlo |
| Barrier | FD or Monte Carlo with correction |
| Lookback | Monte Carlo |
| Multi-asset basket | Monte Carlo |
| Heston/stoch vol European | FFT (characteristic function) |
| Exotic + early exercise | Longstaff-Schwartz MC |

---

## Related Notes
- [[Black-Scholes Model]] — Closed-form pricing foundation
- [[Greeks Deep Dive]] — Numerical Greeks from these methods
- [[Monte Carlo Simulation]] — MC methodology in detail
- [[Volatility Surface Modeling]] — Pricing with vol surface
- [[Options Strategies for Algos]] — Using prices for trading
- [[Stochastic Calculus]] — Mathematical foundations
- [[Mathematics MOC]] — Parent section
