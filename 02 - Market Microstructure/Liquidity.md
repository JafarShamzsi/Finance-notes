# Liquidity

**Liquidity** is the ability to buy or sell an asset quickly, in large quantities, at a price near the fair value, without causing significant market impact. It is the lifeblood of the financial markets and the primary constraint on any quantitative strategy.

---

## 1. The Four Dimensions of Liquidity

| Dimension | Description | Measure |
|-----------|-------------|---------|
| **Tightness** | The cost of a round-trip trade. | [[Bid-Ask Spread]]. |
| **Depth** | The volume available at various price levels. | Order Book Total Size. |
| **Resilience** | The speed at which prices return to equilibrium after a trade. | Reversion Time. |
| **Immediacy** | How quickly an order can be filled. | Execution Latency. |

---

## 2. Liquidity Metrics for Quants

### A. Amihud Illiquidity Ratio
Measures the price move per dollar of volume. A higher value = less liquid.
$$\text{Amihud} = \text{mean} \left( \frac{|Return_t|}{\text{Dollar\_Volume}_t} \right)$$

### B. Turnover Ratio
How much of the total supply trades in a period.
$$\text{Turnover} = \frac{\text{Volume}}{\text{Shares Outstanding}}$$

### C. VPIN (Volume-Synchronized Probability of Informed Trading)
Measures the "toxicity" of the liquidity (see [[Order Flow Analysis]]).

---

## 3. The Liquidity Spiral (Crisis)

Liquidity is non-linear. In normal markets, it is abundant. In a crisis, it evaporates instantly:
1.  **Price Drop:** Triggered by a news event.
2.  **Margin Calls:** Forced selling by leveraged participants.
3.  **Spread Widening:** Market makers withdraw to protect themselves.
4.  **No Buyers:** The "Air Pocket" where the price falls until it hits a deep institutional bid.

---

## 4. Liquidity and Strategy Capacity

Every strategy has a "Capacity" — the maximum AUM it can manage before its own market impact eats all the alpha.
- **High Frequency (HFT):** Low capacity, high turnover.
- **Trend Following:** High capacity, low turnover.

**The Scalability Tradeoff:** As you manage more money, you are forced to trade slower or move to more liquid instruments (like SPY or Treasuries).

---

## 5. Liquidity in Different Asset Classes

- **Equities:** High liquidity in Large-Caps, fragmented across many exchanges.
- **Forex:** Extremely high liquidity in major pairs (EUR/USD), 24/5.
- **Fixed Income:** Less liquid, mostly OTC (except Treasuries).
- **Crypto:** High liquidity but highly concentrated in a few venues (Binance, Coinbase).

---

## Related Notes
- [[Market Microstructure MOC]] — Broader plumbing context
- [[Bid-Ask Spread]] — The cost of liquidity
- [[Order Book Dynamics]] — The source of liquidity
- [[Market Impact]] — The result of insufficient liquidity
- [[Transaction Cost Analysis (TCA)]] — Measuring realized liquidity cost
- [[High-Frequency Trading]] — Providing liquidity for rebates
