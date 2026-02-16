# Tail Risk and Black Swans

**Financial returns have fat tails — extreme events happen far more often than normal distributions predict. A 5-sigma event should happen once every 14,000 years under normality. In markets, it happens every few years.**

---

## Fat Tails in Finance

```
                  Normal Distribution
                  vs
                  Actual Market Returns

Normal:  99.7% within ±3σ     1 in 370 days beyond 3σ
Actual:  ~99% within ±3σ      1 in 50-100 days beyond 3σ
```

**Excess kurtosis** of stock returns: typically 3-10 (vs 0 for normal).

## Historical Tail Events

| Event | Year | S&P Drop | "Sigma" Under Normal |
|---|---|---|---|
| Black Monday | 1987 | -20.5% in 1 day | ~25σ |
| LTCM | 1998 | -20% in weeks | ~7σ |
| GFC | 2008 | -57% peak-trough | N/A |
| Flash Crash | 2010 | -9% in minutes | ~10σ |
| COVID Crash | 2020 | -34% in 23 days | ~8σ |

## Extreme Value Theory (EVT)

Model the tails directly using the Generalized Pareto Distribution:

```python
from scipy.stats import genpareto

def fit_tail(returns, threshold_percentile=5):
    threshold = np.percentile(returns, threshold_percentile)
    tail_data = -(returns[returns < threshold] - threshold)

    shape, loc, scale = genpareto.fit(tail_data, floc=0)

    # Probability of loss > x
    def tail_probability(x):
        return genpareto.sf(x - abs(threshold), shape, loc, scale) * (threshold_percentile / 100)

    return shape, scale, tail_probability
```

## Tail Hedging Strategies

| Strategy | Cost | Protection | Complexity |
|---|---|---|---|
| OTM Put options | Premium (2-5%/yr) | Direct downside hedge | Low |
| VIX calls | Premium | Vol spike protection | Medium |
| Trend following allocation | Drag in calm markets | Crisis alpha | Medium |
| Tail risk funds | 3-8%/yr drag | Outsourced protection | Low |
| Cash buffer | Opportunity cost | Always available | Lowest |

## Stress Testing

```python
def stress_test_portfolio(weights, returns_df, scenarios=None):
    if scenarios is None:
        scenarios = {
            'GFC_2008': ('2008-09-01', '2008-11-30'),
            'COVID_2020': ('2020-02-19', '2020-03-23'),
            'Flash_Crash': ('2010-05-06', '2010-05-06'),
        }

    results = {}
    for name, (start, end) in scenarios.items():
        period_returns = returns_df.loc[start:end]
        port_return = (period_returns @ weights).sum()
        results[name] = port_return

    return results
```

## Key Principles

1. **Normal distributions underestimate tail risk by 10-100x**
2. **Correlations spike to 1.0 in tail events** — see [[Correlation and Diversification]]
3. **Tail hedging has a cost** — like insurance, you pay premium in good times
4. **Position sizing is your first line of defense** — see [[Position Sizing]]
5. **Diversification partially fails** — but still better than concentration

---

**Related:** [[Risk Management MOC]] | [[Value at Risk (VaR)]] | [[Correlation and Diversification]] | [[Options Strategies for Algos]] | [[Monte Carlo Simulation]]
