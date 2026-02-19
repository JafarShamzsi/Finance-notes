# Performance Metrics

Evaluating a trading strategy requires more than just looking at the final profit. A quant must analyze the **risk-adjusted returns**, the **consistency** of the signal, and the **tails** of the return distribution.

---

## 1. Risk-Adjusted Returns

| Metric | Formula | Description |
|--------|---------|-------------|
| **Sharpe Ratio** | $\frac{R_p - R_f}{\sigma_p}$ | Reward per unit of total risk. Most common, but assumes normal returns. |
| **Sortino Ratio** | $\frac{R_p - R_f}{\sigma_{down}}$ | Only penalizes downside volatility. Better for asymmetric strategies. |
| **Information Ratio** | $\frac{\alpha}{\text{Tracking Error}}$ | Measures excess return relative to a benchmark. |
| **Calmar Ratio** | $\frac{\text{Annual Return}}{\text{Max Drawdown}}$ | Reward relative to the worst-case historical loss. |

---

## 2. Drawdown Metrics

Drawdowns are the true test of a quant's psychological and financial resilience.
- **Max Drawdown (MDD):** The largest peak-to-trough decline.
- **Drawdown Duration:** The time spent "underwater" before hitting a new high.
- **Ulcer Index:** Measures the depth and duration of drawdowns simultaneously.

---

## 3. Trade-Level Statistics

| Metric | Calculation | Goal |
|--------|-------------|------|
| **Win Rate** | $\frac{N_{winning}}{N_{total}}$ | Dependent on strategy type (Trend vs. Mean Rev). |
| **Profit Factor** | $\frac{\text{Gross Profit}}{\text{Gross Loss}}$ | Should be $> 1.5$ for a robust strategy. |
| **Avg Win / Avg Loss** | $\frac{\mu_{win}}{\mu_{loss}}$ | The "Payoff Ratio." |
| **CPC Index** | $\text{Profit Factor} \times \text{Win Rate} \times \text{Payoff Ratio}$ | A composite score of trade quality. |

---

## 4. Signal Quality: Information Coefficient (IC)

The **Information Coefficient** measures the correlation between the predicted return and the actual return.
- **IC:** $\text{corr}(\hat{r}_{t+1}, r_{t+1})$.
- **ICIR:** $\frac{\mu_{IC}}{\sigma_{IC}}$ (The "Information Coefficient Information Ratio") — measures signal stability.

---

## 5. Python Implementation: Basic Tearsheet

```python
import numpy as np

def calculate_tearsheet(returns):
    """
    returns: pd.Series of daily returns
    """
    # Risk-Adjusted
    sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252)
    
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_dd = drawdown.min()
    
    # Win Stats
    win_rate = (returns > 0).mean()
    profit_factor = abs(returns[returns > 0].sum() / returns[returns < 0].sum())
    
    return {
        'sharpe': round(sharpe, 2),
        'max_dd': round(max_dd, 4),
        'win_rate': round(win_rate, 2),
        'profit_factor': round(profit_factor, 2)
    }
```

---

## 6. Regulatory Metrics (VaR)

- **Value at Risk (VaR):** The expected loss at a certain confidence level (e.g., 95% 1-day VaR).
- **Expected Shortfall (CVaR):** The average loss *given* that the VaR threshold has been breached.
- See [[Value at Risk (VaR)]] for details.

---

## Related Notes
- [[Backtesting MOC]] — Where metrics are generated
- [[Value at Risk (VaR)]] — Risk-specific metrics
- [[Alpha Research]] — Measuring signal IC
- [[Walk-Forward Analysis]] — Evaluating OOS performance
- [[Drawdown Management]] — How to handle the metrics
- [[Performance Attribution]] — Decomposing the returns
