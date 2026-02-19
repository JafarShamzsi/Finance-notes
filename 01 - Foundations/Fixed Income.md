# Fixed Income

Fixed income is the largest asset class by market value (~$130 trillion globally). Understanding bond math, yield curves, and interest rate models is essential for quant finance — many strategies trade rates directly, and all strategies are affected by the rate environment.

---

## Bond Pricing Fundamentals

### Present Value of Cash Flows
$$P = \sum_{i=1}^{n} \frac{C_i}{(1 + y)^{t_i}} + \frac{F}{(1 + y)^{T}}$$

Where:
- $C_i$ = coupon payment at time $t_i$
- $F$ = face value (par, typically $1000)
- $y$ = yield to maturity (YTM)
- $T$ = maturity

```python
import numpy as np

def bond_price(face, coupon_rate, ytm, years, freq=2):
    """
    Price a fixed-rate bond.

    Parameters:
        face: Face value
        coupon_rate: Annual coupon rate (e.g., 0.05 for 5%)
        ytm: Yield to maturity (annual)
        years: Years to maturity
        freq: Coupon frequency (2=semi-annual)
    """
    n_periods = int(years * freq)
    coupon = face * coupon_rate / freq
    y_per = ytm / freq

    # PV of coupons
    pv_coupons = coupon * (1 - (1 + y_per)**(-n_periods)) / y_per
    # PV of face
    pv_face = face / (1 + y_per)**n_periods

    return pv_coupons + pv_face
```

---

## Yield Curve

The yield curve plots yields against maturities. It's the most important macro indicator for quants.

### shapes
| Shape | Meaning | Historical Frequency |
|-------|---------|---------------------|
| **Normal (upward)** | Economy expanding, positive term premium | ~70% of time |
| **Flat** | Transition, uncertainty | ~15% |
| **Inverted** | Recession signal (3M > 10Y) | ~15% |
| **Humped** | Mixed signals, policy transition | Rare |

### Yield Curve Modeling (Fitting)
Beyond simple linear interpolation, quants use parametric models to fit the entire curve to market data.

#### 1. Nelson-Siegel (1987)
A 3-factor model (Level, Slope, Curvature):
$$y(T) = \beta_0 + \beta_1 \frac{1 - e^{-\lambda T}}{\lambda T} + \beta_2 \left( \frac{1 - e^{-\lambda T}}{\lambda T} - e^{-\lambda T} \right)$$
- $\beta_0$: Long-term level
- $\beta_1$: Short-term slope
- $\beta_2$: Medium-term curvature

#### 2. Nelson-Siegel-Svensson (1994)
Adds a fourth term (second curvature factor) for more flexibility in the long end:
$$y(T) = \beta_0 + \beta_1 \frac{1 - e^{-\lambda_1 T}}{\lambda_1 T} + \beta_2 \left( \frac{1 - e^{-\lambda_1 T}}{\lambda_1 T} - e^{-\lambda_1 T} \right) + \beta_3 \left( \frac{1 - e^{-\lambda_2 T}}{\lambda_2 T} - e^{-\lambda_2 T} \right)$$

### Key Spreads
| Spread | Formula | What It Signals |
|--------|---------|----------------|
| **2s10s** | 10Y - 2Y yield | Business cycle (inversion = recession) |
| **3m10y** | 10Y - 3M yield | Fed vs. market (most predictive) |
| **TED spread** | 3M LIBOR - 3M T-bill | Credit/liquidity stress |
| **OAS** | Spread over Treasury curve | Credit risk of corporates |

### Bootstrapping the Zero Curve
```python
def bootstrap_zero_curve(par_yields, maturities):
    """
    Bootstrap zero-coupon rates from par yields.

    Parameters:
        par_yields: Array of par yields (annual, semi-annual coupons)
        maturities: Array of maturities in years
    """
    zero_rates = np.zeros_like(par_yields)

    for i, (y, T) in enumerate(zip(par_yields, maturities)):
        n = int(T * 2)  # Semi-annual periods
        coupon = y / 2

        # PV of known coupons using already-bootstrapped zero rates
        pv_coupons = 0
        for j in range(n - 1):
            t_j = (j + 1) / 2
            # Interpolate zero rate for this maturity
            if t_j <= maturities[0]:
                z = zero_rates[0]
            else:
                z = np.interp(t_j, maturities[:i+1], zero_rates[:i+1])
            pv_coupons += coupon / (1 + z / 2)**(j + 1)

        # Solve for zero rate at maturity T
        # 1 = pv_coupons + (1 + coupon) / (1 + z_T/2)^n
        remaining = 1 - pv_coupons
        zero_rates[i] = 2 * ((1 + coupon) / remaining)**(1 / n) - 2

    return zero_rates
```

