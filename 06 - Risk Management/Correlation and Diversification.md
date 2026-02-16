# Correlation and Diversification

**Diversification is the only free lunch in finance — but the lunch gets taken away precisely when you need it most. Correlations spike toward 1.0 in crises.**

---

## Correlation Measures

| Measure | Type | Outlier Robust | Best For |
|---|---|---|---|
| **Pearson** | Linear | No | Normal data |
| **Spearman** | Rank (monotonic) | Yes | Non-normal data |
| **Kendall** | Concordance | Yes | Small samples |

```python
def rolling_correlation(series_a, series_b, windows=[21, 63, 252]):
    result = pd.DataFrame(index=series_a.index)
    for w in windows:
        result[f'corr_{w}d'] = series_a.rolling(w).corr(series_b)
    return result
```

## Correlation Breakdown in Crises

| Event | Pre-Crisis Avg Corr | Crisis Corr |
|---|---|---|
| GFC (2008) | 0.35 | 0.85+ |
| COVID Crash (2020) | 0.35 | 0.80+ |
| Rate Shock (2022) | 0.25 | 0.65+ |

**Why:** Margin calls force liquidation across all positions simultaneously.

## Regime-Conditional Correlation

```python
def regime_correlation(returns_df, market_returns, threshold_pct=10):
    stress_threshold = np.percentile(market_returns, threshold_pct)
    stress_mask = market_returns <= stress_threshold
    calm_mask = ~stress_mask

    return {
        'stress_corr': returns_df[stress_mask].corr(),
        'calm_corr': returns_df[calm_mask].corr(),
    }
```

## Diversification Ratio

```
DR = (Σ w_i × σ_i) / σ_portfolio

DR = 1.0: No diversification benefit
DR > 1.0: Diversification is working
```

```python
def diversification_ratio(weights, cov_matrix):
    vols = np.sqrt(np.diag(cov_matrix))
    port_vol = np.sqrt(weights @ cov_matrix @ weights)
    return (np.abs(weights) @ vols) / port_vol
```

## Risk Budgeting

```python
def risk_contributions(weights, cov_matrix):
    port_vol = np.sqrt(weights @ cov_matrix @ weights)
    marginal = cov_matrix @ weights / port_vol
    return weights * marginal  # Each asset's risk contribution
```

## Building Robust Diversification

1. **Different asset classes** — equities, bonds, commodities, FX
2. **Different strategies** — momentum, mean reversion, carry, value
3. **Different time horizons** — intraday, daily, weekly, monthly
4. **Stress-test with crisis correlations** — not calm-period
5. **Monitor correlation regime** — detect when diversification breaks down

> **Key insight:** Value and Momentum are negatively correlated (~-0.40). Combining them is one of the most robust diversification strategies.

---

**Related:** [[Risk Management MOC]] | [[Portfolio Optimization]] | [[Factor Models]] | [[Tail Risk and Black Swans]] | [[Value at Risk (VaR)]]
