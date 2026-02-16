# Volatility Surface Modeling

The [[Black-Scholes Model]] assumes constant volatility across all strikes and expirations. Reality shows a **volatility surface** — implied vol varies by strike (smile/skew) and maturity (term structure). Modeling this surface is critical for [[Options Strategies for Algos|options trading]], [[Derivatives Pricing|exotic pricing]], and [[Greeks Deep Dive|accurate Greeks]].

---

## The Volatility Surface

### Three Dimensions
1. **Strike (K)** or **Moneyness (K/S)** or **Delta** — x-axis
2. **Time to Expiry (T)** — y-axis
3. **Implied Volatility ($\sigma_{impl}$)** — z-axis

### Stylized Facts

| Feature | Equities | FX | Commodities |
|---------|----------|-----|-------------|
| **Skew** | Steep downside skew | Mild smile | Varies |
| **Term Structure** | Inverted in crisis, upward in calm | Mild upward | Backwardation/contango |
| **Wings** | Left wing steep | Symmetric wings | Asymmetric |
| **ATM Level** | VIX ~15-20 normal | 5-15% for majors | 15-40% |

### Skew Metrics
- **25-delta risk reversal:** $\sigma_{25\Delta \text{call}} - \sigma_{25\Delta \text{put}}$ (skew direction)
- **25-delta butterfly:** $\frac{\sigma_{25\Delta \text{call}} + \sigma_{25\Delta \text{put}}}{2} - \sigma_{\text{ATM}}$ (smile curvature)
- **Skew slope:** $\frac{\partial \sigma}{\partial K}$ or $\frac{\partial \sigma}{\partial \delta}$

---

## Why the Smile Exists

1. **Crash risk / demand for protection:** Institutional investors buy OTM puts → drives up left wing IV
2. **Fat tails:** Real returns have excess kurtosis — BSM underprices tail events
3. **Leverage effect:** Stock drops → leverage increases → vol increases (negative spot-vol correlation)
4. **Jumps:** Discrete jumps in price (earnings, events) create smile
5. **Supply/demand:** Market makers charge more for illiquid wings

---

## Local Volatility Model (Dupire, 1994)

### Idea
Instead of constant $\sigma$, use a deterministic function $\sigma_{\text{loc}}(S, t)$ that exactly matches all market prices.

### Dupire's Formula
$$\sigma_{\text{loc}}^2(K, T) = \frac{\frac{\partial C}{\partial T} + (r-q)K\frac{\partial C}{\partial K} + qC}{\frac{1}{2}K^2 \frac{\partial^2 C}{\partial K^2}}$$

### Pros and Cons
| Pros | Cons |
|------|------|
| Exact fit to market prices | Forward smile dynamics are wrong |
| One-factor model (simple) | Smile flattens too fast for forward dates |
| Easy to implement with FD | Not suitable for barrier/exotic pricing |

---

## Stochastic Volatility Models

### Heston Model (1993)

The most widely used stochastic vol model:

$$dS = \mu S \, dt + \sqrt{v} S \, dW_1$$
$$dv = \kappa(\theta - v) \, dt + \xi \sqrt{v} \, dW_2$$
$$\text{corr}(dW_1, dW_2) = \rho$$

| Parameter | Meaning | Typical Value |
|-----------|---------|---------------|
| $\kappa$ | Mean reversion speed | 1-5 |
| $\theta$ | Long-run variance | $(0.20)^2 = 0.04$ |
| $\xi$ | Vol of vol | 0.3-1.0 |
| $\rho$ | Spot-vol correlation | -0.7 (equities) |
| $v_0$ | Initial variance | Current ATM IV squared |

**Key property:** $\rho < 0$ generates downside skew (spot down → vol up).

### Heston Calibration (Characteristic Function)
```python
import numpy as np
from scipy.optimize import minimize

def heston_char_func(u, S, K, T, r, q, v0, kappa, theta, xi, rho):
    """
    Heston model characteristic function for pricing via FFT.
    """
    d = np.sqrt((rho * xi * 1j * u - kappa)**2 +
                xi**2 * (1j * u + u**2))
    g = (kappa - rho * xi * 1j * u - d) / \
        (kappa - rho * xi * 1j * u + d)

    C = (r - q) * 1j * u * T + \
        (kappa * theta / xi**2) * \
        ((kappa - rho * xi * 1j * u - d) * T -
         2 * np.log((1 - g * np.exp(-d * T)) / (1 - g)))

    D = ((kappa - rho * xi * 1j * u - d) / xi**2) * \
        ((1 - np.exp(-d * T)) / (1 - g * np.exp(-d * T)))

    return np.exp(C + D * v0 + 1j * u * np.log(S))


def heston_price_fft(S, K, T, r, q, v0, kappa, theta, xi, rho, N=4096, alpha=1.5):
    """
    Price European options using Heston + FFT (Carr-Madan method).
    """
    dk = 2 * np.pi / N
    b = N * dk / 2

    # Log-strike grid
    ku = -b + dk * np.arange(N)

    # FFT input
    dv = 2 * np.pi / (N * dk)
    v = dv * np.arange(N)

    # Modified characteristic function
    def psi(v):
        cf = heston_char_func(v - (alpha + 1) * 1j, S, K, T, r, q,
                               v0, kappa, theta, xi, rho)
        denom = alpha**2 + alpha - v**2 + 1j * (2 * alpha + 1) * v
        return np.exp(-r * T) * cf / denom

    # Simpson weights
    w = np.ones(N)
    w[0] = 0.5
    w = w * dv * np.exp(-1j * v * ku[0])

    # FFT
    fft_input = psi(v) * w
    fft_result = np.fft.fft(fft_input).real

    # Extract call prices
    call_prices = np.exp(-alpha * ku) * fft_result / np.pi

    # Interpolate to desired strike
    log_K = np.log(K)
    idx = int((log_K + b) / dk)
    if 0 <= idx < N - 1:
        w_interp = (log_K - ku[idx]) / dk
        return call_prices[idx] * (1 - w_interp) + call_prices[idx + 1] * w_interp
    return np.nan
```

