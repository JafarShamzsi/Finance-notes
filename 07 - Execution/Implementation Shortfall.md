# Implementation Shortfall (IS)

**Implementation Shortfall** is the "gold standard" of transaction cost measurement. It calculates the difference between the return on a *hypothetical* paper portfolio (where all trades are executed instantly and perfectly at the decision price) and the *actual* portfolio.

Originally proposed by André Perold (1988), it captures all the hidden costs that simpler benchmarks like [[VWAP Algorithm]] miss.

---

## 1. The Components of IS

Implementation Shortfall is mathematically decomposed into four pieces:

$$IS = \text{Execution Cost} + \text{Opportunity Cost} + \text{Delay Cost} + \text{Explicit Fees}$$

### A. Execution Cost (Market Impact)
The difference between the actual execution prices and the prices at the start of trading.
$$\text{Execution Cost} = \sum q_i (P_i - P_{arrival})$$
- *Captures: Market impact and bid-ask spread.*

### B. Opportunity Cost
The cost of *not* being able to fill the entire order.
$$\text{Opportunity Cost} = (Q_{total} - Q_{filled}) \cdot (P_{final} - P_{decision})$$
- *Captures: The money you would have made if you had filled everything.*

### C. Delay Cost (Slippage)
The price movement between the time the portfolio manager (PM) makes the decision and the time the order is actually sent to the market.
$$\text{Delay Cost} = Q_{filled} \cdot (P_{arrival} - P_{decision})$$
- *Captures: Latency between the PM's "Buy" button and the trader's execution engine.*

### D. Explicit Fees
Commissions, taxes, and exchange fees.
- *Captures: The "hard" costs of trading.*

---

## 2. Why IS is Superior to VWAP

- **VWAP Gaming:** A trader can easily beat a VWAP benchmark by trading slowly throughout the day, even if the price has moved significantly away from the PM's target.
- **IS Insight:** IS penalizes the trader for price drift and for not getting filled. It aligns the interests of the PM and the Execution Desk.

---

## 3. Implementation Shortfall Strategy (Algo)

When a trader chooses an "IS Algorithm" from a broker, they are essentially choosing a strategy that balances:
1.  **Market Impact (trading too fast):** Higher impact costs.
2.  **Market Risk (trading too slow):** Higher chance of adverse price drift (opportunity/delay cost).

The algorithm uses a **Risk Aversion ($\lambda$)** parameter (see [[Market Impact Models|Almgren-Chriss]]) to decide how aggressively to trade.

---

## 4. Measuring IS Performance

To evaluate a desk's performance, quants look at:
- **Arrival Price Benchmark:** Did we buy at a price close to when the order was created?
- **PWP (Participation Weighted Price):** A variation of IS that adjusts for the stock's volume during the trade.

---

## 5. Implementation Checklist for Quants

- [ ] **Capture Decision Time:** Ensure your OMS logs the exact millisecond the PM generated the order.
- [ ] **Record Arrival Prices:** Log the mid-price at the moment the execution engine received the order.
- [ ] **Track Fill Ratios:** Measure what percentage of orders are left unfilled (opportunity cost).
- [ ] **Analyze by Ticker:** Do certain assets (illiquid, volatile) have consistently higher IS?

---

## Related Notes
- [[Execution MOC]] — Parent section
- [[Transaction Cost Analysis (TCA)]] — The broader process
- [[Market Impact Models]] — How to model the "Execution Cost" piece
- [[VWAP Algorithm]] — A simpler (but flawed) benchmark
- [[High-Frequency Trading]] — Minimizing IS with speed
