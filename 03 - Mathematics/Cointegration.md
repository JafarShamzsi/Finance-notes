# Cointegration

Cointegration is the mathematical foundation of [[Statistical Arbitrage]] and [[Pairs Trading]]. Two non-stationary time series are cointegrated if a linear combination of them is stationary.

---

## Intuition

**Correlation ≠ Cointegration.**

- **Correlation:** Two series move together in the short term
- **Cointegration:** Two series are tied together in the long run (they can't diverge permanently)

**Classic analogy:** A drunk person and their dog on a walk. Both wander randomly (non-stationary), but the leash keeps them from diverging (cointegrated).

---

## Mathematical Definition

Two $I(1)$ series $X_t$ and $Y_t$ are cointegrated if there exists $\beta$ such that:

$$Z_t = Y_t - \beta X_t \sim I(0) \quad (\text{stationary})$$

The stationary series $Z_t$ is called the **spread** or **error correction term**.

---

## Testing for Cointegration

### Method 1: Engle-Granger Two-Step (1987)

1. **Regress** $Y_t = \alpha + \beta X_t + \epsilon_t$ using OLS
2. **Test residuals** $\hat{\epsilon}_t$ for stationarity using ADF test

```python
import numpy as np
from statsmodels.tsa.stattools import adfuller
from sklearn.linear_model import LinearRegression

def engle_granger_test(y, x, significance=0.05):
    """
    Engle-Granger cointegration test.

    Returns:
        is_cointegrated: bool
        hedge_ratio: float (beta)
        spread: array
        adf_pvalue: float
    """
    # Step 1: OLS regression
    x_arr = np.array(x).reshape(-1, 1)
    y_arr = np.array(y)

    reg = LinearRegression().fit(x_arr, y_arr)
    hedge_ratio = reg.coef_[0]
    intercept = reg.intercept_

    # Step 2: Compute spread (residuals)
    spread = y_arr - hedge_ratio * x_arr.flatten() - intercept

    # Step 3: ADF test on residuals
    # Use Engle-Granger critical values (more conservative than standard ADF)
    adf_stat, adf_pvalue, _, _, critical_values, _ = adfuller(spread, maxlag=None)

    return {
        'is_cointegrated': adf_pvalue < significance,
        'hedge_ratio': hedge_ratio,
        'intercept': intercept,
        'spread': spread,
        'adf_statistic': adf_stat,
        'adf_pvalue': adf_pvalue,
        'critical_values': critical_values,
        'half_life': _half_life(spread)
    }


def _half_life(spread):
    """Estimate mean-reversion half-life using AR(1) model."""
    spread_lag = spread[:-1]
    spread_diff = np.diff(spread)
    reg = LinearRegression().fit(spread_lag.reshape(-1, 1), spread_diff)
    phi = reg.coef_[0]
    if phi >= 0:
        return np.inf  # Not mean-reverting
    return -np.log(2) / phi
```

### Method 2: Johansen Test (Multiple Series)

Tests for cointegration among $n > 2$ series simultaneously. Can find multiple cointegrating relationships.

```python
from statsmodels.tsa.vector_ar.vecm import coint_johansen

def johansen_test(data, det_order=0, k_ar_diff=1):
    """
    Johansen cointegration test for multiple time series.

    Parameters:
        data: pd.DataFrame or array (T x n)
        det_order: -1 (no const), 0 (const in coint eq), 1 (const in VAR)
        k_ar_diff: Number of lagged differences in VAR

    Returns:
        n_coint: Number of cointegrating relationships
        eigenvectors: Cointegrating vectors
    """
    result = coint_johansen(data, det_order, k_ar_diff)

    # Trace statistic test
    trace_stat = result.lr1
    trace_cv = result.cvt[:, 1]  # 5% critical values

    n_coint = sum(trace_stat > trace_cv)

    return {
        'n_cointegrating_vectors': n_coint,
        'trace_statistics': trace_stat,
        'critical_values_5pct': trace_cv,
        'eigenvectors': result.evec,
        'eigenvalues': result.eig
    }
```

### Method 3: Kalman Filter (Dynamic Hedge Ratio)

The hedge ratio $\beta$ isn't constant — it changes over time. The [[Kalman Filter]] can estimate a time-varying $\beta_t$.

**Advantage:** Adapts to changing relationships.
**Disadvantage:** More complex, more parameters to tune.

---

## Half-Life of Mean Reversion

The half-life tells you how long the spread takes to revert halfway to its mean:

$$\text{half-life} = -\frac{\ln(2)}{\phi}$$

Where $\phi$ is the AR(1) coefficient of the spread.

| Half-life | Interpretation |
|-----------|----------------|
| < 5 days | Very fast mean reversion (great for trading) |
| 5-20 days | Moderate (tradeable) |
| 20-60 days | Slow (still tradeable, lower frequency) |
| > 60 days | Too slow (capital tied up too long) |

---

## Finding Cointegrated Pairs

```python
from itertools import combinations

def find_cointegrated_pairs(prices_df, pvalue_threshold=0.05):
    """
    Scan all pairs in a universe for cointegration.

    Parameters:
        prices_df: pd.DataFrame (dates × tickers) of prices
        pvalue_threshold: Significance level

    Returns:
        List of cointegrated pairs with statistics
    """
    tickers = prices_df.columns
    pairs = []

    for t1, t2 in combinations(tickers, 2):
        result = engle_granger_test(prices_df[t1], prices_df[t2])

        if result['is_cointegrated'] and result['half_life'] < 60:
            pairs.append({
                'pair': (t1, t2),
                'pvalue': result['adf_pvalue'],
                'hedge_ratio': result['hedge_ratio'],
                'half_life': result['half_life']
            })

    # Sort by p-value (most significant first)
    pairs.sort(key=lambda x: x['pvalue'])
    return pairs
```

**Warning:** Testing many pairs creates a multiple testing problem. Apply [[Alpha Research]] correction methods (Bonferroni, FDR).

---

## Related Notes
- [[Statistical Arbitrage]] — Primary application
- [[Pairs Trading]] — Trading cointegrated pairs
- [[Kalman Filter]] — Dynamic hedge ratio estimation
- [[Time Series Analysis]] — Stationarity and ADF tests
- [[Mathematics MOC]] — Parent section
- [[Mean Reversion Strategies]] — Spread mean reversion
