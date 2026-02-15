# Momentum Strategies

**Core Idea:** Assets that have been going up tend to continue going up. Assets that have been going down tend to continue going down. Buy winners, sell losers.

---

## Why Momentum Works

1. **Behavioral biases** — Investors underreact to news, then herd (overreact)
2. **Feedback loops** — Rising prices attract buyers → more rising prices
3. **Institutional flow** — Large funds take time to build positions
4. **Risk premium** — Compensation for crash/reversal risk

Momentum is one of the most robust anomalies in finance. Documented across asset classes, time periods, and geographies.

## Types of Momentum

### 1. Time-Series Momentum (Absolute)
Compare asset's current price to its own past.

**Signal:**
```
Signal = (Price_t - Price_{t-n}) / Price_{t-n}
```
or using returns:
```
Signal = Σ R_{t-i} for i = 1 to n  (total return over lookback)
```

**Rule:** Go long if signal > 0, short if signal < 0.

### 2. Cross-Sectional Momentum (Relative)
Rank assets relative to each other.

**Process:**
1. Compute momentum score for all assets in universe
2. Rank them
3. Go **long top decile**, **short bottom decile**
4. Rebalance monthly

**Classic Jegadeesh & Titman (1993):**
- Lookback: 3-12 months (skip most recent month)
- Holding: 3-12 months
- Skip month avoids short-term [[Mean Reversion Strategies|mean reversion]]

### 3. Intraday Momentum
Shorter-term momentum within a trading day.

**Signals:**
- Opening range breakouts (first 15-30 min)
- VWAP crossovers
- Volume-weighted momentum

## Key Indicators

### Moving Average Crossover
```python
def ma_crossover_signal(prices, fast=10, slow=50):
    """
    Classic dual moving average crossover.
    Buy when fast MA crosses above slow MA.
    """
    fast_ma = prices.rolling(fast).mean()
    slow_ma = prices.rolling(slow).mean()

    signal = np.where(fast_ma > slow_ma, 1, -1)
    # Only trade on crossover
    trades = np.diff(signal)
    return trades
```

**Common Pairs:** 5/20, 10/50, 20/200, 50/200 ("Golden Cross" / "Death Cross")

See [[Sample Strategy - Moving Average Crossover]] for full implementation.

### Rate of Change (ROC)
```
ROC = (Price_t / Price_{t-n} - 1) × 100
```

### RSI (Relative Strength Index)
```
RSI = 100 - 100 / (1 + RS)
RS = Average Gain / Average Loss over n periods
```
- RSI > 70: Strong momentum (or overbought → potential reversal)
- RSI < 30: Weak momentum (or oversold → potential reversal)
- Can be used for both momentum AND [[Mean Reversion Strategies]]

### MACD (Moving Average Convergence Divergence)
```
MACD Line = EMA(12) - EMA(26)
Signal Line = EMA(9) of MACD Line
Histogram = MACD Line - Signal Line
```

### ADX (Average Directional Index)
- Measures trend **strength** (not direction)
- ADX > 25: Trending market → use momentum
- ADX < 20: Range-bound → use [[Mean Reversion Strategies]]

## Implementation

```python
import pandas as pd
import numpy as np

class MomentumStrategy:
    def __init__(self, lookback=252, holding=21, top_n=10, bottom_n=10):
        self.lookback = lookback  # 12 months
        self.holding = holding    # 1 month
        self.top_n = top_n
        self.bottom_n = bottom_n

    def generate_signals(self, prices_df):
        """
        Cross-sectional momentum.
        prices_df: DataFrame with dates as index, tickers as columns.
        """
        # Calculate momentum (skip most recent month)
        momentum = prices_df.pct_change(self.lookback - 21).shift(21)

        signals = pd.DataFrame(0, index=prices_df.index, columns=prices_df.columns)

        for date in prices_df.index:
            ranked = momentum.loc[date].dropna().rank(ascending=False)
            longs = ranked[ranked <= self.top_n].index
            shorts = ranked[ranked > len(ranked) - self.bottom_n].index

            signals.loc[date, longs] = 1.0 / self.top_n
            signals.loc[date, shorts] = -1.0 / self.bottom_n

        return signals
```

## Momentum Crashes

**WARNING:** Momentum strategies are prone to violent reversals.

| Event | Year | Drawdown |
|---|---|---|
| Quant Meltdown | 2007 | -25% in days |
| GFC Recovery | 2009 (Mar) | -40%+ |
| COVID Reversal | 2020 (Nov) | -30% |

**Mitigation:**
- [[Position Sizing]] — Reduce in high-volatility regimes
- [[Drawdown Management]] — Hard stop on strategy drawdown
- [[Correlation and Diversification]] — Combine with [[Mean Reversion Strategies]]
- Dynamic lookback — Shorten in volatile markets
- Volatility scaling — Divide signal by recent volatility

## Performance Characteristics

| Metric | Typical |
|---|---|
| Annual Return | 5-15% (long/short) |
| Sharpe Ratio | 0.4-0.8 |
| Max Drawdown | -20% to -40% |
| Win Rate | 45-55% |
| Profit Factor | 1.2-1.5 |
| Correlation with Market | Low (long/short) |

---

**Related:** [[Trend Following]] | [[Breakout Strategies]] | [[Mean Reversion Strategies]] | [[RSI and Oscillators]] | [[Performance Metrics]]
