# Drawdown Management

**A 50% drawdown requires a 100% return to recover. Drawdown management is the difference between a career and a cautionary tale.**

---

## Max Drawdown Calculation

```python
def max_drawdown(equity_curve):
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    max_dd = drawdown.min()
    max_dd_date = drawdown.idxmin()
    return max_dd, max_dd_date
```

## Recovery Mathematics

| Drawdown | Recovery Needed | At 10%/yr | At 20%/yr |
|---|---|---|---|
| -5% | +5.3% | ~6 months | ~3 months |
| -10% | +11.1% | ~1.1 years | ~6 months |
| -20% | +25.0% | ~2.3 years | ~1.2 years |
| -30% | +42.9% | ~3.7 years | ~1.9 years |
| -50% | +100.0% | ~7.3 years | ~3.8 years |

## Circuit Breakers

### Tiered Response

```python
class CircuitBreaker:
    def __init__(self):
        self.levels = {
            'warning':  {'dd': -0.03, 'action': 'reduce_50pct', 'cooldown_h': 4},
            'caution':  {'dd': -0.05, 'action': 'reduce_75pct', 'cooldown_h': 24},
            'stop':     {'dd': -0.08, 'action': 'flatten',      'cooldown_h': 72},
            'review':   {'dd': -0.12, 'action': 'halt',         'cooldown_h': None},
        }

    def check(self, current_dd, daily_pnl):
        if daily_pnl <= -0.02:
            return 'halt_today'
        for level, cfg in self.levels.items():
            if current_dd <= cfg['dd']:
                return cfg['action']
        return 'continue'
```

## Equity Curve Trading

Trade your own equity curve — if below its moving average, reduce or stop.

```python
def equity_curve_filter(equity_curve, ma_period=63):
    """Binary filter: full size above MA, zero below."""
    ma = equity_curve.rolling(ma_period).mean()
    return (equity_curve > ma).astype(float)
```

## Dynamic Position Reduction

```python
def drawdown_scalar(current_dd):
    """Reduce position size as drawdown deepens."""
    if current_dd >= 0: return 1.0
    elif current_dd >= -0.05: return 0.75
    elif current_dd >= -0.10: return 0.50
    elif current_dd >= -0.15: return 0.25
    else: return 0.10
```

## Drawdown Expectations by Strategy

| Strategy | Typical Max DD | Duration | Calmar Ratio |
|---|---|---|---|
| Stat Arb (L/S) | -5% to -15% | 1-6 months | 1.0-2.0 |
| Trend Following | -15% to -30% | 6-24 months | 0.3-0.7 |
| Mean Reversion (intraday) | -3% to -8% | 1-4 weeks | 2.0-5.0 |
| HFT Market Making | -1% to -3% | 1-5 days | 5.0-20.0 |
| Long-only equity | -30% to -55% | 12-60 months | 0.1-0.3 |

## Key Principles

1. **Know your max DD tolerance before you start** — not during the drawdown
2. **Live drawdowns are always worse than backtested** — slippage, timing, emotions
3. **Multiple uncorrelated strategies reduce DD** — see [[Correlation and Diversification]]
4. **Circuit breakers save careers** — systematic rules prevent emotional decisions

---

**Related:** [[Risk Management MOC]] | [[Position Sizing]] | [[Kelly Criterion]] | [[Stop Loss Strategies]] | [[Performance Metrics]] | [[Correlation and Diversification]]
