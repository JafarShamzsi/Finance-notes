# Order Routing

**Order Routing** is the process by which a parent order (the "intent") is translated into specific child orders and sent to various execution venues. It is the tactical arm of the execution engine.

---

## 1. The Routing Hierarchy

1.  **Parent Order:** "Buy 10,000 AAPL."
2.  **Execution Algorithm:** Decides to use [[VWAP Algorithm]].
3.  **Order Router:** Slices the 10,000 into 100-share chunks.
4.  **Venue Selection:** The [[Smart Order Routing]] (SOR) decides which exchange gets which 100-share chunk.
5.  **Child Order:** Sends `FIX 35=D` to NASDAQ.

---

## 2. Common Routing Tactics

| Tactic | Description | Use Case |
|--------|-------------|----------|
| **Spray** | Sending multiple child orders to all lit exchanges simultaneously to capture existing liquidity before it vanishes. | Aggressive execution, sweep the book. |
| **Probe (Ping)** | Sending tiny orders (100 shares) to various venues to detect hidden liquidity or [[Iceberg Orders]]. | Discovering depth without leaking size. |
| **Sequential** | Filling on the cheapest venue first, then moving to the next. | Minimizing transaction costs. |
| **Pegging** | Dynamically adjusting the limit price of a child order to stay at the bid, ask, or midpoint. | Passive execution, earning rebates. |

---

## 3. Order Lifecycle in Routing

A router must track every child order's state using the **[[FIX Protocol]]**:
- **Pending New:** Order sent, waiting for acknowledgment.
- **New:** Order acknowledged by the exchange.
- **Partial Fill:** Part of the size is done.
- **Filled:** Order complete.
- **Cancelled/Rejected:** Something went wrong or the price moved.

---

## 4. Routing Risks

### A. Adverse Selection
If your router is too predictable, other traders will detect your pattern and "front-run" your orders on other venues.

### B. Race Conditions
In fragmented markets, two different routers might try to hit the same bid simultaneously. The faster router gets the fill; the slower one gets a "Reject" or a worse price.

### C. Over-filling
If you send "Buy 500" to three different venues expecting one to fill, but all three fill, you have bought 1,500 shares. A robust router uses a **Centralized Position Tracker** to prevent this.

---

## 5. Direct Market Access (DMA) vs. Broker Routing

- **DMA:** You control the router and send orders directly to the exchange matching engine. (Preferred by HFTs and sophisticated quants).
- **Broker Routing:** You send the parent order to a broker (e.g., J.P. Morgan, Goldman Sachs), and they use their proprietary SOR to execute it.

---

## Related Notes
- [[Execution MOC]] — Parent section
- [[Smart Order Routing]] — The logic behind venue selection
- [[Execution Venues]] — Where orders are routed
- [[FIX Protocol]] — The language of routing
- [[Connectivity]] — The physical path of the order
- [[Implementation Shortfall]] — Measuring the effectiveness of routing