---

## SABR Model (Hagan et al., 2002)

The standard model for interest rate options (swaptions, caps). Also used in FX.

$$dF = \alpha F^\beta \, dW_1$$
$$d\alpha = \nu \alpha \, dW_2$$
$$\text{corr}(dW_1, dW_2) = \rho$$

| Parameter | Meaning | Controls |
|-----------|---------|----------|
| $\alpha$ | Initial vol level | ATM vol level |
| $\beta$ | CEV exponent (0-1) | Backbone (skew from leverage) |
| $\nu$ | Vol of vol | Smile curvature (wings) |
| $\rho$ | Correlation | Skew direction |

### SABR Implied Vol Approximation (Hagan's formula)
```python
def sabr_vol(F, K, T, alpha, beta, rho, nu):
    """
    Hagan's SABR implied volatility approximation.

    Parameters:
        F: Forward price
        K: Strike
        T: Time to expiry
        alpha: Vol level
        beta: CEV exponent
        rho: Correlation
        nu: Vol of vol
    """
    if abs(F - K) < 1e-12:
        # ATM formula
        FK_mid = F
        logFK = 0
    else:
        FK_mid = (F * K)**((1 - beta) / 2)
        logFK = np.log(F / K)

    A = alpha / (FK_mid * (1 + (1 - beta)**2 / 24 * logFK**2 +
                           (1 - beta)**4 / 1920 * logFK**4))

    B = 1 + T * ((1 - beta)**2 / 24 * alpha**2 / FK_mid**2 +
                  rho * beta * nu * alpha / (4 * FK_mid) +
                  (2 - 3 * rho**2) * nu**2 / 24)

    if abs(F - K) < 1e-12:
        return alpha * B / F**(1 - beta)

    z = nu * FK_mid / alpha * logFK
    x = np.log((np.sqrt(1 - 2 * rho * z + z**2) + z - rho) / (1 - rho))

    if abs(x) < 1e-12:
        return A * B
    return A * z / x * B
```

---

## SVI Parameterization (Gatheral, 2004)

A simple, arbitrage-free parameterization of the total implied variance $w(k) = \sigma^2(k) T$ as a function of log-moneyness $k = \ln(K/F)$.

$$w(k) = a + b \left(\rho(k - m) + \sqrt{(k - m)^2 + \sigma^2}\right)$$

| Parameter | Controls |
|-----------|----------|
| $a$ | Overall variance level |
| $b$ | Slope (angle of wings) |
| $\rho$ | Skew/asymmetry |
| $m$ | Translation (shift left/right) |
| $\sigma$ | Curvature (ATM smoothness) |

### Why SVI?
- Only 5 parameters per slice
- Easy to calibrate (fits market well)
- Can enforce no-butterfly-arbitrage constraints
- Standard at many vol desks

```python
def svi_total_variance(k, a, b, rho, m, sigma):
    """SVI total implied variance w(k) = sigma^2 * T."""
    return a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))

def svi_implied_vol(k, T, a, b, rho, m, sigma):
    """Convert SVI total variance to implied vol."""
    w = svi_total_variance(k, a, b, rho, m, sigma)
    return np.sqrt(np.maximum(w / T, 0))

def calibrate_svi(strikes, market_vols, F, T):
    """Calibrate SVI to a single expiry slice."""
    k = np.log(strikes / F)
    market_w = market_vols**2 * T

    def objective(params):
        a, b, rho, m, sigma = params
        model_w = svi_total_variance(k, a, b, rho, m, sigma)
        return np.sum((model_w - market_w)**2)

    # Bounds: b>0, -1<rho<1, sigma>0
    from scipy.optimize import minimize
    result = minimize(objective, x0=[0.04, 0.1, -0.3, 0.0, 0.1],
                      bounds=[(None, None), (0, None), (-0.999, 0.999),
                              (None, None), (1e-6, None)])
    return dict(zip(['a', 'b', 'rho', 'm', 'sigma'], result.x))
```

---

## Local Vol vs Stochastic Vol vs Jump Models

| Feature | Local Vol | Stochastic Vol (Heston) | Jump-Diffusion |
|---------|-----------|------------------------|----------------|
| Fits market smile? | Exact | Approximate | Approximate |
| Forward smile? | Too flat | Realistic | Realistic for short dates |
| Calibration | Easy (Dupire) | Moderate (FFT) | Hard |
| Exotic pricing | Poor | Good | Good for barriers |
| Hedging Greeks | Wrong dynamics | Better | Best for jumps |
| Parameters | $\sigma(K,T)$ surface | 5 params | 5+ params |

**Industry practice:**
- **Vanilla pricing/quoting:** SABR or SVI (fast, simple)
- **Exotic pricing:** Stochastic local vol (SLV) = best of both worlds
- **Risk management:** Heston for scenario analysis
- **Skew trading:** SABR for swaptions, SVI for equities

---

## Related Notes
- [[Black-Scholes Model]] — The constant-vol baseline
- [[Greeks Deep Dive]] — Accurate Greeks require the vol surface
- [[GARCH Models]] — Econometric vol forecasting
- [[Volatility Trading]] — Trading the surface
- [[Options Strategies for Algos]] — Algorithmic strategies on vol
- [[Stochastic Calculus]] — SDEs underlying the models
- [[Mathematics MOC]] — Parent section
