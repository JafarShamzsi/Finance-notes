# Performance Attribution

Performance attribution answers the critical question: **Where did the returns come from?** It decomposes portfolio returns into explainable sources to evaluate skill vs. luck.

---

## Why Attribution Matters

- **Evaluate PMs** — Is the alpha from skill or risk exposure?
- **Risk monitoring** — Are returns coming from intended sources?
- **Client reporting** — Explain performance to investors
- **Strategy improvement** — Identify what's working and what's not

---

## Brinson Attribution (Equity, Relative to Benchmark)

The classic Brinson-Hood-Beebower (1986) model:

$$R_p - R_b = \text{Allocation} + \text{Selection} + \text{Interaction}$$

| Component | Formula | Meaning |
|-----------|---------|---------|
| **Allocation** | $\sum_j (w_{p,j} - w_{b,j}) \cdot R_{b,j}$ | Overweighting winning sectors |
| **Selection** | $\sum_j w_{b,j} \cdot (R_{p,j} - R_{b,j})$ | Picking better stocks within sectors |
| **Interaction** | $\sum_j (w_{p,j} - w_{b,j}) \cdot (R_{p,j} - R_{b,j})$ | Combined effect |

```python
def brinson_attribution(port_weights, bench_weights, port_returns, bench_returns):
    """
    Brinson-Hood-Beebower attribution by sector.

    All inputs are arrays of shape (n_sectors,).
    """
    allocation = (port_weights - bench_weights) * bench_returns
    selection = bench_weights * (port_returns - bench_returns)
    interaction = (port_weights - bench_weights) * (port_returns - bench_returns)

    return {
        'allocation': allocation,
        'selection': selection,
        'interaction': interaction,
        'total_allocation': allocation.sum(),
        'total_selection': selection.sum(),
        'total_interaction': interaction.sum(),
        'total_active': allocation.sum() + selection.sum() + interaction.sum()
    }
```

---

## Factor-Based Attribution

Decompose returns using a factor model (used at JPM, Bloomberg PORT):

$$R_p = \alpha + \sum_k \beta_k F_k + \epsilon$$

| Source | Calculation |
|--------|-------------|
| Factor return | $\sum_k \beta_k F_k$ |
| Alpha (skill) | $\alpha$ |
| Specific return | $\epsilon$ |

**Common factors:** Market, Size, Value, Momentum, Quality, Volatility, Industry

---

## Key Performance Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Sharpe Ratio** | $(R_p - R_f) / \sigma_p$ | Reward per unit of total risk |
| **Information Ratio** | $(R_p - R_b) / \sigma_{tracking}$ | Reward per unit of active risk |
| **Sortino Ratio** | $(R_p - R_f) / \sigma_{downside}$ | Reward per unit of downside risk |
| **Calmar Ratio** | $R_p / \text{MaxDD}$ | Return per unit of drawdown |
| **Treynor Ratio** | $(R_p - R_f) / \beta$ | Reward per unit of market risk |
| **Alpha** | $R_p - [R_f + \beta(R_m - R_f)]$ | Excess return above CAPM |

---

## Multi-Period Attribution

Single-period attribution doesn't compound correctly. Solutions:

1. **Geometric linking** — Carino (1999) method
2. **Frongello method** — Smooth daily attribution to monthly
3. **GRAP** — Geometric attribution with daily precision

**Rule:** Always do attribution daily, then link to longer periods.

---

## Related Notes
- [[Factor Models]] — Foundation for factor attribution
- [[Portfolio Management MOC]] — Parent note
- [[Backtesting MOC]] — Performance metrics in backtesting
- [[Performance Metrics]] — Detailed metric calculations
