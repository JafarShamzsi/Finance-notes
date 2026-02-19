# Volatility Surface Modeling

The **Volatility Surface** $\sigma(K, T)$ is a 3D plot of implied volatility against strike price ($K$) and time to maturity ($T$). In the Black-Scholes world, this surface should be flat. In reality, it exhibits a "smile" or "skew" and a term structure.

Modeling this surface accurately is the "Holy Grail" of derivatives pricing.

---

## 1. The Implied Volatility Smile

- **Skew:** OTM puts typically trade at higher implied vols than OTM calls (in equities). This reflects the market's fear of crashes (fat tails).
- **Smile:** In FX, both OTM calls and puts trade at a premium, reflecting the risk of large moves in either direction.
- **Term Structure:** Volatility tends to mean-revert. Short-term vol is more variable than long-term vol.

---

## 2. Local Volatility (Dupire, 1994)

Dupire showed that if we have a complete set of European option prices, there exists a unique local volatility function $\sigma_{loc}(S, t)$ that recovers these prices exactly.

### Dupire's Formula
$$\sigma_{loc}^2(K, T) = \frac{\frac{\partial C}{\partial T} + rK\frac{\partial C}{\partial K}}{K^2 \frac{\partial^2 C}{\partial K^2}}$$

- **Pros:** Fits the market prices exactly (by construction).
- **Cons:** Dynamics are unrealistic (volatility moves in the opposite direction of the asset price). "Sticky strike" behavior.

---

## 3. Stochastic Volatility (Heston, 1993)

Assumes volatility itself is a stochastic process.

### Heston Model SDEs
$$dS_t = \mu S_t dt + \sqrt{v_t} S_t dW_t^S$$
$$dv_t = \kappa(\theta - v_t)dt + \xi \sqrt{v_t} dW_t^v$$
$$dW_t^S dW_t^v = \rho dt$$

- $\kappa$: Mean reversion speed
- $\theta$: Long-run variance
- $\xi$: Volatility of volatility (Vol of Vol)
- $\rho$: Correlation between spot and vol (typically negative for equities -> leverage effect)

---

## 4. SABR Model (Hagan et al., 2002)

The industry standard for **Interest Rate Options** (Swaptions, Caps/Floors) and widely used for interpolation.

### SDEs
$$dF_t = \alpha_t F_t^\beta dW_t^1$$
$$d\alpha_t = \nu \alpha_t dW_t^2$$

- $\alpha$: Initial volatility level (ATM vol)
- $\beta$: CEV elasticity parameter ($0 \le \beta \le 1$). Determines backbone.
- $\rho$: Correlation (skew)
- $\nu$: Vol of vol (curvature/smile)

### Why SABR?
It provides an approximate closed-form solution for implied volatility $\sigma_{imp}(K, F)$, making calibration extremely fast.

---

## 5. SVI (Stochastic Volatility Inspired)

A parametric model popular for **Equity Surfaces** (Jim Gatheral). It guarantees no arbitrage (mostly) and fits equity skews well.

### Raw SVI Parametrization
$$w(k) = a + b \{ \rho(k - m) + \sqrt{(k - m)^2 + \sigma^2} \}$$

Where $w(k) = \sigma_{BS}^2(k)T$ is total variance, and $k = \ln(K/F)$ is log-moneyness.

- **a**: Vertical shift (level)
- **b**: Slope of wings
- **rho**: Rotation (skew)
- **m**: Horizontal shift
- **sigma**: Curvature (smoothing at ATM)

---

## Python Implementation: SABR Volatility

```python
import numpy as np

def sabr_vol(K, F, T, alpha, beta, rho, vol_of_vol):
    """
    Hagan's 2002 SABR Log-normal Volatility Approximation.
    """
    # Log-moneyness
    if K <= 0 or F <= 0: return 0.0
    
    # Handle ATM case to avoid division by zero
    if abs(F - K) < 1e-5:
        term1 = alpha / (F**(1-beta))
        term2 = 1 + (((1-beta)**2)/24 * alpha**2 / (F**(2-2*beta)) + 
                     (rho * beta * vol_of_vol * alpha) / (4 * F**(1-beta)) + 
                     (2 - 3*rho**2)/24 * vol_of_vol**2) * T
        return term1 * term2

    z = (vol_of_vol / alpha) * (F * K)**((1 - beta) / 2) * np.log(F / K)
    x = np.log((np.sqrt(1 - 2 * rho * z + z**2) + z - rho) / (1 - rho))
    
    term1 = alpha / ((F * K)**((1 - beta) / 2) * (1 + (1 - beta)**2 / 24 * np.log(F / K)**2 + (1 - beta)**4 / 1920 * np.log(F / K)**4))
    
    if abs(x) < 1e-5: # Avoid division by zero
        term2 = 1
    else:
        term2 = z / x
        
    term3 = 1 + (((1 - beta)**2 / 24) * alpha**2 / ((F * K)**(1 - beta)) + (rho * beta * vol_of_vol * alpha) / (4 * (F * K)**((1 - beta) / 2)) + (2 - 3 * rho**2) / 24 * vol_of_vol**2) * T
    
    return term1 * term2 * term3

# Example usage
alpha = 0.2  # ATM vol
beta = 0.5   # CEV param
rho = -0.3   # Skew
nu = 0.4     # Vol of Vol
T = 1.0
F = 100
Strikes = [80, 90, 100, 110, 120]

vols = [sabr_vol(k, F, T, alpha, beta, rho, nu) for k in Strikes]
print(f"Strikes: {Strikes}")
print(f"SABR Vols: {np.round(vols, 4)}")
```

---

## Related Notes
- [[Black-Scholes Model]] — The base model
- [[Greeks Deep Dive]] — Managing the risks of the surface
- [[Option Pricing.py]] — Code implementation
- [[Fixed Income]] — SABR is standard for rates
- [[Derivatives Pricing]] — General pricing context
