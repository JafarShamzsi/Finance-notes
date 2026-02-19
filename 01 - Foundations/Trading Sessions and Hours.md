# Trading Sessions and Hours

The financial markets never truly sleep, but liquidity and volatility are highly concentrated in specific "windows." For a quant, understanding the global "Market Clock" is critical for execution timing and signal validation.

---

## 1. Global Equity Session Map (Eastern Time - ET)

| Market | Session Name | Hours (ET) | Characteristics |
|--------|--------------|------------|-----------------|
| **New York** | Regular Trading | 09:30 - 16:00 | Highest volume for US Equities. |
| **New York** | Pre/Post-Market | 04:00 - 20:00 | Wide spreads, reaction to earnings. |
| **London** | Regular Trading | 03:00 - 11:30 | Dominates global FX and EU Equities. |
| **Tokyo** | Regular Trading | 19:00 - 01:00 | Primary Asian liquidity hub. |
| **Sydney** | Regular Trading | 18:00 - 00:00 | First to open globally. |

---

## 2. The Intraday "U-Shape"

Empirical studies show that volume and volatility typically follow a U-shaped distribution throughout the day:
- **The Open (9:30 - 10:30 AM):** High volatility as the market incorporates overnight news. Excellent for [[Mean Reversion Strategies]].
- **The Lull (11:30 AM - 2:00 PM):** "Lunchtime in NY." Low volume, tightest spreads. Best for passive execution.
- **The Close (3:00 - 4:00 PM):** High volume surge as institutions rebalance and the "MOC" (Market on Close) orders are matched.

---

## 3. Session Overlaps: The Liquidity Peaks

The most active times in the world are when two major regions are open simultaneously:
- **London/NY Overlap (8:00 AM - 11:30 AM ET):** The highest liquidity period for global markets, especially for **EUR/USD** and **Gold**.
- **Tokyo/London Overlap (3:00 AM - 4:00 AM ET):** Active for Yen crosses.

---

## 4. Market Auctions

Most exchanges use a specific mechanism to set the day's first and last price:
- **Opening Auction:** A single batch trade that clears all accumulated orders from the overnight session.
- **Closing Auction:** The most significant event of the day. Sets the "NAV" for mutual funds.

**Quant Tip:** Strategies that trade the "Closing Auction" often focus on liquidity provision to passive index funds.

---

## 5. Holidays and Early Closings

- **Thin Markets:** Volume drops significantly before major holidays (e.g., day before Thanksgiving).
- **Erratic Behavior:** Without institutional presence, retail-driven moves can be more erratic.
- **Backtesting Tip:** Ensure your backtester uses a "Trading Calendar" (e.g., `pandas_market_calendars`) to avoid trading on weekends or holidays.

---

## Related Notes
- [[Financial Markets Overview]] — Broader market context
- [[VWAP Algorithm]] — Modeling the intraday volume
- [[Liquidity]] — Session-dependent liquidity
- [[Bid-Ask Spread]] — How spreads change throughout the day
- [[Order Types and Execution]] — MOO and MOC orders
- [[Macro Economics]] — Scheduled data release times
