# Reg NMS (Regulation National Market System)

Adopted by the SEC in 2005, Reg NMS fundamentally shaped modern US equity market structure. It's why we have fragmented markets, smart order routing, and high-frequency trading.

---

## The Four Pillars

### 1. Order Protection Rule (Rule 611)
- **Trade-through prohibition** — Cannot execute a trade at a price worse than the best displayed price on any exchange
- Creates the **NBBO** (National Best Bid and Offer) — the best bid across all exchanges and the best offer across all exchanges
- **Exception:** Intermarket sweep orders (ISOs) — can trade through if you simultaneously send orders to protect the better-priced quotes

**Impact on algos:** Must respect NBBO. Smart order routers exist because of this rule.

### 2. Access Rule (Rule 610)
- Limits access fees to **$0.003 per share** (30 mils) for displayed quotes
- Ensures all market participants can access displayed quotes
- Created the **maker-taker model**: exchanges pay rebates (~$0.002) for liquidity provision, charge fees (~$0.003) for taking

**Impact on algos:** Fee optimization is a real alpha source. Some strategies exist purely to capture rebates.

### 3. Sub-Penny Rule (Rule 612)
- Prohibits quoting in increments less than $0.01 for stocks priced above $1.00
- Stocks below $1.00 can quote in $0.0001 increments
- **Exception:** Midpoint orders in dark pools can use sub-penny prices (e.g., $50.005)

**Impact on algos:** Tick size constrains pricing granularity. Tick size pilot programs tested wider ticks.

### 4. Market Data Rules (Rules 601, 603)
- Consolidation of market data from all exchanges into SIP (Securities Information Processor)
- Two feeds: CTA (NYSE-listed) and UTP (NASDAQ-listed)
- Revenue sharing among exchanges

**Impact on algos:** SIP is slow (~1ms). Direct feeds from exchanges are faster (~10-100μs). HFT firms use direct feeds for speed advantage.

---

## How Reg NMS Created Modern Market Structure

```
Before Reg NMS (pre-2007):
  NYSE handled ~80% of NYSE-listed volume
  NASDAQ handled ~90% of NASDAQ-listed volume
  Simple, concentrated

After Reg NMS:
  NYSE: ~20% of its listed volume
  NASDAQ: ~15% of its listed volume
  Rest spread across 13+ exchanges + 40+ dark pools + internalizers
  Fragmented, complex, fast
```

**This fragmentation created:**
1. **Smart order routing** — Need to find best price across venues
2. **HFT** — Arbitrage across fragmented venues
3. **Dark pools** — Alternative venues to avoid information leakage
4. **Latency arms race** — Speed matters for cross-venue arbitrage
5. **Rebate arbitrage** — Trading to capture exchange rebates

---

## NBBO and Price Formation

The National Best Bid and Offer:
```
Exchange A:  Bid $50.01 (500 shares)  |  Ask $50.03 (300 shares)
Exchange B:  Bid $50.02 (200 shares)  |  Ask $50.04 (1000 shares)
Exchange C:  Bid $50.00 (1000 shares) |  Ask $50.02 (100 shares)

NBBO:        Bid $50.02 (Exch B)      |  Ask $50.02 (Exch C)
Spread:      $0.00 (locked market) or $50.02 / $50.02
```

---

## Implications for Algo Trading

| Aspect | Implication |
|--------|------------|
| **Order routing** | Must check all venues for NBBO compliance |
| **Latency** | Faster access to quotes = better execution |
| **Fee optimization** | Route to minimize net fees (maker/taker) |
| **Dark pools** | Can get midpoint fills but no price discovery |
| **Market data** | Pay for direct feeds or accept SIP latency |
| **Internalization** | Retail flow often internalized by wholesalers (Citadel, Virtu) |

---

## Related Notes
- [[SEC and FINRA Rules]] — Broader regulatory framework
- [[Regulation and Compliance MOC]] — Parent note
- [[Smart Order Routing]] — Direct consequence of Reg NMS
- [[Execution Venues]] — Market fragmentation
- [[Market Microstructure MOC]] — How Reg NMS shapes microstructure
- [[High-Frequency Trading]] — Enabled by market fragmentation
