# Stochastic Calculus

The mathematical language of continuous-time finance. Essential for options pricing, risk modeling, and understanding market dynamics.

---

## Brownian Motion (Wiener Process)

A continuous-time random walk:

```
Properties:
  W(0) = 0
  W(t) - W(s) ~ N(0, t-s)   for t > s
  Increments are independent
  Paths are continuous but nowhere differentiable
```

```python
def simulate_brownian_motion(T=1, N=1000, n_paths=5):
    dt = T / N
    dW = np.random.normal(0, np.sqrt(dt), (n_paths, N))
    W = np.cumsum(dW, axis=1)
    W = np.insert(W, 0, 0, axis=1)  # W(0) = 0
    return W
```

## Geometric Brownian Motion (GBM)

The standard model for stock prices:

```
dS = μ·S·dt + σ·S·dW

Solution:
S(t) = S(0) · exp((μ - σ²/2)·t + σ·W(t))

Where:
  S = stock price
  μ = drift (expected return)
  σ = volatility
  W = Brownian motion
```

```python
def simulate_gbm(S0, mu, sigma, T, N, n_paths=1000):
    """
    Simulate stock price paths using GBM.
    """
    dt = T / N
    Z = np.random.standard_normal((n_paths, N))
    paths = np.zeros((n_paths, N + 1))
    paths[:, 0] = S0

    for i in range(N):
        paths[:, i+1] = paths[:, i] * np.exp(
            (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, i]
        )
    return paths
```

## Itô's Lemma

The chain rule of stochastic calculus. If `f(S,t)` is a function of a stochastic process S:

```
df = (∂f/∂t + μS·∂f/∂S + ½σ²S²·∂²f/∂S²)dt + σS·∂f/∂S·dW
```

**Application:** Deriving Black-Scholes. Let `f = ln(S)`:
```
d(ln S) = (μ - σ²/2)dt + σ·dW
```

This shows that log prices follow arithmetic Brownian motion with drift `μ - σ²/2`.

## Stochastic Differential Equations (SDEs)

### Mean-Reverting (Ornstein-Uhlenbeck)
```
dX = θ(μ - X)dt + σdW

Used for: [[Mean Reversion Strategies]], [[Pairs Trading]] spread modeling
```

### Cox-Ingersoll-Ross (CIR)
```
dr = κ(θ - r)dt + σ√r·dW

Used for: Interest rate modeling (always positive)
```

### Heston Stochastic Volatility
```
dS = μ·S·dt + √v·S·dW₁
dv = κ(θ - v)dt + σ_v·√v·dW₂

Corr(dW₁, dW₂) = ρ

Used for: Options pricing with volatility smile
```

## Connection to Options Pricing

Black-Scholes equation (from Itô's lemma + no-arbitrage):
```
∂V/∂t + ½σ²S²·∂²V/∂S² + rS·∂V/∂S - rV = 0
```

This PDE, with boundary conditions, gives option prices.

See [[Options Strategies for Algos]] for practical applications.

---

**Related:** [[Mathematics MOC]] | [[Monte Carlo Simulation]] | [[Options Strategies for Algos]] | [[Probability and Statistics for Trading]]
