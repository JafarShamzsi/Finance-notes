# MiFID II (Markets in Financial Instruments Directive II)

EU regulation effective January 2018. The European equivalent of Reg NMS but much broader in scope. Affects any firm trading EU instruments.

---

## Key Provisions for Algo Trading

### Algorithmic Trading Definition (Article 4(1)(39))
Any trading where a computer algorithm automatically determines:
- Whether to initiate an order
- Timing, price, or quantity of an order
- How to manage the order after submission

With **limited or no human intervention**.

### High-Frequency Trading Definition
Algorithmic trading characterized by:
1. Infrastructure to minimize latency (co-location, proximity hosting)
2. System determination of order without human intervention
3. High intraday message rates (orders, quotes, cancellations)

---

## Requirements for Algo Traders

### RTS 6 — Organizational Requirements

| Requirement | Detail |
|-------------|--------|
| **Testing** | Algos must be tested in non-production environment before deployment |
| **Risk controls** | Pre-trade limits on price, size, value, strategy-level |
| **Kill switch** | Immediate ability to cancel all orders from an algo |
| **Monitoring** | Real-time monitoring of all algo activity |
| **Annual review** | Self-assessment of algo compliance |
| **Records** | Keep records of all algo orders for 5 years |
| **Change management** | Document and test all algo changes |

### Market Making Obligations
If an algo provides liquidity continuously, the firm may be treated as a **market maker** and must:
- Maintain quotes for a minimum percentage of trading hours
- Have a binding market-making agreement with the venue
- Meet minimum quote sizes

### Order-to-Trade Ratio
Exchanges must impose maximum order-to-trade ratios to limit excessive messaging:
- Penalize algorithms that cancel disproportionately many orders
- Designed to curb spoofing and reduce system load

---

## Transaction Reporting (RTS 25)

All trades must be reported with:
- Timestamp accuracy to **1 microsecond** (HFT) or 1 millisecond (others)
- Client identifier
- Instrument identifier (ISIN)
- Price, quantity, venue
- Algorithm identifier (if algo-generated)

**Impact:** Every algo order is tagged with an algo ID — regulators can trace any strategy.

---

## Research Unbundling
MiFID II requires **separation of research costs from execution costs**:
- Buy-side firms must pay for research separately (not bundled with trading commissions)
- Reduced research budgets across the industry
- **Impact on quants:** Alternative data and internal quantitative research became more valuable

---

## Dark Pool Restrictions

### Double Volume Cap (DVC)
- No more than 4% of total EU trading in a single stock on any single dark pool
- No more than 8% of total EU trading in a single stock across all dark pools
- If breached, stock is banned from dark trading for 6 months

### Systematic Internalisers (SIs)
- Firms that regularly deal on own account must register as SIs
- Must provide quotes to clients
- Price improvement rules apply

---

## Comparison: MiFID II vs. US Regulation

| Aspect | MiFID II (EU) | US (SEC/FINRA) |
|--------|---------------|----------------|
| Algo registration | Required | Not separate registration |
| Testing requirement | Mandatory | Expected but not codified |
| Kill switch | Explicit requirement | Required (Rule 15c3-5) |
| Order-to-trade limits | Venue-enforced | No specific limit |
| Timestamp precision | 1 μs (HFT) | 1 ms (CAT) |
| Dark pool caps | Yes (DVC) | No caps |
| Research unbundling | Required | Not required |
| Algo tagging | Required | CAT linkage |

---

## Related Notes
- [[Regulation and Compliance MOC]] — Parent note
- [[Reg NMS]] — US equivalent
- [[SEC and FINRA Rules]] — US rules
- [[Market Manipulation]] — MAR (Market Abuse Regulation)
- [[Execution Venues]] — Venue regulation differences
