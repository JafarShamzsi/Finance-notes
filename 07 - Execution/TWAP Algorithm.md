# TWAP Algorithm (Time-Weighted Average Price)

The **TWAP Algorithm** is one of the simplest and most common execution strategies used by quants to trade large quantities of an asset. It executes an order by slicing it into smaller, equal-sized pieces and spreading them out evenly across a specified time interval.

---

## 1. How It Works: Linear Time-Slicing

For a total order of $Q$ shares to be executed over a period of $T$ minutes, the algorithm calculates the rate of execution:
$$\text{Rate} = \frac{Q}{T}$$

**Example:**
- Buy 10,000 shares of MSFT over 2 hours (120 minutes).
- **Execution:** Buy roughly 83 shares every minute, or 500 shares every 6 minutes.

---

## 2. Advanced TWAP: Randomization

Purely linear TWAP (e.g., buying 500 shares exactly every 360 seconds) is easily detectable by HFT algorithms (see [[High-Frequency Trading]]). To prevent "gaming," quants use randomization:
- **Randomized Intervals:** Instead of every 6 minutes, the algorithm might trade at 4m 12s, then 7m 45s, then 5m 30s.
- **Randomized Slice Sizes:** Instead of 500 shares, the slices could be 420, then 550, then 485.

The goal is to maintain the *average* rate of execution while hiding the systematic nature of the order.

---

## 3. When to Use TWAP

TWAP is the preferred strategy in the following scenarios:
1.  **Low Liquidity:** In assets where volume is thin and a [[VWAP Algorithm]] (which follows volume) would be too erratic.
2.  **Lack of Volume Data:** In some OTC or dark markets where reliable volume data is not available.
3.  **Benchmark Matching:** When the objective is to achieve the average price of the day (often used for accounting or fund-level benchmark matching).

---

## 4. TWAP vs. VWAP

| Feature | TWAP | VWAP |
|---------|------|------|
| **Benchmark** | Average price over time. | Average price over volume. |
| **Logic** | Trades $X$ shares per $Y$ minutes. | Trades $X$ shares per $Y$ volume. |
| **Market Condition** | Good for illiquid/steady markets. | Good for high-volume/volatile markets. |
| **Detection Risk** | Moderate (if not randomized). | Lower (hides in volume). |

---

## 5. Potential Pitfalls: Informed Trading

The biggest risk for a TWAP user is that the market moves *away* from them during the execution window.
- **Adverse Selection:** If a large seller appears halfway through your buy-TWAP, you are stuck buying at the current (and potentially falling) price until your time is up.
- **Predatory Trading:** If other participants detect your TWAP, they can "front-run" your future slices, pushing the price higher before you can buy.

---

## 6. Implementation Checklist for Quants

- [ ] **Define the Time Window:** Does the window include the open/close (where volume is highest)?
- [ ] **Randomization Seed:** Are your intervals and sizes sufficiently stochastic?
- [ ] **Passive vs. Aggressive:** Will you place limit orders (passive) or hit the bid/ask (aggressive)?
- [ ] **Completion Rate:** What happens if the price moves out of your "limit" range? (See [[Smart Order Routing]]).

---

## Related Notes
- [[Execution MOC]] — Parent section
- [[VWAP Algorithm]] — The volume-weighted alternative
- [[Market Impact Models]] — Minimizing impact with TWAP
- [[Implementation Shortfall]] — Measuring the cost of TWAP
- [[High-Frequency Trading]] — The risks of detection
