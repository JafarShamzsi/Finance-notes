# Overfitting (Curve Fitting)

**Overfitting** is the "quant's greatest sin." it occurs when a trading strategy is so perfectly tuned to the noise of historical data that it fails to generalize to the real world. An overfitted backtest looks like a "Holy Grail," but live trading results in a "flatline" or a "crash."

---

## 1. The Backtest Paradox

The more parameters you add to a strategy, the better it will look in a backtest, but the *less* likely it is to work in the future.

- **Underfitting:** Signal is too simple; misses the actual market pattern.
- **Good Fit:** Captures the underlying economic logic.
- **Overfitting:** Captures the specific "noise" of the 2018-2023 price history.

---

## 2. Common Ways Quants Overfit

### A. Parameter Optimization (Grid Search)
Testing 1,000 combinations of SMA lengths and picking the one with the highest Sharpe.
- **The Trap:** The "best" parameters are often just the ones that happened to avoid a few specific bad days in the past.

### B. Multiple Testing (Data Snooping)
Testing 100 different indicators until one "works."
- **The Trap:** If you test 100 random signals, 5 will look significant at the 95% confidence level by pure chance.

### C. Look-Ahead Bias
Accidentally using future information (e.g., using today's high to decide when to buy today). See [[Lookahead Bias]].

---

## 3. How to Detect Overfitting

1.  **Sensitivity Analysis:** Change your parameters by 5-10%. If the P&L collapses, the strategy is overfitted (it's a "fragile" peak).
2.  **In-Sample vs. Out-of-Sample:** If the Sharpe ratio in the "test" data is significantly lower than the "train" data, you have overfitted.
3.  **Monte Carlo Permutation:** Randomly shuffle the order of your returns. If your strategy still "works" on scrambled data, your signal is likely an illusion.

---

## 4. Mitigation Techniques

- **Simplification (Occam's Razor):** Favor strategies with fewer rules and parameters.
- **Cross-Validation:** Using [[Walk-Forward Analysis]] or Combinatorial Purged CV (CPCV).
- **Economic Logic:** Ask yourself: "Why *should* this signal make money?" If there is no behavioral or structural reason, it's likely noise.
- **Deflated Sharpe Ratio (DSR):** A statistical adjustment by Marcos Lopez de Prado that accounts for the number of trials performed during research.

---

## 5. Python: Sensitivity Check

```python
import numpy as np

def parameter_sensitivity_test(strategy_func, data, param_range):
    """
    Runs the strategy across a range of parameters and returns the results.
    Stable strategies should have a 'plateau' of performance.
    """
    results = []
    for p in param_range:
        sharpe = strategy_func(data, p).sharpe_ratio()
        results.append(sharpe)
    
    # Check for stability (standard deviation of results)
    stability = np.std(results)
    return results, stability
```

---

## Related Notes
- [[Backtesting MOC]] — Broader validation context
- [[Walk-Forward Analysis]] — The primary tool to prevent overfitting
- [[Lookahead Bias]] — A specific cause of false results
- [[Survivorship Bias]] — Another way to get fake results
- [[Alpha Research]] — Where the research starts
- [[Machine Learning Strategies]] — High risk of overfitting in ML
