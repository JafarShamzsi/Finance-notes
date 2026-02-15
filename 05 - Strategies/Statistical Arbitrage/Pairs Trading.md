# Pairs Trading

**Core Idea:** Find two historically correlated/cointegrated stocks. When their price relationship diverges, bet on convergence. One of the oldest and most robust [[Statistical Arbitrage]] strategies.

---

## How It Works

```
1. Find pair (e.g., Coca-Cola & Pepsi)
2. Compute spread: Spread = Price_A - β × Price_B
3. When spread is abnormally wide → short the outperformer, long the underperformer
4. When spread reverts to mean → close both positions
5. Profit from convergence regardless of market direction
```

## Step-by-Step Implementation

### Step 1: Pair Selection

**Methods:**
1. **Fundamental** — Same industry, similar business (KO/PEP, XOM/CVX, GS/MS)
2. **Statistical** — Screen all pairs for cointegration
3. **Hybrid** — Filter by sector first, then test cointegration

```python
import itertools
from statsmodels.tsa.stattools import coint

def screen_pairs(prices_df, sector_map=None, significance=0.05):
    """
    Screen universe for cointegrated pairs.
    """
    tickers = prices_df.columns.tolist()

    # Optional: only test within sectors
    if sector_map:
        pair_candidates = []
        for sector, members in sector_map.items():
            pair_candidates.extend(itertools.combinations(members, 2))
    else:
        pair_candidates = itertools.combinations(tickers, 2)

    results = []
    for t1, t2 in pair_candidates:
        score, pvalue, _ = coint(prices_df[t1], prices_df[t2])
        if pvalue < significance:
            # Calculate correlation too
            corr = prices_df[t1].pct_change().corr(prices_df[t2].pct_change())
            results.append({
                'pair': (t1, t2),
                'coint_pvalue': pvalue,
                'correlation': corr
            })

    return sorted(results, key=lambda x: x['coint_pvalue'])
```

### Step 2: Hedge Ratio Calculation

```python
import statsmodels.api as sm

def calculate_hedge_ratio(y, x, method='ols'):
    """
    Calculate hedge ratio (β) for the spread.
    Spread = Y - β·X
    """
    if method == 'ols':
        X = sm.add_constant(x)
        model = sm.OLS(y, X).fit()
        return model.params.iloc[1]

    elif method == 'tls':
        # Total Least Squares (more symmetric)
        from scipy import odr
        data = odr.Data(x, y)
        model = odr.Model(lambda B, x: B[0] * x + B[1])
        out = odr.ODR(data, model, beta0=[1, 0]).run()
        return out.beta[0]
```

### Step 3: Trading Signal

```python
class PairsTradingStrategy:
    def __init__(self, lookback=60, entry_z=2.0, exit_z=0.0,
                 stop_z=3.5, recalc_hedge=True):
        self.lookback = lookback
        self.entry_z = entry_z
        self.exit_z = exit_z
        self.stop_z = stop_z
        self.recalc_hedge = recalc_hedge

    def run(self, price_a, price_b):
        """Execute pairs trading strategy."""
        signals_a = pd.Series(0.0, index=price_a.index)
        signals_b = pd.Series(0.0, index=price_b.index)
        position = 0

        for i in range(self.lookback, len(price_a)):
            # Rolling hedge ratio
            window_a = price_a.iloc[i-self.lookback:i]
            window_b = price_b.iloc[i-self.lookback:i]
            hedge = calculate_hedge_ratio(window_a, window_b)

            # Compute spread and z-score
            spread = price_a.iloc[i] - hedge * price_b.iloc[i]
            spread_hist = price_a.iloc[i-self.lookback:i] - hedge * price_b.iloc[i-self.lookback:i]
            z = (spread - spread_hist.mean()) / spread_hist.std()

            # Entry
            if position == 0:
                if z > self.entry_z:   # Spread too wide
                    position = -1       # Short A, Long B
                elif z < -self.entry_z: # Spread too narrow
                    position = 1        # Long A, Short B

            # Exit
            elif position == 1 and z >= self.exit_z:
                position = 0
            elif position == -1 and z <= -self.exit_z:
                position = 0

            # Stop loss
            if abs(z) > self.stop_z:
                position = 0

            signals_a.iloc[i] = position
            signals_b.iloc[i] = -position * hedge

        return signals_a, signals_b
```

## Classic Pairs Examples

| Pair | Sector | Rationale |
|---|---|---|
| KO / PEP | Consumer Staples | Same industry, similar products |
| XOM / CVX | Energy | Both oil majors, same drivers |
| GS / MS | Financials | Both investment banks |
| GOOG / META | Tech | Both ad-revenue driven |
| GLD / GDX | Commodities | Gold vs gold miners |
| SPY / IWM | Indices | Large cap vs small cap spread |

## Advanced Techniques

### Rolling Cointegration Check
Pair relationships break down. Re-test cointegration regularly:
```python
def is_still_cointegrated(y, x, window=252, threshold=0.05):
    """Check if pair is still cointegrated over recent window."""
    _, pvalue, _ = coint(y[-window:], x[-window:])
    return pvalue < threshold
```

### Dollar-Neutral Position Sizing
```
Position_A = Capital / 2 / Price_A × sign
Position_B = Capital / 2 / Price_B × (-sign) × hedge_ratio
```

### Risk Management
- Maximum position hold time (force exit after N days)
- Portfolio of 10-20 pairs for diversification
- Maximum correlation between pairs in portfolio
- See [[Position Sizing]], [[Drawdown Management]]

## Common Pitfalls

1. **Data mining bias** — Finding spurious cointegration in-sample
2. **Structural breaks** — M&A, spin-offs, business model changes
3. **Crowding** — Popular pairs get arbed away
4. **Execution** — Need to enter both legs simultaneously
5. **Margin** — Short positions require borrowing (locate, fees)

---

**Related:** [[Statistical Arbitrage]] | [[Mean Reversion Strategies]] | [[Kalman Filter]] | [[Cointegration]] | [[Sample Strategy - Pairs Trading]]
