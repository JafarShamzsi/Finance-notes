# Event-Driven Strategies

Event-driven strategies profit from the price movements and dislocations caused by specific corporate or market events. These strategies often have a low correlation with broad market indices, making them attractive for diversification.

---

## 1. Merger Arbitrage (Risk Arbitrage)

Profiting from the price gap between an announced acquisition price and the target company's current stock price.

### How it works
- **Cash Merger:** Buy the target company. If the deal closes at $P_{deal}$, you profit $P_{deal} - P_{current}$.
- **Stock-for-Stock Merger:** Buy the target and short the acquirer in the specified exchange ratio.
- **The "Deal Spread":** The difference between the target's price and the offer price reflects the market's perceived risk that the deal won't close (regulatory hurdles, financing failure, etc.).

### Risks
- **Deal Break:** The target's price usually crashes to pre-announcement levels if the deal fails.
- **Timeline Extension:** Longer closing times reduce the annualized return (IRR).

---

## 2. Index Rebalancing Arbitrage

Trading the buying and selling pressure that occurs when stocks are added to or removed from major indices (S&P 500, MSCI, Russell).

### The "Index Effect"
1. **Announcement:** Index provider announces a change (e.g., Tesla added to S&P 500).
2. **Pre-Trade:** Traders buy the addition and short the deletion.
3. **Execution:** Passive funds must buy the addition at the close on the effective date.
4. **Post-Trade:** The "overhang" often mean-reverts after the passive flows subside.

### Strategy Implementation
- **Anticipation:** Using fundamental and market-cap rules to predict which stocks will be added.
- **Flow Trading:** Providing liquidity to the index funds on the effective day.

---

## 3. Earnings & Corporate Actions

### Earnings-Based Strategies
- **Post-Earnings Announcement Drift (PEAD):** The phenomenon where stocks continue to move in the direction of an earnings surprise for weeks.
- **Earnings Volatility Trading:** Long/short straddles to profit from the realized vs. implied volatility jump on earnings day.

### Share Buybacks
- Companies announcing buybacks often signal that management believes the stock is undervalued.
- Historically, companies announcing large buybacks tend to outperform.

---

## 4. Distressed Debt & Spin-offs

### Spin-offs
- A parent company spins off a subsidiary into a new public entity.
- Parent company shareholders often sell the new shares immediately (forced selling), creating a temporary undervaluation.

### Restructuring & Bankruptcy
- Investing in the debt or equity of companies undergoing reorganization.
- Requires deep legal and fundamental analysis (less systematic, more "quantamental").

---

## Quantitative Implementation

### Event Detection
- Scrape SEC filings (8-K, 13-D), news headlines, and press releases.
- Use [[Natural Language Processing (NLP)]] to identify the event type and sentiment.

### Position Sizing
- Use the **Kelly Criterion** based on the probability of the event succeeding ($p$) and the payoff ratio ($b$).
- See [[Kelly Criterion]] for the formula.

```python
def merger_arb_returns(offer_price, current_price, success_prob, fail_price, days_to_close):
    """
    Estimate expected return and annualized IRR for a merger arb deal.
    """
    expected_profit = success_prob * (offer_price - current_price) + \
                      (1 - success_prob) * (fail_price - current_price)

    return_pct = expected_profit / current_price
    irr = (1 + return_pct) ** (365 / days_to_close) - 1

    return {
        'expected_profit': expected_profit,
        'return_pct': return_pct,
        'annualized_irr': irr
    }
```

---

## Related Notes
- [[Strategies MOC]] — Master navigation
- [[Natural Language Processing (NLP)]] — For event detection
- [[Kelly Criterion]] — For sizing event-driven bets
- [[Sentiment-Based Strategies]] — Connection to event sentiment
- [[Alpha Research]] — Testing event-based alphas
- [[Risk Management MOC]] — Managing event-specific risks
