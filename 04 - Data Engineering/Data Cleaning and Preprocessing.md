# Data Cleaning and Preprocessing

Dirty data produces false signals. Rigorous cleaning is non-negotiable.

---

## Common Data Issues

| Issue | Impact | Fix |
|---|---|---|
| **Missing data** | Gaps in signals | Forward fill, interpolation, or flag |
| **Corporate actions** | False returns (splits, dividends) | Use adjusted prices |
| **Duplicates** | Double-counting | Dedup by timestamp |
| **Outliers / Bad ticks** | Spike signals | Filter by z-score or exchange rules |
| **Timezone issues** | Wrong alignment | Standardize to UTC |
| **Survivorship bias** | Overfit to survivors | Use survivorship-free data |

## Preprocessing Pipeline

```python
import pandas as pd
import numpy as np

def clean_ohlcv(df):
    """Standard OHLCV cleaning pipeline."""

    # 1. Remove duplicates
    df = df[~df.index.duplicated(keep='first')]

    # 2. Sort by time
    df = df.sort_index()

    # 3. Remove bad ticks (price <= 0)
    df = df[(df['close'] > 0) & (df['volume'] >= 0)]

    # 4. OHLC consistency
    df = df[(df['high'] >= df['low']) &
            (df['high'] >= df['open']) &
            (df['high'] >= df['close']) &
            (df['low'] <= df['open']) &
            (df['low'] <= df['close'])]

    # 5. Remove extreme outliers (>5 sigma daily return)
    returns = df['close'].pct_change()
    z_scores = (returns - returns.rolling(60).mean()) / returns.rolling(60).std()
    df = df[abs(z_scores) < 5]

    # 6. Forward fill small gaps (up to 3 periods)
    df = df.reindex(pd.date_range(df.index[0], df.index[-1], freq='B'))
    df = df.ffill(limit=3)

    # 7. Drop remaining NaN rows
    df = df.dropna()

    return df

def adjust_for_splits(df, splits):
    """
    Adjust prices for stock splits.
    splits: DataFrame with 'date' and 'ratio' columns.
    """
    for _, split in splits.iterrows():
        mask = df.index < split['date']
        df.loc[mask, ['open', 'high', 'low', 'close']] /= split['ratio']
        df.loc[mask, 'volume'] *= split['ratio']
    return df
```

## Returns Calculation

```python
def compute_returns(prices, method='log'):
    """
    Log returns are better for statistical analysis.
    Simple returns are better for portfolio calculations.
    """
    if method == 'log':
        return np.log(prices / prices.shift(1))
    else:
        return prices.pct_change()
```

## Handling Missing Data in Multi-Asset Datasets

```python
def align_multi_asset(price_dict, method='inner'):
    """
    Align multiple assets to common dates.
    'inner': Only dates where ALL assets have data
    'outer': All dates, fill missing
    """
    df = pd.DataFrame(price_dict)
    if method == 'inner':
        return df.dropna()
    else:
        return df.ffill().dropna()
```

---

**Related:** [[Data Engineering MOC]] | [[Market Data Sources]] | [[Survivorship Bias]] | [[Look-Ahead Bias]] | [[Feature Engineering for Trading]]