---

## Duration and Convexity

### Macaulay Duration
Weighted average time to receive cash flows:
$$D_{\text{Mac}} = \frac{1}{P} \sum_{i=1}^{n} t_i \frac{C_i}{(1+y)^{t_i}}$$

### Modified Duration
$$D_{\text{mod}} = \frac{D_{\text{Mac}}}{1 + y/f}$$

**Price sensitivity:** $\Delta P \approx -D_{\text{mod}} \times P \times \Delta y$

### Convexity
Second-order price sensitivity:
$$C = \frac{1}{P} \sum_{i=1}^{n} \frac{t_i(t_i + 1) C_i}{(1+y)^{t_i+2}}$$

**Better price approximation:**
$$\frac{\Delta P}{P} \approx -D_{\text{mod}} \cdot \Delta y + \frac{1}{2} C \cdot (\Delta y)^2$$

```python
def duration_convexity(face, coupon_rate, ytm, years, freq=2):
    """Compute modified duration and convexity."""
    n = int(years * freq)
    c = face * coupon_rate / freq
    y = ytm / freq
    price = bond_price(face, coupon_rate, ytm, years, freq)

    mac_dur = 0
    convexity = 0

    for i in range(1, n + 1):
        t = i / freq
        cf = c if i < n else c + face
        pv = cf / (1 + y)**i

        mac_dur += t * pv
        convexity += t * (t + 1/freq) * pv

    mac_dur /= price
    mod_dur = mac_dur / (1 + y)
    convexity /= (price * (1 + y)**2)

    return {
        'macaulay_duration': mac_dur,
        'modified_duration': mod_dur,
        'convexity': convexity,
        'dv01': mod_dur * price / 10000  # Dollar value of 1bp
    }
```

---

## Interest Rate Models

See [[Interest Rate Models]] for mathematical details.

### Short-Rate Models

| Model | SDE | Features |
|-------|-----|----------|
| **Vasicek (1977)** | $dr = \kappa(\theta - r)dt + \sigma dW$ | Mean-reverting, can go negative |
| **CIR (1985)** | $dr = \kappa(\theta - r)dt + \sigma\sqrt{r}dW$ | Mean-reverting, non-negative |
| **Hull-White (1990)** | $dr = (\theta(t) - ar)dt + \sigma dW$ | Time-varying, fits term structure |

### Heath-Jarrow-Morton (HJM) Framework
Models the entire forward rate curve:
$$df(t,T) = \alpha(t,T)dt + \sigma(t,T)dW_t$$

No-arbitrage condition determines drift from volatility:
$$\alpha(t,T) = \sigma(t,T) \int_t^T \sigma(t,s)ds$$

---

## Fixed Income Strategies for Quants

### 1. Curve Trading
- **Steepener:** Long short-end, short long-end (profit from curve steepening)
- **Flattener:** Opposite — profit from curve flattening
- **Butterfly:** Long 2Y and 30Y, short 10Y (curvature trade)

### 2. Carry Trade
- Borrow at low short rates, invest at higher long rates
- Positive carry if curve is upward sloping
- Risk: curve inversion, rate spikes

### 3. Relative Value
- Trade mispricings between similar bonds (on-the-run vs off-the-run)
- Treasury basis trades (cash vs futures)
- See [[Statistical Arbitrage]] for methodology

### 4. Duration Targeting
- Maintain constant portfolio duration
- Rebalance as yields change
- Foundation of many systematic bond strategies

---

## Key Metrics Quick Reference

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **YTM** | IRR of bond cash flows | Expected return if held to maturity |
| **Current Yield** | Annual coupon / Price | Income yield only |
| **DV01** | $D_{\text{mod}} \times P / 10000$ | Dollar P&L per 1bp rate move |
| **BPV** | Same as DV01 | Basis point value |
| **OAS** | Spread over Treasury (option-adjusted) | Credit compensation |
| **Z-spread** | Constant spread over zero curve | Simple credit measure |

---

## Related Notes
- [[Asset Classes]] — Fixed income as an asset class
- [[Financial Markets Overview]] — Market structure
- [[Stochastic Calculus]] — Rate model mathematics
- [[Monte Carlo Simulation]] — MC for rate modeling
- [[Portfolio Optimization]] — Fixed income portfolio construction
- [[Risk Parity]] — Bond allocation in risk parity
- [[Mathematics MOC]] — Mathematical foundations
- [[Trading Algorithms Master Index]] — Master navigation
