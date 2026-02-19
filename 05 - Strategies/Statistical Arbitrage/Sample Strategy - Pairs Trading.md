# Sample Strategy: Pairs Trading (KO vs PEP)

This is a walkthrough of a classic mean-reversion pairs trading strategy using Coca-Cola (KO) and PepsiCo (PEP).

---

## 1. Strategy Hypothesis
KO and PEP are direct competitors in the soft drink industry. They share similar supply chains, input costs (sugar, aluminum), and consumer demand drivers. Their stock prices should be **cointegrated** — if one drifts too far from the other, the relationship should eventually revert.

---

## 2. Research & Validation

### Cointegration Test
Using daily data for the past 5 years:
- **ADF p-value:** 0.02 (Reject Null Hypothesis of unit root).
- **Conclusion:** The pair is cointegrated at the 95% confidence level.

### Hedge Ratio
- **OLS Result:** $Price_{KO} = 0.85 	imes Price_{PEP} + 2.10$
- **Hedge Ratio ($\beta$):** 0.85

---

## 3. Trading Rules

| Event | Logic | Action |
|-------|-------|--------|
| **Entry (Wide Spread)** | Spread Z-score $> +2.0$ | **Short KO / Long PEP** |
| **Entry (Narrow Spread)** | Spread Z-score $< -2.0$ | **Long KO / Short PEP** |
| **Exit (Mean Reversion)** | Spread Z-score crosses $0.0$ | **Close all positions** |
| **Stop Loss** | Spread Z-score $> |3.5|$ | **Flatten (Relationship broken)** |

---

## 4. Backtest Parameters

- **Universe:** [KO, PEP]
- **Timeframe:** 1-Hour OHLCV
- **Initial Capital:** $100,000
- **Position Sizing:** Dollar-neutral ($50k Long / $50k Short)
- **Commissions:** $0.005 per share
- **Slippage:** 1 basis point

---

## 5. Implementation (Python/VectorBT)

```python
import vectorbt as vbt
import pandas as pd

# 1. Download Data
data = vbt.YFData.download(['KO', 'PEP'], period='5y')
prices = data.get('Close')

# 2. Calculate Spread
# Assume beta=0.85 from research
spread = prices['KO'] - (0.85 * prices['PEP'])

# 3. Generate Z-score
zscore = (spread - spread.rolling(20).mean()) / spread.rolling(20).std()

# 4. Define Signals
entries = zscore < -2.0
exits = zscore > 0

# 5. Run Backtest
portfolio = vbt.Portfolio.from_signals(prices['KO'], entries, exits)
print(portfolio.total_return())
```

---

## 6. Performance Expectations

- **Sharpe Ratio:** ~1.2
- **Win Rate:** 62%
- **Max Drawdown:** -8%
- **Correlation to SPY:** 0.05 (Market Neutral)

---

## Related Notes
- [[Pairs Trading]] — Theoretical foundation
- [[Statistical Arbitrage]] — Strategy category
- [[Cointegration]] — Statistical test used
- [[Kalman Filter]] — For dynamic hedge ratios
- [[Backtesting Framework Design]] — How to test this
