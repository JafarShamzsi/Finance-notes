# Factor Investing

Factor investing systematically harvests risk premia by constructing long-short portfolios that are exposed to specific return-driving factors. This is the bread and butter of quant equity — the dominant strategy at AQR, Dimensional, and many JPM/Goldman desks.

---

## The Major Factors

### Value
**Buy cheap, sell expensive** relative to fundamentals.

| Metric | Formula | Classic |
|--------|---------|---------|
| Book-to-Market | Book value / Market cap | Fama-French HML |
| Earnings Yield | E/P (inverse of P/E) | |
| Cash Flow Yield | FCF / EV | |
| Sales Yield | Revenue / EV | |

**Why it works:** Behavioral overreaction to bad news, risk of distress
**When it fails:** Structural disruption (value traps), prolonged growth regime (2018-2020)

### Momentum
**Buy recent winners, sell recent losers.**

| Variant | Lookback | Holding |
|---------|----------|---------|
| Classic cross-sectional | 12-1 months | 1 month |
| Industry momentum | 12-1 months | 1 month |
| Earnings momentum | Earnings surprise | 3 months |
| Short-term reversal | 1 week | 1 week |

**Why it works:** Underreaction, behavioral herding, institutional flows
**When it fails:** Momentum crashes (rapid reversals after extreme markets)

See [[Momentum Strategies]] for implementation details.

### Quality
**Buy high-quality companies, sell low-quality.**

| Signal | Measure |
|--------|---------|
| Profitability | ROE, ROA, gross margin |
| Earnings stability | Earnings volatility, accruals |
| Financial strength | Low leverage, high interest coverage |
| Payout | Dividend growth, buybacks |

**Why it works:** Market undervalues stable, profitable companies
**When it fails:** Rarely — most defensive factor

### Low Volatility
**Low-vol stocks outperform high-vol stocks on a risk-adjusted basis** (the "low-vol anomaly").

**Why it works:**
- Lottery preference: investors overpay for volatile "lottery" stocks
- Leverage constraints: can't lever up low-vol, so they're underpriced
- Benchmarking: PMs are benchmarked to indices, not incentivized to hold low-vol

### Size
**Small caps outperform large caps** (the SMB factor). Weakest factor — premium has shrunk and is debated.

### Carry
**Assets with higher yield tend to outperform** (across currencies, bonds, commodities).

---

## Factor Construction: Long-Short Portfolios

```python
import pandas as pd
import numpy as np

def construct_factor_portfolio(scores, returns, n_quantiles=5):
    """
    Construct a long-short factor portfolio.

    Parameters:
        scores: pd.DataFrame (dates × stocks) — factor scores
        returns: pd.DataFrame (dates × stocks) — forward returns
        n_quantiles: Number of quantile buckets

    Returns:
        factor_return: pd.Series — long-short factor return
    """
    factor_returns = []

    for date in scores.index:
        score = scores.loc[date].dropna()
        ret = returns.loc[date].reindex(score.index).dropna()
        common = score.index.intersection(ret.index)

        if len(common) < n_quantiles * 5:
            continue

        score = score[common]
        ret = ret[common]

        # Rank into quantiles
        quantiles = pd.qcut(score, n_quantiles, labels=False, duplicates='drop')

        # Long top quantile, short bottom quantile
        long_ret = ret[quantiles == n_quantiles - 1].mean()
        short_ret = ret[quantiles == 0].mean()

        factor_returns.append({
            'date': date,
            'long_short': long_ret - short_ret,
            'long_only': long_ret,
            'short_only': short_ret
        })

    return pd.DataFrame(factor_returns).set_index('date')
```

---

## Multi-Factor Portfolios

Combining factors is better than single-factor investing:

### Integration Approaches

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **Portfolio mixing** | Separate factor portfolios, combine at portfolio level | Simple, transparent | Higher turnover |
| **Signal mixing** | Combine factor scores, then construct one portfolio | Lower turnover | Factor dilution |
| **Sequential screens** | Filter by one factor, then sort by another | Simple | Loses diversification |

```python
def multi_factor_score(value_score, momentum_score, quality_score,
                       weights={'value': 0.4, 'momentum': 0.3, 'quality': 0.3}):
    """Combine factor scores into composite alpha signal."""
    # Z-score each factor cross-sectionally
    value_z = (value_score - value_score.mean()) / value_score.std()
    mom_z = (momentum_score - momentum_score.mean()) / momentum_score.std()
    qual_z = (quality_score - quality_score.mean()) / quality_score.std()

    composite = (weights['value'] * value_z +
                 weights['momentum'] * mom_z +
                 weights['quality'] * qual_z)

    return composite
```

---

## Factor Timing (Controversial)

Can you predict which factors will perform well?

| Signal | Predicts | Evidence |
|--------|---------|----------|
| Value spread | Value factor | Moderate (wide spreads → value outperforms) |
| Momentum crashes | Anti-momentum | Weak |
| Volatility regime | Low-vol factor | Moderate |
| Macro indicators | Multiple | Mixed |

**Consensus:** Factor timing is hard. Most quants maintain static factor weights.

---

## Performance History (US Equities)

| Factor | Annual Return | Volatility | Sharpe | Max DD |
|--------|--------------|-----------|--------|--------|
| Market | 8-10% | 15-20% | 0.4-0.5 | -50% |
| Value | 3-5% | 10-12% | 0.3-0.4 | -30% |
| Momentum | 5-8% | 12-15% | 0.4-0.6 | -40% |
| Quality | 3-5% | 8-10% | 0.4-0.5 | -15% |
| Low Vol | 2-4% | 8-10% | 0.3-0.4 | -20% |
| Size | 1-3% | 10-12% | 0.1-0.2 | -30% |
| Multi-factor | 5-10% | 8-12% | 0.5-0.8 | -20% |

---

## Related Notes
- [[Factor Models]] — Mathematical foundation
- [[Modern Portfolio Theory]] — Portfolio construction
- [[Alpha Research]] — Alpha generation pipeline
- [[Momentum Strategies]] — Momentum factor deep dive
- [[Mean Reversion Strategies]] — Value/reversal factors
- [[Strategies MOC]] — Strategy index
- [[Performance Attribution]] — Factor-based attribution
- [[Key People in Quant Finance]] — Cliff Asness (AQR), Fama, French
