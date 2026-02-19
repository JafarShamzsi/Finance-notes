# Backtesting Framework Design

A robust backtesting framework is the "simulator" of the quant world. It must be as close to reality as possible to prevent "Fooling ourselves into a strategy that doesn't exist."

---

## 1. Vectorized vs. Event-Driven Architectures

| Feature | Vectorized (Pandas/NumPy) | Event-Driven (Tick-by-Tick) |
|---------|---------------------------|----------------------------|
| **Speed** | Extremely fast (C-level vector ops). | Slower (Loop-based). |
| **Logic** | Matrix-based. Good for simple signals. | Complex (Order Book, Latency). |
| **Realism** | Low. Assumes instant fills. | High. Simulates exchange matching. |
| **Use Case** | Quick research and screening. | Production-grade validation. |

---

## 2. The Event-Driven Loop (Production Style)

An event-driven backtester mimics a real trading system. It uses an **Event Queue** to process messages in order.

1.  **MarketEvent:** A new tick or OHLCV bar is received.
2.  **SignalEvent:** The strategy calculates its logic and issues a "Buy" or "Sell" intent.
3.  **OrderEvent:** The Portfolio handler checks risk limits and generates a specific order.
4.  **FillEvent:** The Execution handler simulates the exchange, calculating commissions and slippage.

```python
# Simplified Logic
while event_queue:
    event = event_queue.get()
    if event.type == 'MARKET':
        strategy.on_bar(event)
    elif event.type == 'SIGNAL':
        portfolio.on_signal(event)
    elif event.type == 'ORDER':
        execution.execute_order(event)
    elif event.type == 'FILL':
        portfolio.on_fill(event)
```

---

## 3. Simulating Execution (The "Secret Sauce")

The most common source of backtesting bias is "Idealized Execution."
- **Slippage Models:** Don't just fill at the next `Open`. Use [[Market Impact Models]] to estimate how your 10,000-share buy would move the price.
- **Latency Simulation:** Add a 10-100ms delay between `SignalEvent` and `FillEvent` to account for network jitter and processing.
- **Order Book Matching:** For HFT, you must simulate the L2/L3 queue (see [[Order Book Dynamics]]).

---

## 4. Bias Prevention: The "Quant's Enemies"

A good framework makes it impossible (or very difficult) to commit these sins:
1.  **Lookahead Bias:** Ensure the strategy only sees data *before* the current timestamp (use `.shift(1)` in Pandas).
2.  **Survivorship Bias:** Use a point-in-time universe. (Don't backtest on "stocks currently in the S&P 500").
3.  **Data Snooping:** Over-tuning parameters to fit noise (see [[Overfitting]]).

---

## 5. Performance Measurement & Reporting

Beyond just the "Equity Curve," a professional framework should output:
- **Risk Metrics:** Sharpe, Sortino, Calmar, Information Ratio.
- **Drawdown Analysis:** Max Drawdown, Recovery Time, Under-water plot.
- **Trade Analysis:** Win rate, Profit factor, Average win vs. Average loss.
- **TCA Report:** Realized slippage vs. Expected slippage (see [[Implementation Shortfall]]).

---

## 6. Popular Frameworks (Build vs. Buy)

- **VectorBT:** Fast vectorized backtesting for Python.
- **Lean (QuantConnect):** Open-source, multi-asset, C#/Python engine.
- **Zipline/PyFolio:** The legacy standard (from Quantopian).
- **Custom C++:** Essential for HFT and high-frequency market making.

---

## Related Notes
- [[Backtesting MOC]] — Parent section
- [[Walk-Forward Analysis]] — Proper validation
- [[Performance Metrics]] — How to read the results
- [[Market Impact Models]] — Essential for realistic fills
- [[Data Engineering MOC]] — Source of backtesting data
- [[Implementation Shortfall]] — Measuring execution quality
