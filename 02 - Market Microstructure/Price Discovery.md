# Price Discovery

**Price Discovery** is the mechanism through which new information (earnings, economic data, news) is incorporated into the market price of an asset. It is the process of finding the "equilibrium price" where supply equals demand.

Understanding price discovery is essential for quants to identify which venues and times provide the most "accurate" signals.

---

## 1. The Price Discovery Cycle

1.  **Event/Information:** A company releases an earnings surprise.
2.  **Informed Trading:** Sophisticated traders (Hedge Funds, Algos) act on the news.
3.  **Order Imbalance:** A sudden surge in buy orders hits the ask.
4.  **Quote Update:** Market makers observe the imbalance and raise their bid/ask quotes to protect themselves from adverse selection.
5.  **New Equilibrium:** The price stabilizes at a new level that reflects the information.

---

## 2. Lead-Lag Relationships

In fragmented markets, price discovery often happens in one venue before others.

| Leading Venue | Lagging Venue | Reason |
|---------------|---------------|--------|
| **Futures** | **Spot (Cash)** | Higher leverage and easier shorting make futures the preferred venue for informed macro traders. |
| **Primary Exchange** | **Dark Pools** | Discovery happens in the "lit" market where the order book is visible. |
| **Options (IV)** | **Stock Price** | Implied volatility often spikes *before* a major price move as traders buy protection. |
| **CEX (Binance)** | **DEX (Uniswap)** | High-frequency arbitrageurs move prices on centralized exchanges first. |

---

## 3. Measuring Price Discovery: Hasbrouck Information Share (IS)

Joel Hasbrouck (1995) developed a statistical method to determine which venue contributes most to the variance of the "permanent" price component.

- **Component Share:** Measures the contribution of each venue to the price level.
- **Information Share:** Measures the contribution to the discovery of *new* information.

**Quant Tip:** Use a Vector Error Correction Model (VECM) to estimate these shares from multi-venue tick data.

---

## 4. Role of High-Frequency Trading (HFT)

HFTs are the primary "couriers" of price discovery.
- They monitor the NBBO across all exchanges.
- If the price moves on NASDAQ, HFTs instantly update their quotes on NYSE.
- This keeps the market efficient but can lead to "Flash Crashes" if HFTs withdraw their liquidity simultaneously.

---

## 5. Factors that Hinder Price Discovery

- **Dark Pools:** By hiding orders, dark pools delay the time it takes for the market to see the true supply/demand.
- **Market Halts/Circuit Breakers:** Pause the process during extreme volatility to prevent panic.
- **Internalization:** When a broker fills a retail order from their own inventory, that trade never hits the public exchange, "hiding" the information.

---

## Related Notes
- [[Market Microstructure MOC]] — Broader context
- [[Order Book Dynamics]] — The mechanical engine of discovery
- [[Bid-Ask Spread]] — Cost of being on the wrong side of discovery
- [[High-Frequency Trading]] — The speed of discovery
- [[Execution Venues]] — Where discovery happens
- [[Order Flow Analysis]] — Tracking informed traders
