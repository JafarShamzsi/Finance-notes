# Pattern Day Trader (PDT) Rule

The **Pattern Day Trader (PDT) Rule** is a FINRA mandate that applies to US retail margin accounts. For quants building automated strategies, the PDT rule is a critical operational constraint that affects strategy frequency and leverage.

---

## 1. What is a "Day Trade"?

A **Day Trade** is defined as the opening and closing of the same security (stock or option) on the same trading day.
- **Example:** Buy 100 AAPL at 10:00 AM and Sell 100 AAPL at 3:00 PM.

---

## 2. The PDT Definition

A trader is classified as a **Pattern Day Trader** if:
1.  They execute **4 or more day trades within 5 business days**.
2.  Those trades represent more than 6% of their total trading activity for that period.

---

## 3. The Requirement: $25,000 Minimum

Once classified as a PDT, the account must maintain a minimum equity of **$25,000** at all times.
- **The Penalty:** If the account drops below $25k, the trader is restricted from day trading until the balance is restored.
- **Day Trading Buying Power:** PDT accounts are granted **4:1 intraday leverage** (vs. the standard 2:1 overnight leverage).

---

## 4. Impact on Quantitative Strategies

The PDT rule creates a "Liquidity Wall" for small retail algorithms:

| Strategy Type | PDT Impact |
|---------------|------------|
| **High-Frequency (HFT)** | Impossible without $25k+. |
| **Intraday Mean Reversion** | Must limit trades to < 3 per week if < $25k. |
| **Swing Trading** | Generally unaffected (holding periods > 1 day). |
| **Crypto Trading** | **Not Applicable.** Crypto is currently exempt from PDT. |
| **Futures Trading** | **Not Applicable.** Futures have different margin rules. |

---

## 5. Strategies to Manage PDT Constraints

1.  **Hold Overnight:** Design signals that fire at the close and exit at the next day's open. (Increases "Gap Risk").
2.  **Trade Futures/FX/Crypto:** If capital is < $25k, these markets allow high-frequency testing without the PDT restriction.
3.  **Use Cash Account:** PDT only applies to *margin* accounts. However, cash accounts are limited by "T+1 Settlement" (you can't trade with unsettled funds).
4.  **Trade from Overseas:** Non-US brokers (sometimes) have different rules for non-US citizens, though most follow FINRA standards for US listed stocks.

---

## Related Notes
- [[Regulation and Compliance MOC]] — Broader legal context
- [[SEC and FINRA Rules]] — Other regulatory bodies
- [[Asset Classes]] — Where PDT applies (Equities/Options)
- [[Margin and Leverage]] — (To be created) The mechanics of buying power
- [[Trading Sessions and Hours]] — Context for same-day trades
