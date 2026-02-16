# Pattern Day Trader Rule

FINRA Rule 4210 — affects retail and small prop traders. Institutional desks at JPM/Bloomberg are exempt but you need to understand it.

---

## The Rule

**Pattern Day Trader (PDT):** Any margin account that executes **4 or more day trades within 5 business days**, where day trades represent more than 6% of total trading activity.

**Day trade:** Opening and closing the same position in the same trading day.

**Requirement:** PDT accounts must maintain **minimum equity of $25,000** at all times.

---

## Key Details

| Aspect | Rule |
|--------|------|
| Minimum equity | $25,000 (cash + securities) |
| Account type | Margin accounts only (cash accounts exempt but have settlement rules) |
| Buying power | 4x maintenance margin (intraday) |
| Violation | Account restricted to closing trades for 90 days |
| Applies to | US-regulated broker accounts |

---

## Workarounds (Legal)

1. **Cash account** — No PDT rule, but must wait for settlement (T+1)
2. **Multiple brokers** — 3 day trades per 5 days per broker
3. **Swing trading** — Hold overnight to avoid day trade classification
4. **Futures/Forex** — PDT rule doesn't apply
5. **Offshore broker** — Non-US brokers may not enforce PDT
6. **Prop firm** — Trade with firm capital (no PDT)

---

## Why Institutional Quants Don't Worry About PDT

- PDT applies to **individual accounts** at FINRA-member broker-dealers
- Institutional accounts (hedge funds, bank desks) trade under different rules
- But understanding PDT matters when:
  - Building retail-facing products
  - Managing personal accounts
  - Designing strategies for retail platforms

---

## Related Notes
- [[SEC and FINRA Rules]] — Broader FINRA framework
- [[Regulation and Compliance MOC]] — Parent note
