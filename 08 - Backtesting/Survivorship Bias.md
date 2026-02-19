# Survivorship Bias

**Survivorship Bias** is a common backtesting error where a strategy is tested only on assets that "survived" until the end of the data period, ignoring those that were delisted, went bankrupt, or were acquired.

---

## 1. What It Is

It occurs when a quant uses the *current* constituents of an index (e.g., S&P 500) to backtest a strategy that spans the last 10 years.

**The Problem:**
- The current S&P 500 contains the *winners*.
- Companies that went bust in 2012 are *not* in your 2024 index list.
- **Backtest Result:** Artificially high returns (because you've implicitly picked the "survivors").

---

## 2. Real-World Example

If you backtest a "Buy and Hold" strategy on the top 10 tech companies from 1999 that are still in business today, your returns will be spectacular. But if you had *actually* bought the top 10 tech companies in 1999, you would have owned Pets.com, WorldCom, and Global Crossing—all of which went to zero.

---

## 3. How to Prevent Survivorship Bias

### A. Use Point-in-Time (PIT) Universes
- A PIT universe is a list of assets that were in the index *at each specific date in the past*.
- For a trade in Jan 2015, you must use the constituent list from Jan 2015, not from today.

### B. Include Delisted Stocks
- Ensure your database includes stocks that are no longer traded.
- When a stock is delisted, the backtester must handle the "final" price (which could be zero or a low OTC price).

### C. Watch for Name Changes & Re-tickers
- Companies change their ticker symbols (e.g., FB to META). Your database must track these changes so your backtest doesn't "break."

---

## 4. Where to Find Survivorship-Bias-Free Data

- **CRSP (University of Chicago):** The gold standard for historical US equity data (includes delisted stocks).
- **Norgate Data:** Popular among retail and semi-pro quants for its clean, bias-free history.
- **Sharadar (via Nasdaq Data Link):** Affordable PIT data for US stocks.
- **Broker APIs (IBKR, Bloomberg):** Usually provide bias-free data if you query it for specific historical dates.

---

## 5. Technical Checklist for Quants

- [ ] **Data Audit:** Does my dataset include companies that are no longer active?
- [ ] **Universe Logic:** Is my strategy selecting stocks based on the *current* index or a *historical* list?
- [ ] **Handling Delistings:** Does the backtester correctly exit a position when a stock is removed from the exchange? (See [[Backtesting Framework Design]]).

---

## Related Notes
- [[Backtesting MOC]] — Parent section
- [[Backtesting Framework Design]] — Building an anti-bias system
- [[Lookahead Bias]] — The other major backtesting trap
- [[Overfitting]] — Why bias leads to over-optimization
- [[Data Engineering MOC]] — Sourcing and storing PIT data
- [[Asset Classes]] — Context for equities and delisting
- [[Indices and Benchmarks]] — (To be created) Index methodology
