# Lookahead Bias (Data-Peeking)

**Lookahead Bias** is the most common and "deadly" mistake in quantitative backtesting. It occurs when a strategy uses information that would not have been available at the time of the trade.

---

## 1. What It Is

Lookahead bias makes a backtest look "too good to be true" (the "Holy Grail" curve). It is essentially **peeking into the future.**

**Example:**
- Your strategy: "Buy at the Low of the day."
- **Problem:** You only know the *actual* low of the day *after* the market closes.
- **Backtest Result:** 100% win rate.
- **Live Result:** Impossible to execute.

---

## 2. Common Causes in Backtesting

| Cause | Example |
|-------|---------|
| **Next-Bar Filling** | Using the `Close` price of the *current* bar to decide whether to buy at the `Open` of the *same* bar. |
| **Statistical Functions** | Using a 100-day moving average that includes the current day's price in a strategy that trades at the `Open`. |
| **Data Alignment** | Using corporate earnings data (e.g., Q1) that was officially released in April, but backtesting it as if it were known in March. |
| **Normalization** | Calculating the `Mean` and `StdDev` of the *entire* dataset and then using those to standardize features in the first year of the backtest. |

---

## 3. How to Detect Lookahead Bias

1.  **"Too Good" Results:** If your Sharpe ratio is $>3.0$ and your win rate is $>80\%$ on high-frequency data, suspect lookahead bias immediately.
2.  **The "Shift" Test:** In Python/Pandas, always use `.shift(1)` on your signals to ensure they apply to the *next* period's trade.
3.  **Out-of-Sample Test:** A strategy with lookahead bias will often have a spectacular backtest but will "flatline" or crash the second it is applied to live data or a new OOS period.

---

## 4. How to Prevent It (The Quant's Checklist)

- [ ] **Shift Your Signals:** `df['Signal'] = df['Indicator'].shift(1)`.
- [ ] **Point-in-Time Data:** Only use fundamental data (earnings, dividends) based on the *announcement* date, not the *fiscal* date.
- [ ] **Walk-Forward Only:** Train your indicators and ML models on data strictly *before* the test window begins (see [[Walk-Forward Analysis]]).
- [ ] **Limit Order Realism:** If you place a limit order, ensure it is only "filled" if the price *later* trades at or below your limit.
- [ ] **Audit Your Logic:** Have a "Second Pair of Eyes" (or a different framework) review the codebase for `future_price` references.

---

## 5. Technical Tip: The "Lagging" Rule

In any event-driven system (see [[Backtesting Framework Design]]):
- `Time T`: Receive MarketData.
- `Time T+1ms`: Calculate Signal.
- `Time T+2ms`: Issue Order.
- `Time T+3ms`: Get Fill at `Price T+3ms`.

*NEVER fill an order at `Price T` if the signal was generated based on `MarketData T`.*

---

## Related Notes
- [[Backtesting MOC]] — Parent section
- [[Backtesting Framework Design]] — Building an anti-bias system
- [[Walk-Forward Analysis]] — Rigorous OOS testing
- [[Overfitting]] — The other common backtesting sin
- [[Data Engineering MOC]] — Ensuring point-in-time data quality
