# Walk-Forward Analysis (WFA)

**Walk-Forward Analysis** is a more rigorous and realistic alternative to a simple "In-Sample / Out-of-Sample" split. It simulates the real-world process of a quant: **Optimizing, Trading, and Re-optimizing** periodically as new data arrives.

---

## 1. The WFA Mechanism

| Step | Action |
|------|--------|
| **Window Selection** | Choose an **In-Sample (IS)** window (e.g., 2 years) and an **Out-of-Sample (OOS)** window (e.g., 6 months). |
| **Optimization** | Find the "optimal" parameters (e.g., SMA lengths) on the IS window. |
| **Testing** | Apply those *exact* parameters to the subsequent OOS window. Record the results. |
| **The Walk** | Move both windows forward by the length of the OOS window. Repeat until the end of the history. |
| **Aggregation** | Stitched together, the OOS segments form the "Walk-Forward Equity Curve." |

---

## 2. Anchored vs. Rolling Windows

- **Rolling (Standard):** The IS window has a fixed size (e.g., always the *last* 2 years). This is better for markets that undergo frequent regime shifts.
- **Anchored:** The IS window always starts at the same date (e.g., 2010 to current). This is better for strategies that require large amounts of historical data for stability.

---

## 3. Walk-Forward Efficiency (WFE)

The **WFE** is a key metric to determine if your strategy is "robust" or just "overfitted to the noise."

$$WFE = \frac{\text{Annualized Return (OOS)}}{\text{Annualized Return (IS)}} \times 100$$

- **WFE > 50%:** Generally considered a robust strategy.
- **WFE < 50%:** The strategy is likely overfitted. The "optimal" parameters in the past are failing in the future.
- **WFE > 100%:** A rare and excellent sign, meaning the strategy performed better in the unknown future than the known past.

---

## 4. Why WFA is Critical for Quants

1.  **Captures Strategy Decay:** It shows how long a parameter set remains profitable before needing an update.
2.  **Determines Re-optimization Frequency:** It helps you decide if you should re-run your optimizer weekly, monthly, or yearly.
3.  **Realistic Expectations:** WFA results are the closest thing to live trading performance. If your WFA fails, your live strategy will almost certainly fail.

---

## 5. Potential Pitfalls

- **Data Snooping:** If you run WFA multiple times with different window sizes and pick the one that looks best, you have just "overfitted the backtester."
- **Computational Cost:** Running hundreds of optimizations can be slow. Use parallel processing or vectorized backtesters like VectorBT.
- **Regime Bias:** A single, large OOS failure might be due to a unique event (e.g., COVID crash) rather than a bad strategy.

---

## Related Notes
- [[Backtesting Framework Design]] — Implementation of WFA
- [[Overfitting]] — The problem WFA solves
- [[Performance Metrics]] — How to evaluate WFA
- [[Regime Detection]] — When to re-optimize based on market state
- [[Alpha Research]] — The starting point for WFA
- [[Machine Learning Strategies]] — Using WFA for hyperparameter tuning
