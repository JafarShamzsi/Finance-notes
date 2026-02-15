# Order Types and Execution

Understanding order types is fundamental — they are the mechanism through which every algorithm interacts with the market.

---

## Basic Order Types

### Market Order
- **Executes immediately** at the best available price
- Guaranteed fill, NOT guaranteed price
- Crosses the [[Bid-Ask Spread]] — you pay the spread
- Used when speed > price (urgent signals)

### Limit Order
- **Sets a maximum buy price or minimum sell price**
- Only fills at your price or better
- NOT guaranteed to fill — may sit in the [[Order Book Dynamics|order book]]
- Provides [[Liquidity]] (maker) vs. taking it (taker)
- Preferred by most algos for cost control

### Stop Order (Stop-Loss)
- Becomes a market order when price hits the stop level
- Used for risk management (see [[Stop Loss Strategies]])
- **Danger:** Slippage in fast markets — stop at $50 might fill at $49.80

### Stop-Limit Order
- Becomes a limit order when stop is triggered
- Controls slippage but risks no fill at all

---

## Advanced Order Types

| Order Type | Description | Use Case |
|---|---|---|
| **Iceberg** | Only shows partial size to the market | Hide large orders (see [[Iceberg Orders]]) |
| **Fill or Kill (FOK)** | Fill entirely immediately or cancel | All-or-nothing needs |
| **Immediate or Cancel (IOC)** | Fill what you can immediately, cancel rest | Partial fills OK |
| **Good Till Cancelled (GTC)** | Stays active until filled or cancelled | Longer-term limit orders |
| **Market on Close (MOC)** | Executes at closing auction price | End-of-day rebalancing |
| **Market on Open (MOO)** | Executes at opening auction price | Opening strategies |
| **Trailing Stop** | Stop level follows price by fixed offset | Lock in profits dynamically |
| **Peg Orders** | Pegged to NBBO mid/bid/ask | Adaptive limit orders |

## Time in Force

| TIF | Meaning |
|---|---|
| **DAY** | Expires at end of trading day |
| **GTC** | Good until cancelled (or 90 days typically) |
| **IOC** | Immediate or cancel |
| **FOK** | Fill or kill |
| **GTD** | Good till specific date |
| **EXT** | Extended hours trading |

## Maker vs Taker

| | Maker | Taker |
|---|---|---|
| Action | Adds liquidity (limit orders) | Removes liquidity (market/aggressive limit) |
| Fees | Lower (often rebates) | Higher |
| Fill certainty | Uncertain | Certain |
| Speed | Slower | Immediate |

Many exchanges use **maker-taker fee models**:
- Maker rebate: -$0.002/share (you get paid)
- Taker fee: +$0.003/share (you pay)
- Net spread to exchange: $0.001/share

This is critical for [[Market Making Strategies]] and [[High-Frequency Trading]].

## Order Routing

Orders can be routed to different venues (see [[Smart Order Routing]]):
- **Primary exchanges** (NYSE, NASDAQ)
- **ECNs** (ARCA, BATS/Cboe)
- **Dark pools** (hidden liquidity)
- **Internalizers** (broker fills from own inventory)

**Reg NMS** (US) requires brokers to route to the **National Best Bid and Offer (NBBO)**.

## Execution Quality Metrics

- **Fill rate** — % of orders that get filled
- **Slippage** — Difference between expected and actual fill price
- **Market impact** — Price movement caused by your order (see [[Market Impact]])
- **Latency** — Time from order decision to fill confirmation

See [[Transaction Cost Analysis]] for comprehensive measurement.

---

## Python Example: Order Types with IBKR API

```python
from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

contract = Stock('AAPL', 'SMART', 'USD')

# Market Order
market_order = MarketOrder('BUY', 100)

# Limit Order
limit_order = LimitOrder('BUY', 100, 150.00)

# Stop Loss
stop_order = StopOrder('SELL', 100, 145.00)

# Trailing Stop (trail by $2)
trail_order = Order()
trail_order.action = 'SELL'
trail_order.totalQuantity = 100
trail_order.orderType = 'TRAIL'
trail_order.auxPrice = 2.0  # $2 trailing amount

trade = ib.placeOrder(contract, limit_order)
```

---

**Related:** [[Order Book Dynamics]] | [[Bid-Ask Spread]] | [[Fees Commissions and Slippage]] | [[Smart Order Routing]] | [[Market Impact]]
