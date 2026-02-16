# SEC and FINRA Rules

The Securities and Exchange Commission (SEC) and Financial Industry Regulatory Authority (FINRA) govern US equity and options markets. Every algo trading in US markets must comply.

---

## SEC — Key Rules for Quants

### Regulation SHO (Short Selling)
- **Locate requirement** — Must locate shares to borrow before shorting
- **Close-out requirement** — FTDs (fails to deliver) must be closed within specific timeframes
- **Uptick rule (Rule 201)** — Circuit breaker: If stock drops 10%+, can only short on uptick for rest of day + next day
- **Threshold securities** — Stocks with large aggregate FTDs get additional restrictions

### Regulation ATS (Alternative Trading Systems)
- Dark pools must register as ATS with SEC
- Fair access requirements above volume thresholds
- Reporting obligations

### Rule 10b-5 (Anti-Fraud)
The catch-all anti-fraud rule:
- Prohibits manipulation, deception in connection with securities trading
- Basis for insider trading prosecution
- Applies to **any** trading strategy that deceives

### Regulation FD (Fair Disclosure)
- Public companies must disclose material info to all investors simultaneously
- Prevents selective disclosure to favored analysts/funds
- Quants using NLP on earnings calls benefit from Reg FD

---

## FINRA — Key Rules

### FINRA Rule 3110 — Supervision
- Firms must supervise all trading activity
- Written supervisory procedures (WSPs) required
- Algo trading requires specific supervisory protocols

### FINRA Rule 5210 — Publication of Transactions
- All trades must be accurately reported
- Time-stamping requirements

### FINRA Rule 6140 — Clearly Erroneous Transactions
- Exchanges can bust trades executed at clearly erroneous prices
- Important for algo risk: a profitable trade can be reversed

### Best Execution (Rule 5310)
- Brokers must seek the best execution for client orders
- Consider: price, speed, likelihood of execution, size, cost
- Relevant for algos routing orders across venues

---

## Consolidated Audit Trail (CAT)
- Tracks every order event (new, modify, cancel, fill) across all US equity/options venues
- Assigns unique customer IDs
- Full lifecycle tracking from order entry to execution
- **Implication for quants:** Every order you send is permanently recorded and can be analyzed for manipulation

---

## Key Concepts for Algo Compliance

### Wash Trading
Buying and selling the same security to create artificial volume. Illegal under Section 9(a)(1) of the Securities Exchange Act.

**Algo risk:** If your algo crosses with itself (e.g., across two accounts), it could be flagged as wash trading.

### Spoofing and Layering
Placing orders you intend to cancel to create false impression of supply/demand. Prohibited under Dodd-Frank Section 747.

**Algo risk:** If your algo places and cancels orders rapidly, ensure there's legitimate intent to trade.

### Front-Running
Trading ahead of a known large order. Illegal for brokers; gray area for prop traders detecting order flow patterns.

---

## Related Notes
- [[Regulation and Compliance MOC]] — Parent note
- [[Reg NMS]] — National Market System rules
- [[Market Manipulation]] — Detailed manipulation types
- [[Pattern Day Trader Rule]] — Day trading regulations
- [[Execution MOC]] — Best execution requirements
