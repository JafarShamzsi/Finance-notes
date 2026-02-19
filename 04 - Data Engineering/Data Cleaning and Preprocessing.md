# Data Cleaning and Preprocessing

In quantitative finance, "Data is the Signal, but Noise is the Constant." Cleaning raw market data is often the most time-consuming part of strategy development. Garbage in, garbage out.

---

## 1. Common Data Issues

| Issue | Description | Mitigation |
|-------|-------------|------------|
| **Missing Ticks** | Gaps in time series due to network failure. | Forward-fill (`ffill`), Interpolation, or discard if the gap is too large. |
| **Outliers (Bad Prints)** | Erroneous trades far from the current price. | Median filtering, Z-score thresholds, or price-corridor checks. |
| **Corporate Actions** | Stock splits, dividends, spin-offs. | Use "Adjusted Close" or back-adjust the entire history. |
| **Zombie Tickers** | Stocks that have been delisted. | Retain them to avoid [[Survivorship Bias]]. |

---

## 2. Time-Series Alignment

Different assets have different timestamps and exchange hours.
- **As-of Joins:** Joining a trade with the *last known* quote (See [[Database Design for Trading]]).
- **Resampling:** Converting tick data into regular OHLCV bars (Time, Volume, or Dollar bars).
- **Timezone Normalization:** Ensuring all data is in a single reference zone (usually UTC).

---

## 3. Handling Outliers: The "Quant Corridor"

A simple rule to remove bad prints in tick data:
$$\text{Price is Valid IF: } |P_t - \text{median}(P_{t-10:t+10})| < k \times \sigma$$
- $k$ is usually $3$ or $5$.
- This prevents a "fat-finger" trade from skewing your volatility indicators.

---

## 4. Normalization for Machine Learning

ML models (especially Neural Networks) fail if features have different scales.
- **Log Returns:** $r_t = \ln(P_t / P_{t-1})$. (Makes returns additive and reduces skew).
- **Z-Score Scaling:** $\frac{x - \mu}{\sigma}$. (Makes features zero-mean and unit variance).
- **Quantile Transform:** Maps features to a uniform or normal distribution (robust to outliers).

---

## 5. Stationarity: The Ultimate Goal

Most statistical models require the data to be **Stationary** (mean and variance don't change over time).
- **Raw Price:** Non-stationary (Random walk).
- **Returns:** Usually stationary (Mean-reverting around a small drift).
- **Fractional Differentiation:** A technique by Lopez de Prado to achieve stationarity while preserving the "memory" of the price level.

---

## 6. Python: Simple Cleaning Snippet

```python
import pandas as pd

def clean_and_normalize(df):
    # 1. Forward fill missing values (limit 5 steps)
    df = df.ffill(limit=5)
    
    # 2. Calculate Log Returns
    df['log_ret'] = np.log(df['close'] / df['close'].shift(1))
    
    # 3. Remove extreme outliers (> 5 std dev)
    std = df['log_ret'].std()
    df = df[df['log_ret'].abs() < 5 * std]
    
    # 4. Volatility Scaling (Rolling 20-day)
    df['scaled_ret'] = df['log_ret'] / df['log_ret'].rolling(20).std()
    
    return df.dropna()
```

---

## Related Notes
- [[Data Engineering MOC]] — Broader pipeline context
- [[Market Data Sources]] — Where the mess begins
- [[Tick Data and Trade Data]] — The raw material
- [[Survivorship Bias]] — A specific data cleaning trap
- [[Database Design for Trading]] — Storage for cleaned data
- [[Feature Engineering for Trading]] — The next step in the pipeline
