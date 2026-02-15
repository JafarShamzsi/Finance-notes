# Monte Carlo Simulation

Use random sampling to estimate the behavior of complex systems. Essential for risk management, options pricing, and strategy validation.

---

## Core Applications in Trading

### 1. Portfolio Risk Estimation
```python
def monte_carlo_var(returns_df, weights, n_simulations=10000,
                    horizon=21, confidence=0.95):
    """
    Estimate VaR using Monte Carlo simulation.
    """
    mean = returns_df.mean().values
    cov = returns_df.cov().values

    # Simulate portfolio returns
    simulated = np.random.multivariate_normal(mean, cov,
                                               (n_simulations, horizon))
    # Portfolio returns
    port_returns = simulated @ weights

    # Cumulative returns over horizon
    cumulative = np.prod(1 + port_returns, axis=1) - 1

    var = np.percentile(cumulative, (1 - confidence) * 100)
    cvar = cumulative[cumulative <= var].mean()

    return {'VaR': var, 'CVaR': cvar}
```

### 2. Options Pricing
```python
def monte_carlo_option(S0, K, T, r, sigma, n_paths=100000, option_type='call'):
    """
    Price European option via MC simulation.
    """
    Z = np.random.standard_normal(n_paths)
    ST = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)

    if option_type == 'call':
        payoffs = np.maximum(ST - K, 0)
    else:
        payoffs = np.maximum(K - ST, 0)

    price = np.exp(-r*T) * np.mean(payoffs)
    std_error = np.exp(-r*T) * np.std(payoffs) / np.sqrt(n_paths)

    return {'price': price, 'std_error': std_error}
```

### 3. Strategy Robustness (Monte Carlo Backtesting)
See [[Monte Carlo Backtesting]].

```python
def monte_carlo_strategy_test(daily_returns, n_simulations=1000):
    """
    Shuffle returns to test if strategy performance
    is due to skill or luck.
    """
    actual_sharpe = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252)

    random_sharpes = []
    for _ in range(n_simulations):
        shuffled = np.random.permutation(daily_returns)
        sharpe = np.mean(shuffled) / np.std(shuffled) * np.sqrt(252)
        random_sharpes.append(sharpe)

    p_value = np.mean(np.array(random_sharpes) >= actual_sharpe)

    return {
        'actual_sharpe': actual_sharpe,
        'p_value': p_value,
        'percentile': (1 - p_value) * 100
    }
```

### 4. Drawdown Distribution
```python
def simulate_drawdown_distribution(mean_return, volatility,
                                    n_days=252, n_sims=10000):
    """Estimate maximum drawdown distribution."""
    max_drawdowns = []

    for _ in range(n_sims):
        returns = np.random.normal(mean_return/252, volatility/np.sqrt(252), n_days)
        cumulative = np.cumprod(1 + returns)
        peak = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - peak) / peak
        max_drawdowns.append(drawdown.min())

    return np.array(max_drawdowns)
```

## Variance Reduction Techniques

| Technique | Speedup | Idea |
|---|---|---|
| **Antithetic variates** | 2x | Use Z and -Z |
| **Control variates** | 3-10x | Reduce variance with known quantity |
| **Importance sampling** | Variable | Sample more from important regions |
| **Stratified sampling** | 2-5x | Divide into strata, sample each |

---

**Related:** [[Mathematics MOC]] | [[Value at Risk (VaR)]] | [[Options Strategies for Algos]] | [[Monte Carlo Backtesting]] | [[Stochastic Calculus]]
