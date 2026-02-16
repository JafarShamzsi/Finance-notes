# Stop Loss Strategies

**Stops are the emergency brakes of trading. They limit individual trade losses but come with tradeoffs — too tight and you get stopped out of winning trades, too wide and you give back too much.**

---

## Types of Stops

### 1. Fixed Stop
```python
stop_price = entry_price - fixed_amount  # e.g., $2 below entry
```

### 2. Percentage Stop
```python
stop_price = entry_price * (1 - stop_pct)  # e.g., 2% below entry
```

### 3. ATR-Based (Volatility Stop)
```python
def atr_stop(entry, atr, multiplier=2.0, direction='long'):
    if direction == 'long':
        return entry - multiplier * atr
    return entry + multiplier * atr
```

### 4. Trailing Stop
```python
def trailing_stop(prices, trail_pct=0.05):
    peak = prices.cummax()
    stop = peak * (1 - trail_pct)
    triggered = prices < stop
    return stop, triggered
```

### 5. Chandelier Exit
```python
def chandelier_exit(highs, closes, atr, multiplier=3.0):
    highest_high = highs.rolling(22).max()
    return highest_high - multiplier * atr
```

### 6. Time-Based Stop
```python
def time_stop(entry_date, current_date, max_holding_days=10):
    return (current_date - entry_date).days >= max_holding_days
```

## Strategy-Level vs Trade-Level Stops

| Level | What It Protects | Example |
|---|---|---|
| **Trade** | Individual position | ATR stop at 2× ATR |
| **Strategy** | Strategy allocation | Halt at -5% drawdown |
| **Portfolio** | Total capital | Kill switch at -10% daily |

## Stop Placement Considerations

```
Too tight: High win rate on exits → but you exit winners too early
Too wide:  Let trades breathe → but losers can get very large
Optimal:   Wide enough to survive noise, tight enough to cap loss
```

**Rule of thumb:** Stop should be placed beyond normal market noise.
- Intraday: 1-2× ATR
- Swing: 2-3× ATR
- Trend following: 3-5× ATR

## Pros and Cons

| Pros | Cons |
|---|---|
| Limits max loss per trade | Gets triggered by normal volatility (whipsaw) |
| Removes emotion from exits | Reduces win rate |
| Enables position sizing | Guarantees realized losses |
| Required for risk management | Slippage on stop execution in fast markets |

## When NOT to Use Stops

1. **Market-neutral strategies** — Hedged positions have natural protection
2. **Mean reversion** — You're buying dips; a stop prevents the reversion
3. **Options strategies** — Max loss is already defined by premium paid

---

**Related:** [[Risk Management MOC]] | [[Position Sizing]] | [[Drawdown Management]] | [[Order Types and Execution]] | [[Trend Following]]
