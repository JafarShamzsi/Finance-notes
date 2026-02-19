# Stop Loss Strategies

A **Stop Loss** is a predetermined exit point for a trade that is losing money. In quantitative trading, stop losses are not just about "protecting capital"; they are statistical tools used to invalidate a strategy's hypothesis.

---

## 1. Types of Stop Losses

| Type | Logic | Use Case |
|------|-------|----------|
| **Hard Stop** | A fixed price or percentage below entry (e.g., -2%). | Simple momentum/breakout strategies. |
| **Trailing Stop** | The stop level moves up as the price moves in your favor. | Trend following (locking in gains). |
| **Volatility Stop (ATR)** | Stop is placed at $N \times$ Average True Range from the current price. | Adapting to current market noise. |
| **Time Stop** | Exit if the strategy hasn't hit the target within $X$ hours/days. | Mean reversion or event-driven trades. |
| **Technical Stop** | Exit if a specific indicator changes (e.g., RSI crosses 50). | Signal-driven strategies. |

---

## 2. The ATR Stop Logic

Using the **Average True Range (ATR)** is the standard for quants because it scales the stop based on the current risk environment.

**Formula:**
$$\text{Stop Price} = \text{Entry Price} - (k \times \text{ATR})$$
- $k$ is usually between $1.5$ and $3.0$.
- **Why:** In high volatility, you need a wider stop to avoid being "shaken out" by random noise.

---

## 3. The "Stop Loss Paradox"

For mean-reversion strategies, a stop loss can actually **reduce** the total return.
- **The Logic:** Mean reversion bets that the price will come back. A stop loss forces you to exit at the *worst possible point* (the maximum deviation).
- **The Fix:** Use a "Regime-Based Exit" instead of a hard stop, or size the position so small that you can weather the deviation.

---

## 4. Execution of Stops: Slippage Risk

A stop-loss order becomes a **Market Order** once triggered.
- **The Danger:** In a "Flash Crash," your stop at $100 might be triggered, but the next available bid is $90. You lose 10% instead of 2%.
- **Mitigation:** Use "Stop-Limit" orders (with the risk of no fill) or deep-OTM put options for catastrophic protection.

---

## 5. Implementation Checklist

- [ ] **Account for Spread:** Is your stop level inside or outside the bid-ask spread?
- [ ] **Backtest Sensitivity:** Does the strategy's Sharpe Ratio improve or worsen with the stop?
- [ ] **Venue Choice:** Are the stops held locally on your server or at the exchange? (Exchange-side is safer).

---

## Related Notes
- [[Risk Management MOC]] — Broader safety context
- [[Drawdown Management]] — Limiting the portfolio-level hit
- [[Position Sizing]] — Relationship between stop width and size
- [[Order Types and Execution]] — Technical implementation of stops
- [[Volatility Trading]] — Understanding the ATR driver
