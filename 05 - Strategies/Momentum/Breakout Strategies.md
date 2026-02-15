# Breakout Strategies

**Core Idea:** Enter a trade when price breaks through a significant support/resistance level, anticipating a strong directional move.

---

## Types of Breakouts

### 1. Range Breakout
Price breaks above resistance or below support after consolidating.

```python
def range_breakout(prices, lookback=20):
    high = prices.rolling(lookback).max()
    low = prices.rolling(lookback).min()

    long_signal = prices > high.shift(1)   # Break above range
    short_signal = prices < low.shift(1)   # Break below range

    return long_signal.astype(int) - short_signal.astype(int)
```

### 2. Volatility Breakout
Price moves more than expected based on recent volatility.

```python
def volatility_breakout(prices, lookback=20, multiplier=2.0):
    """Keltner Channel / ATR breakout."""
    atr = compute_atr(prices, lookback)
    ma = prices.rolling(lookback).mean()

    upper = ma + multiplier * atr
    lower = ma - multiplier * atr

    long_signal = prices > upper
    short_signal = prices < lower
    return long_signal.astype(int) - short_signal.astype(int)

def compute_atr(df, period=14):
    """Average True Range."""
    high = df['high']
    low = df['low']
    close = df['close'].shift(1)
    tr = pd.concat([high - low, abs(high - close), abs(low - close)], axis=1).max(axis=1)
    return tr.rolling(period).mean()
```

### 3. Opening Range Breakout (ORB)
```
1. Wait for first 15-30 minutes of trading
2. Record the high and low of that range
3. Buy if price breaks above the high
4. Sell if price breaks below the low
5. Stop at opposite side of range
```

### 4. Volume-Confirmed Breakout
```python
def volume_breakout(prices, volume, price_lookback=20, vol_multiplier=2.0):
    """Only trade breakouts with above-average volume."""
    resistance = prices.rolling(price_lookback).max()
    avg_volume = volume.rolling(price_lookback).mean()

    breakout = (prices > resistance.shift(1)) & (volume > vol_multiplier * avg_volume)
    return breakout
```

## False Breakout Filter

Most breakouts fail (60-70%). Filters improve win rate:

1. **Volume confirmation** — Require 2x average volume
2. **Close confirmation** — Price must close above level (not just wick)
3. **ATR filter** — Breakout must exceed 1 ATR
4. **Trend filter** — Only trade breakouts in direction of larger trend
5. **Time filter** — Avoid first/last 15 minutes

## Risk Management

```python
# Stop loss: Below the breakout level
stop_loss = breakout_level - atr * 1.5

# Take profit: Risk-reward ratio
risk = entry_price - stop_loss
take_profit = entry_price + risk * 2.0  # 2:1 reward/risk

# Position size based on risk
risk_per_trade = 0.01 * capital  # 1% risk
shares = risk_per_trade / (entry_price - stop_loss)
```

---

**Related:** [[Trend Following]] | [[Momentum Strategies]] | [[Mean Reversion Strategies]] | [[Position Sizing]] | [[Stop Loss Strategies]]
