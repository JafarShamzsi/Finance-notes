# Probability and Statistics for Trading

Essential statistical concepts every quant must master.

---

## Distributions in Finance

### Normal Distribution
```
f(x) = (1/σ√2π) × e^(-(x-μ)²/2σ²)

68% of data within ±1σ
95% of data within ±2σ
99.7% of data within ±3σ
```

**Problem:** Financial returns are NOT normally distributed. They have:
- **Fat tails** — Extreme events happen more often than normal predicts
- **Negative skewness** — Crashes are larger than rallies
- **Excess kurtosis** — More peaked, heavier tails

### Log-Normal Distribution
If log(X) is normal, X is log-normal. Stock prices are often modeled as log-normal (prices can't go negative).

### Student's t-Distribution
Better for modeling fat-tailed returns. Has a degrees-of-freedom parameter (ν) controlling tail heaviness.

### Power Law / Pareto
Extreme events follow power laws:
```
P(X > x) ~ x^(-α)

α ≈ 3 for stock returns (cubic law)
```

## Key Statistical Measures

```python
import numpy as np
import scipy.stats as stats

def compute_statistics(returns):
    """Comprehensive return statistics."""
    return {
        'mean': np.mean(returns),
        'std': np.std(returns),
        'skewness': stats.skew(returns),
        'kurtosis': stats.kurtosis(returns),  # Excess kurtosis
        'sharpe': np.mean(returns) / np.std(returns) * np.sqrt(252),
        'sortino': sortino_ratio(returns),
        'max_drawdown': max_drawdown(returns),
        'var_95': np.percentile(returns, 5),
        'cvar_95': returns[returns <= np.percentile(returns, 5)].mean(),
        'jarque_bera': stats.jarque_bera(returns),
    }

def sortino_ratio(returns, target=0, annual_factor=252):
    downside = returns[returns < target]
    downside_std = np.std(downside) * np.sqrt(annual_factor)
    annual_return = np.mean(returns) * annual_factor
    return annual_return / downside_std

def max_drawdown(returns):
    cumulative = (1 + pd.Series(returns)).cumprod()
    peak = cumulative.expanding().max()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()
```

## Hypothesis Testing for Trading

### Is My Strategy Real?

**Null Hypothesis (H₀):** Strategy has zero alpha (returns are random).

#### t-test on Returns
```python
def strategy_significance(returns, confidence=0.95):
    """Test if strategy returns are significantly different from zero."""
    t_stat, p_value = stats.ttest_1samp(returns, 0)
    n = len(returns)
    sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252)

    # Minimum backtest length for significant Sharpe
    # t_stat ≈ Sharpe × √(n/252)
    min_years = (stats.norm.ppf(confidence) / sharpe) ** 2 / 252

    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < (1 - confidence),
        'sharpe': sharpe,
        'min_years_needed': min_years
    }
```

#### Multiple Testing Correction
When testing many strategies, some will appear significant by chance.

```python
# Bonferroni correction
adjusted_threshold = 0.05 / num_strategies_tested

# Benjamini-Hochberg (FDR control)
from statsmodels.stats.multitest import multipletests
reject, adjusted_pvals, _, _ = multipletests(p_values, method='fdr_bh')
```

**Bailey, Borwein, Lopez de Prado:** If you tested N strategies, expected max Sharpe of random strategies is:
```
E[max SR] ≈ √(2·ln(N)) × (1 - γ/(2·ln(N))) + γ/√(2·ln(N))

Where γ ≈ 0.5772 (Euler-Mascheroni constant)
```

Your strategy must beat this threshold.

## Regression Analysis

### OLS (Ordinary Least Squares)
```python
import statsmodels.api as sm

# Factor regression
X = sm.add_constant(factor_returns)  # Market, Size, Value, Momentum
model = sm.OLS(strategy_returns, X).fit()

print(model.summary())
# Check:
# - Alpha (intercept): Significant and positive?
# - Factor betas: What risks are you taking?
# - R²: How much is explained by factors?
```

### Rolling Regression
Parameters change over time:
```python
def rolling_beta(returns, market_returns, window=60):
    betas = []
    for i in range(window, len(returns)):
        y = returns[i-window:i]
        x = sm.add_constant(market_returns[i-window:i])
        model = sm.OLS(y, x).fit()
        betas.append(model.params[1])
    return pd.Series(betas, index=returns.index[window:])
```

## Bayesian Methods

### Bayesian Updating for Signal Confidence
```python
def bayesian_signal_update(prior_prob, signal_accuracy, signal_value):
    """
    Update belief about market direction given a signal.

    prior_prob: Prior probability of up move
    signal_accuracy: P(signal=up | market=up)
    signal_value: 'up' or 'down'
    """
    if signal_value == 'up':
        # P(up|signal=up) = P(signal=up|up)×P(up) / P(signal=up)
        p_signal = signal_accuracy * prior_prob + (1-signal_accuracy) * (1-prior_prob)
        posterior = signal_accuracy * prior_prob / p_signal
    else:
        p_signal = (1-signal_accuracy) * prior_prob + signal_accuracy * (1-prior_prob)
        posterior = (1-signal_accuracy) * prior_prob / p_signal

    return posterior
```

## Correlation Analysis

```python
def rolling_correlation(x, y, window=60):
    return x.rolling(window).corr(y)

def correlation_matrix_analysis(returns_df):
    """Analyze correlation structure of returns."""
    corr = returns_df.corr()
    eigenvalues = np.linalg.eigvals(corr)

    # Random Matrix Theory: clean noise
    # Marchenko-Pastur distribution bounds
    T, N = returns_df.shape
    q = T / N
    lambda_plus = (1 + 1/np.sqrt(q))**2
    lambda_minus = (1 - 1/np.sqrt(q))**2

    # Eigenvalues above lambda_plus are signal, below are noise
    signal_eigenvalues = eigenvalues[eigenvalues > lambda_plus]

    return corr, eigenvalues, signal_eigenvalues
```

---

**Related:** [[Mathematics MOC]] | [[Time Series Analysis]] | [[Performance Metrics]] | [[Overfitting and Curve Fitting]] | [[Value at Risk (VaR)]]
