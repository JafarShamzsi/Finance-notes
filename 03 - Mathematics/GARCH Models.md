# GARCH Models

Generalized Autoregressive Conditional Heteroskedasticity (GARCH) models are the workhorse of volatility forecasting in quantitative finance. They capture the key stylized facts of financial returns: **volatility clustering**, **mean reversion**, and **fat tails**.

---

## Why GARCH?

Financial returns exhibit:
1. **Volatility clustering:** Large moves follow large moves, small follow small
2. **Mean reversion of variance:** Vol spikes but eventually returns to a long-run level
3. **Leverage effect:** Negative returns increase vol more than positive returns
4. **Fat tails:** Returns have excess kurtosis even after conditioning on vol

GARCH captures (1) and (2). Extensions handle (3) and (4).

---

## GARCH(1,1) — The Baseline

### Model
$$r_t = \mu + \epsilon_t, \quad \epsilon_t = \sigma_t z_t, \quad z_t \sim N(0,1)$$

$$\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

| Parameter | Meaning | Typical Range |
|-----------|---------|---------------|
| $\omega$ | Constant (baseline variance) | Small positive |
| $\alpha$ | Shock impact (yesterday's squared return) | 0.05 - 0.15 |
| $\beta$ | Persistence (yesterday's variance) | 0.80 - 0.95 |
| $\alpha + \beta$ | Total persistence | < 1 for stationarity |

### Long-Run Variance
$$\bar{\sigma}^2 = \frac{\omega}{1 - \alpha - \beta}$$

### Half-Life of Vol Shocks
$$\text{half-life} = \frac{\ln(2)}{-\ln(\alpha + \beta)}$$

If $\alpha + \beta = 0.97$, half-life $\approx 23$ days.

### Key Insight
**GARCH(1,1) explains ~95% of conditional variance dynamics.** Higher-order models rarely add value.

---

## EGARCH — Exponential GARCH (Nelson, 1991)

Captures the **leverage effect** — negative returns increase vol more than positive returns.

### Model
$$\ln(\sigma_t^2) = \omega + \alpha\left(\frac{|\epsilon_{t-1}|}{\sigma_{t-1}} - \sqrt{2/\pi}\right) + \gamma \frac{\epsilon_{t-1}}{\sigma_{t-1}} + \beta \ln(\sigma_{t-1}^2)$$

| Feature | GARCH(1,1) | EGARCH |
|---------|-----------|--------|
| Leverage effect | No | Yes ($\gamma < 0$) |
| Positivity constraint | Required ($\omega, \alpha, \beta > 0$) | Not needed (log variance) |
| Asymmetry | Symmetric | Asymmetric |

**When to use:** Equity indices where drops cause vol spikes (S&P 500, VIX dynamics).

---

## GJR-GARCH (Glosten, Jagannathan, Runkle, 1993)

Another asymmetric model, simpler than EGARCH:

$$\sigma_t^2 = \omega + (\alpha + \gamma \mathbb{1}_{\epsilon_{t-1}<0}) \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

Where $\mathbb{1}_{\epsilon_{t-1}<0}$ is 1 when the return is negative.

- $\gamma > 0$ means negative shocks have bigger impact on vol
- Common for equity markets ($\gamma \approx 0.05-0.15$)

---

## GARCH with Different Distributions

Standard GARCH assumes $z_t \sim N(0,1)$. Better alternatives:

| Distribution | Captures | Use Case |
|-------------|----------|----------|
| **Student-t** | Fat tails (kurtosis) | General purpose, most common |
| **Skewed-t** | Fat tails + asymmetry | Equity returns |
| **GED** | Generalized error distribution | Flexible tail weight |

Student-t with $\nu \approx 5-8$ degrees of freedom typically fits financial data well.

---

## Python Implementation

```python
import numpy as np
import pandas as pd
from arch import arch_model

def fit_garch(returns, model_type='GARCH', vol_type='GARCH', dist='t', p=1, q=1):
    """
    Fit a GARCH family model.

    Parameters:
        returns: pd.Series of percentage returns (e.g., 100 * log returns)
        model_type: 'GARCH', 'EGARCH', or 'GJR-GARCH'
        dist: 't' (Student-t), 'normal', 'skewt'
        p, q: GARCH order

    Returns:
        Fitted model result
    """
    if model_type == 'EGARCH':
        vol = 'EGARCH'
    elif model_type == 'GJR-GARCH':
        vol = 'GARCH'
        # GJR uses o=1 parameter
        am = arch_model(returns, vol=vol, p=p, o=1, q=q, dist=dist)
    else:
        vol = 'GARCH'
        am = arch_model(returns, vol=vol, p=p, q=q, dist=dist)

    if model_type != 'GJR-GARCH':
        am = arch_model(returns, vol=vol, p=p, q=q, dist=dist)

    result = am.fit(disp='off')
    return result


def forecast_volatility(returns, horizon=22, model_type='GARCH'):
    """
    Forecast volatility for the next `horizon` days.

    Parameters:
        returns: pd.Series of daily returns (as percentages)
        horizon: Number of days to forecast
        model_type: GARCH variant

    Returns:
        Annualized volatility forecast
    """
    result = fit_garch(returns, model_type=model_type)

    # Multi-step forecast
    forecasts = result.forecast(horizon=horizon)
    variance_forecast = forecasts.variance.iloc[-1].values  # Daily variances

    # Annualize: sqrt(252 * mean daily variance)
    annual_vol = np.sqrt(252 * np.mean(variance_forecast)) / 100
    return annual_vol, result


def garch_vol_cone(returns, windows=[21, 63, 126, 252]):
    """
    Compute realized vol cone to compare with GARCH forecast.
    Useful for identifying rich/cheap vol regimes.
    """
    cone = {}
    for w in windows:
        rv = returns.rolling(w).std() * np.sqrt(252)
        cone[f'{w}d'] = {
            'current': rv.iloc[-1],
            'percentile': (rv < rv.iloc[-1]).mean(),
            'min': rv.min(),
            'max': rv.max(),
            'median': rv.median()
        }
    return pd.DataFrame(cone).T


# --- Example Usage ---
if __name__ == '__main__':
    # Simulate or load returns
    np.random.seed(42)
    returns = pd.Series(np.random.normal(0, 1, 2520))  # ~10 years daily

    # Fit different models
    for model in ['GARCH', 'EGARCH', 'GJR-GARCH']:
        result = fit_garch(returns * 100, model_type=model)
        print(f"\n=== {model} ===")
        print(result.summary().tables[1])
```

---

## GARCH for Trading Applications

### 1. Volatility Forecasting for Options
Compare GARCH forecast to implied vol:
- **GARCH forecast > IV** → Buy options (vol is cheap)
- **GARCH forecast < IV** → Sell options (vol is rich)
- See [[Volatility Trading]] for implementation

### 2. Dynamic Position Sizing
Scale position size inversely with GARCH vol:
$$\text{Position Size} = \frac{\text{Target Vol}}{\hat{\sigma}_t^{\text{GARCH}}}$$
See [[Position Sizing]] and [[Risk Management MOC]].

### 3. Regime Detection
High persistence ($\alpha + \beta > 0.98$) → volatile regime. Use with [[Regime Detection]].

### 4. VaR Estimation
GARCH-based VaR is more responsive than historical VaR:
$$\text{VaR}_{99\%} = \hat{\sigma}_t \times z_{0.01}$$
See [[Value at Risk (VaR)]].

---

## Model Comparison

| Criterion | GARCH(1,1) | EGARCH | GJR-GARCH |
|-----------|-----------|--------|-----------|
| **Simplicity** | Best | Moderate | Good |
| **Leverage effect** | No | Yes | Yes |
| **Positivity guaranteed** | With constraints | Always (log) | With constraints |
| **AIC/BIC (typical)** | Baseline | Often best | Close to EGARCH |
| **Industry use** | Universal | Equity, FX | Equity |

**Practical recommendation:** Start with GARCH(1,1)-t. If equity/index, use GJR-GARCH-t. Check EGARCH for comparison. Higher orders (2,1) or (1,2) rarely improve.

---

## Related Notes
- [[Time Series Analysis]] — ARIMA and stationarity foundations
- [[Volatility Surface Modeling]] — Implied vol modeling
- [[Black-Scholes Model]] — Constant vol assumption GARCH replaces
- [[Volatility Trading]] — Trading vol with GARCH forecasts
- [[Value at Risk (VaR)]] — GARCH-based VaR
- [[Regime Detection]] — Detecting vol regime changes
- [[Risk Management MOC]] — Volatility for risk management
- [[Mathematics MOC]] — Parent section
