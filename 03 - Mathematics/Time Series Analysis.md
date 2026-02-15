# Time Series Analysis

Financial data is sequential. Time series analysis provides the tools to model, forecast, and understand temporal patterns in prices, returns, and other financial data.

---

## Stationarity

A time series is **stationary** if its statistical properties don't change over time.

**Why it matters:** Most statistical models require stationarity. Raw prices are non-stationary; returns are (approximately) stationary.

### Testing for Stationarity

```python
from statsmodels.tsa.stattools import adfuller, kpss

def test_stationarity(series):
    """Run ADF and KPSS tests."""
    # ADF: H0 = unit root (non-stationary)
    adf_result = adfuller(series.dropna())
    adf_pvalue = adf_result[1]

    # KPSS: H0 = stationary
    kpss_result = kpss(series.dropna(), regression='c')
    kpss_pvalue = kpss_result[1]

    return {
        'adf_statistic': adf_result[0],
        'adf_pvalue': adf_pvalue,
        'adf_stationary': adf_pvalue < 0.05,
        'kpss_pvalue': kpss_pvalue,
        'kpss_stationary': kpss_pvalue > 0.05,
    }
```

### Making Series Stationary
1. **Differencing:** `Δy_t = y_t - y_{t-1}` (first difference ≈ returns)
2. **Log differencing:** `Δln(y_t)` (log returns)
3. **Detrending:** Remove linear/polynomial trend
4. **Seasonal adjustment:** Remove seasonal components

## Autocorrelation

```python
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# ACF: Total correlation at lag k
# PACF: Direct correlation at lag k (removing intermediate lags)
plot_acf(returns, lags=40)
plot_pacf(returns, lags=40)
```

**Interpreting ACF/PACF:**
- Significant ACF at lag 1 → serial correlation → exploitable!
- ACF dies off slowly → trending (non-stationary)
- PACF cuts off at lag p → AR(p) model appropriate
- ACF cuts off at lag q → MA(q) model appropriate

## ARIMA Models

**ARIMA(p, d, q):** AutoRegressive Integrated Moving Average

```
AR(p):    y_t = c + φ₁y_{t-1} + φ₂y_{t-2} + ... + φₚy_{t-p} + ε_t
MA(q):    y_t = c + ε_t + θ₁ε_{t-1} + θ₂ε_{t-2} + ... + θqε_{t-q}
ARIMA:    Combines AR, differencing (I), and MA
```

```python
from statsmodels.tsa.arima.model import ARIMA
import pmdarima as pm

# Auto ARIMA: automatically selects p, d, q
auto_model = pm.auto_arima(
    returns,
    start_p=0, start_q=0,
    max_p=5, max_q=5,
    seasonal=False,
    stepwise=True,
    suppress_warnings=True,
    information_criterion='bic'
)
print(auto_model.summary())

# Forecast
forecast = auto_model.predict(n_periods=5)
```

## GARCH Models (Volatility Modeling)

Returns may be uncorrelated, but **squared returns** (volatility) are autocorrelated. GARCH captures volatility clustering.

### GARCH(1,1)
```
σ²_t = ω + α·ε²_{t-1} + β·σ²_{t-1}

Where:
  ω = long-run variance weight
  α = reaction to recent shock
  β = persistence of volatility
  α + β < 1 for stationarity
  α + β close to 1 = high persistence
```

```python
from arch import arch_model

# Fit GARCH(1,1)
model = arch_model(returns * 100, vol='GARCH', p=1, q=1, dist='t')
result = model.fit(disp='off')
print(result.summary())

# Forecast volatility
forecast = result.forecast(horizon=5)
predicted_vol = np.sqrt(forecast.variance.iloc[-1].values) / 100

# Use for position sizing
# Higher predicted vol → smaller position
position_scalar = target_vol / predicted_vol
```

### GARCH Variants
| Model | Feature |
|---|---|
| **EGARCH** | Asymmetric — bad news increases vol more |
| **GJR-GARCH** | Leverage effect modeling |
| **FIGARCH** | Long memory in volatility |
| **DCC-GARCH** | Dynamic conditional correlations |

## Regime Switching Models

Markets operate in different regimes (bull/bear, high/low vol). Hidden Markov Models capture this.

```python
from hmmlearn import hmm

def fit_regime_model(returns, n_regimes=2):
    """
    Fit Hidden Markov Model to identify market regimes.
    """
    X = returns.values.reshape(-1, 1)

    model = hmm.GaussianHMM(
        n_components=n_regimes,
        covariance_type='full',
        n_iter=1000,
        random_state=42
    )
    model.fit(X)

    # Predict regimes
    regimes = model.predict(X)
    regime_probs = model.predict_proba(X)

    # Regime characteristics
    for i in range(n_regimes):
        mask = regimes == i
        print(f"Regime {i}: mean={returns[mask].mean():.4f}, "
              f"vol={returns[mask].std():.4f}, "
              f"freq={mask.mean():.1%}")

    return model, regimes, regime_probs
```

**Trading application:**
- Regime 0 (low vol, positive drift): Use [[Momentum Strategies]]
- Regime 1 (high vol, negative drift): Use [[Mean Reversion Strategies]], reduce exposure

## Cointegration → [[Statistical Arbitrage]]

Two non-stationary series whose linear combination is stationary.

```python
from statsmodels.tsa.stattools import coint

# Engle-Granger test
score, pvalue, _ = coint(series_a, series_b)
# pvalue < 0.05 → cointegrated → tradeable with [[Pairs Trading]]
```

## Structural Breaks

Detecting when the data-generating process changes:

```python
import ruptures

def detect_breaks(series, model='rbf', n_breaks=3):
    """Detect structural breaks in time series."""
    algo = ruptures.Pelt(model=model).fit(series.values)
    breakpoints = algo.predict(pen=10)
    return breakpoints
```

---

**Related:** [[Mathematics MOC]] | [[Probability and Statistics for Trading]] | [[Stochastic Calculus]] | [[Mean Reversion Strategies]] | [[Feature Engineering for Trading]]
