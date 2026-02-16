# Risk Management — Map of Content

> Risk management is the only thing that keeps you in the game long enough for your edge to play out. Without it, even the best alpha is worthless.

---

## Risk Taxonomy

```
                         RISK
                          |
          +---------------+---------------+
          |               |               |
     Market Risk    Operational Risk  Liquidity Risk
          |               |               |
    +-----+-----+    +---+---+      +----+----+
    |     |     |    |       |      |         |
  Price  Vol  Corr  Tech  Human   Funding  Market
  Risk   Risk Risk  Fail  Error   Liq.     Liq.
```

## Key Formulas Quick Reference

```
VaR (Parametric):    VaR = μ - z_α × σ × √t
Expected Shortfall:  ES = E[L | L > VaR]
Kelly Fraction:      f* = (p × b - q) / b
Position Size:       N = (Capital × Risk%) / (Entry - Stop)
Sharpe Ratio:        SR = (R - Rf) / σ
Max Drawdown:        MDD = max(peak - trough) / peak
```

## All Risk Management Notes

### Position Management
- [[Position Sizing]] — How much to risk per trade
- [[Kelly Criterion]] — Optimal bet sizing from information theory
- [[Stop Loss Strategies]] — When and how to exit losing trades

### Portfolio Risk
- [[Value at Risk (VaR)]] — Quantifying downside exposure
- [[Drawdown Management]] — Circuit breakers and equity curve trading
- [[Correlation and Diversification]] — Why diversification fails in crises
- [[Tail Risk and Black Swans]] — Fat tails, extreme events, and protection

### Risk Metrics
- [[Performance Metrics]] — Sharpe, Sortino, Calmar, and more

## Risk Limits Framework (Institutional)

| Limit Type | Example | Frequency |
|---|---|---|
| **VaR Limit** | Portfolio VaR < 2% of NAV | Daily |
| **Position Limit** | Max 5% of NAV per name | Per trade |
| **Sector Limit** | Max 25% in any sector | Daily |
| **Drawdown Limit** | Halt at -10% from HWM | Real-time |
| **Daily Loss Limit** | Stop trading at -2% daily | Intraday |
| **Gross Exposure** | Max 200% gross | Real-time |
| **Net Exposure** | Between -20% and +20% | Real-time |

---

**Related:** [[Trading Algorithms Master Index]] | [[Strategies MOC]] | [[Backtesting MOC]] | [[Performance Metrics]] | [[Portfolio Management MOC]]
