# Interest Rate Models

Interest rate models (short-rate models) describe the stochastic evolution of the instantaneous short rate $r_t$. These models are critical for pricing bonds, interest rate derivatives, and managing interest rate risk.

---

## 1. Vasicek Model (1977)

The Vasicek model was the first to capture **mean reversion**, a key characteristic of interest rates.

### Stochastic Differential Equation (SDE)
$$dr_t = \kappa(	heta - r_t)dt + \sigma dW_t$$

Where:
- $\kappa$: Speed of mean reversion
- $	heta$: Long-term mean level
- $\sigma$: Instantaneous volatility
- $W_t$: Standard Brownian motion

### Properties
- **Mean Reversion:** If $r_t > 	heta$, the drift is negative; if $r_t < 	heta$, the drift is positive.
- **Normal Distribution:** $r_t$ is normally distributed.
- **Negative Rates:** The model allows $r_t$ to become negative (historically seen as a flaw, but relevant in modern regimes).
- **Analytical Solution:** Bond prices have a closed-form solution.

### Bond Pricing Formula
$$P(t, T) = A(t, T)e^{-B(t, T)r_t}$$
Where $B(t, T) = \frac{1 - e^{-\kappa(T-t)}}{\kappa}$ and $A(t, T)$ is a more complex function of the parameters.

---

## 2. Cox-Ingersoll-Ross (CIR) Model (1985)

The CIR model improves on Vasicek by ensuring rates remain non-negative.

### SDE
$$dr_t = \kappa(	heta - r_t)dt + \sigma\sqrt{r_t} dW_t$$

### Properties
- **Non-negativity:** The $\sqrt{r_t}$ term ensures that if $r_t$ reaches zero, the volatility drops to zero and the positive drift $\kappa	heta$ pulls it back up.
- **Feller Condition:** If $2\kappa	heta > \sigma^2$, the rate $r_t$ strictly stays above zero.
- **Non-central Chi-squared Distribution:** $r_t$ follows a non-central chi-squared distribution.
- **Analytical Solution:** Still allows for closed-form bond pricing.

---

## 3. Hull-White Model (Extended Vasicek)

The standard Vasicek and CIR models fail to fit the **initial term structure** (the current yield curve). Hull-White addresses this by making parameters time-dependent.

### SDE
$$dr_t = [	heta(t) - a r_t]dt + \sigma dW_t$$

Where $	heta(t)$ is a time-dependent drift chosen to match the initial yield curve exactly.

---

## 4. Heath-Jarrow-Morton (HJM) Framework

Instead of modeling the short rate, HJM models the **entire forward rate curve** simultaneously.

### SDE for Forward Rates
$$df(t, T) = \alpha(t, T)dt + \sigma(t, T)dW_t$$

The HJM framework is "market-consistent" by construction but can be high-dimensional and computationally expensive.

---

## Python Implementation: Simulating Vasicek and CIR

```python
import numpy as np
import matplotlib.pyplot as plt

def simulate_vasicek(r0, kappa, theta, sigma, T, dt):
    n_steps = int(T / dt)
    rates = np.zeros(n_steps)
    rates[0] = r0
    for i in range(1, n_steps):
        dr = kappa * (theta - rates[i-1]) * dt + sigma * np.sqrt(dt) * np.random.normal()
        rates[i] = rates[i-1] + dr
    return rates

def simulate_cir(r0, kappa, theta, sigma, T, dt):
    n_steps = int(T / dt)
    rates = np.zeros(n_steps)
    rates[0] = r0
    for i in range(1, n_steps):
        # Use max(rates[i-1], 0) to avoid sqrt of negative due to discretization
        dr = kappa * (theta - max(rates[i-1], 0)) * dt + 
             sigma * np.sqrt(max(rates[i-1], 0) * dt) * np.random.normal()
        rates[i] = rates[i-1] + dr
    return rates

# Parameters
r0, kappa, theta, sigma = 0.03, 0.5, 0.05, 0.02
T, dt = 10, 1/252

vasicek_path = simulate_vasicek(r0, kappa, theta, sigma, T, dt)
cir_path = simulate_cir(r0, kappa, theta, sigma, T, dt)

plt.figure(figsize=(10, 6))
plt.plot(vasicek_path, label='Vasicek')
plt.plot(cir_path, label='CIR')
plt.axhline(theta, color='red', linestyle='--', label='Long-term Mean')
plt.title('Short-Rate Model Simulations')
plt.legend()
plt.show()
```

---

## Related Notes
- [[Fixed Income]] — Context and bond pricing basics
- [[Stochastic Calculus]] — The math behind SDEs
- [[Monte Carlo Simulation]] — Using MC to price path-dependent options
- [[Derivatives Pricing]] — General pricing frameworks
- [[Mathematics MOC]] — Master navigation
