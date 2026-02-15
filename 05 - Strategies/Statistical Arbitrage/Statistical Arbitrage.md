# Statistical Arbitrage

**Core Idea:** Use statistical models to identify mispricings between related securities and profit from convergence. Market-neutral, low-risk when done correctly.

---

## What is Stat Arb?

Statistical arbitrage is NOT true arbitrage (risk-free profit). It's a **probabilistic edge** — the mispricing reverts to fair value *most* of the time, but not always.

```
True Arbitrage:     Risk = 0, Return > 0    (rare, fleeting)
Statistical Arb:    Risk > 0, E[Return] > 0  (common, manageable)
```

## Types of Statistical Arbitrage

### 1. Pairs Trading → [[Pairs Trading]]
Simplest form: two correlated stocks.

### 2. Multi-Leg Stat Arb
- Trade baskets of stocks against each other
- Long portfolio of undervalued stocks vs. short portfolio of overvalued
- More diversified than pairs

### 3. Index Arbitrage
- Trade the index future vs. the basket of constituent stocks
- Fair value: `F = S × e^{(r-d)T}`
- When `F > Fair Value`: Short future, buy stocks
- When `F < Fair Value`: Buy future, short stocks

### 4. ETF Arbitrage
- Trade ETF vs. its underlying basket
- NAV vs. market price divergences
- Creation/redemption mechanism bounds the spread

### 5. Cross-Asset Stat Arb
- Equity vs. CDS spreads
- ADR vs. underlying foreign stock
- Convertible bond vs. underlying equity

## Mathematical Framework

### Cointegration (Engle-Granger Method)

Two series X and Y are cointegrated if their linear combination is stationary:

```
Z_t = Y_t - β·X_t - α    (residual/spread)

Where:
  β = hedge ratio (from OLS regression)
  α = intercept
  Z_t should be stationary (ADF test p < 0.05)
```

```python
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller

def find_cointegrated_pairs(prices_df, significance=0.05):
    """
    Find all cointegrated pairs in a universe of stocks.
    """
    n = prices_df.shape[1]
    keys = prices_df.columns
    pairs = []

    for i in range(n):
        for j in range(i+1, n):
            S1 = prices_df[keys[i]]
            S2 = prices_df[keys[j]]
            score, pvalue, _ = coint(S1, S2)
            if pvalue < significance:
                pairs.append((keys[i], keys[j], pvalue))

    return sorted(pairs, key=lambda x: x[2])
```

### Johansen Test (Multiple Assets)
Tests cointegration among >2 series simultaneously. More powerful than pairwise Engle-Granger.

```python
from statsmodels.tsa.vector_ar.vecm import coint_johansen

result = coint_johansen(prices_df, det_order=0, k_ar_diff=1)
# Check trace statistics vs critical values
```

### Dynamic Hedge Ratio (Kalman Filter)
Static hedge ratios drift over time. Use [[Kalman Filter]] for adaptive estimation:

```python
from pykalman import KalmanFilter

def kalman_hedge_ratio(x, y):
    delta = 1e-5
    trans_cov = delta / (1 - delta) * np.eye(2)

    kf = KalmanFilter(
        n_dim_obs=1, n_dim_state=2,
        initial_state_mean=np.zeros(2),
        initial_state_covariance=np.ones((2, 2)),
        transition_matrices=np.eye(2),
        observation_matrices=np.expand_dims(
            np.vstack([x, np.ones(len(x))]).T, axis=1),
        observation_covariance=1.0,
        transition_covariance=trans_cov
    )

    state_means, _ = kf.filter(y)
    return state_means[:, 0]  # Time-varying hedge ratio
```

## Full Stat Arb Strategy

```python
class StatArbStrategy:
    def __init__(self, lookback=60, entry_z=2.0, exit_z=0.5,
                 stop_z=4.0, hedge_window=120):
        self.lookback = lookback
        self.entry_z = entry_z
        self.exit_z = exit_z
        self.stop_z = stop_z
        self.hedge_window = hedge_window

    def compute_spread(self, y, x):
        """Compute spread with rolling hedge ratio."""
        hedge_ratios = []
        for i in range(self.hedge_window, len(y)):
            window_x = x.iloc[i-self.hedge_window:i]
            window_y = y.iloc[i-self.hedge_window:i]
            X = sm.add_constant(window_x)
            model = sm.OLS(window_y, X).fit()
            hedge_ratios.append(model.params.iloc[1])

        hedge_ratios = pd.Series(hedge_ratios, index=y.index[self.hedge_window:])
        spread = y.iloc[self.hedge_window:] - hedge_ratios * x.iloc[self.hedge_window:]
        return spread, hedge_ratios

    def generate_signals(self, spread):
        """Z-score based entry/exit."""
        mean = spread.rolling(self.lookback).mean()
        std = spread.rolling(self.lookback).std()
        z = (spread - mean) / std

        signals = pd.Series(0, index=spread.index)
        signals[z < -self.entry_z] = 1    # Long spread
        signals[z > self.entry_z] = -1    # Short spread
        signals[abs(z) < self.exit_z] = 0  # Exit
        signals[abs(z) > self.stop_z] = 0  # Stop loss

        return signals
```

## Risk Factors

| Risk | Description | Mitigation |
|---|---|---|
| **Divergence risk** | Spread keeps widening instead of reverting | Stop-loss at 3-4 sigma |
| **Regime change** | Correlation breaks down permanently | Monitor cointegration stability |
| **Crowding** | Too many funds trade same pairs | Diversify, find unique pairs |
| **Liquidity risk** | Can't exit positions in crisis | Size appropriately, monitor [[Liquidity]] |
| **Model risk** | Wrong hedge ratio, wrong lookback | Robust estimation, [[Walk-Forward Analysis]] |

## Performance Characteristics

| Metric | Typical |
|---|---|
| Annual Return | 5-15% |
| Sharpe Ratio | 1.0-2.5 |
| Max Drawdown | -5% to -15% |
| Market Beta | Near 0 (market neutral) |
| Win Rate | 55-65% |

---

**Related:** [[Pairs Trading]] | [[Mean Reversion Strategies]] | [[Cointegration]] | [[Kalman Filter]] | [[Factor Models]]
