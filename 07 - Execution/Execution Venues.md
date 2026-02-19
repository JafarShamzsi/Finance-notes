# Execution Venues

An **Execution Venue** is any marketplace where a financial instrument can be traded. In the modern, automated trading landscape, selecting the right venue is as important as selecting the right strategy.

---

## 1. Primary Exchange Types

### A. Lit Exchanges (The Public Market)
Venues where the order book is fully visible to all participants.
- **Examples:** NYSE, NASDAQ, Cboe, LSE.
- **Matching:** Price-Time Priority (FIFO).
- **Pros:** Maximum transparency, guaranteed best price (NBBO).
- **Cons:** Information leakage (everyone sees your order size).

### B. Dark Pools (Alternative Trading Systems - ATS)
Private venues where the order book is hidden. Trades are typically matched at the midpoint of the NBBO.
- **Examples:** Sigma X (Goldman), LX (Barclays), Crossfinder (Credit Suisse).
- **Pros:** No market impact, no information leakage.
- **Cons:** Lower fill probability, risk of "gaming" by other participants.

---

## 2. Internalizers & Market Makers

When a retail broker (like Robinhood or E*Trade) receives a buy order, they often don't send it to the NYSE. Instead, they sell it to a **Market Maker** (like Citadel Securities or Virtu).
- **Process:** The Market Maker fills the order from their own inventory, often providing a tiny "Price Improvement" over the NBBO.
- **Payment for Order Flow (PFOF):** The Market Maker pays the broker for this "uninformed" retail flow.

---

## 3. Venue Fee Models

| Model | Description | Typical User |
|-------|-------------|--------------|
| **Maker-Taker** | The exchange pays a rebate to the "Maker" (limit order) and charges a fee to the "Taker" (market order). | High-Frequency Traders, Market Makers. |
| **Inverted (Taker-Maker)** | The exchange pays the "Taker" and charges the "Maker." | Strategies that need urgent fills but want a rebate. |
| **Flat Fee** | A fixed commission per share/trade regardless of order type. | Retail investors, low-frequency institutions. |

---

## 4. Fragmentation and Venue Selection

In the US, there are 16+ lit exchanges and 30+ dark pools. A **[[Smart Order Routing]] (SOR)** algorithm must decide where to send each slice of an order.

**Selection Criteria:**
1.  **Price:** Always the #1 priority (Legal mandate).
2.  **Liquidity Depth:** How many shares are available?
3.  **Fill Probability:** Historical performance of the venue.
4.  **Toxic Flow:** Avoiding venues known for high "adverse selection."

---

## 5. Crypto Venues: CEX vs. DEX

- **Centralized Exchanges (CEX):** Binance, Coinbase. Use a traditional CLOB (Central Limit Order Book). Fast, low latency.
- **Decentralized Exchanges (DEX):** Uniswap, Curve. Use an AMM (Automated Market Maker) model. Slower, higher slippage, but 100% transparent on-chain.

---

## Related Notes
- [[Execution MOC]] — Parent section
- [[Order Book Dynamics]] — The internal logic of venues
- [[Smart Order Routing]] — Logic for navigating venues
- [[Dark Pools]] — (To be created) Deep dive
- [[Maker-Taker Fee Model]] — Economics of venue choice
- [[Market Microstructure MOC]] — Broader market context
