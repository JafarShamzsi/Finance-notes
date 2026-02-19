# Monte Carlo Backtesting

Standard backtesting tells us how a strategy performed on the single path that history took. **Monte Carlo Backtesting** allows a quant to simulate thousands of alternative market paths to understand the strategy's sensitivity to randomness and potential for catastrophic failure.

---

## 1. Why Monte Carlo?

- **The "Flaw of Averages":** A strategy with a positive average return might have a 20% chance of hitting a total wipeout (Ruin) during a specific sequence of bad trades.
- **Path Dependency:** Many strategies (especially those with stop-losses or leverage) are highly sensitive to the *order* of returns, not just the total return.
- **Confidence Intervals:** It provides a range of likely outcomes (e.g., "There is a 95% probability that the Max Drawdown will be between 10% and 18%").

---

## 2. Simulation Techniques

### A. Bootstrapping (Resampling)
Randomly sampling returns from the historical backtest with replacement to create new equity curves.
- **Pros:** Preserves the empirical distribution of returns.
- **Cons:** Breaks serial correlation (autocorrelation) and volatility clustering.

### B. Block Bootstrapping
Resampling "blocks" of consecutive returns (e.g., 5-day blocks) to preserve short-term serial correlation.

### C. Synthetic Path Generation (GBM/GARCH)
Using a mathematical model (like [[Stochastic Calculus|Geometric Brownian Motion]] or [[GARCH Models]]) to generate entirely new price paths that have the same statistical properties as the real market.

---

## 3. Key Monte Carlo Metrics

| Metric | Description |
|--------|-------------|
| **Probability of Ruin** | The % of simulated paths that hit a specific drawdown threshold (e.g., -50%). |
| **Median Sharpe** | The 50th percentile Sharpe ratio across all simulations. |
| **Max Drawdown Distribution** | A histogram showing the range of worst-case scenarios. |
| **Terminal Wealth Distribution** | The range of final portfolio values. |

---

## 4. Sensitivity Testing

Monte Carlo can be combined with parameter variation:
1.  **Slippage Monte Carlo:** Randomly varying execution costs to see at what point the alpha disappears.
2.  **Trade Omission:** Randomly removing the 10 "best" trades from the backtest. If the strategy becomes unprofitable, the edge is too fragile.

---

## 5. Python Implementation: Equity Curve Resampling

```python
import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_equity_curves(strategy_returns, n_sims=1000, horizon=252):
    """
    Resamples historical returns to generate alternative equity curves.
    """
    sim_results = []
    
    for _ in range(n_sims):
        # Sample with replacement
        resampled_rets = np.random.choice(strategy_returns, size=horizon, replace=True)
        equity_curve = np.cumprod(1 + resampled_rets)
        sim_results.append(equity_curve)
        
    # Visualization
    for curve in sim_results[:50]: # Plot first 50
        plt.plot(curve, color='gray', alpha=0.1)
    
    plt.plot(np.median(sim_results, axis=0), color='red', label='Median Path')
    plt.title(f"Monte Carlo: {n_sims} Alternative Realities")
    plt.show()
    
    return sim_results
```

---

## Related Notes
- [[Backtesting MOC]] — General testing framework.
- [[Monte Carlo Simulation]] — General mathematical foundation.
- [[Performance Metrics]] — What we are measuring in the sims.
- [[Risk Management MOC]] — Using MC for drawdown limits.
- [[Stochastic Calculus]] — Models for path generation.
