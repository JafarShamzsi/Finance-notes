# Market Manipulation

Market manipulation is any deliberate attempt to interfere with the free and fair operation of the market. Illegal under US (Section 9(a), Rule 10b-5, Dodd-Frank 747) and EU (Market Abuse Regulation) law.

---

## Types of Manipulation Relevant to Algo Trading

### 1. Spoofing
**Placing orders with intent to cancel before execution** to create false impression of supply/demand.

```
Order Book Before Spoof:
  Ask: $50.03 (1000)
  Ask: $50.02 (500)
  Bid: $50.01 (500)     ← Real market
  Bid: $50.00 (300)

Spoofing Attack (wants to buy cheap):
  Ask: $50.03 (1000)
  Ask: $50.02 (500)
  Bid: $50.01 (500)
  Bid: $50.00 (300)
  Bid: $49.99 (50000)   ← SPOOF: huge fake bid
  Bid: $49.98 (50000)   ← SPOOF: more fake bids

Effect: Others see massive buying interest, move asks down
Spoofer: Buys at lower price, cancels fake bids
```

**Legal risk:** Federal crime under Dodd-Frank. Navinder Sarao got criminal charges for spoofing related to the 2010 Flash Crash.

### 2. Layering
Variant of spoofing — placing multiple orders at different price levels to create an artificial ladder of support/resistance.

### 3. Wash Trading
**Trading with yourself** to inflate volume or create artificial price movement.

```
Account A: Sell 1000 shares at $50.00
Account B: Buy 1000 shares at $50.00
Net effect: No real change in position, but volume increases by 1000 shares
```

**Algo risk:** If you run multiple strategies that cross with each other, ensure there's no wash trading. Many firms use pre-trade checks to prevent self-crossing.

### 4. Momentum Ignition
Submitting aggressive orders to trigger a price move, then profiting from the cascade:

1. Buy aggressively to push price up
2. Trigger stop losses and momentum algos that buy more
3. Sell into the artificially inflated price

**Gray area:** Hard to distinguish from legitimate aggressive trading.

### 5. Quote Stuffing
Flooding exchanges with rapid orders and cancellations to:
- Slow down competing algorithms
- Create information asymmetry (your systems handle the load, others don't)
- Exploit SIP delays

**Rarely prosecuted** but considered manipulative by SEC.

### 6. Marking the Close
Executing orders near market close to influence the closing price. Important because:
- ETFs, mutual funds, and derivatives settle at closing price
- Margin calls based on closing price
- Index rebalancing at close

### 7. Front-Running
**Trading ahead of a known large order.** Illegal for brokers (fiduciary duty). For prop traders detecting order flow patterns through market data — legal gray area.

---

## How Surveillance Systems Detect Manipulation

Exchanges and regulators use sophisticated surveillance:

| Pattern | Detection Method |
|---------|-----------------|
| Spoofing | High cancel-to-fill ratio + price impact analysis |
| Layering | Order placement patterns across price levels |
| Wash trading | Cross-referencing accounts, beneficial ownership |
| Momentum ignition | Aggressive order sequence followed by reversal |
| Quote stuffing | Message rate spikes + order lifespan analysis |
| Marking the close | Unusual volume/price action in last minutes |

### FINRA SMARTS / NASDAQ Market Watch
Automated surveillance scanning every order across all US venues. Pattern recognition flags suspicious activity for human review.

---

## Protecting Your Algo from Manipulation Charges

1. **Document intent** — Every strategy should have written documentation of its purpose
2. **Monitor cancel rates** — High cancel-to-fill ratios attract scrutiny
3. **Prevent self-crossing** — Pre-trade checks across all your accounts
4. **Avoid close manipulation** — Be careful with MOC (Market on Close) orders
5. **Audit trail** — Log every decision your algo makes and why
6. **Compliance review** — Have compliance review any new strategy before deployment
7. **Kill switch** — Required by SEC Rule 15c3-5

---

## Related Notes
- [[Regulation and Compliance MOC]] — Parent note
- [[SEC and FINRA Rules]] — Legal framework
- [[MiFID II]] — EU manipulation rules (MAR)
- [[Order Book Dynamics]] — Understanding order book manipulation
- [[High-Frequency Trading]] — HFT and manipulation overlap
