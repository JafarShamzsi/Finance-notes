# Trend Following

**Core Idea:** Identify and ride sustained price trends across any asset class. Don't predict — react. The oldest and most durable systematic strategy.

---

## Philosophy

> "Cut your losses short and let your profits run." — Classic trend following maxim

Trend following works because:
1. **Behavioral** — Herding, anchoring, slow information diffusion
2. **Structural** — Central bank policy trends, macro cycles
3. **Crisis alpha** — Profits during market crashes (short trends)
4. **Risk premia** — Compensation for taking trend risk

## Core Signal: Price-Based

### Moving Average Systems
```python
# Dual Moving Average
long_signal = fast_ma > slow_ma  # e.g., 50-day > 200-day
short_signal = fast_ma < slow_ma

# Triple Moving Average Filter
trend_up = (fast_ma > medium_ma) and (medium_ma > slow_ma)
```

### Donchian Channel (Turtle Trading)
```python
def donchian_signal(prices, entry_period=20, exit_period=10):
    upper = prices.rolling(entry_period).max()
    lower = prices.rolling(entry_period).min()
    exit_upper = prices.rolling(exit_period).max()
    exit_lower = prices.rolling(exit_period).min()

    signal = pd.Series(0, index=prices.index)
    signal[prices >= upper] = 1     # Breakout long
    signal[prices <= lower] = -1    # Breakout short
    # Exit conditions use shorter period
    return signal
```

### Time-Series Momentum
```
Signal = sign(R_t,t-L)  where L = lookback (e.g., 12 months)

If past 12-month return > 0: Go long
If past 12-month return < 0: Go short
```

Moskowitz, Ooi, Pedersen (2012) — Works across 58 futures markets.

## Position Sizing: Volatility Targeting

**Critical to trend following success:**

```python
def volatility_target_size(capital, target_vol, asset_vol, price):
    """
    Size positions so each contributes equal risk.

    target_vol: e.g., 0.20 (20% annual)
    asset_vol: realized volatility of asset
    """
    dollar_vol = asset_vol * price
    position_size = (capital * target_vol) / (dollar_vol * np.sqrt(252))
    return int(position_size)
```

This is the **Turtle Trading** approach:
- Each market gets equal risk allocation
- High-vol assets get smaller positions
- Low-vol assets get larger positions

See [[Position Sizing]] and [[Kelly Criterion]] for more.

## Multi-Asset Trend Following

Diversification across asset classes is key:

| Asset Class | Instruments |
|---|---|
| Equity Indices | ES, NQ, FTSE, DAX, Nikkei |
| Fixed Income | ZB, ZN, Bund, Gilt |
| FX | EUR/USD, GBP/USD, USD/JPY, AUD/USD |
| Commodities | CL, GC, SI, NG, Corn, Wheat |
| Crypto | BTC, ETH |

**Typical portfolio: 20-50 futures markets**

```python
class TrendFollowingSystem:
    def __init__(self, markets, lookbacks=[20, 60, 120],
                 target_vol=0.15, max_correlation=0.5):
        self.markets = markets
        self.lookbacks = lookbacks
        self.target_vol = target_vol

    def composite_signal(self, prices):
        """Average signal across multiple lookbacks."""
        signals = []
        for lb in self.lookbacks:
            ret = prices.pct_change(lb)
            vol = prices.pct_change().rolling(lb).std() * np.sqrt(252)
            risk_adjusted = ret / vol  # Normalize by volatility
            signals.append(np.sign(risk_adjusted))

        return pd.concat(signals, axis=1).mean(axis=1)
```

## Famous Trend Followers

| Name/Firm | Known For |
|---|---|
| **Richard Dennis / Turtles** | Trained novices to trend follow profitably |
| **John W. Henry** | Systematic FX/futures trending |
| **AQR (Cliff Asness)** | Academic-driven trend following |
| **Man AHL** | One of largest managed futures |
| **Winton Group** | David Harding, systematic CTA |
| **Dunn Capital** | 40+ year track record |

## Performance Characteristics

| Metric | Typical (diversified CTA) |
|---|---|
| Annual Return | 8-15% |
| Sharpe Ratio | 0.5-1.0 |
| Max Drawdown | -15% to -30% |
| Win Rate | 35-45% (low!) |
| Avg Win / Avg Loss | 2.0-4.0 (big wins, small losses) |
| Correlation to S&P 500 | Near 0 or negative in crises |

**Key insight:** Low win rate but large average win — tail-risk harvesting.

## Crisis Alpha

Trend following historically profits during equity crashes:

| Crisis | S&P 500 | Trend Following |
|---|---|---|
| 2000-2002 Dot-com | -49% | +20-40% |
| 2008 GFC | -57% | +15-30% |
| 2020 COVID | -34% | Mixed (V-shaped recovery) |
| 2022 Inflation | -25% | +20-40% |

This makes it an excellent portfolio diversifier. See [[Correlation and Diversification]].

---

**Related:** [[Momentum Strategies]] | [[Breakout Strategies]] | [[Position Sizing]] | [[Drawdown Management]] | [[Performance Metrics]]
