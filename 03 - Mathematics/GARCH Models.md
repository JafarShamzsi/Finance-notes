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

## Interpreting Model Output

When you fit a GARCH model using the `arch` library, the `summary()` method provides a wealth of information. Here is how to interpret the key parts of the parameters table:

| Column | Meaning | What to Look For |
|---|---|---|
| **coef** | The estimated value for the parameter ($\omega, \alpha, \beta, \gamma$, etc.). | - $\alpha + \beta < 1$ for GARCH(1,1) for stationarity. <br> - For GJR-GARCH, $\alpha + \beta + \gamma/2 < 1$ is the stationarity condition. <br> - $\gamma > 0$ in GJR or $\gamma < 0$ in EGARCH confirms the leverage effect. |
| **std err** | The standard error of the coefficient estimate. A measure of the estimate's uncertainty. | Smaller values are better, indicating a more precise estimate. |
| **t** | The t-statistic, calculated as `coef / std err`. | A measure of how statistically significant the parameter is. |
| **P>|t|** | The p-value associated with the t-statistic. | A p-value **< 0.05** (or < 0.01 for stricter tests) indicates that the parameter is statistically significant and should be kept in the model. If a parameter like $\alpha$ is not significant, a simpler ARCH or constant variance model might be better. |
| **[0.025** | The lower bound of the 95% confidence interval for the coefficient. | The interval should not contain zero for a parameter to be considered significant. |
| **0.975]** | The upper bound of the 95% confidence interval for the coefficient. | --- |

**Example Analysis:**
If a GJR-GARCH model shows a `gamma` coefficient of `0.08` with a p-value of `0.002`, you can conclude:
1.  The leverage effect is present and statistically significant.
2.  The impact of a negative shock on next-day variance is `0.08 * (return)^2` larger than a positive shock of the same magnitude.

---

## Understanding Multi-Step Forecasting

The power of GARCH lies in its ability to forecast future variance. A one-step-ahead forecast is trivial from the model equation. For multi-step forecasts ($h > 1$), we iterate forward.

For a GARCH(1,1) model, the forecast for the variance at time $t+h$, made at time $t$, is $E_t[\sigma_{t+h}^2]$.

**Step 1: One-step-ahead forecast ($h=1$)**
$$E_t[\sigma_{t+1}^2] = \sigma_{t+1}^2 = \omega + \alpha \epsilon_t^2 + \beta \sigma_t^2$$
All terms on the right are known at time $t$.

**Step 2: Two-steps-ahead forecast ($h=2$)**
$$E_t[\sigma_{t+2}^2] = \omega + \alpha E_t[\epsilon_{t+1}^2] + \beta E_t[\sigma_{t+1}^2]$$
We know $E_t[\sigma_{t+1}^2]$ from Step 1. The key is that $E_t[\epsilon_{t+1}^2] = E_t[\sigma_{t+1}^2 z_{t+1}^2] = E_t[\sigma_{t+1}^2] E_t[z_{t+1}^2] = E_t[\sigma_{t+1}^2] \times 1$.
So, we can substitute:
$$E_t[\sigma_{t+2}^2] = \omega + (\alpha + \beta) E_t[\sigma_{t+1}^2]$$

**Step h: h-steps-ahead forecast**
This process can be generalized. The h-step forecast recursively depends on the h-1 step forecast and will converge towards the long-run average variance, $\bar{\sigma}^2$.
$$E_t[\sigma_{t+h}^2] - \bar{\sigma}^2 = (\alpha + \beta)^{h-1} (E_t[\sigma_{t+1}^2] - \bar{\sigma}^2)$$
This shows how shocks to volatility decay over the forecast horizon. The speed of decay is governed by the persistence parameter, $\alpha + \beta$. A higher persistence means shocks last longer.

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
