# Regulation and Compliance MOC

> Every quant must understand the rules of the game. Regulatory violations can end careers and firms.

---

## US Regulation

### Securities and Exchange Commission (SEC)
- [[SEC and FINRA Rules]] — Core US equity market regulations
- [[Reg NMS]] — National Market System rules (order protection, access, sub-penny)
- [[Pattern Day Trader Rule]] — PDT rule, $25k minimum for day trading

### Commodity Futures Trading Commission (CFTC)
- Regulates futures, options on futures, swaps
- Dodd-Frank Act — OTC derivatives regulation

---

## European Regulation
- [[MiFID II]] — Markets in Financial Instruments Directive (EU)
- Market Abuse Regulation (MAR) — EU market manipulation rules
- EMIR — European Market Infrastructure Regulation (derivatives)

---

## Market Integrity
- [[Market Manipulation]] — Spoofing, layering, wash trading, front-running
- [[Insider Trading]] — Material non-public information (MNPI)
- Circuit Breakers — LULD (Limit Up-Limit Down), market-wide halts

---

## Algo-Specific Regulation

### Key Requirements for Algorithmic Traders

| Requirement | US | EU (MiFID II) |
|-------------|-----|----------------|
| Registration | SEC/FINRA (broker-dealer) | National regulator |
| Risk controls | SEC Rule 15c3-5 (market access) | RTS 6 (algo requirements) |
| Kill switch | Required | Required |
| Pre-trade risk | Required | Required |
| Testing | Expected | Mandatory (stress testing) |
| Records | 3-6 years | 5 years |
| Reporting | CAT (Consolidated Audit Trail) | Transaction reporting |

### SEC Rule 15c3-5 (Market Access Rule)
Brokers providing market access must implement:
1. **Pre-trade risk controls** — Price, size, position limits
2. **Credit limits** — Aggregate exposure limits
3. **Erroneous order prevention** — Fat finger checks
4. **Kill switch** — Ability to immediately cancel all orders

### MiFID II Algorithm Requirements
1. Algorithms must be tested before deployment
2. Real-time monitoring systems required
3. Kill switch mandatory
4. Annual self-assessment of algo compliance
5. Records of all algorithmic orders for 5 years

---

## Risk Controls Checklist for Algo Trading

```
Pre-Trade:
  ├── Maximum order size check
  ├── Maximum position check
  ├── Price collar check (reject orders far from market)
  ├── Daily loss limit check
  ├── Duplicated order detection
  └── Symbol/venue validation

Real-Time:
  ├── P&L monitoring
  ├── Position tracking
  ├── Execution quality monitoring
  ├── Latency monitoring
  └── Error rate monitoring

Post-Trade:
  ├── Trade reconciliation
  ├── P&L attribution
  ├── TCA (Transaction Cost Analysis)
  ├── Regulatory reporting
  └── Audit trail generation
```

---

## Key Penalties and Cases

| Case | Year | Violation | Penalty |
|------|------|-----------|---------|
| **Knight Capital** | 2012 | Algo malfunction | $440M loss, firm collapsed |
| **Navinder Sarao** | 2015 | Spoofing (Flash Crash) | $38M fine, criminal charges |
| **Tower Research** | 2019 | Spoofing | $67M fine |
| **Citadel Securities** | 2017 | Misleading clients | $22M fine |
| **Deutsche Bank** | 2015 | Spoofing | $30M fine |

---

## Related Areas
- [[Execution MOC]] — Execution regulations and best execution
- [[Market Microstructure MOC]] — Market structure regulations shape microstructure
- [[Risk Management MOC]] — Regulatory risk limits
- [[Infrastructure MOC]] — Compliance infrastructure requirements
