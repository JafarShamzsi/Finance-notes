# Breakout Strategies

**Breakout Strategies** are a subset of [[Momentum Strategies]] that aim to enter a trade when the price moves above a defined resistance level or below a defined support level, usually accompanied by increased volume.

The core hypothesis is that a significant move through a price boundary signals a structural shift in supply and demand.

---

## 1. Defining the "Boundary"

A breakout requires a clear threshold to cross:
- **Horizontal Support/Resistance:** Multi-touch highs or lows.
- **Donchian Channels:** The highest high and lowest low over $N$ periods.
- **Bollinger Bands:** Price crossing the upper or lower standard deviation bands.
- **Volatility-Based:** Price moving more than $k \times \text{ATR}$ from the previous day's close.

---

## 2. The Role of Volume

In quantitative breakout models, volume is the primary **Confirmation Signal**.
- **The Signal:** A breakout on low volume is likely a "False Breakout" or "Bull/Bear Trap."
- **The Filter:** Only enter if the volume during the breakout bar is $> 1.5 \times$ the average volume of the last 20 bars.

---

## 3. Dealing with "False Breakouts" (Traps)

False breakouts occur when the price briefly crosses a level but immediately reverts. Quants use several filters to mitigate this:
1.  **Time Filter:** The price must close above the level for $N$ consecutive bars.
2.  **Distance Filter:** The price must move $X\%$ beyond the level before entry.
3.  **Volatility Filter:** Ensuring the breakout is not just random noise (using ATR).

---

## 4. Strategy Rules: Classic Donchian Breakout

| Parameter | Logic |
|-----------|-------|
| **Entry (Long)** | Current Price $>$ Max(High of last 20 bars). |
| **Entry (Short)** | Current Price $<$ Min(Low of last 20 bars). |
| **Exit** | Price crosses the 10-bar median (Mean reversion exit) OR Trailing Stop. |
| **Stop Loss** | Entry Price $- 2 \times \text{ATR}$. |

---

## 5. Python: Simple Breakout Logic

```python
import pandas as pd

def breakout_signals(df, window=20, vol_multiplier=1.5):
    # Calculate boundaries
    df['upper_band'] = df['high'].rolling(window).max().shift(1)
    df['avg_vol'] = df['volume'].rolling(window).mean().shift(1)
    
    # Generate Long Entry
    df['long_entry'] = (df['close'] > df['upper_band']) & \
                       (df['volume'] > df['avg_vol'] * vol_multiplier)
    
    return df
```

---

## 6. Market Regimes for Breakouts

Breakout strategies perform exceptionally well in **Trending/Expanding Volatility** regimes but suffer massive "Whipsaw" losses in **Mean-Reverting/Congested** regimes.
- **Quant Tip:** Use an indicator like the ADX (Average Directional Index) to only trade breakouts when the trend strength is rising ($ADX > 25$).

---

## Related Notes
- [[Momentum Strategies]] — The parent category
- [[Trend Following]] — Long-term breakouts
- [[Regime Detection]] — Identifying when to use breakouts
- [[Stop Loss Strategies]] — Managing the high failure rate
- [[Volatility Trading]] — Breakouts as vol expansions
- [[Order Book Dynamics]] — Watching for "Sweeps" at the level
