# Model Validation in Finance

Model validation is the process of ensuring that a quantitative model is performing as intended and is robust enough for live trading. In finance, this is exceptionally difficult due to the low Signal-to-Noise Ratio (SNR), non-stationarity, and the risk of **Overfitting**.

At J.P. Morgan, model validation is a regulatory requirement (SR 11-7) and a core risk management function.

---

## 1. Statistical Significance of Alpha

A common mistake is assuming a high Sharpe ratio in a backtest is sufficient. We must test the null hypothesis ($H_0$): "The strategy returns are due to chance."

### A. The t-Statistic
For a strategy with mean return $\mu$ and standard deviation $\sigma$ over $N$ periods:
$$ t = \frac{\mu}{\sigma} \sqrt{N} = 	ext{Sharpe} 	imes \sqrt{N} $$
Typically, we require $|t| > 2.0$ (95% confidence) or $|t| > 3.0$ for high-frequency strategies to account for multiple testing.

### B. Probabilistic Sharpe Ratio (PSR)
Adjusts the Sharpe ratio for the non-normality (skewness and kurtosis) of returns.
- **Why:** Financial returns have fat tails. A "lucky" strategy might have a high Sharpe but also high negative skew (tail risk).

---

## 2. Cross-Validation for Time Series

Standard K-Fold cross-validation fails in finance because observations are not IID (Independent and Identically Distributed).

### A. Purged K-Fold CV
Observations near the boundary of the training and test sets often contain overlapping information (e.g., due to serial correlation in features or targets). 
- **Purging:** Removing training samples that are chronologically close to the test set.
- **Embargo:** Adding a "gap" after the test set to ensure no information leaks into the next training fold.

### B. Combinatorial Purged Cross-Validation (CPCV)
Allows for testing models on many different "paths" of history while maintaining purging and embargoing. This provides a distribution of Sharpe ratios rather than a single point estimate.

---

## 3. Dealing with Multiple Testing (Selection Bias)

The more signals you test, the more likely you are to find one that works by pure chance.

### A. Deflated Sharpe Ratio (DSR)
Developed by Marcos Lopez de Prado, the DSR "deflates" the observed Sharpe ratio based on:
1.  The number of independent trials performed.
2.  The variance of Sharpe ratios across those trials.
3.  The length of the backtest.

### B. False Discovery Rate (FDR)
Using the Benjamini-Hochberg procedure to adjust p-values when testing multiple hypotheses.

---

## 4. Sensitivity & Stability Analysis

A robust model should not be "fragile."

- **Parameter Sensitivity:** If your strategy only works with an RSI period of 14, but crashes at 13 or 15, it is overfitted to noise.
- **Perturbation Testing:** Adding small amounts of Gaussian noise to the input features. A robust model's performance should degrade gracefully, not collapse.
- **Regime Robustness:** Testing the model separately in Bull, Bear, and Sideways markets (see [[Regime Detection]]).

---

## 5. Shadow Trading & Paper Trading

Before committing capital, a model must pass through a "Shadow Mode":
1.  **Code Consistency:** Verifying that the production implementation produces the exact same signals as the backtest engine.
2.  **Latency Audit:** Ensuring that the time taken to compute the signal does not exceed the alpha's decay profile.
3.  **Slippage Validation:** Comparing real-time execution costs to the assumptions used in the backtest.

---

## Related Notes
- [[Backtesting MOC]] — General validation framework.
- [[Overfitting]] — The primary enemy.
- [[Walk-Forward Analysis]] — A robust validation technique.
- [[Alpha Research]] — The origin of the models.
- [[Probability and Statistics for Trading]] — Mathematical tools.
