# Mean Reversion Strategies

**Core Idea:** Prices deviate from their "fair value" or average and tend to revert back. Buy low, sell high — literally.

---

## Why Mean Reversion Works

1. **Overreaction** — Traders overshoot on news (behavioral bias)
2. **Market making** — Bid-ask bounce creates short-term reversals
3. **Inventory effects** — Large trades push prices temporarily (see [[Market Impact]])
4. **Fundamental anchoring** — Prices orbit around intrinsic value

## Mathematical Framework

### Ornstein-Uhlenbeck Process
The classic model for mean-reverting assets:

```
dX_t = θ(μ - X_t)dt + σdW_t

Where:
  X_t = current price/spread
  θ = speed of mean reversion (higher = faster reversion)
  μ = long-run mean
  σ = volatility
  W_t = Wiener process (random walk)
```

**Key parameter: θ (theta)**
- θ > 0: Mean-reverting (tradeable)
- θ ≈ 0: Random walk (not tradeable with MR)
- Half-life of mean reversion: t½ = ln(2) / θ

### Testing for Mean Reversion

**1. Augmented Dickey-Fuller (ADF) Test**
```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(spread_series)
adf_stat = result[0]
p_value = result[1]
# p_value < 0.05 → reject random walk → mean reverting
```

**2. Hurst Exponent**
```python
def hurst_exponent(ts):
    """
    H < 0.5: Mean reverting
    H = 0.5: Random walk
    H > 0.5: Trending
    """
    lags = range(2, 100)
    tau = [np.std(np.subtract(ts[lag:], ts[:-lag])) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0]
```

**3. Variance Ratio Test**
```
VR(q) = Var(r_t(q)) / (q · Var(r_t))

VR < 1: Mean reverting
VR = 1: Random walk
VR > 1: Trending
```

## Signal Generation

### Z-Score (Bollinger Band Logic)
```python
def mean_reversion_signal(prices, lookback=20, entry_z=2.0, exit_z=0.5):
    """
    Classic z-score mean reversion.
    """
    mean = prices.rolling(lookback).mean()
    std = prices.rolling(lookback).std()
    z_score = (prices - mean) / std

    signal = pd.Series(0, index=prices.index)
    signal[z_score < -entry_z] = 1    # Buy when oversold
    signal[z_score > entry_z] = -1    # Sell when overbought
    signal[abs(z_score) < exit_z] = 0  # Exit near mean

    return signal
```

### Bollinger Bands
```
Upper Band = SMA(20) + 2 × StdDev(20)
Lower Band = SMA(20) - 2 × StdDev(20)
Middle Band = SMA(20)

Buy:  Price touches Lower Band
Sell: Price touches Upper Band
Exit: Price returns to Middle Band
```

### RSI Mean Reversion
```
Buy:  RSI(14) < 30  (oversold)
Sell: RSI(14) > 70  (overbought)
Exit: RSI returns to 50
```

## Strategy Variants

### 1. Single-Asset Mean Reversion
Trade one instrument against its own history.
- Works on range-bound assets (FX pairs, commodities)
- Fails on trending assets (growth stocks, crypto in bull runs)

### 2. Pairs Trading → [[Pairs Trading]]
Trade the spread between two correlated assets.
- More robust — neutralizes market risk
- Spread more likely to be stationary than individual prices

### 3. Cross-Sectional Mean Reversion
Buy recent losers, sell recent winners (opposite of [[Momentum Strategies]]).
- Short-term (1-5 days): Mean reversion dominates
- Medium-term (1-12 months): Momentum dominates
- Long-term (3-5 years): Mean reversion dominates

### 4. Intraday Mean Reversion
- **Opening gap fade:** Buy stocks that gap down, sell gaps up
- **VWAP reversion:** Trade toward [[VWAP Algorithm|VWAP]] when price deviates
- Works because intraday moves often overshoot

## Full Strategy Implementation

```python
class BollingerBandMeanReversion:
    def __init__(self, lookback=20, num_std=2.0, exit_std=0.5):
        self.lookback = lookback
        self.num_std = num_std
        self.exit_std = exit_std

    def generate_signals(self, prices):
        sma = prices.rolling(self.lookback).mean()
        std = prices.rolling(self.lookback).std()

        upper = sma + self.num_std * std
        lower = sma - self.num_std * std
        exit_upper = sma + self.exit_std * std
        exit_lower = sma - self.exit_std * std

        position = 0
        signals = []

        for i in range(len(prices)):
            if prices.iloc[i] < lower.iloc[i] and position <= 0:
                position = 1  # Long
            elif prices.iloc[i] > upper.iloc[i] and position >= 0:
                position = -1  # Short
            elif position == 1 and prices.iloc[i] > exit_upper.iloc[i]:
                position = 0  # Exit long
            elif position == -1 and prices.iloc[i] < exit_lower.iloc[i]:
                position = 0  # Exit short

            signals.append(position)

        return pd.Series(signals, index=prices.index)
```

## When Mean Reversion Fails

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Regime change | Asset starts trending | Use [[ADX]] filter; detect regimes |
| Structural break | Fundamental shift (delisting, merger) | Stop-loss; fundamental filters |
| Increasing correlation | Market crisis | [[Tail Risk and Black Swans]] protection |
| Widening spread | Liquidity dries up | Monitor [[Bid-Ask Spread]] |

## Performance Characteristics

| Metric | Typical |
|---|---|
| Annual Return | 5-20% |
| Sharpe Ratio | 0.5-1.5 |
| Max Drawdown | -10% to -25% |
| Win Rate | 55-70% |
| Avg Win/Loss Ratio | 0.5-0.8 |
| Profit Factor | 1.3-2.0 |

High win rate, small wins. Losses tend to be larger when reversion fails (trending market).

---

**Related:** [[Pairs Trading]] | [[Statistical Arbitrage]] | [[Momentum Strategies]] | [[Bollinger Bands]] | [[Time Series Analysis]]
