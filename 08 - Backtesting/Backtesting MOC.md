# Backtesting Map of Content

> *"All backtests are wrong. Some are useful."* — The goal is to reduce the gap between backtest and live performance.

Backtesting simulates a strategy on historical data to estimate future performance. It's the most dangerous step in quant finance — the place where overfitting destroys careers.

---

## The Backtesting Pipeline

```
Hypothesis → Data Collection → Strategy Logic → Backtest Engine → Analysis → Validation → Paper Trading → Live
     ↓              ↓                ↓                ↓              ↓            ↓
  "Momentum     Historical      Entry/exit       Event-driven   Sharpe, DD   Walk-forward
   works in     price/volume    rules, sizing    or vectorized  Calmar, IR   Out-of-sample
   crypto"      cleaned data    risk mgmt        simulation     drawdown     Monte Carlo
```

---

## Biases — The #1 Danger
- [[Lookahead Bias]] — Using future information in past decisions
- [[Survivorship Bias]] — Only testing on stocks that survived (ignoring delisted)
- [[Overfitting]] — Curve-fitting to noise instead of signal

### Other Critical Biases
| Bias | Description | Prevention |
|------|-------------|------------|
| **Selection bias** | Cherry-picking the best strategy variant | Test all variants, report all results |
| **Time-period bias** | Strategy works in one period, not others | Test across regimes (bull, bear, sideways) |
| **Data-snooping** | Testing many strategies, reporting only winners | Bonferroni correction, family-wise error rate |
| **Transaction cost bias** | Ignoring or underestimating trading costs | Use realistic spread, slippage, market impact |
| **Fill assumption bias** | Assuming fills at mid-price or close | Model partial fills, queue position |

---

## Framework Design
- [[Backtesting Framework Design]] — Architecture of a backtest engine
- [[Walk-Forward Analysis]] — Rolling out-of-sample validation

### Event-Driven vs. Vectorized

| Approach | Speed | Accuracy | Complexity |
|----------|-------|----------|------------|
| **Vectorized** | Very fast | Lower (simplifications) | Low |
| **Event-driven** | Slow | High (realistic fills) | High |

**Vectorized:** Compute signals on entire array at once. Good for research.
**Event-driven:** Simulate bar-by-bar or tick-by-tick. Good for production-like testing.

---

## Platforms and Frameworks
- [[Backtesting Platforms and Frameworks]] — Tools comparison

| Platform | Language | Best For | Cost |
|----------|----------|----------|------|
| **Backtrader** | Python | General purpose, flexible | Free |
| **Zipline** | Python | Equity strategies | Free |
| **QuantConnect** | Python/C# | Cloud, multi-asset, live trading | Free/Paid |
| **VectorBT** | Python | Fast vectorized backtesting | Free |
| **QuantLib** | C++/Python | Derivatives pricing | Free |
| Custom engine | Any | Full control, production systems | Build cost |

---

## Performance Analysis
- [[Performance Metrics]] — Sharpe, Sortino, Calmar, drawdown, etc.

### Key Metrics Checklist

| Metric | Good | Great | Red Flag |
|--------|------|-------|----------|
| **Sharpe Ratio** | > 0.5 | > 1.5 | > 3.0 (likely overfit) |
| **Max Drawdown** | < 20% | < 10% | > 40% |
| **Calmar Ratio** | > 0.5 | > 1.0 | < 0.2 |
| **Win Rate** | > 45% | > 55% | > 70% (unless market making) |
| **Profit Factor** | > 1.2 | > 2.0 | > 5.0 (likely overfit) |
| **Avg Trade Duration** | Matches strategy | Consistent | Highly variable |

---

## Validation Workflow

```
1. In-sample training (60% of data)
2. Out-of-sample testing (20% of data)
3. Walk-forward analysis (rolling windows)
4. Monte Carlo simulation (randomize entry points, parameters)
5. Regime analysis (test in bull/bear/sideways/high-vol)
6. Sensitivity analysis (vary parameters ±20%)
7. Paper trading (1-3 months minimum)
8. Small live capital (1/10 target size)
9. Full deployment
```

---

## Related Areas
- [[Strategies MOC]] — Strategies to backtest
- [[Data Engineering MOC]] — Data quality is everything
- [[Risk Management MOC]] — Risk parameters in backtesting
- [[Performance Attribution]] — Understanding backtest results
- [[Execution MOC]] — Realistic execution modeling
- [[Overfitting]] — The #1 enemy
